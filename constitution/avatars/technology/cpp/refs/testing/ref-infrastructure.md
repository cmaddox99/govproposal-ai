---
cpp_version_min: 11
cpp_version_note: >-
  Build infrastructure and spdlog require C++11.
avatar: cpp
---

# C++ Avatar Reference: Infrastructure & Operations


---
## Structured Logging and Diagnostics

Per [ENG-6.7](laws/engineering/eng-6-security.md) (Audit Trail) and [ENG-6.4](laws/engineering/eng-6-security.md) (Data Protection), all C++ services must emit structured logs with PII (Personally Identifiable Information) redaction.

### Recommended Framework

Use **spdlog** as the structured logging framework. spdlog integrates with OpenTelemetry for trace-correlated logs and supports JSON output for machine-readable audit trails.

```cpp
#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>

// Initialize with JSON formatter for production
auto logger = spdlog::stdout_color_mt("flight-service");
logger->set_pattern(R"({"time":"%Y-%m-%dT%H:%M:%S.%f","level":"%l","msg":"%v"})");
```

### Log Level Policy

| Level | Usage | Example |
|-------|-------|---------|
| **TRACE** | Detailed debugging (disabled in production) | Function entry/exit, loop iterations |
| **DEBUG** | Diagnostic information (disabled in production) | Variable values, decision branches |
| **INFO** | Normal operational events | Request received, flight booked, cache hit |
| **WARN** | Unexpected but recoverable situations | Retry triggered, fallback used, slow query |
| **ERROR** | Failures requiring attention | Database connection lost, external API timeout |
| **CRITICAL** | System-level failures requiring immediate action | Out of memory, data corruption detected |

### PII Redaction Requirements

Per [ENG-6.4](laws/engineering/eng-6-security.md), PII must NEVER appear in log output. Implement redaction at the logging boundary:

```cpp
// COMPLIANT — PII masked before logging
spdlog::info("Booking confirmed for passenger={} PNR={}",
    mask_name(passenger.name()),   // "J*** D**"
    mask_pnr(booking.pnr()));     // "AB***4"

// NON-COMPLIANT — PII in plaintext logs
spdlog::info("Booking for {} PNR {}", passenger.name(), booking.pnr());
```

### Structured Fields for Audit

Per [ENG-6.7](laws/engineering/eng-6-security.md), audit-relevant log entries must include: `timestamp`, `service`, `action`, `actor`, `outcome`, `trace_id`. Use spdlog's structured logging with OpenTelemetry trace context injection.

---

## Configuration Management

C++ has no standard configuration framework. Select a library based on your configuration complexity:

| Library | Format | When to Use | License |
|---------|--------|-------------|---------|
| **yaml-cpp** | YAML | Complex hierarchical config, Kubernetes-native | MIT |
| **toml++** | TOML | Simple key-value with sections, human-editable | MIT |
| **nlohmann/json** | JSON | API-driven config, service mesh integration | MIT |
| **CLI11** | CLI args | Command-line tools and overrides | BSD-3 |

### Configuration Loading Pattern

```cpp
struct ServiceConfig {
    std::string host = "0.0.0.0";
    uint16_t port = 8080;
    std::string db_connection;
    spdlog::level::level_enum log_level = spdlog::level::info;

    static ServiceConfig load(const std::filesystem::path& path) {
        auto node = YAML::LoadFile(path.string());
        ServiceConfig cfg;
        cfg.host = node["host"].as<std::string>(cfg.host);
        cfg.port = node["port"].as<uint16_t>(cfg.port);
        cfg.db_connection = node["db_connection"].as<std::string>();  // required — throws if missing
        // Validate invariants at load time, not at use time
        if (cfg.port == 0) throw ConfigError{"port must be non-zero"};
        if (cfg.db_connection.empty()) throw ConfigError{"db_connection required"};
        return cfg;
    }
};
```

**Governance:**
- Validate all configuration at startup — fail fast with clear error messages
- Never hardcode connection strings, ports, or secrets — load from config file or environment
- Use environment variable overrides for container deployments: `${DB_HOST:-localhost}`
- Secrets must come from environment variables or a secrets manager, never config files per [ENG-6.1](laws/engineering/eng-6-security.md)

---

## Health Check and Readiness Probes

For Kubernetes and container deployments, C++ services must expose health endpoints per [ENG-7.1](laws/engineering/eng-7-reliability.md) (Failure Handling) and [ENG-7.7](laws/engineering/eng-7-reliability.md) (Health Check Law):

### Liveness Probe

Confirms the process is running and not deadlocked. Should be lightweight — no dependency checks:

```cpp
// GET /health/live → 200 OK (process is alive)
// Implementation: return immediately, no logic
```

### Readiness Probe

Confirms the service can handle requests. Checks downstream dependencies:

```cpp
// GET /health/ready → 200 OK or 503 Service Unavailable
void handle_readiness(HttpResponse& resp) {
    bool db_ok = db_pool_.check_connection();
    bool cache_ok = cache_.ping();

    if (db_ok && cache_ok) {
        resp.set_status(200);
        resp.set_body(R"({"status":"ready","db":"ok","cache":"ok"})");
    } else {
        resp.set_status(503);
        resp.set_body(fmt::format(
            R"({{"status":"not_ready","db":"{}","cache":"{}"}})",
            db_ok ? "ok" : "failed", cache_ok ? "ok" : "failed"));
    }
}
```

### Graceful Shutdown

When Kubernetes sends SIGTERM, the service must:
1. Stop accepting new requests
2. Drain in-flight requests (with timeout)
3. Close database connections and flush logs
4. Exit with code 0

```cpp
std::atomic<bool> shutting_down{false};
std::signal(SIGTERM, [](int) { shutting_down.store(true); });
// In request loop: if (shutting_down) reject new requests with 503
```

> **Governance:** All C++ services deployed to Kubernetes must implement `/health/live` and `/health/ready` endpoints. Services that do not expose HTTP can use a health check file (write a timestamp to `/tmp/healthy` periodically, check with `exec` probe).

---

## License Compliance and Dependency Governance

Per [ENG-6.6](laws/engineering/eng-6-security.md) (Vulnerability Management), all third-party C++ dependencies must be scanned for license compliance and known vulnerabilities.

### License Scanning

Run automated license scanning in CI for every dependency change. Use `scancode-toolkit`, FOSSA, or Snyk to detect license obligations.

**Approved License Allowlist:**

| License | Status | Notes |
|---------|--------|-------|
| MIT | ✅ Approved | Permissive, no restrictions |
| BSD-2-Clause / BSD-3-Clause | ✅ Approved | Permissive, attribution required |
| Apache-2.0 | ✅ Approved | Permissive, patent grant |
| BSL-1.0 (Boost) | ✅ Approved | Permissive |
| Zlib | ✅ Approved | Permissive |
| ISC | ✅ Approved | Permissive |
| LGPL-2.1 / LGPL-3.0 | ⚠️ Review Required | Dynamic linking only; static linking creates distribution obligation |
| GPL-2.0 / GPL-3.0 | ❌ Prohibited (default) | Copyleft — requires architecture review board approval |
| SSPL / Commons Clause | ❌ Prohibited | Non-open-source restrictions |

Any dependency with a license not on this list requires review by the architecture governance team before adoption.

### Boost Module Policy

With C++20 as the minimum standard, many Boost modules have standard library equivalents. Prefer `std::` over Boost when available:

| Boost Module | Std Equivalent (C++17/20/23) | Policy |
|-------------|------------------------------|--------|
| Boost.Optional | `std::optional` | Use std; migrate existing Boost usage |
| Boost.Variant | `std::variant` | Use std; migrate existing Boost usage |
| Boost.Filesystem | `std::filesystem` | Use std; migrate existing Boost usage |
| Boost.Any | `std::any` | Use std; migrate existing Boost usage |
| Boost.Asio | No std equivalent | ✅ Permitted — primary networking library |
| Boost.Beast | No std equivalent | ✅ Permitted — HTTP/WebSocket on Asio |
| Boost.Serialization | No std equivalent | ✅ Permitted with review |
| Boost.Spirit | No std equivalent | ⚠️ Review required — heavy compile-time cost |
| Boost.MPL / Boost.Hana | C++20 concepts + constexpr | Migrate to concepts; new code must not use |

### Header-Only vs Compiled Library Policy

- **Compiled libraries preferred** for any dependency used in more than 3 translation units — avoids parse-time explosion and ODR risk
- **Header-only permitted** for lightweight utilities (e.g., nlohmann-json, fmt in header-only mode) used in few TUs
- **Never** include a header-only library in a public header — it forces all consumers to parse it

### Vendoring Policy

- Vendor only when the library requires AA-specific patches or is unavailable in vcpkg/Conan
- Vendored code must live in a `third_party/` directory with its own `LICENSE` file
- Document upstream version, applied patches, and update procedure
- Vendored libraries are subject to the same CVE scanning as managed dependencies

---

## Tools and Commands

### Build

```bash
# Configure (out-of-source build)
cmake -B build -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --parallel

# Install dependencies (vcpkg)
vcpkg install
```

### Testing

```bash
# Run all tests
ctest --test-dir build --output-on-failure

# Run single test binary
./build/tests/unit/order_service_test --gtest_filter="OrderServiceTest.*"

# Run with coverage
cmake -B build -DCMAKE_BUILD_TYPE=Debug -DENABLE_COVERAGE=ON
cmake --build build && ctest --test-dir build
llvm-cov report ./build/tests/unit/order_service_test
```

### Code Quality

```bash
# Static analysis
clang-tidy src/**/*.cpp -- -std=c++20

# Format
clang-format -i src/**/*.cpp src/**/*.h

# Sanitizers (ASan + UBSan)
cmake -B build -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"
cmake --build build && ctest --test-dir build

# Mutation testing (Mull — requires LLVM/Clang)
mull-runner ./build/tests/unit/order_service_test
```

---

## Skill Parity

All 4 core skills are mandatory for cross-avatar parity with Java/Python/Node avatars:

- `06-atomic-tdd`
- `07-vertical-slice-dev`
- `08-code-review`
- `04-business-domain-modeling`

**Exception:** `skill-04-business-domain-modeling` may be waived only for low-domain-complexity infrastructure repositories with documented governance approval (Q9 decision).

---

## Project Archetypes

Use these archetypes to select the correct libraries, CI gates, and patterns for your C++ project type.

### High Performance Service

Low-latency network service (e.g., pricing engine, real-time data feed).

- **Recommended libs:** Boost.Asio, spdlog, yaml-cpp, nlohmann/json, GoogleTest
- **CI gates:** clang-tidy, ASan, UBSan, TSan, benchmark-regression
- **Patterns:** async I/O, PMR allocators, health check endpoints, graceful shutdown

### Data Pipeline

Batch or streaming data processing (e.g., ETL, analytics).

- **Recommended libs:** Apache Arrow, spdlog, toml++, GoogleTest
- **CI gates:** clang-tidy, ASan, UBSan, benchmark-regression
- **Patterns:** streaming iterators, PMR for throughput, structured logging for lineage

### CLI Tool

Command-line utility or developer tool.

- **Recommended libs:** CLI11, fmt, spdlog, GoogleTest
- **CI gates:** clang-tidy, ASan, UBSan
- **Patterns:** argument parsing, exit codes, stdin/stdout conventions

### Library

Reusable C++ library consumed by other projects.

- **Recommended libs:** GoogleTest, Google Benchmark
- **CI gates:** clang-tidy, ASan, UBSan, ABI compliance check, Doxygen
- **Patterns:** ABI stability, symbol visibility, semantic versioning, PIMPL

---

## Authorities and References

| Authority | Source |
|---|---|
| Language Standard | ISO C++ Standard Committee — [isocpp.org](https://isocpp.org) |
| Core Guidelines | C++ Core Guidelines — Herb Sutter & Bjarne Stroustrup — [isocpp.github.io/CppCoreGuidelines](https://isocpp.github.io/CppCoreGuidelines) |
| Expert Reference | Herb Sutter — Guru of the Week — [gotw.ca](https://gotw.ca) |
| Language Designer | Bjarne Stroustrup — [stroustrup.com/C++](https://stroustrup.com/C++) |
| Living Reference | cppreference.com — community-maintained C++ reference |

---

## See Also

- [Testing & CI Quality](ref-testing-ci.md)
- [Build & Toolchain](ref-build-toolchain.md)

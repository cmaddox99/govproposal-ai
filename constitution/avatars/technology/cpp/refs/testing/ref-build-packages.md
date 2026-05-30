---
cpp_version_min: 11
cpp_version_note: >-
  vcpkg/Conan package management; language-version neutral tooling, C++11 baseline.
avatar: cpp
---

# C++ Avatar Reference: Build Packages and Reproducible Builds

---

## Package Management

Per [ENG-6.6](laws/engineering/eng-6-security.md) (Vulnerability Management), all third-party C++ dependencies must be tracked, scanned for known vulnerabilities, and managed through a reproducible package manager.

**Default:** [vcpkg](https://vcpkg.io/) (manifest mode) — per Q8 stakeholder decision.

**Supported alternative:** [Conan](https://conan.io/) — permitted when project requirements justify it.

### When to Choose Each

| Criteria | vcpkg (default) | Conan |
|----------|----------------|-------|
| CMake integration | Native via `vcpkg.json` + toolchain file | Requires `conan install` + generated CMake files |
| Microsoft ecosystem alignment | Strong (maintained by Microsoft) | Independent |
| Binary caching | Built-in via GitHub Actions / Azure | Built-in via Conan remote servers |
| Custom/internal packages | Overlay ports | Custom recipes in private Conan remote |
| Pre-existing Conan adoption | Migrate or dual-support | Continue using Conan |

**Selection criteria:** Choose Conan over vcpkg only when (a) the project already has mature Conan infrastructure, (b) custom internal packages require Conan recipes, or (c) cross-platform binary distribution needs are better served by Conan's remote model.

### vcpkg Configuration (Default)

Declare dependencies in `vcpkg.json` at the project root:

```json
{
  "name": "my-service",
  "version-string": "1.0.0",
  "dependencies": [
    "gtest",
    "fmt",
    "spdlog",
    "nlohmann-json"
  ]
}
```

Integrate with CMake via the toolchain file:

```bash
cmake -B build -DCMAKE_TOOLCHAIN_FILE=$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
```

### Conan Configuration (Alternative)

When Conan is selected, declare dependencies in `conanfile.txt` or `conanfile.py`:

```ini
# conanfile.txt
[requires]
gtest/1.14.0
fmt/10.2.1
spdlog/1.13.0

[generators]
CMakeDeps
CMakeToolchain
```

Integrate with CMake:

```bash
conan install . --output-folder=build --build=missing
cmake -B build -DCMAKE_TOOLCHAIN_FILE=build/conan_toolchain.cmake
```

---

## Reproducible Builds

Per [ENG-5.1](laws/engineering/eng-5-devops.md) (Infrastructure as Code), C++ builds must be reproducible for regulatory audit. An auditor must be able to reconstruct any deployed binary from source + toolchain.

### Reproducibility Requirements

1. **Pin compiler versions** — specify exact compiler version in CI configuration (e.g., `gcc-13.2.0`, not `gcc-latest`). Document compiler version in build metadata.
2. **Deterministic build flags** — use `SOURCE_DATE_EPOCH` to eliminate timestamps from binaries:

```bash
export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
cmake -B build -DCMAKE_BUILD_TYPE=Release
```

3. **Lock dependency versions** — use vcpkg manifest mode with pinned versions in `vcpkg.json` and a `vcpkg-configuration.json` baseline. Never use floating versions.
4. **Record build environment** — CI must log: compiler version, OS version, CMake version, vcpkg baseline hash, and all build flags. Store as build metadata artifact.
5. **Avoid non-deterministic outputs** — disable `__DATE__`, `__TIME__` macros (use `-Werror=date-time`), use sorted iteration over unordered containers in code generators.

### Audit Trail

Per [ENG-5.1](laws/engineering/eng-5-devops.md), every production build must produce a manifest linking:
- Git commit SHA → source code
- vcpkg baseline → dependency versions
- Compiler version + flags → build configuration
- Binary hash (SHA-256) → deployed artifact

---

## C++20 Modules

C++20 modules (`import`/`export`) replace header-based inclusion for new code. Per [ENG-2.2](laws/engineering/eng-2-architecture.md), module boundaries must align with architectural layers.

> 💡 **Simpler alternative:** Java developers: C++20 modules are conceptually similar to Java's `module-info.java` (Project Jigsaw), but adoption is much earlier. Start with **header units** (`import <string>;`) before attempting full module declarations. Most C++ projects still use traditional `#include` — this is fine and compliant.

### Adoption Policy

| Project Type | Module Policy |
|-------------|---------------|
| Greenfield (C++20+) | Prefer modules for new translation units; headers for C API compatibility |
| Brownfield | Do NOT convert existing headers to modules without a phased migration plan |
| Libraries consumed externally | Provide both module interface and traditional headers during transition |

### Module Governance Rules

1. **Module interface stability** — exported module interfaces follow the same deprecation policy as public headers (per [ENG-2.3](laws/engineering/eng-2-architecture.md)). Removing an exported symbol is a breaking change.
2. **One module per architectural component** — map modules to domain boundaries (`module flight.domain`, `module flight.application`, `module flight.infrastructure`).
3. **No circular module imports** — module dependency graph must be acyclic. Use tooling to enforce.
4. **Build system requirements** — CMake 3.28+ required for module support. Use `target_sources(mylib PUBLIC FILE_SET CXX_MODULES FILES ...)`.

```cpp
// flight_domain.cppm — module interface unit
export module flight.domain;

export class FlightPlan {
    // ... domain entity
};

export class BookingId {
    // ... value object
};
```

### Migration Path from Headers

1. **Phase 1:** Enable module support in CMake (`CMAKE_CXX_STANDARD 20`, CMake 3.28+)
2. **Phase 2:** Create module interface units (`.cppm`) alongside existing headers
3. **Phase 3:** Migrate internal consumers to `import` statements
4. **Phase 4:** Deprecate internal header usage; keep headers for external consumers

---


---

## Source File Organization (SF.xx)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), follow Core Guidelines
SF.xx to keep interfaces clean and headers dependency-minimal.

| Rule | Guidance |
|------|---------|
| SF.1 | Use a consistent file extension: `.cpp`/`.h` (or `.cc`/`.hh`) — pick one, enforce via CI |
| SF.3/4 | Headers declare interfaces; `.cpp` files provide implementations |
| SF.6 | `using` directives only in narrow local scopes (never at namespace level in headers) |
| SF.7 | Never `using namespace std;` in a header — pollutes every TU that includes it |
| SF.8 | Every header has an include guard or `#pragma once` |
| SF.12 | Prefer `#pragma once` over manual guards (less error-prone; widely supported) |

```cpp
// ✅ Compliant header
#pragma once
#include <string_view>

namespace aa::flight {
class Route {
public:
    explicit Route(std::string_view id);
    std::string_view id() const noexcept;
};
} // namespace aa::flight

// ❌ Non-compliant
#include <everything>
using namespace std;  // SF.7 violation — poisons includers
```

C++20 modules replace `#pragma once` long-term; adopt incrementally per SF module roadmap.

## Profiling Before Optimization (Per.xx)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), Per.1 — *Don't optimize
prematurely*; measure first, then optimize the bottleneck the profiler identifies.

| Step | Tool | Guidance |
|------|------|---------|
| 1 — Understand | Code review | Is the algorithm O(n²) when O(n log n) exists? |
| 2 — Measure | `perf stat`/`valgrind --callgrind`/`tracy` | Find the hot path before touching code |
| 3 — Optimize | Targeted change | `std::move` for sinks (Per.10), `reserve()` for vectors |
| 4 — Verify | Re-profile | Confirm improvement; watch for regressions |

```cpp
// Per.10: avoid copies by moving sinks
void FlightQueue::enqueue(FlightPlan plan) {
    queue_.push_back(std::move(plan));  // no copy; plan is a sink parameter
}

// [[likely]]/[[unlikely]] branch prediction hints (C++20 — on the statement body)
if (flight.is_domestic()) [[likely]] {
    handle_domestic(flight);
} else [[unlikely]] {
    handle_international(flight);
}
```

## See Also

- [Build Toolchain Gap - UBSan and MSVC](ref-build-ubsan-msvc.md)

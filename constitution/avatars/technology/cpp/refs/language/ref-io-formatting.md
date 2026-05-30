---
cpp_version_min: 98
cpp_version_note: >-
  Covers the full I/O progression from C++98 printf through C++23 std::print.
  Use the pattern matching your declared project standard. AA standard: spdlog
  for logging in all C++ versions; std::format for in-memory formatting on
  C++20+; fmtlib as polyfill for C++11/14/17.
avatar: cpp
---

# C++ Avatar Reference: I/O and Formatting

> 📌 **All versions.** This reference spans C++98 → C++23. Find the section
> for your project's `cpp.standard` in `.copilot/project.yaml`.

---

## Context

I/O and string formatting touch security, performance, and correctness simultaneously.
Per [ENG-6.1](laws/engineering/eng-6-security.md), format string injection is a
security defect — printf-family functions must never accept a runtime-constructed
format string. Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), I/O code
must be readable and maintainable; raw `sprintf` into fixed buffers is a code smell.

---

## C++98/03: `printf` — Use Only with Literal Format Strings

```cpp
#include <cstdio>

// ✅ SAFE — literal format string; variable data as arguments
printf("Flight %s has %d seats remaining\n", flight_id, seats);
fprintf(stderr, "[ERROR] booking failed: %s\n", error_msg);

// ✅ SAFE — snprintf with explicit bound
char buf[128];
snprintf(buf, sizeof(buf), "FF%06d", loyalty_number);

// ❌ UNSAFE — runtime-constructed format string (CVE vector)
printf(user_message);          // if user_message = "%n", writes to stack
printf(formatted_log.c_str()); // same problem; use printf("%s", ...) instead
```

**Governance rules (per [ENG-6.1](laws/engineering/eng-6-security.md)):**
1. The first argument to `printf`/`fprintf`/`sprintf` must always be a **string literal**
2. Enable `-Wformat -Wformat-security` in all build configurations
3. Use `snprintf` instead of `sprintf` — always with the correct bound
4. Avoid `printf` for new code; prefer `iostream` or spdlog

---

## All Versions: `iostream` — Type-Safe, Verbose

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), prefer `iostream` over `printf`

```cpp
#include <iostream>
#include <sstream>
#include <string>

// Type safety: operator<< dispatch; no format string injection possible
std::cout << "Flight " << flight_id
          << " | seats: " << seats_remaining
          << " | fare: $" << std::fixed << std::setprecision(2) << fare << '\n';

// std::ostringstream for in-process formatting (all versions)
std::ostringstream oss;
oss << "FF" << std::setw(6) << std::setfill('0') << loyalty_number;
std::string formatted = oss.str();

// std::cerr for error output (unbuffered)
std::cerr << "[ERROR] booking failed: " << error_message << '\n';
```

**Tradeoffs:** `iostream` is verbose for formatted output and significantly slower
than printf for high-volume logging. Use `spdlog` for structured logs.

---

## C++11/14/17: fmtlib and spdlog (AA Standard)

fmtlib is the open-source library that became `std::format` in C++20. It is the
**AA standard** for structured logging and in-process formatting in C++11/14/17 projects.

```cpp
#include <fmt/format.h>
#include <fmt/core.h>

// Positional format: {} tokens, type-safe at runtime (FMT_COMPILE = compile-time)
std::string msg = fmt::format(
    "Flight {:>6} | {:3} seats | fare: ${:.2f}",
    flight_id, seats, fare);

// Named arguments (C++11+)
std::string label = fmt::format(
    "origin={origin} dest={dest}",
    fmt::arg("origin", "DFW"), fmt::arg("dest", "ORD"));
```

```cpp
// ── spdlog — AA standard for structured logging (all C++ versions ≥ C++11) ──
#include <spdlog/spdlog.h>

spdlog::info("Booking confirmed: flight={} passenger={} seats={}", "AA100", "SMITH/J", 2);
spdlog::warn("Seat pressure: flight={} booked={} capacity={}", "AA100", 148, 150);
spdlog::error("Booking rejected: flight={} code={}", "AA100", "ERR_OVERSELL");
spdlog::debug("Fare calc: base={:.2f} tax={:.2f} total={:.2f}", 250.0, 21.25, 271.25);

// Structured context (spdlog 1.9+)
auto logger = spdlog::get("booking");
logger->info("Booking attempt", spdlog::details::log_msg());
```

**Governance rules (per [ENG-6.1](laws/engineering/eng-6-security.md) and [ENG-5.5](laws/engineering/eng-5-devops.md)):**
1. Format strings must be string literals — `spdlog::info(runtime_str)` is banned
2. Use `spdlog` for all diagnostic/operational logging in production code
3. Use `fmt::format` (or `std::format` on C++20+) for in-process string construction
4. Never use `std::cout` / `std::cerr` for structured logging — no severity, no correlation

---

## ★ C++20: `std::format`

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) and [ENG-6.1](laws/engineering/eng-6-security.md), `std::format` is preferred over fmtlib on C++20+ projects (compile-time type safety, stdlib dependency only).

```cpp
#include <format>

// Identical syntax to fmtlib — migration is trivial
std::string msg = std::format(
    "Flight {:>6} | {:3} seats | fare: ${:.2f}",
    flight_id, seats, fare);

// Compile-time format string validation
// std::format_string<Args...> enforces correctness at compile time:
void log_booking(std::format_string<const std::string&, int> fmt_str,
                 const std::string& flight, int seats) {
    spdlog::info(std::format(fmt_str, flight, seats));
}
```

---

## ★ C++23: `std::print` / `std::println`

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), `std::print` avoids intermediate `std::string` allocation and is preferred on C++23+ for direct output.

```cpp
#include <print>

// Writes directly to stdout/file without intermediate std::string allocation
std::print("Flight {} departed\n", "AA100");
std::println("Seats remaining: {}", 42);     // println appends '\n' automatically

// Print to stderr
std::print(stderr, "[ERROR] {}\n", error_message);
```

---

## Governance Rules Summary

| Rule | Law | Applies |
|------|-----|---------|
| printf format string must be a literal | [ENG-6.1](laws/engineering/eng-6-security.md) | All versions |
| Enable `-Wformat -Wformat-security` | [ENG-6.1](laws/engineering/eng-6-security.md) | All versions |
| Use spdlog for operational logging | [ENG-5.5](laws/engineering/eng-5-devops.md) | C++11+ |
| No `std::cout`/`cerr` for structured logs | [ENG-3.1](laws/engineering/eng-3-code-quality.md) | All versions |

---

## See Also

- `format-string-safety.md` — per-version code examples with NON-COMPLIANT patterns (see examples/ directory)
- `refs/safety/ref-concurrency-async.md` — async I/O with futures

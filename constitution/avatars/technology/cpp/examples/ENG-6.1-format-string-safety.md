---
law_id: ENG-6.1
cpp_version_min: 98
cpp_version_note: >-
  Covers the full I/O safety progression: printf (C++98/03, security risks),
  iostream (all versions), fmtlib/spdlog (C++11+ polyfill), std::format
  (C++20), std::print (C++23). Use the pattern matching your project standard.
  AA standard: prefer spdlog for logging; std::format for in-memory formatting
  when on C++20+.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — Format String Safety

> ⚠️ **Version-sensitive.** `printf`-family functions have been the source of
> remote code execution vulnerabilities for decades. This file covers the safe
> alternative for every C++ version from C++98 to C++23.

---

## The Security Risk: `printf` Format String Injection

```cpp
// ─── C++98/03/11 NON-COMPLIANT: format string from user input ────────────────
void log_error(const char* user_message) {
    printf(user_message);   // CRITICAL: user_message IS the format string
                            // If user passes "%s%s%s%s%s%n", stack is read/written
}

// ─── C++98/03/11 COMPLIANT: always use a literal format string ───────────────
void log_error_safe(const char* user_message) {
    printf("%s\n", user_message);   // "%s\n" is a fixed literal — safe
}
```

**Why this matters:** CVE databases list hundreds of format string vulnerabilities.
Compilers (`-Wformat`, `-Wformat-security`) warn about `printf(var)` but only if
the build enables these warnings. Per ENG-6.1, format functions must never accept
runtime-constructed format strings.

---

## COMPLIANT (C++98+): `iostream` — Type-Safe by Design

```cpp
#include <iostream>
#include <string>

// iostream uses operator<< dispatch — format string injection is impossible
// because there IS no format string
std::string flight_id = "AA100";
int seats_remaining = 42;

std::cout << "Flight " << flight_id
          << " has " << seats_remaining << " seats\n";

// Error output
std::cerr << "[ERROR] Booking failed for flight " << flight_id << '\n';
```

**Tradeoff:** `iostream` is type-safe but verbose for complex formatting and
significantly slower than `printf` for high-throughput logging. For structured
logging, use spdlog (below).

---

## COMPLIANT (C++11+): fmtlib / spdlog — Recommended for Logging

fmtlib is the reference implementation that became `std::format` in C++20. It is
available as a C++11-compatible library and is the AA-standard logging backend
via spdlog.

```cpp
// ── Direct fmtlib use (C++11+) ───────────────────────────────────────────────
#include <fmt/format.h>
#include <fmt/core.h>

// Positional format strings — type-safe, compile-time checked
std::string msg = fmt::format(
    "Flight {} departed from {} at {:02d}:{:02d}",
    "AA100", "DFW", 14, 35);
// -> "Flight AA100 departed from DFW at 14:35"

// Throws std::format_error at runtime for type mismatches
// with FMT_COMPILE, checks happen at compile time

// ── spdlog (AA standard for structured logging) ──────────────────────────────
#include <spdlog/spdlog.h>

spdlog::info("Flight {} departed: {} seats sold", "AA100", 142);
spdlog::warn("Seat oversell detected on flight {}: {} booked, {} capacity",
             "AA100", 155, 150);
spdlog::error("Booking failed: flight={} passenger={} code={}",
              "AA100", "SMITH/J", "ERR_CAPACITY");
```

**Why compliant:** fmtlib format strings are literal constants checked by the
compiler (`FMT_COMPILE`). Variable data is always passed as arguments — never
as the format string itself.

---

## COMPLIANT (C++20): `std::format`

```cpp
// ★ C++20+ — std::format is fmtlib standardized into the language
#include <format>
#include <string>

// Type-safe, compile-time format string validation
std::string msg = std::format(
    "Flight {:>6} | {:3} seats | Fare: ${:.2f}",
    "AA100", 42, 299.99);
// -> "Flight  AA100 |  42 seats | Fare: $299.99"

// std::format_string<Args...> enforces the format string at compile time
// std::vformat for runtime-constructed format strings (use with caution)
```

```cpp
// ★ C++23 — std::print writes directly without constructing std::string
#include <print>
std::print("Flight {} departed\n", "AA100");  // no intermediate string allocation
```

---

## NON-COMPLIANT: Common Format String Bugs

```cpp
// ── 1: Runtime-constructed format string ─────────────────────────────────────
std::string fmt_str = "Value: " + unit_label + " = %d";  // unit_label from config
printf(fmt_str.c_str(), value);  // UNSAFE if unit_label contains % characters

// ── 2: sprintf into a fixed buffer — classic buffer overflow ─────────────────
char buf[64];
sprintf(buf, "Flight %s seat %d", flight_id.c_str(), seat_num);
// If flight_id is >55 chars, buf overflows into adjacent stack memory

// ── 3: Missing length modifier — 64-bit value truncated ─────────────────────
uint64_t booking_ref = generate_booking_ref();  // may be > INT_MAX
printf("Booking: %d\n", booking_ref);  // WRONG: %d is 32-bit; use %llu or PRIu64

// ── 4: Using cout for structured logging — no severity, no context ────────────
std::cout << "Error: " << msg << std::endl;  // not structured; endl flushes — slow
// Use spdlog::error() instead
```

---

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `snprintf` used instead of `sprintf` | Safer (bounds-checked) but format string injection still possible if format is variable | Always use a literal format string; prefer `std::format` or fmtlib |
| `fmtlib` format string at runtime (`fmt::runtime(s)`) | Opt-in escape hatch; disables compile-time checks | Use only for genuinely dynamic format strings; document the reason |
| `std::format` on MSVC older than VS 2019 16.10 | `<format>` may not be available despite `/std:c++20` | Check `__cpp_lib_format` feature-test macro; fall back to fmtlib |
| Wide character `wprintf`/`wcout` on Windows | Mixed narrow/wide streams corrupt output; `wcout` and `cout` must not be used in the same process without sync | Pick one; prefer narrow UTF-8 throughout; use `spdlog` which handles encoding |
| `std::print` (C++23) not yet widely available | Only GCC 14+, Clang 17+, MSVC VS 2022 17.9+ | Gate with `#if __cpp_lib_print >= 202207L` |

---

## Version Decision Table

| Your `cpp.standard` | Logging | In-Process Formatting |
|---------------------|---------|----------------------|
| 98, 03 | `printf` (literal format only) or `std::cerr` | `sprintf` with bounds check |
| 11, 14, 17 | spdlog (AA standard) | fmtlib `fmt::format` |
| 20 | spdlog or `std::format` to string | `std::format` |
| 23 | spdlog or `std::print` | `std::format` / `std::print` |

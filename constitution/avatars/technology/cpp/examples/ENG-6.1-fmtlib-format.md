---
law_id: ENG-6.1
cpp_version_min: 11
cpp_version_note: >-
  Uses fmtlib/fmt (MIT) for safe string formatting on C++11/14 teams.
  fmtlib IS the reference implementation that became std::format — API
  is identical; migration to C++20 is a namespace/header change only.
avatar: cpp
rag_exclude: true  # placeholder — content pending CBF adoption; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Safe String Formatting — fmtlib Bridge (C++11/14)

**Avatar:** C++ (Transitional C++11/14 — CWR / IOC_ALP)
**Pattern:** Type-safe, injection-free formatting via `fmt::format`

## Context

`sprintf` and `printf`-family functions accept format strings at runtime,
enabling format-string injection attacks and type mismatch undefined behavior.
Per [ENG-6.1](laws/engineering/eng-6-security.md), format strings must be
compile-time constants with type-safe argument binding.

[fmtlib/fmt](https://github.com/fmtlib/fmt) (MIT, Victor Zverovich) is the
reference implementation that became `std::format` in C++20 (P0645). The API
is intentionally identical — migration is a namespace and header substitution.

## COMPLIANT — Basic Formatting

```cpp
// flight_log.cpp  (CWR / IOC_ALP — C++11/14)
#include <fmt/format.h>

// Type-safe; format string verified at compile time against argument types.
std::string format_departure(const std::string& carrier,
                              int               flight_num,
                              int               hour,
                              int               minute)
{
    return fmt::format("{} flight {} departs {:02d}:{:02d}",
                       carrier, flight_num, hour, minute);
    // e.g. "AA flight 100 departs 06:05"
}

// Structured logging with named fields — readable in audit trail.
void log_crew_assignment(const CrewMember& cm, const std::string& flight_id)
{
    fmt::print("[CREW] id={} name={} flight={} base={}\n",
               cm.id, cm.name, flight_id, cm.base_tz);
}
```

## COMPLIANT — Custom fmt::formatter for Domain Type

```cpp
// flight_id.h
#include <fmt/format.h>

struct FlightId {
    std::string carrier;
    int         number;
    std::string suffix;  // e.g. "W" for wet-lease
};

// Teach fmtlib how to format FlightId — participates in all fmt:: calls.
template <>
struct fmt::formatter<FlightId> {
    // Parse format spec (we accept empty spec only).
    constexpr auto parse(fmt::format_parse_context& ctx) { return ctx.begin(); }

    template <typename FormatContext>
    auto format(const FlightId& fid, FormatContext& ctx) const
    {
        if (fid.suffix.empty())
            return fmt::format_to(ctx.out(), "{}{}", fid.carrier, fid.number);
        return fmt::format_to(ctx.out(), "{}{}/{}", fid.carrier, fid.number, fid.suffix);
    }
};

// Usage — FlightId now works anywhere a format argument is accepted.
// fmt::format("Boarding {}", FlightId{"AA", 100, ""})  → "Boarding AA100"
// fmt::format("Boarding {}", FlightId{"AA", 100, "W"}) → "Boarding AA100/W"
```

## COMPLIANT — fmt::format_to with Output Iterator

```cpp
// Efficient: write directly into a pre-allocated buffer — no temporary string.
#include <fmt/format.h>
#include <vector>

std::string build_manifest(const std::vector<FlightId>& legs)
{
    std::string buf;
    buf.reserve(legs.size() * 12);
    for (const auto& leg : legs) {
        fmt::format_to(std::back_inserter(buf), "{} ", leg);
    }
    return buf;
}
```

## NON-COMPLIANT

```cpp
// WRONG 1: sprintf — format string mismatch is undefined behavior at runtime.
// Passing the wrong type (e.g. int where %s expected) silently corrupts the
// stack or crashes.  No compile-time check.
char buf[64];
sprintf(buf, "%s flight %d departs %02d:%02d",
        carrier.c_str(), flight_num, hour, minute);
// ↑ If carrier is passed as int by mistake: UB, stack smash, silent truncation.

// WRONG 2: snprintf with manual size arithmetic — still no type safety,
// easy to get the size calculation wrong leading to truncation bugs in
// audit-log entries (FAR 117 violation if rest-period times are truncated).
snprintf(buf, sizeof(buf) - 1, "flight %d/%d", hour, minute);

// WRONG 3: std::ostringstream — type-safe but verbose and slow; produces
// code that is hard to audit because format intent is scattered across
// chained operator<< calls.  Use fmt::format instead.
std::ostringstream oss;
oss << carrier << " flight " << flight_num
    << " departs " << std::setfill('0') << std::setw(2) << hour
    << ":" << std::setfill('0') << std::setw(2) << minute;
```

## C++20 Migration Note

fmtlib IS the reference implementation for `std::format`. Migration is a
mechanical substitution:

```cpp
// C++11/14 (fmtlib)          →  C++20 (standard library)
#include <fmt/format.h>        →  #include <format>
fmt::format(...)               →  std::format(...)
fmt::format_to(...)            →  std::format_to(...)
fmt::formatter<T>              →  std::formatter<T>   (same parse/format API)
```

The only behavioral difference to verify: `std::format` locale handling
defaults differ slightly from fmtlib in some edge cases — test locale-sensitive
numeric output (`:L` flag) if used.

## Attribution

[fmtlib/fmt](https://github.com/fmtlib/fmt) — MIT license, © Victor Zverovich.
Standardized as `std::format` in C++20 (P0645R10).

## Edge Cases & Warnings

- **Compile-time format string verification:** fmtlib verifies format strings
  at compile time when they are string literals. If you build a format string
  at runtime (e.g. from a config file), use `fmt::vformat` with
  `fmt::make_format_args` — and treat that string as untrusted input,
  validating it before use.

- **`{:02d}` on non-integer types:** Passing a `float` where `{:d}` is
  specified is a compile-time error in fmtlib (correct behavior). In legacy
  `sprintf` code this was silent UB — the fmtlib error surfacing this is a
  feature, not a bug.

- **Buffer size with `fmt::format_to`:** `fmt::format_to` with a raw `char*`
  pointer does not bounds-check. Prefer `std::back_inserter(buf)` into a
  `std::string` or use `fmt::format_to_n` with an explicit limit.

- **`fmt::formatter<T>` thread safety:** `fmt::formatter` instances are
  stateless by convention — `parse()` is called once per format string
  compilation unit, not per call. Do not store mutable state in `formatter`.

- **fmtlib version pinning:** fmtlib v6+ changed the `FMT_STRING` macro and
  constexpr format string checking API. Pin a version in your build system and
  test after upgrades. The C++20 `std::format` API matches fmtlib v8+.

Per [ENG-6.1](laws/engineering/eng-6-security.md): format strings must be
compile-time constants with type-safe binding. `sprintf` with runtime-
constructed format strings is not compliant.

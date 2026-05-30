---
law_id: ENG-6.1
cpp_version_min: 11
cpp_version_note: >-
  Uses HowardHinnant/date (MIT) for timezone-aware arithmetic on C++11/14.
  API is nearly identical to C++20 std::chrono calendar — migration is
  mechanical when C++20 is available.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): FAR 117 Timezone Arithmetic — HowardHinnant/date (C++11/14)

**Avatar:** C++ (Transitional C++11/14 — CWR / IOC_ALP)
**Pattern:** DST-safe crew rest period boundary calculation using `HowardHinnant/date`

## Context

[FAR 117](https://www.ecfr.gov/current/title-14/chapter-I/subchapter-A/part-117)
mandates precise duty-period and rest-period boundary calculations.
Off-by-one-hour errors caused by DST transitions or hardcoded UTC offsets
constitute a regulation violation and create crew-fatigue liability.

For C++11/14 codebases (CWR, IOC_ALP), use
[HowardHinnant/date](https://github.com/HowardHinnant/date) (MIT license, Howard Hinnant).
Its `date::make_zoned` / `date::zoned_time` API is intentionally designed to
match the C++20 `std::chrono` calendar, so migration is mechanical once C++20
is available.

## COMPLIANT

```cpp
// crew_rest_calculator.cpp  (CWR / IOC_ALP — C++11/14)
#include "date/tz.h"   // HowardHinnant/date — MIT license, Howard Hinnant

// Calculate duty-period start in the crew's base timezone.
// tp is a UTC time_point obtained from the flight plan.
date::zoned_time<std::chrono::minutes>
duty_start_local(std::chrono::system_clock::time_point tp,
                 const std::string& base_tz)
{
    // make_zoned converts UTC to the named IANA timezone — DST-safe.
    return date::make_zoned(base_tz, date::floor<std::chrono::minutes>(tp));
}

// Check FAR 117 §117.21 — domestic operations rest requirement (10 hours).
bool has_minimum_rest(std::chrono::system_clock::time_point rest_start_utc,
                      std::chrono::system_clock::time_point rest_end_utc,
                      const std::string& crew_base_tz)
{
    auto start = date::make_zoned(crew_base_tz,
                     date::floor<std::chrono::seconds>(rest_start_utc));
    auto end   = date::make_zoned(crew_base_tz,
                     date::floor<std::chrono::seconds>(rest_end_utc));

    // Arithmetic on zoned_time uses the underlying sys_time (UTC) —
    // DST transitions are accounted for automatically.
    auto rest_duration = end.get_sys_time() - start.get_sys_time();
    return rest_duration >= std::chrono::hours(10);
}
```

**Why this is safe:** `date::make_zoned` loads the IANA timezone database and
applies the correct UTC offset for that exact instant — including DST.
`get_sys_time()` returns the UTC representation, so duration arithmetic is
always correct even across a DST boundary within the rest period.

## NON-COMPLIANT

```cpp
// WRONG 1: time_t / localtime() with manual UTC offset
bool has_minimum_rest_unsafe_v1(time_t rest_start, time_t rest_end)
{
    // localtime() uses the process timezone (TZ env var), not the crew's
    // base timezone.  On a server running UTC, this silently miscalculates
    // every rest period for crews based in US time zones.
    struct tm* tm_start = localtime(&rest_start);  // process TZ — WRONG
    struct tm* tm_end   = localtime(&rest_end);    // shares static buffer!

    double hours = difftime(rest_end, rest_start) / 3600.0;
    return hours >= 10.0;  // off by 1 h on DST transition nights
}

// WRONG 2: hardcoded UTC offset string
bool has_minimum_rest_unsafe_v2(time_t rest_start, time_t rest_end,
                                 int utc_offset_hours)
{
    // Hardcoded offset is wrong for half the year (DST) — e.g. Chicago is
    // UTC-6 in winter but UTC-5 in summer.  A flight scheduled in January
    // but operated in March will apply the wrong offset.
    time_t adjusted_start = rest_start + utc_offset_hours * 3600;
    time_t adjusted_end   = rest_end   + utc_offset_hours * 3600;
    return difftime(adjusted_end, adjusted_start) / 3600.0 >= 10.0;
}
```

**Why these are unsafe:**
- `localtime()` uses the server's `TZ` environment variable, not the crew base.
- `localtime()` writes to a static buffer — two calls in the same expression
  or thread share memory.
- Hardcoded UTC offset strings (e.g., `"-06:00"`) are wrong for the DST half
  of the year for every US crew base.

## C++20 Migration Note

When upgrading to C++20, replace `date::` with `std::chrono::`:

```cpp
// C++20 equivalent — drop-in replacement
#include <chrono>

auto duty_start_c20 =
    std::chrono::zoned_time<std::chrono::minutes>(
        crew_base_tz,
        std::chrono::floor<std::chrono::minutes>(tp));
```

The type names and constructor signatures are deliberately identical.
Migration is a namespace substitution plus removing the `"date/tz.h"` include.

## Attribution

[HowardHinnant/date](https://github.com/HowardHinnant/date) — MIT license,
© Howard Hinnant. Incorporated into C++20 as `std::chrono` calendar extensions
(P0355R7). IANA timezone database update script included.

## Edge Cases & Warnings

- **DST transition day (spring-forward / fall-back):** When a crew rest period
  spans a DST transition, the wall-clock duration differs from the elapsed time
  by exactly 1 hour. `get_sys_time()` arithmetic is always correct because it
  operates in UTC. Do not use `get_local_time()` for duration arithmetic — it
  will over- or under-count by 1 hour on transition nights.

- **Leap seconds:** `std::chrono::system_clock` (and therefore
  `date::sys_time`) follows the POSIX convention of ignoring leap seconds —
  a day is always 86,400 seconds. This matches FAA/OPS scheduling tools. If
  you need true UTC with leap-second awareness, use
  `date::utc_clock` / `date::utc_time`.

- **`zoned_time` vs `local_time` confusion:** `date::local_time` is an
  unanchored wall-clock reading (no timezone attached). Subtracting two
  `local_time` values across a DST transition gives the wrong duration.
  Always use `zoned_time::get_sys_time()` for elapsed-time calculations.

- **`localtime()` static buffer:** `localtime()` returns a pointer to a
  process-global `struct tm`. On MSVC, `localtime_s()` is the safe variant;
  on POSIX, use `localtime_r()`. Neither is a correct substitute for
  timezone-aware arithmetic — they still use the process `TZ`, not the crew
  base timezone.

- **IANA database currency:** HowardHinnant/date ships a `tzdata` update
  script. DST rules change (e.g., US Energy Policy Act 2005 moved DST
  boundaries). Pin a tzdata version in your build and update it with OS
  patches.

Per [ENG-6.1](laws/engineering/eng-6-security.md): safety-critical
calculations — including FAR 117 crew rest boundaries — must use
timezone-aware libraries. `time_t`/`localtime()` with manual offset is not
compliant.

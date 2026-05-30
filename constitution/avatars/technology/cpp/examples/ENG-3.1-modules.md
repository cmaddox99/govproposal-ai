---
law_id: ENG-3.1
cpp_version_min: 20
cpp_version_note: >-
  C++20 modules require a C++20 compiler and CMake 3.28+ (FILE_SET CXX_MODULES).
  For older projects, use traditional header includes.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): C++20 Modules

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), C++20 modules eliminate
include-order dependencies, reduce parse overhead, and improve build isolation.

## COMPLIANT: Named Module with Partition

**Module interface** (`aa/flight/domain.cppm`):
```cpp
export module aa.flight:domain;   // partition declaration

export struct FlightId { int value; };
export struct FlightLeg { FlightId id; int duration_min; bool is_active; };
```

**Primary module** (`aa/flight.cppm`):
```cpp
export module aa.flight;
export import :domain;            // re-export partition
```

**Consumer** (`booking.cpp`):
```cpp
import aa.flight;                 // ✅ single import, no header order issues
void book(FlightLeg leg) { /* uses FlightId, FlightLeg */ }
```

**CMake 3.28+**:
```cmake
target_sources(aa_flight
  PUBLIC FILE_SET CXX_MODULES FILES
    aa/flight.cppm
    aa/flight/domain.cppm
)
```

## NON-COMPLIANT: Include Cycle

```cpp
// flight_leg.h
#include "flight_id.h"   // ❌ if flight_id.h ever includes flight_leg.h
                         //    — circular dependency, order-sensitive builds
```
Modules break cycles: each module interface is parsed once regardless of import order.

## Edge Cases

### Legacy Header Units

Standard-library headers can be imported as header units where vendor support exists:

```cpp
import <vector>;   // header unit — implementation quality varies; prefer
                   // import std; (C++23) or keep #include <vector> in a
                   // global module fragment for portability
```

Use a **global module fragment** to mix legacy headers safely:

```cpp
module;            // global module fragment — macros visible here only
#include <cassert>

export module aa.flight:domain;   // named module begins here
```

### Mixing Modules with Traditional Headers

- `#include` inside a named module (after `export module`) is **not allowed**.
- Put all `#include` directives before the `module;` line in the global module fragment.
- Never `export` a macro — modules do not export preprocessor symbols.

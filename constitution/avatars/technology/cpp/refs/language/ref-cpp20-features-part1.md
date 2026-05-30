---
id: ref-cpp20-features-part1
cpp_version_min: 20
cpp_version_note: >-
  C++20 features Part 1: C++20 Modules, std::span, std::ranges/views,
  spaceship operator (operator<=>). Requires C++20 compiler support.
  See Part 2 for coroutine generators and calendar/timezone.
  See Part 3 for std::format, std::bit_cast, source_location, constinit, atomic_ref.
avatar: cpp
---

# C++20 Core Features — Part 1

> **Status:** Complete — all sections populated as part of the C++ External Sources Enrichment (ESE) proposal.

Per [ENG-2.2](laws/engineering/eng-2-architecture.md) (Architecture Law), all C++20
features must be introduced with governing context and migration guidance.

---

## C++20 Modules

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity) and
[ENG-2.2](laws/engineering/eng-2-architecture.md) (Architecture), modules replace
`#include` cycles with explicit, ordered interface declarations. Adopt in new
C++20 translation units; do **not** force onto brownfield code unless modernising a
whole subsystem.

### Module Interface Unit

```cpp
// COMPLIANT — module interface unit for AA flight domain
// File: aa.flight.cppm  (or .ixx on MSVC)
export module aa.flight;          // module declaration

import <string>;                  // header unit import
import <vector>;

export namespace aa {
    struct FlightId {
        std::string carrier;      // e.g. "AA"
        int         number;       // e.g. 1234
    };

    export class FlightRoster {
    public:
        void add(FlightId id);
        std::vector<FlightId> all() const;
    private:
        std::vector<FlightId> flights_;
    };
}
```

```cpp
// NON-COMPLIANT — legacy header in a module-adopting translation unit
// roster.h (included everywhere)
#pragma once
#include <vector>
// ❌ macros and internal details leak to all includers; no dependency isolation
struct FlightRoster { /* ... */ };
```

### Module Partitions

Large modules may be split with the `module M:Part` syntax:

```cpp
// COMPLIANT — partition: aa.flight:domain
// File: aa.flight-domain.cppm
export module aa.flight:domain;   // partition declaration

export namespace aa {
    enum class CabinClass { First, Business, Economy };
}

// COMPLIANT — primary module re-exports the partition
// File: aa.flight.cppm
export module aa.flight;
export import :domain;            // re-export partition
```

### Global Module Fragment

Use `module;` before the module declaration to include legacy headers that must not
be part of the module interface:

```cpp
// COMPLIANT — global module fragment isolates legacy macros
module;                           // global module fragment begins
#include <cstdint>                // ✅ macros stay in GMF, not exported
#include "legacy_iata_codes.h"   // ✅ C-style header isolated here

export module aa.codes;
export namespace aa {
    inline constexpr uint16_t MAX_ROUTE_LENGTH = 8;
}
```

### Header Units vs. Module Interfaces

| Mechanism | When to use | Trade-off |
|---|---|---|
| `import <vector>;` (header unit) | Migrating headers incrementally | Compiler pre-processes header; still ODR-constrained |
| `export module M;` (module interface) | New subsystems in C++20 codebase | Clean isolation; requires compiler/CMake support |
| `#include` | C++17 and below; third-party headers not yet wrapped | No isolation; macro leakage |

### CMake Wiring (C++20 Modules)

```cmake
# COMPLIANT — CMake 3.28+ FILE_SET CXX_MODULES
target_sources(aa_flight
    PRIVATE
        FILE_SET CXX_MODULES FILES
            src/aa.flight.cppm
            src/aa.flight-domain.cppm
)
target_compile_features(aa_flight PUBLIC cxx_std_20)

# NON-COMPLIANT — treating module files as regular sources
# target_sources(aa_flight PRIVATE src/aa.flight.cppm)  # ❌ no CXX_MODULES tag
```

**C++ Core Guidelines:** SF.11 (avoid header file cycles), SF.12 (prefer modules).

---

## Ranges and Views

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity), ranged algorithms
and lazy view pipelines replace raw loops with intent-revealing, composable expressions.
Cite: Core Guidelines ES.1 (prefer standard library), P.3 (express intent).

### Ranged Algorithms vs. Iterator Pairs

```cpp
// COMPLIANT — std::ranges::sort: no begin/end boilerplate
std::vector<FlightLeg> legs = get_legs();
std::ranges::sort(legs, {}, &FlightLeg::departure_time);  // projection sort

// NON-COMPLIANT — iterator-pair sort obscures intent
std::sort(legs.begin(), legs.end(),
          [](const FlightLeg& a, const FlightLeg& b){
              return a.departure_time < b.departure_time;
          });  // ❌ range boundary noise; no projection
```

### Lazy View Pipeline

Views are **lazy** — they do not allocate or compute until iterated. Chain with `|`:

```cpp
// COMPLIANT — pipeline over span<const FlightLeg>; zero allocation
auto active_long_haul(std::span<const FlightLeg> legs) {
    return legs
        | std::views::filter([](const FlightLeg& l){ return l.is_active; })
        | std::views::filter([](const FlightLeg& l){ return l.duration_min > 180; })
        | std::views::transform([](const FlightLeg& l){ return l.flight_id; });
    // Lazy: evaluated only when the caller iterates the returned view
}
// ⚠️ Edge Case — Lazy view lifetime: The returned view references the input span's
// data. Ensure the owning container outlives all iteration — destroying it before
// iteration completes is UB. Either iterate immediately or hold both together:
//   std::vector<FlightLeg> legs = get_legs();
//   for (auto id : active_long_haul(legs)) { ... }  // ✅ legs outlives view

// NON-COMPLIANT — eager intermediate vectors waste heap
std::vector<FlightLeg> active;
for (const auto& l : legs)
    if (l.is_active) active.push_back(l);         // ❌ heap allocation
std::vector<FlightLeg> long_haul;
for (const auto& l : active)
    if (l.duration_min > 180) long_haul.push_back(l);  // ❌ second allocation
```

### Materializing a View

When you need an owned container, use `std::ranges::to` (C++23) or the two-step
`begin`/`end` construction with a range constructor:

```cpp
// C++23 — direct materialisation
auto ids = active_long_haul(legs) | std::ranges::to<std::vector>();

// C++20 fallback — explicit construction
auto rng = active_long_haul(legs);
std::vector<FlightId> ids(rng.begin(), rng.end());
```

### Sentinel Types and Bounded vs. Unbounded Ranges

| Range kind | Sentinel | Use case |
|---|---|---|
| Bounded (`std::span`, `std::vector`) | Same type as iterator | Most AA domain ranges |
| Null-terminated C-string (`const char*`) | `std::default_sentinel_t` | C-string interop via `std::views::take_while` |
| Unbounded (`std::views::iota(0)`) | Divergent sentinel | Never on safety-critical paths |

**Governance rule ([ENG-6.1](laws/engineering/eng-6-security.md)):** Unbounded ranges must
not appear on paths that process passenger or safety data — always apply `views::take` to
impose a finite bound.

---

## std::span Governance

`std::span<T>` is a **non-owning view** over a contiguous sequence — it carries a pointer
and a size but owns neither. Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security)
and Core Guidelines I.12 / P.6, span replaces the unsafe `T* data, size_t len` pattern
in all new APIs.

### Replacing Pointer + Count

```cpp
// COMPLIANT — std::span<const SeatData> is self-bounded; no separate size
void assign_seats(std::span<const SeatData> seats, CabinClass cabin) {
    for (const auto& seat : seats)           // ✅ range-for; no index arithmetic
        process(seat, cabin);
}

// COMPLIANT — caller: implicit construction from vector or array
std::vector<SeatData> row = load_row(3);
assign_seats(row, CabinClass::Economy);      // ✅ implicit span construction

// NON-COMPLIANT — pointer + size: caller can pass mismatched len
void assign_seats(const SeatData* data, size_t len, CabinClass cabin); // ❌
```

### Read-Only APIs with `std::span<const T>`

```cpp
// COMPLIANT — const span prevents mutation; no copy
std::string_view first_destination(std::span<const FlightLeg> legs) {
    if (legs.empty()) return {};
    return legs.front().destination;
}

// NON-COMPLIANT — const ref to vector ties caller to vector ownership model
std::string_view first_destination(const std::vector<FlightLeg>& legs); // ❌
```

### Subspan Patterns

```cpp
// COMPLIANT — subspan for a slice of seats without allocation
auto window_seats(std::span<const SeatData> row) {
    // window seats are last 2 per row in AA narrowbody config
    return row.last(2);                      // ✅ std::span::last(n)
}

// COMPLIANT — subspan from offset
auto tail = seats.subspan(offset, count);    // ✅ [offset, offset+count)
```

### Bounds Checking

`span::operator[]` is **unchecked** (UB on out-of-bounds). Use explicit guards:

```cpp
// COMPLIANT — guarded access
if (idx < seats.size())
    process(seats[idx]);

// NON-COMPLIANT — unchecked index into span
process(seats[idx]);  // ❌ UB if idx >= seats.size()
```

### Span vs. Other Views

| Type | Owns data? | Contiguous? | Use when |
|---|---|---|---|
| `std::span<T>` | ❌ | ✅ | Pass arrays/vectors without copy |
| `std::string_view` | ❌ | ✅ | Read-only string access |
| `std::ranges::subrange` | ❌ | ❌ | Non-contiguous iterator ranges |
| `std::vector<T>` | ✅ | ✅ | Ownership required |

**Core Guidelines:** I.12 (declare not-null pointers), P.6 (bounds checkable at runtime).

---

## Three-way Comparison (Spaceship Operator)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity) and
[ENG-3.2](laws/engineering/eng-3-code-quality.md) (Immutability), C++20's `operator<=>`
eliminates hand-rolled comparison boilerplate for value types. Core Guidelines C.11
(make concrete types regular).

### Ordering Categories

| Category | When to use | Example |
|---|---|---|
| `std::strong_ordering` | All equal-valued objects are identical | `FlightId`, integer IDs |
| `std::weak_ordering` | Equal-valued objects may differ in non-observable ways | Case-insensitive strings |
| `std::partial_ordering` | Comparison may be undefined (NaN-equivalent) | `FlightAltitude` with UNKNOWN sentinel |

### Defaulted Operator (Most Value Types)

```cpp
// COMPLIANT — one defaulted <=> generates all six comparison operators
struct FlightId {
    std::string carrier;   // "AA"
    int         number;    // 1234

    auto operator<=>(const FlightId&) const = default;
    // operator== is also synthesised from <=>
};

// Usage: all comparisons work without any extra code
FlightId a{"AA", 100}, b{"AA", 200};
assert(a < b);
assert(a != b);

// NON-COMPLIANT — six hand-rolled operators; all must stay in sync
bool operator<(const FlightId& a, const FlightId& b) {  // ❌
    if (a.carrier != b.carrier) return a.carrier < b.carrier;
    return a.number < b.number;
}
// ... and operator>, operator<=, operator>=, operator==, operator!= — 5 more
```

### Custom Ordering with partial_ordering

```cpp
// COMPLIANT — partial_ordering for altitude with UNKNOWN sentinel
struct FlightAltitude {
    int feet;                           // -1 = UNKNOWN
    bool is_known() const { return feet >= 0; }

    std::partial_ordering operator<=>(const FlightAltitude& o) const {
        if (!is_known() || !o.is_known())
            return std::partial_ordering::unordered;  // ✅ NaN-equivalent
        return feet <=> o.feet;
    }
    bool operator==(const FlightAltitude& o) const = default;
};
```

### Interaction with `operator==`

When `operator<=>` is **defaulted**, `operator==` is synthesised automatically.
When `operator<=>` is **user-defined**, `operator==` must be declared separately:

```cpp
// COMPLIANT — user-defined <=> requires explicit ==
struct RouteKey {
    std::string origin, destination;

    std::strong_ordering operator<=>(const RouteKey& o) const {
        // custom ordering: destination-first for routing table locality
        if (auto c = destination <=> o.destination; c != 0) return c;
        return origin <=> o.origin;
    }
    bool operator==(const RouteKey&) const = default;  // ✅ must be explicit
};
```

### Migration from Manual Comparisons

| Legacy pattern | C++20 replacement |
|---|---|
| 6 `operator<`, `>`, `<=`, `>=`, `==`, `!=` free functions | `auto operator<=>(...) const = default` |
| `std::tie(a,b) < std::tie(o.a,o.b)` | `auto operator<=>(...) const = default` |
| Custom `compare()` returning int | `operator<=>` returning ordering category |

**Core Guidelines:** C.11 (make concrete types regular).

---

## Further Reading

> Further reading: Josuttis, *C++20 — The Complete Guide* (2022) — ranges, concepts, modules,
> `std::format`, `std::span`, and three-way comparison in depth.

> Further reading: Stroustrup, *TC++PL* 4th Ed. (2013) §2–3 — language design rationale for
> features that evolved into C++20.

> ISO/IEC 14882:2020 working draft: https://eel.is/c++draft/ — authoritative normative reference
> for all C++20 features covered in this file.

---

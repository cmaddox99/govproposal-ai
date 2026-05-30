---
law_id: ENG-3.1
cpp_version_min: 20
cpp_version_note: >-
  std::ranges and std::views require C++20. For C++11/14 projects, see
  ENG-3.1-ranges-range-v3.md (range-v3 bridge library).
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): `std::ranges` and `std::views` (C++20)

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), prefer lazy view pipelines over
manual loops. Views are non-owning and allocate nothing until iterated.

## COMPLIANT: Lazy Views Pipeline over Flight Legs

```cpp
#include <ranges>
#include <span>

// Zero heap allocation; stops at first successful booking
auto long_haul_ids(std::span<const FlightLeg> legs) {
    return legs
        | std::views::filter([](const FlightLeg& l){ return l.is_active; })
        | std::views::filter([](const FlightLeg& l){ return l.duration_min > 180; })
        | std::views::transform([](const FlightLeg& l){ return l.flight_id; });
}

for (const FlightId& id : long_haul_ids(roster))
    if (book(id)) break;  // ✅ remaining legs never evaluated
```

## NON-COMPLIANT: Eager Intermediate Vectors

```cpp
// Two heap allocations before any booking attempt
std::vector<FlightLeg> active;
for (const auto& l : legs)
    if (l.is_active) active.push_back(l);              // ❌ allocation 1

std::vector<FlightId> ids;
for (const auto& l : active)
    if (l.duration_min > 180) ids.push_back(l.flight_id); // ❌ allocation 2
```

## Edge Cases

### Infinite / Unbounded Ranges

`std::views::iota` is unbounded. Always bound with `views::take` per
[ENG-6.1](laws/engineering/eng-6-security.md):

```cpp
auto first_ten = std::views::iota(0) | std::views::take(10); // ✅

for (int i : std::views::iota(0)) { /* ❌ infinite loop if no break */ }
```

### Dangling View from Temporary

Views hold a **pointer** to the source range — a view over a temporary is immediately
dangling:

```cpp
// NON-COMPLIANT — get_legs() temporary destroyed before view is iterated
auto v = get_legs() | std::views::filter(is_active);  // ❌ dangling
for (auto& l : v) { /* UB */ }

// COMPLIANT — named container extends lifetime
auto legs = get_legs();
auto v    = legs | std::views::filter(is_active);     // ✅
```

### Owning vs. Non-Owning

Accept `std::span<const T>` in view-producing functions; never store a view beyond
the lifetime of its source range.

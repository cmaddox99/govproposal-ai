---
law_id: ENG-3.1
cpp_version_min: 98
cpp_version_note: >-
  Covers the full comparison operator progression: C++98/03 manual
  6-operator pattern, C++11 std::tie idiom for lexicographic ordering,
  and C++20 operator<=> (spaceship). Choose the pattern matching your
  declared project standard. Never silently use C++20 syntax on C++14 teams.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): Code Quality — Comparison Operators

> ⚠️ **Version-sensitive.** This is one of the most common areas where AI tools give
> C++20 guidance to C++14/17 teams. Check `cpp.standard` in `.copilot/project.yaml`
> before applying any pattern here.

---

## COMPLIANT (C++98/11/14): Manual 6-Operator Pattern

For code that cannot use C++20, all six comparison operators must be implemented
consistently or derived from `operator==` and `operator<`:

```cpp
// C++98/11/14 — implement all 6 operators (or derive 4 from == and <)
class FlightSegment {
    std::string origin_;
    std::string destination_;
    int depart_time_;  // minutes since midnight

public:
    FlightSegment(std::string o, std::string d, int t)
        : origin_(std::move(o)), destination_(std::move(d)), depart_time_(t) {}

    // Core operators — define these two
    bool operator==(const FlightSegment& rhs) const {
        return origin_ == rhs.origin_
            && destination_ == rhs.destination_
            && depart_time_ == rhs.depart_time_;
    }

    bool operator<(const FlightSegment& rhs) const {
        // std::tie idiom (C++11): lexicographic compare with no manual chaining
        return std::tie(origin_, destination_, depart_time_)
             < std::tie(rhs.origin_, rhs.destination_, rhs.depart_time_);
    }

    // Derived operators — implement from == and < (C++98 compatible)
    bool operator!=(const FlightSegment& rhs) const { return !(*this == rhs); }
    bool operator> (const FlightSegment& rhs) const { return rhs < *this; }
    bool operator<=(const FlightSegment& rhs) const { return !(rhs < *this); }
    bool operator>=(const FlightSegment& rhs) const { return !(*this < rhs); }
};
```

**Why compliant:** `std::tie` (C++11) eliminates the error-prone chained `if/else`
comparison pattern. The derived operators guarantee all six are consistent — a class
that defines only `operator<` but not `operator>` is a correctness trap.

---

## COMPLIANT (C++11/14): `std::rel_ops` — Use Sparingly

```cpp
#include <utility>    // std::rel_ops
using namespace std::rel_ops;  // generates !=, >, <=, >= from == and <

// Only operator== and operator< need to be defined
// std::rel_ops provides the rest via ADL
```

**Caution:** `std::rel_ops` is deprecated in C++20. It also applies to ALL types in
scope, which can cause unexpected overload resolution. Prefer the explicit 6-operator
pattern or Boost.Operators for libraries.

---

## COMPLIANT (C++20+): Spaceship Operator `<=>`

```cpp
#include <compare>

// ★ C++20+ only — compile guard required for mixed-standard codebases
class FlightSegment {
    std::string origin_;
    std::string destination_;
    int depart_time_;
public:
    // Single declaration generates all 6 comparison operators
    auto operator<=>(const FlightSegment&) const = default;

    // Note: defaulted <=> also generates operator== in C++20
    // No need to write operator== separately
};

// Usage — all comparisons work
FlightSegment a{"DFW", "ORD", 480};
FlightSegment b{"DFW", "ORD", 720};
assert(a < b);   // true — earlier departure
assert(a != b);  // true — generated from <=>
```

**Why preferred (C++20+):** `= default` generates correct, consistent operators with
no manual code. Compiler verifies member ordering. Refactoring-safe — adding a field
automatically updates all comparisons.

```cpp
// ★ C++20+ — custom ordering when default member-wise order is wrong
class PriorityFlight {
    int priority_;          // sort descending by priority
    std::string flight_id_;
public:
    std::strong_ordering operator<=>(const PriorityFlight& rhs) const {
        if (auto cmp = rhs.priority_ <=> priority_; cmp != 0) return cmp;  // reversed
        return flight_id_ <=> rhs.flight_id_;
    }
    bool operator==(const PriorityFlight& rhs) const = default;
};
```

---

## NON-COMPLIANT: Inconsistent or Incomplete Operators

```cpp
class Booking {
    int id_;
    double fare_;
public:
    // BUG: operator< uses id_ but operator== uses fare_
    // Breaks any container (std::set, std::map) and std::sort
    bool operator<(const Booking& rhs) const { return id_ < rhs.id_; }
    bool operator==(const Booking& rhs) const { return fare_ == rhs.fare_; }

    // MISSING: !=, >, <=, >= — calling code may fail to compile with STL
};
```

**Why non-compliant:** `std::set<Booking>` uses `operator<` for ordering but a
separate `operator==` for equality — if they use different fields, the container
silently stores duplicates. Missing operators cause compilation failures in standard
algorithm calls.

---

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| C++20 `<=>` on a C++14/17 team | `<compare>` header absent; code doesn't compile | Add `#if __cplusplus >= 202002L` guard or use 6-operator pattern |
| Mixing `float`/`double` members with `<=>` | Floating-point NaN causes `partial_ordering`; `= default` may not compile | Use `std::partial_ordering` explicitly or avoid float members in comparison |
| `= default` spaceship with a pointer member | Compares pointer addresses, not pointed-to values | Write a custom `<=>` that dereferences |
| `std::tie` with `const` member references | `std::tie` stores references — safe only for temporary compare, not storage | Use only in `operator<` body; never store the result |
| Forgetting `operator==` alongside custom `<=>` | C++20: custom `<=>` does NOT automatically generate `==` | Always define `operator==` separately when writing custom `<=>` |

---

## Version Decision Table

| Your `cpp.standard` | Use This Pattern |
|---------------------|-----------------|
| 98, 03, 11, 14 | Manual 6-operator with `std::tie` for `operator<` |
| 17 | Manual 6-operator (spaceship not available); consider Boost.Operators |
| 20, 23 | `operator<=> = default` (or custom for non-default ordering) |

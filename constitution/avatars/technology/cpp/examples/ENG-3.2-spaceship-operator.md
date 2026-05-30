---
law_id: ENG-3.2
cpp_version_min: 20
cpp_version_note: >-
  The three-way comparison operator (operator<=>) requires C++20.
  For C++11/14 projects, all six comparison operators must be hand-rolled.
avatar: cpp
---

# [ENG-3.2](laws/engineering/eng-3-code-quality.md): Spaceship Operator `<=>` (C++20)

Per [ENG-3.2](laws/engineering/eng-3-code-quality.md), use defaulted `<=>` for
value types. Custom ordering only when domain semantics require it.

## COMPLIANT: Defaulted `<=>` for `FlightId`

```cpp
#include <compare>

struct FlightId {
    int value;
    auto operator<=>(const FlightId&) const = default; // ✅ all 6 ops generated
    bool operator==(const FlightId&)  const = default;
};

// Usage — all comparison operators available
FlightId a{100}, b{200};
assert(a < b);   // ✅
assert(a != b);  // ✅
```

## COMPLIANT: Custom `partial_ordering` with UNKNOWN Sentinel

When a type has an unordered state (like `NaN` in floating-point), return
`partial_ordering::unordered`:

```cpp
struct FlightAltitude {
    int feet;
    bool valid;

    std::partial_ordering operator<=>(const FlightAltitude& o) const noexcept {
        if (!valid || !o.valid)
            return std::partial_ordering::unordered; // ✅ UNKNOWN sentinel
        return feet <=> o.feet;
    }
    bool operator==(const FlightAltitude& o) const noexcept {
        // Explicit == required: <=> would make unordered==unordered true;
        // we want UNKNOWN altitudes to compare unequal (valid && valid check).
        return valid && o.valid && feet == o.feet;
    }
};
```

## NON-COMPLIANT: Hand-Rolling Six Operators

```cpp
// ❌ 6 operators — any inconsistency is a silent bug
bool operator< (const FlightId& o) const { return value < o.value; }
bool operator> (const FlightId& o) const { return value > o.value; }
bool operator<=(const FlightId& o) const { return value <= o.value; }
bool operator>=(const FlightId& o) const { return value >= o.value; }
bool operator==(const FlightId& o) const { return value == o.value; }
bool operator!=(const FlightId& o) const { return value != o.value; }
```

## Edge Cases

### `partial_ordering` Comparisons Are Three-Valued

```cpp
auto r = a <=> b;
if (r == std::partial_ordering::unordered) { /* neither a<b nor a>=b */ }
```
A sort using `partial_ordering` on a range containing UNKNOWN sentinels has
**undefined relative order** for those elements — sort only fully-valid subranges.

### Explicit `==` with Custom `<=>`

When you define a custom `<=>`, also define `==` explicitly — the compiler does
not synthesise `==` from a non-defaulted `<=>`. Omitting it is a compile error
for equality tests.

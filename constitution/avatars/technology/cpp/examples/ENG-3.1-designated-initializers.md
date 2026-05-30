---
law_id: ENG-3.1
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 aggregate designated initializers ({.field=value}). Transitional teams: use positional initialization or named-parameter pattern.
avatar: cpp
---
# ENG-3.1 — Designated Initializers (C++20)

> **Law:** [ENG-3.1 — Code Quality](laws/engineering/eng-3-code-quality.md)
> **The Rule:** Use designated initializers for any struct with 3+ fields to eliminate positional ambiguity.

## Java Comparison

Java uses the Builder pattern (`new Foo.Builder().field1(v).build()`) for readable construction. C++20 designated initializers achieve the same clarity with zero overhead.

## When to Use

- Struct construction with 3+ fields (eliminates positional guessing)
- Configuration objects passed to functions
- Any aggregate where field order is non-obvious

## COMPLIANT ✅

```cpp
// Named fields — reads like documentation
FlightRequest req{
    .origin      = "DFW",
    .destination = "ORD",
    .date        = "2026-07-04",
    .passengers  = 2,
    .cabin_class = CabinClass::economy
};

// Nested designated initializers
SeatAssignment seat{
    .passenger = {.name = "Smith", .loyalty_id = "AA123456"},
    .seat      = {.row = 14, .letter = 'C'}
};
```

## NON-COMPLIANT ❌

```cpp
// Positional — what is 2? what is "economy"?
FlightRequest req{"DFW", "ORD", "2026-07-04", 2, "economy"};

// Fields out of declaration order — ill-formed in C++
FlightRequest req{
    .destination = "ORD",   // ERROR: must match struct field order
    .origin      = "DFW"
};
```

## Edge Cases

- **C++17 and earlier:** Designated initializers are not available. Use positional args with `/*field=*/` comments, or a named constructor / builder pattern.
- **Field order:** Unlike Java named parameters, C++ designated initializers **must** follow struct declaration order.
- **Omitted fields:** Omitted fields are value-initialized (zeroed), not default-constructed with Java-style defaults.
- **Mixing styles:** You cannot mix designated and positional arguments in the same initializer.

---
law_id: ENG-6.1
cpp_version_min: 20
cpp_version_note: >-
  std::span requires C++20. For C++11/14 projects, see
  ENG-6.1-gsl-span-cpp14.md (gsl::span bridge library, identical API).
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): `std::span` Bounds Safety (C++20)

Per [ENG-6.1](laws/engineering/eng-6-security.md), `std::span` replaces raw
pointer+size pairs with a bounds-aware, non-owning view. It eliminates the class
of bugs where pointer and size arguments become separated or silently mismatched.

## COMPLIANT: `span<const SeatData>` Function Signature

```cpp
#include <span>
#include <cstddef>

struct SeatData { char row; int seat_number; bool occupied; };

// ✅ single parameter — pointer and size cannot be separated
void validate_cabin(std::span<const SeatData> seats) {
    if (seats.empty()) return;                            // ✅ safe empty check

    // Subspan: economy rows only (seats 20–35)
    if (seats.size() < 20) return;
    auto economy = seats.subspan(20, std::min<size_t>(16, seats.size() - 20));
    for (const auto& s : economy)
        audit(s);
}

// ✅ Binary serialisation — span<const std::byte> over any trivial type
void write_manifest(std::span<const SeatData> seats,
                    std::ostream& out) {
    auto bytes = std::as_bytes(seats);                    // ✅ no cast required
    out.write(reinterpret_cast<const char*>(bytes.data()),
              static_cast<std::streamsize>(bytes.size()));
}
```

## NON-COMPLIANT: Raw Pointer + Size Pair

```cpp
// ❌ caller can pass mismatched pointer and count with no compile-time check
void validate_cabin(const SeatData* seats, size_t count) {
    for (size_t i = 0; i < count; ++i)  // ❌ out-of-bounds if count > actual
        audit(seats[i]);
}

// ❌ silently loses size at call site:
validate_cabin(seats, seats_count - 1);  // off-by-one invisible to callee
```

## Edge Cases

### Empty Span

`span.empty()` and `span.size() == 0` are both valid checks; `span.data()` on
an empty span returns an unspecified (possibly null) pointer — **never dereference
it**. Always guard with `if (seats.empty()) return;`.

### Dangling Span from Temporary

A span holds a **pointer** — it does not extend the lifetime of its source:

```cpp
// NON-COMPLIANT — span over a temporary vector; UB after semicolon
std::span<const SeatData> bad = get_seat_vector();  // ❌ temporary destroyed

// COMPLIANT — named owner
auto seats = get_seat_vector();
std::span<const SeatData> view{seats};              // ✅ owner outlives span
```

### Span-of-Span (2-D Cabin Layout)

`std::span` is one-dimensional. For a row×seat 2-D layout, use a span of rows
and index within each row explicitly — do **not** cast a 2-D array as a flat
span unless the total element count and alignment are verified.

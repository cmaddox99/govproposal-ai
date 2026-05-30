---
law_id: ENG-6.1
cpp_version_min: 14
cpp_version_note: >-
  Uses microsoft/GSL (MIT) gsl::span for bounds-safe array views on C++14.
  API is identical to C++20 std::span — migration is a header/namespace change.
avatar: cpp
rag_exclude: true  # placeholder — content pending CBF adoption; excluded from RAG routing
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Bounds-Safe Array View — gsl::span Bridge (C++14)

**Avatar:** C++ (Transitional C++14 — CWR / IOC_ALP)
**Pattern:** Non-owning bounds-safe array view via `gsl::span`

## Context

Raw pointer + size pairs have no bounds guarantee. A callee that receives
`(const SeatData* data, size_t len)` cannot assert at compile time that
`data[i]` is valid for all `i < len`. Off-by-one errors in the size argument
are silent until the buffer overread hits production.

Per [ENG-6.1](laws/engineering/eng-6-security.md), array views passed across
function boundaries must carry their own bounds.

[microsoft/GSL](https://github.com/microsoft/GSL) (MIT, Microsoft) provides
`gsl::span<T>` — a non-owning view with a size baked in. Its API is
intentionally identical to C++20 `std::span` — migration is a header and
namespace substitution.

## COMPLIANT — gsl::span Function Parameter

```cpp
// seat_loader.cpp  (CWR / IOC_ALP — C++14)
#include <gsl/span>

struct SeatData { std::string id; bool is_blocked; int row; };

// COMPLIANT: span carries size — no separate len parameter, no chance of mismatch.
void validate_seat_block(gsl::span<const SeatData> seats)
{
    for (const auto& seat : seats) {          // range-for — no index arithmetic
        if (seat.row < 1 || seat.row > 50) {
            throw std::invalid_argument(
                "seat row out of range: " + seat.id);
        }
    }
}

// COMPLIANT: construct span from std::vector — size deduced automatically.
void process_manifest(const std::vector<SeatData>& manifest)
{
    validate_seat_block(gsl::make_span(manifest));
}

// COMPLIANT: construct from raw array — size deduced from array type.
SeatData cabin_seats[180];
validate_seat_block(gsl::make_span(cabin_seats));
```

## COMPLIANT — subspan for Safe Sub-Range Passing

```cpp
// Pass a window into a larger buffer — bounds enforced at construction.
void process_premium_cabin(gsl::span<const SeatData> all_seats)
{
    // Rows 1–20 are premium cabin (0-based index 0–19, count 20).
    // subspan throws gsl::fail_fast if offset+count > size().
    auto premium = all_seats.subspan(0, 20);
    validate_seat_block(premium);

    // Economy cabin: remaining seats.
    auto economy = all_seats.subspan(20);   // offset only — takes rest
    validate_seat_block(economy);
}
```

## NON-COMPLIANT

```cpp
// WRONG 1: raw pointer + size — no bounds contract, mismatch is silent UB.
void validate_seat_block_unsafe(const SeatData* data, size_t len)
{
    for (size_t i = 0; i <= len; ++i) {  // ← off-by-one: i == len is OOB read
        if (data[i].row < 1) { /* ... */ }
    }
}

// Caller can silently pass wrong size:
validate_seat_block_unsafe(manifest.data(), manifest.size() - 1);
// ↑ Passes too-small len — last seat skipped silently.

// WRONG 2: passing pointer to sub-range with manual arithmetic.
void process_premium_unsafe(const SeatData* all, size_t total)
{
    validate_seat_block_unsafe(all, 20);          // assumes ≥20 — unchecked
    validate_seat_block_unsafe(all + 20, total);  // ← total instead of total-20: OOB
}
```

## C++20 Migration Note

`gsl::span` API is identical to C++20 `std::span` — migration is a header and
namespace substitution:

```cpp
// C++14 (microsoft/GSL)             →  C++20 (standard library)
#include <gsl/span>                  →  #include <span>
gsl::span<const SeatData>            →  std::span<const SeatData>
gsl::make_span(vec)                  →  std::span(vec)        // CTAD
gsl::make_span(arr)                  →  std::span(arr)        // CTAD
span.subspan(offset, count)          →  span.subspan(offset, count)  // identical
```

**One behavioral difference:** `gsl::span` defaults to dynamic extent
(`gsl::dynamic_extent`); `std::span` supports static extent via a second
template parameter. Most code migrates unchanged; fixed-size spans gain
a compile-time size guarantee for free.

## Attribution

[microsoft/GSL](https://github.com/microsoft/GSL) — MIT license, © Microsoft.
`gsl::span` standardized as `std::span` in C++20 (P0122R7).

## Edge Cases & Warnings

- **`gsl::fail_fast` on bounds violation:** Unlike raw pointer access (silent
  UB), `gsl::span::operator[]` calls `gsl::fail_fast` on out-of-bounds access
  when `GSL_THROW_ON_CONTRACT_VIOLATION` or `GSL_TERMINATE_ON_CONTRACT_VIOLATION`
  is set. In production builds with `GSL_UNENFORCED_ON_CONTRACT_VIOLATION`,
  bounds checks are elided — configure consistently across all translation units.

- **`subspan` with out-of-range arguments:** `span.subspan(offset, count)`
  triggers `gsl::fail_fast` if `offset > size()` or `offset + count > size()`.
  This is correct fail-fast behavior. The equivalent raw pointer arithmetic
  would be silent UB.

- **Span does not own its data:** `gsl::span` is a view — it holds a pointer
  and size. If the underlying `std::vector` is destroyed or reallocated while
  the span is live, the span becomes dangling. Never store a span as a class
  member unless you can guarantee the lifetime of the source outlives the
  object.

- **`gsl::make_span` vs direct constructor:** In GSL 3.x+, prefer the
  `gsl::span{ptr, size}` constructor or CTAD. `gsl::make_span` is deprecated
  in newer GSL versions in favour of the constructor. In C++20, use `std::span`
  CTAD directly.

- **`const` propagation:** `gsl::span<T>` allows mutating elements;
  `gsl::span<const T>` is read-only. A `const gsl::span<T>` is a const view
  object but elements are still mutable — prefer `gsl::span<const T>` for
  read-only parameters.

Per [ENG-6.1](laws/engineering/eng-6-security.md): array views passed across
function boundaries must carry bounds. Raw pointer + size pairs have no bounds
contract and enable silent out-of-bounds access.

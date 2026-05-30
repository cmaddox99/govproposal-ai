---
law_id: ENG-6.1
cpp_version_min: 23
cpp_version_note: >-
  Uses C++23 std::expected for value-based error propagation. Transitional teams: use enum class + output param; brownfield: use exception boundaries.
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — Expected Error Handling

## The Rule

Use `std::expected` for **recoverable errors** and exceptions only for **truly exceptional** situations (out of memory, programmer bugs). Errors are values — make them impossible to ignore.

**Java equivalent:** `std::expected<T, E>` is similar to Java's checked exceptions but returned as a value instead of thrown. The `.and_then()` method is monadic (like `Optional.flatMap()`). Note: `std::expected` is C++23 — use `tl::expected` for C++17.

## When to Use

- **Hot paths** where exception overhead (stack unwinding, RTTI) is unacceptable
- API boundaries where every failure mode must be explicitly handled
- Pipeline/chain operations where errors propagate through multiple steps

## COMPLIANT: std::expected with Monadic Chaining

```cpp
#include <expected>
#include <string>

enum class BookingError { seat_unavailable, payment_declined, pnr_invalid };

struct Booking { std::string pnr; std::string seat; };

auto validate_pnr(std::string pnr) -> std::expected<std::string, BookingError> {
    if (pnr.size() != 6) return std::unexpected(BookingError::pnr_invalid);  // why: typed error, caller must handle
    return pnr;
}

auto reserve_seat(std::string pnr) -> std::expected<Booking, BookingError> {
    return Booking{pnr, "12A"};  // why: success path returns value directly
}

auto book_flight(std::string pnr) -> std::expected<Booking, BookingError> {
    return validate_pnr(std::move(pnr))
        .and_then(reserve_seat);  // why: monadic chaining — flat, composable, no nesting
}

// For void-returning functions that can fail:
auto cancel_booking(BookingId id) -> std::expected<void, BookingError> {
    if (!exists(id)) return std::unexpected(BookingError::pnr_invalid);
    do_cancel(id);
    return {};  // why: expected<void, E> signals success with no value
}
```

## NON-COMPLIANT: Exception-Based Control Flow

```cpp
Booking book_flight(std::string pnr) {
    if (pnr.size() != 6) throw std::invalid_argument("bad pnr");  // ❌ recoverable error thrown as exception
    auto seat = find_seat();       // ❌ throws seat_error — hidden error path
    charge_payment();              // ❌ throws payment_error — caller needs 3 catch blocks
    return Booking{pnr, seat};
}
// ❌ At API boundary, any unhandled exception = 500 Internal Server Error
```

## Edge Cases & Warnings

| Scenario | Guidance |
|----------|----------|
| `expected<void, Error>` | Use for void-returning functions that can fail — return `{}` for success. |
| Monadic `.and_then()` / `.transform()` | Requires C++23. On C++17, use `tl::expected` or manual `if (!result)` checks. |
| Mixing exceptions and expected | Keep exceptions for invariant violations (bugs). Use expected for domain errors (bad input, unavailable resource). |
| Error type design | Prefer `enum class` over `std::string` for errors — enables exhaustive `switch` checking. |

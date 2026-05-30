---
law_id: ENG-6.1
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 std::string_view for non-owning string references. Transitional teams: use const std::string& or const char*; avoid dangling string_view.
avatar: cpp
---
# ENG-6.1 — Null Safety and Pointer Contracts

> **Law:** [ENG-6.1 — Security by Design](laws/engineering/eng-6-security.md)
> **The Rule:** Every pointer parameter and return type must have an explicit null contract. Dereferencing null in C++ is UB — not an exception.

## Java Comparison

Java throws `NullPointerException` — a recoverable exception with a stack trace. C++ null pointer dereference is **undefined behavior**: no exception, no crash guarantee, possible silent memory corruption.

## When to Use

- Every function that accepts or returns a pointer
- Every constructor that stores a pointer member
- Every API boundary where null could originate from external input

## COMPLIANT ✅

```cpp
// Best: use references (cannot be null by construction)
void confirm_booking(Booking& booking) {
    booking.confirm();
}

// When nullable: use optional for explicit contract
std::optional<Booking> find_booking(std::string_view pnr) {
    auto it = bookings_.find(pnr);
    if (it == bookings_.end()) return std::nullopt;
    return it->second;
}

// When pointer needed: gsl::not_null enforces contract
void process(gsl::not_null<Booking*> booking) {
    booking->confirm();  // guaranteed non-null
}
```

## NON-COMPLIANT ❌

```cpp
// No null contract — caller has no guidance
Booking* find_booking(const std::string& pnr);

// UB: no null check before dereference
void process(Booking* b) {
    b->confirm();  // UB if b == nullptr
}

// Returning nullptr without documenting the contract
Booking* get_active() {
    if (active_.empty()) return nullptr;  // caller may forget to check
    return &active_.front();
}
```

## Edge Cases

- **`dynamic_cast<T*>`** returns `nullptr` on failure — always check the result.
- **Dangling pointers** are worse than null: they appear non-null but point to freed memory. Prefer `std::unique_ptr` / `std::shared_ptr` to eliminate this class of bugs entirely.
- **Thread safety:** Checking `if (ptr)` then using `*ptr` is a TOCTOU race if another thread can modify the pointer. Copy the pointer (or use `shared_ptr`), then check the copy.
- **Legacy `NULL` / `0`:** Replace with `nullptr` in all touched code. Use `modernize-use-nullptr` clang-tidy check.

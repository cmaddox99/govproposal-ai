---
law_id: ENG-6.1
cpp_version_min: 11
avatar: cpp
---

# [ENG-6.1](laws/engineering/eng-6-security.md): Security by Design — Move Semantics

**Java equivalent:** None. Java passes all objects by reference; there's no 'moving'. In C++, moving transfers ownership of resources (memory, file handles) from one object to another without copying. `noexcept` on move constructors is critical because `std::vector` won't use move during reallocation unless it's guaranteed not to throw.

## COMPLIANT: noexcept Move via Swap

```cpp
#include <string>
#include <utility>
#include <vector>

class FlightReservation {
    std::string pnr_;
    std::vector<std::string> segments_;
public:
    FlightReservation(std::string pnr, std::vector<std::string> segs)
        : pnr_(std::move(pnr)), segments_(std::move(segs)) {}

    FlightReservation(FlightReservation&& other) noexcept
        : pnr_(std::move(other.pnr_)), segments_(std::move(other.segments_)) {}

    FlightReservation& operator=(FlightReservation&& other) noexcept {
        FlightReservation tmp(std::move(other));
        swap(*this, tmp);
        return *this;
    }

    friend void swap(FlightReservation& a, FlightReservation& b) noexcept {
        using std::swap;
        swap(a.pnr_, b.pnr_);
        swap(a.segments_, b.segments_);
    }
};
```

**Why compliant:** noexcept move enables strong exception guarantee. std::vector reallocation uses move safely.

## NON-COMPLIANT: Throwing Move Constructor

```cpp
class FlightReservation {
    std::string pnr_;
    std::vector<std::string> segments_;
public:
    FlightReservation(FlightReservation&& other)  // NOT noexcept
        : pnr_(other.pnr_), segments_(other.segments_) {  // copies, may throw
        if (pnr_.empty()) throw std::runtime_error("bad move");
    }
};
// std::vector falls back to copy on reallocation — silent perf bug
```

**Why non-compliant:** Throwing move forces vector to copy instead of move. Data corruption risk on exception.

## Rule of Five Checklist

When your class manages a resource (memory, file handle, socket), implement all five or explicitly default/delete them:

```cpp
class Connection {
public:
    Connection(std::string host, int port);
    ~Connection();                                          // 1. Destructor
    Connection(const Connection&) = delete;                 // 2. Copy ctor — delete if non-copyable
    Connection& operator=(const Connection&) = delete;      // 3. Copy assign
    Connection(Connection&& other) noexcept;                // 4. Move ctor — always noexcept
    Connection& operator=(Connection&& other) noexcept;     // 5. Move assign — always noexcept
};

// Compile-time verification:
static_assert(std::is_nothrow_move_constructible_v<Connection>,
    "Connection must be nothrow-movable for safe container reallocation");
```

**The Rule:** If you define any of the five, define all five. Mark move operations `noexcept`. Use `static_assert` to verify at compile time. Prefer `= default` when the compiler-generated version is correct.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Moved-from object used after move | Valid-but-unspecified state; null ptr dereference is UB | Set moved-from pointers to `nullptr`; add debug assertion in all methods |
| Move constructor marked `noexcept` incorrectly | `std::vector` moves instead of copies; if move throws, `std::terminate` | Only mark `noexcept` after verifying every member's move is also `noexcept` |
| Self-assignment in move assignment operator | `obj = std::move(obj)` frees then accesses the same resource | Add self-assignment guard: `if (this == &other) return *this;` |

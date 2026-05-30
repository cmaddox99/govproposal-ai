---
law_id: ENG-3.1
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 concepts (requires clause). Transitional teams: use SFINAE with std::enable_if for unconstrained forwarding wrappers.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): Complexity Limits — Perfect Forwarding

**Java equivalent:** None. Java passes objects by reference automatically; there's no concept of 'forwarding' a value's move/copy category. In C++, `T&&` in a template is a 'forwarding reference' — it can bind to both lvalues and rvalues. `std::forward` preserves which kind it was.

## COMPLIANT: Correct Forwarding Patterns

```cpp
#include <utility>   // std::forward, std::move
#include <memory>    // std::make_unique

// Factory with perfect forwarding — forward is LAST use
template <typename T, typename... Args>
std::unique_ptr<T> make(Args&&... args) {
    return std::make_unique<T>(std::forward<Args>(args)...);
}

// Emplace-style API — forward into container
template <typename... Args>
void add_booking(Args&&... args) {
    bookings_.emplace_back(std::forward<Args>(args)...);
}

// Read args before forwarding (correct order)
template <typename T>
void process_and_store(T&& item) {
    log_item(item);                    // ✅ read first (lvalue ref)
    storage_.push_back(std::forward<T>(item));  // ✅ forward last
}
```

## NON-COMPLIANT: Common Forwarding Mistakes

```cpp
// ❌ Forward the same argument twice — use-after-move
template <typename T>
void broken(T&& val) {
    consume(std::forward<T>(val));   // may move val
    log(std::forward<T>(val));       // ❌ UB if val was moved
}

// ❌ std::forward on non-deduced type (rvalue ref, not forwarding ref)
void take_widget(Widget&& w) {
    // Widget&& is an RVALUE REFERENCE, not a forwarding reference
    store(std::forward<Widget>(w));  // ❌ misleading — use std::move
    store(std::move(w));             // ✅ correct for rvalue references
}

// ❌ Forwarding reference is too greedy (suppresses conversions)
class Booking {
public:
    template <typename T>
    Booking(T&& name) : name_{std::forward<T>(name)} {}
    // DANGER: The forwarding reference is a better match than the copy
    // constructor for non-const lvalues (Booking&). The compiler prefers
    // the template instantiation Booking(Booking&) over the implicit
    // Booking(const Booking&), so copies break at compile time.
    // Fix: add `requires(!std::same_as<std::decay_t<T>, Booking>)`
};
```

## Simplification Guide

| Pattern | When to Use | Simpler Alternative |
|---------|-------------|---------------------|
| `T&&` + `std::forward` | Generic library code, factories | `const T&` for read-only |
| Forwarding reference constructor | Rarely — advanced only | Overload: `const std::string&` + `std::string&&` |
| Variadic forwarding | `emplace` style APIs | Named parameters + move |
| `auto&&` | Range-for loops, generic lambdas | `const auto&` when mutation not needed |

## Decision Flowchart

```
Need to preserve value category of generic arg?
├── NO → Use const T& (read) or T (sink/move)
└── YES → Is this a public API?
    ├── YES → Provide const T& + T&& overloads
    └── NO (internal/library) → Use T&& + std::forward
```

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Forwarding to an overloaded function causes ambiguity | `std::forward<T>(arg)` deduces as both `T&` and `T&&`; the overload set has a match for each — compiler error or wrong overload selected | Avoid forwarding to bare overloaded function names; wrap in a lambda: `[](auto&& x){ f(std::forward<decltype(x)>(x)); }` |
| `std::forward` used inside a range-based `for` loop body | Each loop iteration forwards the same value; after the first iteration the value is moved-from; subsequent iterations read a hollow object | Use `std::forward` only at the call site of the final consumer; inside a loop, copy if you need the value in each iteration |
| Universal reference interacting with `explicit` single-argument constructors | `T&& x` matches explicit constructors when `T` is deduced — implicit conversion that the programmer did not intend | Constrain forwarding functions with a concept or SFINAE guard to exclude the implicit-conversion case |

---
law_id: ENG-3.2
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 std::span for non-owning views. Transitional teams: pass const T* with size, or use gsl::span from Guidelines Support Library.
avatar: cpp
---

# [ENG-3.2](laws/engineering/eng-3-code-quality.md): Immutability — C++ Examples

## COMPLIANT: Immutable Value Object

```cpp
class Money {
public:
    static Money of(int cents) { return Money{cents}; }
    static Money zero() { return Money{0}; }

    Money operator+(Money other) const { return Money{cents_ + other.cents_}; }
    Money operator*(double rate) const { return Money{static_cast<int>(cents_ * rate)}; }
    auto operator<=>(const Money&) const = default;

private:
    explicit Money(int cents) : cents_(cents) {}
    int cents_;
};
```

**Why compliant:** All fields are private and set at construction. Operations return new instances. No mutating methods.

## NON-COMPLIANT: Mutable Value Type

```cpp
struct Money {
    int cents;  // Public, mutable
    void add(int amount) { cents += amount; }  // Mutates in place
};
```

**Why non-compliant:** Value type with mutable state. Shared references can be modified unexpectedly. No thread safety.

## Deep const and const Propagation

```cpp
class FlightSchedule {
    std::vector<Segment> segments_;
public:
    // const method returns const view — caller cannot modify segments
    std::span<const Segment> segments() const { return segments_; }

    // Non-const returns mutable span (only when modification is intended)
    std::span<Segment> mutable_segments() { return segments_; }
};

// Propagate const through pointers with std::experimental::propagate_const
// or by returning const references from const methods
```

**The Rule:** In C++, `const` is the primary immutability mechanism — use it aggressively. Mark all non-mutating methods `const`. Return `const&` or `span<const T>` from accessors. Value objects should have no mutating methods; operations return new instances. Unlike Java's `final` (which only prevents reassignment), C++ `const` prevents mutation through the reference — a stronger guarantee.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `const` member function modifies state via `mutable` cache member | Caller sees a `const` method and assumes no side effects; the `mutable` cache is modified, making the function non-thread-safe | Mark the method `const` only if it is also thread-safe; document the mutable member and protect it with a mutex, or remove `mutable` and make the cache external |
| `const` reference to a temporary extends the temporary's lifetime — but only directly | `const T& r = factory();` keeps the temporary alive; `const T& r = wrapper.get_temp();` does NOT — the temporary dies at the semicolon | Only bind a `const` reference directly to a temporary (or use C++17 guaranteed copy elision with a value type); never rely on lifetime extension through an intermediate function call |
| `const` propagation does not apply to pointers inside a `const` object | A `const Foo` with a `Bar*` member still allows `Bar` to be mutated through the pointer | Use `const Bar*` for non-owning members that should not be mutated; wrap owning members in `unique_ptr` or a value type |

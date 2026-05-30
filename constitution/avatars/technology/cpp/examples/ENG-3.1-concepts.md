---
law_id: ENG-3.1
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 concepts (concept/requires). Brownfield/transitional teams: implement constraints via static_assert or SFINAE in C++11/14/17.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md): Complexity Limits — C++20 Concepts

## When to Use

Use concepts to constrain template parameters — similar to Java's `<T extends Comparable<T>>` but checked at compile time. Without concepts (pre-C++20), template errors produce pages of incomprehensible messages.

## COMPLIANT: Named Concept Constraint

```cpp
#include <concepts>
#include <string>

template<typename T>
concept Serializable = requires(const T& t) {
    { t.to_json() } -> std::convertible_to<std::string>;
    { T::from_json(std::string{}) } -> std::same_as<T>;
};

struct CrewRoster {
    std::string crew_id;
    std::string to_json() const { return "{\"crew\":\"" + crew_id + "\"}"; }
    static CrewRoster from_json(std::string json) { return {"CR-001"}; }
};

void publish_to_queue(const Serializable auto& payload) {
    auto json = payload.to_json();
    // send to message broker
}
```

**Why compliant:** Concept makes requirements explicit and readable. Compiler errors name the violated constraint directly.

## NON-COMPLIANT: Unconstrained SFINAE

```cpp
template<typename T,
    typename = std::enable_if_t<
        std::is_member_function_pointer_v<decltype(&T::to_json)> &&
        std::is_constructible_v<T, decltype(T::from_json(std::declval<std::string>()))>
    >>
void publish_to_queue(const T& payload) {
    // incomprehensible error on constraint violation
}
```

**Why non-compliant:** SFINAE produces unreadable errors. High cognitive complexity violates [ENG-3.1](laws/engineering/eng-3-code-quality.md) limits.

## Multi-Constraint Concept with requires Clause

```cpp
template<typename T>
concept DomainEntity = requires(T t) {
    { t.id() } -> std::convertible_to<std::string>;
    { t.version() } -> std::integral;
    requires std::movable<T>;
};

// Constrain a member function (not the whole class)
class EventStore {
public:
    template<DomainEntity E>
    void save(E&& entity) {
        auto json = entity.to_json();
        persist(entity.id(), entity.version(), json);
    }
};
```

**Why It Matters:** Concepts replace SFINAE, `static_assert`, and documentation comments with compiler-enforced contracts. A violation produces an error message naming the unsatisfied requirement — not a 200-line template instantiation backtrace. Always prefer a named concept over `requires` clauses inlined at the template declaration.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Concept subsumption ordering not matching expected overload | Two overloads exist: one constrained with `Sortable`, one with `SortableAndComparable`; the compiler picks the wrong one because subsumption requires one concept to syntactically include the other | Write `SortableAndComparable` to explicitly include `Sortable` via concept composition (`concept SortableAndComparable = Sortable<T> && Comparable<T>`); do not duplicate constraints |
| Concept constraint not checked on explicit template instantiation | `template class Scheduler<FlightLeg>` bypasses concept checks in some compilers before C++20 DR fixes; invalid instantiation compiles | Avoid explicit instantiations unless the type was already verified to satisfy the concept at point of use; add a `static_assert(ConceptName<FlightLeg>)` alongside explicit instantiation |
| `auto` parameter in function signature silently creates an unconstrained template | `void process(auto x)` is equivalent to `template<typename T> void process(T x)` — no concept constraint; accepts any type | Prefer named concept constraint: `void process(Processable auto x)` or an explicit `template<Processable T>` form |

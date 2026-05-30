---
skill:
  id: skill-cpp-template-complexity-management
  name: "C++ Template Complexity Management"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-3.1
      title: Complexity Limits Law
  references:
    - id: ENG-3.5
      title: Naming Law
    - id: ENG-4.1
      title: Atomic TDD Law

triggers:
  phrases:
    - "C++ template complexity"
    - "C++ template metaprogramming"
    - "C++ concepts constraints"
    - "C++ compile time errors"

followed_by:
  - skill-08-code-review
  - skill-14-technical-debt
---

# Skill: C++ Template Complexity Management

## Purpose

Govern template usage so that compile-time abstractions remain readable, testable, and maintainable. Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), template nesting depth and instantiation complexity must be bounded.

## Procedure

1. **Prefer concepts over SFINAE** — use C++20 `requires` clauses for template constraints instead of `std::enable_if` chains
2. **Limit nesting depth** — template instantiation depth must not exceed 3 levels; deeper hierarchies must be refactored
3. **Name constraints clearly** — per [ENG-3.5](laws/engineering/eng-3-code-quality.md), concept names should read as adjectives (`Sortable`, `Hashable`, `Serializable`)
4. **Test template code** — every template must have at least one explicit instantiation test (per [ENG-4.1](laws/engineering/eng-4-testing.md))

## Governance Gate

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md), template metaprogramming that produces compiler error messages longer than 50 lines indicates excessive complexity and must be simplified.

## C++ Specific Patterns

- Use `static_assert` with descriptive messages for constraint violations
- Prefer `if constexpr` over tag dispatch for compile-time branching
- Extract complex type traits into named concepts for reuse
- Document template parameters with `@tparam` in Doxygen-style comments

## Legacy Standard Support

### SFINAE Governance (Pre-C++20)
When concepts are not available, use `std::enable_if_t` patterns:
```cpp
// C++11/14/17: SFINAE with enable_if
template<typename T,
         typename = std::enable_if_t<std::is_arithmetic_v<T>>>
T calculate_fare(T base, T multiplier);

// C++20: Concepts (migration target)
template<std::floating_point T>
T calculate_fare(T base, T multiplier);
```

### Tag Dispatch (Pre-C++17)
For compile-time branching without `if constexpr`:
```cpp
template<typename T>
void serialize_impl(const T& obj, std::true_type /* is_trivial */) { memcpy(...); }
template<typename T>
void serialize_impl(const T& obj, std::false_type) { obj.serialize(stream); }
template<typename T>
void serialize(const T& obj) { serialize_impl(obj, std::is_trivial<T>{}); }
```

### Migration Path
1. Mark all SFINAE patterns with `// TODO(modernize): replace with concept`
2. When upgrading to C++20, replace `enable_if_t` with named concepts
3. Replace tag dispatch with `if constexpr` (C++17) or concepts (C++20)

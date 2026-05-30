---
skill:
  id: skill-cpp-exception-safety-governance
  name: "C++ Exception Safety Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
  references:
    - id: ENG-3.1
      title: Complexity Limits Law
    - id: ENG-6.7
      title: Audit Trail Law

triggers:
  phrases:
    - "C++ exception safety"
    - "C++ noexcept contract"
    - "C++ error handling strategy"
    - "C++ strong guarantee"
    - "C++ std::expected"

followed_by:
  - skill-cpp-ownership-lifetime-safety
  - skill-27-constitution-compliance
---

# Skill: C++ Exception Safety Governance

## Purpose

Enforce exception safety guarantees across all C++ code so that failures never corrupt state or leak resources. Per [ENG-6.1](laws/engineering/eng-6-security.md), exception safety is a security design constraint.

## Procedure

1. **Classify every public function** — assign a guarantee level (nothrow, strong, or basic) and document it
2. **Enforce noexcept contracts** — destructors, move operations, and `swap()` must be `noexcept`. Verify with `static_assert(std::is_nothrow_move_constructible_v<T>)`
3. **Define exception boundaries** — exceptions permitted within modules; translate to `std::expected` or error codes at API/service boundaries
4. **Audit exception propagation** — per [ENG-6.7](laws/engineering/eng-6-security.md), exceptions caught at boundaries must be logged before translation
5. **Test exception paths** — GoogleTest tests must verify both success and exception/error paths

## Governance Gate

Per [ENG-6.1](laws/engineering/eng-6-security.md), a move constructor or destructor that is not `noexcept` is a **blocking violation**. Public API functions without a documented exception safety guarantee are incomplete.

## C++ Specific Patterns

- Use `std::expected<T,E>` (C++23) at API boundaries; fall back to `tl::expected` for C++20
- Implement strong guarantee via copy-and-swap idiom
- Use RAII to ensure basic guarantee (resource cleanup) as the minimum
- Mark leaf functions `noexcept` when they only call nothrow operations

## Legacy Standard Support

### Pre-C++23: tl::expected
For projects that cannot use `std::expected` (C++23), use the `tl::expected` polyfill:
```cpp
#if defined(__cpp_lib_expected) && __cpp_lib_expected >= 202211L
    #include <expected>
    template<typename T, typename E> using Result = std::expected<T, E>;
#else
    #include <tl/expected.hpp>
    template<typename T, typename E> using Result = tl::expected<T, E>;
#endif
```

### Pre-C++17: Error Code Patterns
For C++11/14 projects without std::optional or tl::expected:
```cpp
// Use error code + out parameter pattern
enum class BookingError { not_found, sold_out, system_error };
BookingError create_booking(const Request& req, Booking& out_result);

// Or use pair<bool, T> for simple cases
std::pair<bool, Fare> calculate_fare(const Segment& seg);
```

### Exception Safety in Legacy Code
- Ensure RAII wrappers exist for all resources before adding exception-throwing code
- In C++98 code, prefer error codes over exceptions until RAII is established
- When adding exceptions to legacy code, audit all resource paths for leak safety

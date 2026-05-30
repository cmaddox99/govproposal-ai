---
skill:
  id: skill-cpp-compatibility-headers
  name: "C++ Cross-Standard Compatibility Headers"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp
  description: "Governance for writing headers that compile correctly across C++ standard versions"

laws:
  implements:
    - id: ENG-3.1
      title: Complexity Limits Law
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
    - id: ENG-2.2
      title: Layered Architecture Law

triggers:
  phrases:
    - "backward compatible C++ headers"
    - "cross-standard headers"
    - "C++ header portability"
    - "multi-standard C++ header"

followed_by:
  - skill-cpp-feature-detection
  - skill-cpp-api-compatibility-governance
  - skill-27-constitution-compliance
---

# C++ Cross-Standard Compatibility Headers

## Purpose
Public headers consumed by modules at different C++ standard versions must work correctly at every consumer's standard level. This skill governs how to write such headers.

## Header Compatibility Checklist

Public headers consumed by modules at different standards MUST:

- [ ] Use only features available at the LOWEST supported standard of any consumer
- [ ] Use `__cplusplus` / feature-test macro guards for standard-dependent code paths
- [ ] NOT include standard library headers that don't exist at the minimum standard (e.g., `<optional>` in a header consumed by C++11 code)
- [ ] NOT use `auto` return types in public function declarations (C++14+ only)
- [ ] NOT use `[[nodiscard]]`, `[[maybe_unused]]` without `#if __cplusplus >= 201703L` guards
- [ ] NOT use `constexpr` on functions with non-trivial bodies (only trivial constexpr in C++11)
- [ ] Document the minimum standard in a header comment

## Polyfill Patterns

```cpp
// Type aliasing for standard-dependent types
#if __cplusplus >= 202002L
    #include <span>
    template<typename T> using Span = std::span<T>;
#else
    #include <gsl/span>
    template<typename T> using Span = gsl::span<T>;
#endif
```

## ABI Safety at Header Boundaries

- Never expose `std::string` or `std::vector` in public headers of shared libraries
- Use Pimpl idiom to hide standard library types from public API
- Use `extern "C"` for maximum ABI stability at library boundaries

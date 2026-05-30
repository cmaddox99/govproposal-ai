---
skill:
  id: skill-cpp-api-compatibility-governance
  name: "C++ API Compatibility Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-2.3
      title: Vertical Slice Law
  references:
    - id: ENG-3.1
      title: Complexity Limits Law
    - id: ENG-6.7
      title: Audit Trail Law

triggers:
  phrases:
    - "C++ API compatibility"
    - "C++ ABI stability"
    - "C++ header versioning"
    - "C++ breaking change policy"

followed_by:
  - skill-12-api-design
  - skill-27-constitution-compliance
---

# Skill: C++ API Compatibility Governance

## Purpose

Govern public header stability so that downstream consumers are not broken by internal refactoring. Per [ENG-2.3](laws/engineering/eng-2-architecture.md), vertical slices must be independently deployable without ABI surprises.

## Procedure

1. **Tag public headers** — all headers under `include/project/` are public API; internal headers live under `src/`
2. **Annotate deprecations** — use `[[deprecated("reason — removal in vX.Y")]]` before removing any public symbol
3. **Version the API** — maintain a `VERSION` file or CMake variable; bump major version for breaking changes
4. **Test compatibility** — integration tests must compile against the previous minor version's public headers

## Governance Gate

Per [ENG-2.3](laws/engineering/eng-2-architecture.md), removing or renaming a public symbol without a deprecation cycle is a **blocking violation**.

## C++ Specific Patterns

- Use the pImpl idiom to hide implementation details behind a stable ABI
- Prefer free functions over member functions for extension (Koenig lookup)
- Use `inline namespace` for ABI versioning when binary compatibility is required

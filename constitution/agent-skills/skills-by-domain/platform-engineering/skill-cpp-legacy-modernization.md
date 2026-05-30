---
skill:
  id: skill-cpp-legacy-modernization
  name: "C++ Legacy Code Modernization"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp
  description: "Safe patterns for incrementally modernizing legacy C++ code without wholesale rewrites"

laws:
  implements:
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
    - id: ENG-4.1
      title: Atomic TDD Law (NON-NEGOTIABLE)
    - id: ENG-3.1
      title: Complexity Limits Law

triggers:
  phrases:
    - "modernize legacy C++"
    - "modernize old C++ code"
    - "incremental C++ modernization"
    - "refactor legacy C++"
    - "C++ modernization priority"
    - "ActiveTest migration"
    - "test harness migration C++"
    - "TestRunner.lib replace"
    - "migrate from ActiveTest to GoogleTest"

followed_by:
  - skill-cpp-standard-migration
  - skill-cpp-legacy-code-navigation
  - skill-27-constitution-compliance
---

# C++ Legacy Code Modernization

## Purpose
Defines safe, incremental modernization patterns that improve code quality without the risk of wholesale rewrites. Per [ENG-6.1](laws/engineering/eng-6-security.md), security improvements take priority.

## Modernization Priority Order

Apply these transformations in order when touching legacy code:

| Priority | Transformation | Standard | Risk | Safety Impact |
|---|---|---|---|---|
| 1 | `NULL` → `nullptr` | C++11 | Minimal | Eliminates ambiguity bugs |
| 2 | Add `override` to virtual functions | C++11 | Minimal | Catches signature mismatches |
| 3 | Raw pointer → `unique_ptr` (in touched functions) | C++11 | Medium | Eliminates memory leaks |
| 4 | `#define` constants → `constexpr` | C++11 | Low | Adds type safety |
| 5 | C-casts → `static_cast`/`dynamic_cast` | Any | Low | Makes intent explicit |
| 6 | Range-based for (in touched loops) | C++11 | Low | Eliminates off-by-one |
| 7 | `auto` for complex iterator types | C++11 | Low | Reduces verbosity |
| 8 | `const` correctness sweep | Any | Medium | Prevents mutation bugs |

## "Do Not Touch" Rules

- Working code in files you are NOT modifying for a task
- Third-party or vendored code
- Platform-specific `#pragma` directives
- Legacy naming conventions in untouched files (rename only in files you own)
- Stable test fixtures (modernize only if tests are being updated)

## Compatibility Macros

For projects that must support multiple standards during migration:
```cpp
#if __cplusplus >= 201703L
  #define AA_NODISCARD [[nodiscard]]
  #define AA_FALLTHROUGH [[fallthrough]]
  #define AA_MAYBE_UNUSED [[maybe_unused]]
#else
  #define AA_NODISCARD
  #define AA_FALLTHROUGH
  #define AA_MAYBE_UNUSED
#endif
```

## Module-by-Module Workflow

1. Select leaf module (fewest dependencies)
2. Write characterization tests (Michael Feathers method)
3. Apply modernization priority list to touched code
4. Verify all tests pass
5. Review: did modernization introduce any ABI breaks?
6. Commit with `modernize: <module-name>` prefix
7. Move to next module toward the dependency root

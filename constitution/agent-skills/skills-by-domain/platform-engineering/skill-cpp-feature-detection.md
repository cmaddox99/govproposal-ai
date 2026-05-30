---
skill:
  id: skill-cpp-feature-detection
  name: "C++ Feature Detection Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp
  description: "Correct use of feature-test macros for portable, standard-compliant C++ code"

laws:
  implements:
    - id: ENG-3.1
      title: Complexity Limits Law
    - id: ENG-5.2
      title: Build & Deploy Law

triggers:
  phrases:
    - "C++ feature detection"
    - "__cplusplus macro"
    - "__has_include"
    - "C++ feature test macro"
    - "SD-6 macros"

followed_by:
  - skill-cpp-compatibility-headers
  - skill-cpp-standard-migration
  - skill-27-constitution-compliance
---

# C++ Feature Detection Governance

## Purpose
Governs the correct use of feature-test macros to write portable C++ code across compiler versions and standard levels.

## __cplusplus Values

| Standard | Value |
|---|---|
| C++98 | `199711L` |
| C++11 | `201103L` |
| C++14 | `201402L` |
| C++17 | `201703L` |
| C++20 | `202002L` |
| C++23 | `202302L` |

## SD-6 Feature-Test Macros (Preferred)

| Macro | Feature | Minimum Value |
|---|---|---|
| `__cpp_concepts` | Concepts | `201907L` |
| `__cpp_coroutines` | Coroutines | `201902L` |
| `__cpp_lib_optional` | std::optional | `201606L` |
| `__cpp_lib_span` | std::span | `202002L` |
| `__cpp_lib_expected` | std::expected | `202211L` |

## Rules

1. **Prefer SD-6 macros** (`__cpp_lib_*`, `__cpp_*`) over `__cplusplus` for fine-grained checks
2. **Use `__has_include`** (C++17) for header availability
3. **NEVER use compiler macros** (`__GNUC__`, `_MSC_VER`, `__clang__`) for standard feature detection
4. **Document each #if block** with migration target: `// TODO(modernize): remove when C++20 baseline`
5. **Test both branches** — CI must build with and without the feature to validate both code paths

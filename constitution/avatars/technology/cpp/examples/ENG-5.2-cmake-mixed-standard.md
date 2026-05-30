---
law_id: ENG-5.2
cpp_version_min: 17
cpp_version_note: >-
  Uses C++17 std::optional for conditional build targets. Transitional teams: use boolean flags and conditional CMake blocks instead.
avatar: cpp
---

# [ENG-5.2](laws/engineering/eng-5-devops.md) — CMake Mixed-Standard Repository Configuration

## The Rule

Mixed-standard projects must set per-target C++ standards using `target_compile_features()`. A global `CMAKE_CXX_STANDARD` forces every target to the same standard, breaking legacy modules or silently enabling features in code that hasn't been audited for them.

**Java equivalent:** This is like having modules on Java 8 and Java 17 in the same project. `_GLIBCXX_USE_CXX11_ABI` is a GCC-specific flag that controls which standard library ABI is used — mixing values across linked libraries causes crashes.

## When to Use

- **Module-by-module migration** — migrating a monorepo from C++11→C++20 one library at a time. Each target declares its own standard as it gets modernized.
- **Third-party integration** — wrapping a C++11 vendor SDK alongside your C++20 application code.

Per [ENG-5.2](laws/engineering/eng-5-devops.md) (CI/CD Pipeline Law), multi-standard repositories must configure per-target standards.

## COMPLIANT: Per-Target Standards

```cmake
cmake_minimum_required(VERSION 3.20)
project(flight_ops LANGUAGES CXX)

# Legacy module — C++11, maintenance only
add_library(acars_parser src/legacy/acars_parser.cpp)
target_compile_features(acars_parser PUBLIC cxx_std_11)
target_compile_options(acars_parser PRIVATE -Wall -Wextra)

# Active module — C++17
add_library(gate_assignment src/gate/solver.cpp)
target_compile_features(gate_assignment PUBLIC cxx_std_17)
target_compile_options(gate_assignment PRIVATE -Wall -Wextra -Wpedantic -Werror)

# New module — C++20
add_library(crew_optimizer src/crew/optimizer.cpp)
target_compile_features(crew_optimizer PUBLIC cxx_std_20)
target_compile_options(crew_optimizer PRIVATE
    -Wall -Wextra -Wpedantic -Werror -Wconversion -Wsign-conversion)

# Boundary: C-compatible types only at legacy/modern interface
target_link_libraries(gate_assignment PRIVATE acars_parser)
```

## NON-COMPLIANT: Global Standard

```cmake
# BAD — forces all targets to same standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
```

Use `target_compile_features()` per target, never global `CMAKE_CXX_STANDARD` in mixed repos.

## C++ Standard Tiers

| Tier | Standards | Status | Applies To | Governance |
|---|---|---|---|---|
| Recommended | C++23 | recommended | greenfield | Full constitution governance |
| Required Minimum | C++20 | required for greenfield | greenfield | Full constitution governance |
| Active Brownfield | C++14, C++17 | active | brownfield w/ modernization plan | Modernization plan toward C++20 required |
| Legacy Supported | C++11 | sunset | brownfield only | Modernization to C++17+ within 12 months; no new C++11 modules |
| Legacy Frozen | C++98, C++03 | maintenance only | brownfield only | Bug fixes and security patches only; funded modernization plan required |

### Minimum Compiler Versions by Tier

| Tier | GCC | Clang | MSVC |
|---|---|---|---|
| Recommended (C++23) | 14 | 17 | 19.38 (VS 2022 17.8+) |
| Required Minimum (C++20) | 12 | 15 | 19.34 (VS 2022 17.4+) |
| Active Brownfield (C++14/17) | 7 | 5 | 19.14 (VS 2017 15.7+) |
| Legacy Supported (C++11) | 4.8.1 | 3.3 | 19.0 (VS 2015) |
| Legacy Frozen (C++98/03) | any | any | any |

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| ODR violations from mixed-standard shared headers | `std::string` SSO buffer size and `std::optional` triviality change between standards; a C++11 target and a C++20 target sharing a header cause **silent UB** | Use C-compatible types (`int`, `const char*`, POD structs) at mixed-standard API boundaries; never share STL container types across standard boundaries |
| GCC `_GLIBCXX_USE_CXX11_ABI` mismatch | Incompatible `std::string`/`std::list` ABI between TUs; linker accepts it but runtime crashes on string operations | Ensure all targets link against the same standard library ABI; enforce via a global CMake variable or toolchain file |
| `CXX_STANDARD` not propagating through `FetchContent` dependencies | Third-party targets fetched via `FetchContent` compile with their own default standard, not the project's; mixed-standard binary | Set `CMAKE_CXX_STANDARD` globally in the toolchain file and require a minimum version in `cmake_minimum_required` that propagates it |

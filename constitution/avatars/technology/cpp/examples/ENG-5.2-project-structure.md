---
law_id: ENG-5.2
cpp_version_min: 98
avatar: cpp
topic: project-structure
---

# [ENG-5.2](laws/engineering/eng-5-devops.md): C++ Project Structure — Canonical CMake Layout

## The Rule

Project layout is infrastructure. A well-structured C++ project separates domain logic from infrastructure adapters, isolates public headers from implementation, and co-locates tests with the code they exercise. This layout enables incremental modernization of brownfield codebases without full rewrites.

## When to Use

- Starting a new C++ service or library
- Adding a CMake build to a legacy `src/`-only codebase
- Splitting a monolithic translation unit into layered modules
- Defining where to put tests, mocks, and integration fixtures

## NON-COMPLIANT: Flat Layout (No Separation of Concerns)

```text
project-root/
├── CMakeLists.txt
├── gate_solver.cpp         # ❌ domain, infra, and main mixed in root
├── gate_solver.h
├── database.cpp
├── database.h
├── main.cpp
└── test_gate_solver.cpp    # ❌ tests co-mingled with source
```

```cmake
# ❌ Single flat target — no layer isolation
add_executable(gate_service
    gate_solver.cpp database.cpp main.cpp)
target_link_libraries(gate_service PRIVATE sqlite3)
```

**Why non-compliant:** Domain logic depends directly on infrastructure headers. No include path enforces layer boundaries. All tests rebuild when any source changes.

## COMPLIANT: Layered CMake Project Structure

```text
project-root/
├── CMakeLists.txt
├── cmake/
│   └── sanitizers.cmake
├── include/
│   └── project/
│       ├── domain/
│       │   ├── model/
│       │   ├── repository/
│       │   └── service/
│       ├── application/
│       └── infrastructure/
├── src/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   └── application/
│   └── integration/
├── vcpkg.json
└── .clang-tidy
```

```cmake
cmake_minimum_required(VERSION 3.20)
project(gate_assignment_service LANGUAGES CXX)

add_library(gate_domain
    src/domain/gate_solver.cpp
    src/domain/gate_repository_impl.cpp)
target_include_directories(gate_domain PUBLIC include)
target_compile_features(gate_domain PUBLIC cxx_std_20)

add_library(gate_application src/application/assign_gates_use_case.cpp)
target_link_libraries(gate_application PUBLIC gate_domain)

add_library(gate_infra src/infrastructure/sqlite_gate_repository.cpp)
target_link_libraries(gate_infra PUBLIC gate_application)

enable_testing()
add_executable(gate_unit_tests
    tests/unit/domain/gate_solver_test.cpp
    tests/unit/application/assign_gates_test.cpp)
target_link_libraries(gate_unit_tests PRIVATE gate_application GTest::gtest_main)
add_test(NAME UnitTests COMMAND gate_unit_tests)

add_executable(gate_integration_tests tests/integration/sqlite_repo_test.cpp)
target_link_libraries(gate_integration_tests PRIVATE gate_infra GTest::gtest_main)
add_test(NAME IntegrationTests COMMAND gate_integration_tests)
set_tests_properties(IntegrationTests PROPERTIES LABELS integration)
```

**Why compliant:** Each CMake library target mirrors an architectural layer. Unit tests link only `gate_application` — they cannot accidentally call infrastructure. Integration tests are labeled separately so CI can run unit-only on fast paths.

## Brownfield Adaptation

| Step | Action |
|------|--------|
| Do not move files | Add `include/project/domain/` headers alongside existing `.h` files; introduce new CMake targets without touching the legacy `add_executable` |
| Migrate incrementally | Write characterization tests first (see `ENG-4.1-characterization-test-pattern.md`), then move `.cpp`/`.h` pairs one module at a time |

## Key Rules

| Rule | Rationale |
|------|-----------|
| `include/project/` for public headers only | Prevents consumers from depending on private implementation headers |
| One CMake target per architectural layer | Linker enforces layer dependencies — infra cannot bleed into domain |
| Tests in `tests/unit/` and `tests/integration/` | CTest labels enable selective CI runs (fast path = unit only) |
| `vcpkg.json` committed at root | Reproducible dependency resolution across machines and CI |
| `.clang-tidy` committed | Static analysis config is part of the codebase contract |

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Domain and infra headers mixed in `src/` | `#include "SqlRepo.h"` in domain code; untestable without a database | Enforce via CMake `target_include_directories` with no infra path on the domain target |
| New layer directory added; IDE shows false errors | IDE cached wrong include paths from stale build | Regenerate CMake after structural changes; commit `compile_commands.json` |
| New `.cpp` files missing from CMake source list | File compiles locally (GLOB) but not in CI (explicit list) | Use explicit source lists; CI step diffs source list against `find src/ -name '*.cpp'` |

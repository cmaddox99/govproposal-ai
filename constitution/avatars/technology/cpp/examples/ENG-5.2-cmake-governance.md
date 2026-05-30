---
law_id: ENG-5.2
cpp_version_min: 98
avatar: cpp
---

# [ENG-5.2](laws/engineering/eng-5-devops.md): CI/CD Pipeline — CMake Governance

## The Rule

Build systems are infrastructure-as-code: CMakeLists.txt files must be reviewed, versioned, and governed with the same rigor as production source. Sloppy CMake causes unreproducible builds, silent miscompilation, and CI/CD drift.

## Key CMake Governance Rules

1. **Set `cmake_minimum_required`** — pin a minimum version (≥3.20) so all developers and CI use the same feature set.
2. **Use target-based commands** — `target_compile_features`, `target_compile_options`, `target_link_libraries` scoped to each target. Never use global `CMAKE_CXX_FLAGS` or `add_compile_options`.
3. **No `file(GLOB ...)`** — GLOB does not re-run when files are added/removed, causing silent build failures. List source files explicitly.
4. **Pin dependency versions** — `FetchContent_Declare` with a specific `GIT_TAG`, never `main`/`master`.

## COMPLIANT: Modern Target-Based CMake

```cmake
cmake_minimum_required(VERSION 3.20)
project(gate_assignment_service LANGUAGES CXX)

add_library(gate_assignment src/gate_solver.cpp src/gate_repository.cpp)
target_compile_features(gate_assignment PUBLIC cxx_std_20)
target_compile_options(gate_assignment PRIVATE -Wall -Wextra -Wpedantic -Werror)

option(ENABLE_SANITIZERS "Enable ASan/UBSan" OFF)
if(ENABLE_SANITIZERS)
    target_compile_options(gate_assignment PUBLIC -fsanitize=address,undefined)
    target_link_options(gate_assignment PUBLIC -fsanitize=address,undefined)
endif()

include(FetchContent)
FetchContent_Declare(googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0)
FetchContent_MakeAvailable(googletest)

add_executable(gate_tests tests/gate_solver_test.cpp)
target_link_libraries(gate_tests PRIVATE gate_assignment GTest::gtest_main)
```

**Why compliant:** Target-scoped flags, reproducible deps via FetchContent, sanitizer option for CI, modern CMake idioms.

## NON-COMPLIANT: Global Flag Pollution

```cmake
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -fsanitize=address")
add_subdirectory(vendor/googletest)  # unversioned, mutable
add_executable(gate_tests gate_solver.cpp gate_solver_test.cpp)
```

**Why non-compliant:** Global CMAKE_CXX_FLAGS pollutes all targets. Unversioned vendor dep breaks reproducibility.

## CI Toolchain Requirements

**Mandatory gates (must pass on every PR):**

- Compiler warning flags (`-Wall -Wextra -Wpedantic -Werror`)
- `clang-tidy` static analysis
- AddressSanitizer (ASan)
- UndefinedBehaviorSanitizer (UBSan)

**Recommended gates (enabled where practical):**

- ThreadSanitizer (TSan)
- clang static analyzer
- Mull mutation testing (requires LLVM/Clang)
- `llvm-cov` / `gcov`-compatible coverage reporting
- CodeQL C/C++ (requires GitHub Advanced Security)
- Dependabot alerts + GitHub dependency review

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `file(GLOB)` misses a newly added source file | Developer adds `src/new_handler.cpp`; CMake was configured before the file existed; GLOB won't pick it up until a clean reconfigure; CI passes, local builds fail | Use explicit source lists; if GLOB is unavoidable, add a configure-time check that asserts source count matches expectations |
| `FetchContent_MakeAvailable` downloads in air-gapped CI | Network calls at configure time fail in restricted environments; build breaks silently | Use `FetchContent_Declare` with `FETCHCONTENT_FULLY_DISCONNECTED=ON` and pre-populated dependency directories in CI |
| Target alias collision between subprojects | Two subdirectories both define `::mylib`; the second silently shadows the first | Namespace all aliases with the project prefix: `MyProject::mylib`; enforce in code review |

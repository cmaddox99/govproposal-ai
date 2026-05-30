---
skill:
  id: skill-cpp-portable-build-governance
  name: "C++ Portable Build Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-5.1
      title: Infrastructure as Code Law
    - id: ENG-5.2
      title: CI/CD Pipeline Law
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-6.1
      title: Security by Design Law

triggers:
  phrases:
    - "C++ CMake governance"
    - "C++ cross-platform build"
    - "C++ vcpkg Conan setup"
    - "C++ portable build configuration"

followed_by:
  - skill-cpp-sanitizer-hardening
  - skill-27-constitution-compliance
---

# Skill: C++ Portable Build Governance

## Purpose

Ensure C++ projects build reproducibly across GCC, Clang, and MSVC with consistent dependency management. Per [ENG-5.1](laws/engineering/eng-5-devops.md), the CI/CD pipeline must produce identical artifacts regardless of developer platform.

## Procedure

1. **Use CMake as the build system** — `CMakeLists.txt` at project root; no platform-specific build scripts in production
2. **Pin dependencies** — use `vcpkg.json` (default) or `conanfile.py` with locked versions; no unpinned transitive dependencies
3. **Test on all supported compilers** — CI matrix must include GCC 12+, Clang 15+, and MSVC 19.34+ (if Windows support is required)
4. **Enforce minimum standard** — `set(CMAKE_CXX_STANDARD 20)` with `CMAKE_CXX_STANDARD_REQUIRED ON`
5. **Separate build configurations** — Debug (sanitizers + assertions) and Release (optimization + LTO) as distinct CI jobs

## Governance Gate

Per [ENG-5.1](laws/engineering/eng-5-devops.md), a project that builds on only one compiler is not considered portable and must not be promoted to production without a documented platform restriction waiver.

## C++ Specific Patterns

- Use `target_compile_features(mylib PUBLIC cxx_std_20)` instead of global standard setting
- Prefer `FetchContent` or vcpkg over manual `add_subdirectory` for third-party dependencies
- Use `CMAKE_EXPORT_COMPILE_COMMANDS=ON` for clang-tidy integration
- Keep toolchain files (`cmake/toolchains/`) versioned alongside the project

## Legacy Standard Support

### Brownfield Standard Configuration
For projects not yet on C++20, configure per-target standards:
```cmake
# Mixed-standard repository
target_compile_features(legacy_module PUBLIC cxx_std_11)
target_compile_features(active_module PUBLIC cxx_std_17)
target_compile_features(new_module PUBLIC cxx_std_20)
```

Do NOT use global `CMAKE_CXX_STANDARD` in mixed-standard repositories. Each target must declare its own standard via `target_compile_features()`.

### Pre-CMake Build Systems
For brownfield projects using Make, MSBuild, or Bazel:
- Document the equivalent standard flag (`-std=c++11`, `/std:c++14`, etc.) per target
- Ensure CI validates with the documented standard flag
- Create a migration plan to CMake when feasible

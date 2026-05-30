---
law_id: ENG-3.1
cpp_version_min: 20
cpp_version_note: >-
  Uses C++20 feature-test macros (__cpp_*) and std::span. Transitional teams: use __cplusplus checks and gsl::span or raw pointer+size pairs.
avatar: cpp
---

# [ENG-3.1](laws/engineering/eng-3-code-quality.md) — Feature-Detection Macros for Cross-Standard Code

**The Rule:** Use standard feature-detection macros (`__cplusplus`, `__cpp_lib_*`, `__has_include`) for cross-standard compatibility — never compiler-specific version macros. This ensures code compiles correctly on GCC, Clang, and MSVC without per-compiler maintenance.

**When to use:** Libraries consumed by multiple projects on different C++ standards; airline systems running mixed GCC/Clang CI pipelines; any header shared between C++17 and C++20 code.

## COMPLIANT: Standard Feature Detection

```cpp
// Level 1: Broad standard check via __cplusplus
#if __cplusplus >= 202002L
    #include <span>
    using BufferView = std::span<const std::byte>;
#elif __cplusplus >= 201703L
    #include <gsl/span>
    using BufferView = gsl::span<const std::byte>;
#else
    struct BufferView { const uint8_t* data; size_t size; };
#endif

// Level 2: Fine-grained SD-6 feature-test macros
#if defined(__cpp_lib_optional) && __cpp_lib_optional >= 201606L
    #include <optional>
#else
    #include <tl/optional.hpp>  // polyfill for C++14
    namespace std { using tl::optional; }
#endif

// Level 3: Header availability (C++17 __has_include)
#ifdef __has_include
  #if __has_include(<format>)
    #include <format>
    #define HAS_STD_FORMAT 1
  #else
    #include <fmt/format.h>  // fallback to fmtlib
    #define HAS_STD_FORMAT 0
  #endif
#endif
```

## NON-COMPLIANT: Compiler-Specific Detection

```cpp
// ❌ _MSC_VER tests the compiler, not the feature
#if _MSC_VER >= 1914
    #include <optional>  // wrong: MSVC 19.14 might not enable C++17 by default
#endif

// ❌ __GNUC__ doesn't tell you which -std= flag was used
#if __GNUC__ >= 8
    #include <filesystem>  // wrong: GCC 8 with -std=c++14 won't have this
#endif
```

**⚠️ Edge case:** `__has_include` itself requires C++17 — always guard it with `#ifdef __has_include`. On older compilers, fall back to `__cplusplus` checks.

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| `__has_include` succeeds but the included header is incomplete or stub-only | Feature detection reports the feature as present; code compiles but fails at link time or runtime | Test for a key symbol or macro inside the header after including it: `#if __has_include(<x>) && defined(FEATURE_MACRO)` |
| Feature macros defined differently across translation units in the same build | ODR violation when a class uses `if constexpr` on a macro that is defined in some TUs and not others | Define feature macros exclusively in a single project-wide config header that is force-included by the build system (`-include config.h`) |
| `__cplusplus` reports 199711 on MSVC even with `/std:c++17` without `/Zc:__cplusplus` | Code that checks `__cplusplus >= 201703L` silently falls back to the C++03 path on MSVC | Add `-Zc:__cplusplus` (MSVC) or `set_property(TARGET ... PROPERTY CXX_STANDARD 17)` in CMake; assert the value in a static_assert at project startup |

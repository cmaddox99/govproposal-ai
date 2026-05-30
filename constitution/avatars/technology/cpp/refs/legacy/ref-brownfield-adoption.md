---
cpp_version_min: 98
cpp_version_note: >-
  Brownfield adoption guidance for legacy C++ codebases (C++98/03+).
avatar: cpp
---

# C++ Avatar Reference: Brownfield Adoption

---

## Brownfield Migration

Per [ENG-1.4](laws/engineering/eng-1-core-principles.md) (Incremental Improvement Law), large changes must be broken into vertical slices. Brownfield adoption proceeds module-by-module — no wholesale rewrite required.

For existing C++ codebases adopting this constitution:

### Adoption Kickoff

When a brownfield codebase adopts the Hangar AI Constitution, these steps execute **before** any code changes:

1. **Run Constitution Compliance Rating** — Execute `skill-cpp-compliance-rating` to produce a baseline score across all 10 dimensions. Record the composite score, grade, and per-dimension breakdown. This becomes the remediation starting point. See [Constitution Compliance Rating](#constitution-compliance-rating) for the full rubric.
2. **Notify the team about Developer Guidance** — All developers on the project (especially those new to C++) must be informed that the following resources are available:
   - [Mental Model Transitions](#mental-model-transitions) — 8 critical conceptual gaps for Java/Python/C# developers
   - [Legacy Code Smell Catalog](#legacy-code-smell-catalog) — 14 structural smells with recognition and remediation
   - [Legacy Codebase Triage Playbook](#legacy-codebase-triage-playbook) — Day-by-day week-1 priorities
   - [Survival Patterns](#survival-patterns) — Week-1 through month-6 progression for legacy codebases
   - [Object Design Rehabilitation](#object-design-rehabilitation) — 6 design debt vectors
   - `skill-cpp-legacy-code-navigation` — Step-by-step navigation with triage timeline and seam identification
   - `skill-cpp-legacy-survival-patterns` — Safe modification patterns and progression checklists
3. **Create a `MODERNIZATION_PLAN.md`** — Using the compliance rating breakdown, prioritize dimensions with the lowest scores. Set 30/60/90-day remediation targets.
4. **Establish baseline metrics** — Warning count, sanitizer finding count, test count, and compliance score. These are tracked monthly.

### Non-Rewrite Safeguards

- **No rewrite is recommended by default** — adopt the constitution incrementally, not via wholesale rewrite
- **Migration is allowed only when explicitly requested and approved** by the engineering lead and architecture review
- All brownfield changes must document **preserved behavior** and a **test equivalence** strategy before any refactor begins
- Compatibility and modernization guidance must preserve stack intent before suggesting transformation

### Phased Modernization Path

Modernization proceeds module-by-module through explicit phases:

**Phase 1 — CI Foundation:**
- Add `clang-tidy`, AddressSanitizer (ASan), and UndefinedBehaviorSanitizer (UBSan) to the CI pipeline
- Adopt GoogleTest for new test files; if no test framework exists, adopt immediately
- Configure `clang-format` with a project `.clang-format` file
- No source code changes required in this phase

**Phase 2 — Incremental Modernization:**
- Target C++20 features module-by-module with documented milestones
- Migrate compiler toolchain if needed (e.g., upgrade GCC version or add Clang build configuration)
- Replace raw pointers with `std::unique_ptr` / `std::shared_ptr` in modified modules
- Add `std::span` for buffer parameters in new or refactored APIs
- Each module migration must pass all existing tests before and after changes

**Phase 3 — Full Governance Alignment:**
- Enable Mull mutation testing on modules with Clang build support
- Migrate remaining test files to GoogleTest (if using a legacy framework)
- Achieve full CI gate compliance (all mandatory + recommended gates)
- Declare unsafe boundary governance mode for the repository

### Compiler Migration Path

When a brownfield project requires compiler migration (e.g., older GCC to modern GCC/Clang):

1. Add the new compiler as a **parallel CI build** — do not replace the existing compiler immediately
2. Fix compilation warnings/errors under the new compiler module-by-module
3. Run the full test suite under both compilers until migration is verified
4. Retire the old compiler build only after all modules compile and pass tests under the new compiler

### Rollback Strategy

If a modernization step introduces regressions:

1. **Revert the module-level change** — each modernization change should be scoped to a single module for easy rollback
2. **Run the test equivalence suite** to confirm pre-modernization behavior is restored
3. **Document the rollback** reason in the modernization plan and adjust the timeline
4. **Do not block other modules** — a rollback in one module does not halt modernization of independent modules

### Approval Requirements

| Action | Approval Required |
|--------|-------------------|
| Adding CI gates (Phase 1) | Team lead |
| Module-level modernization (Phase 2) | Engineering lead |
| Compiler migration | Architecture review + engineering lead |
| Full framework migration (e.g., Catch2 → GoogleTest) | Engineering lead |
| Declaring unsafe boundary governance mode | Architect approval (per governance policy) |

---

## Per-Tier clang-tidy Configuration

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity Limits) and [ENG-5.2](laws/engineering/eng-5-devops.md) (CI/CD Pipeline Law), static analysis must run in CI. Configure clang-tidy checks based on the project's C++ standard tier. Running the full modernize-* suite against legacy code produces thousands of false positives and erodes developer trust.

### C++11 Tier (.clang-tidy)
```yaml
Checks: >
  -*,
  bugprone-*,
  performance-*,
  readability-identifier-naming,
  modernize-use-nullptr,
  modernize-use-override,
  modernize-use-auto,
  modernize-replace-auto-ptr,
  -modernize-use-trailing-return-type,
  -modernize-use-nodiscard
# DO NOT enable: modernize-use-std-span, modernize-use-concepts
```

### C++14/17 Tier (.clang-tidy)
```yaml
Checks: >
  -*,
  bugprone-*,
  performance-*,
  readability-*,
  modernize-*,
  -modernize-use-trailing-return-type,
  cppcoreguidelines-*
# Enable: modernize-replace-random-shuffle, modernize-use-nodiscard (C++17)
# DO NOT enable: modernize-use-concepts, modernize-use-std-span (C++20 only)
```

### C++20+ Tier (.clang-tidy)
```yaml
Checks: >
  -*,
  bugprone-*,
  performance-*,
  readability-*,
  modernize-*,
  cppcoreguidelines-*,
  misc-*,
  -modernize-use-trailing-return-type
# Full suite including concepts, ranges, span checks
```

## Per-Tier Testing Framework Matrix

Per [ENG-4.2](laws/engineering/eng-4-testing.md) (Test Pyramid Law), all tiers must have automated tests. The framework varies by standard but the testing requirement does not.

| Standard Tier | Framework | Minimum Version | Notes |
|---|---|---|---|
| C++98/03 (frozen) | CppUnit / Boost.Test | Latest compatible | No migration required; characterization tests only |
| C++11 (sunset) | GoogleTest | ≤1.12.x | `MOCK_METHODn` macros permitted; plan migration to `MOCK_METHOD` with C++14 upgrade |
| C++14/17 (active) | GoogleTest | 1.14+ | `MOCK_METHOD` mandatory; parameterized tests encouraged |
| C++20/23 (recommended) | GoogleTest | 1.14+ | Full feature set including concepts-constrained test helpers |

**Key constraints:**
- GoogleTest 1.14+ requires C++14 minimum. Do NOT mandate it for C++11 projects.
- C++98/03 projects cannot use GoogleTest — CppUnit or Boost.Test are acceptable alternatives.
- All tiers MUST have automated tests in CI — the framework may differ, the requirement does not.

## Per-Tier Code Review Criteria

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md) (Complexity Limits), code review criteria vary by standard tier. Higher tiers enforce the full governance suite; lower tiers focus on safety and correctness.

### C++98/03 (Frozen) — Maintenance Reviews
- **Flag immediately**: Buffer overflows (strcpy, sprintf), data races, uninitialized memory
- **Flag for tracking**: Raw new/delete, C-style casts, void* usage (add to modernization backlog)
- **Leave alone**: Working typedef, #pragma in third-party headers, legacy naming conventions
- **Require**: Characterization tests for any modified function

### C++11 (Sunset) — Modernization-Aware Reviews
- **Flag immediately**: std::auto_ptr (deprecated), NULL macro, volatile for synchronization
- **Modernize when touched**: Raw pointers → unique_ptr in modified functions, C-casts → named casts
- **Verify**: Proper move semantics on touched types, nullptr in new/modified code
- **Leave alone**: Stable code not being modified, std::bind in untouched code

### C++14/17 (Active) — Standard Reviews
- **Flag immediately**: boost::optional where std::optional available (C++17), std::result_of (deprecated C++17)
- **Enforce**: [[nodiscard]] on factory functions, structured bindings where clearer, if constexpr over SFINAE
- **Verify**: No unnecessary Boost usage where std equivalents exist
- **Modernize when touched**: std::bind → generic lambdas

### C++20/23 (Recommended) — Full Governance Reviews
- **Full governance**: All anti-patterns from manifest enforced
- **Enforce**: Concepts over SFINAE, ranges over raw loops in new code, std::expected for error handling
- **Verify**: All current guidance sections apply without exception

## Cross-Standard ABI Boundaries

Per [ENG-2.4](laws/engineering/eng-2-architecture.md) (Bounded Context Law), modules compiled at different C++ standards must have well-defined interfaces. ABI mismatches across standard boundaries cause silent data corruption.

When a repository contains modules compiled at different C++ standards:

### GCC Dual ABI
All modules in a single binary MUST use the same `_GLIBCXX_USE_CXX11_ABI` value. GCC 5+ defaults to the new ABI (`=1`), but linking against libraries built with GCC 4.x requires `=0`. Set explicitly in CMake:
```cmake
add_compile_definitions(_GLIBCXX_USE_CXX11_ABI=1)  # or =0 for legacy compat
```

### Standard Library Types at Boundaries
Do NOT pass `std::string`, `std::vector`, or other standard library types across shared library boundaries between modules compiled at different standards. Use:
- C-compatible types (`const char*`, pointer+size) at library boundaries
- Pimpl idiom to hide standard library types from public headers
- `extern "C"` interfaces for maximum ABI stability

### ODR Compliance
Every header included by translation units at different standards must produce identical type definitions. Use `__cplusplus` guards for standard-dependent code paths in shared headers:
```cpp
#if __cplusplus >= 201703L
    using OptionalFlight = std::optional<Flight>;
#else
    using OptionalFlight = boost::optional<Flight>;
#endif
```

### Link-Time Validation
Add a CI check that verifies all object files in a binary target were compiled with the same `-std=` flag, OR that boundary interfaces use only ABI-safe types. CMake's `target_compile_features()` helps enforce per-target standards:
```cmake
target_compile_features(legacy_module PUBLIC cxx_std_11)
target_compile_features(modern_module PUBLIC cxx_std_20)
```

## Feature-Detection Macro Governance

Per [ENG-5.3](laws/engineering/eng-5-devops.md) (Environment Parity Law), code must behave consistently across environments. Use standard feature-detection macros for cross-standard headers and conditional compilation.

### `__cplusplus` Values by Standard
| Standard | `__cplusplus` Value |
|---|---|
| C++98 | `199711L` |
| C++11 | `201103L` |
| C++14 | `201402L` |
| C++17 | `201703L` |
| C++20 | `202002L` |
| C++23 | `202302L` |

### Feature-Test Macros (SD-6)
Prefer `__cpp_*` feature-test macros over `__cplusplus` version checks for fine-grained detection:
```cpp
#if defined(__cpp_lib_optional) && __cpp_lib_optional >= 201606L
    #include <optional>
#else
    #include <boost/optional.hpp>
#endif

#if defined(__cpp_concepts) && __cpp_concepts >= 201907L
    template<Serializable T> void persist(const T& obj);
#else
    template<typename T> void persist(const T& obj);  // SFINAE fallback
#endif
```

### Header Availability
Use `__has_include` (C++17) for header availability:
```cpp
#if __cplusplus >= 201703L && __has_include(<filesystem>)
    #include <filesystem>
    namespace fs = std::filesystem;
#elif __has_include(<experimental/filesystem>)
    #include <experimental/filesystem>
    namespace fs = std::experimental::filesystem;
#else
    #include <boost/filesystem.hpp>
    namespace fs = boost::filesystem;
#endif
```

### Rules
- Prefer `__cpp_lib_*` / `__cpp_*` feature-test macros over `__cplusplus` version checks
- Use `__has_include(<header>)` for header availability (C++17+)
- **NEVER** use compiler-specific macros (`__GNUC__`, `_MSC_VER`) for standard feature detection
- Document each `#if` block with the migration target: `// TODO(modernize): remove when C++20 is baseline`


---

## See Also

- [Brownfield Project Configuration](ref-brownfield-project-config.md)

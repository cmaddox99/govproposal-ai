---
skill:
  id: skill-cpp-standard-migration
  name: "C++ Standard Migration Governance"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp
  description: "Governs the upgrade path between C++ standard versions, from C++98/03 through C++23"

laws:
  implements:
    - id: ENG-5.2
      title: Build & Deploy Law
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
    - id: ENG-4.1
      title: Atomic TDD Law (NON-NEGOTIABLE)

triggers:
  phrases:
    - "migrate C++ standard"
    - "upgrade C++ version"
    - "C++11 to C++17"
    - "C++14 to C++20"
    - "standard migration checklist"

followed_by:
  - skill-cpp-legacy-modernization
  - skill-cpp-compatibility-headers
  - skill-27-constitution-compliance
---

# C++ Standard Migration Governance

## Purpose
Provides governed procedures for upgrading a C++ codebase from one standard version to another, ensuring safety, ABI stability, and compliance throughout the migration.

## Decision Matrix: When to Upgrade

| Factor | Upgrade Now | Defer |
|---|---|---|
| Compiler support | Target compiler available in CI | Compiler upgrade blocked by infrastructure |
| Team readiness | Team trained on target features | No training completed |
| Dependencies | All deps support target standard | Critical deps require current standard |
| ABI risk | No shared library consumers | External ABI contracts in place |
| Business value | Unlocks safety features (smart ptrs, span) | Mostly syntactic sugar |

## Pre-Migration Checklist

1. [ ] Identify current standard (`CMAKE_CXX_STANDARD` or `__cplusplus` value)
2. [ ] Verify target compiler supports desired standard (see manifest standard_tiers)
3. [ ] Audit dependencies for standard compatibility
4. [ ] Assess ABI impact — are there shared library consumers?
5. [ ] Create MODERNIZATION_PLAN.md in repository root
6. [ ] Set up dual-compiler CI (old + new) per dual-toolchain governance
7. [ ] Identify first migration module (prefer leaf modules with good test coverage)

## Migration Execution Per [ENG-4.1](laws/engineering/eng-4-testing.md)

Each feature adoption follows Atomic TDD:
1. **RED**: Write test exercising the new feature (e.g., test unique_ptr replaces raw pointer)
2. **GREEN**: Apply migration to production code
3. **REFACTOR**: Clean up; verify no regressions
4. **COMMIT**: Reference migration plan in commit message

## Rollback Procedure

If migration introduces ABI breaks or test failures:
1. Revert `-std=` flag change in affected targets
2. Keep the new compiler in CI for analysis-only (no release builds)
3. Document the blocker in MODERNIZATION_PLAN.md
4. Address blocker before reattempting

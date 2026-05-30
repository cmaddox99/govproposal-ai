---
skill:
  id: skill-cpp-legacy-code-navigation
  name: "C++ Legacy Code Navigation"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-4.1
      reason: "Characterization tests before modifying legacy code (TDD for existing behavior)"
    - id: ENG-1.3
      reason: "Continuous refactoring applied incrementally to legacy codebases"
  references:
    - id: ENG-3.1
      reason: "Complexity limits guide modernization scope"
    - id: ENG-6.1
      reason: "Security patterns applied incrementally during modernization"

triggers:
  phrases:
    - "C++ legacy code"
    - "C++ understand codebase"
    - "C++ new to codebase"
    - "C++ code archaeology"
    - "C++ characterization test"
    - "C++ modernization entry point"
    - "C++ onboarding"
    - "help me understand this C++ code"

followed_by:
  - skill-cpp-ownership-lifetime-safety
  - skill-cpp-sanitizer-hardening
  - skill-27-constitution-compliance
---

# C++ Legacy Code Navigation

## Purpose

Guide novice engineers through understanding, safely modifying, and incrementally modernizing existing C++ codebases at American Airlines. Prevents accidental regressions while accelerating time-to-proficiency.

## Procedure

1. **Discover structure** — read `CMakeLists.txt` to understand module boundaries, then scan `include/` headers for public API surface.
2. **Trace execution** — find `main()` or initialization function; follow call chain to understand component wiring.
3. **Write characterization tests** — before modifying anything, write tests that capture current behavior (per [ENG-4.1](laws/engineering/eng-4-testing.md)). These are your safety net.
4. **Identify legacy patterns** — recognize pre-modern patterns (`auto_ptr`, raw `new`/`delete`, `NULL`, manual mutex) and map to modern equivalents.
5. **Apply safe modifications** — use Sprout Method (new function called from old) or Wrap Method (wrap existing function) to minimize risk.
6. **Modernize incrementally** — replace `new`/`delete` with smart pointers, add `const` correctness, use `override`, range-for loops — only in code you touch.
7. **Document discoveries** — update `README.md` or `AGENTS.md` with any tribal knowledge you uncover (undocumented flags, build quirks, environment dependencies).

## Triage Timeline

When joining a legacy C++ codebase, follow this day-by-day sequence during week 1:

| Day | Activity | Deliverable |
|-----|----------|-------------|
| 1–2 | Build and run the project | Documented build steps, test baseline |
| 2–3 | Enable `-fsanitize=address,undefined` on tests | Memory safety debt count |
| 3–4 | Enable `-Wall -Wextra` (no `-Werror` yet) | Type safety debt metrics |
| 4–5 | Map dependency graph (`cmake --graphviz` / IWYU) | Architecture debt map |
| 5 | Write 5 characterization tests for critical paths | First safety net |

Month-1 weekly targets:
- **Weeks 1–2:** Green CI with warnings tracked; 20+ characterization tests
- **Week 3:** Fix CRITICAL sanitizer findings (use-after-free, buffer overflow)
- **Week 4:** Begin `const` correctness sweep and `override` addition on leaf modules

## Seam Identification Guide

Use seams (per Michael Feathers, *Working Effectively with Legacy Code*) to introduce testability without rewriting:

### Preprocessing Seam

Use `#ifdef TEST` to substitute test implementations at compile time — a pragmatic technique for legacy code where dependency injection is not yet available.

### Link Seam

Provide a different `.o` file at link time to substitute test doubles. CMake makes this straightforward — create a test target that links against mock object files instead of production ones.

### Object Seam

Extract a pure virtual base class (interface) from a concrete class. Have the existing class implement it. In tests, inject a mock that also implements the interface. This is the long-term goal — it introduces proper dependency inversion per [ENG-2.1](laws/engineering/eng-2-architecture.md).

### Identifying Seam Candidates

Functions that call external systems (database, network, filesystem) are the highest-value seam candidates — they are where test isolation is most needed. Start with these when introducing testability.

## Characterization Testing Procedure

Per [ENG-4.1](laws/engineering/eng-4-testing.md), write characterization tests before any modification:

1. **Identify critical paths** — what code runs on every request? Handles money? Handles crew scheduling?
2. **Test black-box behavior** — call the public function with known inputs, assert outputs
3. **Test error paths** — null input, empty input, boundary values; legacy code often has surprising edge-case behavior
4. **Use Approval Testing** — for complex outputs (formatted strings, serialized data), capture current output as a "golden file" and assert against it
5. **Target:** 50+ characterization tests covering the top 20 public APIs within month 1

## Metrics to Track

| Metric | Source | Target |
|--------|--------|--------|
| Warning count | `-Wall -Wextra` build output | Decreasing monthly |
| Sanitizer finding count | ASan/UBSan test run | Zero CRITICAL within month 1 |
| Characterization test count | `ctest --test-dir build` | 50+ by end of month 1 |
| Cyclomatic complexity | `lizard` or `pmccabe` | Top-10 functions decreasing |
| Build time | CI logs | Stable or decreasing |

## Governance Gate

- Characterization tests must pass before AND after any modification
- Never mix behavior change and refactor in the same commit
- Modernization changes must be scoped to a single module for easy rollback
- All modifications must pass existing CI gates (clang-tidy, ASan, UBSan)

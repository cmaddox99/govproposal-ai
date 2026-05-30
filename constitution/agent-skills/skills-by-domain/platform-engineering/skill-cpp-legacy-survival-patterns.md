---
skill:
  id: skill-cpp-legacy-survival-patterns
  name: "C++ Legacy Survival Patterns"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-4.1
      reason: "TDD cycle applied to legacy modifications — characterization tests before changes"
    - id: ENG-3.1
      reason: "Complexity management through incremental modernization patterns"
  references:
    - id: ENG-1.3
      reason: "Continuous refactoring as a survival pattern"
    - id: ENG-6.1
      reason: "Security-first modernization — RAII conversion is a security improvement"
    - id: ENG-2.1
      reason: "Architecture layering guides module boundary identification"

triggers:
  phrases:
    - "C++ legacy survival"
    - "C++ safe modification"
    - "C++ sprout method"
    - "C++ wrap method"
    - "C++ modernize incrementally"
    - "C++ onboarding legacy"
    - "C++ new developer legacy code"
    - "C++ first PR legacy"
    - "how to modify legacy C++ safely"

followed_by:
  - skill-cpp-legacy-code-navigation
  - skill-cpp-ownership-lifetime-safety
  - skill-cpp-legacy-modernization
---

# C++ Legacy Survival Patterns

## Purpose

Provide a structured progression for developers — especially those new to C++ — taking over poorly-maintained legacy codebases. Covers safe reading strategies, incremental modification patterns, and a timeline from week 1 through month 6.

## Week 1: Reading and Understanding

Follow these strategies to build a mental model before touching any code:

1. **Read execution-path-first** — Start at `main()` or the service entry point. Follow ONE request through the call chain. Understand one complete path before branching out.
2. **Use a debugger as a reading tool** — Set a breakpoint at the entry point, step through with real input. GDB/LLDB shows what the code *actually does* vs what you *think* it does.
3. **Draw the module dependency graph** — On paper or with Graphviz. Identify cycles and safe boundaries.
4. **Annotate pointer ownership** — For every raw pointer, write "owns" or "borrows." This is the single most important annotation for understanding legacy C++.
5. **Read CMakeLists.txt like a map** — Targets, libraries, flags, and preprocessor defines tell you the project topology.
6. **Use `git log --follow`** — Commit messages and PR descriptions are your archaeological record.

### Week 1 Success Criteria

- [ ] Can build the project from clean checkout
- [ ] Traced one complete request path end-to-end
- [ ] Module dependency graph drawn (even rough sketch)
- [ ] 5 characterization tests written for critical path functions

## Month 1: Safe Modification Patterns

Use these patterns to make changes without breaking existing behavior:

### 1. Sprout Method

Write new logic in a **new function**. Call it from the existing function. You have added behavior without modifying working code.

```
// Existing — don't modify
void processBooking(Booking& b) {
    // ... existing logic ...
    validateNewRules(b);  // ← new call to sprouted method
}

// New — your code, your tests
void validateNewRules(const Booking& b) { /* ... */ }
```

### 2. Wrap Method

Need pre/post behavior? Create a new function with the old name, rename the old function to `_impl`. Callers are unchanged.

### 3. Extract Interface

Need to test a class with external dependencies? Create a pure virtual base class, have the concrete class implement it, inject the interface in tests.

### 4. RAII Conversion

The single most valuable incremental change. Every function with manual `new`/`delete` or `open`/`close`: wrap **one** resource in an RAII guard per PR. Don't rewrite the whole function.

### 5. Boy Scout Rule (Scoped)

Only modernize code on lines you are actively modifying for a feature or bug fix. Don't clean up adjacent code.

### Month 1 Success Criteria

- [ ] 20+ characterization tests covering critical paths
- [ ] Zero CRITICAL sanitizer findings remaining
- [ ] At least 3 PRs merged using Sprout/Wrap/RAII patterns
- [ ] const correctness sweep started on leaf modules

## Month 3: Contributing with Confidence

1. **Write new code to modern standards** — Even in a C++11 codebase, new files should be exemplary: `unique_ptr`, `const` correctness, `override`, range-for, `auto`.
2. **Create islands of quality** — Your new module has: unit tests, zero warnings, zero sanitizer findings, documented public API.
3. **Propose small modernization PRs** — `nullptr` replacement, `override` addition, RAII conversion in modules you have worked in.
4. **Build characterization test suite to 100+** — Covering the critical paths you have encountered.

## Month 6: Leading Modernization

1. **Create `MODERNIZATION_PLAN.md`** — Prioritized by risk × impact. Track publicly.
2. **Establish a compiler warning dashboard** — Track by module. Celebrate reductions.
3. **Champion incremental compiler upgrades** — Add a newer compiler as a CI build (not replacing the old one yet).
4. **Train the team** — Share Mental Model Transitions knowledge with other new-to-C++ developers.

## Governance Gate

Per [ENG-4.1](laws/engineering/eng-4-testing.md):
- Every modification must have a characterization test proving existing behavior is preserved
- Never mix behavior change and refactor in the same commit
- RAII conversions are always safe to merge independently — they fix resource leaks on all paths

Per [ENG-3.1](laws/engineering/eng-3-code-quality.md):
- Modernization scope limited to one module per PR for easy rollback
- New code must meet current complexity limits regardless of legacy context

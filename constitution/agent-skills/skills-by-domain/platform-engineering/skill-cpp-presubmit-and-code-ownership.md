---
skill:
  id: skill-cpp-presubmit-and-code-ownership
  name: "C++ Presubmit and Code Ownership"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-4.1
      title: Atomic TDD Law (NON-NEGOTIABLE)
    - id: ENG-4.2
      title: Test Pyramid Law
  references:
    - id: ENG-6.7
      title: Audit Trail Law

triggers:
  phrases:
    - "C++ presubmit checks"
    - "C++ code review gate"
    - "C++ CI pipeline checks"
    - "C++ CODEOWNERS"

followed_by:
  - skill-08-code-review
  - skill-cpp-sanitizer-hardening
---

# Skill: C++ Presubmit and Code Ownership

## Purpose

Define the mandatory presubmit gate for C++ pull requests. Per [ENG-4.1](laws/engineering/eng-4-testing.md), no code merges without a passing RED-GREEN-REFACTOR cycle verified in CI.

## Procedure

1. **Verify test exists** — every PR must include at least one new or modified GoogleTest test
2. **Run presubmit suite** — `cmake --build build && ctest --test-dir build --output-on-failure`
3. **Run sanitizers** — ASan + UBSan build must pass with zero findings
4. **Run clang-tidy** — static analysis must produce zero warnings on changed files
5. **Check CODEOWNERS** — `include/project/domain/` owned by domain team; `src/infrastructure/` owned by platform team

## Governance Gate

Per [ENG-4.1](laws/engineering/eng-4-testing.md), a PR with production code changes but no corresponding test changes is a **blocking violation**.

## C++ Specific Patterns

- Use `--gtest_filter` to run only tests related to changed files during local development
- CI should build both Debug (sanitizers) and Release (optimization) configurations
- Coverage gate: new code must meet or exceed repository coverage threshold (per [ENG-4.2](laws/engineering/eng-4-testing.md))

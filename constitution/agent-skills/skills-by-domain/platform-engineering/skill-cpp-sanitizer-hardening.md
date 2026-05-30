---
skill:
  id: skill-cpp-sanitizer-hardening
  name: "C++ Sanitizer Hardening"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
  references:
    - id: ENG-4.1
      title: Atomic TDD Law
    - id: ENG-4.2
      title: Test Pyramid Law

triggers:
  phrases:
    - "C++ sanitizer configuration"
    - "C++ ASan UBSan"
    - "C++ ThreadSanitizer"
    - "C++ memory error detection"

followed_by:
  - skill-cpp-ownership-lifetime-safety
  - skill-27-constitution-compliance
---

# Skill: C++ Sanitizer Hardening

## Purpose

Ensure sanitizer-gated CI catches memory errors, undefined behavior, and data races before they reach production. Per [ENG-6.1](laws/engineering/eng-6-security.md), these are mandatory design-time safety checks.

## Procedure

1. **Configure mandatory sanitizers** — AddressSanitizer (ASan) and UndefinedBehaviorSanitizer (UBSan) must be enabled in CI Debug builds
2. **Configure recommended sanitizers** — ThreadSanitizer (TSan) for concurrent code paths
3. **Set compiler flags** — `-fsanitize=address,undefined -fno-omit-frame-pointer` for ASan+UBSan; `-fsanitize=thread` for TSan (mutually exclusive with ASan)
4. **Gate on zero findings** — any sanitizer report is a blocking CI failure
5. **Suppress known false positives** — use sanitizer suppression files (`asan_suppressions.txt`) only with documented justification

## Governance Gate

Per [ENG-6.1](laws/engineering/eng-6-security.md), shipping code that fails ASan or UBSan is a **blocking violation**. TSan failures on concurrent code paths are blocking unless the path has a documented lock-free justification.

## C++ Specific Patterns

- Run sanitizer builds as a separate CI matrix entry (Debug + sanitizers)
- Use `ASAN_OPTIONS=detect_leaks=1` for leak detection on Linux
- Combine with Mull mutation testing for maximum defect detection coverage

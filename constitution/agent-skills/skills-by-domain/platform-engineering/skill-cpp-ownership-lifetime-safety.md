---
skill:
  id: skill-cpp-ownership-lifetime-safety
  name: "C++ Ownership and Lifetime Safety"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-6.1
      title: Security by Design Law (NON-NEGOTIABLE)
    - id: ENG-6.4
      title: Data Protection Law (NON-NEGOTIABLE)
  references:
    - id: ENG-3.2
      title: Immutability Law

triggers:
  phrases:
    - "C++ memory safety"
    - "C++ ownership model"
    - "C++ lifetime management"
    - "C++ smart pointers"
    - "C++ RAII pattern"

followed_by:
  - skill-10-security-review
  - skill-cpp-sanitizer-hardening
---

# Skill: C++ Ownership and Lifetime Safety

## Purpose

Enforce ownership-first API design so that memory safety issues are caught at compile time rather than runtime. Per [ENG-6.1](laws/engineering/eng-6-security.md), security is a design constraint, not an afterthought.

## Procedure

1. **Audit raw pointers** — every `new` must have a corresponding smart pointer wrapper; raw `delete` is forbidden in application code
2. **Verify RAII** — all resources (memory, file handles, locks, network connections) must be released via destructor, not manual cleanup
3. **Check ownership transfer** — `std::unique_ptr` for exclusive ownership, `std::shared_ptr` only when shared lifetime is genuinely required
4. **Validate non-owning views** — use `std::span` or `std::string_view` for borrowed references; never store a view beyond the owner's lifetime

## Governance Gate

Per [ENG-6.1](laws/engineering/eng-6-security.md), any raw owning pointer (`new` without smart pointer) in production code is a **blocking violation**. Exceptions require documented unsafe boundary approval.

## C++ Specific Patterns

- Factory functions return `std::unique_ptr<T>` (not raw `T*`)
- Aggregate roots own children via `std::vector<std::unique_ptr<Child>>`
- Use `[[nodiscard]]` on factory functions to prevent leak-by-ignore
- Const references for read-only access; move semantics for ownership transfer

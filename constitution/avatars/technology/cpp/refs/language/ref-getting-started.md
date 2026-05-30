---
cpp_version_min: 11
cpp_version_note: >-
  C++ fundamentals glossary; RAII, UB, ADL; C++11 baseline.
avatar: cpp
---

# C++ Avatar Reference: Getting Started


---
## Glossary for Java Developers

C++ uses acronyms extensively. This table maps each to its Java equivalent (or notes when there is none).

| Acronym | Full Name | What It Means | Java Equivalent |
|---------|-----------|---------------|-----------------|
| RAII | Resource Acquisition Is Initialization | Objects manage resources via constructor/destructor. When the object goes out of scope, the resource is released automatically. | `try-with-resources` (but RAII is automatic — no syntax needed) |
| UB | Undefined Behavior | The program has no defined semantics — the compiler may do anything. There is no equivalent in Java; Java defines behavior for all operations. | No equivalent — Java has defined behavior for everything |
| ADL | Argument-Dependent Lookup | The compiler searches for functions in the namespaces of the function's argument types. This can cause surprising overload resolution. | No equivalent — Java resolves methods via class hierarchy only |
| ODR | One Definition Rule | Every entity (class, function, template) must have exactly one definition across all translation units. Violating this is UB. | Java's classloader handles this automatically |
| SFINAE | Substitution Failure Is Not An Error | When template argument substitution fails, the compiler silently discards that overload instead of producing an error. Used for compile-time dispatch. Being replaced by C++20 concepts. | No equivalent — Java generics don't have this mechanism |
| NVI | Non-Virtual Interface | A design pattern where public methods are non-virtual and delegate to private/protected virtual methods. Controls how subclasses can customize behavior. | Template Method pattern (`abstract` methods called from concrete methods) |
| PIMPL | Pointer to Implementation | A technique to hide implementation details behind a pointer, reducing compilation dependencies and providing ABI stability. | No direct equivalent — Java interfaces serve a similar decoupling purpose |
| CRTP | Curiously Recurring Template Pattern | A class inherits from a template parameterized by itself: `class Flight : Base<Flight>`. Enables compile-time polymorphism. | No equivalent — Java uses runtime polymorphism only |
| PMR | Polymorphic Memory Resource | C++17 allocator framework that lets you swap memory allocation strategies without changing container types. | No equivalent — JVM manages memory |
| RVO/NRVO | (Named) Return Value Optimization | Compiler optimization that constructs return values directly in the caller's memory, eliminating copies. Guaranteed in C++17 for RVO. | JIT compiler handles this transparently |
| SRP | Single Responsibility Principle | Each class/function should have one reason to change. Same concept as in Java. | Same — SRP is language-agnostic |
| DDD | Domain-Driven Design | Modeling software around business domains using Entities, Value Objects, Aggregates, and Domain Events. | Same — DDD is language-agnostic |

## Quick-Start Guide

> **New here?** Use this decision tree to find the right section immediately.

<a name="brownfield-entry-path"></a>
### Brownfield Entry Path

> For existing codebases (like CWR) adopting the constitution. C++03/C++11 baseline supported.

**5-step onboarding:**

1. **Audit** — Run `skill-cpp-compliance-rating` to get a baseline score across all 10 dimensions. Document in `MODERNIZATION_PLAN.md`.
2. **Freeze** — Stop adding new anti-patterns. Enable `-Wall -Wextra` in CI as a non-failing warning gate.
3. **Modernize in slices** — Per [ENG-2.3](laws/engineering/eng-2-architecture.md), each PR modernizes one vertical slice. Never refactor the whole file.
4. **Gate** — After each dimension reaches ≥ 4/5, add it to the CI compliance gate. Use SonarQube + sonar-cxx for automated MISRA/DO-278A checks.
5. **Graduate** — When all 10 dimensions reach ≥ 4/5 and zero NON-NEGOTIABLE violations remain, the project is Compliant. Update `MODERNIZATION_PLAN.md` to reflect.

**CWR-specific constraints:**
- C++03 in solver core: use error code enums, no exceptions, manual RAII
- C++11 in JNI layer: `unique_ptr`, `noexcept`, `enum class`
- ALP/MFC UI layer: governed by separate avatar (contact platform-engineering team)
- Legacy test harness (CppUnit): new tests must use GoogleTest; existing tests may remain

<a name="skill-decision-tree"></a>
### Which Skill Do I Use?

```
Is this new code or brownfield?
├── New code (greenfield)
│   ├── Start with: 06-atomic-tdd
│   ├── Design: 04-business-domain-modeling
│   └── Review: 08-code-review
└── Brownfield (existing codebase)
    ├── First: skill-cpp-compliance-rating  (get baseline score)
    ├── Safety-critical (DO-278A)?
    │   └── Add: [ENG-6.1](laws/engineering/eng-6-security.md)-misra-do278a example  (MISRA rules + DO-278A level)
    ├── Modernization goal?
    │   ├── Memory safety  → skill-cpp-ownership-lifetime-safety
    │   ├── Thread safety  → skill-cpp-concurrency-thread-safety-governance
    │   ├── Legacy C++03   → skill-cpp-legacy-code-navigation
    │   ├── JNI boundary   → skill-cpp-jni-bridge
    │   └── Build/CI       → skill-cpp-portable-build-governance
    └── Reviewing code?    → 08-code-review + skill-27-constitution-compliance
```

### I'm starting a greenfield C++ project

1. Read [C++ Version Policy](#c-version-policy) — C++20 minimum, C++23 recommended
2. Read [Safety and Ownership](#safety-and-ownership) — smart pointers, RAII, `std::span`
3. Read [CI Quality Toolchain Policy](#ci-quality-toolchain-policy) — mandatory gates (clang-tidy, ASan, UBSan)
4. Follow [Testing Framework](#testing-framework) — RED-GREEN-REFACTOR per [ENG-4.1](laws/engineering/eng-4-testing.md)
5. If safety-critical: read [Safety-Critical C++ (MISRA / DO-178C / JSF AV)](#safety-critical-c-misra-c--do-178c--jsf-av-c)

### I'm adopting the constitution for a brownfield codebase

1. Start with [Brownfield Migration](#brownfield-migration) — compliance rating + team notification
2. Read [Legacy Code Navigation for New Engineers](#legacy-code-navigation-for-new-engineers) — CI first, then incremental modernization
3. Check your standard tier in [Standard Tiers](#per-tier-clang-tidy-configuration) — different rules per tier
4. Use [Migration Playbooks](#migration-playbook-c9803--c11) for your specific upgrade path
5. Schedule [Periodic Re-Rating](#compliance-re-rating-cadence) to track improvement

### I'm a Java developer new to C++

1. **Start here:** [Glossary for Java Developers](#glossary-for-java-developers) — decode C++ acronyms
2. **Critical:** [Mental Model Transitions](#mental-model-transitions) — 13 conceptual gaps between Java and C++
3. Read [Survival Patterns](#survival-patterns) — week-1 through month-6 progression
4. Use [Legacy Codebase Triage Playbook](#legacy-codebase-triage-playbook) — your first-week roadmap
5. Reference [Legacy Code Smell Catalog](#legacy-code-smell-catalog) — recognize and fix structural problems
6. Learn [Cast Governance](#cast-governance) — Java casts are safe; C++ casts can be UB
7. Learn [Object Design Rehabilitation](#object-design-rehabilitation) — fix design-level debt

> **⚠️ Top 5 Java→C++ traps** (read these sections first):
> - `volatile` does NOT mean thread-safe → [§9 volatile](#9-volatile--it-does-not-mean-what-you-think)
> - Lambda `[&]` captures can dangle → [§12 Lambda Captures](#12-lambda-captures--there-is-no-garbage-collector)
> - No checked exceptions, no `finally` → [§11 Exception Handling](#11-exception-handling--no-checked-exceptions-no-finally-no-synchronized)
> - C-style casts can silently reinterpret memory → [Cast Governance](#cast-governance)
> - Templates ≠ Generics → [§10 Generics vs Templates](#10-generics-vs-templates--compile-time-code-generation)

### I need to rate a codebase

1. Read [Constitution Compliance Rating](#constitution-compliance-rating) — 10-dimension rubric
2. Use `skill-cpp-compliance-rating` for the step-by-step assessment procedure
3. See [compliance-rating-system.md](compliance-rating-system.md) for the full 818-line specification

---

## C++ Version Policy

Per the Q3 stakeholder decision:

**Greenfield projects:**
- **C++20 minimum** (mandatory) — enables concepts, ranges, coroutines, `std::span`, three-way comparison
- **C++23 recommended** where toolchain support is verified — adds `std::expected`, `std::print`, deducing `this`
- Must declare target standard in `CMakeLists.txt` via `CMAKE_CXX_STANDARD`

**Brownfield projects:**
- Older standards (C++11, C++14, C++17) are permitted during staged modernization
- Must document a **modernization plan** with milestones toward C++20+
- Modernization proceeds module-by-module — no wholesale rewrite required
- Each modernization milestone must include test equivalence verification
- Compiler upgrade path must be documented (target: GCC 12+, Clang 15+, or MSVC 19.34+)

**Enforcement:**
- `clang-tidy` checks should flag deprecated patterns from older standards
- CI should verify `CMAKE_CXX_STANDARD` matches the declared policy

---

## See Also

- [Core Language Patterns](ref-core-language.md)
- [Domain Modeling & Safety](ref-domain-modeling.md)

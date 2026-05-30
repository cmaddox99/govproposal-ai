---
cpp_version_min: 98
cpp_version_note: >-
  MISRA C++ and DO-178C apply to legacy safety-critical codebases starting from C++98/03.
avatar: cpp
---

# C++ Avatar Reference: Safety-Critical C++ - MISRA and DO-178C

---

## Safety-Critical C++ (MISRA C++ / DO-178C / JSF AV C++)

> **Applicability:** This section applies to C++ code in systems subject to FAA certification, safety-critical avionics software, ground-based aviation systems (crew scheduling, dispatch, weight/balance), or any component where software failure could impact flight safety. Per [ENG-6.1](laws/engineering/eng-6-security.md) (Security by Design), legal and regulatory compliance takes priority over all other concerns.

### MISRA C++ Overview

[MISRA C++:2023](https://misra.org.uk/) (formerly MISRA C++:2008) defines coding guidelines for safety-critical and high-reliability C++ systems. American Airlines systems that interface with flight operations, crew scheduling, or aircraft maintenance systems should evaluate MISRA compliance.

#### MISRA Categories Mapped to Constitutional Laws

| MISRA Category | Constitutional Law | Governance |
|----------------|-------------------|------------|
| Memory management (no dynamic allocation in critical paths) | [ENG-6.1](laws/engineering/eng-6-security.md) | MISRA prohibits `new`/`delete` in critical code; use stack allocation or pre-allocated pools |
| Exception handling (restricted or prohibited) | [ENG-7.1](laws/engineering/eng-7-reliability.md) | MISRA restricts exceptions in DAL A/B; use error codes or `std::expected` |
| RTTI (`dynamic_cast`, `typeid`) restrictions | [ENG-3.1](laws/engineering/eng-3-code-quality.md) | MISRA discourages RTTI; use static polymorphism (CRTP, concepts) |
| Pointer arithmetic restrictions | [ENG-6.1](laws/engineering/eng-6-security.md) | MISRA limits pointer arithmetic; use `std::span` or iterators |
| Implicit conversions prohibited | [ENG-3.1](laws/engineering/eng-3-code-quality.md) | Mark constructors `explicit`; enable `-Wconversion` |
| Macro restrictions | [ENG-3.1](laws/engineering/eng-3-code-quality.md) | Minimize preprocessor use; prefer `constexpr` and `if constexpr` |
| Concurrency rules | [ENG-6.1](laws/engineering/eng-6-security.md) | Use `std::atomic` and `std::mutex`; no volatile for synchronization |
| Static analysis required | [ENG-5.2](laws/engineering/eng-5-devops.md) | MISRA mandates tool-enforced checking; clang-tidy + custom MISRA checks |

#### MISRA Enforcement in CI

```yaml
# .clang-tidy addition for MISRA-aligned projects
Checks: >
  -*,
  bugprone-*,
  cert-*,
  cppcoreguidelines-*,
  misc-misra-*,
  -cppcoreguidelines-avoid-magic-numbers
```

For full MISRA compliance, supplement clang-tidy with dedicated MISRA tools:
- **Parasoft C/C++test** — certified MISRA checker
- **LDRA TBvision** — DO-178C qualified tool suite
- **PC-lint Plus** — MISRA rule enforcement

### JSF AV C++ (Joint Strike Fighter Air Vehicle)

[JSF AV C++](https://www.stroustrup.com/JSF-AV-rules.pdf) is a C++ coding standard developed by Lockheed Martin for the F-35 program. It defines a **safe, analyzable subset of C++** for aerospace and defense systems. While created for military avionics, its rules are directly applicable to safety-critical airline systems.

> **When to use JSF AV C++ vs MISRA:** MISRA C++:2023 is the broader industry standard. JSF AV C++ is stricter and more prescriptive — it specifies exact function size limits, complexity ceilings, and feature bans. Use JSF AV C++ rules for DAL A/B systems; use MISRA for DAL C/D.

#### JSF AV C++ Key Restrictions

| Rule | JSF Requirement | Constitutional Mapping |
|------|----------------|----------------------|
| Exception handling | ❌ Forbidden | Aligns with DAL A/B restrictions (see below) |
| Dynamic allocation (`new`/`delete`/`malloc`) | ❌ Forbidden | [ENG-6.1](laws/engineering/eng-6-security.md) — use stack or pre-allocated pools |
| Recursion | ❌ Forbidden | Prove termination statically |
| RTTI (`dynamic_cast`, `typeid`) | ❌ Forbidden | [ENG-3.1](laws/engineering/eng-3-code-quality.md) — use static polymorphism |
| Multiple inheritance | Severely restricted | Document rationale for any use |
| Templates | Restricted (simple use only) | [ENG-3.1](laws/engineering/eng-3-code-quality.md) — constrain with concepts |
| Function size | ≤ 200 logical lines | [ENG-3.1](laws/engineering/eng-3-code-quality.md) complexity limits |
| Cyclomatic complexity | ≤ 20 per function | [ENG-3.1](laws/engineering/eng-3-code-quality.md) complexity limits |
| Macros | Include guards only | [ENG-3.1](laws/engineering/eng-3-code-quality.md) — use `constexpr` |
| Standard library | Safe subset only | No unbounded containers in critical paths |

#### JSF AV C++ Enforcement

```yaml
# Static analysis tools with JSF AV C++ rule support:
- Parasoft C/C++test    # Full JSF++ rule coverage
- Polyspace Bug Finder  # MathWorks — JSF rule checking
- QA·C++               # QA Systems — JSF + MISRA combined
- PC-lint Plus          # Gimpel — JSF subset rules
```

> **Java developer note:** JSF AV C++ essentially bans the C++ features that make it different from Java — exceptions, dynamic allocation, RTTI, templates. If you're a Java developer writing safety-critical C++, JSF rules will feel familiar: the resulting code resembles "C with classes" rather than modern C++. This is intentional — predictability over expressiveness.

### DO-178C Design Assurance Levels

[DO-178C](https://en.wikipedia.org/wiki/DO-178C) (*Software Considerations in Airborne Systems and Equipment Certification*) defines 5 Design Assurance Levels (DAL) based on failure severity:

| DAL | Failure Condition | C++ Governance Impact |
|-----|-------------------|----------------------|
| **Level A** — Catastrophic | Could cause crash | No dynamic memory, no exceptions, no RTTI, 100% MC/DC coverage, MISRA mandatory |
| **Level B** — Hazardous | Could cause serious injury | Restricted dynamic memory (pre-allocated pools), restricted exceptions, ≥95% MC/DC |
| **Level C** — Major | Could cause discomfort | Smart pointers permitted, exceptions with `noexcept` boundaries, ≥90% statement coverage |
| **Level D** — Minor | Could cause inconvenience | Standard constitution governance applies, ≥80% statement coverage |
| **Level E** — No Effect | No safety impact | Standard constitution governance, normal coverage per [ENG-4.2](laws/engineering/eng-4-testing.md) |

#### DAL-Specific C++ Restrictions

**DAL A/B (safety-critical):**
- ❌ No `new`/`delete` — use stack allocation or pre-allocated memory pools
- ❌ No exceptions — use error return codes or `std::expected` with `-fno-exceptions`
- ❌ No RTTI — compile with `-fno-rtti`
- ❌ No recursive functions — prove termination statically
- ✅ All functions must have documented worst-case execution time (WCET)
- ✅ Full MC/DC (Modified Condition/Decision Coverage) required per [ENG-4.2](laws/engineering/eng-4-testing.md)
- ✅ All MISRA C++ rules mandatory (no deviations without FAA-accepted rationale)

**DAL C (major):**
- ✅ Smart pointers permitted (`unique_ptr`, `shared_ptr`)
- ✅ Exceptions permitted within defined `noexcept` boundaries
- ❌ No unbounded recursion
- ✅ Statement + branch coverage ≥90%
- ✅ MISRA rules advisory (deviations documented)

**DAL D/E (minor/no effect):**
- Standard constitution governance applies
- MISRA rules recommended but not mandatory
- Coverage per [ENG-4.2](laws/engineering/eng-4-testing.md) test pyramid

### Aviation-Specific Compliance Mapping

Per [ENG-6.1](laws/engineering/eng-6-security.md), American Airlines C++ systems must address:

| Regulation | Requirement | C++ Implementation |
|------------|-------------|-------------------|
| **FAA FAR Part 117** | Crew rest calculations must be correct | Characterization tests + formal verification for scheduling algorithms |
| **FAA DO-178C** | Software assurance for airborne systems | DAL-appropriate governance (see above) |
| **FAA DO-278A** | Software assurance for ground-based CNS/ATM systems | Similar DAL structure to DO-178C; applies to dispatch, crew scheduling, ground ops systems |
| **TSA Security Directives** | Vetting and access control | Compile with `-fstack-protector-strong`, ASLR, per [ENG-6.1](laws/engineering/eng-6-security.md) |
| **DOT Consumer Protection** | Fare calculation accuracy | Golden-file testing for fare engines per [ENG-4.1](laws/engineering/eng-4-testing.md) |
| **IATA DGR** | Dangerous goods data integrity | Input validation, bounds checking per [ENG-6.4](laws/engineering/eng-6-security.md) |

### When to Apply Safety-Critical Governance

Not all American Airlines C++ code requires MISRA/DO-178C. Use this decision tree:

```
Does this code run on or directly interface with aircraft systems?
├── YES → Apply full DO-178C governance at appropriate DAL
│         └── Engage FAA DER (Designated Engineering Representative)
└── NO → Is this a ground-based aviation system (CNS/ATM, dispatch, crew scheduling)?
    ├── YES → Apply DO-278A governance at appropriate Assurance Level (AL)
    │         └── Does this code handle safety-related calculations?
    │             ├── YES (crew rest, weight/balance, fuel) → Apply MISRA advisory rules + DAL C governance
    │             └── NO → Apply DO-278A AL 4-6 + standard constitution governance
    └── NO → Does this code handle safety-related calculations?
        ├── YES (crew scheduling, weight/balance, fuel) → Apply MISRA advisory rules + DAL C governance
        └── NO → Standard constitution governance applies
```

---


---

## See Also

- [Memory Lifetime and FFI Safety](ref-safety-memory-lifetime.md)

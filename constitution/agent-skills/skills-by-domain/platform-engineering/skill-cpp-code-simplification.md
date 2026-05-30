---
skill:
  id: skill-cpp-code-simplification
  name: "C++ Code Simplification Advisor"
  category: platform-engineering
  version: "1.0.0"
  avatar: cpp

laws:
  implements:
    - id: ENG-3.1
      reason: "Reduces complexity by suggesting simpler alternatives to advanced patterns"
    - id: ENG-1.3
      reason: "Boy Scout Rule — leave code simpler than you found it"
    - id: ENG-3.8
      reason: "Refactoring patterns — systematic simplification"
  references:
    - id: ENG-6.1
      reason: "Simpler code has fewer security vulnerabilities (memory safety)"
    - id: ENG-4.1
      reason: "Simpler code is easier to test atomically"
    - id: ENG-3.4
      reason: "SRP — simplified components have clearer responsibilities"
    - id: ENG-2.5
      reason: "Dependency inversion enables replacement of complex with simple"

triggers:
  phrases:
    - "simplify this C++ code"
    - "C++ code too complex"
    - "simpler alternative for C++"
    - "reduce C++ complexity"
    - "refactor C++ to simpler"
    - "modernize legacy C++ patterns"
    - "replace template metaprogramming"
    - "simplify C++ inheritance"
    - "make C++ code easier to understand"
    - "C++ code review simplification"

followed_by:
  - "skill-cpp-template-complexity-management"
  - "skill-cpp-exception-safety-governance"

---

# C++ Code Simplification Advisor

## Purpose

This skill analyzes C++ code and recommends simpler, equally effective alternatives. It operationalizes the principle that **the best C++ code is the simplest code that meets the requirements** — advanced patterns are tools for specific problems, not defaults.

## When to Invoke

- During code review when advanced patterns are detected
- When a developer asks "is there a simpler way?"
- When complexity metrics exceed thresholds (cyclomatic > 15, template depth > 3)
- When onboarding new team members to complex codebases

## Simplification Rules

### Tier 1: Always Simplify (No Justification Needed)

| Complex Pattern | Simple Alternative | Why |
|----------------|-------------------|-----|
| `std::auto_ptr` | `std::unique_ptr` | Deprecated, dangerous copy semantics |
| SFINAE (`enable_if`) | C++20 concepts | Better error messages, clearer intent |
| Manual `new`/`delete` | Smart pointers | RAII eliminates leak/double-free |
| `void*` type erasure | `std::any` or `std::variant` | Type-safe, no casts |
| Raw mutex lock/unlock | `std::scoped_lock` | Exception-safe, no deadlock risk |
| C-style casts | `static_cast`/`dynamic_cast` | Intention is visible, compiler checks |
| `#define` constants | `constexpr` | Type-safe, scoped, debuggable |
| Manual iterator loops | Range-for or `<algorithm>` | Less error-prone, self-documenting |

### Tier 2: Simplify Unless Justified

| Complex Pattern | Simple Alternative | When Complex Is Justified |
|----------------|-------------------|--------------------------|
| Multiple inheritance | Composition + delegation | Only for mixin/policy patterns with compile-time combination |
| CRTP | Virtual dispatch | Only when profiler proves vtable overhead matters (>100K calls/sec) |
| Template metaprogramming | `if constexpr` | Only when compile-time computation is required |
| Placement new | `std::optional` / PMR | Only for custom allocators or hardware-mapped memory |
| Custom allocator | `std::pmr::*` | Only when PMR doesn't provide required allocator policy |
| `std::function` | Template parameter | Only when callable must be stored (not just passed) |
| Protected/private inheritance | Composition | Only when virtual method override is needed |
| Variadic templates (recursive) | Fold expressions | Only pre-C++17 code |

### Tier 3: Warn But Allow

| Advanced Pattern | Warning | When Appropriate |
|-----------------|---------|-----------------|
| Coroutines | "Ensure coroutine library is stable" | Async I/O, generator patterns |
| Modules (C++20) | "Compiler support varies" | Large projects with long build times |
| `std::launder` | "Rarely needed — check if std::optional works" | Storage reuse with const/ref members |
| Custom `operator new` | "Profile first — global allocator may suffice" | Arena allocation with measured benefit |

## Procedure

When analyzing code for simplification:

1. **Scan** — Identify all Tier 1/2/3 patterns in the code under review
2. **Categorize** — For each pattern, determine tier and check if justification exists
3. **Recommend** — For unjustified complex patterns, propose the simple alternative with a code example
4. **Preserve** — Do NOT simplify justified patterns; instead, add a `// Justified: <reason>` comment
5. **Test** — Ensure simplified code passes existing tests; if no tests exist, write characterization tests first per [ENG-4.1](laws/engineering/eng-4-testing.md)

## Example Recommendations

### Multiple Inheritance → Composition

```
DETECTED: class CombinedLog : public FlightLog, public CrewLog
RECOMMENDATION: Extract shared behavior into a component class.
  Replace inheritance with member variables (HAS-A).
  See: guidance.md ## Object Design Rehabilitation
TIER: 2 — simplify unless MI provides compile-time mixin combination
```

### SFINAE → Concepts

```
DETECTED: template <typename T, typename = std::enable_if_t<std::is_integral_v<T>>>
RECOMMENDATION: Replace with C++20 concept constraint.
  template <std::integral T> void process(T val);
  See: guidance.md ## Template and Metaprogramming Governance
TIER: 1 — always simplify (if C++20 available)
```

### Raw Pointer → Smart Pointer

```
DETECTED: FlightPlan* plan = new FlightPlan(origin, dest);
RECOMMENDATION: Use std::make_unique for ownership.
  auto plan = std::make_unique<FlightPlan>(origin, dest);
  See: guidance.md ## Safety and Ownership
TIER: 1 — always simplify
```

## Metrics

After applying this skill, track:
- **Simplification ratio:** number of Tier 1/2 patterns simplified vs total detected
- **Test coverage delta:** coverage before/after simplification (should not decrease)
- **Build time impact:** template simplification typically reduces compile time

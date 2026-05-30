---
law_id: ENG-6.1
cpp_version_min: 11
avatar: cpp
title: MISRA C++ and DO-278A Safety-Critical Standards
tokens: ~520
---

# ENG-6.1 MISRA C++ and DO-278A Safety-Critical Standards

**Law:** ENG-6.1 (Security by Design — Non-Negotiable)  
**Avatar:** `avatars/technology/cpp/`  
**Context:** DO-278A governs ground-based CNS/ATM software (e.g., crew scheduling systems
that affect flight operations). MISRA C++ provides the coding standard that satisfies
DO-278A's software quality objectives. These are cited as *engineering constraints*
under ENG-6.1 — not as business laws (per Safeguard 2: technology avatars specialize ENG-* only).

---

## COMPLIANT Patterns

### 1. MISRA C++ Rule 0-1-11 — Unused Variables

```cpp
// MISRA C++ 0-1-11: Every declared variable must be used
// COMPLIANT
CrewError assign_crew(FlightId flight, CrewId crew) noexcept {
    CrewError result = roster_.assign(flight, crew);  // result is used below
    if (result != CrewError::None) {
        spdlog::warn("assign_failed", spdlog::arg("crew", crew.value()));
    }
    return result;
}

// NON-COMPLIANT — MISRA 0-1-11 violation
void log_flight(FlightId flight) {
    std::string name = lookup_name(flight);  // declared but never used
    spdlog::info("flight_logged");
}
```

### 2. MISRA C++ Rule 5-0-15 — Array Indexing via Pointer

```cpp
// MISRA C++ 5-0-15: Array indexing must use subscript operator, not pointer arithmetic
// COMPLIANT
void process(const std::vector<Crew>& crew) {
    for (std::size_t i = 0; i < crew.size(); ++i) {
        process_one(crew[i]);              // subscript operator ✓
    }
}

// NON-COMPLIANT
void process_bad(const Crew* crew, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) {
        process_one(*(crew + i));          // pointer arithmetic — MISRA 5-0-15 violation
    }
}
```

### 3. DO-278A Assurance Level Mapping

```cpp
// DO-278A Assurance Level B (ground-based CNS/ATM supporting ATC):
// - All safety-critical functions must be traceable to requirements
// - Static analysis (MISRA C++) is a recognised means of compliance
// - Use SonarQube + sonar-cxx with MISRA C++ ruleset for automated enforcement

// Crew scheduling domain: ASSURANCE LEVEL B applies when output feeds ATC displays
// Crew scheduling domain: ASSURANCE LEVEL C applies for internal crew ops tools

// Example: mark level in function doc-comment for traceability
/// @safety DO-278A-B: result feeds real-time crew status to ATC display
CrewStatus get_crew_status(CrewId crew) const noexcept;
```

---

## NON-COMPLIANT Patterns

| Anti-Pattern | MISRA Rule | Fix |
|---|---|---|
| `reinterpret_cast` in safety path | 5-2-7 | Use `static_cast` or redesign |
| Exception in safety-critical function | 15-0-1 | Mark `noexcept`, use error codes |
| Dynamic allocation after init | 18-4-1 | Pre-allocate in constructor |
| `goto` statement | 6-6-1 | Restructure with early returns |

---

## CWR Brownfield Path

CWR operates at **DO-278A Assurance Level B** for crew scheduling outputs fed to ATC.
1. Enable MISRA C++ ruleset in SonarQube (sonar-cxx plugin)
2. Prioritise rules: 0-1-x (unused code), 5-0-x (expressions), 15-x (exceptions)
3. Use `// MISRA_DEVIATION(rule, justification)` macro for approved deviations
4. All deviations require engineering lead sign-off per ENG-6.7

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Static analysis tool reports Rule 11.3 violation on driver pointer cast | Rule 11.3 forbids casting between pointer-to-object types; legacy drivers require it | Raise a formal deviation with justification; add `MISRA_DEVIATION(11-3, "hardware register access — approved DD-XXXX")` comment |
| `MISRA_DEVIATION` macro used without a linked deviation record | Suppression recorded in source but not in the deviation log; audit fails | Require the macro argument to contain a document ID; enforce via CI grep check on all new suppressions |
| Importing a third-party C library that itself violates MISRA | All TUs in the translation unit are analysed; vendor headers trigger hundreds of violations | Wrap vendor headers in a `#pragma clang diagnostic push/pop` exclusion zone and document as a blanket deviation in the project deviation register |
| DO-278A AL classification mismatch between component and calling system | A component compiled at AL-C linked into an AL-B system inherits the stricter requirement | Document AL at the component boundary in CMake target metadata; CI must reject mismatched links |

---
law_id: ENG-4.1
cpp_version_min: 98
avatar: cpp
title: FAR 117 Test Traceability
tokens: ~380
---

# ENG-4.1 FAR 117 Test Traceability — C++ Patterns

**Law:** ENG-4.1 (Atomic TDD Law — Non-Negotiable)  
**Avatar:** `avatars/technology/cpp/`  
**Context:** FAR Part 117 governs crew rest and duty time for commercial flight operations.
Tests covering crew scheduling logic that enforces FAR 117 must include regulation citations
in their names so traceability from test → regulation is explicit and auditable (ENG-6.7).

---

## COMPLIANT Patterns

### 1. Test Name Encodes the Regulation

```cpp
// Naming convention: TestSuite_Scenario_FARXXX_YY
// FAR 117.23(a): Minimum 9-hour rest period before a flight duty period
TEST(CrewRestPolicy, MinimumRestBeforeFDP_FAR117_23a) {
    CrewId crew{42};
    FlightDutyPeriod fdp{TimePoint::now()};
    // Crew with only 8.5 hours rest must be rejected
    auto result = rest_policy_.approve(crew, fdp, Hours{8.5});
    EXPECT_EQ(result, RestDecision::Rejected);
    EXPECT_EQ(result.regulation(), "FAR 117.23(a)");
}

// FAR 117.25(b): Maximum 9-hour flight duty period (Class 1 rest)
TEST(CrewRestPolicy, MaxFDPWithClass1Rest_FAR117_25b) {
    CrewId crew{42};
    auto fdp = FlightDutyPeriod::ofDuration(Hours{9.5});
    auto result = rest_policy_.approve_fdp(crew, fdp, RestClass::Class1);
    EXPECT_EQ(result, FDPDecision::Rejected);
}
```

### 2. Traceability Matrix Comment Block

```cpp
// FAR 117 Traceability Matrix — CrewRestPolicyTest
// ┌─────────────────────────────────┬──────────────┬─────────────────────────────────┐
// │ Test name                       │ Regulation   │ Requirement                     │
// ├─────────────────────────────────┼──────────────┼─────────────────────────────────┤
// │ MinimumRestBeforeFDP_FAR117_23a │ FAR 117.23(a)│ Min 9-hr rest before FDP        │
// │ MaxFDPWithClass1Rest_FAR117_25b │ FAR 117.25(b)│ Max FDP with Class 1 rest       │
// │ CumulativeDutyLimit_FAR117_29   │ FAR 117.29   │ 60-hr cumulative duty in 168 hr │
// └─────────────────────────────────┴──────────────┴─────────────────────────────────┘
```

---

## NON-COMPLIANT Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `TEST(CrewRest, TooTired)` | No regulation citation — untraceable | `TEST(CrewRest, TooTired_FAR117_23a)` |
| Test passes with no assertion on regulation | Does not prove which rule is enforced | Assert `.regulation()` value |
| Generic `TEST(Policy, Valid_Invalid)` | Cannot link to compliance audit | Encode the specific FAR section |

---

## CWR Integration with D10 (Compliance Rating)

FAR 117 traceability directly feeds Compliance Rating dimension D10 (Regulatory Coverage).
- D10 score ≥ 3 requires: test coverage of FAR 117.23, 117.25, and 117.29 at minimum
- Each regulation section must have ≥ 1 test naming it explicitly
- Auditors may request test output as evidence — test names ARE the audit record

## Edge Cases & Warnings

| Scenario | Risk | Safe Approach |
|----------|------|---------------|
| Test IDs use internal ticket numbers instead of FAR citation format (e.g., `CWR-4521` vs `FAR_117_23_RestPeriod`) | Auditor cannot map test output to regulatory section without a cross-reference table; creates certification delay | Mandate FAR citation format in test names per team naming guide; CI lint rejects test names matching only ticket-ID patterns |
| Duty-period boundary falls at midnight UTC but crew is in a local time zone | `time_point` arithmetic using system clock returns UTC; naive subtraction misses DST transition by 1 hour | Store all duty times in UTC at source; apply time-zone conversion only at display layer; add a boundary test with a `2:00 AM DST fall-back` fixture |
| Traceability artefacts split across two Git repositories (app code + compliance docs) | A commit in the app repo removes a test; compliance-docs repo is not updated; divergence goes undetected until audit | Use a CI job that cross-checks the compliance matrix in the docs repo against test names in the app repo on every PR |
| FAR 117 amendment issued mid-cycle updates rest-period table | Existing tests still pass because they test the old values; no automated link to regulation version | Pin `FAR_117_VERSION = "2024-01-15"` constant in a central file; bump it on each amendment; tests that reference it fail until updated |
| Scheduling algorithm **times out** and returns a default `"approved"` result | A timeout that silently approves crew rest bypasses FAR 117 validation entirely — the scheduler appears to pass while producing illegal pairings | Timeouts must return `RestDecision::kTimeout` (never `kApproved`); the caller must log and escalate, not retry with a cached result |

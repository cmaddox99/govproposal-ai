---
law_id: BUS-2.1
avatar: crew-training-scheduling
---

# BUS-2.1: Regulatory Mapping Law Examples for Crew Training Scheduling

> **Law:** All applicable regulations MUST be identified and mapped to the controls
> that enforce them. For crew training scheduling, FAR Part 117 rules embedded in
> the optimizer's constraint logic MUST be explicitly traced — from regulation to
> constraint method to test to commit.

---

## COMPLIANT: Regulatory Map for JOSE Constraints

```markdown
## Regulatory Mapping (Per BUS-2.1)

| Regulation | Jurisdiction | Applicability | JOSE Control | Owner |
|------------|--------------|---------------|-------------|-------|
| **FAR Part 117.25(b)** | FAA / USA | All Part 121 operations | Minimum 10-hour rest check in `NetworkGenerator.isFeasibleTransition()` | OR Dev |
| **FAR Part 117.23** | FAA / USA | All Part 121 operations | Rolling 7-day working-day window check in `NetworkGenerator.isWithinRollingDayLimit()` | OR Dev |
| **FAA OE Requirements** | FAA / USA | Pilot initial training | `CompletionRequirementDto` from FSA `api/oeinputs/trainings/` — completion reward fires only when hours met | OR Dev |
| **FAR Part 117 Freeze** | Operational policy (FAA-backed) | All scheduling | Freeze window enforcement — sequences within N days of today excluded from options | OR Dev |

### Evidence of Control (Per BUS-2.4)
Each control is evidenced by:
1. Javadoc in the constraint/filter method citing the specific FAR section
2. A baseline scenario in `hangar-ai-specs/specs/mip-model/spec.md` documenting the rule
3. A characterization test that fails if the rule is removed
```

---

## COMPLIANT: FAR Citation in Constraint Method Javadoc

```java
/**
 * Determines whether the transition from {@code fromSequence} to {@code toSequence}
 * satisfies the minimum rest requirement between duty periods.
 *
 * <p><b>Regulation: FAR Part 117.25(b)</b> — A flight crew member must receive a
 * minimum of 10 consecutive hours of rest immediately before a flight duty period.
 *
 * <p>This method enforces the 10-hour minimum rest as a hard feasibility filter
 * during option generation. Options violating this constraint are excluded before
 * the MIP model is built.
 *
 * @param fromSequence the sequence ending the current duty period
 * @param toSequence   the sequence starting the next duty period
 * @return {@code true} if the rest between duty periods is ≥ 10 hours
 */
private boolean satisfiesMinimumRest(Sequence fromSequence, Sequence toSequence) {
    long restHours = ChronoUnit.HOURS.between(
            fromSequence.getLastDutyPeriodEnd(),
            toSequence.getFirstDutyPeriodStart());
    return restHours >= MINIMUM_REST_HOURS; // MINIMUM_REST_HOURS = 10
}
```

**Why compliant:** The Javadoc contains the regulation identifier (FAR Part 117.25(b)) and the specific requirement it enforces. Any future maintainer changing this method knows immediately they are touching an FAR control. Per BUS-2.1 regulatory mapping, the traceability chain is: `FAR 117.25(b) → satisfiesMinimumRest() → NetworkGenerator`.

---

## COMPLIANT: FAR Control Covered by Characterization Test

```java
/**
 * BASE-MIP-FAR-001: FAR Part 117.25(b) — sequences with < 10h rest are excluded.
 *
 * Source: hangar-ai-specs/specs/mip-model/spec.md
 * Regulatory: FAR Part 117.25(b) — minimum 10-hour rest between duty periods
 * Constitutional: ENG-4.1 Atomic TDD, BUS-2.1 Regulatory Mapping
 */
@Test
@DisplayName("BASE-MIP-FAR-001: sequence pair with < 10h rest is not a feasible option")
void generateOptions_sequencePairWithLessThan10hRest_isExcluded() {
    // Given — seq-A ends at 08:00, seq-B starts at 16:00 (only 8h rest — below FAR minimum)
    Sequence seqA = SequenceFixture.endingAt(LocalDateTime.of(2025, 4, 15, 8, 0));
    Sequence seqB = SequenceFixture.startingAt(LocalDateTime.of(2025, 4, 15, 16, 0));
    Student student = StudentFixture.eligible(seqA, seqB);

    // When
    List<StudentOption> options = networkGenerator.generateOptions(student, bundle);

    // Then — no option contains both seqA and seqB in sequence (FAR 117.25(b) violation)
    assertThat(options).noneMatch(o ->
            o.getSequences().contains(seqA) && o.getSequences().contains(seqB));
}
```

**Why compliant:** The test is named with a `BASE-MIP-FAR-*` ID that traces to the baseline spec and the FAR regulation. The regulatory citation is in the Javadoc. If someone removes the rest check from `NetworkGenerator`, this test fails immediately.

---

## VIOLATION: FAR Constraint with No Citation or Traceability

```java
// ❌ VIOLATES BUS-2.1 — FAR constraint buried in logic with no regulatory citation
private boolean canTransition(Sequence from, Sequence to) {
    // some rest check
    long hours = ChronoUnit.HOURS.between(from.getEnd(), to.getStart());
    return hours >= 10;  // why 10? nobody knows without digging into FAR Part 117
}
```

**Why violates BUS-2.1:** The number `10` is a magic number with no regulatory basis documented. A future developer might change it to `8` for performance reasons, unknowingly creating an FAR violation. There is no test asserting this is an FAR control. The regulatory mapping chain is broken.

---

## COMPLIANT: Regulatory Change Management

```markdown
## Process: FAR Regulation Change Affects JOSE

Example: FAA proposes reducing minimum rest to 9 hours for augmented crews.

### Step 1: Update Regulatory Map (BUS-2.1)
- Identify which JOSE methods cite FAR Part 117.25(b)
- Scope: `NetworkGenerator.satisfiesMinimumRest()` and its test

### Step 2: Create Hangar SDD Proposal
hangar-ai-specs/changes/far-117-augmented-crew-rest/proposal.md
- Constitutional authority: BUS-2.1 regulatory mapping
- Scope: satisfiesMinimumRest() + NetworkGenerator tests
- Risk: relaxing rest check may increase infeasible back-to-back options

### Step 3: Update Characterization Test First (ENG-4.4)
- Add BASE-MIP-FAR-002: augmented crew rest is 9 hours
- Run RED (fails with current 10-hour check)
- Update MINIMUM_REST_HOURS constant
- Run GREEN

### Step 4: Update Regulatory Map and Javadoc
- Javadoc: "FAR Part 117.25(b) as amended [date] — augmented crew minimum 9h"
- Regulatory map table updated with new requirement and effective date
```

**Why compliant:** Regulatory changes trigger a documented change proposal with full traceability. The constraint method's Javadoc and the regulatory map are updated together — neither is allowed to fall out of sync.


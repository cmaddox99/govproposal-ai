# Operations Research / MIP Optimizer Guidance

> **Purpose:** Stack-specific agent behaviors for MIP/LP optimization applications.
> **Reference Implementation:** JOSE — Journey Optimization & Spoilage Elimination (`daily-optimizer`)

---

## Overview

This guidance covers AI agent behaviors for applications that use mathematical programming solvers to make optimal decisions. These are typically batch CLI applications — not web services — that ingest data from external APIs, build a mathematical model, solve it, and produce structured output files.

---

## Core Principle: Math First, Code Second

Per **ENG-3.1** and this avatar's constraint-complexity convention:

**ALWAYS formulate constraints in standard mathematical notation BEFORE writing code.**

```
# ✅ CORRECT — Formulate first (in Javadoc or comment)
# Constraint C2: Each sequence q is used by at most one selected option
# ∀q ∈ Q:  Σ_{o ∈ O_q} x_o ≤ 1
private void addSequenceExclusivityConstraint(XpressOptimizer model, ...) { ... }

# ❌ WRONG — Translate English directly to code
private void addConstraint(XpressOptimizer model, ...) {
    // make sure sequences aren't used twice
    ...
}
```

---

## Testing Patterns

### Pattern 1: Constraint Feasibility Test (Per ENG-4.1)

Test that a valid problem produces a feasible solution with a positive objective value.

```java
/**
 * BASE-MIP-001: Valid inputs produce a feasible solution.
 * Constitutional: ENG-4.1 Atomic TDD
 */
@Test
@DisplayName("BASE-MIP-001: valid student options yields feasible solution with positive reward")
void solve_withValidStudentOptions_returnsFeasibleSolutionWithPositiveReward() {
    // Given — minimal valid bundle with one open blocked sequence
    var bundle = OptimizationDataBundleFixture.withOneOpenBlkdSeqAndOneEligibleStudent();

    // When
    optimizationService.findOptimalSolution(bundle, ScoringWeightProfile.standard(), ...);

    // Then — model is feasible and reward is positive
    assertThat(bundle.getSolverStatus()).isEqualTo(SolverStatus.OPTIMAL);
    assertThat(bundle.getObjectiveValue()).isGreaterThan(0.0);
}
```

### Pattern 2: Constraint Infeasibility Test (Per ENG-4.1)

Test that a contradictory problem correctly produces infeasibility — not a silent empty solution.

```java
/**
 * BASE-MIP-002: Contradictory constraints produce infeasibility, not silent empty output.
 * Constitutional: ENG-4.1 Atomic TDD, ENG-6.7 Audit Trail
 */
@Test
@DisplayName("BASE-MIP-002: all sequences frozen produces infeasible or zero-reward solution")
void solve_withAllSequencesFrozen_returnsEmptyOrInfeasible() {
    // Given — all sequences fall within the freeze window
    var bundle = OptimizationDataBundleFixture.withAllSequencesInFreezeWindow();

    // When
    optimizationService.findOptimalSolution(bundle, ScoringWeightProfile.standard(), ...);

    // Then — no student is moved (freeze constraint enforced)
    assertThat(bundle.getStudentResults())
            .allMatch(result -> result.getActionType() == ActionType.UNCHANGED);
}
```

### Pattern 3: Objective Regression Test (Per ENG-4.6)

Prevent scoring regressions when weights or reward logic change.

```java
/**
 * BASE-SCORE-001: Standard profile reward for open blocked sequence assignment.
 * Regression guard — if this breaks, a weight or formula changed.
 * Constitutional: ENG-4.1, ENG-4.6 Coverage Requirements
 */
@Test
@DisplayName("BASE-SCORE-001: open blkd seq reward equals base * day-decay * flight-time weight")
void computeOpenBlkdSeqReward_standardProfile_matchesExpectedFormula() {
    // Given
    var profile = ScoringWeightProfile.standard();
    var option = StudentOptionFixture.withOneOpenBlkdSeq(
            sequenceDaysFromNow(5), flightHours(3.5));

    // When
    double reward = scorer.computeOpenBlkdSeqReward(profile, option, student, bundle);

    // Then — verify against known formula result
    double expected = profile.getOpenBlkdSeqBaseReward()
            * Math.pow(profile.getOpenBlkdSeqDayDecay(), 5)
            * (3.5 * profile.getOpenBlkdSeqFlightTimeWeight());
    assertThat(reward).isCloseTo(expected, within(0.001));
}
```

### Pattern 4: Solution Structure Test (Per ENG-4.1)

Assert that the solver respects the sequence exclusivity constraint.

```java
/**
 * BASE-MIP-003: No sequence appears in more than one selected option.
 * Constitutional: ENG-4.1 Atomic TDD
 */
@Test
@DisplayName("BASE-MIP-003: selected options contain mutually exclusive sequences")
void solve_selectedOptions_containNoSharedSequences() {
    // Given — multiple students competing for overlapping sequences
    var bundle = OptimizationDataBundleFixture.withStudentsCompetingForSameSequence();

    // When
    optimizationService.findOptimalSolution(bundle, ScoringWeightProfile.standard(), ...);

    // Then — no sequence key appears in more than one selected option
    var selectedSequenceKeys = bundle.getSelectedOptions().stream()
            .flatMap(o -> o.getSequenceKeys().stream())
            .collect(Collectors.toList());
    assertThat(selectedSequenceKeys).doesNotHaveDuplicates();
}
```

---

## Constraint Implementation Pattern

Each constraint is one private method. The Javadoc cites the mathematical formulation and, when applicable, the FAR rule.

```java
/**
 * Constraint C1: Each student selects at most one option.
 *
 * <p>Mathematical formulation:
 * ∀s ∈ S:  Σ_{o ∈ O_s} x_o ≤ 1
 *
 * @param model  the Xpress optimizer model
 * @param bundle the optimization data
 */
private void addOptionSelectionConstraint(XpressOptimizer model,
                                          OptimizationDataBundle bundle) {
    for (Student student : bundle.getEligibleStudents()) {
        List<XpressVariable> studentVars = getVariablesForStudent(student, bundle);
        model.addConstraint(
                model.sum(studentVars).leq(1),
                "option_selection_" + student.getEmployeeId());
    }
}

/**
 * Constraint C3 (FAR Part 117 §117.25): Minimum 10-hour rest between duty periods.
 *
 * <p>Per FAR Part 117.25(b), a flight crew member must receive a minimum 10-hour
 * rest period prior to the flight duty period.
 *
 * <p>Mathematical formulation:
 * ∀s ∈ S, ∀(o1, o2) ∈ BackToBackPairs_s:
 *   x_o1 + x_o2 ≤ 1  if rest(o1, o2) < 10h
 *
 * @param model  the Xpress optimizer model
 * @param bundle the optimization data
 */
private void addMinimumRestConstraint(XpressOptimizer model,
                                       OptimizationDataBundle bundle) {
    // implementation...
}
```

---

## Scoring Weight Profile Pattern

All profiles (`standard`, `limitedMoves`, `experimental`) MUST contain every weight field.
Missing a field causes a silent `0.0` default — the most dangerous anti-pattern.

```java
// ✅ CORRECT — field exists in ALL three factory methods
public static ScoringWeightProfile standard() {
    return ScoringWeightProfile.builder()
            .openBlkdSeqBaseReward(100.0)
            .newRewardField(50.0)          // ← added here
            .build();
}

public static ScoringWeightProfile limitedMoves() {
    return ScoringWeightProfile.builder()
            .openBlkdSeqBaseReward(100.0)
            .newRewardField(50.0)          // ← and here
            .build();
}

public static ScoringWeightProfile experimental(ScoringWeightProfileOverride overrides) {
    var base = standard();
    return ScoringWeightProfile.builder()
            .openBlkdSeqBaseReward(
                    overrides.getOpenBlkdSeqBaseReward() != null
                            ? overrides.getOpenBlkdSeqBaseReward()
                            : base.getOpenBlkdSeqBaseReward())
            .newRewardField(
                    overrides.getNewRewardField() != null  // ← and here
                            ? overrides.getNewRewardField()
                            : base.getNewRewardField())
            .build();
}

// ❌ WRONG — field missing from limitedMoves silently defaults to 0.0
public static ScoringWeightProfile limitedMoves() {
    return ScoringWeightProfile.builder()
            .openBlkdSeqBaseReward(100.0)
            // newRewardField omitted → 0.0 silently disables the reward
            .build();
}
```

---

## Config Null Safety Pattern

Per **ENG-6.1** and this avatar's null-safe-config convention, primitive fields in the Config POJO use `@JsonSetter(nulls = Nulls.SKIP)` so that a JSON `null` preserves the declared Java default rather than silently coercing to `false` or `0`.

```java
// ✅ CORRECT — JSON null preserves freezeDays = 6
@JsonSetter(nulls = Nulls.SKIP)
@JsonProperty("freezeDays")
private int freezeDays = 6;

// ❌ WRONG — JSON null coerces to 0, silently removing the freeze window
@JsonProperty("freezeDays")
private int freezeDays = 6;
```

---

## Solver Audit Trail (Per ENG-6.7)

Every solver invocation MUST log the following at INFO level:

```java
log.info("[MathModel] Solver status: {} | Objective: {} | Solve time: {}ms | "
        + "Variables: {} | Constraints: {}",
        solverStatus, objectiveValue, solveTimeMs, variableCount, constraintCount);
```

This provides the immutable audit record required for reproducibility and post-run analysis.

---

## Anti-Patterns

| Anti-Pattern | Why It's Dangerous | Correct Approach |
|---|---|---|
| Coding constraints without math formulation | Constraint bugs are silent — model just returns wrong answer | Write ∀ notation in Javadoc first |
| Multiple constraints in one method | Violates ENG-3.4; hard to test and reason about | One constraint = one method |
| Missing weight in a scoring profile | Silently disables reward for that profile (0.0 default) | Always update all three factory methods |
| Testing via full pipeline run | Slow, fragile; hides which component failed | Test scoring methods and model constraints independently |
| Ignoring solver status | Empty solution may be INFEASIBLE, not just "nothing to do" | Always check and log solver status before consuming results |


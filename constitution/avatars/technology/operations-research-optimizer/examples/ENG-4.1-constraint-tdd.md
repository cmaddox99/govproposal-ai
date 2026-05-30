---
law_id: ENG-4.1
avatar: operations-research-optimizer
---

# ENG-4.1: Atomic TDD Examples for Operations Research / MIP Optimizer

> All examples use Java with JOSE (Journey Optimization & Spoilage Elimination) as the reference implementation.

---

## COMPLIANT: Constraint Unit Test — One Behavior Per Test

```java
/**
 * BASE-MIP-001: Sequence exclusivity constraint prevents the same sequence
 * from appearing in more than one selected option.
 *
 * Source: hangar-ai-specs/specs/mip-model/spec.md
 * Constitutional: ENG-4.1 Atomic TDD
 */
@Test
@DisplayName("BASE-MIP-001: two students competing for the same sequence — only one wins")
void solve_twoStudentsCompetingForSameSequence_onlyOneWins() {
    // Given — two students each with one option, both containing SEQ-101
    StudentOption optionA = StudentOptionFixture.withSequences("SEQ-101");
    StudentOption optionB = StudentOptionFixture.withSequences("SEQ-101");
    OptimizationDataBundle bundle = BundleFixture.withOptions(optionA, optionB);

    // When
    optimizationService.findOptimalSolution(bundle, ScoringWeightProfile.standard());

    // Then — at most one option selected; SEQ-101 not duplicated
    long selectedCount = bundle.getAllOptions().stream()
            .filter(StudentOption::isSelected)
            .filter(o -> o.getSequenceKeys().contains("SEQ-101"))
            .count();
    assertThat(selectedCount).isLessThanOrEqualTo(1);
}
```

**Why compliant:** One test, one constraint, one assertion. The test is named after its scenario ID so it traces directly to `hangar-ai-specs/specs/mip-model/spec.md`. The fixture isolates setup noise so the assertion reads as the behavior specification.

---

## COMPLIANT: Scoring Unit Test — Guard Clause Behaviour

```java
/**
 * BASE-SCORE-005: Open blocked sequence reward is zero when option has no open blkd sequences.
 *
 * Source: hangar-ai-specs/specs/scoring-engine/spec.md
 * Constitutional: ENG-4.1 Atomic TDD
 */
@Test
@DisplayName("BASE-SCORE-005: no open blkd sequences → open blkd seq reward is 0.0")
void computeOpenBlkdSeqReward_withNoOpenBlkdSeqs_returnsZero() {
    // Given — option contains only an assigned blocked sequence (not open)
    StudentOption option = StudentOptionFixture.withAssignedBlkdSeqOnly();
    ScoringWeightProfile profile = ScoringWeightProfile.standard();

    // When
    double reward = scorer.computeOpenBlkdSeqReward(profile, option, student, bundle);

    // Then
    assertThat(reward).isEqualTo(0.0);
}
```

**Why compliant:** Tests the guard clause in isolation — no solver invocation, no full pipeline setup. Fast (<10ms), deterministic, single-concept.

---

## COMPLIANT: Parameterized Test for Scoring Across Training Types

```java
/**
 * BASE-SCORE-013: Buy drop reward differs by training type.
 * Source: hangar-ai-specs/specs/scoring-engine/spec.md
 * Constitutional: ENG-4.1 Atomic TDD
 */
@ParameterizedTest(name = "trainingType={0} → reward >= floor {1}")
@CsvSource({
    "NH,  HIGH",
    "TT,  HIGH",
    "UG,  HIGH",
    "SRQ, LOW"
})
@DisplayName("BASE-SCORE-013: buy drop reward floor varies by training type")
void computeBuyDropReward_completableStudent_rewardMeetsFloorForTrainingType(
        String trainingType, String expectedTier) {
    // Given
    Student student = StudentFixture.completable(TrainingType.valueOf(trainingType));
    StudentOption option = StudentOptionFixture.withDroppedBuySeq(student);
    ScoringWeightProfile profile = ScoringWeightProfile.standard();

    // When
    double reward = scorer.computeBuyDropReward(profile, option, student, bundle);

    // Then — NH/TT/UG reward is higher than SRQ
    if ("HIGH".equals(expectedTier)) {
        assertThat(reward).isGreaterThan(profile.getBuyDropRewardSrq());
    } else {
        assertThat(reward).isEqualTo(profile.getBuyDropRewardSrq());
    }
}
```

**Why compliant:** One method tests one reward dimension (training-type floor) across four training types. The parameter names document intent. No duplication of identical test bodies.

---

## VIOLATION: Testing Multiple Constraints in One Test

```java
// ❌ VIOLATES ENG-4.1 — multiple constraints, multiple assertions
// If this test fails, you don't know WHICH constraint is broken
@Test
void solve_completeValidation() {
    OptimizationDataBundle bundle = BundleFixture.realistic();

    optimizationService.findOptimalSolution(bundle, ScoringWeightProfile.standard());

    // Testing sequence exclusivity AND option selection AND balance constraint
    // AND objective value AND solver status — all in one test
    assertThat(bundle.getSolverStatus()).isEqualTo(SolverStatus.OPTIMAL);
    assertThat(bundle.getObjectiveValue()).isGreaterThan(0.0);
    assertThat(bundle.getSelectedOptions()).hasSizeLessThanOrEqualTo(bundle.getStudents().size());
    bundle.getSelectedOptions().forEach(o ->
        assertThat(Collections.frequency(bundle.getAllSequenceKeys(), o.getSequenceKeys())).isEqualTo(1));
    assertThat(bundle.getDroppedBlkdSeqHours()).isLessThanOrEqualTo(bundle.getSavedOpenBlkdSeqHours());
}
```

**Why violates ENG-4.1:** Five distinct constraint behaviours in one test. A failure points at the whole solver pipeline, not a specific constraint. RED step means nothing — you don't know what to fix.

---

## VIOLATION: Writing Code Before a Failing Test

```java
// ❌ VIOLATES ENG-4.1 — implementation written first, test added after
// "GREEN" here means the test was written to match the code, not to drive it

// Step 1 (WRONG): Developer writes the constraint method first
private void addMaxGroupSizeConstraint(XpressOptimizer model, OptimizationDataBundle bundle) {
    int max = runContext.getConfig().getMaxStudentsPerGroup();
    // ... 30 lines of constraint logic ...
}

// Step 2 (WRONG): Developer then writes a test that just confirms what the code does
@Test
void addMaxGroupSizeConstraint_works() {
    // This test was written to pass the existing code, not to specify behavior.
    // It has no RED phase — it passed on first run.
    assertThat(true).isTrue(); // placeholder assertion added because test "passes"
}
```

**Why violates ENG-4.1:** No RED phase — the test never failed. The test documents the implementation, not the specification. The constraint logic has no design pressure from tests, so its interface may be harder to use than necessary.

---

## COMPLIANT: Full Atomic TDD Cycle — Adding a New Constraint

### Step 1: RED — Write one failing test first

```java
/**
 * BASE-MIP-NEW-001: Max students per action group is respected.
 * Source: hangar-ai-specs/specs/mip-model/spec.md
 * Constitutional: ENG-4.1 Atomic TDD — RED step
 */
@Test
@DisplayName("BASE-MIP-NEW-001: solution respects maxStudentsPerGroup config")
void solve_withMaxStudentsPerGroup2_actionGroupsHaveAtMost2Students() {
    // Given — 6 students, maxStudentsPerGroup = 2
    var bundle = BundleFixture.withStudents(6);
    runContext.getConfig().setMaxStudentsPerGroup(2);

    // When
    optimizationService.findOptimalSolution(bundle, ScoringWeightProfile.standard());

    // Then — every action group has at most 2 students (FAILS — constraint not yet added)
    bundle.getActionGroups().forEach(group ->
        assertThat(group.getStudents()).hasSizeLessThanOrEqualTo(2));
}
// Run: FAILS — constraint does not exist yet ✓ RED confirmed
```

### Step 2: GREEN — Write minimum code to pass

```java
// Add ONLY this to OptionSelectionModel:
private void addMaxGroupSizeConstraint(XpressOptimizer model, OptimizationDataBundle bundle) {
    int maxSize = runContext.getConfig().getMaxStudentsPerGroup();
    if (maxSize == Integer.MAX_VALUE) return; // feature disabled
    // minimum constraint logic to make the test pass
}
// Run: PASSES ✓
```

### Step 3: REFACTOR — Improve without breaking GREEN

```java
/**
 * Constraint C4: Action groups respect the maxStudentsPerGroup configuration.
 *
 * <p>Mathematical formulation:
 * ∀g ∈ Groups: |{s ∈ g : Σ_{o ∈ O_s} x_o = 1}| ≤ maxStudentsPerGroup
 *
 * <p>Disabled when maxStudentsPerGroup = Integer.MAX_VALUE (default).
 */
private void addMaxGroupSizeConstraint(XpressOptimizer model, OptimizationDataBundle bundle) {
    int maxSize = runContext.getConfig().getMaxStudentsPerGroup();
    if (maxSize == Integer.MAX_VALUE) {
        return;
    }
    for (ActionGroup group : bundle.getActionGroups()) {
        List<XpressVariable> groupVars = getVariablesForGroup(group, bundle);
        model.addConstraint(
                model.sum(groupVars).leq(maxSize),
                "max_group_size_" + group.getId());
    }
}
// Run: PASSES ✓
```

### Step 4: COMMIT

```
test(tdd): BASE-MIP-NEW-001 max students per action group constraint

- RED: test written first, failed before implementation
- GREEN: minimum constraint added to OptionSelectionModel
- REFACTOR: Javadoc with math formulation, guard clause extracted

Constitutional: ENG-4.1 Atomic TDD (NON-NEGOTIABLE)
Source: hangar-ai-specs/specs/mip-model/spec.md
```


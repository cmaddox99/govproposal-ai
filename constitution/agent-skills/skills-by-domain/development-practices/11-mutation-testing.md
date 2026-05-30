---
skill:
  id: skill-11-mutation-testing
  name: Mutation Testing
  category: development
  version: "1.0.0"

laws:
  implements:
    - id: ENG-4.11
      title: Mutation Testing Law
  references:
    - id: ENG-4.1
      title: Atomic TDD Law (NON-NEGOTIABLE)
    - id: ENG-4.2
      title: Test Pyramid Law
    - id: ENG-4.6
      title: Coverage Requirements
    - id: BUS-7.1
      title: Audit Trail Law

triggers:
  phrases:
    - "mutation testing"
    - "mutation score"
    - "test quality"
    - "tests catch bugs"
    - "Verify tests kill mutations"
    - "Run mutation testing"

followed_by:
  - skill-09-refactoring
  - skill-08-code-review

---

# Skill: Mutation Testing

> **Purpose:** Verify that tests are strong enough to catch real bugs, not just achieve coverage. Mutation testing measures the effectiveness of your test suite.
> **Workflow:** See `workflows/greenfield-development.md` and `workflows/legacy-rescue-refactor.md` for integration with the atomic TDD cycle (GREEN and REFACTOR phases).

---

## Constitutional Foundation

**ENG-4.11** establishes mutation testing as the third dimension of test quality:

| Dimension | Measures | ENG Law | Purpose |
|-----------|----------|---------|---------|
| Coverage | Which lines? | ENG-4.6 | Quantity |
| Pyramid | What types? | ENG-4.2 | Distribution |
| **Mutation** | **Catch bugs?** | **ENG-4.11** | **Effectiveness** |

A test that passes with buggy code fails all three dimensions. Mutation testing forces engineers to write **specific, sensitive tests** that validate behavior, not just code paths.

---

## When to Invoke

Invoke this skill when:

- **In GREEN phase** of atomic TDD cycle: After writing passing code, before REFACTOR
- **In REFACTOR phase**: After improving code quality, to verify test quality didn't degrade
- **Assessing test brittle ness**: Coverage ≥ threshold but tests feel weak (over-mocking)
- **Critical path code**: Crew scheduling, dispatch safety, maintenance compliance functions

**Trigger phrases:**
- "Is my test suite actually catching bugs?"
- "My coverage is high but I'm not confident in the tests"
- "Let's validate test quality with mutation testing"
- "SonarQube says mutation score is low"

---

## Quality Checklist

### Pre-Mutation Testing (Code Ready?)

- [ ] Code change complete (GREEN phase or REFACTOR phase)
- [ ] All existing tests passing (zero failures)
- [ ] Coverage ≥70% (general) or ≥90% (critical path) for changed code
- [ ] Code compiles without warnings (for statically-typed languages)
- [ ] No pending refactorings (mutation testing runs on final code)

### Running Mutation Testing

**Step 1: Select Tool by Language**

| Language | Tool | Command | Notes |
|----------|------|---------|-------|
| TypeScript/JavaScript | Stryker | `npm run mutation -- --testRunner=jest` | Integrates with Jest/Mocha |
| Java | Pitest | `mvn pitest:mutationCoverage` | Maven/Gradle plugin |
| Python | mutmut | `mutmut run && mutmut results` | No build tool required |
| Go | gremlins | `gremlins unleash` | Run from Go module root (`go.mod`). Use `--output=gremlins.json` for machine-readable results. Pin a version compatible with your Go toolchain. |
| iOS / Swift | Muter | `muter run --format html --output muter-report.html` | `brew install muter-mutation-testing/formulae/muter`; run `muter init` first |
| Android / Kotlin | pl.droidsonroids.pitest | `./gradlew :<module>:pitestDebug` | OSS Gradle plugin; `id("pl.droidsonroids.pitest") version "0.2.27"` |

**Step 2: Run Mutation Testing**

```bash
# TypeScript example
npm run mutation

# Expected output:
# Mutants: 45 generated
# Killed: 32
# Survived: 8
# Equivalent: 5
# Mutation Score: 71% (32 killed / 45 total, 5 excluded as equivalent)
```

**Step 3: Review Mutation Report**

- Total mutants generated
- Killed mutants (tests caught the bug)
- Survived mutants (tests MISSED the bug — test is weak)
- Equivalent mutants (mutation produces identical behavior)
- **Mutation Score = Killed / (Total - Equivalent)**

### Decision Gateway (GREEN Phase)

| Scenario | Action | Next Step |
|----------|--------|-----------|
| **Mutation score ≥70%/≥85%** | ✅ PASS | Proceed to REFACTOR |
| **Mutation score <70%** | ❌ FAIL | Strengthen tests or simplify code → RE-TEST |
| **Coverage ≥ but mutation <threshold** | ⚠️ DESIGN ISSUE | Tests over-mocked → Refactor test design |
| **Equivalent mutants >10%** | ⚠️ CODE CLARITY | Architect review → Possible code simplification |

### Test Strengthening Tactics (When Score Too Low)

**If tests are too weak:**

1. **Add specific assertions** — Don't just check happy path
   ```typescript
   // Brittle test (zero mutation score on boundary)
   test('duty limit check', () => {
     expect(checkDutyLimit(10)).toBe(false); // Only tests >limit
   });

   // Strong test (100% mutation score)
   test('duty limit check', () => {
     expect(checkDutyLimit(7.999)).toBe(true);  // Below limit
     expect(checkDutyLimit(8.0)).toBe(true);    // Exactly at limit
     expect(checkDutyLimit(8.001)).toBe(false); // Above limit
   });
   ```

2. **Test boundary conditions** — Mutation testing catches off-by-one
   ```typescript
   // Test both sides of operators
   expect(accumulated >= 8).toBe(false);  // Tests '>='
   expect(accumulated > 8).toBe(false);   // Catches operator mutation
   ```

3. **Verify return values exactly** — Not just truthiness
   ```typescript
   // Weak (mutation: return 0, return 2 both pass)
   expect(calculateCarryover()).toBeTruthy();

   // Strong (mutation: return 0 fails, return 2 fails)
   expect(calculateCarryover()).toBe(1);
   ```

4. **Mock at boundaries only** — Over-mocking hides weak tests
   - ✅ Mock HTTP calls, database queries, external APIs
   - ❌ Don't mock domain objects or business logic collaborators

### Decision Gateway (REFACTOR Phase)

After improving code in REFACTOR:

| Scenario | Action |
|----------|--------|
| **Mutation score ≥ original** | ✅ PASS — Code quality improved without losing test rigor |
| **Mutation score degraded** | ❌ FAIL — Refactoring introduced a bug → Revert & investigate |
| **Score improved** | 🎉 EXCELLENT — Both quality and test rigor improved |

**If score drops after refactoring:**
1. Identify which tests are now passing (they weren't before)
2. Revert the refactoring that broke the test
3. Investigate: Did the refactoring introduce a bug, or did the test detect a real issue?
4. Fix the bug, then try refactoring again

---

## Equivalent Mutant Handling

**Definition:** A mutation that produces identical observable behavior (impossible to kill with any test).

**Example:**
```typescript
// Original
return x + 0;

// Mutation 1: return x + 1 (KILLABLE — test expects x)
// Mutation 2: return x - 0 (EQUIVALENT — same observable behavior)
```

**Decision Tree:**

```
IF equivalent_mutant_count > 0:
  ├─ IF equivalent / total > 10%:
  │  ├─ ACTION: Notify architect
  │  ├─ REASON: High equivalent rate indicates code clarity issue
  │  └─ RESPONSE: Consider code simplification before merge
  │
  └─ IF equivalent / total ≤ 10%:
     └─ ACTION: Auto-exclude from score calculation
```

**In SonarQube:**
- Equivalent mutants appear in report with `[EXCLUDED]` tag
- Do NOT count toward denominator if ≤10%
- If >10%, gate triggers ADVISORY (reviewer notices, architect approves simplification)

---

## Critical Path Functions (≥85% Required)

The following function families require ≥85% mutation score due to aviation safety constraints:

### Crew Scheduling
- `crew-scheduling/core/assignment.ts` — Crew legality checks, FAA Part 121 duty time compliance
- `crew-scheduling/core/time-calculations.ts` — Duty hour accumulation, reset logic, boundary calculations

### Dispatch
- `dispatch/core/safety-constraints.ts` — Fuel calculations, weight-and-balance verification, safety margins

### Maintenance
- `maintenance/core/compliance-tracking.ts` — Regulatory compliance state management, audit trail integrity

**Code review SHALL classify functions as critical or general before implementation.** SonarQube gates enforced accordingly:
- **Critical:** <85% mutation score = HARD_BLOCK (no merge, architect override required)
- **General:** <70% mutation score = PHASE_GATE (blocks, architect can override with audit trail)

---

## SonarQube Phase Gate Integration

Once SonarQube Phase 9 is deployed, mutation score gates are automatically enforced:

| Classification | Threshold | Behavior | Override |
|---|---|---|---|
| **HARD_BLOCK** | Critical path <85% | Blocks PR merge | Architect must approve (non-waivable) |
| **PHASE_GATE** | General code <70% | Blocks merge, warns on degradation | Architect may override with BUS-7.1 audit trail |
| **ADVISORY** | Equivalent >10% | Warns reviewer | Architect documents justification |

**Evidence artifacts** stored in `hangar-ai-specs/`:
- `sonarqube-baseline.md` — Phase 1 baseline snapshot
- `sonarqube-gate.md` — Per-phase mutation score verdict
- `sonarqube-delta.md` — Before/After comparison with improvement %

---

## Behavioral Examples

### Example 1: Crew Duty Accumulation (Off-by-One)

**Code:**
```typescript
function accumulateDutyHours(shifts: Shift[]): number {
  let totalHours = 0;
  for (const shift of shifts) {
    totalHours += shift.durationHours;  // Mutation: += becomes =
  }
  return totalHours;
}
```

**Brittle Test (0% mutation score):**
```typescript
test('accumulates duty hours', () => {
  expect(accumulateDutyHours([{ durationHours: 5 }])).toBe(5);
});
// Mutation += → = still passes (returns 5)!
```

**Strong Test (100% mutation score):**
```typescript
test('accumulates duty hours across multiple shifts', () => {
  const shifts = [
    { durationHours: 3 },
    { durationHours: 2 },
    { durationHours: 4 }
  ];
  expect(accumulateDutyHours(shifts)).toBe(9);
});
// Mutation += → = fails! (returns 4, not 9)
```

### Example 2: Boundary Condition (FAA Duty Limit)

**Code:**
```typescript
function isWithinDutyLimit(hoursWorked: number): boolean {
  return hoursWorked <= 8;  // Mutation: <= becomes <
}
```

**Brittle Test (33% mutation score):**
```typescript
test('exceeds duty limit', () => {
  expect(isWithinDutyLimit(9)).toBe(false);
});
// Only tests > 8, misses boundary at exactly 8
```

**Strong Test (100% mutation score):**
```typescript
test('duty limit boundary', () => {
  expect(isWithinDutyLimit(7.999)).toBe(true);   // Below
  expect(isWithinDutyLimit(8.0)).toBe(true);     // Exactly at limit
  expect(isWithinDutyLimit(8.001)).toBe(false);  // Above
});
// Catches mutation <= → <
```

---

## Hands-On Exercise: Stryker (TypeScript)

### Setup

```bash
npm install --save-dev @stryker-mutator/core @stryker-mutator/typescript-checker
npx stryker init  # Creates stryker.conf.js

# Configure stryker.conf.js for your project
# testRunner: "jest" or "mocha"
# reporters: ["html", "clear-text"]
```

### Run Mutation Testing

```bash
npm run mutation
# or
npx stryker run
```

### Review Report

```
StrykerJS Report:
  Tests ran: 45
  Mutants generated: 127
  Killed: 89
  Survived: 28
  Equivalent: 10
  Mutation Score: 70% (89 killed / 127 - 10 equivalent)
```

### Interpret Results

- **High killed rate (>85%)** — Tests are strong, catching most bugs ✅
- **Moderate rate (70–85%)** — Tests adequate for general code ✅
- **Low rate (<70%)** — Tests too brittle, need strengthening ❌

### Iterate

1. Review `mutation-report/index.html` in browser
2. Find "Survived" mutations (tests didn't catch)
3. Strengthen tests to kill those mutations
4. Re-run: `npx stryker run`
5. Repeat until ≥70% (general) or ≥85% (critical)

---

## Integration with Atomic TDD

**RED Phase:**
- Write test that fails
- No mutation testing (test not yet validated)

**GREEN Phase (MANDATORY checkpoint):**
1. Write minimum passing code
2. Run coverage: ≥70%/≥90%? ✅
3. **Run mutation testing ← YOU ARE HERE**
4. Score ≥70%/≥85%? → REFACTOR or RE-TEST

**REFACTOR Phase (MANDATORY re-verification):**
1. Improve code quality
2. **Re-run mutation testing ← VERIFY NO DEGRADATION**
3. Score stable/improved? → MERGE or INVESTIGATE

---

## Skill Interactions

| Skill | Interaction | When |
|-------|-----------|------|
| **skill-06-atomic-tdd** | Mutation testing validates tests within atomic cycle | GREEN/REFACTOR phases |
| **skill-04-business-domain-modeling** | Model identifies critical paths (≥85% required) | Pre-implementation |
| **skill-09-refactoring** | Mutation testing verifies refactoring doesn't weaken tests | Post-refactor |
| **skill-08-code-review** | Reviewers check mutation score gates in SonarQube | PR review |
| **skill-10-security-review** | Security code requires high mutation score (≥85% critical) | Critical path functions |

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| **Ignoring survived mutants** | "Mutation testing is too strict" | Survived mutants indicate real test weakness — fix it |
| **Over-mocking** | High coverage but low mutation score | Mock only I/O boundaries; test domain logic directly (ENG-4.8) |
| **Equivalent mutants** | "This equivalent mutant is inflating our score" | If >10%, simplify code; if ≤10%, exclude and move on |
| **Skipping REFACTOR verification** | Refactoring introduced a bug not caught by tests | Re-run mutation testing after REFACTOR; score must not degrade |
| **Only testing happy path** | Boundary mutations survive | Add specific tests for boundary conditions (off-by-one, >=, >, etc.) |
| **Tool timeout** | Mutation testing takes too long | Reduce mutation operators; run asynchronously in CI; pilot on critical code first |

---

## References

- **ENG-4.11 Law:** Complete mutation testing governance
- **ENG-4.1 Law:** Atomic TDD cycle integration
- **BEHAVIORAL-EXAMPLES.md:** 6 concrete mutations from aviation code
- **CODEBASE-AUDIT.md:** Pre-implementation tool availability checklist
- **Stryker Docs:** https://stryker-mutator.io/docs/stryker-js/typescript-checker
- **Pitest Docs:** http://pitest.org/
- **mutmut Docs:** https://mutmut.readthedocs.io/
- **Muter Docs:** https://github.com/muter-mutation-testing/muter
- **droidsonroids pitest-android Docs:** https://plugins.gradle.org/plugin/pl.droidsonroids.pitest

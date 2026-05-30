# Behavioral Examples: Mutation Testing for Aviation Safety-Critical Code

**Purpose:** Demonstrate how ENG-4.11 (Mutation Testing Law) works in practice with concrete examples from AA-Hangar-AI critical paths.

**Audience:** Test architects, reviewers, and developers learning to apply mutation testing.

---

## Critical Path 1: Crew Scheduling — Duty Time Calculations

### Context
FAA Part 121 defines strict duty time limits (e.g., max 8 hours for domestic duty, with specific accumulation rules). A crew duty calculator with 100% test coverage could still miss boundary bugs if its tests are brittle.

### Example 1.1: Off-by-One Error in Accumulated Hours

**File:** `crew-scheduling/core/time-calculations.ts`  
**Function:** `accumulateCrewDuty(shifts: Shift[]): number`

**Original Code:**
```typescript
function accumulateCrewDuty(shifts: Shift[]): number {
  let totalHours = 0;
  for (const shift of shifts) {
    totalHours += shift.durationHours;  // ← MUTATION: += becomes =
  }
  return totalHours;
}
```

**Potential Mutation:**
```typescript
totalHours = shift.durationHours;  // MUTANT: Overwrites instead of accumulates
```

**Test That KILLS This Mutation (Strong):**
```typescript
describe('accumulateCrewDuty', () => {
  it('should sum all shift durations into total', () => {
    const shifts = [
      { durationHours: 4 },
      { durationHours: 3 },
      { durationHours: 2 },
    ];
    const result = accumulateCrewDuty(shifts);
    // MUTATION KILLING: If mutation applies (= instead of +=), result would be 2 (last shift)
    // This test fails because 2 ≠ 9
    expect(result).toBe(9);  // 4 + 3 + 2
  });
});
```

**Test That MISSES This Mutation (Brittle):**
```typescript
describe('accumulateCrewDuty', () => {
  it('should calculate hours', () => {
    const shifts = [{ durationHours: 4 }];
    const result = accumulateCrewDuty(shifts);
    // MUTATION SURVIVES: If mutation applies (= instead of +=), result would still be 4
    // This test passes even with the mutation, so it's weak
    expect(result).toBeGreaterThan(0);  // 4 > 0 is true either way
  });
});
```

**Mutation Score Impact:**
- With strong test: Mutation **KILLED** ✅ (+1 to score)
- With brittle test: Mutation **SURVIVES** ❌ (no contribution to score)
- **Batch of 10 mutations:** If 8 are killed, mutation score = 8/10 = 80% ✅ (above 70% threshold)

**Why This Matters (Aviation Context):**
A crew with 3 shifts totaling 9 hours might be incorrectly assigned by the mutation (shows as 2-hour duty). Crew duty hour violations can trigger FAA violations, fines, and safety incidents.

---

### Example 1.2: Boundary Condition — Exact Equality vs. Greater-Than

**File:** `crew-scheduling/core/assignment.ts`  
**Function:** `isCrewExceededMaxDuty(accumulatedHours: number): boolean`

**Original Code:**
```typescript
function isCrewExceededMaxDuty(accumulatedHours: number): boolean {
  const FAA_MAX_DUTY_HOURS = 8;
  return accumulatedHours > FAA_MAX_DUTY_HOURS;  // ← MUTATION: > becomes >=
}
```

**Potential Mutations:**
```typescript
return accumulatedHours >= FAA_MAX_DUTY_HOURS;  // MUTANT 1: > becomes >=
return accumulatedHours < FAA_MAX_DUTY_HOURS;   // MUTANT 2: > becomes <
```

**Test That KILLS MUTANT 1 (Strong):**
```typescript
describe('isCrewExceededMaxDuty', () => {
  it('should allow exactly 8 hours (FAA maximum)', () => {
    // MUTATION KILLING: If mutation applies (>= instead of >), result would be true
    // FAA rule: 8 hours is allowed; 8.001 is not
    const result = isCrewExceededMaxDuty(8.0);
    // This test KILLS the >= mutation because 8.0 > 8 is false (correct)
    expect(result).toBe(false);
  });

  it('should reject 8.001 hours (exceeds maximum)', () => {
    const result = isCrewExceededMaxDuty(8.001);
    // This test ALSO kills the >= mutation because 8.001 >= 8 would be true (same result)
    // But distinguishes > from >= via boundary test
    expect(result).toBe(true);
  });
});
```

**Test That MISSES MUTANT 1 (Brittle):**
```typescript
describe('isCrewExceededMaxDuty', () => {
  it('should work with duty hours', () => {
    const result = isCrewExceededMaxDuty(9);
    // MUTATION SURVIVES: Whether > or >=, result for 9 is the same (true)
    // This test doesn't distinguish the boundary
    expect(result).toBe(true);
  });
});
```

**Test That KILLS MUTANT 2 (<):**
```typescript
describe('isCrewExceededMaxDuty', () => {
  it('should return false for hours <= 8', () => {
    expect(isCrewExceededMaxDuty(7)).toBe(false);
    expect(isCrewExceededMaxDuty(8)).toBe(false);
  });

  it('should return true for hours > 8', () => {
    expect(isCrewExceededMaxDuty(9)).toBe(true);
    expect(isCrewExceededMaxDuty(10)).toBe(true);
  });
  // MUTATION KILLING: If mutation applies (< instead of >), both tests fail
  // Because < 8 would return true for 7 (not false)
});
```

**Mutation Score Impact:**
- 3 total mutations in this function (>, >=, <)
- Strong tests kill all 3: score = 3/3 = 100% ✅
- Brittle tests kill only 1: score = 1/3 = 33% ❌ (below 70% threshold)

**Why This Matters (Aviation Context):**
A crew scheduled for exactly 8.0 hours is legal. A crew at 8.001 hours violates FAA Part 121. A > mutation that becomes >= would incorrectly flag the 8.0-hour crew as invalid. This could block legal crew assignments or allow illegal ones.

---

### Example 1.3: Off-by-One in Reset Logic (Multi-Day Duty Accumulation)

**File:** `crew-scheduling/core/time-calculations.ts`  
**Function:** `resetDutyHours(previousDayHours: number): number`

**Original Code:**
```typescript
function resetDutyHours(previousDayHours: number): number {
  // FAA rules: Duty hours reset every 24-hour period
  // If crew rest < 10 hours, carryover 1 hour from previous day
  const MIN_REST_HOURS = 10;
  const REST_AVAILABLE = 16;  // Hours between shifts
  
  if (REST_AVAILABLE < MIN_REST_HOURS) {
    return 1;  // ← MUTATION: 1 becomes 0 or 2
  }
  return 0;
}
```

**Potential Mutations:**
```typescript
return 0;  // MUTANT 1: 1 becomes 0 (under-carryover)
return 2;  // MUTANT 2: 1 becomes 2 (over-carryover)
return previousDayHours;  // MUTANT 3: hardcoded value becomes variable
```

**Test That KILLS All Mutations (Strong):**
```typescript
describe('resetDutyHours', () => {
  it('should carryover exactly 1 hour when rest < 10 hours', () => {
    // Simulate: crew had 7 duty hours yesterday, only 9 hours rest before next shift
    const result = resetDutyHours(7);
    
    // MUTATION KILLING:
    // - If mutation: return 0 → test fails (0 ≠ 1) ✓
    // - If mutation: return 2 → test fails (2 ≠ 1) ✓
    // - If mutation: return previousDayHours → test fails (7 ≠ 1) ✓
    expect(result).toBe(1);
  });

  it('should reset to zero hours when rest >= 10 hours', () => {
    const result = resetDutyHours(7);  // previousDay doesn't matter if rest >= 10
    expect(result).toBe(0);
  });
});
```

**Test That MISSES Mutations (Brittle):**
```typescript
describe('resetDutyHours', () => {
  it('should reset duty hours', () => {
    const result = resetDutyHours(7);
    // MUTATION SURVIVES: Only checks truthiness, not exact value
    // All mutations (0, 1, 2) are truthy or specific values that pass loose checks
    expect(result).toBeGreaterThanOrEqual(0);  // Both 0 and 1 pass
  });
});
```

**Mutation Score Impact:**
- 3 mutations in `resetDutyHours`
- Strong test kills all 3: score = 3/3 = 100% ✅
- Brittle test kills 0: score = 0/3 = 0% ❌ (far below threshold)

**Why This Matters (Aviation Context):**
Incorrect carryover of duty hours could compound multi-day duty violations. Under-carryover (0 instead of 1) could allow a crew to exceed total weekly duty limits. Over-carryover (2 instead of 1) could unnecessarily restrict crew availability.

---

## Critical Path 2: Dispatch — Safety Constraints (Fuel Calculations)

### Context
Dispatch fuel calculations must account for minimum fuel reserves, alternate airport fuel, and contingency. An error in fuel computation could result in an aircraft departing without adequate reserves, violating FAA minimums and creating safety hazards.

### Example 2.1: Fuel Minimum Verification

**File:** `dispatch/core/safety-constraints.ts`  
**Function:** `verifyFuelSufficiency(fuel_available: number, fuel_required: number): boolean`

**Original Code:**
```typescript
function verifyFuelSufficiency(
  fuel_available: number,
  fuel_required: number
): boolean {
  // FAA: Aircraft must carry fuel for planned flight + reserves (alternate + contingency)
  const FUEL_CONTINGENCY_PERCENT = 0.05;  // 5% of flight fuel
  const requiredWithContingency = fuel_required * (1 + FUEL_CONTINGENCY_PERCENT);
  
  return fuel_available >= requiredWithContingency;  // ← MUTATION: >= becomes >
}
```

**Potential Mutations:**
```typescript
return fuel_available > requiredWithContingency;   // MUTANT 1: >= becomes >
return fuel_available <= requiredWithContingency;  // MUTANT 2: >= becomes <=
return fuel_available < requiredWithContingency;   // MUTANT 3: >= becomes <
```

**Test That KILLS All Mutations (Strong):**
```typescript
describe('verifyFuelSufficiency', () => {
  it('should accept when fuel exactly matches requirement', () => {
    const fuel_required = 1000;
    const contingency = 1000 * 0.05;  // 50 gallons
    const fuel_available = 1000 + contingency;  // Exactly meets requirement
    
    // MUTATION KILLING:
    // - If mutation: > instead of >= → test fails (1050 > 1050 is false)
    // - If mutation: <= instead of >= → test fails (1050 <= 1050 is true, but expected false)
    // - If mutation: < instead of >= → test fails (1050 < 1050 is false)
    const result = verifyFuelSufficiency(fuel_available, fuel_required);
    expect(result).toBe(true);  // Exactly enough fuel is acceptable
  });

  it('should reject when fuel is below requirement', () => {
    const fuel_required = 1000;
    const contingency = 1000 * 0.05;
    const fuel_available = (1000 + contingency) - 1;  // 1 gallon short
    
    const result = verifyFuelSufficiency(fuel_available, fuel_required);
    expect(result).toBe(false);  // Short fuel is not acceptable
  });
});
```

**Test That MISSES Mutations (Brittle):**
```typescript
describe('verifyFuelSufficiency', () => {
  it('should check fuel', () => {
    const result = verifyFuelSufficiency(1050, 1000);
    // MUTATION SURVIVES: Tests only happy path; doesn't distinguish >= from >
    // If mutation >= becomes >, result for 1050 vs. 1000 is still true
    expect(result).toBeTruthy();
  });
});
```

**Mutation Score Impact:**
- 3 mutations in boundary condition
- Strong tests kill all 3: score = 3/3 = 100% ✅
- Brittle test kills 0: score = 0/3 = 0% ❌

**Why This Matters (Aviation Context):**
FAA regulations require exact compliance with fuel minimums. An aircraft with exactly the required fuel (including contingency) is legal. A mutation that changes >= to > would illegally reject this aircraft. A mutation that changes >= to <= would accept aircraft with insufficient fuel, violating safety regulations.

---

### Example 2.2: Weight-and-Balance Verification

**File:** `dispatch/core/safety-constraints.ts`  
**Function:** `isWeightWithinLimits(current_cg: number, min_cg: number, max_cg: number): boolean`

**Original Code:**
```typescript
function isWeightWithinLimits(
  current_cg: number,
  min_cg: number,
  max_cg: number
): boolean {
  // Center of Gravity (CG) is critical for flight safety
  // CG outside limits can cause uncontrollable flight
  return current_cg >= min_cg && current_cg <= max_cg;  // ← MUTATIONS: >= becomes >, <= becomes <
}
```

**Potential Mutations:**
```typescript
return current_cg > min_cg && current_cg <= max_cg;      // MUTANT 1: >= becomes >
return current_cg >= min_cg && current_cg < max_cg;      // MUTANT 2: <= becomes <
return current_cg > min_cg || current_cg <= max_cg;      // MUTANT 3: && becomes ||
return current_cg >= min_cg || current_cg <= max_cg;     // MUTANT 4: && becomes ||
```

**Test That KILLS All Mutations (Strong):**
```typescript
describe('isWeightWithinLimits', () => {
  it('should accept when CG is at minimum boundary', () => {
    const min_cg = 25.5;
    const max_cg = 32.0;
    const current_cg = 25.5;  // Exactly at minimum
    
    const result = isWeightWithinLimits(current_cg, min_cg, max_cg);
    // MUTATION KILLING:
    // - If >= becomes > → test fails (25.5 > 25.5 is false, but expected true)
    expect(result).toBe(true);
  });

  it('should accept when CG is at maximum boundary', () => {
    const min_cg = 25.5;
    const max_cg = 32.0;
    const current_cg = 32.0;  // Exactly at maximum
    
    const result = isWeightWithinLimits(current_cg, min_cg, max_cg);
    // MUTATION KILLING:
    // - If <= becomes < → test fails (32.0 < 32.0 is false, but expected true)
    expect(result).toBe(true);
  });

  it('should reject when CG is below minimum', () => {
    const min_cg = 25.5;
    const max_cg = 32.0;
    const current_cg = 25.4;
    
    const result = isWeightWithinLimits(current_cg, min_cg, max_cg);
    // MUTATION KILLING:
    // - If && becomes || → test still fails (25.4 >= 25.5 is false, and || needs false && false)
    expect(result).toBe(false);
  });

  it('should reject when CG is above maximum', () => {
    const min_cg = 25.5;
    const max_cg = 32.0;
    const current_cg = 32.1;
    
    const result = isWeightWithinLimits(current_cg, min_cg, max_cg);
    expect(result).toBe(false);
  });
});
```

**Mutation Score Impact:**
- 4 mutations across 2 operators
- Strong test suite kills all 4: score = 4/4 = 100% ✅
- Brittle tests (only testing 1 boundary): score = 2/4 = 50% ❌ (below 70%)

**Why This Matters (Aviation Context):**
Weight-and-balance violations can cause uncontrollable flight. An aircraft at the exact minimum or maximum CG is still within limits. A mutation changing >= to > would reject legally balanced aircraft. A mutation changing && to || would accept aircraft outside the envelope.

---

## Critical Path 3: Maintenance — Compliance Tracking

### Context
Maintenance records must track regulatory compliance intervals (e.g., annual inspections, airworthiness certificates). An error in compliance state transitions could allow an aircraft to fly with expired certifications, violating FAA regulations and endangering safety.

### Example 3.1: Compliance State Transition Logic

**File:** `maintenance/core/compliance-tracking.ts`  
**Function:** `isAircraftAirworthy(last_inspection_date: Date, inspection_interval_days: number): boolean`

**Original Code:**
```typescript
function isAircraftAirworthy(
  last_inspection_date: Date,
  inspection_interval_days: number
): boolean {
  const today = new Date();
  const daysSinceInspection = Math.floor(
    (today.getTime() - last_inspection_date.getTime()) / (1000 * 60 * 60 * 24)
  );
  
  return daysSinceInspection <= inspection_interval_days;  // ← MUTATION: <= becomes <
}
```

**Potential Mutations:**
```typescript
return daysSinceInspection < inspection_interval_days;   // MUTANT 1: <= becomes <
return daysSinceInspection > inspection_interval_days;   // MUTANT 2: <= becomes >
return daysSinceInspection == inspection_interval_days;  // MUTANT 3: <= becomes ==
```

**Test That KILLS All Mutations (Strong):**
```typescript
describe('isAircraftAirworthy', () => {
  it('should mark as airworthy on the last day of inspection interval', () => {
    const inspection_interval = 365;  // Annual inspection
    const last_inspection = new Date();
    last_inspection.setDate(last_inspection.getDate() - 365);  // Exactly 365 days ago
    
    const result = isAircraftAirworthy(last_inspection, inspection_interval);
    // MUTATION KILLING:
    // - If <= becomes < → test fails (365 < 365 is false, but expected true)
    expect(result).toBe(true);  // On the last day, aircraft is still airworthy
  });

  it('should mark as not airworthy the day after inspection interval expires', () => {
    const inspection_interval = 365;
    const last_inspection = new Date();
    last_inspection.setDate(last_inspection.getDate() - 366);  // 366 days ago (1 day overdue)
    
    const result = isAircraftAirworthy(last_inspection, inspection_interval);
    // MUTATION KILLING:
    // - If <= becomes < → test still fails (366 < 365 is false, correct result)
    // - If <= becomes > → test fails (366 > 365 is true, but expected false)
    expect(result).toBe(false);  // Aircraft is overdue, not airworthy
  });
});
```

**Test That MISSES Mutations (Brittle):**
```typescript
describe('isAircraftAirworthy', () => {
  it('should check airworthiness', () => {
    const result = isAircraftAirworthy(new Date(), 365);
    // MUTATION SURVIVES: Current date is 0 days from inspection (well within interval)
    // All mutations (<, >, <=, ==) would still return true
    expect(result).toBeTruthy();
  });
});
```

**Mutation Score Impact:**
- 3 mutations in boundary condition
- Strong test kills all 3: score = 3/3 = 100% ✅
- Brittle test kills 0: score = 0/3 = 0% ❌

**Why This Matters (Aviation Context):**
A mutation changing <= to < would allow aircraft to fly on the inspection due date without current airworthiness. This violates FAA regulations and creates safety hazards. Strong tests ensure that compliance tracking is precise and legally compliant.

---

## Mutation Score Summary Table

| Critical Path | Function | Mutations | Strong Tests | Brittle Tests | Score (Strong) | Score (Brittle) |
|---|---|---|---|---|---|---|
| Crew Scheduling | `accumulateCrewDuty` | += → = | Kills all | Misses all | 100% ✅ | 0% ❌ |
| Crew Scheduling | `isCrewExceededMaxDuty` | >, >=, < | Kills all | Kills 1 | 100% ✅ | 33% ❌ |
| Crew Scheduling | `resetDutyHours` | Constants (0, 1, 2) | Kills all | Kills 0 | 100% ✅ | 0% ❌ |
| Dispatch | `verifyFuelSufficiency` | >=, >, <=, < | Kills all | Kills 0 | 100% ✅ | 0% ❌ |
| Dispatch | `isWeightWithinLimits` | &&→\|\|, >=→>, <=→< | Kills all | Kills 2 | 100% ✅ | 50% ❌ |
| Maintenance | `isAircraftAirworthy` | <=→<, <=→>, <=→== | Kills all | Kills 0 | 100% ✅ | 0% ❌ |

**Key Insight:** Strong tests kill 80–100% of mutations; brittle tests kill 0–50%. The **ENG-4.11 threshold of ≥70% mutation score** is designed to catch brittle test suites and enforce behavior-driven tests that validate critical safety functions.

---

## Recommendations for Mutation Testing in Code Review

When reviewing PRs for critical paths, check:

1. **Boundary Conditions:** Are tests checking exact boundaries (`<=` vs. `<`, `>=` vs. `>`)?
   - Example: FAA duty limits of exactly 8.0 hours, fuel exactly meeting requirement

2. **Conditional Logic:** Are tests verifying all branches (`&&`, `||`, ternaries)?
   - Example: Weight-and-balance acceptance requires BOTH min and max checks (`&&`)

3. **Arithmetic Operations:** Are tests checking accumulation (`+=` not `=`), subtraction, constants?
   - Example: Multi-shift duty hour accumulation must sum all shifts, not overwrite

4. **State Transitions:** Are tests verifying state changes for compliance tracking?
   - Example: Aircraft airworthiness transitions from valid → overdue at exact boundary

5. **Aviation Context:** Are mutations realistic for the domain (e.g., FAA Part 121, duty time, fuel)?
   - Example: Off-by-one hour in crew duty is plausible safety bug

---

## See Also

- **ENG-4.11:** Mutation Testing Law (full specification)
- **ENG-4.1:** Atomic TDD (RED→GREEN→REFACTOR cycle)
- **ENG-4.3:** Test Quality Law (FIRST principles)
- **ENG-3.5:** Code Review Law (mutation score in checklist)
- **hangar-ai-constitution-workflows:** Workshop exercises using these examples

# Governance Review Session: mutation-testing-governance

**Session ID:** gov-390e7895ee2a  
**Date:** March 31, 2026  
**Verdict:** **BLOCKED** (3 critical conditions)  
**Roles:** Architect, Critic, Test Architect  

---

## VERDICT SUMMARY

The mutation testing governance proposal is **BLOCKED** pending remediation of critical gaps identified by all three governance roles.

**Key Issues:**
1. **Architect (VIOLATION: ENG-2.4, ENG-2.5)** — "Critical paths" undefined; no acceptance criteria for path classification
2. **Critic (VIOLATION: ENG-12.1, ENG-12.3, PRD-1.5)** — Unverified claims about tools, codebase state, risk; missing behavioral specifications
3. **Test Architect (VIOLATION: ENG-4.1, ENG-4.2, ENG-4.6, ENG-4.9)** — Tool selection criteria undefined; mutation operator scope missing; critical path definition needed; equivalent mutant handling unclear; FIRST principle validation incomplete

---

## CRITICAL CONDITIONS REQUIRING REMEDIATION

### **CONDITION 1: Define "Critical Paths" Explicitly (Architect)**

**Violation:** ENG-2.5 (Testability & Acceptance) — Proposal specifies ≥85% mutation score for "critical paths" but does not define what constitutes a critical path in the crew scheduling domain.

**Gap:** 
- Is a critical path any function touching crew availability?
- Only functions in the scheduling algorithm core?
- Only functions with regulatory compliance implications (FAA Part 121)?

**Remediation Required:**
Add explicit definition to ENG-4.11:
```markdown
**Critical Paths (85% mutation score required):**
- Functions in `crew-scheduling/core/assignment.ts`: crew legality determination, conflict detection
- Functions in `crew-scheduling/core/time-calculations.ts`: duty time accumulation, reset logic
- Functions in `dispatch/core/safety-constraints.ts`: fuel calculations, weight-and-balance
- Functions in `maintenance/core/compliance-tracking.ts`: regulatory compliance state management

**General Paths (70% mutation score required):**
- All other business logic functions
- UI/presentation layer functions
- Data formatting and transformation utilities
```

---

### **CONDITION 2: Specify Tool Selection Criteria & Mutation Operator Scope (Test Architect)**

**Violation:** ENG-4.9 (Quality Gates) — Proposal lists tools but doesn't specify when to use each. No specification of mutation operators to enforce.

**Gap:**
- When should a project use Stryker vs. Pitest vs. mutmut?
- Which mutation operators are acceptable (arithmetic, logical, conditional, boundary)?
- Which operators should be excluded from scoring (e.g., constant replacement in logging)?

**Remediation Required:**
Add tool selection matrix and operator specification:
```markdown
**Tool Selection by Language:**
- TypeScript/JavaScript: Stryker (primary), Infected (secondary)
  └─ Configuration: `.stryker-config.json` with operators: [ArithmeticOperator, ConditionalOperator, LogicalOperator]
- Java: Pitest (primary), Major (secondary)
  └─ Configuration: `pom.xml` mutation operators: INVERT_NEGATION, RETURN_VALS, MATH, CONDITIONALS
- Python: mutmut (primary), cosmic-ray (secondary)
  └─ Configuration: `setup.py` mutations: arithmetic, boolean, constants
- Go: cosmic-ray (primary)
  └─ Configuration: Build-system integration with arithmetic, boolean operators
- C#: Stryker.NET (primary)
  └─ Configuration: Visual Studio integration with standard operators

**Excluded Mutation Operators:**
- String literal replacements (unless testing string validation logic)
- Comment deletions
- Constant assignments in non-logic code (e.g., magic numbers in logging)
- Constructor mutations in dependency injection patterns
```

---

### **CONDITION 3: Define Behavioral Workflows & Integration Points (Critic & Test Architect)**

**Violation:** PRD-1.5 (Behavioral Specification) — Missing specification of *how* teams behave under this law and *when* mutation testing gates are enforced in the TDD cycle.

**Gap:**
- When does mutation testing run in RED→GREEN→REFACTOR cycle?
- What happens when a PR fails the 70% threshold? (Auto-block? Warning? Architect approval gate?)
- How do PHASE_GATE (70%) and HARD_BLOCK (85%) differ operationally?
- Does this law apply retroactively to existing code or only new code?
- How does mutation testing interact with coverage gates (ENG-4.6)?

**Remediation Required:**
Add behavioral specification:
```markdown
**Atomic TDD Cycle Integration (ENG-4.1):**

RED Phase:
├─ Write test (no mutation testing yet)

GREEN Phase:
├─ Write minimal code to pass test
├─ (MANDATORY) Run coverage check: ≥threshold coverage achieved?
├─ (MANDATORY) Run mutation testing on GREEN code
├─ Decision:
│  ├─ Mutation score ≥70% (general) / ≥85% (critical): PASS → proceed to REFACTOR
│  ├─ Mutation score <70%: FAIL → either strengthen test or simplify code
│  └─ If test coverage ≥ but mutation < threshold: Test is brittle (over-mocking likely)

REFACTOR Phase:
├─ Improve code quality while maintaining test passage
├─ (MANDATORY) Re-run mutation testing
└─ Mutation score must remain stable or improve
   └─ If score drops: Refactoring introduced a bug; revert

**SonarQube Gate Behavior:**
- PHASE_GATE (70% general code): Blocks merge if violated; can be waived by reviewer with comment
- HARD_BLOCK (85% critical paths): Blocks merge; waiver requires architect approval + BUS-7.1 audit trail
- All waivers logged in PR audit trail (compliance with BUS-7.1)

**Scope (New Code Only):**
- Mutation testing applies ONLY to changed code in PRs
- Existing code is not retroactively subject to this law
- Teams may voluntarily apply to legacy code as part of refactoring
```

---

### **CONDITION 4: Verify Tool Availability & SonarQube Integration (Critic)**

**Violation:** ENG-12.1 (Codebase State Verification) — Unverified claims about tool support and SonarQube capability.

**Gap:**
- No verification that Stryker, Pitest, mutmut are available in AA's environment
- No evidence that SonarQube PHASE_GATE/HARD_BLOCK configurations exist
- No proof that mutation testing data can be fed into SonarQube

**Remediation Required:**
Verification checklist (to be completed before governance approval):
- [ ] SonarQube version supports mutation score gates (verify with SonarQube docs or plugin)
- [ ] Stryker.js is installed and tested in AA's TypeScript ecosystem
- [ ] Pitest Maven plugin is available for Java projects
- [ ] mutmut is available for Python projects
- [ ] Sample SonarQube quality gate configuration is tested and works
- [ ] CI/CD pipeline can invoke mutation testing in GitHub Actions (or equivalent)
- [ ] Mutation score data is successfully imported into SonarQube dashboard

---

### **CONDITION 5: Define Handling of Equivalent Mutants (Test Architect)**

**Violation:** ENG-4.2 (Test Isolation) — Proposal mentions equivalent mutants but doesn't specify how they're handled in score calculation and SonarQube gating.

**Gap:**
- Some mutations don't change code behavior (e.g., `i > 0` vs. `i >= 0` in loop starting at 1)
- Tools automatically detect some equivalent mutants but miss others
- No specification of how to document equivalent mutants or exclude them from scoring

**Remediation Required:**
Add equivalent mutant handling clause:
```markdown
**Equivalent Mutant Handling:**

1. **Tool Exclusion:** Most tools (Stryker, Pitest) automatically detect and exclude simple equivalent mutants
   └─ Example: Stryker's "compatible mutants" option reduces false positives

2. **Manual Documentation:** For complex equivalent mutants, document in code comment:
   ```javascript
   // ENG-4.11: Equivalent mutation (crew-scheduling/core/assignment.ts:142)
   // Mutation: `if (hoursAccumulated > 8)` → `if (hoursAccumulated >= 8)`
   // Reason: Equivalent because all inputs are integers; boundary is irrelevant
   // Tool: Stryker reports as "equivalent mutation"
   ```

3. **SonarQube Scoring:**
   - Equivalent mutants are EXCLUDED from mutation score calculation
   - Only non-equivalent, killed/survived mutants count toward ≥70%/≥85% thresholds
   - If >10% of mutations are equivalent, notify architect (possible code clarity issue)

4. **Code Review Requirement:**
   - Reviewer must verify equivalent mutant documentation is accurate
   - Flag if documentation is used to artificially inflate mutation score
```

---

### **CONDITION 6: Clarify FIRST Principle Alignment, Especially "Timely" (Test Architect)**

**Violation:** ENG-4.3 (Test Quality Law) — Proposal mentions "validates FIRST principles" but doesn't verify "Timely" aspect (fast execution).

**Gap:**
- Mutation testing adds 2-5x runtime to test suite (vs. coverage alone)
- No specification of acceptable performance overhead
- No definition of "timely" for mutation testing (should tests complete in minutes? hours?)

**Remediation Required:**
Add performance SLA to law:
```markdown
**FIRST Principle Alignment (ENG-4.3):**

| Principle | Mutation Testing Validation | Status |
|-----------|---|---|
| **Fast** | Mutation testing may add 2-5x runtime to test suite | ⚠️ CAUTION: See "Performance SLA" below |
| **Isolated** | Mutations are isolated to single code units; tests run independently | ✅ SATISFIED |
| **Repeatable** | Mutation tool output is deterministic; same code produces same score | ✅ SATISFIED |
| **Self-validating** | Mutation score is automatically calculated and gated via SonarQube | ✅ SATISFIED |
| **Timely** | Mutation testing must complete within development cycle | ⚠️ CONDITIONAL |

**Performance SLA:**
- Unit test mutation testing must complete in <5 minutes for typical project (1000 LOC)
- If mutation testing exceeds 10 minutes, optimize mutation operators or test suite
- Mutation testing runs asynchronously in CI; does not block developer feedback loop
```

---

## REMEDIATION SUMMARY

To unblock this proposal, **all 6 conditions must be addressed**:

1. ✅ Define critical paths explicitly (crew scheduling, dispatch, maintenance contexts)
2. ✅ Specify tool selection criteria and mutation operator scope per language
3. ✅ Define behavioral workflows: RED→GREEN→REFACTOR cycle integration, gate behavior, waivers
4. ✅ Verify tool availability and SonarQube integration (checklist)
5. ✅ Document equivalent mutant handling in score calculations
6. ✅ Clarify FIRST principle alignment and performance SLAs

---

## NEXT STEPS

1. **Create REMEDIATION.md** addressing all 6 conditions with detailed specifications
2. **Integrate remediations into PROPOSAL.md** (expand law content section)
3. **Create verification checklist** (SonarQube, tools, CI/CD integration)
4. **Resubmit for governance approval** with updated proposal

**Timeline:** 2–3 days for remediation, 1 day for resubmission review


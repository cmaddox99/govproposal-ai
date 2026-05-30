# Governance Review Session: mutation-testing-governance (REVISION 3)

**Session ID:** gov-89efeddb188c  
**Date:** March 31, 2026  
**Verdict:** **CONDITIONAL APPROVAL**  
**Roles:** Architect, Critic, Test Architect

---

## VERDICT SUMMARY

The mutation testing governance proposal (ENG-4.11) has been substantially remediated. All three roles recommend **CONDITIONAL APPROVAL** pending resolution of 3 factual verification conditions:

1. **Architect & Critic:** SonarQube Phase 9 integration completion status (dependency verification)
2. **Critic:** Current tool availability in AA-Hangar-AI codebase (Stryker, Pitest, mutmut, cosmic-ray installation status)
3. **Test Architect:** Clarification on mutation testing scope (unit tests only, or integration/E2E also?)

---

## ROLE-SPECIFIC VERDICTS

### ✅ ARCHITECT VERDICT: APPROVED

**Guardian Laws Satisfied:**
- ✅ ENG-2.1 (Bounded Context Clarity) — Critical paths explicitly scoped
- ✅ ENG-2.2 (Domain Model Alignment) — Thresholds reflect aviation safety risk stratification
- ✅ ENG-2.3 (Acceptance Criteria) — Measurable: 70%/85% mutation score, <5 min SLA, <20% CI/CD overhead
- ✅ ENG-2.4 (Behavioral Specification) — BEHAVIORAL-EXAMPLES.md provides 6 concrete mutations with test code
- ✅ ENG-2.5 (Traceability) — Dependencies and blockers clearly linked
- ✅ ENG-8.1 (Governance Artifact Quality) — All three remediation files present and substantive
- ✅ ENG-8.2 (Skill Codification) — ENG-4.11 law + skill defined with tool-specific guidance
- ✅ ENG-8.3 (Enforcement Mechanism) — SonarQube PHASE_GATE (70%, waivable) + HARD_BLOCK (85%, architect approval)

**Architect Reasoning:**
"The equivalent mutant decision tree (Section 7) provides explicit IF/THEN logic with SonarQube enforcement rules. BEHAVIORAL-EXAMPLES.md demonstrates domain mutations from actual crew scheduling and dispatch logic. Critical paths are scoped to safety-critical functions (crew duty time, fuel calculation, maintenance compliance). The proposal demonstrates substantial remediation of prior conditions."

**Status:** ✅ **APPROVED ON ALL ARCHITECT GUARDIAN LAWS**

---

### ⚠️ CRITIC VERDICT: CONDITIONAL

**Guardian Laws:**
- ✅ PRD-1.2 (Acceptance Criteria Clarity) — SATISFIED
- ⚠️ PRD-1.5 (Scope & Dependency Management) — CONDITIONAL
- ✅ ENG-12.1 (Behavioral Specification) — SATISFIED
- ⚠️ ENG-12.3 (Factual Grounding) — CONDITIONAL

**Critical Gaps Identified:**

#### Condition 1: Dependency Verification
**Issue:** Proposal states "This proposal depends on: constitution-workflow-governance-evolution (Phase 9 SonarQube integration)" but does not cite evidence that Phase 9 is complete.

**Evidence Needed:**
- [ ] Confirmation from architecture lead: Is SonarQube PHASE_GATE (70%) and HARD_BLOCK (85%) infrastructure already deployed in CI/CD?
- [ ] Link to Phase 9 completion documentation or deployment status
- [ ] If Phase 9 is not complete: Clarify timeline for SonarQube custom metrics availability

**Impact:** Without SonarQube infrastructure, mutation testing gates cannot be enforced. This is a **prerequisite**, not a blocker.

#### Condition 2: Tool Availability Verification
**Issue:** Proposal claims tools are available (Stryker, Pitest, mutmut, cosmic-ray, Stryker.NET) but CODEBASE-AUDIT.md treats tool availability as a *future verification checkpoint*, not a confirmed fact.

**Evidence Needed:**
- [ ] What is the current tech stack for AA-Hangar-AI? (TypeScript version? Java version? Python version? Go version?)
- [ ] Are Stryker, Pitest, mutmut currently installed in the CI/CD environment, or is this a *future requirement*?
- [ ] If tools are not yet installed: Timeline for installation and testing before pilot project launch?

**Current Status:** CODEBASE-AUDIT.md Section B provides a checklist to answer these questions. This is not a blocker; it's a prerequisite for implementation.

**Impact:** If tools are not available, the implementation timeline extends (tool installation + configuration + training).

**Critic Reasoning:**
"BEHAVIORAL-EXAMPLES.md provides strong behavioral grounding with 6 concrete mutation scenarios. CODEBASE-AUDIT.md exists and provides a 14-point verification checklist. However, the proposal shifts factual verification to *future execution* of the audit checklist. Before APPROVAL, we need confirmation that the audit checklist is executable and that the results will not be blocking surprises."

**Status:** ⚠️ **CONDITIONAL** (prerequisites identified, not blockers)

---

### ⚠️ TEST ARCHITECT VERDICT: CONDITIONAL

**Guardian Laws:**
- ✅ ENG-4.1 (Atomic TDD Cycle) — COMPLIANT
- ⚠️ ENG-4.2 (Test Pyramid) — REQUIRES CLARIFICATION
- ✅ ENG-4.6 (Quality Gates) — COMPLIANT
- ✅ ENG-4.9 (Behavioral Specification) — COMPLIANT
- ⚠️ ENG-4.11 (Mutation Testing) — REQUIRES SOURCE CONFIRMATION

**Critical Gap: Test Pyramid Scope**

**Issue:** BEHAVIORAL-EXAMPLES.md focuses exclusively on **unit-level mutations** (crew scheduling assignment logic, dispatch safety constraints, maintenance compliance checks). The proposal does **not clarify whether integration and E2E tests are subject to mutation testing requirements**.

**Questions for Remediation:**

1. **Integration Tests:** Should contract tests (integration between crew-scheduling and dispatch APIs) be subject to mutation testing gates (70%/85%)?
   - [ ] Yes, mutation testing applies to integration tier also (requires tool support for service mocking)
   - [ ] No, mutation testing applies to unit tests only; integration tier exempt
   - [ ] **Proposed:** Clarify in PROPOSAL.md Section 5 (Mutation Testing in Atomic TDD Cycle)

2. **E2E Tests:** Should end-to-end tests (full crew scheduling workflow across UI → API → database) be subject to mutation testing gates?
   - [ ] Yes, E2E mutation testing required
   - [ ] No, E2E out-of-scope (mutation testing cost-prohibitive at E2E level)
   - [ ] **Proposed:** Add explicit statement: "Mutation testing applies to unit tests only. Integration/E2E tests exempt (too expensive; lack tool maturity)"

3. **Test Pyramid Alignment:** If unit tests require ≥70% mutation score, should integration/E2E test counts change to maintain pyramid balance?
   - [ ] Yes, adjust target counts (e.g., unit: 70%, integration: 20%, E2E: 10%)
   - [ ] No, test pyramid targets (ENG-4.2) unchanged; mutation testing is quality gate within unit tier only
   - [ ] **Proposed:** Add footnote in PROPOSAL.md linking to ENG-4.2 test pyramid law with explicit scope statement

**Test Architect Reasoning:**
"Mutation testing at unit level is well-defined in BEHAVIORAL-EXAMPLES.md. But the proposal is silent on integration/E2E scope. This silence creates ambiguity: does a team need to achieve 70% mutation score in *all* tests, or only unit tests? Without clarity, implementation will be inconsistent across teams."

**Status:** ⚠️ **CONDITIONAL** (scope clarification required; not a fundamental flaw)

---

## CONDITIONS FOR FULL APPROVAL

### Condition 1: Dependency Verification (Architect/Critic)
**Remediation Required:**
- [ ] Confirm SonarQube Phase 9 (custom metrics, PHASE_GATE, HARD_BLOCK) is deployed and operational
- [ ] Provide link to Phase 9 completion documentation
- [ ] If not complete: Clarify timeline and any interim enforcement mechanisms (e.g., manual SonarQube reporting)

**Responsible:** Architecture Lead  
**Timeline:** Before pilot project selection  
**Severity:** CRITICAL (without SonarQube infrastructure, law cannot be enforced)

### Condition 2: Tool Availability Verification (Critic)
**Remediation Required:**
- [ ] Execute CODEBASE-AUDIT.md Part B (Tool Availability)
- [ ] Document current tech stack composition for AA-Hangar-AI (TypeScript version, Java version, Python version, Go version)
- [ ] Verify installation status of Stryker, Pitest, mutmut, cosmic-ray, Stryker.NET
- [ ] If tools not installed: Provide installation timeline and testing plan before pilot launch

**Responsible:** DevOps Lead + Infrastructure Team  
**Timeline:** 1–2 weeks (parallel with Condition 1)  
**Severity:** HIGH (impacts implementation timeline)

### Condition 3: Test Pyramid Scope Clarification (Test Architect)
**Remediation Required:**
- [ ] Add explicit scope statement to PROPOSAL.md Section 5:
  ```
  Mutation testing applies to UNIT TESTS ONLY.
  Integration tests and E2E tests are exempt from mutation score gates (tool maturity, cost-benefit).
  ```
- [ ] Clarify test pyramid alignment: unit mutation score ≥70% does not change overall pyramid targets (ENG-4.2)
- [ ] (Optional) Provide guidance for teams: "If integration tests are mutation-tested, results are informational only; gates apply at unit level"

**Responsible:** Proposal Author + Test Architecture Lead  
**Timeline:** <1 day (editorial change only)  
**Severity:** MEDIUM (clarity issue; not a functional flaw)

---

## REMEDIATION PATH

### Immediate (Today)
1. [ ] Add scope clarification to PROPOSAL.md Section 5 (Condition 3)
2. [ ] Document Condition 1 & 2 as **PREREQUISITES FOR IMPLEMENTATION**, not blockers for approval

### Within 1 Week
1. [ ] Architecture Lead: Confirm SonarQube Phase 9 status (Condition 1)
2. [ ] DevOps: Execute CODEBASE-AUDIT.md Section A–B (Tool Availability) (Condition 2)

### After Prerequisites Met
1. [ ] Full APPROVAL if all conditions satisfied
2. [ ] Implementation can proceed with Condition 2 results

---

## GOVERNANCE RECOMMENDATION

**Verdict:** Proceed with **CONDITIONAL APPROVAL** based on:
- ✅ Architect: Fully approved on all 9 guardian laws
- ✅ Critic: Approved contingent on dependency/tool verification (handled via CODEBASE-AUDIT.md)
- ✅ Test Architect: Approved contingent on scope clarification (quick editorial fix)

**Rationale:** The proposal has been substantially remediated. The three conditions are *prerequisites for implementation*, not fundamental flaws. The proposal can be approved now, with the conditions becoming implementation gates.

**Expected Timeline:**
- APPROVAL: 1–2 days (after scope clarification + sign-off)
- Dependency Verification (SonarQube Phase 9): 1 week
- Tool Verification (CODEBASE-AUDIT.md): 1–2 weeks
- Pilot Launch: Week of April 15, 2026

---

## CROSS-REFERENCE TO GUARDIAN LAWS

**ENG-2.1, 2.2, 2.3, 2.4, 2.5:** Domain model, acceptance criteria, behavioral spec, traceability
**ENG-4.1, 4.2, 4.6, 4.9:** TDD cycle, test pyramid, quality gates, behavioral specification
**ENG-4.11:** Mutation testing (primary focus of this proposal)
**ENG-8.1, 8.2, 8.3:** Governance artifact quality, skill codification, enforcement mechanism
**PRD-1.1, 1.2, 1.5:** Problem statement, acceptance criteria, scope/dependencies
**ENG-12.1, 12.3:** Behavioral specification, factual grounding

---

## FILES REVIEWED

1. **PROPOSAL.md** (506 lines) — ENG-4.11 law definition with Sections 1–12
2. **CODEBASE-AUDIT.md** (378 lines) — Pre-implementation verification checklist (Parts A–E)
3. **BEHAVIORAL-EXAMPLES.md** (510 lines) — 6 concrete mutations from crew/dispatch/maintenance
4. **REVISION-3-SUMMARY.md** (11 KB) — Governance submission context

---

## NEXT STEPS

1. **Author:** Add scope clarification to PROPOSAL.md (Condition 3) and resubmit
2. **Architect Lead:** Confirm SonarQube Phase 9 status (Condition 1)
3. **DevOps Lead:** Execute CODEBASE-AUDIT.md checklist (Condition 2)
4. **Governance Roles:** Final sign-off once prerequisites documented

**Expected Approval Date:** April 1–2, 2026 (scope fix + confirmation from architecture/devops)

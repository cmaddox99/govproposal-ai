# Mutation Testing Governance — Implementation Prerequisites

**Status:** Ready for parallel execution (NOT blockers; can proceed during final governance review)

**Timeline:** 1–2 weeks (parallel execution)  
**Target Completion:** Week of April 8, 2026 (before pilot launch April 15)

---

## Overview

Governance review (Session: gov-89efeddb188c) returned **CONDITIONAL APPROVAL** from all 3 roles (architect, critic, test-architect). Three conditions must be verified before production pilot launch:

1. ✅ **Test Architect Condition 3** — Scope clarification (RESOLVED in PROPOSAL.md Revision 3)
2. ⚠️ **Critic Condition 1** — SonarQube Phase 9 infrastructure verification
3. ⚠️ **Critic Condition 2** — Tool availability audit (Stryker, Pitest, mutmut, cosmic-ray)

---

## Action Items

### ACTION ITEM 1: Verify SonarQube Phase 9 (PHASE_GATE/HARD_BLOCK) Infrastructure

**Assigned to:** Architecture Lead  
**Priority:** High  
**Effort:** 2–4 hours (verification + demo)  
**Blocks:** SonarQube CI/CD gate enforcement

**Acceptance Criteria:**
- [ ] SonarQube Phase 9 instance is deployed and accessible via CI/CD pipeline
- [ ] PHASE_GATE enforcement (70% mutation score) blocks PRs without override
- [ ] HARD_BLOCK enforcement (85% mutation score) blocks PRs and requires architect sign-off
- [ ] Audit trail integration (PR comments, BUS-7.1 compliance logging) is functional
- [ ] Override workflow tested: architect can waive gate with audit trail entry
- [ ] Proof of concept (PoC) with sample mutation test result attached to verification ticket

**Related Laws:** ENG-2.3 (Gating), ENG-4.11 (Runtime Process Enforcement), BUS-7.1 (Audit Trail)

**Exit Criteria:**
- SonarQube Phase 9 is production-ready
- Gate behavior has been validated in staging with a test PR
- Documentation link to Phase 9 configuration published to team wiki

---

### ACTION ITEM 2: Audit Tool Availability & Compatibility

**Assigned to:** DevOps Lead  
**Priority:** High  
**Effort:** 4–6 hours (audit + compatibility matrix)  
**Blocks:** Pilot rollout to specific languages/frameworks

**Description:**
Execute `/governance/AA-Hangar-AI-Constitution/hangar-ai-specs/changes/mutation-testing-governance/CODEBASE-AUDIT.md` to verify tool availability across the codebase.

**Acceptance Criteria:**
- [ ] All languages in active codebase have at least one compatible mutation testing tool
- [ ] Tool installation verified in CI/CD pipeline (Docker, npm, pip, Maven, Gradle, etc.)
- [ ] Tool execution time benchmarked for each language (RED phase + GREEN phase + REFACTOR phase)
- [ ] Timeout recommendations documented (e.g., "Stryker 15 min max per test suite")
- [ ] False positive rate (equivalent mutants, unreachable code) estimated for each tool
- [ ] Rollback plan documented if a language/tool is incompatible

**Tool Checklist (from CODEBASE-AUDIT.md):**
- [ ] **JavaScript/TypeScript** — Stryker (primary) or mutmut (secondary)
- [ ] **Java** — Pitest (primary) or mutmut (secondary)
- [ ] **Python** — mutmut (primary) or cosmic-ray (secondary)
- [ ] **Go** — cosmic-ray or custom tool (verify feasibility)
- [ ] **.NET/C#** — Stryker.NET (verify availability)

**Related Laws:** ENG-8.1 (Tool Maturity), ENG-8.2 (Integration), ENG-8.3 (Observability)

**Exit Criteria:**
- Tool compatibility matrix published (language × tool, execution time, maturity rating)
- DevOps confirms CI/CD integration is feasible for Phase 9 gates
- Any language/tool gaps flagged with mitigation plan

---

### ACTION ITEM 3: Phase Gate Entry Verification (Architect Requirement)

**Assigned to:** Architecture Lead  
**Priority:** High  
**Effort:** 2–3 hours (checklist verification)  
**Blocks:** Pilot launch readiness

**Description:**
Verify all items in MUTATION-TESTING-PHASE-GATE-SPEC.md before gate activation.

**Acceptance Criteria:**
- [ ] Codebase alignment audit complete (frameworks, versions compatible)
- [ ] Tool compatibility matrix reviewed (all tools ready for deployment)
- [ ] Phase gate success criteria approved (thresholds, rollback triggers)
- [ ] Stakeholder sign-off collected (E2E exemption approved by product/architecture/tech lead)
- [ ] Governance ownership assigned to Test Architect

**Exit Criteria:**
- Phase gate entry verification checklist 100% complete
- All required sign-offs collected and documented
- Ready for gate activation

---

### ACTION ITEM 4: Phase Gate Enforcement Configuration (Sentinel Requirement)

**Assigned to:** DevOps Lead  
**Priority:** High  
**Effort:** 2–3 hours (CI/CD configuration)  
**Blocks:** Pilot launch readiness

**Description:**
Configure phase gate enforcement in SonarQube Phase 9 and CI/CD pipeline.

**Acceptance Criteria:**
- [ ] Tool execution timeout enforcement configured (Pitest 20 min, Stryker 15 min, mutmut 10 min)
- [ ] Scope boundary enforcement configured (unit tests only, integration/E2E excluded)
- [ ] Architect approval workflow tested and documented
- [ ] Gate activation procedures documented

**Exit Criteria:**
- Phase gate enforcement ready for activation
- Documentation published to team wiki
- Ready for pilot launch

---

## Governance Review Schedule

| Task | Owner | Start | Target Completion | Status |
|------|-------|-------|-------------------|--------|
| Scope clarification fix (Test Architect Condition 3) | @product-lead | ✅ Done | ✅ 2026-04-01 | Complete |
| SonarQube Phase 9 verification (Critic Condition 1) | @architecture-lead | 2026-04-02 | 2026-04-08 | 🔄 Ready |
| Tool audit & compatibility (Critic Condition 2) | @devops-lead | 2026-04-02 | 2026-04-08 | 🔄 Ready |
| Phase gate entry verification (Architect Requirement) | @architecture-lead | 2026-04-02 | 2026-04-08 | 🔄 Ready |
| Phase gate enforcement config (Sentinel Requirement) | @devops-lead | 2026-04-02 | 2026-04-08 | 🔄 Ready |
| PROPOSAL.md resubmission to governance | @product-lead | 2026-04-02 | 2026-04-02 | ✅ Done |
| Phase gate spec resubmission to governance | @product-lead | 2026-04-01 | 2026-04-01 | ⏳ Pending |
| Final governance sign-off (FULL APPROVAL expected) | @governance-council | 2026-04-01 | 2026-04-02 | ⏳ Pending |
| Pilot launch | @product-lead | 2026-04-15 | 2026-04-22 | ⏳ Pending |

---

## Communication Plan

1. **Immediate (2026-04-02):** Share this ACTION ITEMS file with Architecture Lead and DevOps Lead
2. **Daily standups:** Quick sync on SonarQube Phase 9 and tool audit progress
3. **2026-04-08:** Collect verification evidence from both owners
4. **2026-04-08:** Resubmit PROPOSAL.md to governance with evidence attachments
5. **2026-04-12:** Expected final approval; begin pilot onboarding

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| SonarQube Phase 9 not deployed | Fallback: Use SonarQube quality gates (less strict) until Phase 9 available; pilot on subset of repos |
| Tool X incompatible with language Y | Exclude language from pilot; defer to Phase 2 rollout; use manual gates if no tool available |
| Mutation test execution timeout exceeds CI/CD limits | Parallelize test suites; split critical paths; adjust thresholds; document trade-offs |

---

## Notes

- These prerequisites are **NOT blockers** for governance approval; they are implementation readiness checks
- Governance review can conclude while these tasks proceed in parallel
- Pilot launch (April 15) gates on completion of both ACTION ITEMS
- See `CODEBASE-AUDIT.md` for detailed tool evaluation criteria
- See `BEHAVIORAL-EXAMPLES.md` for team onboarding scripts and examples
- See `GOVERNANCE-REVIEW-REVISION3.md` for full feedback from all 3 governance roles

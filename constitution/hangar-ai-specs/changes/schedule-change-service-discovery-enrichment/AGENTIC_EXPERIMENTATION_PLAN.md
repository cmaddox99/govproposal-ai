# AGENTIC_EXPERIMENTATION_PLAN: Schedule Change Self-Serve

**Status:** Draft  
**Planning Horizon:** 90 days  
**Law Anchors:** PRD-4.1, PRD-5.1, ENG-9.4, BUS-7.1

**Law References:**
1. [PRD-4.1: MVP Definition](../../../laws/product/roadmap.md)
2. [PRD-5.1: Metrics and Success Definition](../../../laws/product/metrics.md)
3. [ENG-9.4: Human Override Governance](../../../laws/engineering/governance.md)
4. [BUS-7.1: Risk Stratification](../../../laws/business/risk.md)

---

## Experiment Goals

1. Reduce avoidable escalations by improving eligibility explainability
2. Improve discovery-to-delivery speed for recurring rule-quality and observability tasks
3. Validate low-risk agentic workflows before any booking mutation scenarios

---

## Pilot A: Eligibility Explanation Assistant (Read-Only)

**Hypothesis:** A citation-grounded assistant reduces ineligible-flow escalation and improves customer clarity.

**Scope:**
- Explain ineligibility reason and alternatives
- No mutation authority
- Human fallback always available

**Success Metrics:**
- Escalation rate in ineligible cohort reduced by >=20%
- Clarity score increased by >=1.0 point
- Unauthorized mutation events = 0

**Rollback Criteria:**
- Explanation accuracy below 90%
- Hallucinated policy statements above threshold

---

## Pilot B: Audit Completeness Checker

**Hypothesis:** Automated checks reduce missing audit fields and improve compliance readiness.

**Scope:**
- Detect missing/invalid decision and override fields
- Produce remediation report by service/team

**Success Metrics:**
- Audit completeness improves to >=99%
- Time-to-detect audit defects reduced by >=50%

**Rollback Criteria:**
- False positive rate blocks operational usage
- Checker runtime overhead exceeds agreed budget

---

## Governance Controls

1. Human approval required for any policy-impacting recommendation.
2. Read-only mode default for all customer-facing agent interactions.
3. Full recommendation and outcome logging for audit and review.
4. Weekly review with Product + Engineering + Compliance.

---

## Decision Gates

- Gate 1: Instrumentation and baseline validation complete
- Gate 2: Pilot A meets quality and safety thresholds
- Gate 3: Pilot B proves compliance value
- Gate 4: Decide whether to expand, harden, or stop agentic scope

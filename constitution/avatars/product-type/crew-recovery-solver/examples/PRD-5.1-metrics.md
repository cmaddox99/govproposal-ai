---
avatar: avatar-product-crew-recovery-solver
law: PRD-5.1
title: "MVP Law"
---

# PRD-5.1 — MVP Law: Crew Recovery Application

## What This Law Requires
The crew recovery MVP ships only when FAR Part 117 enforcement and audit trail are both fully functional. No "Phase 2" for safety or compliance features.

## Compliant Example

**CWR MVP Gate Criteria**

The MVP is releasable only when ALL of the following are true:

| Gate | Criteria | Non-negotiable? |
|------|----------|-----------------|
| FAR 117 enforcement | 100% of options filtered through eligibility check | YES — BUS-2.1 |
| Audit trail | Every accept/reject/override produces audit record | YES — BUS-7.1 |
| Correlation ID | Every audit record contains event correlation_id | YES — ENG-6.7 |
| Evidence scoring | Options ranked by recovery_score with factor breakdown | YES — PRD-1.5 |
| Scheduler notification | Recovery options visible within 3 min of IROP event | Performance SLA |
| Crew notification | Assignment notification within 5 min of commitment | Service SLA |

**What is NOT required for MVP:**
- FRMS (fatigue risk) integration (enhances score; not required for safety gate)
- Historical pattern analysis
- Multi-event concurrent recovery UI

**Constitutional check:** PRD-5.1 — MVP is the smallest safe slice that delivers regulatory-compliant crew recovery. Safety gates are present from day one.

## Violation Example
```
❌ "Ship v1 with manual FAR 117 check — we'll automate it in v2."
   → FAR 117 enforcement is non-negotiable (BUS-2.1); manual check is not equivalent.
   → Violates PRD-5.1: MVP ships with known compliance gap.
```

## Edge Cases & Warnings
- "Audit trail" means immutable log — not a UI display. The record must be written even if the UI is not yet built
- The MVP gate is binary — partial compliance (e.g., 90% of events logged) does not pass

---
avatar: avatar-product-crew-recovery-solver
law: PRD-2.5
title: "Discovery Stage-Gate Law"
---

# PRD-2.5 — Discovery Stage-Gate Law: Crew Recovery Application

## What This Law Requires
CWR discovery stages must progress sequentially with documented evidence gates filed in `hangar-ai-specs/`. No stage may begin without prior stage exit criteria met and evidence filed.

## Compliant Example

**CWR Discovery Stage Gates**

| Stage | Exit Criteria | Evidence Filed |
|-------|--------------|----------------|
| Stage A — Problem | Validated problem statement with scheduler interview data | `hangar-ai-specs/changes/cwr-001/stage-a-problem.md` |
| Stage B — User | Journey map validated with ≥4 scheduler observation sessions | `hangar-ai-specs/changes/cwr-001/stage-b-journey.md` |
| Stage C — Domain | FAR 117 rules modeled and reviewed by compliance team | `hangar-ai-specs/changes/cwr-001/stage-c-domain.md` |
| Stage D — MVP Scope | MVP gates defined; FAR 117 + audit trail confirmed non-negotiable | `hangar-ai-specs/changes/cwr-001/stage-d-mvp.md` |
| Stage E — Spec | Executable specs written for all MVP scenarios | `hangar-ai-specs/specs/crew-recovery-solver/` |
| Stage F — Build | TDD cycle begins only after Stage E approval | — |

**Gate enforcement:** Each stage document includes a `status: GATE_PASSED` field before the next stage begins. Product Manager and Compliance Analyst both sign off on Stage C.

**Constitutional check:** PRD-2.5 — no feature spec written (Stage E) until domain model is compliance-reviewed (Stage C exit).

## Violation Example
```
❌ Engineering begins writing specs while scheduler interviews are still in progress.
   → Stage E started before Stage B exit criteria are met.
   → Violates PRD-2.5: stages not sequential; undiscovered journey steps built into spec.
```

## Edge Cases & Warnings
- FAR 117 domain modeling (Stage C) requires aviation compliance team review — this gate cannot be self-certified by the product team
- Stage D MVP scope approval must explicitly confirm audit trail and FAR 117 as non-negotiable (not deferred to v2)

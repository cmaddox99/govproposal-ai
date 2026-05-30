---
avatar: avatar-product-ballot-trading
law: PRD-2.5
title: "Discovery Stage-Gate Law"
---

# PRD-2.5 — Discovery Stage-Gate Law: Ballot Trading Application

## What This Law Requires

Ballot trading discovery stages must progress sequentially with documented evidence
gates filed in `hangar-ai-specs/`. No stage may begin without the prior stage's
exit criteria met and evidence filed. CBA review is a mandatory gate in Stage C.

## Compliant Example

**Ballot Trading Discovery Stage Gates**

| Stage | Exit Criteria | Evidence Filed |
|-------|--------------|----------------|
| Stage A — Problem | Validated problem statement with pilot interview data and session telemetry | `hangar-ai-specs/changes/btrade-001/stage-a-problem.md` |
| Stage B — User | Journey map validated with ≥4 pilot observation sessions across ≥2 domiciles | `hangar-ai-specs/changes/btrade-001/stage-b-journey.md` |
| Stage C — Domain | CBA eligibility rules modeled and reviewed by Labor Relations and CBA Compliance Analyst | `hangar-ai-specs/changes/btrade-001/stage-c-domain.md` |
| Stage D — MVP Scope | MVP gates defined; audit trail and CBA traceability confirmed non-negotiable | `hangar-ai-specs/changes/btrade-001/stage-d-mvp.md` |
| Stage E — Spec | Executable specs written for all MVP scenarios including rejection paths | `hangar-ai-specs/specs/ballot-trading/` |
| Stage F — Build | TDD cycle begins only after Stage E approval | — |

**Gate enforcement:** Each stage document includes a `status: GATE_PASSED` field
before the next stage begins. Labor Relations and CBA Compliance Analyst both
sign off on Stage C — this gate cannot be self-certified by the product team.

**Constitutional check:** PRD-2.5 — no feature spec written (Stage E) until CBA
domain model is compliance-reviewed (Stage C exit). Spec work on a new CBA
article's eligibility logic requires returning to Stage C if the article changes.

## Violation Example

```
❌ Engineering begins writing specs for seniority-based batch awards while CBA
   article review by Labor Relations is still pending.
   → Stage E started before Stage C exit criteria are met.
   → Violates PRD-2.5: CBA compliance risk embedded in spec without Labor review.
   → If CBA interpretation changes after spec is written, all spec work is invalid.
```

## Edge Cases & Warnings

- CBA domain modeling (Stage C) requires Labor Relations sign-off — a product
  manager cannot self-certify CBA rule interpretation; incorrect CBA logic is a
  contractual liability.
- If a new CBA cycle opens mid-discovery, Stage C must be re-entered to validate
  that the domain model reflects the updated contract.
- Stage D MVP scope approval must explicitly confirm that audit trail (BUS-7.1)
  and CBA traceability (BUS-2.2) are non-negotiable scope items, not v2 deferrals.

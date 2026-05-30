---
avatar: avatar-product-crew-recovery-solver
law: PRD-6.2
title: "Retention Over Acquisition Law"
---

# PRD-6.2 — Retention Over Acquisition Law: Crew Recovery Application

## What This Law Requires
CWR must prioritize retaining scheduler and crew adoption over acquiring new feature users. System reliability and trust — especially after a failed recovery — matter more than adding new recovery scenarios before existing ones are stable.

## Compliant Example

**Retention-Driven Roadmap Prioritization**

```
Post-MVP Review (after 30-day production operation):

Scheduler adoption rate: 78% (target: 85%)
Drop-off pattern: Schedulers revert to manual process after any system error
Root cause: When audit write fails (Scenario F2), error message is unclear

Retention decision: Fix F2 error UX + add retry capability BEFORE shipping
cascading multi-leg disruption (next planned feature)

Evidence: 6 schedulers interviewed; "I don't trust it when it errors" — 4/6
```

**Constitutional check:** PRD-6.2 — scheduler retention (trust and reliability) prioritized over acquiring the next use case. New feature gated until retention target met.

## Violation Example
```
❌ Ship cascading delay feature while 22% of schedulers still revert to manual
   process due to unclear error handling.
   → Acquisition of new scenarios while existing users are not retained.
   → Violates PRD-6.2: retention must be solved before new acquisition.
```

## Edge Cases & Warnings
- For safety-critical tools, "retention" includes trust in compliance — a scheduler who bypasses CWR due to a confusing error is a regulatory risk, not just a product metric
- Crew member notification reliability is also a retention signal — if crew don't trust assignment notifications, they call dispatch instead, defeating the system

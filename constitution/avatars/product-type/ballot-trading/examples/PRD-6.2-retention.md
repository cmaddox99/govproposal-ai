---
avatar: avatar-product-ballot-trading
law: PRD-6.2
title: "Retention Over Acquisition Law"
---

# PRD-6.2 — Retention Over Acquisition Law: Ballot Trading Application

## What This Law Requires

The ballot trading platform must prioritize retaining existing pilot adoption over
acquiring new feature users. Pilot trust — especially after an incorrect rejection
or a CBA dispute — matters more than adding new trade scenarios before existing
ones are reliable and well-understood.

## Compliant Example

**Retention-Driven Roadmap Prioritization**

```
Post-MVP Review (after first full ballot period in production):

Pilot adoption rate: 72% (target: 90%)
Drop-off pattern: Pilots revert to calling the scheduler after any unexpected
  DUTY_TIME_LIMIT_EXCEEDED rejection, even when the rejection is correct.
Root cause: Rejection reason code is technically accurate but not pilot-readable;
  "duty_time_limit: 85.0 / limit: 80.0" does not map to CBA Article language.

Retention decision: Improve rejection message clarity and add a CBA article
  deep-link BEFORE shipping the next planned feature (bulk batch submission).

Evidence: 9 pilots interviewed post-ballot; "I didn't trust it so I called —
  I don't know what duty time means" — 6/9 pilots
```

**Constitutional check:** PRD-6.2 — pilot retention (trust in rejection clarity)
prioritized over acquiring the next use case (batch submission). New feature gated
until retention target of 90% adoption is met or root cause is addressed.

## Violation Example

```
❌ Ship bulk batch submission feature while 28% of pilots still revert to
   scheduler calls after their first rejection — due to opaque error messages.
   → Acquisition of new trade scenarios while existing pilots are not retained.
   → Violates PRD-6.2: retention must be solved before new acquisition.
   → Risk: pilots who don't trust individual trades will not trust bulk submission either.
```

## Edge Cases & Warnings

- For CBA-governed workflows, "retention" includes trust in contractual accuracy —
  a pilot who bypasses the system because they distrust the eligibility check
  is a compliance risk, not just a product metric.
- Scheduler adoption is also a retention signal — if schedulers route around the
  system to approve trades manually, the audit trail breaks (BUS-7.1).
- Retention is measured per ballot period, not per sprint — a pilot who used the
  system once and reverted counts as churned for that period.

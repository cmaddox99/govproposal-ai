---
avatar: avatar-product-crew-recovery-solver
law: PRD-2.1
title: "Problem Validation Law"
---

# PRD-2.1 — Problem Validation Law: Crew Recovery Core Journey

## What This Law Requires
The core crew recovery journey must be validated against real scheduler behavior before any feature is built. Assumptions about how schedulers make assignment decisions must be tested.

## Compliant Example

**Core Journey: Single Flight Cancellation Recovery**

```
TRIGGER: Flight AA1234 cancelled (mechanical)
  ↓
1. IROP event published to CWR message bus
   (correlation_id: cwr-event-{uuid})
  ↓
2. CWR resolves affected crew roster for AA1234
  ↓
3. For each affected crew member:
   a. Compute FAR 117 eligibility window (HARD GATE)
   b. Query available replacement flights within eligibility window
   c. Score each option (experience, proximity, fatigue)
   d. Filter: remove any option where far_117_eligible=False
  ↓
4. Present scored recovery options to SOC Scheduler
   (options sorted by recovery_score DESC)
  ↓
5. Scheduler selects option (or requests manual override)
  ↓
6. Assignment committed → audit record written
   (includes: crew_id, flight, score, factors, acting_user, timestamp, far_117_margin)
  ↓
7. Crew member notified via crew notification service
```

**Validated assumptions (from journey interview sessions):**
- Schedulers review ≥3 options before selecting in 80% of IROP events
- FAR 117 eligibility check failure is the #1 reason a preferred option is unavailable
- Audit record review happens during the event (not just post-IROP) in 60% of cases

## Violation Example
```
❌ CWR auto-assigns crew to first available slot without scheduler review.
   → Removes human judgment from safety-critical decision.
   → Violates PRD-2.1: journey not validated; assumes auto-assignment is acceptable.
```

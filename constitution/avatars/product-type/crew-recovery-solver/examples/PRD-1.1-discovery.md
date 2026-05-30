---
avatar: avatar-product-crew-recovery-solver
law: PRD-1.1
title: "Customer-Centric Law"
---

# PRD-1.1 — Customer-Centric Law: Crew Recovery Application

## What This Law Requires
Discovery research must surface the actual pain points of crew schedulers and crew members during IROP events — not assumed operational metrics.

## Compliant Example

**Discovery Sprint: IROP Recovery Scheduler Pain Points**

Continuous discovery session findings (from 6 scheduler interviews + 4 crew member interviews):

| Persona | Pain Point | Evidence Signal |
|---------|-----------|-----------------|
| Crew Scheduler | Must cross-reference 3 systems to check FAR 117 eligibility | 5/6 schedulers; avg 8 min per assignment |
| Crew Scheduler | Can't see why a recovery option was rejected by the system | 4/6 schedulers; leads to manual workarounds |
| Crew Member | Not notified of new assignment until 30 min before report time | 4/4 crew members; FAR 117 rest disputes |
| Operations Manager | Audit trail only available day-after — can't review during event | 3/3 managers in post-IROP debrief |

**Outcome:** Discovery confirms that the #1 scheduler need is **consolidated FAR 117 eligibility view at option selection time**, not faster assignment processing.

**Constitutional check:** PRD-1.1 — customer problem (scheduler visibility) drives feature priority, not operational throughput assumption.

## Violation Example
```
❌ "We need to reduce MTTR for IROP events by 20%."
   → Metric-first without interviewing schedulers or crew.
   → Violates PRD-1.1: output metric assumed, not discovered from customer behavior.
```

## Edge Cases & Warnings
- Schedulers and crew members have opposing interests during IROP — discovery must interview both; do not proxy crew needs through scheduler accounts
- Compliance Analysts are underrepresented in discovery — include them; they surface audit trail gaps that surface 6+ months later

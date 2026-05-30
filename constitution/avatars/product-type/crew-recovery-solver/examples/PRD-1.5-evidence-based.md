---
avatar: avatar-product-crew-recovery-solver
law: PRD-1.5
title: "Evidence-Based Decision Law"
---

# PRD-1.5 — Evidence-Based Decision Law: Crew Recovery Application

## What This Law Requires
Recovery options presented to schedulers must be ranked by evidence-scored criteria, not arbitrary system order. Each option must show its scoring rationale.

## Compliant Example

**Recovery Option Scoring Model**

```python
@dataclass
class RecoveryOption:
    crew_id: str
    flight_assignment: str
    recovery_score: float  # 0.0–1.0

    # Factor breakdown (visible to scheduler)
    far_117_margin_hours: float       # weight: 0.40
    experience_match_score: float     # weight: 0.30 (position/aircraft type)
    proximity_score: float            # weight: 0.20 (current location)
    fatigue_score: float              # weight: 0.10 (FRMS model output)

    far_117_eligible: bool            # HARD GATE — False removes from list entirely
    override_justification: str | None  # Required if scheduler selects non-top option
```

**UI requirement:** Options list displays score and top contributing factor. Scheduler who selects a lower-ranked option must enter a justification (logged to audit trail).

**Constitutional check:** PRD-1.5 — decision to assign is grounded in evidence (FAR 117 status, experience, proximity). Scheduler judgment is preserved but logged.

## Violation Example
```
❌ Recovery options displayed in FIFO order from crew availability roster.
   → No scoring; scheduler cannot evaluate trade-offs.
   → Violates PRD-1.5: decision basis is not evidence-surfaced to the user.
```

## Edge Cases & Warnings
- `far_117_eligible: False` removes the option from the list — it is not shown as a waivable option under any normal circumstance (BUS-2.1)
- Score factors must be documented in the audit trail entry, not just the final selection

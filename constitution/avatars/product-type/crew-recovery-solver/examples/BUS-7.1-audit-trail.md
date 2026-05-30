---
avatar: avatar-product-crew-recovery-solver
law: BUS-7.1
title: "Audit Trail Law"
---

# BUS-7.1 — Audit Trail Law: Crew Assignment Audit in CWR

## What This Law Requires
Every crew assignment decision — accepted, rejected, override, or system-generated — must produce an immutable audit record. The record must be written atomically with the assignment change, in the same transaction or via guaranteed delivery.

## Compliant Example

**Crew Assignment Audit Record Schema**

```python
@dataclass(frozen=True)
class CrewAssignmentAuditRecord:
    # Immutable identity
    record_id: UUID
    correlation_id: str          # IROP event correlation ID (ENG-6.7)
    timestamp_utc: datetime

    # Decision context
    crew_id: str
    from_assignment: str | None  # None if new assignment
    to_assignment: str
    decision_type: Literal["ACCEPT", "REJECT", "OVERRIDE", "SYSTEM_AUTO"]
    acting_user_id: str          # SOC Scheduler employee ID; "SYSTEM" for auto

    # Compliance state at time of decision
    far_117_eligible: bool
    far_117_rest_hours_actual: float
    far_117_rest_hours_required: float
    far_117_regulation: str      # e.g., "FAR 117.25(a)"

    # Override documentation (required if decision_type == OVERRIDE)
    override_justification: str | None
    override_authorized_by: str | None

    # Recovery score context
    recovery_score: float | None
    recovery_score_factors: dict | None
```

**Delivery guarantee:** The audit record is written to an append-only store before the API response is returned. If the audit write fails, the assignment is rolled back — never accepted without an audit record.

## Violation Example
```
❌ Audit record written in a background async job after the assignment is committed.
   → Race condition: assignment exists in roster without an audit record if the job fails.
   → Fix: audit write must be synchronous and in the same transaction boundary as the assignment.
```

## Edge Cases & Warnings
- `decision_type: SYSTEM_AUTO` is permitted only for repatriation assignments (e.g., deadhead home after last IROP event); all other auto-assignments require scheduler review
- Override audit records must include `override_authorized_by` — dual-entry authorization is required for certain FAR 117 deviation scenarios

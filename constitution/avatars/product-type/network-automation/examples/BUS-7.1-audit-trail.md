---
avatar: avatar-product-network-automation
law: BUS-7.1
title: "Audit Trail Law"
---

# BUS-7.1 — Audit Trail Law: Network Automation Application

## What This Law Requires
Every automated network change — approved, rejected, blocked, or rolled back — must produce an **immutable audit record** written atomically with the change action. Failure to write the audit record blocks the change. Records must include operator identity, change ticket ID, device target, action type, and outcome.

## Compliant Example

**Audit Record Schema**

```python
@dataclass(frozen=True)
class NetworkChangeAuditRecord:
    correlation_id: str      # change_ticket_id:device_hostname:UTC
    change_ticket_id: str    # ServiceNow change ticket ID
    actor: str               # SSO username or system principal
    device_hostname: str
    action_type: str         # PUSH | ROLLBACK | BLOCKED | REJECTED
    compliance_state: str    # APPROVED | BLOCKED_NO_APPROVAL | BLOCKED_WINDOW | BLOCKED_TARGET_MISMATCH
    outcome: str             # SUCCESS | FAILURE
    failure_reason: str | None
    pushed_at: datetime      # UTC, set by system
    verified_at: datetime | None
```

**Audit write is atomic with the change commit:**

```python
with audit_store.atomic_write() as writer:
    push_result = nautobot_client.apply_change(job_id, device_hostname)
    writer.write(NetworkChangeAuditRecord(
        correlation_id=f"{ticket.id}:{device_hostname}:{utcnow().isoformat()}",
        change_ticket_id=ticket.id,
        actor=current_principal.username,
        device_hostname=device_hostname,
        action_type="PUSH",
        compliance_state="APPROVED",
        outcome="SUCCESS" if push_result.ok else "FAILURE",
        failure_reason=push_result.error if not push_result.ok else None,
        pushed_at=utcnow(),
        verified_at=None
    ))
# If writer.write() fails → outer transaction rolls back → push NOT committed
```

**Blocked attempts also produce an audit record:**

```python
audit_store.write(NetworkChangeAuditRecord(
    action_type="BLOCKED",
    compliance_state=result.violation_type,
    outcome="FAILURE",
    failure_reason=result.reason, ...
))
```

**Constitutional check:** BUS-7.1 — every action (including blocks) is audited. The audit write is a precondition, not a side effect.

## Violation Example
```
❌ push_result = nautobot_client.apply_change(job_id, device_hostname)
   if push_result.ok:
       audit_store.write(...)  # only logs successes
   → Violates BUS-7.1: failed pushes and blocked attempts are the most
     important audit events for compliance reviewers.
```

## Edge Cases & Warnings
- Audit store unavailability must block the change, not skip the audit
- `correlation_id` must propagate into MOCCA Monitor / Eagle Eye alerts so network anomalies can be traced back to the triggering change
- Audit records are immutable — write a new `CORRECTION` record referencing the original `correlation_id`; never update or delete existing records

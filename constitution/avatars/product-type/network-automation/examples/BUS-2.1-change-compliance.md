---
avatar: avatar-product-network-automation
law: BUS-2.1
title: "Regulatory Mapping Law"
---

# BUS-2.1 — Regulatory Mapping Law: IT Change Management Compliance

## What This Law Requires
Every automated network change must satisfy IT change management controls — CAB approval, maintenance window enforcement, and rollback plan — as a **hard gate** before any device configuration is applied. Change compliance is not a warning; it is a blocking precondition.

## Compliant Example

**Change Compliance Gate — Pre-Push Checklist**

Before the network automation pipeline dispatches a Nautobot job to a device, it must evaluate all of the following. Any `FAIL` blocks the push:

| Control | Check | PASS | FAIL |
|---------|-------|------|------|
| CAB Approval | ServiceNow change ticket status = `Approved` | Proceed | 🔴 BLOCK — "Change ticket {ID} is not in Approved state. Push blocked." |
| Maintenance Window | Current UTC time is within the approved change window | Proceed | 🔴 BLOCK — "Current time is outside approved maintenance window ({start}–{end} UTC). Push blocked." |
| Device Target Match | Nautobot device hostname/IP matches the approved change ticket targets | Proceed | 🔴 BLOCK — "Device {hostname} is not in the approved target list for change {ID}. Push blocked." |
| Rollback Plan Present | Change ticket has a non-empty rollback plan field | Proceed | 🔴 BLOCK — "No rollback plan found for change {ID}. Push blocked." |

**Compliance gate implementation pattern:**

```python
# Compliance gate must run synchronously before Nautobot job dispatch
result = change_compliance_gate.evaluate(
    change_id=ticket.id,
    device_targets=[device.hostname],
    push_timestamp=utcnow()
)
if not result.approved:
    raise ChangeComplianceBlockedError(result.reason)
    # Audit record written for blocked attempt — BUS-7.1
```

**Constitutional check:** BUS-2.1 — IT change management controls mapped to code-level enforcement. No device configuration change bypasses this gate.

## Violation Example
```
❌ if ticket.status != "Approved":
       logger.warning("Change not approved — pushing anyway (emergency)")
   → Treating the compliance gate as a soft warning.
   → Violates BUS-2.1: emergency exceptions require a formal CAB emergency change process,
     not a code-level bypass. The bypass itself must be audited.
```

## Edge Cases & Warnings
- Emergency changes are not a code-path exception — they require a separate CAB emergency approval workflow with its own audit trail
- Clock skew between automation server and change window times must be handled with UTC timestamps and a configurable grace buffer (recommend ≤5 min, documented in change ticket)
- A device target mismatch is a compliance violation, not a data quality issue — treat it as blocking and route to the change manager

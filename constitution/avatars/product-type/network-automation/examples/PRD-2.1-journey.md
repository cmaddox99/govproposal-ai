---
avatar: avatar-product-network-automation
law: PRD-2.1
title: "Problem Validation Law"
---

# PRD-2.1 — Problem Validation Law: Network Automation Application

## What This Law Requires
Every core network automation journey must be validated against the current real-world operator workflow — including manual steps, system handoffs, and known failure modes — before the future-state design is specified.

## Compliant Example

**Journey Map: Network Change Request (Current State)**

Trigger: Network engineer needs to push an ACL update to a core router.

| Step | Actor | System | Pain Point |
|------|-------|--------|------------|
| 1. Verify device in Nautobot | Network Engineer | Nautobot UI | Manual lookup — no API integration with change ticket |
| 2. Create change request in ServiceNow | Network Engineer | ServiceNow | Must manually copy device hostname and IP from Nautobot |
| 3. Write rollback plan | Network Engineer | Word/Confluence | No template; varies by engineer; CAB rejects ~15% for missing rollback detail |
| 4. CAB review and approval | IT Change Manager | ServiceNow | Approver must open Nautobot separately to validate device targets |
| 5. Wait for maintenance window | Network Engineer | — | No automated notification; engineer polls manually |
| 6. Push change via device CLI | Network Engineer | SSH/CLI | Manual; no automated validation post-push |
| 7. Verify change applied | Network Engineer | CLI + Nautobot | Manual ping/trace + Nautobot re-check; no diff view |
| 8. Close change ticket | Network Engineer | ServiceNow | Manual; no automated closure on verified push |

**Identified failure modes:**
- Step 2→3: Nautobot data copied incorrectly into ServiceNow (device target mismatch) — occurs ~10% of changes
- Step 6: Push executed outside approved window (maintenance window notification missed) — 3 CAB violations in last 6 months
- Step 7: Change not verified; ticket closed anyway — 5 silent failures discovered in post-mortem

**Constitutional check:** PRD-2.1 — current-state journey documented with failure modes before future-state automation is specified. Each failure mode becomes a validation gate requirement.

## Violation Example
```
❌ "We'll build an API that accepts change parameters and pushes to devices."
   → Future-state design specified without mapping current manual steps or failure modes.
   → Violates PRD-2.1: the three most common failure modes (data mismatch, out-of-window push,
     silent verification failure) would be automated into the new system.
```

## Edge Cases & Warnings
- Map the exception path (change rejection, rollback) as carefully as the happy path — CAB rejections and rollbacks are where audit trail gaps appear
- Journey maps must distinguish between what engineers *say* they do and what observation/ticket data shows they *actually* do

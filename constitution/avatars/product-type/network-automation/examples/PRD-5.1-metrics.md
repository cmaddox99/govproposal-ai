---
avatar: avatar-product-network-automation
law: PRD-5.1
title: "MVP Law"
---

# PRD-5.1 — MVP Law: Network Automation Application

## What This Law Requires
Network automation features ship only when the change compliance gate (BUS-2.1) and audit trail (BUS-7.1) are both fully operational. No feature that touches device configuration is shippable without both gates present.

## Compliant Example

**MVP Definition: Automated Network Change Pipeline**

| Capability | MVP? | Rationale |
|------------|------|-----------|
| Change compliance gate (CAB window enforcement) | ✅ YES — required | BUS-2.1 hard gate; device push blocked without approval |
| Immutable audit record per change | ✅ YES — required | BUS-7.1; no audit = no MVP |
| Nautobot inventory validation at request time | ✅ YES — required | Eliminates #1 failure mode (device target mismatch) |
| Automated maintenance window notification | ✅ YES — required | Eliminates out-of-window push failure mode |
| Post-push diff verification | ✅ YES — required | Eliminates silent verification failures |
| Automated rollback on verification failure | 🟡 v1.1 | High value; not MVP — manual rollback is the fallback |
| CAB approval workflow integration (ServiceNow) | 🟡 v1.1 | CAB approval still manual in MVP; automation is the gate |
| Multi-device bulk change | 🟡 v2.0 | Risk surface too large for MVP; single-device only in v1 |

**Success metrics for MVP (measured at 30/60/90 days):**

| Metric | Baseline | MVP Target | Measurement |
|--------|----------|------------|-------------|
| Mean time to push approved change | 45 min (cross-system manual) | ≤10 min | ServiceNow ticket open → device push timestamp |
| Out-of-window push incidents | 3 in last 6 months | 0 | CAB violation log |
| Change audit completeness | ~60% (manually closed tickets) | 100% | Audit record count vs change ticket count |
| CAB rejection rate for missing rollback | 15% | ≤3% | ServiceNow CAB rejection reason codes |

**Constitutional check:** PRD-5.1 — MVP ships when the riskiest assumptions (compliance gate, audit completeness) are validated, not when all desired features are complete.

## Violation Example
```
❌ "We'll ship the change automation pipeline now and add audit logging in a follow-up sprint."
   → Violates PRD-5.1: audit trail is not an enhancement — it is an MVP gate.
   → Also violates BUS-7.1: device changes without audit records are a compliance violation.
```

## Edge Cases & Warnings
- Do not equate "MVP" with "low quality" — the audit trail and compliance gate must be production-grade at v1.0
- Rollback automation is intentionally post-MVP: premature automation of rollback creates risk if the rollback itself fails silently

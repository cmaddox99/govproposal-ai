---
avatar: avatar-schedule-change-self-serve
law_id: BUS-7.1
law_title: "Audit Trail Law (Business)"
file_type: example
---

# BUS-7.1 Audit Trail — Schedule Change Self-Serve

## Law Summary

Every eligibility decision, fee waiver authorization, agent override, and rebooking execution must be recorded in an **append-only audit log** with full decision context, retained **7 years** for regulatory audit and DOT inquiry response.

## Audit Schema (DDL-style)

```sql
CREATE TABLE sched_change_audit_log (
  audit_id             VARCHAR(36) PRIMARY KEY,
  decision_id          VARCHAR(36) NOT NULL,
  pnr_ref              VARCHAR(10) NOT NULL,      -- masked PNR reference
  event_type           VARCHAR(50) NOT NULL,      -- ELIGIBILITY_DECISION | FEE_WAIVER | AGENT_OVERRIDE | REBOOKING_EXECUTED
  rule_id              VARCHAR(50),               -- eligibility rule that fired
  eligibility_result   VARCHAR(20),               -- ELIGIBLE | INELIGIBLE | EXCEPTION
  fee_waiver_authorized_by VARCHAR(20),           -- supervisor_id if waiver required approval
  agent_id             VARCHAR(20),               -- for agent actions
  regulation_ref       VARCHAR(100),
  event_detail         JSONB NOT NULL,
  timestamp            TIMESTAMP NOT NULL
);
-- Append-only. No UPDATE or DELETE.
```

## BUS-7.1 Field Mapping

| Event Type | Required event_detail fields |
|------------|------------------------------|
| ELIGIBILITY_DECISION | rule_id, reason_code, fare_class, irop_flag |
| FEE_WAIVER | waiver_amount, waiver_type, supervisor_approval_ref |
| AGENT_OVERRIDE | override_reason, original_decision, approver |
| REBOOKING_EXECUTED | old_flight, new_flight, fare_diff, channel |

---

## ✅ COMPLIANT Example — IROP Eligibility Decision

```json
{
  "audit_id": "elig-20240315-00847",
  "decision_id": "dec-irop-00847",
  "pnr_ref": "ABCDE*",
  "event_type": "ELIGIBILITY_DECISION",
  "rule_id": "IROP-WAIVER-DOT-V3",
  "eligibility_result": "ELIGIBLE",
  "regulation_ref": "DOT 14 CFR 250",
  "event_detail": {
    "fare_class": "Y",
    "irop_flag": true,
    "delay_minutes": 180,
    "waiver_applied": "FEE_WAIVER_FULL",
    "rule_version": "3.2.1"
  },
  "timestamp": "2024-03-15T09:14:22Z"
}
```

---

## ❌ VIOLATION Example — Missing Rule Version in Audit

**Scenario:** An eligibility decision is logged but the rule_version field is omitted because the rule engine didn't expose it. Six months later, a DOT inquiry asks which rule version was applied on a specific date.

**Why this violates BUS-7.1:** Rule version is required to reconstruct the decision during audit. Without it, DOT inquiries cannot be answered definitively. The audit trail must capture enough information to fully reconstruct the decision.

**Correct approach:** Rule version must be captured at decision time and included in every eligibility audit record. The rule engine must expose version metadata. If it doesn't, require this as a prerequisite for the engine's production readiness.

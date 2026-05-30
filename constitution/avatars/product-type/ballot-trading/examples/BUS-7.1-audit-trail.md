---
avatar: avatar-product-ballot-trading
law: BUS-7.1
title: "Audit Trail"
---

# BUS-7.1 — Audit Trail: Ballot Trading Application

## What This Law Requires

Every eligibility decision, CBA rule evaluated, and trade award or rejection outcome must be immutably logged. The record must support CBA dispute resolution and contractual defensibility.

## Compliant Example

**Audit Record Schema (per trade decision)**

```json
{
  "audit_id": "TRD-2026-04-27-DFW-[hash]",
  "event_type": "ELIGIBILITY_DECISION",
  "timestamp_utc": "2026-04-27T22:01:34Z",
  "pilot_id": "P-****[last4]",
  "pairing_id": "PA-DFW-1234",
  "decision": "REJECTED",
  "reason_code": "DUTY_TIME_LIMIT_EXCEEDED",
  "cba_article": "Article 12.3 — Maximum Monthly Flight Hours",
  "cba_value_evaluated": "monthly_flight_hours: 85.0 (limit: 80.0)",
  "requesting_system": "bts-rtt-service",
  "scheduler_id": null,
  "record_hash": "sha256:[immutable-hash]"
}
```

**Immutability Requirements**
- Audit records are append-only; no UPDATE or DELETE operations permitted on audit table.
- Record hash computed at write time; integrity verified on read.
- Retention period: 7 years (CBA dispute statute of limitations).
- Access: read-only for CBA Compliance Analyst; no pilot self-service access to raw records.

**Dispute Retrieval Flow**
```
1. Compliance Analyst receives CBA dispute for Pilot P-****5678, trade date 2026-04-27
2. Query audit store by pilot_id masked key + date range
3. Retrieve all ELIGIBILITY_DECISION records for that window
4. Verify record_hash integrity
5. Present decision + cba_article + cba_value_evaluated to CBA review board
```

## Violation Example

```
❌ VIOLATION: Audit record dropped on system timeout
   "If the audit write fails, we return the trade decision anyway and log to stderr"

   CBA dispute raised: pilot claims trade was wrongly rejected.
   No audit record exists for that decision window.
   System cannot produce evidence of the CBA article evaluated.
   Result: Company has no contractual defense. BUS-7.1 HARD BLOCK.
```

## Edge Cases & Warnings

- **Batch awards require per-award records** — one batch run produces N individual audit records, not one aggregate record.
- **Scheduler overrides are separate audit events** — log override decision with scheduler_id and justification alongside the original eligibility decision.
- **PII masking is mandatory** — pilot_id must be stored as masked key; full PII retrieval only via CBA compliance workflow with access logging (BUS-3.1).

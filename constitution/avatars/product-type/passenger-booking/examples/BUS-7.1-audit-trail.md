---
avatar: avatar-passenger-booking
law_id: BUS-7.1
law_title: "Audit Trail Law (Business)"
file_type: example
---

# BUS-7.1 Audit Trail — Passenger Booking

## Law Summary

Every PNR state transition, payment event, denied boarding compensation, and fare rule application must be recorded in an **append-only audit log** with regulatory reference, retained **7 years**.

## Audit Schema (DDL-style)

```sql
CREATE TABLE booking_audit_log (
  audit_id        VARCHAR(36) PRIMARY KEY,      -- UUID
  pnr_id_hash     VARCHAR(64) NOT NULL,          -- SHA-256 of PNR + DOB
  event_type      VARCHAR(50) NOT NULL,          -- PNR_CREATED | PNR_MODIFIED | PNR_CANCELLED | PAYMENT_PROCESSED | DENIED_BOARDING | FARE_RULE_APPLIED
  agent_id        VARCHAR(20),                   -- NULL for self-service
  regulation_ref  VARCHAR(100),                  -- e.g. "DOT 14 CFR 250" | "PCI DSS v4.0"
  event_detail    JSONB NOT NULL,
  timestamp       TIMESTAMP NOT NULL,
  created_at      TIMESTAMP DEFAULT NOW()
);
-- Append-only. No UPDATE or DELETE.
```

## BUS-7.1 Field Mapping

| Event Type | Required event_detail fields |
|------------|------------------------------|
| PNR_CREATED | origin, destination, fare_class, payment_method_masked |
| PNR_MODIFIED | change_type, old_value, new_value, change_reason |
| PNR_CANCELLED | cancellation_reason, refund_method, refund_amount |
| PAYMENT_PROCESSED | payment_ref (token), amount, currency, gateway_response |
| DENIED_BOARDING | dot_tier, compensation_amount, written_statement_issued |
| FARE_RULE_APPLIED | rule_id, rule_version, fare_basis |

---

## ✅ COMPLIANT Example — PNR Cancellation Audit

```json
{
  "audit_id": "pnr-cancel-20240315-00192",
  "pnr_id_hash": "b7e3f1a2...",
  "event_type": "PNR_CANCELLED",
  "agent_id": null,
  "regulation_ref": "DOT 14 CFR 250.9",
  "event_detail": {
    "cancellation_reason": "PASSENGER_INITIATED",
    "refund_method": "ORIGINAL_PAYMENT",
    "refund_amount": 847.00,
    "currency": "USD",
    "refund_sla_deadline": "2024-03-22",
    "refund_initiated": true
  },
  "timestamp": "2024-03-15T11:22:00Z"
}
```

---

## ❌ VIOLATION Example — Missing Regulation Reference

**Scenario:** A denied boarding event is logged in the audit trail, but the regulation_ref field is left null because the gate agent didn't select a reason code.

**Why this violates BUS-7.1:** Denied boarding events require a regulatory basis in the audit record. A null regulation_ref makes the record useless for DOT audit response and dispute resolution. The system must enforce a non-null regulation_ref for denied boarding events.

**Correct approach:** The UI must require the agent to select a DOT regulation tier (e.g., "DOT 14 CFR 250 — oversale") before confirming deny-boarding. The audit record must be complete at the time of the event, not retroactively filled.

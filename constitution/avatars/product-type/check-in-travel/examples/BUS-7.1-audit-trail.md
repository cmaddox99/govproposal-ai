---
avatar: avatar-check-in-travel
law_id: BUS-7.1
law_title: "Audit Trail Law (Business)"
file_type: example
---

# BUS-7.1 Audit Trail — Check-In & Travel

## Law Summary

Every significant check-in action affecting passenger data or regulatory compliance must be recorded in an **append-only audit log**, immutable and retained **7 years**. This includes boarding pass issuance, CBP/APIS transmissions, deny-boarding events, and ADA accommodations.

## Audit Schema (DDL-style)

```sql
CREATE TABLE checkin_audit_log (
  audit_id          VARCHAR(36) PRIMARY KEY,      -- UUID, append-only
  event_type        VARCHAR(50) NOT NULL,          -- BOARDING_PASS_ISSUED | APIS_TRANSMITTED | DENY_BOARDING | ADA_ACCOMMODATION
  passenger_id_hash VARCHAR(64) NOT NULL,          -- SHA-256 of PNR + DOB, never raw PNR
  flight_number     VARCHAR(10) NOT NULL,
  origin            CHAR(3) NOT NULL,
  destination       CHAR(3) NOT NULL,
  agent_id          VARCHAR(20),                   -- NULL for automated events
  timestamp         TIMESTAMP NOT NULL,
  regulation_ref    VARCHAR(100),                  -- e.g. "CBP 19 CFR 122.49a" | "ADA Title II"
  event_detail      JSONB NOT NULL,                -- event-specific fields
  created_at        TIMESTAMP DEFAULT NOW()
);
-- No UPDATE or DELETE permitted. Erasure handled via anonymization only.
```

## BUS-7.1 Field Mapping

| Event Type | Required event_detail fields |
|------------|------------------------------|
| BOARDING_PASS_ISSUED | gate, seat, boarding_group, issue_method (kiosk/mobile/counter) |
| APIS_TRANSMITTED | government_agency, data_fields_count, ack_reference, transmission_ms |
| DENY_BOARDING | reason_code, regulation_ref, compensation_offered, written_statement_issued |
| ADA_ACCOMMODATION | request_type, fulfillment_status, denial_reason (if denied) |

---

## ✅ COMPLIANT Example — APIS Transmission Log

```json
{
  "audit_id": "cbp-tx-20240315-00042",
  "event_type": "APIS_TRANSMITTED",
  "passenger_id_hash": "a3f9e1b2c4d5...",
  "flight_number": "AA 100",
  "origin": "JFK",
  "destination": "LHR",
  "agent_id": null,
  "timestamp": "2024-03-15T08:14:33Z",
  "regulation_ref": "CBP 19 CFR 122.49a",
  "event_detail": {
    "government_agency": "CBP",
    "data_fields_count": 12,
    "ack_reference": "CBP-ACK-2024-00847291",
    "transmission_ms": 234,
    "transmission_status": "ACCEPTED"
  }
}
```

---

## ❌ VIOLATION Example — Missing Audit Entry

**Scenario:** A deny-boarding event occurs at the gate for a passenger missing a required visa. The gate agent resolves the situation but no audit log entry is created because the gate system encountered an error.

**Why this violates BUS-7.1:** Deny-boarding decisions are regulatory events that require an immutable audit record. Silent failure of the audit write is not acceptable. The system must retry or escalate — never silently drop audit events.

**Correct approach:** Audit writes must be transactional with the event. If the audit log write fails, the system must alert operations and queue the entry for guaranteed delivery. Deny-boarding events must never proceed without an audit record commitment.

---
avatar: avatar-product-travel-docs-compliance
law_id: BUS-7.1
law_title: "Audit Trail Law (Business)"
file_type: example
---

# BUS-7.1 Audit Trail — Travel Docs Compliance

## Law Summary

APIS/CBP transmissions are **government-required records** that must be logged with full fidelity. Every document verification event, passport check result, and denied boarding decision must be immutably recorded and retained per DHS/CBP requirements.

## Audit Schema (DDL-style)

```sql
CREATE TABLE travel_docs_audit_log (
  audit_id           VARCHAR(36) PRIMARY KEY,
  transmission_id    VARCHAR(36),                 -- for APIS events
  pnr_ref            VARCHAR(10) NOT NULL,        -- masked
  government_agency  VARCHAR(20),                 -- CBP | DHS | TSA
  event_type         VARCHAR(50) NOT NULL,         -- APIS_TRANSMITTED | DOC_VERIFICATION | DENIED_BOARDING | PASSPORT_CHECK
  data_fields_transmitted VARCHAR(500),           -- comma-separated field list for APIS
  timestamp          TIMESTAMP NOT NULL,
  ack_reference      VARCHAR(100),                -- government acknowledgment reference
  agent_id           VARCHAR(20),
  event_detail       JSONB NOT NULL,
  created_at         TIMESTAMP DEFAULT NOW()
);
-- Append-only. No UPDATE or DELETE. Retention per DHS/CBP requirements.
```

## BUS-7.1 Field Mapping

| Event Type | Required event_detail fields |
|------------|------------------------------|
| APIS_TRANSMITTED | data_fields_transmitted, transmission_status, ack_reference, latency_ms |
| DOC_VERIFICATION | document_type, verification_result, timatic_ref, agent_id |
| DENIED_BOARDING | doc_failure_reason, regulation_ref, escalation_path, compensation_offered |
| PASSPORT_CHECK | check_method, check_result, discrepancy_noted |

---

## ✅ COMPLIANT Example — APIS Transmission to CBP

```json
{
  "audit_id": "apis-20240315-00042",
  "transmission_id": "TX-CBP-2024-00847291",
  "pnr_ref": "ABCDE*",
  "government_agency": "CBP",
  "event_type": "APIS_TRANSMITTED",
  "data_fields_transmitted": "surname,given_name,dob,nationality,passport_num,gender,country_of_residence,flight_num,origin,destination",
  "timestamp": "2024-03-15T06:14:33Z",
  "ack_reference": "CBP-ACK-2024-00847291",
  "agent_id": null,
  "event_detail": {
    "transmission_status": "ACCEPTED",
    "latency_ms": 188,
    "passenger_count": 1,
    "flight": "AA 100",
    "departure_port": "JFK"
  }
}
```

---

## ❌ VIOLATION Example — Missing Acknowledgment Reference

**Scenario:** APIS transmissions are logged but the ack_reference field is null because the system didn't wait for CBP's acknowledgment before writing the audit record.

**Why this violates BUS-7.1:** For government-required transmissions, the acknowledgment reference is proof that CBP received the data. Logging without an ack_reference means the audit record shows transmission was attempted but not confirmed received. DHS/CBP requirements expect confirmed transmission records.

**Correct approach:** The audit write for APIS events must be deferred until the CBP acknowledgment is received. If acknowledgment times out, log the transmission with status TIMEOUT and trigger an alert for manual follow-up.

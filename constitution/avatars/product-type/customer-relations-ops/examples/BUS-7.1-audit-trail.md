---
avatar: avatar-customer-relations-ops
law_id: BUS-7.1
law_title: "Audit Trail Law (Business)"
file_type: example
---

# BUS-7.1 Audit Trail — Customer Relations Ops

## Law Summary

Every LLM inference, draft generation, compensation decision, prohibited-word check, and agent acceptance/rejection must be recorded in an **append-only audit trace**, retained **7 years** for DOT regulatory audit response.

## Audit Schema (DDL-style)

```sql
CREATE TABLE cr_audit_log (
  trace_id           VARCHAR(36) PRIMARY KEY,
  complaint_id       VARCHAR(36) NOT NULL,        -- hashed in storage
  event_type         VARCHAR(50) NOT NULL,         -- LLM_CALL | DRAFT_GENERATED | COMPLIANCE_CHECK | AGENT_DECISION | COMPENSATION_VALIDATED
  llm_model_version  VARCHAR(50),                  -- e.g. "gpt-4o-2024-08-06"
  prompt_hash        VARCHAR(64),                  -- SHA-256 of redacted prompt
  compensation_amount DECIMAL(10,2),
  agent_id           VARCHAR(20),
  agent_decision     VARCHAR(20),                  -- ACCEPTED | REJECTED | EDITED
  compliance_result  VARCHAR(20),                  -- PASS | FAIL
  event_detail       JSONB NOT NULL,
  timestamp          TIMESTAMP NOT NULL
);
-- Append-only. No UPDATE or DELETE.
```

## BUS-7.1 Field Mapping

| Event Type | Required event_detail fields |
|------------|------------------------------|
| LLM_CALL | model_version, prompt_hash, token_count, latency_ms |
| COMPLIANCE_CHECK | prohibited_words_found, result, rule_version |
| AGENT_DECISION | edit_extent, time_to_decision, acceptance_channel |
| COMPENSATION_VALIDATED | dot_regulation, supervisor_approval_ref, amount |

---

## ✅ COMPLIANT Example — Full LLM Trace for a Complaint

```json
{
  "trace_id": "cr-trace-20240315-00421",
  "complaint_id": "hash-of-complaint-id",
  "event_type": "LLM_CALL",
  "llm_model_version": "gpt-4o-2024-08-06",
  "prompt_hash": "a3f9e1b2...",
  "compensation_amount": 200.00,
  "agent_id": null,
  "compliance_result": "PASS",
  "event_detail": {
    "token_count": 847,
    "latency_ms": 1240,
    "prohibited_words_found": [],
    "complaint_category": "FLIGHT_DELAY",
    "dot_regulation": "DOT 14 CFR 250"
  },
  "timestamp": "2024-03-15T10:14:22Z"
}
```

---

## ❌ VIOLATION Example — Missing Prohibited-Words Log on Pass

**Scenario:** The compliance check runs and finds no prohibited words, so the team decides not to log "pass" results to reduce audit table size.

**Why this violates BUS-7.1:** Every compliance check must be logged, including passes. Without pass records, it is impossible to prove during a DOT audit that the compliance pipeline ran for every draft. Absence of violation records does not demonstrate compliance — positive evidence of checks is required.

**Correct approach:** Log every compliance check result — pass or fail — with rule version and timestamp. The audit log must demonstrate the pipeline ran, not just that violations occurred.

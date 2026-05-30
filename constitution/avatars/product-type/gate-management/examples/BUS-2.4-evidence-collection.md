---
avatar: avatar-product-gate-management
law: BUS-2.4
title: "Evidence Collection Law"
---

# BUS-2.4 — Evidence Collection Law: Gate Management Application

**What this law requires:** Compliance evidence must be collected at the point of decision, retained per regulation, and structured for audit retrieval.

---

## Log Schemas — Per Domain

### Biometric Boarding Event
```json
{
  "event_type": "BIOMETRIC_BOARDING",
  "event_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "flight_id": "AA-1234",
  "gate_id": "DFW-A15",
  "agent_id": "aa-employee-id",
  "pnr_token": "TOKENIZED-PNR",
  "match_result": "MATCH | NO_MATCH | OPT_OUT",
  "match_score": 0.97,
  "no_match_reason_code": "FACE_NOT_FOUND | LOW_SCORE | LIVENESS_FAIL | null",
  "biometric_template_ref": "vault-ref-not-template",
  "cbp_session_id": "cbp-session-uuid"
}
```
**Retention:** 7 years (CBP/TSA). Template ref only — raw biometric never in audit log.

### DSS Gate Event State Transition
```json
{
  "event_type": "GATE_STATE_TRANSITION",
  "event_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "flight_id": "AA-1234",
  "from_gate": "DFW-A12",
  "to_gate": "DFW-B8",
  "source_system": "AOC | DCS | MANUAL",
  "display_types_updated": ["GIDS", "FIDS"],
  "propagation_latency_ms": 2340,
  "agent_id": "null | aa-employee-id"
}
```
**Retention:** 2 years (FAA operational audit).

### Carry-On Compliance Decision
```json
{
  "event_type": "CARRYON_COMPLIANCE_DECISION",
  "event_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "flight_id": "AA-1234",
  "gate_id": "DFW-A15",
  "agent_id": "aa-employee-id",
  "bag_dimensions": { "length_cm": 56, "width_cm": 36, "depth_cm": 23 },
  "rule_version": "v2.4.1",
  "decision": "COMPLIANT | GATE_CHECK | DENIED",
  "override_applied": false,
  "override_supervisor_id": "null | aa-supervisor-id",
  "override_auth_token_ref": "null | token-ref-uuid"
}
```
**Retention:** 1 year (DOT consumer protection).

---

## Audit Retrieval Requirements

Every schema above must support these queries within 30 seconds:
- All boarding events for flight `{flight_id}` on `{date}`
- All carry-on decisions by agent `{agent_id}` in last 30 days
- All gate changes at station `{airport_code}` in last 24 hours

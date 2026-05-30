# Worksheet 04: Domain Model Inventory - Schedule Change Self-Serve

**Purpose:** Enumerate entities, rules, events, and exception flows governing schedule change decisions.  
**Law Anchor:** PRD-2.2, skill-04-business-domain-modeling, skill-05-business-rules  
**Status:** In Progress (code-derived inventory first pass complete)

---

## Core Domain Entities (Initial)

| Entity | Description | Source of Truth | Validation Status |
|-------|-------------|-----------------|-------------------|
| Passenger Name Record (PNR) | Reservation context used for eligibility and mutation | Reservation + Eligibility + BFF + Remarks services | Code-evidenced |
| Itinerary / Slice / Segment | Domain structure for impacted journey logic | Eligibility + DRSS reservation/remarks models | Code-evidenced |
| Eligibility Decision | Structured allow/deny + reason detail | Eligibility service (`EligibilityResponseDetails`, `EligibilityReason`) | Code-evidenced |
| Impact Type | Connection/alternate O&D impact classification | DRSS remarks impact processing | Code-evidenced |
| Rule Data Payload | Prime/time/non-impacted/active-IROP rule model | DRSS remarks `EligibilityData` and creator pipeline | Code-evidenced |
| Audit/History Context | Reservation change retrieval and update markers | Reservation history service + BFF history integration | Partially code-evidenced |

---

## Rule Categories to Inventory

1. IROP status gate rules (`SCHEDULE_CHANGE`/`X_PROTECT`/other statuses, Y-flag, XPT type checks)
2. Segment confirmation rules (`SLICE_HAS_NO_CONFIRMED_SEGMENTS`, `SLICE_HAS_UNCONFIRMED_SEGMENTS`)
3. Active-slice and impacted-segment matching rules (active slice must contain impacted segment)
4. Non-AA prime and O&D impact rules (prime-carrier and origin/destination unchanged filtering)
5. Time-delta disruption rules (less-than-60-minute impact rule data creation)
6. Remarks process stop-rules (HL segment, AA20 marker, active IROP segment short-circuit)

---

## Event and State Transition Questions

1. Eligibility evaluation transitions from reservation + IROP validation into either ineligible reason output or eligible response with details and redirect metadata.
2. Partial-update risk exists when eligibility is true but `remarksService.addRemark(...)` fails; response remains eligible with error `Reservation update failed`.
3. No explicit rollback transaction is observed in current first pass; mutation failure is surfaced as response error and requires downstream/manual handling.
4. Compliance reconstruction fields with strongest evidence today include record locator, impacted slice O&D, eligibility flags/reason data, and transaction/request metadata logs.

---

## Exception Flow Inventory

| Exception | Current Behavior | Risk | Candidate Improvement |
|----------|------------------|------|-----------------------|
| Missing/invalid itinerary or impacted slice | Eligibility component returns detailed ineligibility reason and logs structured ineligible reason | Eligibility opacity if not surfaced clearly to UI | Normalize reason dictionary and propagate user-facing reason classes |
| Unconfirmed/invalid segment state | Eligibility component emits explicit reason enums for unconfirmed/no-confirmed segments | False negatives and customer confusion | Add reason-code analytics and UI explanation templates |
| Remarks mutation failure after eligibility pass | DRSS remarks returns eligible with error `Reservation update failed` | Potential partial-processing ambiguity | Introduce explicit idempotency key + mutation status event trail |
| Rule-based disqualification (HL/AA20/active-IROP/non-AA-prime/time-threshold) | DRSS remarks short-circuits with eligibility data payload describing violated rule family | Rule explainability gap across services | Publish consolidated rule-to-message mapping contract |

---

## Compliance-Required Field Mapping

**Purpose:** Define which regulatory and operational compliance fields must be captured, audited, and preserved for each domain event. Grounds audit completeness pilot (Pilot B) and legal/regulatory defense.

**Law Anchors:** BUS-3.1 (non-discrimination), BUS-3.2 (audit trail), BUS-4.1 (consent tracking), BUS-4.3 (PII privacy), ENG-6.7 (observability)

### Data Event: Eligibility Evaluation

| Compliance Domain | Required Field | Purpose | Storage Location | Access Control |
|---|---|---|---|---|
| **Audit Trail** | Request ID / Trace ID | Link decision to telemetry and logs | Eligibility response metadata | Engineering logs only |
| **Audit Trail** | Evaluation timestamp | Regulatory timeline reconstruction | Eligibility response metadata | Engineering logs + Legal archive |
| **Audit Trail** | Rule version at evaluation | Prove consistent rule application across cohort | DRSS remarks payload + Eligibility service version tag | Engineering + Compliance |
| **Decision Authority** | Service endpoint and version | Track which service made decision | Request context (Eligibility service version) | Engineering logs |
| **Fairness** | Input PNR, impacted segment, IROP status | Audit non-discriminatory rule application | Eligibility service logs (sanitized for PII) | Compliance + Audit |
| **Fairness** | Reason code / enum value | Demonstrate decision explainability for regulatory review | Eligibility response `EligibilityReason` enum | Compliance + Customer support |
| **Data Privacy (PII)** | PNR (hashed/tokenized in logs) | Preserve audit trail without exposing passenger identity | Eligibility service logs (token) + Historic decision store | Compliance + Legal |
| **Data Privacy (PII)** | Passenger name (encrypted in audit) | Optional: for exception investigation only | Separate encrypted audit store | Legal + Security clearance |

### Data Event: Schedule Change Mutation (Remarks Addition)

| Compliance Domain | Required Field | Purpose | Storage Location | Access Control |
|---|---|---|---|---|
| **Audit Trail** | Mutation request ID | Link mutation to eligibility decision | DRSS remarks response metadata | Engineering logs |
| **Audit Trail** | Timestamp (before/after) | Regulatory timeline and latency tracking | BFF history service + remarks service timestamp | Engineering + Compliance |
| **Audit Trail** | Agent/system identity | Track who/what approved or triggered mutation | BFF request context (user ID or automation flag) | Compliance + Audit |
| **Mutation Authority** | Eligibility decision reference | Prove mutation was authorized by eligibility pass | DRSS remarks payload carries eligibility ref | Engineering + Compliance |
| **Mutation Authority** | Consent status (explicit/implicit) | Track consent given by passenger for booking change | BFF consent metadata or passenger action flag | Compliance + Customer |
| **Financial** | Refund/credit amount (if applicable) | Track financial impact for accounting and refund audits | DRSS remarks financial impact field | Finance + Compliance |
| **Financial** | Currency code | Multi-currency audit trail | DRSS remarks payload | Finance |
| **Operational Status** | Mutation success/failure code | Track partial failures for customer support | DRSS remarks response status (`Reservation update failed` etc.) | Support + Engineering |
| **Data Privacy (PII)** | Original booking reference (PII) | Preserve record locator for audit | BFF history encrypted store | Compliance + Legal |
| **Data Privacy (PII)** | Impacted slice O&D (semi-sensitive) | Customer journey reconstruction for audit | BFF history + remarks payload | Compliance + Audit |

### Data Event: Exception or Rule Disqualification

| Compliance Domain | Required Field | Purpose | Storage Location | Access Control |
|---|---|---|---|---|
| **Audit Trail** | Rule family identifier | Track which rule blocked eligibility | DRSS remarks payload `eligibilityData.ruleFamily` | Engineering + Compliance |
| **Audit Trail** | Rule violation reason | Document why rule disqualified passenger | DRSS remarks reason enums and error messages | Compliance + Audit |
| **Fairness** | Context at rule evaluation time | Audit fairness of rule application (e.g., was rule applied to all passengers in cohort?) | Eligibility service decision logs | Compliance |
| **Operational Remedy** | Exception type classification | Track for remediation and exception pattern analysis | Structured exception codes (enum: `UNCONFIRMED_SEGMENT`, `HL_SEGMENT`, etc.) | Engineering + Product Analytics |
| **Observability** | Exception frequency counter | Monitor for systemic issues | Metrics emissions (Prometheus/OpenTelemetry) | Engineering + Observability |

### Compliance Field Enforcement Strategy

**Baseline (v1 - MVP):**
- Audit trail fields (request/trace ID, timestamps, rule version) mandatory
- Decision authority and fairness fields (reason code, rule family) mandatory
- Financial fields optional (defer to transactional systems of record)

**Future (v2 - Hardened):**
- Explicit consent tracking integration (requires customer consent UI change)
- Encrypted PII storage in dedicated audit vault (security uplift)
- Financial reconciliation hooks with accounting systems

---

## Exception-Path Severity Classification and Remediation

**Purpose:** Categorize observed exception patterns by severity (critical/major/minor), identify root causes, and define targeted remediations. Aligns with vertical-slice prioritization and pilot scope.

**Law Anchors:** ENG-6.7 (observability), ENG-10.1 (quality gates), BUS-3.1 (fairness), AV-EXP (experiment governance)

### Exception Classification Matrix

| Exception | Severity | Current Behavior | Root Cause | Candidate Remediations |
|-----------|----------|------------------|------------|------------------------|
| **Missing/Invalid Itinerary or Impacted Slice** | **CRITICAL** | Eligibility returns ineligibility reason; customer sees generic "ineligible" message | Reason codes not normalized to user-facing explanations | (1) Normalize reason dictionary (12 → 4 explanations); (2) Add UI explanation template per reason class; (3) Pilot A: Eligibility Explanation Assistant |
| **Unconfirmed/Invalid Segment State** | **MAJOR** | Eligibility emits explicit reason (`SLICE_HAS_UNCONFIRMED_SEGMENTS`); customer unaware this is temporary | Insufficient customer education on segment confirmation timing | (1) Add segment status badge to reservation detail; (2) Explain why unconfirmed segments block rebooking; (3) Suggest confirmation action (re-validate itinerary) |
| **Remarks Mutation Failure After Eligibility Pass** | **CRITICAL** | DRSS remarks returns eligible-with-error (`Reservation update failed`); ambiguous whether rebooking succeeded | No idempotency key; no separate mutation-status event; partial-processing risk | (1) Introduce idempotency key (request ID); (2) Add explicit mutation-status response field; (3) Implement mutation event trail in history service; (4) Slice 2 priority |
| **Rule-Based Disqualification (HL/AA20/Active-IROP)** | **MAJOR** | DRSS remarks short-circuits with eligibility data payload; rules not human-readable | Consolidated rule-to-message contract missing | (1) Publish rule-to-reason mapping contract; (2) Add rule-explanation context to Pilot A; (3) Implement rule analytics dashboard (Slice 2) |
| **Non-AA Prime or O&D Mismatch** | **MINOR** | Eligibility returns ineligibility reason; customer may not understand carrier/O&D constraints | Filtering rules applied first, no explanation | (1) Add reason-code explanation to Pilot A; (2) Suggest alternative carriers (future: Pilot C) |
| **Time-Delta Disruption (< 60 minutes)** | **MINOR** | Eligibility rule data created but not surfaced to customer | Time-sensitive messaging not structured | (1) Add disruption urgency level to response; (2) Recommend faster re-booking path |
| **High Exception Rate in Cohort** | **MAJOR** (systemic) | Elevated `UNCONFIRMED_SEGMENTS` rate = potential booking confirmation issue upstream | Booking engine confirmation delay or async processing issue | (1) Add cohort-level exception monitoring; (2) Alert on threshold breach; (3) Coordinate with booking team for root-cause analysis |

### Severity Mapping to Pilot and Slice Priority

**CRITICAL Exceptions:**
- Impact: Blocks customer action or produces ambiguous outcomes
- Pilot/Slice: Eligibility Explanation Assistant (Pilot A) + Slice 1 (reason-code quality) + Slice 2 (mutation robustness)
- Acceptance Criteria:
  - Reason codes reduced from 12 unique messages to max 4 user-facing explanations
  - Explanation accuracy >= 90% (validated in Pilot A)
  - Mutation failures tracked with explicit status (not just "eligible with error")

**MAJOR Exceptions:**
- Impact: Reduces confidence or slows customer decision-making
- Pilot/Slice: Slice 1 (reason-code clarity) + Slice 2 (rule transparency + audit completeness)
- Acceptance Criteria:
  - Rule explanation template for top 5 disqualification rules published
  - Exception rate < 5% of eligible population per cohort
  - Observability dashboard operational (Slice 2)

**MINOR Exceptions:**
- Impact: Low customer frustration; good future enhancement opportunity
- Pilot/Slice: Defer to Slice 3+ (conversational assistant can contextualize)
- Acceptance Criteria:
  - Tech debt logged; no blocking priority

### Remediation Sequencing (Autonomous Phase)

**Ready Now (Section 7 - No Human Gate):**
1. Define normalized reason dictionary (CRITICAL #1)
2. Draft rule-to-message contract (MAJOR #4)
3. Design idempotency key strategy for remarks mutation (CRITICAL #3)
4. Create exception monitoring dashboard mock-up (MAJOR #7)

**Ready After Workshops (Human-Gated Phase):**
1. Pilot A: Implement and validate explanation quality
2. Collect segment confirmation timing data from ops team
3. Finalize UI explanation templates with Product/UX
4. Prioritize mutation remediation scope with engineering

---

## Exit Criteria

- [x] Domain glossary finalized with engineering + product sign-off
- [x] Rule catalog first pass mapped to observable code reason families
- [x] Top exception paths first pass mapped to slice opportunities
- [x] Compliance-required fields identified for each domain event
- [x] Exception-path severity classification and remediations defined

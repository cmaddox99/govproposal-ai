# Journey: Complaint Intake & AI-Assisted Draft
# Avatar: avatar-customer-relations-ops | Law: PRD-2.1 Journey Mapping
# Grounded in: ct-service-recovery-bff, servicerecovery-ios (hangar-w4-dp-mobile)

journey:
  id: journey-complaint-intake-draft
  name: Complaint Intake & AI-Assisted Response Draft
  persona: Customer Relations agent handling a post-disruption passenger complaint
  laws: [PRD-2.1, PRD-1.1, BUS-2.1, BUS-2.4, ENG-6.4, ENG-6.7]
  source_evidence: ct-service-recovery-bff, servicerecovery-ios (hangar-w4-dp-mobile)

---

## Journey Map

| Step | Agent action | System | Key law |
|------|-------------|--------|---------|
| 1. Complaint received | Complaint arrives via app, email, or phone | `ServiceRecoveryController` (ct-service-recovery-bff) | BUS-2.1 (DOT regulatory mapping) |
| 2. Eligibility check | Verify passenger eligibility for recovery options | `IROPSController` → `IROPSHubConnector` | BUS-2.4 (Evidence Collection) |
| 3. Reservation lookup | Retrieve PNR, disruption history | `RetriveReservationConnector` | ENG-6.4 (PII data protection) |
| 4. PII redaction | Strip PII before LLM call | `pii_redact.py` | ENG-6.4 (0% PII in LLM payload) |
| 5. AI draft generated | Silent 3-stage pipeline: Analysis → Compliance → Drafting | `ServiceRecoveryServiceImpl` | PRD-2.1 (silent AI pipeline) |
| 6. Agent review | CR Rep edits draft, confirms compensation decision | CR Rep interface (FastAPI response surface) | PRD-1.1, BUS-2.4 |
| 7. Compensation validated | Miles, voucher, or refund decision validated against tier table | `ServiceRecoveryConnector` | BUS-2.1 (DOT 14 CFR Part 250/260) |
| 8. Response sent | Final response dispatched to passenger | CRM Platform outbound | BUS-2.4 (evidence recorded) |
| 9. Audit trace written | All LLM calls and decisions logged immutably | PostgreSQL append-only audit trace | ENG-6.7 (Audit Trail) |

## PII Safety in LLM Workflows (ENG-6.4)

Passenger PII (name, PNR, payment details, medical conditions for ADA complaints) must be
stripped before being passed to the LLM prompt via `pii_redact.py`. The AI pipeline receives
anonymised context only. Re-identification from the draft output occurs only in the final
PII restoration step — never within the LLM boundary.

## Audit Trail (ENG-6.7)

Every compensation decision — amount, type, approver — must be immutably logged with a
correlation ID linking the complaint, the draft, the agent edit, and the final send.
`ServiceRecoveryServiceImpl` writes append-only trace entries to PostgreSQL. Required
for DOT audit response and regulatory inquiry.

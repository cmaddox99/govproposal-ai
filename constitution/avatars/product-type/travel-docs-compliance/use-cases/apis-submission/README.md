# Use Case: APIS Submission for International Departure

## Objective

Ensure Advance Passenger Information (APIS) is accurately compiled and transmitted to the appropriate government authority for every international departure, meeting legal pre-departure requirements and audit obligations.

## Background

APIS (Advance Passenger Information System) is a legal requirement for international air travel. Airlines must transmit passenger biographic and travel document data to destination country border authorities before departure. Non-compliance results in regulatory penalties and potential flight hold.

TravelDocs is responsible for: (1) collecting and validating the required APIS fields from passenger records and verified documents, (2) formatting and transmitting records via Sabre Web Services, and (3) maintaining an immutable audit trail of each submission.

## Trigger

- Check-in completes for an international segment and all documents are verified READY.
- Or: Batch APIS pre-submission run triggered 3 hours before departure.

## Core Flow

1. **Assemble passenger record.** Retrieve verified passport data, nationality, visa status, and PNR details from reservation system and VeriFly document store.

2. **Validate APIS fields.** Confirm all required fields present per destination country schema: surname, given name(s), gender, date of birth, nationality, passport number, passport issuing country, passport expiry, travel document type, flight number, departure date.

3. **Format APIS record.** Transform to required schema (UN/EDIFACT PAXLST or API-PNR format depending on destination authority).

4. **Transmit via Sabre Web Services.** Submit to Sabre APIS transmission service; Sabre routes to CBP (US), EU border systems, or other applicable authority.

5. **Receive acknowledgment.** Record transmission timestamp, message ID, and acknowledgment status in audit log.

6. **Handle rejections.** If submission rejected: parse reason code, identify specific field error, notify check-in agent, initiate remediation. Re-transmit after correction.

7. **Confirm pre-departure completeness.** 30 minutes before gate close, verify 100% of boarding passengers have successful APIS acknowledgment. Alert operations manager for any outstanding failures.

## Exception Flow

- **Rejection — name mismatch:** Document name differs from ticket name → agent reviews; if error in document scan, rescan and re-submit; if ticket name error, involuntary reissue or boarding denial per policy.
- **Rejection — expired document:** System should have caught this in readiness check; escalate to supervisor; boarding denied with DOT documentation.
- **Transmission timeout:** Retry up to 3 times with exponential backoff; if persistent, escalate to operations with manual APIS fallback procedure.
- **Partial manifest (batch):** Flag missing passengers; trigger individual check-in APIS for unsubmitted records.

## Success Metrics

1. **APIS completeness rate:** 100% of departing international passengers have successful APIS acknowledgment before gate close.
2. **Rejection rate:** < 0.5% of APIS submissions result in rejection requiring remediation.
3. **Remediation cycle time:** Rejection identified and re-submitted within 15 minutes of detection.
4. **Audit coverage:** 100% of submissions (success and failure) logged with transmission timestamp, message ID, and disposition.

## Compliance References

- US CBP 19 CFR Part 122 (APIS requirements for US-bound international flights)
- EU Council Directive 2004/82/EC (advance passenger data for EU flights)
- DOT 14 CFR Part 250 and Part 382 (denied boarding documentation obligations)
- BUS-7.1 (audit trail immutability)
- ENG-6.7 (audit trail law — all regulatory interactions logged)

# Travel Documents Readiness — Core Journeys

**Avatar:** `avatar-travel-docs-compliance`
**Grounded in:** traveldocuments-ios (AirportSecurityFlowManager, ScanPassportViewController, MrzScanner, TouchlessEligibilityViewModel)
**Domain:** International Travel Documentation and Compliance

---

## Journey 1: Pre-Departure Requirements Lookup

**Trigger:** Passenger books an international itinerary or queries travel requirements.

**Steps:**
1. Passenger provides itinerary details (origin, destination, transit countries, nationality, passport country)
2. TravelDocs queries Timatic4 and Sherpa for destination visa, passport, and health requirements per segment
3. Requirements resolved and normalized into a structured readiness checklist
4. Checklist presented to passenger: required documents, expiry minimums, visa types, health certificates
5. Checklist persisted with itinerary; refreshed if requirements change before departure

**Success criteria:**
- Requirements returned within latency target (p95)
- Passenger checklist accurate against current Timatic4/Sherpa data
- Requirements refresh triggered by any upstream policy change

**Exception flows:**
- Timatic4 timeout → fallback to cached requirements with staleness warning
- Conflicting provider outputs → prefer conservative (stricter) rule; log review event

---

## Journey 2: 72-Hour Readiness Check

**Trigger:** Automated trigger 72 hours before departure; or passenger self-initiates check.

**Steps:**
1. Passenger identity and itinerary retrieved from Retrieve Reservation Service
2. Documents on file (passport number, expiry, visa records) retrieved from passenger profile
3. Each document validated against segment requirements (Timatic4 rules engine)
4. Readiness decision produced: READY / NOT READY / CONDITIONAL per segment
5. Decision and reason codes returned to calling channel (check-in, app, agent console)
6. Audit record persisted (decision, rule version, timestamp, agent if applicable)

**Success criteria:**
- False-block rate below threshold while maintaining compliance coverage
- Manual intervention rate reduced by ≥ target vs. baseline
- Audit record present for 100% of readiness decisions

**Exception flows:**
- Missing passenger context → fail with explicit remediation instructions
- Partial document data → NOT READY with specific missing-document reason codes

---

## Journey 3: Document Verification (Passport & Health)

**Trigger:** Check-in agent initiates document scan, or passenger submits document via VeriFly.

**Passport verification sub-flow:**
1. Agent scans MRZ or passenger submits via VeriFly
2. `PassportFlowManager` (`Sources/Passport/PassportFlowManager/PassportFlowManager.swift`) orchestrates scan options: camera MRZ via `ScanPassportViewController` or NFC via `MRZEntryViewController` / `PassportNFCScannerMediator`
3. MRZ data parsed by `MrzScanner.swift` / `MrzData.swift` and matched to PNR passenger record
4. `IFCIValidatePassengerViewController` validates passport expiry against destination minimum validity (typically 6 months)
5. Name match verified against ticket name; `VerifyTravelDocumentsViewController` presents outcome
6. APIS (Advance Passenger Information) record created or updated via `UpdateTravelDocumentsEndpoint.swift` → BFF → Sabre Web Services

**Health document sub-flow:**
1. Passenger uploads health certificate or test result via VeriFly
2. Document type and issuer validated against destination health requirements (Sherpa)
3. Test date / certificate issue date validated against entry window
4. Health verification result recorded; readiness decision updated

**Success criteria:**
- Document scan-to-decision within target latency
- APIS record accuracy: 100% name match compliance

---

## Journey 4: APIS Submission (Advance Passenger Information)

**Trigger:** Passenger check-in completes and all required documents verified.

**Steps:**
1. Verified passenger record assembled: name, nationality, passport number/expiry, destination, flight details (from `VerifyTravelDocumentsViewController` / `PassengerViewModel`)
2. APIS record formatted per destination country's regulatory schema (US CBP, EU, etc.) via `TravelDocsStatusRequestBuilder` in the BFF
3. APIS record transmitted to Sabre Web Services via `UpdateTravelDocumentsEndpoint.swift` (iOS) → BFF traveldocs orchestrator → Sabre
4. Transmission acknowledgment received and recorded in audit trail
5. Any APIS rejection returned with reason code; agent notified for remediation

**Regulatory context:** APIS submission is a pre-departure legal requirement for international travel. Non-submission or submission errors may result in denied boarding or regulatory penalties.

**Success criteria:**
- 100% of departing international passengers have APIS submitted before departure
- Submission errors flagged and resolved before gate close
- Audit trail: transmission timestamp, acknowledgment, any error and resolution

---

## Journey 5: Exception Handling for Missing or Expired Documents

**Trigger:** Readiness check returns NOT READY status for one or more segments.

**Steps:**
1. NOT READY status delivered to passenger or agent with specific reason codes
2. Remediation options presented: obtain visa, renew passport, upload health certificate, contact airline
3. Passenger uploads corrected or new document; readiness check re-run
4. If remediated → status updated to READY; audit trail records resolution
5. If not remediated by check-in cutoff → agent escalation; boarding denial logged with regulatory reference

**Exception escalation:**
- Denied boarding logged with DOT-required documentation
- ADA-related document issues escalated per 14 CFR Part 382 procedures

**Success criteria:**
- Exception reason codes actionable (passenger knows exactly what to fix)
- Re-check cycle completes within latency target
- All denied-boarding events logged with regulatory reference

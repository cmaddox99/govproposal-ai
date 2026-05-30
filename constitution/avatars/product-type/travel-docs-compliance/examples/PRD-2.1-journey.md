# PRD-2.1: User Journey Mapping — Travel Documents Compliance

**Law Reference:** [PRD-2.1](../../../../laws/product/user-journey-mapping.md)
**Avatar:** travel-docs-compliance
**Status:** Active — grounded in traveldocuments-ios

---

## Journey: Passenger Pre-Departure Document Verification

**Persona:** International passenger, first-time traveler to EU destination  
**Entry point:** Check-in app, 72-hour pre-departure readiness check

| Step | Passenger action | iOS module | Class | Law |
|------|-----------------|------------|-------|-----|
| 1. Trigger readiness check | Opens app 72h before departure | traveldocuments-ios | `AirportSecurityFlowManager` | PRD-2.1 |
| 2. Passport scan offered | Camera scan option presented | ScanPassport | `PassportScanOptionsViewController` | PRD-1.1 (scan vs. manual discovery) |
| 3. Scan MRZ | Passenger scans passport MRZ | ScanPassport | `ScanPassportViewController` → `MrzScanner` | ENG-6.1 (encrypt MRZ at rest) |
| 4. MRZ validated | Parsed `MrzData` matched to PNR | ScanPassport | `MrzData` → BFF validate | ENG-6.1 (no raw PII in logs) |
| 5. Touchless eligibility check | TSA touchless eligibility evaluated | AirportSecurity | `TouchlessEligibilityViewModel` → `TouchlessEligibilityEndpoint` | BUS-2.1 (APIS mandatory) |
| 6. Consent captured | Facial match consent recorded | AirportSecurity | `TouchlessConsentEndpoint` | BUS-4.3 (biometric consent) |
| 7. Readiness decision | READY / NOT READY returned | AirportSecurity | `TouchlessEligibilityView` | PRD-5.1 (false-block rate) |
| 8. Audit record | Decision immutably logged | traveldocuments-ios | `TravelDocumentsEnvironment` → BFF audit | ENG-6.7 (audit trail) |

---

## Journey: Gate Agent Document Exception Handling

**Persona:** Check-in agent handling passenger flagged as NOT READY  
**Entry point:** Agent console; `TouchlessEligibilityViewController` override path

| Step | Agent action | Module | Key consideration |
|------|-------------|--------|-------------------|
| 1. View exception | Agent sees NOT READY flag with reason codes | `TouchlessEligibilityView` | Reason codes must be actionable |
| 2. Request document | Agent asks passenger for manual document | `PassportScanOptionsViewController` analytics | Track manual-vs-scan choice |
| 3. Manual MRZ entry | Agent enters MRZ data manually | `MRZEntryViewController` | MRZ field validation via `MRZStringHelper` |
| 4. Override or escalate | Agent overrides or escalates to supervisor | `AirportSecurityFlowManager` | ENG-6.7: override event logged with supervisor ID |
| 5. Audit complete | All override events logged | BFF audit endpoint | DOT 14 CFR 14: regulatory evidence required |

---

## Failure States and Branching

| Failure | Module | Handling |
|---------|--------|---------|
| TIMATIC timeout | `TouchlessEligibilityEndpoint` | Return degraded mode flag; conservative (NOT READY) default |
| MRZ parse error | `MrzScanner` → `MrzData` | Re-prompt scan; offer manual entry fallback |
| Biometric match failure | `TouchlessEligibilityViewModel` | Agent review path; consent re-capture if needed |
| Health cert not recognized | BFF `HealthDocsStatusRequestBuilder` | Reason code: health cert format; direct to VeriFly |

---

## Success Metrics (PRD-5.1 alignment)

| Journey step | Metric | Target |
|-------------|--------|--------|
| MRZ scan success rate | `ScanPassportViewController` completion | ≥96% |
| Touchless eligibility latency | `TouchlessEligibilityEndpoint` p95 | ≤1800ms |
| False-block rate | TIMATIC NOT READY overturned by agent | <0.5% |
| APIS submission success | `TouchlessConsentEndpoint` → CBP | 100% |

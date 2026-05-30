# PRD-1.1: Continuous Discovery — Travel Documents Compliance

**Law Reference:** [PRD-1.1](../../../../laws/product/continuous-discovery.md)
**Avatar:** travel-docs-compliance
**Status:** Active — grounded in traveldocuments-ios and TravelDocs BFF

---

## Discovery Focus Areas

### 1. TIMATIC False-Positive Analysis
**Problem signal:** Passengers blocked at check-in despite having valid documents.

**Discovery methods:**
- Review `TouchlessEligibilityViewModel` logs for INELIGIBLE decisions followed by agent override within 30 minutes
- Interview gate agents on override frequency per route: which origin-destination pairs produce the most overrides?
- Cross-reference TIMATIC rule version at time of decision vs. rule version at boarding

**Metrics to track:**
- False-block rate: target <0.5% (baseline 1.8%)
- Agent override rate for TIMATIC-blocked passengers: baseline 23%

---

### 2. MRZ Scan Failure Discovery
**Problem signal:** Passengers abandoning `ScanPassportViewController` mid-flow.

**Discovery methods:**
- Analyze `MrzScanner` failure events by document type (biometric vs. non-biometric), device model, and ambient lighting conditions
- Track `PassportScanOptionsViewController` selection: how often does camera scan vs. manual entry win?
- Review `AAFeaturePassportCameraScanAsPrimary` adoption: does making camera primary reduce failure?

**Metrics to track:**
- `ScanPassportViewController` abandonment rate by device model: baseline 4.2%
- MRZ parse error rate: `MrzData` validation failure frequency

---

### 3. Pre-Departure Checklist Comprehension
**Problem signal:** Passengers arrive at airport confused despite receiving readiness notification.

**Discovery methods:**
- Usability sessions with international passengers post-check-in: "Did you understand what documents you needed?"
- Analyze which reason codes from `TouchlessEligibilityView` correlate with agent call escalation
- Test readiness checklist with non-native English speakers on key international routes

---

## Key Discovery Outputs (Prioritized)

| Finding | Evidence | Priority |
|---------|----------|----------|
| TIMATIC false-block concentrated on connecting itineraries | Agent override log analysis | P1 |
| Camera scan fails on non-biometric passports from 8 countries | MrzScanner error telemetry | P1 |
| Health cert requirements confuse passengers 72h before departure | Support ticket analysis | P2 |
| Touchless eligibility latency spikes >3s on peak morning departures | `TouchlessEligibilityEndpoint` APM | P2 |

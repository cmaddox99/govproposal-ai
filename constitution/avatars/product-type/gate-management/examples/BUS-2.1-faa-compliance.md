---
avatar: avatar-product-gate-management
law: BUS-2.1
title: "FAA Compliance Law"
---

# BUS-2.1 — FAA Compliance Law: Gate Management Application

**What this law requires:** All gate operations software must comply with applicable FAA, TSA, CBP, and DOT regulations. Compliance is not optional and cannot be deferred to post-launch.

---

## Regulatory Map — Gate Management Domains

| Domain | Governing Regulation | Key Obligation |
|---|---|---|
| All gate operations | FAR Part 139 | Airport certification — gate systems must not impair airfield safety or ARFF coordination |
| Biometric Boarding | TSA 49 CFR Part 1542 | Identity verification before sterile area access; no boarding pass bypass without documented biometric match |
| Biometric Boarding | CBP Biometric Exit | Opt-out always available; biometric data retention ≤12 hours post-departure; threshold changes require CBP notification |
| Tarmac events (all domains) | DOT 14 CFR Part 259 | 3-hour domestic / 4-hour international tarmac hard limits; no system override permitted |
| Carry-On Baggage | DOT Consumer Protection | Carry-on fee disclosure at booking and gate; denied boarding compensation documented |
| Biometric + Carry-On (intl) | GDPR / CCPA | Explicit consent before biometric enrollment; right-to-deletion handling; biometric templates on US soil |

---

## Acceptance Criteria — Per Regulation

### FAR Part 139
- [ ] Gate assignment weight/aircraft-type constraints enforced and logged
- [ ] Airfield safety compliance events logged to FAA-accessible audit store

### TSA 49 CFR Part 1542
- [ ] Every boarding event has: biometric match result, agent ID, gate ID, timestamp, PNR reference
- [ ] No-match events have reason code — not just "failed"
- [ ] Boarding system fails closed on identity service outage — never fails open

### CBP Biometric Exit
- [ ] Opt-out UI is prominent on boarding screen — never requires more than one tap
- [ ] Biometric templates purged within 12 hours of flight departure (automated, logged)
- [ ] Threshold change triggers CBP notification workflow before taking effect

### DOT 14 CFR Part 259
- [ ] Tarmac elapsed timer visible to gate agent at all times — never in a sub-screen or settings tab
- [ ] 3hr domestic / 4hr international threshold triggers mandatory alert — no agent override permitted
- [ ] Timer state transitions logged with timestamp for DOT audit

### GDPR / CCPA
- [ ] Biometric enrollment requires explicit, documented consent (not pre-checked box)
- [ ] Deletion request triggers purge of biometric template within 30 days
- [ ] Biometric data never leaves US-based Azure regions

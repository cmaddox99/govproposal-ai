---
avatar: avatar-check-in-travel
law_id: BUS-9.3
law_title: "Breach Notification"
file_type: example
---

# BUS-9.3 Breach Notification — Check-In & Travel

## Law Summary

Unauthorized exposure of passenger check-in data — especially passport scans, facial recognition data, or CBP/TSA APIS records — triggers immediate incident response with **government notification obligations** in addition to GDPR/CCPA requirements.

---

## ✅ COMPLIANT Example — Biometric Vendor Breach Response

**Scenario:** The facial recognition vendor notifies AA that a vulnerability exposed 500K passenger facial match records.

**Incident Response Phases:**

| Phase | Action | SLA |
|-------|--------|-----|
| Detect | Vendor notification received; DLP alert confirms scope | T+0 |
| Contain | Revoke biometric API credentials; suspend facial match service | T+1h |
| Assess | Determine data fields exposed (facial match data, passenger_id_hash, flight records) | T+4h |
| Notify Internal | Legal/Privacy/CISO notified | T+1h |
| Notify Government | CBP notified per data sharing agreement — government partnership data | T+24h |
| Notify Regulators | GDPR DPA notification for EU passenger data within 72h | T+72h |
| Notify Passengers | Affected passengers notified per state law requirements | T+30 days (CCPA/state law) |

**Required notification recipients for biometric breach:**
- CBP (government data sharing obligation)
- GDPR DPA for each EU member state with affected passengers
- Affected passengers (CCPA for CA; state laws for other states)

---

## ✅ COMPLIANT Example — APIS Transmission Intercept

**Scenario:** Security monitoring detects anomalous access to the APIS transmission queue, suggesting possible interception of government-bound passenger manifests.

**Immediate actions:**
1. Suspend APIS transmission pipeline; switch to backup channel
2. Notify Legal within 1 hour
3. Notify CBP per data sharing agreement within 24 hours
4. Engage forensics to determine data exposed
5. GDPR DPA notification within 72 hours (international flights — EU passengers affected)

---

## ❌ VIOLATION Example — Delayed Government Notification

**Scenario:** A passport scan database is breached. The security team notifies GDPR DPA within 72 hours but does not notify CBP for 2 weeks, assuming it is only a regulatory matter.

**Why this violates BUS-9.3:** Passport and APIS data shared with government agencies must be reported to those agencies under data sharing agreement terms — which typically require faster notification than GDPR. Treating it only as a consumer privacy matter violates the government notification obligation.

**Correct approach:** Government notification obligations must be assessed in parallel with GDPR/CCPA obligations, not sequentially. Pre-approve breach templates for both government and regulatory paths before an incident occurs.

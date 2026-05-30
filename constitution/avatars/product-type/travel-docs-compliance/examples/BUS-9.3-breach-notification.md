---
avatar: avatar-product-travel-docs-compliance
law_id: BUS-9.3
law_title: "Breach Notification"
file_type: example
---

# BUS-9.3 Breach Notification — Travel Docs Compliance

## Law Summary

Passport and visa data breach is **HIGHEST sensitivity** — triggers **government reporting obligations** to DHS/CBP/TSA in addition to GDPR and CCPA. Government notification timeframes (defined in data sharing agreements) may be shorter than GDPR's 72-hour window.

---

## ✅ COMPLIANT Example — Passport Scan Storage Breach

**Scenario:** A security vulnerability exposes 50K passport scan images stored for pre-departure document verification.

**Incident Response Phases:**

| Phase | Action | SLA |
|-------|--------|-----|
| Detect | DLP alert on passport scan storage access anomaly | T+0 |
| Contain | Revoke access; isolate affected storage; patch vulnerability | T+2h |
| Assess | Determine scope: passport count, data fields, nationalities exposed | T+6h |
| Notify Legal | Legal/Privacy/CISO/CPO notified | T+1h |
| Notify Government | DHS/CBP notified per data sharing agreement SLA | T+24h (or per agreement) |
| Notify DPA | GDPR notification for EU passport holders | T+72h |
| Notify CCPA | California residents notified per state law | Per CCPA |
| Notify Passengers | Affected passengers notified | Per applicable law |

**Government notification SLA note:** Data sharing agreements with DHS/CBP may specify notification windows shorter than 72 hours. Always check the applicable agreement — government SLA governs, not GDPR, for government notification.

---

## ✅ COMPLIANT Example — Timatic API Credential Compromise

**Scenario:** A Timatic API key is found in a publicly accessible log file.

**Immediate actions:**
1. Revoke Timatic API credential immediately (T+0)
2. Audit Timatic API logs for unauthorized queries (T+4h)
3. If passenger document data was queried by unauthorized party: full breach notification
4. Issue new credential only after security review (T+48h)
5. Report to Legal if any government-bound data was accessible

---

## ❌ VIOLATION Example — Omitting Government Notification

**Scenario:** Passport data is breached. The team notifies the GDPR DPA within 72 hours but does not notify DHS/CBP, reasoning that the breach is an AA IT incident, not a government data matter.

**Why this violates BUS-9.3:** Passport data shared with DHS/CBP under data sharing agreements carries notification obligations to those agencies in the event of a breach. These are contractual and regulatory obligations that run independently of GDPR. Government notification is not optional because the breach occurred in AA's systems.

**Correct approach:** For any breach involving passport, visa, or APIS data, government notification to DHS/CBP/TSA must be assessed in parallel with GDPR/CCPA. Pre-approve notification templates for government agencies before an incident occurs.

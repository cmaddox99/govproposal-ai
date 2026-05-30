---
avatar: avatar-loyalty-aadvantage
law_id: BUS-9.3
law_title: "Breach Notification"
file_type: example
---

# BUS-9.3 Breach Notification — AAdvantage Loyalty

## Law Summary

Unauthorized exposure of AAdvantage member PII (miles balance, travel history, partner data) triggers notification obligations under GDPR (EU members), CCPA (California members), and potentially multiple US state laws given the **180M member base**.

---

## ✅ COMPLIANT Example — Mass Member PII Exposure

**Scenario:** A database misconfiguration exposes AAdvantage member records (name, email, miles balance, travel history) for 2 weeks before detection.

**Incident Response Phases:**

| Phase | Action | SLA |
|-------|--------|-----|
| Detect | Automated DLP alert on anomalous data access pattern | T+0 |
| Contain | Revoke access; patch misconfiguration; isolate affected tables | T+2h |
| Assess | Determine scope: records exposed, data fields, access log analysis | T+8h |
| Notify Legal | Legal, Privacy, CISO notified | T+1h |
| Notify EU DPA | GDPR Article 33 notification for EU member exposure | T+72h |
| Notify CA AG | CCPA notification for California member exposure | Per CCPA timing |
| Notify Members | Affected members notified per applicable state law | Per state law |

**Multi-jurisdiction checklist for 180M member base:**
- GDPR: Any EU member affected → DPA notification within 72 hours
- CCPA: California members → AG notification and member notification
- State laws: Review all 50 states for applicable breach notification requirements

---

## ✅ COMPLIANT Example — Partner API Key Exposure

**Scenario:** A credit card partner's API key (used to post earn transactions) is found in a public repository.

**Immediate actions:**
1. Revoke the exposed API key immediately (T+0)
2. Audit partner API access logs to determine if unauthorized earn transactions were posted (T+4h)
3. If member data was accessed via the partner API: trigger full breach notification
4. Issue new API key to partner only after security review (T+48h)

---

## ❌ VIOLATION Example — US-Only Notification

**Scenario:** Member data is breached. The team sends CCPA notification for California members but does not assess GDPR obligations, reasoning that the AAdvantage program is US-based.

**Why this violates BUS-9.3:** AAdvantage has 180M global members. EU residents who are AAdvantage members are protected under GDPR regardless of where AA is headquartered. Any breach affecting EU member data requires GDPR DPA notification within 72 hours. Global program, global notification obligations.

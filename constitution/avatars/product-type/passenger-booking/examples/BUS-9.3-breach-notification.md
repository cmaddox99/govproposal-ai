---
avatar: avatar-passenger-booking
law_id: BUS-9.3
law_title: "Breach Notification"
file_type: example
---

# BUS-9.3 Breach Notification — Passenger Booking

## Law Summary

Unauthorized exposure of booking data triggers notification across **multiple frameworks**: PCI DSS (card brands), GDPR (DPA within 72 hours), and CCPA for California residents.

---

## ✅ COMPLIANT Example — PCI DSS Card Data Breach

**Scenario:** A security scan reveals that card numbers were inadvertently logged in an application debug log for 48 hours before detection.

**Incident Response Phases:**

| Phase | Action | SLA |
|-------|--------|-----|
| Detect | Log scanner alert triggers; security team validates PAN presence | T+0 |
| Contain | Disable debug logging; purge affected log files; rotate credentials | T+2h |
| Assess | Determine scope (which PANs, how many records, access log review) | T+8h |
| Notify Card Brands | Visa, Mastercard, Amex notified per PCI DSS Incident Response | T+72h |
| Notify DPA | GDPR DPA notification for EU passenger booking data | T+72h |
| Notify Passengers | CCPA notification for California resident card data exposure | As required by state law |

**PCI DSS-specific obligations:**
- Card brands (Visa, Mastercard) must be notified within 72 hours of confirmed card data exposure
- Forensics must confirm scope before notification to card brands

---

## ✅ COMPLIANT Example — GDS API Credential Compromise

**Scenario:** An engineer detects that a GDS API credential was accidentally committed to a public repository.

**Immediate actions:**
1. Revoke GDS API credential immediately (T+0)
2. Assess scope of unauthorized access using GDS access logs (T+4h)
3. If passenger PNR data was accessed: trigger full breach notification workflow
4. Rotate all GDS credentials (T+24h)

---

## ❌ VIOLATION Example — Single-Framework Notification Only

**Scenario:** EU passenger PNR data is exposed. The team notifies only the EU DPA within 72 hours and considers the incident closed.

**Why this violates BUS-9.3:** Multi-framework breaches require parallel notifications. If the PNR data included payment information, PCI DSS card brand notification is also required. If California residents are affected, CCPA notification applies. Single-framework notification leaves legal exposure.

**Correct approach:** At the start of every incident, run a framework checklist: PCI DSS? GDPR? CCPA? Other state laws? All applicable frameworks must be notified in parallel, not sequentially.

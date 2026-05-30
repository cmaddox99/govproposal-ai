---
avatar: avatar-product-travel-docs-compliance
law_id: BUS-1.1
law_title: "Priority Hierarchy Law"
file_type: example
---

# BUS-1.1 Priority Hierarchy — Travel Docs Compliance

## Law Summary

Travel Docs operates at **HIGHEST sensitivity** — government legal obligations (CBP/DHS/TSA) are ABSOLUTE requirements that override ALL other concerns including system efficiency.

| Priority | Level | Travel Docs Domain Example |
|----------|-------|--------------------------|
| 1 | Legal | CBP/DHS APIS transmission is a legal obligation — cannot be skipped for performance |
| 2 | Safety | Denied boarding for missing docs is legally required — Safety > Efficiency |
| 3 | Privacy | Passport and visa data classified RESTRICTED — security controls non-negotiable |
| 4 | Security | Government API credentials in vault — no exception for integration speed |
| 5 | Business Continuity | Government API downtime requires human escalation — no silent failure |
| 6 | Efficiency | System performance improvements — only when all government obligations are satisfied |

---

## ✅ COMPLIANT Example 1 — APIS Transmission During System Degradation

**Scenario:** The APIS transmission service is experiencing intermittent failures due to a network issue. An engineer proposes disabling APIS for domestic connecting flights to reduce system load.

**Decision:** REJECTED. APIS transmission is a **Legal** obligation for international flights and cannot be disabled for any operational reason. The correct response is to escalate the network issue and implement the approved fallback protocol (manual transmission if automated fails).

**Required approach:** Government API obligations require an explicit fallback protocol — not suppression. Document the fallback and escalation path before any APIS integration goes to production.

---

## ✅ COMPLIANT Example 2 — Denied Boarding for Missing Documents

**Scenario:** An efficiency initiative proposes allowing passengers with missing transit visa documentation to board with a "document will be collected onboard" note to improve on-time departure.

**Decision:** REJECTED. Denied boarding for non-compliant documentation is a **Legal/Safety** requirement — airlines are liable for transporting undocumented passengers. Legal > Efficiency, unconditionally. No exception for on-time performance metrics.

---

## ❌ VIOLATION Example 1 — Government API Credential in Config File

**Scenario:** A developer stores the Timatic API key in a committed config file to simplify local development.

**Why this violates BUS-1.1:** Government API credentials must be vault-managed per Security requirements. Security > Efficiency. Local development convenience does not justify exposing government API credentials.

---

## ❌ VIOLATION Example 2 — Silent APIS Failure

**Scenario:** The APIS transmission service fails silently during a high-volume departure wave. The system allows check-in to proceed without logging the failure or alerting operations.

**Why this violates BUS-1.1:** Legal > Efficiency. Silent failure of a government-required transmission violates the Legal priority. The system must fail loudly and trigger the human escalation protocol.

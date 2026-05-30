---
avatar: avatar-passenger-booking
law_id: BUS-1.1
law_title: "Priority Hierarchy Law"
file_type: example
---

# BUS-1.1 Priority Hierarchy — Passenger Booking

## Law Summary

Decisions MUST follow: **Legal > Safety > Privacy > Security > Business Continuity > Efficiency**. Higher-priority concerns win WITHOUT EXCEPTION.

| Priority | Level | Booking Domain Example |
|----------|-------|----------------------|
| 1 | Legal | PCI-DSS card tokenization is non-negotiable — no PAN in logs or URLs |
| 2 | Safety | DOT refund SLAs (7 business days) cannot be extended for operational efficiency |
| 3 | Privacy | GDPR consent for EU passengers overrides conversion funnel optimization |
| 4 | Security | CDE zone isolation for payment flow — cannot be relaxed for feature velocity |
| 5 | Business Continuity | GDS failover maintains booking capability during outages |
| 6 | Efficiency | Booking flow performance improvements — pursued only after higher priorities satisfied |

---

## ✅ COMPLIANT Example 1 — PCI-DSS Tokenization Requirement

**Scenario:** To debug a payment failure, an engineer proposes temporarily logging the full card number to a development log to diagnose the issue faster.

**Decision:** REJECTED. Storing PAN (Primary Account Number) in any log is a PCI-DSS violation. Legal > Efficiency. Debugging must use tokenized card reference only.

**Required approach:** Use payment gateway debugging tools that work with tokens. Never log PAN or unmasked card data regardless of operational urgency.

---

## ✅ COMPLIANT Example 2 — DOT Refund SLA Override

**Scenario:** Customer Service proposes delaying refund processing by 15 business days during peak periods to reduce operational load.

**Decision:** REJECTED. DOT regulations require credit card refunds within 7 business days. Legal compliance is non-negotiable. Operational load must be addressed through resourcing, not SLA extension.

---

## ❌ VIOLATION Example 1 — GDPR Consent Bypass

**Scenario:** To improve EU conversion rates, a product manager proposes pre-ticking the marketing consent checkbox on the EU booking flow.

**Why this violates BUS-1.1:** GDPR requires freely given, specific, informed, and unambiguous consent. Pre-ticked boxes do not constitute valid consent. Privacy > Efficiency — this cannot be overridden for conversion optimization.

---

## ❌ VIOLATION Example 2 — CDE Relaxation

**Scenario:** To accelerate a new payment method feature, engineering proposes routing payment data outside the CDE zone temporarily.

**Why this violates BUS-1.1:** CDE isolation is a Security/Legal requirement under PCI-DSS. No feature velocity justification can override it. Security > Business Continuity > Efficiency.

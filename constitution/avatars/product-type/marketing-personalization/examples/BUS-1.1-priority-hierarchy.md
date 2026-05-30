---
avatar: avatar-product-marketing-personalization
law_id: BUS-1.1
law_title: "Priority Hierarchy Law"
file_type: example
---

# BUS-1.1 Priority Hierarchy — Marketing Personalization

## Law Summary

Decisions MUST follow: **Legal > Safety > Privacy > Security > Business Continuity > Efficiency**. Customer opt-out ALWAYS overrides targeting efficiency. Higher-priority concerns win WITHOUT EXCEPTION.

| Priority | Level | Marketing Personalization Domain Example |
|----------|-------|----------------------------------------|
| 1 | Legal | GDPR consent requirements override conversion funnel optimization for EU customers |
| 2 | Safety | Discriminatory targeting patterns must be ruled out regardless of model accuracy improvement |
| 3 | Privacy | Customer opt-out overrides all targeting — no high-value segment exception |
| 4 | Security | Propensity model data and offer audit table cannot be shared outside approved systems |
| 5 | Business Continuity | Fallback to rule-based targeting when propensity model is unavailable |
| 6 | Efficiency | Campaign ROI optimization — pursued only after all higher-priority obligations are satisfied |

---

## ✅ COMPLIANT Example 1 — Customer Opt-Out Enforcement

**Scenario:** A campaign manager proposes including a recently opted-out customer in a high-value win-back campaign because the customer "opted out by accident" based on support ticket notes.

**Decision:** REJECTED. Customer opt-out is a **Privacy** right. Inferring or assuming the opt-out was accidental is not a valid reason to override it. The customer must re-opt-in voluntarily. Privacy > Efficiency, with no high-value segment exception.

**Required approach:** The opt-out filter must run for every campaign, with no bypass. If a customer has opted out, the only permissible action is to deliver opt-in recovery communications through the consent management system — not to target them with offers.

---

## ✅ COMPLIANT Example 2 — Sensitive Category Data Prohibition

**Scenario:** A data scientist proposes including inferred health-related propensity scores (frequent wheelchair requests → inferred mobility limitation) in the offer targeting model to improve personalization relevance.

**Decision:** REJECTED. Sensitive category data (health/medical inferences) must never be used for targeting. Safety concern (potential discrimination) overrides model accuracy improvement. Safety > Efficiency, unconditionally.

---

## ❌ VIOLATION Example 1 — GDPR Consent Bypass for EU Customers

**Scenario:** To improve EU campaign performance, a product manager proposes pre-populating marketing consent for EU customers who previously engaged with offers.

**Why this violates BUS-1.1:** GDPR requires freely given, unambiguous consent for marketing. Prior engagement does not constitute consent. Privacy (GDPR legal requirement) > Efficiency. Pre-populating consent for EU customers is a GDPR violation regardless of engagement history.

---

## ❌ VIOLATION Example 2 — Model Deployed Without Bias Review

**Scenario:** A new propensity model is deployed to production without a bias/fairness review because the team was confident in the model's performance metrics.

**Why this violates BUS-1.1:** Safety concerns (discriminatory targeting patterns) must be ruled out before deployment. Safety > Efficiency. Model performance metrics do not substitute for a bias review. The safety gate must be passed before the efficiency gain is realized.

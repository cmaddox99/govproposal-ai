---
avatar: avatar-loyalty-aadvantage
law_id: BUS-1.1
law_title: "Priority Hierarchy Law"
file_type: example
---

# BUS-1.1 Priority Hierarchy — AAdvantage Loyalty

## Law Summary

Decisions MUST follow: **Legal > Safety > Privacy > Security > Business Continuity > Efficiency**. Higher-priority concerns win WITHOUT EXCEPTION.

| Priority | Level | Loyalty Domain Example |
|----------|-------|----------------------|
| 1 | Legal | Partner data sharing agreements require legal review before any data is shared |
| 2 | Safety | Elite benefit decisions involving medical accommodations prioritize Safety |
| 3 | Privacy | Member PII protection takes precedence over campaign targeting efficiency |
| 4 | Security | Points ledger security controls cannot be relaxed for partner integration speed |
| 5 | Business Continuity | Partner API failover maintains earn/burn capability during outages |
| 6 | Efficiency | Program margin optimization — pursued only after higher priorities satisfied |

---

## ✅ COMPLIANT Example 1 — Partner Data Sharing

**Scenario:** A new hotel partner requests member travel history data to improve offer targeting. The partnership team proposes sharing the data to accelerate the partner launch.

**Decision:** REQUIRES Privacy review before any data sharing. Legal and Privacy review must confirm the scope of data sharing is covered by member consent and the data sharing agreement.

**Required action:** Privacy review completed and documented. Data sharing scope limited to what is in member consent. Legal sign-off documented before partner receives any data.

---

## ✅ COMPLIANT Example 2 — Elite Medical Accommodation

**Scenario:** An executive requests overriding the standard medical accommodation process for elite members to reduce processing time.

**Decision:** REJECTED. Safety requirements for medical accommodations must not be bypassed for efficiency. The full medical review process must be followed for all members regardless of elite status.

---

## ❌ VIOLATION Example 1 — Partner Integration Without Privacy Review

**Scenario:** A product manager shares member propensity scores with a new credit card partner to improve offer acceptance rates, citing an efficiency gain. No Privacy review was conducted.

**Why this violates BUS-1.1:** Privacy > Efficiency. Sharing member data without Privacy review violates the hierarchy. Even a compelling efficiency or revenue argument cannot bypass Privacy requirements.

---

## ❌ VIOLATION Example 2 — Points Ledger Security Shortcut

**Scenario:** To accelerate a new partner integration, engineering disables an authentication requirement on the points ledger API for the partner.

**Why this violates BUS-1.1:** Security controls on the points ledger protect 180M member accounts. Security > Business Continuity > Efficiency. No partner integration speed justifies weakening security controls.

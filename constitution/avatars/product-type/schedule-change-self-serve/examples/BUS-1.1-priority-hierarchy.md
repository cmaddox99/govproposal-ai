---
avatar: avatar-schedule-change-self-serve
law_id: BUS-1.1
law_title: "Priority Hierarchy Law"
file_type: example
---

# BUS-1.1 Priority Hierarchy — Schedule Change Self-Serve

## Law Summary

Decisions MUST follow: **Legal > Safety > Privacy > Security > Business Continuity > Efficiency**. Higher-priority concerns win WITHOUT EXCEPTION.

| Priority | Level | Schedule Change Domain Example |
|----------|-------|-------------------------------|
| 1 | Legal | DOT-required fee waivers for IROP passengers are non-negotiable |
| 2 | Safety | Same-day change SLAs protect passenger safety in time-critical scenarios |
| 3 | Privacy | Passenger rebooking history privacy overrides agent convenience |
| 4 | Security | BFF API authentication cannot be relaxed for throughput improvement |
| 5 | Business Continuity | Fallback to agent-assisted rebooking when self-serve is unavailable |
| 6 | Efficiency | Self-serve throughput improvements — only after higher priorities satisfied |

---

## ✅ COMPLIANT Example 1 — DOT Fee Waiver Enforcement

**Scenario:** To reduce operational cost, a product manager proposes adding friction to the IROP fee waiver flow to reduce waiver utilization rates.

**Decision:** REJECTED. DOT regulations require fee waivers for IROP-eligible passengers. Adding friction to suppress legally required waivers violates Legal requirements. Legal > Efficiency — unconditionally.

**Required approach:** IROP fee waivers must be automatically applied for eligible passengers. Any suppression of legally required waivers violates the priority hierarchy.

---

## ✅ COMPLIANT Example 2 — Privacy over Agent Convenience

**Scenario:** Agents request read access to all passengers' rebooking history across all flights to make rebooking decisions faster.

**Decision:** REQUIRES Privacy review. Access must be scoped to the specific passenger being served. Bulk rebooking history access creates unnecessary privacy risk and violates data minimization principles.

---

## ❌ VIOLATION Example 1 — Eligibility Rule Bypasses Legal Requirement

**Scenario:** An engineer adjusts the IROP eligibility rule to exclude passengers on non-refundable fares from fee waivers in order to reduce waiver cost.

**Why this violates BUS-1.1:** DOT rules govern IROP fee waiver eligibility — AA's internal fare rules cannot override DOT requirements. Legal > Efficiency, regardless of cost impact.

---

## ❌ VIOLATION Example 2 — BFF Authentication Relaxed

**Scenario:** BFF API authentication is disabled for internal tools to speed up rebooking during an IROP event.

**Why this violates BUS-1.1:** Security controls on the BFF API protect passenger PNR data. Security > Efficiency, including during high-stress operational scenarios.

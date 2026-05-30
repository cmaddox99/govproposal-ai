---
avatar: avatar-check-in-travel
law_id: BUS-1.1
law_title: "Priority Hierarchy Law"
file_type: example
---

# BUS-1.1 Priority Hierarchy — Check-In & Travel

## Law Summary

Decisions MUST follow: **Legal > Safety > Privacy > Security > Business Continuity > Efficiency**. When two concerns conflict, the higher-priority concern wins WITHOUT EXCEPTION.

| Priority | Level | Check-In Domain Example |
|----------|-------|------------------------|
| 1 | Legal | CBP/TSA APIS transmission is a legal obligation — never delayed for performance |
| 2 | Safety | TSA PreCheck must never be bypassed or approximated for boarding speed |
| 3 | Privacy | Biometric enrollment must be opt-in — passenger consent is required |
| 4 | Security | Biometric data encrypted at rest and in transit, no exceptions |
| 5 | Business Continuity | Fallback kiosk check-in when biometric systems fail |
| 6 | Efficiency | Boarding speed improvements — only pursued when higher priorities are satisfied |

---

## ✅ COMPLIANT Example 1 — CBP/APIS Transmission Override

**Scenario:** The APIS transmission service is experiencing latency, adding 800ms to check-in time. Engineering proposes to batch APIS transmissions to reduce latency impact.

**Decision:** REJECTED. APIS transmission to CBP is a **Legal** obligation. Batching creates a window where passengers board without government clearance. Legal > Efficiency — no exception.

**Required action:** Investigate APIS transmission latency root cause. Escalate to vendor. Do NOT reduce transmission frequency.

---

## ✅ COMPLIANT Example 2 — Biometric Opt-In Requirement

**Scenario:** Marketing proposes making facial recognition enrollment the default (opt-out) to drive biometric adoption metrics.

**Decision:** REJECTED. Biometric enrollment must be **opt-in**. Safety (consent) requires the passenger to affirmatively choose biometric processing. Privacy > Efficiency even when adoption metrics would improve.

**Required action:** Keep biometric enrollment as opt-in. Track adoption rate honestly. Improve the opt-in experience instead.

---

## ❌ VIOLATION Example 1 — TSA PreCheck Bypass

**Scenario:** During high-volume boarding, a kiosk engineer routes passengers with TSA PreCheck to the standard lane to reduce kiosk congestion.

**Why this violates BUS-1.1:** TSA PreCheck is a **Safety/Legal** requirement. Routing PreCheck passengers to standard screening violates TSA program rules. Efficiency cannot override Legal obligations.

**Correct approach:** Fix kiosk congestion through capacity or UX improvements. Never suppress TSA PreCheck routing.

---

## ❌ VIOLATION Example 2 — ADA Accommodation Skipped for Speed

**Scenario:** To reduce boarding time, an engineer removes the ADA accommodation prompt from the express check-in flow to simplify the screen.

**Why this violates BUS-1.1:** ADA accommodations are a **Legal** requirement. Removing them from any check-in flow violates accessibility law. Legal > Efficiency, unconditionally.

**Correct approach:** ADA accommodation options must appear in every check-in flow. Boarding time improvements must work around this requirement.

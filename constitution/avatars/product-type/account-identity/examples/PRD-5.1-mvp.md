---
avatar: avatar-account-identity
law_id: PRD-5.1
law_title: "Minimum Viable Product Discipline"
file_type: example
---

# PRD-5.1 Minimum Viable Product Discipline — Example

## Law Summary

**PRD-5.1** requires that MVP scope is constrained to the smallest set of functionality that can validate the core hypothesis. An MVP is a learning vehicle, not a feature-complete release. Scope expansion before hypothesis validation violates this law.

---

## ✅ COMPLIANT Example: Secure Traveler Profile Update

### Feature Context

The secure traveler profile — managed via `SecureTravelerEndpoint` and `SecureTravelerSubmitEndpoint` — allows AAdvantage members to store Known Traveler Number (KTN), TSA PreCheck, Global Entry, and passport details on their account. Product hypothesizes that in-app profile editing will reduce support call volume and improve secure traveler data completeness rates.

### MVP Definition

**Core Hypothesis:** Allowing members to update their Known Traveler Number (KTN) directly in the app via `SecureTravelerSubmitEndpoint` will reduce the support call volume for "update KTN" requests and improve KTN field completeness on accounts.

**MVP Scope — KTN Update Only:**

- One editable field: Known Traveler Number.
- Submitted via `SecureTravelerSubmitEndpoint` with existing validation rules.
- Success state: confirmation screen. Error state: inline field-level error message.
- Entry point: existing account profile screen rendered via `MyAccountBridgedWebViewController`.

**What is explicitly excluded from MVP:**
- TSA PreCheck number editing
- Global Entry number editing
- Passport details editing
- Emergency contact editing
- Any redesign of the profile screen layout

**Success Metrics:**
- KTN update completion rate via in-app flow (target: >70%)
- Support call deflection for KTN update requests (measured via support ticket tagging, 30-day window post-launch)
- Error rate on `SecureTravelerSubmitEndpoint` submissions (baseline from current web form for comparison)

**Learning Gate:** After 30 days, review completion rate and support deflection data. Only if completion rate exceeds 70% and call deflection is measurable does scope expand to TSA PreCheck and Global Entry fields.

---

## ❌ VIOLATION Example: Secure Traveler Profile Update (Scope Expansion at MVP)

> "MVP includes all profile fields: name, address, Known Traveler Number, TSA PreCheck, Global Entry, passport details, and emergency contact."

### Why This Violates PRD-5.1

**This is not an MVP — it is a full product release disguised as an MVP.**

1. **The core hypothesis is untested.** The hypothesis is: "Members will complete secure traveler updates in-app at a higher rate than via other channels, reducing support load." Testing this requires exactly one field, not seven. Adding all fields simultaneously means the team cannot determine which fields drive completion, which drive abandonment, and which generate the most support call deflection.

2. **Scope expansion before validation.** Passport details, emergency contact, and full name editing each carry distinct `AccountProfileEndpoint` and `SecureTravelerEndpoint` integration complexity — and distinct PII risk under BUS-4.3. Combining them into an "MVP" treats scope reduction as optional rather than required.

3. **Learning is impossible at full scope.** If the multi-field MVP has a low completion rate, the team cannot determine whether the problem is the KTN field, the passport field, the screen layout, or `SecureTravelerSubmitEndpoint` error handling. A single-field MVP isolates the variable.

4. **BUS-4.3 risk is amplified unnecessarily.** Every additional profile field in scope expands the PII footprint — name, address, passport number, and emergency contact all carry separate data classification requirements. An MVP that processes all of these simultaneously before the flow is validated creates disproportionate compliance exposure.

**The compliant path:** Ship KTN-only. Measure. Expand only after the hypothesis is confirmed.

---

## Application Notes for account-identity

- `SecureTravelerSubmitEndpoint` and `AccountProfileEndpoint` each represent distinct MVP increments. Treat them as separate validation opportunities, not a combined release.
- Web-bridge rendering via `MyAccountBridgedWebViewController` may limit the granularity of field-level instrumentation. Factor this into MVP success metric design — ensure the completion signal is measurable before committing to a metric.
- BUS-4.3 data subject rights apply to every field added to the secure traveler profile. MVP scope decisions also reduce compliance risk by limiting PII surface area during validation.

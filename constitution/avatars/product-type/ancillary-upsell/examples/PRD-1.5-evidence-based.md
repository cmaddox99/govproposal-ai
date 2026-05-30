---
avatar: avatar-ancillary-upsell
law_id: PRD-1.5
law_title: "Evidence-Based Decision Making"
file_type: example
---

# PRD-1.5 — Evidence-Based Decision Making

## Law Summary

Product decisions must be backed by evidence: quantitative data, qualitative research, or validated analogues. Intuition and preference are inputs to generating hypotheses, not sufficient justification for shipping features or making architectural decisions.

---

## ✅ COMPLIANT Example

### Decision Under Review

Whether to surface miles-as-payment in the instant upsell cabin upgrade flow via `UpgradeYourTripViewModel_MilesAsFormOfPayment` and `MilesOfferShelfViewModel`.

### Evidence Base

**Quantitative signals:**
- **67% of AAdvantage members eligible for a cabin upgrade have a sufficient miles balance** to cover at least one available upgrade offer at the time of offer delivery (data from `mobile-offers-bff` eligibility pipeline, trailing 6 months).
- **45% of eligible passengers with sufficient miles do not attempt to use miles for an upgrade** when only a cash payment path is surfaced. This is measured as: passenger received upgrade offer → passenger was miles-eligible → passenger did not select upgrade.
- When miles payment is surfaced alongside cash payment in A/B test cohort (n=18,400 eligible passengers over 8 weeks): **miles-path conversion rate was 2.3× the cash-path conversion rate** among passengers who had sufficient miles balance.
- Post-purchase survey in test cohort: 71% of passengers who converted via miles path reported they had not been aware they could use miles for post-booking upgrades before seeing the offer.

**Qualitative signals:**
- Usability sessions (n=12 participants): all participants who had miles available expressed strong positive reaction to miles-payment option; 9 of 12 said they would "definitely" or "probably" use it if available post-booking.
- Support ticket analysis: "Can I use miles to upgrade after booking?" is a top-10 inbound support query, suggesting unmet demand is suppressing conversion.

**Analogue evidence:**
- Miles-as-payment is already live in the initial booking upgrade path (passenger-booking avatar boundary); the pattern is architecturally validated. `UpgradeYourTripViewModel_MilesAsFormOfPayment` exists in `instantupsell-ios` and was built to support this path.

### Decision

Activate `MilesOfferShelfViewModel` and `UpgradeYourTripViewModel_MilesAsFormOfPayment` in the instant upsell flow. Measure primary metric: upgrade conversion rate among miles-eligible passengers. Secondary metric: miles redemption volume through post-booking channel.

---

## ❌ VIOLATION Example

### Proposed Decision

> "The product manager believes miles payment will be popular in the post-booking upgrade flow. Team is confident it will improve conversion. Let's enable it this sprint."

### Why This Violates PRD-1.5

This decision relies entirely on a product manager's belief and team confidence — neither of which is evidence. The statement makes a causal claim (miles payment will improve conversion) without any supporting data, experiment, research, or analogue.

**Specific failures:**
1. No quantitative baseline: What is the current conversion rate without miles? There is no measurement to improve against.
2. No evidence of demand: "Will be popular" is an assertion, not a finding. The 45% non-utilization stat (above) required data to discover — without looking, the team wouldn't know whether demand exists.
3. No analogue cited: Even though evidence exists (miles works in booking flow), this proposal doesn't reference it. Evidence must be explicitly cited, not implicitly assumed.
4. Skips hypothesis formation: A compliant approach converts "the PM thinks this will work" into a testable hypothesis with a defined success metric, then gathers evidence before a full rollout decision.

**Correct path:** Retrieve eligibility and miles-balance data from `mobile-offers-bff`. Run a controlled cohort. Cite the booking-flow analogue. Make the decision from evidence.

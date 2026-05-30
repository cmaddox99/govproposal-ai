---
avatar: avatar-ancillary-upsell
law_id: PRD-5.1
law_title: "MVP Discipline"
file_type: example
---

# PRD-5.1 — MVP Discipline

## Law Summary

An MVP is the minimum set of functionality required to test the most critical assumption about a new capability. It is not a feature-reduced v1. The test must be defined before the MVP is built, and the MVP scope must be the minimum required to run that test — nothing more.

---

## ✅ COMPLIANT Example

### Feature Under Development

Instant upsell — surfacing cabin upgrade offers to economy passengers post-booking via `instantupsell-ios`.

### Critical Assumption to Test

*Economy passengers presented with a single cabin upgrade offer on the post-booking screen will convert at a rate that demonstrates willingness to pay for post-booking upgrades.*

If this assumption fails, additional payment methods, multi-segment offers, and benefit callouts add no value. If it holds, there is a clear foundation for incrementally expanding the offer surface.

### MVP Scope Definition

**Included in MVP:**
- Single cabin offer for one flight segment on the post-booking confirmation screen.
- Cash payment path only, using existing `InstantUpsellOffersViewModel` and `SegmentOfferSelectionCoordinator`.
- Basic offer card rendered via `CabinOfferViewModel` with original cabin price from `OriginalCabinOfferViewModel` for price anchoring.
- Fare rules accessible via `FareRulesView` (required for BUS-2.3 compliance — not optional).
- Terms & conditions footer via `TermsAndConditionsFooterView` / `TermsAndConditionsFooterViewModel` (required for BUS-2.3 compliance — not optional).
- Purchase flow routed through `UpgradeYourTripViewController` → `mobile-iu-bff`.

**Explicitly excluded from MVP:**
- Miles-as-payment path (`UpgradeYourTripViewModel_MilesAsFormOfPayment`, `MilesOfferShelfViewModel`) — test cash willingness to pay first.
- Multi-segment offer selection — one segment only.
- Benefit callouts (`BenefitsViewModel`, `BenefitItemViewModel`, `CalloutsListViewModel`) — test raw conversion before adding persuasion elements.
- Promo callouts (`InstantUpsellCallout`) — exclude to keep the conversion signal clean.
- `InstantUpsellFullTeaserMilesHeaderViewModel` — miles teaser adds complexity before miles path is validated.

**Success metric:** Upgrade conversion rate for passengers shown the MVP offer vs. control (no offer shown). Target: ≥ X% conversion to justify full feature expansion (target defined before MVP ships).

**What MVP proves or disproves:** Whether there is baseline willingness to pay for post-booking cabin upgrades. Everything else is optimization.

---

## ❌ VIOLATION Example

### Proposed "MVP"

> "Our MVP for instant upsell will include: all available cabin types and tiers, all flight segments in the itinerary, miles-as-payment and cash-as-payment, fare rules modal, benefit callouts with BenefitItemViewModel and CalloutsListViewModel, promo callout cards via InstantUpsellCallout, and the full miles teaser header. We'll ship this as our MVP and then iterate."

### Why This Violates PRD-5.1

This is not an MVP — it is a full feature set with the word "MVP" applied as a label. PRD-5.1 is violated on three grounds:

1. **No critical assumption identified.** The proposal does not name what assumption the MVP tests. Shipping everything simultaneously means no signal is isolated. If conversion is low, there is no way to determine whether the problem is the price, the payment method, the number of segments displayed, or the callout design.

2. **Scope far exceeds the minimum required to test.** Miles-as-payment, multi-segment selection, benefit callouts, and promo cards each represent distinct product hypotheses. Bundling them into a first release creates complexity debt in `instantupsell-ios` and contaminates the conversion measurement signal.

3. **Compliance components (fare rules, T&C) are conflated with optional features.** `FareRulesView` and `TermsAndConditionsFooterView` are not optional in any scope — they are BUS-2.3 compliance requirements. An "MVP" that debates whether to include them has misunderstood the difference between minimum viable and minimum compliant.

**Correct path:** Ship the single-segment cash-only offer. Measure. Then add miles payment, multi-segment, and persuasion elements incrementally, each with its own hypothesis and measurement plan.

# Journey: Instant Upsell — Cabin Upgrade Post-Booking
# Avatar: avatar-ancillary-upsell | Law: PRD-2.5 Discovery Stage-Gate Law
# Grounded in: instantupsell-ios analysis — 175 source files, InstantUpsell framework
# Source modules: PricingCoordinator, SegmentOfferSelectionCoordinator, InstantUpsellOffersViewModel, MilesOfferShelfViewModel

```yaml
journey:
  id: journey-instant-upsell
  name: Instant Upsell — Cabin Upgrade Post-Booking
  persona: Economy passenger offered a cabin upgrade 48 hours before departure
  laws: [PRD-2.5, PRD-1.2, BUS-2.3, BUS-3.6, BUS-7.1]
  source_evidence: instantupsell-ios source analysis (2026-04-30)
```

---

## Journey Overview

An economy passenger receives a push notification or in-app message 48 hours before departure offering a cabin upgrade. They tap through, evaluate the offer across one or more flight segments, choose between miles and cash payment, review fare rules and terms, and confirm the purchase. The entire flow must be transparent on pricing, compliant with DOT refund disclosure, and produce an audit trail for the transaction.

---

## Step 1 — Offer Entry Point

**Trigger:** Push notification or in-app banner delivered by `mobile-offers-bff`. The offer payload includes eligible segments, available cabin tiers, pricing (cash and miles), and offer expiry.

**Source module:** `mobile-offers-bff` (upstream — consumed, not owned by this avatar)

**PRD-2.5 note:** The offer must exist before the flow begins. Delivering an offer to a passenger who is not eligible — or whose eligibility has expired — is a discovery failure, not a presentation failure. Eligibility is owned by `mobile-offers-bff` / `marketing-personalization`; this avatar receives a validated offer payload.

**UX requirement:** The entry point must not overstate the offer (e.g., "You've been selected for a free upgrade") when a purchase is required. BUS-2.3: misleading offer framing before a purchase is a consumer protection violation.

---

## Step 2 — Offer List

**Screen:** `InstantUpsellOffersView` rendered by `InstantUpsellOffersViewModel`.

**What happens:** The view loads all eligible upgrade offers for the passenger's itinerary. Each offer is scoped to a flight segment. Multi-segment itineraries show multiple offer cards. `InstantUpsellOffersViewModel` fetches the offer list from `mobile-iu-bff` and maps it to the display layer.

**BUS-3.6:** Price shown on the offer list card must be the complete price (base + taxes). If the list shows only the base price and defers taxes to a later screen, this is a violation. Passengers must not be surprised by a higher total at confirmation.

---

## Step 3 — Segment Selection

**Coordinator:** `SegmentOfferSelectionCoordinator`

**What happens:** For itineraries with multiple segments, `SegmentOfferSelectionCoordinator` manages which segment's offer is in focus and routes the passenger through per-segment offer screens. Each segment offer is independently selectable.

**Source models:** `SegmentOfferViewModel` represents an individual segment's offer. `CabinOfferViewModel` renders the cabin tier being offered; `OriginalCabinOfferViewModel` renders the current (booked) cabin for price anchoring.

**PRD-1.2 note:** The price anchoring pattern (`OriginalCabinOfferViewModel` showing current cabin, `CabinOfferViewModel` showing upgrade cabin) exists because passengers need a comparison reference to evaluate the offer. Remove the original cabin display and conversion drops — this is the same anchoring principle as the bag purchase at-airport comparison.

---

## Step 4 — Pricing Display

**Coordinator:** `PricingCoordinator`

**What happens:** `PricingCoordinator` is responsible for assembling the price breakdown for the selected offer: base upgrade price, taxes, fees, and total due. `UpsellCabinOfferLineItem` provides the line-item data model.

**BUS-3.6 (mandatory):** Tax breakdown must be displayed on this screen. Never show only a rounded total. The total must equal the sum of all displayed line items. If `PricingCoordinator` returns a total that does not match visible line items, that is a law violation, not a display bug.

**Audit note (BUS-7.1):** The price shown to the passenger at this step must be recorded in the purchase audit trail. If the price changes between this display and the confirmation screen (e.g., due to offer expiry), the passenger must be explicitly notified and must re-confirm. Silent price changes are a BUS-2.3 violation.

---

## Step 5 — Miles vs. Cash Selection

**View models:** `MilesOfferShelfViewModel`, `UpgradeYourTripViewModel_MilesAsFormOfPayment`

**What happens:** `MilesOfferShelfViewModel` surfaces the miles payment option when the passenger has sufficient AAdvantage balance. The passenger selects either miles or cash as the form of payment. Selecting miles routes to `UpgradeYourTripViewModel_MilesAsFormOfPayment`; cash routes to the standard `UpgradeYourTripViewModel` path.

**BUS-9.3:** Miles redemption must comply with AAdvantage program rules. The redemption rate and any program-specific restrictions must be accurately represented in `MilesOfferShelfViewModel`. `InstantUpsellFullTeaserMilesHeaderViewModel` renders the miles teaser header when miles are available but not yet selected.

**Important:** These are architecturally distinct payment paths. Do not share offer model data across the miles and cash paths — the pricing structures differ, and conflation causes BUS-3.6 display errors.

---

## Step 6 — Benefits Review

**View models:** `BenefitsViewModel`, `BenefitItemViewModel`, `CalloutsListViewModel`

**What happens:** After payment method selection, the passenger can review the benefits included with the upgraded cabin (e.g., extra legroom, priority boarding, meal service). `BenefitsViewModel` loads the benefit list; `BenefitItemViewModel` renders individual benefit items. `CalloutsListViewModel` renders promotional callouts (e.g., "Earn 3× miles in this cabin").

**PRD-5.1 note:** In an MVP, this step may be omitted to isolate conversion signal. In a full-featured flow, benefits review precedes fare rules so the passenger understands what they're buying before reviewing restrictions.

---

## Step 7 — Fare Rules

**View:** `FareRulesView`

**What happens:** The passenger can review the fare rules applicable to the upgraded cabin. This screen must be reachable before confirmation — not only after purchase.

**BUS-2.3 (mandatory):** Fare rules — including change and cancellation policies — must be accessible before purchase confirmation. Hiding `FareRulesView` behind a post-confirmation link is a DOT consumer protection violation. `FareRulesView` is not optional in any production scope.

---

## Step 8 — Terms & Conditions

**Views/ViewModels:** `TermsAndConditionsFooterView`, `TermsAndConditionsFooterViewModel`

**What happens:** Terms & conditions for the upgrade purchase are presented. `TermsAndConditionsFooterViewModel` drives the display logic; `TermsAndConditionsFooterView` renders the footer on the confirmation-adjacent screen.

**BUS-2.3 (mandatory):** Refund policy must be visible and acknowledged before the passenger taps the final confirm button. `AwardFooterView` renders any AAdvantage-specific terms for miles-path purchases.

---

## Step 9 — Purchase Confirmation

**Controller:** `UpgradeYourTripViewController`
**Data model:** `UpgradeYourTripIU2`
**BFF:** `mobile-iu-bff`
**Query param:** `PurchaseFlow_QueryParam`

**What happens:** The passenger taps confirm. `UpgradeYourTripViewController` assembles the purchase request using `UpgradeYourTripIU2` as the data model and `PurchaseFlow_QueryParam` to encode routing parameters. The request is submitted to `mobile-iu-bff`. On success, the passenger receives a confirmation screen with the transaction reference.

**BUS-7.1 (mandatory):** The confirmed transaction — including passenger ID, offer ID, segment, cabin, payment method, amount, and timestamp — must be written to the purchase audit trail at this step. This record is the authoritative receipt for dispute resolution and regulatory inquiry.

**BUS-3.6:** The confirmation screen must display the same itemized total shown at Step 4. If any amount differs, the purchase flow has a data integrity defect.

---

## Step 10 — Analytics & Alerts

**View model:** `UpgradeYourTripViewModel_Alerts`

**What happens:** `UpgradeYourTripViewModel_Alerts` manages post-purchase alert states: success confirmation, error states (e.g., offer expired, payment declined), and any follow-on offers. Analytics events are fired for funnel tracking: offer viewed, payment method selected, purchase confirmed, purchase failed.

**PRD-1.5 note:** These analytics events are the measurement infrastructure for evidence-based iteration. Conversion rate, drop-off by step, and payment method distribution are the primary metrics for evaluating the instant upsell flow.

---

## Law Compliance Summary

| Law | Where Applied |
|---|---|
| PRD-2.5 | Offer eligibility validated upstream before flow begins (Step 1) |
| PRD-1.2 | Price anchoring pattern addresses measured abandonment problem (Steps 3–4) |
| BUS-2.3 | Fare rules (Step 7) and T&C with refund policy (Step 8) required before confirmation |
| BUS-3.6 | Tax breakdown in pricing display (Step 4); itemized total on confirmation (Step 9) |
| BUS-7.1 | Audit trail written at purchase confirmation (Step 9) |
| BUS-9.3 | Miles redemption rate accuracy in miles payment path (Step 5) |

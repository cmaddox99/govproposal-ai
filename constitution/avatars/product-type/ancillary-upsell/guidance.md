# Guidance: Ancillary Upsell & Post-Booking Purchases

## What This Avatar Owns

This avatar governs the **transactional purchase completion layer** for post-booking and in-journey ancillary revenue. Concretely:

- **Instant Upsell (cabin upgrades):** The flow from offer presentation through purchase confirmation, including miles-as-payment and cash-payment paths. Backed by `instantupsell-ios` (175 swift files) and `mobile-iu-bff`.
- **Upgrade Bid/Auction:** The bid placement, bid management, and bid result notification flow. Passengers bid on premium cabin availability when full-price upgrade is out of reach. Backed by `auction-ios` (86 swift files).
- **Bag Purchase Post-Booking:** Adding checked bag allowance after initial booking to avoid higher airport fees. Backed by `bags-ios` (213 swift files) and `mobile-ancillary-bff`.
- **Supporting purchase UX:** Fare rules display (`FareRulesView`), terms & conditions (`TermsAndConditionsFooterView`), offer callouts (`InstantUpsellCallout`, `CalloutsListViewModel`), and price breakdown transparency.

## What This Avatar Does NOT Own

| Concern | Owner |
|---|---|
| Ancillary purchase during initial booking flow | `passenger-booking` avatar |
| Offer selection, targeting, and eligibility | `marketing-personalization` avatar |
| Offer delivery API | `mobile-offers-bff` (consumed, not owned) |
| AAdvantage account balance and miles ledger | Loyalty domain |

Do not extend this avatar to cover initial booking-time ancillaries or to drive offer targeting logic. Boundary violations create coordination failures between these three domains.

## Key Product Considerations

### Monetary Precision (BUS-3.6)
Every price displayed in this avatar — upgrade cash price, bag fee, bid floor/ceiling, tax — must use exact decimal precision. Never round or omit taxes. Show tax breakdown before the purchase confirmation step. This applies to `CabinOfferViewModel`, `OriginalCabinOfferViewModel`, and the bag pricing surface in `bags-ios`.

### DOT Consumer Protection (BUS-2.3)
Payment flows must surface the refund policy (and eligibility window) **before** the passenger confirms purchase. This is a federal requirement, not a UX preference. For bid/auction: refund policy on losing bids must be shown at bid submission, not only at result notification.

### Miles vs. Cash Payment Paths
These are architecturally distinct. `UpgradeYourTripViewModel_MilesAsFormOfPayment` handles the miles redemption path; `UpgradeYourTripViewModel` handles the cash path. Do not conflate offer model data across paths. `MilesOfferShelfViewModel` mediates the selection surface.

### BFF Architecture
- `mobile-iu-bff` — instant upsell purchase completion
- `mobile-ancillary-bff` — bags and general ancillary purchase
- `mobile-offers-bff` — offer payload delivery (upstream, read-only from this avatar's perspective)

Offer data flows in from `mobile-offers-bff`; purchase calls go out to `mobile-iu-bff` or `mobile-ancillary-bff` depending on ancillary type.

## Laws in Force

PRD-1.2 (problem-first), PRD-1.5 (evidence-based), PRD-2.5 (stage-gate), PRD-5.1 (MVP discipline), PRD-6.2 (retention before expansion), BUS-1.1, BUS-2.3 (DOT payments), BUS-3.6 (monetary precision), BUS-4.3 (payment data), BUS-7.1 (audit trail), BUS-9.3 (AAdvantage rules).

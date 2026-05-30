# PRD-3.1 — Roadmap Planning (AAdvantage Loyalty)

## Prioritization Framework

| Factor | Weight | How to Measure |
|--------|--------|----------------|
| Member lifetime value impact | 40% | Delta LTV for targeted cohort in pilot |
| Retention signal | 30% | Correlation with 90-day churn reduction |
| Build complexity | 20% | ENG-11.1 PROPOSAL.md scope estimate |
| Regulatory/compliance | 10% | ENG-6.4 / BUS-4.3 review gate required |

## Roadmap Input: BFF Fleet Health

The loyalty roadmap must account for technical debt in the BFF layer. Two loyalty BFFs are Yellow-tier (5.3 and 5.6/10). Features that increase load on these services carry hidden delivery risk.

**Rules for roadmap planning:**
1. Any feature touching `aa-ct-fly-mobile-loyalty-bff` must assess current 5.3/10 baseline — is the target service stable enough to add behavior?
2. New redemption flows require `aa-ct-mobile-booking-bff` (7.4/10 ✅) — safe to extend
3. Partner integration features (hotel/car earning) route through `mobile-aadvantage-bff` (5.6/10) — moderate confidence

## Roadmap Anti-Pattern: Feature Stacking on Yellow-Tier BFFs

```
❌ Add points-at-checkout to loyalty-bff (5.3/10)
   → Same service that has no deep-dive report and unconfirmed bugs

✅ Add points-at-checkout to booking-bff (7.4/10 — known healthy)
   + simultaneously fund loyalty-bff quality improvement track
```

> Full roadmap template and OKR framework in `PRD-3.1-roadmap-detail.md`.

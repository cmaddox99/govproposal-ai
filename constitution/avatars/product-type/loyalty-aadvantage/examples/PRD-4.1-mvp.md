# PRD-4.1 — MVP & Product-Market Fit (AAdvantage Loyalty)

## MVP Principles for Loyalty Features

1. **One cohort, one hypothesis.** Select a member segment narrow enough to test cleanly (e.g., PLT members with < 2 redemptions in 12 months).
2. **Instrument before you launch.** Every MVP must have PRD-5.1 metrics in place before member exposure.
3. **ENG-11.1 gate applies.** PROPOSAL.md required before any BFF changes that support the MVP.

## Loyalty-Specific MVP Validation

| Feature Type | Minimum Validation | Go/No-Go Signal |
|-------------|-------------------|-----------------|
| New redemption category | 200-member cohort, 30-day pilot | Redemption rate ≥ 5% of eligible actions |
| Elite benefit change | 50-member cohort (EXP only), 14-day pilot | NPS delta ≥ +3 points |
| Partner integration | Beta with 1 partner, 500 members | Earning event success rate ≥ 98% |
| Points display in booking | A/B test 10% traffic | Booking conversion delta ≠ 0 (p < 0.05) |

## BFF Layer Constraint for MVPs

MVP features require BFF support. Before committing to an MVP timeline:
- Check target BFF quality score — Red/Yellow tier services add unpredictable delivery risk
- A BFF with confirmed bugs (e.g., currency precision in `mobile-change-bff`) is not a safe MVP foundation until the bug is resolved

> Full MVP validation framework in `PRD-4.1-mvp-detail.md`.

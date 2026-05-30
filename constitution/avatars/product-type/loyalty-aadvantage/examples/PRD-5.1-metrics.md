# PRD-5.1 — Metrics & Success Definition (AAdvantage Loyalty)

## North Star Metrics

| Metric | Target | Frequency |
|--------|--------|-----------|
| Member Lifetime Value (LTV) | Cohort trend ↑ YoY | Quarterly |
| 90-day active rate (earned or redeemed) | ≥ 60% of enrolled | Monthly |
| Redemption rate (points issued vs redeemed) | ≥ 40% within 12 months | Monthly |
| Elite tier achievement rate | Track per threshold | Monthly |
| 6-month churn rate (no activity) | ≤ 8% of active base | Monthly |

## Feature-Level Success Criteria

Every loyalty feature shipped requires these metrics instrumented **before** member exposure:

```
Earning feature: earning_event_count, earning_failure_rate, avg_points_per_transaction
Redemption feature: redemption_start_rate, redemption_completion_rate, abandonment_step
Elite feature: tier_achievement_rate, threshold_gap_distribution, downgrade_rate
Retention campaign: open_rate, click_rate, reactivation_rate (90-day)
```

## BFF Quality → Metrics Reliability

Analytics data quality depends on BFF implementation quality. Confirmed bugs in the fleet directly compromise metrics:

| Bug | Metric Corrupted |
|-----|-----------------|
| `ConfirmationAnalyticsBuilder` pass-by-value (mobile-iu-bff) | Booking confirmation revenue metrics silently lost |
| `ReviewPayAnalyticsBuilder` cabinType always null | Cabin class breakdowns permanently missing in analytics |
| `ReviewPayAnalyticsBuilder` setPnrInfo 3× duplicate | PNR data overwritten — itinerary analytics unreliable |

> **Fix these bugs before trusting any booking-flow loyalty metrics.**

> Full KPI definitions and dashboard template in `PRD-5.1-metrics-detail.md`.

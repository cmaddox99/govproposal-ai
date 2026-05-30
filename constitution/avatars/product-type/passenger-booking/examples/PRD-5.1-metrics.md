# PRD-5.1: Metrics & Success Definition — Passenger Booking

**Law Reference:** [PRD-5.1](../../../../laws/product/metrics.md)
**Avatar:** passenger-booking
**Status:** Active — all baselines confirmed against booking funnel telemetry

---

## Tier 1: Customer Outcome Metrics

| Metric | Definition | Baseline | 90-Day Target | Source |
|--------|------------|----------|---------------|--------|
| Booking conversion rate | % of search sessions completing PNR confirmation | 34% | 38% | Booking funnel events |
| Payment success rate | % of payment submissions succeeding on first attempt | 89% | 93% | Payment gateway events |
| Fare acceptance rate | % of fare display views proceeding to seat selection | 61% | 67% | FareMapSearchViewModel events |
| Time to PNR (median) | Median seconds from search submit to PNR confirm | 310s | 240s | BFF trace spans |
| DOT refund SLA compliance | % of refunds processed within 7 business days (credit card) | 97.2% | 100% | Refund audit log |

---

## Tier 2: Operational Efficiency Metrics

| Metric | Definition | Baseline | 90-Day Target | Source |
|--------|------------|----------|---------------|--------|
| Search BFF p95 latency | mobile-airfare-search-bff 95th percentile | 1850ms | ≤1400ms | APM / OpenTelemetry |
| Booking BFF p95 latency | aa-ct-mobile-booking-bff 95th percentile | 2200ms | ≤1600ms | APM / OpenTelemetry |
| Seat availability cache hit rate | % of seat requests served from cache | 63% | ≥80% | BFF cache metrics |
| PNR creation failure rate | % of booking attempts failing at PNR write | 1.8% | ≤0.8% | VPNRController error events |

---

## Tier 3: Compliance & Risk Metrics

| Metric | Definition | Target | Regulatory ref |
|--------|------------|--------|----------------|
| PCI-DSS incident rate | Card data exposure incidents per quarter | 0 | PCI DSS v4.0 Req 12.10 |
| PAN in logs (detected) | Occurrences of PAN patterns in application logs | 0 | PCI DSS v4.0 Req 3.3 |
| DOT denied-boarding compensation timeliness | % compensated within DOT FAR 250 deadlines | 100% | DOT 14 CFR Part 250 |
| GDPR erasure SLA compliance | % of erasure requests fulfilled within 30 days | 100% | GDPR Art. 17 |

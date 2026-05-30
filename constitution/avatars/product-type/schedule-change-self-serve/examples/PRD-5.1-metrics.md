# PRD-5.1: Metrics & Success Definition — Schedule Change Self-Serve

**Law Reference:** [PRD-5.1: Metrics & Success Definition](../../../../laws/product/metrics.md)  
**Avatar:** schedule-change-self-serve  
**Status:** Experimental — all baselines are hypotheses until telemetry is instrumented

---

## Metrics Framework

Three tiers covering customer outcome, operational efficiency, and risk/compliance.
All values are experimental until replaced by instrumented telemetry in Sprint 1.

---

## Tier 1: Customer Outcome Metrics

| Metric | Definition | Experimental Baseline | 90-Day Target | Dashboard |
|--------|------------|----------------------|---------------|-----------|
| Self-serve change success rate | % of attempted changes completing without agent assistance | 78% | 88% | TBD — BFF events |
| Agent escalation rate (eligible) | % of eligible change attempts that result in an agent call | 20% | 10% | TBD — call center + BFF join |
| Ineligibility reason code clarity score | Passenger self-report 1-5: "Did you understand why your change was blocked?" | 2.8/5 | ≥4.0/5 | In-app survey |
| Time from eligibility check to confirmation | Wall-clock seconds, 50th percentile | 45s | 25s | BFF trace |
| Post-change confirmation delivery | % receiving email or push within 60 seconds | 88% (est.) | 98% | Notification service |

---

## Tier 2: Operational Efficiency Metrics

| Metric | Definition | Experimental Baseline | 90-Day Target | Dashboard |
|--------|------------|----------------------|---------------|-----------|
| BFF p95 latency | 95th percentile end-to-end BFF response time | 3200ms | ≤1800ms | APM / OpenTelemetry |
| Eligibility service cache hit rate | % of eligibility calls served from cache | 55% | ≥80% | Eligibility service metrics |
| Manual override requests per 1k changes | Agent override frequency normalised to traffic | 18 | ≤8 | Agent console event stream |
| Seat assignment conflict rate | % of completed changes with subsequent seat dispute | 6% (est.) | ≤2% | Reservation service events |
| BFF retry rate | % of downstream calls requiring at least one retry | 8% (est.) | ≤3% | BFF retry counter |

---

## Tier 3: Risk and Compliance Metrics

| Metric | Definition | Experimental Baseline | 90-Day Target | Dashboard |
|--------|------------|----------------------|---------------|-----------|
| Audit trail completeness | % of change requests with full eligibility + outcome record | 82% | ≥99% | Audit service |
| Agent override records with reason field | % of overrides that include a text reason and authority level | 40% (est.) | ≥99% | Agent console audit log |
| Failed compliance events per 10k changes | Audit events flagged for missing or invalid data | 12 | ≤2 | Compliance dashboard |
| PII data retention compliance | % of change-request payloads purged within policy window | Unknown | 100% | Data governance tooling |

---

## Instrumentation Plan

**Sprint 1 priorities:**

1. Add OpenTelemetry spans to BFF (eligibility call, seat query, reservation write)
2. Emit structured change outcome events from BFF (success, ineligible, error, override)
3. Instrument eligibility service cache hit/miss counter
4. Add audit event on every eligibility decision and agent override

**Validation cadence:**

- Week 1-2: Instrument and deploy to 100% of traffic (read-only)
- Week 3-4: Collect data, compare to experimental baselines
- Week 5+: Update baselines with measured values and adjust 90-day targets

**Baseline Replacement Protocol:**

When replacing an experimental baseline, document:

```
Metric: [name]
Previous baseline: [experimental value] (est.)
Measured value: [actual] (from: [time period, sample size])
Updated target: [revised 90-day target]
Updated by: [team member]
Date: [date]
```

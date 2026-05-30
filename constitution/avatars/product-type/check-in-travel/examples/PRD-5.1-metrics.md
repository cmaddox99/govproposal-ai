# PRD-5.1: Metrics & Success Definition — Check-In & Boarding

> **Law:** PRD-5.1 Metrics Law  
> **Detail file:** `PRD-5.1-metrics-detail.md` (Tier 2+3 KPIs, dashboard structure, 2027 targets)

---

## Three Measurement Tiers

| Tier | What it measures | Review cadence |
|------|-----------------|----------------|
| **Tier 1 — Passenger Experience** | Satisfaction, mobile adoption, reliability | Daily |
| **Tier 2 — Operational Efficiency** | Boarding time, gate throughput, labour hours | Daily |
| **Tier 3 — Business Impact** | On-time performance, cost, retention | Weekly |

---

## Tier 1: Passenger Experience KPIs

| Metric | Baseline | 2026 Target | Source |
|--------|----------|-------------|--------|
| Mobile adoption | 52% | 72% | App analytics |
| Mobile reliability (no failure) | 92% | 99.9% | Gate scanner logs |
| Kiosk completion rate | 60% | 75% | Kiosk telemetry |
| Accessibility processing time | 12 min | 6 min | Check-in system |
| Digital traveller NPS | 7/10 | 9/10 | In-app survey |
| Supported traveller NPS | 6/10 | 8.5/10 | Post-trip survey |
| Boarding confusion incidents | 12% | <5% | Gate incident log |

---

## Tier 2: Operational Efficiency KPIs

| Metric | Baseline | 2026 Target | Source |
|--------|----------|-------------|--------|
| Average boarding time | 40 min | 35 min | Gate scanner timestamps |
| Manual lookups per flight | 40 | 6 | Gate dashboard |
| Gate agent satisfaction | 5/10 | 8/10 | Monthly survey |
| Oversell discovery lead time | 0 min (at gate) | 30 min pre-departure | Predictive model |
| Peak-hour counter wait | 30-45 min | 15 min | Queue telemetry |
| Labour hours per 1K pax | 6.8 hr | 5.2 hr | Ops system |

---

## Tier 3: Business Impact KPIs

| Metric | Baseline | 2026 Target | Value |
|--------|----------|-------------|-------|
| On-time performance | 78% | 82% | +$6M/year per point |
| System availability | 99.2% | 99.9% | Cascading delay prevention |
| Gate-level recovery incidents | 112K/day | <10K/day | $11.2M labour savings |
| Missed flights (check-in delays) | 0.8% | <0.1% | $4.8M rebooking cost avoided |

---

## Measurement Anti-Patterns

- **Don't measure inputs as outcomes.** "Feature deployed" is not a metric. "Mobile failure rate" is.
- **Don't report weekly averages for daily-volatile metrics.** Boarding time must be tracked per flight, not averaged into weeks that hide peak-hour failures.
- **Don't track a metric without an owner.** Each KPI has one named team responsible for it — no shared ownership.


---
laws: [PRD-5.1]
avatar: [gate-management]
title: Metrics and Success Definition — Gate Management Platform
---

# PRD-5.1: Metrics and Success Definition

**Law Reference:** [PRD-5.1: Metrics & Success Definition](../../../../laws/product/metrics.md)
**Avatar:** gate-management
**Status:** Experimental — all baselines are hypotheses until telemetry is instrumented.
Replace every "(est.)" value with a measured value at Sprint 1 instrumentation.

---

## Metrics Framework

Four tiers: customer / operational outcome, system performance, safety and compliance,
and per-domain leading indicators. All values experimental until replaced by
instrumented production telemetry.

---

## Tier 1: Customer & Operational Outcome Metrics

| Metric | Definition | Experimental Baseline | 90-Day Target | Instrument |
|--------|-----------|----------------------|---------------|------------|
| Agent wrong-decision rate (stale display) | # of confirmed decisions made on stale GIDS data per 1,000 departures | Unknown — establish at Phase 1 | 0 confirmed incidents | Gate agent debrief log |
| Biometric boarding throughput | Passengers processed per minute via biometric path vs. manual scan | Unknown (est. 22 pax/min manual) | ≥25 pax/min biometric | Boarding API stats endpoint |
| False non-match rate | % of biometric boarding attempts that return a non-match for a correctly-enrolled passenger | Unknown | ≤1.5% | Biometrics dashboard |
| Carry-on gate-check rate | % of screened bags requiring gate check | Unknown (est. 8–12% at high-volume gates) | Establish baseline; 90-day target set post-measurement | Carry-on audit log |
| Agent decision time (carry-on) | Seconds from bag scan to agent compliance decision | Unknown (est. 15–20s) | ≤10s | Carry-on audit log timestamps |
| Alert-to-action latency (Connect Me) | Seconds from AOC event fire to agent Teams read + task acknowledged | Unknown (est. 60–120s) | ≤30s (p95) | Teams delivery receipt + AOC event timestamp |

---

## Tier 2: System Performance Metrics

| Metric | Definition | Experimental Baseline | 90-Day Target | Instrument |
|--------|-----------|----------------------|---------------|------------|
| DSS display staleness | ms from AOC event to screen render (per display type) | Unknown | ≤5,000ms (GIDS); ≤10,000ms (FIDS) | Azure App Insights: `dss.display.staleness_ms` |
| DSS event pipeline lag | ms from AOC event to DisplayHub consumer receipt | Unknown | ≤2,000ms | Service Bus consumer metric |
| Biometrics boarding API p95 latency | 95th percentile response time, face capture to match result | Unknown | ≤3,000ms | Azure App Insights / Biometrics dashboard |
| Bag matrix service p95 latency | 95th percentile response time, scan to compliance decision | Unknown | ≤2,000ms | Apigee proxy metrics |
| Policy propagation time | Seconds from admin bag matrix rule change to all gates running new version | Unknown | ≤60s | Rule version log per gate |
| Connect Me Teams delivery rate | % of operational alerts delivered to agent device within 30s | Unknown (est. 85%) | ≥99% | Teams delivery receipt |
| Unread operational alert rate | % of Connect Me alerts unread within 5 minutes of delivery | Unknown | ≤5% | CME subscription service metrics |

---

## Tier 3: Safety and Compliance Metrics

| Metric | Definition | Experimental Baseline | 90-Day Target | Instrument |
|--------|-----------|----------------------|---------------|------------|
| Tarmac timer visibility compliance | % of tarmac-timer-applicable gates where timer is always in primary view (not sub-screen) | Unknown | 100% | Gate UI audit |
| Biometric opt-out availability | % of biometric-enabled gates where opt-out path is visible without agent intervention | Unknown | 100% | Gate observation checklist |
| Carry-on override supervisor auth rate | % of carry-on agent overrides with documented supervisor authorization | Unknown (est. 40%) | ≥99% | Carry-on audit log |
| Carry-on rule version log coverage | % of compliance decisions with rule version logged | Unknown | 100% | Carry-on audit log |
| Biometric audit log completeness | % of boarding events (match / non-match / opt-out) with full required fields logged | Unknown | ≥99.9% | Biometrics audit log |
| Biometric PII in operational logs | # of operational log entries containing raw biometric templates or match scores | Unknown (est. 0) | 0 | Log scrub tooling (ENG-6.7) |
| Gate context completeness | % of audit log entries including all four required fields (flight_id, gate_id, agent_id, timestamp) | Unknown | 100% | Audit log schema validator |

---

## Tier 4: Per-Domain Leading Indicators

### DSS
| Indicator | Signal | Alert Threshold |
|-----------|--------|----------------|
| Event pipeline queue depth | Messages accumulating in Service Bus → impending staleness spike | >50 messages (baseline to be set at Phase 1) |
| DisplayHub consumer lag | Consumer falling behind producer rate | >3s lag sustained >1 minute |
| GIDS render error rate | Frontend unable to render incoming flight event | >0.5% of render attempts |

### Biometrics
| Indicator | Signal | Alert Threshold |
|-----------|--------|----------------|
| Non-match rate (rolling 15-min) | Camera or enrollment issue developing | >3% in any 15-minute window |
| Opt-out rate spike | Opt-out path confusion or system UX regression | >10% above rolling 7-day average |
| Boarding API error rate | Service degradation | >1% of requests returning non-200 |

### Carry-On
| Indicator | Signal | Alert Threshold |
|-----------|--------|----------------|
| Override rate (rolling 1-hr) | Policy gap or enforcement confusion | >15% of decisions in any 1-hour window |
| Policy version mismatch count | Gates running different versions simultaneously | >0 after 60s from a rule change |

### Connect Me
| Indicator | Signal | Alert Threshold |
|-----------|--------|----------------|
| FLC task completion latency | FLC not acting on load tasks within window | >10 min from task delivery to completion |
| Teams message delivery failure rate | Delivery channel degradation | >1% of messages undelivered after 30s |

---

## Instrumentation Plan

**Sprint 1 priorities (all domains):**

1. Add `dss.display.staleness_ms` custom metric to Azure App Insights per display surface
2. Emit structured boarding outcome events from Biometrics boarding API (match / non-match / opt-out + reason code)
3. Add rule version field to every carry-on compliance decision log entry
4. Add Teams delivery receipt correlation to Connect Me event pipeline
5. Add gate context validation (flight_id, gate_id, agent_id, timestamp) to all audit log schemas

**Baseline replacement protocol:**

When replacing an experimental baseline, document:

```
Metric: [name]
Previous baseline: [experimental value] (est.)
Measured value: [actual] (from: [time period, sample size])
Updated target: [revised 90-day target]
Updated by: [team member]
Date: [date]
```

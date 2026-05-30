# Worksheet 01: Metrics Collection - Schedule Change Self-Serve

**Purpose:** Capture current KPI definitions, sources, and baseline confidence for Schedule Change.  
**Law Anchor:** PRD-5.1  
**Status:** Draft (experimental baselines pre-filled, replace with measured telemetry)

---

## Baseline Derivation Methods (PO Explainability)

The experimental KPI baselines were derived using a triangulated method and are now tagged for explainability.

1. Architecture-derived throughput assumptions from code evidence (service chain depth, fallback paths, and error handling points) captured in W3.
2. Domain-rule complexity weighting from eligibility and remarks rule families captured in W4.
3. Directional external benchmark context (Delta/Southwest/IATA/JD Power) used only to calibrate ambition, not to set internal truth.
4. Stakeholder operational heuristics for override/audit where telemetry is not yet instrumented.

Formula used for experimental baseline derivation:

$$
	ext{Experimental Baseline} = w_1(\text{Code Evidence}) + w_2(\text{Domain Rule Complexity}) + w_3(\text{Directional Benchmark}) + w_4(\text{Stakeholder Signal})
$$

Current weighting policy (pre-telemetry):
- Code evidence: high influence
- Domain-rule complexity: medium-high influence
- Directional benchmark: medium influence
- Stakeholder signal: medium influence

Rebaseline policy remains unchanged: numeric KPI values are locked until telemetry and workshop validation complete.

---

## Current KPI Inventory

| Metric | Tier | Current (Experimental) | 90-Day Target | Source Tag | Confidence | Citation / Evidence |
|-------|------|-------------------------|---------------|------------|------------|---------------------|
| Self-serve change success rate | Customer | 78% | 88% | code-evidenced + public-benchmark | Medium | Service path and fallback complexity from W3 plus directional market benchmark context; still requires telemetry confirmation |
| Agent escalation rate | Customer | 20% | 10% | stakeholder-reported + code-evidenced | Medium-Low | Operational estimate informed by rule/exception complexity seen in W4; pending call-center joined telemetry |
| Reason-code clarity score | Customer | 2.8/5 | >=4.0/5 | code-evidenced + hypothesis-only | Medium-Low | Eligibility reason structures exist in code; customer-facing clarity score still requires survey instrumentation |
| End-to-end confirmation time | Customer | 45s | 25s | code-evidenced + public-benchmark | Medium | Multi-service orchestration depth and known failure paths from W3 calibrated with directional digital UX benchmark expectations |
| BFF p95 latency | Operational | 3200ms | <=1800ms | code-evidenced | Medium | Derived from orchestration complexity and resilience/fallback profile in W3; requires OTel to confirm numeric accuracy |
| Manual overrides per 1k | Operational | 18 | <=8 | stakeholder-reported + code-evidenced | Medium-Low | Stakeholder baseline with added evidence from remarks/eligibility stop-rules and exception paths in W4 |
| Audit trail completeness | Risk | 82% | >=99% | stakeholder-reported + code-evidenced | Medium-Low | Stakeholder estimate strengthened by identified history/update touchpoints and logging patterns in W3; dashboard instrumentation pending |

---

## Public Domain Field Study (Directional)

These references are for directional benchmarking only and do not replace internal telemetry.

| Comparator / Source | Relevant Finding | Metric Implication | Source Tag | Citation (Accessed 2026-03-11) |
|---------------------|------------------|--------------------|------------|--------------------------------|
| Southwest same-day change page | Same-day changes and standby are offered via app/mobile web with explicit step flow and timing constraints | Confirms competitive expectation for mobile-first self-serve flow clarity and fast path execution | public-benchmark | https://www.southwest.com/airfare-types-benefits/sameday-standby-change/ |
| Delta same-day change page | Same-day changes are available online during check-in or in Fly Delta app; standby keeps original flight confirmed until seat clears | Supports roadmap emphasis on low-friction self-serve plus safe fallback behavior during re-accommodation | public-benchmark | https://www.delta.com/us/en/change-cancel/same-day-flight-change |
| IATA Global Passenger Survey 2025 | 78% want one app combining key travel artifacts; passengers value speed, convenience, and digital tools | Reinforces product priority on consolidated digital self-serve journey and reduced channel switching | public-benchmark | https://www.iata.org/en/publications/store/global-passenger-survey/ |
| JD Power 2025 NA Airline Satisfaction Study | Digital tools are one of seven core dimensions; fewer than 10% report problems, and issues materially reduce trust | Supports use of reliability + digital-experience metrics as primary success indicators | public-benchmark | https://www.jdpower.com/business/press-releases/2025-north-america-airline-satisfaction-study |
| IATA March 2025 Demand Release | North America showed demand softness while global demand still grew, increasing pressure to protect customer experience | Supports focus on reducing avoidable escalations and friction during schedule change events | public-benchmark | https://www.iata.org/en/pressroom/2025-releases/2025-04-30-01/ |

### Rebaseline Decision (2026-03-11)

- Numeric KPI values remain unchanged after this field-study pass.
- Public benchmarks are directional and improve prioritization confidence, but do not replace internal telemetry.
- Numeric updates will occur after code evidence plus internal field validation are completed.

### What Changed After Code Analysis

1. Source-tag quality improved from mostly `hypothesis-only` to mixed evidence tags where code support exists.
2. Confidence moved from Low to Medium/Medium-Low for several rows because service-call, rule, and reliability evidence now exists.
3. Numeric baseline values did not change in this cycle.

---

## Measurement Gaps

| Gap | Why It Matters | Owner | Fix Approach |
|-----|----------------|-------|--------------|
| No authoritative self-serve funnel metrics | Cannot separate success vs abandonment root causes | Product + Analytics | Instrument BFF outcome events |
| No reason-code clarity measurement | Cannot validate Slice 1 impact | Product + UX | Add post-decision micro-survey |
| No stable audit completeness dashboard | Compliance risk hidden until audits | Compliance + Engineering | Emit immutable decision + override events |

---

## Instrumentation Plan (Sprint 1)

1. Add OpenTelemetry spans in BFF for eligibility, reservation, seat assignment, and notification.
2. Emit structured events: `eligible`, `ineligible`, `abandoned`, `escalated`, `rebooked`.
3. Add reason-code distribution dashboard with top blockers and trendline.
4. Add compliance dashboard for audit completeness and missing fields.

---

## Stakeholder Validation Checklist

- [ ] Product Owner validated target outcomes
- [ ] Analytics validated metric definitions and calculation formulas
- [ ] Engineering validated event and span feasibility
- [ ] Compliance validated audit metric requirements
- [x] Initial public-domain directional benchmark pass completed with citations

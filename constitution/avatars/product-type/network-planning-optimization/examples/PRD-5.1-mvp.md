---
law: PRD-5.1
avatar: avatar-product-network-planning-optimization
title: "MVP: Unified Route Analysis Workspace (2-Analyst Pilot, 10 Routes)"
---

# PRD-5.1 MVP Law — Network Planning Optimization

## Law Summary

The smallest experiment that validates the time-to-insight hypothesis is the correct first investment. Prove the concept on 10 routes before building for 350+.

---

## ✅ COMPLIANT Example — MVP Canvas

### Hypothesis

> A unified route analysis workspace that pre-integrates data from the 7 source systems (PROS, SABRE, DOT T-100, OAG, weather API, internal cost model, CompStat) will reduce route assessment time from 6.4 hours to ≤ 1 hour for the 2 pilot analysts.

### Riskiest Assumption

Data from all 7 source systems can be reliably integrated with sufficient freshness (< 24 hours stale) for 10 target routes. If any source system has API limitations, brittle data formats, or access restrictions, the integration will fail on a subset of routes.

### MVP Scope

**In scope:**
- 2 analysts: Sr. Network Analyst (domestic routes) and Sr. Network Analyst (Latin America routes)
- 10 routes: 7 domestic (high-volume), 3 Latin America (analyst-selected)
- Data integrated: PROS yield data, DOT T-100 public data, OAG schedule data, internal cost model (read-only export), CompStat competitor data
- Workspace: Databricks notebook environment with pre-assembled data tables per route
- Update frequency: daily refresh (not real-time)

**Out of scope:**
- All 350+ routes (deferred to Phase 2 after pilot validation)
- Automated route recommendations
- International routes (regulatory complexity: EU/LATAM traffic rights)
- Real-time market data feeds (deferred)
- Self-service access for non-analyst stakeholders (deferred)
- SABRE reservation data integration (access provisioning timeline unknown; deferred)

### Acceptance Criteria

```gherkin
Scenario: Network Analyst performs route assessment using unified workspace
  Given I am assessing route DFW-MEX for Q2 2026 schedule review
  And the workspace has integrated data from PROS, DOT T-100, OAG, cost model, and CompStat
  When I open the DFW-MEX route workspace
  Then all relevant data is pre-assembled in a single Databricks notebook
  And no manual data export from external systems is required
  And I can complete the full assessment in ≤ 60 minutes
  And the data is no more than 24 hours stale
```

### Success Criteria (6-Week Pilot)

| Metric | Baseline | Target | Fail Gate |
|--------|----------|--------|-----------|
| Route assessment time (pilot analysts) | 6.4 hours | ≤ 1 hour | > 2 hours → investigate data integration gaps |
| Data freshness | Variable (often 1–2 weeks stale) | ≤ 24 hours | > 48 hours on any source → fix pipeline before proceeding |
| Analyst satisfaction with workspace | N/A | ≥ 4.0/5.0 | < 3.5 → investigate usability |
| % of routes where all 5 sources fully integrated | N/A | ≥ 90% | < 80% → identify which source is the blocker |

### Expansion Gate

Scale to all 350+ routes and additional analysts begins only after: 6-week pilot shows ≤ 1-hour assessment time on ≥ 9 of 10 pilot routes AND analyst satisfaction ≥ 4.0/5.0.

---

## ❌ VIOLATION Example

> "Build the unified route analytics platform for all 350+ routes, with real-time data feeds, automated recommendations, and self-service access for planners and executives."

**Why this violates PRD-5.1:**
- 350+ routes before validating data integration on 10.
- Real-time data feeds are a separate technical problem (API SLAs, cost, rate limits).
- Automated recommendations require a validated model — the workspace hypothesis hasn't been proven yet.
- Executive self-service requires data governance, access control, and documentation — deferred complexity.
- Correct approach: 2 analysts, 10 routes, 6 weeks. Prove 6.4 → 1 hour. Then scale.

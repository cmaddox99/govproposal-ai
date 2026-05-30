---
law: PRD-1.2
avatar: avatar-product-network-planning-optimization
title: "Problem-First: Route Analysis Data Fragmentation"
---

# PRD-1.2 Problem-First — Network Planning Optimization

## Law Summary

Validate the actual bottleneck before building analytics. The request ("route profitability dashboard") often describes a symptom, not the root cause.

---

## ✅ COMPLIANT Example

### Stated Request

> "Build a route profitability dashboard so network planners can make better route investment decisions."

### Research Conducted

3-week workflow observation with 4 Network Planning Analysts performing full route assessments. Time-in-motion study + system inventory.

| Finding | Value | Source |
|---------|-------|--------|
| Average time per route assessment | 6.4 hours | Time-in-motion study |
| Time spent gathering data from disconnected systems | 4.8 hours (75%) | Time-in-motion study |
| Time spent on actual analysis and modeling | 0.8 hours (12%) | Time-in-motion study |
| Number of systems accessed per route assessment | 7 (PROS, SABRE, weather API, DOT T-100, OAG, internal cost model, CompStat) | System inventory |
| % of data that is re-exported manually into Excel | 82% | Workflow observation |
| % of route assessments delayed due to data unavailability | 41% | Analyst interviews (n=4) |
| Analyst #1 pain point | "I spend all day pulling data and no time actually thinking about the route" | 4 analyst interviews |

**Root cause:** 75% of route assessment time is data gathering from 7 disconnected systems. Analysts manually export data into Excel, then apply analysis. A dashboard built on the same disconnected data infrastructure will display stale, incomplete data and will not reduce the 4.8-hour data gathering bottleneck.

### Validated Problem Statement

> Network Planning Analysts spend 75% of a route assessment (4.8 of 6.4 hours) gathering data from 7 disconnected systems. The problem is **data fragmentation**, not analytical capability. A dashboard that doesn't solve the source data integration problem will not reduce time-to-insight.

### Correct Solution Direction

Unified route analysis workspace: a single environment that pre-integrates data from the 7 source systems, so analysts start with data assembled (not data gathering). Target: reduce time-to-insight from 6.4 hours to 1 hour.

---

## ❌ VIOLATION Example

> "Network planners need better analytics. Build a route profitability dashboard with charts, KPI cards, and filters for all 350+ routes."

**Why this violates PRD-1.2:**
- No investigation into where the 6.4 hours goes.
- Dashboard built on disconnected data infrastructure replicates the data quality problems in a new UI.
- "Better analytics" assumes the problem is analysis quality, not data assembly time.
- Correct first step: time-in-motion study to confirm 75% of time is data gathering, then target the integration problem.

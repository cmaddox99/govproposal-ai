---
law: PRD-1.5
avatar: avatar-product-airport-operations
title: "Evidence-Based: Real-Time Ramp Data Feed Investment"
---

# PRD-1.5 Evidence-Based — Airport Operations

## Law Summary

Investment decisions must be backed by quantified data. Hypotheses must be stated before evidence is gathered and tested against it.

---

## ✅ COMPLIANT Example

### Decision

> Invest in a real-time ramp data feed that delivers bag count, fueling status, and catering completion to gate agent workstations within 60 seconds of event occurrence.

### Evidence Package

**Source:** 3 weeks of departure delay logs at DFW (1,847 IROP-affected departures), corroborated by 12 gate agent workflow observations.

| Evidence Point | Value | Source |
|---------------|-------|--------|
| % of departure delays where gate agent lacked real-time bag count | 23% | Delay log analysis |
| Average delay caused by agent waiting for verbal bag count confirmation | 4.2 minutes | Workflow observation |
| Delays per day attributable to ramp data latency at DFW | ~18 | Delay log analysis |
| Estimated delay cost per minute (AA internal benchmark) | $62/min | AA Operations Finance |
| Annual delay cost attributable to ramp data latency (DFW only) | ~$1.7M | Calculated |
| Agent-reported #1 information gap | "Bag count before door close" | 12 agent interviews |

### Hypothesis Tested

> If gate agents receive bag count confirmation within 60 seconds of last bag loaded (vs. current average 6-minute wait for verbal confirmation), departure delays attributable to this gap will decrease by ≥ 50%.

**Test:** 3-week A/B at DFW Terminal B (12 gates with push feed vs. 12 gates without). Measure departure delay minutes attributable to ramp data latency per gate per day.

### Decision Gate

Investment proceeds only if pilot achieves ≥ 50% reduction in ramp-data-attributable delay minutes. Estimated build cost: $340K. Break-even at DFW alone: 7 months. Network rollout ROI: $8.5M/year.

---

## ❌ VIOLATION Example

> "Real-time data is obviously better. Let's build the ramp data feed for all 350 stations and integrate with gate management, crew, and catering systems."

**Why this violates PRD-1.5:**
- No data cited: what is the current delay rate? How much of it is attributable to ramp data latency?
- "Obviously better" is not evidence.
- Network-wide investment before single-station pilot.
- No hypothesis, no test, no decision gate.

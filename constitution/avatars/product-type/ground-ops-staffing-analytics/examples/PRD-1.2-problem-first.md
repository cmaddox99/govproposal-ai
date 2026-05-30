---
law: PRD-1.2
avatar: avatar-product-ground-ops-staffing-analytics
title: "Problem-First: Peak Hour Understaffing at DFW"
---

# PRD-1.2 Problem-First — Ground Operations Staffing Analytics

## Law Summary

Validate the specific staffing problem before proposing predictive AI. The request ("predictive staffing AI") is often more solution than problem.

---

## ✅ COMPLIANT Example

### Stated Request

> "Build a predictive staffing AI so station managers can forecast ground operations headcount needs."

### Research Conducted

6-week analysis of staffing logs, actual vs. scheduled headcount by hour at DFW, delay cause codes, and station manager interviews (n=8).

| Finding | Value | Source |
|---------|-------|--------|
| Average understaffing rate at DFW (all hours) | 4.8% | Staffing log analysis |
| Average understaffing rate at DFW (07:00–09:00) | 12% | Staffing log analysis (peak hours) |
| % of ground delay incidents where understaffing cited as cause | 68% during peak | Delay cause code analysis |
| Current scheduling method | Historical patterns (prior-week same-day) | Station manager interviews |
| Hours when IROP events drive unpredictable staffing spikes | 07:00–09:00, 16:00–18:00 | Staffing log analysis |
| % of 07:00–09:00 understaffing incidents preceded by IROP night before | 74% | Staffing log + IROP log correlation |
| Station manager #1 pain point | "I don't know we're short until we're already short" | 8 interviews |

**Root cause:** DFW ground operations schedules using prior-week historical patterns that do not account for overnight IROP events. 74% of peak understaffing incidents follow an overnight IROP — a condition that is **already known** at 23:00 the night before. This is a **real-time alerting problem**, not a prediction problem.

### Validated Problem Statement

> DFW ground operations averages 12% understaffing during peak hours (07:00–09:00). 74% of these incidents follow an IROP event that was known the prior evening. Station managers are not alerted to the predicted staffing gap until the gap is already causing delays. The problem is **notification latency on known events**, not unpredictable demand. A predictive AI adds complexity without addressing this specific root cause.

### Correct Solution Direction

Real-time staffing gap alert: when overnight IROP events are confirmed (flights cancelled, significant delays, aircraft swaps), trigger a next-day staffing gap calculation and alert the station manager at 23:00 for corrective action before the morning peak.

---

## ❌ VIOLATION Example

> "Build a predictive staffing AI with ML models for all 350 AA stations that forecasts headcount 7 days out based on flight schedules, weather, and historical patterns."

**Why this violates PRD-1.2:**
- No root cause: is the problem prediction accuracy, or notification timing on already-known events?
- 350-station scope before validating the hypothesis at one station.
- ML model for 7-day forecasting adds complexity when 74% of understaffing follows yesterday's IROP — which is already known.
- Correct first step: 6-week staffing log analysis at the worst-performing station (DFW) to identify the specific root cause.

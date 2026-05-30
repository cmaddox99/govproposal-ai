---
law: PRD-5.1
avatar: avatar-product-ground-ops-staffing-analytics
title: "MVP: DFW Peak-Hour Staffing Gap Alert"
---

# PRD-5.1 MVP Law — Ground Operations Staffing Analytics

## Law Summary

The smallest experiment that validates the hypothesis is the correct first investment. Single-station pilot before multi-station platform.

---

## ✅ COMPLIANT Example — MVP Canvas

### Hypothesis

> Station managers at DFW who receive a staffing gap alert at 23:00 the night before a predicted peak-hour shortfall (triggered by overnight IROP events) will reduce understaffing incidents during 07:00–09:00 from 12% to ≤ 6%.

### Riskiest Assumption

Station managers will act on the 23:00 alert and successfully recall or reschedule additional ground operations staff in time for the 07:00 peak. If labor contract constraints prevent same-night schedule changes, the alert will have no operational impact.

### MVP Scope

**In scope:**
- Single station: DFW only
- Alert window: 23:00 the night before, for 07:00–09:00 peak only (3-hour window)
- Trigger: when overnight IROP events (cancellations, significant delays, aircraft swaps affecting DFW arrivals) total ≥ 8 flight changes
- Alert channel: SMS and email to DFW Station Manager and Assistant Station Manager
- Alert content: predicted headcount gap (# of positions understaffed), flights affected, suggested call-back list (from current schedule, sorted by overtime eligibility)

**Out of scope:**
- Automated scheduling or shift reassignment
- Multi-station deployment
- Crew assignments (separate system, separate domain)
- Predictive forecasting beyond IROP-triggered alerts
- 16:00–18:00 peak (validate 07:00–09:00 first)
- Hiring or labor force planning

### Acceptance Criteria

```gherkin
Scenario: DFW Station Manager receives IROP-triggered staffing alert
  Given ≥ 8 DFW IROP events are confirmed by 22:30
  When the staffing gap calculation runs at 23:00
  Then the DFW Station Manager receives an SMS and email alert
  And the alert shows: predicted headcount gap, flights affected, suggested callback list
  And the alert is delivered by 23:05
  And the Station Manager can confirm corrective action via reply SMS
```

### Success Criteria (8-Week Pilot at DFW)

| Metric | Baseline | Target | Fail Gate |
|--------|----------|--------|-----------|
| 07:00–09:00 understaffing rate | 12% | ≤ 6% | > 10% → investigate labor contract constraints |
| Station Manager alert acknowledgment rate | N/A | ≥ 90% | < 70% → investigate alert delivery or channel |
| Corrective action rate (callback confirmed before 06:00) | N/A | ≥ 70% | < 50% → investigate labor availability constraints |
| Alert false positive rate (alert sent, no actual gap) | N/A | ≤ 10% | > 25% → review IROP threshold trigger |

### Expansion Gate

CLT and ORD deployment begins only after: 8-week DFW pilot shows understaffing rate ≤ 6% AND corrective action rate ≥ 70%.

---

## ❌ VIOLATION Example

> "Deploy AI staffing optimization for all 350 stations with automated shift reassignment, crew callouts, and 7-day predictive forecasting."

**Why this violates PRD-5.1:**
- 350 stations before validating at one station.
- Automated shift reassignment introduces labor contract compliance risk.
- 7-day predictive forecasting is a different hypothesis from IROP-triggered same-night alerting.
- Bundling automated callouts adds union/labor relations risk that could block the entire project.
- Correct approach: manual alert at DFW for 8 weeks, prove the 12% → 6% hypothesis, then automate incrementally.

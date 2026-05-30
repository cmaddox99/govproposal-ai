---
avatar: avatar-flight-status-flifo
law_id: PRD-1.5
law_title: "Evidence-Based Decision Making"
file_type: example
---

# PRD-1.5 Evidence-Based Decision Making — Flight Status & FLIFO

## Law Summary

Product decisions must be grounded in quantified evidence — not assumptions, competitive observation, or intuition alone. Each decision point must document the evidence used, the alternative considered, and why evidence favored the chosen path.

---

## ✅ COMPLIANT Example

### Decision: Enable `AAFeatureFlightStatusSearchNextDayDeparture` for All Users

**Decision context:** The `AAFeatureFlightStatusSearchNextDayDeparture` toggle currently gates a cross-midnight search window — allowing users to search for flights departing between 00:00 and 05:59 the following calendar day. The toggle is enabled for 5% of users in a limited rollout. The product team is deciding whether to expand to 100%.

---

### Evidence Reviewed

**Search pattern analysis** (March–April 2026, n = 2.1M status searches):

- **28%** of all flight status searches are submitted between 18:00–23:59 local time.
- Of those late-evening searches, **61%** target a flight with a scheduled departure time between 00:00–06:00 the following calendar day.
- Without `AAFeatureFlightStatusSearchNextDayDeparture` enabled, these searches return zero results — because the search window defaults to the current calendar date only.
- **Zero-result rate** for late-evening status searches (toggle disabled): 38%.
- **Zero-result rate** for same cohort (toggle enabled, 5% rollout): 4% — a 34-point improvement.

**Support signal:**
- "Can't find my early morning flight" support contacts: 2,100/month.
- Estimated 80% attributable to calendar-date boundary issue based on flight time correlation.

**Session outcome comparison (A/B, 5% rollout, 14 days):**
- Toggle-enabled cohort: search completion rate 91%; status result reached 89%.
- Toggle-disabled cohort: search completion rate 74%; status result reached 71%.
- Difference: +17 points completion rate, +18 points result rate.

---

### Decision Record

**Decision:** Expand `AAFeatureFlightStatusSearchNextDayDeparture` to 100% of users.

**Evidence basis:** 28% of status searches target next-day early-morning departures. Toggle-disabled cohort shows 38% zero-result rate for this segment. 5% rollout demonstrates 17-point improvement in search completion with no regression in same-day search accuracy.

**Alternative considered:** Educate users to search the following day's date manually. Rejected: requires users to understand a system constraint they have no reason to know about; adds 2+ taps; does not address the zero-result failure.

**Guardrail metrics monitored:** Same-day search completion rate (must not decrease), BFF request volume (cross-midnight queries add ~12% load — within capacity headroom), zero-result rate.

**Rollout plan:** 100% over 7 days via feature toggle; monitor same-day search guardrail for 14 days post-launch.

---

## ❌ VIOLATION Example

### Violation Statement

> "We should add next-day departure search because our competitor has it. Let's ship it in the next sprint."

### Why This Violates PRD-1.5

1. **Competitive observation is not evidence.** The fact that a competitor has a feature says nothing about whether AA users need it, how many are affected, or whether it solves a real problem in the AA context.
2. **No quantification of impact.** There is no data on how many users fail to find early-morning flights, no zero-result analysis, no session funnel data.
3. **No alternative considered.** The decision jumps to implementation without documenting what alternatives were assessed.
4. **No success metric defined.** "Ship it" is not a measurable outcome. There is no stated hypothesis to validate.

### Compliant Reframe

Pull search funnel data: what is the zero-result rate for late-evening status searches? If >10%, quantify the affected session volume. Only then design and prioritize a solution.

---

*Grounded in flightinfo-ios analysis — AAFeatureFlightStatusSearchNextDayDeparture, FlightStatusSearchViewModel, Mobile-FLIFO-BFF.*

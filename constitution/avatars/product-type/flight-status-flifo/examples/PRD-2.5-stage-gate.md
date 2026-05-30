---
avatar: avatar-flight-status-flifo
law_id: PRD-2.5
law_title: "Discovery Stage-Gate Law"
file_type: example
---

# PRD-2.5 Discovery Stage-Gate Law — Flight Status & FLIFO

## Law Summary

Product work proceeds through sequential, gated stages: Problem Gate → Solution Gate → Build Gate → Launch Gate. No gate may be skipped. Each gate requires explicit evidence review before advancing. Committing engineering resources before the Problem Gate is cleared is a direct violation.

---

## ✅ COMPLIANT Example

### Feature: Proactive Disruption Notification — Stage-Gate Progression

**Feature summary:** Passengers who have opted in to flight alerts should receive a push notification when their flight is delayed, gate-changed, or cancelled. Currently, push notification opt-in sits at 34% and delivery reliability is 78%.

---

### Stage A — Problem Gate

**Entry criterion:** Is there a validated, quantified problem worth solving?

**Evidence:**
- Support contacts tagged "missed gate change": 4,800/month.
- Post-trip survey: 31% of disrupted passengers report they were not notified in time.
- Session data: On days with >20% disruption rate, app opens from non-opted-in users spike 190% — indicating demand for proactive information exists.
- Current push opt-in rate: 34% (iOS consent prompt shown at first launch only).
- Current notification delivery reliability: 78% (APNs delivery confirmation rate).

**Gate outcome:** Problem confirmed. Proceed to Stage B.

---

### Stage B — Solution Gate

**Entry criterion:** Is there a solution hypothesis with a testable design?

**Hypothesis:** If we improve the push notification opt-in prompt placement (show contextually after a user searches a flight, via `FlightStatusNotificationViewController`) and fix the BFF-to-APNs delivery pipeline to reach 95% reliability, opt-in rate will increase from 34% to ≥ 50% within 90 days, and disrupted passengers receiving timely notification will increase by ≥ 20 points.

**Solution design:**
- Move opt-in prompt to post-search context using `FlightStatusNotificationViewController`
- Configure alert types via `FlightStatusNotificationConfiguration` (gate change, delay, cancellation)
- Fix Mobile-FLIFO-BFF delivery pipeline to close the 22-point reliability gap

**Gate outcome:** Solution hypothesis accepted. Proceed to Stage C.

---

### Stage C — Build Gate

**Entry criterion:** Is the build scope bounded to the validated hypothesis?

**Scope:** Contextual opt-in prompt + BFF delivery pipeline fix. Gate change notification only in MVP (highest volume disruption type). Delay and cancellation alerts deferred to next increment pending MVP measurement.

**Not in scope:** Rebuilding the full notification stack, adding new alert types beyond gate change, social sharing of flight status.

**Gate outcome:** Scope confirmed. Sprint planning authorized.

---

### Stage D — Launch Gate

**Entry criterion:** Are success metrics, rollout plan, and guardrails defined?

**Success metric:** Push opt-in rate ≥ 50% within 90 days of contextual prompt launch. Notification delivery reliability ≥ 95%.
**Guardrail:** Notification opt-out rate must not increase >5 points.
**Rollout:** 10% → 50% → 100% via feature toggle `AAFeatureFlifoFlightStatusBanner`.

**Gate outcome:** Launch approved.

---

## ❌ VIOLATION Example

### Violation Statement

> "We've got a sprint starting Monday. Let's add disruption notifications to the backlog — everyone knows passengers want them. Design can start on the opt-in screen now."

### Why This Violates PRD-2.5

1. **Problem Gate skipped.** No evidence cited that notifications are failing or that the problem is quantified. "Everyone knows" is not a gate-clearance document.
2. **Solution Gate skipped.** Design is authorized before a solution hypothesis has been tested or reviewed.
3. **Build Gate skipped.** Sprint planning starts before scope is bounded by evidence.
4. **No success metric.** There is no stated outcome to measure against, no rollout plan, no guardrail.

### Compliant Reframe

Pull support contacts, delivery rate, and opt-in funnel data. Clear Problem Gate with evidence. Only then design a solution and authorize sprint work.

---

*Grounded in flightstatusnotification-ios — FlightStatusNotificationViewController, FlightStatusNotificationConfiguration, AAFeatureFlifoFlightStatusBanner.*

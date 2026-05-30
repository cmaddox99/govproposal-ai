---
avatar: avatar-flight-status-flifo
law_id: PRD-5.1
law_title: "Minimum Viable Product Discipline"
file_type: example
---

# PRD-5.1 Minimum Viable Product Discipline — Flight Status & FLIFO

## Law Summary

An MVP is the smallest releasable increment that validates the core hypothesis. It is not a stripped-down version of the full vision — it is a scoped test. For FLIFO features, MVP scope must be bounded by the notification type or search path with the highest validated user demand, not the full feature surface.

---

## ✅ COMPLIANT Example

### MVP: Proactive Gate Change Alert

**Validated problem (from Problem Gate):**
- 4,800 support contacts/month for missed gate changes.
- Gate changes are the highest-volume single disruption type: 58% of all disruption events.
- Current push delivery reliability: 78% — 22-point gap to acceptable.

**MVP hypothesis:**
> If we deliver reliable push notifications for gate changes only — the highest-volume disruption type — to passengers who have opted in via `FlightStatusNotificationViewController`, we will see ≥ 30% reduction in "missed gate change" support contacts within 60 days and notification delivery reliability will reach ≥ 95%.

---

### What the MVP Includes

| Component | Scope |
|---|---|
| Notification type | Gate change only |
| Opt-in flow | `FlightStatusNotificationViewController` — contextual post-search prompt |
| Alert configuration | `FlightStatusNotificationConfiguration` — gate change type enabled |
| Alert delivery | Mobile-FLIFO-BFF → APNs pipeline, reliability fix applied |
| `ChooseAlertTableViewCell` | Gate change row only; delay and cancellation rows hidden |
| Success metric | Support contacts for missed gate change; delivery confirmation rate |

### What the MVP Explicitly Excludes

- Delay notifications (deferred — lower urgency, higher false-positive risk)
- Cancellation notifications (deferred — lower volume, more complex passenger reaction)
- Weather disruption alerts (deferred — no validated user demand data yet)
- Crew change notifications (deferred — operational data, not passenger-facing)
- Aircraft swap notifications (deferred — low user awareness, unclear action trigger)
- Watch app notification delivery (deferred — `AAFeatureIncomingFlifoFlightStatusWatch` separate toggle)

### Measurement Plan

- **Primary metric:** "Missed gate change" support contacts (target: -30% in 60 days)
- **Secondary metric:** Push notification delivery confirmation rate (target: ≥ 95%)
- **Guardrail:** Notification opt-out rate (must not increase >3 points post-launch)
- **Decision gate:** If primary metric does not improve ≥ 20% in 60 days, do not expand to delay/cancellation types

---

### Why This MVP Is Compliant

- Scope is bounded by the single highest-impact disruption type with validated demand.
- Success metrics are pre-registered and falsifiable.
- Deferral decisions are explicit and documented — not accidental omissions.
- The MVP tests the hypothesis without rebuilding the entire notification architecture.

---

## ❌ VIOLATION Example

### Violation Statement

> "MVP includes gate changes, delays, cancellations, weather disruptions, crew changes, and aircraft swap notifications — plus watch app delivery. We'll also redesign the `ChooseAlertTableViewCell` to show all types and add a 'notify a friend' feature."

### Why This Violates PRD-5.1

1. **Not minimal.** Six notification types + watch delivery + social feature is not an MVP — it is the full vision shipped at once.
2. **Untested demand.** Weather, crew, and aircraft swap notifications have no validated user demand evidence. Including them in "MVP" buries the signal from the hypothesis being tested.
3. **Unmeasurable core hypothesis.** If six types launch simultaneously, there is no way to isolate which type (if any) is reducing support contacts or driving opt-in.
4. **Over-engineered.** Rebuilding `ChooseAlertTableViewCell` for all types before knowing which types users want is waste.

### Compliant Reframe

Gate change only. Measure. If gate change alert reduces support contacts ≥ 20%, advance to delay alert. Build evidence for each type before expanding.

---

*Grounded in flightstatusnotification-ios — FlightStatusNotificationViewController, FlightStatusNotificationConfiguration, ChooseAlertTableViewCell. AAFeatureFlifoFlightStatusBanner, AAFeatureIncomingFlifoFlightStatusWatch.*

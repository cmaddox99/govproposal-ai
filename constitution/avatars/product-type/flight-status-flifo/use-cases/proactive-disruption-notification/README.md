```yaml
use_case:
  id: uc-flifo-disruption-notification
  name: Proactive Disruption Notification
  jtbd: "When a flight is delayed, gate-changed, or cancelled, a subscribed passenger needs to receive a push notification so they can react before arriving at the wrong gate."
  actor: Subscribed Passenger
  laws: [PRD-1.2, PRD-5.1, PRD-6.2, BUS-7.1, BUS-9.3]
  avatar: avatar-flight-status-flifo
  source_modules:
    - FlightStatusNotificationViewController
    - FlightStatusNotificationConfiguration
    - FlightStatusNotificationLegacyViewControllerProvider
    - AccessibleCheckboxView
    - ChooseAlertTableViewCell
  bff: Mobile-FLIFO-BFF
```

# Use Case: Proactive Disruption Notification

**Avatar:** `avatar-flight-status-flifo`
**Module source:** `flightstatusnotification-ios` (14 Swift files)

---

## Problem Statement (PRD-1.2)

Passengers who have opted in to flight alerts should receive a push notification when their flight status changes due to a disruption event. Currently:

- Push notification delivery confirmation rate: **78%** — 22-point gap to acceptable threshold of ≥ 95%.
- "Missed gate change" support contacts: **4,800/month**.
- Post-trip NPS for disrupted passengers who did not receive an alert: **-42**.
- Post-trip NPS for disrupted passengers who received a timely alert: **+18**.

The problem is not that passengers don't want notifications — opt-in rate is 34% and rising. The problem is delivery reliability and opt-in prompt placement.

---

## Actor

**Subscribed Passenger:** A traveler who has explicitly opted in to push notifications for a specific flight via `FlightStatusNotificationViewController`. This actor has a direct, time-sensitive need for disruption information. Non-opted-in users are out of scope for this use case.

---

## Trigger

Mobile-FLIFO-BFF receives a status change event from the FAA FLIFO feed for a flight with one or more active notification subscriptions. Trigger types:

- **Gate change** — highest volume (58% of disruption events)
- **Departure delay** — second highest volume (31% of disruption events)
- **Cancellation** — lower volume but highest passenger impact

---

## Notification Opt-In UX

### `FlightStatusNotificationViewController`

The primary opt-in surface. Displayed contextually after a user searches a flight and views status results — not at first app launch. Contextual placement has evidence basis: users who have just searched a flight are the highest-intent cohort for notification opt-in.

**Consent requirement (BUS-9.3):** The notification opt-in is explicit and affirmative. The user taps to subscribe — there is no silent or default enrollment. The opt-in action must be logged with:
- Timestamp
- Anonymized user identifier
- Flight identifier (flight number + date)
- Alert types selected

### `ChooseAlertTableViewCell`

Renders each available alert type as a selectable row within the opt-in flow. Each row uses `AccessibleCheckboxView` to render the selection state — ensuring VoiceOver accessibility compliance. Alert types shown are controlled by `FlightStatusNotificationConfiguration` for the specific flight.

**MVP scope (PRD-5.1):** Gate change row is the initial MVP type. Delay and cancellation rows are present in the component but gated — hidden by configuration until MVP measurement confirms gate change alert drives ≥ 20% reduction in support contacts.

### `FlightStatusNotificationConfiguration`

Governs which alert types are available for a given flight. Not all alert types are enabled for all flights or routes:

- Domestic short-haul: gate change + delay (weather alert not applicable)
- International: all types
- Codeshare flights: limited by data availability from operating carrier

This configuration is resolved at opt-in time and persisted with the subscription.

---

## Delivery Architecture

### Mobile-FLIFO-BFF → APNs Pipeline

1. FAA FLIFO feed pushes a status change event to Mobile-FLIFO-BFF.
2. BFF resolves active subscriptions for the affected flight.
3. BFF constructs notification payloads per subscriber's configured alert types.
4. BFF dispatches to Apple Push Notification service (APNs).
5. APNs delivers to subscriber device; delivery confirmation logged.

**Current reliability gap:** 22% of dispatched notifications are not confirmed delivered. Root causes under investigation: stale APNs device tokens, BFF retry logic gaps, APNs sandbox vs. production routing errors.

**Reliability target (PRD-6.2):** ≥ 95% delivery confirmation rate, sustained for 60 days, before any new notification types are added.

---

## Legacy Opt-In Path

### `FlightStatusNotificationLegacyViewControllerProvider`

Provides backward-compatible access to the notification opt-in flow for surfaces that predate `FlightStatusNotificationViewController`. This provider bridges older navigation contexts to the current opt-in ViewController.

**Deprecation note:** Active subscriptions created through legacy entry points must not be orphaned. Before deprecating this provider, a migration audit must confirm all legacy-created subscriptions have corresponding records in the current subscription store. Orphaned subscriptions are a likely contributor to the 22% delivery failure rate.

---

## Laws Applied

### PRD-1.2 — Problem-First

Any expansion of notification types (beyond the MVP gate change type) must be preceded by a quantified problem statement. "Users want delay notifications" is not sufficient — show the demand signal, the support contact volume, or the session behavior that evidences the need.

### PRD-5.1 — MVP Discipline

Gate change alert is the MVP. Delay and cancellation alerts are deferred until MVP measurement confirms the hypothesis. Do not expand `ChooseAlertTableViewCell` visible rows until the gate holds.

### PRD-6.2 — Retention First

Delivery reliability (78% → 95%) must be fixed before adding new notification types or new opt-in surfaces. Existing opted-in users are being under-served. Retention obligation precedes capability expansion.

### BUS-7.1 — Audit Trail

Every opt-in event, opt-out event, and notification dispatch must be logged. Fields required: timestamp, user identifier hash, flight identifier, alert type, delivery outcome (confirmed / failed / pending).

### BUS-9.3 — Consent

Opt-in is explicit and affirmative. No silent enrollment. Opt-out must be immediately honored. Consent record must be retained per BUS-9.3 retention schedule.

---

## Success Metrics

| Metric | Target | Timeframe |
|---|---|---|
| Notification delivery confirmation rate | ≥ 95% | 60 days post-pipeline fix |
| "Missed gate change" support contacts | -30% | 60 days post-MVP launch |
| Push opt-in rate | ≥ 50% | 90 days post-contextual prompt |
| NPS — disrupted + notified passengers | ≥ +10 points vs. baseline | 90 days |
| Opt-out rate post-launch | No increase >3 points | 30 days |

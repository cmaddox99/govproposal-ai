---
avatar: avatar-flight-status-flifo
law_id: PRD-6.2
law_title: "Retention-First Sequencing"
file_type: example
---

# PRD-6.2 Retention-First Sequencing — Flight Status & FLIFO

## Law Summary

Retention of existing users and reliability of existing features must be prioritized over acquisition of new users or addition of new capabilities. A feature that is unreliable for current users destroys trust faster than new features build it. For FLIFO, reliability of status data delivery and notification delivery are retention-critical.

---

## ✅ COMPLIANT Example

### Decision: Fix Notification Delivery Reliability Before Adding New Alert Types

**Current state:**
- Push notification delivery confirmation rate: 78% (target: ≥ 95%).
- 22% of opted-in passengers are not receiving flight alerts they explicitly subscribed to.
- Post-trip NPS for disrupted passengers who did not receive a notification: -42.
- Post-trip NPS for disrupted passengers who received a timely notification: +18.
- Gap: 60-point NPS difference between informed and uninformed disrupted passengers.

**Proposed new feature competing for resources:** "Track any flight" social sharing — allow users to share a flight status link with non-app users.

---

### Retention-First Analysis

| Dimension | Fix Delivery Reliability | Add Social Sharing |
|---|---|---|
| Affected users | 22% of opted-in users (actively harmed today) | New acquisition path (zero current harm) |
| NPS impact | +60 points for disrupted passengers who receive alerts | Unknown; no baseline |
| Trust signal | Fixing what users paid for (explicit opt-in) | Adding what users did not ask for |
| Evidence base | Delivery confirmation logs, NPS segmentation | No validated demand |
| Retention effect | Direct: app re-opens after alert delivery | Indirect, speculative |

**Decision:** Fix notification delivery reliability first. Social sharing not authorized until delivery reliability ≥ 95% for 60 consecutive days.

---

### What "Reliability First" Means in Practice

1. **Mobile-FLIFO-BFF → APNs pipeline audit:** Identify the 22% delivery gap root cause before any new feature work.
2. **`FlightStatusNotificationConfiguration` review:** Confirm notification payload structure is valid for all opt-in configurations.
3. **`FlightStatusNotificationLegacyViewControllerProvider` deprecation path:** Ensure legacy opt-in flows do not create orphaned subscriptions that contribute to delivery failures.
4. **Delivery rate monitoring:** Instrument delivery confirmation rate as a tracked metric in all sprint reviews until ≥ 95%.
5. **Only after 95% sustained for 60 days:** Evaluate social sharing or new notification types based on demand evidence.

### Why This Sequencing Is Compliant

- Existing opted-in users are actively harmed by the current 78% delivery rate. They took an explicit action (opt-in) and received less than what was promised.
- Fixing this is a retention obligation — not a nice-to-have.
- Adding new features on top of a broken foundation accelerates trust erosion, not recovery.
- PRD-6.2 requires that reliability of existing features precedes new capability expansion.

---

## ❌ VIOLATION Example

### Violation Statement

> "Let's add a 'Track any flight' social sharing feature so users can share flight status links with family members who don't have the app. This will drive new installs and grow our FLIFO user base. We can circle back to the notification delivery issue later."

### Why This Violates PRD-6.2

1. **Retention ignored.** 22% of existing opted-in users are not receiving alerts they signed up for. "Circle back later" means continuing to harm them.
2. **Acquisition over retention.** Social sharing is an acquisition mechanism. PRD-6.2 requires retention reliability to be addressed before acquisition expansion.
3. **No demand evidence.** "Family members who don't have the app" is an assumption. No user research or demand data is cited.
4. **Trust erosion compounded.** A user who does not receive their gate change alert and then sees a "share flight" prompt has no reason to trust the product.
5. **NPS gap ignored.** The 60-point NPS gap between notified and not-notified disrupted passengers is a direct business retention signal — it is not referenced in the proposal.

### Compliant Reframe

Fix notification delivery to ≥ 95%. Measure NPS recovery for disrupted passengers. Once trust baseline is restored, evaluate social sharing with demand evidence.

---

*Grounded in flightstatusnotification-ios — FlightStatusNotificationViewController, FlightStatusNotificationConfiguration, FlightStatusNotificationLegacyViewControllerProvider. Mobile-FLIFO-BFF APNs delivery pipeline.*

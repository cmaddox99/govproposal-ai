```yaml
use_case:
  id: uc-manage-trip-contact-update
  name: Reservation Contact Information Update
  jtbd: "When a traveler changes their phone number or email after booking, they need to update contact details on their reservation so they receive flight notifications."
  actor: Booked Traveler
  laws: [PRD-1.2, PRD-1.5, BUS-4.3, BUS-7.1, BUS-9.3]
```

# Use Case: Reservation Contact Information Update

## Problem

When a traveler books a flight, their phone number and email address are
stored on the PNR at time of purchase. AA's notification systems — flight
status alerts, gate change messages, delay notifications, and boarding reminders
— use these contact details to reach the traveler. If the traveler changes their
phone number or email after booking, they receive no further notifications for
that reservation.

There is currently no self-service path in the iOS app to update contact
information on an existing reservation. Travelers who need to update their
details must call the AA reservations line.

### Evidence

| Signal | Data |
|--------|------|
| Call center tagging | 4,200 calls/month tagged "update contact info" (Salesforce, 90-day avg.) |
| Notification failures | 9.1% of push and SMS notification delivery failures trace to mismatched phone or email on PNR (Adobe Analytics, 90-day window) |
| Session recordings | Travelers who open `ReservationSummaryView` and search for an edit affordance on the contact section spend avg. 2.1 min before abandoning (FullStory) |
| Post-call CSAT | Calls to update contact info score 2.1/5 — below the 3.4/5 overall call center average |

### Impact Hypothesis

If a self-service contact update flow is built in the iOS app, ≥ 50% of contact
update attempts will shift from call center to self-service within 45 days of
launch, reducing monthly support cost and improving notification delivery rates.

---

## Solution Overview

A new "Edit Contact Info" capability is introduced within `ReservationSummaryView`
(trips-ios). Contact mutations are routed through `Mobile-Update-Reservation`
BFF, with reservation reads provided by `mobile-reservation-bff`. The flow is
minimal: a single edit screen covering phone and email with inline validation.

### User Flow

1. Traveler opens the AA app and navigates to their reservation via `MyTripsView`
2. `ReservationSummaryView` renders the current contact section (phone and email,
   read-only today)
3. An "Edit" affordance is added to the contact section — tapping opens the
   contact update form
4. The form displays the current phone number and email pre-populated from the
   PNR data returned by `mobile-reservation-bff`
5. Traveler edits one or both fields
6. Client-side validation runs:
   - Phone: E.164 format, domestic or international
   - Email: RFC 5322 basic format check
7. Traveler taps "Save"
8. `Mobile-Update-Reservation` BFF receives the mutation request, validates the
   PNR lock state, and writes the updated contact details
9. Confirmation inline state shown in `ReservationSummaryView` — contact section
   refreshes with the new values

---

## Engineering Context

### BFF Layer

**`mobile-reservation-bff`** — provides the reservation read endpoint used to
populate `ReservationSummaryView`, including the current contact information
stored on the PNR. The contact section (phone, email) is returned as part of
the reservation detail response.

**`Mobile-Update-Reservation`** — owns the contact information write path.
Accepts a PUT or PATCH request with PNR locator, passenger token, and updated
contact fields. Validates that the PNR is not locked (no active check-in, no
PSS write embargo), then routes the mutation to the PSS layer. Returns the
updated reservation state on success.

**`aa-ct-mobile-reservationlist-bff`** — provides the trip list aggregation
used by `MyTripsView`. Not directly involved in the contact update write path,
but its cached trip list data must be invalidated or refreshed after a
successful contact update so that the updated contact details are shown
consistently.

### iOS Layer

**`ReservationSummaryView` (trips-ios)** — the primary UI surface for this use
case. Today it renders contact information in a read-only section. The change
required is:
- Add an "Edit" button/icon to the contact info section
- On tap, present an inline or modal edit form
- On save success from `Mobile-Update-Reservation`, refresh the contact section
  in place without full-screen navigation

The edit form itself is a new, lightweight view — it is not part of an existing
module and does not require changes to the CancelRes or LapInfant modules.

---

## Compliance Notes

**BUS-4.3 — Passenger Data Accuracy:**
Contact information on a PNR is safety-relevant: AA gate agents and crew use
it to reach travelers in irregular operations. The contact update flow must
validate format before writing. An invalid phone number or unparseable email
must be rejected client-side. `Mobile-Update-Reservation` must perform a
second-layer validation before writing to PSS — client-side validation alone
is insufficient.

**BUS-7.1 — Audit Logging:**
Every contact information mutation must be logged with: PNR locator, passenger
token, field changed (phone/email), old value hash, new value hash, timestamp,
and originating device session identifier. The log record must be immutable.
This is required to support dispute resolution when a traveler claims they did
not receive a notification — the audit log establishes what contact information
was on record at the time of the notification attempt.

**BUS-9.3 — Data Privacy:**
Contact information (phone and email) is personal data subject to AA's data
retention and access policies. The update flow must:
- Confirm the requester is authenticated and is the passenger on the PNR
- Not log or transmit the raw new phone/email value in plain text in analytics
  pipelines (hash or truncate in telemetry)
- Comply with applicable state privacy law requirements for data mutation
  acknowledgment (e.g., CCPA for California residents)

---

## PRD-1.5 Compliance — Decision Grounding

The decision to build this use case rests on three specific evidence points:

1. 4,200 calls/month is a quantified, taggable signal — not an estimate
2. 9.1% notification delivery failure is a measurable system outcome tied
   directly to the problem (stale contact data)
3. 2.1/5 post-call CSAT for contact update calls is below the call center
   average — indicating this interaction is unusually painful

The success measurement plan: track contact update call volume (call center tag)
and notification delivery failure rate (Adobe Analytics) 45 days post-launch.
Both metrics have clean baselines above. Success = ≥ 50% call deflection and
≥ 2 percentage point improvement in notification delivery rate.

---

## MVP Scope (PRD-5.1)

**In scope:**
- Phone number and email update on existing domestic reservations
- Inline edit from `ReservationSummaryView`
- Write via `Mobile-Update-Reservation` BFF
- Client-side and BFF-side validation
- BUS-7.1 audit log on every write

**Out of scope for MVP:**
- Address update (separate PSS field with different validation requirements)
- Emergency contact update
- Updating contact info across multiple reservations in bulk
- AAdvantage profile contact sync (separate identity system)

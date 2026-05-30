# Journey: Trip Cancellation via iOS App
# Avatar: avatar-manage-trip | Law: PRD-2.5 Discovery Stage-Gate Law
# Grounded in: managetrip-ios analysis — CancelRes + LapInfant modules
# Source modules: CancelTripViewModel, CancelEligibilityEndpoint, CancelReservationCoordinator

```yaml
journey:
  id: journey-cancel-trip
  name: Trip Cancellation via iOS App
  persona: Booked traveler who needs to cancel a future flight
  laws: [PRD-2.5, PRD-1.2, BUS-2.3, BUS-3.1, BUS-7.1]
  source_evidence: managetrip-ios source analysis (2026-04-30)
```

---

## Journey Map

| Step | What the user does | iOS module | Key law |
|------|--------------------|------------|---------|
| 1 | Opens the AA app and taps "My Trips" | `MyTripsView` (trips-ios via `ViewController_MyTrips.swift`) | PRD-1.2 |
| 2 | Selects the reservation to cancel from the trip list | `ReservationSummaryView` (trips-ios) | — |
| 3 | Taps "Cancel Trip" action on the reservation detail | `CancelTripView` (managetrip-ios / CancelRes/) | PRD-2.5 |
| 4 | App performs eligibility check against the BFF | `CancelEligibilityEndpoint` → `CancelTripViewModel_Fetcher` | BUS-2.3 |
| 5 | Reviews cancellation terms, fees, and refund method | `CancelTripViewModel` + `TaxesAndFeesViewModel` + `CostSummaryViewModel` | BUS-2.3 |
| 6 | Reviews segment-level cost breakdown | `SegmentCardViewModel` (CancelRes/) | BUS-2.3 |
| 7 | Confirms cancellation | `CancelReservationCoordinator` → `CancelConfirmationEndpoint` | BUS-3.1 |
| 8 | Confirmation screen shown with PNR reference and refund timeline | `CancelTripViewModel` (post-confirm state) | BUS-3.1 |
| 9 | Analytics event fired for cancellation outcome | `CancelTripViewModel_Metrics` | BUS-7.1 |

---

## Step Detail

### Step 1 — My Trips Entry

`MyTripsView` (surfaced by `ViewController_MyTrips.swift` in trips-ios) renders
the traveler's active and upcoming reservations. The list is aggregated by
`mobile-travelhub-bff` which fans out to `aa-ct-mobile-reservationlist-bff` for
reservation data. The traveler taps a trip card to enter the detail view.

### Step 2 — Reservation Summary

`ReservationSummaryView` presents segment details, passenger names, and
available actions. The "Cancel Trip" action is rendered conditionally — it is
only shown when the eligibility pre-check (from `mobile-travelhub-bff`) returns
a cancellable flag. This prevents the action from appearing on non-refundable
fares where cancellation is unavailable.

### Step 3 — Cancel Trip Entry Point

Tapping "Cancel Trip" launches `CancelTripView`. The view is owned by the
CancelRes/ module in managetrip-ios (AmericanManageTrip framework). It
initializes `CancelTripViewModel` and begins the eligibility fetch.

### Step 4 — Eligibility Check

`CancelTripViewModel_Fetcher` calls `CancelEligibilityEndpoint` on
`aa-ct-mobile-manage-bff`. The BFF evaluates:

- Fare class and ticket type (refundable vs. non-refundable)
- Purchase date vs. departure date (DOT 24-hour rule: BUS-2.3)
- Whether the PNR is currently locked by active check-in

The eligibility response determines which cancellation path the user enters:
full refund, partial refund, travel credit only, or no-cancellation (with
change-fee alternatives surfaced instead).

### Step 5 — Terms & Fees Review

`CancelTripViewModel` loads the refund summary. `TaxesAndFeesViewModel`
populates the taxes and fees breakdown. `CostSummaryViewModel` presents the
total cancellation cost and the net refund amount. Per BUS-2.3, the refund
method must be disclosed explicitly before the traveler confirms:

- Original Form of Payment (credit card / cash refund)
- AAdvantage miles (for award tickets)
- Travel credit / eVoucher

The user must scroll through this information before the "Confirm" button
becomes active. This enforces disclosure intent rather than burying it.

### Step 6 — Segment-Level Breakdown

For multi-segment itineraries, `SegmentCardViewModel` renders per-leg cost
cards so the traveler can see which segments contribute which costs. This is
particularly important for mixed-fare itineraries where one leg may be
refundable and another non-refundable.

### Step 7 — Confirmation

The traveler taps "Confirm Cancellation." `CancelReservationCoordinator` (which
implements `CancelReservationRoutingDestinationProvider`) orchestrates the
cancellation request:

1. Builds a `CancelReservationRequest` with PNR, passenger tokens, and confirmed
   refund method
2. Calls `CancelConfirmationEndpoint` on `aa-ct-mobile-manage-bff`
3. BFF routes to `Mobile-Manage-Minilith` for PSS-layer PNR mutation
4. On success, routes to the confirmation screen via
   `CancelReservationPresenter`

The `CancelReservationResponse` carries the new PNR state, refund reference
number, and estimated processing timeline.

### Step 8 — Confirmation Screen

The post-cancel state of `CancelTripView` renders:

- Cancellation confirmation message
- PNR reference number (required by BUS-3.1 for audit trail)
- Refund method and estimated processing time
- "Contact Support" deep link if the refund has not appeared within 10 days

Per BUS-3.1, the PNR is retained in a CANCELLED state — it is not deleted. This
allows loyalty, check-in, and dispute-resolution systems to query historical PNR
state.

### Step 9 — Analytics

`CancelTripViewModel_Metrics` fires a cancellation analytics event capturing:

- Cancellation pathway taken (refund vs. credit)
- Time-to-confirm from first entry to CancelTripView
- Whether the user expanded the `TaxesAndFeesViewModel` detail section
- BFF response time

Per BUS-7.1, this telemetry also writes an immutable audit record of the
cancellation action associated with the PNR and passenger identity.

---

## Architecture Notes

**BFF layer:**
`aa-ct-mobile-manage-bff` owns cancellation mutation. `mobile-travelhub-bff`
provides the pre-check eligibility flag used by `ReservationSummaryView` to
conditionally render the "Cancel Trip" entry point. `Mobile-Manage-Minilith`
is the legacy orchestration layer between the BFF and the PSS.

**DOT Compliance (BUS-2.3):**
The 24-hour free cancellation rule requires that any booking made 7 or more
days before departure is cancellable for a full refund within 24 hours of
purchase. `CancelEligibilityEndpoint` must evaluate purchase timestamp and
departure date. The refund method disclosure in `CostSummaryViewModel` must
appear before confirmation — not after — to satisfy DOT disclosure requirements.

**PNR Retention (BUS-3.1):**
After cancellation, the PNR transitions to CANCELLED state and is retained for
a minimum retention window. The PNR must not be purged. Downstream systems
including loyalty award reversal and dispute resolution depend on PNR history.

**Audit Trail (BUS-7.1):**
`CancelTripViewModel_Metrics` must write an immutable record of: who cancelled,
what PNR, what refund method was confirmed, and when. This record is independent
of the analytics event and must be persisted even if the analytics pipeline is
unavailable.

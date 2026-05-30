```yaml
use_case:
  id: uc-manage-trip-lap-infant
  name: Lap Infant Management
  jtbd: "When a parent books a flight and then realizes they are traveling with an infant under 2, they need to add the lap infant to the reservation without calling the airline."
  actor: Parent Traveler
  laws: [PRD-1.2, PRD-5.1, BUS-2.3, BUS-4.3, BUS-7.1]
```

# Use Case: Lap Infant Management

## Problem

Parents traveling with an infant under age 2 can carry the child on their lap
at no additional charge on most domestic AA itineraries. However, the infant
must be formally added to the reservation — the PNR must include the infant
as an associated passenger — for the child to be accounted for in crew safety
headcounts and for the parent to receive the correct boarding documents.

Today, there is no self-service path in the iOS app to add a lap infant after
the initial booking is complete. Parents who realize they need to add an infant
must call the AA reservations line.

### Evidence

| Signal | Data |
|--------|------|
| Call center tagging | 23% of family travelers who call after booking are trying to add a lap infant |
| Abandonment (FullStory) | Parents who open `ReservationSummaryView` and search for an add-passenger option spend avg. 3.4 min before abandoning |
| Second-attempt rate | 34% of lap infant additions require a second contact attempt (callback or repeat call) due to incomplete info gathered on first call |
| Cost | $8.40 average handle time cost per call × 11,200 monthly lap infant calls = $94,080/month in avoidable support cost |

### Impact Hypothesis

If a self-service lap infant add flow is built in the iOS app, ≥ 40% of
lap infant additions will shift from call center to self-service within 60 days
of launch, reducing monthly support cost by ≥ $37,000.

---

## Solution Overview

A new "Add Lap Infant" flow is introduced within the manage-trip surface,
accessible from `ReservationSummaryView` in trips-ios. The flow is implemented
in the LapInfant/ module of managetrip-ios (AmericanManageTrip framework) and
orchestrated through `aa-ct-mobile-manage-bff`.

### User Flow

1. Parent opens the AA app and navigates to the reservation via `MyTripsView`
2. On `ReservationSummaryView`, an "Add Lap Infant" entry point is rendered when
   the reservation is lap-infant-eligible
3. `LapInfantEligibilityEndpoint` is called to confirm the PNR accepts infant
   additions (checks: fare class, seat availability, segment type, existing
   infant count)
4. `LapInfantViewModel` loads the infant data collection flow
5. `LapInfantInputViewModel` collects:
   - Infant first and last name
   - Date of birth (must be under age 2 on the travel date)
   - Relationship to traveling adult
6. `LapInfantPassengerListViewModel` shows a review screen listing all
   passengers including the new infant
7. `LapInfantPassengerViewModel` presents per-passenger confirmation state
8. Parent confirms; `AddLapInfantEndpoint` sends `LapInfantAddRequest` to
   `aa-ct-mobile-manage-bff`
9. BFF routes to `Mobile-Manage-Minilith` for PSS PNR mutation
10. Confirmation screen displays updated passenger list with infant included

---

## Engineering Context

### Module: LapInfant/ (managetrip-ios / AmericanManageTrip framework)

**`LapInfantViewModel`** — top-level view model for the lap infant add flow.
Owns the state machine: eligibility loading → data entry → review → confirmation.
Consumes the response from `LapInfantEligibilityEndpoint` to determine whether
to proceed or surface an ineligibility message.

**`LapInfantInputViewModel`** — manages the data entry form state. Validates:
- Date of birth produces an age < 2 years on each travel segment date
- Name fields are non-empty and contain only allowable characters
- All required fields are populated before enabling the continue action

**`LapInfantPassengerViewModel`** — models a single passenger entry in the
review screen, used for both the traveling adult and the new infant.

**`LapInfantPassengerListViewModel`** — aggregates the full passenger list
(existing passengers + new infant) for the review step. Surfaces a warning
if the infant's age will exceed 2 years on the return segment.

**`LapInfantEligibilityEndpoint`** — calls `aa-ct-mobile-manage-bff` to
evaluate whether the PNR is eligible for infant addition. Eligibility rules:
- International itineraries may require a separate infant ticket (out of scope
  for MVP — domestic only)
- PNR must not already contain a lap infant associated with the same adult
- Check-in must not be active for any segment

**`AddLapInfantEndpoint`** — sends the `LapInfantAddRequest` to
`aa-ct-mobile-manage-bff`. The request carries: PNR locator, traveling adult
passenger token, infant name, date of birth. The BFF validates, appends the
infant to the PNR via `Mobile-Manage-Minilith`, and returns a confirmation with
the updated passenger list.

---

## Compliance Notes

**BUS-2.3 — DOT Disclosure:**
The confirmation screen must display the infant's fare basis (lap infant = $0
for domestic) and any applicable international surcharges. For domestic MVP,
the screen must state that the infant travels at no additional charge and
clarify that this applies only to U.S. domestic itineraries.

**BUS-4.3 — Passenger Data Accuracy:**
The infant's date of birth entered by the parent must be validated against the
travel date for each segment. If the infant will turn 2 before any segment
departs, `LapInfantInputViewModel` must surface an error and not proceed. The
PNR must not contain an infant record for a child who is 2 or older on the
travel date.

**BUS-7.1 — Audit Logging:**
`AddLapInfantEndpoint` must log: PNR locator, traveling adult token, infant name
hash, date of birth, and timestamp of the add operation. This record must be
immutable and retained for the PNR lifecycle window.

---

## MVP Scope (PRD-5.1)

**In scope:**
- Domestic itineraries only
- One lap infant per traveling adult
- `LapInfantEligibilityEndpoint` evaluation before data entry
- Name and DOB collection via `LapInfantInputViewModel`
- PNR update via `AddLapInfantEndpoint`
- Confirmation screen with updated passenger list

**Out of scope for MVP:**
- International itineraries (require separate infant ticket logic)
- Multiple infants per adult
- Modifying or removing a previously added lap infant
- Infant seat selection or bassinette request

**Success criteria:**
1. ≥ 40% of lap infant additions shift to self-service within 60 days
2. Second-attempt rate drops from 34% to < 10% (in-app, both attempts captured)
3. `AddLapInfantEndpoint` error rate < 1.5%

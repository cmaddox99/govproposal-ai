# Journey: Involuntary Schedule Change Self-Serve
# Avatar: avatar-schedule-change-self-serve | Law: PRD-2.1 User Journey Mapping
# Grounded in: changetrip-ios, samedayflightchange-ios, schedulechange-ios, mobile-change-bff

journey:
  id: journey-involuntary-schedule-change
  name: Involuntary Schedule Change — Self-Serve Rebooking
  persona: Passenger notified of flight cancellation or significant schedule change
  laws: [PRD-2.1, BUS-2.1, BUS-2.4, ENG-6.1, ENG-6.4]
  source_evidence: hangar-w4-dp-mobile codebase — mobile-change-bff, changetrip-ios, schedulechange-ios

---

## Journey Map

| Step | Passenger action | iOS module | BFF / Backend | Key law |
|------|-----------------|------------|---------------|---------|
| 1. Notification | Push notification of disruption received | `schedulechange-ios` / `ScheduleChangeBannerProvider` | `aa-ct-mobile-airship` (push) | BUS-2.1 (DOT rights disclosure) |
| 2. View updates | `TripUpdatesViewController` surfaces schedule change card | `TripUpdatesViewController` | `mobile-change-bff` / `ChangeTripController` | BUS-2.1 (written rights statement) |
| 3. Eligibility check | System validates rebooking rules for PNR | `ChangeTripCoordinator` → `ChangeTripInfoFetcher` | `EligibilityEndpoint` (ChangeTripController) | ENG-6.1 (JWT-scoped PNR access) |
| 4. Choose new flight | Passenger selects from alternatives | `ChangeTripChooseFlightsViewModel` → `ChooseFlightsScreen` | `FlightsEndpoint` / `ReshopConnector` | PRD-2.1 (JTBD: reach destination) |
| 5. Review fare difference | Cost summary displayed | `CostSummaryViewModel` | `TripSummaryEndpoint` | BUS-2.4 (fare difference transparency) |
| 6. Seat selection | Optional seat re-selection | `CabinInfoViewModel` → `ChooseCabinScreen` | `CabinsEndpoint` | PRD-2.1 |
| 7. Confirm rebooking | Passenger confirms; new PNR written | `PassengerSelectionViewModel` → `ShoppingCartEndpoint` | `ChangeTripServiceImplementation` → `drss-schedule-change-reservation-service` | ENG-6.4 (audit: immutable change record) |
| 8. Confirmation | Updated itinerary displayed; push confirmation sent | `BookingFinish` / confirmation screen | `ChangeTripController` response | ENG-6.4 (BUS-2.1 rights confirmed) |

---

## Same-Day Flight Change (SDFC) Sub-Path

When the change is same-day eligible, `samedayflightchange-ios` handles the dedicated flow:

| Step | Module | Class | BFF endpoint |
|------|--------|-------|--------------|
| Show SDFC options | `samedayflightchange-ios` | `SameDayFlightOptionsViewController` | `SDFCController` / `SDFCOffersEndpoint` |
| Select new flight | `samedayflightchange-ios` | `SameDayFlightChangeNewFlightViewController` | `SDFCOffersEndpoint` |
| Confirm booking | `samedayflightchange-ios` | `SameDayFlightChangeShoppingCartDestinationProvider` | `SDFCShoppingCartEndpoint` → `SDFCServiceImplementation` |

---

## DOT Consumer Protection (BUS-2.1)

Per DOT 14 CFR Part 250, involuntary schedule changes require:
- Full refund option prominently surfaced — not buried below rebooking offers
- Rebooking options on comparable service; codeshare restrictions documented
- Written statement of rights presented in `TripUpdatesViewController` (Step 2)
- Audit record in `HistoryDataFetcher` / `HistoryData` domain type for regulatory inspection

## Ineligibility Path

When `EligibilityEndpoint` returns ineligible:
1. `ChangeTripCoordinator` routes to reason-code display screen
2. `ScheduleChangeCalloutViewModelProvider` surfaces actionable reason and next steps
3. Agent escalation path offered via `ScheduleChangeReaccomFlightCardDataProvider`
4. `AAFeatureScheduleChange` toggle controls rollout of reason-code transparency feature

## Audit Trail (ENG-6.4)

Every change decision produces an immutable record via `mobile-change-bff`:
- Decision: ELIGIBLE / INELIGIBLE, rule match, timestamp, agent if applicable
- Executed rebooking: PNR ref, old/new segments, fare delta, `ChangeTripConstants` rule_ref
- Override events: supervisor ID, override reason, `CSRetrieveReservationConnector` confirmation

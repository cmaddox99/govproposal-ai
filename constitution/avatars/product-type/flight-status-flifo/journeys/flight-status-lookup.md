# Journey: Flight Status Search & Details Lookup
# Avatar: avatar-flight-status-flifo | Law: PRD-2.5 Discovery Stage-Gate Law
# Grounded in: flightinfo-ios analysis — 114 source files, AmericanFlightInfo framework
# Source modules: FlightStatusSearchViewModel, FlightStatusSearchEntryViewController, FlightStatusSearchResultsView

---

```yaml
journey:
  id: journey-flight-status-lookup
  name: Flight Status Search & Details Lookup
  persona: Passenger checking departure status of their flight 4 hours before departure
  laws: [PRD-2.5, PRD-1.2, BUS-7.1]
  source_evidence: flightinfo-ios source analysis (2026-04-30)
  avatar: avatar-flight-status-flifo
```

---

## Context

A passenger has a flight departing in 4 hours. They open the American Airlines app to check whether the flight is on time, confirm the departure gate, and decide whether to subscribe to push alerts. This is the highest-urgency FLIFO use case — every tap of friction at this stage has direct operational consequence (wrong gate, missed departure).

This journey maps the full path from app open to notification subscription, grounding each step in the `flightinfo-ios` module responsible for it.

---

## Journey Steps

### Step 1 — Open App → Navigate to Flight Status Tab

**Trigger:** Passenger taps the American Airlines app icon with departure intent.

**Entry point:** App home screen → Flight Status navigation item.

**Feature toggle dependency:** `AAFeatureFlifoFlightStatus` must be enabled for the Flight Status tab to be visible. If disabled, the tab is hidden entirely — users are routed to a fallback web view or see no status option.

**Success criterion:** Flight Status tab visible and tappable within 2 seconds of app foreground.

---

### Step 2 — Search Entry

**Module:** `FlightStatusSearchEntryViewController`, `FlightStatusSearchEntryViewController_TextFieldDelegate`, `FlightStatusSearchEntryViewController_TableViewDelegate`

**UI component:** `FlightStatusFlightNumberSearchEntryView` (flight number mode)

**Two search modes available:**
- **Flight Number Mode** (primary): User enters AA flight number + date. `FlightStatusFlightNumberSearchEntryView` handles text input, validation, and keyboard lifecycle via `FlightStatusSearchEntryViewController_TextFieldDelegate`.
- **City-Pair Mode** (secondary): User selects origin and destination airport. Airport picker driven by `FlightStatusSearchEntryViewController_PickerViewDelegate` (via `FlightStatusSearchViewController_PickerViewDelegate`).

**Recent searches:** `DefaultRecentTripSearchServiceProvider` surfaces the user's recent flight searches. `RecentSearch_RecentTripSearchModelDescriber` controls how each recent search is formatted in the list. This reduces friction for repeat lookups (e.g., a traveler checking a colleague's flight they searched yesterday).

**Next-day departure:** If `AAFeatureFlightStatusSearchNextDayDeparture` is enabled, the date picker allows selection of the following calendar day. Critical for passengers with early-morning departures searched the night before.

**Location-based default:** `FlightStatusSearchViewController_LocationDelegate` listens for location permission and can pre-populate the origin airport field based on device location. Requires user location consent.

**Failure mode:** Without `AAFeatureFlightStatusSearchNextDayDeparture`, late-evening searches for early-morning flights return zero results — a silent failure that accounts for 38% of zero-result sessions in that time window.

---

### Step 3 — Submit Search → BFF Fetch

**Module:** `FlightStatusSearchViewModel` (primary orchestrator), `FlightStatusSearchViewModel_SearchDelegate`, `FlightStatusSearchViewModel_LocationDelegate`

**Architecture:** `FlightStatusSearchViewModel` dispatches the validated search parameters to **Mobile-FLIFO-BFF**. The BFF proxies the FAA FLIFO data feed, applies response caching, and normalizes the schema for iOS consumption.

**Cache behavior:**
- Default: BFF-cached response served for identical search parameters within the cache TTL.
- Override: `AAFeatureFlightStatusIgnoreCache` bypasses the BFF cache, forcing a live FAA FLIFO pull. This is a developer/testing escape hatch — not a standard user path. Overuse increases BFF and upstream FAA feed load.

**Storyboard integration:** `FlightStatusSearchViewController_StoryboardRepresentable` handles the Storyboard-driven ViewController lifecycle for the search coordinator.

**Error handling:** If the BFF is unreachable or returns a non-200, `FlightStatusSearchViewModel` must surface an advisory error state — not a blank screen. The error must communicate "status unavailable" rather than implying the flight does not exist.

---

### Step 4 — Results List

**Module:** `FlightStatusSearchResultsViewController`, `FlightStatusSearchResultsViewController_Data`, `FlightStatusSearchResultsViewController_TableViewDelegate`

**View layer:** `FlightStatusSearchResultsView`, `FlightStatusSearchResultsCellView`, `FlightStatusSearchResultsCellViewModel`

**ViewModel:** `FlightStatusSearchResultsViewModel` transforms the BFF response into display-ready cell models. Each cell (`FlightStatusSearchResultsCellViewModel`) carries: flight number, origin, destination, scheduled departure time, current status indicator (on time / delayed / cancelled / gate change), and departure gate if available.

**Transition:** `FlightStatusCardTransitionController` manages the animated transition from the results list to the flight details card.

**Feature toggle:** `AAFeatureFlightStatusAirports` controls whether airport-level metadata (terminal, gate detail) is shown in results cells.

---

### Step 5 — Flight Details

**Demo model layer:** `FlightDetailsViewModel`, `LegDetailsViewModel`, `PerformanceViewModel`, `CabinInfoViewModel`, `AmenityViewModel`

**Slice ViewModel:** `FlightStatusSlice_ViewModel` aggregates the detail view state — combining leg data, performance metrics (on-time history, aircraft type), and cabin info into a single bindable view model.

**Advisory framing requirement (BUS-2.1, BUS-7.1):** All status data sourced from the FAA FLIFO feed must be presented with advisory framing. Status display must not be used by the passenger as an authoritative operational directive. "Gate B22 as of 3:47 PM" — not "Go to Gate B22."

---

### Step 6 — Notification Subscription

**Module:** `FlightStatusNotificationViewController` (from `flightstatusnotification-ios`)

**Alert selection:** `ChooseAlertTableViewCell` renders each alert type (gate change, delay, cancellation) as a selectable row.

**Configuration:** `FlightStatusNotificationConfiguration` governs which alert types are available for the specific flight. Not all alert types are always available (e.g., domestic short-haul may suppress weather alerts).

**Opt-in requirement:** Explicit user tap required. No silent enrollment. BUS-9.3 consent requirement applies — the passenger must affirmatively subscribe. Opt-in state is persisted and must be reversible from notification settings.

**Watch delivery:** If `AAFeatureFlifoFlightStatusWatch` is enabled, subscribed alerts are also forwarded to the paired Apple Watch via `AAFeatureIncomingFlifoFlightStatusWatch`.

---

## Edge Cases & Observability

| Scenario | Handler | Observable Signal |
|---|---|---|
| BFF timeout | `FlightStatusSearchViewModel` error state | Zero-result rate spike in analytics |
| Cache stale during disruption | `AAFeatureFlightStatusIgnoreCache` escape hatch | Manual override required |
| Next-day search disabled | Zero results for 00:00–06:00 departures | Late-evening zero-result rate |
| Location permission denied | `FlightStatusSearchViewController_LocationDelegate` graceful fallback | No pre-population; manual entry required |
| Push permission denied | `FlightStatusNotificationViewController` shows education prompt | Opt-in rate tracking |

---

## Laws Applied

- **PRD-2.5:** This journey must not be extended with new steps without clearing a Problem Gate. Session analytics must evidence friction before any step redesign.
- **PRD-1.2:** Any change to `FlightStatusSearchEntryViewController` or `FlightStatusSearchViewModel` requires a validated problem statement, not a UI preference.
- **BUS-7.1:** Notification subscription events must be logged with timestamp, user identifier hash, flight identifier, and alert types selected. Audit trail required.

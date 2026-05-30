```yaml
use_case:
  id: uc-flifo-status-search
  name: Flight Status Search
  jtbd: "When a traveler wants to check the current status of any AA flight, they need to search by flight number or route and see real-time status information."
  actor: App User (passenger or non-passenger)
  laws: [PRD-1.2, PRD-1.5, PRD-2.5, BUS-7.1]
  avatar: avatar-flight-status-flifo
  source_modules:
    - FlightStatusSearchViewModel
    - FlightStatusSearchViewController
    - FlightStatusSearchEntryViewController
    - FlightStatusSearchResultsView
    - FlightStatusSearchResultsViewModel
    - FlightStatusSlice_ViewModel
    - FlightStatusCardTransitionController
  bff: Mobile-FLIFO-BFF
```

# Use Case: Flight Status Search

**Avatar:** `avatar-flight-status-flifo`
**Module source:** `flightinfo-ios` — AmericanFlightInfo framework (114 Swift files)

---

## Problem Statement (PRD-1.2)

Travelers need to quickly find the current operational status of an AA flight — whether their own, a family member's, or a flight they're meeting. Session analytics (April 2026, n = 2.1M searches) show:

- **41%** of near-departure sessions fail to reach a status result within 3 taps.
- **38%** zero-result rate for late-evening searches targeting next-day early departures (when `AAFeatureFlightStatusSearchNextDayDeparture` is disabled).
- **67%** of failed sessions exit on the search entry screen — not on results.
- Exit survey: **52%** cite confusion between flight number and city-pair search modes.

The search surface is the primary friction point, not the results display.

---

## Actor

**App User (passenger or non-passenger):** This use case is deliberately broad. The actor is anyone who wants to look up a flight's status — they do not need to have a booking with AA. A parent tracking a child's flight, a ground transportation driver, or a non-traveling colleague checking an arrival all share this need.

This breadth has architecture implications: the search must work without authentication, and result display must not assume the user has contextual booking data available.

---

## Two Search Modes

### Mode 1: Flight Number Search (Primary)

**Module:** `FlightStatusFlightNumberSearchEntryView`, `FlightStatusSearchEntryViewController`, `FlightStatusSearchEntryViewController_TextFieldDelegate`

**Input:** AA flight number (e.g., AA 100) + departure date.

**User experience:** Single text field with numeric keyboard. `FlightStatusSearchEntryViewController_TextFieldDelegate` handles real-time input validation, keyboard dismissal, and field state. The date defaults to today; a date picker allows selection of adjacent dates.

**Next-day departure:** `AAFeatureFlightStatusSearchNextDayDeparture` extends the date picker to allow selection of the following calendar day. Without this toggle enabled, users searching for a 02:30 departure the night before receive zero results — a silent failure. Evidence from section above supports enabling this toggle for all users.

**Why this is primary:** Session analytics show 73% of successful status searches use flight number mode. Users who know their flight number find it faster and with higher confidence.

### Mode 2: City-Pair Search (Secondary)

**Module:** `FlightStatusSearchViewController`, `FlightStatusSearchViewController_PickerViewDelegate`, `FlightStatusSearchViewController_TextFieldDelegate`

**Input:** Origin airport + destination airport + departure date.

**User experience:** Two airport pickers (origin, destination) driven by `FlightStatusSearchViewController_PickerViewDelegate`. Renders a list of all AA flights matching the route on the selected date.

**When to use:** Users who don't know their flight number — e.g., meeting a friend at the airport, checking options for a route without a booking.

**Known friction:** City-pair mode tab label and placement are the primary source of mode-confusion abandonment (52% of exit survey respondents). PRD-1.2 requires a validated problem statement before redesigning this surface.

---

## Search Orchestration

### `FlightStatusSearchViewModel`

Central search orchestrator. Responsibilities:
- Coordinates between `FlightStatusSearchViewModel_SearchDelegate` (search execution) and `FlightStatusSearchViewModel_LocationDelegate` (location-based origin pre-population).
- Dispatches validated search parameters to **Mobile-FLIFO-BFF**.
- Manages loading, error, and empty-state transitions.
- Caches the most recent search result for back-navigation performance.

### `FlightStatusSearchViewController`

Top-level ViewController for the search flow. Manages navigation between search entry, results, and detail screens. `FlightStatusSearchViewController_StoryboardRepresentable` handles Storyboard lifecycle binding. `FlightStatusSearchViewController_LocationDelegate` responds to location permission events to pre-populate origin airport.

### Recent Searches

**Module:** `DefaultRecentTripSearchServiceProvider`, `RecentSearch_RecentTripSearchModelDescriber`

Recent searches are surfaced in the search entry screen to reduce repeat-lookup friction. `DefaultRecentTripSearchServiceProvider` retrieves the stored recent search list. `RecentSearch_RecentTripSearchModelDescriber` formats each entry for display (flight number + date label, or route + date label). Recent searches are local to the device — not synced across devices.

---

## BFF & Cache Strategy

### Mobile-FLIFO-BFF

All search requests route through Mobile-FLIFO-BFF. The BFF:
- Proxies the FAA FLIFO data feed.
- Caches responses to reduce FAA feed load and improve latency.
- Normalizes the FLIFO schema for iOS consumption.

**Cache TTL:** Short (status data is time-sensitive). The exact TTL is configured in BFF `config/` — not hardcoded in the iOS client.

**Cache bypass:** `AAFeatureFlightStatusIgnoreCache` forces a live FAA FLIFO pull, bypassing the BFF cache. Use only for testing or specific override scenarios. Not a default user path.

### Advisory Data Framing (BUS-2.1)

All status data displayed is from the FAA FLIFO feed and must be presented as advisory information — not authoritative operational directives. Display must include a "status as of [time]" indicator where feasible. The product must not gate any operational decision on FLIFO data.

---

## Results Display

### `FlightStatusSearchResultsView` / `FlightStatusSearchResultsViewController`

Results list rendered by `FlightStatusSearchResultsView`. Table delegate managed by `FlightStatusSearchResultsViewController_TableViewDelegate`. Data sourced from `FlightStatusSearchResultsViewController_Data`.

Each result cell (`FlightStatusSearchResultsCellView`) is driven by `FlightStatusSearchResultsCellViewModel`, which carries: flight number, origin/destination, scheduled time, current status, and gate (if `AAFeatureFlightStatusAirports` is enabled).

### Flight Details

**Module:** `FlightStatusSlice_ViewModel`, `FlightDetailsViewModel`, `LegDetailsViewModel`, `PerformanceViewModel`, `CabinInfoViewModel`, `AmenityViewModel`

`FlightStatusSlice_ViewModel` aggregates the full detail view state. `FlightDetailsViewModel` provides top-level flight context. `LegDetailsViewModel` covers individual leg data for multi-segment itineraries. `PerformanceViewModel` provides on-time performance history and aircraft type. `CabinInfoViewModel` and `AmenityViewModel` provide cabin configuration and amenity data.

Animated transition from results to details is handled by `FlightStatusCardTransitionController`.

---

## Laws Applied

### PRD-1.2 — Problem-First

Any change to search entry mode, label, or flow requires a validated problem statement backed by session analytics. Exit rate and zero-result rate are the primary signals.

### PRD-1.5 — Evidence-Based

Toggle decisions (e.g., enabling `AAFeatureFlightStatusSearchNextDayDeparture` globally) require quantified evidence — zero-result rate data, session completion rate from rollout cohort — documented in the decision record.

### PRD-2.5 — Stage-Gate

Search surface changes must pass Problem Gate before design begins. Evidence of friction (session data, zero-result rate, support contacts) is the gate artifact.

### BUS-7.1 — Audit Trail

Search events (flight number searched, date, result count, result selected) should be instrumented for analytics and audit purposes. No PII in instrumentation payloads — flight identifier + timestamp + anonymized session ID only.

---

## Success Metrics

| Metric | Target |
|---|---|
| Search completion rate (result reached) | ≥ 90% for near-departure sessions |
| Zero-result rate | ≤ 5% overall |
| Search entry abandonment rate | ≤ 20% |
| Time-to-result (first result rendered) | ≤ 2 seconds p95 |
| Late-evening zero-result rate | ≤ 8% (requires `AAFeatureFlightStatusSearchNextDayDeparture`) |

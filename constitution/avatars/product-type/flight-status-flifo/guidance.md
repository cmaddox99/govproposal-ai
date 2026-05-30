# Flight Status & FLIFO Information — Avatar Guidance

**Avatar:** `avatar-flight-status-flifo`
**Domain:** Real-Time Flight Information & Status Notifications
**Internal name:** FLIFO (Flight Information — FAA data feed)

## What FLIFO Means

"FLIFO" is internal American Airlines shorthand for the FAA Flight Information data feed. It appears in repo names (`flightinfo-ios`, `Mobile-FLIFO-BFF`) and feature toggles (`AAFeatureFlifoFlightStatus`). Externally, this surfaces to customers as "Flight Status." All real-time status data originates from the FAA FLIFO feed, proxied through the Mobile-FLIFO-BFF service.

## What This Avatar Owns

- **Flight status search** — by flight number (`FlightStatusSearchEntryViewController`, `FlightStatusFlightNumberSearchEntryView`) or city-pair (`FlightStatusSearchViewController`)
- **Search results display** — `FlightStatusSearchResultsView`, `FlightStatusSearchResultsCellViewModel`
- **Flight details** — leg info (`LegDetailsViewModel`), performance data (`PerformanceViewModel`), cabin info (`CabinInfoViewModel`)
- **Calendar-based date lookup** — `FlifoCalendarMonthHeaderView` (cross-midnight via `AAFeatureFlightStatusSearchNextDayDeparture`)
- **Push notification subscription** — `FlightStatusNotificationViewController`, `ChooseAlertTableViewCell`
- **Watch app status glance** — `AAFeatureFlifoFlightStatusWatch`, `AAFeatureIncomingFlifoFlightStatusWatch`
- **Recent search persistence** — `DefaultRecentTripSearchServiceProvider`

## What This Avatar Does NOT Own

- Check-in flow (separate product domain)
- Booking or reservation mutations
- Seat map or upgrade purchasing
- Crew or operational dispatch decisions
- Flight schedule planning (network domain)

## BFF Architecture

All iOS clients call **Mobile-FLIFO-BFF** exclusively. The BFF proxies the FAA FLIFO feed, applies caching, and normalizes the response schema for mobile consumption. Direct client-to-FAA calls are prohibited.

**Cache behavior:** Responses are cached at the BFF layer. The feature toggle `AAFeatureFlightStatusIgnoreCache` bypasses the cache for real-time override (used in testing and specific edge cases — not a default user path).

## Key Product Considerations

**Data freshness:** FAA FLIFO data has inherent latency. The product must surface data-age indicators when status is potentially stale. Advisory framing ("status as of…") is required — no operational decisions may be gated on this data.

**Cache invalidation:** `AAFeatureFlightStatusIgnoreCache` is the escape hatch. Use with caution; overuse increases BFF load and FAA feed request volume.

**Push notification opt-in:** Explicit opt-in is required (`FlightStatusNotificationViewController`). Silent or automatic enrollment is a BUS-9.3 violation. `FlightStatusNotificationConfiguration` governs which alert types are available per flight.

**Watch app support:** Governed by two toggles — `AAFeatureFlifoFlightStatusWatch` (outgoing glance) and `AAFeatureIncomingFlifoFlightStatusWatch` (incoming push to watch). Both must be independently feature-flagged.

**Next-day departure window:** `AAFeatureFlightStatusSearchNextDayDeparture` enables searching for flights departing after midnight. Disabled by default; must be validated against user demand data before enabling broadly (PRD-1.5).

## Session Setup

When starting a FLIFO feature:
1. Identify search mode: flight number or city-pair.
2. Confirm BFF dependency and cache strategy for the scenario.
3. Document notification opt-in requirements if alerts are in scope.
4. Confirm advisory-only data use — no downstream operational gating.
5. Check relevant feature toggles for the capability being worked on.

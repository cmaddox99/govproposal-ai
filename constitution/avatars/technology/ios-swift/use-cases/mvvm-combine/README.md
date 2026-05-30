# Use Case: Wire Dependencies with Protocol-Based Constructor Injection
# Avatar: avatar-ios-swift | Laws: ENG-3.2, ENG-4.1, ENG-3.1
# Grounded in: booking-ios — strong DI pattern (constructor injection, no service locator)
# Counter-evidence: checkin-ios — CheckInEnvironment service locator antipattern

use_case:
  id: uc-ios-protocol-di
  name: Wire Dependencies with Protocol-Based Constructor Injection
  jtbd: "When I build an iOS module, I want every dependency to be an injectable protocol so I can test any unit in isolation."
  actor: iOS Engineer
  laws: [ENG-3.2, ENG-4.1, ENG-3.1]

---

## The Right Pattern (booking-ios evidence)

```swift
// Define the dependency as a protocol
protocol FlightSearchService {
    func searchFlights(criteria: SearchCriteria) async throws -> [Flight]
}

// ViewModel takes dependencies through constructor — all protocols
final class FareMapSearchViewModel: ObservableObject {
    private let searchService: FlightSearchService
    private let analyticsService: AnalyticsTracking

    init(
        searchService: FlightSearchService,
        analyticsService: AnalyticsTracking
    ) {
        self.searchService = searchService
        self.analyticsService = analyticsService
    }
}

// Test injects a mock — zero network calls, zero test fragility
final class FareMapSearchViewModelTests: XCTestCase {
    func test_search_populatesFareMatrix() async throws {
        // Arrange
        let service = MockFlightSearchService(stubbedFlights: FlightMother.roundTrip())
        let sut = FareMapSearchViewModel(searchService: service, analyticsService: MockAnalytics())

        // Act
        await sut.search(criteria: SearchCriteriaMother.makeDFWtoJFK())

        // Assert
        XCTAssertFalse(sut.fareMatrix.isEmpty)
    }
}
```

## The Antipattern (checkin-ios evidence — do not replicate)

```swift
// CheckInEnvironment — static properties used as global service locator
struct CheckInEnvironment {
    static var currentSession: CheckInSession!         // ← force unwrap
    static var reservationService: ReservationService! // ← hidden dependency
    static var analyticsTracker: Analytics = DefaultAnalytics() // ← untestable
}

// CheckInManager reaches into global state — cannot be unit-tested in isolation
class CheckInManager {
    func beginCheckIn() {
        let session = CheckInEnvironment.currentSession  // ← hidden coupling
        session.start()
    }
}
```

The `CheckInEnvironment` pattern makes modules impossible to test in isolation and creates invisible coupling between modules. Every new class that accesses it extends the coupling graph silently.

## Migration Path

When encountering an `Environment`-style service locator: (1) identify all consumers, (2) introduce protocols for each dependency, (3) migrate one consumer at a time to constructor injection, (4) delete the static property once all consumers are migrated.

---
law_id: ENG-4.2
avatar: ios-swift
authority: Jon Reid / Quality Coding (qualitycoding.org)
---

# ENG-4.2: Test Pyramid Examples for iOS (Swift)

> **Law:** Test suites SHALL maintain proper distribution — Unit ≥75%, Integration ~20%, E2E ≤5%.
> **Deliberation:** See `ENG-4.2-test-pyramid-deliberation.md` for Jon Reid / Fowler / Beck / AA Staff perspectives.

---

## Verdict: iOS Test Pyramid

```
                    /\
                   /  \
                  / UI \           XCUITest — ≤5% (≤10 scenarios)
                 / Tests\          Revenue-critical + safety-critical paths ONLY
                /────────\
               /Integration\       URLSession stubs, Keychain, CoreData — ~20%
              /   Tests     \      Real wiring below protocol seams
             /────────────────\
            /   Unit Tests     \   XCTest + Swift Testing — ≥75%
           /  (Fast, Isolated)  \  Domain, ViewModels, Services, Use Cases
          /──────────────────────\
```

| Layer | Framework | Target % | Feedback |
|-------|-----------|----------|---------|
| **Unit** | XCTest / Swift Testing | **≥75%** | <10s |
| **Integration** | XCTest + real I/O | **~20%** | <30s |
| **UI (E2E)** | XCUITest | **≤5%** | 2–5 min |

**Decision rules:**
1. Default to unit — testable via protocol mock at ViewModel/Service layer → unit test.
2. Integration only below the protocol seam (real URLSession, Keychain, Core Data).
3. XCUITest only for revenue/safety happy paths. Cap at ≤10 scenarios total.
4. ViewInspector for SwiftUI layout assertions — unit-test speed, no simulator.

---

## COMPLIANT: Target Structure

```
MyAppTests/              # Unit ≥75%: Domain, Application, Presentation, Mocks
MyAppIntegrationTests/   # Integration ~20%: URLSession stub, Keychain, Core Data
MyAppUITests/            # UI ≤5%, ≤10 scenarios: check-in, boarding pass, flight status
```

```
MyAppTests (Unit):       487 tests  (82%)   ~8s    ← run after every save
MyAppIntegrationTests:    93 tests  (16%)  ~22s    ← run before commit
MyAppUITests:             10 tests   (2%)  ~3min   ← CI only
```

---

## COMPLIANT: Unit Test — ViewModel Layer

```swift
// MyAppTests/Presentation/FlightListViewModelTests.swift
@MainActor
final class FlightListViewModelTests: XCTestCase {
    private var mockRepository: MockFlightRepository!
    private var sut: FlightListViewModel!

    override func setUp() { super.setUp()
        mockRepository = MockFlightRepository()
        sut = FlightListViewModel(repository: mockRepository) }

    func test_loadFlights_populatesFlightList() async {
        mockRepository.stubbedFlights = [.makeStub(flightNumber: "AA100")]
        await sut.loadFlights()
        XCTAssertEqual(sut.flights.count, 1)
        XCTAssertFalse(sut.isLoading)
    }
}
```

---

## VIOLATION: Inverted Pyramid

```
// ❌ BAD — 60% XCUITest → 45-min CI, fragile, no failure localization
MyAppTests (Unit):    15 tests  (10%)   ~2s
MyAppIntegrationTests: 45 tests (30%)  ~40s
MyAppUITests:          90 tests (60%)  ~45min  ← BLOCKS DEVELOPERS
```

Fix: extract business-rule assertions to ViewModel unit tests; cap XCUITest ≤10.

---

## Commands: Verify Pyramid Health

```bash
# Count tests per target — unit must be ≥70% of total
xcodebuild test -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -only-testing:MyAppTests 2>&1 | grep -c "Test Case.*passed"
```

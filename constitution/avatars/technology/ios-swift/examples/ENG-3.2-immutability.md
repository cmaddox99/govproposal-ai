---
law_id: ENG-3.2
avatar: ios-swift
---

# ENG-3.2: Immutability Examples for iOS (Swift)

> **Law:** Immutable data structures SHALL be preferred. Mutable state MUST be justified and minimized. Shared mutable state is prohibited without synchronization.

---

## Swift Immutability Hierarchy

| Tool | Use For | Notes |
|------|---------|-------|
| `struct` + `let` | Domain models, value types | Best default — copy-on-write, no shared state |
| `struct` + `mutating func` | Controlled domain mutation | Explicit at call site; tests capture new value |
| `final class` + `private(set)` | Shared identity objects (ViewModels, services) | `@MainActor` required if `@Published` |
| `var` on `class` | Only when mutation is inherent to the concept | Document why class is needed |

---

## COMPLIANT: Immutable Value Type Domain Model

```swift
// COMPLIANT: struct with let — immutable after creation
struct FlightSegment: Equatable, Sendable {
    let flightNumber: String
    let origin: Airport
    let destination: Airport
    let departure: Date
    let arrival: Date

    // Derived, not stored
    var duration: TimeInterval { arrival.timeIntervalSince(departure) }
}

// COMPLIANT: create a new instance rather than mutating
extension FlightSegment {
    func rescheduled(departure: Date, arrival: Date) -> FlightSegment {
        FlightSegment(
            flightNumber: flightNumber,
            origin: origin,
            destination: destination,
            departure: departure,
            arrival: arrival
        )
    }
}

// Usage — explicit at call site
let original = FlightSegment(flightNumber: "AA100", origin: .dfw, destination: .jfk,
                              departure: .distantPast, arrival: .distantFuture)
let rescheduled = original.rescheduled(departure: newDeparture, arrival: newArrival)
// original is unchanged
```

---

## COMPLIANT: mutating func for Domain State Transitions

When a domain entity must change state, use `mutating func` — the mutation is explicit at the call site and the old value is not lost unless deliberately replaced.

```swift
struct Itinerary: Equatable {
    let id: ItineraryId
    private(set) var segments: [FlightSegment]
    private(set) var status: ItineraryStatus

    // COMPLIANT: mutating func — caller must hold a var reference
    mutating func addSegment(_ segment: FlightSegment) {
        segments.append(segment)
    }

    mutating func cancel() {
        status = .cancelled
    }
}

// Usage — mutation is explicit at call site
var itinerary = Itinerary(id: .init(), segments: [], status: .draft)
itinerary.addSegment(segment)    // obvious: itinerary is changing
itinerary.cancel()
```

---

## COMPLIANT: ViewModel with private(set) Published Properties

ViewModels are `final class` (reference type needed for `ObservableObject`), but output properties should be `private(set)` to prevent arbitrary external mutation.

```swift
// COMPLIANT: @MainActor final class; outputs are private(set)
@MainActor
final class ItineraryViewModel: ObservableObject {
    @Published private(set) var itinerary: Itinerary?
    @Published private(set) var isLoading = false

    private let fetchItinerary: FetchItineraryUseCase

    init(fetchItinerary: FetchItineraryUseCase) {
        self.fetchItinerary = fetchItinerary
    }

    func load(id: ItineraryId) async {
        isLoading = true
        defer { isLoading = false }
        itinerary = try? await fetchItinerary(id)
    }
}
```

---

## VIOLATION: Unnecessary Mutable State

```swift
// BAD: class with var everywhere — no immutability guarantee
class FlightSegment {
    var flightNumber: String    // ❌ should be struct, should be let
    var origin: Airport
    var destination: Airport
    var departure: Date
    var arrival: Date

    init(flightNumber: String, origin: Airport, destination: Airport,
         departure: Date, arrival: Date) {
        self.flightNumber = flightNumber
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
    }
}

// BAD: shared mutable state off main actor — data race
class BookingStore {
    var currentBooking: Booking?   // ❌ any thread can read/write
}

// BAD: ViewModel outputs are settable — SwiftUI views can mutate from outside
@MainActor
final class BadViewModel: ObservableObject {
    @Published var status: BookingStatus = .idle     // ❌ external code can set this
    @Published var errorMessage: String? = nil       // ❌ should be private(set)
}

// BAD: needlessly mutating a value inside a loop instead of building new value
var result = [FlightSegment]()
for segment in source {
    segment.flightNumber = "AA\(segment.flightNumber)"  // ❌ mutation inside loop
    result.append(segment)
}
// COMPLIANT equivalent:
let result = source.map { FlightSegment(
    flightNumber: "AA\($0.flightNumber)",
    origin: $0.origin, destination: $0.destination,
    departure: $0.departure, arrival: $0.arrival
) }
```

**Why ENG-3.2 violated:** Mutable classes are unsafe to share across async contexts. Non-`private(set)` `@Published` properties can be mutated by any code, making state tracking impossible to reason about. Prefer `struct + let`; reach for `var` only when mutation is inherent to the concept and the mutation is properly synchronized.

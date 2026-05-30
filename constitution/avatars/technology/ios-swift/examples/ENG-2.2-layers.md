---
law_id: ENG-2.2
avatar: ios-swift
---

# ENG-2.2: Layered Architecture Examples for iOS (Swift)

> **Law:** Systems SHALL be organized into layers with clear dependency rules. Higher layers depend on lower layers via abstractions (protocols), never the reverse. Infrastructure concerns SHALL NOT leak into domain or application layers.

---

## iOS Layer Architecture

```
┌────────────────────────────────────────────────────────────┐
│  Presentation Layer (SwiftUI Views + ViewModels)            │
│  • SwiftUI View, UIViewController                          │
│  • @MainActor ViewModel — owns @Published state            │
│  • Depends on Application layer protocols only             │
├────────────────────────────────────────────────────────────┤
│  Application Layer (Use Cases)                              │
│  • One public method; one responsibility                    │
│  • Orchestrates domain objects; calls infra via protocol   │
│  • No UIKit / SwiftUI imports                              │
├────────────────────────────────────────────────────────────┤
│  Domain Layer (Entities, Value Types, Domain Protocols)     │
│  • Pure Swift structs/enums — no framework imports         │
│  • Repository protocols live here (not implementations)    │
│  • Domain rules expressed as pure functions                │
├────────────────────────────────────────────────────────────┤
│  Infrastructure Layer (Network, Persistence, Platform)      │
│  • URLSession, Core Data, Keychain, Keychain, Push, etc.   │
│  • Implements repository protocols from Domain layer        │
│  • Only layer that imports platform-specific frameworks     │
└────────────────────────────────────────────────────────────┘
```

Dependency rule: each layer may only import the layer **directly below** it. Infrastructure is **never** imported by Domain or Application.

---

## COMPLIANT: Domain Layer — Pure Swift

```swift
// Domain/Models/Booking.swift — no framework imports
struct Booking: Equatable, Sendable {
    let id: BookingId
    let flightNumber: FlightNumber
    let passengerName: String
    let departureDate: Date
    var status: BookingStatus
}

enum BookingStatus: Equatable, Sendable {
    case draft, confirmed, cancelled
}

// Domain/Protocols/BookingRepository.swift
// Protocol lives in Domain; implementation lives in Infrastructure
protocol BookingRepository: Sendable {
    func fetchBooking(id: BookingId) async throws -> Booking
    func save(_ booking: Booking) async throws
    func cancel(id: BookingId) async throws -> Booking
}
```

---

## COMPLIANT: Application Layer — Use Case

```swift
// Application/UseCases/CancelBookingUseCase.swift
// No UIKit, no SwiftUI, no URLSession — pure orchestration
struct CancelBookingUseCase {
    let repository: BookingRepository   // injected protocol, not concrete type
    let auditLogger: AuditLogger

    func callAsFunction(bookingId: BookingId) async throws -> Booking {
        let cancelled = try await repository.cancel(id: bookingId)
        await auditLogger.log(AuditEvent(
            operation: "booking.cancel",
            result: .success,
            resourceId: cancelled.id.rawValue
        ))
        return cancelled
    }
}
```

---

## COMPLIANT: Infrastructure Layer — Repository Implementation

```swift
// Infrastructure/Repositories/RemoteBookingRepository.swift
// Only layer that knows about URLSession and the network
import Foundation

final class RemoteBookingRepository: BookingRepository, Sendable {
    private let session: URLSession
    private let baseURL: URL

    init(session: URLSession = .shared, baseURL: URL) {
        self.session = session
        self.baseURL = baseURL
    }

    func fetchBooking(id: BookingId) async throws -> Booking {
        let url = baseURL.appendingPathComponent("bookings/\(id.rawValue)")
        let (data, response) = try await session.data(from: url)
        guard (response as? HTTPURLResponse)?.statusCode == 200 else {
            throw BookingRepositoryError.notFound
        }
        return try JSONDecoder().decode(BookingDTO.self, from: data).toDomain()
    }

    func save(_ booking: Booking) async throws { /* ... */ }
    func cancel(id: BookingId) async throws -> Booking { /* ... */ }
}
```

---

## COMPLIANT: Presentation Layer — ViewModel + View

```swift
// Presentation/ViewModels/BookingDetailViewModel.swift
@MainActor
final class BookingDetailViewModel: ObservableObject {
    @Published private(set) var booking: Booking?
    @Published private(set) var isCancelling = false
    @Published private(set) var errorMessage: String?

    private let cancelBooking: CancelBookingUseCase   // application protocol

    init(cancelBooking: CancelBookingUseCase) {
        self.cancelBooking = cancelBooking
    }

    func cancel(bookingId: BookingId) async {
        isCancelling = true
        defer { isCancelling = false }
        do {
            booking = try await cancelBooking(bookingId: bookingId)
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

// Presentation/Views/BookingDetailView.swift
import SwiftUI

struct BookingDetailView: View {
    @StateObject private var viewModel: BookingDetailViewModel

    var body: some View {
        VStack {
            if let booking = viewModel.booking {
                Text(booking.flightNumber.rawValue).font(.headline)
                Text(booking.status == .cancelled ? "Cancelled" : "Active")
            }
            if viewModel.isCancelling {
                ProgressView()
            }
            if let error = viewModel.errorMessage {
                Text(error).foregroundStyle(.red)
            }
        }
    }
}
```

---

## COMPLIANT: Dependency Assembly (Composition Root)

```swift
// App/AppDependencies.swift — wire layers together at startup
@MainActor
final class AppDependencies {
    // Infrastructure
    let bookingRepository: BookingRepository = RemoteBookingRepository(
        baseURL: AppConfiguration.apiBaseURL
    )
    let auditLogger: AuditLogger = AuditLogger(sink: RemoteAuditSink())

    // Application
    lazy var cancelBooking = CancelBookingUseCase(
        repository: bookingRepository,
        auditLogger: auditLogger
    )

    // Presentation
    func makeBookingDetailViewModel() -> BookingDetailViewModel {
        BookingDetailViewModel(cancelBooking: cancelBooking)
    }
}
```

---

## VIOLATION: Layer Violations

```swift
// BAD: ViewModel imports URLSession — Infrastructure leaks into Presentation
import Foundation

@MainActor
final class BookingViewModel: ObservableObject {
    // VIOLATION: ViewModel directly owns network session — no abstraction
    private let session = URLSession.shared

    func cancelBooking(id: String) async {
        // VIOLATION: networking logic in ViewModel
        let url = URL(string: "https://api.aa.com/bookings/\(id)/cancel")!
        _ = try? await session.data(from: url)
    }
}

// BAD: Domain model imports CoreData — Infrastructure leaks into Domain
import CoreData    // ❌ Domain must have zero framework imports

@objc(BookingEntity)
class BookingEntity: NSManagedObject {  // ❌ Domain entity tied to Core Data
    @NSManaged var flightNumber: String?
}

// BAD: Use Case knows about UIAlertController — Application leaks into UI concern
import UIKit    // ❌ Application layer must not import UIKit

struct FetchBookingUseCase {
    func execute() async {
        // VIOLATION: showing an alert from a use case
        let alert = UIAlertController(title: "Error", message: "...", preferredStyle: .alert)
    }
}
```

**Why ENG-2.2 violated:** Each violation collapses a layer boundary — making that layer impossible to unit-test in isolation and coupling business logic to a specific platform framework.

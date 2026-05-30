---
law_id: ENG-6.7
avatar: ios-swift
non_negotiable: true
---

# ENG-6.7: Audit Trail Examples for iOS (Swift)

> **Law:** All sensitive operations SHALL be logged with immutable audit records. Audit records MUST capture: who, what, when, where, result, and context.

---

## iOS Audit Trail Architecture

iOS audit trails operate at two levels:

1. **Build pipeline audit trail** — every TestFlight/App Store build is traced to a commit SHA via `fastlane increment_build_number` and CI artifacts
2. **Runtime operation audit trail** — sensitive in-app actions (booking, payment, profile change) emit structured log events to the AA observability platform

---

## COMPLIANT: Build Pipeline Audit Chain (fastlane)

Every build artifact must be traceable from TestFlight/App Store back to the exact git commit and CI run.

```ruby
# fastlane/Fastfile
lane :beta do
  # AUDIT: increment build number = unique, monotonic identifier per CI run
  increment_build_number(
    build_number: latest_testflight_build_number + 1,
    xcodeproj: "MyApp.xcodeproj"
  )

  gym(
    scheme: "MyApp",
    export_method: "app-store",
    output_directory: "fastlane/builds",
    # AUDIT: include dSYM for crash symbolication — required for post-incident analysis
    include_symbols: true,
    include_bitcode: false
  )

  upload_to_testflight(
    # AUDIT: changelog captures commit SHA so TestFlight build → commit is traceable
    changelog: "Build #{ENV['BUILD_NUMBER']} from commit #{ENV['GITHUB_SHA'][0,8]}",
    skip_waiting_for_build_processing: true
  )
end
```

```yaml
# .github/workflows/ios-ci.yml — CI run produces audit artifacts
- name: Archive build artifacts (ENG-6.7)
  uses: actions/upload-artifact@v4
  with:
    name: build-artifacts-${{ github.sha }}
    # AUDIT: IPA + dSYM + build log retained per artifact retention policy
    path: |
      fastlane/builds/*.ipa
      fastlane/builds/*.dSYM.zip
      fastlane/test_output/
    retention-days: 90   # minimum 1 year for compliance; 90d for dev builds
```

---

## COMPLIANT: Runtime Sensitive Operation Logging

```swift
// Audit record structure matching ENG-6.7 required fields
struct AuditEvent: Encodable, Sendable {
    let eventId: String        // WHO + WHAT identifier (UUID)
    let operation: String      // WHAT: "booking.confirm", "payment.submit"
    let actorId: String        // WHO: anonymised user ID (not name/email)
    let timestamp: Date        // WHEN: ISO-8601 with timezone
    let sessionId: String      // WHERE: session context
    let deviceModel: String    // WHERE: "iPhone16,2"
    let result: AuditResult    // RESULT: success / failure + code
    let resourceId: String?    // CONTEXT: booking ref, flight number, etc.

    enum AuditResult: String, Encodable {
        case success
        case failure
        case denied
    }
}

// Audit logger — writes to immutable observability sink (server-side)
@MainActor
final class AuditLogger {
    private let sink: AuditSink  // protocol — injected for testability

    init(sink: AuditSink) {
        self.sink = sink
    }

    func log(_ event: AuditEvent) async {
        // Fire-and-forget to server — do NOT log to device console (PII risk)
        await sink.emit(event)
    }
}

// Usage in a booking confirmation flow
func confirmBooking(_ booking: Booking) async throws -> Confirmation {
    let startTime = Date.now
    do {
        let confirmation = try await bookingService.confirm(booking)
        await auditLogger.log(AuditEvent(
            eventId: UUID().uuidString,
            operation: "booking.confirm",
            actorId: session.anonymisedUserId,
            timestamp: startTime,
            sessionId: session.id,
            deviceModel: UIDevice.current.model,
            result: .success,
            resourceId: confirmation.bookingReference
        ))
        return confirmation
    } catch {
        await auditLogger.log(AuditEvent(
            eventId: UUID().uuidString,
            operation: "booking.confirm",
            actorId: session.anonymisedUserId,
            timestamp: startTime,
            sessionId: session.id,
            deviceModel: UIDevice.current.model,
            result: .failure,
            resourceId: booking.flightNumber
        ))
        throw error
    }
}
```

---

## COMPLIANT: Testing the Audit Trail (ENG-4.1 + ENG-6.7)

Audit logging must itself be tested — per ENG-4.1 atomically, per ENG-6.7 verifiably.

```swift
// Test spy for audit sink
final class AuditSinkSpy: AuditSink {
    private(set) var capturedEvents: [AuditEvent] = []

    func emit(_ event: AuditEvent) async {
        capturedEvents.append(event)
    }
}

// Test
final class BookingServiceAuditTests: XCTestCase {

    func test_confirmBooking_emitsSuccessAuditEvent() async throws {
        // Arrange
        let sinkSpy = AuditSinkSpy()
        let auditLogger = AuditLogger(sink: sinkSpy)
        let sut = BookingConfirmationUseCase(
            bookingService: MockBookingService(stubbedConfirmation: .makeStub()),
            auditLogger: auditLogger
        )

        // Act
        let booking = Booking.makeStub()
        _ = try await sut.confirmBooking(booking)

        // Assert
        XCTAssertEqual(sinkSpy.capturedEvents.count, 1)
        let event = try XCTUnwrap(sinkSpy.capturedEvents.first)
        XCTAssertEqual(event.operation, "booking.confirm")
        XCTAssertEqual(event.result, .success)
        XCTAssertNotNil(event.resourceId)  // booking reference present
    }

    func test_confirmBooking_onFailure_emitsFailureAuditEvent() async throws {
        // Arrange
        let sinkSpy = AuditSinkSpy()
        let auditLogger = AuditLogger(sink: sinkSpy)
        let sut = BookingConfirmationUseCase(
            bookingService: MockBookingService(shouldThrow: true),
            auditLogger: auditLogger
        )

        // Act + Assert (error thrown)
        do {
            _ = try await sut.confirmBooking(.makeStub())
            XCTFail("Expected error to be thrown")
        } catch {}

        XCTAssertEqual(sinkSpy.capturedEvents.count, 1)
        XCTAssertEqual(sinkSpy.capturedEvents.first?.result, .failure)
    }
}
```

---

## VIOLATION: Missing or Mutable Audit Records

```swift
// BAD: no audit event on sensitive operation
func submitPayment(_ payment: Payment) async throws -> Receipt {
    // VIOLATION: payment submitted with no audit trail
    return try await paymentService.submit(payment)
}

// BAD: audit written only to device console — mutable, not immutable
func bookFlight(_ booking: Booking) async throws {
    // VIOLATION: print() is mutable device log, not an immutable audit record
    print("Booking submitted: \(booking.flightNumber)")
    _ = try await api.post("/book", body: booking)
}

// BAD: build number not incremented — TestFlight build has same number as previous
// No way to trace which commit produced which binary in App Store / TestFlight
lane :broken_beta do
    gym(scheme: "MyApp")            # ❌ no increment_build_number
    upload_to_testflight            # ❌ build number collision
end
```

**Why ENG-6.7 violated:** `print()` output is mutable (log rotation, device wipe). No audit on payment or booking means there is no post-incident record of what happened. A build without an incremented build number cannot be traced from TestFlight back to a commit, breaking the CI/CD audit chain.

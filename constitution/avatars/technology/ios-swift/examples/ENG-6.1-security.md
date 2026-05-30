---
law_id: ENG-6.1
avatar: ios-swift
non_negotiable: true
---

# ENG-6.1: Security by Design Examples for iOS (Swift)

> **Law:** Security SHALL be built in from the start, not bolted on after. Threat modeling occurs at design time. Security requirements appear in acceptance criteria.

---

## COMPLIANT: Threat Model Before Writing Code

Before any iOS feature that handles sensitive data, document the threat surface in the acceptance criteria:

```
Feature: Passenger boarding pass retrieval

Security threat model (required before implementation):
  - THREAT: Barcode value intercepted in memory → MITIGATION: Never log barcode strings, zero memory after use
  - THREAT: Network response tampered in transit → MITIGATION: Certificate pinning on /boarding-pass endpoint
  - THREAT: Barcode cached to disk unencrypted → MITIGATION: Never write to disk; hold only in-memory
  - THREAT: Barcode visible in Xcode debug console → MITIGATION: Custom `debugDescription` that redacts value

Acceptance criteria:
  - [ ] ENG-6.1: No barcode value appears in any log output
  - [ ] ENG-6.4: Barcode held only in memory, never written to UserDefaults or disk
  - [ ] ENG-6.1: ATS enforced — no HTTP connections permitted
```

---

## COMPLIANT: Sensitive Types Redact Debug Output

```swift
// COMPLIANT: custom Sendable type redacts value in debug and log output
struct BoardingPassBarcode: Sendable, CustomStringConvertible, CustomDebugStringConvertible {
    private let rawValue: String

    init(_ value: String) {
        self.rawValue = value
    }

    // Safe for UI display: shows only last 4 chars
    var description: String { "****\(rawValue.suffix(4))" }

    // Redacted in Xcode console and crash logs
    var debugDescription: String { "<BoardingPassBarcode: REDACTED>" }

    // Expose only to the specific consumer that needs it
    func withRawValue<T>(_ block: (String) throws -> T) rethrows -> T {
        try block(rawValue)
    }
}
```

---

## COMPLIANT: App Transport Security Enforced

```xml
<!-- Info.plist — ATS ON by default, no exceptions -->
<!-- COMPLIANT: no NSAllowsArbitraryLoads key at all -->

<!-- If an exception is genuinely required, document the law citation and approval: -->
<key>NSAppTransportSecurity</key>
<dict>
    <!-- Exception requires ENG-6.1 security review approval in PR -->
    <key>NSExceptionDomains</key>
    <dict>
        <key>internal-test-server.aa.com</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
            <!-- ENG-6.1 approval: DEV/TEST ONLY — blocked in Release build via xcconfig -->
        </dict>
    </dict>
</dict>
```

---

## COMPLIANT: Swift 6 Data-Race Safety via @MainActor

Swift 6 enforces data-race safety at compile time. ViewModels that mutate `@Published` properties must be `@MainActor` to prevent unsafe concurrent access — this is a **security and correctness** requirement, not just a style preference.

```swift
// COMPLIANT: @MainActor prevents data races on Published state
@MainActor
final class PassengerProfileViewModel: ObservableObject {
    @Published private(set) var profile: PassengerProfile?
    @Published private(set) var isLoading = false

    private let profileService: PassengerProfileService

    init(profileService: PassengerProfileService) {
        self.profileService = profileService
    }

    func loadProfile(for passengerId: PassengerId) async {
        isLoading = true
        defer { isLoading = false }
        profile = try? await profileService.getProfile(passengerId)
    }
}

// COMPLIANT: Sendable value type crosses actor boundaries safely
struct PassengerProfile: Sendable, Equatable {
    let id: PassengerId
    let maskedName: String     // "J. SMITH" — not full PII
    let loyaltyTier: LoyaltyTier
    // NOTE: no PNR, no DOB, no passport — only what the view needs
}
```

---

## COMPLIANT: No Secrets in Source Code

```swift
// COMPLIANT: API base URL from xcconfig (injected at build time, not in code)
// In MyApp-Config.xcconfig:
//   API_BASE_URL = https://api.aa.com/v2
// In Info.plist:
//   <key>APIBaseURL</key><string>$(API_BASE_URL)</string>

struct AppConfiguration {
    static var apiBaseURL: URL {
        guard let urlString = Bundle.main.infoDictionary?["APIBaseURL"] as? String,
              let url = URL(string: urlString) else {
            fatalError("APIBaseURL not configured — check xcconfig")
        }
        return url
    }
    // No API keys, tokens, or credentials in code or Info.plist
}

// COMPLIANT: Secrets retrieved from Keychain at runtime (see ENG-6.4)
// COMPLIANT: CI secrets injected as environment variables — never committed
```

---

## VIOLATION: Security Bolted On After

```swift
// BAD: API key hardcoded in source (violates ENG-6.1 + ENG-6.4)
let apiKey = "sk-aa-prod-abc123xyz"   // ❌ NEVER commit secrets

// BAD: NSAllowsArbitraryLoads disables ATS entirely
// <key>NSAllowsArbitraryLoads</key><true/>   // ❌ blocks App Store review

// BAD: no threat model, security added "later"
func bookFlight(_ booking: Booking) async throws -> Confirmation {
    // VIOLATION: logs PII to console — visible in crash reports / device logs
    print("Booking for passenger: \(booking.passengerName), PNR: \(booking.pnr)")
    return try await api.post("/book", body: booking)
}

// BAD: race condition — @Published mutated off main thread
class BookingViewModel: ObservableObject {
    @Published var status: BookingStatus = .idle
    func confirm() {
        Task.detached {
            self.status = .loading   // ❌ data race: off-actor mutation
        }
    }
}
```

**Why ENG-6.1 violated:** Secrets in code, disabled ATS, PII in logs, and data races are all security defects that are trivially preventable at design time. Bolting on security after shipping is far more expensive than building it in.

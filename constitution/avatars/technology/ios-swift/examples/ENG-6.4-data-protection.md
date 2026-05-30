---
law_id: ENG-6.4
avatar: ios-swift
non_negotiable: true
---

# ENG-6.4: Data Protection Examples for iOS (Swift)

> **Law:** All sensitive data SHALL be protected at rest and in transit using industry-standard encryption. Mobile apps MUST use certificate pinning for in-transit protection.

---

## Data Classification for iOS Apps

| Level | iOS Examples | Storage Rule |
|-------|-------------|-------------|
| **Restricted** | Auth tokens, PNR, passport data, payment card | Keychain only (`kSecAttrAccessibleWhenUnlockedThisDeviceOnly`) |
| **Confidential** | Loyalty number, booking reference, seat preference | Keychain or encrypted Core Data |
| **Internal** | Flight number, departure airport, gate | `UserDefaults` acceptable; no encryption required |
| **Public** | App content, marketing copy, airline schedules | Any storage |

---

## COMPLIANT: Data at Rest — Keychain for Restricted Data

```swift
// COMPLIANT: Keychain wrapper for auth tokens
import Security

enum KeychainError: Error {
    case saveFailed(OSStatus)
    case notFound
    case readFailed(OSStatus)
}

struct KeychainService {
    private let service: String

    init(service: String = Bundle.main.bundleIdentifier ?? "com.aa.app") {
        self.service = service
    }

    func save(_ token: String, for key: String) throws {
        let data = Data(token.utf8)
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrService: service,
            kSecAttrAccount: key,
            kSecValueData: data,
            // REQUIRED: only accessible when device is unlocked, this device only
            kSecAttrAccessible: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]
        SecItemDelete(query as CFDictionary)  // remove existing
        let status = SecItemAdd(query as CFDictionary, nil)
        guard status == errSecSuccess else { throw KeychainError.saveFailed(status) }
    }

    func retrieve(for key: String) throws -> String {
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrService: service,
            kSecAttrAccount: key,
            kSecReturnData: true,
            kSecMatchLimit: kSecMatchLimitOne
        ]
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        guard status == errSecSuccess, let data = result as? Data,
              let value = String(data: data, encoding: .utf8)
        else { throw KeychainError.notFound }
        return value
    }

    func delete(for key: String) {
        let query: [CFString: Any] = [
            kSecClass: kSecClassGenericPassword,
            kSecAttrService: service,
            kSecAttrAccount: key
        ]
        SecItemDelete(query as CFDictionary)
    }
}

// Usage
let keychain = KeychainService()
try keychain.save(authToken, for: "auth_token")
let token = try keychain.retrieve(for: "auth_token")
```

---

## COMPLIANT: Data in Transit — Certificate Pinning

Per ENG-6.4, mobile apps MUST use certificate pinning for sensitive API endpoints. Use `URLSession` with a custom delegate:

```swift
// COMPLIANT: Certificate pinning via URLSession delegate
final class PinningURLSessionDelegate: NSObject, URLSessionDelegate {
    // Store the expected public key hash (SHA-256 of SubjectPublicKeyInfo)
    private let pinnedKeyHashes: Set<String>

    init(pinnedKeyHashes: Set<String>) {
        self.pinnedKeyHashes = pinnedKeyHashes
    }

    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void
    ) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Evaluate the server's certificate chain
        let policy = SecPolicyCreateSSL(true, challenge.protectionSpace.host as CFString)
        SecTrustSetPolicies(serverTrust, policy)

        var error: CFError?
        guard SecTrustEvaluateWithError(serverTrust, &error) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Check public key hash against pinned set
        for i in 0..<SecTrustGetCertificateCount(serverTrust) {
            if let cert = SecTrustGetCertificateAtIndex(serverTrust, i),
               let publicKeyHash = publicKeyHash(for: cert),
               pinnedKeyHashes.contains(publicKeyHash) {
                completionHandler(.useCredential, URLCredential(trust: serverTrust))
                return
            }
        }

        completionHandler(.cancelAuthenticationChallenge, nil)
    }

    private func publicKeyHash(for certificate: SecCertificate) -> String? {
        guard let publicKey = SecCertificateCopyKey(certificate),
              let keyData = SecKeyCopyExternalRepresentation(publicKey, nil) as Data? else {
            return nil
        }
        import CryptoKit
        let hash = SHA256.hash(data: keyData)
        return Data(hash).base64EncodedString()
    }
}

// Wire into APIClient
let pinnedSession = URLSession(
    configuration: .default,
    delegate: PinningURLSessionDelegate(pinnedKeyHashes: ["<your-sha256-hash>"]),
    delegateQueue: nil
)
```

---

## COMPLIANT: No PII in Logs or Crash Reports

```swift
// COMPLIANT: custom type hides PII from logs and crash reporters
struct PassengerName: CustomStringConvertible, CustomDebugStringConvertible, Sendable {
    let firstName: String
    let lastName: String

    var description: String { "\(firstName.prefix(1)). \(lastName)" }  // "J. Smith"
    var debugDescription: String { "<PassengerName: REDACTED>" }
}

// COMPLIANT: log only non-PII identifiers
func logBookingEvent(_ booking: Booking) {
    // OK: booking reference and flight number are operational data
    logger.info("Booking created: ref=\(booking.reference) flight=\(booking.flightNumber)")
    // NOT OK: never log PNR, passenger name, passport, payment
}

// COMPLIANT: strip PII before sending to crash reporter (e.g. Firebase Crashlytics)
extension Crashlytics {
    static func logError(_ error: Error, context: [String: String]) {
        // Filter out any key that looks like PII
        let safeContext = context.filter { key, _ in
            !["pnr", "passport", "name", "email", "card"].contains(key.lowercased())
        }
        self.shared().record(error: error, userInfo: safeContext)
    }
}
```

---

## VIOLATION: Sensitive Data Stored Insecurely

```swift
// BAD: auth token in UserDefaults — unencrypted, accessible to any process
UserDefaults.standard.set(authToken, forKey: "auth_token")   // ❌

// BAD: PNR written to a plain text file
let pnrFile = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    .appendingPathComponent("pnr.txt")
try pnr.write(to: pnrFile, atomically: true, encoding: .utf8)  // ❌ unencrypted on disk

// BAD: PII in log output — appears in device console and crash reports
print("Processing booking for \(passenger.fullName), PNR: \(booking.pnr)")  // ❌

// BAD: ATS disabled — all network traffic unencrypted
// Info.plist: <key>NSAllowsArbitraryLoads</key><true/>  ❌ never

// BAD: sensitive data in iCloud backup (default behavior)
// Must set kSecAttrAccessibleWhenUnlockedThisDeviceOnly (not kSecAttrAccessibleAlways)
// to prevent sensitive Keychain items from being included in backups
```

**Why ENG-6.4 violated:** `UserDefaults` is a plain plist file readable without encryption. Arbitrary logs are included in iTunes/iCloud backups and crash reports. Disabled ATS exposes all traffic to interception. Certificate pinning bypass allows MITM attacks.

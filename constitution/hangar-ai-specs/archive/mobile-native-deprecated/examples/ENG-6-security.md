---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [mobile-native]
title: Security Laws — Mobile Native (iOS & Android)
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — Mobile Native (iOS & Android)

## ENG-6.1: Security by Design

### iOS (Swift)
Store credentials exclusively in Keychain. Enforce ATS. Use certificate pinning for the AA API.

```swift
import Security

struct KeychainStore {
    static func save(token: String, forKey key: String) {
        let data = Data(token.utf8)
        let query: [CFString: Any] = [
            kSecClass:           kSecClassGenericPassword,
            kSecAttrAccount:     key,
            kSecValueData:       data,
            kSecAttrAccessible:  kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
        ]
        SecItemDelete(query as CFDictionary)          // remove stale item first
        SecItemAdd(query as CFDictionary, nil)
    }
    // ❌ NEVER: UserDefaults.standard.set(token, forKey: "auth_token")
}
```

### Android (Kotlin)
Use `EncryptedSharedPreferences` and implement certificate pinning:

```kotlin
// ✅ Encrypted credential storage
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
    .build()

val prefs = EncryptedSharedPreferences.create(
    context, "aa_secure_prefs", masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
)
prefs.edit().putString("auth_token", token).apply()
// ❌ NEVER: getSharedPreferences("aa", MODE_PRIVATE).edit().putString("auth_token", token)

// Certificate pinning via OkHttp
val client = OkHttpClient.Builder()
    .certificatePinner(CertificatePinner.Builder()
        .add("api.aa.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
        .build())
    .build()
```

## ENG-6.4: Data Protection

### iOS
Mask sensitive data in UI; strip PII from logs; use `#if DEBUG` guards.

```swift
// Mask card number display
func maskedCard(_ number: String) -> String {
    let last4 = number.suffix(4)
    return "**** **** **** \(last4)"
}

// Log only in DEBUG builds
#if DEBUG
    print("DEBUG: flight list loaded, count=\(flights.count)")
#endif
// ❌ NEVER in production: os.log("Passenger: \(passenger.name) PNR: \(pnr)")

// Clear sensitive data from memory after use
func clearPaymentInfo() {
    cardNumber = ""
    cvv = ""
    // Overwrite memory for sensitive Swift types
}
```

### Android
Block screenshots on payment screens; guard logs with `BuildConfig.DEBUG`.

```kotlin
// Prevent screenshots on payment screen
override fun onResume() {
    super.onResume()
    window.setFlags(WindowManager.LayoutParams.FLAG_SECURE,
                    WindowManager.LayoutParams.FLAG_SECURE)
}

// PII-safe logging
if (BuildConfig.DEBUG) {
    Timber.d("Booking details: flightId=%s", flightId)
    // ❌ NEVER: Timber.d("Passenger: %s email: %s", name, email)
}
```

Encrypt local offline data (e.g., saved itineraries):

```kotlin
val encryptedFile = EncryptedFile.Builder(context, File(filesDir, "itinerary.enc"),
    masterKey, EncryptedFile.FileEncryptionScheme.AES256_GCM_HKDF_4KB).build()
```

## ENG-6.7: Audit Trail

### iOS — Structured audit events via `os.log`

```swift
import os

let auditLog = Logger(subsystem: "com.aa.mobile", category: "audit")

func logBookingEvent(action: String, flightId: String, correlationId: String) {
    auditLog.info("booking_event action=\(action, privacy: .public) flightId=\(flightId, privacy: .public) correlationId=\(correlationId, privacy: .public)")
    // privacy: .public — safe fields only
    // privacy: .private (default) — redacts in production OS logs
    // ❌ NEVER: auditLog.info("Passenger \(passenger.name) booked \(pnr)")
}
```

### Android — Structured audit events via Timber

```kotlin
fun logPaymentEvent(action: String, correlationId: String) {
    Timber.tag("audit").i("payment_event|action=%s|correlationId=%s", action, correlationId)
    // ❌ NEVER include card number, CVV, or passenger email
}
```

Sync local audit log to backend on connectivity:

```swift
// Append-only local audit buffer synced to AA audit service
struct AuditEvent: Codable {
    let event: String
    let correlationId: String
    let timestamp: Date
    // No PII fields
}
```

## Anti-Patterns

1. **`UserDefaults` (iOS) / `SharedPreferences` (Android) for auth tokens** — both are plaintext; readable by any process with the same app group or root access.
2. **Logging full network response bodies** — booking and payment responses contain PNR, seat, passenger name, and payment info; log only status codes and correlation IDs.
3. **Cleartext HTTP in production** — ATS exceptions (`NSAllowsArbitraryLoads`) and Android `cleartextTrafficPermitted=true` open connections to MITM attacks on airport Wi-Fi.
4. **PII in analytics events** — sending `passenger_name` or `email` to Firebase/Amplitude violates privacy policy; use anonymized user IDs only.
5. **Screenshot allowed on payment screens** — without `FLAG_SECURE` (Android) or `UITextField.isSecureTextEntry` + app-switcher blur (iOS), device screenshots capture card numbers and PNR.

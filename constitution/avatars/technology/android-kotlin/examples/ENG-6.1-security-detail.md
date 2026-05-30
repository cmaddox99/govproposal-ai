---
law_id: ENG-6.1
avatar: android-kotlin
non_negotiable: true
---

# ENG-6.1: Security by Design Examples for Android (Kotlin)

> **Law:** Security SHALL be built in from the start, not bolted on after. Threat modeling occurs at design time. Security requirements appear in acceptance criteria.

---

## COMPLIANT: Threat Model Before Writing Code

```
Feature: Passenger boarding pass display

Security threat model (required before implementation):
  - THREAT: AAB reverse-engineered → class names expose business logic
    MITIGATION: ProGuard/R8 minifyEnabled = true; custom keep rules only where needed
  - THREAT: HTTP traffic intercepted in transit
    MITIGATION: Network Security Config — no cleartext; certificate pinning on /boarding-pass
  - THREAT: Tampered/cloned app bypasses integrity checks
    MITIGATION: Play Integrity API verdict checked before displaying restricted data
  - THREAT: API key committed to source control
    MITIGATION: BuildConfig field injected from CI environment variable; not in code or VCS

Acceptance criteria:
  - [ ] ENG-6.1: minifyEnabled = true in release build type
  - [ ] ENG-6.1: No cleartext traffic in Network Security Config
  - [ ] ENG-6.4: Boarding pass value never written to Logcat or SharedPreferences
  - [ ] ENG-6.1: Play Integrity check passes before restricted data displayed
```

---

## COMPLIANT: ProGuard/R8 Always Enabled in Release

```groovy
// app/build.gradle (Groovy DSL)
android {
    buildTypes {
        release {
            // REQUIRED: minification hides class/method names from reverse engineering
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        debug {
            minifyEnabled false  // OK for debug — faster build
        }
    }
}
```

```
# proguard-rules.pro
# Keep data classes used with JSON serialisation (Moshi)
-keepclassmembers class com.aa.**.dto.** { *; }

# Keep Dagger 2 generated components
-keep class com.aa.**.*_Factory { *; }
-keep class com.aa.**.*_MembersInjector { *; }

# Rule of thumb: keep rules narrow — do NOT use -keep class ** { *; }
```

---

## COMPLIANT: Network Security Config (no cleartext, certificate pin)

```xml
<!-- res/xml/network_security_config.xml -->
<network-security-config>
    <!-- Default: trust system CAs only; no user CAs in release -->
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <certificates src="system"/>
        </trust-anchors>
    </base-config>

    <!-- Pin the AA API certificate for additional in-transit protection -->
    <!-- ENG-6.4: certificate pinning required for mobile apps -->
    <domain-config>
        <domain includeSubdomains="true">api.aa.com</domain>
        <pin-set expiration="2026-12-31">
    <!-- SHA-256 of SubjectPublicKeyInfo (openssl x509 pin extraction) -->
            <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
            <!-- Backup pin — always include one backup -->
            <pin digest="SHA-256">BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=</pin>
        </pin-set>
    </domain-config>

    <!-- DEV/TEST only — blocked in release via build-type res overlay -->
</network-security-config>
```

```xml
<!-- AndroidManifest.xml — wire Network Security Config -->
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
```

---

## COMPLIANT: No Secrets in Code — BuildConfig Injection

```kotlin
// app/build.gradle.kts
android {
    defaultConfig {
        // API base URL from CI environment variable — never hardcoded
        buildConfigField("String", "API_BASE_URL", "\"${System.getenv("API_BASE_URL") ?: "https://api.aa.com/v2"}\"")
        // Never put API keys here — inject from CI secrets manager
    }
}

// Usage — safe, no secret exposed
val apiBaseUrl: String = BuildConfig.API_BASE_URL
```

```kotlin
// local.properties (gitignored) — developer override only, never committed
// api_base_url=https://api-dev.aa.com/v2
```

---

## COMPLIANT: Play Integrity API for Runtime Attestation

```kotlin
// Check app integrity before showing restricted passenger data
class IntegrityChecker @Inject constructor(
    private val integrityManager: IntegrityManager
) {
    suspend fun checkIntegrity(nonce: String): IntegrityVerdict {
        return suspendCancellableCoroutine { cont ->
            IntegrityTokenRequest.builder()
                .setNonce(nonce)
                .build()
                .let { request ->
                    integrityManager.requestIntegrityToken(request)
                        .addOnSuccessListener { response ->
                            cont.resume(IntegrityVerdict.fromToken(response.token()))
                        }
                        .addOnFailureListener { e ->
                            cont.resumeWithException(e)
                        }
                }
        }
    }
}

// Usage — check before displaying boarding pass (Restricted data)
suspend fun showBoardingPass(passId: PassId) {
    val nonce = generateNonce()  // server-issued, single-use
    val verdict = integrityChecker.checkIntegrity(nonce)
    // Send token to backend for server-side verification — never trust client result alone
    if (!boardingPassService.verifyIntegrityAndFetch(passId, verdict.token).isAllowed) {
        throw SecurityException("App integrity check failed")
    }
}
```

---

## COMPLIANT: Sensitive Type Redacts Debug Output

```kotlin
// Wrapper type prevents barcode from appearing in logs, crash reports, toString()
@JvmInline
value class BoardingPassBarcode(private val rawValue: String) {
    override fun toString(): String = "<BoardingPassBarcode: REDACTED>"

    // Expose raw value only within a scoped block — explicit at call site
    fun <T> withRawValue(block: (String) -> T): T = block(rawValue)
}

// Usage
val barcode = BoardingPassBarcode("AA1234567890")
Log.d("TAG", "Barcode: $barcode")  // Logs: "Barcode: <BoardingPassBarcode: REDACTED>"
barcode.withRawValue { raw -> renderBarcodeView(raw) }  // Only consumed where needed
```

---

## VIOLATION: Security Bolted On After

```kotlin
// BAD: API key hardcoded in source (ENG-6.1 + ENG-6.4 violation)
private val apiKey = "sk-aa-prod-abc123xyz"  // ❌ committed to VCS

// BAD: minifyEnabled = false in release — binary is trivially reverse-engineered
release {
    isMinifyEnabled = false  // ❌ never in release
}

// BAD: cleartext traffic permitted
// <base-config cleartextTrafficPermitted="true">  // ❌ never in release

// BAD: PII in Logcat — appears in Android bug reports and device logs
Log.d("Boarding", "Showing pass for passenger: ${passenger.fullName}, PNR: ${booking.pnr}")  // ❌

// BAD: no integrity check before restricted data — any tampered app can request it
fun showBoardingPass(passId: PassId) {
    // VIOLATION: no Play Integrity check — tampered or cloned app has full access
    val pass = repository.fetchPass(passId)
    displayPass(pass)
}
```

**Why ENG-6.1 violated:** Hardcoded secrets are trivially scraped. Disabled minification exposes your architecture to reverse engineers. Cleartext traffic is interceptable. PII in Logcat appears in bug reports. No integrity check allows repackaged apps to access restricted data.

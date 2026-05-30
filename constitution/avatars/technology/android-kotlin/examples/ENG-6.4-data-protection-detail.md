---
law_id: ENG-6.4
avatar: android-kotlin
non_negotiable: true
---

# ENG-6.4: Data Protection Examples for Android (Kotlin)

> **Law:** All sensitive data SHALL be protected at rest and in transit using industry-standard encryption. Mobile apps MUST use certificate pinning for in-transit protection.

---

## Data Classification for Android Apps

| Level | Android Examples | Storage Rule |
|-------|-----------------|-------------|
| **Restricted** | Auth tokens, PNR, passport data, payment card | Android Keystore (AES-256-GCM hardware-backed) |
| **Confidential** | Loyalty number, booking reference, seat preference | EncryptedSharedPreferences or Keystore |
| **Internal** | Flight number, departure airport, gate number | DataStore or Room (no encryption required) |
| **Public** | App content, schedules, marketing copy | Any storage |

---

## COMPLIANT: Data at Rest — Android Keystore (Restricted Data)

The Android Keystore stores cryptographic keys in hardware-secured storage — keys never leave the secure enclave.

```kotlin
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec

class AndroidKeystoreService @Inject constructor() {

    private val keyAlias = "aa_auth_token_key"
    private val keyStore = KeyStore.getInstance("AndroidKeyStore").apply { load(null) }

    fun generateKey() {
        if (keyStore.containsAlias(keyAlias)) return

        KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore").apply {
            init(
                KeyGenParameterSpec.Builder(
                    keyAlias,
                    KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT
                )
                    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                    .setKeySize(256)
                    // REQUIRED: key only usable when device is unlocked
                    .setUserAuthenticationRequired(false)
                    .build()
            )
            generateKey()
        }
    }

    fun encrypt(plaintext: String): Pair<ByteArray, ByteArray> {
        val key = keyStore.getKey(keyAlias, null) as SecretKey
        val cipher = Cipher.getInstance("AES/GCM/NoPadding").apply {
            init(Cipher.ENCRYPT_MODE, key)
        }
        val ciphertext = cipher.doFinal(plaintext.toByteArray(Charsets.UTF_8))
        return Pair(cipher.iv, ciphertext)
    }

    fun decrypt(iv: ByteArray, ciphertext: ByteArray): String {
        val key = keyStore.getKey(keyAlias, null) as SecretKey
        val cipher = Cipher.getInstance("AES/GCM/NoPadding").apply {
            init(Cipher.DECRYPT_MODE, key, GCMParameterSpec(128, iv))
        }
        return String(cipher.doFinal(ciphertext), Charsets.UTF_8)
    }

    fun deleteKey() = keyStore.deleteEntry(keyAlias)
}
```

---

## COMPLIANT: Data at Rest — EncryptedSharedPreferences (Confidential Data)

For Confidential-level data (e.g., loyalty number, preferences), use Jetpack Security's `EncryptedSharedPreferences` — simpler than raw Keystore for key-value storage.

```kotlin
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class SecurePreferencesService @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val prefs = EncryptedSharedPreferences.create(
        context,
        "aa_secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun saveAuthToken(token: String) = prefs.edit().putString("auth_token", token).apply()

    fun getAuthToken(): String? = prefs.getString("auth_token", null)

    fun clearAuthToken() = prefs.edit().remove("auth_token").apply()
}
```

---

## COMPLIANT: Data in Transit — Certificate Pinning (OkHttp)

Per ENG-6.4, mobile apps MUST use certificate pinning. OkHttp's `CertificatePinner` is the primary mechanism for Android (complementing Network Security Config).

```kotlin
import okhttp3.CertificatePinner
import okhttp3.OkHttpClient

object HttpClientFactory {

    fun create(): OkHttpClient {
        val certificatePinner = CertificatePinner.Builder()
            // Pin the SHA-256 hash of the SubjectPublicKeyInfo for api.aa.com
            .add("api.aa.com", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
            // Always add a backup pin in case primary certificate rotates
            .add("api.aa.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=")
            .build()

        return OkHttpClient.Builder()
            .certificatePinner(certificatePinner)
            // 30s timeouts — never set to 0 (no timeout = potential resource leak)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()
    }
}

// Wire into Hilt module
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient = HttpClientFactory.create()
}
```

---

## COMPLIANT: No PII in Logcat

Android Logcat is accessible to any app with `READ_LOGS` permission and appears in Android bug reports. PII must never appear there.

```kotlin
// COMPLIANT: Redacting wrapper type
@JvmInline
value class PassengerName(private val value: String) {
    // Shows only first initial + last name: "J. Smith"
    override fun toString(): String = value.split(" ").let { parts ->
        if (parts.size >= 2) "${parts.first().first()}. ${parts.last()}" else "<name>"
    }
}

// COMPLIANT: Debug-only logging with PII guard
fun logBookingEvent(flightNumber: String, passengerName: PassengerName) {
    // Safe: flight number is operational data, not PII
    Log.i("Booking", "Booking created for flight $flightNumber")
    // Safe in DEBUG only, and PassengerName.toString() is masked anyway
    if (BuildConfig.DEBUG) {
        Log.d("Booking", "Passenger: $passengerName")  // "J. Smith"
    }
    // NEVER: Log.d("Booking", "PNR: ${booking.pnr}") — no PII in any log level
}
```

---

## VIOLATION: Sensitive Data Stored Insecurely

```kotlin
// BAD: auth token in plain SharedPreferences — unencrypted XML file
context.getSharedPreferences("prefs", Context.MODE_PRIVATE)
    .edit().putString("auth_token", token).apply()  // ❌ plaintext on disk

// BAD: PNR stored in a file without encryption
val file = File(context.filesDir, "pnr.txt")
file.writeText(booking.pnr)  // ❌ world-readable by backup tools

// BAD: PII in Logcat — captured by Android bug reports and third-party crash SDKs
Log.d("TAG", "User logged in: name=${user.fullName} email=${user.email}")  // ❌

// BAD: no certificate pinning — susceptible to MITM with a rogue CA cert
val client = OkHttpClient.Builder().build()  // ❌ trusts all system CAs; no pinning

// BAD: API key hardcoded — visible in decompiled APK even with ProGuard
companion object {
    const val API_KEY = "aa-prod-secret-key-12345"  // ❌ never hardcode credentials
}

// BAD: cleartext traffic permitted (also ENG-6.1)
// <base-config cleartextTrafficPermitted="true">  // ❌ exposes all traffic
```

**Why ENG-6.4 violated:** Plain `SharedPreferences` is an unencrypted XML file trivially read via `adb backup` or a rooted device. PII in Logcat is captured by Android bug reports, third-party crash SDKs, and accessible to privileged apps. No certificate pinning allows MITM with a trusted CA. Hardcoded API keys survive ProGuard's class renaming.

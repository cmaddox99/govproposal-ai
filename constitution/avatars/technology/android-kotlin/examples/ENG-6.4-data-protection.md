---
law_id: ENG-6.4
avatar: android-kotlin
non_negotiable: true
---

# ENG-6.4 — Data Protection (Android Kotlin)

> Android Keystore for auth tokens. EncryptedSharedPreferences for Confidential data. No PII in Logcat.

## COMPLIANT — Android Keystore (Restricted data)

```kotlin
// Hardware-backed AES-256-GCM key — auth token storage
val keyGenerator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore")
keyGenerator.init(
    KeyGenParameterSpec.Builder("aa_auth_key",
        KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
        .setUserAuthenticationRequired(true)
        .build()
)
val secretKey = keyGenerator.generateKey()
```

## COMPLIANT — EncryptedSharedPreferences (Confidential data)

```kotlin
val masterKey = MasterKey.Builder(context)
    .setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build()

val prefs = EncryptedSharedPreferences.create(
    context, "aa_secure_prefs", masterKey,
    EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
    EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
)
```

## COMPLIANT — PII Redaction

```kotlin
@JvmInline value class SensitiveString(private val value: String) {
    override fun toString() = "***REDACTED***"   // never leaks to Logcat
    fun reveal() = value
}
data class PassengerProfile(val name: SensitiveString, val passportNumber: SensitiveString)
```

## VIOLATION

```kotlin
// ❌ PII in SharedPreferences (plaintext)
prefs.edit().putString("passport_number", passportNumber).apply()

// ❌ PII in Logcat
Log.d("CheckIn", "Passenger: ${passenger.name}, DOB: ${passenger.dob}")
```

> Full detail with OkHttp CertificatePinner: see `ENG-6.4-data-protection-detail.md`.

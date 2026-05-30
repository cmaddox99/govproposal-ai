---
law_id: ENG-6.1
avatar: android-kotlin
non_negotiable: true
---

# ENG-6.1 — Security by Design (Android Kotlin)

> ProGuard/R8 always on. Network Security Config enforces HTTPS. No secrets in code. Play Integrity for attestation.

## COMPLIANT — Release Build Config

```kotlin
// app/build.gradle.kts
android {
    buildTypes {
        release {
            isMinifyEnabled = true        // R8 minification — hides class names
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    buildFeatures { buildConfig = true }
}
```

## COMPLIANT — No Secrets in Code

```kotlin
// ✅ CI injects via environment — never hardcoded
android {
    defaultConfig {
        buildConfigField("String", "API_KEY", "\"${System.getenv("API_KEY") ?: ""}\"")
    }
}
// local.properties (gitignored): API_KEY=dev-local-key
```

## COMPLIANT — Network Security Config

```xml
<!-- res/xml/network_security_config.xml -->
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors><certificates src="system"/></trust-anchors>
    </base-config>
</network-security-config>
```

## VIOLATION

```kotlin
// ❌ Hardcoded API key
private val apiKey = "sk-aa-prod-1234abcd"

// ❌ Cleartext traffic permitted (default — must be explicitly disabled)
// Missing network_security_config.xml → cleartext allowed

// ❌ Debug logging in production
Log.d("BookingViewModel", "User token: $authToken")
```

> Full detail with Play Integrity API, OkHttp certificate pinning: see `ENG-6.1-security-detail.md`.

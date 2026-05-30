---
law_id: ENG-6.1
avatar: ios-build-infrastructure
non_negotiable: true
---

# ENG-6.1: Security by Design — Build Scripts and Signing Credentials

> **Law:** Security SHALL be designed in from the start, not bolted on. For the iOS build toolchain, this means: secrets and signing credentials must never appear in xcconfig files, build scripts, or source control.

---

## What Counts as a Secret in an iOS Build Context

| Artifact | Secret Type | Correct Location |
|---|---|---|
| Apple Distribution certificate | P12 + passphrase | CI Keychain / Fastlane match repo |
| Provisioning profile | `.mobileprovision` | CI Keychain / match / Apple API |
| App Store Connect API key | `.p8` private key | CI environment variable |
| Firebase/Crashlytics API key | String key | CI secret → `Info.plist` at build time |
| xcconfig with secrets | Any `API_KEY = …` | Never committed; inject at CI build step |

---

## Compliant: Inject API Keys at Build Time from CI Secrets

```bash
# In CI (e.g., GitHub Actions) — secret injected at build time, not in repo
- name: Inject Firebase config
  env:
    FIREBASE_API_KEY: ${{ secrets.FIREBASE_API_KEY }}
  run: |
    /usr/libexec/PlistBuddy -c \
      "Set :FIREBASE_API_KEY $FIREBASE_API_KEY" \
      AmericanApp/Supporting\ Files/GoogleService-Info.plist
```

```swift
// In source: read from bundle, never hardcode
guard let path = Bundle.main.path(forResource: "GoogleService-Info", ofType: "plist"),
      let config = NSDictionary(contentsOfFile: path),
      let apiKey = config["API_KEY"] as? String else {
    // ✅ Fail loudly if config is missing — never provide a fallback literal
    fatalError("GoogleService-Info.plist missing or malformed")
}
```

---

## Non-Compliant: Hardcoded Credentials in xcconfig or Source

```bash
# ❌ DON'T: xcconfig with real API key committed to repo
# AmericanApp/Config/Release.xcconfig
FIREBASE_API_KEY = AIzaSyBxxxxxxxxxxxxxxxxxxxxxxx
APP_STORE_CONNECT_KEY = AuthKey_XXXXXXXXXX
```

```swift
// ❌ DON'T: Literal secret in Swift source
let crashlyticsKey = "0xDEADBEEFdeadbeef"  // real key, committed to git
```

---

## Signing Credentials (Fastlane match pattern)

```bash
# ✅ Compliant: match manages certificates in an encrypted repo
fastlane match appstore --readonly
# Certificates stored encrypted; passphrase in CI secret MATCH_PASSWORD

# ❌ Non-compliant: committing P12 directly
git add AmericanAirlines_Distribution.p12  # never do this
```

Build scripts that call `xcodebuild` must not pass `-allowProvisioningUpdates` with embedded credentials. Use match or the Apple Developer API with a short-lived key injected via CI secrets.

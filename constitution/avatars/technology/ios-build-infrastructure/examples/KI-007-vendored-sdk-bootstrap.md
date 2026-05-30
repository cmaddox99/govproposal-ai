# KI-007 — Vendored Binary SDKs Not Auto-Copied to Carthage/Build

## Symptom
```
error: There is no XCFramework found at '.../Carthage/Build/AEPCore.xcframework'.
error: There is no XCFramework found at '.../Carthage/Build/AkamaiBMP.xcframework'.
error: There is no XCFramework found at '.../Carthage/Build/Mapbox.xcframework'.
(in target 'AmericanUI' from project 'AmericanUI')
```

## Root Cause
6 third-party SDKs are bundled as pre-built binaries **inside** internal AA Carthage Checkouts, but `carthage bootstrap` does not copy them to `Carthage/Build/`. No script or runbook documents this step.

| SDK | Source in Checkouts | Target in Build |
|-----|---------------------|-----------------|
| AEP* (9 frameworks) | `analytics-ios/ios/Sources/AmericanAnalytics/ThirdParty/Adobe/` | `Carthage/Build/` |
| AkamaiBMP + companion | `devicevalidation-ios/ThirdParty/AkamaiBMP/` | `Carthage/Build/` |
| ASAPPSDK | `chat-ios/ios/` | `Carthage/Build/` |
| Mapbox | `maps-ios/ios/AmericanMaps/ThirdParty/LocusLabs/` | `Carthage/Build/` |
| LocusLabsSDK | unknown — not found in Checkouts | `Carthage/Build/` |
| Qualtrics | unknown — not found in Checkouts | `Carthage/Build/` |

## Fix
After `carthage bootstrap`, manually copy all vendored SDKs:
```bash
BUILD="Carthage/Build"
CHECKOUTS="Carthage/Checkouts"
cp -r "$CHECKOUTS/analytics-ios/ios/Sources/AmericanAnalytics/ThirdParty/Adobe/Analytics/AEPAnalytics.xcframework" "$BUILD/"
cp -r "$CHECKOUTS/analytics-ios/ios/Sources/AmericanAnalytics/ThirdParty/Adobe/Core/AEPCore.xcframework" "$BUILD/"
# ... (repeat for all AEP*, AkamaiBMP, ASAPPSDK, Mapbox)
```

## Remediation
Create a `scripts/copy-vendored-sdks.sh` and invoke it in CI after `carthage bootstrap`. Document in README.

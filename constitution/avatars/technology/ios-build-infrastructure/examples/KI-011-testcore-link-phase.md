---
id: KI-011
title: "AmericanTestCore.xcframework not linked in test target — Swift module unresolvable"
severity: high
avatar: ios-build-infrastructure
discovered: 2026-05-07
law: ENG-4.2
---

## Symptom

```
error: unable to resolve module dependency: 'AmericanTestCore'
AmericanAirlinesTests/AppQuickActionsTests/AppQuickActionsTests.swift:13:8: error: Unable to resolve module dependency: 'AmericanTestCore'
```

Three test files import `AmericanTestCore`:
- `AppQuickActionsTests/AppQuickActionsTests.swift` (Swift Testing `@Suite`)
- `BannerProviderTests.swift`
- `BoardingNotificatificationTests.swift`

## Root Cause

`AmericanTestCore.xcframework` is referenced in the Xcode project navigator
(`PBXFileReference`) but has **zero `PBXBuildFile` entries** — it is not linked
to any target's frameworks build phase.

The test target `AmericanAirlinesTests` frameworks build phase (`A78B5B1C1BD436FB00222E5E`)
contains only one entry: `AmericanUI.framework in Frameworks`.

Because the xcframework is not linked, the Swift compiler cannot resolve the
`AmericanTestCore` module during test bundle compilation.

## Why It Survived Until Now

- CI likely runs in a pre-baked Docker/macOS image that may cache DerivedData containing
  a previously linked version of `AmericanTestCore.framework`
- Local developers who have never cleaned DerivedData may have a cached module map
- The 3 affected test classes may be effectively dead (not run in CI)

## Fix (Workaround for coverage measurement)

Copy the simulator inner framework to `Carthage/Build/iOS/` and pass framework
search path + linker flag overrides to xcodebuild:

```bash
cp -R Carthage/Build/AmericanTestCore.xcframework/ios-arm64_x86_64-simulator/AmericanTestCore.framework \
      Carthage/Build/iOS/

xcodebuild test \
  -workspace AmericanAirlines.xcworkspace \
  -scheme "AmericanAirlines - iOS - Debug" \
  -destination "platform=iOS Simulator,..." \
  -enableCodeCoverage YES \
  ENABLE_TESTABILITY=YES \
  "FRAMEWORK_SEARCH_PATHS=$(inherited) $(SRCROOT)/Carthage/Build/iOS" \
  "OTHER_LDFLAGS=$(inherited) -framework AmericanTestCore"
```

## Proper Fix (Project Level)

In Xcode:
1. Select the `AmericanAirlinesTests` target
2. Build Phases → Link Binary with Libraries → `+`
3. Add `AmericanTestCore.xcframework`
4. Set embedding to "Do Not Embed" (host app provides it at runtime)

This should be committed as a project fix and verified in CI.

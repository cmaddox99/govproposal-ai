# KI-006 — WatchKit Extension Requires watchOS Carthage Slices

## Symptom
```
error: While building for watchOS Simulator, no library for this platform was found
in '.../Carthage/Build/AmericanCore.xcframework'.
(in target 'AmericanAirlines WatchKit Extension' from project 'AmericanAirlines')
** TEST FAILED **
```

## Root Cause
`AmericanAirlines WatchKit Extension` is a **project-level build dependency** of the main app target. When `xcodebuild test` runs, it builds all dependencies for their native platform — including the watch extension for watchOS Simulator. `carthage bootstrap --platform iOS` builds no watchOS slices.

**What does NOT work:**
- `EMBED_WATCH_CONTENT=NO` — prevents embedding, not building
- `xcconfig EXCLUDED_ARCHS[sdk=watchsimulator*]` — xcodebuild ignores per-SDK conditional in xcconfig for dependency targets
- Setting `buildForTesting=NO` in a user scheme for the extension — the main app target still pulls it as a dependency

## Fix
```bash
carthage bootstrap --platform iOS,watchOS --use-xcframeworks --cache-builds
```
Builds both iOS and watchOS slices. Build time: ~2× longer than iOS-only.

## Workaround (partial coverage)
None available without project modification. This is a hard requirement.

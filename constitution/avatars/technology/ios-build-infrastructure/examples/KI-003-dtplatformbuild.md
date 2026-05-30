# KI-003 — DTPlatformBuild Simulator Race Condition

**Law:** ENG-4.1 (Atomic TDD Law)

## Symptom

```
FBSApplicationLibrary returned nil Code 4
```

Intermittent test launch failure after an Xcode point-release update. 13-second `FBSApplicationLibrary registration` delay logged.

## Root Cause

App binary compiled with SDK `23E252`; simulator runtime updated to `23E254a`. `DTPlatformBuild` in the app's `Info.plist` doesn't match the current SDK. Xcode force-reinstalls the app on every `test-without-building` run, triggering a registration race condition.

## Fix

After any Xcode version change, run a full build+test — not `test-without-building`:

```bash
xcodebuild test \
  -workspace AmericanAirlines.xcworkspace \
  -scheme "AA QA - iOS - Debug" \
  -destination "platform=iOS Simulator,id=$SIMULATOR_ID"
```

The full build recompiles the app binary with the current SDK, eliminating the `DTPlatformBuild` mismatch.

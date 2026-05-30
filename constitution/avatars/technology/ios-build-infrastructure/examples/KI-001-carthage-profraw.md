# KI-001 — Carthage profraw Contamination

**Law:** ENG-4.2 (Test Pyramid Law)

## Symptom

```
error: Failed to merge raw profiles …
raw profile version mismatch: Profile uses raw profile version = 8; expected version = 10
```

## Root Cause

Carthage prebuilt XCFrameworks (`Carthage/Build/`) were compiled with an older Xcode. At test runtime every loaded framework writes a profraw file. Carthage frameworks write v8; current LLVM (Xcode 26.4.1 / Build 17E202) requires v10. `llvm-profdata merge` rejects the mixed set. Clearing DerivedData does NOT fix this — the source is the Carthage binary on disk.

> **Note:** Xcode version naming changed. What was previously called "Xcode 16.3" is now reported as "Xcode 26.4.1 / Build 17E202" in this toolchain.

## Fix Options

| Option | Command | Cost |
|--------|---------|------|
| Rebuild Carthage (iOS + watchOS) | `carthage bootstrap --platform iOS,watchOS --use-xcframeworks --cache-builds` | 60–120 min |
| Restrict coverage targets | Add `CODE_COVERAGE_TARGET_NAMES = AmericanAirlines AmericanAirlinesTests` to xcconfig | Low |
| Measure via CI | Trigger CI run — agents have no cached Carthage binaries | None local |

> **Important:** Use `--platform iOS,watchOS` — iOS-only bootstrap will block test runs because the WatchKit Extension is a project-level build dependency (see KI-006). Use `--cache-builds` to avoid re-downloading unchanged deps on subsequent runs.

## Prerequisites

- AAInternal GitHub network access required. Verify before starting:
  ```bash
  git ls-remote https://github.com/AAInternal/businessui-ios HEAD
  # Must return a SHA — if it hangs, you are off VPN or off AAInternal network
  ```
- Do NOT use `carthage update --no-build` as a dry-run — it hangs indefinitely on graphs with 50+ dependencies.

## Detection

```bash
# Check build version of a Carthage framework
otool -l Carthage/Build/AmericanCore.xcframework/ios-arm64_x86_64-simulator/AmericanCore.framework/AmericanCore \
  | grep -A2 "LC_BUILD_VERSION"
# minos field shows Xcode SDK version it was compiled with
```

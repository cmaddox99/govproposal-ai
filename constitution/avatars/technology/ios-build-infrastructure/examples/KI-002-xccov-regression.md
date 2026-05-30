# KI-002 — xccov Xcode 16.3 Regression

**Law:** ENG-4.2 (Test Pyramid Law)

## Symptom

```
xccov: Failed to load coverage archive … action '(null)'
```

## Root Cause

In Xcode 16.3, the `archiveRef` field in the xcresult action record is null. `xccov` hardcodes `/tmp/action.xccovarchive/Metadata.plist` as its extraction path — when `archiveRef` is null, nothing is written there. Coverage data IS present in the xcresult (`reportRef` populated) but stored as an `NSKeyedArchiver` blob of private class `XCTHCodeCoverage` — not decodable without Apple's private frameworks.

## Workaround

- Always pass `-resultBundlePath` to a path outside `/tmp` (e.g., `~/Desktop/`)
- Use Xcode Report Navigator as fallback for human-readable numbers
- Track fix status in Apple release notes

## Warning

The "28% of duration" stat in Xcode Report Navigator is **test duration**, not line coverage. Do not report it as a coverage percentage.

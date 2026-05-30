# KI-005 — WireMock Force-Unwrap Test Host Crash

**Law:** ENG-4.1 (Atomic TDD Law)

## Symptom

All tests in the suite report "did not run" after a single test fails. Zero tests execute.

## Root Cause

A force-unwrap (`!`) in test code causes a fatal error that kills the **entire test host process**. Every test in the suite reports "did not run" — not just the failing test. This is especially dangerous when WireMock is not running: a network call returns nil, the force-unwrap fires, and the host process exits with a non-zero code before any test results are recorded.

## Fix

```swift
// ❌ NEVER — kills test host process when nil; 0 tests execute
let data = receivedData!

// ✅ ALWAYS — this test fails gracefully; all other tests continue running
let data = try XCTUnwrap(receivedData, "Expected data from stub — is WireMock running on :8080?")
```

## WireMock Architecture Constraint

`Foundation.Process` is unavailable in iOS SDK test targets. The WireMock JAR **must** be started externally before `xcodebuild test`. Always verify it is up first:

```bash
curl -s http://localhost:8080/__admin/health | grep healthy || echo "WireMock not running"
```

WireMock started with `&` is fragile — always health-check, never assume.

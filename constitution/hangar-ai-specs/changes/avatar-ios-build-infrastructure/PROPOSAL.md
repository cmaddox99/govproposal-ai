---
title: "iOS Build Infrastructure Avatar — New Technology Avatar"
spec_id: "avatar-ios-build-infrastructure"
status: "PROPOSED"
author: "Tech Coach (American Airlines)"
created: "2026-05-07"
scope: "avatars/technology/ios-build-infrastructure/ · avatars/index.yaml · BOOTSTRAP-REMEDIATION.md"
triggered_by: "disc-2026-005 Stage C iOS — repeated rabbit-holing into Xcode/LLVM internals; ios-swift avatar has zero build toolchain knowledge"
affects: "ios-swift avatar (companion), BOOTSTRAP-REMEDIATION.md, avatars/index.yaml"
laws_applied:
  - ENG-4.2
  - ENG-10.1
  - ENG-11.1
  - ENG-13.1
  - BUS-7.1
exit_checklist:
  - item: "Taxonomy gates passed (technology avatar, not product)"
    status: "done"
  - item: "manifest.yaml created with id, triggers, laws, stack details"
    status: "pend"
  - item: "guidance.md encodes all toolchain lessons from disc-2026-005 iOS track"
    status: "pend"
  - item: "Known issues table complete (profraw, xccov, DTPlatformBuild, DerivedData)"
    status: "pend"
  - item: "Coverage measurement recipe documented (working path + blocked path)"
    status: "pend"
  - item: "WireMock iOS integration pattern documented"
    status: "pend"
  - item: "avatars/index.yaml updated with new avatar entry"
    status: "pend"
  - item: "Render gate passed (aa-artifact-render on this PROPOSAL.md)"
    status: "pend"
  - item: "Stakeholder approval obtained"
    status: "pend"
stakeholder:
  name: "Adeel Ali"
  role: "Co-founder / Inventor"
  affirm: true
  note: "Approved 2026-05-07"
audit_log:
  - date: "2026-05-07"
    actor: "Tech Coach"
    action: "Proposal created — taxonomy gates passed, scope confirmed: technology avatar, not product"
    outcome: "DRAFTED"
avatars:
  - "avatar-ios-swift"
spec_artifacts:
  - path: "hangar-ai-specs/changes/avatar-ios-build-infrastructure/PROPOSAL.md"
    type: "proposal"
    status: "IN_PROGRESS"
template_version: "1.0.0"
---

# iOS Build Infrastructure Avatar — New Technology Avatar

## Problem Statement

The `ios-swift` avatar (`avatar-ios-swift`, v1.2.0) governs application code patterns — architecture, TDD, complexity limits, fastlane lanes, Carthage setup basics. It has **zero knowledge** of the iOS build toolchain.

During `disc-2026-005` Stage C iOS, a tech coach spent multiple sessions attempting to measure line coverage using the CLI. The session rabbit-holed repeatedly through Xcode internals, LLVM profraw format versions, DerivedData lifecycle management, and simulator race conditions. A knowledgeable iOS platform engineer would have recognized all of these patterns immediately. The `ios-swift` avatar could not surface any of this knowledge because it was never encoded.

The knowledge gap caused:
1. **Misread coverage output** — Xcode UI test duration metric ("28% of duration") was initially mistaken for line coverage %, producing a false finding in Stage C
2. **3+ sessions of repeated troubleshooting** for issues that have deterministic root causes and known fixes
3. **F-C-iOS-09** filed as a health finding: "CLI coverage structurally blocked — Carthage prebuilt binaries inject LLVM profraw v8 at runtime; current llvm-profdata expects v10"
4. A `BOOTSTRAP-REMEDIATION.md` iOS section that encodes the fixes but is not constitutionally governed

**This avatar captures all lessons learned and makes them constitutionally retrievable for the next coach who builds this project.**

---

## Taxonomy Decision

| Gate | Result | Rationale |
|------|--------|-----------|
| Domain gate | ✅ PASS | Durable runtime capability — iOS build, test, and coverage toolchain; independent of team names |
| User journey gate | ✅ PASS (N/A) | Technology avatar — no distinct user journeys required |
| Boundary gate | ✅ PASS | `ios-swift` explicitly excludes toolchain; no overlap |
| Stability gate | ✅ PASS | Survives org changes; tied to Xcode/LLVM/Carthage versions not teams |
| Retrieval gate | ✅ PASS | Agents searching "Carthage coverage", "profraw", "DerivedData", "xccov" will land here and not pollute `ios-swift` |

**Classification:** Technology/runtime capability → `avatars/technology/` ✅

---

## Scope

### In Scope

- Carthage prebuilt binary behavior and coverage instrumentation interaction
- LLVM profraw version compatibility (v8 vs v10; Xcode version matrix)
- `xccov` known regressions by Xcode version
- DerivedData lifecycle management (multiple directories, wipe procedure)
- Coverage measurement recipe: working path (CI, fresh agent), blocked path (Carthage prebuilts), fix path (rebuild Carthage)
- `DTPlatformBuild` mismatch — simulator race condition and fix
- WireMock iOS integration pattern (external JAR, `AAWireMockURLProtocol`, `XCTUnwrap` crash safety)
- Bootstrap checklist for a new coach setting up the project locally

### Out of Scope

- Application architecture (belongs in `ios-swift`)
- TDD test patterns (belongs in `ios-swift` + `skill-06-atomic-tdd`)
- CI/CD pipeline configuration beyond what affects local coverage measurement

---

## Deliverables

| Artifact | Layer | Location |
|----------|-------|----------|
| `manifest.yaml` | Technology avatar | `avatars/technology/ios-build-infrastructure/manifest.yaml` |
| `guidance.md` | Technology avatar | `avatars/technology/ios-build-infrastructure/guidance.md` |
| `examples/coverage-measurement.md` | Technology avatar | `avatars/technology/ios-build-infrastructure/examples/coverage-measurement.md` |
| `avatars/index.yaml` entry | Registry | `avatars/index.yaml` |

---

## Key Knowledge to Encode

### 1. Carthage Prebuilt Binary + Coverage Instrumentation

Carthage prebuilt XCFrameworks in `Carthage/Build/iOS/` are compiled once and checked in or cached. When the project upgrades Xcode, the prebuilt binaries are NOT recompiled. These binaries contain LLVM coverage instrumentation at whatever format version was current when they were built.

**Failure chain:**
```
Older Xcode built Carthage deps → profraw v8 written at runtime
Current Xcode 16.3 llvm-profdata expects v10
llvm-profdata merge fails: "raw profile version mismatch: Profile uses raw profile version = 8; expected version = 10"
xccov gets zero data
```

**Clearing DerivedData does NOT fix this.** The contamination source is the Carthage binary, not the DerivedData.

**Fix options (in order of preference):**
1. Rebuild Carthage with current Xcode: `carthage bootstrap --platform iOS --use-xcframeworks`
2. Restrict coverage instrumentation to app+test targets only via `CODE_COVERAGE_TARGET_NAMES` build setting (Xcode 14+)
3. Measure coverage via CI (fresh agents; no pre-compiled Carthage binaries)

### 2. xccov Xcode 16.3 Regression

`xcrun xccov view --report <path>.xcresult` fails with:
```
Failed to load coverage archive … action '(null)'
```

Root cause: `archiveRef` is null in the xcresult action record (Xcode 16.3 bug). `xccov` hardcodes `/tmp/action.xccovarchive` as the extraction path; when `archiveRef` is missing, nothing is written there, and xccov finds nothing.

Coverage data IS present in the xcresult (`reportRef` field is populated), but it is stored as an `NSKeyedArchiver` blob of private class `XCTHCodeCoverage` — not decodable without Apple's private frameworks.

**Workaround:** Use Xcode Report Navigator (manual), or measure via CI pipeline.

### 3. DTPlatformBuild Mismatch — Simulator Race Condition

After a Xcode point-release update, `xcodebuild test-without-building` fails intermittently:
```
FBSApplicationLibrary returned nil Code 4
```

Root cause: The app was built with SDK `23E252`, but the simulator runtime updated to `23E254a`. Xcode force-reinstalls the app on every `test-without-building` run, triggering a 13-second `FBSApplicationLibrary registration` delay and a race condition.

**Fix:** Run full `xcodebuild test` (not `test-without-building`) after any Xcode version change. The full build + test path avoids the race condition.

### 4. DerivedData Directory Accumulation

Xcode creates a new `AmericanAirlines-XXXXXXXX` directory per workspace path variation. After workspace moves, renames, or symlink changes, stale directories accumulate. Each contains old profraw files from previous Xcode versions.

**Wipe command:**
```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/AmericanAirlines-*
```

Always wipe ALL matching directories (wildcard), not a specific named one.

### 5. WireMock iOS Integration Pattern

`Foundation.Process` is unavailable in iOS SDK test targets — WireMock JAR must be started **externally** before running xcodebuild. The test target cannot launch or manage the JAR.

Pattern: `AAWireMockURLProtocol` (self-contained `URLProtocol` subclass) intercepts configured hosts and rewrites to `http://localhost:8080`.

**XCTUnwrap over force-unwrap:**
```swift
// ❌ Crashes entire test host when data is nil — 0 tests execute
let data = receivedData!

// ✅ Fails gracefully — other tests continue running
let data = try XCTUnwrap(receivedData, "Expected data from stub — is WireMock running on :8080?")
```

Force-unwrap in a test causes a fatal error that kills the test host process. Every test in the suite reports as "did not run."

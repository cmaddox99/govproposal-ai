# iOS Build Infrastructure Guidance

> **Companion to `ios-swift`.** Covers build toolchain, coverage measurement, DerivedData lifecycle, and WireMock integration. For app code patterns see `avatars/technology/ios-swift/guidance.md`.

## Quick Diagnosis

| Symptom | See |
|---------|-----|
| `raw profile version mismatch: version 8, expected 10` | `examples/KI-001-carthage-profraw.md` |
| `xccov: Failed to load coverage archive … action '(null)'` | `examples/KI-002-xccov-regression.md` |
| `FBSApplicationLibrary returned nil Code 4` | `examples/KI-003-dtplatformbuild.md` |
| Coverage 0% silently | `examples/KI-004-deriveddata.md` |
| All tests "did not run" after one failure | `examples/KI-005-wiremock-crash.md` |

## Bootstrap (once per machine or after any Xcode upgrade)

```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/AmericanAirlines-*
xcrun simctl boot "iPhone 17 Pro" 2>/dev/null || true
```

> Stale profraw v8 files silently corrupt coverage merge — #1 cause of wasted time on this project.

## Run Tests + Coverage

See `examples/coverage-measurement.md` for full command and simulator device name.

## See Also

- `examples/coverage-measurement.md` — 3 coverage paths (CI / local-blocked / Carthage-rebuild)
- `examples/KI-001` through `KI-005` — root cause + fix per known issue
- `use-cases/local-coverage-setup/` — first-time coach walkthrough
- `use-cases/wiremock-ios-integration/` — WireMock stub pattern for iOS test targets

## Non-Negotiable Laws

### ENG-6.7 — Audit Trail

The toolchain is a constitutional actor: xcresult evidence is trustworthy only if profraw files were captured (verify count > 0), xccov parsed without error, and DerivedData was cleared before the run. Do not attest coverage figures from an unverified pipeline. See `examples/ENG-6.7-audit-trail.md`.

### ENG-4.1 — Atomic TDD

Force-unwrap (`!`) in test code kills the entire XCTest host process — every test in the suite reports "did not run" with zero evidence. Treat any test host crash as an immediate RED that blocks all other tests. See `examples/KI-005-wiremock-crash.md`.

### ENG-4.2 — Test Pyramid

profraw v8/v10 version mismatch (KI-001) and missing watchOS slices (KI-006) silently exclude test targets, producing a false pyramid. Verify the full target list is exercised before recording a coverage figure.

# iOS Coverage Measurement — Worked Example

> **Law:** ENG-4.2 (Test Pyramid Law)

## The Three Paths

### Path A — Working: CI Pipeline (Recommended)

CI agents start clean — no cached Carthage binaries, no stale DerivedData. Only fully reliable path until Carthage is rebuilt locally.

```bash
xcodebuild test -enableCodeCoverage YES \
  -resultBundlePath artifacts/coverage.xcresult
xcrun xccov view --report artifacts/coverage.xcresult
# → TOTAL  XX.XX%
```

### Path B — Blocked Locally (Carthage prebuilt contamination)

```bash
xcodebuild test ... -enableCodeCoverage YES \
  -resultBundlePath ~/Desktop/aa-ios-coverage.xcresult
xcrun xccov view --report ~/Desktop/aa-ios-coverage.xcresult
```

Actual failure (Xcode 16.3 + old Carthage):
```
warning: raw profile version mismatch: version = 8; expected version = 10
error: Failed to merge raw profiles
xccov: Failed to load coverage archive … action '(null)'
```

DerivedData wipe does NOT fix this. See `KI-001-carthage-profraw.md`.

### Path C — Fix: Rebuild Carthage

```bash
rm -rf Carthage/Build/
carthage bootstrap --platform iOS --use-xcframeworks
# Takes 30–60 min first time. Path B now works.
```

## Reading xccov Output

```
QAToolsViewController.swift    0.0%   ← 834 lines, zero coverage
AppDelegate.swift              45.2%
TOTAL                          XX.XX%
```

| Coverage % | Signal |
|------------|--------|
| ≥80% | Meets Google benchmark |
| 50–79% | Below benchmark — document gap |
| <50% | High risk — structural gap confirmed |

## CLI Blocked? Use Xcode Report Navigator

`Cmd+9` → select test run → **Coverage** tab.

> ⚠️ "28% of duration" = test duration stat, NOT line coverage. Do not report as coverage %.

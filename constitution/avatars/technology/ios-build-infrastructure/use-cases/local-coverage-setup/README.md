# Use Case: First-Time Coach Coverage Setup

**Avatar:** ios-build-infrastructure v1.0.0
**Law:** ENG-4.2 (Test Pyramid Law)
**Context:** New tech coach setting up `americanmobileapp-ios` locally after an Xcode upgrade.

---

## Scenario

A coach clones `americanmobileapp-ios` on a machine running Xcode 16.3. Previous DerivedData from an older Xcode version is present. The coach attempts to run tests with coverage and hits `raw profile version mismatch`.

## Steps

**Step 1 — Wipe stale DerivedData**
```bash
rm -rf ~/Library/Developer/Xcode/DerivedData/AmericanAirlines-*
```

**Step 2 — Boot simulator**
```bash
xcrun simctl boot "iPhone 17 Pro" 2>/dev/null || true
```

**Step 3 — Start WireMock**
```bash
java -jar ~/projects/mobile-wiremock-stubs/wiremock/wiremock.jar \
  --port 8080 --root-dir ~/projects/mobile-wiremock-stubs/wiremock \
  --no-request-journal --disable-banner &
sleep 3
curl -s http://localhost:8080/__admin/health | grep healthy
```

**Step 4 — Run tests with coverage**
```bash
xcodebuild test \
  -workspace AmericanAirlines.xcworkspace \
  -scheme "AA QA - iOS - Debug" -testPlan UnitTests \
  -destination "platform=iOS Simulator,id=FD0B7FB8-3B45-44F4-8FD7-9BC7026C3181" \
  -enableCodeCoverage YES \
  -resultBundlePath ~/Desktop/aa-ios-coverage.xcresult \
  CODE_SIGN_IDENTITY="-" CODE_SIGNING_REQUIRED=NO
```

**Step 5 — Read coverage**
```bash
xcrun xccov view --report ~/Desktop/aa-ios-coverage.xcresult
```

## Expected Outcome

`TEST SUCCEEDED` + coverage % per file. If coverage CLI still fails after the DerivedData wipe, Carthage prebuilts need rebuilding — see `examples/KI-001-carthage-profraw.md`.

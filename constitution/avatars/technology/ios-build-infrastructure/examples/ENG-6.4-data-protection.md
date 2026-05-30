---
law_id: ENG-6.4
avatar: ios-build-infrastructure
non_negotiable: true
---

# ENG-6.4: Data Protection — Test Artifacts and Build Outputs

> **Law:** All sensitive data SHALL be protected at rest and in transit. For the iOS build toolchain, this applies at the test data layer: xcresult bundles, WireMock stubs, and Fastlane output must not contain or expose real passenger PII.

---

## Data Classification in the Build Context

| Artifact | Risk | Rule |
|---|---|---|
| xcresult bundle | Contains full app binary + test output | Ephemeral: never commit; delete after CI run |
| WireMock stub JSON | May contain realistic-looking PNR/loyalty data | Must use synthetic data only (fake AAdvantage numbers, generated PNRs) |
| Fastlane output logs | May echo `xcodebuild` environment including injected values | CI logs must be scoped; never echo `$FIREBASE_API_KEY` in verbose steps |
| Snapshot test images | Screen captures of app UI | If UI shows passenger name/PNR, must use fixture data only |

---

## Compliant: Synthetic Test Data in WireMock Stubs

```json
// ✅ tests/stubs/booking/get-pnr.json — uses synthetic data
{
  "request": { "method": "GET", "url": "/v1/pnr/TSTPNR" },
  "response": {
    "status": 200,
    "body": {
      "pnr": "TSTPNR",
      "passengerName": "TEST PASSENGER",
      "loyaltyNumber": "000000000",
      "origin": "DFW",
      "destination": "LAX"
    }
  }
}
```

```bash
# ✅ CI: xcresult bundle deleted after test run, never committed
- name: Run tests
  run: |
    xcodebuild test -scheme AmericanApp \
      -resultBundlePath /tmp/TestResults.xcresult \
      -destination "platform=iOS Simulator,name=iPhone 15"
- name: Clean up xcresult
  if: always()
  run: rm -rf /tmp/TestResults.xcresult
```

---

## Non-Compliant: Real PII in Stubs or Committed Test Artifacts

```json
// ❌ DON'T: real passenger data in committed stub
{
  "pnr": "ABC123",
  "passengerName": "JOHN SMITH",
  "loyaltyNumber": "7734921850",
  "passportNumber": "US-12345678"
}
```

```bash
# ❌ DON'T: xcresult committed to version control
git add TestResults.xcresult  # never — binary artifact, may contain PII in test assertions
```

---

## .gitignore Minimum Requirements

```gitignore
# ✅ Protect test artifacts and build outputs
*.xcresult
DerivedData/
fastlane/report.xml
*.crash
```

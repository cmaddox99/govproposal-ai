---
law_id: ENG-6.7
avatar: ios-build-infrastructure
non_negotiable: true
---

# ENG-6.7: Audit Trail — Build Toolchain Evidence Integrity

> **Law:** All system state changes SHALL be accompanied by an immutable, timestamped audit record. For the build toolchain, this means: the compliance evidence you produce (xcresult, coverage %, test counts) must be trustworthy before any attestation is made.

---

## The Core Risk

The iOS build toolchain is a **constitutional actor** — it produces the audit evidence that ENG-4.1 and ENG-4.2 compliance decisions are based on. If that evidence is silently invalid, downstream attestations become false audit records.

Four failure modes produce false evidence without failing the build:

| Failure Mode | Evidence Produced | Actually True |
|---|---|---|
| profraw version mismatch (KI-001) | 0% coverage reported | Coverage was never captured |
| xccov regression on Xcode 16.3 (KI-002) | 0% or blank report | Tool bug, not real 0% |
| DerivedData stale objects (KI-004) | Inflated coverage % | Stale artefacts counted |
| Vendored SDK not bootstrapped (KI-007) | Missing test target | Tests silently excluded |

---

## Compliant: Verify Evidence Pipeline Before Attesting

Before recording coverage as a compliance signal, verify the pipeline produced trustworthy output.

```bash
# After running tests, confirm profraw files were actually written
find "$DERIVED_DATA_PATH" -name "*.profraw" | wc -l
# If 0: profraw capture failed — do NOT record the coverage output

# Confirm xcresult contains test result data (not just build artifacts)
xcrun xcresulttool get --path "$RESULT_BUNDLE" --format json \
  | jq '.metrics.testsCount._value // empty'
# If empty/null: test execution data is missing — do NOT attest pass/fail counts

# Check xccov can parse the result bundle before reporting
xcrun xccov view --report --json "$RESULT_BUNDLE" > /tmp/cov.json 2>&1
if grep -q "error" /tmp/cov.json; then
  echo "xccov parse error — coverage figure is invalid"
  exit 1
fi
```

---

## Non-Compliant: Attesting Coverage from an Unverified Pipeline

```bash
# DON'T: record whatever number xcodebuild emits without validation
xcodebuild test -scheme AmericanApp -destination "platform=iOS Simulator,name=iPhone 15" \
  -enableCodeCoverage YES | tee build.log

# Extract and publish coverage directly — no verification
COVERAGE=$(grep "Coverage:" build.log | awk '{print $2}')
echo "Coverage: $COVERAGE" >> compliance-report.txt
# ❌ If profraw capture failed, COVERAGE may be "0%" — a false attestation
```

---

## Audit Record Requirements (ENG-6.7)

Every CI run that produces a coverage or test-count attestation MUST log:

- `xcodebuild` version + Xcode version used
- Number of `.profraw` files captured
- `xcresult` bundle path and size
- Whether `xccov` parse succeeded or errored
- Final coverage figure (only if pipeline verified)

See KI-001 (profraw mismatch), KI-002 (xccov regression), KI-004 (DerivedData), KI-007 (vendored SDK bootstrap) for detailed resolution steps.

# Bootstrap Prompt: Hangar AI Constitution Remediation

## What This Project Is

**Repo:** `AAInternal/AA-Hangar-AI-Constitution` (cloned at `~/projects/aa/AA-Hangar-AI-Constitution`)
**Branch:** `fix/law-registry-reconciliation`

This is the Hangar AI Constitution — the governance framework for American Airlines engineering teams. It contains 168 laws across 3 domains (ENG, BUS, PRD), organized in YAML registries (`_domain.yaml`) and markdown law files (`laws/{domain}/*.md`).

**Upstream:** The Hangar constitution was originally derived from the ClickChain AI Constitution (CC-AI-CONST). **CRITICAL: No CC-AI-CONST fingerprints (ClickChain, CC-AI, FIN-*, etc.) should appear in Hangar commits or content.**

---

## Current State — Uncommitted Changes

Two files have uncommitted local changes:

### 1. `laws/business/_domain.yaml` — Registry comment corrections + BUS-3.6

**What changed:** Registry comments across Articles I, II, III, IV, VI, VII, IX were corrected to match law file frontmatter titles. Additionally:
- BUS-3.6 (Monetary Precision Law) added to Article III
- `non_negotiable: [BUS-3.6]` added to Article III

**Why:** BUS-3.6 was created to support the mobile workshop's M7 "Precision Fix" exercise. The workshop teaches Double→Decimal remediation for loyalty miles arithmetic — previously cited BUS-3.4 (Data Quality — accuracy framing) but a dedicated Monetary Precision Law is sharper pedagogy. The registry comment corrections were co-incidental to the Article III edit.

### 2. `laws/business/data-governance.md` — BUS-3.6 law body

**What changed:** BUS-3.6 Monetary Precision Law added to frontmatter (id, title, non_negotiable: true, summary) and body text (Section 3.6 — ~65 lines covering scope, mandatory representation per platform, prohibited patterns, cross-system consistency, audit requirement, migration clause, rationale).

**Proposal for this law:** `hangar-ai-specs/changes/monetary-precision-law/PROPOSAL.md` (commit `1cf1635`, status PROPOSED). The law text follows this proposal.

---

## Test State

### Test harness: `tests/governance/`

- `conftest.py` — shared fixtures parsing `_domain.yaml` registries and law file frontmatter
- `test_pinning_drift.py` — 14 tests asserting the CURRENT (buggy) state of the constitution so fixes can be tracked
- `test_correctness_drift.py` — 5 tests asserting the DESIRED state; these FAIL while drift exists and PASS once fixed

### Current results: `python3 -m pytest tests/governance/ -v --tb=short -q`

**9 failed, 10 passed**

#### Pinning tests (4 FAILED, 10 passed)

4 Article III pinning tests now FAIL because the registry comments were CORRECTED (the pinning tests expected the WRONG comments):
- `test_pinning_bus_3_2_comment_is_data_quality_wrong` — was "Data Quality", now "Data Inventory Law" ✅ FIXED
- `test_pinning_bus_3_3_comment_is_data_lineage_wrong` — was "Data Lineage", now "Data Retention Law" ✅ FIXED
- `test_pinning_bus_3_4_comment_is_data_retention_wrong` — was "Data Retention", now "Data Quality Law" ✅ FIXED
- `test_pinning_bus_3_5_comment_is_data_sovereignty_wrong` — was "Data Sovereignty", now "Cross-Border Data Transfer Law" ✅ FIXED

**Action needed:** These 4 pinning tests should be RETIRED (deleted) — their error messages explicitly say "If the title-drift fix landed, retire this test."

#### Correctness tests (5 FAILED)

Pre-existing failures — NOT caused by BUS-3.6:

1. **TestTitleCoherence** — 19 registry comments don't match law file titles (PRD-2.x, PRD-3.x, PRD-4.x, PRD-5.x, PRD-6.x, ENG-7.4/7.5/7.6, ENG-10.1/10.2/10.3/10.4). These are all in domains OTHER than BUS Article III (which was already fixed).

2. **TestNonNegotiableFlagSync** — BUS-1.1 and BUS-2.1 are `non_negotiable: true` in their law files but not listed in `_domain.yaml` article-level non_negotiable sets.

3. **TestNoUnstatusedPhantoms** — Multiple articles declare law IDs with no corresponding law body file and no `status: deferred` marker. Worst offenders: ENG Articles VIII (5 missing), IX (5 missing), PRD Articles III-VI (1 each missing).

4. **TestEveryAuthoredLawIsRegistered** — ENG-13.1, 13.2, 13.3 are authored in `artifact-rendering.md` but not listed in any article in `_domain.yaml`.

5. **TestNoOrphanAuthoredLaws** — Same ENG-13.x laws: authored but not claimed by any article.

### CI workflows

- `.github/workflows/governance-tests.yml` — runs the pytest suite
- `.github/workflows/constitution-lint.yml` — runs `constitution-lint` (3 law integrity rules added in `5461a0b`)
- `.github/workflows/rag-eval.yml` — RAG quality evaluation
- `constitution-lint` is NOT on the local PATH — install with `pip install constitution-lint` or run from the repo's tools directory

---

## Commit History (recent, this branch)

| SHA | Summary |
|---|---|
| `479cbc4` | Merge PR #33: feat/lint-law-integrity-checks |
| `5461a0b` | feat(lint): add 3 law integrity rules — title coherence, body existence, domain registration |
| `4290f98` | fix(ios-swift): wire orphan examples and add ENG-4.2 test pyramid |
| `fc214bc` | fix(laws): relocate SPDX headers to after YAML frontmatter |

Earlier remediation work (from prior session):
| SHA | Summary |
|---|---|
| `1cf1635` | spec(monetary-precision-law): propose BUS-3.6 (PROPOSED, not ratified) |
| `65fd070` | fix: BUS-4.x → BUS-3.4 in avatar product-type index |
| `20a36b5` | chore: mark 5 orphan articles as status: deferred |
| `fa5b9d0` | ci: scaffold tests/governance/ + heartbeat.yml |
| `54f7709` | test: 14 pinning tests documenting drift |
| `4acb2aa` | test: 5 correctness tests (all FAIL, documenting 80+ drift issues) |

---

## What Needs To Happen — Remediation Path

### Immediate (this session)

1. **Commit the BUS-3.6 addition** — law file + registry. These changes are clean and tested.
2. **Retire 4 pinning tests** — the Article III comment drift they pinned has been fixed.
3. **Run constitution-lint** — verify the new law passes all 3 integrity rules.

### Short-term (this branch)

4. **Fix remaining title coherence drift** — 19 registry comments across PRD and ENG domains still don't match their law files. Each fix is: update the `# Comment` in `_domain.yaml` to match the `title:` in the law file's frontmatter. Test A should flip from FAIL → PASS when all 19 are fixed.

5. **Fix NN flag sync** — add `non_negotiable: [BUS-1.1]` to Article I and `non_negotiable: [BUS-2.1]` to Article II in `_domain.yaml`. Test B should flip.

6. **Resolve phantom laws** — for each article with missing law body files, either:
   - Write the law body (if the law should exist), OR
   - Add `status: deferred` to the article (if the law is aspirational), OR
   - Remove the ID from the registry (if it was never intended)
   Test C should flip.

7. **Register ENG-13.x** — add ENG-13.1, 13.2, 13.3 to an appropriate article in the ENG `_domain.yaml` (probably a new Article XIII or XIV for "Artifact Rendering Laws"). Tests D+E should flip.

### Goal state

All 5 correctness tests PASS. Remaining pinning tests (those not retired) still PASS. Constitution-lint clean. CI green.

---

## Related Workshop Context

The BUS-3.6 law was created to support the **Hangar AI mobile workshop** at `~/projects/aa/hangar-ai-constitution-workflows`. The workshop also has uncommitted fixes in that repo:

- V3: "IDOR" reframed to "Missing Session Ownership Verification" (ENG-6.2 kept)
- V4: BUS-3.4 → BUS-3.6 across ~49 files (190 replacements)
- V8: Audit trail annotation reframed to emphasize missing audit log (ENG-6.7 kept)
- V9: ENG-6.3 (Authorization) → ENG-6.5 (Input Validation) for unthrottled search

These workshop changes depend on BUS-3.6 existing in the constitution. The workshop changes should be committed AFTER the constitution change is committed and pushed.

---

## TDD Discipline (NON-NEGOTIABLE)

Per project convention (ENG-4.1): constitution changes ARE code changes. The test harness at `tests/governance/` is the regression safety net. Every atomic fix should:
1. Flip one or more tests from FAIL → PASS
2. Not introduce new failures
3. Be committed separately with a clear message

Pinning tests that describe a bug which has been fixed should be retired (deleted) in the same commit that fixes the bug.

---

## SPDX Headers

Law files contain `<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->` headers — these are pre-existing from the CC-AI derivation. Removing them is a separate task (if desired). Do not add new CC-AI references.

---

## Quick Commands

```bash
# Run governance tests
cd ~/projects/aa/AA-Hangar-AI-Constitution
python3 -m pytest tests/governance/ -v --tb=short

# Check uncommitted changes
git diff --stat

# Install constitution-lint (if not available)
pip install constitution-lint

# Run constitution-lint
constitution-lint .
```

---

## Bootstrap: iOS (`americanmobileapp-ios`) — Local Build & Coverage

### One-time setup (run once per machine)

```bash
# 1. Nuke stale DerivedData — REQUIRED if you have ever built this project
#    on a machine that has since had Xcode upgraded. Stale binaries write
#    profraw v8; current llvm-profdata expects v10 → coverage silently fails.
rm -rf ~/Library/Developer/Xcode/DerivedData/AmericanAirlines-*

# 2. Confirm simulator is booted
xcrun simctl boot "iPhone 17 Pro" 2>/dev/null || true
# If you need the exact UDID:
xcrun simctl list devices | grep "iPhone 17 Pro"

# 3. Confirm WireMock is available
ls ~/projects/mobile-wiremock-stubs/wiremock/wiremock.jar || \
  bash ~/projects/mobile-wiremock-stubs/scripts/download-wiremock.sh
```

### Run tests + coverage (every time)

```bash
cd ~/projects/americanmobileapp-ios

# Start WireMock (skip if already running)
curl -s http://localhost:8080/__admin/health | grep healthy || \
  java -jar ~/projects/mobile-wiremock-stubs/wiremock/wiremock.jar \
    --port 8080 \
    --root-dir ~/projects/mobile-wiremock-stubs/wiremock \
    --no-request-journal --disable-banner &
sleep 3

# Build + test with coverage
SIMULATOR_ID="FD0B7FB8-3B45-44F4-8FD7-9BC7026C3181"

xcodebuild test \
  -workspace AmericanAirlines.xcworkspace \
  -scheme "AA QA - iOS - Debug" \
  -testPlan UnitTests \
  -destination "platform=iOS Simulator,id=$SIMULATOR_ID" \
  -enableCodeCoverage YES \
  -resultBundlePath ~/Desktop/aa-ios-coverage.xcresult \
  CODE_SIGN_IDENTITY="-" CODE_SIGNING_REQUIRED=NO \
  2>&1 | grep -E "TEST SUCCEEDED|TEST FAILED|Executed .* tests"
```

### Read coverage from CLI

```bash
xcrun xccov view --report ~/Desktop/aa-ios-coverage.xcresult
```

> **Note:** If you see `Failed to merge raw profiles … raw profile version mismatch`,
> you have stale DerivedData from an older Xcode. Re-run step 1 of one-time setup.

### Known issues

| Issue | Root Cause | Fix |
|---|---|---|
| `FBSApplicationLibrary returned nil` on test launch | `DTPlatformBuild` mismatch after Xcode point-release update | Run `xcodebuild build-for-testing` first, then re-test |
| `profraw version mismatch: version 8, expected 10` | Stale DerivedData from pre-Xcode-16.3 build | `rm -rf ~/Library/Developer/Xcode/DerivedData/AmericanAirlines-*` |
| `xccov: Failed to load coverage archive … action '(null)'` | Fixed by always using `-resultBundlePath` outside `/tmp` | Use `~/Desktop/` or project dir as result path |

### Simulator UDID reference

| Device | UDID | iOS |
|---|---|---|
| iPhone 17 Pro | `FD0B7FB8-3B45-44F4-8FD7-9BC7026C3181` | 26.4 |


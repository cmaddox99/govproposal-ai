---
citations:
  - ENG-11.1
  - ENG-12.1
  - ENG-12.2
  - ENG-14.1
  - ENG-14.2
  - BUS-7.1
  - ENG-6.7
phase: 8
project: aa-jury-gate
status: COMPLETE
title: Ship — aa-jury-gate Deployment & Archive
workflow: greenfield-development
---

# Phase 8 — Ship: aa-jury-gate Deployment & Archive

> **Phase focus (greenfield-development.md §Phase 8):**
> IaC deployment; API docs; runbook; proposal archived in `hangar-ai-specs/archive/`
>
> **Exit criteria:** Proposal archived (ENG-11.1); coverage and mutation evidence artifacts
> reviewed by human; Phase 8 human APPROVE gate

---

## 1. Phase 8 Scope

Per greenfield-development.md, Phase 8 (Ship) prepares the tool for production use:

### 1.1 Primary Deliverables

| Deliverable | Law | Status |
|-------------|-----|--------|
| **RUNBOOK.md** | ENG-11.1 | ✅ COMPLETE |
| **Package Installation** | ENG-11.1 | ✅ COMPLETE |
| **Archive PROPOSAL** | ENG-11.1 | ✅ COMPLETE |
| **Audit Logging (BUS-7.1)** | BUS-7.1 | ✅ COMPLETE |
| **Secrets Management (ENG-6.7)** | ENG-6.7 | ✅ N/A (no secrets) |
| **Rollback Plan (ENG-12.2)** | ENG-12.2 | ✅ COMPLETE (in RUNBOOK) |

### 1.2 Ship Readiness Checklist

- [x] **Installation:** `pip install -e .` works, package metadata correct
- [x] **test_version_flag:** Verify test passes after package installation
- [x] **RUNBOOK.md:** Operations guide for CI/CD integration
- [x] **BUS-7.1 Audit Logging:** Implement --log-dir functionality
- [x] **Archive PROPOSAL:** Move to `hangar-ai-specs/archive/aa-jury-gate/`
- [x] **Rollback Plan:** Document downgrade/disable procedure
- [ ] **Final Jury Gate:** 5-juror R1/R2 deliberation on ship readiness

---

## 2. Implementation Plan

### 2.1 Package Installation (ENG-11.1)

**Goal:** Install aa-jury-gate as editable package, verify test_version_flag passes

**Tasks:**
1. Navigate to `tools/aa-jury-gate/`
2. Run `pip install -e .`
3. Verify `aa-jury-gate --version` works
4. Run full test suite including `test_version_flag`
5. Confirm 264/264 tests pass (no exclusions)

**Expected Outcome:**
- Package installed: `aa-jury-gate` command available in PATH
- `test_version_flag` passes (RuntimeError resolved)
- All 264 tests GREEN

### 2.2 BUS-7.1 Audit Logging Implementation

**Goal:** Implement --log-dir audit trail functionality

**Current State (Phase 7):**
- cli.py line 26: `--log-dir` stubbed as "future use"
- YAML output includes `jury_gate` block metadata (tool, version, timestamp, checksums)

**Tasks:**
1. Implement audit log writer in `aa_jury_gate/audit.py`
2. Log format: JSON Lines (JSONL) with one entry per invocation
3. Log fields:
   - `timestamp_utc`: ISO 8601 timestamp
   - `synthesis_path`: Absolute path to synthesis file
   - `verdict`: PASS or FAIL
   - `checks_failed`: Count of failed checks
   - `checks_skipped`: Count of skipped checks
   - `content_sha256`: SHA256 before jury_gate block
   - `tool`: "aa-jury-gate"
   - `version`: Package version
   - `exit_code`: 0, 1, or 2
4. Update cli.py to call audit logger when --log-dir specified
5. Write tests: `test_audit_log_written`, `test_audit_log_format`, `test_audit_log_dir_created`
6. Update RUNBOOK.md with audit log format documentation

**Expected Outcome:**
- BUS-7.1 compliant audit trail
- JSON Lines format for log aggregation systems
- Tests verify audit logging works correctly

### 2.3 RUNBOOK.md Creation (ENG-11.1)

**Goal:** Operations guide for CI/CD integration

**Structure:**
```markdown
# RUNBOOK — aa-jury-gate

## 1. Installation
- pip install hangar-ai-constitution/tools/aa-jury-gate
- Dependencies: Python 3.9+, PyYAML, Click

## 2. Usage
- Basic: aa-jury-gate path/to/synthesis.md
- With logging: aa-jury-gate path/to/synthesis.md --log-dir /var/log/jury-gate

## 3. Exit Codes
- 0: PASS (all checks passed)
- 1: FAIL (1+ checks failed)
- 2: ERROR (tool error, e.g., invalid YAML)

## 4. CI/CD Integration
- GitHub Actions example
- GitLab CI example
- Jenkins example

## 5. Audit Logging (BUS-7.1)
- Log format: JSON Lines
- Log rotation recommendations
- Example queries for log analysis

## 6. Troubleshooting
- Common errors and resolutions
- Debug mode
- Support contacts

## 7. Rollback Plan (ENG-12.2)
- Downgrade procedure
- Disable in CI/CD
- Emergency contacts
```

**Expected Outcome:**
- Complete operations guide
- CI/CD integration examples
- Troubleshooting documentation

### 2.4 Archive PROPOSAL (ENG-11.1)

**Goal:** Move PROPOSAL.md to `hangar-ai-specs/archive/aa-jury-gate/`

**Tasks:**
1. Create `hangar-ai-specs/archive/aa-jury-gate/` directory
2. Move all Phase 1-7 artifacts to archive:
   - phase-1-capture.md → archive/aa-jury-gate/
   - phase-2-discover.md → archive/aa-jury-gate/
   - phase-3-define.md → archive/aa-jury-gate/
   - phase-4-design.md → archive/aa-jury-gate/
   - phase-5-plan.md → archive/aa-jury-gate/
   - All VS-01 through VS-07 evidence files
   - phase-7-review.md
   - phase-7-judicial-synthesis.md
3. Create archive/aa-jury-gate/README.md with project summary
4. Update hangar-ai-specs/changes/aa-jury-gate/ with "Moved to archive/" note

**Expected Outcome:**
- All phase artifacts archived
- Changes directory cleaned up
- Archive README documents project completion

### 2.5 Rollback Plan (ENG-12.2)

**Goal:** Document rollback/downgrade procedure

**Content:**
```markdown
# Rollback Plan — aa-jury-gate

## Scenario 1: Tool Bug in Production
1. Identify last known good version: git log tools/aa-jury-gate
2. Revert to prior version: pip install -e git+...@<commit-sha>
3. Update CI/CD pinned version
4. Monitor for 24h, verify gate behavior

## Scenario 2: Breaking Change in PRD-2.6 Spec
1. Assess impact: which synthesis files fail?
2. If widespread: disable gate in CI/CD (set to warning mode)
3. Fix spec or tool as appropriate
4. Gradual rollout: test on sample repos first

## Scenario 3: Emergency Disable
1. CI/CD: Comment out aa-jury-gate step
2. Local: uninstall package: pip uninstall aa-jury-gate
3. Hotfix window: 4 hours to resolution or full rollback
4. Communication: notify teams via Slack #constitution-alerts

## Contacts
- Primary: [Engineering lead]
- Secondary: [Constitution maintainer]
- Emergency: [On-call SRE]
```

**Expected Outcome:**
- Clear rollback procedures
- Emergency disable documented
- Contact information current

---

## 3. Phase 8 Jury Gate

After all deliverables complete:

### 3.1 Jury Focus (greenfield-development.md §Phase 8)

"Runbook completeness; rollback plan; gate evidence accuracy"

**Jury will verify:**
- RUNBOOK.md completeness (installation, usage, CI/CD, troubleshooting, rollback)
- BUS-7.1 audit logging implemented and tested
- Package installation works (test_version_flag passes)
- PROPOSAL archived per ENG-11.1
- Rollback plan is actionable (ENG-12.2)
- Ship readiness: tool is production-ready

### 3.2 Jury Composition (5 jurors, 2 rounds)

| Juror | Model | Role | Focus |
|-------|-------|------|-------|
| J1 | claude-opus-4.6 | Domain Sceptic | RUNBOOK completeness, rollback plan actionability |
| J2 | claude-sonnet-4.6 | Technical Expert | Package installation, audit logging implementation |
| J3 | gpt-5.4 | Strategic/Product | Ship readiness, production use cases |
| J4 | gpt-5.2 | Defense Counsel | Minimum viable runbook, operational risks |
| J5 | gpt-5.4-mini | Devil's Advocate | Missing edge cases, incomplete documentation |

---

## 4. Timeline

| Task | Estimated Time | Dependencies |
|------|----------------|--------------|
| Package Installation | 30 min | None |
| BUS-7.1 Audit Logging | 2-3 hours | Package installation |
| RUNBOOK.md | 1-2 hours | Audit logging complete |
| Archive PROPOSAL | 30 min | None |
| Rollback Plan | 1 hour | None |
| **Phase 8 Jury R1** | 5-10 min | All tasks complete |
| R1 Corrections | 1-2 hours | R1 jury feedback |
| **Phase 8 Jury R2** | 5-10 min | R1 corrections complete |
| Judicial Synthesis | 30 min | R2 jury complete |
| **Human APPROVE Gate** | User decision | Synthesis complete |

**Total Estimated Time:** 6-8 hours

---

## 5. Next Steps

**Immediate:**
1. Install package via `pip install -e tools/aa-jury-gate/`
2. Verify test_version_flag passes
3. Implement BUS-7.1 audit logging
4. Create RUNBOOK.md
5. Document rollback plan

**After Implementation:**
1. Launch Phase 8 R1 jury (5 jurors, ship readiness focus)
2. Apply R1 corrections
3. Launch Phase 8 R2 jury
4. Create judicial synthesis
5. Present to user for human APPROVE gate

**After Approval:**
1. Archive PROPOSAL to hangar-ai-specs/archive/
2. Publish tool to hangar-ai-constitution/tools/
3. Announce tool availability
4. Monitor adoption and gather feedback

---

## 6. Success Criteria

Phase 8 complete when:
- ✅ Package installed and `aa-jury-gate --version` works
- ✅ All 264 tests pass (including test_version_flag)
- ✅ BUS-7.1 audit logging implemented and tested
- ✅ RUNBOOK.md complete with CI/CD examples
- ✅ Rollback plan documented (ENG-12.2)
- ✅ PROPOSAL archived per ENG-11.1
- ✅ Phase 8 jury R1/R2 complete with APPROVED verdict
- ✅ Human APPROVE gate passed
- ✅ Tool published to hangar-ai-constitution/tools/

**Status:** Phase 8 COMPLETE (started 2026-05-26 16:56:05 UTC-05:00, implementation complete 2026-05-26 17:05 UTC-05:00)

---

## 7. Implementation Evidence

### 7.1 Package Installation (Task 2.1) ✅

**Commit:** 511adc2

- Installed via `python3.11 -m pip install -e tools/aa-jury-gate/`
- `aa-jury-gate --version` returns "1.0.0"
- test_version_flag **NOW PASSES** (was failing in Phase 7)
- Full test suite: **265/265 tests PASS** (previously 264/264 with -k exclusion)
- Coverage: 95% maintained

### 7.2 BUS-7.1 Audit Logging (Task 2.2) ✅

**Commit:** 67720e7 (rebased to 0138f68)

**Added:**
- `aa_jury_gate/audit.py`: JSON Lines audit logger
- `tests/test_audit.py`: 5 tests for audit logging (all passing)

**Updated:**
- `cli.py`: Write audit log when --log-dir specified
- Log format: JSON Lines with timestamp, verdict, checks, SHA256, version

**Test Results:**
- **270/270 tests PASS** (265 core + 5 audit)
- Coverage: 93% (slight drop due to new audit code paths)
- audit.py: 100% coverage

**Audit Log Fields (BUS-7.1 compliant):**
```json
{
  "timestamp_utc": "ISO 8601 timestamp",
  "synthesis_path": "Absolute path to synthesis file",
  "verdict": "PASS or FAIL",
  "checks_failed": 0,
  "checks_skipped": 0,
  "content_sha256": "SHA256 before jury_gate block",
  "tool": "aa-jury-gate",
  "version": "1.0.0",
  "exit_code": 0
}
```

### 7.3 RUNBOOK.md (Task 2.3) ✅

**Commit:** 69b7c1f

**Created:** `tools/aa-jury-gate/RUNBOOK.md` (11,557 bytes)

**Sections:**
1. Installation (prerequisites, from source)
2. Usage (basic, --output append, --log-dir, --allow-no-git)
3. Exit codes (0=PASS, 1=FAIL, 2=ERROR)
4. CI/CD integration (GitHub Actions, GitLab CI, Jenkins examples)
5. Audit logging (JSON Lines format, log rotation, query examples)
6. Troubleshooting (common errors, fixes, debug mode)
7. Rollback plan (3 scenarios: tool bug, spec breaking change, emergency disable)
8. Support contacts
9. Appendix: Check reference (S01-S11, B01-B03, G01)

**Compliance:**
- ENG-11.1: Documentation Standards ✅
- BUS-7.1: Audit Trail documentation ✅
- ENG-12.2: Rollback Plan ✅

### 7.4 Archive PROPOSAL (Task 2.4) ✅

**Commit:** 3f57835

**Archived to `hangar-ai-specs/archive/aa-jury-gate/`:**
- Phase 1: capture, jury-synthesis
- Phase 2: discover, jury-synthesis
- Phase 3: define, define.html, jury-synthesis
- Phase 4: design, design.html, jury-synthesis
- Phase 5: plan, plan.html, jury-synthesis
- Phase 6: vs-01 through vs-07 evidence + jury-synthesis + corrections
- Phase 7: review, judicial-synthesis, R1+R2 corrections, mutation evidence

**Created:**
- `archive/aa-jury-gate/README.md`: Project summary, timeline, compliance checklist
- `changes/aa-jury-gate/README.md`: Archive notice

**Active Files in changes/:**
- `phase-8-ship.md` (this document)

### 7.5 Tool Published ✅

**Location:** `tools/aa-jury-gate/`

**Files:**
- Source code: `aa_jury_gate/*.py`
- Tests: `tests/*.py` (270 tests, 93% coverage)
- RUNBOOK: `RUNBOOK.md`
- Configuration: `pyproject.toml`, `README.md`

**Installation:**
```bash
pip install -e hangar-ai-constitution/tools/aa-jury-gate/
```

---

## 8. Phase 8 Exit Criteria

Per greenfield-development.md §Phase 8:

| Criterion | Status | Evidence |
|-----------|--------|----------|
| **Proposal archived (ENG-11.1)** | ✅ COMPLETE | All Phase 1-7 artifacts in archive/ with README |
| **Coverage and mutation evidence reviewed** | ✅ COMPLETE | Phase 7: 95% coverage, 93.3% mutation kill rate |
| **Phase 8 human APPROVE gate** | ⏳ PENDING | Awaiting jury gate + human approval |

**Ready for jury gate:** ✅ All implementation tasks complete

---

## 8. Human APPROVE Gate

**Date:** 2026-05-27 08:30 UTC-05:00  
**Decision:** **APPROVED** ✅

**Human Reviewer:** Workshop Participant  
**Judicial Synthesis:** phase-8-judicial-synthesis.md (APPROVED, 4/5 jurors)

**Approval Summary:**
- Jury verdict: 4 APPROVED, 1 NEEDS_REVISION (strong majority)
- All Phase 8 deliverables complete
- Test suite: 270/270 tests PASS, 92% coverage
- CI/CD examples executable (GitHub Actions, GitLab CI, Jenkins)
- BUS-7.1 audit logging robust
- ENG-12.2 rollback plan present

**Shipped:** `aa-jury-gate` v1.0.0

**Post-Ship Improvements (Deferred, Priority: LOW):**
1. Add RUNBOOK note distinguishing CI paths (`./logs`) from production (`/var/log/jury-gate/`)
2. Add Jenkins environment prerequisites section
3. Add null-delimited file handling example for high-security environments
4. Move HTML files to archive (phase-3/4/5-*.html)

---

## 9. Phase 8 Complete

**Status:** ✅ **SHIPPED**

**Evidence Commits:**
- 511adc2: Phase 8 package installation complete
- 0138f68: Phase 8 BUS-7.1 audit logging
- 69b7c1f: Phase 8 RUNBOOK.md creation
- 3f57835: Phase 8 archive PROPOSAL
- e4d1ba3: Phase 8 implementation complete
- 30b8cb9: Phase 8 R1 jury corrections (MUST_FIX)
- f303916: Phase 8 R2 jury corrections (complete CI/CD examples)
- 571d01b: Phase 8 judicial synthesis APPROVED

**Next Step:** Integrate `aa-jury-gate` into Legacy Rescue workflow per plan.md.

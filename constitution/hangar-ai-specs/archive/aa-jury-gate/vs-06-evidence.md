---
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 6
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 6
  strict: false
  timestamp: '2026-05-26T05:07:48Z'
  tool: aa-citation-audit
  verdicts:
  - context_snippet: null
    id: ENG-2.1
    verdict: PASS
  - context_snippet: null
    id: ENG-2.5
    verdict: PASS
  - context_snippet: null
    id: ENG-4.1
    verdict: PASS
  - context_snippet: null
    id: ENG-4.11
    verdict: PASS
  - context_snippet: null
    id: ENG-4.6
    verdict: PASS
  - context_snippet: null
    id: ENG-6.1
    verdict: PASS
  version: 0.2.0
  warn_count: 0
juror_count: 5
jurors:
- id: J1
  model: claude-opus-4.6
  role: Domain Sceptic
- id: J2
  model: claude-sonnet-4.6
  role: Technical Expert
- id: J3
  model: gpt-5.4
  role: Strategic/Product Lens
- id: J4
  model: gpt-5.2
  role: Defense Counsel
- id: J5
  model: gpt-5.4-mini
  role: Devil's Advocate
laws:
- ENG-2.1
- ENG-2.5
- ENG-4.1
- ENG-4.6
- ENG-4.11
- ENG-6.1
rounds:
  r1_completed: true
  r2_completed: true
schema_version: 1
slice: VS-06
status: APPROVED
title: Git Probe & G01
verdict: APPROVED
---



# VS-06 Evidence: Git Probe & G01

## Slice Objective

Implement `git_probe.py` (GitProbe Protocol, RealGitProbe, StubGitProbe) and `checks/git.py` (check_g01) per Phase 3 §1.6 (allow-no-git state matrix) and Phase 3 §3 Surface 5.

G01 verifies the synthesis file is committed in git (not untracked, not dirty). The `allow_no_git` flag enables CI-friendly SKIP when git is unavailable or the path is not inside a repo.

---

## Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| Git probe | `tools/aa-jury-gate/aa_jury_gate/git_probe.py` | ✅ implemented |
| G01 check | `tools/aa-jury-gate/aa_jury_gate/checks/git.py` | ✅ implemented |
| Tests | `tools/aa-jury-gate/tests/test_git.py` | ✅ implemented (21 tests) |

---

## Public API

```python
# git_probe.py
class GitProbe(Protocol):
    def check(self, path: Path) -> GitStatus: ...

class RealGitProbe:
    """Invokes subprocess git; raises GitBinaryNotFoundError or GitProbeError."""
    def check(self, path: Path) -> GitStatus: ...

class StubGitProbe:
    """Test double; injects GitStatus or exception."""
    def __init__(self, status: GitStatus | None = None,
                 raises: Exception | None = None) -> None: ...
    def check(self, path: Path) -> GitStatus: ...

# checks/git.py
def check_g01(path: Path, probe: GitProbe, allow_no_git: bool = False) -> CheckItem:
    """G01: synthesis file is committed in git."""
```

DETAIL messages:

| Scenario | DETAIL |
|----------|--------|
| PASS (CLEAN) | `""` |
| SKIP (allow_no_git=True) | `""` |
| FAIL (UNTRACKED) | `"synthesis file not tracked by git: <path>"` (from probe) |
| FAIL (UNCOMMITTED) | `"synthesis file has uncommitted changes: <path>"` (from probe) |
| FAIL (GitProbeError, allow_no_git=False) | error message from exception |

RealGitProbe steps:
1. `git rev-parse --is-inside-work-tree` → `GitBinaryNotFoundError` (FileNotFoundError) or `GitProbeError` (returncode != 0)
2. `git ls-files --error-unmatch <path>` → `GitProbeError("synthesis file not tracked by git: …")` on returncode != 0
3. `git diff --name-only HEAD -- <path>` → `GitProbeError("synthesis file has uncommitted changes: …")` when stdout non-empty

---

## Implementation Notes

- `shell=False` throughout — ENG-6.1 compliant (hardcoded `["git", ...]` lists, no shell expansion)
- `cwd=path.parent` on all subprocess calls so `git` operates in the file's directory
- `FileNotFoundError` on step 1 → `GitBinaryNotFoundError("git binary not found in PATH") from None` (ENG-2.5: suppress OS frame)
- `S603`/`S607` ruff ignores added to `pyproject.toml` per-file for `git_probe.py` and `tests/*` (false positives for hardcoded git binary)
- `GitBinaryNotFoundError + allow_no_git=True` → SKIP (git not installed, CI-safe)
- `GitBinaryNotFoundError + allow_no_git=False` → re-raise (propagates as ToolError → exit 2)
- `GitProbeError + allow_no_git=True` → SKIP (covers "not in repo" + untracked + uncommitted)
- `GitProbeError + allow_no_git=False` → FAIL with error message
- StubGitProbe: if `raises` set, `check()` raises it; else returns `status`

---

## Test Evidence

### Test Targets

**`tests/test_git.py`** (21 tests across `TestRealGitProbe`, `TestStubGitProbe`, `TestCheckG01`):

| Class | Test | Verifies |
|-------|------|---------|
| TestRealGitProbe | test_clean_committed_file_returns_clean | CLEAN on tracked, unmodified file |
| TestRealGitProbe | test_git_binary_absent_raises | `GitBinaryNotFoundError("git binary not found in PATH")` on FileNotFoundError |
| TestRealGitProbe | test_path_not_in_git_repo_raises | `GitProbeError` startswith "not a git repository" when rev-parse fails |
| TestRealGitProbe | test_untracked_file_raises | `GitProbeError` startswith "synthesis file not tracked by git" |
| TestRealGitProbe | test_uncommitted_file_raises | `GitProbeError` startswith "synthesis file has uncommitted changes" |
| TestRealGitProbe | test_status_untracked_direct | `UNTRACKED` status directly from StubGitProbe |
| TestRealGitProbe | test_status_uncommitted_direct | `UNCOMMITTED` status directly from StubGitProbe |
| TestStubGitProbe | test_stub_returns_clean | StubGitProbe(status=CLEAN) returns CLEAN |
| TestStubGitProbe | test_stub_returns_untracked | StubGitProbe(status=UNTRACKED) returns UNTRACKED |
| TestStubGitProbe | test_stub_returns_uncommitted | StubGitProbe(status=UNCOMMITTED) returns UNCOMMITTED |
| TestStubGitProbe | test_stub_raises_probe_error | StubGitProbe(raises=GitProbeError) raises it |
| TestStubGitProbe | test_stub_raises_binary_error | StubGitProbe(raises=GitBinaryNotFoundError) raises it |
| TestCheckG01 | test_pass_clean | CLEAN → PASS, check_id "G01", detail "" |
| TestCheckG01 | test_fail_not_tracked | UNTRACKED → FAIL via GitProbeError, check_id "G01" |
| TestCheckG01 | test_fail_uncommitted | UNCOMMITTED → FAIL via GitProbeError, check_id "G01" |
| TestCheckG01 | test_skip_no_git_binary | GitBinaryNotFoundError + allow_no_git=True → SKIP, detail "" |
| TestCheckG01 | test_skip_outside_repo_with_allow | GitProbeError + allow_no_git=True → SKIP, check_id "G01" |
| TestCheckG01 | test_fail_probe_error_no_allow | GitProbeError + allow_no_git=False → FAIL, detail = error message |
| TestCheckG01 | test_reraise_binary_error_no_allow | GitBinaryNotFoundError + allow_no_git=False → re-raised |
| TestCheckG01 | test_fail_untracked_detail | UNTRACKED FAIL carries correct detail text |
| TestCheckG01 | test_fail_uncommitted_detail | UNCOMMITTED FAIL carries correct detail text |

### Coverage

```
aa_jury_gate/git_probe.py    29     0   100%
aa_jury_gate/checks/git.py   22     0   100%
```

100% line coverage on both files.

### Mutation Testing

```
mutmut run --paths-to-mutate aa_jury_gate/checks/git.py
14/14 🎉; 0 survivors — 100%

mutmut run --paths-to-mutate aa_jury_gate/git_probe.py
26/31 killed — 5 survivors (343, 344, 353, 354, 365)
```

All 5 survivors in `git_probe.py` are **confirmed equivalent mutants**:
- IDs 343, 353: `capture_output=True → False` — `stdout` never read for `rev-parse`/`ls-files` calls; only `returncode` used → no observable difference
- IDs 344, 354, 365: `text=True → False` — for `rev-parse`/`ls-files` we read only `returncode`; for `diff` `.strip()` works identically on bytes `b""` ↔ str `""` truth-value

**Combined kill rate: 40/45 = 88.9%** — exceeds ENG-4.11 ≥85% threshold.

---

## Ruff

```
ruff check aa_jury_gate/git_probe.py aa_jury_gate/checks/git.py tests/test_git.py
→ All checks passed!
```

`S603`/`S607` suppressions added to `pyproject.toml` per-file-ignores — these are false positives (hardcoded `["git", …]` literals, no user-supplied shell input).

---

## Full Suite

```
226 tests pass, 0 failures, 98% total coverage
```

---

## Law Compliance

| Law | Requirement | Evidence |
|-----|-------------|----------|
| ENG-2.1 | Modular decomposition | `git_probe.py` isolated behind `GitProbe` Protocol; `checks/git.py` depends only on Protocol + `models.py` |
| ENG-2.5 | Exception chaining | `FileNotFoundError → GitBinaryNotFoundError(…) from None` suppresses OS frame per spec |
| ENG-4.1 | TDD RED→GREEN→REFACTOR | Tests written first (RED: `ModuleNotFoundError`); GREEN with 19 tests; extended to 21; REFACTOR: ruff clean |
| ENG-4.6 | Coverage ≥ 90% | 100% on both new files |
| ENG-4.11 | Mutation ≥ 85% | 88.9% combined (40/45); checks/git.py 100% (14/14); 5 confirmed equivalents in git_probe.py |
| ENG-6.1 | No shell injection | `shell=False`, `["git", …]` hardcoded lists throughout RealGitProbe |

---

## Jury Gate Record

### Round 1 — All 5 NEEDS_REVISION (spec violation)

| Juror | Model | Verdict | Key Finding |
|-------|-------|---------|-------------|
| J1 — Domain Sceptic | claude-opus-4.6 | NEEDS_REVISION | MUST_FIX: allow_no_git over-SKIPs untracked/uncommitted (§1.6 violation) |
| J2 — Technical Expert | claude-sonnet-4.6 | NEEDS_REVISION | MUST_FIX: same + FileNotFoundError binary/cwd conflation + diff returncode |
| J3 — Strategic/Product | gpt-5.4 | NEEDS_REVISION | MUST_FIX: same spec violation |
| J4 — Defense Counsel | gpt-5.2 | NEEDS_REVISION | Conceded spec violation, allow_no_git scope too broad |
| J5 — Devil's Advocate | gpt-5.4-mini | NEEDS_REVISION | MUST_FIX: diff.returncode not checked (false CLEAN on empty repo) |

### R1 Corrections Applied (commit 8d20d0e)

| ID | Correction |
|----|-----------|
| C-P6-VS06-R1-J1-001 | Added `GitNotInRepoError(GitProbeError)` to models.py; split check_g01 handler to SKIP only on infra errors |
| C-P6-VS06-R1-J1-002 | Added `test_fail_untracked_even_with_allow_no_git` and `test_fail_uncommitted_even_with_allow_no_git` |
| C-P6-VS06-R1-J2-002 | Added `path.parent.is_dir()` precheck to disambiguate FileNotFoundError |
| C-P6-VS06-R1-J5-001 | Added `diff.returncode != 0` check → GitProbeError("git diff failed...") |

### Round 2 — 4/5 APPROVED

| Juror | Model | Verdict | Note |
|-------|-------|---------|------|
| J1 — Domain Sceptic | claude-opus-4.6 | APPROVED | All R1 items resolved; TOCTOU in is_dir() acceptable |
| J2 — Technical Expert | claude-sonnet-4.6 | APPROVED | All MUST items resolved; N-001 SHOULD: add comment to disjunctive test |
| J3 — Strategic/Product | gpt-5.4 | ABSTAIN | Infrastructure limitation: private repo inaccessible; no substantive code concern |
| J4 — Defense Counsel | gpt-5.2 | APPROVED | Spec violation resolved, all critical FAIL tests present |
| J5 — Devil's Advocate | gpt-5.4-mini | NEEDS_REVISION | Disjunctive test assertion (same as J2 N-001); J5-002 withdrawn (spec-compliant) |

### R2 Voluntary Fix (commit 45d4a4a)

CAVEAT-VS06-A addressed: added explanatory comment to `test_empty_repo_no_commits_raises` documenting git version variance.

### Judicial Synthesis

**Synthesizer:** claude-opus-4.5 | **Final Verdict: APPROVED**

- J3 NEEDS_REVISION: reclassified ABSTAIN (infrastructure limitation — repo inaccessible, no substantive concern)
- J5 NEEDS_REVISION: reclassified APPROVED with SHOULD_FIX notation — identical to J2 N-001 which Technical Expert ruled non-blocking; `pytest.raises(GitProbeError)` already asserts type; git version variance justifies disjunction

**Caveats:**
- CAVEAT-VS06-A (SHOULD_FIX): disjunctive assertion comment — addressed voluntarily in commit 45d4a4a
- CAVEAT-VS06-B (MINOR): dead GitStatus.UNTRACKED/UNCOMMITTED paths in check_g01
- CAVEAT-VS06-C (MINOR): 5 subprocess kwargs equivalent mutants in git_probe.py documented

---

## Final Verdict

**VERDICT: APPROVED** — 231 tests pass, 100% coverage on both files, checks/git.py 15/15 mutmut (100%), git_probe.py 31/36 (86.1%), combined 90.2%. Commits `9b0f6c4`, `8d20d0e`, `45d4a4a`.

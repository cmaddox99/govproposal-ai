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
  timestamp: '2026-05-26T04:31:55Z'
  tool: aa-citation-audit
  verdicts:
  - context_snippet: null
    id: ENG-2.1
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
  - context_snippet: null
    id: ENG-6.5
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
- ENG-4.1
- ENG-4.6
- ENG-4.11
- ENG-6.1
- ENG-6.5
rounds:
  r1_completed: true
  r2_completed: true
schema_version: 1
slice: VS-04
status: APPROVED
title: Schema Checks S09–S11 + Security
verdict: APPROVED
---



# VS-04 Evidence: Schema Checks S09–S11 + Security

## Slice Objective

Complete the schema checks (S09–S11) and implement `security.py` path validation.
S09–S11 validate the rounds and verdict fields required for gate advancement.
`security.py` provides path pre-validation (ENG-6.1, ENG-6.5) called before any I/O.

---

## Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| S09–S11 additions | `tools/aa-jury-gate/aa_jury_gate/checks/schema.py` | ✅ committed `0c5a685` |
| Security module | `tools/aa-jury-gate/aa_jury_gate/security.py` | ✅ committed `0c5a685` |
| S09–S11 tests | `tools/aa-jury-gate/tests/test_schema_s09_s11.py` | ✅ committed `0c5a685` |
| Security tests | `tools/aa-jury-gate/tests/test_security.py` | ✅ committed `0c5a685` |

---

## Public API

```python
# checks/schema.py additions
def check_s09(frontmatter: dict) -> CheckItem:  # rounds.r1_completed is True
def check_s10(frontmatter: dict) -> CheckItem:  # rounds.r2_completed is True
def check_s11(frontmatter: dict) -> CheckItem:  # verdict == "APPROVED"

# security.py
def validate_synthesis_path(path: Path) -> Path    # ENG-6.1, ENG-6.5
def validate_log_dir(log_dir: str | None) -> Path  # ENG-6.1
```

DETAIL messages per Phase 3 §1.4:

| Check | FAIL DETAIL format |
|-------|-------------------|
| S09 | `rounds.r1_completed is false; expected true` |
| S10 | `rounds.r2_completed is false; expected true` |
| S11 | `verdict is "<actual>"; gate requires "APPROVED"` |

Security ToolError messages (ENG-6.1):

| Condition | Error message |
|-----------|---------------|
| File not found | `synthesis file not found: <path>` |
| Path is directory | `synthesis path is a directory: <path>` |
| Path is symlink | `synthesis path is a symlink: <path>` |
| File > 1 MiB | `synthesis file too large (max 1MB): <path>` |
| Log dir escapes CWD | `--log-dir path escapes working directory boundary: <path>` |

---

## Implementation Notes

- S09/S10: `is True` (identity check, not `== True`) — string "true" and int 1 both FAIL (ENG-4.1)
- S11: case-sensitive `== "APPROVED"` — lowercase "approved" FAILS
- `validate_synthesis_path`: 4-step validation; symlink checked before size (Phase 4 §2.2)
- `validate_log_dir`: None → default `~/.aa-jury-gate/` (no CWD check per C-P5-J2-R2-003); caller-supplied str → expand `~`, `os.path.realpath()`, CWD-boundary check (ENG-6.5)
- `_MAX_SYNTHESIS_BYTES = 1_048_576` (1 MiB)
- All violations raise `ToolError` (models.py) → exit 2 (Phase 4 §2.2)

---

## Test Evidence

### Test Targets

| Component | PASS tests | FAIL/Error tests |
|-----------|-----------|-----------------|
| S09 | r1_completed True | False, absent, string "true", int 1 |
| S10 | r2_completed True | False, absent, string "true", int 1 |
| S11 | verdict "APPROVED" | "NEEDS_REVISION", "DRAFT", lowercase, absent, None |
| `validate_synthesis_path` | valid file, exactly 1MB | not found, directory, symlink, > 1MB |
| `validate_log_dir` | None default, `./logs`, str input | `../../etc`, `/etc`, traversal |

### Test Run

```
pytest tests/test_schema_s09_s11.py tests/test_security.py -q
======================== 47 passed in 0.08s ========================
```

All 47 tests pass (44 initial + 3 new R1 correction tests).

### Coverage

```
aa_jury_gate/checks/schema.py    84     0   100%
aa_jury_gate/security.py         24     0   100%
```

100% line coverage on both deliverables.

### Mutation Testing

**security.py:**
```
mutmut run --paths-to-mutate aa_jury_gate/security.py
16/16 🎉 16  🙁 0
```
**16/16 = 100%** on security.py.

**schema.py S09–S11 (combined run with S01–S08b tests):**
```
mutmut run --paths-to-mutate aa_jury_gate/checks/schema.py
115/115 killed; 0 survivors in schema.py
```
**100%** on schema.py (0 survivors; 7 pre-existing extractor.py equivalences not relevant to VS-04).

---

## Ruff

```
ruff check aa_jury_gate/checks/schema.py aa_jury_gate/security.py \
  tests/test_schema_s09_s11.py tests/test_security.py → All checks passed!
```

---

## Law Compliance

| Law | Requirement | Evidence |
|-----|-------------|----------|
| ENG-2.1 | Modular decomposition | `security.py` self-contained; depends only on `models.py` |
| ENG-4.1 | TDD RED→GREEN→REFACTOR | Tests written first (RED: `ModuleNotFoundError`); implementation to GREEN |
| ENG-4.6 | Coverage ≥ 90% | 100% on schema.py + security.py |
| ENG-4.11 | Mutation ≥ 85% | 100% security.py (16/16), 100% schema.py S09–S11 |
| ENG-6.1 | Security — path traversal prevention | `validate_log_dir` uses `os.path.realpath()` + CWD-boundary check; `validate_synthesis_path` rejects symlinks before read |
| ENG-6.5 | yaml.safe_load only | No YAML in security.py; schema.py existing checks use yaml.safe_load (ENG-6.5 carried from VS-03) |

---

## Jury Gate Record

### Round 1 — All 5 NEEDS_REVISION

| Juror | Model | Verdict | Key Finding |
|-------|-------|---------|-------------|
| J1 — Domain Sceptic | claude-opus-4.6 | NEEDS_REVISION | CWD `startswith` bypass in `validate_log_dir` (MUST-FIX) |
| J2 — Technical Expert | claude-sonnet-4.6 | NEEDS_REVISION | CWD `startswith` bypass (MUST-FIX); S09/S10 AttributeError on non-dict `rounds` (SHOULD-FIX) |
| J3 — Strategic/Product | gpt-5.4 | NEEDS_REVISION | CWD `startswith` bypass (MUST-FIX); S11 None clarity (non-blocking) |
| J4 — Defense Counsel | gpt-5.2 | NEEDS_REVISION | CWD `startswith` bypass; S09/S10 AttributeError on non-dict `rounds` |
| J5 — Devil's Advocate | gpt-5.4-mini | NEEDS_REVISION | CWD bypass; broken symlink ordering concern; S11 None detail |

### R1 Corrections Applied

| ID | Correction | Commit |
|----|-----------|--------|
| C-P6-VS04-R1-001 | `validate_log_dir`: replaced `startswith()` with `resolved.relative_to(cwd)` in try/except, raises `from None`; `test_sibling_prefix_dir_raises` added | `0c5a685` |
| C-P6-VS04-R1-002 | `check_s09`/`check_s10`: `isinstance(rounds, dict)` guard prevents AttributeError on non-dict `rounds`; `test_fail_rounds_not_a_dict` added for S09 and S10 | `0c5a685` |

### Round 2 — All 5 APPROVED

| Juror | Model | Verdict | Note |
|-------|-------|---------|------|
| J1 — Domain Sceptic | claude-opus-4.6 | APPROVED | Both corrections confirmed, attack vectors closed |
| J2 — Technical Expert | claude-sonnet-4.6 | APPROVED | Corrections semantically sound, `from None` correct, no regressions |
| J3 — Strategic/Product | gpt-5.4 | APPROVED | Both corrections correct, no new concerns |
| J4 — Defense Counsel | gpt-5.2 | APPROVED | Both fixes correct, 167 tests pass |
| J5 — Devil's Advocate | gpt-5.4-mini | APPROVED | Fixes sound, broken-symlink spec-compliant, no new attack surface |

### Judicial Synthesis

**Synthesizer:** claude-opus-4.5 | **Final Verdict: APPROVED**

All five jurors unanimously approved in R2. C-P6-VS04-R1-001 closes the CWD boundary bypass; C-P6-VS04-R1-002 ensures graceful FAIL on malformed `rounds`. Broken-symlink ordering and S11 None rendering ruled spec-compliant. No caveats.

---

## Final Verdict

**VERDICT: APPROVED** — 167 tests pass, 100% coverage, 0 mutation survivors, ruff clean. Commit `0c5a685`.

---
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 5
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 5
  strict: false
  timestamp: '2026-05-26T04:08:36Z'
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
- ENG-6.5
- ENG-4.6
- ENG-4.11
rounds:
  r1_completed: true
  r2_completed: true
schema_version: 1
slice: VS-03
status: APPROVED
title: File & Schema Checks S01–S08b
verdict: APPROVED
---


# VS-03 Evidence: File & Schema Checks S01–S08b

## Slice Objective

Implement `aa_jury_gate/checks/schema.py` — the nine check functions for file-level
validation (S01–S04) and frontmatter schema validation (S05–S08b). These provide
the core fast-fail and schema enforcement layer that `gate.py` (VS-07) will orchestrate.

---

## Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| `checks/__init__.py` | `tools/aa-jury-gate/aa_jury_gate/checks/__init__.py` | ✅ committed `7e23b84` |
| Implementation | `tools/aa-jury-gate/aa_jury_gate/checks/schema.py` | ✅ committed `2ed4164` (R1 corrections) |
| Tests | `tools/aa-jury-gate/tests/test_schema.py` | ✅ committed `2ed4164` (R1 corrections) |

---

## Public API

```python
# checks/schema.py — each function: no exceptions raised, no side effects

def check_s01(path: Path) -> CheckItem:        # file exists and is_file()
def check_s02(path: Path) -> CheckItem:        # extension in {.md, .yaml, .yml}
def check_s03(content: str) -> CheckItem:      # yaml.safe_load(content) succeeds
def check_s04(parsed: Any) -> CheckItem:       # isinstance(parsed, dict)
def check_s05(frontmatter: dict) -> CheckItem: # schema_version == 1
def check_s06(frontmatter: dict) -> CheckItem: # juror_count == 5
def check_s07(frontmatter: dict) -> CheckItem: # len(jurors) == 5 (hardcoded constant)
def check_s08a(frontmatter: dict) -> CheckItem: # all juror model strings distinct
def check_s08b(frontmatter: dict) -> CheckItem: # no claude-haiku-4.5
```

DETAIL messages exactly per Phase 3 §1.4:

| Check | FAIL DETAIL format |
|-------|-------------------|
| S01 (not found) | `synthesis file not found: <path>` |
| S01 (directory) | `synthesis path is a directory: <path>` |
| S02 | `unsupported extension '<ext>'; expected .md, .yaml, or .yml` |
| S03 | `<YAMLError message>` |
| S04 | `YAML root is a <type>; expected a mapping` |
| S05 (missing) | `field 'schema_version' is missing` |
| S05 (wrong) | `schema_version is <actual>; expected 1` |
| S06 (missing) | `field 'juror_count' is missing` |
| S06 (wrong) | `juror_count is <actual>; expected 5` |
| S07 | `jurors list has <actual> entries; expected 5` |
| S07 (non-list) | `jurors field must be a list; got <type>` |
| S08a | `duplicate model: <model_string>` |
| S08b | `prohibited model: claude-haiku-4.5` |

---

## Implementation Notes

- All functions: pure — no exceptions raised, no filesystem side effects beyond S01
- Fast-fail ordering (S01→S04 stop-on-fail) is enforced by gate.py (VS-07); check functions are stateless
- S07: uses hardcoded constant `5` — NOT `juror_count` value (Phase 3 §3 C-P3-J2-001)
- S08b: exact case-sensitive string match `"claude-haiku-4.5"` (no broader pattern)
- S08a/S08b: `isinstance(jurors, list)` guard — non-list jurors PASS (S07 owns structural validation); non-dict juror entries silently skipped (spec gap, not a code defect — Phase 3 defines no juror-entry-type check)
- S08a: `j.get("model", "")` — jurors missing model key yield `""` as their model string
- `yaml.safe_load` only (ENG-6.5 / AC-SEC-01); `yaml.load` is prohibited
- `# noqa: PLR2004` applied to hardcoded constant `5` in S07 (ruff magic-value rule)

---

## Test Evidence

### Test Targets (per Phase 5 §VS-03)

| Check | PASS test | FAIL test(s) | Missing-key test |
|-------|-----------|-------------|-----------------|
| S01 | existing file | nonexistent path, directory | — |
| S02 | .md, .yaml, .yml | .txt, .json, no extension | — |
| S03 | valid YAML, empty string | unclosed list, tab indent | — |
| S04 | dict | list, None, str, int | — |
| S05 | schema_version: 1 | schema_version: 2, string "1" | missing key |
| S06 | juror_count: 5 | juror_count: 4 | missing key |
| S07 | 5 jurors | 4 jurors, 6 jurors, juror_count=3, non-list (dict), string-len-5 | missing jurors key |
| S08a | all distinct | duplicate model, case-sensitivity | missing model key, non-list jurors (PASS) |
| S08b | no haiku | haiku present, "Claude-Haiku-4.5" | missing jurors key, non-list jurors (PASS) |

### Test Run

```
pytest tests/test_schema.py -v
======================== 58 passed in 0.12s ========================
```

All 58 tests pass. (54 original + 4 added for R1 corrections: S05 exact format, S07 non-list, S08a non-list, S08b non-list.)

### Coverage

```
aa_jury_gate/checks/__init__.py    0     0   100%
aa_jury_gate/checks/schema.py     69     0   100%
```

100% line coverage on schema.py (69 statements after R1 corrections).

### Mutation Testing

```
mutmut run --paths-to-mutate aa_jury_gate/checks/schema.py \
  --runner "python3.11 -m pytest tests/test_schema.py -x -q"

89/89 🎉 89  🙁 0
```

**89/89 = 100%** mutation score — all mutants eliminated.

No surviving mutants. Zero equivalences.

---

## Ruff

```
ruff check aa_jury_gate/checks/schema.py tests/test_schema.py → All checks passed!
```

---

## Law Compliance

| Law | Requirement | Evidence |
|-----|-------------|----------|
| ENG-2.1 | Modular decomposition | `checks/schema.py` self-contained; depends only on `models.py`; no circular imports |
| ENG-4.1 | TDD RED→GREEN→REFACTOR | Tests written first (RED: `ModuleNotFoundError`); implementation to GREEN |
| ENG-4.6 | Coverage ≥ 90% | 100% on schema.py (69 statements) |
| ENG-4.11 | Mutation ≥ 85% | 100% (89/89) |
| ENG-6.5 | yaml.safe_load only | `check_s03` sole YAML call is `yaml.safe_load(content)` |

---

## Jury Deliberation

### R1 (Initial Review)

| Juror | Model | Role | Verdict |
|-------|-------|------|---------|
| J1 | claude-opus-4.6 | Domain Sceptic | APPROVED |
| J2 | claude-sonnet-4.6 | Technical Expert | NEEDS_REVISION |
| J3 | gpt-5.4 | Strategic/Product Lens | NEEDS_REVISION |
| J4 | gpt-5.2 | Defense Counsel | APPROVED |
| J5 | gpt-5.4-mini | Devil's Advocate | NEEDS_REVISION |

**R1 Score: 2 APPROVED / 3 NEEDS_REVISION**

R1 corrections applied (commit `2ed4164`):

| ID | Finding | Source | Fix |
|----|---------|--------|-----|
| C-P6-VS03-R1-001 | S05 `{actual!r}` violates spec DETAIL format | J2 (MUST-FIX) | Removed `!r`; test updated to assert exact string |
| C-P6-VS03-R1-002 | S03 docstring ambiguous about `content` parameter | J2 | Clarified: content = extracted frontmatter YAML text between `---` delimiters |
| C-P6-VS03-R1-003 | S07/S08a/S08b missing `isinstance(jurors, list)` guard | J3, J5 | S07 → FAIL with type detail; S08a/S08b → PASS (defer to S07) |

Post-correction metrics: 58 tests, 100% coverage, 89/89 mutants caught.

### R2 (Post-Correction Review)

| Juror | Model | Role | Verdict |
|-------|-------|------|---------|
| J1 | claude-opus-4.6 | Domain Sceptic | APPROVED |
| J2 | claude-sonnet-4.6 | Technical Expert | APPROVED |
| J3 | gpt-5.4 | Strategic/Product Lens | NEEDS_REVISION |
| J4 | gpt-5.2 | Defense Counsel | APPROVED |
| J5 | gpt-5.4-mini | Devil's Advocate | NEEDS_REVISION |

**R2 Score: 3 APPROVED / 2 NEEDS_REVISION**

R2 findings assessed by judicial synthesis:

- **J3/J5: Non-dict juror entries bypass** — list of 5 non-dict entries passes S07/S08a/S08b. Judicial synthesis ruled: **SPEC GAP** (Phase 3 §1.4 defines no juror-entry-type check). Out of VS-03 scope. Deferred to future slice (CAVEAT-001).
- **J2: `True == 1` bool edge in S05/S06** — Ruled **non-blocking**. YAML parser behavior, not a code defect, not spec-covered.
- **J5: PASS vs SKIP semantics** — Ruled **correct**. `CheckResult` has only PASS/FAIL; PASS is the correct response when a check's invariant is vacuously satisfied.

### Judicial Synthesis

**Synthesizer:** claude-opus-4.5 (distinct from all 5 jurors)

**FINAL VERDICT: APPROVED**

All R1 corrections properly implemented. No regressions. Contested R2 issues ruled non-blocking or out of scope. Gate advances to VS-04.

**Caveats deferred:**
- CAVEAT-001: Define "S06b: all juror entries must be dicts" as new check in Phase 3.1 or future schema slice.
- CAVEAT-002: Consider integration test documenting `["a","b","c","d","e"]` as known spec gap behavior.

---

## Commits

| Commit | Description |
|--------|-------------|
| `7e23b84` | `feat(vs-03): checks/schema.py — S01 through S08b` (initial, 54 tests, 80/80 mutmut) |
| `2ed4164` | `feat(vs-03): apply R1 corrections C-P6-VS03-R1-001/002/003` (58 tests, 89/89 mutmut) |

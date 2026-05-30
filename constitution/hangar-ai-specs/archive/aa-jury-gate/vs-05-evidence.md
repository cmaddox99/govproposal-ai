---
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 4
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 4
  strict: false
  timestamp: '2026-05-26T04:47:27Z'
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
rounds:
  r1_completed: true
  r2_completed: true
schema_version: 1
slice: VS-05
status: APPROVED
title: Body Checks B01–B03
verdict: APPROVED
---


# VS-05 Evidence: Body Checks B01–B03

## Slice Objective

Implement `checks/body.py` with B01–B03 section-heading detection checks.
Body checks operate on the text after the closing `---` frontmatter delimiter.
SKIP logic is the orchestrator's responsibility (VS-07); these functions return PASS/FAIL only.

---

## Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| Body checks | `tools/aa-jury-gate/aa_jury_gate/checks/body.py` | ✅ committed `0d454bc` |
| Body tests | `tools/aa-jury-gate/tests/test_body.py` | ✅ committed `0d454bc` |

---

## Public API

```python
# checks/body.py
def check_b01(body: str) -> CheckItem  # R1 section heading present
def check_b02(body: str) -> CheckItem  # R2 section heading present
def check_b03(body: str) -> CheckItem  # Synthesis/Final/Judicial heading present
```

DETAIL messages per Phase 3 §1.4:

| Check | FAIL DETAIL format |
|-------|-------------------|
| B01 | `R1 section heading not found in body` |
| B02 | `R2 section heading not found in body` |
| B03 | `synthesis section heading not found in body` |

Patterns (multiline, case-insensitive — Phase 3 §3 Surface 4):

| Check | Pattern |
|-------|---------|
| B01 | `^##\s+(Round\s+1\|R1)(\s\|:\|-\|$)` |
| B02 | `^##\s+(Round\s+2\|R2)(\s\|:\|-\|$)` |
| B03 | `^##\s+(Synthesis\|Final\|Judicial)(\s\|:\|-\|$)` |

---

## Implementation Notes

- Patterns compiled at module level (not per-call) for efficiency (ENG-2.1)
- `re.MULTILINE | re.IGNORECASE` on all three patterns
- `## R10` does NOT match B01 — trailing `(\s|:|-|$)` prevents digit continuation
- `## R1.1` does NOT match B01 — `.` absent from trailing char class (RC-P3-J2-009a)
- SKIP logic (B01–B03 skipped when S11 fails) is in `gate.py` (VS-07), not here (C-P5-J1-005, C-P5-J5-001)

---

## Test Evidence

### Test Targets

| Component | PASS tests | FAIL tests |
|-----------|-----------|------------|
| B01 | Round 1, R1:, R1-, R1 EOL, case-insensitive, midway in body | no heading, ## R10, ## R1.1, ## Round 10, empty, inline prose |
| B02 | Round 2, R2:, R2-, R2 EOL, case-insensitive | no heading, ## R20, ## R2.1, empty, inline prose |
| B03 | Synthesis, Final, Judicial, :, -, EOL, case-insensitive×2, all-three-present | no heading, empty (BDD F04), inline prose, ## Judicial.1 |

### Test Run

```
pytest tests/test_body.py -q
======================== 40 passed in 0.07s ========================
```

All 40 tests pass (35 initial + 5 R1 observation additions).

### Coverage

```
aa_jury_gate/checks/body.py    39     0   100%
```

100% line coverage.

### Mutation Testing

```
mutmut run --paths-to-mutate aa_jury_gate/checks/body.py
21/21 🎉; 0 survivors in body.py
```

**21/21 = 100%** on body.py.

---

## Ruff

```
ruff check aa_jury_gate/checks/body.py tests/test_body.py → All checks passed!
```

---

## Law Compliance

| Law | Requirement | Evidence |
|-----|-------------|----------|
| ENG-2.1 | Modular decomposition | `body.py` self-contained; depends only on `models.py`; patterns compiled at module level |
| ENG-4.1 | TDD RED→GREEN→REFACTOR | Tests written first (RED: `ModuleNotFoundError`); implementation to GREEN |
| ENG-4.6 | Coverage ≥ 90% | 100% on body.py |
| ENG-4.11 | Mutation ≥ 85% | 100% body.py (21/21, 0 survivors) |

---

## Jury Gate Record

### Round 1 — All 5 APPROVED

| Juror | Model | Verdict | Note |
|-------|-------|---------|------|
| J1 — Domain Sceptic | claude-opus-4.6 | APPROVED | Patterns correct, tests comprehensive, no deviations |
| J2 — Technical Expert | claude-sonnet-4.6 | APPROVED | SHOULD-FIX: add `$`-branch tests + B02 Round-20 non-match |
| J3 — Strategic/Product | gpt-5.4 | APPROVED | Product alignment confirmed |
| J4 — Defense Counsel | gpt-5.2 | APPROVED | No issues |
| J5 — Devil's Advocate | gpt-5.4-mini | APPROVED | Patterns and tests sound |

### J2 Observations Addressed (commit `0d454bc`)

| ID | Test Added |
|----|-----------|
| C-P6-VS05-R1-J2-001 | `test_pass_r1_end_of_string_no_newline`, `test_pass_round_1_end_of_string_no_newline` (B01 `$` branch) |
| C-P6-VS05-R1-J2-002 | `test_fail_round_20_does_not_match`, `test_pass_r2_end_of_string_no_newline` (B02 symmetry + `$` branch) |
| C-P6-VS05-R1-J2-003 | `test_pass_synthesis_end_of_string_no_newline` (B03 `$` branch) |

### Round 2 — 4/5 APPROVED, 1 NEEDS_REVISION

| Juror | Model | Verdict | Note |
|-------|-------|---------|------|
| J1 — Domain Sceptic | claude-opus-4.6 | APPROVED | New tests correct and well-targeted |
| J2 — Technical Expert | claude-sonnet-4.6 | APPROVED | All R1 observations confirmed |
| J3 — Strategic/Product | gpt-5.4 | APPROVED | Slice ready to ship |
| J4 — Defense Counsel | gpt-5.2 | APPROVED | 40 tests pass |
| J5 — Devil's Advocate | gpt-5.4-mini | NEEDS_REVISION | Code-block false positives + indented headings missed |

### Judicial Synthesis

**Synthesizer:** claude-opus-4.5 | **Final Verdict: APPROVED**

J5's concerns (code-block false positives, indented ATX headings) ruled **SPEC-LEVEL DESIGN CHOICES** — Phase 3 §3 Surface 4 specifies pure regex on body text, no code-block exclusions, and explicitly `^##` with no leading spaces. CAVEAT-VS05-A/B document both for future spec revision if needed.

---

## Final Verdict

**VERDICT: APPROVED** — 40 tests pass, 100% coverage, 21/21 mutmut (0 survivors), ruff clean. Commits `db20848`, `0d454bc`.

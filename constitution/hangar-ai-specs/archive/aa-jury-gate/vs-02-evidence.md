---
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 3
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 3
  strict: false
  timestamp: '2026-05-26T03:35:29Z'
  tool: aa-citation-audit
  verdicts:
  - context_snippet: null
    id: ENG-2.1
    verdict: PASS
  - context_snippet: null
    id: ENG-4.1
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
- ADR-002
rounds:
  r1_completed: true
  r2_completed: true
schema_version: 1
slice: VS-02
status: APPROVED
title: Extractor — parse() and strip_jury_gate()
verdict: APPROVED
---


# VS-02 Evidence: Extractor

## Slice Objective

Implement `aa_jury_gate/extractor.py` — the module responsible for parsing YAML frontmatter
from synthesis files and stripping the `jury_gate:` block before computing content hashes.
This module underpins every downstream gate check (VS-03 through VS-05) and the SHA-256
content-hash idempotency guarantee required by ADR-002.

---

## Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| Implementation | `tools/aa-jury-gate/aa_jury_gate/extractor.py` | ✅ committed `ebffbcb` |
| Tests | `tools/aa-jury-gate/tests/test_extractor.py` | ✅ committed `ebffbcb` |

---

## Public API (Phase 4 §2.1 normative)

```python
class UnclosedFrontmatterError(Exception): ...

def parse(path: Path) -> tuple[dict, str]:
    """Returns (frontmatter_dict, body_str).

    Returns ({}, '') if no opening '---' found.
    Raises UnclosedFrontmatterError if opening '---' has no closing '---'.
    Raises yaml.YAMLError on invalid YAML in frontmatter.
    """

def strip_jury_gate(content: str) -> str:
    """Removes jury_gate: key from YAML frontmatter.

    Input: full file string (including '---' delimiters and body).
    Returns content unchanged if no jury_gate: key present.
    Idempotent: strip(strip(C)) == strip(C) (ADR-002).
    """
```

---

## Implementation Notes

- `UnclosedFrontmatterError` extends `Exception` directly (Phase 4 §2.1 — NOT ToolError)
- Uses `yaml.safe_load` only — never `yaml.load` (ENG-6.5 / AC-SEC-01)
- Frontmatter delimiter detection: scans line-by-line for `---`; uses the **first** closing
  `---` found (not the last) — crucial for multi-section synthesis documents
- `strip_jury_gate` uses **line-level filter** (not YAML round-trip) — preserves key order,
  quoting style, block scalars, and comments byte-for-byte (R1 C-001)
- BOM stripping: `_strip_bom()` helper applied in both `parse()` and `strip_jury_gate()` (R1 C-004)
- `isinstance(loaded, dict)` guard after `yaml.safe_load` in both functions (R1 C-002/C-003)
- Empty-line handling in block scalar skip: `if not line or line[0] in (" ", "\t")` covers blank
  lines within multi-line jury_gate values (R2 C-001)
- Sole-key empty-fm fix: `fm_block = "\n".join(out_lines) + "\n" if out_lines else ""`
  prevents `---\n\n---` when jury_gate is the only frontmatter key (R2 C-002)
- CRLF normalisation: `split("\n")` / `"\n".join()` normalises line endings as a side effect

---

## Test Evidence

### Test Targets (8 per phase-5-plan.md §VS-02)

| # | Target | Test(s) | Result |
|---|--------|---------|--------|
| TT-1 | `parse()` valid frontmatter → `(dict, body_str)` | `test_parse_valid_frontmatter`, `test_parse_returns_body_without_frontmatter_delimiters` | ✅ PASS |
| TT-2 | `parse()` no opening `---` → `({}, "")` | `test_parse_no_frontmatter_returns_empty_dict` | ✅ PASS |
| TT-3 | `parse()` unclosed `---` → `UnclosedFrontmatterError` | `test_parse_unclosed_frontmatter_raises`, `test_unclosed_frontmatter_error_is_exception` | ✅ PASS |
| TT-4 | `parse()` invalid YAML → `yaml.YAMLError` | `test_parse_invalid_yaml_raises` | ✅ PASS |
| TT-5 | `strip_jury_gate()` removes block; preserves other keys + body | `test_strip_jury_gate_removes_block`, `test_strip_jury_gate_preserves_other_keys`, `test_strip_jury_gate_preserves_body` | ✅ PASS |
| TT-6 | `strip_jury_gate()` without `jury_gate:` → unchanged | `test_strip_jury_gate_no_block_unchanged` | ✅ PASS |
| TT-7 | `strip_jury_gate()` idempotent | `test_strip_jury_gate_idempotent_with_block`, `test_strip_jury_gate_idempotent_without_block` | ✅ PASS |
| TT-8 | Cross-run sha256 idempotency (ADR-002) | `test_sha256_idempotent_across_jury_gate_block`, `test_content_sha256_formula` | ✅ PASS |

### Test Run

```
pytest tests/test_extractor.py -v
======================== 33 passed in 0.09s ========================
```

All 33 tests pass (23 initial + 7 R1 mutation-killing tests + 2 R2 regression tests + 1 R1-005 empty frontmatter contract).

### Coverage

```
aa_jury_gate/extractor.py      64      0   100%
```

100% line coverage achieved.

### Mutation Testing

```
mutmut run --paths-to-mutate aa_jury_gate/extractor.py \
  --runner "python3.11 -m pytest tests/test_extractor.py -x -q"

88/88 🎉 82  🙁 6
```

**82/88 = 93.2%** mutation score — exceeds the ≥85% threshold.

**Equivalent survivors (6):**

| Mutant | Location | Reason equivalent |
|--------|----------|-------------------|
| 56, 82 | `int \| None` type annotation | Type annotation mutations — no runtime effect |
| 81 | `or` → `and` in `not lines or lines[0]...` guard | For synthesis files starting with `---`, `not lines` is always False; both `False and X` and `False or X` yield X — same result in practice |
| 128, 129 | `skip = False` initialization | First `fm_lines` line is always a top-level YAML key (non-indented); `skip` reset on first iteration regardless of initialization |
| 152 | `line[0] in (" ", "\t")` tab detection | Tab-indented YAML is invalid per spec; PyYAML raises `YAMLError` before reaching the line filter; branch unreachable for valid YAML |

---

## Ruff

```
ruff check aa_jury_gate/extractor.py tests/test_extractor.py  → All checks passed!
ruff format aa_jury_gate/extractor.py tests/test_extractor.py → 2 files reformatted (clean)
```

---

## Law Compliance

| Law | Requirement | Evidence |
|-----|-------------|----------|
| ENG-2.1 | Modular decomposition | `extractor.py` is a self-contained module; no circular imports |
| ENG-4.1 | TDD RED→GREEN→REFACTOR | Tests written first (RED: `ModuleNotFoundError`), then implementation |
| ENG-6.5 | `yaml.safe_load` only | Sole YAML load call is `yaml.safe_load(fm_text)` (line 49, 85) |
| ADR-002 | Strip idempotency / sha256 stability | TT-7 and TT-8 verify both properties with dedicated mutation-killing tests |

---

## R1 Jury Summary (5/5 NEEDS_REVISION → 7 corrections applied)

| Juror | Model | Finding |
|-------|-------|---------|
| J1 | claude-opus-4.6 | sort_keys reorders keys; empty-dict-after-pop; parse() no-frontmatter ambiguity; silent YAMLError |
| J2 | claude-sonnet-4.6 | sort_keys + complex scalar corruption → recommended line-level filter; CRLF issue |
| J3 | gpt-5.4 | no-frontmatter ambiguity; hash not source-stable |
| J4 | gpt-5.2 | non-dict frontmatter not guarded; sort_keys; surviving mutants |
| J5 | gpt-5.4-mini | non-lossless round-trip; CRLF normalisation; UTF-8 BOM breaks detection |

**Corrections applied (R1):**

| ID | Correction |
|----|-----------|
| C-P6-VS02-R1-001 | Switch `strip_jury_gate` from yaml.dump round-trip to line-level filter |
| C-P6-VS02-R1-002 | `isinstance(fm, dict)` guard in `parse()` |
| C-P6-VS02-R1-003 | `isinstance(fm, dict)` guard in `strip_jury_gate()` |
| C-P6-VS02-R1-004 | `_strip_bom()` helper — strip UTF-8 BOM in both functions |
| C-P6-VS02-R1-005 | Test for empty frontmatter `---\n---\nbody` contract |
| C-P6-VS02-R1-006 | Module docstring with pipeline ordering, CRLF, design notes |
| C-P6-VS02-R1-007 | Mutation-killing tests (key order, block scalar, BOM, non-dict, single-space indent) |

R1 corrections committed at `eec7079`.

---

## R2 Jury Summary (2/5 APPROVED, 3/5 NEEDS_REVISION → 2 corrections applied)

| Juror | Model | Finding |
|-------|-------|---------|
| J1 | claude-opus-4.6 | NEEDS_REVISION — R2-001 MAJOR: empty lines in block scalars leak; R2-002 MINOR: spurious blank line |
| J2 | claude-sonnet-4.6 | APPROVED — all 7 R1 corrections confirmed; blank-line issue LOW non-blocking |
| J3 | gpt-5.4 | APPROVED — foundation adequate for VS-03/04/05 |
| J4 | gpt-5.2 | NEEDS_REVISION — mutant equivalence debate (stale cache for 8 vs 6); coverage claim |
| J5 | gpt-5.4-mini | NEEDS_REVISION — blank-line issue confirmed |

**Corrections applied (R2):**

| ID | Correction |
|----|-----------|
| C-P6-VS02-R2-001 | Fix empty-line leak: `if skip: if not line or line[0] in (" ", "\t"): continue; skip=False` |
| C-P6-VS02-R2-002 | Sole-key empty-fm: `fm_block = "\n".join(out_lines) + "\n" if out_lines else ""` |

Also: Anchor `match=r"^frontmatter must"` to eliminate mutant 115. J4's stale-cache mutant count resolved (88 mutants, not 85). Coverage confirmed 100% on extractor.py.

R2 corrections committed at `ebffbcb`.

---

## Judicial Synthesis

**Synthesizer:** claude-opus-4.5 (distinct from all 5 jurors) — **VERDICT: APPROVED**

All 9 corrections (7 R1 + 2 R2) confirmed. 6 surviving mutants documented as equivalent. No outstanding concerns.

---

## Commit

- R1 code + tests: `eec7079`
- R2 corrections: `ebffbcb`
- Evidence + synthesis: (this commit)

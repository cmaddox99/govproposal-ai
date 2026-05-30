---
schema_version: 1
slice: VS-02
synthesizer: claude-opus-4.5
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
rounds:
  r1_completed: true
  r2_completed: true
verdict: APPROVED
---

# VS-02 Judicial Synthesis: Extractor

## Round 1 Jury Findings

Five jurors unanimously returned **NEEDS_REVISION** for the initial VS-02 implementation.
Seven corrections were required and applied at commit `eec7079`.

### J1 (claude-opus-4.6 — Domain Sceptic)
- `yaml.dump(sort_keys=True)` reorders keys — breaks idempotency requirement
- Empty dict after pop leaves malformed output
- `parse()` no-frontmatter ambiguity (returns `({}, "")`)
- Silent `YAMLError` swallowed in strip path

### J2 (claude-sonnet-4.6 — Technical Expert)
- `sort_keys` + complex scalar corruption → **recommended line-level filter** (adopted)
- CRLF normalisation gap identified

### J3 (gpt-5.4 — Strategic/Product Lens)
- `parse()` no-frontmatter ambiguity; hash not source-stable across YAML round-trips

### J4 (gpt-5.2 — Defense Counsel)
- Non-dict frontmatter not guarded in either function
- `sort_keys` issue confirmed; mutation survivors noted

### J5 (gpt-5.4-mini — Devil's Advocate)
- Non-lossless round-trip confirmed
- CRLF normalisation gap
- UTF-8 BOM breaks frontmatter detection

### R1 Corrections Applied

| ID | Correction | Commit |
|----|-----------|--------|
| C-P6-VS02-R1-001 | Switch `strip_jury_gate` to line-level filter (no yaml.dump) | `eec7079` |
| C-P6-VS02-R1-002 | `isinstance(dict)` guard in `parse()` | `eec7079` |
| C-P6-VS02-R1-003 | `isinstance(dict)` guard in `strip_jury_gate()` | `eec7079` |
| C-P6-VS02-R1-004 | `_strip_bom()` helper; applied in both functions | `eec7079` |
| C-P6-VS02-R1-005 | Test for empty frontmatter `---\n---\nbody` contract | `eec7079` |
| C-P6-VS02-R1-006 | Module docstring with pipeline ordering, CRLF, design notes | `eec7079` |
| C-P6-VS02-R1-007 | Mutation-killing tests (key order, block scalar, BOM, non-dict) | `eec7079` |

---

## Round 2 Jury Findings

Two jurors returned **APPROVED** (J2, J3). Three returned **NEEDS_REVISION** (J1, J4, J5).
Two additional corrections were required and applied at commit `ebffbcb`.

### J1 (claude-opus-4.6 — Domain Sceptic)
- **R2-001 MAJOR:** Blank lines within `jury_gate:` block scalars leaked through the skip filter
  — `if skip and line and line[0] in (...)` reset `skip=False` on empty lines
- **R2-002 MINOR:** Spurious `\n` when `jury_gate:` is the only frontmatter key; produced
  `---\n\n---` instead of `---\n---`

### J2 (claude-sonnet-4.6 — Technical Expert)
All 7 R1 corrections confirmed. Blank-line issue noted as LOW non-blocking.
**Verdict: APPROVED**

### J3 (gpt-5.4 — Strategic/Product Lens)
Implementation adequate for downstream VS-03/04/05 integration. No new issues.
**Verdict: APPROVED**

### J4 (gpt-5.2 — Defense Counsel)
Mutant equivalence debate (stale cache reported 8 survivors, actual 6). Coverage claim
on overall package (not extractor.py scope). Both resolved by anchor fix and scope clarification.

### J5 (gpt-5.4-mini — Devil's Advocate)
Blank-line issue confirmed as genuine edge case. Agreed fix approach is correct.

### R2 Corrections Applied

| ID | Correction | Commit |
|----|-----------|--------|
| C-P6-VS02-R2-001 | Fix skip: `if skip: if not line or line[0] in (" ", "\t"): continue; skip=False` | `ebffbcb` |
| C-P6-VS02-R2-002 | Sole-key fix: `fm_block = "\n".join(out_lines) + "\n" if out_lines else ""` | `ebffbcb` |

Also: Anchored `match=r"^frontmatter must"` to eliminate mutant 115.

---

## Judicial Synthesis

**Synthesizer:** claude-opus-4.5 (model distinct from all 5 jurors per greenfield-development.md)

All 9 corrections (7 from R1, 2 from R2) are **CONFIRMED** in the final implementation at
commit `ebffbcb`.

### Quality Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Tests | 33 | — | ✅ |
| Coverage (extractor.py) | 100% | ≥90% | ✅ |
| Mutation score | 82/88 = 93.2% | ≥85% | ✅ |
| Ruff | All checks passed | 0 errors | ✅ |

### Surviving Mutants Rationale

| Mutant | Reason equivalent |
|--------|-------------------|
| 56, 82 | Type annotation union operators — no runtime effect |
| 81 | `or→and` guard — equivalent for synthesis files starting with `---` per Phase 4 §2.1 contract |
| 128, 129 | `skip = False` init — first `fm_lines` line is always a top-level YAML key; reset on first iteration |
| 152 | Tab-indent branch — PyYAML rejects tab-indented YAML per spec; branch unreachable |

### Verdict

**VERDICT: APPROVED**

VS-02 is production-ready. The line-level filter design correctly preserves YAML formatting
while safely removing `jury_gate:` blocks. The R2 blank-line bug (C-P6-VS02-R2-001) was a
genuine edge case caught and resolved by the jury process.

All Phase 4 §2.1 normative API contracts are implemented and verified. VS-03 (Validator) may proceed.

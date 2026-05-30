---
schema_version: 1
project: aa-jury-gate
phase: 4
artifact: phase-4-design.md
synthesizer: claude-opus-4.5
juror_count: 5
distinct_models_required: true
jurors:
  - id: J1
    model: claude-opus-4.6
    role: Domain Sceptic
    r1_verdict: NEEDS_REVISION
    r2_verdict: APPROVED
  - id: J2
    model: claude-sonnet-4.6
    role: Technical Expert
    r1_verdict: NEEDS_REVISION
    r2_verdict: NEEDS_REVISION
  - id: J3
    model: gpt-5.4
    role: Strategic/Product Lens
    r1_verdict: NEEDS_REVISION
    r2_verdict: NEEDS_REVISION
  - id: J4
    model: gpt-5.2
    role: Defense Counsel
    r1_verdict: NEEDS_REVISION
    r2_verdict: NEEDS_REVISION
  - id: J5
    model: gpt-5.4-mini
    role: Devil's Advocate
    r1_verdict: NEEDS_REVISION
    r2_verdict: NEEDS_REVISION
rounds:
  r1_completed: true
  r2_completed: true
verdict: APPROVED
date: 2026-05-26
---

## Phase 4 — Design: Judicial Synthesis

**Synthesizer:** claude-opus-4.5
**Artifact:** `phase-4-design.md` (aa-jury-gate CLI)
**Date:** 2026-05-26

---

## Round 1 (R1) — Summary

All 5 jurors returned NEEDS_REVISION in R1. Key findings addressed across 10 correction IDs:

| Correction ID | Summary | Juror(s) |
|--------------|---------|---------|
| C-P4-J1-001 | content_sha256 strip ambiguity → ADR-002 canonical formula | J1, J2, J5 |
| C-P4-J2-003 | §0 env constraints table added (Python ≥3.10, click ≥8.1, PyYAML ≥6.0) | J2 |
| C-P4-J1-002 | PermissionError mapped → ToolError → exit 2 | J1 |
| C-P4-J2-002 | GateVerdict.exit_code @property added (PASS→0, FAIL→1, ERROR→2) | J2, J4 |
| C-P4-J3-001 | Module count corrected to 11; import DAG added | J3, J5 |
| C-P4-J4-001 | §2.1 extractor.py public API specified (parse() + strip_jury_gate()) | J4 |
| C-P4-J4-002 | §2.2 security.py public API specified (validate_synthesis_path() + validate_log_dir()) | J4 |
| C-P4-J5-007 | GitBinaryNotFoundError(ToolError) split from GitProbeError | J5 |
| C-P4-J2-005 | AuditEntry serialization via dataclasses.asdict(); checks: list[dict] | J2 |
| C-P4-J3-003 | §7.1 smoke test spec added; tests/test_smoke.py CI-blocking | J3 |

Citation audit post-R1: 16/16 PASS.

---

## Round 2 (R2) — Summary

| Juror | R2 Verdict | Key Items |
|-------|-----------|-----------|
| J1 (claude-opus-4.6) | APPROVED | All 10 R1 corrections confirmed; no residual gaps |
| J2 (claude-sonnet-4.6) | NEEDS_REVISION | `dataclasses.asdict()` does NOT auto-convert Enum → .value (TypeError at runtime); strip_jury_gate input boundary ambiguous |
| J3 (gpt-5.4) | NEEDS_REVISION | "AA internal PyPI" aspirational; v1 path is `pip install -e .`; Python ≥3.10 AA CI compatibility note needed |
| J4 (gpt-5.2) | NEEDS_REVISION | Searched wrong repo (workshops vs constitution); no substantive new findings |
| J5 (gpt-5.4-mini) | NEEDS_REVISION | CRITICAL: enum serialization crash confirmed; HIGH: strip_jury_gate input boundary; MEDIUM: CI single-writer guidance |

**Procedural note — J2/J4 repo search failure:** Both agents searched `AAInternal/hangar-ai-constitution-workshops` instead of the constitution repo. Their "UNVERIFIABLE" claims are procedural failures, not substantive design gaps. J2's `dataclasses.asdict()` finding (NF-003) is independently confirmed by J5 and stands on its own technical merit.

---

## Judicial Synthesis — Adjudication Rulings

### Issue 1: dataclasses.asdict() enum serialization (J2-NF-003, J5-004) — CRITICAL

**RULING: REQUIRED CHANGE — Option A (inline `default=` lambda) adopted**

J2 and J5 are correct. `dataclasses.asdict()` preserves `Enum` objects — it does NOT call `.value`. The original §6.1 claim "CheckResult enum serializes to its .value string via asdict()" is factually wrong and would cause `TypeError: Object of type CheckResult is not JSON serializable` in production.

**Fix:** `json.dumps(dataclasses.asdict(entry), default=lambda o: o.value if isinstance(o, Enum) else str(o))`. The inline lambda requires no new abstractions and is transparent to readers.

### Issue 2: strip_jury_gate() input boundary (J5-001, J2-NF-003) — HIGH

**RULING: REQUIRED CHANGE — clarifying sentence added**

The docstring said "YAML frontmatter text" but the canonical formula (ADR-002) passes `raw_bytes.decode('utf-8')` — the full file string including `---` delimiters and body. One clarifying sentence resolves the ambiguity without changing behavior.

### Issue 3: AA internal PyPI aspirational (J3-006) — MEDIUM

**RULING: REQUIRED CHANGE — v1 path corrected**

J3 is correct. There is no guarantee an AA internal PyPI registry exists at v1 workshop time. The honest v1 install path is `pip install -e .` from the constitution repo clone. Internal PyPI is aspirational for v1.1+.

### Issue 4: Python ≥3.10 AA CI compatibility (J3) — MEDIUM

**RULING: INCORPORATED — advisory note added to §0**

J3's concern is valid. §0 now includes a note that AA CI must provide Python 3.10+, and documents the backport path (PEP 563 + typing module) if CI is pinned to 3.9. This does not change the `python_requires` floor — 3.10 is correct for idiomatic code.

### Issue 5: CI single-writer guidance (J5-006) — MEDIUM

**RULING: DISMISSED — already documented**

§6.4 already states: "Do not run concurrent gate invocations on the same synthesis file." This is sufficient. No additional change needed.

---

## Required Changes Applied

1. **§6.1** — Replaced incorrect `dataclasses.asdict(c)` comment; added `default=lambda o: o.value if isinstance(o, Enum) else str(o)` pattern; documented that `dataclasses.asdict()` does NOT auto-convert Enum → .value (C-P4-J2-NF-003-R2, C-P4-J5-004-R2)
2. **§2.1** — Added explicit input boundary docstring to `strip_jury_gate()`: full file content including `---` delimiters and body (C-P4-J5-001-R2, C-P4-J2-NF-003-R2)
3. **§9.4** — v1 distribution is `pip install -e .` from constitution repo clone; AA internal PyPI aspirational (v1.1+) (C-P4-J3-006-R2)
4. **§9.3** — CI install row updated: `pip install -e .` or `pip install aa-jury-gate` (if AA internal PyPI available) (C-P4-J3-006-R2)
5. **§0** — Python ≥3.10 row now includes AA CI requirement note and 3.9 backport path (C-P4-J3-R2)

## Deferred to v2

- T9 mechanical hash verification deferred to v2; spec note: "single gate invocation per synthesis file per run" in CI
- AA internal PyPI registry (v1.1+)
- Python 3.9 backport variant (if AA CI requires)

## Dismissed

- Issue 5 (CI single-writer guidance): DISMISSED — §6.4 already documents this

---

## Synthesizer Re-Verification

All 5 required changes confirmed present in `phase-4-design.md`:

| Change | Location | Confirmed |
|--------|----------|-----------|
| §0 Python ≥3.10 AA CI note + backport path | §0 table row | ✅ |
| strip_jury_gate() input boundary docstring | §2.1 | ✅ |
| dataclasses.asdict() enum default= lambda | §6.1 comment + serialization contract | ✅ |
| CI install command updated | §9.3 table | ✅ |
| v1 distribution = pip install -e . | §9.4 | ✅ |

Citation audit: 16/16 PASS. HTML rendered.

**VERDICT: APPROVED**

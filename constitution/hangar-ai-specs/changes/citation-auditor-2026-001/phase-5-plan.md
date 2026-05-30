---
phase: 5
title: "Plan — Law Citation Auditor"
project: citation-auditor-2026-001
workflow: greenfield-development
version: v1.2.0
status: APPROVED
approved_by: claude-opus-4.5
approved_at: 2026-05-23
amendment_v1.2.0: "Article XII amendment — SonarQube gates replaced with pytest-cov ≥90% (ENG-4.6) + ruff bugs=0 + mutmut ≥85% critical modules (ENG-4.11) + multi-cognition jury deliberation (ENG-12.1). SonarQube removed from constitution by user decision."
author: Hangar AI (claude-sonnet-4.6)
date: 2026-05-23
law_citations: [PRD-2.6, ENG-1.5, ENG-2.2, ENG-2.3, ENG-3.4, ENG-3.7, ENG-4.1, ENG-4.6, ENG-4.11, ENG-6.1, ENG-6.4, ENG-6.5, ENG-6.7, ENG-10.1, ENG-10.2, ENG-11.1, ENG-11.2, ENG-12.1, ENG-13.1, BUS-7.1]
preceding_phase_approved: phase-4-design.md v1.1.0 (APPROVED claude-opus-4.5 2026-05-23)
j6_activation: "20 distinct law IDs ≥5 threshold per ENG-14.2 condition 3 — ENG-14.2 is PROPOSED; J6 advisory-only until Phase 8 merge"
r2_corrections:
  - C-P5-R2-001: S-01 test_registry.py stripped of cli.py references (cli is S-04) — only unit-tests RegistryLoadError raised on bad input; all cli.py exit(2) + audit.log tests moved to S-04
  - C-P5-R2-002: S-04 test_cli.py adds audit.log JSON structure test (fields: artifact, fail_count, warn_count, pass_count, tool_version, timestamp, sha256_artifact per Phase 4 §5); plus exit(2) taxonomy tests moved from S-01
  - C-P5-R2-003: S-04 --output console corrected to stdout (ANSI colour-formatted) — Phase 3 §4.5 Sc-8 ground truth; plan previously said stderr (incorrect)
  - C-P5-R2-004: S-05 test_bdd_status_mismatch.py scope expanded to Scenarios 5–7 (STRICTLY ENFORCED on NON-NEG law → WARN, Phase 3 §4.2 Sc-7 added)
  - C-P5-R2-005: S-02 and S-03 add "All paths relative to tools/citation-auditor/" note for consistency with S-01 tree
  - C-P5-R2-006: §4 success metrics table corrected — source is Phase 4 §0 Success Criteria (not "design spec §8"); metrics updated to match Phase 4 §0 exactly
  - C-P5-R2-007: J4 C-P5-002 staged rollout challenge rejected — plan matches Phase 3 §5 exactly; no --exit-zero flag exists; staged rollout is a CI script change
  - C-P5-R1-001: models.py moved to S-01 (Verdict enum + CitationResult + AuditResult); enables true S-02/S-03 parallel build
  - C-P5-R1-002: S-01 SP increased 3→5; exceptions.py adds both RegistryLoadError AND AuditError with exit(2) mapping test
  - C-P5-R1-003: S-01 pyproject.toml fixed — rapidfuzz==3.* (was >=3.0, defeats T-08); [build-system] table added
  - C-P5-R1-004: S-01 SP increased 3→5; exceptions.py adds both RegistryLoadError AND AuditError — unit tests confirm exception types (cli.py exit(2) wiring tested in S-04, not S-01)
  - C-P5-R1-005: S-03 dataclass contracts corrected to Phase 3 §2.2 exactly — Verdict enum (3 members only), note not reason, @property computed fields, removed skip_count/pass_rate/SKIP, added registry_path/law_count/scanned/allow_draft/strict
  - C-P5-R1-006: S-05 SP increased 8→13; BDD test_bdd_code_block.py added for Phase 3 §4.3 (T-07 highest-impact); section refs corrected; Scenarios 5-9 added to test_bdd_core.py scope; no-frontmatter fixture added; CI staged rollout completed (Week 1 warn-only + Week 2+ enforce + --allow-draft)
  - C-P5-R1-007: S-06 workflow table corrected — 7 actual files (3 legacy-rescue tracks, avatar-workflow, adoption, greenfield, product-discovery); phantom files removed; SonarQube gate note corrected
  - C-P5-R1-008: §2 dependency graph adds Phase 7 Review downstream acknowledgment
  - C-P5-R1-009: §3 test pyramid adds ENG-4.1 atomic TDD execution constraint; mutation gate ownership clarified (Phase 6 runs, Phase 7 verifies)
  - C-P5-R1-010: §4 adds design spec §8 success metrics as acceptance criteria
  - C-P5-R1-011: §5 Phase 8 Deliverables adds _domain.yaml entry + validation re-run
  - C-P5-R1-012: S-03 dep table corrected (S-01 only — no import dep on S-02)
---

# Phase 5 — Plan: Law Citation Auditor

**Jury focus (greenfield-development.md §Per-Phase Jury Focus):**
"Slice independence; dependency accuracy; test pyramid balance; estimate realism"

**Constitutional gate:** Implementation proposal approved in `hangar-ai-specs/changes/` before Phase 6 Build begins.

---

## 0. Problem / Solution Recap (ENG-11.2)

`aa-citation-audit` is a Python 3.11+ CLI tool (project `citation-auditor-2026-001`) that audits constitutional law citations in Hangar AI Constitution workflow artifacts before jury invocation. Approved design (Phase 4) defines: 4-layer DI architecture (registry/scanner/auditor/cli), 5 ADRs, 9-threat security model, Article XIV proposed law text (ENG-14.1 + ENG-14.2), and BUS-7.1 CI-delegation audit trail.

Phase 5 decomposes the approved design into 6 independent vertical slices for Phase 6 atomic TDD delivery (ENG-4.1 NON-NEGOTIABLE), with a dependency graph (ENG-2.3), test pyramid strategy, and complexity estimates.

---

## 1. Vertical Slice Definitions

### S-01: Project Scaffold + Registry Layer + Data Models

| Field | Value |
|-------|-------|
| Slice ID | S-01 |
| Complexity | 5 story points |
| Depends on | None (first slice) |
| Layer | Infrastructure (registry.py) + Shared models (models.py, exceptions.py) |

**Files created:**
```
tools/citation-auditor/
├── pyproject.toml
├── src/
│   └── citation_auditor/
│       ├── __init__.py
│       ├── models.py            # Verdict enum, CitationResult, AuditResult (shared by S-02/S-03/S-04)
│       ├── registry.py          # load_registry() + RegistryEntry
│       └── exceptions.py        # RegistryLoadError, AuditError
└── tests/
    ├── conftest.py
    ├── fixtures/
    │   └── registry/            # mini index.yaml + sample law files
    └── unit/
        └── test_registry.py
```

**`models.py` contracts (Phase 3 §2.2 — authoritative):**
```python
class Verdict(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    # Draft IDs are NOT added to results as CitationResult entries.
    # They are tracked in AuditResult.draft_skipped (list[str]).

@dataclass
class CitationResult:
    law_id: str
    verdict: Verdict
    note: str | None             # human-readable reason for WARN/FAIL
    context_snippet: str | None  # ±150 chars from match_start in stripped body; None for PASS

@dataclass
class AuditResult:
    artifact_path: str
    registry_path: str
    law_count: int               # total laws in registry
    scanned: int                 # unique IDs found in stripped body
    results: list[CitationResult]  # sorted: FAIL→WARN→PASS, then alpha within tier
    draft_skipped: list[str]     # IDs skipped due to --allow-draft
    allow_draft: list[str]
    strict: bool
    timestamp: str               # YYYY-MM-DDTHH:MM:SSZ
    tool_version: str

    @property
    def fail_count(self) -> int: ...

    @property
    def warn_count(self) -> int: ...

    @property
    def pass_count(self) -> int: ...

    @property
    def audit_exit_code(self) -> int:
        # Returns 0 or 1 only. Exit 2 is cli.py's responsibility.
        # strict=True: exit 1 if any WARN
        ...
```

**`exceptions.py` contracts:**
- `RegistryLoadError` — raised by `registry.py` on any registry load failure → cli.py catches → `exit(2)`
- `AuditError` — raised by `auditor.py` on internal verdict logic failure → cli.py catches → `exit(2)`

**`registry.py` contracts:**
- `RegistryEntry(id: str, domain: str, non_negotiable: bool, title: str | None, summary: str | None)`
- `load_registry(laws_dir: Path) -> dict[str, RegistryEntry]`
  - Reads `index.yaml` for `law_ids` (existence) and `non_negotiable` lists
  - Scans ALL `domains.{domain}.files` law markdown files; matches `id` in each file's `laws:` frontmatter list for `title`/`summary` (no direct ID→filename mapping — must scan all)
  - Raises `RegistryLoadError` on any failure

**pyproject.toml (Phase 3 §5 + Phase 4 ADR-005 + T-08 supply-chain mitigation):**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "aa-citation-audit"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["click>=8.1", "PyYAML==6.0.*", "rapidfuzz==3.*"]

[project.scripts]
aa-citation-audit = "citation_auditor.cli:main"

[tool.pytest.ini_options]
addopts = "--cov=citation_auditor --cov-report=term-missing --cov-fail-under=90"

[tool.hatch.build.targets.wheel]
packages = ["src/citation_auditor"]
```

**Additional test coverage (test_registry.py):**
- `RegistryLoadError` raised on missing index.yaml — unit test confirms exception type and message (exception taxonomy only; cli.py exit(2) wiring tested in S-04)
- `RegistryLoadError` raised on malformed YAML — unit test confirms exception type
- `load_registry()` returns correct `RegistryEntry` dict for mini fixture registry

**Quality gate:** `pytest-cov ≥ 90%` (ENG-4.6), `ruff bugs=0`, `mutmut ≥ 85%` on `registry.py` (ENG-4.11)

---

### S-02: Scanner Layer

| Field | Value |
|-------|-------|
| Slice ID | S-02 |
| Complexity | 3 story points |
| Depends on | S-01 (RegistryEntry for draft filtering; models.py for shared types) |
| Layer | Application (scanner.py) |

**Files created/modified (all paths relative to `tools/citation-auditor/`):**
```
src/citation_auditor/
tests/
├── fixtures/
│   └── scanner/
│       ├── artifact_clean.md
│       ├── artifact_code_block_ids.md      # T-07: IDs inside fenced blocks
│       ├── artifact_indented_fence.md      # T-07: indented fence edge case
│       ├── artifact_inline_code_ids.md     # T-07: IDs inside inline code
│       ├── artifact_oversized.bin          # T-09: 10MB+ file
│       ├── artifact_encoding_latin1.md     # T-09: non-UTF-8 encoding
│       └── artifact_many_citations.md      # T-09: >1000 citation matches
└── unit/
    └── test_scanner.py
```

**Contracts delivered:**
- `scan_artifact(artifact_path: Path, registry: dict[str, RegistryEntry], allow_draft: list[str]) -> tuple[list[tuple[str, str]], list[str]]`
  - Pass 1: strip fenced blocks with `re.DOTALL` (ADR-003)
  - Pass 2: strip inline code
  - Regex: `\b(ENG|PRD|BUS)-\d+\.\d+\b`
  - Deduplicate: first-occurrence wins; context_snippet ±150 chars (Phase 3 §2.2)
  - Draft filtering: allow_draft IDs → `draft_skipped`
  - T-09 guards: reject >10 MB (pre-read), decode UTF-8 `errors='replace'`, cap matches at 1,000

**Quality gate:** `pytest-cov ≥ 90%` (ENG-4.6), `ruff bugs=0`, `mutmut ≥ 85%` on `scanner.py` (ENG-4.11)

---

### S-03: Auditor + Verdict Logic

| Field | Value |
|-------|-------|
| Slice ID | S-03 |
| Complexity | 5 story points |
| Depends on | S-01 (RegistryEntry + Verdict + CitationResult + AuditResult from models.py) |
| Layer | Domain (auditor.py) — pure function; no I/O |

> **Note:** S-02 and S-03 can build in parallel after S-01. `auditor.py` takes
> `citations: list[tuple[str, str]]` (plain Python type) — no import dependency on
> `scanner.py`. All shared types (`Verdict`, `CitationResult`, `AuditResult`) are
> in `models.py` (S-01).

**Files created/modified (all paths relative to `tools/citation-auditor/`):**
```
src/citation_auditor/
└── auditor.py               # audit()
tests/
├── fixtures/
│   └── auditor/
│       ├── registry_with_titles.yaml   # known titles for WARN/TITLE_MISMATCH testing
│       └── artifact_status_mismatch.md # STATUS_MISMATCH scenario (Phase 3 §4.2 Sc-5/6/7)
└── unit/
    └── test_auditor.py
```

**`auditor.py` contract:**
```python
def audit(citations: list[tuple[str, str]], registry: dict[str, RegistryEntry],
          strict: bool) -> AuditResult:
    """Apply L1 verdict logic. Pure function — no I/O.

    Verdict rules (per Phase 3 §2.2):
      FAIL  — law_id not in registry
      WARN  (TITLE_MISMATCH) — explicit title phrase ±30 chars of ID, partial_ratio < 60
      WARN  (STATUS_MISMATCH) — explicit NON-NEGOTIABLE/STRICTLY ENFORCED claim contradicts registry
      PASS  — in registry, no mismatch

    Results sorted: FAIL → WARN → PASS, then alphabetical within tier.
    Raises AuditError on internal failure (caught by cli.py → exit 2).
    """
```

**Quality gate:** `pytest-cov ≥ 90%` (ENG-4.6), `ruff bugs=0`, `mutmut ≥ 85%` on `auditor.py` (ENG-4.11 — highest-value mutation target)

---

### S-04: CLI + DI Orchestration

| Field | Value |
|-------|-------|
| Slice ID | S-04 |
| Complexity | 5 story points |
| Depends on | S-01, S-02, S-03 |
| Layer | Presentation (cli.py) |

**Files created/modified:**
```
src/citation_auditor/
└── cli.py                   # @click.command main()
tests/
└── unit/
    └── test_cli.py
```

**Contracts delivered (Phase 3 §1, Phase 4 §4.4):**
- Click interface with `--laws-dir`, `--allow-draft`, `--strict`, `--output [stdout|append|console]`
- ENG-6.5 validation surfaces in order:
  1. Surface 1: artifact exists, regular file, `.md` ext, canonical path within root (T-01), size ≤10 MB
  2. Surface 2: `laws_dir` exists and contains `index.yaml`
  3. Surface 3: each `--allow-draft` value matches `[A-Z]+-\d+\.\d+`
  4. Surface 4 (write-time): write permission check for `--output append`
- DI orchestration: `load_registry()` → `scan_artifact(registry=...)` → `audit(citations=..., registry=...)`
- `--output append`: atomic write via `tempfile.NamedTemporaryFile(dir=artifact_path.parent)` + `os.replace()` (T-06)
- `--output console`: ANSI colour-formatted table to `stdout` (Phase 3 §4.5 Sc-8 ground truth: "stdout contains colour-formatted output")
- BUS-7.1: appends JSON line to `~/.aa-citation-audit/audit.log` (includes `sha256_artifact`)
- Exit: `sys.exit(result.audit_exit_code)` for 0/1; `sys.exit(2)` on validation/tool error

**Additional test coverage (test_cli.py):**
- `RegistryLoadError` raised by registry.py → cli.py catches → `sys.exit(2)` verified end-to-end
- `AuditError` raised by auditor.py → cli.py catches → `sys.exit(2)` verified end-to-end
- `~/.aa-citation-audit/` directory created on first invocation; subsequent runs append (BUS-7.1)
- `audit.log` JSON line structure verified: fields `artifact`, `fail_count`, `warn_count`, `pass_count`, `tool_version`, `timestamp`, `sha256_artifact` all present (Phase 4 §5 `citation_audit.scan` schema)
- `citation_audit.tool_error` event emitted on exit 2 (Phase 4 §5)

**Quality gate:** `pytest-cov ≥ 90%` (ENG-4.6), `ruff bugs=0`

---

### S-05: BDD + Integration + CI

| Field | Value |
|-------|-------|
| Slice ID | S-05 |
| Complexity | 13 story points |
| Depends on | S-01, S-02, S-03, S-04 (full stack) |
| Layer | Cross-cutting (tests + CI) |

**Files created/modified:**
```
tests/
├── bdd/
│   ├── test_bdd_core.py          # Phase 3 §4.1 Scenarios 1–9:
│   │                             #   Sc-1: FAIL/exit-1; Sc-2: PASS/exit-0; Sc-3: WARN/exit-0;
│   │                             #   Sc-4: draft-skip/exit-0; Sc-5: --strict WARN/exit-1;
│   │                             #   Sc-6: draft-present-not-in-body; Sc-7: ENG-12.1 PASS after fix;
│   │                             #   Sc-8: same-ID dedup (first-occurrence); Sc-9: zero-citations/exit-0
│   ├── test_bdd_status_mismatch.py  # Phase 3 §4.2 Scenarios 5–7 (STATUS_MISMATCH):
│   │                                #   Sc-5: NON-NEG assertion on non-NON-NEG law → WARN
│   │                                #   Sc-6: status assertion matches registry → PASS
│   │                                #   Sc-7: STRICTLY ENFORCED on NON-NEG law → WARN
│   ├── test_bdd_code_block.py       # Phase 3 §4.3 Scenarios (T-07 code-block exclusion):
│   │                                #   fenced IDs not extracted; inline code IDs not extracted;
│   │                                #   mixed occurrence (body + fenced); multiline fenced block
│   └── test_bdd_no_frontmatter.py   # Phase 3 §4.5 Scenario: --output append on no-frontmatter
│                                    #   artifact → prepend block; existing content preserved
├── integration/
│   ├── test_real_artifact.py     # scan an actual constitution artifact (known-clean → exit 0)
│   └── test_regex_redos.py       # T-03/ADR-003: ≥10,000-char crafted string, assert <100ms per pattern
└── fixtures/
    ├── scanner/                  # (from S-02) + additional:
    │   └── artifact_many_citations.md      # T-09: >1000 citation matches → WARN
    ├── auditor/                  # (from S-03)
    ├── bdd/
    │   ├── artifact_no_frontmatter.md      # Phase 3 §4.5: file with no ---...--- block
    │   └── artifact_code_block_ids.md      # Phase 3 §4.3: T-07 fenced block IDs
    └── constitution_sample/      # copy of known-clean phase-1-capture.md for integration

.github/
└── workflows/
    └── citation-audit.yml        # Phase 3 §5 CI pipeline spec:
                                  # - scans ALL modified .md files in PR diff
                                  # - --allow-draft ENG-14.1,ENG-14.2 (until Phase 8 merge)
                                  # - Week 1: warn-only (exit 0); Week 2+: enforce (exit $FAILED)
                                  # - exit 2 on tool error halts CI immediately
```

**Coverage requirement:** `--cov-fail-under=90` across ALL modules (ENG-4.6 NON-NEGOTIABLE).

**Quality gate:** `pytest-cov ≥ 90%` (ENG-4.6), `ruff bugs=0`, `new_security_hotspots_reviewed = 0`

---

### S-06: Workflow Amendments

| Field | Value |
|-------|-------|
| Slice ID | S-06 |
| Complexity | 5 story points |
| Depends on | S-05 (tool verified working before amending workflows) |
| Layer | Constitution (workflow .md files) |

**Files modified (7 actual workflow files on disk):**

| Workflow file | Jury gate today? | Change |
|--------------|:---:|--------|
| `workflows/greenfield-development.md` | ✅ Yes | Add J6 Citation Auditor row to jury table; add `aa-citation-audit` pre-jury step; update `law_citations` frontmatter |
| `workflows/product-discovery-stage-a-f.md` | ✅ Yes | Add `aa-citation-audit` pre-jury step; add J6 row; update frontmatter |
| `workflows/legacy-rescue-refactor.md` | ❌ No | Add PRD-2.6 jury gate + `aa-citation-audit` step + J6 row together (must land atomically) |
| `workflows/legacy-rescue-rewrite.md` | ❌ No | Same as above |
| `workflows/legacy-rescue-decision-track.md` | ❌ No | Same as above |
| `workflows/avatar-workflow.md` | ❌ No | Same as above |
| `workflows/adoption.md` | ❌ No | Same as above |

> **Design spec §5.3 constraint:** For the 5 workflows without jury gates, PRD-2.6 jury
> gate language and the citation audit step MUST land in the same commit — citation audit
> is meaningless without a jury gate.

**Phase 8 only (not in S-06):** `proposed/citation-integrity.md` → `laws/engineering/citation-integrity.md` merge + all index.yaml updates (requires human APPROVE gate per A-P2-006). See §5.

**Quality gate:** `ruff bugs=0` (N/A for Markdown). Workflow amendment correctness verified by manual review + `aa-constitution-lint` if available.

---

## 2. Dependency Graph (ENG-2.3)

```
S-01: Project Scaffold + Registry + Data Models
  │
  ├─────────────────────┐
  ▼                     ▼
S-02: Scanner         S-03: Auditor
(parallel)            (parallel — no import dep on S-02;
                       both import models.py from S-01)
  │                     │
  └──────────┬──────────┘
             ▼
           S-04: CLI + DI Orchestration
             │
             ▼
           S-05: BDD + Integration + CI
             │
             ▼
           S-06: Workflow Amendments
             │
             ▼ (Phase 6 completes here)
           Phase 7 Review (separate phase — constitution compliance + OWASP + mutation verification)
             │
             ▼ (Phase 7 completes here)
           Phase 8 Ship (Article XIV merge — human APPROVE gate)
```

**ENG-2.3 independence check:**
- S-01 has zero upward dependencies ✅
- S-02 needs `RegistryEntry` + `models.py` types from S-01; no auditor/cli coupling ✅
- S-03 needs `Verdict`, `CitationResult`, `AuditResult`, `RegistryEntry` from S-01; plain `list[tuple[str,str]]` from S-02 signature (no import dep — parallel is valid) ✅
- S-04 wires DI; no domain logic ✅
- S-05 black-box tests full stack; no new production code ✅
- S-06 is constitution-level amendments; independent of unit test results (only requires S-05 green) ✅

---

## 3. Test Pyramid Strategy

```
         ┌──────────────┐
         │  Integration  │  ~15%  (BDD end-to-end, real artifact scan)
         ├──────────────┤
         │  Fixtures /   │  ~15%  (T-07 code-block, T-09 DoS, ReDoS regression)
         │  Boundary     │
         ├──────────────┤
         │   Unit Tests  │  ~70%  (registry, scanner, auditor, cli units)
         └──────────────┘
```

| Layer | Target files | Coverage target | Mutation target |
|-------|-------------|-----------------|----------------|
| Unit | registry.py, scanner.py, auditor.py, cli.py | ≥90% (ENG-4.6) | ≥85% scanner.py + auditor.py (ENG-4.11) |
| Boundary/Fixture | T-07 §4.3 code-block, T-09 DoS, T-03 ReDoS | 100% scenario coverage | N/A (fixture-driven) |
| Integration | Full stack end-to-end | ≥1 PASS + ≥1 FAIL scenario | N/A |

**No system tests** — `aa-citation-audit` has no network I/O; integration tests substitute.

**ENG-4.1 Atomic TDD Execution Constraint (NON-NEGOTIABLE):**
Each slice in Phase 6 MUST demonstrate the RED→GREEN→REFACTOR cycle:
1. Commit `test_*.py` with failing assertions (RED) — test file committed before production code
2. Implement production code to pass tests (GREEN) — commit separately
3. Refactor + VERIFY — confirm coverage and mutation thresholds met
4. Only after GREEN+VERIFY → advance to next slice

**Mutation testing ownership:**
- **Phase 6 Build** — mutation tests EXECUTE per slice (S-02 for scanner.py, S-03 for auditor.py, S-05 verifies overall)
- **Phase 7 Review** — mutation score VERIFIED as part of constitution compliance review; Phase 7 jury owns the ≥85% attestation
Both phases are required. Phase 6 produces the score; Phase 7 confirms it meets the threshold.

---

## 4. Complexity Summary

| Slice | Story Points | Critical Path? | Quality gate |
|-------|-------------|----------------|--------------|
| S-01 | 5 | ✅ Yes | pytest-cov ≥90% (ENG-4.6), ruff bugs=0, mutmut ≥85% on registry.py (ENG-4.11) |
| S-02 | 3 | ✅ Yes | pytest-cov ≥90% (ENG-4.6), mutmut ≥85% on scanner.py (ENG-4.11) |
| S-03 | 5 | ✅ Yes | pytest-cov ≥90% (ENG-4.6), mutmut ≥85% on auditor.py (ENG-4.11) |
| S-04 | 5 | ✅ Yes | pytest-cov ≥90% (ENG-4.6), ruff bugs=0 |
| S-05 | 13 | ✅ Yes | pytest-cov ≥90% (ENG-4.6), ruff bugs=0 |
| S-06 | 5 | No (parallelisable post-S-05) | ruff bugs=0; Markdown — coverage N/A |
| **Total** | **36** | | |

> **Phase 6 gate (ENG-12.1 NON-NEGOTIABLE):** Each slice is committed only after pytest-cov ≥90%, ruff bugs=0, and mutmut ≥85% on critical modules. Jury deliberation on slice evidence before advancing. Human reviews jury synthesis before approving phase advance.

**Acceptance criteria (Phase 4 §0 Success Criteria — all must pass at Phase 7):**

| Criterion | Measure | Target |
|-----------|---------|--------|
| FAIL detection accuracy | % fabricated IDs caught | 100% (zero false negatives) |
| WARN precision | WARN/false-WARN ratio | ≥80% precision at Phase 7 threshold calibration |
| False PASS rate | Semantic citation missed due to code-block stripping | 0 in fixture suite |
| Exit code correctness | Correct exit code per Phase 3 BDD scenarios | 100% |
| Performance | Scan time for 500-line artifact | <2 seconds |
| BUS-7.1 audit trail | Structured scan record per invocation | 100% (frontmatter + audit.log) |

---

## 5. Phase 8 Deliverables (This Plan Identifies, Not Executes)

The following are Phase 8 Ship items tracked here for completeness:
- Copy `proposed/citation-integrity.md` → `laws/engineering/citation-integrity.md`
- Apply `laws/engineering/_domain.yaml` Article XIV entry (Phase 4 §3.2)
- Apply `laws/index.yaml` Article XIV entries (Phase 4 §3.3): `domains.engineering.files`, `domains.engineering.articles`, `law_ids.engineering`, `non_negotiable.engineering`, `law_counts`
- Human APPROVE gate (executive sign-off on Article XIV — A-P2-006)
- Re-run `aa-citation-audit` on ALL Phase 1–4 artifacts with `--allow-draft` removed — confirm 0 FAIL
- Remove `--allow-draft ENG-14.1,ENG-14.2` from CI config (`citation-audit.yml`)
- Delete `proposed/` directory

---

## 6. Phase 5 Deliverables

| Deliverable | File | Status |
|-------------|------|--------|
| Slice plan (this artifact) | `phase-5-plan.md` | Authored |
| Human-readable PROPOSAL | `PROPOSAL.md` | Authored |
| PROPOSAL rendered as HTML | `html/PROPOSAL.html` | Rendered (ENG-13.1) |

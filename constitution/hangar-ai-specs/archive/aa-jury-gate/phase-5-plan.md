---
author: Hangar AI (claude-sonnet-4.6)
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 13
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 13
  strict: false
  timestamp: '2026-05-26T02:40:34Z'
  tool: aa-citation-audit
  verdicts:
  - context_snippet: null
    id: BUS-7.1
    verdict: PASS
  - context_snippet: null
    id: ENG-1.5
    verdict: PASS
  - context_snippet: null
    id: ENG-11.1
    verdict: PASS
  - context_snippet: null
    id: ENG-12.1
    verdict: PASS
  - context_snippet: null
    id: ENG-2.1
    verdict: PASS
  - context_snippet: null
    id: ENG-2.3
    verdict: PASS
  - context_snippet: null
    id: ENG-3.7
    verdict: PASS
  - context_snippet: null
    id: ENG-4.1
    verdict: PASS
  - context_snippet: null
    id: ENG-4.11
    verdict: PASS
  - context_snippet: null
    id: ENG-4.4
    verdict: PASS
  - context_snippet: null
    id: ENG-4.6
    verdict: PASS
  - context_snippet: null
    id: PRD-2.3
    verdict: PASS
  - context_snippet: null
    id: PRD-2.6
    verdict: PASS
  version: 0.2.0
  warn_count: 0
date: 2026-05-25
law_citations:
- ENG-1.5
- ENG-2.1
- ENG-2.3
- ENG-4.1
- ENG-4.4
- ENG-4.6
- ENG-4.11
- ENG-11.1
- ENG-12.1
- PRD-2.3
- PRD-2.6
- BUS-7.1
phase: 5
project: aa-jury-gate
status: CORRECTED-R2
title: Plan — aa-jury-gate CLI
workflow: greenfield-development
---



# Phase 5 — Plan: aa-jury-gate CLI

> **Phase focus (greenfield-development.md §Phase 5):**
> Vertical slices with dependency graph (ENG-2.3); complexity estimates;
> test pyramid strategy. Implementation proposal in `hangar-ai-specs/changes/`.
>
> **Inputs:** Phase 3 Define (14 checks, 26 BDD scenarios, CLI contract)
> Phase 4 Design (11 modules, 4 ADRs, public APIs, GateRunner DI, GateVerdict.exit_code)
> **Output:** PROPOSAL with 8 vertical slices, dependency graph, test pyramid, estimates

---

## 0. Planning Constraints

| Constraint | Requirement | Source |
|-----------|-------------|--------|
| TDD mandatory | Every slice: RED → GREEN → REFACTOR → VERIFY → COMMIT | ENG-4.1 (NON-NEGOTIABLE) |
| Coverage floor | `pytest-cov ≥ 90%` across all modules | ENG-4.6 |
| Mutation floor | `mutmut ≥ 85%` on critical modules | ENG-4.11 |
| Lint gate | `ruff check --select E,W,F,B,S` — zero `bugs` findings | ENG-1.5 |
| Slice independence | Each slice reviewable and testable in isolation | ENG-2.3 |
| BDD traceability | All 26 Phase 3 BDD scenarios assigned to exactly one slice | ENG-4.4 |
| Per-slice jury | Per-slice 5-juror jury in Phase 6 before advancing to next slice | PRD-2.6 |
| Per-slice gate | Each slice: commit evidence → jury → judicial synthesis → human APPROVE | ENG-12.1 |

**CLI contract (Phase 3 §1.1):** `aa-jury-gate SYNTHESIS [OPTIONS]` — `SYNTHESIS` is a **positional** argument, not a flag.
**Python floor:** `>=3.10` — `str | None` syntax, `list[T]` generics (Phase 4 §0)
**Test runner:** `pytest` with `pytest-cov` and `mutmut`

### Phase 3 Check IDs (immutable — from Phase 3 §3)

| ID | Surface | Check |
|----|---------|-------|
| **S01** | File | File exists and is readable |
| **S02** | File | Extension is `.md`, `.yaml`, or `.yml` |
| **S03** | File | File is valid YAML (`yaml.safe_load`) |
| **S04** | File | YAML root is a mapping |
| **S05** | Schema | `schema_version == 1` |
| **S06** | Schema | `juror_count == 5` |
| **S07** | Schema | `jurors` list has exactly 5 entries (hardcoded `5`, NOT `juror_count`) |
| **S08a** | Schema | All juror `model` values distinct (case-sensitive) |
| **S08b** | Schema | No juror model equals `"claude-haiku-4.5"` |
| **S09** | Schema | `rounds.r1_completed` is `True` |
| **S10** | Schema | `rounds.r2_completed` is `True` |
| **S11** | Schema | `verdict == "APPROVED"` |
| **B01** | Body | Body contains heading matching `^##\s+(Round\s+1\|R1)(\s\|:\|-\|$)` |
| **B02** | Body | Body contains heading matching `^##\s+(Round\s+2\|R2)(\s\|:\|-\|$)` |
| **B03** | Body | Body contains heading matching `^##\s+(Synthesis\|Final\|Judicial)(\s\|:\|-\|$)` |
| **G01** | Git | Synthesis file tracked by git and has no uncommitted changes |

**Check ordering (Phase 3 §3):** S01→S02→S03→S04 (fast-fail). Then S05–S11–B01–B03–G01 (collect all, report all).
**B01-B03 SKIP rule:** Skipped when S11 FAIL (`verdict ≠ "APPROVED"`).

---

## 1. Vertical Slice Registry (ENG-2.3)

Eight slices decompose the 11-module architecture into independently deliverable and verifiable increments.

| Slice | Name | Modules | Points | Depends on |
|-------|------|---------|--------|-----------|
| VS-01 | Scaffold & Domain Model | `models.py`, `pyproject.toml` | 3 | — |
| VS-02 | Extractor | `extractor.py` | 5 | VS-01 |
| VS-03 | File & Schema Checks S01–S08b | `checks/schema.py` (S01–S08b) | 8 | VS-02 |
| VS-04 | Schema Checks S09–S11 + Security | `checks/schema.py` (S09–S11), `security.py` | 5 | VS-02 |
| VS-05 | Body Checks B01–B03 | `checks/body.py` | 3 | VS-02 |
| VS-06 | Git Probe & G01 | `git_probe.py`, `checks/git.py` | 5 | VS-02 |
| VS-07 | Gate + CLI + Output | `gate.py`, `cli.py`, `output.py`, `tests/conftest.py` | 13 | VS-03, VS-04, VS-05, VS-06 |
| VS-08 | Audit + Smoke + Packaging | `audit.py`, `tests/test_smoke.py`, full `pyproject.toml` | 8 | VS-07 |

**Total: 50 points** (Fibonacci; 1 pt ≈ ~1 hr focused TDD)
**Single-developer calendar estimate:** 50 pts / ~5 pts/day effective ≈ 10 working days (~2 calendar weeks), excluding per-slice jury gate overhead (~1–2 days additional).

---

## 2. Slice Specifications

### VS-01: Scaffold & Domain Model

**Goal:** Establish the importable package skeleton and complete domain model. No business logic.

**Deliverables:**
- `pyproject.toml` (scaffold: entry point, dependencies, build backend, `python_requires=">=3.10"`)
- `aa_jury_gate/__init__.py`
- `aa_jury_gate/models.py`:
  - `CheckResult(Enum)`: `PASS = "PASS"`, `FAIL = "FAIL"`, `SKIP = "SKIP"` — **`Enum` only** (not `str, Enum`; consistent with Phase 4 §5.3)
  - `GateVerdict(Enum)`: `PASS`, `FAIL`, `ERROR` with `@property exit_code` (PASS→0, FAIL→1, ERROR→2) — **`Enum` only**
  - `@dataclass CheckItem`: `check_id: str`, `result: CheckResult`, `detail: str`
  - `@dataclass GateResult`: `content_sha256: str`, `verdict: GateVerdict`, `checks: list[CheckItem]` (Phase 4 §1.2)
  - `@dataclass AuditEntry`: all fields per Phase 4 §6.1
  - `GitStatus(Enum)`: `CLEAN`, `UNTRACKED`, `UNCOMMITTED` — return type of `GitProbe.check()` (Phase 4 §2.3; C-P5-J2-R2-002)
  - `ToolError(Exception)`, `GitBinaryNotFoundError(ToolError)`, `GitProbeError(Exception)` (Phase 4 §5.2)
- `tests/test_models.py`

> **Note on enum mixin (C-P5-J2-007):** `Enum` only (no `str` mixin) matches Phase 4 §5.3. Audit serialization must use the `default=` lambda (Phase 4 §6.1) since `.value` is not auto-coerced.

**Test targets (ENG-4.1 RED→GREEN):**
1. `GateVerdict.exit_code`: PASS→0, FAIL→1, ERROR→2
2. `CheckResult.PASS.value == "PASS"`, FAIL, SKIP
3. `GitBinaryNotFoundError` is subclass of `ToolError`
4. `GitProbeError` is NOT a subclass of `ToolError`
5. `GitStatus` values: `CLEAN`, `UNTRACKED`, `UNCOMMITTED`
6. `GateResult` instantiation with defaults

**Slice jury gate:** Commit `tests/test_models.py` + `models.py` → R1 jury (5 jurors) → corrections → R2 → synthesis → human APPROVE → proceed to VS-02.

**Exit criteria:** `pytest tests/test_models.py` passes; `ruff` zero bugs; `pip install -e .` installs entry point; committed.

---

### VS-02: Extractor

**Goal:** Implement `extractor.py` — the YAML frontmatter parser and `strip_jury_gate()`.
Foundation for content_sha256 (ADR-002) and all schema/body checks.

**Deliverables:**
- `aa_jury_gate/extractor.py`:
  - `parse(path: Path) -> tuple[dict, str]` — reads file, returns `(frontmatter_dict, body_text)`; raises `UnclosedFrontmatterError(ToolError)` if opening `---` found but no closing `---`; raises `yaml.YAMLError` on invalid YAML; returns `({}, "")` if no opening `---` found. (Phase 4 §2.1)
  - `strip_jury_gate(content: str) -> str` — input is the **full file string** including `---` delimiters and body; removes `jury_gate:` key from frontmatter using YAML parse-and-remove (not regex); returns full file unchanged if no `jury_gate:` key present. (Phase 4 §2.1 — C-P4-J5-001-R2)
- `tests/test_extractor.py`

**content_sha256 formula (ADR-002):**
```python
raw_bytes: bytes = path.read_bytes()
stripped: str = extractor.strip_jury_gate(raw_bytes.decode('utf-8'))
content_sha256: str = hashlib.sha256(stripped.encode('utf-8')).hexdigest()
```

**Test targets (ENG-4.1 RED→GREEN):**
1. `parse()` — valid frontmatter → `(dict, body_str)`
2. `parse()` — no opening `---` → `({}, "")`
3. `parse()` — opening `---` with no closing `---` → `UnclosedFrontmatterError`
4. `parse()` — invalid YAML frontmatter → `yaml.YAMLError`
5. `strip_jury_gate()` — file with `jury_gate:` block → block removed; other keys preserved; body preserved
6. `strip_jury_gate()` — file without `jury_gate:` → content unchanged (C vs C yields C)
7. `strip_jury_gate()` — idempotent: `strip(strip(C)) == strip(C)`
8. **Cross-run idempotency (ADR-002):** Given `C` (no `jury_gate:` block) and `C'` (same content with `jury_gate:` block written in), assert `sha256(strip(C).encode()) == sha256(strip(C').encode())` — both files hash identically, proving strip is stable. (C-P5-J2-004)

> **Note (C-P5-J5-004):** `strip_jury_gate` stability is byte-for-byte over UTF-8 encoded content. Cross-platform CRLF normalisation is the caller's responsibility; the tool does not normalise line endings. If `path.read_bytes()` produces CRLF on Windows, the sha256 will differ from a LF system. This is accepted behaviour for v1 (POSIX-only per Phase 4 §0).

**Slice jury gate:** Commit slice evidence → jury → human APPROVE → proceed to VS-03.

**Exit criteria:** `pytest tests/test_extractor.py` passes; `mutmut ≥ 85%` on `extractor.py`; committed.

---

### VS-03: File & Schema Checks S01–S08b

**Goal:** Implement S01–S08b in `checks/schema.py`. These are the file-level fast-fail checks
(S01–S04) and schema content checks (S05–S08b).

**Deliverables:**
- `aa_jury_gate/checks/__init__.py`
- `aa_jury_gate/checks/schema.py` (S01–S08b):
  - `S01` — `path.exists() and path.is_file()`
  - `S02` — `path.suffix in {'.md', '.yaml', '.yml'}`
  - `S03` — `yaml.safe_load(content)` succeeds (AC-SEC-01)
  - `S04` — `isinstance(parsed, dict)`
  - `S05` — `frontmatter.get('schema_version') == 1`
  - `S06` — `frontmatter.get('juror_count') == 5`
  - `S07` — `len(frontmatter.get('jurors', [])) == 5` (hardcoded `5`, NOT `juror_count`)
  - `S08a` — all 5 juror `model` strings distinct (case-sensitive)
  - `S08b` — no juror model equals `"claude-haiku-4.5"` (exact match)
- `tests/test_schema.py`

> **S08b scope (C-P5-J1-003):** S08b = no haiku-4.5. Synthesizer model distinctness is **v2** per Phase 3 §11 and Phase 5 §6.

**Test targets (TDD per check — PASS and FAIL path for each):**
- S01: non-existent path → FAIL; valid file → PASS
- S02: `.txt` extension → FAIL; `.md` → PASS; `.yaml` and `.yml` → PASS
- S03: invalid YAML → FAIL; valid YAML → PASS
- S04: YAML root is list (not dict) → FAIL; dict → PASS
- S05: `schema_version: 2` → FAIL; `schema_version: 1` → PASS; key absent → FAIL
- S06: `juror_count: 4` → FAIL; `juror_count: 5` → PASS
- S07: `jurors` list with 4 entries → FAIL; 5 entries → PASS; S07 uses hardcoded `5`, not `juror_count`
- S08a: two jurors with same model → FAIL; all distinct → PASS
- S08b: one juror model = `"claude-haiku-4.5"` → FAIL; none → PASS

**Slice jury gate:** Commit slice evidence → jury → human APPROVE → proceed.

**Exit criteria:** `pytest tests/test_schema.py` passes; ruff zero bugs; committed.

---

### VS-04: Schema Checks S09–S11 + Security

**Goal:** Complete schema checks (S09–S11) and implement `security.py` path validation.
S09–S11 validate the rounds and verdict fields. `security.py` provides path pre-validation
called by `gate.py` / `cli.py` before any checks run.

**Deliverables:**
- `aa_jury_gate/checks/schema.py` (S09–S11 appended):
  - `S09` — `frontmatter.get('rounds', {}).get('r1_completed') is True`
  - `S10` — `frontmatter.get('rounds', {}).get('r2_completed') is True`
  - `S11` — `frontmatter.get('verdict') == "APPROVED"`
- `aa_jury_gate/security.py`:
  - `validate_synthesis_path(path: Path) -> Path` — validation sequence: (1) exists → (2) is_file → (3) is_symlink → (4) size ≤ 1 MB; raises `ToolError` on any violation; symlink rejected before size read (Phase 4 §2.2)
  - `validate_log_dir(log_dir: str | None) -> Path` — `str | None` input (Click passes raw string); if None returns default `~/.aa-jury-gate/`; expands `~`; calls `os.path.realpath()` (resolves symlinks); verifies result does not escape CWD **only when caller-supplied** (not when None default is used — C-P5-J2-R2-003); raises `ToolError` on traversal (Phase 4 §2.2 — C-P5-J2-003)
- `tests/test_schema_s09_s11.py`, `tests/test_security.py`

**Test targets:**
- S09: `rounds.r1_completed: false` → FAIL; `true` → PASS; key absent → FAIL
- S10: `rounds.r2_completed: false` → FAIL; `true` → PASS
- S11: `verdict: "NEEDS_REVISION"` → FAIL; `"APPROVED"` → PASS
- `validate_synthesis_path`: each of 4 steps (missing, is-dir, symlink, oversized) → `ToolError`
- `validate_log_dir`: `"../../etc"` → `ToolError`; `"./logs"` → resolved absolute path; `None` → default path
- `validate_log_dir`: `str` input (not `Path`) → correct (C-P5-J2-003)

**Slice jury gate:** Commit slice evidence → jury → human APPROVE → proceed.

**Exit criteria:** `pytest tests/test_schema_s09_s11.py tests/test_security.py` passes; `mutmut ≥ 85%` on `security.py`; committed.

---

### VS-05: Body Checks B01–B03

**Goal:** Implement B01–B03 in `checks/body.py`. These checks operate on the body portion
of the synthesis file (text after the closing `---` frontmatter delimiter).

**Deliverables:**
- `aa_jury_gate/checks/body.py`:
  - `B01` — body matches `^##\s+(Round\s+1|R1)(\s|:|-|$)` (multiline, case-insensitive; Phase 3 §3)
  - `B02` — body matches `^##\s+(Round\s+2|R2)(\s|:|-|$)`
  - `B03` — body matches `^##\s+(Synthesis|Final|Judicial)(\s|:|-|$)`
  - Each function signature: `check_bXX(body: str) -> CheckItem` — takes body text only; returns PASS or FAIL
  - **SKIP logic is in `gate.py` (VS-07):** B01–B03 are skipped by the orchestrator when S11 fails. Body check functions themselves do NOT implement skip — they return PASS/FAIL on the body they are given. (C-P5-J1-005, C-P5-J5-001)
- `tests/test_body.py`

**Test targets:**
- B01: body with `## Round 1 Summary` → PASS; body without → FAIL; `## R1: Results` → PASS; `## R10` does NOT match → FAIL
- B02: body with `## Round 2` → PASS; without → FAIL
- B03: body with `## Synthesis` → PASS; `## Final` → PASS; `## Judicial` → PASS; without → FAIL
- F04 (BDD): body missing `Synthesis`/`Final`/`Judicial` heading → B03 FAIL (unit-level)

> **SKIP unit-level clarification:** VS-05 unit tests verify B01-B03 return PASS/FAIL correctly. The "B01-B03 SKIP when S11 FAIL" BDD assertion (Phase 3 scenario 11) is an integration-level assertion verified in VS-07.

**Slice jury gate:** Commit → jury → human APPROVE → proceed.

**Exit criteria:** `pytest tests/test_body.py` passes; committed.

---

### VS-06: Git Probe & G01

**Goal:** Implement `git_probe.py` (Protocol + real + stub) and `checks/git.py` (G01).
G01 checks: synthesis file is tracked by git AND has no uncommitted changes.

**Deliverables:**
- `aa_jury_gate/git_probe.py`:
  - `class GitProbe(Protocol)`: `def check(self, path: Path) -> GitStatus` (Phase 4 §2.3 — C-P5-J2-R2-001)
  - `class RealGitProbe`: invokes `git rev-parse` + `git ls-files` + `git status`; raises `GitBinaryNotFoundError` if git absent; raises `GitProbeError` on non-zero exit or unexpected state; returns `GitStatus.CLEAN` on success
  - `class StubGitProbe`: in-process test double; configurable to return a `GitStatus` value or raise `GitProbeError` / `GitBinaryNotFoundError` without subprocess
- `aa_jury_gate/checks/git.py`:
  - `G01(probe: GitProbe, path: Path, allow_no_git: bool) -> CheckItem`
  - `allow_no_git=True` + no git binary → SKIP; `allow_no_git=True` + inside repo → PASS (F06); `allow_no_git=False` + outside repo → FAIL
- `tests/test_git.py`

**Test targets:**
- `RealGitProbe`: git binary absent → `GitBinaryNotFoundError`
- `RealGitProbe`: path not in git repo → `GitProbeError`
- G01 with `StubGitProbe`: `allow_no_git=False`, outside repo → `CheckItem(result=FAIL)`
- G01 with `StubGitProbe`: `allow_no_git=True`, no git binary → `CheckItem(result=SKIP)`
- G01 with `StubGitProbe`: `allow_no_git=True`, inside repo → `CheckItem(result=PASS)` (BDD-F06)
- G01 PASS: tracked, committed file → `CheckItem(result=PASS)`

**Slice jury gate:** Commit → jury → human APPROVE → proceed.

**Exit criteria:** `pytest tests/test_git.py` passes; committed.

---

### VS-07: Gate + CLI + Output

**Goal:** Wire all checks into `GateRunner`, expose via Click CLI, implement `--output append`
atomic write, and verify all integration-level BDD scenarios. Largest slice; integrates all
prior modules into observable CLI behaviour.

**Deliverables:**
- `aa_jury_gate/gate.py`:
  - `class GateRunner`: `__init__(self, git_probe: GitProbe)` — only DI seam (ADR-004); `cli.py` is composition root (Phase 4 §2.3)
  - `def run(self, path: Path, allow_no_git: bool) -> GateResult`
  - Check execution order: `extractor.parse()` → S01-S04 (fast-fail) → S05-S11 (collect all) → B01-B03 (skip if S11 FAIL) → G01
  - **`validate_synthesis_path()` is called by `cli.py` BEFORE `runner.run()` — NOT inside `GateRunner.run()`** (single call site; C-P5-J4-R2-001)
  - **`GitProbeError` handling:** `checks/git.py` catches `GitProbeError` from `git_probe.check()` and returns `CheckItem(result=FAIL, detail=...)` — this becomes a FAIL verdict, NOT ERROR (Phase 4 §5.2; C-P5-J5-R2-001)
  - `content_sha256` computed via ADR-002 formula
  - Returns `GateVerdict.ERROR` on `ToolError`; `GateVerdict.FAIL` if any check FAIL; `GateVerdict.PASS` otherwise
- `aa_jury_gate/output.py`:
  - `append_gate_result(path: Path, result: GateResult) -> None`
  - Atomically writes `jury_gate:` YAML block to frontmatter via `tempfile.NamedTemporaryFile(dir=path.parent)` + `os.replace()` (Phase 3 §4 same-dir requirement)
  - Written on `GateVerdict.PASS` and `FAIL` (exit 0 and 1); **NOT written on `ERROR` (exit 2)** (ADR-003, BDD-F05)
- `aa_jury_gate/cli.py`:
  - `@click.command` with `SYNTHESIS` positional arg (`click.argument`) + options: `--output [append]`, `--log-dir PATH`, `--allow-no-git / --no-allow-no-git` (Phase 3 §1.1)
  - Calls `validate_synthesis_path()` (single call — NOT repeated inside runner), instantiates `GateRunner(git_probe=RealGitProbe())`, calls `runner.run()`, optionally calls `append_gate_result()`, calls `sys.exit(result.verdict.exit_code)`
  - Prints stdout table per Phase 3 §1.3 format
- `tests/conftest.py`:
  - `tmp_git_repo(tmp_path)` fixture: `git init` + `git add` + `git commit` — provides a real git repo with a valid committed synthesis file
  - `synthesis_factory(tmp_path)` fixture: builds synthesis `.md` files with configurable frontmatter
  - `env_isolation(monkeypatch, tmp_path)` fixture: sets `--log-dir` to `tmp_path/logs` for all CLI/integration tests; asserts no writes outside `tmp_path` (C-P5-J4-008)
- `tests/test_gate.py`, `tests/test_output.py`, `tests/test_cli.py`

**Test targets (ENG-4.1 RED→GREEN — full integration via `CliRunner`):**
1. `GateRunner.run()`: valid APPROVED synthesis in git repo → `GateResult(verdict=PASS)`
2. `GateRunner.run()`: invalid synthesis (S05 FAIL) → `GateResult(verdict=FAIL)`
3. `GateRunner.run()`: unreadable file / `ToolError` → `GateResult(verdict=ERROR)`
4. `output.py`: `GateVerdict.FAIL` → writes `jury_gate:` block; `GateVerdict.ERROR` → does NOT write (BDD-F05)
5. `output.py`: idempotent overwrite — writing twice produces same block (not duplicated)
6. `output.py`: atomic replace — temp file created in `path.parent` (same-dir)
7. CLI: `aa-jury-gate SYNTHESIS` missing → usage error (positional arg required)
8. CLI: `aa-jury-gate <valid>` → exit 0, stdout contains `PASS` (BDD scenario 1)
9. CLI: `aa-jury-gate <valid> --output append` → exit 0, `jury_gate:` block written (BDD scenario 2)
10. CLI: `aa-jury-gate <valid> --output append` (idempotent re-run) → exit 0, block not duplicated (BDD scenario 3)
11. CLI: `aa-jury-gate <fail>` → exit 1, stdout contains `FAIL` lines (BDD scenario 4)
12. CLI: `aa-jury-gate <nonexistent>` → exit 2, no `--output` write (BDD scenario 15)
13. CLI: `aa-jury-gate <directory>` → exit 2 (BDD scenario 16)
14. CLI: `aa-jury-gate <invalid_yaml>` → exit 2 (BDD scenario 17)
15. CLI: exit-2 stdout is empty or error-only (Phase 3 §1.3 contract)
16. CLI: `aa-jury-gate <valid> --allow-no-git` outside git repo → exit 0 (G01 SKIP, BDD scenario 19); (C-P5-J2-005)
17. CLI: `aa-jury-gate <valid> --allow-no-git` inside git repo → exit 0 (G01 PASS, BDD-F06)
18. CLI: `aa-jury-gate <valid>` outside git repo WITHOUT `--allow-no-git` → exit 1, stdout contains `G01    FAIL` (BDD scenario 18; C-P5-J4-R2-001)
18. CLI: S11 FAIL → B01-B03 all SKIP in stdout (BDD scenario 11)
19. CLI: `--version` flag → version string; requires `pip install -e .[dev]` (importlib.metadata)

> **VS-07 sub-task ordering (C-P5-J4-001):** (a) `gate.py` + unit tests first; (b) `output.py` + atomic-write tests; (c) `cli.py` wiring + CliRunner integration. If (c) is blocked, (a) and (b) can be committed independently.

**Slice jury gate:** Commit slice evidence → jury → human APPROVE → proceed to VS-08.

**Exit criteria:** All test targets pass; `pytest-cov ≥ 90%` on VS-07 modules; ruff zero bugs; committed.

---

### VS-08: Audit Logging + Smoke Test + Packaging

**Goal:** Implement `audit.py` (JSONL audit with enum-safe serialisation), ship CI-blocking
`tests/test_smoke.py`, update `cli.py` to wire audit, and complete `pyproject.toml`.

**Deliverables:**
- `aa_jury_gate/audit.py`:
  - `write_audit_entry(entry: AuditEntry, log_dir: Path) -> None`
  - Serialises via `json.dumps(dataclasses.asdict(entry), default=lambda o: o.value if isinstance(o, Enum) else str(o))` — **mandatory** `default=` lambda (Phase 4 §6.1; C-P4-J2-NF-003-R2)
  - Appends to `{log_dir}/gate.log` (JSONL)
  - Write failure: `print(f"Warning: audit log write failed: {e}", file=sys.stderr)` then continue — **not** `warnings.warn()`; does NOT affect exit code (ENG-3.7; C-P5-J5-002)
- **`cli.py` updated (audit wiring — C-P5-J4-002):**
  - After `runner.run()` and (optional) `append_gate_result()`, call `write_audit_entry(entry, log_dir)` for `PASS` and `FAIL` verdicts ONLY
  - **Do NOT call `write_audit_entry()` on `ERROR` (exit 2)** — consistent with `--output` no-write contract
  - Ordering: `append_gate_result()` → `write_audit_entry()` → `sys.exit()`
- `tests/test_audit.py`
- `tests/test_smoke.py` (CI-blocking per Phase 3 §7 / Phase 4 §7.1):
  - **3 scenarios using `tmp_path`-based dynamically-initialised git repo** (NOT the committed `phase-3-jury-synthesis.md` directly — C-P5-J2-006, C-P5-J4-004):
    - Smoke 1: valid committed synthesis → exit 0
    - Smoke 2: synthesis with uncommitted changes → exit 1 (G01 FAIL)
    - Smoke 3: nonexistent path → exit 2
  - Invokes `aa-jury-gate SYNTHESIS` subprocess; requires `pip install -e .[dev]` before `pytest`
  - Does NOT pass `--output append` (prevents dirty-worktree self-poisoning)
- `pyproject.toml` (complete):
  - `[project.scripts]`: `aa-jury-gate = "aa_jury_gate.cli:main"`
  - `[project.optional-dependencies]`: `dev = ["pytest>=7", "pytest-cov", "mutmut", "ruff", "click", "pyyaml"]`
  - `python_requires = ">=3.10"`
  - `version` single-source via `importlib.metadata`

**Test targets:**
1. `write_audit_entry`: JSONL line parseable; `CheckResult.PASS` serialises to `"PASS"` (not `<CheckResult.PASS: 'PASS'>`) — enum-safe lambda (C-P4-J2-NF-003-R2)
2. `write_audit_entry`: permission error on log dir → `print(..., file=sys.stderr)` called; no exception propagated
3. `audit.py` call on `ERROR` verdict: NOT called (log dir isolation via `env_isolation` fixture)
4. Smoke 1: subprocess exit code 0
5. Smoke 2: subprocess exit code 1
6. Smoke 3: subprocess exit code 2

**Slice jury gate:** Commit → jury → human APPROVE → Phase 6 complete.

**Exit criteria:** `pytest tests/` passes; `pytest-cov ≥ 90%` overall; `mutmut ≥ 85%` on `extractor.py`, `checks/schema.py`, `gate.py`, `security.py`, `models.py`; ruff zero bugs; committed.

---

## 3. Dependency Graph (ENG-2.3)

```
VS-01 (Scaffold & Models)
  └─→ VS-02 (Extractor)
        ├─→ VS-03 (S01–S08b)   ─────────────────────────────────┐
        ├─→ VS-04 (S09–S11 + Security)  ──────────────────────── │
        ├─→ VS-05 (Body Checks B01–B03)  ─────────────────────── │
        └─→ VS-06 (Git Probe + G01)  ─────────────────────────→  VS-07 (Gate + CLI + Output)
                                                                       └─→ VS-08 (Audit + Smoke + Packaging)
```

**Critical path:** VS-01 → VS-02 → VS-03 → VS-07 → VS-08 (24 points)

**Parallelisable window:** VS-03, VS-04, VS-05, VS-06 may be built concurrently after VS-02 commits.
**Recommended serial order (single developer):** VS-01 → VS-02 → VS-03 → VS-04 → VS-05 → VS-06 → VS-07 → VS-08.

---

## 4. Test Pyramid Strategy (ENG-4.1, ENG-4.4, ENG-4.6, ENG-4.11)

```
         ┌──────────────────────────┐
         │  Smoke Tests (3)         │  VS-08 — subprocess, real install
         ├──────────────────────────┤
         │  Integration Tests (~20) │  VS-07 — CliRunner, real synthesis fixtures
         ├──────────────────────────┤
         │  Unit Tests (~85)        │  VS-01–VS-06, VS-08 — isolated modules
         └──────────────────────────┘
```

### 4.1 Coverage Requirements (ENG-4.6)

| Module | Target |
|--------|--------|
| `models.py` | 100% |
| `extractor.py` | ≥95% |
| `checks/schema.py` | ≥90% |
| `checks/body.py` | ≥90% |
| `checks/git.py` | ≥90% |
| `security.py` | ≥95% |
| `gate.py` | ≥90% |
| `output.py` | ≥90% |
| `audit.py` | ≥90% |
| **Overall** | **≥90%** |

### 4.2 Mutation Testing (ENG-4.11)

**Critical modules — mutmut ≥85% required:**
```bash
mutmut run --paths-to-mutate \
  aa_jury_gate/extractor.py,\
  aa_jury_gate/checks/schema.py,\
  aa_jury_gate/gate.py,\
  aa_jury_gate/security.py,\
  aa_jury_gate/models.py
mutmut results  # ≥85% killed
```

> **gate.py included (C-P5-J4-003):** `gate.py` orchestrates skip logic, fast-fail ordering, and verdict computation. Mutation testing ensures guards are not vacuous.

### 4.3 Fixture Strategy

**Fixture file location:** `~/Repos/governance/hangar-ai-constitution/hangar-ai-specs/changes/aa-jury-gate/phase-3-jury-synthesis.md` — available as a reference for constructing synthetic fixtures. (C-P5-J3-005)

**Test isolation approach:**
- Unit tests: in-memory fixture construction (no file I/O); `StubGitProbe` for G01 unit tests
- Integration tests: `tmp_git_repo` pytest fixture (init + commit in `tmp_path`) from `tests/conftest.py`
- Smoke tests: `tmp_path`-based dynamically-initialised git repo; NOT the committed `phase-3-jury-synthesis.md` (dirty-worktree risk)
- All CLI/integration tests: `--log-dir tmp_path/logs` via `env_isolation` fixture (C-P5-J4-008)

**`tests/conftest.py` fixtures (C-P5-J4-006):**
- `tmp_git_repo(tmp_path)` — `git init` + create file + `git add` + `git commit`
- `synthesis_factory(tmp_path)` — builds `.md` synthesis files with configurable frontmatter dict
- `env_isolation(monkeypatch, tmp_path)` — overrides log dir; asserts no writes outside `tmp_path`

---

## 5. Phase 6 Entry Criteria (ENG-12.1)

All of the following must be verifiable before Phase 6 — Build begins:

| Criterion | Verification command |
|-----------|---------------------|
| Phase 5 Plan jury APPROVED, committed | `git log --oneline hangar-ai-specs/changes/aa-jury-gate/phase-5-*` |
| Python ≥3.10 available | `python3 --version` (must show 3.10.x or higher) |
| Dev tools installable independently | `pip install pytest pytest-cov mutmut ruff click pyyaml` succeeds (tools available before VS-01 scaffold) |
| `pip install -e .[dev]` succeeds (after VS-01) | `pip install -e .[dev] && aa-jury-gate --version` — run at start of VS-01 exit criteria |
| `pytest` + `pytest-cov` available | `pytest --version && python3 -c "import pytest_cov"` |
| `mutmut` available | `mutmut --version` |
| `ruff` available | `ruff --version` |
| Phase 3 jury synthesis exists as reference fixture | `ls hangar-ai-specs/changes/aa-jury-gate/phase-3-jury-synthesis.md` |

> **Note (C-P5-J1-007):** All runtime deps (`click`, `pyyaml`) and dev deps (`pytest>=7`, `pytest-cov`, `mutmut`, `ruff`) are installed by `pip install -e .[dev]` from the VS-01 scaffold `pyproject.toml`. No separate install steps needed after VS-01 is committed.

---

## 6. Per-Slice Jury Gate Checklist (PRD-2.6, ENG-12.1 — C-P5-J3-006)

Each slice in Phase 6 MUST complete this gate sequence before advancing to the next slice:

1. **Commit slice code** — TDD cycles complete; all test targets pass; ruff zero bugs
2. **Run `aa-citation-audit`** — 0 FAIL on the slice's evidence doc
3. **Run R1 jury** — 5 jurors in parallel (J1–J5); assign correction IDs `C-P6-VS0N-XXX`
4. **Apply corrections** — all NEEDS_REVISION items addressed
5. **Run R2 jury** — 5 jurors re-deliberate; acknowledge R1 corrections by ID
6. **Judicial synthesis** — `claude-opus-4.5`; APPROVED verdict required
7. **Re-verify** — synthesizer confirms all required changes applied
8. **Render HTML** — `aa-artifact-render`
9. **Commit artifacts** — slice evidence `.md` + `.html` + jury synthesis `.md`
10. **Human APPROVE** → advance to next slice

---

## 7. BDD Scenario Traceability (ENG-4.4)

All 26 Phase 3 BDD scenarios assigned. "Primary module" = where check logic lives; "BDD slice" = where full CLI-level assertion is verified.

| # | Phase 3 Scenario (exact title) | Primary module | BDD slice |
|---|-------------------------------|---------------|-----------|
| 1 | Valid synthesis file passes all checks | `gate.py` | VS-07 |
| 2 | --output append on passing gate writes jury_gate frontmatter block | `output.py` | VS-07 |
| 3 | --output append is idempotent on a file already containing jury_gate block | `output.py` | VS-07 |
| 4 | --output append on failing gate records failed state | `output.py` | VS-07 |
| 5 | Wrong file extension fails S02 | `checks/schema.py` | VS-07 |
| 6 | Wrong schema_version fails S05 | `checks/schema.py` | VS-07 |
| 7 | Synthesis with only 4 jurors fails S06 and S07 | `checks/schema.py` | VS-07 |
| 8 | Synthesis with duplicate juror models fails S08a | `checks/schema.py` | VS-07 |
| 9 | Synthesis with claude-haiku-4.5 juror model fails S08b | `checks/schema.py` | VS-07 |
| 10 | Synthesis with r1_completed false fails S09 | `checks/schema.py` | VS-07 |
| 11 | Synthesis with verdict NEEDS_REVISION fails S11 and skips B01-B03 | `gate.py` | VS-07 |
| 12 | Synthesis missing R2 body section fails B02 | `checks/body.py` | VS-07 |
| 13 | Synthesis missing synthesis section fails B03 | `checks/body.py` | VS-07 |
| 14 | Uncommitted synthesis file fails G01 | `checks/git.py` | VS-07 |
| 15 | Synthesis file does not exist returns exit 2 | `security.py` / `gate.py` | VS-07 |
| 16 | Synthesis path is a directory returns exit 2 | `security.py` | VS-07 |
| 17 | Synthesis file contains invalid YAML returns exit 2 | `checks/schema.py` (S03) | VS-07 |
| 18 | Non-git repo without --allow-no-git fails G01 | `checks/git.py` | VS-07 |
| 19 | Non-git repo with --allow-no-git downgrades to warning | `checks/git.py` | VS-07 |
| 20 | Audit log write failure is non-fatal | `audit.py` | VS-08 |
| 21 | BDD-F01 — Synthesis file with schema_version field absent fails S05 | `checks/schema.py` | VS-07 |
| 22 | BDD-F02 — Synthesis with invalid juror model string fails S05 | `checks/schema.py` | VS-07 |
| 23 | BDD-F03 — Synthesis with claude-haiku-4.5 juror fails S08b | `checks/schema.py` | VS-07 |
| 24 | BDD-F04 — Synthesis missing judicial synthesis body section fails B03 | `checks/body.py` | VS-07 |
| 25 | BDD-F05 — Exit 2 with --output append supplied does not write file | `output.py` | VS-07 |
| 26 | BDD-F06 — --allow-no-git inside a git repo still requires G01 checks | `checks/git.py` | VS-07 |

> All 26 scenarios fully verified at CLI integration level in VS-07, except scenario 20 (audit) which is VS-08.

---

## 8. Out of Scope (Phase 6)

| Item | Reason |
|------|--------|
| T9 mechanical hash verification (body-level) | Deferred to v2 per Phase 4 ADR |
| `fcntl.flock()` concurrent write locking | Deferred to v2 per Phase 4 §6.4 |
| Size-based log rotation (`--log-max-size`) | v2 per Phase 4 §6.2 |
| JSON stdout output mode | Not in Phase 3 CLI contract |
| AA internal PyPI publication | Aspirational; v1.1+ per Phase 4 §9.4 |
| `--dry-run` flag | Not in Phase 3 CLI contract |
| Python 3.9 backport variant | v1.1+ per Phase 4 §0 |
| Synthesizer model distinctness enforcement (S08b extension) | v2 PRD-2.6 hardening per Phase 3 §11 |

---

*Artifact status: CORRECTED-R1 — pending citation audit, R2 jury, and synthesis before commit.*

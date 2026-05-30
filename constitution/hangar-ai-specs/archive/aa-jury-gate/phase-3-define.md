---
author: Hangar AI (claude-sonnet-4.6)
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 19
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 19
  strict: false
  timestamp: '2026-05-26T01:36:47Z'
  tool: aa-citation-audit
  verdicts:
  - context_snippet: null
    id: BUS-7.1
    verdict: PASS
  - context_snippet: null
    id: ENG-1.5
    verdict: PASS
  - context_snippet: null
    id: ENG-10.1
    verdict: PASS
  - context_snippet: null
    id: ENG-11.1
    verdict: PASS
  - context_snippet: null
    id: ENG-12.1
    verdict: PASS
  - context_snippet: null
    id: ENG-12.3
    verdict: PASS
  - context_snippet: null
    id: ENG-13.1
    verdict: PASS
  - context_snippet: null
    id: ENG-14.1
    verdict: PASS
  - context_snippet: null
    id: ENG-2.1
    verdict: PASS
  - context_snippet: null
    id: ENG-2.5
    verdict: PASS
  - context_snippet: null
    id: ENG-3.5
    verdict: PASS
  - context_snippet: null
    id: ENG-3.7
    verdict: PASS
  - context_snippet: null
    id: ENG-4.4
    verdict: PASS
  - context_snippet: null
    id: ENG-6.1
    verdict: PASS
  - context_snippet: null
    id: ENG-6.4
    verdict: PASS
  - context_snippet: null
    id: ENG-6.5
    verdict: PASS
  - context_snippet: null
    id: ENG-6.7
    verdict: PASS
  - context_snippet: null
    id: PRD-2.6
    verdict: PASS
  - context_snippet: null
    id: PRD-5.1
    verdict: PASS
  version: 0.2.0
  warn_count: 0
date: 2026-05-26
law_citations:
- ENG-1.5
- ENG-2.1
- ENG-2.5
- ENG-3.5
- ENG-3.7
- ENG-4.4
- ENG-6.1
- ENG-6.4
- ENG-6.5
- ENG-6.7
- ENG-10.1
- ENG-11.1
- ENG-12.1
- ENG-12.3
- ENG-13.1
- ENG-14.1
- PRD-2.6
- PRD-5.1
- BUS-7.1
phase: 3
project: aa-jury-gate
r1_corrections: 15
status: CORRECTED-R1
title: Define — aa-jury-gate CLI
workflow: greenfield-development
---



# Phase 3 — Define: aa-jury-gate CLI

> **Phase focus (greenfield-development.md §Phase 3):**
> API contracts (ENG-1.5); data model with classification (ENG-6.4);
> BDD acceptance criteria (ENG-4.4).
>
> **Primary validation target:** `hangar-ai-specs/templates/jury-synthesis-template.md`

---

## 1. CLI Contract (ENG-1.5 — API-First Design)

### 1.1 Command Surface

```
aa-jury-gate SYNTHESIS [OPTIONS]
```

| Element | Value | Notes |
|---------|-------|-------|
| Command name | `aa-jury-gate` | Matches constitution tool naming convention |
| Framework | `click >= 8.1` | Consistent with citation-auditor; testable via CliRunner |
| Primary arg | `SYNTHESIS` (required positional) | Path to jury synthesis `.md` or `.yaml` file |

### 1.2 Arguments and Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `SYNTHESIS` | Path (required) | — | Jury synthesis file to validate |
| `--allow-no-git` | bool flag | False | If set AND the path is not inside a git repo, G01 downgrades to WARN+SKIP. If set but path IS inside a git repo, git checks apply normally (see §1.6 state matrix). |
| `--output append` | string literal | — | After gate check completes, atomically overwrite the `jury_gate:` frontmatter block in SYNTHESIS (idempotent). Written on exit 0 AND exit 1. NOT written on exit 2. |
| `--log-dir PATH` | Path | `~/.aa-jury-gate/` | Audit log directory. `AA_JURY_GATE_LOG_DIR` env var takes precedence over this flag. Default `~/.aa-jury-gate/` is used if neither flag nor env var is set. |
| `--version` | bool flag | — | Print `aa-jury-gate <semver>` and exit 0 |

### 1.3 Exit Code Contract

| Code | Meaning | Condition |
|------|---------|-----------|
| `0` | Gate **PASSED** | All applicable checks pass |
| `1` | Gate **FAILED** — policy violation | One or more checks FAIL; synthesis does not meet PRD-2.6 structural requirements |
| `2` | **Invocation error** | File not found, path-is-directory, permission denied, YAML parse failure, unexpected exception. **No --output write. No audit log entry.** stdout is empty on exit 2 (ENG-6.1). |

### 1.4 stdout Contract (exit 0 and exit 1)

```
aa-jury-gate check results for: <synthesis_path>
──────────────────────────────────────────────────────────
 CHECK  RESULT  DETAIL
 S01    PASS
 S02    PASS
 S03    PASS
 S04    PASS
 S05    PASS
 S06    PASS
 S07    PASS
 S08a   PASS
 S08b   PASS
 S09    PASS
 S10    PASS
 S11    FAIL    verdict is "NEEDS_REVISION"; gate requires "APPROVED"
 B01    SKIP    (S11 failed)
 B02    SKIP    (S11 failed)
 B03    SKIP    (S11 failed)
 G01    PASS
──────────────────────────────────────────────────────────
GATE: FAIL  (1 check failed)
```

**DETAIL field format (C-P3-J3-004):** On FAIL, DETAIL must include expected vs actual:

| Check | DETAIL format |
|-------|--------------|
| S05 | `schema_version is <actual>; expected 1` |
| S06 | `juror_count is <actual>; expected 5` |
| S07 | `jurors list has <actual> entries; expected 5` |
| S08a | `duplicate model: <model_string>` |
| S08b | `prohibited model: claude-haiku-4.5` |
| S09 | `rounds.r1_completed is false; expected true` |
| S10 | `rounds.r2_completed is false; expected true` |
| S11 | `verdict is "<actual>"; gate requires "APPROVED"` |
| B01 | `R1 section heading not found in body` |
| B02 | `R2 section heading not found in body` |
| B03 | `synthesis section heading not found in body` |
| G01 | `synthesis file has uncommitted changes` or `synthesis file not tracked by git` |

### 1.5 stderr Contract

| Condition | Stderr output |
|-----------|--------------|
| File not found | `Error: synthesis file not found: <path>` |
| Path is directory | `Error: synthesis path is a directory: <path>` |
| Permission denied | `Error: cannot read synthesis file: <path>` |
| YAML parse failure | `Error: synthesis file is not valid YAML: <parse_error_message>` |
| Git binary not found | `Error: git binary not found in PATH` |
| Unexpected exception | `Error: unexpected error: <exception_type>: <message>` |
| Audit log write failure | `Warning: could not write to audit log: <path>: <reason>` |
| Git check WARN (--allow-no-git) | `Warning: not a git repository; git check skipped (--allow-no-git)` |

### 1.6 --allow-no-git State Matrix (C-P3-J1-005)

| Flag set? | Is git repo? | File committed? | G01 result |
|-----------|-------------|----------------|-----------|
| No | Yes | Yes | PASS |
| No | Yes | No | FAIL (exit 1) |
| No | No | N/A | FAIL (exit 1) |
| Yes | Yes | Yes | PASS |
| Yes | Yes | No | FAIL (exit 1) — flag does not bypass git checks inside a repo |
| Yes | No | N/A | SKIP + Warning (non-fatal) |

**Note:** `--allow-no-git` only changes behaviour when the SYNTHESIS path is NOT inside any git repository. If the path IS inside a git repo, normal git checks apply unconditionally.

---

## 2. YAML Frontmatter Extraction (C-P3-J1-001, C-P3-J2-003)

> **All checks operate on the parsed frontmatter and body separately.
> The extraction algorithm MUST be specified to prevent implementor divergence.**

### 2.1 Extraction Algorithm

Synthesis files (`.md`) use YAML frontmatter delimited by `---` on its own line:

```
---
schema_version: 1
...
---
<body content>
```

**Algorithm:**
1. Read file as UTF-8 text (binary for content_sha256; text for parsing).
2. If the file begins with `---\n` (or `---\r\n`), scan for the closing `---` line.
3. The content between the opening and closing `---` lines is parsed as YAML via `yaml.safe_load()`.
4. Everything after the closing `---` line is the **body** for B01-B03 heading checks.
5. If no opening `---` found: treat entire file as body, frontmatter is empty dict → S05-S11 all FAIL.
6. If opening `---` found but no closing `---`: exit 2 (`Error: synthesis file has unclosed YAML frontmatter`).

**Body heading detection (B01-B03):**
- Operates on the body portion only (after closing `---`). Never scan frontmatter for headings.
- Uses line-anchored regex (multiline mode): `^##\s+(Round\s+1|R1)(\s|:|$)` (case-insensitive)
- B01 pattern: `^##\s+(Round\s+1|R1)(\s|:|-|$)`
- B02 pattern: `^##\s+(Round\s+2|R2)(\s|:|-|$)`
- B03 pattern: `^##\s+(Synthesis|Final|Judicial)(\s|:|-|$)`
- These patterns prevent `## R10` from matching B01 (word-boundary via `(\s|:|-|$)`)
- **Note (RC-P3-J2-009a):** `## R1.1` and `## Round 1.1` do NOT match B01 by design — `.` is absent from the trailing character class. Subsection headings are not structural section markers.

---

## 3. Validation Check Register (14 checks — ENG-6.5 4-surface model)

> **C-P3-J2-002 applied:** S08 split into S08a (model distinctness) and S08b (haiku prohibition)
> for unambiguous FAIL detail. Total checks: 14 (was 13).

### Surface 1 — Path Validation (fast-fail on FAIL → exit 2)

| ID | Check | Pass condition | Fail → exit |
|----|-------|---------------|-------------|
| **S01** | File exists and is readable | `path.exists() and path.is_file()` | 2 |
| **S02** | Extension is `.md`, `.yaml`, or `.yml` | `path.suffix in {'.md', '.yaml', '.yml'}` | 1 (policy — caller invoked CLI correctly but artifact violates the accepted-file contract) |

### Surface 2 — YAML Parse (fast-fail on FAIL → exit 2)

| ID | Check | Pass condition | Fail → exit |
|----|-------|---------------|-------------|
| **S03** | File is valid YAML (safe load) | `yaml.safe_load(content)` succeeds | 2 |
| **S04** | YAML root is a mapping | `isinstance(parsed, dict)` | 2 |

### Surface 3 — Frontmatter Schema (collected, all reported)

| ID | Check | Pass condition | Fail → exit |
|----|-------|---------------|-------------|
| **S05** | `schema_version` == 1 | `frontmatter.get('schema_version') == 1` | 1 |
| **S06** | `juror_count` == 5 | `frontmatter.get('juror_count') == 5` | 1 |
| **S07** | `jurors` list has exactly 5 entries | `len(frontmatter.get('jurors', [])) == 5` — compared against **hardcoded constant 5**, NOT against `juror_count` value (C-P3-J2-001) | 1 |
| **S08a** | All juror `model` values are distinct | All 5 model strings are unique (case-sensitive full-string equality) | 1 |
| **S08b** | No prohibited juror model | None of the model strings equals `"claude-haiku-4.5"` (exact case-sensitive match) | 1 |
| **S09** | `rounds.r1_completed` is `true` | `frontmatter.get('rounds', {}).get('r1_completed') is True` | 1 |
| **S10** | `rounds.r2_completed` is `true` | `frontmatter.get('rounds', {}).get('r2_completed') is True` | 1 |
| **S11** | `verdict` is `"APPROVED"` | `frontmatter.get('verdict') == "APPROVED"` | 1 |

**Missing-key handling (C-P3-J1-006):** If any required key is absent, the check FAILS with detail `field '<name>' is missing`. This is treated as a FAIL (exit 1), not exit 2 — the file was parsed successfully; the content doesn't meet the schema.

### Surface 4 — Body Section Checks (collected; SKIP if S11 failed)

| ID | Check | Pass condition | Fail → exit |
|----|-------|---------------|-------------|
| **B01** | R1 section heading in body | Body matches `^##\s+(Round\s+1|R1)(\s|:|-|$)` | 1 |
| **B02** | R2 section heading in body | Body matches `^##\s+(Round\s+2|R2)(\s|:|-|$)` | 1 |
| **B03** | Synthesis section heading in body | Body matches `^##\s+(Synthesis|Final|Judicial)(\s|:|-|$)` | 1 |

> **SKIP rule:** B01-B03 are SKIPPED if S11 failed (verdict != APPROVED). When verdict is not
> APPROVED, the gate fails from S11; body checks are informational only and skipping avoids
> misleading FAIL counts. A synthesis claiming verdict==APPROVED DOES have B01-B03 run.

### Git Check

| ID | Check | Pass condition | Fail → exit |
|----|-------|---------------|-------------|
| **G01** | Synthesis file committed, no uncommitted changes | `git diff --name-only HEAD -- <path>` returns no output AND `git ls-files --error-unmatch <path>` exits 0. Note: `git diff HEAD` traverses the index and covers both staged and unstaged changes relative to HEAD (empirically confirmed by J2). See §1.6 for --allow-no-git matrix. | 1 |

**Check ordering:** S01→S02→S03→S04 (fast-fail each). Then S05–S11–B01–B03–G01 (collect all, report all).

---

## 4. Security Constraints (ENG-6.1, ENG-6.5 — C-P3-J4-006)

> **Security invariants for Phase 4 threat model:**

| Constraint | Enforcement |
|-----------|-------------|
| **No symlink traversal** | Before reading SYNTHESIS: resolve path with `path.resolve()` and verify it stays within expected boundaries; refuse symlinks to targets outside the working directory tree (configurable) |
| **YAML DoS protection** | Synthesis files capped at 1 MB before YAML parsing. Files exceeding this limit fail with exit 2: `Error: synthesis file too large (max 1MB)` |
| **No YAML execute** | `yaml.safe_load()` ONLY — per AC-SEC-01 (Phase 2 §4.6). `yaml.load()` without SafeLoader is PROHIBITED. |
| **--output append atomicity** | Write to temp file **in the same directory as the target file** (e.g., `tempfile.NamedTemporaryFile(dir=target_dir, delete=False)`), then `os.replace()` (atomic on POSIX). Same-directory placement is required; cross-filesystem moves are non-atomic. Never write in-place via overwrite. |
| **--log-dir path safety** | Validate `--log-dir` using realpath normalization: (1) expand `~` via `os.path.expanduser()`, (2) resolve symlinks via `os.path.realpath()`, (3) verify resolved path does not escape the current working directory. Reject with exit 2 if validation fails. String-check for `..` is insufficient (bypassed by symlinks). |
| **No shell injection** | All git commands use `subprocess.run([...])` with list args, never shell=True. |

---

## 5. `--output append` Semantics (C-P3-J1-002, C-P3-J2-005, C-P3-J2-007)

### 5.1 What is written

The `jury_gate:` block is a YAML mapping written into the synthesis file's frontmatter:

```yaml
jury_gate:
  tool: aa-jury-gate
  version: "<semver>"
  timestamp_utc: "<ISO-8601>"
  verdict: "PASS"          # tool verdict: PASS | FAIL
  content_sha256: "<hex>"
  checks_failed: 0
  checks_skipped: 0
```

### 5.2 Idempotency / overwrite semantics

On every `--output append` invocation:
1. Parse frontmatter from SYNTHESIS (as per §2.1 algorithm).
2. Remove any existing `jury_gate:` key from the parsed frontmatter dict (prior run results discarded).
3. Add the new `jury_gate:` key with current run results.
4. Serialize updated frontmatter back to YAML; reconstruct `---\n<yaml>\n---\n<body>`.
5. Write atomically via temp file (in same directory as target) + `os.replace()`.

**Result:** Exactly one `jury_gate:` block in the output file regardless of prior runs.

**Note (RC-P3-J2-009b):** Re-serialization places `jury_gate:` at the end of the frontmatter block. Key ordering is not semantically significant but produces observable `git diff` deltas on the first and any subsequent gate run.

### 5.3 content_sha256 computation (RC-P3-J2-008)

`content_sha256` is computed on the **file bytes after stripping the `jury_gate:` frontmatter key and its entire value block**. This produces a stable content-address: re-running `aa-jury-gate` on an unchanged synthesis file yields the same `content_sha256` regardless of prior gate runs.

**Implementation note:** Strip the `jury_gate:` key via YAML parse-and-remove before hashing. The strip operation must be deterministic. The resulting hash reflects the synthesis content only, not the gate's own prior annotations.

**Operation order (RC-P3-J2-011):** Exit-2 triggers (invalid args, wrong extension, non-parseable YAML) are evaluated before `content_sha256` computation. SHA256 is only computed when the file is successfully parsed. No invocation of an exit-2 code path computes or discards a sha256.

### 5.4 Write conditions

| Exit code | --output append writes? |
|-----------|------------------------|
| 0 (PASS) | YES |
| 1 (FAIL) | YES — records the failed gate state as an audit trail |
| 2 (ERROR) | NO — no side effects on exit 2 |

**Rationale:** A gate failure is a meaningful state. Recording it in the synthesis artifact creates a durable audit trail durable in CIs where stdout/logs are ephemeral. CI pipelines requiring a clean worktree post-failure may discard the written state via `git checkout -- <synthesis_file>`.

**DETAIL column contract (RC-P3-J3-004):** The DETAIL column is informational and human-readable. Automated parsers MUST rely on the exit code, CHECK_ID, and RESULT columns only. DETAIL text format is not guaranteed stable across versions.

---

## 6. Data Model (ENG-6.4, ENG-2.1, ENG-3.5)

### 6.1 Enumerations

```python
# models.py
from enum import Enum

class CheckResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"

class GateVerdict(Enum):
    PASS = "PASS"    # all checks PASS (exit 0)
    FAIL = "FAIL"    # one or more checks FAIL (exit 1)
    ERROR = "ERROR"  # invocation/parse error (exit 2)
```

### 6.2 Dataclasses

```python
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

@dataclass
class CheckItem:
    """Result of a single validation check."""
    id: str                          # e.g. "S05", "S08a", "G01"
    result: CheckResult              # PASS | FAIL | SKIP
    detail: str | None = None        # "expected X; found Y" on FAIL; None on PASS/SKIP

@dataclass
class GitStatus:
    """Result of the git probe for a given path."""
    is_git_repo: bool
    committed: bool                  # True if file in index AND git diff HEAD shows no changes
    sha: str                         # HEAD SHA of synthesis file; empty string if not committed
    missing: bool                    # True if path absent from git index entirely (untracked)

@dataclass
class GateResult:
    """Complete result of one aa-jury-gate invocation."""
    synthesis_path: Path
    content_sha256: str              # sha256 of file bytes after stripping jury_gate: block (stable content-address)
    verdict: GateVerdict             # tool's computed verdict: PASS | FAIL | ERROR
    checks: list[CheckItem]
    git_status: GitStatus
    allow_no_git: bool
    timestamp_utc: datetime
    tool_version: str
    synthesis_verdict: str | None    # raw verdict string from synthesis frontmatter (renamed from frontmatter_verdict per C-P3-J2-006)
```

### 6.3 Data Classification (ENG-6.4)

| Field | Classification | Rationale |
|-------|---------------|-----------|
| `synthesis_path` | Internal | File path; no PII; logged in gate.log |
| `content_sha256` | Internal | Hash of synthesis content bytes (jury_gate stripped); stable content-address; tamper-evident; non-sensitive |
| `verdict` | Internal | Gate decision; logged |
| `checks[].detail` | Internal | Validation error messages; no PII |
| `git_status.sha` | Internal | Git commit SHA; non-sensitive |
| `tool_version` | Public | Semver string |
| `synthesis_verdict` | Internal | Raw verdict string from synthesis; no PII |
| All fields | **No PII** | Tool processes governance artifacts only; no user data |

### 6.4 Protocol Interface (ENG-2.5)

```python
# git_probe.py
from typing import Protocol

class GitProbe(Protocol):
    """Injectable interface for git state inspection (ENG-2.5 Dependency Inversion)."""
    def check(self, path: Path) -> GitStatus: ...
```

---

## 7. BDD Acceptance Criteria (ENG-4.4)

> **C-P3-J5-008 + C-P3-J3-001 applied:** Expanded to 20 scenarios covering all 14 checks
> plus edge cases. Each check has at least one dedicated FAIL scenario.

```gherkin
Feature: aa-jury-gate CLI validates PRD-2.6 jury synthesis structural compliance

  Background:
    Given the aa-jury-gate CLI is installed
    And a valid jury synthesis template fixture exists

  # ─── EXIT 0: GATE PASS ────────────────────────────────────────────────────

  Scenario: Valid synthesis file passes all checks
    Given a synthesis file with schema_version 1
    And the synthesis has exactly 5 jurors with distinct model strings
    And no juror model is "claude-haiku-4.5"
    And rounds.r1_completed is true and rounds.r2_completed is true
    And the verdict field is "APPROVED"
    And the body contains ## Round 1, ## Round 2, and ## Synthesis headings
    And the synthesis file is committed to git
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 0
    And stdout contains "GATE: PASS"
    And all 14 checks show PASS in the output table
    And gate.log records a PASS entry with content_sha256 and timestamp_utc

  # ─── --output append ──────────────────────────────────────────────────────

  Scenario: --output append on passing gate writes jury_gate frontmatter block
    Given a valid synthesis file that passes all checks
    When aa-jury-gate is invoked with "--output append"
    Then the exit code is 0
    And the synthesis file contains exactly one "jury_gate:" frontmatter block
    And the jury_gate block contains verdict "PASS" and content_sha256

  Scenario: --output append is idempotent on a file already containing jury_gate block
    Given a synthesis file that already contains a "jury_gate:" block from a prior run
    When aa-jury-gate is invoked again with "--output append"
    Then the exit code is 0
    And the synthesis file contains exactly one "jury_gate:" block
    And the jury_gate block contains the data from the current run, not the prior run

  Scenario: --output append on failing gate records failed state
    Given a synthesis file where the verdict is "NEEDS_REVISION"
    When aa-jury-gate is invoked with "--output append"
    Then the exit code is 1
    And the synthesis file contains a "jury_gate:" block with verdict "FAIL"

  # ─── EXIT 1: GATE FAIL — per-check scenarios ──────────────────────────────

  Scenario: Wrong file extension fails S02
    Given a synthesis file with extension ".txt"
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S02    FAIL"

  Scenario: Wrong schema_version fails S05
    Given a synthesis file where schema_version is 2
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S05    FAIL"
    And the S05 DETAIL contains "schema_version is 2; expected 1"

  Scenario: Synthesis with only 4 jurors fails S06 and S07
    Given a synthesis file with juror_count 4 and only 4 juror entries
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S06    FAIL"
    And stdout contains "S07    FAIL"

  Scenario: Synthesis with duplicate juror models fails S08a
    Given a synthesis file where two jurors share the same model string
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S08a   FAIL"
    And the S08a DETAIL contains "duplicate model:"

  Scenario: Synthesis with claude-haiku-4.5 juror model fails S08b
    Given a synthesis file where one juror model is "claude-haiku-4.5"
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S08b   FAIL"
    And the S08b DETAIL contains "prohibited model: claude-haiku-4.5"

  Scenario: Synthesis with r1_completed false fails S09
    Given a synthesis file where rounds.r1_completed is false
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S09    FAIL"

  Scenario: Synthesis with verdict NEEDS_REVISION fails S11 and skips B01-B03
    Given a synthesis file where the frontmatter verdict is "NEEDS_REVISION"
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S11    FAIL"
    And stdout contains "B01    SKIP"
    And stdout contains "B02    SKIP"
    And stdout contains "B03    SKIP"
    And stdout contains "GATE: FAIL"

  Scenario: Synthesis missing R2 body section fails B02
    Given a synthesis file with verdict APPROVED but no "## Round 2" heading in body
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "B02    FAIL"
    And the B02 DETAIL contains "R2 section heading not found in body"

  Scenario: Synthesis missing synthesis section fails B03
    Given a synthesis file with verdict APPROVED but no synthesis/final/judicial heading
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "B03    FAIL"

  Scenario: Uncommitted synthesis file fails G01
    Given a synthesis file that is modified but not yet committed
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "G01    FAIL"
    And the G01 DETAIL contains "uncommitted changes"

  # ─── EXIT 2: INVOCATION ERRORS ────────────────────────────────────────────

  Scenario: Synthesis file does not exist returns exit 2
    Given a synthesis path that does not exist
    When aa-jury-gate is invoked with that path
    Then the exit code is 2
    And stderr contains "Error: synthesis file not found:"
    And stdout is empty

  Scenario: Synthesis path is a directory returns exit 2
    Given a synthesis path that is a directory
    When aa-jury-gate is invoked with that path
    Then the exit code is 2
    And stderr contains "Error: synthesis path is a directory:"
    And stdout is empty

  Scenario: Synthesis file contains invalid YAML returns exit 2
    Given a synthesis file containing invalid YAML content
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 2
    And stderr contains "Error: synthesis file is not valid YAML:"
    And stdout is empty

  # ─── --allow-no-git ───────────────────────────────────────────────────────

  Scenario: Non-git repo without --allow-no-git fails G01
    Given the synthesis file is not inside a git repository
    When aa-jury-gate is invoked WITHOUT "--allow-no-git"
    Then the exit code is 1
    And stdout contains "G01    FAIL"

  Scenario: Non-git repo with --allow-no-git downgrades to warning
    Given the synthesis file is not inside a git repository
    And all other checks pass
    When aa-jury-gate is invoked WITH "--allow-no-git"
    Then the exit code is 0
    And stderr contains "Warning: not a git repository; git check skipped"
    And G01 shows SKIP in the output table

  # ─── AUDIT LOG ────────────────────────────────────────────────────────────

  Scenario: Audit log write failure is non-fatal
    Given the audit log directory is not writable
    When aa-jury-gate is invoked with a valid synthesis file
    Then the exit code is 0
    And stderr contains "Warning: could not write to audit log:"
    And stdout still contains "GATE: PASS"

  # ─── BDD-F01 through BDD-F06 (RC-P3-J2-010, RC-P3-J5-011, RC-P3-J3-002) ─

  Scenario: BDD-F01 — Synthesis file with schema_version field absent fails S05
    Given a synthesis file where the schema_version key is entirely absent
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S05    FAIL"
    And the S05 DETAIL contains "field 'schema_version' is missing"

  Scenario: BDD-F02 — Synthesis with invalid juror model string fails S05
    Given a synthesis file where a juror model string is "not-a-real-model"
    And the schema_version is 1 and all other structural fields are valid
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S05    PASS"

  Scenario: BDD-F03 — Synthesis with claude-haiku-4.5 juror fails S08b
    Given a synthesis file where one juror model is exactly "claude-haiku-4.5"
    And all other checks would pass
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "S08b   FAIL"
    And the S08b DETAIL contains "prohibited model: claude-haiku-4.5"

  Scenario: BDD-F04 — Synthesis missing judicial synthesis body section fails B03
    Given a synthesis file with verdict "APPROVED"
    And the body contains R1 and R2 section headings
    But the body does not contain any heading matching "Synthesis", "Final", or "Judicial"
    When aa-jury-gate is invoked with the synthesis path
    Then the exit code is 1
    And stdout contains "B03    FAIL"
    And the B03 DETAIL contains "synthesis section heading not found in body"

  Scenario: BDD-F05 — Exit 2 with --output append supplied does not write file
    Given a synthesis path that does not exist
    And aa-jury-gate is invoked with "--output append"
    When the invocation completes
    Then the exit code is 2
    And no file is created or modified at the synthesis path
    And no jury_gate block is written anywhere

  Scenario: BDD-F06 — --allow-no-git inside a git repo still requires G01 checks
    Given a synthesis file that is inside a git repository but has uncommitted changes
    When aa-jury-gate is invoked WITH "--allow-no-git"
    Then the exit code is 1
    And stdout contains "G01    FAIL"
    And the G01 DETAIL contains "uncommitted changes"
```

---

## 8. Validation Input Schema Reference (PRD-2.6, ENG-11.1)

> **Primary schema source:** `hangar-ai-specs/templates/jury-synthesis-template.md`

### 8.1 Required Frontmatter Fields Validated by aa-jury-gate

| Field | Type | Check | Validation |
|-------|------|-------|-----------|
| `schema_version` | integer | S05 | must equal `1` |
| `juror_count` | integer | S06 | must equal `5` |
| `jurors` | list | S07 | must have exactly 5 items |
| `jurors[].model` | string | S08a | all 5 distinct (case-sensitive) |
| `jurors[].model` | string | S08b | none equals `"claude-haiku-4.5"` |
| `rounds.r1_completed` | boolean | S09 | must be `true` |
| `rounds.r2_completed` | boolean | S10 | must be `true` |
| `verdict` | string | S11 | must equal `"APPROVED"` |

### 8.2 Schema Version Forward-Compatibility

- `schema_version` != 1 → fail closed (S05 FAIL, exit 1)
- Unknown fields → ignored (schema is open for extension)
- Missing required field → check FAIL with `field '<name>' is missing`

---

## 9. Audit Log Contract (ENG-6.7, ENG-10.1, BUS-7.1)

**Location:** `~/.aa-jury-gate/gate.log` (default) or `AA_JURY_GATE_LOG_DIR/gate.log` or `--log-dir/gate.log`.

**Format:** JSON-Lines (one JSON object per line). Append-only. Never truncated.

```json
{
  "tool": "aa-jury-gate",
  "version": "1.0.0",
  "timestamp_utc": "2026-05-26T01:00:00Z",
  "synthesis_path": "/abs/path/to/phase-2-jury-synthesis.md",
  "content_sha256": "abc123...",
  "verdict": "PASS",
  "allow_no_git": false,
  "checks_failed": 0,
  "checks_skipped": 0,
  "checks": [
    {"id": "S01", "result": "PASS", "detail": null},
    {"id": "S08a", "result": "FAIL", "detail": "duplicate model: claude-sonnet-4.6"}
  ]
}
```

**Write semantics:** content_sha256 computed BEFORE `--output append` write (after stripping any prior jury_gate block). Audit log NOT written on exit 2. Log directory created automatically; creation failure is a Warning (non-fatal).

---

## 10. Phase 3 Summary

| Contract element | Section | Status |
|-----------------|---------|--------|
| CLI surface (command, args, flags) | §1.1–1.2 | Defined |
| Exit code contract (0/1/2) | §1.3 | Defined |
| stdout table format + DETAIL spec | §1.4 | Defined |
| stderr error/warning messages | §1.5 | Defined |
| --allow-no-git state matrix | §1.6 | Defined |
| YAML frontmatter extraction algorithm | §2 | Defined |
| 14 validation checks (4 surfaces) | §3 | Defined |
| Security constraints | §4 | Defined |
| --output append semantics + atomicity | §5 | Defined |
| Data model (enums + dataclasses) | §6.1–6.3 | Defined |
| GitProbe Protocol | §6.4 | Defined |
| BDD Gherkin scenarios (26 scenarios) | §7 | Defined |
| Input schema reference (jury template) | §8 | Defined |
| Audit log schema (JSON-Lines) | §9 | Defined |
| Out of scope for v1 | §11 | Defined |

---

## 11. Out of Scope for v1 (RC-P3-J3-005)

The following features are explicitly NOT in v1 scope per PRD-5.1. They are deferred to v2 or later:

| Feature | Deferral reason |
|---------|----------------|
| `--dry-run` flag | Requires design; no implementation surface in v1 |
| JSON stdout format (`--format json`) | v1.1 polish; DETAIL format is intentionally informational only |
| Alternate failure-write modes (e.g., `--append-fail-state`) | v2 feature; current write-on-exit-1 is the correct default |
| Synthesizer model distinctness validation | PRD-2.6 v2 hardening; synthesizer identity not a required template field in v1 |
| Configurable symlink-boundary policy | v2 security; v1 uses cwd-boundary refusal |

---
phase: 3
title: "Define — Law Citation Auditor"
project: citation-auditor-2026-001
workflow: greenfield-development
version: v1.1.0
status: APPROVED
approved_by: claude-opus-4.5
approved_at: 2026-05-23
author: Hangar AI (claude-sonnet-4.6)
date: 2026-05-23
law_citations: [PRD-2.6, ENG-1.5, ENG-2.1, ENG-2.2, ENG-3.4, ENG-3.5, ENG-3.6, ENG-3.7, ENG-4.4, ENG-5.2, ENG-6.1, ENG-6.4, ENG-6.5, ENG-6.7, ENG-10.2, ENG-11.1, ENG-13.1, ENG-13.2, BUS-7.1]
preceding_phase_approved: phase-2-discover.md v1.1.0 (APPROVED claude-opus-4.5 2026-05-23)
r1_corrections: 16
r2_corrections: 5
---

# Phase 3 — Define: Law Citation Auditor

**Jury focus (greenfield-development.md §Per-Phase Jury Focus):**
"Contract completeness; data model correctness; BDD coverage of edge cases"

---

## 1. CLI Contract (ENG-1.5)

ENG-1.5 (API-First Design Law) requires the interface contract to be defined and approved
before any implementation begins. This section IS that contract.

### 1.1 Command Signature

```
aa-citation-audit <artifact> [OPTIONS]
```

| Argument / Flag | Type | Required | Default | Semantics |
|----------------|------|---------|---------|-----------|
| `<artifact>` | path | ✅ Yes | — | Path to markdown artifact to scan. Must exist, be readable, end in `.md`. |
| `--laws-dir <path>` | path | ❌ No | `laws/` relative to CWD | Directory containing `index.yaml`. Tool exits 2 if `index.yaml` not found. |
| `--allow-draft <ids>` | comma-separated string | ❌ No | `""` (empty) | Comma-separated law IDs to treat as draft (skip FAIL check). Each ID must match `[A-Z]+-\d+\.\d+`. Invalid format → exit 2. |
| `--strict` | flag | ❌ No | `false` | Exit 1 if any WARN exists (does NOT upgrade Verdict values — WARNs remain WARN in results/YAML). |
| `--output <mode>` | enum | ❌ No | `stdout` | `stdout` = print summary table to stdout; `append` = write `citation_audit` block to artifact frontmatter; `console` = human-readable rich table. |
| `--help` | flag | ❌ No | — | Print usage and exit 0. |
| `--version` | flag | ❌ No | — | Print version and exit 0. |

### 1.2 Exit Codes

> C-P3-001-J1/J2/J3/J5 (BLOCKING): STATUS_MISMATCH path had zero BDD coverage — added §4.2 Scenarios 5–6.
> C-P3-002-J1 (BLOCKING): Draft ID Verdict type was undefined — defined as excluded from results list; see §2.2 note.
> C-P3-001-J4 (BLOCKING): `--strict` semantics clarified below; YAML block now includes `exit_code`.
> C-P3-002-J4/J5 (BLOCKING): Zero-citations edge case added to BDD §4.1 Scenario 7.
> C-P3-003-J4 (BLOCKING): `--output append` on no-frontmatter artifact defined in §1.4; BDD §4.5 Scenario 5 added.
> C-P3-003-J3 (BLOCKING): Input validation §3 expanded with non-.md, laws-dir/index.yaml distinction, wrong-type law_citations.
> C-P3-004-J2: ENG-5.2 added to frontmatter law_citations (now 19 IDs).
> C-P3-003-J2: pass_count @property added to AuditResult §2.2.
> C-P3-005-J2: Timestamp format specified as YYYY-MM-DDTHH:MM:SSZ.
> C-P3-005-J4/J5-C-P3-002: context_snippet anchor defined as ±150 chars centered on match start.
> C-P3-005-J1/J5-C-P3-006: Deduplication semantics defined — one result per unique ID (not per occurrence).
> C-P3-006-J4: CI dual-change spec added to §5.
> C-P3-003-J1: Invalid --output enum added to §3 input validation.
> C-P3-001-J3 (CONTESTED): J3 claims default output should be `append` not `stdout`. Design spec §4.1 explicitly shows `aa-citation-audit <artifact.md>` (no flag) = "basic scan" with stdout table only; `--output append` is an explicit flag. J3's claim contradicts the approved design spec. Flagged for Judicial Synthesis adjudication. Default remains `stdout`.
> C-P3-006-J2: verdict ordering stability — append output sorts FAIL→WARN→PASS, same as stdout.

| Code | Meaning | When |
|------|---------|------|
| `0` | Success — zero FAILs | All citations PASS (WARNs alone do not produce exit 1 unless `--strict`) |
| `1` | Citation failure | At least one FAIL verdict; or any WARN when `--strict` is set |
| `2` | Tool execution error | Registry not found; YAML parse failure; invalid `--allow-draft` format; unreadable artifact; invalid `--output` value; write permission failure on `--output append` |

**`--strict` semantics (C-P3-001-J4):** `--strict` affects the exit code calculation only —
it does NOT change Verdict values from WARN to FAIL. WARNs remain WARNs in the results list
and YAML block; `--strict` causes `AuditResult.audit_exit_code` to return 1 when `warn_count > 0`.
The YAML block records `strict: true` so audit records are replayable under the same policy.

**Fail-closed guarantee ([PROPOSED] ENG-14.1 Req 2 / ENG-6.5):** Exit 2 is never silently swallowed
by CI. The CI integration spec (§5) requires checking `exit_code != 2` before asserting `== 0`.

### 1.3 Standard Output Schema (`--output stdout`)

Printed to `stdout`; nothing else is written to `stdout` in this mode (ENG-6.1).

```
aa-citation-audit v<version>
Artifact: <path>
Registry: <laws-dir>/index.yaml (<N> laws loaded)

ID          Verdict  Note
----------  -------  -----------------------------------------------
ENG-3.5     PASS
ENG-14.1    FAIL     ID not in registry
PRD-2.6     WARN     Title phrase "discovery stage gate" score 42 < 60

Summary: <N> citations scanned | <F> FAIL | <W> WARN | <P> PASS
Exit: <exit_code>
```

**Constraints:**
- One row per unique citation instance found in the artifact body (code blocks excluded)
- Rows sorted: FAIL first, then WARN, then PASS, then SKIP (draft IDs)
- SKIP row format: `ENG-14.1  SKIP  draft — not evaluated`
- No ANSI colour codes in `--output stdout`; ANSI permitted in `--output console`
- Empty stdout except the table above (no debug, no progress, no spinner — ENG-6.1)

### 1.4 Append Output Schema (`--output append`)

Writes (or overwrites) the `citation_audit` YAML block in the artifact's frontmatter
(ENG-6.7, ENG-10.2). If no frontmatter exists, adds one with `---\n...\n---` delimiters
before the first line of the file. Prints the same table as `--output stdout` plus a
trailing `[written: citation_audit block]` line. (C-P3-003-J4)

**No-frontmatter insertion:** If the artifact has no `---` frontmatter block, prepend:
```
---
citation_audit:
  ...
---

```
before the existing content. The existing content is not modified.

```yaml
citation_audit:
  tool: aa-citation-audit
  version: "<semver>"
  timestamp: "YYYY-MM-DDTHH:MM:SSZ"   # e.g. "2026-05-23T14:32:01Z" (C-P3-005-J2)
  registry: "<resolved absolute path to index.yaml>"
  law_count: <N>
  scanned: <N>          # unique IDs found (excludes draft_skipped)
  draft_skipped: ["ENG-14.1", "ENG-14.2"]   # empty list if none
  fail_count: <N>
  warn_count: <N>
  pass_count: <N>
  exit_code: <0|1>      # audit_exit_code value at time of run (C-P3-001-J4)
  allow_draft: ["ENG-14.1", "ENG-14.2"]
  strict: false
  verdicts:             # sorted: FAIL first, then WARN, then PASS (stable ordering C-P3-006-J2)
    - id: "ENG-14.1"
      verdict: "FAIL"
      note: "ID not in registry"
      context_snippet: "...governed by ENG-14.1 (proposed) which requires..."   # FAIL entries: snippet populated (C-P3-005-J2, C-P3-007-J5)
    - id: "PRD-2.6"
      verdict: "WARN"
      note: "Title phrase score 42 < 60"
      context_snippet: "...the PRD-2.6 discovery stage gate ensures..."
    - id: "ENG-3.5"
      verdict: "PASS"
      context_snippet: null   # PASS entries: snippet is null
```

**ENG-10.2 enforcement record requirements:**
- `citation_audit` block is append-only once committed (do not remove historical runs)
- For artifact versioning: each new scan overwrites the block but the artifact commit
  history preserves all prior states (git is the retention mechanism, ≥1 year per ENG-10.2)
- Structured, immutable-per-commit, machine-readable
- `verdicts` list order is deterministic (FAIL→WARN→PASS, then alphabetical within tier)
  to ensure stable git diffs across repeated runs (C-P3-006-J2)

---

## 2. Data Model (ENG-6.4 — Classification)

### 2.1 Registry Data Structures

```python
@dataclass(frozen=True)
class RegistryEntry:
    law_id: str           # e.g. "ENG-3.5"
    title: str            # canonical title from law file
    summary: str          # one-line summary
    non_negotiable: bool  # True if in index.yaml non_negotiable section
    domain: str           # "engineering" | "product" | "business"
```

**Classification (ENG-6.4):**
- `law_id`: non-PII identifier, system-internal key — no privacy concern
- `title` / `summary`: constitutional text, public constitution content — no PII
- `non_negotiable`: boolean derived from index.yaml registry — no PII
- No user data, no PII at any layer of the data model

### 2.2 Scan and Verdict Structures

```python
class Verdict(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    # Note: Draft IDs are NOT added to results as CitationResult entries.
    # They are tracked in AuditResult.draft_skipped (list[str]) and noted
    # in stdout as "draft — not evaluated". This avoids polluting the
    # verdicts list with a non-verdict state. (C-P3-002-J1)

@dataclass
class CitationResult:
    law_id: str
    verdict: Verdict
    note: str | None           # human-readable reason for WARN/FAIL
    context_snippet: str | None  # ±150 chars: slice [match_start-150:match_start+150]
                                  # on the stripped body text (C-P3-005-J4/J5)

@dataclass
class AuditResult:
    artifact_path: str
    registry_path: str
    law_count: int             # total laws in registry
    scanned: int               # unique IDs found in stripped body (C-P3-005-J1/J5: per unique ID, not per occurrence)
    results: list[CitationResult]   # one entry per unique law_id (deduplication: first-occurrence wins)
    draft_skipped: list[str]   # IDs skipped due to --allow-draft (C-P3-002-J1)
    allow_draft: list[str]
    strict: bool
    timestamp: str             # Format: YYYY-MM-DDTHH:MM:SSZ (C-P3-005-J2)
    tool_version: str

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == Verdict.FAIL)

    @property
    def warn_count(self) -> int:
        return sum(1 for r in self.results if r.verdict == Verdict.WARN)

    @property
    def pass_count(self) -> int:  # C-P3-003-J2
        return sum(1 for r in self.results if r.verdict == Verdict.PASS)

    @property
    def audit_exit_code(self) -> int:
        # C-P3-002-J2: renamed from exit_code to audit_exit_code to clarify
        # this returns 0|1 only. Exit 2 is cli.py's responsibility (raised
        # before AuditResult is instantiated, during input validation).
        if self.fail_count > 0:
            return 1
        if self.strict and self.warn_count > 0:
            return 1
        return 0
```

**Deduplication semantics (C-P3-005-J1/J5):** When the same law ID appears multiple times
in the artifact body (outside code blocks), only one `CitationResult` is recorded — the
first occurrence is used for `context_snippet`. The `scanned` count reflects unique IDs
found, not total occurrences.

### 2.3 Four-Layer Architecture Binding (ENG-2.2)

| Layer | Module | Responsibility | ENG-3.4 SRP |
|-------|--------|---------------|-------------|
| Infrastructure | `registry.py` | Load/parse index.yaml → `dict[str, RegistryEntry]` | Registry I/O only |
| Application | `scanner.py` | Strip code blocks → extract `(law_id, context)` tuples | Extraction only, no verdicts |
| Domain | `auditor.py` | Apply L1/L2 verdict logic → `AuditResult` | Verdict logic only, no I/O |
| Presentation | `cli.py` | Wire args → invoke stack → emit output → sys.exit | I/O + exit only |

---

## 3. Input Validation Contract (ENG-6.5)

All four surfaces identified in Phase 2 §2.4 must be validated **before** registry load
or body scan begins. Any validation failure → `exit 2` with a structured error message.

> C-P3-003-J3/J4: Expanded with non-.md check, laws-dir vs index.yaml missing distinction,
> wrong-type law_citations, invalid --output enum, and write permission failure.

| Surface | Validation Rule | Error Message Template |
|---------|----------------|----------------------|
| 1 — Artifact file path | File exists; is a regular file (not dir); is readable; path ends in `.md` | `[ERROR] Artifact not found or unreadable: {path}` / `[ERROR] Artifact must be a .md file: {path}` |
| 2 — Law registry YAML | `{laws_dir}/` directory exists; `{laws_dir}/index.yaml` file exists; loads without YAML error; `law_ids` key is a dict of lists; all entries match `[A-Z]+-\d+\.\d+` | `[ERROR] Registry directory not found: {laws_dir}` / `[ERROR] Registry file not found: {laws_dir}/index.yaml` / `[ERROR] Registry load failed: {reason}` |
| 3 — `--allow-draft` values | Each comma-separated value matches `[A-Z]+-\d+\.\d+` | `[ERROR] Invalid --allow-draft ID: {value}` |
| 4 — Artifact frontmatter YAML | If YAML front-matter block present: must parse without error; `law_citations` if present must be a list of strings (not scalar or dict) | `[ERROR] Artifact frontmatter parse failed: {reason}` / `[ERROR] law_citations must be a list of strings` |
| — `--output` enum | Value must be one of `stdout`, `append`, `console` | `[ERROR] Invalid --output value: {value}. Must be stdout, append, or console` |
| — `--output append` write permission | Artifact file must be writable | `[ERROR] Artifact is not writable: {path}` |

**Important:** Validation errors are written to `stderr` only. `stdout` remains clean
(ENG-6.1). Exit 2 on any validation failure. Nothing is written to the artifact on exit 2.

---

## 4. BDD Acceptance Criteria (ENG-4.4)

All scenarios use Gherkin syntax. These ARE the acceptance tests — Phase 6 TDD cycles
MUST produce passing implementations for every scenario below.

### 4.1 L1 — Registry ID Validation (Core)

```gherkin
Feature: L1 Law Citation Registry Validation

  Background:
    Given the law registry at "laws/index.yaml" is loaded
    And the registry contains law IDs including "ENG-3.5", "PRD-2.6", "BUS-7.1"
    And the registry does NOT contain "ENG-99.9" or "PRD-0.0"

  Scenario: Valid citation passes
    Given an artifact containing "This implements ENG-3.5 naming conventions"
    When aa-citation-audit runs on the artifact
    Then the ENG-3.5 result verdict is "PASS"
    And the exit code is 0

  Scenario: Hallucinated ID produces FAIL and exit 1
    Given an artifact containing "Governed by ENG-99.9 (Fictional Law)"
    When aa-citation-audit runs on the artifact
    Then the ENG-99.9 result verdict is "FAIL"
    And the note contains "ID not in registry"
    And the exit code is 1

  Scenario: Multiple citations — one FAIL, rest PASS → exit 1
    Given an artifact containing both "ENG-3.5" and "ENG-99.9"
    When aa-citation-audit runs on the artifact
    Then the ENG-3.5 verdict is "PASS"
    And the ENG-99.9 verdict is "FAIL"
    And the exit code is 1

  Scenario: All citations valid → exit 0
    Given an artifact containing only "ENG-3.5" and "PRD-2.6"
    When aa-citation-audit runs on the artifact
    Then all verdicts are "PASS"
    And the exit code is 0

  Scenario: Draft ID excluded from FAIL check
    Given an artifact containing "ENG-14.1 (proposed)"
    And the flag --allow-draft ENG-14.1 is set
    When aa-citation-audit runs on the artifact
    Then ENG-14.1 does NOT appear in the results list
    And AuditResult.draft_skipped contains "ENG-14.1"
    And stdout contains "ENG-14.1  SKIP  draft — not evaluated"
    And the exit code is 0

  Scenario: --allow-draft ID set but does not appear in artifact body
    Given the flag --allow-draft ENG-14.1 is set
    And the artifact body contains no mention of ENG-14.1
    When aa-citation-audit runs on the artifact
    Then ENG-14.1 does NOT appear in results or draft_skipped
    And the exit code is 0

  Scenario: ENG-12.1 passes after Phase 0 fix
    Given an artifact containing "ENG-12.1"
    And the registry contains ENG-12.1 (confirmed by Phase 0 fix commit ab44374)
    When aa-citation-audit runs on the artifact
    Then the ENG-12.1 verdict is "PASS"
    And the exit code is 0

  Scenario: Artifact with zero law citations
    Given an artifact containing no text matching [A-Z]+-\d+\.\d+
    When aa-citation-audit runs on the artifact
    Then AuditResult.scanned equals 0
    And AuditResult.results is empty
    And stdout contains "0 citations scanned | 0 FAIL | 0 WARN | 0 PASS"
    And the exit code is 0

  Scenario: Same law ID appears multiple times in body — deduplicated
    Given an artifact containing "ENG-3.5" on line 5 and "ENG-3.5" on line 20
    When aa-citation-audit runs on the artifact
    Then AuditResult.scanned equals 1
    And exactly one CitationResult for ENG-3.5 exists (first occurrence wins)
    And the exit code is 0
```

### 4.2 L1 — Title Mismatch and Status Mismatch (WARN)

```gherkin
Feature: L1 Title Mismatch Warning

  Scenario: Explicit title phrase with score < 60 produces WARN
    Given an artifact containing "ENG-10.1 (Amendment Process Law)"
    And the registry title for ENG-10.1 is "Constitution Metrics Collection Law"
    And rapidfuzz partial_ratio("amendment process law", "constitution metrics collection law") < 60
    When aa-citation-audit runs on the artifact
    Then the ENG-10.1 verdict is "WARN"
    And the note contains "Title phrase score"
    And the exit code is 0

  Scenario: No explicit title phrase → no WARN
    Given an artifact containing "governed by ENG-10.1"
    And there is no bold or quoted text within 30 chars of ENG-10.1
    When aa-citation-audit runs on the artifact
    Then the ENG-10.1 verdict is "PASS"
    And the exit code is 0

  Scenario: Explicit title phrase with score >= 60 → PASS
    Given an artifact containing "ENG-3.5 **Naming Conventions Law**"
    And rapidfuzz partial_ratio("naming conventions law", registry_title) >= 60
    When aa-citation-audit runs on the artifact
    Then the ENG-3.5 verdict is "PASS"

  Scenario: WARN in --strict mode → exit 1
    Given an artifact with a title WARN on ENG-10.1
    And the --strict flag is set
    When aa-citation-audit runs on the artifact
    Then the exit code is 1

  Scenario: STATUS_MISMATCH — artifact asserts NON-NEGOTIABLE on a non-NON-NEG law → WARN
    Given an artifact containing "ENG-3.5 (NON-NEGOTIABLE)" within 50 chars of ENG-3.5
    And the registry marks ENG-3.5 as non_negotiable: false
    When aa-citation-audit runs on the artifact
    Then the ENG-3.5 verdict is "WARN"
    And the note contains "status mismatch"
    And the exit code is 0

  Scenario: STATUS_MISMATCH — artifact status assertion matches registry → PASS
    Given an artifact containing "BUS-7.1 (NON-NEGOTIABLE)" within 50 chars of BUS-7.1
    And the registry marks BUS-7.1 as non_negotiable: true
    When aa-citation-audit runs on the artifact
    Then the BUS-7.1 verdict is "PASS"
    And the exit code is 0

  Scenario: STATUS_MISMATCH — STRICTLY ENFORCED asserted on NON-NEG law → WARN
    Given an artifact containing "BUS-7.1 (STRICTLY ENFORCED)" within 50 chars of BUS-7.1
    And the registry marks BUS-7.1 as non_negotiable: true
    When aa-citation-audit runs on the artifact
    Then the BUS-7.1 verdict is "WARN"
    And the note contains "status mismatch"
```

### 4.3 Code Block Exclusion

```gherkin
Feature: Code Block Citation Exclusion

  Scenario: ID inside fenced code block is not evaluated
    Given an artifact with a fenced code block containing "ENG-99.9"
    And ENG-99.9 is not in the registry
    When aa-citation-audit runs on the artifact
    Then ENG-99.9 is NOT present in the results
    And the exit code is 0

  Scenario: ID inside inline code span is not evaluated
    Given an artifact containing "`ENG-99.9`" (backtick-wrapped)
    And ENG-99.9 is not in the registry
    When aa-citation-audit runs on the artifact
    Then ENG-99.9 is NOT present in the results
    And the exit code is 0

  Scenario: Same ID in code block and body → only body instance evaluated
    Given an artifact with "ENG-99.9" in a code block AND "ENG-99.9" in the body text
    When aa-citation-audit runs on the artifact
    Then exactly 1 FAIL result for ENG-99.9 exists
    And the exit code is 1

  Scenario: Multiline fenced code block stripped correctly
    Given a fenced code block spanning 10 lines containing "ENG-0.0" on line 5
    When aa-citation-audit runs on the artifact
    Then ENG-0.0 is NOT in the results
```

### 4.4 Input Validation (ENG-6.5)

```gherkin
Feature: Input Surface Validation

  Scenario: Artifact file does not exist → exit 2
    Given a path "nonexistent-artifact.md" that does not exist
    When aa-citation-audit runs with that artifact path
    Then the exit code is 2
    And stderr contains "Artifact not found or unreadable"

  Scenario: Artifact is not a .md file → exit 2
    Given a path "artifact.txt" (not a .md file)
    When aa-citation-audit runs with that path
    Then the exit code is 2
    And stderr contains "Artifact must be a .md file"

  Scenario: Registry directory missing → exit 2
    Given --laws-dir points to a directory that does not exist
    When aa-citation-audit runs
    Then the exit code is 2
    And stderr contains "Registry directory not found"

  Scenario: Registry directory exists but index.yaml missing → exit 2
    Given --laws-dir points to a directory that exists
    And that directory does NOT contain index.yaml
    When aa-citation-audit runs
    Then the exit code is 2
    And stderr contains "Registry file not found"

  Scenario: Registry YAML malformed → exit 2
    Given laws/index.yaml contains invalid YAML
    When aa-citation-audit runs
    Then the exit code is 2
    And stderr contains "Registry load failed"

  Scenario: law_citations in frontmatter is not a list → exit 2
    Given an artifact with frontmatter where law_citations is a string (not a list)
    When aa-citation-audit runs
    Then the exit code is 2
    And stderr contains "law_citations must be a list of strings"

  Scenario: Invalid --allow-draft ID format → exit 2
    Given the flag --allow-draft "not-a-law-id"
    When aa-citation-audit runs
    Then the exit code is 2
    And stderr contains "Invalid --allow-draft ID"

  Scenario: Invalid --output enum value → exit 2
    Given the flag --output "xml"
    When aa-citation-audit runs
    Then the exit code is 2
    And stderr contains "Invalid --output value"

  Scenario: --output append on read-only artifact → exit 2
    Given an artifact that is readable but not writable (chmod 444)
    And the --output append flag is set
    When aa-citation-audit runs
    Then the exit code is 2
    And stderr contains "Artifact is not writable"

  Scenario: Artifact frontmatter malformed → exit 2
    Given an artifact with a frontmatter block containing invalid YAML
    When aa-citation-audit runs
    Then the exit code is 2
    And stderr contains "Artifact frontmatter parse failed"

  Scenario: Nothing written to stdout on exit 2
    Given any condition that causes exit 2
    When aa-citation-audit runs
    Then stdout is empty
    And the error message is on stderr only
```

### 4.5 Output Modes

```gherkin
Feature: Output Mode Correctness

  Scenario: --output stdout prints table and nothing else (ENG-6.1)
    Given a clean artifact with 3 citations
    When aa-citation-audit --output stdout runs
    Then stdout contains exactly the audit table header and 3 rows and summary line
    And no other content appears on stdout
    And stderr is empty

  Scenario: --output append writes citation_audit block to frontmatter (ENG-6.7)
    Given an artifact with existing frontmatter (no citation_audit block)
    When aa-citation-audit --output append runs
    Then the artifact frontmatter contains a citation_audit YAML block
    And the block contains tool, version, timestamp, fail_count, warn_count, pass_count, exit_code
    And stdout also contains the audit table

  Scenario: --output append on artifact with no frontmatter — creates frontmatter
    Given an artifact with no YAML frontmatter block
    When aa-citation-audit --output append runs
    Then the artifact file is prepended with "---\ncitation_audit:\n  ...\n---\n"
    And the original artifact content is preserved after the new frontmatter
    And the exit code is 0

  Scenario: --output append overwrites existing citation_audit block (idempotent structure)
    Given an artifact with an existing citation_audit block (from a prior run)
    When aa-citation-audit --output append runs again with identical inputs
    Then the artifact contains exactly one citation_audit block
    And the timestamp is updated
    And the verdicts list order is identical to the previous run (FAIL→WARN→PASS, then alphabetical)

  Scenario: --output append verdict ordering is stable across runs
    Given an artifact with citations for ENG-3.5 (PASS), ENG-10.1 (WARN), ENG-99.9 (FAIL)
    When aa-citation-audit --output append runs twice
    Then both runs produce verdicts in order: ENG-99.9 FAIL, ENG-10.1 WARN, ENG-3.5 PASS
    And the git diff between the two runs contains only the timestamp field

  Scenario: --output console emits ANSI-formatted table to stdout
    Given a clean artifact
    When aa-citation-audit --output console runs
    Then stdout contains colour-formatted output
```

### 4.6 Audit Performance (ENG-8.x — not applicable; using design spec §8 metric)

```gherkin
Feature: Audit Runtime

  Scenario: Benchmark — scan completes within 60 seconds
    Given an artifact with 50 distinct law citations
    And the registry contains 200+ laws
    When aa-citation-audit runs
    Then the wall-clock time is less than 60 seconds
```

---

## 5. CI Integration Contract (ENG-5.2)

> C-P3-004-J3: Expanded with artifact discovery pattern, new/modified-artifact scope,
> and staged rollout from design spec §6. (C-P3-006-J4: dual PR change spec added.)

Phase 6 CI pipeline MUST include the following step for **every modified `.md` artifact**
in the PR diff (not just a single hardcoded path):

```yaml
# excerpt from CI pipeline (GitHub Actions or equivalent)
# Scans all .md artifacts modified in this PR against the checked-out registry.
# IMPORTANT: registry is read from the checked-out branch (not pinned to main).
# If a PR modifies both an artifact AND laws/index.yaml, the scan runs against
# the new registry — this is intentional (validate artifact against updated laws).
- name: Citation audit — all modified artifacts
  run: |
    set -e
    LAWS_DIR="laws"   # always relative to repo root, checked-out branch
    # Get list of modified/added .md files in this PR
    ARTIFACTS=$(git diff --name-only origin/main HEAD | grep '\.md$' || true)
    if [ -z "$ARTIFACTS" ]; then
      echo "No .md artifacts modified — skipping citation audit."
      exit 0
    fi
    FAILED=0
    for ARTIFACT in $ARTIFACTS; do
      echo "Auditing: $ARTIFACT"
      aa-citation-audit "$ARTIFACT" --laws-dir "$LAWS_DIR"
      EXIT=$?
      if [ $EXIT -eq 2 ]; then
        echo "TOOL ERROR on $ARTIFACT — halting CI."
        exit 2
      fi
      if [ $EXIT -ne 0 ]; then
        echo "CITATION FAIL: $ARTIFACT has hallucinated or misrepresented law IDs."
        FAILED=1
      fi
    done
    exit $FAILED
```

**Staged rollout schedule (design spec §6):**
- **Week 1:** warn-only mode — replace `exit $FAILED` with `exit 0` (non-blocking)
- **Week 2+:** enforce as above (exit $FAILED blocks merge)

**[PROPOSED] ENG-14.1 Req 8 enforcement:** Reading `fail_count` from the artifact frontmatter is
NOT acceptable CI enforcement. The tool MUST be re-executed and the exit code asserted.

---

## 6. ENG-6.7 — Citation Audit Frontmatter Requirement

Every artifact produced or modified by `aa-citation-audit --output append` MUST carry
a `citation_audit` block as defined in §1.4. This block:
- Is the structured audit record required by ENG-6.7
- Constitutes an enforcement record per ENG-10.2
- Must be machine-readable YAML (no freeform text values in structured fields)
- The `verdicts` list preserves all per-ID outcomes for retroactive inspection

---

## 7. Known Constraints and Residuals

| Constraint | Source | Notes |
|-----------|--------|-------|
| `--cov-fail-under=90` in pyproject.toml (not 80 as in design spec §4.3) | Phase 2 §2.2 ENG-4.6 note | Design spec has a known defect here; Phase 3 governs |
| Draft law exclusion: `--allow-draft ENG-14.1,ENG-14.2` required for all artifacts in this project | Phase 2 §2.4, design spec §4.1 | Until Phase 4 authors Article XIV and merges index.yaml update. ENG-14.1 is cited as [PROPOSED] in §1.2 and §5; aa-citation-audit run on this artifact requires `--allow-draft ENG-14.1` (C-P3-008-J2) |
| `avatar-python-cli` does not exist in registry | Phase 2 §1.1 | Advisory: propose as Phase 4 output |
| Title mismatch threshold: partial_ratio < 60 | Design spec §4.2 algorithm | Calibrated in Phase 6 fixture suite |

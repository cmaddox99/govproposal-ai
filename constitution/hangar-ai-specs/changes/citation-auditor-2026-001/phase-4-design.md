---
phase: 4
title: "Design — Law Citation Auditor"
project: citation-auditor-2026-001
workflow: greenfield-development
version: v1.1.0
status: APPROVED — Judicial Synthesis claude-opus-4.5 2026-05-23
judicial_synthesis:
  synthesizer: claude-opus-4.5
  verdict: APPROVED
  citations_verified: 22/22
  hallucinated_ids: 0
  j6_invoked: false
  j6_activation: "N/A — L1 tool not yet built; manual verification performed"
  unmitigated_high_threats: 0
  contested_findings_resolved: "J3 C-P4-003 BUS-7.1 RESOLVED — CI-delegation model accepted"
  conditions: none
author: Hangar AI (claude-sonnet-4.6)
date: 2026-05-23
law_citations: [PRD-2.6, ENG-1.5, ENG-2.1, ENG-2.2, ENG-2.3, ENG-3.4, ENG-3.7, ENG-4.11, ENG-6.1, ENG-6.4, ENG-6.5, ENG-6.7, ENG-6.8, ENG-10.1, ENG-10.2, ENG-10.5, ENG-11.1, ENG-11.2, ENG-12.1, ENG-13.1, ENG-13.2, BUS-7.1]
preceding_phase_approved: phase-3-define.md v1.1.0 (APPROVED claude-opus-4.5 2026-05-23)
r2_corrections:
  - C-P4-R2-001: ADR ordering fixed — ADR-004 now precedes ADR-005 (was reversed)
  - C-P4-R2-002: §4.1 step 3 clarified — scan-all-domain-files approach explicit; no direct law-ID→filename mapping
  - C-P4-R2-003: §5 BUS-7.1 tamper-evidence scoped — CI execution environment provides immutability; sha256_artifact field added to audit log; v1 limitation explicitly accepted
  - C-P4-R2-004: §5 inconsistency resolved — "no centralized metrics service" vs audit.log clarified
  - C-P4-R2-005: T-09 PyYAML depth claim corrected — PyYAML has no configurable depth limit; 10MB file-size limit is the effective DoS guard
  - C-P4-R1-001: Added ENG-4.11, ENG-12.1, ENG-10.5, ENG-6.8 to law_citations (body cited; frontmatter omitted)
  - C-P4-R1-002: ADR-001 revised to reflect DI-orchestration pattern (cli.py as host); diagram and table corrected
  - C-P4-R1-003: ADR-002 false premise removed; registry loading revised to load title/summary from law markdown files
  - C-P4-R1-004: ADR-003 added CommonMark indentation scope note and ReDoS test commitment
  - C-P4-R1-005: ADR-005 added — Python version target (3.11+)
  - C-P4-R1-006: T-01 mitigation strengthened — canonical path + symlink policy
  - C-P4-R1-007: T-06 temp file dir= constraint added (same-filesystem guarantee)
  - C-P4-R1-008: T-08 added — supply-chain compromise threat (PyYAML/rapidfuzz)
  - C-P4-R1-009: T-09 added — malicious artifact DoS threats (oversized, encoding, YAML)
  - C-P4-R1-010: §3.3 index.yaml proposed edits completed — domains.engineering.files/articles, law_counts.total
  - C-P4-R1-011: §4.1 registry loading step 3 corrected (title/summary from law files; non_negotiable from index.yaml)
  - C-P4-R1-012: §5 BUS-7.1 compliance note added; ENG-10.1 sub-requirements scoped
  - C-P4-R1-013: §6 deliverables table — added proposed/citation-integrity.md row; PRD-2.6 amendment note
  - C-P4-R1-014: §7 proposed/ deferral and Phase 8 merge rules added
  - C-P4-R1-015: §0 Problem/Solution/Success Criteria added (ENG-11.2 compliance)
---

# Phase 4 — Design: Law Citation Auditor

**Jury focus (greenfield-development.md §Per-Phase Jury Focus):**
"Architecture tradeoffs; threat model completeness; unmitigated risks"

**Constitutional gate:** No unmitigated HIGH threats.

---

## 0. Problem / Solution / Success Criteria (ENG-11.2)

### Problem

Hangar AI Constitution workflow artifacts regularly cite constitutional law IDs (e.g., `ENG-4.1`, `PRD-2.6`). There is currently no automated gate verifying these citations are valid, correctly titled, or accurately described before jury deliberation. This creates a hallucination vector: fabricated IDs can propagate through jury deliberation and into approved artifacts, causing compliance drift (confirmed incident: disc-2026-006 mobile platform discovery).

### Solution

Build `aa-citation-audit` — a Python CLI tool that:
1. Parses an artifact for law ID patterns outside code blocks
2. Validates each ID against `laws/index.yaml` (the authoritative registry)
3. Flags unregistered IDs as FAIL (blocks jury), title mismatches as WARN (activates J6)
4. Writes structured audit results as `citation_audit` frontmatter block

The tool operates as a pre-jury L1 gate (ENG-14.1) and a J6 activator (ENG-14.2).

### Success Criteria

| Criterion | Measure | Target |
|-----------|---------|--------|
| FAIL detection accuracy | % fabricated IDs caught | 100% (zero false negatives) |
| WARN precision | WARN/false-WARN ratio | ≥80% precision at Phase 7 threshold calibration |
| False PASS rate | Semantic citation missed due to code-block stripping | 0 in fixture suite |
| Exit code correctness | Correct exit code per Phase 3 BDD scenarios | 100% |
| Performance | Scan time for 500-line artifact | <2 seconds |
| BUS-7.1 audit trail | Structured scan record per invocation | 100% (frontmatter + optional log)

---

## 1. Architecture Decision Record (ADR-001)

### ADR-001: Four-Layer CLI Architecture

| Field | Value |
|-------|-------|
| ID | ADR-001 |
| Status | ACCEPTED |
| Law | ENG-2.2 (Layered Architecture), ENG-3.4 (SRP) |
| Context | `aa-citation-audit` is a pure Python CLI tool with no network I/O. All work is local filesystem + in-memory processing. |

**Decision:** Implement four distinct layers. `cli.py` acts as the **dependency injection host** — it calls all three lower modules directly, injecting dependencies downward. Each lower module is stateless and accepts dependencies as parameters (no upward calls):

```
cli.py (Presentation / DI Host)
    ├──calls──→ registry.py (load_registry) → returns dict[str, RegistryEntry]
    ├──calls──→ scanner.py  (scan_artifact, inject registry) → returns (citations, draft_skipped)
    └──calls──→ auditor.py  (audit, inject citations + registry) → returns AuditResult
```

`registry.py`, `scanner.py`, and `auditor.py` do NOT call each other. Dependency direction is enforced by parameter injection, not import-chain.

**Rationale:**

| Layer | Module | ENG-3.4 SRP | Dependency direction |
|-------|--------|------------|---------------------|
| Infrastructure | `registry.py` | Load `index.yaml` + law files; return `dict[str, RegistryEntry]` | No upward deps; called by cli.py |
| Domain | `auditor.py` | Apply L1 verdict logic; return `AuditResult` | Accepts (citations, registry) injected; no I/O |
| Application | `scanner.py` | Strip code blocks; extract `(law_id, context)` tuples | Accepts (artifact_path, registry, allow_draft) injected; extraction only |
| Presentation | `cli.py` | Parse args; orchestrate registry→scanner→auditor; format output; `sys.exit()` | DI host — calls all three modules |

**Alternatives considered:**

| Option | Rejected reason |
|--------|----------------|
| Single-module script | Fails ENG-3.4 SRP; untestable units |
| Three layers (no separate domain) | Mixes verdict logic with scanning; harder to mutation-test |
| Plugin architecture | Over-engineering for v1 single-registry use case |

**ENG-2.1 DDD lite mapping:**
- `registry.py` = anti-corruption layer (shields domain from YAML specifics)
- `auditor.py` = domain logic (pure functions; no I/O; injected dependencies)
- `scanner.py` = application service (extraction only; injected registry for draft filtering)
- `cli.py` = presentation / interface adapter + DI host (orchestrates all three)

---

### ADR-002: Registry Loading Strategy

| Field | Value |
|-------|-------|
| ID | ADR-002 |
| Status | ACCEPTED |
| Law | ENG-6.5 (input validation), ENG-3.4 (SRP) |

**Decision:** Load `index.yaml` once per invocation using PyYAML to retrieve the authoritative law ID list and non-negotiable flags. Load individual law markdown files in `laws/{domain}/{file}.md` using PyYAML frontmatter to retrieve per-law `title` and `summary`. Build an in-memory `dict[str, RegistryEntry]` keyed by law ID.

**Rationale:** `index.yaml` `law_ids` arrays are the authoritative registry for ID existence and non-negotiable status. Per-law `title` and `summary` are defined in individual law markdown files — `index.yaml` does not contain per-law metadata fields. Law markdown frontmatter is YAML-structured and stable; PyYAML parsing is reliable for these well-typed files.

**Alternative considered:** Regex parsing of law `.md` bodies for title/summary. Rejected: coupling to prose formatting adds fragility and is not machine-readable.

**Source of truth per field:**
| Field | Source |
|-------|--------|
| `id` | `index.yaml` `law_ids.{domain}` arrays |
| `non_negotiable` | `index.yaml` `non_negotiable.{domain}` lists |
| `title` | Individual law file frontmatter (`laws/{domain}/{file}.md`) |
| `summary` | Individual law file frontmatter (`laws/{domain}/{file}.md`) |

---

### ADR-003: Code Block Stripping Order

| Field | Value |
|-------|-------|
| ID | ADR-003 |
| Status | ACCEPTED |
| Law | ENG-3.7 (error handling — no false positives) |

**Decision:** Strip code blocks in two passes in this exact order:
1. Fenced blocks: `re.sub(r'\`\`\`.*?\`\`\`', '', text, flags=re.DOTALL)`
2. Inline code: `re.sub(r'\`[^\`]+\`', '', text)`

**Rationale:** DOTALL pass first prevents inline-code regex from matching inside multi-line fenced blocks. Reversing the order produces false negatives on fenced blocks containing backtick-wrapped text.

**CommonMark scope note:** CommonMark spec allows fenced code blocks with up to 3 spaces of leading indentation (e.g., inside blockquotes or list items). This stripper targets column-0 fenced blocks only. Indented fenced blocks are an accepted edge case; Phase 6 fixture `artifact_indented_fence.md` tests this boundary (ENG-12.1 fixture coverage).

**ReDoS note:** The claim "no catastrophic backtracking" for `\b(ENG|PRD|BUS)-\d+\.\d+\b` is well-founded (no nested quantifiers, no ambiguous alternation on repeated characters), but Phase 6 MUST include a `test_regex_redos.py` fixture running each pattern against a ≥10,000-char crafted string to provide an empirical regression guard (ENG-6.7).

---

### ADR-004: rapidfuzz Title Mismatch Strategy

| Field | Value |
|-------|-------|
| ID | ADR-004 |
| Status | ACCEPTED |
| Law | ENG-6.5 (validation surfaces) |

**Decision:** Use `rapidfuzz.fuzz.partial_ratio` with threshold 60 for title mismatch detection. Apply only when an explicit title phrase (quoted or `**bold**`) appears within ±30 chars of the law ID in the stripped body.

**Rationale:** `partial_ratio` handles partial string overlap better than simple Levenshtein for law titles that share common words (e.g., "Metrics Collection" vs "Metrics Enforcement"). Threshold 60 calibrated in Phase 6 fixture suite.

---

### ADR-005: Python Version Target

| Field | Value |
|-------|-------|
| ID | ADR-005 |
| Status | ACCEPTED |
| Law | ENG-2.3 (Dependency Management), ENG-6.5 (input validation) |

**Decision:** Target Python 3.11+ only.

**Rationale:** Aligns with AA's `avatarpython-fastapi` platform baseline (Python 3.11+). Python 3.11 introduces `tomllib` (stdlib), faster CPython, and `ExceptionGroup` — avoidance of 3.8/3.9 backports reduces maintenance surface. `pyproject.toml` `requires-python = ">=3.11"` enforces this gate.

**Alternatives considered:**
| Option | Rejected reason |
|--------|----------------|
| Python 3.8+ | Requires backports (`tomllib`, type hints); incompatible with AA platform baseline |
| Python 3.12+ | Too aggressive; 3.11 is already the AA baseline |

---

## 2. Security Threat Model (ENG-6.1)

### 2.1 Trust Boundary

`aa-citation-audit` runs as a local CLI tool with the invoking process's filesystem permissions. Attack surface is limited to:
- Artifact files read from disk
- `laws/index.yaml` read from disk
- Output written to disk (`--output append`) or stdout/stderr

No network I/O. No authentication surface. No user sessions.

### 2.2 OWASP-Aligned Threat Analysis

| ID | Threat | Surface | Likelihood | Impact | Mitigated? | Mitigation |
|----|--------|---------|-----------|--------|-----------|------------|
| T-01 | **Path traversal** — attacker supplies `../../etc/passwd` as artifact path | CLI arg Surface 1 | Low (local tool) | Low | ✅ Yes | ENG-6.5 Surface 1: (a) file must exist, be regular, be `.md`; (b) resolve `os.path.realpath()` before extension check — symlinks followed to canonical path; (c) canonical path must reside within the invocation CWD subtree or an explicit `--root` allow-list; (d) `.md` extension check applied post-realpath |
| T-02 | **YAML bomb** (recursive YAML anchors) — malicious `index.yaml` hangs process | Surface 2 registry load | Low (controlled repo) | Medium | ✅ Yes | PyYAML `safe_load` (no `!!python/object`); process timeout not needed at CLI scale |
| T-03 | **Regex ReDoS** — crafted artifact body causes backtracking explosion | Surface 4 body scan | Low | Medium | ✅ Yes | Patterns `\b(ENG\|PRD\|BUS)-\d+\.\d+\b` have no catastrophic backtracking; Phase 6 `test_regex_redos.py` regression fixture required (ADR-003) |
| T-04 | **Audit record injection** — crafted `--allow-draft` value injects YAML into citation_audit block | Surface 3 CLI flag | Low | Medium | ✅ Yes | ENG-6.5 Surface 3: each value must match `[A-Z]+-\d+\.\d+`; YAML serialised via PyYAML (not string template) |
| T-05 | **PII exposure via context snippets** | `--output console/append` | Low (internal tool) | Medium | ✅ Qualified | ENG-6.4: snippets only in explicit output modes; never to stdout default; ENG-6.8 scoping assumption A-P2-005 documented in Phase 2 §2.3 |
| T-06 | **Frontmatter overwrite corruption** — `--output append` writes partial block on interrupt | Surface 4 write | Low | Medium | ✅ Yes | Write to temp file with `dir=artifact_path.parent` (same-filesystem, prevents cross-device `os.replace()` failure), then `os.replace()` atomic rename; original preserved on any failure; output path symlink semantics: `os.replace()` replaces the symlink entry itself, not the resolved target — this is accepted read/write path symmetry |
| T-07 | **False PASS masking real FAILs** — code block stripper too aggressive, removes semantic citations | Body scan | Low | High | ✅ Yes | ADR-003 ordering; ENG-12.1 fixture suite in Phase 6 (`artifact_code_block_ids.md`, `artifact_indented_fence.md`); T-07 is highest impact — mitigated by dedicated fixtures + ENG-4.11 mutation ≥85% on scanner.py |
| T-08 | **Supply-chain compromise** — malicious version of PyYAML or rapidfuzz introduced via dependency update | Dependency install | Low (controlled CI) | High | ✅ Yes | Version-pinned in `pyproject.toml` (`PyYAML==6.0.*`, `rapidfuzz==3.*`); Dependabot alerts on any pin drift; SHA-pinned in CI lockfile (ENG-2.3) |
| T-09 | **Malicious artifact DoS** — oversized file (memory exhaustion), pathological frontmatter YAML, invalid byte encoding, or excessive citation match count | CLI Surface 1+4 | Low | Medium | ✅ Yes | (a) File size hard-limit 10 MB (ENG-6.5 Surface 1 pre-read check — enforces before any YAML/regex); (b) UTF-8 decode with `errors='replace'` prevents encoding crash; (c) frontmatter YAML parsed with PyYAML `safe_load` — prevents code execution; deep nesting bounded by 10 MB file-size limit (PyYAML has no configurable depth limit; size limit is the effective DoS guard); (d) citation match count capped at 1,000 per artifact (returns WARN for over-limit) |

**Constitutional gate result: ZERO unmitigated HIGH threats.** ✅

### 2.3 Residual Risk Register

| Risk | Accepted by | Rationale |
|------|------------|-----------|
| T-05 PII in snippets if operator misuses `--output console` | Phase 8 Ship human APPROVE | Scoped to explicit mode; documented assumption A-P2-005 |
| T-07 fixture coverage does not guarantee 100% stripper correctness | ENG-4.11 mutation ≥85% on scanner.py at Phase 7 | Mutation testing hardens the stripper |
| T-08 supply-chain: pinned deps drift window between Dependabot PRs | Phase 8 Ship human APPROVE | Dependabot weekly scan; risk window is hours-to-days in controlled CI |

---

## 3. Article XIV Law Authoring (ENG-11.1, ENG-11.2)

Phase 4 produces two new law files. Both are PROPOSED — not merged into index.yaml until Phase 8 human APPROVE gate (executive approval per A-P2-006).

### 3.1 `laws/engineering/citation-integrity.md` — Article XIV (proposed text)

```markdown
---
domain: engineering
article: XIV
title: Citation Integrity Laws
laws:
  - id: ENG-14.1
    title: Law Citation Audit Gate Law
    non_negotiable: true
    summary: Every artifact with law citations MUST pass aa-citation-audit before jury; ≥1 FAIL blocks jury invocation; tool unavailability halts jury (fail-closed)
  - id: ENG-14.2
    title: Jury Citation Auditor Law
    non_negotiable: false
    summary: PRD-2.6 jury panels meeting J6 activation conditions MUST include J6 Citation Auditor (gpt-4.1); elevated to NON-NEGOTIABLE if J6 detection rate >5% per 10 phases
---

# Article XIV: Citation Integrity Laws

> Govern the integrity of constitutional law citations in all Hangar AI Constitution
> workflow artifacts. These laws operate as a pre-jury gate (ENG-14.1) and a
> conditional jury-seat enhancement (ENG-14.2).

---

## ENG-14.1: Law Citation Audit Gate Law

**Law ID:** `ENG-14.1` | **Status:** NON-NEGOTIABLE

Every artifact containing law ID patterns (`[A-Z]+-\d+\.\d+` outside code blocks) MUST
pass `aa-citation-audit` before jury invocation.

### Requirements

1. **Pre-jury mandatory scan** — `aa-citation-audit <artifact.md>` before every
   jury invocation on any artifact containing law citations.
2. **Fail-closed** — If the tool is not installed or returns exit 2, jury MUST HALT.
   Silent advisory mode is prohibited.
3. **Registry source** — `laws/index.yaml` `law_ids` arrays are authoritative.
4. **Draft law exclusion** — `--allow-draft <ids>` excludes proposed-not-yet-merged
   IDs from FAIL checks. Preferred: `draft_ids` section in index.yaml.
5. **Verdict tiers:**
   - `FAIL` = ID not in registry → blocks jury
   - `WARN` = explicit title phrase in artifact contradicts registry title
   - `PASS` = all other citations
6. **FAIL blocks jury.** Re-run after correction; confirm exit 0 before proceeding.
7. **WARN passed to jury brief** — activates J6 per ENG-14.2 conditions.
8. **CI enforcement** — CI MUST re-execute `aa-citation-audit <artifact.md>` and assert
   exit code 0. Reading `fail_count` from frontmatter is NOT acceptable CI enforcement.

---

## ENG-14.2: Jury Citation Auditor Law

**Law ID:** `ENG-14.2` | **Status:** STRICTLY ENFORCED

PRD-2.6 jury panels meeting any J6 activation condition MUST include J6 Citation Auditor.

### J6 Activation Conditions (ANY triggers J6)

- L1 audit produced ≥1 WARN
- Artifact is Stage E or Stage F in product-discovery workflow
- Artifact cites ≥5 distinct law IDs in frontmatter `law_citations`

### Requirements

1. **Conditional 6th juror** — compliant 5-juror panel when no activation condition is met.
2. **Model: `gpt-4.1`** — Distinct from J1-J5 and Judicial Synthesizer. Inter-generation
   diversity (gpt-4.x vs gpt-5.x for J3/J4/J5).
3. **J6 responsibilities:** Verify cited law accuracy; detect citation omissions; detect
   status misrepresentation; flag contextual misapplication; resolve L1 WARNs.
4. **Citation-only scope** — J6 MUST NOT evaluate content claims. Non-citation J6
   findings are advisory only; carry no blocking weight.
5. **Mandatory verdict schema:**

   ```
   J6 — Citation Auditor | gpt-4.1
   Verdict: VALIDATED | QUALIFIED | CHALLENGED

   Citations audited: N
   Citations valid: N

   Citations challenged:
     - [law ID] | artifact span: "[exact quoted text]"
       Issue: ID_NOT_IN_REGISTRY | TITLE_MISMATCH | STATUS_MISREPRESENTED | CONTEXTUAL_MISAPPLICATION
       Registry says: "[actual title/summary/status]"
       Artifact says: "[what artifact claims]"

   Citation omissions detected:
     - Substance: "[quoted artifact text]"
       Applicable law: [best-match ID and title]

   L1 WARN resolution:
     - [law ID]: RESOLVED | UNRESOLVED | JUSTIFIED — [explanation]
   ```

6. **J6 CHALLENGED verdict** carries same blocking weight as content jurors (PRD-2.6 Req 10).
7. **Round 2 cross-pass** — J6 confirms Round 1 citation challenges resolved; checks for
   new citation issues introduced by corrections.
8. **Judicial Synthesizer Citation Integrity Block** (required in synthesis):

   ```
   Citation Integrity Block:
   - L1 audit status: PASS | WARN count: N
   - J6 verdict (if invoked): VALIDATED | QUALIFIED | CHALLENGED
   - Hallucinated IDs in final artifact: 0
   - Unresolved J6 CHALLENGED verdicts: 0
   ```

### Elevation Clause

If J6 CHALLENGED verdict rate exceeds 5% across any 10 consecutive discovery phases
post-deployment (measured per ENG-10.5), ENG-14.2 elevates to NON-NEGOTIABLE via the
executive approval process (index.yaml `non_negotiable` comment + human APPROVE gate).
```

### 3.2 `_domain.yaml` Article XIV Entry (proposed)

```yaml
  XIV:
    title: Citation Integrity Laws
    non_negotiable: [ENG-14.1]
    laws:
      - ENG-14.1  # Law Citation Audit Gate Law (NON-NEGOTIABLE)
      - ENG-14.2  # Jury Citation Auditor Law (STRICTLY ENFORCED)
```

### 3.3 `index.yaml` Article XIV Entry (proposed)

Under `domains.engineering.files`, append:
```yaml
      - citation-integrity.md
```

Under `domains.engineering.articles`, append:
```yaml
      - XIV: Citation Integrity Laws
```

Under `law_ids.engineering`, append after ENG-13.3:
```yaml
    - ENG-14.1  # Law Citation Audit Gate Law (NON-NEGOTIABLE — proposed 2026-05-23)
    - ENG-14.2  # Jury Citation Auditor Law (proposed 2026-05-23)
```

Under `non_negotiable.engineering`, append after ENG-13.1:
```yaml
    - ENG-14.1  # Law Citation Audit Gate Law
```

Under `law_counts`:
```yaml
  engineering: 72  # was 70
  total: 170       # was 168
```

**IMPORTANT:** These index.yaml changes are NOT applied in Phase 4. They are authored here as proposed text and applied in Phase 8 at the executive approval (human APPROVE) gate. Until then, all artifacts use `--allow-draft ENG-14.1,ENG-14.2`.

---

## 4. Module-Level Design

### 4.1 `registry.py` — Infrastructure Layer

```python
# Public interface (ENG-1.5 API-first)
def load_registry(laws_dir: Path) -> dict[str, RegistryEntry]:
    """Load laws/index.yaml and return {law_id: RegistryEntry}.
    
    Raises:
        RegistryLoadError: if index.yaml missing, malformed, or law_ids invalid
    """
```

**Internal flow:**
1. `laws_dir / "index.yaml"` → `yaml.safe_load()` (PyYAML)
2. Iterate `law_ids` dict of lists → flatten to `{id: domain}`
3. For each law ID: `non_negotiable` from `index.yaml` `non_negotiable.{domain}` lists. For `title` and `summary`: iterate ALL files listed in `domains.{domain}.files`, parse each file's YAML frontmatter `laws:` list via `yaml.safe_load()`, match on `id` field. There is no direct law-ID→filename mapping; all domain files must be scanned and matched by `id`.
4. Return `dict[str, RegistryEntry]`

**Error handling (ENG-3.7):** `RegistryLoadError` raised on any failure — caught by `cli.py` → exit 2.

### 4.2 `scanner.py` — Application Layer

```python
# Public interface
def scan_artifact(artifact_path: Path, registry: dict[str, RegistryEntry],
                  allow_draft: list[str]) -> tuple[list[tuple[str, str]], list[str]]:
    """Strip code blocks, extract (law_id, context_snippet) pairs, skip drafts.
    
    NOTE: scanner.py is extraction-only. It does NOT call auditor.py.
    registry is injected by cli.py and used only for draft-ID lookup.
    
    Returns:
        (citations, draft_skipped)
        citations: list of (law_id, context_snippet) — one per unique ID (first occurrence)
        draft_skipped: list of draft IDs found in body
    """
```

**Internal flow (ADR-003):**
1. Read artifact text (UTF-8 with `errors='replace'`; reject if >10 MB per T-09)
2. Strip fenced blocks (`re.DOTALL`)
3. Strip inline code
4. Regex `\b(ENG|PRD|BUS)-\d+\.\d+\b` — collect unique IDs with context (first-occurrence wins)
5. Separate draft vs non-draft (draft = in `allow_draft` list)

**cli.py orchestration:** `cli.py` calls `load_registry()` → `scan_artifact(registry=...)` → `audit(citations=..., registry=...)` in sequence. Scanner does not call auditor.

### 4.3 `auditor.py` — Domain Layer

```python
# Public interface
def audit(citations: list[tuple[str, str]], registry: dict[str, RegistryEntry],
          strict: bool) -> AuditResult:
    """Apply L1 verdict logic to each citation.
    
    Per citation:
      - Not in registry → FAIL
      - In registry + explicit title phrase + partial_ratio < 60 → WARN
      - In registry + status assertion contradicts registry → WARN
      - Otherwise → PASS
    """
```

**Pure function — no I/O.** Testable without filesystem. High mutation testing value (ENG-4.11).

### 4.4 `cli.py` — Presentation Layer

```python
@click.command()
@click.argument("artifact", type=click.Path(exists=False))  # validated manually per ENG-6.5
@click.option("--laws-dir", default="laws", type=click.Path())
@click.option("--allow-draft", default="", type=str)
@click.option("--strict", is_flag=True, default=False)
@click.option("--output", type=click.Choice(["stdout", "append", "console"]), default="stdout")
def main(artifact, laws_dir, allow_draft, strict, output): ...
```

**Validation order (ENG-6.5):** Surface 1 → Surface 2 → Surface 3 → Surface 4 → scan → output.
Exit 2 on any validation failure (stderr only, stdout clean per ENG-6.1).

---

## 5. ENG-10.1 Metrics Design

Per ENG-10.1 (Constitution Metrics Collection Law — NON-NEGOTIABLE), citation audit events
MUST be emitted as structured metrics. Design:

| Metric | When emitted | Fields |
|--------|-------------|--------|
| `citation_audit.scan` | Every successful scan | `artifact`, `fail_count`, `warn_count`, `pass_count`, `tool_version`, `timestamp` |
| `citation_audit.fail` | Per FAIL verdict | `artifact`, `law_id`, `reason` |
| `citation_audit.warn` | Per WARN verdict | `artifact`, `law_id`, `warn_type` (TITLE_MISMATCH / STATUS_MISMATCH) |
| `citation_audit.tool_error` | Exit 2 event | `artifact`, `error_type`, `message` |

**ENG-10.1 sub-requirements satisfied in v1:**
| Sub-requirement | Satisfied? | How |
|----------------|-----------|-----|
| Structured metrics per invocation | ✅ Yes | `citation_audit` frontmatter block (per-artifact view) + `~/.aa-citation-audit/audit.log` (persistent log) |
| Machine-readable format | ✅ Yes | YAML frontmatter + newline-delimited JSON log |
| Per-law granularity | ✅ Yes | `citation_audit.fail` / `.warn` per law ID |

**ENG-10.1 sub-requirements deferred to v2:**
| Sub-requirement | Deferred reason |
|----------------|----------------|
| Time-series queryability via centralized metrics service | Frontmatter is per-artifact; audit.log is a flat file (no query engine). v2 will add `--metrics-sink` flag for structured sink (e.g., OpenTelemetry endpoint) |
| Cross-artifact aggregation queries | Same as above |

**BUS-7.1 audit trail compliance (NON-NEGOTIABLE):** Frontmatter blocks are mutable (v1 limitation — any editor can change them). The tool's BUS-7.1 obligation is to produce a structured, durable audit record per invocation. Design:

- **v1 structured record:** Tool appends one JSON line to `~/.aa-citation-audit/audit.log` on every invocation (fields: `timestamp`, `artifact`, `fail_count`, `warn_count`, `pass_count`, `tool_version`, `sha256_artifact`). The SHA-256 hash of the artifact at scan time is included to enable post-hoc verification.
- **Tamper-evident responsibility scoping:** The local `audit.log` file itself is NOT inherently tamper-evident (a local user with write access could modify it). **BUS-7.1 immutability is delegated to the CI execution environment** — CI systems capture build logs and artifacts as immutable records. When `aa-citation-audit` runs in CI, the CI log constitutes the tamper-evident audit trail. Local developer runs are best-effort; CI runs are the compliance record.
- **≥1yr retention:** Delegated to CI artifact retention policy (configured at org level). The `audit.log` file format is stable; log rotation is the operator's responsibility.
- **v1 limitation accepted:** Phase 8 Ship human APPROVE gate must acknowledge this scoping explicitly.

**Implementation:** Metrics written to `citation_audit` frontmatter block (`--output append`) and to ENG-10.2 enforcement record. Audit log appended to `~/.aa-citation-audit/audit.log` on every invocation (created if absent; append-only).

---

## 6. Phase 4 Deliverables

| Deliverable | File | Type | Phase | Status |
|-------------|------|------|-------|--------|
| ADR-001–005 | This artifact §1 | Text in artifact | 4 | Authored |
| Security threat model (T-01–T-09) | This artifact §2 | Text in artifact | 4 | Authored; 0 unmitigated HIGH |
| Problem/Solution/Success Criteria | This artifact §0 | Text in artifact | 4 | Authored |
| Article XIV law file (proposed) | `proposed/citation-integrity.md` | **On-disk file** | 4 (text) / 8 (merge) | Written to disk |
| `laws/engineering/citation-integrity.md` merge instructions | This artifact §3.1 | Text in artifact | 8 (merge) | Proposed text — NOT yet on-disk in `laws/` |
| `_domain.yaml` XIV entry | This artifact §3.2 | Text in artifact | 8 (merge) | Proposed — NOT yet applied |
| `index.yaml` XIV entries | This artifact §3.3 | Text in artifact | 8 (merge) | Proposed — NOT yet applied |
| Module-level design (registry/scanner/auditor/cli) | This artifact §4 | Text in artifact | 4 | Authored |
| Metrics design (ENG-10.1, BUS-7.1) | This artifact §5 | Text in artifact | 4 | Authored |
| proposed/ deferral rules | This artifact §7 | Text in artifact | 4 | Authored |

> **PRD-2.6 amendment note:** Phase 5 Plan (D5) will add the J6 Citation Auditor row to `workflows/greenfield-development.md` jury composition table and the pre-jury `aa-citation-audit` step to each phase gate. This is a workflow amendment — requires human APPROVE per A-P2-006 at Phase 8.

---

## 7. proposed/ Deferral Rules and Phase 8 Merge Process

### 7.1 Rationale for Deferral

Article XIV law files are authored in Phase 4 but NOT merged into `laws/` until Phase 8 human APPROVE gate (executive approval per A-P2-006). Reasons:
1. Pre-merge, `aa-citation-audit` itself is under construction — merging governing laws before the tool exists creates an unenforceable mandate
2. Executive approval required per constitution amendment process (A-P2-006 assumption)
3. Prevents partial enforcement — all law merge + tool ship + CI integration MUST land atomically in Phase 8

### 7.2 Drift Prevention

| Rule | Owner | Enforcement |
|------|-------|------------|
| `proposed/citation-integrity.md` is the **source of truth** for Article XIV law text | Phase 4 artifact §3.1 cross-references it | Any divergence between §3.1 and `proposed/citation-integrity.md` is a Phase 8 blocking defect |
| No changes to `proposed/` without a corresponding version bump in this Phase 4 artifact | Human reviewer at Phase 8 jury | Cross-check before merge |
| `proposed/` directory MUST be deleted after Phase 8 merge | Phase 8 Ship checklist | Merge script step |

### 7.3 Phase 8 Merge Checklist

1. Copy `proposed/citation-integrity.md` → `laws/engineering/citation-integrity.md`
2. Apply `_domain.yaml` XIV entry (§3.2) to `laws/engineering/_domain.yaml`
3. Apply `index.yaml` XIV entries (§3.3): `domains.engineering.files`, `domains.engineering.articles`, `law_ids.engineering`, `non_negotiable.engineering`, `law_counts`
4. Delete `proposed/` directory
5. Run `aa-citation-audit` on all Phase 1–4 artifacts with `--allow-draft` removed — confirm 0 FAIL
6. Human APPROVE gate (executive sign-off on Article XIV)

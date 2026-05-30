---
author: Hangar AI (claude-sonnet-4.6)
citation_audit:
  allow_draft: []
  draft_skipped: []
  exit_code: 0
  fail_count: 0
  law_count: 125
  pass_count: 42
  registry: /Users/979925/Repos/governance/hangar-ai-constitution/laws/index.yaml
  scanned: 42
  strict: false
  timestamp: '2026-05-26T01:09:16Z'
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
    id: ENG-11.2
    verdict: PASS
  - context_snippet: null
    id: ENG-12.1
    verdict: PASS
  - context_snippet: null
    id: ENG-12.2
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
    id: ENG-14.2
    verdict: PASS
  - context_snippet: null
    id: ENG-2.1
    verdict: PASS
  - context_snippet: null
    id: ENG-2.2
    verdict: PASS
  - context_snippet: null
    id: ENG-2.3
    verdict: PASS
  - context_snippet: null
    id: ENG-2.5
    verdict: PASS
  - context_snippet: null
    id: ENG-3.1
    verdict: PASS
  - context_snippet: null
    id: ENG-3.4
    verdict: PASS
  - context_snippet: null
    id: ENG-3.5
    verdict: PASS
  - context_snippet: null
    id: ENG-3.6
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
    id: ENG-4.12
    verdict: PASS
  - context_snippet: null
    id: ENG-4.2
    verdict: PASS
  - context_snippet: null
    id: ENG-4.3
    verdict: PASS
  - context_snippet: null
    id: ENG-4.4
    verdict: PASS
  - context_snippet: null
    id: ENG-4.6
    verdict: PASS
  - context_snippet: null
    id: ENG-5.1
    verdict: PASS
  - context_snippet: null
    id: ENG-6.1
    verdict: PASS
  - context_snippet: null
    id: ENG-6.2
    verdict: PASS
  - context_snippet: null
    id: ENG-6.3
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
    id: ENG-6.8
    verdict: PASS
  - context_snippet: null
    id: PRD-1.2
    verdict: PASS
  - context_snippet: null
    id: PRD-2.1
    verdict: PASS
  - context_snippet: null
    id: PRD-2.2
    verdict: PASS
  - context_snippet: null
    id: PRD-2.3
    verdict: PASS
  - context_snippet: null
    id: PRD-2.5
    verdict: PASS
  - context_snippet: null
    id: PRD-2.6
    verdict: PASS
  - context_snippet: null
    id: PRD-5.1
    verdict: PASS
  version: 0.2.0
  warn_count: 0
date: 2026-05-25
law_citations:
- PRD-1.2
- PRD-2.1
- PRD-2.2
- PRD-2.3
- PRD-2.5
- PRD-2.6
- PRD-5.1
- ENG-1.5
- ENG-2.1
- ENG-2.2
- ENG-2.3
- ENG-2.5
- ENG-3.1
- ENG-3.4
- ENG-3.5
- ENG-3.6
- ENG-3.7
- ENG-4.1
- ENG-4.2
- ENG-4.3
- ENG-4.4
- ENG-4.6
- ENG-4.11
- ENG-4.12
- ENG-5.1
- ENG-6.1
- ENG-6.4
- ENG-6.5
- ENG-6.7
- ENG-10.1
- ENG-11.1
- ENG-11.2
- ENG-12.1
- ENG-12.2
- ENG-12.3
- ENG-13.1
- ENG-14.1
- ENG-14.2
- BUS-7.1
phase: 2
project: aa-jury-gate
r1_corrections: 18
status: CORRECTED-R1-R2
title: Discover — aa-jury-gate CLI
workflow: greenfield-development
---



# Phase 2 — Discover: aa-jury-gate CLI

## 1. Avatar Activation

### 1.1 Technology Avatar — Python CLI Subset

> **C-P2-J1-001 applied:** No `python-cli` avatar exists in the constitution. Activating
> `python-fastapi` and carving FastAPI-specific exclusions is misleading — it inflates the
> audit surface and misdirects reviewers. Instead, the Python language stack is used as the
> technical baseline directly, without claiming a full FastAPI avatar inheritance.

**Avatar status:** No registered technology avatar exactly fits a Python CLI tool. The Python
3.11+ language stack is used directly. The following law sets are inherited from the engineering
domain laws; FastAPI-specific laws are not in scope and require no explicit exclusion.

> **C-P2-J5-005 applied — avatar inheritance rules:**
> - **Active (full inheritance):** All engineering domain laws as listed in §2
> - **Suppressed (not applicable to CLI context):** ENG-7.x (API performance SLAs),
>   integration/gateway domain (not registered in law registry), ENG-9.x (IaC/deployment)
> - **No overrides:** CLI adds no constitution law overrides; it narrows scope by exclusion only

Stack definition (Python CLI baseline):

- Language: Python 3.11+
- CLI framework: click >= 8.1
- YAML parsing: PyYAML 6.0.*
- Testing: pytest, pytest-cov, mutmut
- Linter/formatter: ruff
- Build: hatchling
- Complexity: radon (CC per function)
- Git integration: subprocess (`git ls-files`, `git log`)

### 1.2 Product-Type Avatar Evaluation

> **C-P2-J3-003 + C-P2-J5-003 applied:** Both `internal-productivity` and no-product-avatar
> options were formally evaluated.

| Avatar | Evaluation | Verdict |
|--------|-----------|---------|
| `internal-productivity` | Applies to employee-facing tools with UX workflows, task orchestration, and human process mapping. `aa-jury-gate` is a CLI utility invoked by agents and CI pipelines; it has no UX workflow, no human task design, and no business process mapping. **Secondary stakeholder only** — internal productivity teams benefit from gate.log observability but are not primary users for v1. | **NOT PRIMARY** |
| None (constitutional governance tool) | `aa-jury-gate` operates within the constitution tooling namespace (`tools/jury-gate/`). It is a meta-governance tool — enforcing constitution compliance, not implementing a product domain. | **SELECTED** |

No product-type avatar applies as primary. Constitutional governance tools are their own category. Internal productivity teams are secondary stakeholders through the observability surface (gate.log → compliance dashboard).

---

## 2. Applicable Laws Analysis

### 2.1 NON-NEGOTIABLE Laws — Hard Constraints (13 laws)

| Law | Title | Constraint on aa-jury-gate |
|-----|-------|---------------------------|
| **PRD-2.6** | Multi-Cognition Phase Gate Jury | Every build phase must complete a 5-juror R1+R2 jury gate before human advance |
| **PRD-2.5** | Discovery Stage-Gate Law | This Phase 2 artifact must identify ALL applicable laws before Phase 3 Define begins |
| **PRD-1.2** | Problem-First Law | Validated in Phase 1 |
| **ENG-4.1** | Atomic TDD Law | RED to GREEN to REFACTOR per slice. No production code before a failing test |
| **ENG-6.1** | Security by Design Law | No network calls; no secrets; stdout clean on exit 2; only `git` subprocess |
| **ENG-6.5** | Input Validation Law | ALL inputs validated: path to YAML to frontmatter schema to body sections. This is the tool's primary function; validation of inputs is constitutionally required, not optional (see C-P2-J1-002, C-P2-J2-002, C-P2-J4-001 — unanimous convergence) |
| **ENG-6.7** | Audit Trail Law | gate.log — immutable JSON append per invocation; write failure non-fatal |
| **ENG-10.1** | Constitution Metrics Collection Law | "All systems governed by the Constitution MUST implement standardized metrics collection for law compliance, violation tracking, and adoption health." gate.log IS the metrics collection point — structured JSON with required fields (see §4 gate.log schema) |
| **ENG-11.1** | Hangar SDD Law | Spec-driven; PROPOSAL.md (Phase 5) mandatory before build |
| **ENG-12.1** | Agentic Feedback Loop Law | Human gate required before each phase advance; jury synthesis committed first |
| **ENG-13.1** | Artifact Rendering Standard | See §2.4 for scoping rule |
| **ENG-14.1** | Citation Audit Gate Law | `aa-citation-audit` must pass before each jury gate |
| **PRD-5.1** | MVP Law | **v1 positive scope:** validates jury-synthesis YAML structure (schema_version, juror roster, R1+R2 rounds, verdict field, body sections), enforces quorum rules per PRD-2.6, emits gate.log for ENG-10.1 compliance dashboards. **v1 exclusions:** model policy-file enforcement, multi-repo federation, real-time streaming, GUI, synthesis quality scoring. (C-P2-J3-001: scope boundary, not architecture style) |

> **C-P2-J1-002 note:** ENG-6.5 is elevated to NON-NEGOTIABLE in this project's context.
> The constitution marks it as enforced (not globally NON-NEGOTIABLE), but for a tool whose
> entire purpose is validation, ENG-6.5 admits no partial compliance. This elevation is a
> project-level declaration, not a constitution amendment.

### 2.2 Enforced Laws (binding but not elevated to NON-NEGOTIABLE)

| Law | Title | Constraint |
|-----|-------|-----------|
| PRD-2.1 | Problem Validation Law | Validated Phase 1 |
| PRD-2.2 | Assumption Mapping Law | See §5 — Assumption Register |
| PRD-2.3 | Jobs-to-be-Done Law | Personas framed as jobs in Phase 1; applicable for Phase 3 acceptance criteria |
| ENG-1.5 | API-First Design | CLI contract (args, flags, exit codes, stdout) defined before implementation (Phase 3) |
| ENG-2.1 | Domain-Driven Design | `validator.py` = domain; `cli.py` = presentation — must not be coupled |
| ENG-2.2 | Layered Architecture | cli.py to validator.py to models.py; no layer skip |
| ENG-2.3 | Vertical Slice Architecture | Phase 5 slices S-01 through S-07 must be independent |
| ENG-2.5 | Dependency Inversion | Git check must use injectable Protocol (see §4 architecture constraints) |
| ENG-3.1 | Complexity Limits | CC <= 10 per function via decomposition mandate (see §4) |
| ENG-3.4 | Single Responsibility | One module, one job: cli.py, validator.py, models.py, git_probe.py |
| ENG-3.5 | Naming Conventions | Snake_case; `GateResult`, `CheckResult` dataclasses |
| ENG-3.6 | Documentation Law | Module docstrings required |
| ENG-3.7 | Error Handling Law | Full error taxonomy defined in §4 |
| ENG-4.2 | Test Pyramid Law | Unit tests dominant; integration for CLI wiring; BDD for acceptance |
| ENG-4.3 | Test Quality Law | One assertion focus per test; no magic numbers |
| ENG-4.4 | Test Structure Law | Every test SHALL follow Given-When-Then / Arrange-Act-Assert (C-P2-J1-003) |
| ENG-4.6 | Coverage Requirements | pytest-cov >= 90% on `src/jury_gate/` |
| ENG-4.11 | Mutation Testing Law | mutmut >= 85% on `validator.py` |
| ENG-4.12 | Legacy Rescue Mutation Hardening | Applicable: `validator.py` is gate-enforcement code; a mutant inverting the verdict check silently passes all invalid syntheses. Mutation hardening is warranted even for new-build enforcement tools (C-P2-J2-005) |
| ENG-5.1 | Observability Law | gate.log structured JSON; stderr for warnings; stdout for human table |
| ENG-11.2 | Proposal Completeness Law | PROPOSAL.md (Phase 5) must be complete before human review |
| ENG-12.2 | Dashboard-First Development | gate.log structured JSON output directly enables future compliance dashboards (ENG-10.1); this IS standard ENG-12.2 compliance for a CLI tool (secondary stakeholder: internal-productivity via observability) |
| ENG-12.3 | External Referee Principle | aa-jury-gate implements the external referee check for PRD-2.6 **structural compliance** (validates synthesis YAML structure and quorum rules; does not independently adjudicate deliberation quality) |
| ENG-14.2 | Law Authoring Law | No new laws required |
| ENG-6.4 | Secrets Management Law | No secrets; no environment variable injection of credentials |
| BUS-7.1 | Audit Trail Law | gate.log: one JSON record per invocation; SHA-256 of synthesis recorded |

### 2.3 Not Applicable Laws (systematic scan)

> **C-P2-J5-004 applied:** Key exclusions are listed with explicit rationale per domain group
> plus individual exceptions. Full enumeration of all 125 laws is impractical; exclusion basis
> stated per group and for materially relevant individual laws.

| Law or group | Exclusion basis |
|--------------|----------------|
| ENG-6.2 (Authentication) | No auth required — CLI utility with no user sessions |
| ENG-6.3 (Authorisation) | No authz scope |
| ENG-6.8 (Privacy/PII) | No personal data; synthesis files are governance artifacts |
| ENG-7.x (Performance SLAs) | CLI tool; sub-second execution; no SLA contract |
| Integration/Gateway domain | Not registered in law registry; confirmed absent from laws/index.yaml |
| ENG-9.x (Infrastructure) | pip install; no container or IaC deployment |
| ENG-4.12 | **RE-INCLUDED** — see §2.2 above |
| BUS-1.x through BUS-6.x | Aviation regulatory, FAA, DOT, PNR, dangerous goods — not applicable to internal governance tooling |
| BUS-9.x (Breach notification) | No personal data |
| PRD-3.x, PRD-4.x, PRD-6.x | Customer-market, competitive, retention laws — internal tool |

### 2.4 ENG-13.1 Scoping Rule

> **C-P2-J1-005 + C-P2-J3-002 applied:**

ENG-13.1 (Artifact Rendering Standard) requires HTML rendering. Scoping rule for this project:

| Artifact type | Format rule |
|--------------|-------------|
| In-phase working documents (capture.md, discover.md) | `.md` acceptable — these are governance process documents, not deliverables |
| Phase gate artifacts (PROPOSAL, design, review artifacts) | **HTML required** — rendered before jury review and human APPROVE gate |
| Jury synthesis files | `.md` — synthesis is a process record, not a rendered deliverable |
| RUNBOOK.md (Phase 8) | `.md` — runbook is an operational document |

This scoping is consistent with ENG-13.1's intent (human-reviewable rendered artifacts) without requiring HTML rendering of every working document.

---

## 3. Non-Negotiable Constraint Register (13 hard constraints)

| # | Law | Hard constraint | Propagates to |
|---|-----|----------------|---------------|
| 1 | PRD-2.6 | 5-juror R1+R2 jury committed before human advance — every phase | Phases 3 through 8 |
| 2 | ENG-12.1 | Human APPROVE gate before phase advance — jury synthesis committed first | Phases 3 through 8 |
| 3 | ENG-4.1 | RED before GREEN, per slice — no exceptions | Phase 6 |
| 4 | ENG-6.1 | No network; no external process except `git`; stdout clean on exit 2 | Phase 3 (contract), Phase 6 (build) |
| 5 | ENG-6.5 | 4-surface validation in order: path to YAML parse to frontmatter schema to body sections. No surface may be skipped (C-P2-J1-002, J2-002, J4-001) | Phase 3 (contract), Phase 6 (build) |
| 6 | ENG-6.7 | Audit trail per invocation — gate.log written (write failure non-fatal) | Phase 6 |
| 7 | ENG-10.1 | gate.log must be metrics-compatible per §4 schema | Phase 3 (contract) |
| 8 | ENG-11.1 | PROPOSAL.md (Phase 5) mandatory before build | Phase 5 |
| 9 | ENG-13.1 | Gate-exit artifacts rendered as HTML (per §2.4 scoping) | Phases 3, 4, 5, 7 |
| 10 | ENG-14.1 | aa-citation-audit passes before every jury gate | Phases 3 through 8 |
| 11 | PRD-5.1 | v1 scope boundary (positive): validates synthesis YAML structure + quorum rules; emits gate.log. Exclusions: model policy-file, multi-repo, GUI, quality scoring. | Phase 3 (scope guard) |
| 12 | PRD-1.2 | Problem validated — Phase 1 complete | Complete |
| 13 | PRD-2.5 | Discovery completeness — this artifact must be jury-approved before Phase 3 | This phase |

---

## 4. Architecture Constraints from Law Discovery

### 4.0 PRD-2.6 Quorum Rule

> **RC-P2-J2-005 (Synthesizer required):** The gate-pass threshold for PRD-2.6 compliance
> must be stated at discovery level to anchor Phase 3 validation logic.

The greenfield workflow specifies a 5-juror panel. PRD-2.6 requires multi-cognition jury deliberation; the constitution does not define a specific quorum fraction. Project-level ruling (to be confirmed in Phase 3 contract):

- **Gate PASS**: judicial synthesis returns APPROVED (after R1+R2 rounds complete)
- **Gate FAIL**: any juror returns NEEDS_REVISION AND synthesizer upholds it as blocking
- **CHALLENGED verdicts**: synthesizer adjudicates; if unresolved, gate does not pass
- Minimum: all 5 jurors must complete R1 and R2 before synthesis may be invoked

Phase 3 will formalise this into a schema-level quorum field (`minimum_jurors`, `round_requirements`).

### 4.1 Module Decomposition (ENG-2.1, ENG-2.2, ENG-3.4)

```
cli.py          — DI host: orchestrates calls to validator + git_probe + audit_log
validator.py    — Pure function domain: all 13 schema/body checks
git_probe.py    — Git integration: GitProbe Protocol + RealGitProbe + GitStatus dataclass
models.py       — Data structures: GateResult, CheckResult, GateVerdict
audit_log.py    — BUS-7.1 / ENG-10.1 log writer
```

### 4.2 Git Injection Interface (ENG-2.5, ENG-4.1 — C-P2-J2-001)

```python
from typing import Protocol
from dataclasses import dataclass
from pathlib import Path

@dataclass
class GitStatus:
    committed: bool
    sha: str        # empty string if not committed
    missing: bool   # True if path absent from git index

class GitProbe(Protocol):
    def check(self, path: Path) -> GitStatus: ...
```

Production: `RealGitProbe` wraps `subprocess.run(["git", "ls-files", "--error-unmatch", path])`.
Test fixture: `FakeGitProbe(committed=True, sha="abc123", missing=False)`.
This enables ENG-4.1 RED tests without subprocess side effects.

### 4.3 Complexity Decomposition (ENG-3.1 — C-P2-J2-003)

CC <= 10 per function. **Decomposition mandate:**

- `validator.py` MUST decompose into per-check functions: one function per check (CC <= 4 each)
- The orchestrator function iterates check functions and aggregates results; it MUST NOT contain
  branching logic (target CC = 1 to 2)
- CI gate: `radon cc -n C src/jury_gate/validator.py` must return exit 0 (no violations)

### 4.4 gate.log Schema — ENG-10.1 + BUS-7.1 (C-P2-J2-004, C-P2-J4-002)

```json
{
  "tool": "aa-jury-gate",
  "version": "<semver>",
  "timestamp_utc": "<ISO-8601>",
  "spec_id": "<string or null>",
  "phase": "<int or null>",
  "synthesis_path": "<absolute path>",
  "sha256_synthesis": "<sha256 of synthesis file bytes BEFORE any --output write>",
  "verdict": "PASS | FAIL | ERROR",
  "allow_no_git": "<bool>",
  "checks": [
    {"id": "<check-id>", "result": "PASS | FAIL", "detail": "<string or null>"}
  ]
}
```

> **C-P2-J4-002:** `sha256_synthesis` is computed from the exact bytes of the synthesis file
> BEFORE any `--output append` mutation. The file is never mutated before hashing.
> The gate tool reads the file once, computes SHA-256, then performs all checks, then
> (optionally) writes the `jury_gate` frontmatter block. The SHA in gate.log reflects the
> pre-write state, making it tamper-evident.

### 4.5 Error Taxonomy (ENG-3.7 — C-P2-J4-003)

| Error class | Exit code | Stderr prefix | Example |
|-------------|-----------|---------------|---------|
| Tool invocation error | 2 | `Error:` | Path not found, git binary missing, malformed args |
| YAML parse failure | 2 | `Error:` | Synthesis file is not valid YAML |
| Policy violation | 1 | (table output) | Missing juror, verdict != APPROVED, uncommitted |
| Audit log write failure | 0 (non-fatal) | `Warning:` | `~/.aa-jury-gate/` not writable |

All subprocess exceptions caught and surfaced as exit 2 with `Error: <message>` to stderr.
stdout is clean on exit 2 (ENG-6.1).

### 4.6 YAML Safe Loading Mandate — AC-SEC-01 (ENG-6.5 — RC-P2-J5-003)

> **Synthesizer REQUIRED change:** This is a security invariant, not merely an assumption.

All YAML parsing MUST use `yaml.safe_load()` or `yaml.load(Loader=yaml.SafeLoader)`.
Direct use of `yaml.load()` without a safe loader is **PROHIBITED**.

Rationale: PyYAML's default `yaml.load()` can execute arbitrary Python code when parsing
untrusted input (CVE-2017-18342 class). Synthesis files are external inputs to the gate tool
and must be treated as untrusted. This constraint derives from ENG-6.5 (Input Validation Law)
and is a project-level hard constraint (AC-SEC-01).

Phase 6 build verification: `grep -rn "yaml\.load(" src/jury_gate/` must return 0 results
(any `yaml.load` without `Loader=yaml.SafeLoader` is a build failure).

---

## 5. Assumption Register (PRD-2.2 — C-P2-J1-004, C-P2-J3-004)

> **Correction note:** J1 and J3 cited PRD-2.3 for assumption mapping. PRD-2.3 is the
> Jobs-to-be-Done Law. The correct law is PRD-2.2 (Assumption Mapping Law).

| # | Assumption | Risk if false | Validation path |
|---|-----------|--------------|----------------|
| A-01 | Python 3.11+ is available in all target environments | Tool fails to install/run | Phase 0 env check; pyproject.toml requires-python |
| A-02 | `git` binary is available in CI environments | Git check fails; --allow-no-git required | Phase 0 env check; graceful degradation |
| A-03 | PyYAML 6.0.x has stable parsing behaviour for synthesis frontmatter | Schema validation yields inconsistent results | Pinned in pyproject.toml; tested with fixtures |
| A-04 | P4 (Template Maintainer) role exists or will be created in the AA engineering org | CI enforcement linchpin is a fictional persona | Validate during Phase 8 Ship rollout |
| A-05 | Stub synthesis cost > real jury cost (enforcement model assumption) | Tool provides false assurance | Accepted residual risk; documented in Phase 1 §7 |
| A-06 | Schema version 1 will be stable for >= 12 months | Schema changes require CLI update | Versioned schema; forward-incompatibility fails closed |
| A-07 | sha256_synthesis computed before --output append is stable across OS newline normalisations | Hash differs between Linux/macOS CI and local Windows | Binary read mode; no text normalisation |

---

## 6. Phase 2 Discovery Summary

| Item | Status |
|------|--------|
| Technology avatar | Python 3.11+ CLI baseline (no registered python-cli avatar; python-fastapi avatar NOT activated) |
| Product-type avatar | None — constitutional governance tool |
| `internal-productivity` avatar | Secondary stakeholder (gate.log observability); not primary user for v1 |
| Total laws surveyed | 125 in registry |
| Applicable laws | 39 (added ENG-6.5, ENG-4.4, PRD-2.2, PRD-2.3, ENG-4.12 vs original draft) |
| NON-NEGOTIABLE laws | 13 (ENG-6.5 elevated to NON-NEGOTIABLE for this project) |
| Architecture constraints | 7 (added git Protocol, CC decomposition, gate.log schema, error taxonomy, quorum rule §4.0, AC-SEC-01 §4.6) |
| Assumption register | 7 assumptions documented under PRD-2.2 |
| ENG-13.1 scoping | .md for process docs; HTML for gate-exit artifacts |
| Synthesizer required changes | 5 applied (R1–R5): AC-SEC-01, ENG-12.3 precision, quorum rule, positive v1 scope, internal-productivity secondary stakeholder |

---
phase: 2
title: "Discover — Law Citation Auditor"
project: citation-auditor-2026-001
workflow: greenfield-development
version: v1.1.0
status: APPROVED
approved_by: claude-opus-4.5
approved_at: 2026-05-23
author: Hangar AI (claude-sonnet-4.6)
date: 2026-05-23
law_citations: [PRD-2.1, PRD-2.2, PRD-2.3, PRD-2.6, ENG-1.5, ENG-2.1, ENG-2.2, ENG-2.3, ENG-3.1, ENG-3.4, ENG-3.5, ENG-3.6, ENG-3.7, ENG-4.1, ENG-4.2, ENG-4.3, ENG-4.4, ENG-4.6, ENG-4.7, ENG-4.8, ENG-4.11, ENG-5.2, ENG-5.4, ENG-6.1, ENG-6.4, ENG-6.5, ENG-6.6, ENG-6.7, ENG-10.1, ENG-10.2, ENG-11.1, ENG-11.3, ENG-12.1, ENG-12.2, ENG-12.3, ENG-13.1, ENG-13.2, BUS-7.1]
preceding_phase_approved: phase-1-capture.md v1.1.0 (APPROVED claude-opus-4.5 2026-05-23)
r1_corrections: 16
r2_corrections: 6
---

# Phase 2 — Discover: Law Citation Auditor

## 1. Avatar Activation

### 1.1 Selected Avatar: `avatar-python-fastapi` (Python 3.11+)

**Justification:** The `aa-citation-audit` CLI tool is a pure Python 3.11+ package.
`avatar-python-fastapi` is the authoritative Hangar AI stack specification for Python
3.11+ projects, providing pytest, ruff, mypy, radon, and pytest-cov — all directly
applicable. No closer Python CLI-specific avatar exists in the registry.

**Avatar applicability scope:** Language, testing stack, formatter, linter, type
checker, and dependency tooling apply. FastAPI/async/httpx/pydantic/SQLAlchemy
requirements do NOT apply (no web framework in scope).

> C-P2-003-J1: Avatar registry gap noted — no `avatar-python-cli` exists. This project
> uses `avatar-python-fastapi` with explicit exclusions (§1.2). A future governance
> proposal for `avatar-python-cli` is recommended as a Phase 4 advisory deliverable.

### 1.2 Avatar Stack Bindings

| Component | Applies? | Binding |
|-----------|---------|---------|
| Language: Python 3.11+ | ✅ Yes | `requires-python = ">=3.11"` |
| Testing: pytest + pytest-cov | ✅ Yes | Primary test framework |
| Formatter: ruff | ✅ Yes | Format enforcement in CI |
| Linter: ruff | ✅ Yes | Lint + docstring enforcement (ENG-3.6) |
| Type checker: mypy | ✅ Yes | Static type checking |
| Complexity: radon | ✅ Yes | ENG-3.1 complexity gate (CC ≤ 10) |
| FastAPI / uvicorn / pydantic | ❌ No | No web framework in scope |
| httpx / pytest-asyncio | ❌ No | No async/HTTP in scope |
| SQLAlchemy / MongoDB | ❌ No | No database in scope |

### 1.3 Skills Activated

| Skill | Activation Reason |
|-------|------------------|
| `skill-06-atomic-tdd` | ENG-4.1 NON-NEGOTIABLE — all slices via RED→GREEN→REFACTOR |
| `skill-07-vertical-slice-dev` | ENG-2.3 — vertical slices with dependency graph at Phase 5 |
| `skill-spec-governance` | ENG-11.1 — each phase advances the spec trail |
| `skill-sonarqube-compliance-gate` | ENG-12.1 — gate provisioned before Phase 6 |

---

## 2. Constitution Laws — Full Discovery

### 2.1 Non-Negotiable Laws (active for this project)

> C-P2-001-J1: BUS-7.1 moved from Strictly Enforced to NON-NEGOTIABLE per
> index.yaml non_negotiable.business classification.

| Law ID | Title | Why It Applies | Phase Active |
|--------|-------|---------------|-------------|
| ENG-4.1 | Atomic TDD Law | All source code via TDD cycle (RED→GREEN→REFACTOR→VERIFY→COMMIT) | 6 |
| ENG-6.1 | Security by Design Law | Default output behavior defined; console output explicit opt-in; no unintended stdout leakage | 3, 6 |
| ENG-6.4 | Data Protection Law | Law registry non-PII; context snippets written only in `--output console` mode, no personal data | 3, 6 |
| ENG-6.7 | Audit Trail Law | `citation_audit` frontmatter block written to every scanned artifact; append-only per ENG-6.7 | 3, 6 |
| ENG-10.1 | Constitution Metrics Collection Law | Citation audit events (`citation_audit.fail_count`, `jury_deliberation.j6_challenged_count`) collected as constitution compliance metrics | 4, 6 |
| ENG-11.1 | Hangar SDD Law | All implementation spec-driven; no code without preceding approved spec | 1–8 |
| ENG-12.1 | Agentic Feedback Loop Law | SonarQube Constitutional Gate must be provisioned before Phase 6 Build; human dashboard review required at each slice | 0 (provision), 6 |
| ENG-13.1 | Artifact Rendering Standard | All human-facing phase artifacts rendered as HTML before human review; PROPOSAL.md rendered at Phase 5 gate | 1–8 |
| PRD-2.6 | Multi-Cognition Phase Gate Jury Law | Every phase artifact (1–8) requires 2-round 5-juror jury + Judicial Synthesis before human review | 1–8 |
| BUS-7.1 | Audit Trail Law (Business) | Audit events: `citation_audit.fail_count`, `jury_deliberation.j6_challenged_count` for ENG-14.2 elevation tracking; immutable, structured, retained ≥ 1 year | 6 |

> C-P2-004-J1: ENG-13.1 applies to all human-facing phase artifacts (Phases 1–8),
> not just Phase 5. Phase 5 PROPOSAL.md is the most prominent instance.

### 2.2 Strictly Enforced Laws (active for this project)

> C-P2-001-J2 (BLOCKING): ENG-3.5 and ENG-3.6 added — body (§5) references them but
> they were absent from frontmatter. Self-referential citation failure: the citation
> auditor's own artifact must be citation-clean. Now corrected.
> C-P2-002-J2: ENG-10.2 added — `citation_audit` block constitutes an enforcement record.
> C-P2-004-J2: ENG-2.2 moved from §2.3 "not applicable" — the CLI implements a four-layer
> architecture (registry/scanner/auditor/cli) consistent with ENG-2.2.
> C-P2-006-J2: ENG-6.6 added — Python dependencies require pip-audit in CI.
> C-P2-001-J4: PRD-2.1 and ENG-2.1 included — both are listed as workflow laws in
> greenfield-development.md frontmatter. PRD-2.3 also listed in workflow laws; added.
> C-P2-007-J4 (BLOCKING): PRD-2.2 was in frontmatter and depended on in §3 Assumption
> Registry but missing from §2.2 table — citation without classification. Added.
> C-P2-008-J2 (BLOCKING): ENG-11.1 was in §2.1/§1.3/§4/§2.5 body but absent from
> frontmatter — corrected (now 38 IDs). ENG-11.3 in §2.5 also added to frontmatter and §2.2.

| Law ID | Title | Why It Applies | Phase Active |
|--------|-------|---------------|-------------|
| PRD-2.1 | Problem Validation Law | The problem was validated at Phase 1 Capture (evidence: Jason's report, disc-2026-008 archive, categorical harm threshold). Binding as a workflow law (greenfield-development.md laws array). | 1 (satisfied) |
| PRD-2.2 | Assumption Mapping Law | All assumptions underpinning design and scoping decisions must be documented with risk and validation hook. Governs §3 Assumption Registry in this artifact. | 2 |
| PRD-2.3 | Jobs-to-be-Done Law | Binding as a workflow law. For this project: agent-as-user (P1) job = "cite laws without hallucinating"; practitioner (P2) job = "receive verified artifacts". Satisfied at Phase 1 persona definition. | 1 (satisfied) |
| ENG-1.5 | API-First Design Law | CLI interface is a contract (`aa-citation-audit <artifact.md> [flags]`); exit codes, flags, and output schema designed before implementation | 3 |
| ENG-2.1 | Domain-Driven Design Law | Binding as a workflow law. CLI CLI pipeline maps to DDD lite: `registry.py` = anti-corruption layer; `auditor.py` = domain logic; `scanner.py` = application service; `cli.py` = presentation. Full DDD ceremony (aggregates, events) not warranted at this scale. | 3, 6 |
| ENG-2.2 | Layered Architecture Law | CLI implements four layers: infrastructure (registry.py), application (scanner.py), domain (auditor.py), presentation (cli.py). ENG-2.2 applies at CLI scale without formal DI container. | 3, 6 |
| ENG-2.3 | Vertical Slice Architecture Law | Implementation decomposed into independent vertical slices with dependency graph; required at Phase 5 | 5 |
| ENG-3.1 | Complexity Limits | Each module: `radon cc` cyclomatic complexity ≤ 10 per function | 6 |
| ENG-3.4 | Single Responsibility Principle | registry.py loads/validates; scanner.py strips + extracts; auditor.py applies verdicts; cli.py wires IO — no cross-responsibility | 3, 6 |
| ENG-3.5 | Naming Conventions Law | `snake_case` for functions/variables; `PascalCase` for classes; `UPPER_SNAKE` for constants | 6 |
| ENG-3.6 | Documentation Law | Docstrings on all public functions and classes; ruff D-rule enforcement in CI | 6 |
| ENG-3.7 | Error Handling Law | Exit codes exhaustive: 0 (no FAILs), 1 (≥1 FAIL), 2 (tool error); no silent failures | 3, 6 |
| ENG-4.2 | Test Pyramid Law | Unit: registry/scanner/auditor logic. Integration: full artifact→verdict pipeline. No inversion. | 6 |
| ENG-4.3 | Test Quality Law | Tests assert meaningful outcomes; fixture artifacts represent realistic constitution documents | 6 |
| ENG-4.4 | Test Structure Law | BDD acceptance criteria (Gherkin) for all critical paths at Phase 3 | 3 |
| ENG-4.6 | Coverage Requirements | SonarQube gate: `new_coverage` ≥ 90% per slice; `--cov-fail-under=90` in pyproject.toml (design spec §4.3 requires correction from 80%) | 6 |
| ENG-4.7 | Test Isolation Law | Each test uses fixture artifacts; no shared mutable state; no filesystem side effects outside tmp dirs | 6 |
| ENG-4.8 | Mock Boundaries Law | Mock only at I/O boundaries (file reads, yaml loads); never mock internal auditor/scanner logic | 6 |
| ENG-4.11 | Mutation Testing Law | Mutation score ≥ 70% per slice; ≥ 85% on critical paths (registry loader, FAIL verdict logic) at Phase 7; `mutmut` or `cosmic-ray` | 6, 7 |
| ENG-5.2 | CI/CD Pipeline Law | CI: ruff check + mypy + pytest + pip-audit + `aa-citation-audit` re-execution on modified artifacts | 6, 8 |
| ENG-5.4 | Git Workflow Law | Conventional commits per TDD cycle per slice | 6 |
| ENG-6.5 | Input Validation Law | Four input surfaces must be validated (see §2.4): (1) artifact file path, (2) law registry YAML, (3) `--allow-draft` flag values, (4) artifact frontmatter YAML structure | 3, 6 |
| ENG-6.6 | Vulnerability Management Law | `pip-audit` in CI; no critical CVEs in `pyproject.toml` dependencies at merge | 6 |
| ENG-10.2 | Enforcement Tracking Law | `citation_audit` frontmatter block IS an enforcement record per ENG-10.2; must be structured, immutable, append-only, retained ≥ 1 year | 3, 6 |
| ENG-12.2 | Dashboard-First Development Law | SonarQube dashboard open during Phase 6; each slice scan visible before advancing | 6 |
| ENG-12.3 | External Referee Law | SonarQube is compliance referee; agent cannot self-certify | 6, 7 |
| ENG-11.3 | Spec Freshness Law | D5 workflow amendments must not go stale — amended workflows must remain consistent with the CLI implementation and each other. Governs D5 (7 workflow files) at Phase 5 and Phase 8 archive. | 5, 8 |
| ENG-13.2 | Citation Transparency Law | All phase artifacts in this project must include complete `law_citations` frontmatter | 1–8 |

### 2.3 Laws Assessed as Not Applicable

> C-P2-002-J1: All NON-NEGOTIABLE laws from index.yaml explicitly accounted for below.
> C-P2-005-J2: PRD-2.5 inapplicability formally stated.

| Law ID | Title | Rationale for Exclusion |
|--------|-------|------------------------|
| PRD-2.5 | Discovery Stage-Gate Law (NON-NEGOTIABLE) | PRD-2.5 governs product-market evidence gates for customer-facing feature discovery — sequential stage progression with filed evidence in hangar-ai-specs/. This project is a greenfield internal tooling build governed by the greenfield-development workflow's Phase 1–8 gates, not PRD-2.5 discovery stages. No PRD-2.5 override required; its scope does not extend to internal engineering tooling builds. |
| PRD-1.2 | Problem-First Law (NON-NEGOTIABLE) | Governs product discovery sequencing — problem before solution. Phase 1 Capture satisfied this intent by validating the citation hallucination problem before design. Not a recurring per-phase gate for engineering builds. |
| PRD-1.5 | Evidence-Based Decision Law (NON-NEGOTIABLE) | Governs product decisions requiring evidence. Design decisions in this greenfield are governed by PRD-2.6 jury gates, which subsume the evidence-based review requirement. |
| PRD-5.1 | MVP Law (NON-NEGOTIABLE) | Governs customer-facing product scope minimization. Internal constitution tooling does not have an "MVP" in the customer-facing sense; v1 scope is explicitly defined in §1.1 of Phase 1 Capture. |
| PRD-6.2 | Retention Over Acquisition Law (NON-NEGOTIABLE) | Customer retention metric law. Not applicable to internal tooling. |
| BUS-1.1 | Priority Hierarchy Law (NON-NEGOTIABLE) | Legal > Safety > Regulatory > Constitution. Implicitly active at all times; no specific manifestation required in this tooling project. |
| ENG-4.12 | Legacy Rescue Mutation Hardening Law (NON-NEGOTIABLE) | Not a legacy rescue project. |
| ENG-2.4 | Bounded Context Law | DDD bounded contexts not applicable at CLI tool scale. |
| ENG-2.5 | Dependency Inversion Law | CLI tool uses direct imports; formal DI interfaces add overhead at this scale. |
| ENG-6.2 | Authentication Law | No authentication surface — local filesystem tool, no user sessions. |
| ENG-6.3 | Authorization Law | No authorization surface — runs with invoking process permissions. |
| ENG-6.8 | Privacy Law | No PII stored; context snippets (±150 chars) written only in explicit `--output console` mode and scoped to artifact under review. If future versions accept network sources, ENG-6.8 must be re-evaluated. |
| ENG-7.1–7.8 | Resiliency Laws | No distributed system, no network I/O, no circuit-breaking. ENG-3.7 covers fail-closed exit codes. |
| PRD-2.4 | Competitive Analysis Law | No competitive market context applicable to internal tooling. |
| PRD-3.x–8.x | Journey/Roadmap/Metrics/Stakeholder Laws | Product lifecycle laws outside engineering internal tooling scope. |

### 2.4 ENG-6.5 Input Validation Surfaces

> C-P2-003-J2: Expanded from single surface (file path) to all four input surfaces.

All four surfaces MUST be validated before processing (exit 2 on validation failure):

| Surface | Input | Validation Required |
|---------|-------|-------------------|
| 1 | Artifact file path | File exists, is readable, is a text file |
| 2 | Law registry YAML | `laws/index.yaml` loads without error; `law_ids` key exists and is a dict of lists; all entries are strings matching `[A-Z]+-\d+\.\d+` |
| 3 | `--allow-draft` values | Each value matches `[A-Z]+-\d+\.\d+` pattern; reject arbitrary strings to prevent audit record injection |
| 4 | Artifact frontmatter YAML | If YAML block present, must be parseable; `law_citations` if present must be a list of strings; malformed frontmatter → exit 2 with structured error |

### 2.5 Deliverable-Level Law Applicability Split

> C-P2-002-J5: D1 (CLI tool) and D5 (workflow amendments) have distinct law surfaces.

| Deliverable | Primary Governing Laws |
|-------------|----------------------|
| D1 — `tools/citation-auditor/` Python CLI | ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.5, ENG-6.6, ENG-6.7, ENG-3.x, ENG-4.x, ENG-12.x, PRD-2.6 (per-slice jury) |
| D2–D4 — Law files + index.yaml updates | ENG-11.1 (SDD), ENG-10.1 (metrics), BUS-7.1 (audit trail), ENG-13.1 (rendered as HTML) |
| D5 — 7 workflow file amendments | PRD-2.6 (jury gate addition), ENG-13.1 (rendering), ENG-13.2 (citation transparency), ENG-11.3 (spec freshness — amended workflows must not go stale) |
| D6 — PROPOSAL.md (HTML) | ENG-11.1, ENG-13.1 (HTML render gate), PRD-2.6 (jury gate before human APPROVE) |
| D7 — Integration tests | ENG-4.1, ENG-4.6, ENG-4.11, ENG-12.3 (SonarQube referee) |
| D8 — Archive | ENG-11.1 (archive = ENG-11.1 requirement), BUS-7.1 (audit trail preserved) |

---

## 3. Assumption Registry

> C-P2-001-J5: PRD-2.2 (Assumption Mapping Law) requires all assumptions documented
> and tested systematically.

| ID | Assumption | Risk if Wrong | Test / Validation |
|----|-----------|--------------|------------------|
| A-P2-001 | `avatar-python-fastapi` is the best available avatar for a pure Python CLI tool | Wrong avatar specializations applied; wasted rework | Verified: no `avatar-python-cli` in registry; FastAPI avatar stack is Python-idiomatic. Accept. |
| A-P2-002 | The 7 workflow files are the complete set of files requiring jury gate + citation audit amendments | Workflows added after this project launches would be unprotected | Phase 5 implementation will enumerate files matching `workflows/*.md` programmatically, not hardcode 7 |
| A-P2-003 | `rapidfuzz>=3.0` partial_ratio threshold < 60 correctly identifies material title conflicts | False WARNs (too aggressive) or missed misrepresentations (too lenient) | Phase 6 fixture suite calibration; success metric: 0 false-positive FAILs on known-valid fixtures |
| A-P2-004 | The law registry is not in agent context at citation time (root cause) | If registry IS in context, L1 FAIL rate may already be 0 | Phase 7 RAG evaluation earmarked per design spec §9 |
| A-P2-005 | ENG-6.8 Privacy exclusion holds — artifacts scanned never contain PII | Future artifacts containing PII would require ENG-6.8 mitigations | Scoping constraint documented in §2.3; re-evaluate if tool scope expands to network sources |
| A-P2-006 | "Executive approval" is the correct gate for amending a NON-NEGOTIABLE law | No formal amendment process law exists; assumption derived from index.yaml comment | Phase 4 law authoring must not create a PRD-2.6 amendment without explicit human approval; human APPROVE gate enforces this |
| A-P2-007 | Exactly 5 of 7 workflows currently lack a PRD-2.6 jury gate (discovery.md and greenfield-development.md have them; the other 5 do not) | If more/fewer workflows already have jury gates, D5 amendment scope is wrong | Phase 5 implementation will enumerate existing jury gate rows in each `workflows/*.md` file before applying amendments |

---

## 4. Non-Negotiable Constraint Map

> C-P2-001-J3: Map corrected — ENG-12.1 applies pre-Phase 1 (provision) and at Phase 6
> (dashboard), not Phase 6 only. ENG-13.1 applies to all human-facing artifacts (1–8).
> ENG-6.4 and ENG-10.1 added. ENG-4.4 clarified as Strictly Enforced (not NON-NEG).
> C-P2-004-J1: Map heading clarified — lists phase gate dependencies, not exclusively NON-NEGs.
> C-P2-001-J3-R2: J3 raises ENG-12.1 applies "before each phase transition" per the law text.
> Governing source is greenfield-development.md workflow spec: ENG-12.1 gates are at
> Phase 0 (provision before Phase 1 begins) and Phase 6 (per-slice dashboard review). The
> workflow is the authoritative operationalization of the law for this build; no additional
> per-phase gate is specified by the workflow. Flagged for Judicial Synthesis adjudication.
> C-P2-007-J3: ENG-13.1 timing conflict — artifact says "before human review"; ENG-13.1
> says "before ensemble deliberation"; PRD-2.6 Req 8 says "render after jury". Resolution:
> PRD-2.6 Req 8 supersedes ENG-13.1 "before ensemble" clause for the jury stage only
> (established in design spec §5.1 note, approved 2026-05-22). For the human APPROVE gate,
> "before human review" IS the ENG-13.1 requirement — no conflict exists there.

```
Phase 0:    ENG-12.1  — SonarQube gate provisioned (NON-NEGOTIABLE)
Phase 1–8:  PRD-2.6   — 5-juror 2-round jury + Judicial Synthesis on every phase artifact (NON-NEGOTIABLE)
Phase 1–8:  ENG-11.1  — all implementation spec-driven; no code without approved spec (NON-NEGOTIABLE)
Phase 1–8:  ENG-13.1  — all human-facing artifacts rendered as HTML before human review (NON-NEGOTIABLE)
Phase 3:    ENG-1.5   — CLI contract designed before implementation (Strictly Enforced)
Phase 3:    ENG-4.4   — BDD acceptance criteria for all critical paths (Strictly Enforced)
Phase 3:    ENG-6.5   — all 4 input validation surfaces specified (Strictly Enforced)
Phase 5:    ENG-2.3   — vertical slice dependency graph (Strictly Enforced)
Phase 6:    ENG-4.1   — Atomic TDD (RED→GREEN→REFACTOR) for all source code ← HARD GATE (NON-NEGOTIABLE)
Phase 6:    ENG-6.1   — no unintended stdout; console output explicit opt-in (NON-NEGOTIABLE)
Phase 6:    ENG-6.4   — no PII; context snippets in explicit mode only (NON-NEGOTIABLE)
Phase 6:    ENG-6.7   — citation_audit frontmatter block on all scanned artifacts (NON-NEGOTIABLE)
Phase 6:    ENG-10.1  — citation audit events collected as constitution metrics (NON-NEGOTIABLE)
Phase 6:    ENG-12.1  — human dashboard review at each slice ← HARD GATE (NON-NEGOTIABLE)
Phase 6:    BUS-7.1   — audit events structured, immutable, retained ≥1yr (NON-NEGOTIABLE)
Phase 7:    ENG-4.11  — critical path mutation score ≥85% ← HARD GATE (Strictly Enforced)
Phase 8:    ENG-11.1  — proposal archived (NON-NEGOTIABLE)
```

---

## 5. Constitutional Amendment Obligations

### 5.1 ENG-14.2 Modifies PRD-2.6 (NON-NEGOTIABLE)

ENG-14.2 adds a conditional 6th juror (J6 Citation Auditor) to the PRD-2.6 jury protocol.
Since PRD-2.6 is NON-NEGOTIABLE, this modification requires:

1. **Ensemble deliberation** (complete) — design spec v1.1.0 passed 2-round jury +
   Judicial Synthesis (APPROVED claude-opus-4.5 2026-05-22)
2. **Executive approval** before the amended PRD-2.6 can be merged into the constitution
3. **ENG-10.1 metrics** — J6 detection events tracked and fed into ENG-14.2 elevation clause

> C-P2-004-J4: Governing source for "executive approval" obligation: `laws/index.yaml`
> non_negotiable section states "require executive approval to amend." No formal
> constitutional amendment process law exists (documented as an assumption in §3
> A-P2-006). The human APPROVE gate in this greenfield workflow IS the executive approval
> gate for this change — the human approving Phase 8 Ship constitutes the required
> executive approval for the PRD-2.6 amendment.
> C-P2-002-J3-R2: J3 challenges that human APPROVE authority depends on an assumption, not
> a cited constitutional mechanism. Response: index.yaml is the governing constitutional
> document for non-negotiable law enforcement. The `non_negotiable` section comment is the
> explicit constitutional basis. No separate amendment process law exists — this is an
> honest documentation of the constitution's current state, not a defect in this artifact.
> Flagged for Judicial Synthesis adjudication.
> C-P2-008-J4: J4 challenges ENG-14.2 absence from law_citations. Response: ENG-14.2 is a
> PROPOSED draft law — not yet merged into laws/index.yaml. Per §2.4 design spec §4.2,
> all artifacts in this project use `--allow-draft ENG-14.1,ENG-14.2` when scanned.
> Draft law IDs are intentionally excluded from law_citations (they are not in index.yaml
> law_ids and would fail L2 validation). This is by design. Flagged for Judicial Synthesis.

### 5.2 D5 Workflow Amendments — PRD-2.6 Implication

Once ENG-14.2 is merged, PRD-2.6 jury tables in all 7 workflows must include the J6 row.
Phase 5 adds J6 row + citation audit step simultaneously to all 7 workflow files. Five
of the 7 workflows also receive their first PRD-2.6 jury gate at this point.

---

## 6. Avatar-Specific Law Specializations

Per `avatar-python-fastapi` manifest (Python 3.11+ bindings):

| Law | Python/CLI Specialization |
|-----|--------------------------|
| ENG-4.1 | `pytest` as test runner; each test file mirrors source module |
| ENG-3.1 | `radon cc` — cyclomatic complexity; no function > CC=10 |
| ENG-3.5 | `snake_case` functions/variables; `PascalCase` classes; `UPPER_SNAKE` constants |
| ENG-3.6 | Docstrings on all public functions/classes; `ruff --select D` enforcement |
| ENG-4.6 | `pytest-cov` with `--cov-fail-under=90`; `coverage.py` as backend |
| ENG-4.11 | `mutmut` or `cosmic-ray` as mutation test runner; Phase 7 |
| ENG-5.2 | CI pipeline: `ruff check` + `mypy` + `pytest` + `pip-audit` + `aa-citation-audit` |
| ENG-6.6 | `pip-audit` in CI; critical CVEs remediated before merge |

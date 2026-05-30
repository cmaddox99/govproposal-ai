---
phase: 1
title: "Capture — Law Citation Auditor"
project: citation-auditor-2026-001
workflow: greenfield-development
version: v1.1.0
status: APPROVED
approved_by: claude-opus-4.5
approved_at: 2026-05-23
judicial_synthesis_verdict: "APPROVED — 16/16 citations valid; J5 CHALLENGED adjudicated (workflow misinterpretation + design-spec re-litigation); zero unresolved blocking verdicts"
author: Hangar AI (claude-sonnet-4.6)
date: 2026-05-23
law_citations: [PRD-2.1, PRD-2.6, PRD-2.5, ENG-4.1, ENG-4.6, ENG-4.11, ENG-6.1, ENG-6.4, ENG-6.7, ENG-10.1, ENG-11.1, ENG-12.1, ENG-12.2, ENG-13.1, ENG-2.3, BUS-7.1]
r1_corrections: 20
r2_corrections: 5
---

# Phase 1 — Capture: Law Citation Auditor

## 1. Problem Statement

### 1.1 Scope

This project addresses constitutional law citation integrity within Hangar AI Constitution
workflow artifacts. Two failure modes are in scope for v1:

1. **ID does not exist in the registry** — hallucinated law ID (e.g. `ENG-9.9`)
2. **Title/status misrepresentation** — law ID exists but is described with the wrong
   title, scope, or non-negotiable status

**Out of scope (v1):** general factual hallucination, third-party citations (ADO, git,
external URLs), semantic misapplication without explicit title conflict.

> C-P1-020 (J5): v1 scope is L1 enforcement only (ID existence + explicit title/status
> phrase conflicts). Contextual misapplication (richer semantic checks) is explicitly
> deferred; this is a narrowing of the problem definition, not the full citation-risk
> surface.

### 1.2 Evidence of Harm

Jason (Mobile Platform team) reported hallucinated law IDs in disc-2026-008 discovery
artifacts that were delivered to stakeholders, causing credibility risk for the AA
engineering governance program.

> C-P1-007 (J1/J5): This is a single-trigger governance response. One incident of
> hallucinated law IDs reaching stakeholder documents is sufficient to mandate a
> NON-NEGOTIABLE guardrail (ENG-14.1) — the constitutional credibility harm is
> categorical, not frequency-based. Quantitative corpus sampling (scanning existing
> archived artifacts for hallucinated IDs) is a Phase 2 Discover activity to establish
> baseline and confirm the fix is effective.

> C-P1-008 (J1): Traceability reference — disc-2026-008 is committed to the hangar-ai-
> constitution repo at `hangar-ai-specs/archive/2026-05-22-disc-2026-008/`. The specific
> hallucinated law IDs will be identified and documented during Phase 2 corpus scan.

### 1.3 Root Cause

Agents cite laws from memory without verifying against the registry. Deeper root cause:
the law registry is not in agent context at citation time. A RAG-based root-cause fix
(preloading registry at citation time) is earmarked for evaluation after 3 discovery
cycles; this project implements output-stage validation as an immediately deployable fix.

---

## 2. Initiating Context

| Item | Detail |
|------|--------|
| Triggering report | Jason (Mobile Platform), post disc-2026-008 review; reference: `hangar-ai-specs/archive/2026-05-22-disc-2026-008/` |
| Harm severity | Hallucinated law IDs in stakeholder documents — constitutional credibility risk (categorical, single-incident threshold) |
| Approved design spec | `law-citation-auditor-design.md` v1.1.0 (APPROVED, claude-opus-4.5, 2026-05-22) |
| Design spec jury rounds | R1 (21 corrections) + R2 (7 corrections) + Judicial Synthesis |
| Applicable workflows | product-discovery (Stage A-F), greenfield, legacy-rescue (×3), avatar, adoption |
| Constitution repo | `/Users/979925/Repos/governance/hangar-ai-constitution/` |

### 2.1 Phase 0 Prerequisite — COMPLETE

> C-P1-002 (J3/J4): Phase 0 blocking prerequisite acknowledged and confirmed complete.

The approved design spec §9 designated a Phase 0 prerequisite before any tool code:
fix `laws/index.yaml` — add ENG-12.1, ENG-12.2, ENG-12.3 to `law_ids.engineering`
(the registry was jumping ENG-11.3 → ENG-13.1, which would have produced false FAILs
on valid Agentic Compliance Feedback Loop citations).

**Status: COMPLETE — commit `ab44374` (2026-05-23).**

ENG-12.1, ENG-12.2, ENG-12.3 confirmed present in `laws/index.yaml law_ids.engineering`.
All 10 governance tests pass (`python3 -m pytest tests/governance/`).

### 2.2 Design Spec ENG-10.1 Citation Note

> C-P1-001 (J2 BLOCKING): The approved design spec v1.1.0 §3.1 Req 10 cites ENG-10.1
> as the "amendment process" law — this is a Failure Mode 2 misrepresentation. ENG-10.1
> is the **Constitution Metrics Collection Law** (NON-NEGOTIABLE), which mandates
> standardized metrics collection for law compliance and adoption health — not an
> amendment process. No law in the constitution currently defines a formal amendment
> procedure for NON-NEGOTIABLE laws; only an index.yaml comment ("require executive
> approval to amend") exists. This error in the design spec is a known inherited defect.
> The Phase 4 law authoring step (Article XIV) must NOT propagate this misrepresentation.
> The amendment obligation for ENG-14.2 modifying PRD-2.6 is real but governed by
> executive approval and the PRD-2.6 jury gate process — not by ENG-10.1 requirements.

---

## 3. Personas

### P1 — Constitution Workflow Agent
**Who:** Any Hangar AI agent operating a constitution workflow (product-discovery,
greenfield, legacy-rescue, avatar, adoption).
**Problem:** Cites law IDs from memory; may produce hallucinated or misrepresented
citations in phase artifacts.
**Need:** A pre-jury citation audit that blocks progression on hallucinated IDs; a
dedicated Citation Auditor in the jury when citation density warrants it.

### P2 — Human Practitioner (Engineer / Product Coach)
**Who:** AA engineers and product coaches receiving jury-corrected artifacts.
**Problem:** Manual cross-referencing of law IDs against the registry is not a standard
practice and cannot be relied upon as a systematic control.
**Need:** Confidence that all law citations in artifacts they review and approve have
been machine-verified before reaching them.

> C-P1-009 (J1): P2's assumption that practitioners do not manually verify is hedged
> — the need is for a systematic machine control regardless of current ad-hoc practice.

### P3 — Constitution Maintainer
**Who:** Author/maintainer of the Hangar AI Constitution.
**Problem:** Hallucinated law IDs accumulate in archived artifacts, creating drift.
May be misquoted in future work using archived artifacts as templates.
**Need:** An audit-trail frontmatter block on each artifact and a CI gate that enforces
zero hallucinated IDs on new/modified artifacts.

### P4 — Judicial Synthesizer / Jury (PRD-2.6)
**Who:** The 5-juror + Synthesizer ensemble invoked at each phase gate.
**Problem:** J1-J5 currently have no structured citation verification mandate.
The Synthesizer has no citation integrity block in the synthesis schema.
**Need:** A structured Citation Auditor (J6) verdict schema and a mandatory Citation
Integrity Block in every Judicial Synthesis for qualifying artifacts.

### P5 — CI/CD Pipeline Operator
**Who:** Engineer responsible for maintaining CI pipeline health across the constitution
repo and downstream projects.
**Problem:** A fail-closed citation audit tool, if misconfigured or unavailable, will
block jury invocations with unclear resolution paths. Version skew between environments
can produce inconsistent results.
**Need:** Clear tool availability requirements, fail-closed resolution paths, staged
enforcement (warn-only → enforce), and runtime SLO for large artifacts.

> C-P1-006 (J1/J3): P5 added to represent rollout/operator needs distinct from P2
> (artifact consumer) and P3 (constitution maintainer).

---

## 4. Compliance Discovery

> C-P1-010 (J1): All constraints below are project-scope — they are active at their
> respective phases, not all simultaneously at Phase 1. They are surfaced here to
> ensure no constraints are discovered late.

### 4.1 Non-Negotiable Constraints

| Law | Accurate Title | Constraint for this project |
|-----|---------------|----------------------------|
| ENG-4.1 | Atomic TDD Law | All tool code via RED→GREEN→REFACTOR (Phase 6) |
| ENG-6.1 | Security by Design Law | CLI tool must define default output behavior; console output is explicit opt-in; no unintended artifact content leakage to stdout |
| ENG-6.4 | Data Protection Law | Law registry is not sensitive data; no PII in citations |
| ENG-10.1 | **Constitution Metrics Collection Law** | Metrics must be collected for citation audit events; J6 detection rate feeds ENG-14.2 elevation clause via BUS-7.1 audit events. NOTE: ENG-10.1 is NOT the amendment process law — see §2.2 |
| ENG-11.1 | Spec-Driven Development Law | All implementation spec-driven; this Capture artifact initiates the spec trail |
| ENG-12.1 | Agentic Feedback Loop Law | SonarQube gate must be provisioned before Phase 6 Build |
| ENG-13.1 | Artifact Rendering Standard | Phase 5 PROPOSAL rendered as HTML before human APPROVE gate |
| PRD-2.6 | Multi-Cognition Phase Gate Jury Law | Every phase artifact (Phases 1-8) must pass 2-round jury + Judicial Synthesis before human sees it |

> C-P1-001 (J2 BLOCKING): ENG-10.1 description corrected from "Constitution Governance
> — amendment process" to accurate title "Constitution Metrics Collection Law." The
> amendment obligation for ENG-14.2 is real but derives from executive approval and
> PRD-2.6 jury process, not ENG-10.1 requirements.

### 4.2 Strictly Enforced Constraints

| Law | Accurate Title | Constraint |
|-----|---------------|-----------|
| ENG-2.3 | Dependency Management Law | Vertical slice dependency graph required at Phase 5 |
| ENG-4.6 | Code Coverage Gate Law | SonarQube `new_coverage` ≥ 90% per slice (Phase 6) |
| ENG-4.11 | Mutation Testing Law | Mutation score ≥ 70% per slice; ≥ 85% on critical paths (Phase 7) |
| ENG-6.7 | Audit Trail Law | `citation_audit` frontmatter block on all scanned artifacts |
| BUS-7.1 | Audit Trail Law | Audit events: `jury_deliberation.j6_challenged_count`, `citation_audit.fail_count` for ENG-14.2 elevation tracking and ENG-10.1 metrics |
| PRD-2.5 | Discovery Stage-Gate Law | This greenfield implementation is gated by Phases 1-8 |

### 4.3 Explicit v1 Requirements (surfaced at Capture)

> C-P1-004 (J4 BLOCKING): Fail-closed and CI re-execution requirements made explicit.

1. **Fail-closed** — when the citation audit tool is unavailable (exit 2) or the
   registry is not parseable, jury invocation MUST HALT. Silent advisory mode is
   prohibited. The resolution path and human confirmation step must be defined.
2. **CI re-execution** — CI must RE-EXECUTE `aa-citation-audit <artifact.md>` and
   assert exit code 0. Reading `fail_count` from frontmatter is NOT acceptable
   CI enforcement.
3. **Default output behavior** — console output is an explicit opt-in mode. Default
   behavior writes a `citation_audit` frontmatter block; no artifact content is
   written to stdout by default.

> C-P1-005 (J4 BLOCKING): ENG-6.1 operationalized — "no unexpected stdout leakage"
> defined as: default mode writes frontmatter only; `--output console` is explicit;
> context snippets (±150 chars) are written only in `--output console` mode and
> are scoped to the artifact being audited (not constituting PII).

---

## 5. Deliverables

| # | Deliverable | Phase | Notes |
|---|------------|-------|-------|
| D0 | `laws/index.yaml` ENG-12.x gap fixed | **COMPLETE** (pre-Phase-1) | Commit `ab44374` |
| D1 | `tools/citation-auditor/` — Python CLI package (`aa-citation-audit`) | 6 | Per design spec §4 |
| D2 | `laws/engineering/citation-integrity.md` — Article XIV (ENG-14.1 + ENG-14.2) | 4 | With accurate law title/status |
| D3 | `laws/index.yaml` — Article XIV added; ENG-14.1 in `non_negotiable` | 4 | Separate index.yaml update |
| D4 | `laws/engineering/_domain.yaml` — Article XIV section added | 4 | |
| D5 | Amendments to all 7 workflow files (PRD-2.6 jury table + citation audit step) | 5 | 5 workflows need jury gate added simultaneously |
| D6 | `hangar-ai-specs/changes/citation-auditor-2026-001/PROPOSAL.md` (HTML rendered) | 5 | ENG-13.1 |
| D7 | Integration test suite in `tools/citation-auditor/tests/` | 6 | Coverage ≥ 90% (SonarQube ENG-4.6) |
| D8 | `hangar-ai-specs/archive/2026-citation-auditor-2026-001/` — full archive | 8 | ENG-11.1 |

---

## 6. Risk Register

| ID | Risk | Likelihood | Impact | Mitigation |
|----|------|-----------|--------|-----------|
| R1 | ENG-14.2 modifies PRD-2.6 (NON-NEGOTIABLE) — requires executive approval and PRD-2.6 jury gate before merge (not ENG-10.1 process — see §2.2) | Certain | High | Amendment framing corrected: obligation is executive approval + PRD-2.6 jury gate; Phase 4 law authoring must not propagate ENG-10.1 misrepresentation |
| R2 | rapidfuzz title-match threshold calibrated too aggressively → false WARNs | Medium | Low | WARN fires only on explicit title phrases; threshold calibrated against fixture suite at Phase 6 |
| R3 | 5 of 7 workflows lack PRD-2.6 jury gates → Phase 5 must add both jury gate + citation audit simultaneously | Certain | Medium | Design spec §5.3 matrix prescribes simultaneous addition; citation audit is inert without jury gate |
| R4 | SonarQube unavailable at Phase 6 (ENG-12.1) | Medium | High | Flagged; Docker provision instructions in project README; practitioner action required before Phase 6 |
| R5 | Phase 7 RAG evaluation may make L1 tool obsolete | Low | Low | Grandfathered archives exempt; L1 downgrade via executive approval if RAG proves effective |
| R6 | Adoption friction: output-stage citation audit adds jury-cycle drag before upstream RAG fix | Medium | Low | Staged CI enforcement (warn-only Week 1, enforce Week 2+); escalation to enforce-mode is also triggered if false-positive rate = 0 AND WARN resolution ≥90% after Week 1 — metric-gated, not time-only; runtime SLO <60s; Phase 7 upstream evaluation earmarked |
| R7 | pyproject.toml `--cov-fail-under=80` conflicts with SonarQube ENG-4.6 gate (≥90%) | Certain | Medium | pyproject.toml floor must be raised to ≥90 at Phase 6 Build; design spec §4.3 requires correction before Phase 6 |
| R8 | Tool install/version skew across CI environments (P5 need) | Medium | Low | Specify exact dependency bounds: `rapidfuzz>=3.0,<4.0` and `click>=8.1,<9.0`; runtime bounds test in CI; P5 resolution path documented |

> C-P1-011 (J1): R2 "threshold tested" reframed as forward-looking mitigation (fixture suite calibration at Phase 6).
> C-P1-015 (J3): R6 added — adoption friction and throughput risk.
> C-P1-014 (J2): R7 added — pyproject.toml coverage floor inconsistency.
> C-P1-019 (J4): R8 added — operational risk (install/version skew).

---

## 7. Success Criteria

| Criterion | Measurable Outcome |
|-----------|-------------------|
| Zero hallucinated law IDs in new/modified artifacts | `aa-citation-audit` CI gate exits 0 on all new or modified artifacts (not archived; grandfathered artifacts exempt) |
| Fail-closed enforced | Tool unavailability (exit 2) produces jury HALT with documented resolution path; no silent advisory mode |
| CI uses re-execution (not frontmatter) | CI script calls `aa-citation-audit <artifact.md>`; does not read `fail_count` from frontmatter |
| J6 Citation Auditor active in qualifying juries | Jury logs show J6 invocations for: L1 WARN ≥1, OR Stage E/F product-discovery, OR artifact cites ≥5 distinct law IDs; BUS-7.1 audit events recorded |
> C-P1-022 (J4 R2): J6 trigger wording tightened — "≥5 distinct law IDs cited in the artifact" not "≥5 distinct law citation artifacts".|
| All 7 workflows have PRD-2.6 jury gates | All workflow files contain jury gate protocol block |
| Governance tests pass post-implementation | `python3 -m pytest tests/governance/` — 100% pass (count TBD at Phase 3) |
| SonarQube Phase 6 gate | SonarQube dashboard evidence: `new_coverage` ≥ 90% (ENG-4.6); `mutation_score` ≥ 70% (ENG-4.11); `bugs` = 0; committed per ENG-12.2 |
| False-positive rate | 0 hallucinated FAIL verdicts on known-valid fixtures (ENG-12.x citation fixture must PASS) |
| L1 audit runtime | <60 seconds on typical phase artifact |
| WARN resolution rate | ≥90% of L1 WARNs resolved by J6 without escalation to human |

> C-P1-016 (J3): Added operator-facing success metrics: false-positive rate, runtime, WARN resolution rate.
> C-P1-013 (J2/J4): "10/10" changed to "100% pass (count TBD at Phase 3)".
> C-P1-017 (J4): J6 activation criteria inlined with BUS-7.1 fields.
> C-P1-018 (J4): "new/modified artifacts" enforcement scope clarified; grandfathering stated.
> C-P1-012 (J2): law_citations frontmatter updated with all body-cited IDs.

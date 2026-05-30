---
title: "aa-citation-audit — Implementation Proposal"
project: citation-auditor-2026-001
version: v0.1.0
date: 2026-05-23
status: PROPOSED — PENDING JURY APPROVAL
---

# aa-citation-audit: Implementation Proposal

> **Project:** `citation-auditor-2026-001`
> **Tool:** `aa-citation-audit` — Law Citation Auditor CLI
> **Owner:** Hangar AI Constitution Engineering
> **Date:** 2026-05-23

---

## What We're Building

A Python CLI tool that validates law citations in Hangar AI Constitution workflow artifacts
**before** jury invocation. When a practitioner references a law like `ENG-4.1` in a discovery
document, this tool confirms the ID is real, registered, and accurately described — catching
hallucinated citations before they corrupt jury deliberation.

**The problem it solves:** In disc-2026-006 (Mobile Platform Health Engineering), law citation
hallucinations were identified post-jury — an embarrassing and compliance-drifting outcome.
This tool closes the pre-jury gap with a two-layer defense:
- **L1 gate (ENG-14.1):** `aa-citation-audit` scans every artifact → blocks jury on FAIL
- **J6 seat (ENG-14.2):** A Citation Auditor juror (gpt-4.1) joins every jury panel that triggers
  activation conditions (≥1 WARN, Stage E/F artifacts, or ≥5 cited laws)

---

## Implementation Plan: 6 Vertical Slices

| Slice | What Gets Built | Story Points |
|-------|----------------|:---:|
| **S-01** | Project scaffold + `registry.py` — loads `laws/index.yaml` + all law markdown files to build an in-memory ID registry | 3 |
| **S-02** | `scanner.py` — strips code blocks, extracts law ID citations with context, enforces size/encoding guards | 3 |
| **S-03** | `auditor.py` + data models — verdict logic (FAIL/WARN/PASS), rapidfuzz title mismatch, status mismatch detection | 5 |
| **S-04** | `cli.py` — click interface, 4-surface input validation, 3 output modes, atomic write, BUS-7.1 audit log | 5 |
| **S-05** | BDD scenarios, fixture suite, integration tests, ReDoS regression, CI pipeline config | 8 |
| **S-06** | Amend all 7 constitution workflow files — add pre-jury citation audit step + J6 jury seat | 5 |
| | **Total** | **29** |

**Build order:** S-01 → (S-02 ∥ S-03) → S-04 → S-05 → S-06

---

## Quality Gates (Per Slice)

Every slice must pass before the next begins (ENG-4.1 NON-NEGOTIABLE):

- ✅ All unit tests green (RED → GREEN → REFACTOR → VERIFY → COMMIT)
- ✅ Code coverage ≥ 90% (`--cov-fail-under=90`)
- ✅ Mutation score ≥ 85% on `scanner.py` and `auditor.py`
- ✅ SonarQube: `new_coverage ≥ 90%`, `bugs = 0`

---

## What Happens After Phase 6 (Ship — Phase 8)

Once the tool is verified and all workflows amended:

1. Article XIV (ENG-14.1 + ENG-14.2) merges into `laws/engineering/` — requires executive approval
2. `laws/index.yaml` updated with 2 new ENG laws (70 → 72 engineering laws)
3. `--allow-draft ENG-14.1,ENG-14.2` removed from CI — citations now fully enforced
4. Every future jury invocation across all 7 workflows is protected

---

## Key Decisions Already Approved

| Decision | ADR | Rationale |
|----------|-----|-----------|
| 4-layer DI architecture (registry/scanner/auditor/cli) | ADR-001 | ENG-3.4 SRP; cli.py is DI host |
| Title/summary from law markdown files | ADR-002 | index.yaml has no per-law metadata |
| Fenced-then-inline code block stripping | ADR-003 | Prevents false PASS from code-block IDs |
| rapidfuzz partial_ratio threshold 60 | ADR-004 | Best overlap match for constitutional law titles |
| Python 3.11+ only | ADR-005 | AA platform baseline |

---

## Blockers Before Phase 6

| Blocker | Action Required |
|---------|----------------|
| SonarQube not running | `docker run -d -p 9000:9000 sonarqube:community` |
| | `./tools/sonarqube-gate/provision.sh --project-key citation-auditor-2026-001` |

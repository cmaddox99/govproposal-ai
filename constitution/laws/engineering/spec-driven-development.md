---
domain: engineering
article: XI
title: Spec-Driven Development Laws
laws:
  - id: ENG-11.1
    title: Hangar SDD Law
    non_negotiable: true
    summary: Every project adopting the constitution MUST have a hangar-ai-specs/ folder; all significant work governed by Hangar SDD PROPOSE→IMPLEMENT→ARCHIVE lifecycle
  - id: ENG-11.2
    title: Proposal Completeness Law
    summary: PROPOSAL.md SHALL include problem, solution, deliverables, success criteria, and law citations — proposals without law citations SHALL be rejected
  - id: ENG-11.3
    title: Spec Freshness Law
    summary: Specs in hangar-ai-specs/specs/ SHALL reflect current system truth — stale specs contradicting the codebase are a compliance violation
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article XI: Spec-Driven Development Laws

> Govern the Hangar SDD process — tool-independent; `PROPOSE → IMPLEMENT → ARCHIVE`.

---

## ENG-11.1: Hangar SDD Law

**Law ID:** `ENG-11.1` | **Status:** NON-NEGOTIABLE

Every project adopting the Hangar AI Constitution SHALL implement the Hangar SDD process.

1. `hangar-ai-specs/` folder MUST exist in every adopted project; `openspec/` is prohibited
2. Significant work MUST have an approved `PROPOSAL.md` before implementation
3. All work follows `PROPOSE → IMPLEMENT → ARCHIVE`
4. No external spec tool required or permitted

| Stage | Action | Output |
|---|---|---|
| PROPOSE | Scaffold `changes/[verb-noun-id]/` | `PROPOSAL.md` + `tasks.md` |
| IMPLEMENT | Execute tasks; update `PROGRESS.md` | Working code; tasks checked |
| ARCHIVE | Move to `archive/YYYY-MM-DD-[id]/` | Completed, dated entry |

---

## ENG-11.2: Proposal Completeness Law

**Law ID:** `ENG-11.2`

`PROPOSAL.md` SHALL include all required sections with ≥1 law citation. Missing any section or citation → rejected.

| Section | Requirement |
|---|---|
| Problem | Broken, missing, or improving |
| Solution | What will be done |
| Deliverables | Concrete, verifiable outputs |
| Success Criteria | Measurable targets |
| References | ≥1 law ID citation |

---

## ENG-11.3: Spec Freshness Law

**Law ID:** `ENG-11.3`

Specs in `hangar-ai-specs/specs/` SHALL reflect the current system state. Stale specs contradicting the codebase are a compliance violation. Spec updates follow `PROPOSE → IMPLEMENT → ARCHIVE`.

---

## Governing Skill

See `agent-skills/skills-by-domain/discovery-research/spec-governance.md` (`skill-spec-governance`)

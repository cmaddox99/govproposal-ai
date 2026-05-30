---
title: "Avatar Workflow V2 — Quality Strengthening"
spec_id: "avatar-workflow-v2"
status: "PROPOSED"
author: "Amaya (Technical Coach)"
created: "2026-04-18"
scope: "workflows/avatar-workflow.md · docs/templates/avatars/ · agent-skills/skills-by-domain/platform-engineering/skill-avatar-workflow.md"
triggered_by: "Parity with discovery workflow improvements — render gate, structured templates, discovery handoff"
affects: "avatar-workflow, skill-avatar-workflow, templates/avatars"
laws_applied:
  - ENG-11.1
  - ENG-11.2
  - ENG-13.1
  - ENG-13.2
exit_checklist:
  - item: "Ensemble deliberation completed (Architect + Reviewer + Sentinel)"
    status: "pend"
  - item: "Render gate added at Phase 6 commit (ENG-13.1 NON-NEGOTIABLE)"
    status: "pend"
  - item: "Structured frontmatter on RAG validation + blast radius templates"
    status: "pend"
  - item: "Discovery handoff protocol defined in workflow"
    status: "pend"
  - item: "Stakeholder approval obtained"
    status: "pend"
stakeholder:
  name: "Adeel Ali"
  role: "Co-founder / Inventor"
  affirm: false
  note: "Pending review"
audit_log:
  - date: "2026-04-18"
    actor: "Amaya (Technical Coach)"
    action: "Initial analysis — scope confirmed: render gate + structured templates + discovery handoff"
    outcome: "DRAFTED"
avatars:
  - "avatar-technology-nodejs-typescript"
  - "avatar-product-airport-operations"
spec_artifacts:
  - path: "hangar-ai-specs/changes/avatar-workflow-v2/PROPOSAL.md"
    type: "proposal"
    status: "IN_PROGRESS"
template_version: "1.0.0"
---

# Avatar Workflow V2 — Quality Strengthening

## Problem Statement

The avatar workflow (v1.0.0) governs single-avatar lifecycles well across six modes. Three quality gaps exist that mirror problems already solved in the discovery workflow: evidence artifacts are committed as raw Markdown without a render gate (violating ENG-13.1 NON-NEGOTIABLE today), artifact templates carry no structured frontmatter, and the avatar workflow produces no handoff that feeds Discovery Stage A — requiring manual copy-paste of avatar IDs into every discovery run.

---

## Gap 1 — No Render Gate at Phase 6
**Severity:** 🔴 BLOCKING — ENG-13.1 NON-NEGOTIABLE

ENG-13.1 (Artifact Rendering Standard, NON-NEGOTIABLE) requires all human-facing governance artifacts to be rendered as self-contained HTML before stakeholder presentation. The avatar workflow commits RAG validation reports and blast radius reports as raw Markdown — no HTML render step before the Phase 6 commit gate.

**This is an active law violation.** Every avatar committed under Modes 1, 2, or 4 since the workflow shipped has breached ENG-13.1.

**Fix:** Add a render gate to Phase 6. Before `index.yaml` is updated and the commit is made, run `aa-artifact-render` on every evidence artifact and confirm the rendered output reads correctly in browser.

```
RENDER GATE — Phase 6 (ENG-13.1 NON-NEGOTIABLE)
─────────────────────────────────────────────────────
aa-artifact-render hangar-ai-specs/changes/{spec-id}/rag-validation-{avatar-id}.md
open hangar-ai-specs/changes/{spec-id}/rag-validation-{avatar-id}.html
→ Human confirms: yes / no
→ If no: return to Phase 5 and resolve
→ If yes: proceed to index.yaml update and commit
```

---

## Gap 2 — No Structured Frontmatter on Evidence Templates
**Severity:** 🟡 WARNING

Discovery workflow stage templates carry structured YAML frontmatter — `exit_checklist`, `audit_log`, `stakeholder`, `laws_applied`, `spec_artifacts` — which renders as navigable structured cards via `aa-artifact-render`. Avatar workflow templates in `docs/templates/avatars/` carry none of this structure, making them:

- Visually inconsistent with discovery workflow output
- Missing the audit trail required by BUS-7.1
- Not renderable as proper structured HTML evidence cards (feeds Gap 1)

**Fix:** Update two existing templates and add one new template:

| Template | Change |
|----------|--------|
| `example-template.md` | Add structured frontmatter (laws_applied, exit_checklist, audit_log) |
| `use-case-template.md` | Add structured frontmatter (laws_applied, audit_log) |
| `rag-validation-template.md` *(new)* | Full structured frontmatter — 5 RAG query checklist items, audit log, stakeholder sign-off |

The `rag-validation-template.md` is the primary artifact flowing through the Phase 6 render gate. It needs structured frontmatter to render correctly as a structured evidence card.

---

## Gap 3 — No Discovery Handoff Protocol
**Severity:** 🟡 WARNING

Avatars are activated in Discovery Stage A (`avatars[]` and `avatar_path` frontmatter fields). Today these are filled manually — the engineer copy-pastes avatar IDs from `avatars/index.yaml` into the Stage A template. There is no governed link from avatar workflow output to Discovery Stage A.

**Fix:** At the end of Phase 6 (after commit), the avatar workflow produces a `discovery-handoff.md` alongside the evidence artifacts:

```yaml
---
title: "{Domain} — Avatar Handoff for Discovery Stage A"
status: "READY"
avatars:
  - "{technology-avatar-id}"
  - "{product-avatar-id}"
avatar_path: "avatars/{type}/{slug}/"
rag_validated: true
rag_validation_date: "{YYYY-MM-DD}"
ready_for_discovery: true
---
```

This file is the authoritative source for `avatars[]` and `avatar_path` in Discovery Stage A frontmatter. Rendered via `aa-artifact-render` as part of the Phase 6 render gate batch. No manual fill.

---

## Deliverables

| # | Deliverable | File | Effort |
|---|-------------|------|--------|
| 1 | Render gate step in Phase 6 | `workflows/avatar-workflow.md` | S |
| 2 | Render gate step in skill | `skill-avatar-workflow.md` | XS |
| 3 | `rag-validation-template.md` with structured frontmatter | `docs/templates/avatars/` | S |
| 4 | `discovery-handoff-template.md` | `docs/templates/avatars/` | S |
| 5 | Update `example-template.md` + `use-case-template.md` | `docs/templates/avatars/` | S |

---

## Laws

| Law | Title | Relevance |
|-----|-------|-----------|
| ENG-11.1 | Hangar SDD Law (NON-NEGOTIABLE) | This proposal follows PROPOSE→IMPLEMENT→ARCHIVE |
| ENG-11.2 | Proposal Completeness Law | Law citations satisfied above |
| ENG-13.1 | Artifact Rendering Standard (NON-NEGOTIABLE) | Gap 1 is an active violation of this law |
| ENG-13.2 | Citation Transparency Law | Structured frontmatter enables citation card rendering |

---

## Success Criteria

1. Every avatar workflow run ends with at least one rendered HTML artifact reviewed in browser before commit
2. `rag-validation-{avatar}.md` uses structured frontmatter and renders as a structured evidence card
3. A `discovery-handoff.md` is produced after every Phase 6 commit — Stage A `avatars[]` is never manually filled again
4. Gate management and ballot trading avatar runs on Monday 2026-04-21 use this protocol

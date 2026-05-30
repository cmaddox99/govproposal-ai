# Proposal: Constitutional Adoption Workflow

**Proposal ID:** adoption-workflow
**Submitted:** 2026-04-08
**Status:** PROPOSED
**Laws:** ENG-10.1, ENG-11.1, ENG-1.2

---

## Problem

The Hangar AI Constitution has five governed workflows for building and rescuing products, but **no workflow for adopting the constitution itself**. This creates four practical gaps:

**1. No governed adoption path.**
Teams adopt the constitution by reading `docs/guides/adoption/brownfield-adoption.md` — a static guide, not a governed workflow. There are no constitutional phase gates, no verification artifact, and no consistent output structure.

**2. No migration handling.**
Repos that adopted during the `openspec/` era (before the rename to `hangar-ai-specs/`) have no governed path to migrate. Teams either leave stale directory names in place or delete and re-adopt from scratch — both unacceptable.

**3. No staleness detection.**
When the constitution evolves (new laws, new avatar structure, new workflow format), there is no workflow that checks whether an existing adoption is current and triggers a targeted update. Teams discover staleness by accident.

**4. No conditional Phase 0.**
Every other workflow (greenfield, legacy rescue, product discovery) silently assumes adoption is already correct. There is no guard that checks adoption state before allowing a team to start a governed workflow.

**5. Workshop is misaligned.**
The `hangar-ai-constitution-workflows` workshop repo teaches legacy rescue using the old brownfield adoption guide as the setup step. With a governed adoption workflow now in the constitution, the workshop's prompt guide and setup exercises should reference `workflows/adoption.md` as the authoritative entry point — not the static guide. Participants doing the legacy rescue track are exactly the audience who need to understand and practice the adoption workflow first.

---

## Proposed Solution

Add `workflows/adoption.md` — a three-phase adoption workflow that:

1. **Checks** the current adoption state of a codebase (fresh / stale / migration needed / up-to-date)
2. **Adopts or updates** constitutional governance files (`AGENTS.md`, `hangar-ai-specs/`, `project-rules.md`)
3. **Verifies** the result with `aa-constitution-lint` and produces a signed evidence artifact

The workflow runs as a **conditional Phase 0** before every other workflow. If adoption is current it skips silently. If stale or missing it runs first.

Additionally, update all existing workflow files to declare adoption as a prerequisite, and add a `docs/guides/prompts/adoption-workflow-prompt.md` that gives teams a single copy-paste prompt to trigger the adoption workflow from Copilot Chat.

---

## Scope

### In scope
- `workflows/adoption.md` — new adoption workflow (3 phases, constitutional frontmatter)
- `workflows/README.md` — add adoption workflow to index table
- `workflows/greenfield-development.md`, `legacy-rescue-*.md`, `product-discovery-stage-a-f.md` — add `preceded_by: adoption` declaration in frontmatter
- `docs/guides/prompts/adoption-workflow-prompt.md` — replace `adoption-bootstrap.md` prompt with workflow-aware version that handles fresh / update / migrate scenarios
- `docs/guides/adoption/how-to-adopt-constitution.md` — add reference to the new workflow as the authoritative adoption path
- **`hangar-ai-constitution-workflows` repo** — update workshop to replace old brownfield guide setup with adoption workflow; add adoption as Exercise 0 in the legacy rescue track; update prompt guide with adoption workflow prompt

### Out of scope
- Changes to any downstream codebase (adoption happens in the team's repo, not here)
- Changes to any law content
- Cross-referencing with any other constitution

---

## Key Design Decisions

### Inspired by, not copied from
This workflow follows the same three-phase structure (Check → Adopt → Verify) and conditional Phase 0 pattern proven in prior governance work. The implementation uses Hangar AI tools (`aa-constitution-lint`), law IDs (`ENG-*`, `PRD-*`, `BUS-*`), and directory conventions (`hangar-ai-specs/`) exclusive to this constitution.

### Migration cases handled
| State detected | Action |
|---|---|
| No `AGENTS.md`, no `hangar-ai-specs/` | Full fresh adoption |
| `AGENTS.md` + `hangar-ai-specs/` current | Skip — proceed to target workflow |
| `AGENTS.md` references old brownfield guide | Update AGENTS.md only |
| `openspec/` exists | Migrate `openspec/` → `hangar-ai-specs/`, update AGENTS.md |
| `openspec/` + `hangar-ai-specs/` both exist | Merge into `hangar-ai-specs/`, remove `openspec/` |

### Verification is mandatory
Phase 3 runs `aa-constitution-lint` against the adopted repo's `AGENTS.md` and `hangar-ai-specs/` structure. It produces a signed `evidence/adoption-verified.md` artifact. No workflow may proceed to Phase 1 without this artifact being present or Phase 3 completing cleanly.

---

## Success Criteria

- `aa-constitution-lint . --constitution .` passes with 0 failures after adoption
- A repo with stale `openspec/` naming runs the workflow and exits with `hangar-ai-specs/` and no `openspec/`
- A repo with a current adoption runs the workflow and skips phases 1–3 (no-op)
- All five existing workflow files declare `preceded_by: adoption` in frontmatter
- `docs/guides/prompts/adoption-workflow-prompt.md` is a single copy-paste prompt that covers all three migration cases

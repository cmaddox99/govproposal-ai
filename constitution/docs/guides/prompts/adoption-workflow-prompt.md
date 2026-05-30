# Adoption Workflow Prompt

> A single copy-paste prompt that runs the Hangar AI Constitution adoption workflow.
> Three labelled variants: fresh adoption, update existing adoption, migrate from openspec/.

---

## When to Use Which Variant

| Your Situation | Use |
|---|---|
| New repo — no `AGENTS.md`, no `hangar-ai-specs/` | **Variant A: Fresh Adoption** |
| Adopted before using the old brownfield guide — has `AGENTS.md` + `hangar-ai-specs/` but no governed workflow | **Variant B: Update Existing Adoption** |
| Adopted during `openspec/` era — directory is still called `openspec/` | **Variant C: Migrate from openspec/** |

---

## Variant A — Fresh Adoption

Copy and paste into GitHub Copilot Chat. Replace `{{CONSTITUTION_PATH}}` with the path to your local clone of `hangar-ai-constitution`.

```
The Hangar AI Constitution is at {{CONSTITUTION_PATH}}.

Run the Constitutional Adoption workflow for this project:

1. Read {{CONSTITUTION_PATH}}/workflows/adoption.md — this is the governed adoption workflow.
2. Execute Phase 1 (Check): inspect the project root for AGENTS.md, hangar-ai-specs/, and openspec/. Classify the action as full_adoption. Commit evidence/adoption-check.md.
3. Execute Phase 2 (Adopt):
   - Identify the technology stack and AA product domain from the codebase.
   - Resolve the closest technology avatar and product avatar from {{CONSTITUTION_PATH}}/avatars/.
   - Create AGENTS.md at the project root following the template in the adoption workflow.
   - Create hangar-ai-specs/ with changes/, archive/, and specs/ subdirectories.
   - Create hangar-ai-specs/project-rules.md with project name, avatar IDs, and placeholder extensions section.
4. Execute Phase 3 (Verify):
   - Run: aa-constitution-lint . --constitution {{CONSTITUTION_PATH}}
   - Confirm all checklist items pass.
   - Commit evidence/adoption-verified.md with linter result.
5. Commit all governance artifacts with message: "chore: adopt Hangar AI Constitution (ENG-1.2, ENG-11.1)"

Do not modify any source code, tests, or business logic. Governance files only.
```

---

## Variant B — Update Existing Adoption

Use when `AGENTS.md` exists but references the old brownfield guide or is missing avatar declarations.

```
The Hangar AI Constitution is at {{CONSTITUTION_PATH}}.

Run the Constitutional Adoption workflow — UPDATE mode — for this project:

1. Read {{CONSTITUTION_PATH}}/workflows/adoption.md — this is the governed adoption workflow.
2. Execute Phase 1 (Check): inspect the existing AGENTS.md. Classify the action as update (AGENTS.md references old brownfield guide or is missing avatar declarations or workflow references).
3. Execute Phase 2 (Adopt) — update only:
   - Do NOT delete or recreate hangar-ai-specs/ — it already exists.
   - Rewrite AGENTS.md using the template in Section 2.2 of the adoption workflow.
   - Identify technology and product avatars from the codebase and declare them in the new AGENTS.md.
   - If hangar-ai-specs/project-rules.md is missing, create it.
4. Execute Phase 3 (Verify):
   - Run: aa-constitution-lint . --constitution {{CONSTITUTION_PATH}}
   - Commit evidence/adoption-verified.md with linter result.
5. Commit with: "chore: update Hangar AI Constitution adoption (ENG-1.2, ENG-11.1)"

Do not modify source code, tests, or any file outside AGENTS.md, hangar-ai-specs/, and evidence/.
```

---

## Variant C — Migrate from openspec/

Use when the project has `openspec/` (the old directory name) that needs to become `hangar-ai-specs/`.

```
The Hangar AI Constitution is at {{CONSTITUTION_PATH}}.

Run the Constitutional Adoption workflow — MIGRATE mode — for this project:

1. Read {{CONSTITUTION_PATH}}/workflows/adoption.md — this is the governed adoption workflow.
2. Execute Phase 1 (Check): confirm openspec/ exists. Classify the action as migrate.
3. Execute Phase 2 (Adopt) — migration:
   - If hangar-ai-specs/ does NOT exist: rename openspec/ → hangar-ai-specs/
   - If hangar-ai-specs/ ALREADY exists (merge case): copy openspec/changes/, openspec/archive/, openspec/specs/ into hangar-ai-specs/ without overwriting existing files; then remove openspec/.
   - Update AGENTS.md to reference hangar-ai-specs/ (not openspec/). If AGENTS.md is missing or references the old brownfield guide, rewrite it using the template in Section 2.2 of the adoption workflow.
   - Ensure hangar-ai-specs/project-rules.md exists. Create it if missing.
   - Commit evidence/adoption-update.md documenting the migration.
4. Execute Phase 3 (Verify):
   - Confirm no openspec/ directory remains.
   - Run: aa-constitution-lint . --constitution {{CONSTITUTION_PATH}}
   - Commit evidence/adoption-verified.md.
5. Commit with: "chore: migrate openspec/ → hangar-ai-specs/, update Hangar AI Constitution adoption (ENG-1.2, ENG-11.1)"

Do not modify source code or tests. Governance and directory structure changes only.
```

---

## Finding Your Constitution Path

```bash
# If hangar-ai-constitution is in a sibling directory to your project:
ls ../hangar-ai-constitution/workflows/adoption.md   # should exist

# Common paths at AA:
# ~/repos/american-airlines/governance/hangar-ai-constitution
# ../hangar-ai-constitution
```

---

## What the Agent Will Produce

After running any variant, the project root will contain:

```
your-project/
├── AGENTS.md                          ← Updated with constitution, avatars, workflows
├── hangar-ai-specs/
│   ├── changes/                       ← In-progress proposals
│   ├── archive/                       ← Completed proposals
│   ├── specs/                         ← Baseline behavioral specifications
│   │   └── README.md
│   └── project-rules.md               ← Project-specific constitutional extensions
└── evidence/
    ├── adoption-check.md              ← Phase 1 classification artifact
    ├── adoption-verified.md           ← Phase 3 linter-verified artifact
    └── adoption-update.md             ← Migration log (Variant C only)
```

# Tasks: adoption-workflow

---

## Phase 1 — Adoption Workflow Document

- [x] 1.1 Create `workflows/adoption.md` with YAML frontmatter (`id`, `name`, `laws`, `skills`, `triggers`, `preceded_by: null`, `followed_by`)
- [x] 1.2 Write Phase 1 (Check) — detect adoption state: fresh / stale / openspec-migration / current; define decision table for each state
- [x] 1.3 Write Phase 2 (Adopt) — Step 2.1: avatar resolution (technology + product-type); Step 2.2: create/update `AGENTS.md`; Step 2.3: create `hangar-ai-specs/` structure; Step 2.4: create/update `project-rules.md`
- [x] 1.4 Write Phase 2 (Adopt) — Step 2.5: migration path for `openspec/` → `hangar-ai-specs/` (handle merge case where both exist)
- [x] 1.5 Write Phase 3 (Verify) — run `aa-constitution-lint`; checklist of required artifacts; produce `evidence/adoption-verified.md`
- [x] 1.6 Write failure modes table (avatar not found, lint fails after adopt, partial migration, AGENTS.md already exists with conflicting content)
- [x] 1.7 Define `evidence/adoption-check.md` and `evidence/adoption-verified.md` artifact schemas (YAML)
- [x] 1.8 Add conditional skip logic: if `evidence/adoption-verified.md` exists and `hangar-ai-specs/` is current → skip all phases

---

## Phase 2 — Workflow Index + Existing Workflow Updates

- [x] 2.1 Update `workflows/README.md` — add adoption workflow row to index table (before all other workflows; note it as conditional Phase 0)
- [x] 2.2 Update `workflows/greenfield-development.md` frontmatter — add `preceded_by: adoption`
- [x] 2.3 Update `workflows/product-discovery-stage-a-f.md` frontmatter — add `preceded_by: adoption`
- [x] 2.4 Update `workflows/legacy-rescue-decision-track.md` frontmatter — add `preceded_by: adoption`
- [x] 2.5 Update `workflows/legacy-rescue-refactor.md` frontmatter — add `preceded_by: adoption`
- [x] 2.6 Update `workflows/legacy-rescue-rewrite.md` frontmatter — add `preceded_by: adoption`

---

## Phase 3 — Adoption Prompt

- [x] 3.1 Create `docs/guides/prompts/adoption-workflow-prompt.md` — single copy-paste Copilot Chat prompt that auto-detects scenario (fresh / stale / openspec migration) and runs the adoption workflow
- [x] 3.2 Include three labelled variants in the prompt file: (a) fresh adoption, (b) update existing adoption, (c) migrate from openspec/
- [x] 3.3 Update `docs/guides/adoption/how-to-adopt-constitution.md` — add section at top pointing to the new workflow as the authoritative path; mark old bootstrap prompt as legacy

---

## Phase 4 — Validation

- [x] 4.1 Run `aa-constitution-lint . --constitution .` — verify 0 failures after all workflow and doc changes
- [x] 4.2 Manually verify adoption workflow covers Jay's scenario: repo with `AGENTS.md` + old brownfield guide + `openspec/` → clean transition to `hangar-ai-specs/` with no deletions
- [x] 4.3 Update `PROGRESS.md` to COMPLETE
- [x] 4.4 Commit and push hangar-ai-constitution changes to main

---

## Phase 5 — Workshop Repo (`hangar-ai-constitution-workflows`)

> Updates to `/Users/aali/repos/american-airlines/governance/hangar-ai-constitution-workflows`
> These changes are additive — no existing exercises are removed, only updated to reference the new workflow.

- [x] 5.1 Add **Exercise 0: Constitutional Adoption** to `exercises/part-1-decision-track-exercises.html`
  - Placed before the existing Exercise 1 (Archaeology)
  - Content: run the adoption workflow prompt against the sample codebase (`sample-codebase/`); verify `AGENTS.md` + `hangar-ai-specs/` created; confirm linter passes — then proceed to decision track
  - Law citations: ENG-1.2, ENG-11.1

- [x] 5.2 Update `exercises/prompt-guide.html` — replace the "Setup / Adoption" prompt section
  - Remove reference to `docs/guides/adoption/brownfield-adoption.md`
  - Replace with the new adoption workflow prompt from `docs/guides/prompts/adoption-workflow-prompt.md`
  - Add the three variant prompts (fresh / update / migrate from openspec) as labelled blocks
  - Add expected output: `AGENTS.md` created, `hangar-ai-specs/` initialised, linter passes

- [x] 5.3 Update `instructor/instructor-guide.html` — add "Phase 0: Adoption Workflow" section
  - Timing: 10 minutes at start of Part 1 before Exercise 1
  - Instructor note: explain that the adoption workflow is a conditional Phase 0 — once passed it skips on subsequent workflows; participants will see this in practice during the refactor/rewrite tracks

- [x] 5.4 Update `index.html` workshop landing page
  - Add adoption workflow callout card in the "What You'll Learn" section
  - Link to `exercises/part-1-decision-track-exercises.html#exercise-0`

- [x] 5.5 Commit and push workshop repo changes to main

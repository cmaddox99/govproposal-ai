# Tasks: Enrich Product Discovery Stage A–F Workflow

> **Change:** `enrich-product-discovery-stage-a-f`
> **Proposal:** `hangar-ai-specs/changes/enrich-product-discovery-stage-a-f/PROPOSAL.md`
> **Status:** In Progress — 23 deliverables, ~58 tasks
> **Scope:** Original 5 gaps (Jay / turp-aa) + Gap 6 (adeel-ali-aa) + human amendments Q4 + Q5
> **Ensemble Deliberation:** `ensemble-pr31-gap6-2026-04-15` — APPROVED WITH CONDITIONS
> **Protocol:** ENG-4.1 Atomic TDD — one failing test → green → refactor → verify → commit → STOP
> **Lint/RAG baseline:** Run `aa-constitution-lint .` before starting to capture baseline

---

## Phase 0 — Scope Update (this commit)

- [x] 0.1 Update `PROPOSAL.md` to 23-deliverable scope — Gap 6 + human amendments Q4/Q5 incorporated
- [x] 0.2 Update `tasks.md` to full ~58-task scope — all phases and TDD cycles defined
- [x] 0.3 Commit: `docs(specs): update enrich-product-discovery-stage-a-f scope — 23 deliverables, Gap 6 + Q4/Q5 amendments`

---

## Phase 1 — Housekeeping: Establish Baseline

- [x] 1.1 Run `aa-constitution-lint .` → record baseline pass/fail count in `PROGRESS.md`
- [x] 1.2 Confirm no pre-existing failures in `product-discovery-stage-a-f.md` or `product-discovery-orchestration.md`
- [x] 1.3 Run RAG eval → record baseline score for product-discovery routing queries
- [x] 1.4 Commit baseline note: `chore(baseline): record aa-constitution-lint + RAG baseline before enrich-product-discovery-stage-a-f`

---

## Phase 2 — D17: ENG-13.1 Global Law Amendment (HIGHEST PRIORITY — Elena condition)

RED: Write a lint/schema test that asserts `ENG-13.1` `non_negotiable: true` in `laws/engineering/artifact-rendering.md`

- [x] 2.1 RED — add test `tests/laws/test_eng13_non_negotiable.py`: assert `artifact-rendering.md` YAML frontmatter has `non_negotiable: true` for ENG-13.1 and no mention of "30-day" in ENG-13.1 body text
- [x] 2.2 GREEN — amend `laws/engineering/artifact-rendering.md`:
  - Change ENG-13.1 YAML field `non_negotiable: false` → `non_negotiable: true`; remove `recommended: true`
  - Remove the sentence *"(promoted to NON-NEGOTIABLE after 30-day adoption window)"* from law status line and body text
  - Update ENG-13.1 status line to: `**Law ID:** \`ENG-13.1\` | **Status:** NON-NEGOTIABLE`
- [x] 2.3 REFACTOR — add a "Constitutional Change Record" block below the law title noting the amendment date and deliberation reference (`ensemble-pr31-gap6-2026-04-15`)
- [x] 2.4 VERIFY — run test + `aa-constitution-lint .` → 0 new failures
- [ ] 2.5 Commit: `feat(laws): elevate ENG-13.1 to NON-NEGOTIABLE globally — remove 30-day adoption window (ensemble-pr31-gap6-2026-04-15) [enrich-product-discovery-stage-a-f]`

---

## Phase 3 — D15: Update stage-transition-audit-event.yaml

RED: Write a YAML schema test that asserts required new fields exist

- [ ] 3.1 RED — add test `tests/templates/test_audit_event_schema.py`: assert `stage-transition-audit-event.yaml` contains fields: `schema_version`, `discovery_mode`, `human_browser_review.reviewer_name`, `human_browser_review.reviewer_role`, `human_browser_review.review_timestamp`, `human_browser_review.decision`, `human_browser_review.enhancement_round`
- [ ] 3.2 GREEN — update `tools/templates/product-discovery/stage-transition-audit-event.yaml`:
  - Add `schema_version: "1.1"` immediately after `discovery_id`
  - Add `discovery_mode: exploratory  # exploratory | accelerated` after `schema_version`
  - Update `evidence_artifact` comment to reference `stage-[X]-evidence.md` naming convention
  - Add `human_browser_review:` block with `reviewer_name`, `reviewer_role`, `review_timestamp`, `decision: APPROVE | REJECT | ENHANCE`, `enhancement_round: 0  # max 3 per stage`
  - Update `law_citations` to include `ENG-13.1`
- [ ] 3.3 REFACTOR — add inline comments explaining enhancement_round semantics; update YAML header comment block with schema version changelog
- [ ] 3.4 VERIFY — run test + `aa-constitution-lint .`
- [ ] 3.5 Commit: `feat(templates): update stage-transition-audit-event.yaml — schema_version, discovery_mode, human_browser_review block (BUS-7.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 4 — D18: Update stage-a-proposal.md (mode selection + Tier rubric)

RED: Write a template completeness test asserting new required blocks

- [ ] 4.1 RED — add test `tests/templates/test_stage_a_template.py`: assert `stage-a-proposal.md` frontmatter includes `discovery_mode` and `tier` fields; body contains `## Mode Selection`, `## Tier Complexity Rubric`, and `## Per-Stage Reviewer` sections
- [ ] 4.2 GREEN — update `tools/templates/product-discovery/stage-a-proposal.md`:
  - Add `discovery_mode: exploratory  # exploratory | accelerated` to YAML frontmatter
  - Add `tier: 1  # 1 = simple ≤1 service | 2 = complex 3+ services` to frontmatter
  - Add `## Mode Selection` section at top of body with Exploratory vs Accelerated criteria table; validation citation fields for Accelerated mode; agent flag note for non-PRD-2.1-validated sources
  - Add `## Tier Complexity Rubric` section with 5-question rubric (service count, data flows, stakeholder groups, external integrations, ADO backlog size)
  - Add per-stage reviewer role table to `## Exit Gate Checklist` (both modes, all 6 stages)
  - Update exit gate checklist to include: `[ ] Evidence rendered as HTML via render-package.sh`, `[ ] HTML opened in browser`, `[ ] Human reviewer APPROVED`, `[ ] human_browser_review block populated in audit event`
- [ ] 4.3 REFACTOR — ensure all `<PLACEHOLDER>` fields are updated for the new sections; improve inline guidance comments
- [ ] 4.4 VERIFY — run tests + `aa-constitution-lint .`
- [ ] 4.5 Commit: `feat(templates): update stage-a-proposal.md — mode selection, Tier rubric, per-stage reviewer roles, HTML gate (ENG-13.1, PRD-2.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 5 — D19: stage-b-field-study.md

- [ ] 5.1 RED — add test `tests/templates/test_stage_b_template.py`: assert file exists; frontmatter has `stage: B`; body contains `## Entry Gate`, `## Field Study Findings`, `## Persona Insights`, `## Domain Model`, `## Exit Gate Checklist`, `## Audit Log`
- [ ] 5.2 GREEN — create `tools/templates/product-discovery/stage-b-field-study.md`:
  - YAML frontmatter: stage B, laws (PRD-2.3, PRD-2.4, PRD-3.1, PRD-3.2, BUS-7.1, ENG-13.1), extends `docs/templates/enrichment/02-persona-validation.md` + `04-domain-model-inventory.md`
  - `## Entry Gate` checklist (Stage A exit gate met)
  - `## Market Research & Competitive Analysis` (PRD-2.4)
  - `## User Interviews` (PRD-3.1 — ≥3 users; JTBD framing per PRD-2.3)
  - `## Persona Insights` (extends 02-persona-validation; ≥3 validated insights)
  - `## Domain Model` (extends 04-domain-model-inventory)
  - `## Exit Gate Checklist` (≥3 validated insights, competitive landscape, HTML render gate, human APPROVE)
  - `## Audit Log` BUS-7.1 block with `aa-artifact-render` invocation
  - Reviewer role: Product Owner + ≥1 domain expert (both modes)
- [ ] 5.3 VERIFY — run tests + lint
- [ ] 5.4 Commit: `feat(templates): add stage-b-field-study.md evidence template (PRD-2.3, PRD-3.1, ENG-13.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 6 — D20: stage-c-code-evidence.md

- [ ] 6.1 RED — add test `tests/templates/test_stage_c_template.py`: assert file exists; frontmatter `stage: C`; body contains `## Codebase Assessment`, `## Domain Model Extraction`, `## Tech Debt Inventory`, `## Exit Gate Checklist`, `## Audit Log`
- [ ] 6.2 GREEN — create `tools/templates/product-discovery/stage-c-code-evidence.md`:
  - YAML frontmatter: stage C, laws (ENG-3.1, ENG-6.7, BUS-7.1, ENG-13.1), extends `docs/templates/enrichment/03-codebase-assessment.md`
  - `## Entry Gate` checklist (Stage B exit gate met)
  - `## Repository Ingestion` (repos assessed, tooling used)
  - `## Codebase Assessment` (extends 03-codebase-assessment)
  - `## Domain Model Extraction` (bounded contexts, key entities)
  - `## Tech Debt Inventory` (ENG-3.1 critical findings list; unreviewed critical findings block)
  - `## Exit Gate Checklist` (evidence report exists, no unreviewed critical findings, HTML render gate, human APPROVE)
  - `## Audit Log` BUS-7.1 block; reviewer: Engineering Lead + Product Owner (both modes)
- [ ] 6.3 VERIFY — run tests + lint
- [ ] 6.4 Commit: `feat(templates): add stage-c-code-evidence.md evidence template (ENG-3.1, ENG-6.7, ENG-13.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 7 — D21: stage-d-validation.md

- [ ] 7.1 RED — add test `tests/templates/test_stage_d_template.py`: assert file exists; frontmatter `stage: D`; body contains `## DVFT Matrix`, `## Assumption Map`, `## Blocker Resolution Log`, `## Exit Gate Checklist`, `## Audit Log`
- [ ] 7.2 GREEN — create `tools/templates/product-discovery/stage-d-validation.md`:
  - YAML frontmatter: stage D, laws (PRD-2.2, PRD-2.1, BUS-7.1, ENG-13.1) — no enrichment source (new)
  - `## Entry Gate` checklist (Stage C exit gate met)
  - `## DVFT Matrix` (Design / Validate / Feasibility / Technical — 4-column table with stakeholder sign-off columns)
  - `## Assumption Map` (PRD-2.2 — assumptions, confidence level, validation method, outcome)
  - `## Problem Re-validation` (PRD-2.1 check — confirm problem statement still holds after C evidence)
  - `## Blocker Resolution Log` (blocker, raised by, resolution, date resolved)
  - `## Exit Gate Checklist` (all blockers resolved, DVFT complete, HTML render gate, human APPROVE)
  - `## Audit Log` BUS-7.1 block; reviewer: Full DVFT stakeholder group (both modes)
- [ ] 7.3 VERIFY — run tests + lint
- [ ] 7.4 Commit: `feat(templates): add stage-d-validation.md evidence template — DVFT matrix (PRD-2.2, BUS-7.1, ENG-13.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 8 — D22: stage-e-metrics.md

- [ ] 8.1 RED — add test `tests/templates/test_stage_e_template.py`: assert file exists; frontmatter `stage: E`; body contains `## Success Metrics`, `## Baselines`, `## PMF Targets`, `## Exit Gate Checklist`, `## Audit Log`
- [ ] 8.2 GREEN — create `tools/templates/product-discovery/stage-e-metrics.md`:
  - YAML frontmatter: stage E, laws (PRD-6.1, ENG-10.1, BUS-7.1, ENG-13.1), extends `docs/templates/enrichment/01-metrics-collection.md`
  - `## Entry Gate` checklist (Stage D exit gate met)
  - `## Success Metrics` (extends 01-metrics-collection; metric name, type, formula, data source)
  - `## Baselines` (current state measurements)
  - `## PMF Targets` (PRD-6.1 — Product-Market Fit targets, timeframe, measurability confirmation)
  - `## Instrumentation Plan` (ENG-10.1 — tooling, event names, owner)
  - `## Exit Gate Checklist` (metrics spec exists, measurability confirmed, HTML render gate, human APPROVE)
  - `## Audit Log` BUS-7.1 block; reviewer: Product Owner + Finance/Analytics representative (both modes)
- [ ] 8.3 VERIFY — run tests + lint
- [ ] 8.4 Commit: `feat(templates): add stage-e-metrics.md evidence template (PRD-6.1, ENG-10.1, ENG-13.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 9 — D23: stage-f-roadmap.md

- [ ] 9.1 RED — add test `tests/templates/test_stage_f_template.py`: assert file exists; frontmatter `stage: F`; body contains `## Now/Next/Later Roadmap`, `## Vertical Slices`, `## Implementation Proposal`, `## Exit Gate Checklist`, `## Audit Log`
- [ ] 9.2 GREEN — create `tools/templates/product-discovery/stage-f-roadmap.md`:
  - YAML frontmatter: stage F, laws (PRD-4.1, PRD-4.2, ENG-11.1, BUS-7.1, ENG-13.1), extends `docs/templates/enrichment/05-agentic-workflow-discovery.md`
  - `## Entry Gate` checklist (Stage E exit gate met)
  - `## Now/Next/Later Roadmap` (PRD-4.2 — outcome framing per PRD-4.1; Now/Next/Later columns)
  - `## Agentic Workflow Opportunities` (extends 05-agentic-workflow-discovery)
  - `## Vertical Slices` (slice ID, outcome, acceptance criteria, dependencies, stage-ready?)
  - `## Implementation Proposal Reference` (link to `hangar-ai-specs/changes/[impl-id]/PROPOSAL.md`)
  - `## Exit Gate Checklist` (roadmap approved, impl proposal scaffolded, audit event logged, HTML render gate, human APPROVE)
  - `## Audit Log` BUS-7.1 block; reviewer: Executive Sponsor + Product Owner (both modes)
- [ ] 9.3 VERIFY — run tests + lint
- [ ] 9.4 Commit: `feat(templates): add stage-f-roadmap.md evidence template (PRD-4.1, PRD-4.2, ENG-13.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 10 — D13: discovery-package-index.md

- [ ] 10.1 RED — add test `tests/templates/test_package_index.py`: assert `discovery-package-index.md` exists; contains Tier 1 and Tier 2 manifests; each has required/optional/deferred columns
- [ ] 10.2 GREEN — create `tools/templates/product-discovery/discovery-package-index.md`:
  - Header: discovery_id, tier, mode, declared_at (Stage A)
  - `## Tier 1 Package Manifest` (simple, ≤1 service): discovery-guide, worksheets 01–03, forward-roadmap, slice-1-ready-brief — each with status (required / optional / deferred)
  - `## Tier 2 Package Manifest` (complex, 3+ services): full service-recovery model — all worksheets 01–05 + executive-briefing-deck + discovery-guide + forward-roadmap + slice-1-ready-brief + ado-gap-analysis-brief (optional) + discovery-prompt-guide (optional)
  - `## Artifact Naming Convention` (stage-[X]-evidence.md per stage; worksheet-0N-*.html for worksheets)
  - Reference: `aa-hangar-labs/discovery-packages/service-recovery/complex-disruption-scenarios/` as Tier 2 exemplar
- [ ] 10.3 VERIFY — run tests + lint
- [ ] 10.4 Commit: `feat(templates): add discovery-package-index.md — Tier 1 + Tier 2 manifests (ENG-11.1, PRD-2.5) [enrich-product-discovery-stage-a-f]`

---

## Phase 11 — D16: render-package.sh

- [ ] 11.1 RED — add test `tests/templates/test_render_script.py`: assert `render-package.sh` is executable; contains `aa-artifact-render` invocation; handles `--stage` argument; includes `open` (macOS) and `xdg-open` (Linux) browser opening logic
- [ ] 11.2 GREEN — create `tools/templates/product-discovery/render-package.sh`:
  - Shebang `#!/usr/bin/env bash`
  - Usage: `./render-package.sh [stage|all] [discovery-id]`
  - For each stage A–F: `aa-artifact-render hangar-ai-specs/changes/[id]/stage-[X]-evidence.md --artifact-type evidence --laws-dir laws`
  - `--stage A` renders only Stage A artifact; `all` renders all 6
  - After render: detect OS (`uname`); `open` on Darwin, `xdg-open` on Linux, warning on other
  - Exit code propagation: fail if `aa-artifact-render` fails
  - `--help` flag with usage text
- [ ] 11.3 REFACTOR — add `set -euo pipefail`; inline comments for each major block; ensure idempotent (re-running does not fail if HTML already exists)
- [ ] 11.4 VERIFY — run tests + lint; test script is executable (`chmod +x`)
- [ ] 11.5 Commit: `feat(templates): add render-package.sh — full discovery package render + browser open (ENG-13.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 12 — D1–D6, D9–D12: Workflow Amendments (product-discovery-stage-a-f.md)

- [ ] 12.1 RED — add test `tests/workflows/test_product_discovery_workflow.py`:
  - Assert Stage A row contains `disc-YYYY-NNN` format reference
  - Assert Stage A row mentions avatar activation record
  - Assert Stage A row mentions `Director+` approval authority
  - Assert all stage exit gates mention HTML render and human APPROVE
  - Assert `## Stage A Detail` section exists with Discovery ID, Avatar Activation, Approval Authority, and Two-Mode subsections
  - Assert `## Per-Stage Reviewer Role Table` exists with both modes
  - Assert Governance Rules mentions Audit Event Contract
  - Assert evidence naming convention `stage-[X]-evidence.md` appears for each stage

- [ ] 12.2 GREEN — amend `workflows/product-discovery-stage-a-f.md`:
  - **D1/D9:** Update Stage A row in Stage Table:
    - Key Activities: *"Assign Discovery ID (disc-YYYY-NNN); activate constitution; record avatar activation; select discovery mode (Exploratory / Accelerated); declare Tier (1 / 2)"*
    - Exit Gate: *"Problem statement approved by named Product Owner or Discovery Sponsor (Director+); PROPOSAL.md scaffolded from template; avatars activated and recorded; stage-a-evidence.md rendered as HTML + human APPROVED; BUS-7.1 audit event filed"*
  - **D3:** Add avatar activation requirement to Stage A Key Activities and exit gate
  - **D5:** Add approval authority (Director+, self-cert PROHIBITED) to Stage A exit gate
  - **D11/D12:** Update ALL six stage rows (B–F) exit gates to include: *"stage-[X]-evidence.md rendered as HTML + human reviewer APPROVED"*
  - **D10:** Add `## Stage A Detail` section (after Stage Table, before Governance Rules) with:
    - `### Discovery ID` — disc-YYYY-NNN format, rules, example
    - `### Discovery Mode` — Exploratory vs Accelerated criteria, validation citation requirement
    - `### Tier Selection` — Tier 1 / Tier 2 criteria, package manifest reference
    - `### Avatar Activation Record` — fields required in PROPOSAL.md §Participating Avatars
    - `### Approval Authority` — required role, capture method, rejection path, self-cert PROHIBITED
    - `### HTML Evidence Gate` — ENG-13.1 NON-NEGOTIABLE; render-package.sh reference; APPROVE/REJECT/ENHANCE protocol; max 3 enhancement rounds
    - `### Stage A → B Audit Event` — reference to stage-transition-audit-event.yaml template
  - **D10 (cont):** Add `## Per-Stage Reviewer Role Table` section (dual-column: Exploratory + Accelerated)
  - **Governance Rules:** Add Audit Event Contract paragraph (NON-NEGOTIABLE)
  - **Governance Rules:** Add ENG-13.1 rendering requirement (NON-NEGOTIABLE)
  - Add 🎨 render hints for all 6 stages referencing render-package.sh

- [ ] 12.3 REFACTOR — ensure consistent formatting; verify all NON-NEGOTIABLE laws are marked ⛔; remove the duplicate 🎨 hints that were at the bottom of the original file
- [ ] 12.4 VERIFY — run tests + `aa-constitution-lint .`
- [ ] 12.5 Commit: `feat(workflows): enrich product-discovery-stage-a-f — Discovery ID, two modes, Tier selection, avatar activation, approval authority, A–F HTML gates, per-stage reviewer table (PRD-2.5, BUS-7.1, ENG-11.1, ENG-13.1) [enrich-product-discovery-stage-a-f]`

---

## Phase 13 — D2, D4, D6, D14: Skill Amendments (product-discovery-orchestration.md)

- [ ] 13.1 RED — add test `tests/skills/test_product_discovery_skill.py`:
  - Assert YAML frontmatter `laws.implements` includes `ENG-13.1`
  - Assert `§Discovery ID Naming Convention` section exists
  - Assert `§Initialize Discovery` mentions `disc-YYYY-NNN`, avatar activation record, approval authority, template reference, mode selection
  - Assert `§Gate Each Transition` checklist includes HTML render gate item, human APPROVE item, enhancement round cap item
  - Assert `§HTML Render Gate` section exists with APPROVE/REJECT/ENHANCE protocol

- [ ] 13.2 GREEN — amend `agent-skills/skills-by-domain/discovery-research/product-discovery-orchestration.md`:
  - Add `ENG-13.1` and `ENG-1.2` to `laws.implements` block in YAML frontmatter
  - Add `§Discovery ID Naming Convention` section (format, rules, example) before §Initialize Discovery
  - Expand `§Initialize Discovery`:
    - Step 0: Select discovery mode (Exploratory / Accelerated); flag non-validated sources in Accelerated mode
    - Step 0a: Declare Tier (1 / 2) using complexity rubric
    - Step 1 (existing): Create PROPOSAL.md using `tools/templates/product-discovery/stage-a-proposal.md`
    - Step 1a (new): Assign Discovery ID — `disc-YYYY-NNN` before creating spec folder
    - Step 1b (new): Record avatar activation in PROPOSAL.md §Participating Avatars
    - Step 4a (new): Record stakeholder approval — named approver must be Director+; self-cert PROHIBITED
  - Add `§HTML Render Gate` section: invoke render-package.sh → open browser → APPROVE/REJECT/ENHANCE → max 3 rounds → log each round
  - Update `§Gate Each Transition` checklist:
    - `[ ] Stage evidence artifact exists as stage-[X]-evidence.md`
    - `[ ] Evidence rendered as HTML via render-package.sh`
    - `[ ] HTML opened in user's browser`
    - `[ ] Human reviewer decision = APPROVE (max 3 ENHANCE rounds)`
    - `[ ] human_browser_review block populated in BUS-7.1 audit event`
    - `[ ] Audit event schema_version = "1.1"; discovery_mode set`
    - `[ ] Audit event filed in PROPOSAL.md §Audit Log`
    - `[ ] Audit event matches structure in stage-transition-audit-event.yaml`
  - Update Quality Checklist with new items for all additions

- [ ] 13.3 REFACTOR — consolidate the Surface Laws Per Stage table to include ENG-13.1 for every stage; review ordering of sections for logical flow
- [ ] 13.4 VERIFY — run tests + `aa-constitution-lint .`
- [ ] 13.5 Commit: `feat(skills): enrich product-discovery-orchestration — Discovery ID, two modes, avatar activation, approval authority, HTML render gate, enhanced gate checklist (PRD-2.5, BUS-7.1, ENG-13.1, ENG-1.2) [enrich-product-discovery-stage-a-f]`

---

## Phase 14 — Validation and Retrospective

- [ ] 14.1 Apply amended workflow to `gate-mgmt` disc-2026-001 Stage A — re-run checklist using enriched workflow and templates; confirm all 6 gaps are now addressed
- [ ] 14.2 Verify 6 gaps closed:
  - [ ] Gap 1: disc-2026-001 uses compliant `disc-2026-001` ID format
  - [ ] Gap 2: PROPOSAL.md §Participating Avatars is populated
  - [ ] Gap 3: PROPOSAL.md §Stakeholder Approval has named Director+ approver
  - [ ] Gap 4: PROPOSAL.md was created from stage-a-proposal.md template — all sections present including mode selection and Tier rubric
  - [ ] Gap 5: PROPOSAL.md §Audit Log has a structured entry matching stage-transition-audit-event.yaml v1.1
  - [ ] Gap 6: stage-a-evidence.md rendered as HTML, opened in browser, human APPROVED recorded in human_browser_review block
- [ ] 14.3 Run `aa-constitution-lint .` → final pass: ≥ baseline PASS count; 0 regressions
- [ ] 14.4 Run RAG eval → product-discovery routing ≥ baseline score
- [ ] 14.5 Verify D17: `laws/engineering/artifact-rendering.md` ENG-13.1 correctly marked NON-NEGOTIABLE; 30-day window removed
- [ ] 14.6 Verify render-package.sh renders all 6 stage artifacts end-to-end on macOS
- [ ] 14.7 Update this `tasks.md` with final commit hashes and scores
- [ ] 14.8 Commit: `test(validation): enrich-product-discovery-stage-a-f — all 6 gaps closed, lint + RAG pass [enrich-product-discovery-stage-a-f]`

---

## Phase 15 — Archive

- [ ] 15.1 Update `PROPOSAL.md` Status field to `COMPLETE`
- [ ] 15.2 Move `hangar-ai-specs/changes/enrich-product-discovery-stage-a-f/` → `hangar-ai-specs/archive/2026-04-15-enrich-product-discovery-stage-a-f/`
- [ ] 15.3 Update `hangar-ai-specs/README.md` — move from Active Proposals to Archived
- [ ] 15.4 Update `workflows/README.md` — add entry for `product-discovery-stage-a-f` with templates directory reference
- [ ] 15.5 Commit: `feat(archive): enrich-product-discovery-stage-a-f complete — 6 gaps closed, 23 deliverables (BUS-7.1) [enrich-product-discovery-stage-a-f]`
- [ ] 15.6 Push

---

## Progress Summary

| Phase | Total Tasks | Done | Remaining |
|-------|-------------|------|-----------|
| 0. Scope update | 3 | 3 | 0 |
| 1. Housekeeping | 4 | 0 | 4 |
| 2. D17 — Law amendment | 5 | 0 | 5 |
| 3. D15 — Audit event YAML | 5 | 0 | 5 |
| 4. D18 — Stage A template update | 5 | 0 | 5 |
| 5. D19 — Stage B template | 4 | 0 | 4 |
| 6. D20 — Stage C template | 4 | 0 | 4 |
| 7. D21 — Stage D template | 4 | 0 | 4 |
| 8. D22 — Stage E template | 4 | 0 | 4 |
| 9. D23 — Stage F template | 4 | 0 | 4 |
| 10. D13 — Package index | 4 | 0 | 4 |
| 11. D16 — Render script | 5 | 0 | 5 |
| 12. D1–D12 — Workflow amendments | 5 | 0 | 5 |
| 13. D2,D4,D6,D14 — Skill amendments | 5 | 0 | 5 |
| 14. Validation & retro | 8 | 0 | 8 |
| 15. Archive | 6 | 0 | 6 |
| **Total** | **75** | **3** | **72** |

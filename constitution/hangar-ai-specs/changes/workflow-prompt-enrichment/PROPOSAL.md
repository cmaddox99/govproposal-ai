# Proposal: Workflow Prompt Enrichment

**Proposal ID:** `workflow-prompt-enrichment`
**Submitted:** 2026-04-09
**Status:** PROPOSED
**Laws:** ENG-11.1 (NON-NEGOTIABLE), ENG-1.2, ENG-10.1

---

## Problem

### 1. Two-Generation Gap in Workflow Richness

The constitution's workflows exist in two very different generations:

| Workflow | Lines | Step-by-step guidance | Copilot prompts | Evidence templates | Failure modes |
|----------|-------|-----------------------|-----------------|-------------------|---------------|
| `adoption.md` | 429 | ✅ Full (3 phases × 3-5 steps each) | ✅ Embedded per step | ✅ YAML templates | ✅ Table |
| `legacy-rescue-decision-track.md` | 55 | ❌ Phase table only | ❌ None | ❌ None | ❌ None |
| `legacy-rescue-refactor.md` | 54 | ❌ Phase table only | ❌ None | ❌ None | ❌ None |
| `legacy-rescue-rewrite.md` | 68 | ❌ Phase table only (+ build cycle template) | ❌ None | ❌ None | ❌ None |
| `greenfield-development.md` | 56 | ❌ Phase table only | ❌ None | ❌ None | ❌ None |

The `adoption.md` workflow was recently (April 2026) enriched to 429 lines with complete step-by-step agent guidance, Copilot-ready prompts, terminal commands, evidence artifact templates, and a failure modes table. This is now the canonical workflow standard. The legacy-rescue and greenfield workflows have not yet been brought to this standard.

An engineer opening `legacy-rescue-refactor.md` today can read the phase gates (WHAT to achieve) but receives no guidance on HOW to execute each phase with GitHub Copilot — what to prompt, what files to load, what to commit as evidence, or how to recover from failures.

### 2. Prompt Guidance Lives in the Wrong Repo

The only comprehensive Copilot prompt guide for the legacy-rescue workflows currently exists in `hangar-ai-constitution-workflows/exercises/prompt-guide.html` (52KB HTML, 17 exercises). That file is:

- **Tightly coupled** to the `loyalty-accrual` / `loyalty-tiers` sample codebase
- **HTML format** — not the constitution's native markdown
- **Training-specific** — written for workshop exercises, not general adoption
- **In a separate repo** — engineers who haven't attended the workshop don't know it exists

The constitution itself should be self-sufficient: if someone opens a legacy-rescue workflow, the governance document should tell them exactly how to engage Copilot for each phase.

### 3. No Governed Authoring Process for New Workflows

The constitution currently has:
- A process for adopting the constitution (`adoption.md`)
- A process for building features (`greenfield-development.md`)
- A process for rescuing legacy code (`legacy-rescue-*.md`)

But **no governed process for authoring a new workflow**. When a team wants to contribute a new workflow to the constitution, they have no skill or template defining:
- Required frontmatter schema
- Mandatory sections (prerequisites, phase table, per-phase guidance, failure modes)
- How to embed Copilot prompt sections
- How to register in `workflows/README.md`
- How to write the SDD proposal

This creates inconsistency — every new workflow author starts from scratch and produces different quality levels.

### 4. Pre-existing Lint Failures from Recent Pull

The April 2026 pull introduced 2 lint failures:
- `ENG-12.1` has `non_negotiable: true` in its law file but is not listed in `laws/index.yaml`'s `non_negotiable` array
- (One additional lint failure — verify by running `aa-constitution-lint .` at start of implementation)

These must be fixed before any new work is merged.

---

## Proposed Solution

### Decision: Inline Enrichment, Not Separate Prompt Files

The question of *where* prompt guides live has a clear answer from the `adoption.md` precedent: **embed per-phase guidance directly in the workflow file**. The alternative — a separate `workflows/prompts/` subdirectory — would split governance (what the phase requires) from usage (how to execute the phase), creating two sources of truth.

`adoption.md` establishes the canonical pattern: one self-contained markdown file per workflow that includes all phases, all step-by-step guidance, all Copilot prompts, and all evidence templates. We follow this pattern.

**No `prompts/` subdirectory. No HTML files. Inline markdown, consistent with `adoption.md`.**

### Change 1: Fix Pre-existing Lint Failures (Housekeeping)

Add `ENG-12.1` to `laws/index.yaml`'s `non_negotiable` array. Fix any other failures uncovered by the baseline scan. Zero lint failures before any workflow enrichment begins.

### Change 2: Create `skill-workflow-authoring` (Meta-Skill First)

Before enriching the workflow files, codify the workflow file format as a governed skill. This ensures the enriched workflows are authored against a defined contract — and future workflow authors have a clear template.

**Location:** `agent-skills/skills-by-domain/development-practices/`

**Skill defines:**
- Required frontmatter fields (`workflow.id`, `name`, `avatar_context`, `laws`, `skills`, `preceded_by`)
- Mandatory sections: Prerequisites, Phase Table, Per-Phase Detail Sections, Failure Modes
- Copilot prompt block format per phase (environment setup → per-phase prompts → evidence prompts → recovery prompts)
- Evidence artifact template format (YAML frontmatter)
- How to register the workflow in `workflows/README.md`
- How to write the SDD proposal for a new workflow

### Change 3: Enrich `legacy-rescue-decision-track.md`

Expand from 55 lines to `adoption.md`-scale richness. Add for each of the 6 phases:
- **Step-by-step instructions** specific to the decision-track context (bounded context mapping, SonarQube per-context baseline, REFACTOR/REWRITE deliberation, ADR filing)
- **Copilot-ready prompts** with file load sequences (which constitution files to attach, which workflow file to reference)
- **Evidence artifact templates** (bounded-context-map.md, violation-inventory.md, decision-matrix.md, adr.md)
- **Failure modes table** (no matching bounded contexts, SonarQube baseline not comparable, deadlocked deliberation)
- **ENG-12.1 compliance** — human dashboard review checkpoints per phase gate

### Change 4: Enrich `legacy-rescue-refactor.md`

Expand from 54 lines. Add for each of the 6 phases:
- **Step-by-step instructions** (characterization test strategy, violation priority ordering, Boy Scout commits, complexity measurement)
- **Copilot-ready prompts** with specific prompts for characterization tests (ENG-4.1 atomic TDD), security remediation (ENG-6.1), and audit trail implementation (ENG-6.7)
- **Evidence artifact templates** (characterization-coverage.md, remediation-log.md, sonarqube-delta.md)
- **Failure modes table** (characterization tests reveal unknown behavior, P0 violations block refactor, complexity won't reduce)
- **Build cycle template** (analogous to the rewrite track's cycle template, adapted for refactoring)

### Change 5: Enrich `legacy-rescue-rewrite.md`

Expand from 68 lines. The Build Cycle Template already exists — extend the rest of the file:
- **Step-by-step instructions** (behavioral contract extraction, golden-file generation, parity test strategy, decommission planning)
- **Copilot-ready prompts** with specific prompts for specification extraction, golden-file test generation, parity validation, and regulatory documentation
- **Evidence artifact templates** (behavioral-contracts.md, golden-files/, parity-report.md, decommission-plan.md)
- **Failure modes table** (golden-file mismatch > 5%, intentional divergence disagreement, legacy decommission blocked)
- **ENG-12.3 compliance** — external referee (SonarQube) citations per phase

### Change 6: Update `workflows/README.md`

- Add a **Workflow File Format** section documenting the canonical structure (derived from `skill-workflow-authoring`)
- Add a **Prompt Guide** column to the workflow index table (documenting that prompts are embedded inline)
- Add a link from each workflow entry to its phase-1 prompt anchor

### Change 7: Add RAG Test Cases

Add 6 RAG test cases (`tc-wf-001`..`tc-wf-006`) covering:
- Decision-track workflow routing on archaeology/deliberation queries
- Refactor-track routing on characterization/remediation queries
- Rewrite-track routing on parity/golden-file queries

---

## Files To Create / Modify

| File | Change | Law |
|------|--------|-----|
| `laws/index.yaml` | Add ENG-12.1 to `non_negotiable` list | ENG-10.1 |
| `agent-skills/skills-by-domain/development-practices/skill-workflow-authoring.md` | **CREATE** | ENG-11.1 |
| `agent-skills/skills-by-domain/development-practices/index.yaml` | Add workflow-authoring entry | ENG-10.1 |
| `workflows/legacy-rescue-decision-track.md` | Expand with per-phase guidance + prompts | ENG-11.1 |
| `workflows/legacy-rescue-refactor.md` | Expand with per-phase guidance + prompts | ENG-11.1 |
| `workflows/legacy-rescue-rewrite.md` | Expand with per-phase guidance + prompts | ENG-11.1 |
| `workflows/README.md` | Add workflow format section + prompt guide column | ENG-11.1 |
| `tools/rag-eval/test-cases/workflows.yaml` | Add tc-wf-001..tc-wf-006 | ENG-10.1 |

---

## What Is Out of Scope

- `greenfield-development.md` enrichment — follows naturally from this proposal's pattern but is deferred
- `product-discovery-stage-a-f.md` enrichment — deferred
- HTML prompt guide format — rejected; markdown inline is the canonical pattern
- Separate `workflows/prompts/` subdirectory — rejected; inline per `adoption.md` precedent

---

## Acceptance Criteria

- [ ] `aa-constitution-lint .` → **0 failures** (pre-existing failures fixed in Phase 1)
- [ ] `legacy-rescue-decision-track.md` — has all 6 phases with step-by-step guidance and Copilot prompts
- [ ] `legacy-rescue-refactor.md` — has all 6 phases with step-by-step guidance and Copilot prompts
- [ ] `legacy-rescue-rewrite.md` — has all 6 phases with step-by-step guidance and Copilot prompts
- [ ] `skill-workflow-authoring.md` created and registered in `index.yaml`
- [ ] RAG eval → ≥ 90.0% PASS (no regression from 90.4% baseline)
- [ ] Each workflow's prompts tested manually against the `sample-codebase/loyalty-*` modules in `hangar-ai-constitution-workflows/`
- [ ] `workflows/README.md` updated with Workflow File Format section

---

## Relationship to Workshop Repo

This proposal makes the constitution **self-sufficient** for Copilot-guided workflow execution. The workshop repo (`hangar-ai-constitution-workflows`) remains a separate concern:

- Workshop: training-specific, loyalty-codebase-coupled, HTML, facilitated exercises
- Constitution: generic, codebase-agnostic, markdown, self-service for any AA team

The constitution's prompt guidance should be general enough that the workshop facilitator can supplement it with the loyalty-specific `prompt-guide.html`, not depend on it.

---

## Constitutional Compliance

| Law | How Satisfied |
|-----|--------------|
| ENG-4.1 ⛔ | All new skill and workflow content authored with RED→GREEN→REFACTOR TDD on lint/RAG gates |
| ENG-11.1 ⛔ | This proposal is the SDD artifact; `tasks.md` governs implementation |
| ENG-10.1 | All law references validated; `laws/index.yaml` updated for ENG-12.1 |
| BUS-7.1 | Proposal archived on completion |

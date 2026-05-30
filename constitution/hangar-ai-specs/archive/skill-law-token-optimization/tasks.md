# Tasks: skill-law-token-optimization

**Branch:** `feature/hangar-ai-governance-evolution`  
**Laws governing this work:** `ENG-4.1`, `ENG-11.1`, `ENG-11.2`, `BUS-7.1`

## Progress Summary

- Completed: 27 / 27
- In Progress: 0
- Blocked: 0

---

## Phase 1: Extract Examples from 11 Workflow-Referenced Skills

> **Goal:** Move `## Good Examples` and `## Bad Examples` sections to companion `*-examples.md` files. Skills with ≤1,500 tokens (`spec-governance`, `product-discovery-orchestration`) are excluded.

- [x] 1.0 **Baseline snapshot** — record pre-extraction token counts for all 11 skills (measurement gate per governance AC)
- [x] 1.1 Extract examples: `06-atomic-tdd.md` → `06-atomic-tdd-examples.md`
- [x] 1.2 Extract examples: `04-business-domain-modeling.md` → `04-business-domain-modeling-examples.md`
- [x] 1.3 Extract examples: `10-security-review.md` → `10-security-review-examples.md`
- [x] 1.4 Extract examples: `14-technical-debt.md` → `14-technical-debt-examples.md`
- [x] 1.5 Extract examples: `09-refactoring.md` → `09-refactoring-examples.md`
- [x] 1.6 Extract examples: `02-user-journey-mapping.md` → `02-user-journey-mapping-examples.md`
- [x] 1.7 Extract examples: `03-executable-spec.md` → `03-executable-spec-examples.md`
- [x] 1.8 Extract examples: `07-vertical-slice-dev.md` → `07-vertical-slice-dev-examples.md`
- [x] 1.9 Extract examples: `12-api-design.md` → `12-api-design-examples.md`
- [x] 1.10 Extract examples: `01-roadmapping.md` → `01-roadmapping-examples.md`
- [x] 1.11 Extract examples: `08-code-review.md` → `08-code-review-examples.md`
- [x] 1.12 **Structural validation** — confirm law citations, triggers, followed_by, Workflow refs, Constitutional Foundation, Quality Checklist, When to Invoke, Skill Interactions all present in each skill body
- [x] 1.13 **Token validation** — confirm ≥30% reduction and ≤2,000 tokens per skill body
- [x] 1.14 **Linter run** — `tools/constitution-lint/` 5/5

## Phase 2: Refactor `governance.md` Law Bodies (ENG-10.x)

> **Goal:** Move implementation schemas, metrics formats, dashboard specs, roll-out roadmap to `docs/guides/constitution/constitution-observability.md`. Law bodies keep only SHALL/MUST statements and Requirements bullet lists.

- [x] 2.1 Create `docs/guides/constitution/constitution-observability.md` — scaffold with headings matching each ENG-10.x law
- [x] 2.2 Extract ENG-10.1 implementation detail → `constitution-observability.md`
- [x] 2.3 Extract ENG-10.2 implementation detail → `constitution-observability.md`
- [x] 2.4 Extract ENG-10.3 implementation detail → `constitution-observability.md`
- [x] 2.5 Extract ENG-10.4 implementation detail → `constitution-observability.md`
- [x] 2.6 Extract ENG-10.5 implementation detail → `constitution-observability.md`
- [x] 2.7 Add bidirectional cross-references: each law body → guide; guide intro → each law
- [x] 2.8 **Law body validation** — confirm every ENG-10.x SHALL/MUST clause readable without consulting guide
- [x] 2.9 **Token validation** — confirm governance.md ≤1,000 tokens total (≤200/law)

## Phase 3: Trim `spec-driven-development.md` (ENG-11.x)

> **Goal:** Compress PROPOSE→IMPLEMENT→ARCHIVE narrative to a reference table. Zero law citations or SHALL clauses removed.

- [x] 3.1 Rewrite PROPOSE→IMPLEMENT→ARCHIVE section as a 3-row reference table
- [x] 3.2 **Token validation** — confirm ≤600 tokens total (≤200/law)
- [x] 3.3 **Law citation check** — zero citations removed vs. baseline

## Phase 4: Governance Review & Commit

- [x] 4.1 **Final structural scan** — Laws → Skills → Workflows chain spot-check (2 workflows end-to-end)
- [x] 4.2 **Final linter run** — `tools/constitution-lint/` 5/5
- [x] 4.3 Commit all changes with token delta summary in commit message
- [x] 4.4 Update PROGRESS.md — status COMPLETE

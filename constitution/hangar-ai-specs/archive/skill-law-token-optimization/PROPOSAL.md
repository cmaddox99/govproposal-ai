# Proposal: Skill & Law Token Optimization

**Proposal ID:** skill-law-token-optimization  
**Submitted:** March 31, 2026  
**Last Updated:** March 31, 2026  
**Status:** DRAFT — Governance Review Pending  
**Governance Session:** `gov-740b8edb501e` — CONDITIONAL (see conditions addressed below)  
**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-11.3`, `BUS-7.1`, `ENG-4.1`

---

## Problem

A token density audit (2026-03-31) identified three structural inefficiencies in the Hangar AI Constitution:

**1. Skill files embed pedagogical content alongside governance content.**  
All 13 workflow-referenced skills contain `## Good Examples` and `## Bad Examples (Anti-Patterns)` sections with full code samples. These sections travel with every RAG retrieval regardless of whether the agent needs examples or just the checklist and law citations. Token analysis shows example/template code blocks account for **36–56% of skill body tokens** in workflow-referenced skills. At retrieval time, an agent asking "what does the refactoring checklist require?" receives ~3,900 tokens when the actionable governance content (checklist + law citations + triggers) is ~1,500–2,000 tokens.

**2. `laws/engineering/governance.md` embeds implementation guidance inside law bodies.**  
ENG-10.x laws contain metrics collection schemas, dashboard specifications, event format definitions, and a four-phase roll-out roadmap — implementation artifacts that belong in `docs/guides/`, not in the law body. Result: 3,416 tokens across 5 laws (683 tok/law vs. the constitution average of 123–199 tok/law).

**3. `laws/engineering/spec-driven-development.md` is slightly dense for 3 laws.**  
286 tok/law vs. the average. The PROPOSE→IMPLEMENT→ARCHIVE lifecycle section contains narrative that could be compressed to a reference table.

---

## Governing Constraints (from governance verdict `gov-740b8edb501e`)

The following must be maintained at all times. These are not negotiable:

| Element | Must Remain In | Must NOT Move |
|---|---|---|
| Law citation blocks (`- id: ENG-x.x`) | Skill frontmatter | — |
| `triggers: phrases:` list | Skill frontmatter | — |
| `followed_by:` list | Skill frontmatter | — |
| `> **Workflow:**` cross-reference lines | Skill body (header) | — |
| `## Constitutional Foundation` section | Skill body | — |
| `## Quality Checklist` section | Skill body | — |
| `## When to Invoke` section | Skill body | — |
| `## Skill Interactions` section | Skill body | — |
| Law requirement statement | Law body | — |
| Law acceptance criteria / SHALL clauses | Law body | — |
| `## Good Examples` sections | → companion `-examples.md` | Skill body |
| `## Bad Examples (Anti-Patterns)` sections | → companion `-examples.md` | Skill body |
| Implementation schemas / metrics formats | → `docs/guides/constitution/` | Law body |
| Roll-out roadmaps / phase tables | → `docs/guides/constitution/` | Law body |

**Companion file contract:**
- `-examples.md` files are **optional pedagogical supplements** — skills are fully functional without them
- `-examples.md` files SHALL NOT contain law citations or governance checklists
- `-examples.md` files are NOT in scope for governance compliance reviews
- `-examples.md` files reference their parent skill in a header: `> Examples for: [skill-id]`

---

## Scope

### Phase 1: Extract Examples from 13 Workflow-Referenced Skills

The 13 skills composed by the 5 governed workflows, verified against `workflows/` frontmatter:

| Skill ID | File | Used By Workflow(s) |
|---|---|---|
| `skill-spec-governance` | `discovery-research/spec-governance.md` | All 5 |
| `skill-product-discovery-orchestration` | `discovery-research/product-discovery-orchestration.md` | product-discovery |
| `skill-02-user-journey-mapping` | `discovery-research/02-user-journey-mapping.md` | product-discovery, greenfield |
| `skill-01-roadmapping` | `product-planning/01-roadmapping.md` | product-discovery |
| `skill-03-executable-spec` | `product-planning/03-executable-spec.md` | product-discovery, greenfield, rewrite |
| `skill-04-business-domain-modeling` | `development-practices/04-business-domain-modeling.md` | greenfield, decision-track, rewrite |
| `skill-06-atomic-tdd` | `development-practices/06-atomic-tdd.md` | greenfield, refactor, rewrite |
| `skill-07-vertical-slice-dev` | `development-practices/07-vertical-slice-dev.md` | greenfield |
| `skill-08-code-review` | `development-practices/08-code-review.md` | decision-track, refactor |
| `skill-09-refactoring` | `development-practices/09-refactoring.md` | decision-track, refactor |
| `skill-10-security-review` | `platform-engineering/10-security-review.md` | greenfield, refactor, rewrite |
| `skill-12-api-design` | `platform-engineering/12-api-design.md` | greenfield, rewrite |
| `skill-14-technical-debt` | `platform-engineering/14-technical-debt.md` | decision-track |

**Token baseline (chars ÷ 4, measured 2026-03-31):**

| Skill | Baseline Tokens | Code% | Example Risk |
|---|---|---|---|
| `06-atomic-tdd.md` | 4,881 | 45% | 24 code blocks / 284 lines |
| `04-business-domain-modeling.md` | 4,428 | 53% | 12 code blocks / 324 lines |
| `10-security-review.md` | 3,884 | 43% | 16 code blocks / 230 lines |
| `14-technical-debt.md` | 3,884 | 55% | 18 code blocks / 310 lines |
| `09-refactoring.md` | 3,877 | 41% | — |
| `02-user-journey-mapping.md` | 3,552 | 36% | — |
| `03-executable-spec.md` | 3,517 | 51% | — |
| `07-vertical-slice-dev.md` | 3,330 | 47% | — |
| `12-api-design.md` | 3,221 | 56% | 25 code blocks / 324 lines |
| `01-roadmapping.md` | 3,115 | 42% | — |
| `08-code-review.md` | 3,777 | (TBD) | — |
| `spec-governance.md` | 896 | 17% | Low — no extraction needed |
| `product-discovery-orchestration.md` | 773 | 0% | None — no code blocks |

Skills with baseline ≤1,500 tokens (`spec-governance`, `product-discovery-orchestration`) are **excluded from extraction** — extraction overhead not justified.

**Extraction rule:** Move `## Good Examples` and `## Bad Examples (Anti-Patterns)` sections (and any section containing only code blocks with no law citations) to `<skill-file-basename>-examples.md` in the same directory. Add a cross-reference at the bottom of the skill body: `> 📎 Examples: See [skill-id]-examples.md`

### Phase 2: Refactor `governance.md` Law Bodies

Sections to move to `docs/guides/constitution/constitution-observability.md`:
- `### Implementation` sub-sections containing metric schemas and event formats
- `### Metrics` sub-sections with field definitions
- `### Dashboard Specifications` content
- `### Roll-out Roadmap` table

Sections that stay in `governance.md` law bodies:
- `**Law ID:**` header
- `**Status:**` (NON-NEGOTIABLE flag)
- The `SHALL` / `MUST` requirement statement
- `### Requirements` bullet list (no code)
- `### Rationale` (1 sentence)
- Cross-reference: `> Implementation guidance: See docs/guides/constitution/constitution-observability.md`

Target: ≤200 tok/law (1,000 tokens total for 5 laws).

### Phase 3: Trim `spec-driven-development.md`

Compress the PROPOSE→IMPLEMENT→ARCHIVE lifecycle narrative into a reference table. No law citations, checklist items, or SHALL clauses removed. Target: ≤200 tok/law (600 tokens total for 3 laws).

---

## Acceptance Criteria

### Phase 1 AC
- [ ] All 11 in-scope skills have companion `*-examples.md` files in the same directory
- [ ] Original skill files retain 100% of: law citations, `triggers:`, `followed_by:`, `> **Workflow:**` lines, `## Constitutional Foundation`, `## Quality Checklist`, `## When to Invoke`, `## Skill Interactions`
- [ ] RAG-relevant skill body (skill file excluding companion) is ≤2,000 tokens for each extracted skill
- [ ] Token reduction ≥30% vs. baseline for each extracted skill
- [ ] Linter passes: `tools/constitution-lint/` 5/5

### Phase 2 AC
- [ ] `governance.md` ≤1,000 tokens total (≤200 tok/law)
- [ ] Every ENG-10.x law body independently states its SHALL requirement without requiring the guide
- [ ] `docs/guides/constitution/constitution-observability.md` exists with all moved content
- [ ] Bidirectional cross-references in place (law → guide, guide → law)

### Phase 3 AC
- [ ] `spec-driven-development.md` ≤600 tokens (≤200 tok/law)
- [ ] Zero law citations removed
- [ ] All SHALL/MUST clauses preserved verbatim

---

## Test Strategy

**Unit (verify structure, ~70%):**
- Token counter script: measure each skill file and companion file post-extraction
- Structural validator: confirm law citations, checklists, triggers present in skill body; absent in companion
- Law body validator: confirm SHALL/MUST clauses present in governance.md law bodies

**Integration (verify RAG chain, ~20%):**
- Workflow composition check: skill IDs in workflow frontmatter resolve to valid skill files
- `followed_by` chain check: every skill ID in followed_by exists
- Cross-reference check: `> **Workflow:**` and `> 📎 Examples:` links resolve to existing files

**E2E (verify model integrity, ~10%):**
- Laws → Skills → Workflows chain: spot-check 2 workflows end-to-end
- Linter: `tools/constitution-lint/` full run

---

## Rollback Plan

Each phase is a separate commit. If Phase 2 (governance.md) breaks law enforceability per governance review:
1. `git revert <phase-2-commit>`
2. Restore `governance.md` from pre-phase-2 state
3. Re-scope: identify which ENG-10.x sections are normative (not implementation), keep those

---

## Success Criteria Summary

| Criterion | Target | Measurement |
|---|---|---|
| Workflow-referenced skill token reduction | ≥30% per skill (11 skills) | `wc -c` on skill body file pre/post |
| governance.md density | ≤200 tok/law (1,000 total) | `wc -c ÷ 4 ÷ 5` |
| spec-driven-development.md density | ≤200 tok/law (600 total) | `wc -c ÷ 4 ÷ 3` |
| Law citations preserved | 100% | Structural validator |
| Linter | 5/5 | `tools/constitution-lint/` |
| No broken workflow→skill references | 0 | Cross-reference check |

---

## References

- `tools/constitution-lint/` — existing linter for structural validation
- `laws/engineering/governance.md` — ENG-10.x laws
- `laws/engineering/spec-driven-development.md` — ENG-11.x laws
- `workflows/` — 5 governed workflows referencing the 13 skills
- Governance session: `gov-740b8edb501e` (CONDITIONAL verdict, 2026-03-31)
- Prior work: `constitution-workflow-governance-evolution` Phase 6 model integrity

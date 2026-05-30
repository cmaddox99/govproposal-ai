# Proposal: Avatar Workflow

**Status:** PROPOSED
**Spec ID:** `avatar-workflow`
**Triggered by:** Field observations during avatar creation — 2026-04-10
**Scope:** `governance/hangar-ai-constitution/` — new workflow, new agent skill, avatar model schema

---

## Problem

### 1. No Governed Process for Creating or Maintaining Avatars

The constitution has 30+ technology avatars and 15+ product-type avatars. Every one of them was created without a governed workflow. There is no orchestrated guidance for anyone — an agent or a human — to:

- **Generate** a new technology or product-type avatar with a complete, constitutionally valid model structure
- **Assess** an existing avatar and identify structural gaps or law coverage deficiencies
- **Validate** any avatar against the constitution's required model schema
- **Enrich** an avatar with real patterns, examples, and conventions extracted from an actual codebase

The result: avatar quality is inconsistent. Some avatars have complete non-negotiable law examples; others have partial examples or none at all. Some have use cases; most do not. RAG retrieval quality degrades when avatars are incomplete because the chunk strategy (`guidance + specific example + use-case`) assumes all three document types exist.

### 2. The Avatar Model Is Implicit — Never Made Explicit as a Schema

The required structure of a constitutionally valid avatar is buried across `AVATAR-RAG-INDEX.yaml`, individual manifests, and the README. No document defines:

- What fields in `manifest.yaml` are **non-negotiable** (must exist for every avatar type)
- What examples are **required** (at minimum: one per non-negotiable law)
- What the minimum use-case count is before an avatar is considered RAG-ready
- What token budget each document must respect to stay within the 2000–3500 token query window

Without an explicit schema, there is no way to lint an avatar, and no way for an agent to know when a generated avatar is **done** vs. merely started.

### 3. No RAG Evaluation Threshold Enforcement at Avatar Creation Time

The `AVATAR-RAG-INDEX.yaml` defines:
- Recall target: ≥95% for product domain queries
- Precision target: ≥90% (minimal false positives)
- Token budget: 2000–3500 per query (selective loading)

These thresholds exist but are never enforced at the point where an avatar is created or modified. An avatar with a 4,000-token `guidance.md` or missing use-cases will degrade retrieval quality silently. There is no gate.

### 4. Codebase Enrichment Is a Critical Gap

In the field, the most valuable avatar improvement is **extracting real patterns from an existing codebase**: actual project structure, real test examples, real CI commands, real naming conventions. Currently this enrichment is done manually and inconsistently. There is no workflow for an agent to systematically analyze a codebase and update an avatar with high-fidelity, grounded examples — replacing generic patterns with production-proven ones.

---

## Solution

A new `avatar-workflow.md` in `workflows/` governing four operating **modes** on top of a shared phase structure. Each mode is a constitutional workflow with phase gates, law enforcement, and RAG validation checkpoints.

### Operating Modes

| Mode | Trigger | Starting State | End State |
|---|---|---|---|
| **Generate** | "Create a new [tech/product] avatar for [domain]" | No avatar exists | Constitutionally valid avatar committed |
| **Assess & Correct** | "Assess and fix the [domain] avatar" | Avatar exists, completeness unknown | Avatar corrected and validated |
| **Validate** | "Validate the [domain] avatar" | Avatar exists | Validation report committed; no changes made |
| **Enrich** | "Enrich the [domain] avatar with [codebase path]" | Avatar exists + codebase provided | Avatar updated with codebase-grounded patterns |

---

### Workstream 1 — Avatar Model Schema (`docs/guides/avatar-model-schema.md`)

Define the **Avatar Model Schema** — the explicit contract that every constitutionally valid avatar must satisfy.

#### Minimum Required Structure (All Avatar Types)

```
avatars/{type}/{domain}/
├── manifest.yaml           ← REQUIRED: non-negotiable fields defined below
├── guidance.md             ← REQUIRED: ≤450 tokens, non-negotiable laws section mandatory
└── examples/               ← REQUIRED: one file per non-negotiable law specialization
```

#### Additional Requirements by Type

| Avatar Type | Additional Requirements |
|---|---|
| `technology` | `examples/` includes: ENG-4.1 (atomic TDD), ENG-3.1 (complexity) with real stack code |
| `product-type` | `examples/` includes: PRD-1.1 (discovery), PRD-2.1 (journey); ≥1 `use-cases/` directory |
| `industry` | `examples/` includes: BUS-2.1 (regulatory mapping), BUS-2.2 (control framework) |

#### Non-Negotiable `manifest.yaml` Fields

```yaml
avatar:
  id: avatar-{type}-{domain-slug}   # REQUIRED — must match directory name
  type: technology | product | industry   # REQUIRED
  name: "Human Readable Name"        # REQUIRED
  version: "x.y.z"                   # REQUIRED — semver

# technology avatars: stack block REQUIRED
stack:                               # REQUIRED for technology type
  language: ...
  framework: ...
  testing: [...]

# product-type avatars: domain block REQUIRED
domain:                              # REQUIRED for product type
  category: "..."
  description: |
    ...
  personas: [...]                    # REQUIRED — minimum 2 personas

activates:
  skills: [...]                      # REQUIRED — minimum 2 skills
  workflows: [...]                   # REQUIRED — minimum 1 workflow

specializes_laws:                    # REQUIRED — minimum 1 non-negotiable law
  - id: ENG-x.x | PRD-x.x | BUS-x.x
    title: "..."
    example_file: examples/...       # REQUIRED — must reference an existing file
```

#### RAG Budget Constraints (Enforced at Gate)

| Document | Max Tokens | Violation = |
|---|---|---|
| `manifest.yaml` | 150 tokens | FAIL — trim stack/project_structure |
| `guidance.md` | 450 tokens | FAIL — restructure, move detail to examples |
| Each `examples/*.md` | 850 tokens | WARNING — split into sub-examples |
| Each `use-cases/*/README.md` | 1,500 tokens | FAIL — split into phases |
| Total selective query load | 3,500 tokens | FAIL — avatar exceeds RAG window |

---

### Workstream 2 — New Workflow: `workflows/avatar-workflow.md`

A full constitutional workflow with four modes, shared phases, and per-mode gates.

#### Phase Table (All Modes)

| Phase | Name | Modes | Key Activities | Constitutional Gate |
|---|---|---|---|---|
| 1 | Identify | All | Detect avatar type (tech/product/industry); confirm domain; locate existing avatar if any; select mode | Mode confirmed; avatar path resolved |
| 2 | Scan | Assess, Validate, Enrich | Load all avatar files; run schema completeness check; produce gap report | Schema gap report committed to `hangar-ai-specs/evidence/avatar-scan-{domain}.md` |
| 3 | Discover | Generate, Enrich | Surface applicable constitution laws; identify non-negotiable laws for this domain/stack; identify RAG query patterns | Non-negotiable laws listed; query patterns documented |
| 4 | Build / Correct / Enrich | Generate, Assess, Enrich | Produce or repair avatar artifacts per schema; extract patterns from codebase (Enrich only) | All schema-required files present; token budgets within limits |
| 5 | RAG Validate | All | Simulate 5 canonical RAG queries against the avatar; measure token load per query; check recall/precision proxies | Recall proxy ≥95%; total query load ≤3,500 tokens; no schema violations |
| 6 | Commit | Generate, Assess, Enrich | Commit avatar artifacts; update `avatars/index.yaml` and `AVATAR-RAG-INDEX.yaml` if new; archive proposal | `AVATAR-RAG-INDEX.yaml` updated; `avatars/index.yaml` entry present |

> **Validate mode** runs Phases 1, 2, and 5 only — read-only, no files modified.

---

#### Phase 1: Identify

**Goal:** Establish mode, avatar type, and domain before any file is created or modified.

**Step 1.1 — Classify Request**

| Trigger Pattern | Mode | Avatar Type |
|---|---|---|
| "Create a new avatar for [X]" | Generate | Infer from X: language/framework → technology; AA product domain → product-type |
| "Assess / fix / correct the [X] avatar" | Assess & Correct | Inspect existing avatar at `avatars/*/[X]/` |
| "Validate the [X] avatar" | Validate | Inspect existing avatar — read-only |
| "Enrich [X] avatar with [codebase]" | Enrich | Requires existing avatar + accessible codebase path |

**Step 1.2 — Confirm Domain Slot**

For **Generate** mode: if the domain does not match any existing `avatars/{type}/` directory, confirm with the user:
- Proposed `avatar.id` slug
- Avatar type (technology / product / industry)
- Target directory path

**Step 1.3 — Locate Avatar**

For Assess, Validate, Enrich modes: confirm the avatar directory exists. If not found, offer Generate mode instead.

**Phase Gate:** Mode confirmed; avatar path resolved; domain slug agreed.

---

#### Phase 2: Scan (Assess, Validate, Enrich Modes)

**Goal:** Produce a complete gap report against the Avatar Model Schema before any corrections begin.

**Step 2.1 — Structural Completeness Check**

For each required artifact:

```
✅ manifest.yaml present?
  ✅ avatar.id matches directory slug?
  ✅ avatar.type is technology | product | industry?
  ✅ avatar.version present (semver)?
  ✅ stack (tech) or domain (product) block present?
  ✅ activates.skills has ≥2 entries?
  ✅ activates.workflows has ≥1 entry?
  ✅ specializes_laws has ≥1 non-negotiable law?
  ✅ all example_file references resolve to existing files?

✅ guidance.md present?
  ✅ Non-Negotiable Laws section present?
  ✅ Token count ≤450?

✅ examples/ directory present?
  ✅ One example file per law in specializes_laws?
  ✅ Each example ≤850 tokens?

✅ use-cases/ present? (product-type only)
  ✅ ≥1 use-case with README.md?
  ✅ Each use-case README ≤1,500 tokens?
```

**Step 2.2 — Gap Classification**

| Severity | Condition | Impact |
|---|---|---|
| 🔴 BLOCKING | Missing manifest.yaml, missing guidance.md, missing non-negotiable law example, broken example_file reference | Avatar cannot be loaded by RAG pipeline |
| 🟡 WARNING | Token budget exceeded on any document, missing use-cases (product-type), fewer than 2 personas | RAG retrieval degraded |
| 🟢 ADVISORY | Missing optional sections (commands, project_structure), no anti-patterns section | Quality improvement opportunity |

**Phase Gate:** Gap report committed to `hangar-ai-specs/evidence/avatar-scan-{domain}.md`.

---

#### Phase 3: Discover (Generate, Enrich Modes)

**Goal:** Surface the correct laws and RAG query patterns for this domain before any artifacts are generated.

**Step 3.1 — Law Discovery**

For **technology** avatars:
- Map the stack to applicable engineering laws: ENG-3.1, ENG-3.2, ENG-4.1 are always non-negotiable for any tech avatar
- Identify stack-specific law specializations: security frameworks (ENG-6.x) if the stack involves HTTP/API/auth; immutability laws (ENG-3.2) if functional style

For **product-type** avatars:
- Map the domain to applicable product laws: PRD-1.1 (discovery), PRD-2.1 (journey), PRD-5.1 (metrics) are always required
- Identify business laws: BUS-2.x (regulatory) if the domain has compliance obligations; BUS-4.x (data) if PII is involved

For **Enrich** mode: surface law gaps by comparing the existing `specializes_laws` list against the standard law set for the avatar type.

**Step 3.2 — RAG Query Pattern Definition**

Define 5 canonical query patterns for this avatar. These become the RAG validation test cases in Phase 5.

```
Technology Avatar Canonical Queries:
  Q1: "How do I write a test for [stack]?" → ENG-4.1 example
  Q2: "What are the complexity limits for [stack]?" → ENG-3.1 example
  Q3: "How do I handle [stack-specific concern]?" → guidance.md
  Q4: "What is the project structure for [stack]?" → manifest.yaml
  Q5: "What are the non-negotiable rules for [stack]?" → guidance.md Non-Negotiable section

Product Avatar Canonical Queries:
  Q1: "How do we discover [domain] user needs?" → PRD-1.1 example
  Q2: "What is the [domain] core journey?" → PRD-2.1 example
  Q3: "What are the success metrics for [domain]?" → PRD-5.1 example
  Q4: "What is the [domain] regulatory context?" → BUS-2.x example (if applicable)
  Q5: "Walk me through a [domain] workflow" → use-cases/ README
```

**Phase Gate:** Non-negotiable laws listed with citations; 5 canonical query patterns documented.

---

#### Phase 4: Build / Correct / Enrich

**Goal:** Produce or repair all avatar artifacts to satisfy the Avatar Model Schema.

##### Mode: Generate — Build from Scratch

**Step 4.1 — Scaffold Avatar Directory**

```
avatars/{type}/{domain-slug}/
├── manifest.yaml    ← Generate from schema template
├── guidance.md      ← Generate with domain-specific laws and patterns
└── examples/        ← Generate one file per non-negotiable law
```

For product-type avatars, also scaffold:
```
└── use-cases/
    └── {primary-use-case}/
        └── README.md
```

**Step 4.2 — Generate `manifest.yaml`**

Follow the non-negotiable field schema. Every `specializes_laws` entry must reference an `example_file` that will be created in Step 4.3.

**Step 4.3 — Generate `guidance.md`**

Structure:
```markdown
# [Name] Guidance

> **Purpose:** [One sentence]

---

## Overview
[2-3 sentences, domain summary]

## Non-Negotiable Laws

### [LAW-ID] — [Title]
- [What the law requires in this stack/domain]
- [What violates it]
- [Implementation note]

## [Stack Patterns | Core Journeys]
[Code examples for technology; journey tables for product]

## Anti-Patterns to Avoid
[2-3 common mistakes]
```

Token budget: ≤450 tokens. If overview + patterns exceed budget, move patterns to `examples/`.

**Step 4.4 — Generate Law Examples**

One markdown file per non-negotiable law. Format:
```markdown
---
avatar: avatar-{type}-{domain}
law: {LAW-ID}
title: "{Law Title}"
---

# {LAW-ID} — {Law Title}: {Domain} Application

## What This Law Requires
[1-2 sentences]

## Compliant Example
[Code or scenario example — primary content, ~600 tokens]

## Violation Example
[What a violation looks like — ~150 tokens]
```

##### Mode: Assess & Correct — Fix Gaps from Phase 2

Address each 🔴 BLOCKING gap first, then 🟡 WARNINGs:

| Gap Type | Correction Action |
|---|---|
| Missing `manifest.yaml` fields | Add required fields; validate slug matches directory |
| Missing `guidance.md` Non-Negotiable section | Add section; cite laws from `specializes_laws` |
| Missing law example file | Generate example file; add `example_file` reference to manifest |
| Broken `example_file` reference | Locate or regenerate the referenced file |
| Token budget exceeded | Split or summarize the offending document |
| Missing use-cases (product-type) | Generate primary use-case from domain journeys |
| Missing personas | Derive from domain description; add ≥2 realistic personas |

##### Mode: Enrich — Extract Patterns from Codebase

**Step 4.1 — Codebase Discovery**

Systematically analyze the target codebase:

```
Discover:
  - Project structure (actual directories, not generic templates)
  - Test framework and test file naming conventions
  - Actual CI/CD commands from package.json / Makefile / pom.xml / pyproject.toml
  - Real dependency versions from lockfiles
  - Naming conventions from 10+ file samples (components, services, tests)
  - Anti-patterns: detect complexity violations, missing tests, inconsistent naming
```

**Step 4.2 — Map Codebase Patterns to Avatar**

For each discovered pattern:
- Replace generic `project_structure` in `manifest.yaml` with actual directory tree (sampled, not full)
- Replace generic `commands` block with actual CI/CD commands
- Replace generic examples with real code extracted from the codebase (anonymized of business logic, preserving structural patterns)
- Add anti-patterns observed in the codebase to `guidance.md`

**Step 4.3 — Update `manifest.yaml` Conventions Block**

```yaml
conventions:
  naming:
    # Replace with actual patterns observed in codebase
    components: [observed pattern with real example]
  patterns:
    # Replace with real code patterns from codebase
commands:
  test:
    all: [actual command from package.json / Makefile]
project_structure: |
  # Replace with actual directory tree from codebase (3 levels deep)
```

**Step 4.4 — Regenerate Affected Law Examples**

For any law example that was previously generic: replace with a real code example extracted from the codebase, preserving the law example format.

**Phase Gate (all modes):** All schema-required files present; token budgets within limits; no broken `example_file` references.

---

#### Phase 5: RAG Validate (All Modes)

**Goal:** Simulate the RAG retrieval pipeline against the avatar and verify it meets the constitutional thresholds.

**Step 5.1 — Simulate 5 Canonical Queries**

For each query defined in Phase 3 (or the standard set for Validate mode):
1. Identify which avatar files would be loaded by the selective chunk strategy
2. Count the total tokens that would be consumed
3. Confirm the answer to the query is present in the loaded files

**Step 5.2 — Evaluate Thresholds**

| Metric | Threshold | Evaluation Method |
|---|---|---|
| Recall proxy | ≥95% | 5/5 queries answered with specific content from avatar files (4/5 = WARNING, 3/5 = FAIL) |
| Precision proxy | ≥90% | No loaded file is irrelevant to the query being evaluated |
| Total query token load | ≤3,500 tokens | Sum of tokens for all files loaded per query |
| Per-query token load | ≤3,500 tokens | Each query must be answerable within one context window |
| Schema violations | 0 | No BLOCKING gaps from Phase 2 scan |

**Step 5.3 — RAG Validation Report**

Commit to `hangar-ai-specs/evidence/avatar-rag-{domain}.md`:

```markdown
# RAG Validation Report — {Domain} Avatar
Date: {date}
Mode: {Generate | Assess | Validate | Enrich}

## Query Results

| Query | Files Loaded | Tokens | Answered? | Notes |
|---|---|---|---|---|
| Q1: ... | guidance.md, examples/ENG-4.1.md | 650 | ✅ | |
| Q2: ... | examples/ENG-3.1.md | 750 | ✅ | |
| Q3: ... | guidance.md | 400 | ✅ | |
| Q4: ... | manifest.yaml | 120 | ✅ | |
| Q5: ... | use-cases/primary/README.md | 1,300 | ✅ | |

## Summary
- Recall: 5/5 (100%) ✅
- Precision: 5/5 (100%) ✅
- Max query token load: 1,300 tokens ✅
- Schema violations: 0 ✅

## Gate Result: PASS
```

**Phase Gate (Hard Stop):**
- Recall proxy < 95% (< 5/5) → 🔴 FAIL — return to Phase 4
- Token load > 3,500 on any query → 🔴 FAIL — trim offending document
- Any BLOCKING schema violation → 🔴 FAIL — return to Phase 4

---

#### Phase 6: Commit (Generate, Assess, Enrich Modes)

**Goal:** Commit all avatar artifacts and update the constitution registry files.

**Step 6.1 — Update Registry Files**

`avatars/index.yaml` — add or update the avatar entry:
```yaml
- id: avatar-{type}-{domain}
  name: "..."
  type: technology | product | industry
  path: {type}/{domain}/
  version: "x.y.z"
  rag_validated: true
  last_validated: {date}
```

`AVATAR-RAG-INDEX.yaml` — add or update the avatar's RAG entry with:
- File list with token estimates
- Canonical search queries
- Key metrics (product-type avatars)
- Law specializations list

**Step 6.2 — Commit Artifacts**

Commit all new/modified avatar files plus evidence files in a single structured commit:

```
feat(avatar): {mode} {domain} avatar

Mode: {Generate | Assess & Correct | Enrich}
Avatar: {avatar.id}
Type: {technology | product | industry}

Changes:
- {list of files created/modified}

RAG validation: PASS (recall 5/5, max 1,300 tokens/query)
Schema violations: 0

Ref: hangar-ai-specs/changes/avatar-workflow/PROPOSAL.md
```

**Step 6.3 — Archive Proposal Reference**

Update `hangar-ai-specs/evidence/` with a record of the avatar workflow run linking to the RAG validation report.

**Phase Gate:** `AVATAR-RAG-INDEX.yaml` updated; `avatars/index.yaml` entry present; RAG evidence committed.

---

### Workstream 3 — New Skill: `agent-skills/skill-avatar-workflow.md`

A dedicated agent skill that provides the agent with the avatar workflow protocol. This skill is activated whenever an avatar Generate, Assess, Validate, or Enrich operation is triggered.

**Skill responsibilities:**
- Load the Avatar Model Schema
- Execute the phase sequence for the selected mode
- Run Phase 5 RAG simulation (token counting, query coverage check)
- Produce structured evidence artifacts

**Skill triggers:**
```
- "Create a new [tech/product] avatar for [domain]"
- "Generate an avatar for [X]"
- "Assess the [X] avatar"
- "Fix the [X] avatar"
- "Validate the [X] avatar"
- "Enrich the [X] avatar with [codebase]"
- "Is the [X] avatar complete?"
- "Update the [X] avatar from this codebase"
```

---

### Workstream 4 — Update `workflows/README.md`

Add avatar-workflow to the workflow registry table:

| Workflow | Description | Laws | Skills |
|---|---|---|---|
| [avatar-workflow.md](avatar-workflow.md) | Avatar Workflow — Four-mode workflow for generating, assessing, validating, and enriching constitution avatars | ENG-11.1, ENG-1.2 | skill-avatar-workflow, skill-spec-governance |

---

### Workstream 5 — Update `avatars/index.yaml`

Add `rag_validated` and `last_validated` fields to the index schema so avatar registry entries carry their RAG validation status. Backfill existing avatars with `rag_validated: unknown` pending their first run through the Validate mode.

---

## Variants Identified in the Field

The four modes cover distinct field scenarios. These are not speculative — they were observed during the avatar creation process:

| Variant | Field Scenario | Mode |
|---|---|---|
| **Greenfield tech avatar** | Team adopts a stack (e.g., Databricks/PySpark) not in the constitution; needs a complete avatar before starting greenfield development | Generate |
| **Stale tech avatar** | An existing avatar's examples reference an old framework version; `guidance.md` lacks non-negotiable law examples added in a later constitution update | Assess & Correct |
| **Pre-merge avatar audit** | Before merging a community-contributed avatar PR, run constitutional validation to confirm it meets the schema before it enters the index | Validate |
| **Brownfield codebase onboarding** | A team is adopting the constitution into an existing codebase; they have a React/TypeScript avatar but it has generic examples; the real codebase uses a specific component library, monorepo structure, and Nx build commands | Enrich |
| **New product domain** | A new AA product domain (e.g., NDC API gateway) needs a product-type avatar before the product discovery workflow begins | Generate (product-type) |
| **Avatar divergence correction** | A product avatar was accurate at creation but the domain has evolved (new compliance obligations, new personas); an Assess & Correct run brings it current | Assess & Correct |

---

## Laws Enforced

| Law | Enforcement Point | Non-Negotiable? |
|---|---|---|
| ENG-11.1 — Proposal Lifecycle | Phase 6: proposal reference archived in evidence | Yes |
| ENG-1.2 — Spec-Driven Development | Phase 3: laws discovered before any artifact generated | Yes |
| ENG-3.1 — Complexity Limits | Phase 5: token budgets enforced as complexity proxy | No |
| PRD-2.1 — User Journey | Phase 4 (product-type): core journeys required in guidance.md | No |

---

## Success Criteria

A successful implementation of this proposal produces:

1. **`workflows/avatar-workflow.md`** — fully governed four-mode workflow matching the structure of `greenfield-development.md` and `adoption.md`
2. **`docs/guides/avatar-model-schema.md`** — explicit, lintable avatar schema document
3. **`agent-skills/skill-avatar-workflow.md`** — agent skill file with triggers, phase protocol, and RAG simulation procedure
4. **`workflows/README.md` updated** — avatar-workflow added to the registry table
5. **`avatars/index.yaml` updated** — `rag_validated` field added to schema
6. **All four modes validated** against at least one existing avatar (react-typescript for Generate/Validate, passenger-booking for product-type Assess/Enrich)

---

---

## Safeguards & Constitutional Integrity Gates

These safeguards address five failure modes that have been observed in the existing avatar corpus and will continue to occur without governed enforcement. Several are not hypothetical — **live violations exist today** and are documented below as evidence.

---

### Safeguard 1 — Deduplication Gate (Phase 1, all modes)

**Problem:** Without a deduplication check, Generate mode can produce a new avatar that overlaps significantly with an existing one. This fragments the RAG index, creates divergent guidance for the same domain, and doubles maintenance burden.

**Two tiers of detection:**

**Tier 1 — Exact Match (BLOCK)**

Before generating or assessing any avatar, check `avatars/index.yaml` and the filesystem:

```
Does avatars/{type}/{proposed-slug}/ already exist?
  YES → BLOCK Generate. Offer: Assess, Validate, or Enrich the existing avatar instead.
  NO  → Continue to Tier 2.
```

**Tier 2 — Semantic Overlap (WARN or REDIRECT)**

Evaluate the proposed avatar against all existing avatars of the same type:

| Overlap Signal | Weight |
|---|---|
| Same primary language or framework (tech avatars) | 40% |
| Same AA product domain or >50% of core journeys (product avatars) | 40% |
| >60% shared `specializes_laws` entries | 10% |
| >50% shared `activates.skills` | 10% |

**Thresholds:**

| Overlap Score | Action |
|---|---|
| ≥70% | 🔴 REDIRECT — Enrich the existing avatar rather than generating a new one. The agent must surface the overlapping avatar and explain which specific gaps in it justify a new one (if any). |
| 40–69% | 🟡 WARN — Flag the overlapping avatar, require explicit user confirmation with documented justification in the proposal before proceeding |
| <40% | ✅ PROCEED — Document the nearest neighbor avatar in the evidence file |

**Merge Offer Protocol (≥70% overlap):**

When overlap is ≥70%, the agent must present:
```
OVERLAP DETECTED: Proposed avatar "[X]" overlaps 75% with existing avatar "[Y]".

Option A (Recommended): Enrich [Y] — add [specific gaps] to the existing avatar.
  Impact: No new index entry, no RAG fragmentation, one maintained artifact.

Option B: Justify new avatar — explain what [X] covers that [Y] cannot.
  Required: Written justification committed to evidence before proceeding.
```

---

### Safeguard 2 — Law Domain Boundary Enforcement

**Problem:** Technology avatars are referencing Business and Product laws. Product avatars are referencing Engineering architecture laws. This collapses the three-constitution model — if a tech avatar carries compliance law, there is no clear separation between *how we build* (ENG) and *why we build safely* (BUS). The compliance context then travels with the stack rather than with the domain.

**Live violations found in the current avatar corpus (evidence for this safeguard):**

| Avatar | Violating Law | Domain Crossing | Correction |
|---|---|---|---|
| `react-typescript` | `PRD-3.4` | Product law in tech avatar | Remove; reference `ENG-3.x` for implementation quality; `PRD-3.4` belongs in product-type avatars that use React |
| `databricks-pyspark` | `BUS-7.1` | Business compliance law in tech avatar | Replace with `ENG-6.7` (Audit Trail from engineering side) |
| `postgresql-sqlalchemy` | `BUS-7.1` | Business compliance law in tech avatar | Replace with `ENG-6.7` |
| `azure-openai` | `BUS-7.1` | Business compliance law in tech avatar | Replace with `ENG-6.7` |
| `opentelemetry-python` | `BUS-7.1` | Business compliance law in tech avatar | Replace with `ENG-6.7` |
| `operations-research-optimizer` | `BUS-2.1` | FAA compliance law in tech avatar | Remove; FAA compliance belongs in the product or industry avatar that uses this stack |

**The Permitted Law Matrix:**

| Avatar Type | Primary Laws | Conditionally Permitted | FORBIDDEN |
|---|---|---|---|
| `technology` | `ENG-*` (all) | — | `PRD-*` (product decisions belong in product avatars), `BUS-*` (compliance authority belongs in product/industry avatars) |
| `product` | `PRD-*` (all), `BUS-*` (compliance obligations of the domain) | `ENG-6.x` only (security/privacy laws, when the product has direct security obligations) | `ENG-1.x`–`ENG-5.x` (pure engineering architecture), `ENG-7.x`–`ENG-12.x` (DevOps, governance) |
| `industry` | `BUS-*` (all), `PRD-*` (applicable product laws for the vertical) | `ENG-6.x` only (security/privacy where the industry standard requires it) | `ENG-1.x`–`ENG-5.x`, `ENG-7.x`–`ENG-12.x` |

**Why `ENG-6.x` is conditionally permitted in product/industry avatars:**

`ENG-6.7` (Audit Trail), `ENG-6.1` (Security by Design), `ENG-6.4` (Data Protection) describe *implementation requirements* that product/industry avatars must specify for their domain context. The product avatar for Passenger Booking correctly references `ENG-6.1`, `ENG-6.4`, and `ENG-6.7` because it is specifying *how the product must implement security* — not defining the security laws themselves. This is the correct composition model.

**Boundary Check (Phase 2, Step 2.1 — added sub-check):**

```
For each law in specializes_laws:
  Extract prefix: ENG | PRD | BUS
  Check against Permitted Law Matrix for avatar.type

  technology + PRD-* → 🔴 BLOCKING — Remove or migrate to product avatar
  technology + BUS-* → 🔴 BLOCKING — Remove; if ENG-6.x equivalent exists, replace; otherwise file product-avatar amendment
  product + ENG-1.x–5.x → 🔴 BLOCKING — Remove; these are tech-stack implementation laws
  product + ENG-7.x+ → 🔴 BLOCKING — Remove; these are DevOps/governance laws
  product + ENG-6.x → 🟡 WARN — Permitted with justification: "Why does this product avatar need to specify [ENG-6.x]?"
  industry + ENG-* (except 6.x) → 🔴 BLOCKING — Remove
```

**Backfill Required:** All six live violations listed above must be corrected as part of this proposal's implementation. Each correction goes through Assess & Correct mode and produces a RAG validation report.

---

### Safeguard 3 — Product Taxonomy Integrity Gate (Phase 1, product-type Generate mode)

**Problem:** New product-type avatars can be created outside the AA product taxonomy, creating orphan domains that don't compose correctly with the product discovery workflow, don't map to known business stakeholders, and fragment the product knowledge base.

**The Taxonomy Contract:**

Every product-type avatar `domain.category` must map to an established category in `avatars/product-type/index.yaml` OR trigger a taxonomy extension proposal:

```
Established categories (as of v2.0.0):
  Product (Operations)         — Airport Ops, Cargo, Check-In, Crew, Ground Ops
  Product (Customer Engagement) — Customer Relations, Customer Service, Loyalty, Marketing
  Product (Revenue)            — Passenger Booking, Network Planning
  Product (Internal)           — Internal Productivity
  Product (Compliance)         — Travel Docs & Compliance, Schedule Change
```

**Taxonomy Gate (Phase 1, Step 1.2 — product-type Generate mode):**

```
Does domain.category match an established taxonomy category?
  YES → Continue.
  NO  → Two options:
    Option A: Map to closest existing category (agent must justify the mapping)
    Option B: Propose new taxonomy category — file a product taxonomy extension
              in hangar-ai-specs/changes/ before proceeding with avatar generation.
              Avatar cannot be committed to index.yaml without taxonomy entry.
```

**Core Journey Overlap Check:**

After taxonomy category is confirmed, check for journey overlap with existing avatars in the same category:

```
For each proposed core_journey in the new avatar:
  Is this journey >80% semantically equivalent to a journey in an existing avatar in the same category?
    YES → Explain differentiation: what makes this journey distinct in context?
          If no distinct context exists → Do not create a duplicate journey; enrich the existing avatar instead.
    NO  → Proceed.
```

**Why this matters:** The product-type avatar model is the knowledge graph for AA product domains. If "Booking Modification" appears in both `passenger-booking` and `schedule-change-self-serve` without clear differentiation, RAG retrieval produces ambiguous results for agents executing the product discovery workflow.

---

### Safeguard 4 — Law ID Validity & Content Compliance Gate (Phase 5, extended)

**Problem:** An avatar can reference a law ID that doesn't exist, cite the wrong law for a concern, or — worse — write example content that actually contradicts the law it claims to demonstrate.

**Step 5.0 — Law ID Validation (added before RAG simulation):**

```
For each law in specializes_laws:
  Validate law.id exists in the appropriate _domain.yaml:
    ENG-* → laws/engineering/_domain.yaml articles
    PRD-* → laws/product/_domain.yaml articles
    BUS-* → laws/business/_domain.yaml articles

  Law ID not found → 🔴 BLOCKING: Invalid law reference. Remove or correct.
  Law ID found → Proceed to content compliance check.
```

**Step 5.1b — Content Compliance Check (added to RAG simulation):**

For each law example file referenced in `specializes_laws`:

```
Content Compliance Checks:
  □ Does the compliant example actually satisfy the law's stated requirement?
  □ Does the violation example show an actual violation (not a correct pattern)?
  □ Does the content introduce NEW requirements not in the original law?
    → If YES: flag as shadow governance (see Safeguard 5)
  □ Does the content override or soften the law?
    → "For this stack, ENG-4.1 is optional because..." → 🔴 HARD BLOCK
    → Law overrides require a formal amendment through ENG-10.x process
  □ Are all regulatory citations accurate? (regulation numbers, CFR parts, version)
    → Inaccurate regulatory citation → 🔴 BLOCKING: correct or remove
```

**Content Compliance Result:**

| Finding | Classification | Action |
|---|---|---|
| Example contradicts the law it cites | 🔴 BLOCKING | Rewrite example |
| Example introduces new enforcement requirements | 🟡 SHADOW GOVERNANCE | Triage per Safeguard 5 |
| Law is softened or marked optional | 🔴 HARD BLOCK | Remove override; file amendment if exception is legitimate |
| Regulatory citation is wrong | 🔴 BLOCKING | Correct citation |
| Example is correct but weak | 🟢 ADVISORY | Strengthen with a more complete scenario |

---

### Safeguard 5 — Shadow Governance Detection (Phase 2, Assess & Correct and Enrich modes)

**Problem:** Avatars that were created without this workflow — meaning the entire existing avatar corpus — may have developed internal governance that bypasses the constitutional amendment process. This includes invented law IDs, embedded skill definitions, inline policy overrides, and convention blocks that function as laws. These are "shadow governance" artifacts.

**Definition:** Shadow governance is any content in an avatar that:
1. Defines new mandatory requirements not traceable to a constitution law ID
2. Defines or modifies skills outside `agent-skills/`
3. Overrides, softens, or conditionally negates a constitution law
4. Introduces law-like IDs that do not exist in any `_domain.yaml`

**Detection Patterns (Phase 2, Step 2.3 — Assess & Correct, Enrich modes):**

Scan all avatar files (`manifest.yaml`, `guidance.md`, all `examples/*.md`, all `use-cases/**`) for:

```
Pattern 1 — Invented Law IDs:
  Regex: /[A-Z]{2,6}-\d+\.\d+/ not matching ENG-|PRD-|BUS-
  Examples: "TECH-1.1", "STACK-2.3", "AA-9.1", "AZURE-4.2"
  → Shadow governance: invented law reference

Pattern 2 — Inline Mandatory Requirement without Law Citation:
  Trigger: "must", "required", "NON-NEGOTIABLE", "mandatory" appearing without
           adjacent law ID citation (e.g., "ENG-4.1")
  → Candidate shadow governance: ungrounded mandatory requirement

Pattern 3 — Embedded Skill Definition:
  Trigger: "skill-" prefix in headings or content blocks that define agent behaviors
           outside the context of "activates.skills" references
  → Shadow governance: skill defined outside agent-skills/

Pattern 4 — Law Override / Exception:
  Trigger: "except for this stack", "in this context, [LAW-ID] does not apply",
           "override:", "for [technology], ignore [LAW-ID]"
  → Hard block: law overrides must go through ENG-10.3 Exception Request process

Pattern 5 — Scope Creep (Laws added to guidance that belong in another avatar type):
  Trigger: PRD-* citations in technology avatar guidance.md prose
           BUS-* citations in technology avatar guidance.md prose
  → Law boundary violation (Safeguard 2)
```

**Shadow Governance Triage (applied after detection):**

For each detected shadow governance artifact:

| Finding | Triage Question | Resolution |
|---|---|---|
| Invented law ID | Does this represent a genuine constitutional gap? | YES → File amendment proposal to add law to appropriate domain. NO → Remove and reference nearest existing law. |
| Ungrounded mandatory requirement | Is this covered by an existing law? | YES → Replace with law citation. NO → File amendment to formalize it. |
| Embedded skill definition | Does this skill already exist in `agent-skills/`? | YES → Remove duplicate; add to `activates.skills`. NO → File proposal to create the skill properly. |
| Law override / exception | Is there a legitimate stack/domain exception? | YES → File ENG-10.3 Exception Request. NO → Remove override; law applies as written. |
| Scope creep (cross-domain law) | Move to correct avatar type via Safeguard 2 resolution. | |

**Evidence Commitment:**

All shadow governance findings must be committed to:
```
hangar-ai-specs/evidence/avatar-shadow-governance-{domain}.md
```

With status for each finding: `triaged-amended | triaged-removed | triaged-law-cited | pending-amendment`.

**Amendment Filing Protocol:**

When a shadow governance finding requires a formal amendment (new law, new skill, exception request):
1. Create a new proposal in `hangar-ai-specs/changes/{amendment-slug}/PROPOSAL.md`
2. Set the avatar finding as the trigger evidence
3. The avatar's Assess & Correct run is **not blocked** by the pending amendment — the shadow governance content is removed from the avatar and the amendment is filed in parallel
4. The amendment is tracked in the avatar's evidence file with a link

---

### Safeguard Enforcement Summary

| Safeguard | Phase | Mode(s) | Gate Level |
|---|---|---|---|
| Exact duplicate detection | 1 | Generate | 🔴 BLOCK |
| Semantic overlap ≥70% | 1 | Generate | 🔴 REDIRECT to Enrich |
| Semantic overlap 40–69% | 1 | Generate | 🟡 WARN + confirmation |
| Law domain boundary check | 2 | All | 🔴 BLOCKING (per violation) |
| Product taxonomy mapping | 1 | Generate (product) | 🔴 BLOCK until taxonomy confirmed |
| Core journey overlap | 1 | Generate (product) | 🟡 WARN + differentiation required |
| Law ID validity | 5 | All | 🔴 BLOCKING |
| Content contradicts cited law | 5 | All | 🔴 BLOCKING |
| Law override in content | 5 | All | 🔴 HARD BLOCK |
| Shadow governance detection | 2 | Assess, Enrich | 🟡 WARN + triage required |
| Embedded skill definitions | 2 | Assess, Enrich | 🟡 WARN + triage required |
| Invented law IDs | 2 | All | 🔴 BLOCKING |
| Backfill: 6 live boundary violations | Assess mode | Six named avatars | Required as part of proposal implementation |

---

---

## Workflow Improvements — Identified from Field Evidence

The following improvements are grounded in findings from PR #14 (C++ Avatar Enrichment, sfraseraa). That PR had **209 commits**, **10 informal "amendments"**, and **8 constitutional violations** — all of which would have been prevented if the workflow had existed. Each improvement below addresses a specific failure mode that the four original modes do not cover.

---

### Improvement 1 — Mode 5: PR Review

**Evidence:** PR #14 assessment was performed manually. There is no workflow mode that triggers on an incoming PR touching avatar files.

**Addition:** A fifth operating mode: **PR Review**.

| Mode | Trigger | Starting State | End State |
|---|---|---|---|
| **PR Review** | Incoming PR touches any file in `avatars/` or `agent-skills/` | PR open, changeset available | Review comment posted with structured assessment; PR status updated |

**Phase sequence for PR Review mode:**

| Phase | Action |
|---|---|
| 1 | Identify all avatar files modified in the PR diff |
| 2 | Run Scan (Phase 2) against each modified avatar — gap report + law boundary check + manifest unknown blocks + shadow governance detection |
| 5 | Run RAG Validate (Phase 5) against each modified avatar |
| Output | Post structured assessment comment to PR using the assessment template from the Assess & Correct mode; do not modify any files |

**PR Review is read-only.** It never modifies files — it produces a structured review comment identical in format to the PR #14 assessment posted above. The comment must include:
- Safeguard results (1–5) with PASS/FAIL for each
- Violation inventory with severity and correction action
- RAG simulation results
- Explicit PASS or BLOCKED verdict

**Trigger:** Any PR that modifies a file matching `avatars/**`, `agent-skills/**`, or `AVATAR-RAG-INDEX.yaml`.

---

### Improvement 2 — Pre-flight Mode (Mode 0): Shift Left

**Evidence:** PR #14 reached 209 commits before assessment. All 8 violations could have been caught before commit 1 if the author had run a pre-flight check on their stated intent.

**Addition:** A lightweight **Pre-flight mode** (Mode 0) that runs before any files are created and validates the author's intent against the constitution.

**Trigger:** "I want to create/enrich/add a C++ avatar" — before any files are created.

**Phase sequence for Pre-flight:**

| Step | Action | Output |
|---|---|---|
| 0.1 | Confirm avatar type and domain from intent statement | `type: technology`, `domain: cpp` |
| 0.2 | Run Safeguard 1 (Deduplication) — exact match and semantic overlap check | PASS / REDIRECT |
| 0.3 | Run law domain boundary pre-check: present the Permitted Law Matrix for the declared avatar type and require the author to acknowledge which law domains they intend to specialize | Author confirms: "I will only use ENG-* laws" |
| 0.4 | Run product taxonomy check if `type: product` | Category confirmed or taxonomy extension flagged |
| 0.5 | State the 5 canonical RAG query patterns before any content is written | RAG queries agreed → content will be designed to answer them |

**Pre-flight output:** A `hangar-ai-specs/evidence/avatar-preflight-{domain}.md` filed before first commit. This document is the author's contract with the constitution. The Assess & Correct pass that runs later uses it to verify intent was followed.

**Why this matters:** The law boundary guidance (Safeguard 2) is currently enforcement-only — it runs after the work is done. Pre-flight makes it advisory before the work starts. Step 0.3 in particular would have prevented every BUS-* and PRD-* example file in PR #14 from being created.

---

### Improvement 3 — Content Routing Protocol (Route, Don't Delete)

**Evidence:** PR #14 had 14 well-written BUS-* and PRD-* example files that the assessment correctly flagged as misplaced. The current workflow says "remove them." But that destroys good work — the FAR Part 117 C++ example, the DOT consumer protection pattern, the problem-first example — all are high quality and belong somewhere in the constitution.

**Addition:** A **Content Routing** step in Phase 4 (Assess & Correct) and Phase 2 (PR Review) that, for each misplaced artifact found:

```
For each BLOCKING law boundary violation (misplaced BUS-* or PRD-* example):

  Step: Route, don't delete
  1. Identify the correct destination avatar(s):
     - BUS-2.1 (FAA compliance) C++ example → crew-training-scheduling avatar (uses C++)
     - PRD-1.2 (problem-first) C++ example → any product avatar that uses C++ and needs a problem-first example
  2. Draft a routing proposal: create a stub file at the destination with a header noting the source and the routing rationale
  3. Flag the routing in the evidence file: "BUS-2.1 C++ example routed to crew-training-scheduling — see routing-proposal.md"
  4. Remove from current (incorrect) avatar
  5. Do NOT delete the content — preserve it in hangar-ai-specs/evidence/avatar-content-routing-{domain}.md pending destination avatar PR
```

**Content Routing is not automatic adoption.** The destination avatar still needs to go through its own Enrich or Assess & Correct mode to formally incorporate the routed content. But the content is preserved and tracked, not discarded.

**Why this matters:** "Remove and discard" creates contributor friction and wastes good work. "Remove and route" preserves the author's contribution, directs it to where it creates value, and gives the author credit for the correct content.

---

### Improvement 4 — Manifest Unknown Blocks Guard

**Evidence:** The C++ manifest contained 6 blocks outside the defined schema: `governance_overrides`, `brownfield_adoption`, `skill_parity`, `project_archetypes`, `anti_patterns`, `retrieval_triggers`. The current Phase 2 scan checks for missing required blocks but does not check for unexpected additional blocks.

**Addition:** An explicit **unknown blocks check** in Phase 2, Step 2.1:

```
Known manifest blocks (exhaustive list):
  avatar, stack (tech), domain (product), core_journeys (product),
  activates, specializes_laws, conventions, commands, project_structure,
  dependencies, compliance_domains (product), tags

For each block in the submitted manifest.yaml:
  Is the block name in the known list?
    YES → proceed
    NO  → 🟡 WARN: Unknown manifest block detected: [{block_name}]
          Classify:
          - Content that belongs in guidance.md → move it
          - Content that belongs in examples/ → move it
          - Content that belongs in AVATAR-RAG-INDEX.yaml → move it
          - Content that asserts governance or policy → Safeguard 5 triage (shadow governance)
          - Legitimate structural extension → file manifest schema amendment
```

**Why this matters:** The manifest is being used as a second guidance.md and a second AVATAR-RAG-INDEX entry and a compliance framework. An allowlist check is cheap and catches schema drift before it compounds. Every block in PR #14 that didn't belong in the manifest would have been flagged on day one.

---

### Improvement 5 — activates.skills Existence Validation

**Evidence:** The C++ manifest references `skill-06-atomic-tdd`, `skill-07-vertical-slice-dev`, `skill-08-code-review`, `skill-04-business-domain-modeling` in `activates.skills`. It also references 23 `skill-cpp-*` skills created in `agent-skills/skills-by-domain/platform-engineering/`. The workflow does not currently validate that any of these referenced skills actually exist.

**Addition:** A skill existence check in Phase 2, Step 2.1:

```
For each skill in activates.skills:
  Does a corresponding file exist in agent-skills/ matching the skill ID?
    skill-{id}.md in agent-skills/base/ OR
    skill-{id}.md in agent-skills/skills-by-domain/**/ OR
    {id}.md matched by prefix convention

    YES → ✅
    NO  → 🔴 BLOCKING: Referenced skill does not exist — {skill-id}
           Options: create the skill (file a skill proposal) or remove the reference
```

**Inverse check** — also run in PR Review mode:

```
For each new skill file added in the PR diff (agent-skills/**/*.md):
  Is this skill referenced in at least one avatar's activates.skills?
    NO → 🟡 WARN: Orphaned skill — not referenced by any avatar. Add to at least one avatar or remove.
```

**Why this matters:** An avatar that references a non-existent skill fails silently — the agent tries to load the skill and gets nothing. The inverse check catches "skill proliferation without avatar integration" — 23 skills created that may be disconnected from the avatars they're meant to serve.

---

### Improvement 6 — Cross-Avatar Blast Radius Check

**Evidence:** When we found `BUS-7.1` in the C++ avatar's examples, the same violation already existed in `databricks-pyspark`, `postgresql-sqlalchemy`, `azure-openai`, and `opentelemetry-python`. And `PRD-3.4` was already in `react-typescript`. A single violation in one avatar is often a pattern across many avatars.

**Addition:** After any violation is found in Phase 2 (Scan), run a **blast radius check** that scans all avatars of the same type for the same violation pattern:

```
Blast Radius Check — triggered by each BLOCKING finding in Phase 2:

  Finding: BUS-7.1 in avatars/technology/cpp/examples/
  Blast radius query: Scan all avatars/technology/*/examples/ and */manifest.yaml for BUS-7.1 references
  Result: [databricks-pyspark, postgresql-sqlalchemy, azure-openai, opentelemetry-python]

  Output in evidence file:
    BLAST RADIUS: BUS-7.1 in tech avatars affects 5 avatars:
      - cpp (this PR)
      - databricks-pyspark
      - postgresql-sqlalchemy
      - azure-openai
      - opentelemetry-python
    Recommended: file a single Assess & Correct run across all 5 rather than fixing one at a time.
```

**Why this matters:** Without blast radius, each violation is fixed one avatar at a time as they're discovered. With blast radius, a single violation finding produces a remediation scope across the entire avatar corpus — enabling bulk correction proposals instead of 5 separate PRs. It also surfaces the constitutional health of the full avatar registry, not just the avatar being assessed.

---

### Improvement 7 — Avatar Versioning Protocol

**Evidence:** The cpp manifest is `version: "2.0.0"`. No version existed before this PR. The workflow says avatars have a `version` field in semver format but never defines when to bump major vs minor vs patch.

**Addition:** An explicit versioning protocol applied at Phase 6 (Commit):

| Change Type | Semver Bump | Examples |
|---|---|---|
| Initial creation | `1.0.0` | New avatar from Generate mode |
| Add new law specialization, new use-case, new example | `MINOR` (x.Y.0) | Adding ENG-7.1 example to existing avatar |
| Correct existing content, fix token budgets, fix broken references | `PATCH` (x.y.Z) | Assess & Correct for schema violations |
| Remove law specializations, change avatar type, restructure manifest schema | `MAJOR` (X.0.0) | Removing BUS-* from tech avatar, changing from `product` to `technology` type |
| Enrich with codebase (replaces generic examples with real patterns) | `MINOR` | Enrich mode always bumps minor — it changes the knowledge content |

**Deprecation:** If an avatar is no longer maintained (stack is end-of-life, domain no longer exists), it must be marked in `avatars/index.yaml`:
```yaml
status: deprecated
deprecated_since: "2026-04-10"
replaced_by: "avatar-{successor}"  # optional
sunset_date: "2026-10-10"          # 6-month sunset window
```

Deprecated avatars are excluded from RAG indexing after `sunset_date` but remain in the repository for historical reference.

---

### Updated Operating Modes Table

| Mode | Trigger | Starting State | End State |
|---|---|---|---|
| **0 — Pre-flight** | "I want to create/enrich [domain] avatar" — before any files created | Intent only | Pre-flight contract in evidence; law domain acknowledged |
| **1 — Generate** | "Create a new [tech/product] avatar for [domain]" | No avatar exists | Constitutionally valid avatar committed |
| **2 — Assess & Correct** | "Assess and fix the [domain] avatar" | Avatar exists, completeness unknown | Avatar corrected, content routed, validated, committed |
| **3 — Validate** | "Validate the [domain] avatar" | Avatar exists | Validation report committed; no changes made |
| **4 — Enrich** | "Enrich the [domain] avatar with [codebase path]" | Avatar exists + codebase provided | Avatar updated with codebase-grounded patterns |
| **5 — PR Review** | PR opened/updated touching `avatars/**` or `agent-skills/**` | PR open | Structured review comment posted; no files modified |

---

## Out of Scope

- Automated token counting tooling (Phase 5 RAG validation uses manual/agent counting, not a script)
- Bulk avatar migration (existing avatars are not retroactively corrected — they receive `rag_validated: unknown` until explicitly run through Validate or Assess mode)
- Industry avatar support in the first iteration (technology and product-type are the primary types; industry avatars follow the same schema but are not used as workflow examples in this proposal)
- CI/CD automation for avatar validation (future proposal; this workflow is agent-executed)

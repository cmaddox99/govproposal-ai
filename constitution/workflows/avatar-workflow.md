---
workflow:
  id: avatar-workflow
  name: Avatar Workflow — Six-Mode Avatar Lifecycle Management
  version: "1.0.0"
  avatar_context: [technology, product-type, industry]
  laws: [ENG-1.2, ENG-10.1, ENG-11.1, ENG-11.2]
  skills: [skill-avatar-workflow, skill-spec-governance]
  preceded_by: null
  modes: [pre-flight, generate, assess-correct, validate, enrich, pr-review]
---

# Workflow: Avatar Workflow — Six-Mode Avatar Lifecycle Management

> **Laws enforced:** ENG-11.1 (NON-NEGOTIABLE), ENG-1.2 (NON-NEGOTIABLE), ENG-10.1
> **Skills:** `skill-avatar-workflow`, `skill-spec-governance`
> **Schema:** `docs/guides/avatar-model-schema.md`
> **Purpose:** Govern the complete lifecycle of constitution avatars — from creation through correction, validation, codebase enrichment, and PR review — ensuring every avatar satisfies the Avatar Model Schema, respects law domain boundaries, and meets RAG retrieval thresholds before entering the constitution.

---

## Prerequisites — Phase Gate Prerequisites (ENG-12.1)

Each phase gate requires:
1. Phase artifact committed to `hangar-ai-specs/changes/<project-id>/`
2. `aa-citation-audit` run on the artifact (ENG-14.1 — pre-jury citation gate)
3. Multi-cognition jury R1 + R2 deliberation (PRD-2.6 — 5 jurors, distinct LLM models)
4. Judicial synthesis APPROVED verdict committed
5. `aa-jury-gate` mechanical validation PASS (PRD-2.6 enforcement)
6. **Human reviews jury synthesis findings before approving phase advance** ← THE CHECKPOINT

> **ENG-12.1 (NON-NEGOTIABLE):** Agent cannot advance to a new phase without a human reviewing jury synthesis findings. Jury APPROVED verdict required — agent cannot self-declare phase complete.

---

## Operating Modes

| Mode | Trigger Phrases | Starting State | End State |
|---|---|---|---|
| **0 — Pre-flight** | "I want to create a [X] avatar", "I'm going to add an avatar for [X]" | Intent only — no files exist | Pre-flight contract committed to evidence |
| **1 — Generate** | "Create a new avatar for [X]", "Generate a [tech/product] avatar for [X]" | No avatar exists | Constitutionally valid avatar committed to index |
| **2 — Assess & Correct** | "Assess the [X] avatar", "Fix the [X] avatar", "Is the [X] avatar complete?" | Avatar exists, completeness unknown | Avatar corrected, content routed, validated, committed |
| **3 — Validate** | "Validate the [X] avatar", "Check if [X] avatar is constitutionally valid" | Avatar exists | Validation report committed; no files modified |
| **4 — Enrich** | "Enrich the [X] avatar with [codebase]", "Update [X] avatar from this codebase" | Avatar exists + codebase path provided | Avatar updated with codebase-grounded patterns |
| **5 — PR Review** | PR opened/updated touching `avatars/**`, `agent-skills/**`, or `AVATAR-RAG-INDEX.yaml` | PR open with changeset | Structured PASS/BLOCKED review comment posted; no files modified |

---

## Phase Table

| Phase | Name | Modes | Key Activities | Constitutional Gate |
|---|---|---|---|---|
| 0 | Pre-flight | Pre-flight | Intent classification; deduplication check; law boundary acknowledgement; RAG query pattern agreement | Pre-flight evidence file committed |
| 1 | Identify | All | Mode + type + domain confirmation; existing avatar location; mode selection | Mode confirmed; avatar path resolved |
| 2 | Scan | Assess, Validate, Enrich, PR Review | Schema completeness; manifest unknown blocks guard; law boundary check; activates.skills existence; shadow governance detection; blast radius trigger | Gap report committed to evidence |
| 3 | Discover | Generate, Enrich | Law discovery by avatar type; 5 canonical RAG query patterns defined | Non-negotiable laws listed; query patterns documented |
| 4 | Build / Correct / Enrich | Generate, Assess, Enrich | Generate scaffold (Generate); gap resolution + content routing (Assess); codebase extraction (Enrich) | All schema-required files present; token budgets within limits |
| 5 | RAG Validate | All | Simulate 5 canonical queries; token budget enforcement; recall/precision proxy evaluation | Recall ≥95% (5/5); max query load ≤3,500 tokens; 0 BLOCKING violations |
| 6 | Commit | Generate, Assess, Enrich | Registry updates; versioning (semver); evidence commit; deprecation if applicable | `index.yaml` + `AVATAR-RAG-INDEX.yaml` updated; evidence committed |

> **Validate mode:** Phases 1, 2, 5 only — read-only, no files modified.
> **PR Review mode:** Phases 2 and 5 only, scoped to PR diff — no files modified, review comment posted.

---

## Phase 0: Pre-flight (Pre-flight Mode Only)

**Goal:** Validate the author's intent before any files are created. Every violation caught here prevents N commits of rework.

### Step 0.1 — Classify Intent

| Intent Pattern | Inferred Mode | Avatar Type |
|---|---|---|
| Language, framework, or stack name | Generate → technology | `technology` |
| AA product domain name | Generate → product-type | `product` |
| Regulatory standard or industry vertical | Generate → industry | `industry` |
| Existing avatar mentioned | Offer Assess / Validate / Enrich instead | — |

### Step 0.2 — Run Deduplication (Safeguard 1)

> See Phase 1, Step 1.2 for full deduplication logic. Pre-flight runs the same check before any work begins.

### Step 0.3 — Law Boundary Acknowledgement (Safeguard 2)

Present the Permitted Law Matrix for the declared avatar type and require explicit acknowledgement:

**For technology avatars:**
> "This avatar is `type: technology`. It may only specialize `ENG-*` laws. `PRD-*` and `BUS-*` laws are FORBIDDEN in this avatar. Product and compliance concerns belong in product-type or industry avatars that compose with this one. Do you acknowledge this constraint?"

**For product-type avatars:**
> "This avatar is `type: product`. It may specialize `PRD-*` and `BUS-*` laws. `ENG-6.x` is conditionally permitted with justification. `ENG-1.x`–`ENG-5.x` and `ENG-7.x`–`ENG-12.x` are FORBIDDEN. Do you acknowledge this constraint?"

**For industry avatars:**
> "This avatar is `type: industry`. It may specialize `BUS-*` and `PRD-*` laws. `ENG-6.x` is conditionally permitted. All other `ENG-*` laws are FORBIDDEN. Do you acknowledge this constraint?"

### Step 0.4 — RAG Query Pattern Agreement

Define 5 canonical RAG queries the avatar must answer before content is written. These become the Phase 5 test cases. See `docs/guides/avatar-model-schema.md` Section 8 for canonical query templates by avatar type.

### Step 0.5 — Product Taxonomy Check (product-type only)

Does the proposed `domain.category` match an established category in `avatars/product-type/index.yaml`?
- YES → Proceed
- NO → Two options: map to closest existing category with justification, or file a taxonomy extension proposal before proceeding. **Avatar cannot be committed to `index.yaml` without a taxonomy entry.**

**Phase Gate:** Commit `hangar-ai-specs/evidence/avatar-preflight-{domain}.md` documenting: confirmed type, acknowledged law boundary, 5 agreed RAG queries, taxonomy category.

---

## Phase 1: Identify (All Modes)

**Goal:** Confirm mode, avatar type, domain slug, and avatar path before any scan or build begins.

### Step 1.1 — Classify Mode

| Trigger | Mode |
|---|---|
| "Create / generate / new avatar for [X]" | Generate (Mode 1) |
| "Assess / fix / correct / check the [X] avatar" | Assess & Correct (Mode 2) |
| "Validate / audit / verify the [X] avatar" | Validate (Mode 3) |
| "Enrich [X] avatar with [codebase path]" | Enrich (Mode 4) |
| PR opened/updated touching `avatars/**` or `agent-skills/**` | PR Review (Mode 5) |

### Step 1.2 — Deduplication Check (Safeguard 1 — Generate mode)

**Tier 1 — Exact Match:**
```
Does avatars/{inferred-type}/{proposed-slug}/ already exist?
  YES → BLOCK Generate. Offer Assess, Validate, or Enrich instead.
  NO  → Continue to Tier 2.
```

**Tier 2 — Semantic Overlap:**

Score the proposed avatar against all existing avatars of the same type:

| Overlap Signal | Weight |
|---|---|
| Same primary language or framework (technology) | 40% |
| Same AA product domain or >50% of core journeys (product) | 40% |
| >60% shared `specializes_laws` entries | 10% |
| >50% shared `activates.skills` | 10% |

| Score | Action |
|---|---|
| ≥70% | 🔴 REDIRECT — present existing avatar + specific gaps that would justify a new one |
| 40–69% | 🟡 WARN — surface overlapping avatar; require explicit justification before proceeding |
| <40% | ✅ PROCEED — document nearest neighbor in evidence |

**Merge Offer (≥70% overlap):**
```
OVERLAP DETECTED: Proposed avatar "[X]" overlaps {N}% with existing "[Y]".

Option A (Recommended): Enrich [Y] — add [specific gaps] to the existing avatar.
Option B: Justify new avatar — explain what [X] covers that [Y] cannot.
  Required: Written justification committed to evidence before proceeding.
```

### Step 1.3 — Locate Avatar

For Assess, Validate, Enrich, PR Review: confirm the avatar directory exists at `avatars/{type}/{domain-slug}/`. If not found, offer Generate mode instead.

**Phase Gate:** Mode confirmed; avatar type and domain slug agreed; avatar path resolved.

---

## Phase 2: Scan (Assess, Validate, Enrich, PR Review Modes)

**Goal:** Produce a complete gap report against the Avatar Model Schema and all 5 safeguard families before any corrections begin.

### Step 2.1 — Schema Completeness Check

```
manifest.yaml
  ✅ File present?
  ✅ avatar.id valid? (starts with "avatar-", contains directory slug, registered in avatars/index.yaml)
  ✅ avatar.type is technology | product | industry?
  ✅ avatar.version present (semver)?
  ✅ stack block present (technology only)?
  ✅ domain block present (product only)?
  ✅ domain.personas has ≥2 entries (product only)?
  ✅ activates.skills has ≥2 entries?
  ✅ activates.skills — each skill exists in agent-skills/ ? (Safeguard 5)
  ✅ activates.workflows has ≥1 entry?
  ✅ specializes_laws has ≥1 non-negotiable law?
  ✅ all example_file references resolve to existing files?
  ✅ manifest estimated tokens ≤150?
  ✅ all blocks in manifest are in the known allowlist? (Safeguard 5 — unknown blocks guard)

guidance.md
  ✅ File present?
  ✅ Non-Negotiable Laws section present?
  ✅ Estimated tokens ≤450?

examples/
  ✅ Directory present?
  ✅ One file exists per law in specializes_laws?
  ✅ Each example file estimated tokens ≤850?

use-cases/ (product-type only)
  ✅ Directory present?
  ✅ ≥1 use-case with README.md?
  ✅ Each README.md estimated tokens ≤1,500?
```

### Step 2.2 — Law Domain Boundary Check (Safeguard 2)

```
For each law in specializes_laws:
  Extract prefix: ENG | PRD | BUS
  Apply Permitted Law Matrix (see avatar-model-schema.md Section 4):

  technology + PRD-* → 🔴 BLOCKING
  technology + BUS-* → 🔴 BLOCKING (replace with ENG-6.x equivalent if applicable)
  product + ENG-1.x–5.x → 🔴 BLOCKING
  product + ENG-7.x–12.x → 🔴 BLOCKING
  product + ENG-6.x → 🟡 WARN — permitted with inline justification
  industry + ENG-* (except 6.x) → 🔴 BLOCKING

For each examples/ file:
  Apply same law prefix check based on filename (BUS-*.md, PRD-*.md in tech avatar → BLOCKING)
```

### Step 2.3 — Law ID Validity Check (Safeguard 4)

```
For each law in specializes_laws:
  Validate law.id exists in the appropriate _domain.yaml:
    ENG-* → laws/engineering/_domain.yaml
    PRD-* → laws/product/_domain.yaml
    BUS-* → laws/business/_domain.yaml
  Law ID not found → 🔴 BLOCKING: Invalid law reference
```

### Step 2.4 — Shadow Governance Detection (Safeguard 5 — Assess & Correct, Enrich, PR Review)

Scan all avatar files for the following patterns:

| Pattern | Detection | Classification |
|---|---|---|
| Invented law IDs | Regex `[A-Z]{2,6}-\d+\.\d+` not matching ENG-\|PRD-\|BUS- | 🔴 BLOCKING |
| Ungrounded mandatory requirements | "must" / "required" / "NON-NEGOTIABLE" without adjacent law ID | 🟡 SHADOW GOVERNANCE |
| Embedded skill definitions | "skill-" prefix in headings defining agent behaviors (not referencing existing skills) | 🟡 SHADOW GOVERNANCE |
| Law overrides or self-approval | "override:", "does not apply", `governance_overrides:`, self-approval comments | 🔴 HARD BLOCK |
| Unknown manifest blocks | Any block not in the manifest allowlist | 🟡 SHADOW GOVERNANCE |
| Governance framework with authority assertions | "Authority: {org}" in avatar files | 🔴 SHADOW GOVERNANCE |

**Triage for each finding:**

| Finding | Question | Resolution |
|---|---|---|
| Invented law ID | Is this a genuine constitutional gap? | YES → file amendment proposal. NO → remove, cite nearest existing law. |
| Ungrounded mandatory requirement | Covered by existing law? | YES → replace with law citation. NO → file amendment. |
| Embedded skill definition | Skill already in `agent-skills/`? | YES → remove duplicate; add to `activates.skills`. NO → file skill proposal. |
| Law override / self-approval | Legitimate exception? | YES → file ENG-10.3 Exception Request. NO → remove; law applies as written. |
| Unknown manifest block | Where does this content belong? | Move to correct artifact per manifest allowlist (Section 3 of schema). |

### Step 2.5 — activates.skills Existence Validation (Safeguard 5)

```
For each skill in activates.skills:
  Search for matching file in agent-skills/base/ and agent-skills/skills-by-domain/**/
  Found → ✅
  Not found → 🔴 BLOCKING: Referenced skill does not exist — {skill-id}

Inverse check (PR Review mode — for new skill files in PR diff):
  For each new agent-skills/**/*.md added in the PR:
    Is this skill referenced by at least one avatar's activates.skills?
    NO → 🟡 WARN: Orphaned skill — add to at least one avatar or remove.
```

### Step 2.6 — Blast Radius Check

```
For each BLOCKING law boundary violation found in Step 2.2:
  Query: scan all avatars/{same-type}/*/manifest.yaml and examples/ for the same law reference
  Collect: list of all affected avatars
  Output in evidence: "BLAST RADIUS: {law} affects {N} avatars: [{list}]"
  Recommendation: file a single Assess & Correct run scoped to all affected avatars
```

### Gap Classification

| Severity | Condition | Impact |
|---|---|---|
| 🔴 BLOCKING | Missing required file, law boundary violation, invalid law ID, law override, invented law ID | Avatar cannot be committed; RAG pipeline will fail or produce invalid results |
| 🟡 WARNING | Token budget exceeded, missing use-cases (product), shadow governance (non-override), orphaned skill | RAG retrieval degraded; quality issue |
| 🟢 ADVISORY | Missing optional conventions, no anti-patterns section, weak examples | Improvement opportunity; does not block |

**Phase Gate:** Gap report committed to `hangar-ai-specs/evidence/avatar-scan-{domain}.md`.

---

## Phase 3: Discover (Generate, Enrich Modes)

**Goal:** Surface the correct laws and RAG query patterns before any artifacts are generated or modified.

### Step 3.1 — Law Discovery

**For technology avatars:**
- Non-negotiable baseline: `ENG-4.1` (Atomic TDD), `ENG-3.1` (Complexity Limits) — always required
- Add security laws (`ENG-6.x`) if the stack involves HTTP, auth, or data persistence
- Add architecture laws (`ENG-2.x`) if the stack supports DDD patterns
- For Enrich mode: compare existing `specializes_laws` against the standard baseline — surface gaps

**For product-type avatars:**
- Non-negotiable baseline: `PRD-1.1` (Discovery), `PRD-2.1` (Journey), `PRD-5.1` (Metrics) — always required
- Add compliance laws (`BUS-2.x`) if the domain has regulatory obligations
- Add privacy laws (`BUS-4.x`) if the domain handles PII
- Add security implementation laws (`ENG-6.x`) if the product has direct security obligations

**For industry avatars:**
- Non-negotiable baseline: `BUS-2.1` (Regulatory Mapping), `BUS-2.2` (Control Framework) — always required
- Add applicable `PRD-*` laws for the industry's product characteristics
- Add `ENG-6.x` if the industry standard has specific security implementation requirements

### Step 3.2 — 5 Canonical RAG Query Patterns

Define 5 queries the avatar must answer. These become the Phase 5 test cases. Use the canonical templates from `docs/guides/avatar-model-schema.md` Section 8 as the starting point, customized for the specific stack or domain.

**Phase Gate:** Non-negotiable laws listed with citations; 5 canonical query patterns documented.

---

## Phase 4: Build / Correct / Enrich

**Goal:** Produce or repair all avatar artifacts to satisfy the Avatar Model Schema.

### Mode 1 — Generate: Build from Scratch

**Step 4.1 — Scaffold Avatar Directory**

```
avatars/{type}/{domain-slug}/
├── manifest.yaml
├── guidance.md
└── examples/
    └── (one file per non-negotiable law from Phase 3)
```

For product-type avatars, also scaffold:
```
└── use-cases/
    └── {primary-use-case}/
        └── README.md
```

**Step 4.2 — Generate `manifest.yaml`**

Follow the non-negotiable field schema from `docs/guides/avatar-model-schema.md` Section 3. Every `specializes_laws` entry must reference an `example_file` that will be created in Step 4.3. Set `version: "1.0.0"`.

**Step 4.3 — Generate `guidance.md`**

Follow the required structure from `docs/guides/avatar-model-schema.md` Section 5. Stay within 450 tokens. If the Non-Negotiable Laws section exceeds budget, move implementation notes to the corresponding `examples/` files.

**Step 4.4 — Generate Law Examples**

One file per non-negotiable law. Follow the format from `docs/guides/avatar-model-schema.md` Section 6. Stay within 850 tokens per file.

### Mode 2 — Assess & Correct: Fix Gaps from Phase 2

Address BLOCKING gaps first, then WARNINGs:

| Gap Type | Correction Action |
|---|---|
| Missing required manifest field | Add field; re-validate slug matches directory |
| Missing `guidance.md` Non-Negotiable Laws section | Add section with citations from `specializes_laws` |
| Missing law example file | Generate file; add `example_file` reference to manifest |
| Broken `example_file` reference | Locate or regenerate the referenced file |
| Law boundary violation (BUS/PRD in tech avatar) | **Content Routing** — see Step 4.5 below |
| Unknown manifest block | Move to correct artifact per allowlist |
| Token budget exceeded | Split or summarize the offending document |
| Missing use-cases (product-type) | Generate primary use-case from domain journeys |
| Shadow governance finding | Apply triage per Phase 2, Step 2.4 |
| activates.skills reference not found | Remove broken reference or create the missing skill |

**Step 4.5 — Content Routing Protocol (Route, Don't Delete)**

When a law boundary violation is found (e.g., BUS-* in a tech avatar):

```
For each misplaced artifact:
  1. Identify correct destination:
     - BUS-* example in tech avatar → product-type or industry avatar that uses this stack
     - PRD-* example in tech avatar → product-type avatar that uses this stack

  2. Draft routing note in evidence file:
     "{file} routed from {source-avatar} → {destination-avatar}: {reason}"

  3. Preserve content in:
     hangar-ai-specs/evidence/avatar-content-routing-{domain}.md

  4. Remove from current (incorrect) avatar

  5. Do NOT open the destination avatar PR automatically —
     flag the routing for a future Enrich run on the destination avatar
```

Content Routing is not automatic adoption. The destination avatar receives the content as a candidate for its next Enrich mode run.

### Mode 4 — Enrich: Extract Patterns from Codebase

**Step 4.1 — Codebase Discovery**

```
Analyze the target codebase:
  - Actual project structure (real directories, not generic templates)
  - Testing framework, test file naming conventions, test count
  - CI/CD commands from package.json / Makefile / pom.xml / pyproject.toml / CMakeLists.txt
  - Real dependency versions from lockfiles
  - Naming conventions from ≥10 file samples
  - Anti-patterns: complexity violations, missing tests, inconsistent naming
```

**Step 4.2 — Map Patterns to Avatar**

Replace generic manifest content with codebase-grounded specifics:
- `project_structure` block → actual directory tree (3 levels, sampled)
- `commands` block → actual CI/CD commands
- `conventions` naming block → patterns observed in ≥10 real files

**Step 4.3 — Regenerate Affected Examples**

For any law example that was previously generic: replace with real code extracted from the codebase, preserving the law example format from `docs/guides/avatar-model-schema.md` Section 6. Anonymize business logic; preserve structural patterns.

**Phase Gate (all modes):** All schema-required files present; token budgets within limits; no broken `example_file` references; no BLOCKING schema violations.

---

## Phase 5: RAG Validate (All Modes)

**Goal:** Simulate the RAG retrieval pipeline and verify the avatar meets constitutional thresholds.

### Step 5.1 — Simulate 5 Canonical Queries

For each query defined in Phase 3 (or the standard canonical queries for Validate/PR Review modes):
1. Identify which avatar files would be loaded by the selective chunk strategy
2. Estimate token count for all loaded files
3. Confirm the query is answerable from the loaded files

### Step 5.2 — Evaluate Thresholds

| Metric | Threshold | Failure |
|---|---|---|
| Recall proxy | ≥95% (5/5 queries answered) | 4/5 = WARNING; 3/5 or fewer = FAIL |
| Precision proxy | ≥90% (no irrelevant files loaded) | Loaded file irrelevant to query = WARNING |
| Total query token load | ≤3,500 per query | Any query exceeding budget = FAIL |
| Schema violations | 0 BLOCKING violations | Any BLOCKING violation = FAIL |

### Step 5.3 — RAG Validation Report

Commit to `hangar-ai-specs/evidence/avatar-rag-{domain}.md` using the template from `docs/guides/avatar-model-schema.md` Section 8.

**Phase Gate (hard stops — return to Phase 4):**
- Recall < 5/5 → 🔴 FAIL
- Any query > 3,500 tokens → 🔴 FAIL — trim offending document
- Any BLOCKING schema violation → 🔴 FAIL

---

## Phase 6: Commit (Generate, Assess, Enrich Modes)

**Goal:** Update all registry files and commit all artifacts with a constitutional commit message.

### Step 6.1 — Update `avatars/index.yaml`

Add or update the avatar entry with all required fields:
```yaml
- id: avatar-{type}-{domain}
  name: "..."
  type: technology | product | industry
  path: {type}/{domain}/
  version: "x.y.z"           # per versioning protocol
  status: active
  rag_validated: true
  last_validated: "{date}"
```

### Step 6.2 — Update `AVATAR-RAG-INDEX.yaml`

Add or update the avatar's RAG entry:
- File list with token estimates
- Canonical search queries (from Phase 3)
- Key metrics (product-type avatars)
- Law specializations list

### Step 6.3 — Apply Versioning Protocol

| Change Type | Semver Bump |
|---|---|
| New avatar (Generate) | `1.0.0` |
| Added law specialization, use-case, or example (Assess adding missing content) | `MINOR` |
| Corrected existing content, fixed broken references, trimmed tokens | `PATCH` |
| Removed law specializations, corrected law boundary violations | `MAJOR` |
| Codebase enrichment (Enrich) | `MINOR` |

### Step 6.4 — Render Gate (ENG-13.1 NON-NEGOTIABLE)

Before updating `index.yaml` or committing, render all evidence artifacts from this run and confirm in browser:

```
RENDER GATE — ENG-13.1 NON-NEGOTIABLE
─────────────────────────────────────────────────────────────
For each artifact produced in this run:
  aa-artifact-render hangar-ai-specs/changes/{spec-id}/rag-validation-{avatar-id}.md
  aa-artifact-render hangar-ai-specs/changes/{spec-id}/blast-radius-{avatar-id}.md   # if violations found
  aa-artifact-render hangar-ai-specs/changes/{spec-id}/discovery-handoff-{avatar-id}.md

open all rendered .html files in browser
→ Human confirms each reads correctly: yes / no
→ If no: return to Phase 5 and resolve before re-rendering
→ If yes: proceed to Step 6.5
```

Templates:
- RAG validation: `docs/templates/avatars/rag-validation-template.md`
- Discovery handoff: `docs/templates/avatars/discovery-handoff-template.md`

### Step 6.5 — Commit

```
feat(avatar): {mode} {domain} avatar — {brief description}

Mode: {Generate | Assess & Correct | Enrich}
Avatar: {avatar.id}  |  Type: {type}  |  Version: {x.y.z}

Changes:
- {list of files created/modified}

RAG validation: PASS (recall 5/5, max {N} tokens/query)
Schema violations: 0

Ref: hangar-ai-specs/changes/avatar-workflow/PROPOSAL.md

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

**Phase Gate:** `AVATAR-RAG-INDEX.yaml` updated; `avatars/index.yaml` entry present and valid; RAG evidence committed; all evidence artifacts rendered as HTML and reviewed in browser (ENG-13.1).

---

## Phase 5 (PR Review Mode): Review Incoming PR

**Goal:** Assess an incoming PR's avatar changes against the Avatar Model Schema and all safeguards. Post a structured review comment. Modify no files.

### Step PR.1 — Identify Changed Avatars

From the PR diff, collect all files under `avatars/**` and `agent-skills/**`. Group by avatar domain.

### Step PR.2 — Run Scan (Phase 2) Against Diff

Run all Phase 2 steps (2.1 through 2.6) against each modified avatar. Evaluate only the post-change state of the files in the diff.

### Step PR.3 — Run RAG Validate (Phase 5)

Simulate the 5 canonical queries for each modified avatar using the post-change file states.

### Step PR.4 — Post Review Comment

Post a structured review comment to the PR using this template:

```markdown
## Avatar Workflow Assessment — {Avatar Name}

> Assessed against: docs/guides/avatar-model-schema.md
> Mode: PR Review

### Verdict: ✅ PASS / 🔴 BLOCKED

## Safeguard 1 — Deduplication: ✅ PASS / 🔴 FAIL
[finding]

## Safeguard 2 — Law Domain Boundary: ✅ PASS / 🔴 FAIL ({N} violations)
[violation table if failed]

## Safeguard 3 — Product Taxonomy: ✅ PASS / 🔴 FAIL / ✅ N/A
[finding]

## Safeguard 4 — Law ID Validity & Content Compliance: ✅ PASS / 🔴 FAIL
[finding]

## Safeguard 5 — Shadow Governance: ✅ PASS / 🔴 FAIL ({N} findings)
[findings table if failed]

## RAG Validation: ✅ PASS / 🔴 FAIL
[query simulation table]

## Required Changes Before Merge
[table of required actions if BLOCKED]
```

**PR Review is read-only.** No files are modified. The author resolves violations and re-triggers PR Review (automatically on new push, or manually).

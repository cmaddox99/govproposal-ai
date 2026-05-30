# Avatar Model Schema

> **Version:** 1.0.0
> **Authority:** hangar-ai-constitution v2.0.0
> **Enforced by:** `workflows/avatar-workflow.md` — Phases 2 and 5
> **Referenced by:** `AVATAR-RAG-INDEX.yaml`, `avatars/index.yaml`

This document is the **explicit contract** that every constitutionally valid avatar must satisfy. It is the source of truth for the `avatar-workflow` Phase 2 (Scan) completeness check and Phase 5 (RAG Validate) budget enforcement.

---

## 1. Required Directory Structure

### All Avatar Types (Minimum)

```
avatars/{type}/{domain-slug}/
├── manifest.yaml     ← REQUIRED — identity, stack/domain, law specializations
├── guidance.md       ← REQUIRED — non-negotiable laws section mandatory
└── examples/         ← REQUIRED — one file per law in specializes_laws
```

### Technology Avatars (`type: technology`)

```
avatars/technology/{stack-slug}/
├── manifest.yaml
├── guidance.md
└── examples/
    ├── ENG-4.1-atomic-tdd.md       ← REQUIRED (non-negotiable law)
    ├── ENG-3.1-complexity.md       ← REQUIRED (non-negotiable law)
    └── {ENG-x.x}-{topic}.md       ← one per additional specializes_laws entry
```

### Product-Type Avatars (`type: product`)

```
avatars/product-type/{domain-slug}/
├── manifest.yaml
├── guidance.md
├── examples/
│   ├── PRD-1.1-discovery.md       ← REQUIRED (non-negotiable law)
│   ├── PRD-2.1-journey.md         ← REQUIRED (non-negotiable law)
│   └── {PRD|BUS-x.x}-{topic}.md  ← one per additional specializes_laws entry
└── use-cases/                      ← REQUIRED — minimum 1
    └── {primary-use-case}/
        └── README.md
```

### Industry Avatars (`type: industry`)

```
avatars/industry/{standard-slug}/
├── manifest.yaml
├── guidance.md
└── examples/
    ├── BUS-2.1-regulatory-mapping.md  ← REQUIRED (non-negotiable law)
    ├── BUS-2.2-control-framework.md   ← REQUIRED (non-negotiable law)
    └── {BUS-x.x}-{topic}.md          ← one per additional specializes_laws entry
```

---

## 2. Token Budget Constraints

These budgets are enforced at Phase 5 (RAG Validate). Violations block the commit gate.

| Document | Max Tokens | Violation Level | Action |
|---|---|---|---|
| `manifest.yaml` | 150 tokens | 🔴 BLOCKING | Trim; move content to guidance.md or examples/ |
| `guidance.md` | 450 tokens | 🔴 BLOCKING | Restructure; move detail to examples/ |
| Each `examples/*.md` | 850 tokens | 🟡 WARNING | Split into sub-examples |
| Each `use-cases/*/README.md` | 1,500 tokens | 🔴 BLOCKING | Split into phases |
| Total per RAG query load | 3,500 tokens | 🔴 BLOCKING | Avatar exceeds RAG context window |

> **Note on governance overrides:** A token budget override requires a formal ENG-10.3 Exception Request filed as a separate proposal in `hangar-ai-specs/changes/`. An avatar cannot self-approve a token budget change. The self-approval comment pattern `# Approved: {date}` inside a manifest has no constitutional authority.

---

## 3. Non-Negotiable `manifest.yaml` Fields

All fields below are **REQUIRED**. Missing any field is a 🔴 BLOCKING violation.

```yaml
avatar:
  id: <see id format rules below>       # must be registered in avatars/index.yaml
  type: technology | product | industry # one of three — no other values
  name: "Human Readable Name"           # title-cased display name
  version: "x.y.z"                      # semver — see Section 6 for bump rules

# --- technology avatars ---
stack:                                   # REQUIRED if type: technology
  language: "..."                        # primary language and version
  framework: "..."                       # primary framework (or "N/A")
  testing: [...]                         # minimum 1 testing framework

# --- product-type avatars ---
domain:                                  # REQUIRED if type: product
  category: "..."                        # must match avatars/product-type/index.yaml taxonomy
  description: |                         # 2-4 sentence domain summary
    ...
  personas: [...]                        # REQUIRED — minimum 2 named personas

# --- all avatar types ---
activates:
  skills: [...]                          # REQUIRED — minimum 2 skill IDs; each must exist in agent-skills/
  workflows: [...]                       # REQUIRED — minimum 1 workflow ID

specializes_laws:                        # REQUIRED — minimum 1 non-negotiable law
  - id: ENG-x.x | PRD-x.x | BUS-x.x    # must exist in the appropriate laws/_domain.yaml
    title: "..."
    example_file: examples/...           # must reference an existing file
```

### `avatar.id` Format Rules

Two patterns are permitted. The **canonical form** is recommended for all new avatars.

| Pattern | Form | When to use |
|---------|------|-------------|
| **Canonical** (recommended) | `avatar-{type}-{domain-slug}` | All new avatars; required for product-type and industry avatars where slug-only form risks collision |
| **Legacy** (permitted, do not rename) | `avatar-{domain-slug}` | Existing technology avatars created before this rule was established |

**Examples:**

```
avatar-technology-cpp       ← canonical; type=technology, slug=cpp
avatar-product-loyalty      ← canonical; type=product, slug=loyalty
avatar-industry-aviation-faa ← canonical; type=industry, slug=aviation-faa
avatar-java-spring          ← legacy; permitted; do not rename
avatar-angular              ← legacy; permitted; do not rename
```

**Validation rule** — `avatar.id` is valid if ALL of the following are true:
1. Starts with `avatar-`
2. Contains the avatar's directory slug as a substring
3. Registered in `avatars/index.yaml`

> ⚠️ **Do not rename existing legacy-form avatars.** Renaming breaks `avatars/index.yaml`, `AVATAR-RAG-INDEX.yaml`, and all associated tests with no correctness gain. Grandfathering is intentional.

### Manifest Known Block Allowlist

The following are the **only** blocks permitted in `manifest.yaml`. Any block not on this list is an unknown block and triggers the manifest scope guard (Phase 2, Step 2.1):

```
avatar          stack (technology only)    domain (product only)
core_journeys   activates                  specializes_laws
conventions     commands                   project_structure
dependencies    compliance_domains         tags
```

> **Blocks that are NOT permitted in the manifest and where they belong:**
>
> | Forbidden Block | Where it belongs |
> |---|---|
> | `governance_overrides` | ENG-10.3 Exception Request (separate proposal) |
> | `anti_patterns` | `examples/` files or `guidance.md` |
> | `anti_patterns_by_tier` | `guidance.md` or separate example files |
> | `retrieval_triggers` | `AVATAR-RAG-INDEX.yaml` |
> | `brownfield_adoption` | `guidance.md` or dedicated workflow phase |
> | `skill_parity` | `guidance.md` conventions section |
> | `project_archetypes` | `guidance.md` or separate example files |
> | `compliance_rating` | Constitution law amendment (not an avatar artifact) |

---

## 4. Permitted Law Domain Matrix

Technology, product, and industry avatars each have strict law domain jurisdiction. Cross-domain law references are a 🔴 BLOCKING violation.

| Avatar Type | Primary Laws | Conditionally Permitted | FORBIDDEN |
|---|---|---|---|
| `technology` | `ENG-*` (all) | — | `PRD-*`, `BUS-*` |
| `product` | `PRD-*` (all), `BUS-*` (compliance obligations of the domain) | `ENG-6.x` only — security/privacy laws when the product has direct security obligations; requires inline justification | `ENG-1.x`–`ENG-5.x`, `ENG-7.x`–`ENG-12.x` |
| `industry` | `BUS-*` (all), `PRD-*` (applicable product laws for the vertical) | `ENG-6.x` only | `ENG-1.x`–`ENG-5.x`, `ENG-7.x`–`ENG-12.x` |

**Why `ENG-6.x` is conditionally permitted in product/industry avatars:** Laws like `ENG-6.7` (Audit Trail) and `ENG-6.1` (Security by Design) describe implementation requirements that a product or industry avatar must specify for its domain context. A product avatar is permitted to reference these when it is defining *how the product must implement security* — not defining the security laws themselves.

**The `BUS-7.1` ↔ `ENG-6.7` distinction for technology avatars:** If a tech avatar needs to show how audit logging is implemented in that stack, the correct law to cite is `ENG-6.7` (Audit Trail Law — Engineering). `BUS-7.1` (Audit Trail Law — Business) defines the *compliance obligation*, not the stack implementation. Technology avatars implement; they do not define compliance policy.

---

## 5. `guidance.md` Required Structure

`guidance.md` must follow this structure and stay within 450 tokens:

```markdown
# {Name} Guidance

> **Purpose:** {One sentence — what this avatar governs}

---

## Overview
{2–3 sentences maximum — domain or stack summary}

## Non-Negotiable Laws

### {LAW-ID} — {Law Title}
- **What this law requires in this {stack/domain}:** {one sentence}
- **What violates it:** {one sentence}
- **Implementation note:** {one sentence}

### {LAW-ID} — {Law Title}
...

## {Core Journeys (product) | Key Patterns (technology)}
{Journey table (product) or one-line pattern summary pointing to examples/ (technology)}

## Anti-Patterns to Avoid
{2–3 bullet points — the most common mistakes in this domain/stack}
```

> If the Non-Negotiable Laws section + Anti-Patterns exceeds 450 tokens, move the implementation notes to the corresponding `examples/` file. `guidance.md` is a **navigation document**, not a reference document.

---

## 6. `examples/` File Required Structure

Each example file follows this format (token budget: ≤850 tokens per file):

```markdown
---
avatar: avatar-{type}-{domain}
law: {LAW-ID}
title: "{Law Title}"
---

# {LAW-ID} — {Law Title}: {Domain/Stack} Application

## What This Law Requires
{1–2 sentences — the specific requirement in this context}

## Compliant Example
{Primary content — ~600 tokens of code or scenario}

## Violation Example
{What a violation looks like — ~150 tokens}

## Edge Cases & Warnings
{Optional — 2–3 bullets if the law has non-obvious edge cases in this context}
```

---

## 7. `use-cases/` Required Structure (Product-Type Only)

Each use-case directory contains one `README.md` (token budget: ≤1,500 tokens):

```markdown
# Use Case: {Name}

## Context
{Domain and persona — 2 sentences}

## Trigger
{What initiates this use case}

## Happy Path
{Step-by-step — numbered list, 5–8 steps}

## Failure Scenarios
{2–3 named failure states with expected behavior}

## Laws Applied
{Law IDs invoked in this use case with one-line description each}

## Success Metric
{Measurable outcome — one sentence}
```

---

## 8. RAG Validation — 5 Canonical Query Patterns

Before committing any avatar, define and simulate these 5 queries. Each query must be answerable from the avatar's files within the 3,500-token window.

### Technology Avatar Canonical Queries

| Query | Expected Files Loaded | Max Tokens |
|---|---|---|
| Q1: "How do I write a test for {stack}?" | `examples/ENG-4.1-*.md` | ≤850 |
| Q2: "What are the complexity limits for {stack}?" | `examples/ENG-3.1-*.md` | ≤850 |
| Q3: "What are the non-negotiable rules for {stack}?" | `guidance.md` | ≤450 |
| Q4: "What is the project structure for {stack}?" | `manifest.yaml` | ≤150 |
| Q5: "How do I handle {stack-specific concern}?" | `guidance.md` + relevant `examples/` | ≤1,300 |

### Product-Type Avatar Canonical Queries

| Query | Expected Files Loaded | Max Tokens |
|---|---|---|
| Q1: "How do we discover {domain} user needs?" | `examples/PRD-1.1-*.md` | ≤850 |
| Q2: "What is the {domain} core journey?" | `examples/PRD-2.1-*.md` | ≤850 |
| Q3: "What are the success metrics for {domain}?" | `examples/PRD-5.1-*.md` | ≤850 |
| Q4: "What are the non-negotiable rules for {domain}?" | `guidance.md` | ≤450 |
| Q5: "Walk me through a {domain} workflow" | `use-cases/{primary}/README.md` | ≤1,500 |

### RAG Validation Report Template

Commit to `hangar-ai-specs/evidence/avatar-rag-{domain}.md`:

```markdown
# RAG Validation Report — {Domain} Avatar
Date: {date}  |  Mode: {Generate | Assess | Validate | Enrich}  |  Version: {x.y.z}

| Query | Files Loaded | Tokens | Answered? | Notes |
|---|---|---|---|---|
| Q1 | ... | ... | ✅/❌ | |
| Q2 | ... | ... | ✅/❌ | |
| Q3 | ... | ... | ✅/❌ | |
| Q4 | ... | ... | ✅/❌ | |
| Q5 | ... | ... | ✅/❌ | |

Recall: {N}/5 ({%}) | Precision: {N}/5 ({%}) | Max query load: {N} tokens
Schema violations: {N} | Gate result: PASS ✅ / FAIL 🔴
```

**Gate thresholds (hard stops):**
- Recall < 5/5 (< 95%) → 🔴 FAIL — return to Phase 4
- Any query > 3,500 tokens → 🔴 FAIL — trim the offending document
- Any BLOCKING schema violation → 🔴 FAIL — return to Phase 4

---

## 9. Avatar Versioning Protocol

Applied at Phase 6 (Commit) by the avatar-workflow.

| Change Type | Semver Bump | Examples |
|---|---|---|
| Initial creation | `1.0.0` | New avatar from Generate mode |
| Add new law specialization, new use-case, new example file | `MINOR` (x.**Y**.0) | Adding ENG-7.1 example |
| Correct existing content, fix token budgets, fix broken references | `PATCH` (x.y.**Z**) | Typo fix, token trim, broken example_file reference |
| Remove law specializations, correct law boundary violations, restructure manifest schema | `MAJOR` (**X**.0.0) | Removing BUS-* from tech avatar, changing avatar type |
| Enrich with codebase (replaces generic with real patterns) | `MINOR` | Enrich mode always bumps MINOR — knowledge content changes |

### Deprecation Fields (in `avatars/index.yaml`)

```yaml
- id: avatar-technology-{domain}
  status: deprecated               # active | deprecated
  deprecated_since: "YYYY-MM-DD"
  replaced_by: "avatar-{successor}" # optional
  sunset_date: "YYYY-MM-DD"        # 6-month window from deprecated_since
```

Deprecated avatars are excluded from `AVATAR-RAG-INDEX.yaml` after `sunset_date` but remain in the repository for historical reference.

# Proposal: Enrich Product Avatars with Examples, Guidance, and RAG Pipeline

**Proposal ID:** enrich-product-avatars-rag-pipeline  
**Submitted:** February 18, 2026  
**Last Updated:** February 23, 2026  
**Status:** COMPLETE — All phases delivered

---

## Problem

Technology avatars (Java Spring, React, Python) have manifest files, guidance documents, code examples, and law citations that enable agents to cite ENG-* laws with precision. Product avatars (Cargo, Loyalty, Check-In) had none of this — only adoption stories. Agents couldn't cite PRD-* laws in product decisions, and the flat folder of 28 agent skills made domain-specific RAG indexing inefficient.

## Solution

Four changes to bring product avatars to parity with technology avatars and ensure pipeline integrity:

1. **Product Avatar Enrichment** — Add `manifest.yaml`, `guidance.md`, law-specific examples (PRD-1.1 through PRD-5.1), personas, and use-cases to each product avatar
2. **Agent Skills by Domain** — Organize 29 skills into 5 domain folders (`discovery-research`, `product-planning`, `development-practices`, `platform-engineering`, `ml-ai`) with domain-specific `index.yaml` files
3. **Consolidation** — Remove the legacy flat `skills/` folder (redundant with `skills-by-domain/`) and the `workflows/` folder (premature structure, not serving the pipeline). Update all references.
4. **RAG Pipeline Integrity Scan** — Verify zero broken references across the full pipeline: `laws/` → `avatars/` → `agent-skills/skills-by-domain/` → `docs/guides/` → READMEs

## What Was Delivered

### Phase 1: Infrastructure ✅

Skills organized into domain folders with indices:

```
agent-skills/skills-by-domain/
├── discovery-research/       (2 skills + index.yaml)
├── product-planning/         (3 skills + index.yaml)
├── development-practices/    (8 skills + index.yaml)
├── platform-engineering/     (7 skills + index.yaml)
└── ml-ai/                    (9 skills + index.yaml)
```

### Phase 2: Templates & Guides ✅

| Deliverable | Location |
|-------------|----------|
| Manifest template | `docs/templates/avatars/manifest-template.yaml` |
| Manifest schema | `docs/templates/avatars/manifest-schema.yaml` |
| Example template | `docs/templates/avatars/example-template.md` |
| Personas template | `docs/templates/avatars/personas-template.md` |
| Use-case template | `docs/templates/avatars/use-case-template.md` |
| Law citation guide | `docs/guides/avatars/law-citation-guide.md` |
| Product avatar guide | `docs/guides/avatars/product-avatar-guide.md` |
| PRD laws reference | `docs/guides/avatars/prd-laws-reference.md` |

### Phase 3: Avatar Implementation ✅

Three product avatars created with full structure:

**Cargo & Freight** (`avatars/product-type/cargo-freight/`):
- `manifest.yaml` — Law specializations, personas, skill activation
- `guidance.md` — Product-specific guidance with law citations
- `examples/` — PRD-1.1 through PRD-5.1 + personas.md
- `use-cases/` — booking-workflow, claims-processing, rate-optimization

**Loyalty / AADvantage** (`avatars/product-type/loyalty-aadvantage/`):
- `manifest.yaml`, `guidance.md`
- `examples/` — PRD-1.1 through PRD-5.1 + personas.md

**Check-In Travel** (`avatars/product-type/check-in-travel/`):
- `manifest.yaml`, `guidance.md`
- `examples/` — PRD-1.1 through PRD-5.1 + personas.md

Global RAG index created: `avatars/AVATAR-RAG-INDEX.yaml`

### Phase 4: Consolidation & RAG Pipeline Integrity ✅

**4a. Remove redundant folders:**
- [x] Delete `agent-skills/skills/` — redundant with `agent-skills/skills-by-domain/`
- [x] Delete `agent-skills/workflows/` — premature structure, not serving the pipeline
- [x] Delete `agent-skills/generate-domain-indices.py` — one-time generation script, no longer needed

**4b. Update all references (49 refs across 18 files):**
- [x] `AGENTS.md` — update structure diagram and skill registry path
- [x] `README.md` — update skill links table and remove workflow references
- [x] `agent-skills/README.md` — rewrite to reflect skills-by-domain as the only structure
- [x] `agent-skills/base/AGENT.md` — remove workflow references
- [x] `docs/guides/adoption/` — update skill paths in brownfield, greenfield, how-to-adopt guides
- [x] `docs/articles/` — update token optimization articles
- [x] `docs/slides/` — update presentation references
- [x] `docs/guides/observability/` — remove workflow references
- [x] Skills within `skills-by-domain/` — remove internal workflow cross-references

**4c. Full RAG pipeline broken reference scan:**
Scanned 525 links across all `.md` files. Fixed 204 broken references:
- [x] `avatars/` — fixed law file paths (`index.yaml` → `_domain.yaml`), path depths, cross-refs
- [x] `agent-skills/skills-by-domain/` — fixed cross-domain skill paths, avatar link depths
- [x] `docs/guides/` — fixed `constitution/base/` → `laws/`, `constitution/avatars/` → `avatars/`, path depths
- [x] `docs/templates/` — fixed law file names (`prd-1.md` → `discovery.md`), template depths
- [x] `docs/articles/` — fixed law file names, stale references
- [x] Root files — `AGENTS.md`, `README.md` skill domain assignments corrected
- [x] Created `claims-processing/README.md` stub (empty directory)
- [x] 61 remaining are false positives (code blocks, `{{ }}` templates, cross-repo slides, regex in code)

## Success Criteria

| Criteria | Target | Current |
|----------|--------|---------|
| Product avatars with manifest | 3 (Cargo, Loyalty, Check-In) | ✅ 3 |
| Example files per avatar | 5 | ✅ 5 (all three) |
| Skills organized by domain | 5 domains | ✅ 5 |
| Legacy `skills/` folder removed | Deleted | ✅ Deleted |
| `workflows/` folder removed | Deleted | ✅ Deleted |
| Broken internal links across RAG pipeline | 0 real | ✅ 0 real (61 false positives) |

## Open Questions

None — all resolved.

## References

- [Product Laws](../../../laws/product/)
- [Technology Avatars](../../../avatars/technology/) — reference for avatar structure
- [Agent Skills](../../../agent-skills/)
- [Avatar RAG Index](../../../avatars/AVATAR-RAG-INDEX.yaml)

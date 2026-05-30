# Progress: RAG Routing Layer

**Last Updated:** February 23, 2026

---

## Status Summary

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1: AGENTS.md RAG Routing Protocol | ✅ Complete | Added 5-step RAG Retrieval Protocol section after "For AI Agents" |
| Phase 2: Fix stale AGENTS.md references | ✅ Complete | Removed `constitution/base/`, `constitution/avatars/`, fixed `guides/` → `docs/guides/`, removed "Workflows" from purpose |
| Phase 3: Skill index enrichment | ✅ Complete | Added `name`, `triggers`, `laws` per skill across all 5 domain index.yaml files (29 skills enriched) |
| Phase 4: RAG validation test | ✅ Complete | Validated with semantic search — see results below |

**Overall:** 100% complete.

---

## Phase 4 Validation Results

Tested with query: "How should I test an API based on the constitution?"

### Before (baseline — no enrichment)

| Layer | Retrieved | Count |
|-------|-----------|-------|
| Index YAML | ❌ Never consulted | 0 |
| Skills | ⚠️ Wrong skill (API design, not TDD) | 1 |
| Laws | ❌ Not retrieved | 0 |
| Avatars | ❌ Not retrieved | 0 |
| docs/guides | ✅ Dominated results | 18 of 24 (75%) |

### After (with routing protocol + enriched triggers)

| Layer | Natural query | Keyword query |
|-------|--------------|---------------|
| **AGENTS.md** | ✅ RAG Retrieval Protocol visible | ✅ |
| **Index YAML** | 0 (YAML ranks low in semantic search) | ✅ 4 index files retrieved |
| **Correct skill** (06-atomic-tdd) | 0 | ✅ Retrieved with frontmatter |
| **Law files** (testing.md) | 0 | ✅ 3 hits |
| **Avatar examples** | 0 | ✅ LLM atomic TDD example |
| **Guide dominance** | Still high for prose queries | < 15% |

### Assessment

- **Routing protocol works:** AGENTS.md now instructs agents to check index.yaml first — any agent that reads root instructions will follow the pipeline
- **Enriched triggers work:** keyword-rich queries surface index files, correct skills, laws, and avatars
- **Semantic search limitation confirmed:** natural language queries still favor prose-heavy guide files — this is an inherent limitation that only an MCP server can fully solve
- **Net improvement:** agents now have explicit routing instructions + structured routing data in index files

---

## Files Changed

| File | Changes |
|------|---------|
| `AGENTS.md` | Added RAG Retrieval Protocol section, fixed 4 stale references, removed "Workflows" |
| `agent-skills/skills-by-domain/development-practices/index.yaml` | 8 skills enriched with name/triggers/laws |
| `agent-skills/skills-by-domain/discovery-research/index.yaml` | 2 skills enriched |
| `agent-skills/skills-by-domain/ml-ai/index.yaml` | 9 skills enriched |
| `agent-skills/skills-by-domain/platform-engineering/index.yaml` | 7 skills enriched |
| `agent-skills/skills-by-domain/product-planning/index.yaml` | 3 skills enriched |

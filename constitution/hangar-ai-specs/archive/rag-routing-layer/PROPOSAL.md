# Proposal: RAG Routing Layer — Force Pipeline Traversal for AI Agents

**Proposal ID:** rag-routing-layer  
**Submitted:** February 23, 2026  
**Status:** COMPLETE — All phases delivered

---

## Problem

The Multi-RAG architecture is designed as a 4-layer pipeline:

```
Index catalogs → Skills → Avatars → Laws
   (routing)     (procedure)  (context)  (authority)
```

But AI agents (GitHub Copilot, Claude, etc.) **don't follow this pipeline.** When given a prompt like "How should I test an API?", semantic search skips the routing layer entirely:

### What RAG Actually Retrieves

| Layer | Designed Role | What Gets Retrieved | Problem |
|-------|--------------|---------------------|---------|
| **Layer 1: Index catalogs** | Route intent → skill | ❌ Never consulted | No routing happens |
| **Layer 2: Avatars** | Stack-specific patterns | ❌ Zero examples retrieved | No code patterns |
| **Layer 3: Skills** | Executable procedure | ⚠️ Wrong skill (API design, not TDD) | Keyword match, not intent match |
| **Layer 4: Guides/Docs** | Supporting detail | ✅ 18 of 24 results | Verbose prose dominates |

### Root Cause

1. **No explicit retrieval instructions** — `AGENTS.md` says "read the laws" but doesn't prescribe the index-first retrieval pattern
2. **Skill Discovery Protocol is buried** — Section 6.3 of `agent-skills/base/AGENT.md` describes skill discovery, but it's never loaded into context because agents don't know to look there
3. **Index files have no semantic weight** — YAML index files rank low in semantic search because they're structured data, not prose
4. **Guides are prose-heavy** — `docs/guides/` files are long, keyword-rich documents that dominate semantic similarity scores
5. **`AGENTS.md` has stale references** — Still references `constitution/base/`, `constitution/avatars/`, `guides/` (wrong paths)

### Impact

- Agents burn **20-25K tokens** on guide prose instead of **12-15K** via the designed pipeline
- Law authority is bypassed — agents cite guides (Layer 4) instead of laws (Layer 1)
- Stack-specific patterns missing — no avatar code examples retrieved
- Inconsistent responses — different prompts hit different guide fragments

## Solution

Add an explicit **RAG Routing Protocol** to `AGENTS.md` that forces agents to follow the pipeline. Fix stale references. Make index files semantically discoverable.

### Phase 1: AGENTS.md RAG Routing Protocol

Add a new section to `AGENTS.md` that prescribes the exact retrieval sequence:

```markdown
## RAG Retrieval Protocol

When answering ANY question about how to build, test, design, or implement:

1. **Route via index** — Read `agent-skills/skills-by-domain/*/index.yaml` 
   to find the skill whose `keywords` or `laws` match the user's intent
2. **Load skill** — Read the matched skill `.md` file. The `laws.implements[]` 
   frontmatter tells you which laws apply (DO NOT load law files separately)
3. **Load avatar** — If the user's stack is known, read the matching 
   `avatars/technology/*/guidance.md` for stack-specific patterns
4. **Stop** — Do NOT read `docs/guides/` unless the user explicitly asks 
   for a guide or tutorial

NEVER skip step 1. NEVER go directly to docs/guides/.
```

### Phase 2: Fix Stale AGENTS.md References

Update the Key Directories table and structure diagram:
- `constitution/base/` → `laws/` (directory doesn't exist)
- `constitution/avatars/` → `avatars/` (directory doesn't exist)
- `guides/` → `docs/guides/` (wrong path)
- Remove "Workflows" from repository purpose description

### Phase 3: Skill Index Enrichment

Add `trigger_phrases` and `description` fields to each domain `index.yaml` so they're semantically discoverable:

```yaml
# Before (current)
skills:
  - file: 06-atomic-tdd.md

# After (enriched)  
skills:
  - file: 06-atomic-tdd.md
    name: Atomic TDD
    triggers: ["test", "testing", "TDD", "write tests", "test an API"]
    laws: [ENG-4.1, ENG-4.2, ENG-4.3]
```

### Phase 4: Validate with RAG Test

Re-run the same semantic search query ("How should I test an API?") and verify:
- [ ] At least one `index.yaml` file appears in results
- [ ] The correct skill (`06-atomic-tdd.md`) appears in top 5 results
- [ ] At least one avatar example appears
- [ ] Guide prose does NOT dominate (< 50% of results)

## Files Changed

| File | Change |
|------|--------|
| `AGENTS.md` | Add RAG Routing Protocol section, fix stale directory references |
| `agent-skills/skills-by-domain/*/index.yaml` (5 files) | Enrich with trigger phrases, skill names, law mappings per skill |
| `agent-skills/base/AGENT.md` | Add cross-reference to AGENTS.md RAG protocol |

## Success Criteria

| Criteria | Target |
|----------|--------|
| AGENTS.md has explicit retrieval protocol | Yes |
| AGENTS.md has zero stale directory references | Yes |
| All 5 domain index.yaml files enriched with triggers | Yes |
| Semantic search for "test API" returns skill in top 5 | Verified |
| Semantic search for "test API" returns avatar example | Verified |

## Open Questions

1. Should the RAG Routing Protocol also live in `agent-skills/base/AGENT.md` (which is the agent's "operating system") or only in root `AGENTS.md`?
2. Should we add a `.copilot/instructions.md` file (VS Code Copilot workspace instructions) that pre-loads the routing protocol?

## References

- [Token Optimization Article](../../docs/articles/token-optimization-multi-rag-architecture.md) — documents the designed architecture
- [AGENT.md Skill Discovery](../../agent-skills/base/AGENT.md) — Section 6.3, current discovery protocol
- [Previous Proposal](../enrich-product-avatars-rag-pipeline/PROPOSAL.md) — built the pipeline this proposal routes through

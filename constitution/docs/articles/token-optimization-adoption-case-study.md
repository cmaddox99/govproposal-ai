# Token Optimization Case Study: Constitution Adoption

> How efficient constitution reading reduces AI token consumption by 70%+

**Date:** 2026-02-04  
**Context:** Simplifying the hangar-ai-constitution adoption prompt  
**Related:** [adoption-bootstrap.md](../guides/prompts/adoption-bootstrap.md)

---

## Executive Summary

When an AI agent adopts the hangar-ai-constitution to a project, it doesn't need to read the entire ~500K token constitution. Through **index-first navigation** and **selective reading**, the agent can complete a full adoption while reading less than 30% of the total content.

This case study documents the techniques applied and metrics achieved.

---

## The Problem: Naive Constitution Reading

A naive approach would have the AI agent read the entire constitution before adopting:

```
Total Constitution Size: ~496,000 tokens
├── laws/                    ~50,000 tokens
├── avatars/                ~200,000 tokens  
├── agent-skills/           ~100,000 tokens
├── docs/guides/            ~120,000 tokens
└── other files              ~26,000 tokens
```

**Issues with naive reading:**
- Exceeds context window limits
- Wastes tokens on irrelevant content (e.g., React avatar for a Java project)
- Slow processing time
- Higher API costs

---

## The Solution: Optimized Reading Strategy

### Index-First Navigation

Instead of reading everything, the agent starts with index files:

```yaml
# laws/index.yaml (~500 tokens)
# avatars/index.yaml (~300 tokens)
# agent-skills/skills-by-domain/*/index.yaml (~200 tokens each)

Total navigation cost: ~1,500 tokens
```

From indexes, the agent discovers:
- Which law categories exist
- Which avatars are available
- Which skills and workflows are defined

### Selective Reading Based on Analysis

After analyzing the target codebase:

1. **Detect technology** from build files (pom.xml, package.json, etc.)
2. **Detect domain** from code patterns and entity names
3. **Read ONLY matching avatar** (e.g., `java-spring/` not `react-frontend/`)
4. **Read ONLY relevant laws** for brownfield adoption

---

## Metrics: Before and After

### Prompt Size Reduction

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Word Count | 1,410 | 199 | **86%** |
| Estimated Tokens | ~2,140 | ~389 | **82%** |
| Placeholders | 14 (4 unique) | 2 (1 unique) | **86%** |
| Manual Steps | 6 | 1 | **83%** |

### Constitution Reading Efficiency

For a **Java/Spring + Loyalty domain** adoption:

| Content | Tokens | Read? | Reason |
|---------|--------|-------|--------|
| Index files | ~1,000 | ✅ Yes | Navigation |
| brownfield-adoption.md | ~8,000 | ✅ Yes | Primary guide |
| java-spring avatar | ~15,000 | ✅ Yes | Matching tech |
| loyalty-aadvantage avatar | ~10,000 | ✅ Yes | Matching domain |
| aviation-faa adoption | ~5,000 | ✅ Yes | Required industry |
| Engineering laws (relevant) | ~10,000 | ✅ Yes | Core laws |
| Other avatars | ~175,000 | ❌ No | Not matching |
| Other guides | ~100,000 | ❌ No | Not needed |
| Other docs | ~172,000 | ❌ No | Not relevant |

**Reading Summary:**
- **Total Constitution:** ~496,000 tokens
- **Actually Read:** ~49,000 tokens
- **Efficiency:** Read only **9.9%** of constitution

---

## Token Optimization Techniques Applied

### 1. Agentic Delegation

**Before:** Embed detailed instructions in the prompt
```
### 1. ANALYZE the existing codebase:
   - Identify technology stack and versions from build files
   - Identify the business domain and core entities
   - Assess current test coverage
   - Identify code smells and architectural issues
   ... (500+ words of instructions)
```

**After:** Point to the guide, let agent read it
```
read the adoption guide at hangar-ai-constitution/docs/guides/adoption/brownfield-adoption.md
```

**Savings:** ~1,500 tokens (instructions now read on-demand, not embedded)

### 2. Reference vs Copy

**Before:** Copy avatar selection tables into prompt
```
**Technology Avatars:**
- `java-spring` - Java/Spring Boot
- `python-fastapi` - Python/FastAPI
- `dotnet-core` - .NET Core/C#
... (full list)
```

**After:** Agent discovers from index files
```
# Agent reads avatars/index.yaml and selects based on codebase analysis
```

**Savings:** ~500 tokens

### 3. Single Responsibility

**Before:** One prompt with 7 tasks
```
### 1. ANALYZE the existing codebase
### 2. DETERMINE relevant constitution components
### 3. CREATE the foundational structure
### 4. ADOPT the relevant avatars
### 5. WRITE characterization tests
### 6. CREATE an Hangar SDD change proposal
### 7. OUTPUT a compliance report
```

**After:** One clear directive
```
fully adopt the constitution to my project
```

**Savings:** ~800 tokens (task breakdown now in guide, not prompt)

### 4. Placeholder Minimization

**Before:** 4 unique placeholders requiring user input
```
<YOUR_PROJECTS_DIRECTORY>
<YOUR_PROJECT_NAME>
<YOUR_TECHNOLOGY>
<YOUR_PRODUCT_DOMAIN>
```

**After:** 1 placeholder
```
{{TARGET_REPO_PATH}}
```

**User Effort:** 4 replacements → 1 replacement
**Token Savings:** ~200 tokens (fewer placeholder references)

### 5. Implicit Context Discovery

**Before:** User must specify technology and domain
```
- `<YOUR_TECHNOLOGY>` → Your stack (e.g., `Java/Spring Boot`)
- `<YOUR_PRODUCT_DOMAIN>` → Your AA domain (e.g., `Loyalty`)
```

**After:** Agent discovers from codebase
```
# Agent reads pom.xml → detects Java/Spring
# Agent reads entity names → infers Loyalty domain
```

**Savings:** ~300 tokens (discovery is implicit, not explicit)

---

## Constitution Structure Recommendations

Based on this analysis, recommendations for constitution maintainers:

### 1. Maintain Index Files

Every major directory should have an `index.yaml` for navigation:
```
laws/index.yaml                          ✅ Exists
avatars/index.yaml                       ✅ Exists
agent-skills/skills-by-domain/*/index.yaml ✅ Exists (5 domain indices)
docs/guides/index.yaml                   ⚠️ Should add
```

### 2. Consistent File Naming

Use predictable names so agents can guess paths:
```
avatars/technology/{stack}/guidance.md     ✅ Predictable
avatars/technology/{stack}/manifest.yaml   ✅ Predictable
avatars/technology/{stack}/examples/       ✅ Predictable
```

### 3. Front-Load Key Information

Put the most important content at the top of files:
```markdown
# Avatar: Java Spring

> Java 17+ with Spring Boot 3.x applications

## Quick Reference (first 50 lines)
[Essential patterns here]

## Detailed Guidance (rest of file)
[Extended content here]
```

### 4. Cross-Reference with Relative Paths

Enable agents to navigate between related content:
```markdown
See also:
- [Testing patterns](../testing/java-patterns.md)
- [Security requirements](../../laws/engineering/security.md)
```

---

## Lessons Learned

### For Prompt Authors

1. **Trust the agent** - Don't over-specify; agents can discover context
2. **Reference, don't embed** - Point to docs instead of copying content
3. **One task, one prompt** - Complex prompts confuse; simple prompts work
4. **Minimize user input** - Every placeholder is friction

### For Constitution Authors

1. **Index everything** - Agents need navigation, not just content
2. **Be predictable** - Consistent naming enables smart guessing
3. **Front-load value** - Key info should be in first 50 lines
4. **Modular design** - Enable reading only what's needed

### For AI Agent Developers

1. **Start with indexes** - Read navigation files before content
2. **Analyze first** - Understand the project before reading docs
3. **Read selectively** - Only fetch content matching your analysis
4. **Track what you read** - Log files read for transparency

---

## Conclusion

The adoption prompt simplification achieved:

| Improvement | Result |
|-------------|--------|
| Prompt tokens | **82% reduction** |
| User placeholders | **75% reduction** |
| Manual steps | **83% reduction** |
| Constitution reading | **~90% reduction** (only 10% needed) |

**Key insight:** A well-structured constitution with good indexes enables AI agents to be efficient readers. The constitution author invests in organization; the agent rewards this with focused, efficient adoption.

---

## Related Resources

- [Adoption Bootstrap Prompt](../guides/prompts/adoption-bootstrap.md)
- [Brownfield Adoption Guide](../guides/adoption/brownfield-adoption.md)
- [Token Optimization Multi-RAG Architecture](./token-optimization-multi-rag-architecture.md)

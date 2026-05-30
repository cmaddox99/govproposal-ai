# Token Optimization Analysis: hangar-ai-constitution Multi-RAG Architecture

**Author:** AA Engineering Team  
**Date:** February 2026  
**Audience:** Engineers, Architects, AI/ML Teams

---

## Executive Summary

The hangar-ai-constitution implements a **Multi-RAG (Retrieval-Augmented Generation) Architecture** that reduces AI context window usage by **97-98%** while maintaining full constitutional compliance. This document explains how the architecture works and why it matters for AI-assisted development at scale.

---

## The Problem: Context Window Limits

Modern AI assistants have context window limits:
- GPT-4: ~128K tokens
- Claude: ~200K tokens
- GitHub Copilot: Varies by model

A naive approach of loading the entire constitution into context is **impossible**:

| Component | Tokens |
|-----------|--------|
| Full hangar-ai-constitution | **~549,250 tokens** |
| Typical AI context limit | ~128,000 tokens |
| **Overflow** | **421,250 tokens (4.3x over limit)** |

---

## The Solution: Multi-RAG Architecture

Instead of loading everything, we use **indexed catalogs** that enable selective retrieval:

```
┌──────────────────────────────────────────────────────────────┐
│ LEVEL 1: CATALOG LOOKUP (~6K tokens always loaded)          │
│ ┌──────────────┬──────────────────────────┬────────────┐     │
│ │ laws/        │ skills-by-domain/        │ avatars/   │     │
│ │ index.yaml   │ */index.yaml (5 domains) │ index.yaml │     │
│ │ (90 lines)   │ (~240 lines total)       │ (375 lines)│     │
│ └──────────────┴──────────────────────────┴────────────┘     │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ Intent matching
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ LEVEL 2: SELECTIVE SKILL RETRIEVAL (~4-8K tokens per skill) │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 13-observability.md                                     │ │
│ │ ├─ frontmatter: laws.implements, triggers, followed_by  │ │
│ │ ├─ method: Three Pillars (Logs, Metrics, Traces)       │ │
│ │ ├─ templates: Structured logging, Prometheus metrics   │ │
│ │ └─ checklist: Quality verification                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ Stack detection
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ LEVEL 3: AVATAR SPECIALIZATION (~2-5K tokens per avatar)    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ java-spring/ADOPTION.md                                 │ │
│ │ ├─ stack: JUnit 5, Mockito, Micrometer                 │ │
│ │ ├─ patterns: @Observed, @Timed annotations             │ │
│ │ └─ examples: Spring Boot Actuator config               │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ aviation-faa/ADOPTION.md                               │ │
│ │ ├─ compliance: FAA Part 121, DO-178C                   │ │
│ │ └─ requirements: Audit trail MANDATORY                  │ │
│ └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Repository Size Metrics

| Component | Lines | Characters | Est. Tokens* |
|-----------|-------|------------|--------------|
| **Full Repository** | 73,057 | 2,197,003 | **~549,250** |
| Base Constitutions (3) | 3,133 | 100,502 | ~25,125 |
| All Skills (28) | 18,414 | ~550,000 | ~137,500 |
| All Workflows (7) | 2,827 | ~85,000 | ~21,250 |
| All Avatars (17) | 5,692 | ~170,000 | ~42,500 |
| **Index Files Only (4)** | 886 | 25,018 | **~6,255** |

*Token estimate: ~4 characters per token

---

## Real-World Scenario: Adding Observability

### Without Multi-RAG (Naive Approach)

```
Load: Full Repository → 549,250 tokens ❌ IMPOSSIBLE
```

### With Multi-RAG (Selective Retrieval)

| Step | What's Retrieved | Tokens | Cumulative |
|------|------------------|--------|------------|
| 1. User prompt | "Add monitoring to cargo-api" | ~20 | 20 |
| 2. Index lookup | `skills-by-domain/*/index.yaml` (find relevant skill) | ~1,000 | 1,020 |
| 3. Skill retrieval | `13-observability.md` | ~4,400 | 5,420 |
| 4. Avatar lookup | `avatars/index.yaml` (find java-spring) | ~1,500 | 6,920 |
| 5. Avatar retrieval | `java-spring/ADOPTION.md` | ~4,820 | 11,740 |
| 6. Industry avatar | `aviation-faa/ADOPTION.md` (audit requirements) | ~950 | 12,690 |
| **Total Context** | | | **~12,700** |

### Token Savings

```
549,250 - 12,700 = 536,550 tokens saved (97.7% reduction)
```

---

## How Abstraction Works for Engineers

Engineers don't need to know about laws, indexes, or RAG. They just ask their question:

```
┌─────────────────────────────────────────────────────────────────────┐
│ ENGINEER'S VIEW (Simple)                                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Prompt: "Add monitoring and alerting to the cargo API service"    │
│                                                                     │
│  AI Response: [Structured logging, metrics, traces - per skill]    │
│               [Java/Spring patterns - per avatar]                   │
│               [Audit trail for FAA compliance - per industry]       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### What Happens Behind the Scenes

```
┌───────────────────────────────────────────────────────────────────────┐
│ WHAT THE AI AGENT DOES (Hidden from Engineer)                         │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1. Parse intent → "monitoring" → skill-13-observability             │
│                                                                       │
│  2. Load skills-by-domain/*/index.yaml (~1K tokens)                │
│     └─ Find: skill-13-observability                                  │
│     └─ See: primary_laws: [ENG-5.5, ENG-6.7, BUS-7.1]               │
│                                                                       │
│  3. Load 13-observability.md (~4.4K tokens)                          │
│     └─ Has: triggers, followed_by, full implementation guide         │
│     └─ Laws EMBEDDED in skill, not separately loaded                 │
│                                                                       │
│  4. Detect project context → Java/Spring                             │
│     └─ Load avatars/index.yaml → find avatar-java-spring            │
│     └─ Load java-spring/ADOPTION.md (~4.8K tokens)                   │
│                                                                       │
│  5. Apply industry → Aviation                                        │
│     └─ Load aviation-faa/ADOPTION.md (~950 tokens)                  │
│     └─ See: BUS-7.1 audit trail is NON-NEGOTIABLE                   │
│                                                                       │
│  6. Generate response with context-aware patterns                    │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Index Files Enable Smart Retrieval

The key to this architecture is **YAML index files** that act as lookup tables:

### skills-by-domain/*/index.yaml

```yaml
- id: skill-13-observability
  file: 13-observability.md
  name: Observability
  category: operations
  primary_laws: [ENG-5.5, ENG-6.7, BUS-7.1]  # Laws embedded here
```

### avatars/index.yaml

```yaml
- id: avatar-java-spring
  name: Java/Spring Boot
  path: technology/java-spring/
  activates:
    skills: [skill-06-atomic-tdd, skill-07-vertical-slice-dev]
  specializes_laws: [ENG-4.1, ENG-3.1, ENG-2.1]
```

### What Engineers DON'T Need to Do

| ❌ Don't Need To | ✅ AI Does Automatically |
|------------------|--------------------------|
| Say "use ENG-6.7 audit trail law" | Matches intent to skills via trigger phrases |
| Say "apply the java-spring avatar" | Detects tech stack and applies avatar |
| Say "check aviation compliance" | Applies industry compliance (aviation-faa) |
| Know which skills map to which laws | Pulls laws through skill frontmatter |

---

## Comparison: Traditional vs Multi-RAG

| Aspect | Traditional (Monolithic) | Multi-RAG (Indexed) |
|--------|--------------------------|---------------------|
| **Initial context** | Full constitution (~549K tokens) | Index files only (~6K tokens) |
| **Per-task context** | Same (~549K) | Skill + avatars (~12-15K) |
| **Context window fit** | ❌ Exceeds most models | ✅ Fits easily |
| **Relevance** | Low (90% irrelevant) | High (95% relevant) |
| **Law invocation** | Engineer must cite | Implicit via skills |
| **Tech patterns** | Generic | Stack-specific via avatars |
| **Industry compliance** | Manual checking | Automatic via industry avatar |

---

## Example Scenarios

### Scenario 1: Monitoring Engineer

```
Prompt: "Add logging and metrics to the shipment tracking service"

AI receives via RAG:
├─ skills-by-domain/*/index.yaml → maps to skill-13-observability
├─ 13-observability.md → full observability patterns
├─ java-spring/ADOPTION.md → Micrometer, Actuator patterns
└─ aviation-faa/ADOPTION.md → audit trail requirements

Engineer sees: Java code with structured logging, Prometheus metrics,
              correlation IDs, and FAA-compliant audit events

Laws applied automatically:
- ENG-5.5 (Observability) via skill
- ENG-6.7 (Audit Trail) via skill
- BUS-7.1 (Audit Trail) via industry avatar
```

### Scenario 2: Cargo Developer

```
Prompt: "Build an API for dangerous goods validation"

AI receives via RAG:
├─ skills-by-domain/discovery-research/index.yaml → find business-rules skill
├─ 05-business-rules.md → rules encoding
├─ 12-api-design.md → API patterns
├─ java-spring/ADOPTION.md → Spring patterns
└─ cargo-freight/ADOPTION.md → cargo domain rules

Engineer sees: Spring Boot controller with dangerous goods validation,
              TSA compliance checks, proper test coverage

Laws applied automatically:
- BUS-2.2 (TSA Security) via domain avatar
- BUS-6.4 (Dangerous Goods) via domain avatar
- ENG-4.1 (TDD) via skill
```

### Scenario 3: New Feature Development

```
Prompt: "Create a new endpoint for miles redemption"

AI receives via RAG:
├─ skills-by-domain/development-practices/index.yaml → find atomic-tdd, api-design
├─ 06-atomic-tdd.md → TDD cycle
├─ 12-api-design.md → API patterns
├─ java-spring/ADOPTION.md → Spring patterns
└─ loyalty-aadvantage/ADOPTION.md → miles/redemption rules

Engineer sees: Test-first implementation with proper miles deduction,
              balance validation, and audit logging

Laws applied automatically:
- ENG-4.1 (Atomic TDD) via skill
- BUS-7.1 (Audit Trail) via domain avatar
```

---

## Key Metrics Summary

| Metric | Value |
|--------|-------|
| **Full repo tokens** | ~549,250 |
| **Index files tokens** | ~6,255 |
| **Typical task context** | ~12-15K tokens |
| **Token reduction** | **97-98%** |
| **Skills indexed** | 29 |
| **Avatars indexed** | 17 |
| **Laws auto-mapped** | ~50 unique laws across skills |

---

## Why This Architecture Works

### 1. Index Files Are Small
- 886 lines total across all 4 index files
- Always loadable as "base context"
- Enables intent-to-skill matching

### 2. Skills Embed Law References
- Frontmatter contains `laws.implements[]` and `laws.references[]`
- No need to load law files separately
- Laws are "cited" automatically when skill is invoked

### 3. Avatars Specify Stack Patterns
- `specializes_laws[]` in avatar index
- Technology-specific testing frameworks
- Framework-specific code patterns

### 4. Domain Indices Organize Skills
- Domain `index.yaml` files group related skills
- Skills contain `laws.implements[]` references
- Lookup by domain narrows the search space

### 5. Industry Avatars Enforce Compliance
- Aviation always loaded for AA projects
- FAA/TSA/DOT requirements automatic
- Audit trail requirements enforced

---

## Implementation Checklist

To enable Multi-RAG architecture in your constitution:

- [x] Create `laws/index.yaml` with domain registry
- [x] Create `agent-skills/skills-by-domain/*/index.yaml` with law mappings
- [ ] Create `avatars/index.yaml` with technology/industry/product catalogs
- [ ] Add YAML frontmatter to all skill files with `laws.implements[]`
- [ ] Add `activates.skills[]` and `specializes_laws[]` to avatars
- [ ] Configure AI tools to load index files as base context

---

## Conclusion

The Multi-RAG architecture transforms the hangar-ai-constitution from an impossible-to-load monolith into an efficient, contextual retrieval system. Engineers get:

- **Full constitutional compliance** without knowing law numbers
- **Stack-specific patterns** without specifying technology
- **Domain-aware guidance** without manual avatar selection
- **97-98% token reduction** enabling AI assistance at scale

The key insight: **Index files act as a routing layer** that maps engineer intent to the minimal set of constitution components needed for any given task.

---

## References

- [hangar-ai-constitution Repository](https://github.com/AAInternal/hangar-ai-constitution)
- [Skills by Domain](../../agent-skills/skills-by-domain/)
- [Avatars Index](../../avatars/index.yaml)
- [Laws Index](../../laws/index.yaml)

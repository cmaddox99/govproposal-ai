# Split-Reference Architecture Guide

> **Purpose:** Explains how the C++ avatar's split-reference architecture works — why `full-reference.md` was decomposed into topic-aligned files and how the pseudo-RAG retrieval chain operates.
>
> **Audience:** Avatar maintainers, constitution contributors, AI agents
>
> **Laws:** [ENG-10.1](../../laws/engineering/eng-10-constitution.md) (Constitution Compliance), [ENG-11.1](../../laws/engineering/eng-11-hangar-sdd.md) (Hangar SDD)

---

## The Problem

Technology avatars face two competing constraints:

1. **`guidance.md` must be small** (≤450 tokens) — it is loaded on every RAG query and must fit within the 3,500-token per-query window alongside example files.
2. **Engineering reference content is large** — a mature avatar like C++ requires 40,000+ tokens of governance content covering language patterns, migration playbooks, safety-critical compliance, and brownfield modernization.

The original solution was a **two-file architecture**: a slim `guidance.md` pointing to a monolithic `full-reference.md`. But when an agent followed the link, it loaded the entire 45,000+ token file — 13× the RAG query window. Most of that content was irrelevant to the user's question.

---

## The Solution: Three-Tier Retrieval

The split-reference architecture introduces an intermediate **reference index** that acts as a semantic router, directing the agent to the right topic file:

```
┌─────────────────────────────────────────────────────────┐
│                    RAG Query Flow                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  User: "How do I handle thread safety in C++?"          │
│                                                         │
│  Tier 1 ─ guidance.md (≤450t, always loaded)            │
│           Contains: law table + single index link       │
│           ↓                                             │
│  Tier 2 ─ reference-index.md (≤500t, on-demand)        │
│           Contains: categorized topic list + links      │
│           Agent reads categories → picks "Concurrency"  │
│           ↓                                             │
│  Tier 3 ─ ref-concurrency.md (≤3,500t, on-demand)      │
│           Contains: Concurrency, Coroutines,            │
│           Exception Safety, Resiliency Patterns         │
│           Agent finds the answer here                   │
│                                                         │
│  Total loaded: ~405t + ~400t + ~3,257t = ~4,062t        │
│  vs. monolith: ~405t + ~45,484t = ~45,889t              │
│  Savings: 91% reduction in loaded context               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Why "Pseudo-RAG"?

A true RAG system uses vector embeddings and semantic search to find relevant documents. This architecture achieves a similar result using **structured navigation**:

- The **reference index** contains topic descriptions that the agent can match against the user's query using natural language understanding
- Each **reference file** is sized to fit within a single RAG query window (≤3,500 tokens)
- The agent follows links rather than performing embedding search, but the outcome is the same: only relevant content is loaded

This creates a **last-resort retrieval layer** between the slim guidance document and general LLM knowledge. The agent exhausts constitutional authority before falling back to its training data.

---

## File Structure

```
avatars/technology/cpp/
├── manifest.yaml                           ← Machine-readable config (≤150t or exception)
├── guidance.md                             ← Always-loaded RAG anchor (≤450t)
├── reference-index.md                      ← Topic router / pseudo-RAG index (≤1,500t)
│
├── refs/language/                          ← Core language patterns (9 files)
│   ├── ref-getting-started.md              ← Glossary, Quick-Start, Version Policy (~2370t)
│   ├── ref-core-type-safety.md             ← Const, Casts, Null Safety (~2764t)
│   ├── ref-core-modern-idioms.md           ← Designated initializers, variant, any, optional (~2153t) ★ C++17+
│   ├── ref-domain-patterns.md              ← DDD, DI, Ownership Patterns (~3008t)
│   ├── ref-domain-quality.md               ← SRP Refactoring, Anti-Patterns (~1834t)
│   ├── ref-object-design-rehabilitation.md ← Object Rehabilitation Anti-Patterns 1–5 (~2984t)
│   ├── ref-object-design-patterns.md       ← Move Semantics, Design Patterns (~2267t)
│   ├── ref-templates-metaprogramming.md    ← Templates, ADL, Lambdas, Forwarding (~3336t)
│   └── ref-advanced-patterns.md            ← Preprocessor, Allocators, ABI (~1871t)
│
├── refs/safety/                            ← Safety, concurrency & runtime (6 files)
│   ├── ref-safety-misra-do178.md           ← MISRA C++, DO-178C, JSF AV Rules (~2443t)
│   ├── ref-safety-memory-lifetime.md       ← Advanced Memory Lifetime, FFI (~1931t)
│   ├── ref-safety-jni-abi.md               ← JNI Safety, ABI Stability (~1083t)
│   ├── ref-safety-far117-cwr.md            ← FAR 117 Compliance, CWR Anti-Pattern Catalog (~3234t)
│   ├── ref-concurrency-threading.md        ← Threads, Coroutines, Exception Safety (~2891t) ★ C++11+
│   └── ref-concurrency-async.md            ← Resiliency Patterns, Circuit Breakers (~2462t) ★ C++17+
│
├── refs/testing/                           ← Testing, build & toolchain (6 files)
│   ├── ref-testing-ci-policy.md            ← CI Toolchain Policy, clang-tidy Gates (~2778t)
│   ├── ref-testing-gtest-core.md           ← TEST/TEST_F/EXPECT/ASSERT, Exception Testing (~2883t)
│   ├── ref-testing-gtest-advanced.md       ← Template Tests, Fixtures, Concurrency Testing (~1494t)
│   ├── ref-build-packages.md               ← CMake, vcpkg, C++20 Modules (~1492t) ★ C++20+
│   ├── ref-build-ubsan-msvc.md             ← UBSan/MSVC Toolchain Gap, Sanitizer Alternatives (~3327t)
│   └── ref-infrastructure.md               ← Logging, Config, Health, Tools (~3101t)
│
├── refs/legacy/                            ← Brownfield, migration & legacy (10 files)
│   ├── ref-brownfield-adoption.md          ← Per-Tier clang-tidy, Testing, ABI (~3291t)
│   ├── ref-brownfield-project-config.md    ← Compiler Flags, Sanitizers, IOC_ALP, MFC (~2999t)
│   ├── ref-migration-pre-cpp17.md          ← C++98→11→14→17 Step-by-Step, Dual-Toolchain (~3302t) ★ C++98-C++17
│   ├── ref-migration-cpp17-plus.md         ← C++17→20 Survival Patterns, ActiveTest→GoogleTest (~2305t) ★ C++17+
│   ├── ref-legacy-navigation.md            ← Codebase Navigation, Survival Patterns (~1749t)
│   ├── ref-legacy-triage-playbook.md       ← Triage Playbook, ActiveTest Migration Strategies (~2576t)
│   ├── ref-mental-models-memory.md         ← Value Semantics, RAII, UB — Gaps 1–6 (~2316t)
│   ├── ref-mental-models-lang.md           ← Linking, Templates, ODR, Runtime — Gaps 7–13 (~2492t)
│   ├── ref-legacy-smells-structural.md     ← Smell Catalog Smells 1–7, Summary Table (~2470t)
│   └── ref-legacy-smells-patterns.md       ← Smell Catalog Smells 8–14, Remediation Patterns (~2416t)
│
└── examples/                               ← Law-specific example files (≤850t each)
```

> **★ = version-annotated**: content is specific to one C++ standard tier. Route to these files only when the project's `__cplusplus` value matches the annotation.

---

## Token Budget Design

| Tier | File | Budget | Loaded When |
|------|------|--------|-------------|
| 1 | `guidance.md` | ≤450t | Every query (always loaded) |
| 2 | `reference-index.md` | ≤1,500t | Agent needs deeper detail than guidance provides |
| 3 | `ref-*.md` (each) | ≤3,500t | Agent identifies the relevant topic from the index |
| — | `examples/*.md` (each) | ≤850t | RAG matches a specific law query |

**Per-query budget math (C++ split-reference corpus, 31 files, 73,696t total):**
- Tier 1 alone: ~310t (9% of 3,500t window)
- Tier 1 + Tier 2: ~1,210t (35% of 3,500t window)
- Tier 1 + Tier 2 + one Tier 3 file: ~4,510t (agent loads one ref file; prioritize by relevance)
- Tier 1 + one example: ~1,160t (33% of 3,500t window — the common case)
- Worst-case Tier 3 file: ref-templates-metaprogramming.md (~3,336t) — still ≤3,500t target

The architecture optimizes for the **common case** (guidance + example = ~1,160t) while providing a **deep-dive path** (guidance + index + one ref file ≤ ~4,510t) when needed. Before this split, the monolithic reference files averaged ~4,300t each — 23% over the per-query window.

---

## Law Domain Alignment

Each reference file is aligned to engineering law domains, making routing predictable:

| Reference File | Primary Laws | Query Signal |
|---------------|-------------|-------------|
| `ref-core-type-safety.md` | ENG-3.x (Code Quality) | "const", "type safety", "casts", "null" |
| `ref-core-modern-idioms.md` | ENG-3.x (Code Quality) | "designated initializer", "variant", "optional" |
| `ref-domain-patterns.md` | ENG-2.x (Architecture) | "DDD", "aggregate", "dependency injection" |
| `ref-domain-quality.md` | ENG-2.x (Architecture) | "SRP", "anti-pattern", "refactor" |
| `ref-testing-ci-policy.md` | ENG-4.x (Testing) | "CI", "pipeline", "clang-tidy", "quality gate" |
| `ref-testing-gtest-core.md` | ENG-4.x (Testing) | "test", "TEST_F", "EXPECT", "ASSERT" |
| `ref-testing-gtest-advanced.md` | ENG-4.x (Testing) | "fixture", "template test", "concurrency test" |
| `ref-build-packages.md` | ENG-5.x (DevOps) | "build", "cmake", "vcpkg", "modules" |
| `ref-build-ubsan-msvc.md` | ENG-5.x (DevOps) | "sanitizer", "UBSan", "MSVC", "toolchain gap" |
| `ref-safety-misra-do178.md` | ENG-6.x (Security) | "MISRA", "DO-178C", "safety-critical" |
| `ref-safety-memory-lifetime.md` | ENG-6.x (Security) | "memory lifetime", "FFI", "C interop" |
| `ref-concurrency-threading.md` | ENG-7.x (Reliability) | "thread", "coroutine", "exception safety" |
| `ref-concurrency-async.md` | ENG-7.x (Reliability) | "async", "resilience", "circuit breaker" |
| `ref-brownfield-*.md` | ENG-3.x, ENG-5.x | "brownfield", "migrate", "legacy", "modernize" |
| `ref-migration-*.md` | ENG-3.x, ENG-5.x | "C++11", "C++17", "upgrade", "dual-toolchain" |

When an agent sees a query about "thread safety", it can match `ENG-7.x → ref-concurrency-threading.md` without reading the index — the law domain acts as a secondary routing signal.

---

## How to Add Content

When adding new governance content to a technology avatar that uses this architecture:

1. **Identify the topic cluster** — which `ref-*.md` file does it belong in?
2. **Check the token budget** — will the target file still be ≤3,500t after your addition?
3. **If it fits:** Add the section to the appropriate `ref-*.md` file
4. **If it doesn't fit:** Split the target file along a natural boundary, creating a new `ref-*.md` file
5. **Update `reference-index.md`** — add or update the entry for the new/modified file
6. **Never add content to `guidance.md`** — it is a navigation document, not a reference document

### Creating a New Reference File

```markdown
# C++ Avatar Reference: {Topic Title}

---

## {Section Title}

{Content with law references per ENG-10.1}

---

## See Also

- [{Related File Title}]({related-file}.md)
```

---

## Applying to Other Avatars

This architecture is not C++-specific. Any technology avatar whose reference content exceeds the guidance.md token budget can adopt it:

1. **Create `reference-index.md`** — categorized topic list with links
2. **Split reference content** into topic-aligned files (≤3,500t each)
3. **Update `guidance.md`** — replace inline content with a single link to the index
4. **Align files to law domains** — makes routing predictable for agents

The key principle: **guidance.md is a navigation document, reference files are retrieval targets, and the index is the router between them.**

---

## Related Resources

- [Avatar Model Schema](../avatar-model-schema.md) — token budgets and file structure requirements
- [Proposal: cpp-split-reference-architecture](../../../hangar-ai-specs/changes/cpp-split-reference-architecture/PROPOSAL.md) — the formal proposal that introduced this pattern

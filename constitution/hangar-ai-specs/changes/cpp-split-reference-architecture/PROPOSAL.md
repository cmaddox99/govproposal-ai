# Proposal: Split-Reference (Pseudo-RAG) Architecture for C++ Avatar

**Proposal ID:** cpp-split-reference-architecture
**Submitted:** April 14, 2026
**Status:** 🔵 IN PROGRESS
**Parent PR:** #14 (c-plus-plus-avatar-enrichment)
**Source:** Critique §1.1 analysis in `hangar-ai-specs/evidence/avatar-scan-cpp.md`
**Related:** `cpp-manifest-token-exception` (separate PR), `cpp-manifest-150t-compliance` (contingency)

---

## Laws Cited (ENG-11.2 Compliance)

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law | Governs proposal lifecycle |
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | RAG retrieval precision is a compliance metric |
| [ENG-4.1](laws/engineering/eng-4-testing.md) | Atomic TDD Law | All code changes follow RED–GREEN–REFACTOR |
| [ENG-6.7](laws/engineering/eng-6-security.md) | Audit Trail Law | Content routing must be traceable |

---

## Problem Statement

The C++ avatar's `full-reference.md` is a **45,484-token monolith** containing 67 sections across 5,628 lines. When an agent follows the link from `guidance.md`, it loads the entire file — **13× the 3,500t per-query RAG window**. Most of that content is irrelevant to any given query.

This creates a precision problem: a query about "thread safety in C++" loads 45,484 tokens when only the Concurrency section (~3,226t) is relevant. The agent must search through memory management, brownfield migration playbooks, license compliance, and 60+ other sections to find the answer.

### Current Architecture (Two-Hop)

```
User query
    → guidance.md (~405t, always loaded)
        → full-reference.md (45,484t — entire file loaded on-demand)
```

### Impact

- **Wasted context window:** 92% of loaded content is irrelevant to any given query
- **Reduced precision:** Agent must disambiguate across 67 sections
- **No topic isolation:** Cannot load "just security" or "just concurrency"
- **Last-resort gap:** Between guidance.md (405t summary) and general LLM knowledge, there is no intermediate retrieval layer with constitutional authority

---

## Solution: Three-Tier Split-Reference Architecture

Split `full-reference.md` into **topic-aligned reference files** with a **reference index** acting as a semantic router. This creates a pseudo-RAG pipeline — a structured retrieval chain that is the last constitutionally-authoritative layer before the agent falls back to general LLM knowledge.

### Architecture

```
guidance.md (~405t, always loaded)
    → reference-index.md (~300t, loaded on-demand)
        → ref-core-patterns.md        (ENG-2.x, ENG-3.x)
        → ref-testing-quality.md       (ENG-4.x)
        → ref-security-safety.md       (ENG-6.x)
        → ref-concurrency.md           (ENG-7.x)
        → ref-build-toolchain.md       (ENG-5.x)
        → ref-memory-lifetime.md       (ENG-3.x)
        → ref-brownfield-migration.md  (ENG-3.x, ENG-5.x)
        → ref-brownfield-playbooks.md  (ENG-3.x)
        → ref-legacy-navigation.md     (ENG-3.x)
        → ref-operational.md           (operational)
```

### How It Works

1. **User query** → RAG loads `guidance.md` (~405t, always loaded)
2. **`guidance.md`** contains one link: `→ [Reference Index](reference-index.md)`
3. **Agent loads `reference-index.md`** (~300t) — a categorized topic router with descriptions and anchor links
4. **Agent selects the right cluster** based on query semantics (e.g., "thread safety" → `ref-concurrency.md`)
5. **Agent loads ONE reference file** (≤3,500t) — fits within the RAG query window

### Topic File Breakdown

| Reference File | Law Domain | Sections | Est. Tokens | Fits 3,500t? |
|---------------|------------|----------|-------------|:------------:|
| `ref-core-patterns.md` | ENG-2.x, ENG-3.x | Domain Modeling, DI, Safety, Naming, Const, Casts, Nulls, SRP, Object Design, Implicit Conversions, Type-Safe Unions, Designated Initializers | 13 | ~3,200t | ⚠️ tight |
| `ref-testing-quality.md` | ENG-4.x | Testing Framework, Test Isolation, CI Quality Toolchain, Toolchain Gap | 4 | ~2,800t | ✅ |
| `ref-security-safety.md` | ENG-6.x | Safety-Critical C++ (MISRA/DO-178C/JSF AV) | 1 | ~1,600t | ✅ |
| `ref-concurrency.md` | ENG-7.x | Concurrency, Coroutines, Resiliency, Exception Safety, Termination | 5 | ~3,200t | ✅ |
| `ref-build-toolchain.md` | ENG-5.x | Packages, Builds, Modules, ABI, Allocators, Templates, Lambdas, ADL, Logging, Config, Health, Preprocessor, License | 14 | ~3,000t | ✅ |
| `ref-memory-lifetime.md` | ENG-3.x | Advanced Memory/Object Lifetime, C/C++ Interop, FFI | 2 | ~1,200t | ✅ |
| `ref-brownfield-migration.md` | ENG-3.x, ENG-5.x | Brownfield Migration, Per-Tier configs (clang-tidy, testing, code review), Cross-Standard ABI, Feature-Detection, Compiler Flags, Sanitizer Availability | 8 | ~3,400t | ⚠️ tight |
| `ref-brownfield-playbooks.md` | ENG-3.x | Migration Playbooks (98→11, 11→14, 14→17, 17→20), Dual-Toolchain, Dep Mismatch, Writing New Code for Legacy | 7 | ~3,400t | ⚠️ tight |
| `ref-legacy-navigation.md` | ENG-3.x | Legacy Navigation, Mental Models, Code Smells, Triage, Survival Patterns, Priority Matrix | 6 | ~3,400t | ⚠️ tight |
| `ref-operational.md` | — | Tools & Commands, Anti-Patterns, Skill Parity, Project Archetypes, Authorities | 5 | ~1,500t | ✅ |

> **Design constraint:** Each file targets ≤3,500t. Files marked ⚠️ will be measured during extraction and split further if they exceed the budget.

### Preamble Routing

The preamble sections (Overview, Table of Contents, Glossary, Quick-Start Guide — ~1,869t) will be incorporated into `reference-index.md` as a compact summary with the Quick-Start Guide as an inline section and the Glossary as a dedicated `ref-getting-started.md` if it exceeds the index budget.

### `guidance.md` Changes

Replace the current 4-entry quick-links table (~40t) with a single link to `reference-index.md` (~10t). This **frees ~30t of headroom** in guidance.md.

### What This Proposal Does NOT Change

- **`manifest.yaml`** — no changes; manifest stays at ~985t
- **`examples/*.md`** — no changes to any example files
- **Token budgets** — no budget overrides requested
- **Test token budget default** — stays at 850t (per schema §2)

---

## Deliverables

| # | Artifact | Description | Status |
|---|----------|-------------|--------|
| D1 | `reference-index.md` | Categorized topic router (~300t) | ⬜ Pending |
| D2 | `ref-core-patterns.md` | Core language patterns and domain modeling | ⬜ Pending |
| D3 | `ref-testing-quality.md` | Testing framework and CI quality | ⬜ Pending |
| D4 | `ref-security-safety.md` | Safety-critical C++, MISRA, DO-178C | ⬜ Pending |
| D5 | `ref-concurrency.md` | Concurrency, coroutines, resiliency | ⬜ Pending |
| D6 | `ref-build-toolchain.md` | Build system, packages, modules, ABI | ⬜ Pending |
| D7 | `ref-memory-lifetime.md` | Memory management, object lifetime, FFI | ⬜ Pending |
| D8 | `ref-brownfield-migration.md` | Brownfield migration and per-tier configs | ⬜ Pending |
| D9 | `ref-brownfield-playbooks.md` | Migration playbooks (C++98 through C++20) | ⬜ Pending |
| D10 | `ref-legacy-navigation.md` | Legacy navigation, triage, survival patterns | ⬜ Pending |
| D11 | `ref-operational.md` | Commands, tools, skill parity, archetypes, authorities | ⬜ Pending |
| D12 | `guidance.md` update | Replace quick-links table with reference-index.md link | ⬜ Pending |
| D13 | Test suite updates | Update tests referencing full-reference.md → split files | ⬜ Pending |
| D14 | `full-reference.md` removal | Remove monolith after content verified in split files | ⬜ Pending |
| D15 | Token budget validation | Verify each ref-*.md ≤ 3,500t | ⬜ Pending |

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| Each `ref-*.md` ≤ 3,500 tokens | `word_count × 1.3 ≤ 3500` per file |
| `reference-index.md` ≤ 500 tokens | Compact enough for single retrieval hop |
| `guidance.md` ≤ 450 tokens | Existing budget maintained |
| Zero content loss | Every section from `full-reference.md` present in exactly one `ref-*.md` |
| All tests pass | Full test suite green after restructure |
| RAG 5-query validation | All 5 canonical queries answerable within 3,500t window |
| No manifest changes | `manifest.yaml` unchanged (diff is empty for this file) |

---

## Impact Assessment

- **Test files affected:** All tests referencing `full-reference.md` (~20 test files)
- **Semver bump:** MINOR — content relocated, not removed
- **Risk:** Cross-cutting sections may need duplication or cross-links
- **Mitigation:** Each `ref-*.md` includes a "See Also" footer for related files

---

## Relationship to Other Proposals

| Proposal | Relationship |
|----------|-------------|
| `cpp-manifest-token-exception` | Independent — this proposal improves RAG regardless of manifest budget |
| `cpp-manifest-150t-compliance` | Depends on this proposal — uses split files as routing destinations |

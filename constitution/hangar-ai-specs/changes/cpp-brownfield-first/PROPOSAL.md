# Proposal: C++ Avatar — Brownfield-First Enrichment (CBF-*)

**ID:** cpp-brownfield-first  
**Status:** DRAFT  
**Author:** Copilot (via version-sensitivity review panel)  
**Date:** 2026-04-27  
**Predecessor:** `cpp-external-sources-enrichment` (DEFERRED — this proposal is its prerequisite)  
**Laws:** ENG-11.1, ENG-11.2, ENG-4.1, ENG-6.1, ENG-10.1, ENG-3.1  

---

## Problem Statement (PRD-1.2)

The C++ avatar version routing system (PR #47/#48) successfully implemented 5-tier routing based on project C++ standard. However, a version-sensitivity review of the `cpp-external-sources-enrichment` proposal (6 reviewers, 2026-04-27) revealed two categories of urgent unresolved gaps:

**Category 1 — Active liability exposure (R7: Plaintiff Attorney)**

The routing system correctly gates C++20 content away from CWR (C++14, ~60% of AA C++ LOC) but left **no content in its place** for two safety-critical topics:

1. **FAR 117 timezone arithmetic:** `std::chrono::zoned_time` (C++20) is correctly filtered away from CWR. There is currently zero timezone-aware guidance for the team legally obligated to implement FAR 117 duty-period calculations. The routing system's own correctness is evidence against AA in litigation. Every day without a C++14 bridge extends the willful-knowledge period.

2. **JNI thread safety:** The avatar's concurrency content (`ref-concurrency-threading.md`) correctly routes to `transitional` tier for CWR — but contains zero JNI guidance. "Routing to nothing" is worse than "routing to wrong": the causal chain from `static JNIEnv* g_env` (a real pattern in `CrewWatchSolverJNI.cpp`) to a production thread-safety defect is now *shorter*, not longer. `CrewWatchSolverJNI.cpp` was identified as "the most dangerous file in AA's C++ portfolio" in the ESE review panel.

**Category 2 — Version routing coverage gaps (R8: Cross-Version Completeness)**

55% of the planned ESE content targets the `greenfield` tier (~0% of current AA C++ LOC). The 95% of AA C++ LOC in `legacy`/`brownfield`/`transitional` tiers received coverage grades of D, C, and C respectively. Specific gaps:

- CWR/IOC_ALP developers (C++14) have **no avatar guidance** for safe string formatting, ranges pipelines, bounds-safe array views, or cooperative thread cancellation — all available TODAY via bridge libraries with C++11/14 minimums
- C++98/03 developers have no Rule of Three guidance (serving Rule of Five to C++98 produces uncompilable code)
- No `const char*` lifetime trap documentation for pre-C++17 developers
- `AVATAR-RAG-INDEX.yaml` tier `prefer`/`avoid` lists are not yet updated for the planned ESE deliverables

**Category 3 — Routing infrastructure completeness**

Before any ESE task can execute, the version routing infrastructure must be finalized:
- Zero `cpp_version_min` on any planned ESE deliverable (CI fails on merge)
- Planned C++20-only files have no `transitional.avoid`/`brownfield.avoid` entries (recreates pre-PR#47 silent routing failures)
- Two planned reference files exceed the ≤2,800t token ceiling at conception

---

## Laws Cited (ENG-11.2 Compliance)

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law | Governs proposal lifecycle |
| [ENG-11.2](laws/engineering/eng-11-hangar-sdd.md) | Proposal Completeness | Citations, success criteria, deliverables |
| [ENG-4.1](laws/engineering/eng-4-testing.md) | Atomic TDD Law | All code examples TDD-demonstrable |
| [ENG-6.1](laws/engineering/eng-6-security.md) | Security by Design | JNI safety, lock-free patterns, timezone safety-critical |
| [ENG-6.5](laws/engineering/eng-6-security.md) | Format String Safety | fmtlib replaces unsafe printf-family |
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | Avatar taxonomy and routing rules |

---

## Governing Principle

> **Brownfield-first, greenfield-later.** 95% of AA's C++ LOC is in `legacy`/`brownfield`/`transitional` tiers TODAY. Every deliverable in this proposal must reach at least one of these tiers. Greenfield (C++20) content is explicitly out of scope — that is ESE's job after this proposal ships.

---

## AA Production Tier Context

| Repository | Standard | Tier | LOC Share |
|---|---|---|---|
| IOC_ALP, hte_pm_hostconn, CWR, IOC_FosQuery2 | C++14 | `transitional` | ~60% |
| SPEClient | MSVC 6.0 / pre-C++98 | `legacy` | ~24% |
| herc-odyssey-linux | C++98/03 | `brownfield` | ~11% |
| IOC_ScreenPrinter | C++17 | `modern` | ~5% |

**CWR scenario:** `standard: "14"`, `idiom_level: "03"` — compiled C++14, written in C++03 idioms.

---

## Deliverables

### Phase 0: Routing Infrastructure Wiring

Fixes the `AVATAR-RAG-INDEX.yaml` to wire existing and planned brownfield content into correct tiers. Must complete before any Phase 1–4 work merges.

| Task | Deliverable | Change |
|------|------------|--------|
| CBF-00.1 | `AVATAR-RAG-INDEX.yaml` | Add `ref-brownfield-survival.md` to `transitional.prefer`, `brownfield.prefer`, `legacy.prefer` |
| CBF-00.2 | `AVATAR-RAG-INDEX.yaml` | Add all CBF bridge files to `transitional.prefer` as they are created |
| CBF-00.3 | `AVATAR-RAG-INDEX.yaml` | Add avoid-list stubs for future ESE C++20-only files (`transitional.avoid`, `brownfield.avoid`) |

### Phase 1: R7 Liability Closures — Immediate Priority

Two tasks that close R7's two strongest litigation theories. Ship these first.

| Task | File | `cpp_version_min` | Tier | Gap |
|------|------|-------------------|------|-----|
| CBF-01 | `examples/ENG-6.1-timezone-cpp14.md` | 11 | `transitional.prefer` | FAR 117 C++14 bridge (HowardHinnant/date) |
| CBF-02 | `examples/ENG-6.1-jni-thread-cpp98.md` | 98 | `legacy.prefer`, `brownfield.prefer` | JNI thread safety — C++98 `pthread_key_t`/`TlsAlloc` |
| CBF-03 | `examples/ENG-6.1-jni-thread-cpp11.md` | 11 | `transitional.prefer` | JNI thread safety — C++11 `thread_local` RAII |

### Phase 2: Bridge Deliverables for Transitional Tier

Libraries available TODAY for C++11/14 teams with APIs identical to their C++20 counterparts.

| Task | File | `cpp_version_min` | Bridge for | OSS Source |
|------|------|-------------------|-----------|------------|
| CBF-04 | `examples/ENG-6.1-fmtlib-format.md` | 11 | `std::format` (C++20) | `fmtlib/fmt` (MIT) |
| CBF-05 | `examples/ENG-3.1-ranges-range-v3.md` | 14 | `std::ranges` (C++20) | `ericniebler/range-v3` (Boost) |
| CBF-06 | `examples/ENG-6.1-gsl-span-cpp14.md` | 14 | `std::span` (C++20) | `microsoft/GSL` (MIT) |
| CBF-07 | `examples/ENG-6.1-thread-stop-flag.md` | 11 | `std::jthread`/`stop_token` (C++20) | Original (std::atomic pattern) |
| CBF-08 | `examples/ENG-6.1-lock-free-cpp14.md` | 11 | `std::hazard_pointer` (C++23) | `boostorg/lockfree` (Boost) |

### Phase 3: Version Correctness Fixes

Existing content gaps that, if unaddressed, serve technically incorrect guidance to brownfield tiers.

| Task | File | `cpp_version_min` | Issue |
|------|------|-------------------|-------|
| CBF-09 | Rule of Three subsection in `ref-core-language.md` | 98 | Move semantics don't exist pre-C++11; serving Rule of Five to C++98 produces uncompilable code |
| CBF-10 | `examples/ENG-6.1-const-char-lifetime.md` | 03 | `const char*` lifetime traps for pre-C++17 (parallels `string_view` traps) |
| CBF-11 | `ref-brownfield-survival.md` — MSVC 6.0 golden-master section | 98 | MSVC 6.0 has no GTest path; stdlib-only fallback needed for SPEClient tier |

### Phase 4: ESE Routing Preparation

Infrastructure work that unblocks ESE execution. Produces no user-facing content — only governance wiring.

| Task | Deliverable | Purpose |
|------|------------|---------|
| CBF-12 | `hangar-ai-specs/changes/cpp-external-sources-enrichment/tasks.md` annotations | Add `cpp_version_min` to every ESE task definition (ESE-V1) |
| CBF-13 | `AVATAR-RAG-INDEX.yaml` full ESE wiring | All planned ESE files in correct tier prefer/avoid lists (ESE-V2) |
| CBF-14 | ESE `tasks.md` — confirm file splits | ESE-V3 (ref-cpp20-features Part 1+2) and ESE-V4 (ref-concurrency-advanced Part 1+2) |
| CBF-15 | `tests/unit/test_phase2_e4_rag_eval.py` | Add brownfield routing scenarios: FAR 117 C++14 query routes to transitional; JNI query routes to legacy/brownfield; fmtlib query routes to transitional |

---

## Copyright and Source Licensing

All Phase 2 deliverables derive from OSS sources. License summary:

| OSS Source | License | Use Mode | Task |
|-----------|---------|---------|------|
| `HowardHinnant/date` | MIT | Derive examples with attribution | CBF-01 |
| `android/ndk-samples` | Apache 2.0 | Derive examples with attribution | CBF-02, CBF-03 |
| `fmtlib/fmt` | MIT | Derive examples with attribution | CBF-04 |
| `ericniebler/range-v3` | Boost Software License | Derive examples with attribution | CBF-05 |
| `microsoft/GSL` | MIT | Derive examples with attribution | CBF-06 |
| `boostorg/lockfree` | Boost Software License | Derive examples with attribution | CBF-08 |

All example files must include derivation comment block per ESE OSS governing principle:
```cpp
// Derived from: <repo> (<license>)
// Algorithm/pattern: <reference>
// AA adaptation: <domain context>
```

---

## Acceptance Criteria

A task is **done** when:
1. File created/updated with correct `cpp_version_min` frontmatter
2. File appears in correct `prefer` list in `AVATAR-RAG-INDEX.yaml`
3. Code examples contain `// COMPLIANT` and `// NON-COMPLIANT` blocks with rationale
4. `## Edge Cases & Warnings` section present
5. OSS derivation comment block present in all Phase 2 files
6. `aa-constitution-lint .` passes
7. Token budget respected (≤ 700t for examples, ≤ 2,800t for ref sections)

The full proposal is **done** when:
- CBF-01 and CBF-02 are merged (closes R7's two strongest theories)
- All bridge files are in `transitional.prefer` and reachable to CWR/IOC_ALP
- CBF-12–14 complete (ESE is unblocked and can execute without CI failures)
- CBF-15 complete (RAG eval harness validates brownfield routing)
- `cpp-external-sources-enrichment` proposal status updated from DEFERRED to READY-TO-EXECUTE

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| `transitional` tier coverage grade (R8) | C | B+ |
| `brownfield` tier coverage grade (R8) | C | B |
| `legacy` tier coverage grade (R8) | D | C+ |
| R7 FAR 117 theory | Open | Closed |
| R7 JNI wrongful-death theory | Open | Closed |
| ESE CI readiness | Fails immediately | Passes all gates |

---

## Source Citation Index

**OSS Derivation Sources:**

1. `HowardHinnant/date` — MIT — CBF-01. Howard Hinnant (author of C++20 `<chrono>`). Same API as `std::chrono` calendar; migration to C++20 is mechanical.
2. `android/ndk-samples` — Apache 2.0 — CBF-02/03. Android Open Source Project. JNI thread lifecycle patterns.
3. `fmtlib/fmt` — MIT — CBF-04. Victor Zverovich. IS the reference implementation that became `std::format`.
4. `ericniebler/range-v3` — Boost Software License — CBF-05. Eric Niebler. IS the reference implementation for ISO C++20 ranges. Namespace differs from `std::ranges`.
5. `microsoft/GSL` — MIT — CBF-06. Microsoft. `gsl::span` API identical to C++20 `std::span`.
6. `boostorg/lockfree` — Boost Software License — CBF-08. Tim Blechmann. Algorithms: Treiber 1986, Michael & Scott 1996.

**Further Reading (no-embed):**

1. Williams, A. *C++ Concurrency in Action, 2nd Ed.* Manning, 2019. `<!-- further-reading no-embed -->`
2. Howard Hinnant. *date library documentation.* https://howardhinnant.github.io/date/date.html `<!-- further-reading no-embed -->`

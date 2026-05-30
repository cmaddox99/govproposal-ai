# Version-Sensitivity Review: ESE Proposal (Round 3)

**Change:** cpp-external-sources-enrichment  
**Review trigger:** PR #47 + PR #48 — 5-tier C++ version-sensitive RAG routing system merged to main  
**Date:** 2026-04-27  
**Branch:** feat/cpp-external-sources-enrichment  
**Reviewers:** R1 (Copyright), R4 (RAG Expert), R5 (C++ Master), R6 (AA Engineer), R7 (Plaintiff Attorney), R8 (Cross-Version Completeness)  

---

## Post-Review Correction: GAP-AA1 (Characterization Testing)

**Finding:** R8 identified GAP-AA1 as missing content requiring a stdlib-only golden-master pattern for all C++98 codebases. This was overly conservative.

**Correction:** `ENG-4.1-characterization-test-pattern.md` already exists in the avatar. GoogleTest 1.8.x was specifically designed to support pre-C++11 compilers — it is the final C++98-compatible GTest release (EOL 2018). The actual gap was a **routing gap**, not missing content: the file had `cpp_version_min: 11`, preventing it from reaching legacy/brownfield tiers.

**Fix applied:**
- `ENG-4.1-characterization-test-pattern.md` `cpp_version_min` lowered `11 → 98`
- `ref-testing-gtest-core.md` `cpp_version_note` updated to document GTest 1.8.x C++98 support and vcpkg pin (`gtest==1.8.1`)
- ESE-65 scope narrowed: stdlib-only golden-master now targets **MSVC 6.0 (SPEClient) only** — GTest 1.8.x requires MSVC 8.0+ (VS 2005+) and does not support MSVC 6.0

**Net change to GAP-AA1:** Primary solution is a `cpp_version_min` routing fix. ESE-65 survives as a small MSVC 6.0 fallback section, not a full new content item.

---

## Executive Summary

The ESE proposal was authored **before** the version-sensitive routing system (PR #47/#48) existed. As written, the proposal would recreate the exact routing failures that PR #47/#48 was built to prevent:

- **Zero `cpp_version_min` annotations** on any proposed deliverable → CI fails immediately on merge (R4-B5)  
- **No tier `prefer`/`avoid` placements** → 20 new files served to all tiers indiscriminately (R4-B6)  
- **55% of new content targets `greenfield` (~0% AA LOC)** while 95% of AA C++ LOC gets ~30% of new content (R4, R8)  
- **FAR 117 timezone guidance is gated behind C++20** with no C++14 fallback — the routing system correctly filters it away from CWR, creating a safety regression (R5, R7, R8)  
- **Two reference files exceed the ≤2,800t ceiling at conception** and must be pre-split in the proposal (R4-B7)

**Net verdict: AMENDMENTS REQUIRED before execution begins.** The routing infrastructure is sound. The proposal must be updated to wire into it correctly.

---

## Panel Summary

| Reviewer | Pre-Version-Routing Verdict | Post-Version-Routing Verdict | Change |
|---|---|---|---|
| R1 — Copyright Counsel | ✅ PROCEED (3 prerequisites) | ✅ PROCEED (3 prerequisites + 3 new doc items) | Non-blocking additions only |
| R4 — RAG Expert | ⚠️ CONDITIONAL (4 blockers) | 🔴 BLOCKED (9 blockers — 5 new) | 5 new blocking issues |
| R5 — C++ Master | ⚠️ CONDITIONAL (6 blockers) | 🔴 NOT SAFE TO IMPLEMENT (9 blockers — 3 new) | 3 new blockers; 12 split decisions |
| R6 — AA Engineer | ⚠️ CONDITIONAL (8 changes req.) | 🔴 BLOCKED (8 changes req., all new context) | All routing-related; 5 blocking |
| R7 — Plaintiff Attorney | ⚠️ DEMAND: HIGH | ⚠️ DEMAND: Neutral↓ on IP, UNCHANGED wrongful death, UP↑ on FAR 117 | FAR 117 regression is new theory |
| R8 — Cross-Version Completeness | _(new reviewer)_ | 🔴 AMENDMENTS REQUIRED — HIGH SEVERITY | 95% AA LOC gets D/C/C grade |

---

## Consolidated Blocking Issues

### Blocking: Must fix before any ESE task execution

| ID | Source | Issue | Required Action |
|----|--------|-------|-----------------|
| **B5** | R4 | Zero `cpp_version_min` frontmatter on any ESE deliverable | Add `cpp_version_min` to every proposed file; CI test `test_phase2d_c4_ref_frontmatter.py` will fail on merge |
| **B6** | R4, R6 | No tier `prefer`/`avoid` placements for any ESE deliverable | Add all new files to `AVATAR-RAG-INDEX.yaml` tier lists before Phase 1 |
| **B7** | R4 | `ref-concurrency-advanced.md` (~5,600t) and `ref-cpp20-features.md` (~6,300t) exceed ≤2,800t ceiling | Split each into two files at conception (see split decisions below) |
| **B8** | R4, R5 | GAP-C5 (lock-free) version split undeclared; `std::hazard_pointer` is C++23; C++14 developers receive wrong content | Produce two files: `ENG-6.1-lock-free-cpp14.md` (ABA/atomic pattern) + `ENG-6.1-lock-free-cpp23.md` (hazard_pointer) |
| **B9** | R4 | `transitional.avoid` and `brownfield.avoid` not extended for 13 new C++20 files | Extend avoid lists in `AVATAR-RAG-INDEX.yaml` for all C++20-only deliverables before any ESE merge |
| **FAR-117** | R5, R6, R7, R8 | GAP-20-11 (timezone) is C++20-only; routing correctly filters it away from CWR (C++14); **no guidance remains** for the team legally obligated by FAR 117 | Add `HowardHinnant/date` (MIT, C++11+) as bridge; create `ref-cpp14-bridges.md` or add section to existing transitional-tier file |
| **JNI-CPP98** | R8 | GAP-AA2 JNI RAII wrapper uses `std::atomic` (C++11); CWR may have C++98 TUs; no `pthread_key_t`/`TlsAlloc` pattern | Add C++98-safe JNI thread pattern alongside C++11 RAII wrapper |
| **GATE-THREAD-POOL** | R5 | `bshoshany/thread-pool` requires C++17; not gated to `modern`/`greenfield` avoid in proposal | Add `bshoshany/thread-pool` examples to `transitional.avoid` and `brownfield.avoid` |
| **CG11-VERSION** | R5 | GAP-CG11 `cpp_version_min` must be `17` (not `14`) — `std::string_view` is C++17 | Set `cpp_version_min: 17`; add pre-C++17 `const char*` lifetime trap section at a lower version min |

---

## Blocking: File Split Decisions (12 required — R5)

| Gap | C++11/14 File | C++20+ File | Basis for split |
|-----|--------------|-------------|-----------------|
| GAP-20-2 Ranges | `ENG-3.1-ranges-range-v3.md` (`cpp_version_min: 14`) | `ENG-3.1-ranges-views.md` (`cpp_version_min: 20`) | Different namespaces; `filter_view` const-iterability semantics differ |
| GAP-20-3 Format | `ENG-6.1-fmtlib-format.md` (`cpp_version_min: 11`) | `ENG-6.1-std-format.md` (`cpp_version_min: 20`) | fmtlib is a C++11 polyfill with identical API; serves CWR today |
| GAP-C5 Lock-free | `ENG-6.1-lock-free-cpp14.md` (`cpp_version_min: 11`) | `ENG-6.1-lock-free-cpp23.md` (`cpp_version_min: 23`) | `std::hazard_pointer` is C++23; ABA + epoch reclamation serves C++11+ today |
| GAP-C3 jthread | `ENG-6.1-thread-stop-flag.md` (`cpp_version_min: 11`) | `ENG-6.1-jthread-stop-token.md` (`cpp_version_min: 20`) | `std::jthread` is C++20; manual stop-flag pattern covers C++11/14 |
| GAP-20-11 Timezone | `ENG-6.1-timezone-cpp14.md` (`cpp_version_min: 11`) using `HowardHinnant/date` | `ENG-6.1-timezone-cpp20.md` (`cpp_version_min: 20`) | Legal obligation (FAR 117); CWR cannot wait for C++20 |
| GAP-20-5 span | `ENG-6.1-gsl-span-cpp14.md` (`cpp_version_min: 14`) using `gsl::span` | `ENG-6.1-span-bounds-safety.md` (`cpp_version_min: 20`) | `std::span` is C++20; `gsl::span` is C++14-compatible |
| GAP-CG11 string_view | `ENG-6.1-const-char-lifetime.md` (`cpp_version_min: 03`) | `ENG-6.1-string-view-lifetime.md` (`cpp_version_min: 17`) | `const char*` traps exist pre-C++17; `string_view` is C++17 |
| GAP-CG3 Rule of Zero/Five | Rule of Three subsection (`cpp_version_min: 98`) | Rule of Five section (`cpp_version_min: 11`) | Move semantics don't exist pre-C++11; serving Rule of Five to C++98 is broken |
| GAP-AA2 JNI | `ENG-6.1-jni-thread-cpp98.md` (`cpp_version_min: 98`) using `pthread_key_t` | `ENG-6.1-jni-thread-cpp11.md` (`cpp_version_min: 11`) using `thread_local` RAII | JNI is a C API; C++98 TUs need `pthread_key_t`/`TlsAlloc` pattern |
| ref-cpp20-features.md | Split into `ref-cpp20-features-part1.md` (≤2,800t) | `ref-cpp20-features-part2.md` (≤2,800t) | Token budget: ~6,300t at conception exceeds ≤2,800t ceiling |
| ref-concurrency-advanced.md | Split into `ref-concurrency-advanced-part1.md` (≤2,800t) | `ref-concurrency-advanced-part2.md` (≤2,800t) | Token budget: ~5,600t at conception exceeds ≤2,800t ceiling |
| `std::atomic<shared_ptr<T>>` | C++14: free functions only (`std::atomic_load`/`atomic_store` — deprecated) | C++20: `std::atomic<shared_ptr<T>>` type | C++14 type doesn't exist; only deprecated free functions; gap in current content |

---

## Tier Coverage Scorecard (R8)

| Tier | AA LOC Share | ESE Content Directed Here | Coverage Grade | Change Needed |
|------|-------------|--------------------------|----------------|---------------|
| `legacy` (pre-C++98) | ~24% | GAP-AA2 C++98 JNI, GAP-AA1 C++98 golden-master, GAP-CG3 Rule of Three | **D → C** with amendments | Add C++98-safe variants |
| `brownfield` (C++98/03) | ~11% | ESE-A Brownfield Survival Pack | **C → B** with routing fix | Wire to `brownfield.prefer` |
| `transitional` (C++11/14) | ~60% | ESE-A + bridge libs (fmtlib, range-v3, HowardHinnant/date, gsl::span) | **C → B+** with splits | Split files + FAR 117 bridge |
| `modern` (C++17) | ~5% | GAP-CG11 string_view, bshoshany thread-pool, source_location | **B** | Add `cpp_version_min: 17` gate on bshoshany |
| `greenfield` (C++20+) | ~0% | 55% of ESE content | **A** | Extend avoid lists to block from older tiers |

---

## Required `AVATAR-RAG-INDEX.yaml` Changes (R4, R6)

### Tier prefer additions

```yaml
# transitional.prefer — add ALL of these:
- ref-brownfield-survival.md       # cpp_version_min: 98 (covers up through C++14)
- ref-cpp14-bridges.md             # cpp_version_min: 11 (fmtlib, range-v3, HH date, gsl::span)
- ENG-6.1-fmtlib-format.md        # cpp_version_min: 11
- ENG-3.1-ranges-range-v3.md      # cpp_version_min: 14
- ENG-6.1-timezone-cpp14.md       # cpp_version_min: 11 (FAR 117 bridge)
- ENG-6.1-lock-free-cpp14.md      # cpp_version_min: 11
- ENG-6.1-gsl-span-cpp14.md       # cpp_version_min: 14
- ENG-6.1-thread-stop-flag.md     # cpp_version_min: 11

# brownfield.prefer — add:
- ref-brownfield-survival.md       # cpp_version_min: 98
- ENG-6.1-const-char-lifetime.md  # cpp_version_min: 03
- ENG-6.1-jni-thread-cpp98.md     # cpp_version_min: 98

# legacy.prefer — add:
- ref-brownfield-survival.md       # cpp_version_min: 98
- ENG-6.1-jni-thread-cpp98.md     # cpp_version_min: 98
```

### Tier avoid additions (B9 — critical)

```yaml
# transitional.avoid — add ALL C++20-only ESE deliverables:
- ref-cpp20-features-part1.md
- ref-cpp20-features-part2.md
- ENG-3.1-ranges-views.md         # std::ranges C++20
- ENG-6.1-std-format.md           # std::format C++20
- ENG-6.1-jthread-stop-token.md   # std::jthread C++20
- ENG-6.1-lock-free-cpp23.md      # std::hazard_pointer C++23
- ENG-6.1-timezone-cpp20.md       # std::chrono::zoned_time C++20
- ENG-6.1-span-bounds-safety.md   # std::span C++20
- ENG-6.1-string-view-lifetime.md # std::string_view C++17→ use modern.prefer
- ENG-3.2-spaceship-operator.md   # C++20
- ENG-3.1-modules.md              # C++20

# brownfield.avoid — same list plus:
- ENG-6.1-gsl-span-cpp14.md      # gsl::span requires C++14
- ENG-3.1-ranges-range-v3.md     # range-v3 requires C++14
```

---

## Priority Changes Required

| Gap | Old Priority | New Priority | Reason |
|-----|-------------|-------------|--------|
| GAP-20-4 (spaceship `<=>`) | P1 | **P3** | 0% AA LOC is C++20; CWR domain objects are mutable int-returning structs; no value-type domain objects in active use |
| GAP-20-11 (timezone) | P1 | **P1** (confirmed) | Legal obligation; FAR 117 applies to CWR TODAY; requires C++14 bridge alongside C++20 content |
| GAP-C5 (lock-free) | P2 | **P2** (confirmed, but split required) | C++14 lock-free path (B8) must be produced; C++23 hazard_pointer path is greenfield-only |

---

## New Deliverables Required (not in original proposal)

| New Task ID | File | Version Min | Tier | Rationale |
|-------------|------|------------|------|-----------|
| ESE-56 | `ENG-6.1-timezone-cpp14.md` | C++11 | transitional, brownfield.prefer | FAR 117 bridge using HowardHinnant/date — R5, R7, R8 |
| ESE-57 | `ENG-6.1-fmtlib-format.md` | C++11 | transitional.prefer | fmtlib bridge for std::format — R6 split of GAP-20-3 |
| ESE-58 | `ENG-3.1-ranges-range-v3.md` | C++14 | transitional.prefer | range-v3 bridge for std::ranges — R6 split of GAP-20-2 |
| ESE-59 | `ENG-6.1-gsl-span-cpp14.md` | C++14 | transitional.prefer | gsl::span bridge for std::span — R5 split of GAP-20-5 |
| ESE-60 | `ENG-6.1-lock-free-cpp14.md` | C++11 | transitional.prefer | ABA/atomic lock-free for C++11/14 — R4-B8, R5 split of GAP-C5 |
| ESE-61 | `ENG-6.1-thread-stop-flag.md` | C++11 | transitional.prefer | Manual stop-flag pattern for C++11/14 — R5 split of GAP-C3 |
| ESE-62 | `ENG-6.1-jni-thread-cpp98.md` | C++98 | legacy.prefer, brownfield.prefer | C++98 JNI `pthread_key_t`/`TlsAlloc` pattern — R8-1 |
| ESE-63 | Rule of Three subsection in `ref-core-language.md` | C++98 | brownfield.prefer, legacy.prefer | Move semantics don't exist pre-C++11 — R8-3 |
| ESE-64 | `ENG-6.1-const-char-lifetime.md` | C++03 | brownfield.prefer | `const char*` lifetime traps — R8-5 split of GAP-CG11 |
| ESE-65 | GAP-AA1 C++98 golden-master pattern section | C++98 | legacy.prefer | C++98-safe characterization testing (no C++11 test framework) — R8-2 |

---

## R1 Documentation Items (non-blocking)

| ID | Item |
|----|------|
| V1 | Add "derived files by tier" attribution table to ESE-00.3 as version-split files multiply |
| V2 | Routing guide must clarify whole-file vs. section-level context loading; if section-level, inline attribution in `★ C++NN` sections becomes mandatory |
| V3 | `bshoshany/thread-pool` C++14 backport entry in ESE-00.3 with Use Mode A/B determination |

---

## R7 Required Immediate Actions (liability closure)

Two actions close R7's two strongest theories:

1. **Add C++14 timezone guidance (ESE-56)** to transitional tier — closes the FAR 117 routing gap. Until this lands, the routing system is evidence against AA (routing correctly excludes C++20 content but leaves nothing in its place for CWR).  
2. **Implement GAP-AA2 JNI (ESE-29 + ESE-62)** — closes the `static JNIEnv*` wrongful-death theory. The "approved but unimplemented" state extends the willful-knowledge period for every day these tasks remain unchecked.

---

## New Phase 0.5 Required in tasks.md

Before any Phase 1 work begins, the following must complete:

- **ESE-V1**: Add `cpp_version_min` frontmatter to all ESE task definitions (preparation)
- **ESE-V2**: Extend `AVATAR-RAG-INDEX.yaml` with all new `prefer` and `avoid` placements from this review
- **ESE-V3**: Split `ref-cpp20-features.md` plan into Part 1 + Part 2 (≤2,800t each)
- **ESE-V4**: Split `ref-concurrency-advanced.md` plan into Part 1 + Part 2 (≤2,800t each)
- **ESE-V5**: Add new ESE-56 through ESE-65 tasks for bridge/split/C++98 deliverables

---

## Individual Reviewer Files

| Reviewer | File |
|----------|------|
| R1 (Copyright) | `R1-VERSION-REVIEW.md` — committed `f85b7fc` |
| R4 (RAG Expert) | `R4-VERSION-REVIEW.md` — committed `4b8f0ff` |
| R5 (C++ Master) | `R5-VERSION-REVIEW.md` — committed `4fb39f4` |
| R6 (AA Engineer) | `R6-VERSION-REVIEW.md` — committed `31f70c2` |
| R7 (Plaintiff Attorney) | `R7-VERSION-REVIEW.md` — committed `80bf7ac` |
| R8 (Cross-Version Completeness) | `R8-VERSION-REVIEW.md` — committed `da0756a` |

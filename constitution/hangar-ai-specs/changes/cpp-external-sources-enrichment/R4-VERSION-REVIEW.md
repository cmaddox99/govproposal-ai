# R4 — RAG Expert: Version-Sensitivity Review of ESE Proposal

**Reviewer:** R4 — Constitutional AI RAG Expert (version-routing system architect, PR #47/#48)
**Review Date:** 2026-07-15
**Proposal Under Review:** `cpp-external-sources-enrichment` (ESE-*)
**Files Reviewed:** PROPOSAL.md, AVATAR-RAG-INDEX.yaml (`version_routing_policy` section and `refs_inventory`),
`docs/guides/avatars/cpp-version-sensitive-routing.md`, REVIEW-PANEL.md (R4 original sections + OSS response)
**Governing System:** Five-tier version-sensitive routing (PR #47 foundation + PR #48 Amendment 1)
**Laws:** ENG-10.1, ENG-11.1, ENG-11.2

---

## Executive Finding

The ESE proposal adds 20 deliverable artifacts (3 new ref files, 5 expanded ref files, 17 new example files,
3 governance wiring updates) with **zero `cpp_version_min` assignments and zero tier routing placements** for any
new file. This is not a documentation gap — it is a structural routing defect that will cause the five-tier
version routing system (built in PR #47/#48 at significant test-suite investment: 301 tests across 7 files) to
silently serve C++20 content to C++14 developers and C++11 content to C++98 developers. The 95% of AA C++ LOC
that lives in legacy/brownfield/transitional tiers receives between zero and marginal benefit from the majority
of ESE deliverables because those deliverables are C++20-centric and have no routing instructions to exclude
them from version-mismatched queries. Five new blocking defects are added to the four already identified in the
original R4 review (and escalated in R4-OSS-RESPONSE.md), bringing the total R4 blocking count to
**9 blocking issues**. The proposal must be amended with per-deliverable `cpp_version_min` values, tier `prefer`
placements, extended `avoid` list entries for all new C++20 content, pre-split decisions for all over-budget
files, and C++03-idiom variant specifications for the CWR scenario before any ESE task may begin.

---

## Section 1: Per-Deliverable Version Analysis

### 1.1 New Reference Files

| File | `cpp_version_min` | Tier placement (`prefer`) | Version split needed | Token concern |
|------|:-----------------:|--------------------------|----------------------|---------------|
| `ref-cpp20-features.md` (proposed) | **20** | `greenfield` ONLY | **YES — mandatory split.** Already projected at ~5,700t before OSS overhead (~6,300t after). At ≤2,800t ceiling this requires at minimum TWO files: `ref-cpp20-core.md` (~2,400t) covering Modules, Ranges/Views, span, spaceship, format, bit_cast (6 P1/P2 sections); `ref-cpp20-runtime.md` (~2,400t) covering source_location, constinit, atomic_ref, coroutine generators, Calendar, lambda improvements, aggregate improvements (7 P2/P3 sections). **This split was already required by original BLOCKING Issue 1 — the version-routing lens confirms it is non-negotiable.** | 🔴 CRITICAL — exceeds ceiling by 125% |
| `ref-concurrency-advanced.md` (proposed) | **11** (baseline); `★ C++17` on parallel-algorithms section; `★ C++20` on jthread, hazard_pointer, atomic_ref | `transitional.prefer`, `modern.prefer`, `greenfield.prefer` | **YES — mandatory split.** Already projected at ~5,000t pre-ESE content + ~600t OSS overhead = ~5,600t. The version-routing split is also the content split: **`ref-concurrency-advanced-core.md`** (`cpp_version_min: 11`, ~2,400t) covering memory ordering, lock-free basics, false sharing, condition variables, promise/future, CP.42/43/50 — routes into `transitional.prefer`; **`ref-concurrency-advanced-modern.md`** (`cpp_version_min: 17`, ~2,200t) covering parallel algorithms, jthread/stop_token, CP.51/52/53 coroutine rules, hazard pointers, atomic_ref — routes into `modern.prefer` + `greenfield.prefer`. | 🔴 CRITICAL — exceeds ceiling by 100% |
| `ref-brownfield-survival.md` (proposed) | **98** | `legacy.prefer`, `brownfield.prefer` | **SINGLE file acceptable** — all 8 gaps (GAP-AA1–AA8) target C++98/03 era codebases. RCPtr migration section notes the migration *destination* may use C++11 smart pointers (add `★ C++11` inline callout, do NOT gate the whole section). Projected ~2,600t including OSS overhead — marginally within ≤2,800t ceiling; requires disciplined section sizing. | 🟠 TIGHT — must be measured before commit |

### 1.2 Enhanced Reference Files

| File | Additions' `cpp_version_min` | Tier routing impact | Version split needed | Token concern |
|------|:----------------------------:|--------------------|-----------------------|---------------|
| `ref-advanced-cpp.md` (currently ~5,040t) | CRTP: **11/98**; type traits: **11**; tag dispatch: **98**; advanced concepts: **20**; NTTPs: **20**; policy-based: **98**; C++20 lambda: **20**; `deducing this`: **23** | New `★` markers required for C++20/23 sections. File is ALREADY ~5,040t — 80% over the ≤2,800t ceiling before ESE additions. Projected at ~7,100t post-ESE. | **YES — retroactive split required BEFORE any ESE additions.** Proposed: `ref-advanced-cpp-templates.md` (`cpp_version_min: 98`, covers CRTP + type traits + tag dispatch + policy-based, ~2,400t) + `ref-advanced-cpp-modern.md` (`cpp_version_min: 20`, covers advanced concepts + NTTPs + C++20 lambda improvements + `deducing this`, ~2,200t). This split has version-routing benefits: transitional-tier developers see CRTP + type traits without C++20 advanced concepts noise. | 🔴 CRITICAL — already over ceiling today |
| `ref-core-language.md` (currently ~4,769t) | CG1/CG2/CG3/CG4: **11**; string_view governance (CG11): **17**; C++20 aggregate (GAP-20-13): **20** | Must add `★ C++17` on string_view section; `★ C++20` on aggregate section. File is already ~4,769t — projected ~7,540t post-ESE. | **YES — retroactive split required BEFORE any ESE additions.** Proposed: `ref-core-language-fundamentals.md` (`cpp_version_min: 11`, covers CG1–CG4, container selection, ~2,400t) + `ref-core-language-modern.md` (`cpp_version_min: 17`, covers string_view governance + C++20 aggregates, ~2,000t). | 🔴 CRITICAL — already over ceiling today |
| `ref-concurrency.md` (currently ~5,176t) | CP.42/43/50: **11**; CP.51/52/53: **20** (coroutine context) | CP.51–53 MUST carry `★ C++20`. File is ALREADY ~5,176t. | **YES — split audit required BEFORE ESE-17/24/25 content is added (per R4-OSS-RESPONSE.md).** Adding even CP.42/43/50 pushes this to ~5,600t+. The CP.51–53 coroutine content must go into the `modern`/`greenfield`-tier split portion. | 🔴 CRITICAL — live defect, already in production at 5,176t |
| `ref-build-toolchain.md` | SF.xx: **11** (pragma once); C++20 modules in SF: **20**; profiling: version-agnostic | Modules content in SF.xx must carry `★ C++20` and must be in `transitional.avoid` and `brownfield.avoid`. | **Single file likely OK** if additions are targeted (~2 sections). Requires token measurement before commit. | 🟡 LOW — if additions are scoped |
| `ref-safety-memory.md` | CPL.xx: **98**; GSL Profiles: **11** | GSL Profiles should appear in `brownfield.prefer` (CPL.xx governance helps C++98/03 codebases interoperating with C). | No split needed if additions are scoped. | 🟢 LOW — targeted additions |

### 1.3 New Example Files

| File | `cpp_version_min` | Tier `prefer` | Tier `avoid` | Token concern |
|------|:-----------------:|---------------|--------------|---------------|
| `ENG-6.1-memory-ordering.md` | **11** | `transitional`, `modern`, `greenfield` | — | ≤700t example ceiling; R6 argued 1,200–1,500t for concurrency — assess whether memory ordering requires the higher budget |
| `ENG-6.1-parallel-algorithms.md` | **17** | `modern`, `greenfield` | `transitional`, `brownfield`, `legacy` | C++17 execution policies (`std::execution::par`) do not exist in C++14; must be in all sub-17 `avoid` lists |
| `ENG-6.1-span-bounds-safety.md` | **20** | `greenfield` | `transitional`, `brownfield`, `legacy` | Note: `gsl::span` (C++14) is a valid alternative; add `★ C++14-GSL` callout |
| `ENG-6.1-jthread-stop-token.md` | **20** | `greenfield` | `modern`, `transitional`, `brownfield`, `legacy` | `std::jthread` is C++20 only; transitional developers have `std::thread` |
| `ENG-6.1-condition-variable.md` | **11** | `transitional`, `modern`, `greenfield` | — | HIGH VALUE for 60% of AA LOC |
| `ENG-6.1-lock-free-intro.md` | **11** | `transitional`, `modern`, `greenfield` | — | C++20 hazard_pointer section MUST carry `★ C++20`; C++11 atomic spinlock as baseline |
| `ENG-6.1-std-format.md` | **20** | `greenfield` | `modern`, `transitional`, `brownfield`, `legacy` | `modern` (C++17) tier: fmtlib is the alternative; do NOT serve std::format to C++17 developers |
| `ENG-3.1-crtp.md` | **98** | `brownfield`, `transitional`, `modern`, `greenfield` | — | C++03-idiom variant REQUIRED for CWR (see Section 2); `deducing this` C++23 alternative must carry `★ C++23` |
| `ENG-3.1-ranges-views.md` | **20** | `greenfield` | `modern`, `transitional`, `brownfield`, `legacy` | range-v3 (Boost) works on C++14; add `★ C++14-range-v3` callout for transitional developers |
| `ENG-3.1-modules.md` | **20** | `greenfield` | **`modern`, `transitional`, `brownfield`, `legacy`** | 🔴 MUST be in ALL sub-C++20 `avoid` lists — modules require CMake 3.28+, GCC 14+, Clang 17+, MSVC 19.38+; serving to C++14 CWR developers is actively harmful |
| `ENG-3.1-type-traits.md` | **11** | `transitional`, `modern`, `greenfield` | — | HIGH VALUE for 60% of AA LOC (C++14 metaprogramming) |
| `ENG-3.1-coroutine-generators.md` | **20** | `greenfield` | `modern`, `transitional`, `brownfield`, `legacy` | `co_yield` generator pattern is C++20; `modern` (C++17) has no coroutines |
| `ENG-3.1-policy-based-design.md` | **98** | `brownfield`, `transitional`, `modern`, `greenfield` | — | Policy-based design predates C++11; C++20 concepts alternative must carry `★ C++20` |
| `ENG-3.2-spaceship-operator.md` | **20** | `greenfield` | `modern`, `transitional`, `brownfield`, `legacy` | Three-way comparison (`<=>`) is C++20; `modern` (C++17) uses manual `bool operator<` chains |
| `ENG-5.5-source-location.md` | **20** | `greenfield` | `modern`, `transitional`, `brownfield`, `legacy` | Transitional/modern developers use `__FILE__`/`__LINE__` macros; add `★ C++03-macro` callout note |
| `ENG-3.1-false-sharing.md` | **11** | `transitional`, `modern`, `greenfield` | — | `alignas` is C++11; MSVC `__declspec(align(64))` is the C++98 equivalent — add `★ C++98-MSVC` callout |
| `ENG-3.1-constinit.md` | **20** | `greenfield` | `modern`, `transitional`, `brownfield`, `legacy` | `constinit` is C++20; note: `constexpr` variables are the C++11/14 alternative for the same initialization-order concern |

### 1.4 GAP-C5 Lock-Free: One File or Two?

**Ruling: ONE multi-version file with ★ callouts** (`ENG-6.1-lock-free-intro.md`, `cpp_version_min: 11`).

Rationale: The full lock-free progression — C++11 `std::atomic` spinlock → ABA problem via tagged
pointer (C++11) → Treiber/Michael-Scott queue (C++11 `std::atomic<T*>`) → `std::hazard_pointer` (C++20) —
is conceptually unified. Splitting it would break the pedagogical "why do we need hazard pointers"
progression. The file must carry:

```
## Treiber Stack — Baseline Lock-Free (C++11)        ← no marker, all tiers see this
## ABA Problem and Tagged Pointer Mitigation (C++11) ← no marker
## Lock-Free Queue (Boost.Lockfree derivation)        ← no marker; Boost works C++11+
## std::hazard_pointer ★ C++20                        ← gated; transitional developers see warning
```

The `transitional` tier (CWR/IOC_ALP, C++14) MUST receive a version-gate warning when the
`★ C++20` section is encountered: *"std::hazard_pointer requires C++20. Your project is C++14.
Use the tagged-pointer ABA mitigation pattern above, or Boost.Lockfree hazard_pointer (C++11+)."*

**Token budget**: The lock-free progression across 4 major sections × ~350t each + ~300t OSS overhead
≈ ~1,700t — within the ≤2,800t ceiling if example file budget is applied (and within R6's requested
1,200–1,500t range for concurrency examples with the 2,800t ceiling as the absolute bound).

---

## Section 2: CWR Scenario — ESE Gaps Requiring C++03-Idiom Variants

CWR configuration: `standard: C++14, idiom_level: C++03`. The avatar uses `idiom_level` — not
`standard` — to select examples. This means CWR developers receive examples without:
- `std::unique_ptr` / `std::shared_ptr` (raw pointer patterns only)
- `std::move` / rvalue references
- Lambdas
- `override`, `final`, `= delete`, `= default`
- Range-based for loops
- `auto` return types

### Priority Matrix for C++03-Idiom Variants

| Gap | ESE File | C++03 Variant Required? | What Changes in C++03 Version |
|-----|----------|:-----------------------:|-------------------------------|
| GAP-T1 (CRTP) | `ENG-3.1-crtp.md` | **YES — CRITICAL** | Raw pointer in `Derived*` casts, no `final`, no `override`, no `using Base::method` (C++11), explicit virtual destructor, no `= default` copy/move. Without this, Copilot suggests `std::unique_ptr<Derived>` inside a CRTP base — which does not compile at C++03 idiom level |
| GAP-AA2 (JNI) | `ref-brownfield-survival.md` | **YES — CRITICAL** | JNI code is inherently C-like; all examples must use raw pointers, C arrays, no std::string (use `std::string` only at the boundary), no lambdas in callbacks |
| GAP-AA3 (MFC) | `ref-brownfield-survival.md` | **YES — by definition** | MFC patterns are C++03; all `CObject`-derived classes, `CString`, message-map macros. No smart pointers in MFC class members. |
| GAP-CG3 (Rule of Zero/Five) | additions to `ref-core-language.md` | **YES — CRITICAL** | In C++03 idiom the "Rule of Three" applies (no move constructor, no move assignment). Must show `Rule of Three` before `Rule of Five` with `★ C++11` on move operations. Without this, Copilot generates `= default` move constructors for C++03-style code |
| GAP-CG1 (Interface design, Expects/Ensures) | additions to `ref-core-language.md` | **YES — HIGH** | GSL `Expects()`/`Ensures()` use C++11 `static_assert`-compatible syntax. C++03 idiom equivalent is `BOOST_ASSERT` or raw `assert()`. `not_null<T*>` becomes a hand-rolled typedef/template wrapper. |
| GAP-C4 (Condition variables) | `ENG-6.1-condition-variable.md` | **YES — HIGH** | CWR uses `CRITICAL_SECTION` (Win32) + `pthread_cond_t` (Linux). `std::condition_variable` (C++11) is technically available at C++14 but the `idiom_level: C++03` flag means legacy patterns dominate. Add `★ C++03-POSIX` fallback showing `pthread_cond_wait` + predicate |
| GAP-C7 (False sharing) | `ENG-3.1-false-sharing.md` | **MODERATE** | `alignas(64)` is C++11; C++03 idiom uses `__declspec(align(64))` (MSVC) or `__attribute__((aligned(64)))` (GCC). Add `★ C++98-MSVC` and `★ C++98-GCC` callouts |
| GAP-CG11 (string_view lifetime) | additions to `ref-core-language.md` | **MODERATE** | `std::string_view` (C++17) doesn't exist at C++03 idiom level. Reframe as `const char*` + `std::string` dangling trap — still highly relevant (returning `const char*` to a local `std::string` is the C++03 equivalent anti-pattern) |
| GAP-T2 (Type traits) | `ENG-3.1-type-traits.md` | **LOW** | `std::type_traits` (C++11) not available at C++03. Show `boost::type_traits` as the C++03 equivalent. Do NOT omit — type traits are critical for template code that CWR has today |
| GAP-T4 (Policy-based design) | `ENG-3.1-policy-based-design.md` | **LOW** | Policy-based design predates C++11; C++03 idiom version is just the standard template parameter pattern. No changes needed to make it C++03 compatible — this is naturally C++03 |

### CWR Routing Decision Table

The avatar's `idiom_level: C++03` mechanism fires when CWR's `.copilot/project.yaml` has `idiom_level: "03"`.
The following routing behavior must be validated:

```
Query: "How do I implement CRTP for FlightScheduler policy injection?" in CWR project
Step 1: Detect cpp.standard = "14", idiom_level = "03"
Step 2: Tier = transitional (from standard)
Step 3: Idiom level = C++03 → select C++03 variant of ENG-3.1-crtp.md
Step 4: C++03 variant shows raw pointer CRTP, no unique_ptr, no override
Step 5: Serve WITHOUT C++11 section content (despite project compiling at C++14)
```

This routing path is NOT tested by any existing RAG eval scenario. It requires a dedicated E4 scenario
(see Section 5, tc-ese-005).

---

## Section 3: Tier Coverage Analysis — Who Benefits from ESE

### 3.1 Net New Content per Tier

| Tier | AA LOC% | New files clearly assigned | New ref sections | Benefit level | Gap |
|------|:-------:|:--------------------------:|:----------------:|:-------------:|-----|
| `legacy` (pre-C++98) | ~24% | 0 | 0 | **NONE** | ESE delivers zero new guidance to SPEClient's MSVC 6.0 codebase — the single largest AA C++ LOC segment |
| `brownfield` (C++98/03) | ~11% | 2 (`ENG-3.1-crtp.md`, `ENG-3.1-policy-based-design.md`) | `ref-brownfield-survival.md` + CPL.xx + GSL Profile additions | **MODERATE** | MFC/JNI/FICO Xpress covered; but only if `ref-brownfield-survival.md` is placed in `brownfield.prefer` |
| `transitional` (C++11/14) | **~60%** | 6 (`ENG-6.1-memory-ordering.md`, `ENG-6.1-condition-variable.md`, `ENG-6.1-lock-free-intro.md`, `ENG-3.1-type-traits.md`, `ENG-3.1-false-sharing.md`, `ENG-3.1-crtp.md`) | CG1/CG2/CG3/CG4 in `ref-core-language.md`; core concurrency sections | **SIGNIFICANT** | ~30% of all ESE content is transitional-tier usable — which is good but still only 30% for 60% of the LOC |
| `modern` (C++17) | ~5% | 7 (all transitional + `ENG-6.1-parallel-algorithms.md`) | Parallel algorithms, jthread alternatives, `★ C++17` concurrency | **GOOD** | Parallel algorithms is the primary new value for C++17 |
| `greenfield` (C++20/23) | **~0%** | **11 new C++20 example files** + 2 new ref files | All GAP-20-* coverage | **ENORMOUS** | Applies to near-zero current AA LOC |

### 3.2 Critical Finding: 95% LOC Underserved by Majority of ESE Content

Of the 20 deliverable files in ESE:
- **11 files** are `cpp_version_min: 20` → serve `greenfield` only (~0% of AA LOC)
- **6 files** are `cpp_version_min: 11` → serve `transitional` / `modern` / `greenfield` (~65% of AA LOC)
- **2 files** are `cpp_version_min: 98` → serve all tiers including `brownfield` / `legacy` (~95% of AA LOC)
- **1 file** is `cpp_version_min: 17` → serves `modern` / `greenfield` (~5% of AA LOC)

The proposal allocates approximately 55% of its new artifacts to the greenfield tier that represents ~0% of
current production LOC. The R6 critique that "the ratio should be inverted" is validated by this routing
analysis: even after the Brownfield Survival Pack amendment, the proposal remains approximately:
- **55% greenfield content** (serves ~0% of current AA LOC)
- **30% transitional content** (serves ~60% of current AA LOC)
- **10% brownfield content** (serves ~11% of current AA LOC)
- **5% neither** (governance wiring)

### 3.3 `legacy` Tier: No New Content — Structural Gap

The `legacy` tier (SPEClient, pre-C++98, MSVC 6.0 `.dsp` era, ~24% of AA LOC) receives nothing
from the ESE proposal. The `ref-brownfield-survival.md` covers C++98/03 patterns (CRITICAL_SECTION,
RCPtr, MFC) — but SPEClient predates C++98. The characterization testing gap (GAP-AA1) is
conceptually applicable to legacy code but requires a pre-C++98 test harness note.

**Required amendment**: Add `ref-brownfield-survival.md` to `legacy.prefer` with the following
section-level restriction: Section "Characterization Testing" applies to all tiers; sections
"MFC Integration", "FICO Xpress", "RCPtr Migration" carry a `★ C++98` marker indicating
they require at minimum C++98-era toolchain capability.

### 3.4 `transitional` Tier: Routing Gap for New C++20 Content

The `transitional` tier `avoid` list currently contains only `examples/ENG-3.7-error-handling.md`.
After ESE, 11 new C++20 example files exist. Without explicit `avoid` entries, the conservative
default rule ("warn; do not silently serve") cannot fire — the routing system has no instruction
to suppress these files for C++14 developers. **This is a silent failure mode**: a CWR developer
asking "how do I do formatted output?" may receive `ENG-6.1-std-format.md` (C++20 std::format)
instead of `ref-io-formatting.md` (fmtlib/spdlog for C++14), with no warning.

---

## Section 4: Required AVATAR-RAG-INDEX.yaml Changes

All changes below must be made in a single structured amendment. No ESE task may begin without
these changes being planned (they may be implemented during Phase 0 governance wiring).

### 4.1 New `refs_inventory` Entries

```yaml
# Add to cpp.files.reference_files list:
- refs/language/ref-cpp20-core.md (~2400t)      — Modules, Ranges/Views, span, spaceship, format, bit_cast ★ C++20+
- refs/language/ref-cpp20-runtime.md (~2400t)   — source_location, constinit, atomic_ref, coroutine generators, Calendar, lambda improvements ★ C++20+
- refs/safety/ref-concurrency-advanced-core.md (~2400t)   — memory ordering, lock-free basics, false sharing, condition vars, promise/future, CP.42/43/50 ★ C++11+
- refs/safety/ref-concurrency-advanced-modern.md (~2200t) — parallel algorithms, jthread/stop_token, CP.51/52/53, hazard pointers, atomic_ref ★ C++17/C++20+
- refs/legacy/ref-brownfield-survival.md (~2600t) — JNI thread safety, MFC integration, FICO Xpress, RCPtr migration, characterization testing ★ C++98+
```

### 4.2 Tier `prefer` List Additions

```yaml
version_routing_policy:
  by_standard:
    legacy:
      prefer:
        - refs/legacy/ref-brownfield-survival.md    # NEW — characterization testing applies to all legacy tiers
    brownfield:
      prefer:
        - refs/legacy/ref-brownfield-survival.md    # NEW — primary ESE value delivery for brownfield
        - examples/ENG-3.1-crtp.md                 # NEW — cpp_version_min: 98; CRTP is C++98-viable
        - examples/ENG-3.1-policy-based-design.md  # NEW — policy-based design predates C++11
    transitional:
      prefer:
        - refs/safety/ref-concurrency-advanced-core.md    # NEW — C++11 memory ordering, lock-free, false sharing
        - examples/ENG-6.1-memory-ordering.md             # NEW — cpp_version_min: 11
        - examples/ENG-6.1-condition-variable.md          # NEW — cpp_version_min: 11
        - examples/ENG-6.1-lock-free-intro.md             # NEW — cpp_version_min: 11 (C++20 section gated by ★)
        - examples/ENG-3.1-type-traits.md                 # NEW — cpp_version_min: 11
        - examples/ENG-3.1-false-sharing.md               # NEW — cpp_version_min: 11
    modern:
      prefer:
        - refs/safety/ref-concurrency-advanced-core.md    # NEW
        - refs/safety/ref-concurrency-advanced-modern.md  # NEW — C++17 parallel algorithms + jthread
        - examples/ENG-6.1-parallel-algorithms.md         # NEW — cpp_version_min: 17
        - examples/ENG-6.1-memory-ordering.md             # NEW (inherits from transitional)
        - examples/ENG-6.1-condition-variable.md          # NEW (inherits from transitional)
    greenfield:
      prefer:
        - refs/language/ref-cpp20-core.md                 # NEW
        - refs/language/ref-cpp20-runtime.md              # NEW
        - refs/safety/ref-concurrency-advanced-modern.md  # NEW — C++20 jthread, hazard pointers
        - examples/ENG-3.1-ranges-views.md                # NEW
        - examples/ENG-3.1-modules.md                     # NEW
        - examples/ENG-3.2-spaceship-operator.md          # NEW
        - examples/ENG-5.5-source-location.md             # NEW
        - examples/ENG-3.1-coroutine-generators.md        # NEW
        - examples/ENG-6.1-std-format.md                  # NEW
        - examples/ENG-6.1-span-bounds-safety.md          # NEW
        - examples/ENG-6.1-jthread-stop-token.md          # NEW
        - examples/ENG-3.1-constinit.md                   # NEW
```

### 4.3 Tier `avoid` List Additions

```yaml
    legacy:
      avoid:
        # (existing entries kept)
        - examples/ENG-6.7-audit-trail.md
        - examples/ENG-3.7-error-handling.md
        - examples/ENG-2.1-aggregates.md
        # NEW — all C++11+ content:
        - examples/ENG-6.1-memory-ordering.md         # requires C++11 std::atomic
        - examples/ENG-6.1-condition-variable.md      # requires C++11 std::condition_variable
        - examples/ENG-6.1-lock-free-intro.md         # requires C++11 std::atomic
        - examples/ENG-3.1-type-traits.md             # requires C++11 <type_traits>
        - examples/ENG-3.1-false-sharing.md           # requires C++11 alignas
        - examples/ENG-6.1-parallel-algorithms.md     # requires C++17
        - examples/ENG-6.1-std-format.md              # requires C++20
        - examples/ENG-6.1-span-bounds-safety.md      # requires C++20
        - examples/ENG-6.1-jthread-stop-token.md      # requires C++20
        - examples/ENG-3.1-ranges-views.md            # requires C++20
        - examples/ENG-3.1-modules.md                 # requires C++20 + CMake 3.28+
        - examples/ENG-3.1-coroutine-generators.md    # requires C++20
        - examples/ENG-3.2-spaceship-operator.md      # requires C++20
        - examples/ENG-5.5-source-location.md         # requires C++20
        - examples/ENG-3.1-constinit.md               # requires C++20
        - refs/language/ref-cpp20-core.md             # requires C++20
        - refs/language/ref-cpp20-runtime.md          # requires C++20
        - refs/safety/ref-concurrency-advanced-modern.md  # requires C++17/20

    brownfield:
      avoid:
        # (existing entries kept)
        - examples/ENG-6.7-audit-trail.md
        - examples/ENG-3.7-error-handling.md
        # NEW — C++17+ content not available in C++98/03:
        - examples/ENG-6.1-parallel-algorithms.md     # requires C++17
        - examples/ENG-6.1-std-format.md              # requires C++20
        - examples/ENG-6.1-span-bounds-safety.md      # requires C++20
        - examples/ENG-6.1-jthread-stop-token.md      # requires C++20
        - examples/ENG-3.1-ranges-views.md            # requires C++20
        - examples/ENG-3.1-modules.md                 # requires C++20 + CMake 3.28+
        - examples/ENG-3.1-coroutine-generators.md    # requires C++20
        - examples/ENG-3.2-spaceship-operator.md      # requires C++20
        - examples/ENG-5.5-source-location.md         # requires C++20
        - examples/ENG-3.1-constinit.md               # requires C++20
        - refs/language/ref-cpp20-core.md             # requires C++20
        - refs/language/ref-cpp20-runtime.md          # requires C++20
        - refs/safety/ref-concurrency-advanced-modern.md  # requires C++17/20 (parallel algorithms)

    transitional:
      avoid:
        # (existing entries kept)
        - examples/ENG-3.7-error-handling.md
        # NEW — C++17+ content not available in C++11/14:
        - examples/ENG-6.1-parallel-algorithms.md     # requires C++17 std::execution
        - examples/ENG-6.1-std-format.md              # requires C++20 (use fmtlib for C++14)
        - examples/ENG-6.1-span-bounds-safety.md      # requires C++20 (use gsl::span for C++14)
        - examples/ENG-6.1-jthread-stop-token.md      # requires C++20
        - examples/ENG-3.1-ranges-views.md            # requires C++20 (use range-v3 for C++14)
        - examples/ENG-3.1-modules.md                 # requires C++20 + CMake 3.28+; ACTIVELY HARMFUL in CWR
        - examples/ENG-3.1-coroutine-generators.md    # requires C++20
        - examples/ENG-3.2-spaceship-operator.md      # requires C++20
        - examples/ENG-5.5-source-location.md         # requires C++20 (use __FILE__/__LINE__ macros)
        - examples/ENG-3.1-constinit.md               # requires C++20
        - refs/language/ref-cpp20-core.md             # requires C++20
        - refs/language/ref-cpp20-runtime.md          # requires C++20

    modern:
      avoid:
        # (existing entries kept)
        - examples/ENG-3.7-error-handling.md
        # NEW — C++20+ content not available in C++17:
        - examples/ENG-6.1-jthread-stop-token.md      # requires C++20 (use std::thread + stop_flag)
        - examples/ENG-3.1-modules.md                 # requires C++20 + CMake 3.28+
        - examples/ENG-3.1-coroutine-generators.md    # requires C++20
        - examples/ENG-3.2-spaceship-operator.md      # requires C++20
        - examples/ENG-5.5-source-location.md         # requires C++20
        - examples/ENG-3.1-constinit.md               # requires C++20
        - refs/language/ref-cpp20-core.md             # requires C++20
        - refs/language/ref-cpp20-runtime.md          # requires C++20
```

### 4.4 New `search_queries` Entries

Add to the `cpp.search_queries` list:

```yaml
# ESE concurrency additions (transitional-tier queries — highest value for AA LOC)
- C++ memory ordering acquire release seq_cst C++11 atomic? → refs/safety/ref-concurrency-advanced-core.md (~2400t)
- C++ condition variable wait with predicate spurious wakeup? → examples/ENG-6.1-condition-variable.md
- C++ lock-free data structure ABA problem atomic? → examples/ENG-6.1-lock-free-intro.md
- C++ false sharing cache line alignas? → examples/ENG-3.1-false-sharing.md
- C++ type traits is_trivially_copyable decay_t? → examples/ENG-3.1-type-traits.md
# ESE brownfield-survival additions
- C++ JNI thread safety AttachCurrentThread CrewWatchSolver? → refs/legacy/ref-brownfield-survival.md (~2600t)
- C++ MFC CObject RAII smart pointer integration? → refs/legacy/ref-brownfield-survival.md (~2600t)
- C++ FICO Xpress solver thread safety XPRSprob? → refs/legacy/ref-brownfield-survival.md (~2600t)
- C++ characterization test pinning test legacy? → refs/legacy/ref-brownfield-survival.md + examples/ENG-4.1-characterization-test-pattern.md
- C++ RCPtr migration to shared_ptr legacy? → refs/legacy/ref-brownfield-survival.md (~2600t)
# ESE C++20 additions (greenfield-only queries)
- C++ ranges views filter transform pipeline C++20? → refs/language/ref-cpp20-core.md (~2400t)
- C++ modules import export C++20 CMake? → examples/ENG-3.1-modules.md (greenfield ONLY)
- C++ std::format custom formatter C++20? → examples/ENG-6.1-std-format.md
- C++ spaceship operator three-way comparison C++20? → examples/ENG-3.2-spaceship-operator.md
- C++ std::span bounds safety non-owning view C++20? → examples/ENG-6.1-span-bounds-safety.md
- C++ jthread stop_token cooperative cancellation C++20? → examples/ENG-6.1-jthread-stop-token.md
- C++ parallel algorithms execution policy par_unseq C++17? → examples/ENG-6.1-parallel-algorithms.md
# ESE C++20 additions (greenfield-only, advanced)
- C++ coroutine generator co_yield lazy sequence C++20? → examples/ENG-3.1-coroutine-generators.md
- C++ source_location structured logging C++20? → examples/ENG-5.5-source-location.md
- C++ constinit init order fiasco prevention C++20? → examples/ENG-3.1-constinit.md
# ESE templates/patterns additions
- C++ CRTP static polymorphism mixin curiously recurring? → examples/ENG-3.1-crtp.md
- C++ policy-based design compile-time strategy injection? → examples/ENG-3.1-policy-based-design.md
```

---

## Section 5: RAG Eval Harness — New Scenarios Required

**Current state:** 30 scenarios, 100% pass rate (4 metrics: routing_accuracy, tier_version_safety,
answer_coverage, no_ungated_leakage).

**Minimum new scenarios required:** 20 (revised upward from original R4 requirement of ≥15,
per R4-OSS-RESPONSE.md).

All new scenarios must be added to `tools/rag-eval/test-cases/cpp-c++20.yaml` (ESE-00.4).

### 5.1 New Scenarios Table

| ID | Query | Project tier | Expected routing | `must_not_retrieve` | Risk |
|----|-------|:------------:|------------------|---------------------|:----:|
| tc-ese-001 | "C++14 project: how do I safely format a string for logging?" | transitional | `ref-io-formatting.md` (fmtlib/spdlog) | `ENG-6.1-std-format.md` | 🔴 |
| tc-ese-002 | "C++14 project: thread-safe producer-consumer queue" | transitional | `ENG-6.1-condition-variable.md` | `ENG-6.1-jthread-stop-token.md`, `ENG-3.1-ranges-views.md` | 🔴 |
| tc-ese-003 | "C++98 project: how do I handle concurrent access to shared data?" | brownfield | `ref-concurrency-brownfield.md` | `ref-concurrency-advanced-core.md`, `ENG-6.1-lock-free-intro.md` | 🔴 |
| tc-ese-004 | "C++14 CWR project: how do I implement CRTP for a policy-injected solver?" | transitional + idiom_level:03 | `ENG-3.1-crtp.md` C++03-idiom variant | `ENG-6.1-jthread-stop-token.md`, `ENG-3.1-ranges-views.md`, any C++11 `unique_ptr` CRTP example | 🔴 |
| tc-ese-005 | "C++14 project: should I use C++20 Modules for my service?" | transitional | Warning: Modules require C++20 + CMake 3.28+; suggest `ref-build-toolchain.md` instead | `ENG-3.1-modules.md` must NOT be silently served | 🔴 |
| tc-ese-006 | "What lock-free data structure should I use in C++14?" | transitional | `ENG-6.1-lock-free-intro.md` with C++11 atomic section only | `★ C++20` hazard_pointer section must be gated (no_ungated_leakage metric) | 🔴 |
| tc-ese-007 | "C++17 project: parallel processing of flight data arrays" | modern | `ENG-6.1-parallel-algorithms.md` | `ENG-3.1-ranges-views.md` (C++20 ranges, not C++17) | 🟠 |
| tc-ese-008 | "C++20 project: import a module in CMake" | greenfield | `ENG-3.1-modules.md` | `ref-brownfield-survival.md`, `ref-legacy-navigation.md` | 🟠 |
| tc-ese-009 | "C++14 project: spaceship operator for FlightId comparison" | transitional | Warning: `<=>` requires C++20; recommend manual `bool operator<` pattern | `ENG-3.2-spaceship-operator.md` must NOT be silently served | 🔴 |
| tc-ese-010 | "C++98 project: shared_ptr lifecycle for CObject-derived class" | brownfield | `ref-brownfield-survival.md` MFC section | `ref-core-language-fundamentals.md` Rule of Five (move semantics, C++11) | 🟠 |
| tc-ese-011 | "C++14 project: cache line false sharing in concurrent scheduler" | transitional | `ENG-3.1-false-sharing.md` | — | 🟡 |
| tc-ese-012 | "What OSS license is the lock-free C++ content derived from?" | any | `oss-reference-registry.yaml` | `ENG-6.1-lock-free-intro.md` (OSS metadata query, not programming query) | 🟠 |
| tc-ese-013 | "C++14 CWR: JNI AttachCurrentThread lifecycle for CrewWatchSolverJNI" | transitional + idiom_level:03 | `ref-brownfield-survival.md` JNI section | `ENG-6.1-jthread-stop-token.md` (jthread is C++20; JNI query should NOT route to modern concurrency) | 🔴 |
| tc-ese-014 | "C++20 project: ranges views filter transform flight legs pipeline" | greenfield | `ref-cpp20-core.md` + `ENG-3.1-ranges-views.md` | `ENG-6.1-memory-ordering.md`, `ref-concurrency-advanced-core.md` | 🟠 |
| tc-ese-015 | "C++14 project: policy-based design for configurable fare calculator" | transitional | `ENG-3.1-policy-based-design.md` | C++20 concepts-based alternatives in policy-based file (must be gated by ★) | 🟡 |
| tc-ese-016 | "C++14 project: Rule of Five for RCPtr wrapper" | transitional | `ref-core-language-fundamentals.md` Rule of Three/Five section with C++03 idiom variant | `★ C++11` move constructor section must be presented as optional migration | 🟠 |
| tc-ese-017 | "C++17 project: std::source_location for structured logging" | modern | Warning: `std::source_location` requires C++20; recommend `__FILE__`/`__LINE__` macros or spdlog | `ENG-5.5-source-location.md` must NOT be silently served to C++17 project | 🔴 |
| tc-ese-018 | "C++20 project: co_yield generator for lazy fare calculation sequence" | greenfield | `ENG-3.1-coroutine-generators.md` | `ref-safety-jni-abi.md` (coroutine query must not match JNI suspension rules from CP.51) | 🟠 |
| tc-ese-019 | "Unknown standard project: how do I safely handle concurrent access?" | unknown (legacy-safe) | Prompt user for C++ standard before serving any `★`-gated content | No version-gated content served without confirmation | 🟠 |
| tc-ese-020 | "C++14 project: constinit for global scheduler state" | transitional | Warning: `constinit` requires C++20; recommend `constexpr` for compile-time init or `std::once_flag`/`std::call_once` for lazy | `ENG-3.1-constinit.md` must NOT be silently served | 🟡 |

### 5.2 Highest-Risk Scenarios

In priority order, the scenarios most likely to route to the wrong tier and cause production harm:

1. **tc-ese-001** — `std::format` served to C++14 developer asking for "safe string formatting."
   Semantic similarity is HIGH (both are "safe C++ formatting"); version gate is the ONLY discriminator.
   This is the exact silent failure mode the routing system was built to prevent.

2. **tc-ese-009** — `<=>` spaceship operator served to C++14 developer. Value type comparison is a
   common query; the spaceship operator example looks authoritative; C++14 developer applies it;
   code silently fails to compile on GCC 9 / Clang 12.

3. **tc-ese-005** — C++20 Modules example served to C++14 CWR developer. Modules require CMake 3.28+.
   CWR builds with `nbproject/Makefile-CI-Release.mk` from 2015. This would break the CWR build
   completely and silently.

4. **tc-ese-013** — `ENG-6.1-jthread-stop-token.md` (C++20) served in response to a JNI thread
   safety query for a C++14/idiom_level:C++03 project. "JNI thread" and "jthread" share vocabulary;
   the version gate is the only discriminator. A developer applying jthread semantics to JNI callbacks
   produces `JNIEnv*` threading errors — `CrewWatchSolverJNI.cpp` risk identified by R6.

5. **tc-ese-017** — `std::source_location` served to C++17 project. The query is a natural successor
   to the ENG-5.5 observability law; C++17 developers expect C++17 answers; serving C++20 content
   silently creates compile failures.

---

## Section 6: Blocking Issues and Required PROPOSAL.md Amendments

### 6.1 New Blocking Issues (Version-Routing Specific)

The following blocking issues are **in addition to** the 4 original R4 blocking issues and 4 OSS-response
blocking issues documented in R4-OSS-RESPONSE.md. Running total: **9 R4 blocking issues.**

---

**NEW BLOCKING Issue 5 — Zero `cpp_version_min` Assignments for Any ESE Deliverable**

Every ref file and example file added under ESE will be auto-discovered by
`test_phase2d_c4_ref_frontmatter.py`. This test validates `cpp_version_min` frontmatter on ALL files in
`refs/**/*.md` and `examples/**/*.md`. Any new file added without this frontmatter will FAIL the test suite
immediately. More critically: without `cpp_version_min`, the routing system cannot apply the conservative
default rule (warn; do not silently serve). Files without this metadata are served to ALL tiers
indiscriminately, including the exact version-mismatch scenarios that PR #47 was built to prevent.

**Required PROPOSAL.md amendment:** Add a `cpp_version_min` column to the "New Reference Files",
"Enhanced Reference Files", and "New Example Files" tables. Every row must carry an explicit value.
The values in Section 1 of this review represent the required assignments.

---

**NEW BLOCKING Issue 6 — No Tier Routing Placements for Any ESE Deliverable**

The "Proposed Deliverables" section in PROPOSAL.md has three tables (new ref files, enhanced ref
files, new example files) with NO column for tier placement. Files not placed in any tier's `prefer`
list are reachable only via semantic similarity. With `top_k: 3`, this means:

- A C++20 file not in `greenfield.prefer` competes for top_k slots with every other C++ file
- A C++14-appropriate file not in `transitional.prefer` may lose to semantically similar but
  version-inappropriate alternatives
- The conservative default rule cannot fire for specific files — it only fires on `cpp_version_min`
  mismatches detected at content-filter time (Step 4 in the routing flow), NOT at Step 2

**Required PROPOSAL.md amendment:** Add a "Tier routing" column to all deliverable tables with
explicit `prefer` and `avoid` assignments per the values in Section 4 of this review.

---

**NEW BLOCKING Issue 7 — File Size Violations at Creation Time**

The following proposed files violate the ≤2,800t ceiling **before content is even written**:
- `ref-concurrency-advanced.md` (projected ~5,600t including OSS overhead) — exceeds ceiling by 100%
- `ref-cpp20-features.md` (projected ~6,300t including OSS overhead) — exceeds ceiling by 125%

Additionally, two existing files already exceed the ceiling and must be split BEFORE ESE content is added:
- `ref-advanced-cpp.md` (~5,040t today) — must be split before CRTP/type-traits sections are added
- `ref-core-language.md` (~4,769t today) — must be split before CG1/CG2/CG3 sections are added

These are pre-commit violations. The `test_phase2d_e3_token_automation.py` token automation test will
detect them, but only after the file is created. **The split decisions must be made NOW in the proposal,
not detected at test time.**

**Required PROPOSAL.md amendment:** Replace the single-file entries with their split equivalents in
all deliverable tables. Update affected task entries in `tasks.md` accordingly.

---

**NEW BLOCKING Issue 8 — GAP-C5 Version-Split Decision Undeclared**

The proposal lists `ref-concurrency-advanced.md` as a single file covering "memory ordering deep dive,
lock-free, thread pools/work-stealing, parallel algorithms, false sharing, condition variables, jthread/
stop_token, promise/future, CP.42/43/50/51/52/53." This single file covers a span from C++11 to C++20
(parallel algorithms are C++17; jthread is C++20; hazard_pointer is C++20). The proposal makes no
declaration about:

1. Which sections carry `★ C++NN` markers
2. Whether the file is split by version boundary or kept as multi-version
3. Which `prefer` and `avoid` lists each section or sub-file appears in

Without this declaration, the 60% of AA LOC in the `transitional` tier (C++14) will encounter
C++20 content (`std::jthread`, `std::hazard_pointer`) within the same file they receive for
"memory ordering" queries. The `no_ungated_leakage` RAG eval metric WILL catch this — but only
after the file has been incorrectly written.

**Required PROPOSAL.md amendment:** Declare the explicit split of `ref-concurrency-advanced.md`
into `ref-concurrency-advanced-core.md` (`cpp_version_min: 11`) and
`ref-concurrency-advanced-modern.md` (`cpp_version_min: 17`) as documented in Section 1.2 of
this review.

---

**NEW BLOCKING Issue 9 — `transitional.avoid` and `brownfield.avoid` Not Extended for C++20 Content**

The `transitional.avoid` list currently contains a single entry: `examples/ENG-3.7-error-handling.md`.
After ESE, there will be 11+ new C++20 example files and 2 new C++20 ref files in the avatar. None of
them are designated for `transitional.avoid` in the proposal. The conservative default rule
("warn; do not silently serve") requires the explicit `avoid` entry to fire the warning — without it,
C++20 content is served to C++14 developers without any version gate warning.

**This is the highest-impact routing defect in the ESE proposal.** The entire purpose of PR #47 was to
prevent the silent failure mode of C++20 content reaching C++14 developers. ESE adds 13 new C++20
artifacts without any `avoid` list entries, recreating the pre-PR-#47 routing behavior for all new
content.

**Required PROPOSAL.md amendment:** Add a governance wiring task in Phase 0 that explicitly extends
all tier `avoid` lists per Section 4.3 of this review, BEFORE any Phase 1 task begins.

---

### 6.2 Required `tasks.md` Amendments

In addition to PROPOSAL.md changes, the following task-level changes are required:

| Amendment | Task | Required Change |
|-----------|------|-----------------|
| Version routing | ESE-01 | Add to acceptance criteria: "Each new file MUST include valid `cpp_version_min` frontmatter (verified by `test_phase2d_c4_ref_frontmatter.py`)" |
| Tier routing | ESE-01 | Add to acceptance criteria: "Each new file MUST appear in at least one tier `prefer` list in AVATAR-RAG-INDEX.yaml" |
| Token enforcement | ESE-01 | Add to acceptance criteria: "No new or modified ref file may exceed 2,800t (`test_phase2d_e3_token_automation.py` must pass)" |
| File splits | New task (Phase 0) | Split `ref-advanced-cpp.md` BEFORE ESE CRTP/type-traits additions — add as Phase 0 task |
| File splits | New task (Phase 0) | Split `ref-core-language.md` BEFORE ESE CG1/CG2/CG3 additions — add as Phase 0 task |
| CWR idiom variants | ESE-19 (CRTP) | Add: "Provide C++03-idiom variant of CRTP examples for `idiom_level: C++03` routing — raw pointers, no `override`, no `unique_ptr`" |
| CWR idiom variants | Brownfield survival tasks | Add: "All JNI and MFC examples must use C++03 idioms (no lambdas, no std::function, no std::unique_ptr in MFC classes)" |
| Avoid list wiring | New Phase 0 task | "Extend `transitional.avoid`, `brownfield.avoid`, `legacy.avoid` in AVATAR-RAG-INDEX.yaml with all new C++20 files per R4-VERSION-REVIEW.md Section 4.3 BEFORE Phase 1 begins" |
| RAG eval harness | ESE-00.4 | Expand to ≥20 new scenarios per Section 5 of this review; include all tc-ese-001 through tc-ese-020 scenarios |

---

## Updated R4 Verdict

**Severity: 🔴 BLOCKED — 9 blocking issues total (4 original + 4 from OSS response + 5 new version-routing)**

The ESE proposal is architecturally unsound from a version-routing perspective as currently written.
It would, upon execution, recreate the exact class of silent routing failures that PR #47 was built to
eliminate — but for an even larger set of files (20 new artifacts, all without routing assignments).

The content quality, copyright framework, and brownfield reorientation are all commendable. The routing
architecture is completely absent. A proposal that adds 13 C++20 example files with no `avoid` list
entries for the tiers occupied by 95% of AA's C++ production codebase is not a partial gap — it is a
complete absence of version governance for all new content.

**Amendment priority order:**

1. **Today** — Declare explicit `cpp_version_min` for every deliverable (Section 1 provides the values)
2. **Today** — Declare explicit tier routing placements (Section 4 provides the YAML)
3. **Today** — Declare file splits for `ref-concurrency-advanced.md` and `ref-cpp20-features.md`
4. **Before Phase 1** — Implement Phase 0 task: extend `avoid` lists for all new C++20 content
5. **Before Phase 1** — Retroactively split `ref-advanced-cpp.md` and `ref-core-language.md`
6. **Before Phase 1** — Specify C++03-idiom variants for the 5 critical CWR scenario gaps
7. **Before Phase 1** — Add ≥20 RAG eval scenarios to `cpp-c++20.yaml` (ESE-00.4 expanded scope)

Once these amendments are in place, the version routing system will correctly serve the ESE content
to version-appropriate developers. The 95% of AA C++ LOC in legacy/brownfield/transitional tiers
will receive only version-compatible guidance, and the 5-tier routing investment of PR #47/#48 will
extend to cover all new ESE deliverables.

---

*R4 — RAG Expert: Version-Sensitivity Review completed 2026-07-15.*
*Governs routing architecture for ESE-* under the five-tier version routing system (PR #47/#48).*
*Prior R4 findings remain in force: R4-OSS-RESPONSE.md (4 blocking issues from OSS analysis).*
*This review adds 5 new blocking issues specific to the version-routing integration.*

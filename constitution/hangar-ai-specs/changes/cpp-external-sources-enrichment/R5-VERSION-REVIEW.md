# R5 — C++ Master: Version-Sensitivity Review of ESE Proposal

**Reviewer:** R5 — C++ Master (20+ years; standards committee contributor)
**Review Date:** 2026-07-22
**Scope:** ESE proposal (`cpp-external-sources-enrichment`) evaluated through the lens of the
newly-implemented 5-tier version-sensitive routing system.
**Prior Reviews:** REVIEW-PANEL.md §R5 (original), R5-OSS-RESPONSE.md (post-OSS)
**Routing System Reference:** `docs/guides/avatars/cpp-version-sensitive-routing.md`

---

## Executive Finding

> **⚠️ NOT SAFE TO IMPLEMENT AS-IS FROM A VERSION-CORRECTNESS STANDPOINT.**
>
> The ESE proposal will introduce new version-routing hazards beyond those already flagged
> in prior reviews. The 5-tier routing system is technically sound and correctly implemented.
> The problem is that the ESE deliverables, as currently specified, are not structured to
> integrate with it safely. Fifteen of the forty-five gaps require decisions the proposal has
> not made: which content goes in which tier, what `cpp_version_min` frontmatter applies,
> and which gaps require genuinely separate files for different standards vs. callouts within
> a single file.
>
> The three prior blocking issues (false lock-free claim, hallucinated CVE, missing
> string_view traps) remain. The version-routing dimension adds new blockers:
>
> 1. **GAP-20-11 (FAR 117 timezone)** has no C++14 fallback path — the 60% of AA C++ LOC
>    running on CWR/IOC_ALP cannot access this content at all as currently specified.
>    This is not a cosmetic omission. FAR 117 is a legal obligation.
>
> 2. **GAP-CG11 (string_view lifetime)** has an incorrect implied `cpp_version_min`.
>    `std::string_view` is a C++17 feature. If this content is assigned `cpp_version_min: 14`,
>    it will be routed to every C++14 project in AA's portfolio — where it cannot compile.
>
> 3. **`bshoshany/thread-pool`** (the OSS source designated for GAP-C6) requires C++17 minimum
>    and uses `std::jthread`/`std::counting_semaphore`. It must not be routed to the
>    `transitional` tier (C++11/14) under any circumstances.
>
> 4. **Twelve gaps** need explicit version-split decisions before implementation tasks execute.
>    The current proposal leaves this ambiguous, guaranteeing inconsistent `cpp_version_min`
>    values across the new reference files.
>
> **The routing system cannot protect against incorrect `cpp_version_min` frontmatter.**
> The test suite validates that frontmatter *exists*; it does not validate that the declared
> version is technically correct. R5 is identifying the values that must be correct before
> the tests become meaningful.

---

## Section 1: Version Requirements per Gap

Legend for "Split Required" column:
- ✂️ = Separate content per version tier required (substantively different approaches)
- 📌 = Single file with `★ C++NN` callouts sufficient

### Concurrency Gaps (GAP-C1 – GAP-C10)

| Gap | Min Standard | C++11/14 Fallback Exists? | `cpp_version_min` | Split Required | Misrouting Risk |
|-----|-------------|--------------------------|-------------------|----------------|-----------------|
| GAP-C1 Memory ordering | C++11 | N/A — IS C++11 content | **11** | 📌 callout for C++20 `atomic::wait` | 🟡 LOW — C++98 teams get irrelevant content; routing must gate at `brownfield` |
| GAP-C2 Parallel algorithms | C++17 | C++14: `std::async` + `std::launch::async`; OpenMP | **17** | ✂️ **SPLIT REQUIRED** — C++14 alternative section needed; `par_unseq` TBB linkage trap must be in a separate modern-only section | 🔴 HIGH — `par_unseq` silently falls back to sequential without TBB; compile succeeds, correctness fails |
| GAP-C3 `std::jthread` / `stop_token` | C++20 | C++11: `std::thread` + `std::atomic<bool>` stop flag | **20** | ✂️ **SPLIT REQUIRED** — C++11 stop-flag idiom and C++20 jthread are substantively different patterns, not a syntax upgrade | 🔴 HIGH — `bshoshany/thread-pool` (OSS source) requires C++17 minimum; must not reach `transitional` tier |
| GAP-C4 Condition variable patterns | C++11 | N/A — IS C++11 content | **11** | 📌 callout for C++20 `std::atomic::wait` + `std::semaphore` | 🟢 LOW |
| GAP-C5 Lock-free data structures | C++11 | N/A — IS C++11 content (`std::atomic`) | **11** | 📌 callout for C++20 `std::atomic_ref` (separate section ★ C++20) | 🔴 HIGH — the `std::atomic<shared_ptr<T>>` content (part of this gap) requires C++20; if incorrectly placed in the C++11 section, the false lock-free claim becomes a version-leakage incident |
| GAP-C6 Thread pool / work-stealing | C++11 (manual); C++17 (bshoshany) | C++11: manual `std::thread` + CV + `atomic<bool>` | **11** (base); ★ C++17 section | ✂️ **SPLIT REQUIRED** — C++11 manual pool and C++17/20 jthread-native pool are different implementations; `bshoshany/thread-pool` (OSS source) is C++17 minimum, must be section-gated | 🔴 HIGH — `bshoshany` content routed to C++14 will not compile |
| GAP-C7 False sharing / alignas | C++11 | N/A — IS C++11 content (`alignas`) | **11** | 📌 callout: `std::hardware_destructive_interference_size` is ★ C++17 | 🟢 LOW |
| GAP-C8 `std::promise` / `std::future` | C++11 | N/A — IS C++11 content | **11** | 📌 callout for C++20 `std::latch`, `std::barrier` | 🟢 LOW |
| GAP-C10 CP.51/52/53 (lambdas + coroutines) | C++20 (coroutine rules) | C++11: lambda capture-by-ref in threads is still dangerous but governed differently | **20** | ✂️ **SPLIT REQUIRED** — CP.51 (don't capture this in coroutines) is meaningless without coroutines; serving it to C++14 creates confusion; a separate C++11-applicable rule about lambda capture in threads must be extracted | 🔴 HIGH — CP.52 "don't hold locks across suspension points" is irrelevant in C++14; serving it causes incorrect refactoring decisions |

### Template Gaps (GAP-T1 – GAP-T7)

| Gap | Min Standard | C++11/14 Fallback Exists? | `cpp_version_min` | Split Required | Misrouting Risk |
|-----|-------------|--------------------------|-------------------|----------------|-----------------|
| GAP-T1 CRTP | C++11 (idiomatic); C++98 (pattern) | N/A — IS pre-C++11 content | **11** | ✂️ **SPLIT REQUIRED** — CRTP is the C++11/14/17 approach; `deducing this` (C++23) supersedes it for mixin use case; must be gated separately to avoid C++23 leakage | 🟡 MEDIUM — if `deducing this` examples bleed into a file with cpp_version_min: 11, greenfield devs will use it and C++14 devs will see inapplicable content |
| GAP-T2 Type traits | C++11 | N/A — IS C++11 content | **11** | 📌 callout: `_t`/`_v` aliases are ★ C++14; `std::void_t` is ★ C++17; concepts replacing traits is ★ C++20 | 🟢 LOW |
| GAP-T3 Tag dispatching | C++11 | N/A — IS C++11 pattern | **11** | 📌 callout: "reading and migrating legacy code only — new code uses `if constexpr` ★ C++17 or concepts ★ C++20" | 🟡 MEDIUM — if routed to greenfield devs without the "legacy only" framing, they will write new tag-dispatch code in 2026 |
| GAP-T4 Policy-based design | C++11 | N/A — IS C++11 content | **11** | 📌 callout: `if constexpr` improvements ★ C++17, concepts constraining policies ★ C++20 | 🟢 LOW |
| GAP-T5 Expression templates | C++98 | N/A — predates C++11 | **11** (modern idiom note) | 📌 callout: "superseded by `std::views` ★ C++20"; reading/brownfield only | 🟡 MEDIUM — teaching expression templates for new code in 2026 is actively harmful |
| GAP-T6 NTTPs | C++98 (integral); C++20 (float/class/string literal) | Integral NTTPs work in C++11+ | **11** (integral); ★ C++20 (float, class, string-literal NTTPs) | ✂️ **SPLIT REQUIRED** — floating-point and class-type NTTPs are C++20 only; a C++14 developer who sees these examples will get confusing compiler errors | 🔴 HIGH — NTTP type restrictions are toolchain-version-sensitive; error messages do not say "requires C++20" clearly |
| GAP-T7 Concepts advanced | C++20 | C++11/14: SFINAE + `std::enable_if` | **20** | ✂️ **SPLIT REQUIRED** — advanced concepts (requires-expressions, subsumption, auto-concept) are C++20 only; SFINAE is the C++11/14 parallel and needs its own documentation for transitional teams | 🔴 HIGH — concepts syntax is a hard compile error on C++14; error messages are cryptic |

### C++20 Feature Gaps (GAP-20-1 – GAP-20-13)

| Gap | Min Standard | C++14 Polyfill Exists? | `cpp_version_min` | Split Required | Misrouting Risk |
|-----|-------------|------------------------|-------------------|----------------|-----------------|
| GAP-20-1 Modules | C++20 + CMake 3.28+ | No polyfill — `#include` is the alternative | **20** | ✂️ **GATE ONLY** — greenfield tier exclusively; hard build-system prerequisite gate must be in frontmatter note | 🚨 CRITICAL — `export module` breaks C++14 builds catastrophically; no graceful degradation |
| GAP-20-2 Ranges/views | C++20 (std::ranges); C++14 (range-v3) | ✅ YES — `ericniebler/range-v3` works on C++14 | **14** (range-v3 section); ★ C++20 (std::ranges section) | ✂️ **SPLIT REQUIRED** — range-v3 namespace (`ranges::`) differs from std::ranges namespace (`std::ranges::`) and adapter composition semantics differ subtly; a combined file without explicit labeling creates confusion | 🔴 HIGH — `std::views::filter` on C++17 is a hard compile failure; range-v3 compiles on C++14 |
| GAP-20-3 `std::format` | C++20 (std::format); C++11 ({fmt}) | ✅ YES — `fmtlib/fmt` is a C++11 polyfill | **11** ({fmt} section); ★ C++20 (std::format section) | ✂️ **SPLIT REQUIRED** — both sections belong in the same file but must be clearly labelled; `fmt::format_string<T>` differs from `std::format_string<T>` in edge cases | 🟡 MEDIUM — `std::format` on C++17 fails to compile; `{fmt}` on C++11 works as a drop-in with clear attribution |
| GAP-20-4 Spaceship `<=>` | C++20 | C++11: explicit `operator<` + Boost.Operators | **20** | 📌 callout: C++14 alternative (explicit comparison operators or Boost.Operators) | 🟡 MEDIUM — `<=>` is a hard compile error on C++14; error message is clear |
| GAP-20-5 `std::span` | C++20 (std::span); C++14 (gsl::span) | ✅ YES — Microsoft GSL `gsl::span` works on C++14 | **14** (gsl::span section); ★ C++20 (std::span section) | ✂️ **SPLIT REQUIRED** — gsl::span and std::span have behavioral differences (dynamic extent handling, checked iterator behavior, API surface); combining without explicit labelling creates incorrect usage | 🔴 HIGH — `std::span` on C++14 fails; gsl::span subtly differs; a C++17 developer who reads the C++20 section may think std::span is available and be surprised |
| GAP-20-6 `std::bit_cast` | C++20 | C++11: `std::memcpy` pattern | **20** | 📌 callout: C++14 safe alternative (`memcpy` into a correctly-typed local; not `reinterpret_cast` which is UB) | 🟡 MEDIUM — `std::bit_cast` on C++14 fails to compile; the C++14 workaround (memcpy) must be documented |
| GAP-20-7 `std::source_location` | C++20 | C++11: `__FILE__`/`__LINE__` macros | **20** | 📌 callout: C++14 alternative (macro-based; document migration path) | 🟢 LOW — error message on C++14 is clear; developers already know the macro approach |
| GAP-20-8 `constinit` | C++20 | C++11: no exact equivalent; document init-order-fiasco prevention via other means | **20** | 📌 callout: C++14 workarounds (Schwarz counter, function-local static, explicit initialization ordering) | 🟡 MEDIUM — C++14 developers who see `constinit` have no fallback without documentation |
| GAP-20-9 Coroutine generators | C++20 (`co_yield`); C++23 (`std::generator<T>`) | No polyfill | **20** | ✂️ **SPLIT REQUIRED** — C++20 custom generator (using `promise_type` boilerplate) and C++23 `std::generator<T>` are substantively different; custom generator must remain documented (the boilerplate is how it works); `std::generator` is a callout in the same file | 🔴 HIGH — coroutines will not compile on C++14 or C++17; must be strictly greenfield/modern-gated |
| GAP-20-10 `std::atomic_ref` | C++20 | No equivalent — `std::atomic` wrapping is different semantics | **20** | 📌 callout: alignment requirement warning must be in frontmatter note AND inline; misaligned `atomic_ref` is UB with no compile-time diagnostic | 🔴 HIGH — most dangerous content in the C++20 section from a silent-UB standpoint; see Section 3 |
| GAP-20-11 Calendar/timezone | C++20 (std::chrono); C++11 (HowardHinnant/date) | ✅ YES — `HowardHinnant/date` (MIT) is a C++11 polyfill with nearly identical API | **11** (HowardHinnant section); ★ C++20 (std::chrono section) | ✂️ **SPLIT REQUIRED — BLOCKING** — see Section 5 for full FAR 117 analysis; the C++14 path is NOT optional | 🚨 CRITICAL — CWR (C++14, FAR 117 obligation) cannot access timezone guidance as currently specified |
| GAP-20-12 Lambda improvements | C++20 (template lambdas, unevaluated contexts) | C++14: generic lambdas (`auto` parameter) | **14** (generic lambdas note); ★ C++20 (template lambdas, unevaluated) | 📌 callout sufficient | 🟢 LOW |
| GAP-20-13 Aggregate improvements | C++20 | C++14: strict aggregate rules | **20** | 📌 callout sufficient | 🟢 LOW |

### Core Guidelines Gaps (GAP-CG1 – GAP-CG12)

| Gap | Min Standard | C++11/14 Applicable? | `cpp_version_min` | Split Required | Misrouting Risk |
|-----|-------------|----------------------|-------------------|----------------|-----------------|
| GAP-CG1 Interface design (I.11/I.12) | C++11 (gsl::not_null) | ✅ YES — fully applicable | **11** | 📌 callout: C++20 contracts proposal context | 🟢 LOW |
| GAP-CG2 Parameter passing (F.16-F.20) | C++11 (move semantics required) | ✅ YES | **11** | 📌 sufficient | 🟢 LOW |
| GAP-CG3 Rule of Zero/Five | C++11 (defaulted/deleted members) | ✅ YES | **11** | 📌 callout: C++20 spaceship for comparison operator | 🟢 LOW |
| GAP-CG4 Regular types / value semantics | C++11 (move constructor) | ✅ YES | **11** | 📌 callout: C++20 `<=>` automates comparison | 🟢 LOW |
| GAP-CG5 Performance / RVO | C++11 context (NRVO, move) | ✅ YES | **11** | 📌 sufficient | 🟢 LOW |
| GAP-CG6 Stdlib usage / string_view governance | C++17 for `std::string_view` | ⚠️ PARTIAL — SL.xx applies from C++11; `string_view` itself is C++17 | **17** for string_view sections; **11** for SL.xx algorithm rules | ✂️ **SPLIT REQUIRED** — string_view content must not be in the same section as C++11 stdlib guidance without explicit ★ C++17 gating | 🔴 HIGH — C++14 developers receiving `std::string_view` guidance cannot compile it |
| GAP-CG7 C-style / `extern "C"` | C++98+ | ✅ YES | **98** | 📌 sufficient | 🟢 LOW |
| GAP-CG8 Source file organization (SF.xx) | C++11+ for general; C++20 for modules | ✅ PARTIAL | **11** | 📌 callout: SF.xx module guidance is ★ C++20 | 🟡 MEDIUM — modules guidance must not reach non-greenfield tiers |
| GAP-CG9 GSL Profiles (Pro.xx) | C++11 for GSL | ✅ YES | **11** | 📌 sufficient | 🟢 LOW |
| GAP-CG10 CP.42/43/50 | C++11 | ✅ YES | **11** | 📌 sufficient | 🟢 LOW |
| GAP-CG11 `std::string_view` lifetime traps | **C++17** (CRITICAL — see below) | NO — `string_view` does not exist in C++14 | **17** ← MUST BE 17 | ✂️ **CRITICAL VERSION DECISION** — see Section 6 | 🚨 CRITICAL — if set to 14, this content reaches CWR (C++14) where it cannot compile AND may teach patterns the team cannot use |
| GAP-CG12 `deducing this` (C++23) | C++23 | NO | **23** | 📌 gate to greenfield only | 🟡 MEDIUM — if linked from CRTP section without version gate, C++14 devs will attempt it |

### AA Brownfield Gaps (GAP-AA1 – GAP-AA8)

| Gap | Min Standard | C++11/14 Applicable? | `cpp_version_min` | Split Required | Misrouting Risk |
|-----|-------------|----------------------|-------------------|----------------|-----------------|
| GAP-AA1 Characterization testing | C++98+ (testing methodology) | ✅ YES | **98** | 📌 callout: C++14 Catch2 vs C++11 GoogleTest API differences | 🟢 LOW |
| GAP-AA2 JNI thread safety | C++98+ (JNI is C-based) | ✅ YES | **98** | 📌 sufficient | ⚠️ Note: governance doc must NOT suggest `std::atomic<JNIEnv*>` (wrong for non-C++ reasons — JNIEnv is thread-local by JVM contract, not a shared pointer); see version trap in Section 3 |
| GAP-AA3 MFC integration | C++14 (modern C++ + MFC) | ✅ YES | **14** | 📌 sufficient | 🟢 LOW |
| GAP-AA4 FICO Xpress solver | C++98+ | ✅ YES | **98** | 📌 sufficient | 🟢 LOW |
| GAP-AA5 CMake migration | C++14+ (modern CMake); C++20 for modules | ✅ PARTIAL | **14** | 📌 callout: module support requires C++20 + CMake 3.28+ | 🟡 MEDIUM |
| GAP-AA6 RCPtr migration | C++11 (std::shared_ptr target) | ✅ YES | **11** | 📌 sufficient | 🟢 LOW |
| GAP-AA7 Resource Handle Pattern | C++11 (RAII wrappers) | ✅ YES | **11** | 📌 sufficient | 🟢 LOW |
| GAP-AA8 Legacy serialization | C++11 (memcpy base); C++20 (std::bit_cast) | ✅ PARTIAL | **11** (memcpy section); ★ C++20 (bit_cast section) | 📌 callout: `std::bit_cast` is ★ C++20; use `memcpy` pattern for C++14 codebases | 🟡 MEDIUM |

---

## Section 2: Version-Split Decisions

The following decisions govern which gaps need genuinely separate files or sections and which
can be handled with `★ C++NN` callouts. The criterion applied: if the C++11/14 and C++20
approaches to the same problem are substantively different in idiom, API, library dependency, or
compilation result — not just a syntax upgrade — they require separate content.

### Files / Sections Requiring a Split (12 total)

These REQUIRE separate content (separate section, separate file, or at minimum a clearly-bounded
`★ C++20` section that the routing layer will not serve to `transitional`):

| # | Gap | Why Split is Required | Recommended Structure |
|---|-----|-----------------------|-----------------------|
| 1 | GAP-C2 (Parallel algorithms) | C++14 has no `std::execution`; `par_unseq` + TBB linkage is a different architectural decision from `std::async` | Two sections: `## Parallel Algorithms ★ C++17` and `## Async Patterns (C++11/14)` in same file; `cpp_version_min: 11` |
| 2 | GAP-C3 (jthread / stop_token) | Manual stop flag vs. cooperative stop_token are substantively different patterns | Two sections or two examples files; `bshoshany/thread-pool` derives only from ★ C++17 section |
| 3 | GAP-C6 (Thread pool) | `bshoshany/thread-pool` requires C++17; C++11 manual pool is architecturally different | `ref-concurrency-advanced.md` sections: `## Thread Pool (C++11/14)` and `## Thread Pool ★ C++17/20` |
| 4 | GAP-C10 (CP.51/52/53) | Coroutine rules inapplicable in C++14; `## Lambda-in-Coroutine Rules ★ C++20` must be a separate heading | Separate heading with ★ C++20; extract a C++11-applicable "lambda capture in threads" rule to an ungated section |
| 5 | GAP-T1 (CRTP) | `deducing this` (C++23) supersedes CRTP for mixin use case; must be visually separate | Single file: `## CRTP (C++11 – C++20)` and `## Explicit Object Parameter ★ C++23`; `cpp_version_min: 11` |
| 6 | GAP-T6 (NTTPs) | Floating-point and class-type NTTPs are C++20 only; integral NTTPs are C++98 | `## Non-Type Template Parameters (integral, C++98+)` and `## NTTP Extensions ★ C++20` |
| 7 | GAP-T7 (Advanced concepts) | Concepts are C++20 only; SFINAE is the C++11/14 parallel | `## Advanced Template Constraints (C++11/14 SFINAE)` and `## Concepts ★ C++20` in same file |
| 8 | GAP-20-2 (Ranges/views) | `range-v3` namespace differs from `std::ranges`; `ranges::view::filter` ≠ `std::views::filter` | Two sections: `## Range Pipelines with range-v3 (C++14)` and `## std::ranges / std::views ★ C++20` |
| 9 | GAP-20-3 (std::format) | `{fmt}` and `std::format` are separate libraries with differing edge-case behavior | Two sections: `## String Formatting with {fmt} (C++11+)` and `## std::format ★ C++20` |
| 10 | GAP-20-5 (std::span) | gsl::span and std::span have different default extents and checked-iterator semantics | Two sections: `## Array View with gsl::span (C++14)` and `## std::span ★ C++20` |
| 11 | GAP-20-9 (Coroutine generators) | C++20 custom generator (promise_type boilerplate) and C++23 `std::generator<T>` are different teaching targets | Two sections: `## Custom Generator (C++20)` and `## std::generator<T> ★ C++23` |
| 12 | GAP-20-11 (Calendar/timezone) | HowardHinnant/date and std::chrono zoned_time require entirely different includes and types | Two sections: `## Timezone Arithmetic with Howard Hinnant's date (C++11/14)` and `## std::chrono Calendar and Timezone ★ C++20` — see Section 5 |

### Files That Can Use Callouts (remaining)

These do NOT require splits — `★ C++NN` markers in a single file are sufficient:
GAP-C1, GAP-C4, GAP-C5 (except atomic_ref), GAP-C7, GAP-C8,
GAP-CG1 through CG5, GAP-CG7 through CG10,
GAP-20-4, GAP-20-6, GAP-20-7, GAP-20-8, GAP-20-12, GAP-20-13,
GAP-AA1 through AA8 (AA2 requires a correctness trap note, see Section 3).

---

## Section 3: Version-Specific Accuracy Traps in ESE Content

The following are the highest-risk cases where a C++14 developer might receive guidance that
compiles (or partially compiles) but produces incorrect behavior silently. Ordered by severity.

### TRAP-1 🚨 `std::atomic<shared_ptr<T>>` — Lock-Free Claim × Version Routing

**Risk level: CRITICAL**

This is already a blocking issue from prior reviews. The version routing system makes it **worse**:

| Scenario | What Happens |
|----------|-------------|
| Content routed to `transitional` (C++14) as C++20 guidance | `std::atomic<shared_ptr<T>>` does not exist in C++14; the C++14 API uses deprecated free functions `std::atomic_load()`/`std::atomic_store()` — also not lock-free, but with a different API |
| Content routed to `greenfield` (C++20) with "lock-free" claim | `is_lock_free()` returns `false` on libstdc++, libc++, and MSVC STL today (spinlock-based hash table / internal locking); developer assumes lock-free; uses in safety-critical code |
| C++26 context | P2197 (`std::atomic_shared_ptr`) may provide hardware lock-free support; treating C++20 as the target confounds this migration path |

The version routing system does not cure this because the error is in the *claim*, not in the
routing. Even with perfect routing (greenfield only), the claim remains false. But incorrect
routing (to `transitional`) adds a second hazard: the developer encounters the C++14 API
(`atomic_load`/`atomic_store`), which is:
1. Deprecated in C++20
2. Still not lock-free
3. Has different call syntax

**Required action:** `cpp_version_min: 20` for this content; explicit note:
`is_lock_free() == false` on all three major implementations; direct to `std::atomic<T*>` +
hazard pointer pattern for genuinely lock-free semantics.

---

### TRAP-2 🚨 `std::atomic_ref` Alignment Requirements (GAP-20-10)

**Risk level: HIGH — silent UB, no compile-time diagnostic**

`std::atomic_ref<T>` requires the referenced object to be aligned to
`std::atomic_ref<T>::required_alignment`, which may be larger than `alignof(T)`.

```cpp
struct LegacyNode {
    int id;          // offset 0
    char flags;      // offset 4
    int next_id;     // offset 5 ← misaligned! (on most platforms, int requires 4-byte alignment)
};

LegacyNode node;
// Compiles; runtime UB on every major implementation:
std::atomic_ref<int> ref(node.next_id);  // next_id is at offset 5 — UB
```

This is the primary use case for `atomic_ref` in AA's context: applying atomic operations to
fields of legacy structs without modifying the struct layout. If the field is misaligned
(common in hand-packed binary protocol structs like those in the CWR serialization layer),
`atomic_ref` is UB. There is no runtime error — the atomic operation simply races.

**Required frontmatter note in `cpp_version_min: 20` section:**
> ⚠️ `std::atomic_ref<T>` requires `alignof(T)` alignment at the reference target.
> Packed structs, manually-laid-out binary formats, and `#pragma pack` structs are
> not safe atomic_ref targets without explicit alignment verification.
> Use `static_assert(offsetof(Struct, field) % sizeof(T) == 0)` before applying atomic_ref.

---

### TRAP-3 🔴 Parallel Algorithms Silent Fallback to Sequential (GAP-C2)

**Risk level: HIGH — silent correctness failure in performance-critical code**

R5 noted this in the original review. The routing dimension adds a new angle:

`std::execution::par_unseq` on Clang/libc++ requires explicit TBB linkage (`-ltbb`).
Without it, behavior silently falls back to sequential — correct output, wrong performance
contract. **This means a developer who tests their parallel algorithm locally (perhaps on a
system with TBB installed globally) and then deploys to a Docker container without TBB will
observe correct output with no error**, believing the algorithm is parallelized.

This trap applies to the `modern` tier (C++17). The routing system will correctly not serve
this content to `transitional` (C++14). But within the `modern` tier, the CMake linkage
section is not optional — it is a correctness constraint. The governance doc must include:

```cmake
# Required for std::execution::par/par_unseq on libc++/Clang:
find_package(TBB REQUIRED)
target_link_libraries(myapp PRIVATE TBB::tbb)
```

And a compiler support table: GCC/libstdc++ has native par_unseq support; Clang/libc++ requires
TBB; MSVC has built-in parallel algorithms support (no TBB needed).

---

### TRAP-4 🔴 `boost::lockfree::queue<T>` Bounded Capacity — Push Returns False Silently

**Risk level: HIGH — silent message loss in production queues**

`boostorg/lockfree::queue<T>` is a **bounded queue** — capacity is fixed at construction:

```cpp
boost::lockfree::queue<Task*> q(1024);  // max 1024 elements
bool success = q.push(new Task(...));    // returns false when full — silently drops the task
```

`push()` returning `false` when at capacity is easy to ignore. Production code that does
`q.push(task)` without checking the return value silently drops tasks when the queue is full.

This is a use case AA needs: CWR uses unbounded-growth patterns for work queues. The governance
doc must state prominently in the GAP-C5/C6 sections:

> ⚠️ `boost::lockfree::queue<T>` is a **bounded queue** — capacity is fixed at construction
> and cannot grow. `push()` returns `false` when full; the caller must handle this.
> For unbounded-growth semantics, `std::deque` with a mutex is simpler and correct for most
> AA workloads. Lock-free is not free — benchmark first.

---

### TRAP-5 🔴 `filter_view` Not `const`-Iterable (GAP-20-2)

**Risk level: HIGH — "works in one context, compile failure in another"**

Already flagged in R5's original review. The routing dimension makes this a version-split
trigger: `std::ranges::filter_view` caches its `begin()` iterator (to satisfy the O(1)
begin() requirement), which requires mutability. The consequence:

```cpp
// Does NOT compile:
void print(const std::ranges::filter_view<std::vector<int>&, auto> fv) {
    for (int x : fv) { ... }  // begin() is not const; compile error
}

// Compiles — passes by value:
void print(std::ranges::filter_view<std::vector<int>&, auto> fv) { ... }

// range-v3 (C++14 polyfill): behaves differently — range-v3 views are const-iterable
// in many cases; the C++14 polyfill does NOT exhibit this std::ranges constraint
```

This is a behavioral difference between `range-v3` (C++14) and `std::ranges` (C++20) that
makes the split mandatory (not just cosmetic). A developer who migrates from range-v3 code
to std::ranges will find previously-const function signatures fail to compile with confusing
messages about `begin()`.

The split section structure should explicitly call this out as a migration trap.

---

### TRAP-6 🔴 `std::atomic<JNIEnv*>` Anti-Pattern (GAP-AA2)

**Risk level: HIGH in JNI context — incorrect guidance that sounds authoritative**

This is not a C++ version trap — it is a JNI semantics trap. But it interacts with version
routing in a dangerous way: an AI agent that receives `ref-concurrency-advanced.md` (with
C++11 `std::atomic` patterns) alongside a JNI threading question may synthesize:

```cpp
// WRONG — sounds like modern C++ but is fatally incorrect:
static std::atomic<JNIEnv*> env_cache;  // DO NOT DO THIS

// CORRECT — JNIEnv* is thread-local by JVM contract:
JNIEnv* env = nullptr;
jvm->AttachCurrentThread(reinterpret_cast<void**>(&env), nullptr);
// Use env; DetachCurrentThread when done
```

`JNIEnv*` is **thread-local by JVM contract** — it is not a shared pointer. No amount of
`std::atomic` wrapping makes it safe to share across threads because the pointer is valid only
for the thread that created it. This is a JVM rule, not a C++ rule, and `std::atomic<JNIEnv*>`
looks like correct concurrent code.

The `ref-brownfield-survival.md` file must contain a prominent `// NON-COMPLIANT` example
showing this anti-pattern, explicitly noting that the JNI thread-local contract is independent
of C++ memory model guarantees. It must also be included in the `transitional` tier's prefer
list (CWR runs C++14 and uses JNI today).

---

### TRAP-7 🟡 `range-v3` Namespace Leakage into `std::ranges` Code

**Risk level: MEDIUM — incorrect namespace causes confusing compile failures**

When teaching both range-v3 and std::ranges in adjacent sections:
- `range-v3`: `ranges::view::filter`, `ranges::view::transform`, `ranges::sort`
- `std::ranges`: `std::views::filter`, `std::views::transform`, `std::ranges::sort`

If a developer copying examples from the C++14 section uses `ranges::filter` in a C++20
codebase (which has range-v3 as a dependency), the code compiles but uses range-v3's filter
view, not std::ranges' filter view. The behavioral differences are subtle (lazy evaluation
semantics, sentinel types, const-iterability) but real.

The split sections must use `#include` guards and namespace declarations in every code example
to make the source unambiguous.

---

## Section 4: OSS Source Version Compatibility

Per-source assessment for the five primary OSS derivation references.

### `boostorg/lockfree` — Boost Software License

| Dimension | Assessment |
|-----------|-----------|
| C++ standard required | C++03+ (uses `boost::atomic`); C++11 `std::atomic` available as option |
| Safe for `transitional` (C++11/14)? | ✅ YES — `boost::atomic` maps to C++11 `std::atomic` semantics; API is compatible |
| Safe for `brownfield` (C++98/03)? | ✅ YES with Boost dependency; `boost::atomic` provides the threading model |
| Key version caveat | Tagged-pointer ABA prevention requires `cmpxchg16b` (DWCAS) on x86-64; ARM64 portability concerns; documentation must note this |
| Bounded-capacity caveat | `queue<T>` capacity fixed at construction; `push()` returns `false` when full; **must be prominently documented in all tier sections** |
| Version routing verdict | ✅ SAFE across `transitional`, `modern`, `greenfield` tiers — with documented caveats |

### `bshoshany/thread-pool` — MIT License (2021)

| Dimension | Assessment |
|-----------|-----------|
| C++ standard required | **C++17 minimum** — uses `std::invoke`, `if constexpr`, `std::invoke_result_t`, `std::apply`; the v4.x series uses `std::jthread` and `std::counting_semaphore` (C++20) |
| Safe for `transitional` (C++11/14)? | ❌ **NO** — will not compile on C++14; must not be in `transitional` tier's prefer list |
| Safe for `modern` (C++17)? | ✅ YES for v3.x series; ⚠️ C++20 features in v4.x — check version in oss-reference-registry.yaml |
| Key version caveat | `cpp_version_min` for any content derived from this library must be **17** (v3.x) or **20** (v4.x). The AVATAR-RAG-INDEX.yaml `transitional.prefer` list must not include files derived from this source |
| Proposal proposal assessment | The proposal designates `bshoshany/thread-pool` as the OSS source for GAP-C6 without specifying which version tier. This is a gap that must be resolved before ESE-25 executes |
| Version routing verdict | ⚠️ **CONDITIONALLY SAFE** — only for `modern`/`greenfield` tiers; explicitly excluded from `transitional` |

### `fmtlib/fmt` — MIT License (2012)

| Dimension | Assessment |
|-----------|-----------|
| C++ standard required | C++11 minimum for the library itself |
| Safe for `transitional` (C++11/14)? | ✅ YES — this is the primary use case; `{fmt}` as a C++11 polyfill for `std::format` |
| API compatibility with `std::format` | `fmt::format_string<T>` maps to `std::format_string<T>`; `fmt::formatter<T>` maps to `std::formatter<T>`. Recent `{fmt}` versions (v10+) track the C++20 standard closely |
| Key migration note | When C++20 becomes available, migration from `{fmt}` to `std::format` is mechanical: change `#include <fmt/core.h>` to `#include <format>`, change `fmt::` to `std::`. Document this in the split section |
| `vformat` trap | `fmt::vformat` (runtime format string) is the hazard equivalent to `std::vformat` — both require input validation. The governance doc must cover both |
| Version routing verdict | ✅ **SAFE and CORRECT** for `transitional` tier as C++11 polyfill; `std::format` section gated to ★ C++20 |

### `ericniebler/range-v3` — Boost Software License (2013)

| Dimension | Assessment |
|-----------|-----------|
| C++ standard required | C++14 minimum (uses generic lambdas and constexpr improvements) |
| Safe for `transitional` (C++11/14)? | ✅ YES for C++14 — this is the canonical C++14 ranges polyfill |
| As `std::ranges` C++14 teaching source | ✅ YES — range-v3 was the reference implementation from which C++20 `std::ranges` was designed; Eric Niebler co-authored P0896R4 |
| API difference from `std::ranges` | Namespace: `ranges::view::filter` vs `std::views::filter`. Const-iterability semantics differ (see TRAP-5). Sentinel types differ. Code examples must not mix namespaces |
| Key migration note | range-v3 → std::ranges migration is NOT always mechanical; `filter_view` const-iterability change is a breaking behavioral difference (not just a namespace rename) |
| Version routing verdict | ✅ **SAFE** for `transitional` (C++14) tier in clearly-labelled range-v3 sections; `std::ranges` content gated to ★ C++20 |

### C++ Standard Version Not Explicitly in OSS Source — `boostorg/iterator` (CRTP)

| Dimension | Assessment |
|-----------|-----------|
| C++ standard required | C++03 (from 2002); fully C++11/14 compatible |
| Safe for `transitional`? | ✅ YES |
| Critical note | `iterator_facade` uses a 5-parameter CRTP template — correct but opaque to beginners. The governance doc should simplify to a 2-3 parameter teaching example derived from the concept, not copy the 5-parameter interface |
| `deducing this` pairing required | Any file that teaches CRTP from `boostorg/iterator` MUST include a gated `## Explicit Object Parameter ★ C++23` section that demonstrates how `deducing this` eliminates the `static_cast<Derived&>(*this)` cast entirely |
| Version routing verdict | ✅ SAFE for all tiers; `deducing this` section gated to C++23 |

---

## Section 5: FAR 117 Timezone — C++14 Fallback Path for CWR Teams

This is the most urgent version-routing gap in the entire proposal.

### The Problem

GAP-20-11 (C++20 Calendar/timezone) is now correctly prioritized at P1 due to FAR 117
obligations. But the C++20 `std::chrono::zoned_time` / `std::chrono::get_tzdb()` API
requires C++20. CWR — the primary system performing FAR 117 crew rest calculations — runs
C++14. As currently specified, GAP-20-11 teaches a standard that CWR cannot use.

This is not a cosmetic gap. **A CWR developer asking "how do I calculate UTC offset for
America/Chicago for a given crew rest window?" must receive actionable C++14 guidance, not
an explanation that C++20 has `zoned_time`.**

### The Correct C++14 Path: HowardHinnant/date

The authoritative C++14 solution is `HowardHinnant/date` (MIT license), authored by Howard
Hinnant — the same engineer who redesigned `std::chrono` for C++20. The `date` library:

1. Provides `date::year_month_day`, `date::zoned_time<Duration>`, `date::get_tzdb()` — the
   same types and API as C++20 `std::chrono`, in a C++11-compatible header-only library
2. Requires the IANA timezone database (`tzdata`) to be installed at runtime (or bundled)
3. Is MIT-licensed — clean OSS derivation, no commercial-book exposure
4. Is the direct ancestor of C++20 chrono: the migration from `date::zoned_time` to
   `std::chrono::zoned_time` is mechanical (namespace change only)

```cpp
// C++14 — CWR TODAY (using HowardHinnant/date, MIT):
#include "date/tz.h"  // Howard Hinnant, https://github.com/HowardHinnant/date

// FAR 117 crew rest window: does this rest period meet minimum in New York timezone?
date::zoned_time<std::chrono::minutes> tz_rest_start =
    date::make_zoned("America/New_York", rest_start_utc);

auto local_tp = tz_rest_start.get_local_time();
auto day = date::floor<date::days>(local_tp);
date::year_month_day ymd{day};

// C++20 MIGRATION (identical semantics, namespace change only):
// std::chrono::zoned_time<std::chrono::minutes> tz_rest_start =
//     std::chrono::make_zoned("America/New_York", rest_start_utc);
```

### Why NOT POSIX `localtime_r` + `TZ` Environment Variable

The intuitive C++14 fallback (manipulate `TZ`, call `tzset()`, use `localtime_r()`) is
**incorrect for FAR 117 purposes for the following reasons:**

1. **Thread safety:** `setenv("TZ", ...)` / `tzset()` are not thread-safe in multi-threaded
   programs. CWR uses a multi-threaded solver. Setting `TZ` in one thread affects all threads.
   This is undefined behavior under POSIX in the presence of other calls to `getenv`.

2. **POSIX-only:** `localtime_r` is not available on Windows; if any CWR component has a
   Windows build path, this breaks.

3. **IANA timezone name handling:** FAR 117 rest calculations require named IANA timezones
   (e.g., `"America/Chicago"`, `"America/New_York"`). POSIX TZ strings use a different
   format (`CST6CDT` vs `America/Chicago`). Mapping is error-prone and incomplete.

4. **DST transitions:** POSIX `mktime` does not reliably handle the ambiguous hour during
   DST "fall back" — crew rest windows that span a DST transition will be incorrectly
   calculated. HowardHinnant/date handles this explicitly via `choose::earliest`/
   `choose::latest` disambiguation.

### Required Governance Doc Structure for GAP-20-11

The `ref-cpp20-features.md` (or the brownfield ref) MUST have two explicitly-labelled sections:

```markdown
## Timezone-Aware Time Arithmetic (C++11/14) — HowardHinnant/date

cpp_version_min: 11
cpp_version_note: "Requires HowardHinnant/date library (MIT). C++20 migration path provided."

[C++14 examples using date::zoned_time]
[IANA timezone database setup]
[FAR 117 crew rest window calculation example]
[Migration note: namespace change only to get to C++20]

## std::chrono Calendar and Timezone ★ C++20

[C++20 examples using std::chrono::zoned_time]
[Same FAR 117 example for comparison]
```

The `transitional` tier's `prefer` list in `AVATAR-RAG-INDEX.yaml` MUST include the file
containing the C++14 HowardHinnant/date section. The CWR developer who asks "how do I
handle timezone-aware time arithmetic for FAR 117?" must receive the C++14 path.

### Runtime Dependency Note (Required)

Both `HowardHinnant/date` (in timezone mode) and C++20 `std::chrono` timezone support
require an IANA timezone database at runtime. Options:
- System-installed `tzdata` package (standard on Linux; must be in Docker images)
- Bundled with the library (`INSTALL_TZ_DB` option in HowardHinnant/date)
- The `date` library's `"date/tz.h"` will throw `std::runtime_error` if no database is found

This is an operational dependency that CWR's deployment infrastructure must address. The
governance doc must document this requirement explicitly — it is a FAR 117 compliance
prerequisite.

---

## Section 6: Prior Blocking Issues — Version Dimension

### `std::atomic<shared_ptr<T>>` — Does Version Routing Make This Worse?

**Answer: YES in two dimensions.**

**Dimension 1 — C++14 API incompatibility not documented:**

In C++14, `std::atomic<std::shared_ptr<T>>` does not exist. The C++14 API for atomic shared
pointer operations uses deprecated free functions:

```cpp
// C++14 (the only way to atomically operate on shared_ptr):
std::shared_ptr<T> loaded = std::atomic_load(&ptr);      // deprecated in C++20
std::atomic_store(&ptr, new_value);                        // deprecated in C++20
std::atomic_compare_exchange_strong(&ptr, &expected, desired); // deprecated in C++20

// C++20:
std::atomic<std::shared_ptr<T>> atomic_ptr;
// is_lock_free() == false on all implementations
```

If the ESE content is correctly gated at `cpp_version_min: 20` and routed to `greenfield`
only, C++14 developers will not receive it. But they will also not receive guidance on the
C++14 API — leaving them to discover `std::atomic_load` independently, which is deprecated
in C++20 and appears nowhere in the routing system's transitional refs.

**The correct fix:** Add a section to `ref-concurrency-advanced.md` or the existing
`ref-concurrency.md` covering the C++11/14 `std::atomic_load/store` free functions at
`cpp_version_min: 11`, clearly noting:
> "These are deprecated in C++20. In C++20, use `std::atomic<std::shared_ptr<T>>` — but
> be aware `is_lock_free()` returns `false` on all major implementations today."

**Dimension 2 — The false claim itself remains independent of routing:**

Even with perfect routing (greenfield only), the claim that
`std::atomic<shared_ptr<T>>` provides "lock-free node update" is factually wrong on every
major implementation. A C++20 developer on a `greenfield` project who receives this content
will implement a spinlock-based concurrent data structure believing it to be lock-free.

This is a pre-existing blocker. The version routing system does not cure it because the error
is in the claim, not in which tier receives it.

---

### `std::string_view` Lifetime Traps (GAP-CG11) — Correct `cpp_version_min`

**The correct value is `17`. Anything other than `17` is technically wrong.**

`std::string_view` was introduced in C++17 (P0254R2). It does not exist in C++14. There are
no polyfills in the AA stack equivalent to HowardHinnant/date — `std::string_view` is a
standard library type with no widely-deployed C++14 alternative in AA's codebase.

**If `cpp_version_min` is set to `14` (incorrect):**
- The test `test_phase2d_c4_ref_frontmatter.py` will pass (14 is a valid value)
- The routing layer will include this content in the `transitional` tier's pool
- CWR (C++14) developers will receive `std::string_view` guidance
- Every example in the content will fail to compile in their codebase
- The `// NON-COMPLIANT` trap examples may mislead them about which patterns to avoid

**If `cpp_version_min` is set to `17` (correct):**
- The routing system correctly routes to `modern` and `greenfield` tiers only
- C++14 developers do not receive `string_view` content until they upgrade
- A separate note in the C++14 tier should say: "C++14 alternative: `const std::string&`
  parameters provide string ownership safety without `string_view` lifetime concerns."

**The `cpp_version_min` test does not validate correctness.** This is a gap in the
test harness that the ESE work will expose: the test validates that the field *exists*
with a *valid* value, but does not validate that the value is technically correct for the
content. R5 recommends adding a content-review gate to the acceptance criteria for every
new reference file that documents the `cpp_version_min` decision with a rationale comment:

```yaml
# cpp_version_min: 17
# Rationale: std::string_view was introduced in C++17 (P0254R2).
#            C++14 alternative: use `const std::string&` for read-only string parameters.
#            Do not set to 14 — string_view is not available in CWR/IOC_ALP toolchain.
```

---

### C++20 Calendar/Timezone (GAP-20-11) — Prior Blocking Issue + Version Dimension

This gap intersects prior blocking (P3 → P1 promotion, which has been addressed) with the
version-routing dimension (C++14 fallback path, which has NOT been addressed). See Section 5
for the complete analysis.

**Summary status:**
- Priority promotion (P3 → P1): ✅ Addressed in amended proposal
- FAR 117 legal rationale documented: ✅ Addressed in amended proposal
- C++14 fallback path (HowardHinnant/date): ❌ **NOT addressed — BLOCKING for CWR**
- AVATAR-RAG-INDEX.yaml routing for transitional tier: ❌ **NOT addressed — BLOCKING**
- IANA tzdata runtime dependency documentation: ❌ **NOT addressed**

---

## Updated Verdict

### Prior Blocking Issues Status

| Blocking Issue | Prior Status | Version-Routing Dimension Added |
|---------------|-------------|--------------------------------|
| `std::atomic<shared_ptr<T>>` false lock-free claim | 🔴 BLOCKING — unaddressed | 🔴 WORSE — C++14 API gap also undocumented; two separate required actions now |
| "CVE-2024" `std::format` hallucination | 🔴 BLOCKING — unaddressed | No change from version routing |
| `std::string_view` lifetime traps absent | 🔴 BLOCKING — gap not yet scheduled | 🔴 NEW DIMENSION — `cpp_version_min` must be 17; if set to 14, routing actively serves invalid content |
| C++20 Calendar/timezone C++14 fallback | 🔴 NEW BLOCKING | 🔴 HowardHinnant/date path required; CWR (60% of AA C++ LOC) cannot access this guidance as currently specified |

### New Blocking Issues from Version-Routing Analysis

| # | Issue | Severity |
|---|-------|----------|
| 1 | GAP-20-11 has no C++14 fallback path for FAR 117 compliance in CWR | 🔴 BLOCKING |
| 2 | `bshoshany/thread-pool` (C++17 minimum) not scoped to `modern`/`greenfield` tiers in proposal | 🔴 BLOCKING — will produce invalid content for transitional tier if not gated |
| 3 | GAP-CG11 `cpp_version_min` must be 17 (string_view is C++17) | 🔴 BLOCKING — test passes with 14 but content is wrong |
| 4 | 12 gaps lack version-split decisions; `ref-concurrency-advanced.md` and `ref-cpp20-features.md` will have inconsistent `cpp_version_min` values without explicit decisions pre-implementation | 🟠 HIGH |
| 5 | GAP-20-2 (Ranges) `range-v3` vs `std::ranges` API differences require split; `filter_view` const-iterability behavioral difference is a migration trap | 🟠 HIGH |
| 6 | GAP-C2 `par_unseq` TBB linkage trap must be in a `★ C++17` gated section with CMake linkage note | 🟠 HIGH |
| 7 | `std::atomic_ref` alignment UB trap not documented; no frontmatter note | 🟠 HIGH |
| 8 | JNI trap: `std::atomic<JNIEnv*>` anti-pattern may be generated by routing C++11 atomic content alongside JNI context | 🟠 HIGH |

### Required Actions Before Any ESE Task Executes

| # | Action | Tier Impact |
|---|--------|------------|
| 1 | Remove "lock-free" claim from `std::atomic<shared_ptr<T>>`; add `is_lock_free() == false` + C++14 free-function API note | All tiers |
| 2 | Remove hallucinated "CVE-2024" from ESE-06; replace with compile-time safety explanation | All tiers |
| 3 | Add GAP-20-11 C++14 fallback section using HowardHinnant/date (MIT); include in `transitional` tier prefer list | `transitional` |
| 4 | Set GAP-CG11 `cpp_version_min: 17` with rationale comment; add C++14 alternative note | `transitional` exclude |
| 5 | Gate `bshoshany/thread-pool`-derived content to `modern`/`greenfield` tiers explicitly | `transitional` exclude |
| 6 | Record version-split decisions (Section 2 table) as explicit acceptance criteria in `tasks.md` for each affected task | All tiers |
| 7 | Document `std::atomic_ref` alignment UB in frontmatter note + inline warning | `greenfield` |
| 8 | Document JNI `std::atomic<JNIEnv*>` anti-pattern in `ref-brownfield-survival.md` with `// NON-COMPLIANT` example | `transitional`/`brownfield` |
| 9 | Add `filter_view` non-const-iterability as P1 gotcha to GAP-20-2 scope | `greenfield` |
| 10 | Add Boost.Lockfree bounded-capacity warning to all tier sections covering GAP-C5/C6 | All tiers |

---

*R5 version-sensitivity review filed 2026-07-22. Supersedes relevant portions of R5-OSS-RESPONSE.md on version-routing questions. Prior blocking findings from REVIEW-PANEL.md §R5 remain in effect.*

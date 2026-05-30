# R6 — Senior AA Engineer: Version-Sensitivity Review of ESE Proposal

**Reviewer:** R6 — Senior AA Engineer, 15+ years CWR / IOC_ALP / crew scheduling  
**Review Scope:** C++ Avatar External Sources Enrichment (ESE-*) re-reviewed through the lens of the 5-tier version-sensitive routing system  
**Date:** 2026-07-14  
**Prior findings:** REVIEW-PANEL.md §R6 and R6-OSS-RESPONSE.md  
**Routing system baseline:** `docs/guides/avatars/cpp-version-sensitive-routing.md` + `AVATAR-RAG-INDEX.yaml` `version_routing_policy`  

---

## Executive Finding

The version-routing system was built specifically because ~95% of AA's C++ LOC was receiving
systematically wrong guidance. The ESE proposal was conceived, structured, and prioritised
before that routing system existed. Now that the routing system is live, I have to answer a
direct question on behalf of every CWR and IOC_ALP developer who will actually receive this
enrichment: **will the right content reach the right teams, or will the proposal's highest-value
deliverables route to the 5% of LOC that doesn't need them and silently miss the 95% that do?**

The answer, as the proposal currently stands, is: **the ESE deliverables will largely miss the
teams who need them most.** The five-tier routing system enforces `prefer` lists in
`AVATAR-RAG-INDEX.yaml`. Three of the four AA Brownfield Survival Pack files (ESE-A) do not
appear in any tier's `prefer` list at all. Fifteen of the sixteen P1 gaps produce deliverables
with an implied `cpp_version_min` of 20 — and **zero percent of AA's current C++ LOC is C++20.**
The fmtlib and range-v3 bridge paths exist as OSS alternatives in the proposal but are not
surfaced as separate routeable entries for `transitional` tier developers.

This is not a theoretical concern. The CWR developer opening `CrewWatchSolverJNI.cpp` today
sits in the `transitional` tier (`standard: "14"`, `idiom_level: "03"`). The routing system
will preferentially serve `ref-core-type-safety.md`, `ref-safety-memory-lifetime.md`, and
`ref-concurrency-threading.md` to that developer. The `ref-brownfield-survival.md` file —
the single most important ESE deliverable for that developer's actual production work — is
not in the `transitional` tier's prefer list and will not be retrieved by the routing system
without an explicit query. It will be unreachable in practice.

**Bottom line:** The ESE proposal must wire its deliverables into the routing system's `prefer`
lists before execution begins. `ref-brownfield-survival.md` must appear in BOTH `transitional`
AND `brownfield` tier prefer lists. C++20 gaps GAP-20-2 and GAP-20-3 must be split to expose
their bridge-library paths as separate `transitional`-tier routeable entries. GAP-20-4 must be
demoted from P1 — it has no practical application in AA's current value-type landscape.

---

## Section 1: Team Routing Matrix

### 1.1 Current Tier Assignments

| Repository | Standard | idiom_level | Tier | LOC Share |
|---|---|---|---|---|
| IOC_ALP, hte_pm_hostconn, CWR, IOC_FosQuery2 | C++14 | C++03 (CWR) / unset (others) | `transitional` | ~60% |
| SPEClient | MSVC 6.0 / pre-C++98 | pre-98 | `legacy` | ~24% |
| herc-odyssey-linux | C++98/03 | C++98/03 | `brownfield` | ~11% |
| IOC_ScreenPrinter, app-mgmt-killapp | C++17 (explicit) | C++17 | `modern` | ~5% |
| (no AA repo) | C++20/23 | C++20+ | `greenfield` | ~0% |

**Zero percent of current AA C++ LOC routes through the `greenfield` tier.**

### 1.2 CWR Team: What They Get vs. What Is Blocked

CWR project configuration: `standard: "14"`, `idiom_level: "03"`. Tier: `transitional`.
Avatar selects examples by `idiom_level` when it diverges from `standard` — so CWR gets C++03-idiom examples even though the compiler accepts C++14.

**Current `transitional` tier prefer list (AVATAR-RAG-INDEX.yaml):**
1. `refs/language/ref-core-type-safety.md`
2. `refs/safety/ref-safety-memory-lifetime.md`
3. `refs/safety/ref-concurrency-threading.md`

**ESE deliverables routed to CWR through `transitional` prefer list:**

| ESE Deliverable | Routed? | Reason |
|---|---|---|
| `ref-brownfield-survival.md` (GAP-AA1–AA8) | ❌ **NOT ROUTED** | Not in `transitional` prefer list |
| `ref-concurrency-advanced.md` (GAP-C1–C10) | ❌ **NOT ROUTED** | Not in `transitional` prefer list |
| `ref-cpp20-features.md` (GAP-20-*) | 🔴 **BLOCKED** | `cpp_version_min: 20` — blocked by tier version filter |
| `ENG-6.1-jthread-stop-token.md` (GAP-C3) | 🔴 **BLOCKED** | C++20 feature; `cpp_version_min: 20` |
| `ENG-3.1-ranges-views.md` (GAP-20-2) | 🔴 **BLOCKED** | `cpp_version_min: 20` (no bridge split) |
| `ENG-6.1-std-format.md` (GAP-20-3) | 🔴 **BLOCKED** | `cpp_version_min: 20` (no bridge split) |
| `ENG-3.1-crtp.md` (GAP-T1) | 🟡 **REACHABLE via query** | Not in prefer list; only via direct query |
| `ENG-6.1-memory-ordering.md` (GAP-C1) | 🟡 **REACHABLE via query** | Not in prefer list; only via direct query |

> **CWR impact:** Of the four AA Brownfield P1 gaps (GAP-AA1 through GAP-AA4), zero are
> reachable through the default routing path. A CWR developer asking about thread safety will
> receive `ref-concurrency-threading.md` — which contains general threading patterns — not
> the JNI-specific `AttachCurrentThread`/`DetachCurrentThread` lifecycle guidance in
> `ref-brownfield-survival.md`. This is the exact failure mode the routing system was built
> to prevent, now recreated for ESE content.

### 1.3 IOC_ALP Team: What They Get

IOC_ALP: C++14 (toolset default), no `idiom_level` declared. Tier: `transitional`.
Same prefer list as CWR. Same routing gaps apply.

**Additional IOC_ALP-specific concern:** GAP-AA3 (MFC integration) and GAP-AA5 (RCPtr
migration) are in `ref-brownfield-survival.md`. IOC_ALP's threading bugs are its #1 production
incident category. The content exists in ESE-A; the routing does not deliver it.

The `ref-brownfield-project-config.md` file (already live, in `brownfield` tier prefer list)
covers some MFC patterns — but not for IOC_ALP's specific tier (`transitional`). IOC_ALP
developers will miss the ESE-A MFC content entirely through default routing.

### 1.4 SPEClient Team: What They Get

SPEClient: MSVC 6.0 / pre-C++98. Tier: `legacy`.

**Current `legacy` tier prefer list:**
1. `refs/legacy/ref-legacy-navigation.md`
2. `refs/legacy/ref-mental-models-lang.md`
3. `refs/legacy/ref-legacy-smells-structural.md`
4. `refs/legacy/ref-concurrency-brownfield.md`

**ESE deliverables routed to SPEClient:**

| ESE Deliverable | Status |
|---|---|
| All GAP-20-* (C++20) | 🔴 **BLOCKED** — tier version filter + standard mismatch |
| All GAP-C* (advanced concurrency) | 🔴 **BLOCKED** — not in prefer list; most require C++11 atomics |
| `ref-brownfield-survival.md` (GAP-AA1–AA8) | ❌ **NOT ROUTED** — not in `legacy` prefer list |
| GAP-AA1 (characterization testing) | 🟡 Conceptually applicable but not routed |
| GAP-CG3 (Rule of Zero/Five) | 🔴 **BLOCKED** — MSVC 6.0 does not have C++11 special member functions |

> **SPEClient reality check:** Characterization testing (GAP-AA1) is universally applicable
> regardless of C++ standard. The Feathers seam injection technique works with C++98 codebases
> and is precisely what SPEClient developers need before touching any module. It must be in
> the `legacy` tier prefer list, not just `transitional`.

### 1.5 Unreachable ESE Content by Tier

| Tier | LOC Share | ESE P1 Gaps Reachable (of 16) | ESE P1 Gaps Blocked/Unrouted |
|---|---|---|---|
| `legacy` | 24% | 0 via default routing | 16 of 16 |
| `brownfield` | 11% | 0 via default routing | 16 of 16 |
| `transitional` | 60% | 0 via default routing (4–5 reachable via query) | 16 of 16 via prefer-list routing |
| `modern` | 5% | 4–5 (non-C++20 gaps) | 11+ C++20-only gaps |
| `greenfield` | ~0% | All 16 reachable | 0 |

**Finding: ~100% of AA C++ LOC will miss at least 11 of 16 P1 ESE gaps through the default
routing path as currently wired.** For the 84% of LOC in `legacy`/`brownfield`/`transitional`,
this rises to all 16 P1 gaps being either blocked or absent from `prefer` lists.

---

## Section 2: Brownfield Survival Pack Routing and `cpp_version_min` Decisions

### 2.1 Which Tier Should `ref-brownfield-survival.md` Appear In?

**Answer: BOTH `transitional` AND `brownfield` simultaneously.**

The gap analysis for ESE-A covers:
- GAP-AA1 (characterization testing): Applies to ALL brownfield codebases regardless of standard
- GAP-AA2 (JNI thread safety): CWR + any repo with JNI integration
- GAP-AA3 (MFC integration): IOC_ALP (C++14 transitional) + SPEClient (pre-C++98 legacy)
- GAP-AA4 (FICO Xpress): CWR (C++14 transitional)
- GAP-AA5–AA8 (RCPtr, resource handles, serialization, CMake): Both transitional and brownfield

The file must appear in:

```yaml
transitional:
  prefer:
    - refs/language/ref-core-type-safety.md
    - refs/safety/ref-safety-memory-lifetime.md
    - refs/safety/ref-concurrency-threading.md
    - refs/legacy/ref-brownfield-survival.md   # ADD — CWR/IOC_ALP primary path
    - refs/legacy/ref-concurrency-brownfield.md # ADD — JNI overlaps with brownfield concurrency

brownfield:
  prefer:
    - refs/legacy/ref-legacy-navigation.md
    - refs/legacy/ref-brownfield-adoption.md
    - refs/legacy/ref-brownfield-project-config.md
    - refs/legacy/ref-mental-models-memory.md
    - refs/legacy/ref-concurrency-brownfield.md
    - refs/legacy/ref-brownfield-survival.md   # ADD — herc-odyssey-linux
```

The `legacy` tier should also gain `ref-brownfield-survival.md` at minimum for the
characterization testing section (GAP-AA1), which is applicable to MSVC 6.0 era codebases.
SPEClient developers need characterization tests before touching any module.

### 2.2 What `cpp_version_min` Should `ref-brownfield-survival.md` Carry?

**Answer: `cpp_version_min: 98`**

This is the single most important `cpp_version_min` decision in the ESE proposal. The file's
primary audience is C++98/03 codebases and C++14-compiled-but-C++03-idiom codebases (CWR).
Setting `cpp_version_min: 11` would block the file from `brownfield` tier filtering, which
would defeat the entire purpose.

The file should use `★ C++11` section markers for the RAII wrapper variants that use
`std::unique_ptr`, `thread_local`, or `std::mutex`. The base patterns for each gap must be
demonstrable in C++98.

```yaml
---
cpp_version_min: 98
cpp_version_note: "Base patterns are C++98-safe. Sections marked ★ C++11 require C++11
  (unique_ptr, thread_local, std::mutex). All AA production repos compile at C++14+
  and receive the C++11 variants; only MSVC 6.0 era repos require C++98 fallbacks."
avatar: cpp
---
```

### 2.3 The JNI Thread Safety Question: `std::atomic` and C++ Standard Requirements

**GAP-AA2 (JNI thread safety): What standard does JNI itself require?**

JNI is a C API (`jni.h`). It has **no C++ standard requirement**. The JNI thread model is
enforced at the JVM level, not the C++ standard level:

| JNI Contract | C++ Standard Needed |
|---|---|
| `JNIEnv*` is thread-local by JVM spec | None — this is a runtime contract |
| `AttachCurrentThread` / `DetachCurrentThread` lifecycle | None — C API |
| `NewGlobalRef` / `DeleteGlobalRef` ownership | None — C API |
| RAII wrapper for attachment tracking | C++98 minimum (manual RAII), C++11 preferred (`thread_local`) |

The dangerous wrong pattern `std::atomic<JNIEnv*>` uses C++11 atomics — but it is wrong
because `JNIEnv*` is thread-local by contract (not because of any synchronisation primitive
behaviour). The atomic operation itself requires C++11. The example file must clearly mark:

```cpp
// ❌ WRONG — sounds sophisticated, is fatally incorrect
// std::atomic<JNIEnv*> g_env;   // requires C++11 but is STILL undefined behavior
//                                 // JNIEnv* is thread-local by JVM contract
//                                 // Atomic does not make a thread-local pointer shareable
```

**Recommended `cpp_version_min` for the JNI example file:**

| Section | Min Standard | Reason |
|---|---|---|
| Core JNI contract (what NOT to do) | 98 | Pure explanation, no C++ feature needed |
| C++98 RAII via `pthread_key_t` destructor | 98 | POSIX thread destructor for DetachCurrentThread |
| C++11 RAII via `thread_local` + lambda | 11 ★ | `thread_local` keyword required |
| C++14 RAII with `unique_ptr` scoped attachment | 14 ★★ | `make_unique`, cleaner lifetime |

For CWR specifically (`standard: "14"`, `idiom_level: "03"`): the C++11 `thread_local` variant
is the recommended target. Even though CWR uses C++03 idioms, `thread_local` is a keyword
addition (not a library feature) and is safe to introduce in isolation without upgrading the
rest of the codebase's idiom style.

**Required file-level frontmatter for `examples/ENG-6.1-jni-thread-safety.md`:**

```yaml
---
cpp_version_min: 98
cpp_version_note: "JNI is a C API with no C++ standard requirement. Base anti-patterns
  and C++98 POSIX fallback documented for all tiers. ★ C++11 section for thread_local
  RAII wrapper (recommended for CWR/transitional). ★★ C++14 section for unique_ptr
  scoped attachment."
avatar: cpp
---
```

---

## Section 3: ESE-A Version Ladder (Per Gap)

For each ESE-A gap, this section specifies: minimum standard for the primary example code,
whether a C++03-safe variant is needed, and what the CWR developer can use TODAY without a
toolchain upgrade (CWR: compiles C++14, writes C++03 idioms).

### 3.1 GAP-AA1: Characterization Testing for Legacy C++

**Primary derivation:** Michael Feathers seam techniques (WEWLC); `catchorg/Catch2` (Boost);
GoogleTest (Apache 2.0).

| Example | Min Standard | C++03 variant needed? | CWR usable today? |
|---|---|---|---|
| Sprout Method seam | C++98 | Yes (core pattern is C++98) | ✅ YES |
| Wrap Method seam | C++98 | Yes | ✅ YES |
| Link seam (test double via linker) | C++98 | Yes | ✅ YES |
| TEST_F fixture (GoogleTest) | C++11 (GTest 1.10+) | No — test harness only, not production code | ✅ YES (test builds can use C++11) |
| Golden-master assertion | C++98 | No | ✅ YES |

**Verdict:** `cpp_version_min: 98`. No separate C++03 variant needed — the production-side seam
patterns are inherently C++98-safe. The test harness (GoogleTest) uses C++11 syntax but only in
test files, not in the production code being characterized.

**Routing note:** This gap must be in the `legacy` tier prefer list as well, not just
`transitional` and `brownfield`. MSVC 6.0 era (SPEClient) codebases need characterization tests
before any modernization touch.

### 3.2 GAP-AA2: JNI Thread Safety

See Section 2.3 above for the full `std::atomic` analysis.

| Example | Min Standard | C++03 variant needed? | CWR usable today? |
|---|---|---|---|
| Anti-patterns (`static JNIEnv*`, `std::atomic<JNIEnv*>`) | 98/11 (in comments) | N/A — these are NON-COMPLIANT examples | ✅ YES (documentation) |
| C++98 POSIX RAII (`pthread_key_t` destructor) | C++98 | **Yes — primary C++98 path** | ✅ YES |
| C++11 `thread_local` attachment tracker | C++11 ★ | No — C++11 upgrade from above | ✅ YES (C++14 compiler) |
| C++14 `unique_ptr` scoped RAII wrapper | C++14 ★★ | No — natural upgrade | ✅ YES (native) |
| `GlobalRef` lifecycle with RAII | C++98 | Yes | ✅ YES |

**Verdict:** `cpp_version_min: 98`. The C++11 `thread_local` variant is the recommended path
for CWR developers — they compile C++14 and can use it without any toolchain changes. The
C++03-idiom style constraint does not prohibit new C++11 keywords in targeted new code.

### 3.3 GAP-AA3: MFC Integration Patterns

**MFC baseline:** MFC classes predate C++98; `CObject`/`CWinThread`/`CRITICAL_SECTION` are
Win32 API wrappers. No C++ standard requirement from MFC itself.

| Example | Min Standard | C++03 variant needed? | CWR/IOC_ALP usable today? |
|---|---|---|---|
| `CString` ↔ `std::string` interop | C++98 | **Yes — CObject's `GetString()` + `std::string(s)` | ✅ YES |
| `CRITICAL_SECTION` manual RAII guard (C++98) | C++98 | **Yes — IOC_ALP has C++03 idiom code** | ✅ YES |
| `CRITICAL_SECTION` with `std::lock_guard` adapter | C++11 ★ | No | ✅ YES (C++14 compiler) |
| Smart pointer interop with MFC `CObject` | C++11 ★ | Yes — `CObject` uses message heap alloc | ✅ YES with caveats |
| `PostMessage` / `SendMessage` thread safety | C++98 | Yes | ✅ YES |

**Critical note:** `std::shared_ptr<CObject-derived>` is dangerous because MFC objects carry
COM-style reference semantics via `AFX_MANAGE_STATE` and frame-managed heap. The example must
include a specific warning section: *"DO NOT wrap CObject-derived classes in std::shared_ptr.
Use raw pointers managed by MFC's frame-window lifecycle, or extract to a non-CObject wrapper
first."*

**Verdict:** `cpp_version_min: 98`. C++03-safe variants are needed for the lock guard section.
Both variants must be demonstrated because IOC_ALP's `idiom_level` is effectively C++03 for
its legacy modules even if the compiler is C++14.

### 3.4 GAP-AA4: FICO Xpress Solver Integration

**Xpress baseline:** FICO Xpress Optimizer is a C API (`xprs.h`). Thread model: one `XPRSenv`
global; per-thread `XPRSprob` instances. Callbacks invoked from solver thread, not calling
thread.

| Example | Min Standard | C++03 variant needed? | CWR usable today? |
|---|---|---|---|
| `XPRSprob` lifecycle (create/destroy RAII) | C++98 | **Yes** | ✅ YES |
| Callback reentrancy guard (manual flag, C++98) | C++98 | **Yes** | ✅ YES |
| Callback reentrancy with `std::atomic<bool>` (C++11) | C++11 ★ | No | ✅ YES (C++14 compiler) |
| Thread-local `XPRSprob` per solve thread | C++98 (`__declspec(thread)`) / C++11 (`thread_local`) | Yes | ✅ YES |
| Exception barrier at solver boundary | C++98 | **Yes — solver C callbacks cannot propagate C++ exceptions** | ✅ YES |

**Critical correctness note for the exception barrier:** FICO Xpress callbacks cross a C/C++
ABI boundary. C++ exceptions thrown inside a solver callback are undefined behavior (they
cross the C frame, which has no unwind tables). The example MUST demonstrate:

```cpp
// Exception barrier — REQUIRED at all Xpress callback entry points
int XPRS_CC solverCallback(XPRSprob prob, void* userData) {
    try {
        return doActualWork(prob, userData);
    } catch (const std::exception& e) {
        // Log, set error flag — do NOT rethrow
        static_cast<SolverContext*>(userData)->setError(e.what());
        return 1; // solver-level error code
    } catch (...) {
        static_cast<SolverContext*>(userData)->setUnknownError();
        return 1;
    }
}
```

This pattern is C++98-safe and must be the default example. The C++11 variant can use
`std::atomic<bool>` for the error flag.

**Verdict:** `cpp_version_min: 98`. C++03-safe variants required for RAII wrapper and
callback guard. The exception barrier is non-negotiable safety content with no standard
dependency.

---

## Section 4: C++20 Priority Reassessment

### 4.1 The Reachability Gap

The routing system prevents C++20 content from reaching sub-C++20 tiers. Since zero percent
of AA's current C++ LOC is C++20:

| Gap | Current Priority | Reachable by AA LOC? | Recommended Priority |
|---|---|---|---|
| GAP-20-1: C++20 Modules | P1 (greenfield only) | ~0% — already gated | Keep P1-greenfield; add CMake gate |
| GAP-20-2: Ranges/views | P1 | ~0% without bridge split | P1 with bridge, but SPLIT required |
| GAP-20-3: std::format | P1 | ~0% without bridge split | P1 with bridge, but SPLIT required |
| GAP-20-4: Spaceship operator | P1 | ~0% | **Demote to P3** (see 4.3) |
| GAP-20-5: std::span | P1 | ~0% native; GSL available at C++14 | P1 but add GSL polyfill path |
| GAP-20-11: Calendar/timezone | P1 | ~0% native; partial chrono at C++14 | Keep P1 — FAR 117 legal obligation |

### 4.2 Are These P1 for the Wrong Reason?

GAP-20-2 (ranges), GAP-20-3 (std::format), and GAP-20-5 (std::span) are P1 for the RIGHT
reason — but they're labelled as "C++20 features" when they should be labelled as
"available now via bridge library for C++14 teams, natively at C++20." The P1 priority is
justified by the developer benefit; the gap is that the proposal assumes the native C++20
path when the bridge path reaches 60% of AA LOC today.

GAP-20-4 (spaceship operator) is P1 for the WRONG reason. The proposal frames it as "needed
for all value types (FlightId, Seat, Route comparisons)." But:

1. CWR's primary domain objects (`CrewNode`, `FlightNode`) are **mutable structs with integer
   return codes** — not value types in the sense that `<=>` applies to
2. IOC_ALP's domain objects are similarly procedural structs
3. The use case for `<=>` at AA is largely greenfield new service design — and there are no
   greenfield C++ services in the AA portfolio today
4. `<=>` requires C++20 with no bridge library alternative

Spaceship operator will be used by 0% of AA's current LOC and teaches patterns that don't
apply to AA's existing domain object design.

### 4.3 Recommended Priority Changes

| Gap | Before | After | Justification |
|---|---|---|---|
| GAP-20-2: Ranges | P1 | **P1 (split: range-v3 C++14 path + std::ranges C++20 path)** | range-v3 reaches 60% of LOC now |
| GAP-20-3: std::format | P1 | **P1 (split: fmtlib C++11 path + std::format C++20 path)** | fmtlib reaches 60%+ of LOC now |
| GAP-20-4: Spaceship | P1 | **P3** | 0% AA LOC is C++20; AA domain objects are not value types |
| GAP-20-5: std::span | P1 | **P1 — add `gsl::span` C++14 polyfill path** | GSL span reaches transitional tier |
| GAP-20-11: Calendar/timezone | P1 | **P1 — add C++14 `<chrono>` partial path** | FAR 117 legal obligation unchanged |

### 4.4 Practical Timeline for CWR and IOC_ALP to Reach C++20

| Repository | Current Blocker | Steps to C++20 | Realistic Timeline |
|---|---|---|---|
| CWR | `nbproject/Makefile-CI-Release.mk` from 2015; GCC version unknown | 1) CMake migration (GAP-AA8), 2) GCC 11+ upgrade, 3) `-std=c++20` flag, 4) Feature adoption | **24–36 months** minimum |
| IOC_ALP | VS2019; MSVC v142 (partial C++20) | 1) VS2022 upgrade (MSVC v143, full C++20), 2) `/std:c++20` flag, 3) Feature audit | **12–18 months** |
| herc-odyssey-linux | C++98 GCC build; C++11 not yet adopted | 1) C++11 migration, 2) C++14 migration, 3) then C++20 | **36–48+ months** |
| SPEClient | MSVC 6.0 — no viable C++20 path | Complete rewrite or retirement | **Indefinite** |

**The proposal should explicitly acknowledge this timeline.** Labelling GAP-20-2 through
GAP-20-5 as P1 without a bridge library path creates a two-year window where the P1 content
is unreachable and developers who try to apply it will fail silently. The routing system
enforces this correctly (blocking C++20 content for `transitional` tier), but the proposal's
priority labels need to reflect the bridge path as the actual near-term P1 value.

---

## Section 5: Bridge Libraries — Split Recommendations

### 5.1 GAP-20-3 (std::format) → Split Required

**fmtlib/fmt** (Victor Zverovich, MIT, 2012) is not merely an alternative to `std::format` —
it IS the reference implementation. The C++20 standard was written from the fmtlib design.
The library supports C++11+ and is used in production at scale.

**Current proposal:** One deliverable `examples/ENG-6.1-std-format.md` labelled as C++20.

**Required split:**

| Sub-gap | ID | Standard | Routing Tier | Priority |
|---|---|---|---|---|
| fmtlib — available now | GAP-20-3a | C++11+ | `transitional` and above | **P1** |
| std::format — C++20 native | GAP-20-3b | C++20 | `greenfield` only | P2 |

**AVATAR-RAG-INDEX.yaml routing change required:**

```yaml
transitional:
  prefer:
    - ...existing...
    - examples/ENG-6.1-fmtlib-formatting.md  # ADD — fmtlib C++11 path (GAP-20-3a)
```

**Frontmatter for the split files:**

`examples/ENG-6.1-fmtlib-formatting.md`:
```yaml
---
cpp_version_min: 11
cpp_version_note: "Uses fmtlib/fmt (Victor Zverovich, MIT, 2012) — the reference
  implementation that became std::format. Available today for C++11+ projects.
  CWR/IOC_ALP: add fmtlib via vcpkg or Conan. See ★ C++20 section for std::format
  (no external dependency)."
avatar: cpp
---
```

`examples/ENG-6.1-std-format.md` (existing, renamed scope):
```yaml
---
cpp_version_min: 20
cpp_version_note: "std::format is a C++20 standard library feature (no external
  dependency). See examples/ENG-6.1-fmtlib-formatting.md for C++11 equivalent."
avatar: cpp
---
```

**Practical gain:** A CWR developer writing a `CrewWatchSolverJNI.cpp` log message today can
use `fmt::format("{}: crew duty {} exceeds rest limit", flightId, dutyHours)` with zero
toolchain changes. This replaces the `snprintf` buffer-overrun vulnerability (ENG-6.5) in the
current codebase. That is a P1 security improvement available today — not in 24 months.

### 5.2 GAP-20-2 (Ranges) → Split Required

**ericniebler/range-v3** (Eric Niebler, Boost Software License, 2013) is the reference
implementation of C++20 ranges. It requires C++14. CWR and IOC_ALP developers can use it today.

**Current proposal:** One deliverable `examples/ENG-3.1-ranges-views.md` labelled as C++20.

**Required split:**

| Sub-gap | ID | Standard | Routing Tier | Priority |
|---|---|---|---|---|
| range-v3 — available now | GAP-20-2a | C++14+ | `transitional` and above | **P1** |
| std::ranges — C++20 native | GAP-20-2b | C++20 | `greenfield` only | P2 |

**Practical gain for CWR:** A C++14 flight data pipeline that currently uses raw loops over
`std::vector<FlightNode*>` can be rewritten using range-v3 views:

```cpp
// range-v3 example (C++14 — available to CWR today):
// Adapted from: ericniebler/range-v3/test/algorithm/*.cpp (Boost Software License, 2013)
// Authors: Eric Niebler
#include <range/v3/view/filter.hpp>
#include <range/v3/view/transform.hpp>

auto activeFlights = flights
    | ranges::views::filter([](const FlightNode* f) { return f->isActive(); })
    | ranges::views::transform([](const FlightNode* f) { return f->flightId(); });
```

This pattern is available TODAY without a toolchain upgrade. The C++20 native equivalent
(`std::views::filter`) can replace it in place when the compiler is upgraded.

**Frontmatter for the split files:**

`examples/ENG-3.1-range-v3-pipeline.md`:
```yaml
---
cpp_version_min: 14
cpp_version_note: "Uses ericniebler/range-v3 (Eric Niebler, Boost Software License, 2013)
  — the reference implementation that became std::ranges. Available for C++14+ projects
  via vcpkg or Conan. See ★ C++20 section for std::ranges (no external dependency)."
avatar: cpp
---
```

**AVATAR-RAG-INDEX.yaml routing change:**

```yaml
transitional:
  prefer:
    - ...existing...
    - examples/ENG-3.1-range-v3-pipeline.md   # ADD — range-v3 C++14 path (GAP-20-2a)
    - examples/ENG-6.1-fmtlib-formatting.md   # ADD — fmtlib C++11 path (GAP-20-3a)
    - refs/legacy/ref-brownfield-survival.md   # ADD — JNI/MFC/Xpress (GAP-AA1–AA4)
```

### 5.3 GAP-20-5 (std::span) → GSL Polyfill Path

`microsoft/GSL` (MIT) provides `gsl::span` at C++14. The GSL span is the direct predecessor
of `std::span`. The governance difference is minimal.

**Required addition to GAP-20-5 scope:**
> Add a `gsl::span` section marked `★ C++14` to `examples/ENG-6.1-span-bounds-safety.md`.
> Add `examples/ENG-6.1-span-bounds-safety.md` to `transitional` tier prefer list with
> `cpp_version_min: 14` (gsl::span section) and `★ C++20` on native `std::span` section.

---

## Section 6: Required Changes to the Proposal

### 6.1 Blocking — Must Fix Before Any ESE Task Begins

These changes gate the routing system's ability to deliver ESE content to the teams who need it:

| # | Change | Gap(s) | Effort |
|---|---|---|---|
| **R6-V-01** | Add `refs/legacy/ref-brownfield-survival.md` to `transitional` AND `brownfield` tier `prefer` lists in `AVATAR-RAG-INDEX.yaml` | GAP-AA1–AA8 | Low (YAML edit) |
| **R6-V-02** | Add `refs/legacy/ref-brownfield-survival.md` to `legacy` tier `prefer` list (for GAP-AA1 characterization testing) | GAP-AA1 | Low |
| **R6-V-03** | Set `cpp_version_min: 98` on `ref-brownfield-survival.md` with `★ C++11`/`★★ C++14` section markers | All ESE-A gaps | Low |
| **R6-V-04** | Split GAP-20-3 into GAP-20-3a (fmtlib C++11) and GAP-20-3b (std::format C++20); create separate example files; add GAP-20-3a to `transitional` prefer list | GAP-20-3 | Medium |
| **R6-V-05** | Split GAP-20-2 into GAP-20-2a (range-v3 C++14) and GAP-20-2b (std::ranges C++20); create separate example files; add GAP-20-2a to `transitional` prefer list | GAP-20-2 | Medium |
| **R6-V-06** | Add `gsl::span` C++14 polyfill section to `examples/ENG-6.1-span-bounds-safety.md`; set `cpp_version_min: 14`; add to `transitional` prefer list | GAP-20-5 | Medium |
| **R6-V-07** | Demote GAP-20-4 (spaceship operator) from P1 to P3 with rationale: 0% AA LOC is C++20; AA domain objects are not value types that benefit from `<=>` | GAP-20-4 | Low |
| **R6-V-08** | Add `cpp_version_min: 98` frontmatter to all ESE-A example files (JNI, MFC, Xpress, characterization); add `★ C++11` markers on modern variant sections | All ESE-A | Low |

### 6.2 Required — Before Phase 1 Execution

| # | Change | Gap(s) | Effort |
|---|---|---|---|
| **R6-V-09** | Add `ref-concurrency-advanced.md` to `transitional` tier `prefer` list (memory ordering GAP-C1 is applicable to C++11 atomics); set `cpp_version_min: 11` with `★ C++17` on jthread/scoped_lock sections | GAP-C1 through GAP-C8 | Low + Medium |
| **R6-V-10** | Add C++20 timeline section to PROPOSAL.md: document that CWR is 24–36 months from C++20; IOC_ALP is 12–18 months; greenfield content prioritisation must account for this | Proposal metadata | Low |
| **R6-V-11** | Add `READING-PATHS.md` (R6 prior finding, confirmed): "If CWR → start with [brownfield-survival, concurrency-brownfield, characterization-test]" | Navigation | Low |
| **R6-V-12** | For GAP-AA4 (FICO Xpress): add non-negotiable exception barrier example (`try/catch` at C API boundary) with `cpp_version_min: 98`; this is a safety-critical pattern with no standard dependency | GAP-AA4 | Medium |
| **R6-V-13** | For GAP-AA2 (JNI): add C++98 POSIX `pthread_key_t` variant for herc-odyssey-linux (`brownfield` tier); do not assume `thread_local` availability | GAP-AA2 | Medium |
| **R6-V-14** | Add chrono partial path for GAP-20-11 (FAR 117): C++14 `<chrono>` can represent UTC durations but not IANA timezone databases; example must clarify that `std::chrono::zoned_time` requires C++20 and document the Howard Hinnant `date` library as a C++14 bridge for timezone-correct rest arithmetic | GAP-20-11 | Medium |

### 6.3 Recommended — Before Phase 2 Execution

| # | Change | Gap(s) | Effort |
|---|---|---|---|
| **R6-V-15** | For GAP-AA3 (MFC): add explicit `// DO NOT use std::shared_ptr<CObject-derived>` warning with AFX frame lifecycle explanation | GAP-AA3 | Low |
| **R6-V-16** | For all ESE-A files: add `<!-- triggers: JNI, AttachCurrentThread, CrewWatchSolverJNI, MFC, FICO Xpress, XPRSprob, RCPtr, characterization test -->` heading convention per R4's trigger-phrase requirement | All ESE-A | Low |
| **R6-V-17** | Increase token budget for `ref-concurrency-advanced.md` to 1,200–1,500 tokens as previously recommended; the memory ordering (all 5 orders + happens-before graph) cannot be covered adequately in 700 tokens | GAP-C1 | Low (YAML token estimate) |

---

## Updated Verdict

### Prior R6 Verdict (REVIEW-PANEL.md)

> ⚠️ **Significant reorientation needed.** ESE-A (Brownfield Survival Pack) must precede Phase 1.
> JNI gap is the most dangerous unaddressed item.

### Updated R6 Verdict (Version-Sensitivity Review)

> ⚠️ **ESE-A routing is not wired. Bridge library paths are unrouted. C++20 priorities need
> recalibration. Do not execute Phase 1 until routing changes R6-V-01 through R6-V-08 are
> applied.**

The ESE proposal's content is sound. The gaps are real. The OSS derivation chain is correct.
What is missing is the routing wiring that connects ESE deliverables to the teams who need them.

The five-tier version routing system solved the problem of "wrong guidance reaching wrong teams."
The ESE proposal, as currently specified, will recreate that same problem for its own content:

- `ref-brownfield-survival.md` reaches zero AA teams by default
- `ref-concurrency-advanced.md` reaches zero AA teams by default
- `ref-cpp20-features.md` correctly reaches zero AA teams by default — because zero AA teams are C++20

The only ESE content that would route correctly today is whatever lands in `transitional` tier's
three existing prefer-list entries. None of the new ESE deliverables are in those entries.

This is an 8-line YAML change to fix the routing (R6-V-01 through R6-V-03). The bridge library
splits (R6-V-04 through R6-V-06) are medium-effort but unlock the highest-priority P1 content
for 60% of AA's LOC immediately. The spaceship operator demotion (R6-V-07) corrects a priority
misjudgement that would route C++20 theory content to developers who write mutable int-returning
structs in C++03 idioms.

**Fix the routing wiring. Ship ESE-A. Then execute the bridge splits. Then Phase 1.**

Everything else can follow the existing execution order.

---

*This review was conducted in the role of R6 — Senior AA Engineer, with specific focus on the
version-sensitive routing system introduced after the original review panel. Findings in this
document supersede R6's prior routing opinions where they conflict. Findings from the original
R6 review (REVIEW-PANEL.md §R6) and OSS response (R6-OSS-RESPONSE.md) remain valid and
are incorporated by reference here.*

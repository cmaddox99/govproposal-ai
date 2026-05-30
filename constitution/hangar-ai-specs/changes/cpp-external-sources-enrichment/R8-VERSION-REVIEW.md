# R8 — Cross-Version Completeness Auditor: Version-Sensitivity Review of ESE Proposal

**Reviewer:** R8 — Cross-Version Completeness Auditor  
**Proposal:** C++ Avatar Enrichment — External Sources Gap Analysis (`cpp-external-sources-enrichment`)  
**Review Type:** Cross-version coverage equivalence audit  
**Date:** 2026-04-24  
**Status:** FORMAL REVIEW — AMENDMENTS REQUIRED  

---

## Executive Finding

**The ESE proposal is systematically and materially skewed toward modern C++ (C++17/20+), with the
skew concentrated precisely where it does the most damage: in the P1 priority tier.**

Six of the sixteen P1 gaps deliver their primary value to the `greenfield` tier (C++20+), which
represents approximately **0% of AA's current production C++ LOC**. The transitional tier
(C++11/14, **60% of LOC**) is treated as a pass-through — it receives routing to existing refs
but is addressed by fewer than half the ESE gaps and receives no equivalent-functionality guidance
for the same developer problems that modern tiers receive in full.

The three highest-severity individual failures are:

1. **GAP-20-11 (FAR 117 timezone arithmetic) is P1-rated as a legal compliance obligation, yet
   the proposed solution (`std::chrono::zoned_time`) requires C++20 and delivers zero usable
   guidance to the 35% of AA LOC at legacy/brownfield tiers — including CWR itself (C++98),
   the primary system implementing FAR 117.** The legal obligation exists at every tier; the
   guidance exists only at one.

2. **The Brownfield Survival Pack (GAP-AA1–AA4) — ordered first by R6 specifically because it
   serves AA's actual production codebase — implicitly requires C++11 for its key patterns**
   (atomic-based RAII in GAP-AA2, GoogleTest in GAP-AA1, MSVC C++11+ for GAP-AA3). CWR, the
   primary system the pack is written for, is C++98.

3. **GAP-CG3 (Rule of Zero/Five), rated P1 as "fundamental AA C++ correctness gap," does not
   acknowledge that for pre-C++11 codebases the correct rule is the Rule of Three.** Serving
   Rule of Five guidance to a C++98 developer introduces move-semantics content that will
   not compile and misrepresents the actual governance requirement.

**Verdict: AMENDMENTS REQUIRED before the ESE proposal proceeds to Phase 1 execution.** The
Brownfield Survival Pack (ESE-A) and three specific gap files must be revised to add tier-split
or tier-conditional content before execution begins.

---

## Section 1: Full Gap-by-Gap Cross-Version Coverage Matrix

Coverage ratings per tier:
- **Covered**: substantive guidance exists or is proposed for this tier
- **Partial**: some guidance but missing key idioms for that tier
- **None**: no guidance at all for this tier
- **N/A**: concept genuinely does not apply at this version
- **⚠ Skewed**: rich modern coverage, sparse legacy/transitional for the SAME problem

### 1.1 Concurrency Gaps (GAP-C1 through GAP-C10)

| Gap | Priority | Legacy (pre-98) | Brownfield (98/03) | Transitional (11/14) | Modern (17) | Greenfield (20+) | Balance |
|-----|----------|---|---|---|---|---|---|
| GAP-C1 Memory ordering (happens-before, all 5 orders) | P1 | None | Partial¹ | Covered | Covered | Covered | ⚠ Skewed |
| GAP-C2 Parallel algorithms (std::execution policies) | P1 | N/A | N/A | None² | Covered | Covered | ⚠ Skewed |
| GAP-C3 std::jthread + std::stop_token | P2 | N/A | N/A | Partial³ | N/A | Covered | ⚠ Skewed |
| GAP-C4 Condition variable (wait-with-predicate) | P2 | Covered⁴ | Covered⁴ | Covered | Covered | Covered | Balanced |
| GAP-C5 Lock-free data structures | P2 | N/A | None⁵ | Partial⁶ | Partial⁶ | Covered | ⚠ Skewed |
| GAP-C6 Thread pool / work-stealing | P2 | N/A | N/A | None⁷ | None⁷ | Covered | ⚠ Skewed |
| GAP-C7 False sharing (alignas, cache line padding) | P2 | None⁸ | None⁸ | Covered | Covered | Covered | ⚠ Skewed |
| GAP-C8 std::promise/std::future deep patterns | P2 | N/A | N/A | Covered | Covered | Covered | Balanced |
| GAP-C10 CP.42/43/50 (wait-predicate, critical section, mutex+data) | P2 | Partial⁹ | Partial⁹ | Covered | Covered | Covered | Partial |

**Notes:**  
¹ `ref-concurrency-brownfield.md` covers the `volatile` pitfall and POSIX mutex RAII, but has
no treatment of memory ordering semantics with pre-C++11 compiler intrinsics (`__sync_*`,
`MemoryBarrier()`). C++98 developers on multi-core systems have the same ordering problem
— only their API is different. Proposed `ENG-6.1-memory-ordering.md` will be `cpp_version_min: 11`.  
² `std::execution` policies are C++17+. For C++11/14 (60% of LOC), the equivalent
parallelism path is manual `std::thread` decomposition or `std::async` batching.
No equivalent-functionality path is proposed.  
³ C++14-compatible migration path: `std::thread` + `std::atomic<bool>` stop flag.
The proposed example targets C++20 `jthread`/`stop_token`. A C++14 developer migrating
from raw thread teardown has no guidance on the canonical pre-C++20 stop-token idiom.  
⁴ `ref-concurrency-brownfield.md` explicitly covers `pthread_cond_t` with predicate loop.
⁵ Pre-C++11 lock-free patterns require compiler intrinsics. No guidance exists or is proposed.  
⁶ C++11 provides `std::atomic`, making basic lock-free operations achievable. The proposed
Boost.Lockfree derivation requires C++11. ABA prevention patterns via epoch-based reclamation
work on C++11+ but this is not called out.  
⁷ The proposed OSS sources (taskflow, bshoshany) require C++17+. No C++11/14 thread-pool
pattern is proposed. For CWR-era code, even a basic fixed-size thread pool pattern
using `std::thread` + `std::queue` + `std::condition_variable` is absent.  
⁸ `alignas` requires C++11. `__declspec(align)` / `__attribute__((aligned))` are the C++98
equivalents; neither is mentioned in any proposed content.  
⁹ The CP.42/43/50 rules conceptually apply to POSIX mutexes too. `ref-concurrency-brownfield.md`
covers POSIX mutex RAII (CP.50 analog) but does not explicitly map CP.42/43/50 rule IDs.

---

### 1.2 Template Gaps (GAP-T1 through GAP-T7)

| Gap | Priority | Legacy (pre-98) | Brownfield (98/03) | Transitional (11/14) | Modern (17) | Greenfield (20+) | Balance |
|-----|----------|---|---|---|---|---|---|
| GAP-T1 CRTP (static polymorphism) | P1 | Partial¹⁰ | Partial¹⁰ | Covered | Covered | Covered | ⚠ Routing gap |
| GAP-T2 Type traits systematic reference | P2 | N/A | N/A | Covered | Covered | Covered | Balanced for applicable tiers |
| GAP-T3 Tag dispatching (reading legacy) | P3 | Covered | Covered | Covered | N/A | N/A | Balanced |
| GAP-T4 Policy-based design | P3 | Covered¹¹ | Covered¹¹ | Covered | Covered | Covered | Balanced |
| GAP-T5 Expression templates (note only) | P3 | N/A | N/A | Covered | Covered | Covered | Acceptable |
| GAP-T6 NTTPs (basic/advanced) | P3 | Partial¹² | Partial¹² | Partial¹² | Partial¹² | Covered | ⚠ Skewed |
| GAP-T7 Advanced concepts | P2 | N/A | N/A | N/A | N/A | Covered | N/A (C++20 only — balanced) |
| GAP-CG12 Deducing this (C++23) | P2 | N/A | N/A | N/A | N/A | Covered | N/A (C++23 only — balanced) |

**Notes:**  
¹⁰ CRTP is a C++98 pattern — it predates `std::enable_if` and has been used to eliminate
virtual dispatch in constrained-resource systems since the early 2000s. SPEClient (24% of LOC,
pre-C++98) and herc-odyssey-linux (11%, C++98/03) would benefit directly from CRTP guidance.
**However, the proposed `ENG-3.1-crtp.md` is not added to the `brownfield` or `legacy` tier
`prefer` lists in `AVATAR-RAG-INDEX.yaml`, so these developers will not be routed to it.**
The routing gap is the critical failure, not the content itself.  
¹¹ Policy-based design works in C++98. The proposed `ENG-3.1-policy-based-design.md` will
likely target C++11+ (`cpp_version_min: 11`) but the technique is applicable to C++98/03
with minor adjustment.  
¹² Basic NTTPs (integral, pointer types) are C++98. Floating-point and string-literal NTTPs
are C++20. The proposed enhancement conflates them — no tier split is shown.

---

### 1.3 C++20 Feature Gaps (GAP-20-1 through GAP-20-13)

| Gap | Priority | Legacy (pre-98) | Brownfield (98/03) | Transitional (11/14) | Modern (17) | Greenfield (20+) | Balance |
|-----|----------|---|---|---|---|---|---|
| GAP-20-1 C++20 Modules | P1 (greenfield only) | N/A | N/A | N/A | N/A | Covered | Balanced (explicit scope) |
| GAP-20-2 Ranges and views pipelines | P1 | N/A | N/A | None¹³ | Partial¹³ | Covered | ⚠ Skewed |
| GAP-20-3 std::format | P1 | Partial¹⁴ | Partial¹⁴ | Partial¹⁴ | Partial¹⁴ | Covered | ⚠ Skewed |
| GAP-20-4 Three-way comparison (spaceship) | P1 | N/A | N/A | None¹⁵ | None¹⁵ | Covered | ⚠ Skewed |
| GAP-20-5 std::span (bounds-safe array view) | P1 | N/A | N/A | None¹⁶ | None¹⁶ | Covered | ⚠ Skewed |
| GAP-20-6 std::bit_cast | P2 | N/A | N/A | None¹⁷ | None¹⁷ | Covered | ⚠ Skewed |
| GAP-20-7 std::source_location | P2 | None¹⁸ | None¹⁸ | None¹⁸ | None¹⁸ | Covered | ⚠ Skewed |
| GAP-20-8 constinit | P2 | N/A | N/A | N/A | N/A | Covered | N/A (C++20 only — balanced) |
| GAP-20-9 Coroutine generators (co_yield) | P2 | N/A | N/A | N/A | N/A | Covered | N/A (C++20 only — balanced) |
| GAP-20-10 std::atomic_ref | P2 | N/A | N/A | N/A | N/A | Covered | N/A (C++20 only — balanced) |
| GAP-20-11 C++20 Calendar / timezone | **P1** | **None¹⁹** | **None¹⁹** | **None¹⁹** | **None¹⁹** | Covered | **🚨 CRITICAL SKEW** |
| GAP-20-12 C++20 Lambda improvements | P3 | N/A | N/A | N/A | N/A | Covered | N/A (C++20 — balanced) |
| GAP-20-13 C++20 Aggregate improvements | P3 | N/A | N/A | Partial | Partial | Covered | Acceptable |

**Notes:**  
¹³ Ranges/views are C++20. For C++11/14 (60% of LOC), the equivalent of a ranges pipeline is
`std::sort` + `std::copy_if` + `std::transform` with functors or lambdas. No equivalent
guidance proposed. For read-only data pipelines on flight manifests, a C++14 developer needs
iterator-based composition patterns, not a C++20 ref.  
¹⁴ `ENG-6.1-format-string-safety.md` exists at `cpp_version_min: 98` and partially covers the
underlying problem. However, it focuses on injection safety (`%s` misuse), not on the broader
format-string governance and replacement path. The proposed `ENG-6.1-std-format.md` will be
`cpp_version_min: 20`. No C++11/14 equivalent showing the safe `ostringstream`/`snprintf`
governance pattern alongside C++20 `std::format` is proposed as a paired deliverable.  
¹⁵ For C++11/14, ordering is achieved by manually providing `operator<`, `operator==`, etc.
No guidance on the exhaustive comparison operator pattern for value types (FlightId, Seat)
on pre-C++20 tiers. `ENG-3.1-comparison-operators.md` exists at `cpp_version_min: 98` — but
covers basic patterns only, not the full governance for value type ordering at each tier.  
¹⁶ For C++11/14, the `std::span` equivalent is GSL `gsl::span`, or a raw `{ptr, size}` pair
with explicit API documentation. No equivalent-functionality guidance proposed.  
¹⁷ For pre-C++20, type punning is done via `memcpy` + `reinterpret_cast` (with strict-aliasing
warnings). `ENG-6.1-strict-aliasing.md` exists at `cpp_version_min: 11` and partially covers
this. The proposed `GAP-20-6` guidance for C++20 `std::bit_cast` should cross-reference
the C++11 `memcpy`-based safe alternative.  
¹⁸ Pre-C++20 structured logging uses `__FILE__`, `__LINE__`, `__PRETTY_FUNCTION__` macros. The
proposed `ENG-5.5-source-location.md` (C++20 only) does not describe the canonical macro-based
pattern for all older tiers. `ENG-6.7-audit-trail.md` and `ENG-5.5-observability.md` exist but
do not provide a multi-tier treatment.  
¹⁹ **CRITICAL.** FAR 117 is cited as the legal rationale for the P1 upgrade of this gap. CWR
(`CrewRecoveryFAR117`) is C++98. The legacy and brownfield tiers ARE the primary FAR 117
implementation systems today. Yet the proposed `ref-cpp20-features.md` section on C++20
calendar/timezone provides guidance exclusively for `std::chrono::zoned_time` (C++20).  
Pre-C++20 FAR 117 timezone arithmetic uses `localtime_r()`, `gmtime_r()`, `mktime()`, UTC
offset tables, and DST offset tables — all POSIX C APIs callable from C++98. The `ref-safety-far117-cwr.md` (v98) covers FAR 117 characterization testing but has **zero timezone
arithmetic guidance**. This combination — P1 priority on legal grounds, ZERO guidance for
the tiers actually implementing the law — is the most severe cross-version skew in the proposal.

---

### 1.4 Core Guidelines Gaps (GAP-CG1 through GAP-CG11)

| Gap | Priority | Legacy (pre-98) | Brownfield (98/03) | Transitional (11/14) | Modern (17) | Greenfield (20+) | Balance |
|-----|----------|---|---|---|---|---|---|
| GAP-CG1 Interface design (I.11, I.12, Expects/Ensures) | P1 | Partial²⁰ | Partial²⁰ | Covered | Covered | Covered | Acceptable |
| GAP-CG2 Parameter passing table (F.16–F.20) | P2 | Partial²¹ | Partial²¹ | Covered | Covered | Covered | Acceptable |
| GAP-CG3 Rule of Zero/Five (C.20/C.21) | P1 | None²² | None²² | Partial²² | Covered | Covered | ⚠ Skewed |
| GAP-CG4 Regular types / value semantics (C.11) | P2 | Partial²³ | Partial²³ | Covered | Covered | Covered | Acceptable |
| GAP-CG5 Avoid unnecessary copies (Per.xx) | P2 | N/A | N/A | Covered | Covered | Covered | Balanced |
| GAP-CG6 SL.xx / string_view governance | P2 | N/A | N/A | Partial²⁴ | Covered | Covered | Partial |
| GAP-CG7 CPL.xx C-style programming | P3 | Covered | Covered | Covered | Covered | Covered | Balanced |
| GAP-CG8 Source file organization (SF.xx) | P2 | Partial | Partial | Covered | Covered | Covered | Acceptable |
| GAP-CG9 GSL Profiles (Pro.xx) | P3 | None | None | Partial | Covered | Covered | ⚠ Skewed |
| GAP-CG10 CP.42/43/50 (see GAP-C10) | P2 | Partial | Partial | Covered | Covered | Covered | Partial |
| GAP-CG11 std::string_view lifetime traps | P1 | None²⁵ | None²⁵ | None²⁵ | Covered | Covered | **⚠ Critical skew** |

**Notes:**  
²⁰ `gsl::not_null` requires C++11. For C++98, the I.11 principle (no raw pointer ownership
transfer) is enforced by naming conventions and code review, not types. The proposed `ref-core-language.md` enhancement should acknowledge this and provide a C++98-compatible enforcement approach.  
²¹ Pre-C++11, "in-out" parameters use raw pointers; const references for "in." The table still
applies conceptually but with different vocabulary.  
²² **CRITICAL for P1 gap.** The "Rule of Zero / Rule of Five" framing is C++11+. For C++98/03
codebases, the applicable concept is the **Rule of Three** (destructor, copy constructor, copy
assignment operator). Move constructor and move assignment operator do not exist in C++03.
A CWR (C++98) developer reading Rule of Five guidance will find 40% of the content (move
operations) completely inapplicable, with no warning. The proposed section should include a
`## Rule of Three ★ C++98/03` subsection explicitly for brownfield and legacy tiers.  
²³ "Regular type" in C++98 is equality-comparable, copyable, default-constructible, and
swappable. The `std::swap` specialization requirement is a C++98 concern. The C++11 addition
is movability. The section should tier-split: C++98 regular type requirements vs. C++11 full
regular type requirements.  
²⁴ `std::string_view` is C++17. For C++11/14 (60% of LOC), the equivalent governance concept
is `const std::string&` vs. raw `const char*` parameter passing rules. No guidance proposed.  
²⁵ **`const char*` dangling pointer traps are the C++98/03 equivalent of `string_view` lifetime
traps.** Returning `c_str()` of a `std::string` that goes out of scope, holding a pointer into
a `std::string` that gets reallocated — these are exactly the same class of bug at the brownfield
tier. The proposed section addresses only C++17+ `string_view`. Legacy/brownfield developers
facing the same crash pattern get zero guidance. A tier-split section (`## const char* Lifetime
Traps ★ pre-C++17`) would close this gap with minimal effort.

---

### 1.5 AA Brownfield Gaps (GAP-AA1 through GAP-AA8)

| Gap | Priority | Legacy (pre-98) | Brownfield (98/03) | Transitional (11/14) | Modern (17) | Greenfield (20+) | Balance |
|-----|----------|---|---|---|---|---|---|
| GAP-AA1 Characterization testing | P1 | None²⁶ | Partial²⁶ | Covered | Covered | Covered | ⚠ Skewed |
| GAP-AA2 JNI thread safety | P1 | N/A | None²⁷ | Partial²⁷ | Covered | Covered | **⚠ Critical skew** |
| GAP-AA3 MFC integration patterns | P1 | Partial²⁸ | Partial²⁸ | Covered | Covered | N/A | Partial |
| GAP-AA4 FICO Xpress solver integration | P1 | None²⁹ | None²⁹ | Covered | Covered | N/A | Partial |
| GAP-AA5 CMake migration from legacy | P2 | Covered | Covered | Covered | Covered | Covered | Balanced |
| GAP-AA6 RCPtr legacy reference counting | P2 | Covered | Covered | Covered | Covered | N/A | Balanced |
| GAP-AA7 Resource Handle Pattern (pre-RAII) | P2 | Covered | Covered | Covered | Covered | N/A | Balanced |
| GAP-AA8 Legacy serialization migration | P3 | Covered | Covered | Covered | Covered | N/A | Balanced |

**Notes:**  
²⁶ The existing `ENG-4.1-characterization-test-pattern.md` has `cpp_version_min: 11` because
it uses GoogleTest. GoogleTest requires C++11 (`std::tuple`, variadic templates). CWR and
SPEClient are C++98. The proposed `ref-brownfield-survival.md` does not address characterization
testing in codebases without a C++11-capable compiler. For C++98-only codebases, the "golden
master" pinning approach requires a custom test harness or the ActiveTest framework (already
referenced in migration docs). This gap should be acknowledged and a C++98-compatible
characterization test pattern (file-comparison golden master, custom assert macros) provided.  
²⁷ **The most actionable version skew in the entire Brownfield Survival Pack.** The proposal
explicitly mentions "std::atomic-based RAII wrapper" for JNI attachment management. `std::atomic`
requires C++11. CWR (`CrewWatchSolverJNI.cpp`) is C++98. A C++98 JNI RAII attachment wrapper
must use a POSIX mutex or Win32 CRITICAL_SECTION to protect thread-local `JNIEnv*` state — not
`std::atomic<JNIEnv*>` (which would also be semantically incorrect: `JNIEnv*` is a thread-local
handle, not a shared atomic state). The existing `ENG-6.1-safety-critical-jni.md` has
`cpp_version_min: 11`. Zero C++98-safe JNI thread safety guidance exists anywhere in the avatar.  
²⁸ MSVC C++11 support was incomplete before Visual Studio 2015 (MSVC v140). The proposal
mentions "MSVC 2015+ supports C++11/14" but does not specify which MSVC version SPEClient or
herc-odyssey-linux uses. SPEClient is identified as "MSVC 6.0 / pre-C++98" — MSVC 6.0 has no
C++11 support whatsoever. MFC guidance that relies on `std::unique_ptr` or `override` will
not compile in MSVC 6.0. The proposal should explicitly mark MFC patterns by minimum MSVC
toolset version, not just C++ standard version.  
²⁹ FICO Xpress exposes a C API; the C++ wrapper layer is version-dependent. If CWR's Xpress
integration uses C++98 conventions, threading guidance based on `std::thread` will be
inapplicable. The proposal does not specify the Xpress integration's target C++ version.

---

## Section 2: Equivalent-Functionality Pair Analysis

The following table maps each modern C++ feature targeted by an ESE gap to the pre-modern idiom
that a legacy/brownfield/transitional developer would use for the **same problem**. For each pair,
the table assesses whether the proposal addresses both sides.

| Modern Feature (Proposed) | Pre-Modern Equivalent | Same Problem | Pre-Modern Addressed? | Gap |
|---------------------------|-----------------------|---|---|---|
| `std::format` (C++20, GAP-20-3) | `printf`/`snprintf`/`ostringstream` | Format string safety | Partial (existing `ENG-6.1-format-string-safety.md` v98, injection focus only) | No governance-equivalent pairing in ESE |
| `std::chrono::zoned_time` (C++20, GAP-20-11) | `localtime_r`/`gmtime_r`/`mktime`/UTC offset tables | Timezone-correct time arithmetic for FAR 117 | **None** | **Critical — legal obligation unaddressed at primary implementation tier** |
| `std::jthread` + `stop_token` (C++20, GAP-C3) | `std::thread` + `std::atomic<bool>` flag (C++11) | Cooperative thread cancellation | None | C++14 developers have no stop-flag governance |
| `std::execution::par` (C++17, GAP-C2) | Manual `std::thread` decomposition / `std::async` | Data parallelism | None | 60% of LOC (C++14) has no parallel path |
| `std::atomic<T>` memory ordering (C++11, GAP-C1) | `__sync_*` / `MemoryBarrier()` / `volatile` pitfall | Multi-core ordering | Partial (`ref-concurrency-brownfield.md` — volatile pitfall only) | No compiler intrinsic ordering guidance |
| `std::hazard_pointer` / Boost.Lockfree (C++11+, GAP-C5) | Hand-rolled lock-free with compiler intrinsics | Lock-free access to shared state | None | Pre-C++11 lock-free has no guidance |
| `std::span` (C++20, GAP-20-5) | GSL `span` / `{ptr, size}` pair (C++11/14) | Bounds-safe buffer passing | None | 60% of LOC has no span-equivalent governance |
| `std::bit_cast` (C++20, GAP-20-6) | `memcpy`-based type punning (C++11+) | Safe type punning for binary parsing | Partial (existing strict-aliasing ref v11) | No explicit C++11/14 paired governance |
| `std::source_location` (C++20, GAP-20-7) | `__FILE__`/`__LINE__`/`__PRETTY_FUNCTION__` macros | Structured logging location | None | All pre-C++20 tiers unaddressed |
| `std::string_view` lifetime (C++17, GAP-CG11) | `const char*` dangling pointer | Pointer/view lifetime safety | None | Same bug class, zero pre-C++17 guidance |
| Rule of Five (C++11+, GAP-CG3) | Rule of Three (C++98) | Special member function completeness | None | C++98 devs receive wrong-version guidance |
| Ranges pipelines (C++20, GAP-20-2) | `std::sort`/`std::copy_if`/`std::transform` chains | Functional data transformation | None | No C++14 algorithm-composition patterns |
| Advanced Concepts (C++20, GAP-T7) | `enable_if` / SFINAE (C++11) | Template constraint enforcement | Covered (`ENG-3.1-sfinae-cpp11.md` v11) | Transitional tier covered — balanced |
| CRTP for static polymorphism (C++98+, GAP-T1) | Virtual dispatch (C++98) | Polymorphic behavior without runtime overhead | Partial (CRTP works C++98, but not routed to legacy/brownfield tier) | Routing gap, not content gap |

**Summary:** Of 14 equivalent-functionality pairs, **8 have no pre-modern coverage** in the
ESE proposal. Of the 3 most safety-critical pairs (timezone/FAR 117, string_view/const-char
lifetime, Rule of Five/Three), **all 3 are unaddressed** at the pre-modern side.

---

## Section 3: Brownfield Survival Pack Cross-Tier Assessment

The R6 reviewer correctly ordered the Brownfield Survival Pack (ESE-A, GAP-AA1–AA4) to execute
**before** Phase 1 (C++20 features). The intent was to serve AA's actual production C++ codebase.
This section assesses whether the pack actually does so across tiers.

### GAP-AA1: Characterization Testing

**What the proposal says:** Michael Feathers' "Pinning Tests" / golden-master approach for
untested C++ code. No existing guidance.

**Cross-tier assessment:**  
The primary target (CWR, C++98/03) CANNOT use GoogleTest without a compiler upgrade. The
existing `ENG-4.1-characterization-test-pattern.md` (`cpp_version_min: 11`) uses `TEST_F`,
`ASSERT_THAT`, and GoogleTest v1.12+ features that require C++11. For a strict C++98 codebase,
characterization testing requires either:
- A custom assert-and-log harness (no C++11 features required)
- The ActiveTest framework (referenced in migration docs, but not shown in a characterization context)
- A file-comparison golden-master pattern using `system()`/`popen()` for output capture

**Finding:** The proposed `ref-brownfield-survival.md` should include a `### Characterization
Testing Without C++11` subsection showing the golden-master file-comparison pattern in raw C++
using `FILE*`/`fopen()`/`fclose()` for codebases that cannot adopt GoogleTest. Without this,
the P1 gap is only partially closed for the primary target.

### GAP-AA2: JNI Thread Safety

**What the proposal says:** `AttachCurrentThread`/`DetachCurrentThread` lifecycle, `JNIEnv*`
thread-local contract, RAII wrapper for JNI attachment. Derive from `android/ndk-samples`
(Apache 2.0). "Common wrong patterns: `static JNIEnv*`, `std::atomic<JNIEnv*>`."

**Cross-tier assessment:**  
The proposal identifies `std::atomic<JNIEnv*>` as a wrong pattern — which is correct. But the
proposed correct pattern (RAII wrapper) is described in terms that imply `std::atomic` for
thread detection. CWR (`CrewWatchSolverJNI.cpp`) is C++98. A C++98-safe RAII JNI attachment
wrapper must use one of:
- A POSIX `pthread_key_t` (thread-local storage) to store the per-thread `JNIEnv*`
- A Win32 `TlsAlloc`/`TlsSetValue`/`TlsGetValue` sequence for the same purpose

Neither pattern is mentioned. The `android/ndk-samples` OSS source uses C++11 (`__thread` or
`thread_local`), not C++98-compatible `pthread_key_t`. The derivation chain leads to C++11+
patterns. A C++98 JNI RAII wrapper is an entirely different implementation.

**Finding:** The proposed `ref-brownfield-survival.md` MUST include a C++98-compatible JNI
attachment pattern using `pthread_key_t` for Linux or `TlsAlloc` for Windows, labeled
`## JNI Thread Safety Without C++11`. The C++11 version (using `thread_local`) should be
presented as the upgrade target.

### GAP-AA3: MFC Integration

**What the proposal says:** No guidance on mixing modern C++ (smart pointers, RAII, `std::string`)
with MFC's `CObject`-derived classes and message maps. CWR UI layer is MFC.

**Cross-tier assessment:**  
The proposal does not specify the MSVC toolset range covered by the MFC guidance.
Key MSVC milestones:
- MSVC 6.0 (Visual C++ 6.0): C++98, no `std::unique_ptr`, no lambda, no `override`
- MSVC 2010 (v100): partial C++11
- MSVC 2013 (v120): better C++11; `std::unique_ptr` available but no `constexpr`
- MSVC 2015 (v140): substantially complete C++11/14

SPEClient is identified as "MSVC 6.0 / pre-C++98." If the MFC integration guidance uses
`std::unique_ptr`, `override`, lambdas, or `std::string::data()` (non-const pre-C++11), it
will not compile in MSVC 6.0. The guidance must explicitly state the minimum MSVC toolset
and provide MSVC 6.0-compatible alternatives where applicable (raw pointer + destructor RAII,
`std::auto_ptr` with explicit caveats, string conversion via `CString::GetBuffer()`).

**Finding:** MFC guidance must include a MSVC toolset matrix analogous to the C++ version tier
system. At minimum, an explicit compatibility header: "This section requires MSVC 2015+ (v140).
For MSVC 2010/2013 or MSVC 6.0, see `### MSVC Pre-2015 Compatibility` subsection."

### GAP-AA4: FICO Xpress Solver Integration

**What the proposal says:** "No guidance on C++ integration patterns for the FICO Xpress
optimizer. Incorrect threading assumptions around solver calls cause deadlocks."

**Cross-tier assessment:**  
The Xpress C API (`XPRSprob`, `XPRSsetcbmessage`, etc.) is version-agnostic C callable from
any C++ standard. The threading concern is which synchronization primitive wraps Xpress calls.
If CWR's Xpress integration layer is C++98, the threading wrapper must use POSIX mutexes or
Win32 CRITICAL_SECTION, not `std::mutex`. The proposal does not specify the target version,
meaning the resulting guidance could be served to C++98 Xpress callers with C++11 patterns.

**Finding:** The Xpress integration section should declare its target C++ version and provide
a version-conditional pattern (POSIX mutex for C++98, `std::mutex` for C++11+).

---

## Section 4: Tier Coverage Completeness Scorecard

### Methodology

- **ESE Gaps Addressed**: Gaps where the ESE proposal adds substantive, tier-appropriate new
  content (not just routing to existing refs that already existed)
- **Existing Ref Coverage**: Refs in the version routing `prefer` list for that tier that address
  the problem domains targeted by ESE gaps
- **Grade**: A = comprehensive, B = mostly covered with minor gaps, C = meaningful gaps present,
  D = significant gaps affecting developer productivity, F = absent

| Tier | LOC% | ESE Gaps Directly Addressed | Existing Ref Coverage (before ESE) | Combined Coverage (after ESE as proposed) | Grade |
|------|------|---|---|---|---|
| **legacy** (pre-C++98) | **24%** | 0 | Strong for navigation/smells/brownfield; weak for domain topics | Legacy gets no new ESE content. FAR 117 timezone, string lifetime traps, memory ordering equivalents, CRTP routing — all absent | **D** |
| **brownfield** (C++98/03) | **11%** | 4 (GAP-AA1–AA4, with C++11 drift) | Good: concurrency brownfield ref, mental models, project config | Brownfield Survival Pack delivers real value but the C++11 assumption in JNI and characterization testing creates a coverage illusion: guidance exists but doesn't compile in the target environment | **C** |
| **transitional** (C++11/14) | **60%** | ~8 (GAP-C1, C4, C8, CG1, CG2, CG3 partial, CG4, AA1–AA4 partial) | Good for core safety/type safety; weak for domain-specific (timezone, format safety, parallelism) | Transitional is the majority tier and the most underserved by the C++20 gaps. Six P1 gaps add zero transitional coverage. FAR 117 timezone and string lifetime are entirely absent | **C** |
| **modern** (C++17) | **5%** | ~14 (majority of ESE gaps apply at C++17+) | Good; existing refs well-matched to C++17 | Well served. Most non-C++20-specific ESE content lands here | **B** |
| **greenfield** (C++20+) | **~0% current** | 20+ (all C++20 gaps) | Thin; `ref-concurrency-coroutines.md`, `ref-core-modern-idioms.md` | Comprehensively covered by ESE. 6 P1 gaps serve this tier exclusively — the most richly served tier for the least deployed standard | **A** |

### Grade Interpretation

| Tier | Grade | Primary Deficiency |
|------|-------|--------------------|
| legacy | **D** | Zero ESE content produced; FAR 117, memory ordering, CRTP routing all absent |
| brownfield | **C** | Brownfield pack has C++11 version drift; Rule of Three absent; C++98 JNI pattern absent |
| transitional | **C** | Six P1 gaps produce zero transitional-applicable content; FAR 117 timezone entirely absent |
| modern | **B** | Well served; minor gaps in equivalent-functionality pairing |
| greenfield | **A** | Comprehensively addressed; over-represented relative to LOC share |

**The proposal receives an overall cross-version completeness grade of C−.**  
The tiers representing 95% of AA's current LOC (legacy + brownfield + transitional) receive
grades of D, C, and C respectively. The tier with 0% current LOC receives an A.

---

## Section 5: Version Ladder Analysis

A well-designed multi-version guidance system provides a **coherent upgrade path**: a C++03
developer who wants to migrate to C++14 should find guidance on the migration steps, not just
the destination.

### Existing Ladder (before ESE)

| Migration Path | Coverage | File |
|---|---|---|
| C++98/03 → C++11 | Excellent | `ref-migration-pre-cpp17.md` (22-step sequence, ABI pitfalls, CI changes) |
| C++11 → C++14 | Good | `ref-migration-pre-cpp17.md` (generic lambdas, `make_unique`) |
| C++14 → C++17 | Good | `ref-migration-pre-cpp17.md` + `ref-migration-cpp17-plus.md` |
| C++17 → C++20 | **Absent** | No migration ladder exists for this step |
| C++20 → C++23 | Absent | No migration ladder needed (so few at C++20 today) |

### ESE Proposal's Contribution to the Ladder

**The ESE proposal adds no migration ladder content.** It creates destination islands:
- `ref-cpp20-features.md` describes what C++20 features are
- `ref-concurrency-advanced.md` describes C++20 concurrency patterns
- `ref-brownfield-survival.md` describes brownfield-to-modern bridges

None of these files are structured as "if you are at C++17, here is the path to C++20 that
applies in your brownfield context." The GAP-AA5 (CMake migration) is the sole exception — it
addresses the build system prerequisite for C++20 Modules adoption — but it is rated P2 despite
being an explicit prerequisite for the highest-value P1 gap (GAP-20-1, Modules).

### Specific Ladder Gaps

**C++17 → C++20 migration ladder is absent.** A C++17 developer (5% of LOC, IOC_ScreenPrinter)
who wants to adopt Ranges, std::format, or std::span has no step-by-step adoption guide analogous
to what `ref-migration-pre-cpp17.md` provides for C++98→C++11. The ESE proposal should include
a `ref-migration-cpp20.md` or a "Adoption Sequence" section in `ref-cpp20-features.md` following
the same safety-first priority sequence established by the existing migration refs.

**The C++14 "why not yet" guide is absent.** For transitional (60% of LOC) developers who
want specific C++20 features but cannot migrate their entire codebase, there is no "feature
availability matrix" explaining which C++20 features can be back-ported via third-party libraries
(e.g., `fmtlib` for C++11, `range-v3` for C++11, `gsl::span` for C++11, `std::experimental::source_location` for C++17). The ESE proposal is structured as binary: either you have C++20 or you
do not. A pragmatic library-based equivalence table would serve 60% of current LOC.

**GAP-AA5 priority inversion.** CMake migration (GAP-AA5, P2) is explicitly named as a
prerequisite for GAP-20-1 (Modules, P1). A prerequisite ranked lower than the thing it enables
is a sequencing error. GAP-AA5 should be promoted to P1 if GAP-20-1 remains P1.

---

## Section 6: Recommendations for Balance

### 6.1 Critical Amendments Required (Must-fix before ESE-A execution)

These amendments are required because the current proposal creates guidance that will produce
incorrect or uncompilable code for the target codebase.

**Amendment R8-1: GAP-AA2 — Add C++98-compatible JNI attachment wrapper**

The `ref-brownfield-survival.md` JNI thread safety section MUST include a C++98-compatible pattern
using `pthread_key_t` for Linux or `TlsAlloc/TlsSetValue/TlsGetValue` for Windows. This is not
optional — CWR's `CrewWatchSolverJNI.cpp` is C++98. Suggested structure:

```
## JNI Thread Safety: Attaching and Detaching Threads
### C++98 Pattern: pthread_key_t for thread-local JNIEnv* (Linux)
### C++98 Pattern: TlsAlloc/TlsSetValue for thread-local JNIEnv* (Windows)  
### C++11+ Pattern: thread_local JNIEnv* with RAII guard  ★ C++11
### Upgrade path: C++98 → C++11
```

**Amendment R8-2: GAP-AA1 — Add C++98 characterization test pattern**

The `ref-brownfield-survival.md` characterization testing section MUST include a golden-master
file-comparison pattern usable without GoogleTest, for C++98 codebases. Suggest deriving from
Michael Feathers' pattern descriptions (paraphrased, not copied) using a raw `FILE*`/`fprintf()`
harness. Label it `### Characterization Testing Without GoogleTest (C++98)`.

**Amendment R8-3: GAP-CG3 — Rule of Three section required**

The `ref-core-language.md` Rule of Zero/Five section MUST include a `## Rule of Three ★ C++98/03`
subsection that:
1. Names the three members (destructor, copy ctor, copy assign) without reference to move operations
2. Provides a C++98-compatible example (e.g., `FlightPlan` with heap-allocated member)
3. Cross-references the Rule of Five as the C++11 extension

**Amendment R8-4: GAP-20-11 — Add pre-C++20 timezone arithmetic for FAR 117**

If this gap retains its P1 priority on FAR 117 legal grounds, the gap MUST produce guidance at
**all tiers** where FAR 117 is implemented. Specifically:
- A new subsection in `ref-safety-far117-cwr.md` (existing, v98) covering safe UTC offset
  arithmetic using `localtime_r()`/`gmtime_r()`/`mktime()` for C++98/03 codebases
- The C++20 `zoned_time` guidance then becomes the upgrade target, not the entire answer

Alternatively, if the gap scope is constrained to C++20 only, it should be **demoted to P2**
(greenfield-only) and a **new P1 gap** — "FAR 117 timezone arithmetic for legacy/brownfield/
transitional tiers" — created and added to the Brownfield Survival Pack.

**Amendment R8-5: GAP-CG11 — Add const char* lifetime trap section**

The `ref-core-language.md` `string_view` lifetime section MUST include a `## const char*
Lifetime Traps ★ pre-C++17` subsection. This requires approximately 200 words and two
NON-COMPLIANT / COMPLIANT example pairs. It closes the identical problem for 35% of AA's LOC.

### 6.2 High-Priority Routing Fixes (Apply before ESE ref files are added to RAG index)

**R8-6: Route CRTP to brownfield and transitional prefer lists**

After creating `ENG-3.1-crtp.md`, add it to the `brownfield` and `transitional` `prefer` lists
in `AVATAR-RAG-INDEX.yaml`. CRTP is a C++98 pattern used precisely in the codebases where
virtual dispatch overhead is highest. Not routing to these tiers defeats the primary use case.

**R8-7: Create a "pre-modern library equivalence" section in `ref-brownfield-survival.md`**

A table mapping C++20 features to their library-based equivalents for C++11/14 codebases:

| C++20 Feature | C++11/14 Library Equivalent | Availability |
|---|---|---|
| `std::format` | `fmtlib` (MIT, the reference implementation) | vcpkg/conan |
| `std::ranges` | `range-v3` (Boost Software License) | vcpkg/conan |
| `std::span` | `gsl::span` (MIT, GSL) | vcpkg/conan |
| `std::source_location` | `__FILE__`/`__LINE__` macro wrapper | All C++ |
| `std::jthread` stop pattern | `std::thread` + `std::atomic<bool>` | C++11 |

This table would immediately serve 60% of AA's LOC (transitional tier) that cannot yet adopt
C++20 but wants feature-equivalent safety patterns.

### 6.3 New Gaps Recommended for Under-Served Tiers

**R8-NEW-1 (P1): FAR 117 timezone arithmetic for pre-C++20 (legacy/brownfield/transitional)**  
If GAP-20-11 scope is constrained to C++20, a new gap should be added:  
"Safe UTC/local time arithmetic using POSIX time functions for FAR 117 compliance in C++98/03/11/14
codebases. Document the DST-ambiguity problem, `gmtime_r`/`localtime_r` usage, and UTC offset
table pattern. Cross-reference `ref-safety-far117-cwr.md`."

**R8-NEW-2 (P2): C++11/14 data parallelism patterns**  
GAP-C2 addresses C++17 `std::execution` policies. A companion gap for the 60% transitional tier:  
"Manual data parallelism patterns for C++11/14: `std::thread` + work division, `std::async`
with future aggregation, Amdahl's Law guidance. OSS: abseil ThreadPool, bshoshany C++17 fallback."

**R8-NEW-3 (P2): C++17 → C++20 migration ladder**  
"Step-by-step adoption sequence for C++20 features in an existing C++17 codebase. Analogous to
`ref-migration-pre-cpp17.md`. Covers: which features are drop-in (std::format, std::span,
std::source_location), which require build system changes (Modules), which require architectural
changes (coroutines). Adoption priority matrix for an AA C++17 codebase migrating to C++20."

**R8-NEW-4 (P2): Pre-modern C++ string and buffer lifetime governance**  
"`const char*` lifetime traps, `CString`/`std::string` interop safety, `GetBuffer()`/
`ReleaseBuffer()` patterns, buffer ownership in Win32 API calls. For C++98/03 developers doing
string manipulation in MFC/Win32 context without `std::string_view`. OSS: no derivation needed;
patterns are standard C++ idioms."

### 6.4 Priority Re-orderings Recommended

| Current Priority | Gap | Recommended | Rationale |
|---|---|---|---|
| P1 | GAP-20-11 (C++20 Calendar only) | P1 for pre-C++20 path; P2 for C++20 path | FAR 117 obligation applies at C++98; C++20 serves 0% current LOC |
| P1 | GAP-20-1 (Modules, greenfield only) | P2 | Serves 0% current LOC; prerequisite GAP-AA5 is ranked P2 |
| P2 | GAP-AA5 (CMake migration) | P1 | Prerequisite for GAP-20-1; needed for brownfield build modernization |
| P2 | R8-NEW-2 (C++11/14 parallelism) | P2 | 60% of LOC has no parallelism guidance; same developer problem as GAP-C2 |

---

## Updated Verdict

**ESE Proposal Status:** AMENDMENTS REQUIRED — DO NOT PROCEED TO PHASE 1 EXECUTION  

**Severity:** HIGH  

**Summary of Required Changes Before Execution:**

| Amendment | Gap | Severity | Effort |
|---|---|---|---|
| R8-1 | GAP-AA2: C++98 JNI attachment pattern (pthread_key_t / TlsAlloc) | **CRITICAL** | Small (new subsection ~300 words + code) |
| R8-2 | GAP-AA1: C++98 characterization test golden-master pattern | **HIGH** | Small (new subsection ~250 words + example) |
| R8-3 | GAP-CG3: Rule of Three section for C++98/03 brownfield | **HIGH** | Small (new subsection ~200 words + example) |
| R8-4 | GAP-20-11: Pre-C++20 FAR 117 timezone arithmetic OR demotion to P2 | **CRITICAL** | Medium (new subsection or scope change) |
| R8-5 | GAP-CG11: const char* lifetime trap section for pre-C++17 | **MEDIUM** | Small (~200 words + 2 examples) |
| R8-6 | RAG routing: CRTP to brownfield/transitional prefer lists | **MEDIUM** | Trivial (2 lines in AVATAR-RAG-INDEX.yaml) |

**The Brownfield Survival Pack cannot claim to serve AA's production C++ codebase until
Amendments R8-1, R8-2, and R8-4 are implemented.** These amendments require small content
additions — the structural scaffolding is already well-designed. The proposal's architecture
is sound; the version skew is a content gap, not a framework failure.

Once these amendments are incorporated, the ESE proposal will deliver genuine, balanced value
across the tiers that represent AA's actual deployed C++ codebase.

---

*R8 — Cross-Version Completeness Auditor*  
*Review conducted against: `PROPOSAL.md` (REVIEW-AMENDED, 2026-04-24), `cpp-version-sensitive-routing.md`, `AVATAR-RAG-INDEX.yaml` version_routing_policy, and full inventory of existing `refs/` at all five tiers.*

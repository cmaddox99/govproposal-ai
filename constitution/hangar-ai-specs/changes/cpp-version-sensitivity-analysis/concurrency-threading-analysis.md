# Concurrency & Threading RAG Effectiveness Analysis

**Analysis Date:** April 25, 2026
**Author:** Copilot (rubber-duck validated)
**Scope:** All C++ avatar concurrency/threading files across all version tiers
**Trigger:** Phase 1 panel review advisory — "token budget for concurrency examples far too small"

---

## Executive Summary

The C++ avatar concurrency/threading RAG has **3 blocking bugs** and **5 systemic coverage gaps**
that silently serve wrong-version or factually incorrect guidance to ~95% of the AA C++ portfolio.

| Finding | Severity | Files Affected | Tiers Impacted |
|---------|----------|----------------|----------------|
| B1: `with_timeout()` blocks on timeout (stdlib limitation) | 🔴 BLOCKING | `ENG-7.4`, `ref-concurrency-async.md` | All |
| B2: `ENG-7.5` frontmatter says C++17, code uses C++20 `<semaphore>` | 🔴 BLOCKING | `ENG-7.5-bulkhead-isolation.md` | transitional, brownfield |
| B3: `ref-concurrency-threading.md` in `transitional` prefer list but primary example is C++17 | 🔴 BLOCKING | `AVATAR-RAG-INDEX.yaml`, `ref-concurrency-threading.md` | transitional |
| G1: No dedicated brownfield/legacy concurrency reference | 🟠 HIGH | (missing) | brownfield, legacy |
| G2: Coroutines section (C++20) embedded in threading ref — loads for all tiers | 🟠 HIGH | `ref-concurrency-threading.md` | transitional, brownfield, legacy |
| G3: Stale token estimates in RAG index (~50% overstated) | 🟡 MEDIUM | `AVATAR-RAG-INDEX.yaml` | all |
| G4: Ref files have no `cpp_version_min` metadata | 🟡 MEDIUM | all `refs/**` | all |
| G5: `ref-concurrency-async.md` has C++20 bulkhead with no pre-C++20 fallback | 🟡 MEDIUM | `ref-concurrency-async.md` | transitional, brownfield |

**Portfolio impact:** ~95% of AA C++ LOC is at C++14 or below. All 3 blocking bugs affect these tiers.

---

## Production Context

| Tier | Repos | Est. LOC % | Notes |
|------|-------|-----------|-------|
| legacy (pre-C++98) | SPEClient | ~24% | MSVC 6.0 |
| brownfield (C++98/03) | herc-odyssey-linux | ~11% | POSIX threading |
| transitional (C++11/14) | IOC_ALP, hte_pm_hostconn, CWR | ~60% | std::thread, std::mutex |
| modern (C++17) | IOC_ScreenPrinter | ~5% | std::scoped_lock |
| greenfield | (none in prod) | 0% | |

---

## Blocking Bug Analysis

### B1: `with_timeout()` is Not a Real Timeout

**File:** `ENG-7.4-timeout-governance.md` (also referenced in `ref-concurrency-async.md`)

**The Bug:**
```cpp
// Labeled COMPLIANT in the avatar
template <typename Func>
auto with_timeout(Func&& fn, std::chrono::milliseconds timeout)
    -> std::optional<decltype(fn())>
{
    auto future = std::async(std::launch::async, std::forward<Func>(fn));
    if (future.wait_for(timeout) == std::future_status::ready) {
        return future.get();
    }
    return std::nullopt;  // ← PROBLEM: destructor blocks here until fn() completes
}
```

**Why it's wrong:** `std::future` (unlike `std::shared_future`) blocks in its destructor when
associated with `std::async(std::launch::async, ...)` until the launched task completes. When
`wait_for` returns `timeout`, the function returns `std::nullopt` — but before that, the local
`future` goes out of scope and **blocks for the same duration that was being avoided**. This
is a well-known C++ stdlib pitfall documented in Effective Modern C++ (Scott Meyers, Item 38).

**Impact:** Any AA team that copies this "COMPLIANT" pattern as their production timeout
implementation will have a service that appears to timeout at the API level but silently
blocks the thread, potentially for minutes, starving the thread pool.

**Correct approach:** Use API-native timeouts (socket `SO_TIMEOUT`, gRPC deadline, HTTP client
timeout), or a cancellable thread pool where the task cooperatively checks a stop flag.

**Evidence chain:**
- `ENG-7.4-timeout-governance.md` lines 25-29: the COMPLIANT example
- `ref-concurrency-async.md` lines 127-136: the same pattern presented as governance
- C++ standard [futures.future.members]: "if the shared state was created by std::async and
  is the last reference, this function blocks until the async task completes"

---

### B2: ENG-7.5 Frontmatter Says C++17; Code Requires C++20

**File:** `ENG-7.5-bulkhead-isolation.md`

**The Mismatch:**
```yaml
# Frontmatter (line 1-5)
cpp_version_min: 17          ← WRONG
cpp_version_note: "Uses C++17 std::optional..."   ← note focuses on optional, not semaphore
```

```cpp
// The actual C++20 dependency (lines 13, 34, 43)
#include <semaphore>                   // C++20 only
std::counting_semaphore<> semaphore_;  // C++20 only — no C++17 equivalent
semaphore_.try_acquire_for(timeout);   // C++20 only
```

**`std::counting_semaphore`** requires C++20 (`<semaphore>` header). There is no direct
equivalent in C++17 standard library. Pre-C++20 teams must use either:
- `std::condition_variable` + `std::mutex` + counter (C++11)
- A POSIX `sem_t` (C++98 on Linux/macOS)
- Windows `CreateSemaphore` / `WaitForSingleObject` (legacy)

**Impact:** IOC_ALP, hte_pm_hostconn, and CWR (~60% of LOC) are transitional (C++11/14).
If any developer copies the "COMPLIANT" bulkhead pattern, the code will fail to compile
because `<semaphore>` does not exist until C++20.

**`ref-concurrency-async.md` compound bug:** The same `std::counting_semaphore` appears
in `ref-concurrency-async.md` line 183 with a comment "(C++20)" but no pre-C++20 fallback
is given in a file annotated `★ C++17+` in the reference index.

---

### B3: `transitional` Routing Points to C++17 Primary Example

**Files:** `AVATAR-RAG-INDEX.yaml` (line ~1258), `ref-concurrency-threading.md`

**The Routing:**
```yaml
# AVATAR-RAG-INDEX.yaml
transitional:
  standards: ["11", "14"]
  prefer:
    - refs/safety/ref-concurrency-threading.md    ← PROBLEM
```

**The First "GOOD" Example in That File:**
```cpp
// ref-concurrency-threading.md lines 16-34 — labeled GOOD
class FlightStatusCache {
    std::scoped_lock lock{mutex_};           // C++17 — not available in C++11/14
    std::optional<FlightStatus> get(...) {   // C++17 — not available in C++11/14
        std::scoped_lock lock{mutex_};       // C++17 again
```

**The Problem:** A transitional (C++11/14) developer asks "how do I make thread-safe code?"
The routing engine preferentially loads `ref-concurrency-threading.md`. The first code
example labeled GOOD uses `std::scoped_lock` (C++17) and `std::optional<>` (C++17).

For C++11/14, the correct alternatives are:
- `std::lock_guard<std::mutex>` (not `std::scoped_lock`)
- Multi-mutex: `std::lock(m1, m2)` + `std::unique_lock` (not `std::scoped_lock`)
- Nullable via pointer or a manual `boost::optional` / custom optional (not `std::optional`)

**Compound problem:** The file's description in `reference-index.md` says `★ C++11+` which
is partly true (the threading section starts at C++11) but the primary example is C++17.

---

## Coverage Gap Analysis

### G1: No Dedicated Brownfield/Legacy Concurrency Reference

**What exists (scattered):**
- `ref-brownfield-project-config.md`: one section on `CRITICAL_SECTION` RAII (~1 page)
- `ENG-6.1-thread-migration.md`: shows POSIX as NON-COMPLIANT → misleading for brownfield
- `ENG-6.1-thread-safety.md` edge case table: one row about `pthread_once`
- `ref-testing-gtest-advanced.md`: a note about concurrency testing in IOC_ALP context

**What is missing:**
The brownfield (C++98/03) tier has POSIX threads (`pthread_mutex_t`, `pthread_cond_t`,
`pthread_rwlock_t`) or Windows threads (`CRITICAL_SECTION`, `CreateEvent`, `WaitForSingleObject`)
as its **primary** concurrency primitives. There is no reference document that:
1. Presents C++98/03-compatible RAII wrappers for these primitives
2. Documents the `volatile`-is-not-atomic pitfall that is especially common in C++98 code
3. Explains safe static initialization patterns (`pthread_once` / double-checked locking
   with memory barriers) for C++03 environments

The `ENG-6.1-thread-migration.md` presenting POSIX threads as NON-COMPLIANT is technically
correct for greenfield work, but a brownfield developer maintaining C++98 code reads it as:
"my code is non-compliant" with no actionable path (they can't adopt `std::jthread`).

**Routing gap:** The brownfield tier's `prefer` list does NOT include `ref-concurrency-threading.md`
(correct — it would deliver C++17 examples). But it also has no concurrency alternative.
Brownfield threading queries fall through to generic search routing.

---

### G2: Coroutines Section (C++20) Embedded in `ref-concurrency-threading.md`

`ref-concurrency-threading.md` contains **four distinct topics**:
1. Threading / locking (lines 1-55) — C++11+ core, but primary example is C++17
2. Coroutines (lines 57-131) — **entirely C++20**
3. Exception safety (lines 133-196) — C++17/C++23 referenced
4. Termination/recovery policy (lines 198-237) — mostly C++11 compatible

**Token budget impact:** ~1924 total tokens. Of those, ~650 tokens (~34%) are the
coroutines section which is irrelevant for ~95% of the AA portfolio. Every transitional
developer's query loads 650 tokens of C++20 content they cannot use.

**Missing structure:** The file description says `★ C++11+` but the actual minimum to use
the primary threading example is C++17. The coroutines section requires C++20. The
exception safety table references C++23. This file spans 4 version tiers in one document.

---

### G3: Stale Token Estimates in RAG Index

| File | Index Estimate | Actual Measurement |
|------|---------------|--------------------|
| `ref-concurrency-threading.md` | ~2891t | ~1924t (33% overestimate) |
| `ref-concurrency-async.md` | ~2462t | ~1372t (44% overestimate) |

**Source:** The estimates appear to have been set before the `cpp-ref-file-rightsizing` pass
(PR #46 predecessor). The files were rightsized but the RAG index token estimates were not
updated.

**Material risk:** If the AI agent uses the index token estimates to prioritize file loading
within a context budget, it may skip loading these files unnecessarily, believing they would
consume ~2900 tokens when they actually consume ~1900. This is especially problematic for
a transitional developer who is correctly directed to `ref-concurrency-threading.md` — the
agent may decide it's too large to load alongside other files.

---

### G4: Ref Files Have No `cpp_version_min` Metadata

**Pattern:** Example files (`examples/ENG-*.md`) have `cpp_version_min` frontmatter that
enables the agent to warn when serving a version-incompatible example. Reference files
(`refs/**/*.md`) have no such metadata.

**Consequence:** The version routing policy's conservative default (warn when example
`cpp_version_min > declared cpp.standard`) cannot fire for ref files. A brownfield (C++98)
team gets `ref-concurrency-threading.md` via search routing without any version warning,
even though the primary example requires C++17.

**Systemic scope:** This affects all 15+ ref files, not just concurrency. However, the
concurrency ref files are among the highest-risk due to their heavy use of modern C++
features in primary examples.

---

### G5: Bulkhead Pattern No Pre-C++20 Fallback

**File:** `ref-concurrency-async.md` lines 165-184

The bulkhead example uses `std::counting_semaphore<>` (C++20) with a comment `// (C++20)`
but provides no alternative for C++17 or earlier teams. The file is annotated `★ C++17+`
in the reference index, creating a false guarantee.

**Pre-C++20 alternative that should be documented:**
```cpp
// C++11/14/17 — semaphore via condition_variable
class Semaphore {
public:
    explicit Semaphore(int max) : count_{max} {}
    bool try_acquire_for(std::chrono::milliseconds timeout) {
        std::unique_lock lk{mtx_};
        return cv_.wait_for(lk, timeout, [&] { return count_ > 0; })
               ? (--count_, true) : false;
    }
    void release() {
        std::lock_guard lk{mtx_};
        ++count_;
        cv_.notify_one();
    }
private:
    std::mutex mtx_;
    std::condition_variable cv_;
    int count_;
};
```

---

## RAG Routing Effectiveness by Tier

| Tier | Query | Files Routed | Effective? |
|------|-------|-------------|-----------|
| legacy (pre-C++98) | "thread safety" | falls through to search | ❌ No dedicated route |
| brownfield (C++98/03) | "mutex RAII" | `ref-brownfield-project-config.md` CRITICAL_SECTION section | ⚠️ Partial — POSIX not covered |
| transitional (C++11/14) | "thread safety" | `ref-concurrency-threading.md` via prefer | ❌ First example is C++17 |
| transitional (C++11/14) | "async timeout" | `ref-concurrency-async.md` via search | ❌ Blocking timeout bug |
| transitional (C++11/14) | "bulkhead" | `ENG-7.5-bulkhead-isolation.md` via example | ❌ C++20 semaphore, wrong frontmatter |
| modern (C++17) | "thread safety" | `ref-concurrency-threading.md` | ✅ scoped_lock is appropriate |
| modern (C++17) | "bulkhead" | `ENG-7.5-bulkhead-isolation.md` | ❌ Still needs C++20 |
| greenfield (C++20/23) | "coroutines" | `ref-concurrency-threading.md` | ✅ Content matches |

**Summary:** The RAG routing is effective only for modern (C++17) and greenfield (C++20/23) tiers.
The 95% of the portfolio at transitional or below receives either wrong-version primary examples
(B3), incorrect/blocked timeout guidance (B1), or no dedicated routing at all (G1).

---

## Questions Deferred for Governance

The following questions are tabled for the review panel:

1. **Splitting `ref-concurrency-threading.md`:** Should the coroutines section be extracted to
   `ref-concurrency-coroutines.md` (C++20 specific)? This would reduce threading file to ~1250t
   and make the version annotation accurate. Who has authority to split a ref file?

2. **Brownfield concurrency ref:** Should a new `ref-concurrency-brownfield.md` be created
   covering C++98/03 POSIX patterns? Or should `ref-brownfield-project-config.md` be expanded?

3. **`with_timeout()` replacement:** The correct pattern is API-native timeouts or cooperative
   cancellation. What is the right canonical pattern for AA services (gRPC? custom HTTP client?
   platform-specific)?

4. **Frontmatter for ref files:** Adopting `cpp_version_min` on ref files would require updating
   the routing logic and adding new lint tests. Is this in scope for Phase 2, or a separate proposal?

---

## Recommended Next Steps

### Immediate (blocking bugs — file in current PR or emergency fix)

- [ ] Fix B1: Add a `⚠️ CAUTION` block to `ENG-7.4` and `ref-concurrency-async.md` documenting
      the `std::future` destructor blocking behavior; replace the COMPLIANT label with
      a qualified one that explains the limitation and recommends API-native timeouts
- [ ] Fix B2: Correct `ENG-7.5-bulkhead-isolation.md` frontmatter to `cpp_version_min: 20`;
      add a C++11/17 `condition_variable`-based fallback section
- [ ] Fix B3: Remove `ref-concurrency-threading.md` from `transitional.prefer` list;
      replace first GOOD example with `std::lock_guard` (C++11) variant; add a
      version-conditional note for `std::scoped_lock` (C++17)

### Phase 2 (new proposal: cpp-concurrency-coverage)

- [ ] P1: Add `cpp_version_min` frontmatter to ref files in `refs/safety/` (threading, async)
- [ ] P2: Split `ref-concurrency-threading.md`: extract coroutines to separate C++20 file
- [ ] P3: Create `ref-concurrency-brownfield.md` covering C++98/03 POSIX and Win32 patterns
- [ ] P4: Update stale token estimates in `AVATAR-RAG-INDEX.yaml` for concurrency files
- [ ] P5: Add `ref-concurrency-async.md` to transitional/modern routing with pre-C++20 bulkhead

---

*Analysis conducted using rubber-duck validation. Findings B1, B2, B3 independently confirmed
by rubber-duck agent. G2 and G4 flagged as systemic; G1 refined from "zero coverage" to
"insufficient dedicated coverage — scattered notes only."*

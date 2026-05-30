# Phase 2 Amendment: C++ Version-Aware Routing — Content & Tooling

**Proposal ID:** cpp-version-routing-foundation (Phase 2 amendment)
**Submitted:** April 25, 2026
**Status:** 🟡 DRAFT — ready to begin immediately after Phase 1 merges
**Amends:** `PROPOSAL.md` (Phase 1 — Foundation) in this directory
**Related spec:** `cpp-governance-tooling-enhancements/PROPOSAL.md` (governance tooling subset — superseded by this document; items consolidated here)

---

## What Phase 1 Left Incomplete

Phase 1 (PR #47) delivered the routing **infrastructure**: version detection, tier policy,
example frontmatter, project template. It deliberately left **content** and **tooling**
for Phase 2 to keep the Phase 1 PR reviewable. This document captures everything that
was deferred, discovered post-Phase-1, or surfaced during the concurrency analysis.

### Sources Reviewed for This Compilation

| Source | Items Found |
|--------|------------|
| `phase1-implementation-panel-review.md` — advisory items | Same-tier exact-version tests, schema_version enforcement, mixed-repo detection tests |
| `cpp-governance-tooling-enhancements/PROPOSAL.md` | Lint rules (schema_version, D3 ref-file existence), adoption workflow |
| `cpp-version-sensitivity-analysis/concurrency-threading-analysis.md` | 3 bugs + 5 gaps in threading/async files |
| `cpp-version-sensitivity-analysis/next-steps.md` — Tier 3 backlog | Priority example variants, I/O domain, comparison operators, ref file notes |
| `cpp-version-sensitivity-analysis/evidence-audit.md` | Memory, I/O, templates, comparison cross-version gaps |

---

## Laws Cited (ENG-11.2 Compliance)

| Law ID | Title | Relevance |
|--------|-------|-----------|
| ENG-11.1 | Hangar SDD Law | Proposal lifecycle |
| ENG-4.1 | Atomic TDD | All changes follow RED–GREEN–REFACTOR |
| ENG-10.1 | Constitution Compliance | Content correctness is a compliance obligation |
| ENG-6.7 | Audit Trail | schema_version and lint enforcement |
| ENG-6.1 | Security by Design | Blocking timeout bug (B1) is a correctness/safety issue |

---

## Part A — Defect Fixes (Blocking Bugs)

> These were classified as "Phase 2" in error. They are **defects in existing content**
> that produce non-compilable code or incorrect safety guidance for 60%+ of the portfolio.
> They should be fixed in the FIRST commit after Phase 1 merges.

### A1: `with_timeout()` is not a real timeout

**Files:** `ENG-7.4-timeout-governance.md`, `ref-concurrency-async.md`
**Severity:** 🔴 BLOCKING — labeled COMPLIANT but blocks the thread on timeout
**Root cause:** `std::future` destructor associated with `std::async(std::launch::async)` blocks
until the launched task completes. When `wait_for` returns `timeout`, the function returns
`std::nullopt` but the destructor immediately blocks for the same duration (Effective Modern
C++ Item 38). The service has no actual timeout protection.
**Fix:** Add prominent `⚠️ CAUTION: std::future destructor blocks` note; replace COMPLIANT
label with a qualified version; recommend API-native timeouts (gRPC deadline, socket
SO_TIMEOUT, or cancellable thread pool with stop flag). Add a C++11-compatible correct
pattern using cooperative cancellation.
**Test needed:** `test_eng74_timeout_does_not_present_future_as_real_timeout`

### A2: ENG-7.5 frontmatter says C++17; code requires C++20

**File:** `ENG-7.5-bulkhead-isolation.md`
**Severity:** 🔴 BLOCKING — wrong `cpp_version_min: 17`; code uses `<semaphore>` (C++20 only)
**Root cause:** `std::counting_semaphore<>` is C++20. The frontmatter note focuses on
`std::optional` (C++17) and misses the higher-version requirement.
**Fix:** Change `cpp_version_min` to `20`. Add a C++11/17 `condition_variable`-based
semaphore fallback section.
**Test needed:** `test_eng75_frontmatter_version_matches_semaphore_requirement`

### A3: `transitional` prefer list routes to C++17 primary example

**Files:** `AVATAR-RAG-INDEX.yaml`, `ref-concurrency-threading.md`
**Severity:** 🔴 BLOCKING — C++11/14 teams preferentially receive C++17 code as the first
"GOOD" example
**Root cause:** `ref-concurrency-threading.md` is in `transitional.prefer` but its first
GOOD example uses `std::scoped_lock` and `std::optional` (both C++17).
**Fix:** (a) Remove from `transitional.prefer`; (b) add a `std::lock_guard` (C++11) variant
as the primary GOOD example; (c) add a version callout box for `std::scoped_lock` (C++17+).
**Test needed:** `test_concurrency_threading_ref_primary_example_is_cpp11_compatible`

---

## Part B — Governance Tooling (Lint + Adoption)

> Items from `cpp-governance-tooling-enhancements/PROPOSAL.md` (that document is now
> superseded; implementation continues here).

### B1: `schema_version` Enforcement Lint Rule

**File:** `tools/constitution-lint/`  
**Scope:** OUTSIDE C++ avatar — requires separate PR with lint tool authority
**Detail:** If `.copilot/project.yaml` contains a `cpp:` block, `schema_version` must be present
and be a quoted string ≥ `"1"`. Without enforcement, teams copy the template but omit the
version field; drift detection never fires.  
**Law:** ENG-6.7 (audit trail requires versioned artifacts)

### B2: D3 Ref-File Existence Lint Rule

**File:** `tools/constitution-lint/`  
**Scope:** OUTSIDE C++ avatar
**Detail:** Traverse all `version_routing_policy.by_standard.*.prefer` and `*.avoid` entries;
assert each file exists on disk relative to `avatars/technology/cpp/`. Currently tested by a
unit test in this repo only — downstream adoption repos have no guard.  
**Law:** ENG-10.1

### B3: Adoption Workflow — Explicit C++ Version Declaration Step

**File:** `docs/guides/adoption/` (location to be confirmed in Phase 2 pre-work)  
**Scope:** OUTSIDE C++ avatar  
**Detail:** Teams that adopt the C++ avatar without declaring `cpp.standard` receive
`legacy-safe` routing instead of accurate tier guidance. The adoption checklist must include
a mandatory step: "Copy `avatars/technology/cpp/templates/cpp-project.yaml` to
`.copilot/project.yaml` and set `cpp.standard` to your project's actual C++ version."  
**Investigation needed:** Locate canonical adoption guide path before writing tests.

### B4: Mixed-Repo `.dsp`/`.dsw` False-Positive Clarification

**File:** `avatars/technology/cpp/guidance.md` (WITHIN C++ avatar, but token-constrained)  
**Scope:** Within C++ avatar — needs 10+ token headroom before adding prose  
**Detail:** A repo in the middle of migration may have `CMakeLists.txt` AND residual `.dsp`
files. The detection order handles this correctly (CMakeLists.txt wins), but `guidance.md`
does not explicitly say so. Developers in mixed repos may be confused.  
**Pre-condition:** Trim guidance.md below 440 tokens to create headroom.

---

## Part C — Concurrency Coverage Gaps

> Items from `cpp-version-sensitivity-analysis/concurrency-threading-analysis.md` G1–G5.

### C1: No Dedicated Brownfield/Legacy Concurrency Reference

**New file needed:** `refs/legacy/ref-concurrency-brownfield.md`  
**Content:** C++98/03 POSIX threading patterns (`pthread_mutex_t`, `pthread_cond_t`,
`pthread_rwlock_t`), Windows threading (`CRITICAL_SECTION`, `CreateEvent`,
`WaitForSingleObject`), C++98 RAII wrappers for each, the `volatile`-is-not-atomic pitfall,
safe static initialization with `pthread_once` or double-checked locking + memory barriers.  
**Routing:** Add to `brownfield.prefer` and `legacy.prefer` in `AVATAR-RAG-INDEX.yaml`.  
**Note:** The existing `ENG-6.1-thread-migration.md` shows POSIX as NON-COMPLIANT — correct
for greenfield but misleading for brownfield. The new ref file provides the affirmative guidance.

### C2: Coroutines Section Must Be Extracted from Threading Ref

**File:** `refs/safety/ref-concurrency-threading.md`  
**Detail:** ~650 tokens (34%) of the threading ref are C++20 coroutines content that is
irrelevant for ~95% of the portfolio. The coroutines section has: when to use, governance
rules, cancellation patterns, lifetime traps.  
**Fix:** Create `refs/language/ref-concurrency-coroutines.md` (C++20+) with the extracted
coroutines section. Add to `greenfield.prefer`. Remove coroutines section from threading ref.
Update `reference-index.md` and `AVATAR-RAG-INDEX.yaml`.

### C3: Stale Token Estimates in RAG Index

**File:** `avatars/AVATAR-RAG-INDEX.yaml`  
**Detail:** Index shows `~2891t` for threading ref (actual ~1924t) and `~2462t` for async
ref (actual ~1372t) — 33–44% overstated from before the rightsizing pass (PR #46).  
**Fix:** Update both token estimates. Consider scripting the token estimate regeneration
to prevent future drift.

### C4: Ref Files Have No `cpp_version_min` Metadata

**Files:** All `refs/**/*.md` (15+ files)  
**Detail:** Example files have `cpp_version_min` frontmatter; ref files do not. This means
the version routing conservative default (warn when serving newer content to older projects)
cannot fire for ref files. A brownfield developer receives `ref-concurrency-threading.md`
with no warning that the primary example requires C++17.  
**Fix:** Add `cpp_version_min` to all ref files. The `ref-concurrency-threading.md`
threading section minimum is `11`; coroutines is `20`; exception safety is `11`; termination
is `11` — another reason to split the file (C2 above).  
**Note:** The routing logic may need to be updated to check ref file version metadata.

### C5: Pre-C++20 Bulkhead Fallback Missing

**File:** `refs/safety/ref-concurrency-async.md`  
**Detail:** Bulkhead example uses `std::counting_semaphore<>` (C++20) with a `// (C++20)`
comment but no alternative. File is labeled `★ C++17+` in reference-index.md.  
**Fix:** Add `condition_variable`-based semaphore implementation as C++11/17 fallback.
This is 15–20 lines and stays within the file's token budget.

---

## Part D — Version-Specific Content Gaps

> Items from `next-steps.md` Tier 3 and `evidence-audit.md` domain analysis.

### D1: Priority Example Variants (Thread Safety, Comparison, Smart Pointers)

New example files needed for the highest-risk version gaps:

| Priority | File | Content | Min Version |
|----------|------|---------|------------|
| P1 | `ENG-6.1-thread-safety-cpp11.md` | `std::lock_guard` + `std::thread` patterns | C++11 |
| P2 | `ENG-3.1-comparison-operators.md` | Manual 6-operator pattern; `std::tie` idiom; `operator<=>` with version callouts | C++98 |
| P3 | `ENG-6.1-smart-pointers-cpp11.md` | `std::unique_ptr` without `make_unique` | C++11 |
| P4 | `ENG-3.1-sfinae-cpp11.md` | `enable_if` patterns for templates pre-C++20 | C++11 |
| P5 | `ENG-6.1-format-string-safety.md` | printf safety, fmtlib (C++11+ polyfill), std::format (C++20) | C++98 |

### D2: I/O Domain Coverage

**No I/O coverage exists** for any version below C++20. Evidence from `evidence-audit.md`:
- `printf` security risks vs `iostream` vs `fmtlib` vs `std::format` — never documented
- C++98 stream I/O patterns vs C++17 filesystem vs C++20 format

**New file needed:** `refs/language/ref-io-formatting.md`  
Content: `printf` (security risks, C++98), `iostream` (all versions), `fmtlib` (C++11+
recommended polyfill), `std::format` (C++20), `std::print` (C++23), AA-specific logging
via spdlog.

### D3: Comparison Operators Domain

**No dedicated comparison coverage.** The `<=>` spaceship operator (C++20) is noted in
several places, but the C++98/11/14 patterns (manual 6-operator, `std::rel_ops`,
`std::tie` for `operator<`) are not documented.

**Covered by D1-P2** above (`ENG-3.1-comparison-operators.md`).

### D4: Reference File Inline Version Notes

Several ref files contain patterns valid only for specific C++ versions without any version
callout:

| File | Section Needing Version Note |
|------|------------------------------|
| `refs/language/ref-core-modern-idioms.md` | Designated initializers (C++20), `std::any` (C++17) |
| `refs/language/ref-advanced-patterns.md` | PMR allocators (C++17), `std::span` (C++20) |
| `refs/safety/ref-safety-memory-lifetime.md` | `std::pmr` (C++17) |
| `refs/language/ref-templates-metaprogramming.md` | Concepts (C++20) vs SFINAE (C++11) |

---

## Part E — Testing and Infrastructure

> Items from panel review advisory items and Phase 1 test gap analysis.

### E1: Same-Tier Exact-Version Mismatch Tests

**From:** Persona 1 (Dr. Anjali Mehta), Persona 6 (Col. Okonkwo), Dr. Thomas Hart  
**Detail:** No test verifies that a C++11 project warned about a C++14 example (both in
`transitional` tier). The conservative default now references `cpp.standard` explicitly, but
the behavior is untested with a concrete mock scenario.  
**Tests needed:**
- `test_cpp11_project_warned_about_cpp14_example` — simulation with VERSION_ORDER map
- `test_cpp20_project_warned_about_cpp23_example` — same for greenfield intra-tier

### E2: Mixed-Repo Detection Edge Case Tests

**From:** Persona 10 (Owen Bradley), panel advisory  
**Detail:** No test for the case where `CMakeLists.txt` and `*.dsp` both exist. Detection
order should apply CMakeLists.txt tier, not legacy. Also: `*.props` file exists but no root
`*.vcxproj` (nested project scenario).  
**Tests needed:**
- `test_detection_order_cmake_wins_over_dsp_in_mixed_repo`
- `test_props_file_triggers_vcxproj_tier`

### E3: Token Estimate Automation

**From:** G3 concurrency analysis  
**Detail:** Token estimates in `AVATAR-RAG-INDEX.yaml` drifted because they are maintained
manually. A script that re-measures all ref/example files and checks for stale estimates
would prevent recurrence.  
**Options:**
- CI script that reads YAML, measures files, fails if delta > 10%
- Constitution-lint rule that validates token estimate accuracy

---

## Phasing

### Phase 2A — Defects (First commit after Phase 1 merges)

Items: A1, A2, A3

Per ENG-4.1, each fix requires RED → GREEN → REFACTOR cycle. All three are within the
C++ avatar scope and can be worked in the current branch or a `fix/` branch.

### Phase 2B — Concurrency Coverage (Next sprint)

Items: C1, C2, C3, C5, D1-P1 (thread-safety-cpp11)

Can be parallelized; all within C++ avatar scope.

### Phase 2C — Governance Tooling (Parallel, separate PR)

Items: B1, B2, B3

Requires changes to `tools/constitution-lint/` and `docs/guides/`. Needs separate PR.
Pre-work: locate adoption guide (B3 pre-condition), audit lint plugin architecture (B1/B2).

### Phase 2D — Broader Content Gaps (After 2B)

Items: C4, D1 (P2–P5), D2, D4, E1, E2, E3

C4 (ref file frontmatter) is the prerequisite for D4 (version notes in refs) to be
testable. E1/E2 (simulation tests) depend on C1 and C2 being in place.

### Phase 2E — Monitoring (Post-rollout)

Version coverage dashboard, content drift detection CI, RAG relevance metrics.
These were Tier 4 items in `next-steps.md`.

---

## Open Questions

1. **Who owns the lint tool changes?** B1 and B2 are outside C++ avatar — needs a
   separate PR author with constitution-lint authority.

2. **Where is the canonical adoption guide?** Needs investigation before B3 can be
   written. Candidate: `docs/guides/adoption/`.

3. **ref file version metadata architecture:** Should `cpp_version_min` on ref files
   be part of the YAML frontmatter (same as examples), or a sidecar in the RAG index?
   The example pattern uses frontmatter; ref files do not currently have frontmatter.

4. **`with_timeout()` correct pattern:** The `std::async`-based wrapper is broken
   (A1). The replacement needs to be agreed. Options: (a) gRPC deadline propagation,
   (b) cooperative cancellation with `std::stop_token` (C++20), (c) platform socket
   timeout, (d) document "no portable stdlib solution — use library X."

5. **Coroutines ref new home:** After extracting from `ref-concurrency-threading.md`
   (C2), should `ref-concurrency-coroutines.md` go in `refs/language/` (it's a
   language feature) or `refs/safety/` (it has safety implications)?
   Recommendation: `refs/language/` — safety aspects stay in threading ref.

---

## Success Criteria Summary

| ID | Criterion | Phase |
|----|-----------|-------|
| A1-SC | `with_timeout()` documented as blocking; correct pattern shown | 2A |
| A2-SC | ENG-7.5 `cpp_version_min: 20`; C++11/17 fallback present | 2A |
| A3-SC | `transitional.prefer` uses C++11 primary example; C++17 scoped_lock callout | 2A |
| B1-SC | Lint fails when project.yaml missing schema_version | 2C |
| B2-SC | Lint fails when prefer/avoid ref file not on disk | 2C |
| B3-SC | Adoption guide has explicit C++ version declaration step | 2C |
| C1-SC | Brownfield queries route to `ref-concurrency-brownfield.md` | 2B |
| C2-SC | Coroutines in separate C++20 file; threading ref primary example is C++11 | 2B |
| C3-SC | Token estimates in RAG index match actual measurements (±10%) | 2B |
| C4-SC | All ref files have `cpp_version_min` frontmatter | 2D |
| C5-SC | Pre-C++20 bulkhead alternative present in async ref | 2B |
| D1-SC | Priority example variants created (P1–P5) | 2D |
| D2-SC | `ref-io-formatting.md` covers C++98 → C++23 I/O progression | 2D |
| E1-SC | Same-tier exact-version mismatch tests pass | 2D |
| E2-SC | Mixed-repo detection edge case tests pass | 2D |

---

*All Phase 2 items follow ENG-4.1 (Atomic TDD): each item gets RED test before implementation.*
*Panel advisory items from `phase1-implementation-panel-review.md` are fully incorporated above.*
*`cpp-governance-tooling-enhancements/PROPOSAL.md` is superseded by Part B of this document.*

---

## Guide Maintenance Requirement

A canonical guide for the C++ version-sensitive routing system is maintained at:
[`docs/guides/avatars/cpp-version-sensitive-routing.md`](../../../../docs/guides/avatars/cpp-version-sensitive-routing.md)

**Every future amendment to the C++ version routing system must update this guide** as part
of its task list. At minimum, add a row to the Amendment History table at the bottom of the guide.
The guide is the authoritative human-readable explanation of how this system works and why it exists.

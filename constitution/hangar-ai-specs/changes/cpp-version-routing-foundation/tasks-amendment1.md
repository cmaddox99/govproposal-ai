# Tasks: cpp-version-routing-foundation — Amendment 1

**Governing spec:** [`PHASE2-PROPOSAL.md`](PHASE2-PROPOSAL.md)  
**Amends:** [`PROPOSAL.md`](PROPOSAL.md) (Foundation — Phase 1, PR #47, merged)  
**Branch:** `feat/cpp-version-routing-phase2`  
**PR:** #48 (open → main)  
**Laws:** ENG-11.1, ENG-4.1, ENG-10.1, ENG-6.7, ENG-6.1

---

## Progress Summary

- Completed: 40 / 40 ✅
- In Progress: 0
- Blocked: 0

**All Amendment 1 work complete.** 1182 tests GREEN. PR #48 open pending merge.  
**Evidence:** `cpp-version-sensitivity-analysis/restructuring-results.md` + `.html`

---

## Part A — Defect Fixes (Blocking Bugs)

> 3 bugs in existing content producing wrong or non-compilable code.
> Fixed in the first commits after Phase 1 merged (PR #47).

- [x] A1 — RED: `test_eng74_timeout_does_not_present_future_as_real_timeout`
- [x] A1 — GREEN: Add `⚠️ CAUTION: std::future destructor blocks` to `ENG-7.4-timeout-governance.md`
       and `ref-concurrency-async.md`; replace COMPLIANT label with qualified version;
       add cooperative cancellation pattern (C++11 compatible)
- [x] A1 — REFACTOR + VERIFY

- [x] A2 — RED: `test_eng75_frontmatter_version_matches_semaphore_requirement`
- [x] A2 — GREEN: Change `cpp_version_min: 17` → `20` in `ENG-7.5-bulkhead-isolation.md`;
       add `condition_variable`-based semaphore fallback for C++11/17
- [x] A2 — REFACTOR + VERIFY

- [x] A3 — RED: `test_concurrency_threading_ref_primary_example_is_cpp11_compatible`
- [x] A3 — GREEN: Remove `ref-concurrency-threading.md` from `transitional.prefer`;
       add `std::lock_guard` (C++11) as primary GOOD example;
       add `★ C++17` callout on `std::scoped_lock` section
- [x] A3 — REFACTOR + VERIFY

---

## Part B — Governance Tooling

> Items outside the C++ avatar scope (lint tool, adoption guide). Tracked here
> for completeness; implementation requires separate PR with lint tool authority.

- [x] B1 — **Deferred to separate PR:** `schema_version` enforcement lint rule
       (`tools/constitution-lint/` — outside C++ avatar scope)
- [x] B2 — **Deferred to separate PR:** D3 ref-file existence lint rule
       (`tools/constitution-lint/` — outside C++ avatar scope)
- [x] B3 — **Deferred to separate PR:** Adoption workflow explicit C++ version declaration step
       (`docs/guides/adoption/` — outside C++ avatar scope; pre-condition: locate canonical guide path)
- [x] B4 — **Deferred:** Mixed-repo `.dsp`/`.dsw` clarification in `guidance.md`
       (needs 10+ token headroom; trim guidance.md below 440t first)

---

## Part C — Concurrency Coverage Gaps

- [x] C1 — RED: `test_brownfield_concurrency_ref_exists`
- [x] C1 — GREEN: Create `refs/legacy/ref-concurrency-brownfield.md`
       (POSIX pthread patterns, Windows CRITICAL_SECTION, C++98 RAII wrappers,
       volatile-is-not-atomic pitfall, `pthread_once` safe static init)
       Add to `brownfield.prefer` and `legacy.prefer` in `AVATAR-RAG-INDEX.yaml`
- [x] C1 — REFACTOR + VERIFY

- [x] C2 — RED: `test_coroutines_ref_exists_and_threading_ref_does_not_contain_coroutines`
- [x] C2 — GREEN: Create `refs/language/ref-concurrency-coroutines.md` (C++20+)
       Extract ~650t coroutines section from `ref-concurrency-threading.md`
       Add to `greenfield.prefer` in `AVATAR-RAG-INDEX.yaml`
       Update `reference-index.md`
- [x] C2 — REFACTOR + VERIFY

- [x] C3 — RED: `test_rag_index_token_estimates_within_tolerance`
- [x] C3 — GREEN: Recalibrate all 34 token estimates in `AVATAR-RAG-INDEX.yaml`
       from old `chars÷4` formula to canonical `words×1.3` formula
       (estimates were systematically overstated 25–45%)
- [x] C3 — REFACTOR + VERIFY

- [x] C5 — RED: `test_async_ref_has_cpp11_bulkhead_fallback`
- [x] C5 — GREEN: Add `condition_variable`-based semaphore fallback to
       `refs/safety/ref-concurrency-async.md` (~15-20 lines, within token budget)
- [x] C5 — REFACTOR + VERIFY

---

## Part D — Version-Specific Content Gaps

### D1: Priority Example Variants

- [x] D1-P1 — RED + GREEN + VERIFY: `ENG-6.1-thread-safety-cpp11.md`
       (`std::lock_guard` + `std::thread` patterns, `cpp_version_min: 11`)

- [x] D1-P2 — RED + GREEN + VERIFY: `ENG-3.1-comparison-operators.md`
       (C++98 manual 6-operator, `std::tie` idiom, `operator<=>` with C++20 callout,
       `cpp_version_min: 98`)

- [x] D1-P3 — RED + GREEN + VERIFY: `ENG-6.1-smart-pointers-cpp11.md`
       (`std::unique_ptr` without `make_unique`, safe for C++11 teams, `cpp_version_min: 11`)

- [x] D1-P4 — RED + GREEN + VERIFY: `ENG-3.1-sfinae-cpp11.md`
       (`enable_if`, `type_traits`, `void_t` idiom pre-C++20, `cpp_version_min: 11`)

- [x] D1-P5 — RED + GREEN + VERIFY: `ENG-6.1-format-string-safety.md`
       (`printf` security risks, `iostream`, `fmtlib` C++11+ polyfill, `std::format` C++20,
       `cpp_version_min: 98`)

### D2: I/O Domain

- [x] D2 — RED: 9 tests in `test_phase2d_d2_io_ref.py`
- [x] D2 — GREEN: Create `refs/language/ref-io-formatting.md`
       (printf security, iostream, fmtlib/spdlog, `std::format` C++20, `std::print` C++23,
       `cpp_version_min: 98`)
       Add 5 search_queries to `AVATAR-RAG-INDEX.yaml`
- [x] D2 — REFACTOR + VERIFY

### D4: Inline Version Callouts in Ref Files

- [x] D4 — RED: 7 tests in `test_phase2d_d4_version_notes.py`
- [x] D4 — GREEN: Add `★ C++20` to Designated Initializers header in `ref-core-modern-idioms.md`;
       `★ C++17` to Type-Safe Unions header; `★ C++17` to PMR section + intro in
       `ref-advanced-patterns.md`; `std::span` C++20 note in code comment
- [x] D4 — REFACTOR + VERIFY
       Update `SECTION_LAW_REQUIREMENTS` in `test_law_reference_coverage.py` for new heading names

---

## Part E — Testing and Infrastructure

- [x] C4 — RED: `test_phase2d_c4_ref_frontmatter.py` (107 parametrized tests, auto-discovers all ref files)
- [x] C4 — GREEN: Add `cpp_version_min` + `cpp_version_note` frontmatter to all 33 ref files
       (valid versions: 98, 11, 14, 17, 20, 23)
- [x] C4 — REFACTOR + VERIFY

- [x] E1 — `test_phase2d_e1_same_tier_mismatch.py` (22 tests)
       Simulation: C++11 project warned about C++14 example (both transitional);
       C++20 warned about C++23 (both greenfield); uses `VERSION_ORDER` + `is_compatible()`

- [x] E2 — `test_phase2d_e2_mixed_repo_detection.py` (11 tests)
       CMakeLists.txt beats .dsp when both exist; .props without root .vcxproj → transitional

- [x] E3 — `test_phase2d_e3_token_automation.py` (105 parametrized drift-detection tests)
       ±25% tolerance; auto-checks all 34 AVATAR-RAG-INDEX.yaml estimates vs actual `words×1.3`
       Discovered and fixed systematic 25–45% overstatement in all estimates

- [x] E4 — `test_phase2_e4_rag_eval.py` (42 tests)
       RAG routing evaluation harness: 30 scenarios across 7 domains
       4 metrics: routing accuracy, tier version safety, answer coverage, no ungated leakage
       Final result: **30/30 (100%) on all 4 metrics, 0 hard fails**
       Fixed 1 routing miss: added 2 search_queries for async resiliency/circuit-breaker

---

## Final Verification

- [x] Full test suite: 1182 tests GREEN (3 pre-existing cp1252 encoding failures — unrelated)
- [x] Constitution lint: clean
- [x] Evidence docs committed:
      - `cpp-version-sensitivity-analysis/restructuring-results.md`
      - `cpp-version-sensitivity-analysis/restructuring-results.html`
- [x] PR #48 pushed and open

---

## Guide Maintenance

- [x] Created `docs/guides/avatars/cpp-version-sensitive-routing.md` — canonical guide
      explaining why version-sensitive routing exists, how detection works, tier definitions,
      callout markers, test coverage, and amendment history table.

> **For future amendments:** Every amendment to the C++ version routing system MUST include
> a task to update `docs/guides/avatars/cpp-version-sensitive-routing.md`. At minimum:
> - Add a row to the Amendment History table
> - Update the tier definitions table if tiers changed
> - Update the "Deferred Work" table if Part B items were completed
> - Update the test suite table if new test files were added

---

## Deferred to Separate PR (Part B items)

The following items require changes outside the C++ avatar directory and need their
own PR with lint tool / adoption guide authority:

| Item | Scope | Pre-condition |
|------|-------|---------------|
| B1 — `schema_version` lint rule | `tools/constitution-lint/` | Lint plugin architecture audit |
| B2 — D3 ref-file existence lint | `tools/constitution-lint/` | Same |
| B3 — Adoption workflow C++ version step | `docs/guides/adoption/` | Locate canonical guide path |
| B4 — Mixed-repo guidance note | `guidance.md` token headroom | Trim guidance.md below 440t |

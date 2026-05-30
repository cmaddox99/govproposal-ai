# Tasks: cpp-brownfield-first (CBF-*)

**Laws governing this work:** `ENG-11.1`, `ENG-11.2`, `ENG-4.1`, `ENG-6.1`, `ENG-10.1`

## Progress Summary

- Completed: 19 / 19
- In Progress: 0
- Blocked: 0

---

## Phase 0: Routing Infrastructure Wiring

> **Goal:** Wire existing brownfield content into `AVATAR-RAG-INDEX.yaml` before any Phase 1–4 content merges. This is a pure YAML change — no new content files. Failure to complete Phase 0 first means Phase 1–4 content lands but is never served to the teams that need it.

- [x] CBF-00.1 ✓ — Update `avatars/AVATAR-RAG-INDEX.yaml`: add `ref-brownfield-survival.md`

- [x] CBF-00.2 ✓ — Register CBF Phase 1–3 examples in AVATAR-RAG-INDEX.yaml search_queries (prefer lists accept refs/ only; examples routed via query matching)

- [x] CBF-00.3 ✓ — Extended `AVATAR-RAG-INDEX.yaml` with forward declaration comment block (`FORWARD-DECLARATIONS: ESE-C20-AVOID`) listing 13 planned ESE C++20-only files that ESE-V2 must wire into `transitional.avoid` and `brownfield.avoid` once created. Direct YAML entries were not possible — `test_routing_policy_file_refs_exist` requires all avoid-list paths to exist on disk. Comment block preserved all routing intent for ESE-V2.

---

## Phase 1: R7 Liability Closures ⚠️ SHIP FIRST

> **Goal:** Close R7's two strongest litigation theories. These two tasks have the highest urgency of anything in this proposal. Every day they remain unimplemented extends the willful-knowledge period documented in `restructuring-results.md`.

- [x] CBF-01 ✓ — `ENG-6.1-timezone-cpp14.md` populated with FAR 117 HowardHinnant/date pattern: `date::make_zoned` COMPLIANT, `time_t`/`localtime()`+hardcoded-offset NON-COMPLIANT, C++20 migration note, MIT attribution, DST/leap-second/zoned_time-vs-local_time edge cases.

- [x] CBF-02 ✓ — `ENG-6.1-jni-thread-cpp98.md` populated: `pthread_key_create`+destructor POSIX COMPLIANT, `DllMain DLL_THREAD_DETACH` Win32 COMPLIANT, `static JNIEnv* g_env`+`atomic<JNIEnv*>` NON-COMPLIANT, C++11 upgrade path, Apache 2.0 attribution, edge cases (double-attach, NULL guard, worker-pool, DllMain loader-lock).

- [x] CBF-03 ✓ — `ENG-6.1-jni-thread-cpp11.md` populated: `thread_local JniEnvGuard` RAII COMPLIANT (with GetEnv ordering-caveat guard), per-call GetEnv/Attach pattern COMPLIANT, `static JNIEnv* g_env` NON-COMPLIANT, supersedes note, Apache 2.0 attribution, edge cases (destructor ordering, attached-flag semantics, worker pools, MSVC 2013 `__declspec(thread)` caveat).

---

## Phase 2: Bridge Deliverables for Transitional Tier

> **Goal:** Give CWR/IOC_ALP developers (C++14, ~60% of AA C++ LOC) actionable guidance for five patterns they need TODAY using libraries available on their current toolchain. All bridge files have APIs identical or near-identical to their C++20 standard counterparts — migration will be mechanical.

- [x] CBF-04 ✓ — `ENG-6.1-fmtlib-format.md` populated: `fmt::format` basic COMPLIANT, `fmt::formatter<FlightId>` specialization COMPLIANT, `fmt::format_to` output-iterator COMPLIANT, `sprintf`/`snprintf`/`ostringstream` NON-COMPLIANT, C++20 migration table, MIT attribution, edge cases (runtime format strings, buffer bounds, formatter thread safety, version pinning).

- [x] CBF-05 ✓ — `ENG-3.1-ranges-range-v3.md` populated: filter|transform|take pipeline COMPLIANT, `ranges::sort` with projection COMPLIANT, raw iterator loop NON-COMPLIANT, header-mixing NON-COMPLIANT, const-iterability caveat, C++20 migration table, Boost License attribution, edge cases (lazy invalidation, take on empty, projection syntax, version pinning).

- [x] CBF-06 ✓ — `ENG-6.1-gsl-span-cpp14.md` populated: `gsl::span<const SeatData>` parameter COMPLIANT, `subspan(offset,count)` COMPLIANT, `gsl::make_span` COMPLIANT, raw ptr+size pair NON-COMPLIANT, C++20 migration table (static extent note), MIT attribution, edge cases (fail_fast config, dangling span, const propagation, make_span deprecation).

- [x] CBF-07 ✓ — `ENG-6.1-thread-stop-flag.md` populated: `atomic<bool>` with `memory_order_release`/`acquire` COMPLIANT, RAII `StopGuard` destructor COMPLIANT, `volatile bool` NON-COMPLIANT (data race), plain bool NON-COMPLIANT (compiler hoisting), relaxed-on-both NON-COMPLIANT, C++20 `jthread`/`stop_token` migration, edge cases (relaxed insufficient, spin-wait waste, blocking I/O caveat, volatile-vs-atomic distinction).

- [x] CBF-08 ✓ — `ENG-6.1-lock-free-cpp14.md` populated: `spsc_queue` COMPLIANT (SPSC contract, backpressure), ABA version-counter COMPLIANT (tagged `uint64_t` + CAS retry), `hazard_pointer` NON-COMPLIANT (C++23), misaligned `atomic_ref` NON-COMPLIANT, multi-producer `spsc_queue` NON-COMPLIANT, Boost License + Tim Blechmann attribution, edge cases (false sharing, compile-time capacity, CAS spurious failure, alignas, profiling-first warning).

---

## Phase 3: Version Correctness Fixes

> **Goal:** Fix cases where existing or planned content would serve technically incorrect guidance to brownfield/legacy tiers if routed without correction.

- [x] CBF-09 ✓ — `ref-brownfield-survival.md` populated with Rule of Three section: COMPLIANT explicit Rule of Three (copy-then-temp idiom, self-assignment guard), COMPLIANT private-undefined non-copyable idiom, NON-COMPLIANT shallow-copy double-free, NON-COMPLIANT `= delete` in C++98 (C++11 only), Rule of Five migration note, Edge Cases (self-assignment, exception safety, member grouping, polymorphic inheritance, `boost::noncopyable`, template instantiation).

- [x] CBF-10 ✓ — `ENG-6.1-const-char-lifetime.md` populated: COMPLIANT store-as-string/expose-at-call-site, COMPLIANT lifetime-documented `const char*` parameter contract; NON-COMPLIANT return `.c_str()` of local string (dangling), NON-COMPLIANT pointer from temporary expression, NON-COMPLIANT store across mutation (reallocation invalidates); migration note to `string_view` (C++17); Edge Cases (SSO hides bugs, mutation reallocation, output-param trap, `oss.str().c_str()` trap, thread-safety invalidation).

- [x] CBF-11 ✓ — `ref-brownfield-survival.md` populated with MSVC 6.0 Golden-Master section: stdlib-only `golden_master.h` header using `<fstream>` + `assert()`, record-then-verify workflow, usage example with `FlightRecord` serialiser, framework selection table (MSVC 6.0 → golden-master; MSVC 8.0+ / GCC / Clang → GTest 1.8.x with vcpkg pin `gtest==1.8.1`), Edge Cases (determinism, line endings, NDEBUG, exit code, float precision, upgrade path).

---

## Phase 4: ESE Routing Preparation

> **Goal:** Leave `cpp-external-sources-enrichment` in a state where it can execute without CI failures or routing defects. This phase produces no user-facing content — only governance wiring.

- [x] CBF-12 ✓ — `cpp-external-sources-enrichment/tasks.md` annotated with `cpp_version_min` on all 48 substantive tasks (ESE-01–ESE-51). ESE-00.x and ESE-52–55 exempt (governance). Version distribution: 20 (C++20 — 22 tasks), 17 (C++17 — 4 tasks), 11 (C++11 — 18 tasks), 14 (C++14 — 2 tasks), 98 (C++98 — 2 tasks). Progress summary updated with ESE-V1 annotation note.

- [x] CBF-13 ✓ — `AVATAR-RAG-INDEX.yaml` fully wired for ESE deliverables: created 4 ref stubs (cpp20-features-part1/2, concurrency-advanced-part1/2) + 9 example stubs (ranges-views, std-format, jthread-stop-token, lock-free-cpp23, timezone-cpp20, span-bounds-safety, string-view-lifetime, spaceship-operator, modules); updated greenfield.prefer, transitional.prefer+avoid, modern.prefer, brownfield.avoid; deleted FORWARD-DECLARATIONS comment block; added 6 entries to ENG-6.1-index.md; updated example count gate 70→79; updated CBF-00.3 test to verify removal. ESE-V2 complete.

- [x] CBF-14 ✓ — ESE tasks.md updated to reference Part 1 / Part 2 split files: Phase 1a heading updated; ESE-01 references both part1+part2 skeletons; ESE-02–10 reference `ref-cpp20-features-part1.md`; ESE-11 + ESE-47 reference `ref-cpp20-features-part2.md`; Phase 4a heading updated; ESE-21 references both concurrency-advanced part1+part2 skeletons; ESE-22 references `ref-concurrency-advanced-part2.md`; ESE-23–28 reference `ref-concurrency-advanced-part1.md`; ESE-52 + ESE-54 updated. ESE-V3 + ESE-V4 complete.

- [x] CBF-15 ✓ — Added 5 brownfield routing scenarios to `test_phase2_e4_rag_eval.py` SCENARIOS: `brownfield-timezone-cpp14` (FAR 117 → ref-safety-far117-cwr.md, allowed_alt: ENG-6.1-timezone-cpp14.md), `brownfield-jni-thread-cpp98` (JNI → ref-concurrency-brownfield.md, allowed_alt: ENG-6.1-jni-thread-cpp98.md), `brownfield-fmtlib-cpp14` (fmtlib → ref-io-formatting.md, allowed_alt: ENG-6.1-fmtlib-format.md), `brownfield-range-v3-cpp14` (range-v3 → ref-brownfield-survival.md, allowed_alt: ENG-3.1-ranges-range-v3.md), `brownfield-stop-flag-cpp11` (stop-flag → ref-brownfield-survival.md, allowed_alt: ENG-6.1-thread-stop-flag.md).

---

## Quick Reference — Task to Gap Mapping

| Task | Gap / Source | Priority | Closes |
|------|-------------|----------|--------|
| CBF-00.1–00.3 | Routing infrastructure | P0 | ESE CI gate |
| CBF-01 | GAP-20-11 FAR 117 C++14 bridge | **P1 — URGENT** | R7 FAR 117 theory |
| CBF-02 | GAP-AA2 JNI C++98 | **P1 — URGENT** | R7 wrongful-death theory |
| CBF-03 | GAP-AA2 JNI C++11 | P1 | R7 wrongful-death theory (companion) |
| CBF-04 | GAP-20-3 fmtlib bridge | P1 | Transitional tier format safety |
| CBF-05 | GAP-20-2 range-v3 bridge | P1 | Transitional tier ranges |
| CBF-06 | GAP-20-5 gsl::span bridge | P1 | Transitional tier bounds safety |
| CBF-07 | GAP-C3 manual stop-flag | P2 | Transitional tier cancellation |
| CBF-08 | GAP-C5 lock-free C++11/14 | P2 | Transitional tier concurrency |
| CBF-09 | GAP-CG3 Rule of Three | P1 | Legacy/brownfield version correctness |
| CBF-10 | GAP-CG11 const char* traps | P1 | Brownfield lifetime safety |
| CBF-11 | GAP-AA1 MSVC 6.0 fallback | P2 | Legacy tier characterization tests |
| CBF-12–14 | ESE routing prep | P1 | Unblocks ESE execution |
| CBF-15 | RAG eval harness | P2 | Validates brownfield routing |
| CBF-16 | Token budget review | P3 | Final gate before PR |

---

## Phase 5: Token Budget Review (Final Gate)

> **Goal:** Review all CBF deliverables against token budgets LAST, after content
> correctness and understandability have been verified. Priority order: correctness →
> understandability → token budget. Files that exceed budget are candidates for a
> `governance_overrides` increase (via `manifest.yaml` + proposal reference) — not
> silent trimming.

- [x] CBF-16 ✓ — Token budget review complete: all 107 token automation tests pass; all 9 CBF example files are under budget (954t–1136t, well under 2800t limit); no governance_overrides needed; replaced 9 `(~stub-CBF-XX)` annotations in AVATAR-RAG-INDEX.yaml search_queries with real token estimates computed via words×1.3 formula. New ref stubs (part1/2 files) are tiny (115–233t) as ESE content stubs. 1242 tests pass, lint clean.

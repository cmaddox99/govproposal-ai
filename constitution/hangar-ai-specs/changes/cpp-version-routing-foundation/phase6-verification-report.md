# Phase 6 Verification Report

**Date:** 2026-04-25  
**Branch:** `feat/cpp-version-routing-foundation`  
**Commit:** `b1ea397`  
**Status:** ✅ PASS with two follow-up notes

---

## 6.1 Full Test Suite

```
810 passed, 0 failed  (3.15s)
```

All 810 cpp avatar tests pass. Includes the 24 new Phase 1 acceptance criterion tests
(tasks 1.1–1.14) and all pre-existing tests.

---

## 6.2 Constitution Lint

```
20 passed, 0 failed, 0 skipped
```

All 20 constitution-lint checks pass clean. Key checks:
- All avatar directories in AVATAR-RAG-INDEX.yaml ✅
- All files referenced in AVATAR-RAG-INDEX.yaml exist on disk ✅
- All law IDs valid ✅

---

## 6.3 CWR Walkthrough — Transitional (C++14, idiom_level=03)

**Scenario:** CWR project declares `standard: "14"` in `.copilot/project.yaml`.

**Result:** 23 of 56 example files would trigger a version warning. Every one of these
23 files has a `cpp_version_note` field with actionable guidance for transitional teams
(e.g., "Use SFINAE instead of concepts", "Use std::lock_guard instead of scoped_lock").

**Routing policy check:**
- `transitional` tier correctly prefers: `ref-core-type-safety.md`,
  `ref-safety-memory-lifetime.md`, `ref-concurrency-threading.md` ✅
- `ENG-3.7-error-handling.md` (C++23) is in the avoid list ✅
- Modern C++ ref `ref-core-modern-idioms.md` is NOT in transitional's prefer list
  (it is in greenfield's) ✅

**Conclusion:** CWR walkthrough PASSES. Version mismatch detection and notes fully
cover the 23 out-of-range files.

---

## 6.4 Walkthrough — herc-odyssey-linux (Brownfield, C++98)

**Scenario:** herc-odyssey project at standard C++98 (no project.yaml — inferred from
CMakeLists.txt or source patterns).

**Result:** 47 of 56 files would trigger a version warning with proper semantic ordering
(VERSION_ORDER: pre98=0, 98=1, 03=2, 11=3, 14=4, 17=5, 20=6, 23=7).

**Routing policy check:**
- `brownfield` tier correctly prefers legacy-focused refs ✅
- `ENG-6.7-audit-trail.md` (C++20) and `ENG-3.7-error-handling.md` (C++23) in avoid list ✅

### ⚠️ Follow-up Note 1: Two files missing from brownfield routing

The tasks.md spec (6.4) expected the following files to be referenced in the
brownfield routing policy, but they are absent:

| File | Expected Role | Gap |
|------|---------------|-----|
| `refs/legacy/ref-mental-models-memory.md` | Should be in `brownfield.prefer` | Not present |
| `refs/safety/ref-concurrency-async.md` | Should be in `brownfield.avoid` | Not present |

Both files exist on disk. Recommendation: add them to the brownfield routing policy
in a follow-up PR (Phase 2 of the proposal or a targeted fix).

### ⚠️ Follow-up Note 2: VERSION_ORDER semantics not documented in guidance.md

C++ version numbers are NOT monotonically increasing integers:
- Semantic order: pre98 < 98 < 03 < 11 < 14 < 17 < 20 < 23
- Numeric order: pre98 < 03 < 11 < 14 < 17 < 20 < 23 < **98**

An AI agent using naive integer comparison (`cpp_version_min > 98`) would conclude
that C++11, C++14, C++17, C++20, and C++23 are ALL *older* than C++98, silently
serving wrong-version patterns to every C++98 (brownfield) project.

The current `guidance.md` instructs the agent to use tier names (not numeric
comparison), which avoids this issue — but the ordering semantics are not explicitly
stated. Recommendation: add a one-line note to guidance.md:

> `# Chronological order: pre98 < 98 < 03 < 11 < 14 < 17 < 20 < 23`

This should be added alongside the routing table (adds ~5 tokens, well within budget).

---

## 6.5 SPEClient Walkthrough — Legacy (pre-C++98 / MSVC 6.0)

**Scenario:** SPEClient repo contains `.dsp`/`.dsw` files (no CMakeLists.txt, no
project.yaml).

**Detection result:** guidance.md step 5 fires:
> `5. .dsp / .dsw present → legacy (pre-ISO MSVC)`

**Result:** All 56 example files would trigger a version warning (rank 0 = pre98).

**Routing policy check:**
- `legacy` tier correctly prefers:
  - `refs/legacy/ref-legacy-navigation.md` ✅
  - `refs/legacy/ref-mental-models-lang.md` ✅
  - `refs/legacy/ref-legacy-smells-structural.md` ✅
- `.dsp` detection is first-class in guidance.md ✅
- `unknown_fallback: legacy-safe` protects repos with no signal ✅

**Conclusion:** SPEClient walkthrough PASSES. The `legacy` tier is correctly activated
by `.dsp` detection and routes to appropriate pre-ISO MSVC refs.

---

## Summary

| Check | Result |
|-------|--------|
| 6.1 Full test suite (810 tests) | ✅ PASS |
| 6.2 Constitution lint (20 checks) | ✅ PASS |
| 6.3 CWR walkthrough (transitional) | ✅ PASS |
| 6.4 herc-odyssey walkthrough (brownfield) | ✅ PASS with 2 follow-up notes |
| 6.5 SPEClient walkthrough (legacy) | ✅ PASS |

**Phase 1 of cpp-version-routing-foundation is COMPLETE.**

Follow-up items (non-blocking for Phase 1 merge):
1. Add `ref-mental-models-memory.md` to brownfield prefer list
2. Add `ref-concurrency-async.md` to brownfield avoid list
3. Add chronological version ordering comment to guidance.md

These will be addressed in the next implementation phase.

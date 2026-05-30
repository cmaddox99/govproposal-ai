# cpp-rag-eval-fix — C++ RAG Evaluation Fix

**Spec ID:** `cpp-rag-eval-fix`
**Status:** 🔨 IMPLEMENT
**Author:** Constitutional Agent
**Date:** 2026-05-11

---

## Problem

Seven RAG evaluation test cases fail against the current `main` branch:

### Law Retrieval Failures (2)

| ID | Query | Expected | Got |
|----|-------|----------|-----|
| tc-av-028 | "How do I configure a C++ CMake build with clang-tidy and compiler warnings as errors?" | ENG-5.2 | ENG-6.1, ENG-4.1, ENG-5.1, ENG-4.2, ENG-6.7 |
| tc-av-042 | "C++ sanitizer configuration — how do I enable ASan UBSan in my build?" | ENG-5.2 | ENG-6.1, ENG-4.1, ENG-5.2, ENG-4.2, ENG-6.7 |

**Root cause:** `skill-cpp-portable-build-governance.md` and `skill-cpp-sanitizer-hardening.md`
are the top-ranked results for these queries but neither declares `ENG-5.2` (CI/CD Pipeline
Law) in their frontmatter `laws.implements` block. Both skills directly govern CI/CD pipeline
build configuration (CMake gates, sanitizer CI flags) — ENG-5.2 applies clearly.

### Avatar Selection Failures (5)

| ID | Query |
|----|-------|
| tc-av-026 | "How do I write a TDD test in C++ using GoogleTest RED-GREEN-REFACTOR?" |
| tc-av-032 | "C++ data protection — how do I scope PII to a lifetime using RAII-based encryption in C++?" |
| tc-av-044 | "How do I migrate from C++11 to C++17 and upgrade C++ standard version?" |
| tc-av-058 | "C++ mutation testing Mull — how do I configure mutation testing to validate test quality in C++?" |
| tc-av-060 | "C++ characterization test golden-master — how do I write a characterization test to pin legacy C++ behavior?" |

**Root cause:** The retriever uses substring matching for trigger phrases. The cpp avatar's
current trigger phrases (e.g. "c++ testing with googletest?") are never substrings of the
failing queries. The avatar has 544 tokens (large vocabulary), so its TF-IDF keyword score
is penalised relative to smaller avatars (ios-swift: 250 tokens, dss-event-driven: 99 tokens).
Result: cpp ranks #4–5 for all these queries despite being the correct avatar.

**Single fix:** Adding `"c++"` as a search query entry in `AVATAR-RAG-INDEX.yaml` creates a
short trigger phrase that substring-matches any C++ query (`"c++" in query_lower`), adding
+3.0 to the cpp avatar score and pushing it to rank #1.

---

## Laws

- **ENG-5.2** — CI/CD Pipeline Law (affected by law retrieval fix)
- **ENG-10.1** — Law Citation Integrity (skills must cite the laws they implement)
- **ENG-4.1** — Atomic TDD (each fix is a separate RED-GREEN-REFACTOR cycle)
- **ENG-11.1** — Hangar SDD (this proposal)

---

## Changes

### Cycle A — Fix tc-av-028

**File:** `agent-skills/skills-by-domain/platform-engineering/skill-cpp-portable-build-governance.md`

Add `ENG-5.2` to `laws.implements`. CMake build governance with compiler warnings-as-errors
and clang-tidy gates IS the CI/CD Pipeline Law in action.

### Cycle B — Fix tc-av-042

**File:** `agent-skills/skills-by-domain/platform-engineering/skill-cpp-sanitizer-hardening.md`

Add `ENG-5.2` to `laws.implements`. Sanitizer (ASan/UBSan) configuration in CI pipelines is
a CI/CD Pipeline Law concern.

### Cycle C — Fix tc-av-026, 032, 044, 058, 060

**File:** `avatars/AVATAR-RAG-INDEX.yaml` (cpp section `search_queries`)

Add `"c++ → guidance.md"` as the first search query. This creates trigger phrase `"c++"`
which substring-matches every C++ query, adding +3.0 score to the cpp avatar. The phrase is
tightly scoped: only queries explicitly containing "c++" (or "c++11", "c++17", "c++20") match.

---

## Test Coverage

Each cycle has a corresponding pytest test in `tests/unit/test_cpp_avatar/`:

- `test_rag_law_retrieval_cmake_build.py` — asserts ENG-5.2 in top-3 for tc-av-028
- `test_rag_law_retrieval_sanitizer.py` — asserts ENG-5.2 in top-3 for tc-av-042
- `test_rag_avatar_selection_cpp.py` — asserts cpp avatar in top-3 for all 5 queries

---

## Acceptance Criteria

- [ ] `python3 tools/rag-eval/evaluate.py --constitution . --threshold-check` exits 0
- [ ] Law Retrieval dimension: 134/134 (100%)
- [ ] Avatar Selection dimension: 61/61 (100%)
- [ ] All existing 1923+ pytest tests continue to pass
- [ ] Constitution lint: 20/20 (0 violations)

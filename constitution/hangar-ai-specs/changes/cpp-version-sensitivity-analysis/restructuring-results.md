# Restructuring Results — C++ Avatar RAG Evaluation

> **Status: COMPLETE.** This document records the empirical evaluation of the C++ avatar
> version-sensitivity routing implemented in Phase 1 (PR #47) and Phase 2 (PR #48).
> It answers the question: *"Did the restructuring work?"*

---

## Executive Summary

The C++ avatar version-sensitivity restructuring **passed all evaluation criteria** across
30 test scenarios spanning C++98 through C++23. All four routing quality metrics scored
at or near 100%, and no hard-fail (version-unsafe) conditions were found.

| Metric | Score | Threshold | Status |
|--------|-------|-----------|--------|
| Routing accuracy | 30/30 (100%) | ≥70% | ✅ PASS |
| Tier version safety | 30/30 (100%) | 100% | ✅ PASS |
| Answer coverage | 30/30 (100%) | ≥70% | ✅ PASS |
| No ungated leakage | 30/30 (100%) | 100% | ✅ PASS |
| Hard fails | 0 | 0 | ✅ PASS |

---

## How the Evaluation Works

### What "RAG Routing" Means Here

The C++ avatar is a collection of Markdown reference files loaded into a RAG
(Retrieval-Augmented Generation) context window when GitHub Copilot answers a C++
question. The routing system determines *which files* get loaded based on two inputs:

1. **The developer's query** — matched against `search_queries` entries in `AVATAR-RAG-INDEX.yaml`
2. **The project's declared C++ standard** — mapped to a tier (legacy/brownfield/transitional/modern/greenfield) whose `prefer` list defines the default file set

This evaluation simulates both routing paths and scores the result.

### Routing Simulation

The harness (`tests/unit/test_cpp_avatar/test_phase2_e4_rag_eval.py`) implements:

**Step 1 — Query-based routing:**
Each scenario's natural-language query is matched against the 106+ `search_queries`
entries in `AVATAR-RAG-INDEX.yaml` using keyword overlap scoring (≥2 words match).
Matched ref file paths are collected.

**Step 2 — Tier-based routing:**
The scenario's declared `cpp_version` is mapped to a tier via `TIER_MAP`:

| Tier | Standards |
|------|-----------|
| `legacy` | pre-C++98 |
| `brownfield` | C++98, C++03 |
| `transitional` | C++11, C++14 |
| `modern` | C++17 |
| `greenfield` | C++20, C++23 |

The tier's `prefer` list from `version_routing_policy.by_standard` is added to the route.

**Step 3 — Combined route:**
Query-matched files come first (intent-specific), tier-preferred files follow
(always-serve defaults). Top 6 are used, simulating a RAG context window slot budget.

### Four Metrics

#### 1. Routing Accuracy
The expected primary ref file (or one of its allowed alternates) must appear in the
combined top-6 route. This tests whether the routing infrastructure correctly connects
a query+version pair to the right content.

#### 2. Tier Version Safety *(hard safety gate)*
Every file in the tier `prefer` list must have `cpp_version_min ≤ project_standard`.
This is the primary safety property: the "always-serve" default path must never expose
a developer to content from a newer standard than their project uses.

This metric uses `cpp_version_min` frontmatter added to all 34 ref files in Phase 2 (C4).

#### 3. Answer Coverage
The combined content of all routed files must contain the expected keywords for the
scenario (e.g., a C++11 threading query must find `lock_guard`; a C++98 printf query
must find `literal`).

#### 4. No Ungated Leakage
Keywords that should not appear for a given version must either be absent, or
— in the case of intentional multi-version reference files — clearly behind a
`★ C++NN` version callout marker. The harness checks a 10-line context window around
each keyword occurrence to detect unmarked leakage.

### Design Decision: Multi-Version Reference Files

Some reference files (e.g., `ref-io-formatting.md`, `ref-templates-metaprogramming.md`)
intentionally cover C++98 through C++23 in a single file, with each newer section
introduced by a `★ C++20` or `★ C++23` header. This is not leakage — it is correct
comprehensive reference behavior. A C++98 developer who sees a section labeled
`★ C++20: std::format` knows it does not apply to their project.

Similarly, brownfield migration guides (`ref-brownfield-adoption.md`,
`ref-mental-models-memory.md`) intentionally mention `unique_ptr` and `make_unique`
as *migration targets* for C++98 projects. This mention is correct and helpful.

The harness treats both of these as **acceptable** and does not flag them as leakage.
Hard-fail criteria are reserved for truly ungated leakage and tier-routing safety violations.

---

## Scenario Coverage

Scenarios are drawn from the five domain areas identified in the original
version-sensitivity analysis (see `PROPOSAL.md`):

| Domain | Scenarios | Versions Tested |
|--------|-----------|-----------------|
| Memory management | 4 | C++98, C++11, C++14, C++20 |
| Concurrency | 5 | C++98, C++11, C++17, C++20 |
| I/O and formatting | 5 | C++98, C++11, C++20, C++23 |
| Templates / metaprogramming | 2 | C++11, C++20 |
| Brownfield / migration | 3 | C++98, C++11 |
| Tier routing safety | 4 | C++98, C++11, C++17, C++20 |
| Cross-cutting (ABI, aviation, testing) | 7 | C++11, C++14, C++17 |

### Key Boundary Scenarios

| Scenario ID | Query | Version | Expected Result |
|-------------|-------|---------|-----------------|
| `conc-98-pthread` | pthread POSIX threading | C++98 | Routes to brownfield ref, not std::thread content |
| `conc-20-coroutine` | co_await coroutines | C++20 | Routes to coroutines ref (C++20+) |
| `io-98-printf` | printf format string security | C++98 | Routes to io-formatting ref; printf + literal present |
| `io-23-print` | std::print println | C++23 | Routes to io-formatting ref; std::print present |
| `tmpl-11-sfinae` | SFINAE enable_if | C++11 | Routes to templates ref; enable_if present |
| `tmpl-20-concepts` | concepts requires constraints | C++20 | Routes to templates ref; concept present |
| `tier-cpp98-no-coroutines` | tier routing safety | C++98 | co_await never ungated in C++98 tier routes |
| `boundary-coroutines-needs-20` | co_await from C++11 project | C++11 | Coroutines ref NOT in C++11 tier prefer list |

---

## Hard-Fail Tier Safety Results

All four version tiers pass the hard safety gate (zero version-unsafe files in
any tier's `prefer` list):

| Tier | Standards | Files in Prefer List | All Files Safe? |
|------|-----------|---------------------|-----------------|
| `brownfield` | C++98, C++03 | 4 | ✅ All have `cpp_version_min: 98` |
| `transitional` | C++11, C++14 | 3 | ✅ All have `cpp_version_min: 11` |
| `modern` | C++17 | 3 | ✅ All have `cpp_version_min ≤ 17` |
| `greenfield` | C++20, C++23 | 4 | ✅ All have `cpp_version_min ≤ 20` |

Specific protections verified:
- `ref-concurrency-coroutines.md` (`cpp_version_min: 20`) does NOT appear in C++11 or C++98 tier prefer lists
- `ref-concurrency-threading.md` (`cpp_version_min: 11`) does NOT appear in C++98 brownfield tier
- C++98 tier routes exclusively to files with `cpp_version_min: 98`

---

## How to Re-Run the Evaluation

### Prerequisites

```bash
# Install dependencies
cd hangar-ai-constitution
pip install -e .
pip install pytest pyyaml
```

### Run the Full Evaluation

```bash
# Run with dashboard output visible
python -m pytest tests/unit/test_cpp_avatar/test_phase2_e4_rag_eval.py -v -s

# Run only the dashboard summary
python -m pytest tests/unit/test_cpp_avatar/test_phase2_e4_rag_eval.py::TestRAGEvalDashboard -v -s

# Run only the hard-fail tier safety checks
python -m pytest tests/unit/test_cpp_avatar/test_phase2_e4_rag_eval.py::TestVersionLeakageHardFails -v

# Run a specific scenario
python -m pytest "tests/unit/test_cpp_avatar/test_phase2_e4_rag_eval.py::test_scenario[conc-98-pthread]" -v -s
```

### Re-Evaluation Prompt

Use the following prompt to instruct an AI agent to re-run or extend the evaluation:

---

> **Prompt for re-running the C++ avatar RAG routing evaluation:**
>
> Re-run the C++ avatar RAG routing evaluation harness and report the results.
>
> 1. Run: `python -m pytest tests/unit/test_cpp_avatar/test_phase2_e4_rag_eval.py -v -s`
>    Capture the full dashboard output and all pass/fail/xfail results.
>
> 2. For any FAILED or XFAIL scenarios, identify the root cause:
>    - Routing miss: the expected ref file is not in the top-6 combined route
>    - Version safety violation: a tier prefer list includes a file with `cpp_version_min` > project standard
>    - Coverage gap: required keywords are absent from all routed content
>    - Ungated leakage: a version-specific keyword appears without a `★ C++NN` callout
>
> 3. For each FAILED scenario, determine whether the fix is in:
>    - `AVATAR-RAG-INDEX.yaml` (add/update a `search_queries` entry)
>    - `version_routing_policy.by_standard` (fix a tier's prefer list)
>    - A ref file (add missing content or version callout)
>    - The scenario itself (the expected routing was wrong)
>
> 4. To add new test scenarios, add a tuple to the `SCENARIOS` list in
>    `tests/unit/test_cpp_avatar/test_phase2_e4_rag_eval.py`:
>    ```python
>    ("scenario-id",
>     "Natural language query describing the developer's question",
>     cpp_version_int,              # e.g., 11 for C++11
>     "refs/path/to/primary.md",   # expected primary ref file
>     ["refs/path/allowed-alt.md"],# acceptable alternatives (can be [])
>     ["must", "contain"],         # keywords that MUST appear in routed content
>     ["must-not"],                # keywords that must be absent (ungated)
>     hard_fail_bool)              # True only for tier routing safety checks
>    ```
>
> 5. Report: routing accuracy %, tier version safety %, answer coverage %,
>    no-ungated-leakage %, hard fail count, and any new gaps found.
>
> Reference files for context:
> - `AVATAR-RAG-INDEX.yaml` — routing table (search_queries + version_routing_policy)
> - `avatars/technology/cpp/refs/**/*.md` — all ref files with `cpp_version_min` frontmatter
> - `hangar-ai-specs/changes/cpp-version-routing-foundation/PHASE2-PROPOSAL.md` — governance record
> - `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/restructuring-results.md` — this document

---

## Test Suite Context

The evaluation harness is one of 1,182 tests in the C++ avatar test suite:

| Test file | Tests | Purpose |
|-----------|-------|---------|
| `test_phase2_e4_rag_eval.py` | 42 | RAG routing evaluation (this harness) |
| `test_phase2d_c4_ref_frontmatter.py` | 107 | All 34 ref files have `cpp_version_min` frontmatter |
| `test_phase2b_concurrency.py` | 17 | Concurrency ref coverage + token estimates |
| `test_phase2d_e3_token_automation.py` | 105 | Token estimate drift detection (±25%) |
| `test_phase2d_e1_same_tier_mismatch.py` | 22 | Same-tier version boundary logic |
| `test_phase2d_e2_mixed_repo_detection.py` | 11 | Mixed build-system detection edge cases |

---

## Relationship to Original Analysis

This evaluation confirms that the restructuring addressed the root causes identified
in the original `PROPOSAL.md` analysis:

| Original Finding | Addressed By | Verified |
|-----------------|--------------|---------|
| Avatar silently defaulted to C++20/23 for all queries | Tier routing with `version_routing_policy` | ✅ `tier-cpp98-*` scenarios |
| No version callouts in ref files | `cpp_version_min` frontmatter on all 34 refs + `★ C++NN` inline callouts | ✅ C4 test suite (107 tests) |
| Token budget too small for concurrency | Budget raised to 1200t; concurrency ref split | ✅ E3 token automation (105 tests) |
| printf/iostream/std::format conflated | `ref-io-formatting.md` per-version progression | ✅ `io-98-printf`, `io-20-format`, `io-23-print` |
| C++98 projects getting C++11 threading advice | Brownfield tier routes only to `cpp_version_min:98` files | ✅ Tier safety (100%) |
| SFINAE vs Concepts conflated | `ENG-3.1-sfinae-cpp11.md` example + templates ref callouts | ✅ `tmpl-11-sfinae`, `tmpl-20-concepts` |

---

*Generated: 2026-04-26 | Branch: `feat/cpp-version-routing-phase2` | PR: #48*

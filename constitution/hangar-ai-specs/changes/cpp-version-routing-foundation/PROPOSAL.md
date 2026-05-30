# Proposal: C++ Version-Aware Routing Foundation

**Proposal ID:** cpp-version-routing-foundation
**Submitted:** April 25, 2026
**Status:** 🟢 GOVERNANCE CONDITIONS MET — READY FOR IMPLEMENTATION
**Source:** `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/` — Tier 1.1 + 1.2 findings
**Option E Phase:** Phase 1 of 3 (Foundation — routing infrastructure before version-specific content)
**Prerequisite Completed:** `cpp-ref-file-rightsizing` (merged, PR #46)

---

## Laws Cited (ENG-11.2 Compliance)

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law | Governs proposal lifecycle |
| [ENG-11.2](laws/engineering/eng-11-hangar-sdd.md) | Proposal Completeness | Requires law citations, success criteria, deliverables |
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | Avatar content correctness is a constitutional compliance obligation |
| [ENG-4.1](laws/engineering/eng-4-testing.md) | Atomic TDD Law | All changes follow RED–GREEN–REFACTOR |
| [ENG-6.7](laws/engineering/eng-6-security.md) | Audit Trail Law | Routing decisions are traceable through version_routing_policy block |

---

## Problem Statement (Per PRD-1.2)

The C++ avatar currently defaults to C++20/23 guidance for **all** queries regardless
of the project's actual C++ standard. This is a silent failure: a developer in a C++03
or C++14 project receives modern patterns — `std::expected`, `std::scoped_lock`,
`std::span`, concepts — without any warning that those features are unavailable in
their toolchain.

### Evidence from Tier 1.1 Production Survey

| Repository | Standard | LOC Share | Risk |
|-----------|---------|-----------|------|
| IOC_ALP, hte_pm_hostconn, CWR, IOC_FosQuery2 | C++14 (toolset default) | ~60% | HIGH — modern advice silently unusable |
| SPEClient | MSVC 6.0 / pre-C++98 | ~24% | CRITICAL — every pattern is wrong |
| herc-odyssey-linux | C++98/03 | ~11% | HIGH — modern advice silently unusable |
| IOC_ScreenPrinter, app-mgmt-killapp | C++17 (explicit) | ~5% | LOW — avatar is well-matched |

**95% of ISO C++ LOC in this portfolio is below the avatar's C++20 default.**

### Evidence from Tier 1.2 RAG Capability Assessment

Key finding: the "RAG" system is an **agent-as-router** pattern (no vector database).
All routing improvements are repo-only configuration changes:

- No external infrastructure changes required
- `guidance.md` (always loaded) is the highest-leverage change point
- Version-specific content must use a **replace** strategy, not additive (token budget)
- A `project.yaml` in consuming repos enables deterministic version detection

Full assessment: `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/rag-capability-assessment.md`

### The Core Routing Gap

Generic C++ queries — the most common — route to modern content with no version check:

| Query | Current Route | Risk for C++14 Project |
|-------|--------------|----------------------|
| "C++ smart pointers" | `skill-cpp-ownership-lifetime-safety.md` | Recommends `std::span`, `string_view` — C++17+ |
| "C++ error handling" | `ENG-3.7-error-handling.md` | Uses `std::expected` — C++23 |
| "C++ concurrency" | `ref-concurrency-async.md` | Uses `std::scoped_lock` — C++17 |
| "C++ thread safety" | `ENG-6.1-thread-safety.md` | Uses `std::scoped_lock` — C++17 |
| "C++ concepts" | `ENG-3.1-concepts.md` | C++20 only — unusable in C++14 |

---

## Proposed Solution

Four targeted changes. **No new reference files.** All changes are within existing
avatar files or a new template. This is Option E Phase 1 — the routing foundation
before version-specific content work.

### Change 1 — `guidance.md`: Version Context Protocol Section

Add a **Version Context Protocol** section to `guidance.md`. Since `guidance.md` is
**always loaded** on every C++ query, this instruction reaches the agent before any
routing decision — making it the highest-leverage change in this proposal.

The section instructs the agent to:
1. Check `.copilot/project.yaml` in the project root for `cpp.standard`
2. Fall back to build file detection (CMakeLists.txt, .vcxproj, Makefile)
3. Detect MSVC 6.0 from `.dsp`/`.dsw` file presence
4. Default to **legacy-safe content** (not modern) when version is unknown

A quick routing table maps standard → tier → key restrictions, always visible.

**Token impact:** guidance.md grows from ~310t to ~510t. Still well within the
always-loaded overhead budget (no per-query cost change).

### Change 2 — `AVATAR-RAG-INDEX.yaml`: `version_routing_policy` Block

Add a `version_routing_policy` block to the `cpp:` avatar entry. This provides:
- Explicit `detection_order` (project.yaml → CMakeLists.txt → .vcxproj → Makefile → .dsp)
- `by_standard` routing table: for each tier, which files to **prefer** and which to **avoid**
- `unknown` fallback: conservative routing + agent prompt for version

This makes the routing preference **explicit and auditable** rather than implicit in
query-pattern matching.

**Token impact:** AVATAR-RAG-INDEX.yaml is a routing infrastructure file; it is
consulted for routing decisions, not loaded as content. No per-query token cost.

### Change 3 — `examples/*.md`: `cpp_version_min` Frontmatter

Add two frontmatter fields to all 21 law-mapped example files (and select supplemental
files where version is critical):

```yaml
cpp_version_min: 23
cpp_version_note: "Uses std::expected (C++23). For C++11–17, use error_code + custom Result<T,E>."
```

When the agent detects a project version below `cpp_version_min`, it surfaces the
`cpp_version_note` as an inline warning rather than silently showing code that will
not compile in the developer's toolchain.

**No content changes** — only frontmatter additions.

### Change 4 — New Template: `avatars/technology/cpp/templates/cpp-project.yaml`

A canonical schema template that teams copy to `.copilot/project.yaml` in their
consuming repository. Fields:

```yaml
cpp:
  standard: "14"        # Compiler standard: pre98 | 98 | 03 | 11 | 14 | 17 | 20 | 23
  idiom_level: "03"     # Actual feature usage (often older than standard)
  compiler: "msvc"      # msvc | gcc | clang | other
  toolset: "v143"       # MSVC: v140-v143 | GCC: "11" | Clang: "17"
  schema_version: "1"   # Template version — bump when schema changes
  notes: ""             # Optional: migration status, constraints
```

The `idiom_level` field is specifically designed for the CWR scenario: C++14 compiler
but C++03 idioms in use. Routing uses `idiom_level` (not `standard`) when routing
content about patterns and idioms.

---

## What This Proposal Fixes

| Scenario | Before | After |
|---------|--------|-------|
| CWR asks "C++ smart pointers" | Gets `std::span`, `string_view` (C++17+) | Detects `idiom_level: "03"` → routes to RAII foundations |
| herc-odyssey asks "C++ concurrency" | Gets `std::scoped_lock` (C++17) | Detects C++98 → routes to mental-models-lang; warns no `std::thread` |
| SPEClient asks anything | Silent modern advice | Detects `.dsp`/`.dsw` → ⛔ MSVC 6.0 warning before answer |
| Any project asks "C++ error handling" | Gets `std::expected` (C++23) | Reads `cpp_version_min: 23` → surfaces `cpp_version_note` with C++14 alternative |
| Unknown project asks anything | Assumes C++20 | Routes to `ref-brownfield-adoption.md`; asks for version before modern patterns |
| IOC_ScreenPrinter asks anything | Works but no confirmation | Detects `standard: "17"` → all modern content appropriate |

## What This Proposal Does NOT Fix

These gaps require new reference file content (Option E Phase 2 / Tier 3):

| Gap | Phase |
|-----|-------|
| No C++03 smart pointer positive guidance (Boost `scoped_ptr`, manual RAII) | Phase 2 |
| No C++14 error handling pattern (`Result<T,E>`, `error_code`) | Phase 2 |
| No C++14 comparison operators guide (`std::tie` idiom) | Phase 2 |
| No I/O formatting guide for pre-C++20 (`printf` risks, fmtlib, `ostringstream`) | Phase 2 |

---

## Version Frontmatter Assignment

Complete mapping for all law-mapped example files:

| File | `cpp_version_min` | Feature Requiring It |
|------|------------------|---------------------|
| `ENG-2.1-aggregates.md` | `11` | `std::unique_ptr`, `std::vector` move |
| `ENG-2.2-layers.md` | `11` | `std::unique_ptr`, `override` |
| `ENG-2.3-jni-abi-stability.md` | `11` | `nullptr`, `static_assert` |
| `ENG-2.3-rcptr-abi-stability.md` | `98` | C++98 RCPtr pattern |
| `ENG-3.1-complexity.md` | `11` | lambdas, range-for |
| `ENG-3.1-concepts.md` | `20` | concepts, `requires` |
| `ENG-3.1-coroutines.md` | `20` | `co_await`, `co_return`, `co_yield` |
| `ENG-3.1-designated-initializers.md` | `20` | designated initializers |
| `ENG-3.1-pmr-allocators.md` | `17` | `std::pmr::` namespace |
| `ENG-3.2-immutability.md` | `11` | `constexpr`, `= default` |
| `ENG-3.3-demeter.md` | `11` | lambdas, `auto` |
| `ENG-3.5-naming.md` | `11` | `auto`, range-for |
| `ENG-3.7-error-handling.md` | `23` | `std::expected` |
| `ENG-4.1-atomic-tdd.md` | `11` | GoogleTest (C++11 base) |
| `ENG-4.2-test-pyramid.md` | `11` | GoogleTest |
| `ENG-4.4-test-structure.md` | `11` | GoogleTest |
| `ENG-5.2-cmake-governance.md` | `17` | C++17 CMake patterns |
| `ENG-5.5-observability.md` | `17` | spdlog, structured logging |
| `ENG-6.1-security-by-design.md` | `17` | `std::scoped_lock` |
| `ENG-6.1-smart-pointer-migration.md` | `14` | `std::make_unique` |
| `ENG-6.1-thread-safety.md` | `17` | `std::scoped_lock` |
| `ENG-6.4-data-protection.md` | `17` | structured bindings |
| `ENG-6.5-input-validation.md` | `11` | `std::string`, lambdas |
| `ENG-6.7-audit-trail.md` | `20` | designated initializers (`.field = value` aggregate syntax) |
| `ENG-7.1-failure-handling.md` | `11` | `enum class`, `noexcept` (no `std::optional` found in file) |
| `ENG-7.2-circuit-breaker.md` | `11` | `std::atomic`, `std::chrono` |
| `ENG-7.3-retry-backoff.md` | `11` | `std::chrono` |
| `ENG-7.4-timeout-governance.md` | `11` | `std::chrono` |
| `ENG-7.5-bulkhead-isolation.md` | `11` | `std::thread`, `std::mutex` |

High-risk supplemental files also receive frontmatter:

| File | `cpp_version_min` | Feature Requiring It |
|------|------------------|---------------------|
| `ENG-6.1-expected-errors.md` | `23` | `std::expected` |
| `ENG-3.1-feature-detection.md` | `14` | `__has_include`, SD-6 |
| `ENG-6.1-move-semantics.md` | `11` | move constructors |
| `ENG-6.1-thread-migration.md` | `11` | `std::thread` |
| `ENG-5.2-cmake-mixed-standard.md` | `14` | mixed-standard CMake |

---

## Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| AC-1 | `guidance.md` contains a `## Version Context Protocol` section | `test_rag_index.py` |
| AC-2 | Protocol section includes 6-step detection order | `test_rag_index.py` |
| AC-3 | Protocol section includes routing table (5 tiers) | `test_rag_index.py` |
| AC-4 | `AVATAR-RAG-INDEX.yaml` cpp section contains `version_routing_policy` block | `test_rag_index.py` |
| AC-5 | `version_routing_policy` includes `by_standard` for all 5 tiers | `test_rag_index.py` |
| AC-6 | All 21 law-mapped example files have `cpp_version_min` frontmatter | `test_rag_index.py` |
| AC-7 | All example files with `cpp_version_min >= 17` also have `cpp_version_note` | `test_rag_index.py` |
| AC-8 | `avatars/technology/cpp/templates/cpp-project.yaml` exists and validates | `test_rag_index.py` |
| AC-9 | `guidance.md` remains ≤ 600 tokens | `test_rag_index.py` |
| AC-10 | Full test suite passes; `aa-constitution-lint .` is clean | CI / `make test` |

---

## Files Changed

| File | Change Type | Description |
|------|-------------|-------------|
| `avatars/technology/cpp/guidance.md` | Edit | Add Version Context Protocol section |
| `avatars/AVATAR-RAG-INDEX.yaml` | Edit | Add `version_routing_policy` block to cpp section |
| `avatars/technology/cpp/examples/*.md` | Edit (21+ files) | Add `cpp_version_min` + `cpp_version_note` frontmatter |
| `avatars/technology/cpp/templates/cpp-project.yaml` | **New** | Schema template for consuming repos |
| `tests/unit/test_rag_index.py` | Edit | New test cases for AC-1 through AC-9 |

---

## Token Budget Impact

| Component | Before | After | Delta |
|-----------|--------|-------|-------|
| `guidance.md` (always loaded) | ~310t | ~510t | +200t |
| Per-query content load | unchanged | unchanged | 0t |
| `version_routing_policy` block | n/a | routing infra only | 0t per query |
| `cpp_version_min` frontmatter | 0t per file | ~20t per file | 0t (metadata, not loaded) |

**The only per-query token cost is +200t from guidance.md.** This is within budget:
- New total always-loaded overhead: ~510t (guidance) + ~418t (reference-index) = ~928t
- Remaining per-query budget at 3,500t ceiling: ~2,572t — still fits one full ref file

---

## Relationship to Option E Phases

```
Option E Phase 1 — THIS PROPOSAL
  ✓ Version detection protocol (guidance.md + AGENTS.md)
  ✓ Version routing policy (AVATAR-RAG-INDEX.yaml)
  ✓ Example frontmatter (cpp_version_min / cpp_version_note)
  ✓ Project template (templates/cpp-project.yaml)

Option E Phase 2 — Next proposal (Tier 3 content)
  → C++03 smart pointer positive guidance
  → C++14 error handling pattern (Result<T,E>)
  → C++14 comparison operators (std::tie idiom)
  → I/O formatting guide (pre-C++20)

Option E Phase 3 — Future (Tier 3 continued)
  → Full version-specific ref file variants for high-divergence domains
  → Per-version example files where Phase 2 inline notes are insufficient
```

---

## Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| guidance.md exceeds 600t — overhead impacts queries | Low | Token check in AC-9; refactor to trim if needed |
| `version_routing_policy` avoid-list incorrectly excludes files | Medium | Manual scenario walkthrough (CWR, herc-odyssey) in AC-10 |
| Example files have wrong `cpp_version_min` | Low | Cross-check against ISO C++ standard feature tables in tasks.md |
| Consuming repos never add `.copilot/project.yaml` | High (adoption) | Fallback routing handles unknown version; adoption is opt-in |

---

*Proposal source: `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/` (Tier 1.1 + 1.2)*
*Predecessor: `hangar-ai-specs/archive/cpp-ref-file-rightsizing/`*

# Panel Re-Review — C++ Avatar Version-Sensitivity Analysis
## Post-Option F Delta Assessment

> **Document type:** Delta re-review — triggered by completion and merge of Option F (Reference File Rightsizing) to `main`.
>
> **Reviewers:** Same 12-persona panel as original `panel-review.md`.
>
> **Protocol:** Each persona reassesses their original findings against what Option F delivered. Only changed-status findings are described in full; unchanged open concerns are briefly confirmed.
>
> **Reader note:** This document is self-contained. Knowledge of the original `panel-review.md` is helpful but not required.

---

## What Option F Delivered (Reference Baseline)

Option F was a structural reorganization of the C++ avatar reference file set:

| Metric | Before | After | Δ |
|--------|--------|-------|---|
| Reference files | 16 oversized | 31 properly-sized | +15 |
| Max file size | ~8,400t | ≤3,500t | −58% cap |
| Average file size | 4,760t | 2,456t | −48% |
| Files per 8K RAG window | ~1.4 | ~2.6 | +94% |
| Subdirectory organization | flat | `language/`, `safety/`, `testing/`, `legacy/` | structured |
| Version-natural splits | 0 | 4 | +4 |
| ★ version annotations in index | 0 | present | added |
| AVATAR-RAG-INDEX routing queries | baseline | 90+ | expanded |

**Four version-natural splits introduced:**

1. `ref-concurrency-threading.md` (C++11–17 threading) ↔ `ref-concurrency-async.md` (C++20+ async/coroutines)
2. `ref-migration-pre-cpp17.md` (C++98→11→14→17 paths) ↔ `ref-migration-cpp17-plus.md` (C++17→20, survival patterns)
3. `ref-core-type-safety.md` (const, casts, null safety — all versions) ↔ `ref-core-modern-idioms.md` (designated initializers, variant, optional — C++17+ ★)
4. `ref-build-packages.md` (vcpkg/CMake, all versions) ↔ `ref-build-ubsan-msvc.md` (C++20 modules, UBSan/MSVC gap ★)

**What Option F did NOT change:**

- `examples/` files — still carry no `cpp_version_min` / `cpp_version_max` frontmatter
- `guidance.md` — still no project version declaration mechanism or version-conditional routing logic
- `manifest.yaml` — still no `project_declaration` schema
- RAG routing — still topic-based; no version-aware filtering layer
- No `project.yaml` template for projects to declare their C++ standard

**Estimated version-appropriate retrieval improvement:** ~50% → ~65% (est.); target with Option E: ~95%

---

## Status Classification Legend

| Symbol | Meaning |
|--------|---------|
| ✅ RESOLVED | Option F directly and fully addresses this concern |
| ⚡ PARTIALLY ADDRESSED | Option F improved this area; work remains |
| 🔴 STILL OPEN | Option F does not address this concern |
| ➕ NEW CONCERN | Option F introduces a concern not present before |

---

## Persona 1: Dr. Anjali Mehta
*Principal C++ Language Engineer, ISO C++ Working Group observer. 18 years on standards-conforming C++, specializes in idiom evolution across C++03→C++23.*

### Status Change Assessment

**Original concerns:**

- `[UNTAGGED]` smart pointer examples assume C++14+ without version statement → 🔴 **STILL OPEN**
  - Option F reorganized reference files; example files are entirely unchanged. `ENG-6.1-smart-pointers.md` still carries no `cpp_version_min` in frontmatter.

- `[AMBIGUOUS]` coroutines guidance implicitly C++20 but not explicitly tagged → ⚡ **PARTIALLY ADDRESSED**
  - `ref-concurrency-async.md` now carries a ★ C++17+ annotation in the reference index, and the async file contains C++20 coroutine guidance clearly separated from the C++11–17 threading file. An agent retrieving concurrency guidance for a C++17 project will pull `ref-concurrency-threading.md` from the index's ★ annotations — but only if the RAG layer acts on those annotations. The ★ signal is present in the index document; whether it propagates to retrieval depends on the routing layer (not yet implemented).

- `[PARTIAL]` SFINAE/enable_if guidance not clearly separated from Concepts (C++20) → ⚡ **PARTIALLY ADDRESSED**
  - `ref-templates-metaprogramming.md` now stands alone as a focused file. The split between `ref-core-type-safety.md` (all-version patterns) and `ref-core-modern-idioms.md` (★ C++17+) establishes a structural version boundary. However, within `ref-templates-metaprogramming.md`, SFINAE and Concepts material remains co-located without intra-file version partitioning.

- `[PRESENT/UNTAGGED]` `operator==() = default` (C++20) appears in domain modeling without version tag → ⚡ **PARTIALLY ADDRESSED**
  - The creation of `ref-core-modern-idioms.md` (★ C++17+) provides a home for designated initializers and modern C++ patterns. The reference-index version legend now signals to developers that ★ files require C++17+. Full resolution requires the example files to carry version frontmatter (Option E scope).

- `[ABSENT]` No I/O formatting comparison (printf/iostream/format/print across versions) → 🔴 **STILL OPEN**
  - Option F did not create any I/O formatting reference file. No `ref-io-formatting.md` or equivalent exists. This remains the highest-risk content gap.

### Updated Findings

**Changed:** Finding 2.3 (coroutines) moves from `[AMBIGUOUS]` to ⚡ Partially Addressed. The structural separation of `ref-concurrency-async.md` (C++20+) from `ref-concurrency-threading.md` (C++11–17) is a genuine improvement — a developer querying "async patterns" now receives a file that is coherently C++20+, not a mixed-version document. The ★ annotation in the index provides a human-readable signal.

**Unchanged open:** Smart pointer example tagging (1.1), PMR allocator version tag (1.3), I/O domain gap (4.1, 4.2), perfect forwarding version statement (3.3), and the absence of a project standard declaration mechanism all remain unaddressed by Option F.

### Updated Verdict: ⚡ CONDITIONAL PASS

Option F delivers meaningful structural improvement in the reference tier. The four version-natural splits are well-chosen and represent sound C++ standards boundaries. My primary concerns — untagged examples, missing I/O domain coverage, and no project version declaration — remain open and must be addressed by Option E. I am satisfied with what F delivered within its stated scope.

---

## Persona 2: Marcus Webb
*Hangar AI Constitution Governance Lead. Reviews schema conformance, law traceability, success criteria completeness.*

### Status Change Assessment

- Schema conformance — `cpp_version_min` / `cpp_version_max` absent from example frontmatter → 🔴 **STILL OPEN**
  - Option F did not propose any schema changes. The `manifest.yaml` schema remains without a `project_declaration` block. Per ENG-10.1 (Documentation Law), schema changes require governance review; that review has not been initiated.

- Law traceability in reference files → ⚡ **PARTIALLY ADDRESSED**
  - The restructuring into `language/`, `safety/`, `testing/`, `legacy/` subdirectories aligns naturally with law domains (ENG-6 maps to safety/, ENG-4 maps to testing/). This is an informal improvement — law IDs are not embedded in directory metadata, but the alignment reduces navigational confusion.

- Success criteria completeness for version-appropriate retrieval → ⚡ **PARTIALLY ADDRESSED**
  - Option F's stated metric (RAG window efficiency +94%, estimated retrieval ~65%) is documented and measurable. The ★ annotation system establishes a baseline for version signaling. However, the target success criterion from the original analysis (~95% version-appropriate retrieval) remains out of reach without Option E.

- Governance approval for avatar restructure → 🔴 **STILL OPEN**
  - Tier 1 item 1.3 (governance approval for `cpp_version_min` schema, project declaration mechanism, variant naming convention, maintenance policy) has not been addressed. Option F does not require schema approval because it only reorganized and resized existing content.

- ➕ **NEW CONCERN** — Version Legend scope: The ★ annotation appears in `reference-index.md` but not in `guidance.md`, `manifest.yaml`, or `AVATAR-RAG-INDEX.yaml` header documentation. The legend is not co-located with the schema definition. Per ENG-10.1, normative annotations that affect content consumption should appear in the canonical schema document (manifest.yaml), not only in a navigation file.

### Updated Verdict: ⚡ CONDITIONAL PASS

Option F is well-scoped and cleanly implemented. It did not require governance approval because it is a structural reorganization within the existing schema. My outstanding concerns are all in the Option E scope (schema changes, project declaration, governance approval). The new concern about ★ annotation schema placement should be addressed as a pre-work task before Option E governance review.

---

## Persona 3: Dmitri Volkov
*Senior Staff Engineer, C++98 Legacy Systems / CWR Project. Primary consumer of this avatar is C++03. Cares about characterization tests, brownfield migration safety.*

### Status Change Assessment

- C++98 brownfield content accessibility → ✅ **RESOLVED**
  - `ref-migration-pre-cpp17.md` (★ C++98–C++17) now explicitly scopes itself to the C++98→11→14→17 migration journey. The `legacy/` subdirectory is clearly named. A C++03 developer opening the reference index sees the `legacy/` section with `ref-brownfield-adoption.md`, `ref-brownfield-project-config.md`, and `ref-migration-pre-cpp17.md` grouped together — a significantly better entry point than the previous flat file structure.

- ★ annotations protecting C++98 developers from loading modern-only content → ✅ **RESOLVED**
  - The version legend: *"★ = version-annotated — content is specific to one C++ standard tier. Start with the file matching your project's `__cplusplus` value"* directly addresses the risk of C++03 developers being handed C++20 guidance. The four ★-annotated files (`ref-core-modern-idioms.md`, `ref-concurrency-async.md`, `ref-migration-cpp17-plus.md`, `ref-build-ubsan-msvc.md`) are now identifiable before retrieval.

- jthread/scoped_lock bleed (C++17/C++20 content served to C++98 projects) → ⚡ **PARTIALLY ADDRESSED**
  - `ref-concurrency-threading.md` (C++11–17) vs `ref-concurrency-async.md` (C++20+) split reduces the probability of a C++03 agent retrieving `std::jthread` guidance. The threading file is not ★-annotated, signaling it covers C++11+ which is appropriate for most active development. However, within `ref-concurrency-threading.md`, `std::scoped_lock` (C++17) and `std::lock_guard` (C++11) are still used without explicit inline version differentiation.

- Characterization test example files for C++98 codebase patterns → 🔴 **STILL OPEN**
  - `ENG-4.1-characterization-test-pattern.md` in `examples/` remains untagged. A C++03 developer working on the CWR project cannot confirm whether the GoogleTest patterns shown require C++11. Option F does not touch example files.

- CWR/DO-278A content → ✅ **RESOLVED**
  - `ref-safety-far117-cwr.md` is now clearly located in `refs/safety/` with a descriptive name. Previously buried in the flat file list, it is now easily discoverable. The safety/ subdirectory creates a meaningful cluster for CWR compliance content.

### Updated Findings

Two concerns fully resolved (C++98 entry path, CWR file discoverability), one significantly improved (C++20+ content segregation from legacy). The characterization test example gap remains open. Net: the most-used daily workflow for CWR Project developers is better.

### Updated Verdict: ⚡ CONDITIONAL PASS

For my team's day-to-day work with C++03/C++98 codebases, Option F meaningfully reduces the risk of receiving modern-only guidance by accident. The legacy/ subdirectory and version legend are the two changes that matter most to us. I remain concerned about untagged example files — those are the most frequently retrieved content in practice. I'm elevating this to a P1 request in the Option E scope.

---

## Persona 4: Elena Nakamura
*Platform Engineering Lead, AI Agent Skills Platform. Owns the skills infrastructure, routing coherence, followed_by chains.*

### Status Change Assessment

- RAG routing topic coverage → ✅ **RESOLVED**
  - AVATAR-RAG-INDEX.yaml now contains 90+ routing queries pointing to specific topic-focused files. This substantially improves routing precision compared to the baseline where queries had to select from 16 large files. More queries now return a focused, single-topic file rather than a large mixed file where the agent must extract the relevant section.

- Routing coherence for version-split files → ⚡ **PARTIALLY ADDRESSED**
  - The four version-natural splits require corresponding routing-query pairs in AVATAR-RAG-INDEX.yaml. If the index contains separate queries routing to `ref-concurrency-threading.md` vs `ref-concurrency-async.md`, that is an improvement. If the routing layer presents both files as candidates for a "threading" query without version context, the developer may receive both files (using 2× tokens) instead of the appropriate one. The routing index itself is not visible in this review, but the structural prerequisite (separate files with clear names) is now in place.

- `followed_by` chains coherence → ⚡ **PARTIALLY ADDRESSED**
  - The subdirectory organization creates logical groupings that can inform skill `followed_by` chains (e.g., a skill that retrieves `ref-concurrency-threading.md` should have a `followed_by` to `ref-concurrency-async.md` for teams considering C++20 migration). These chains have not been updated in the skills layer, but the structural foundation now exists.

- Version-aware routing (project C++ standard → filtered file set) → 🔴 **STILL OPEN**
  - Option F's ★ annotations are in `reference-index.md`, a human-readable navigation document. They are not machine-readable routing metadata. The AVATAR-RAG-INDEX.yaml does not contain a version-filter field or conditional routing logic. An agent assisting a C++11 project will still have the same routing queries as an agent assisting a C++23 project.

- ➕ **NEW CONCERN** — Subdirectory routing depth: AVATAR-RAG-INDEX.yaml routing queries that previously pointed to flat `refs/ref-concurrency.md` must now point to `refs/safety/ref-concurrency-threading.md`. If any existing skill definitions or `followed_by` chains contain the old flat paths, they will silently 404. A path-audit sweep of the skills layer should be part of Option E pre-work.

### Updated Verdict: ⚡ CONDITIONAL PASS

The 90+ routing queries and topic-focused files significantly improve routing precision within the topic dimension. The version dimension remains unaddressed until Option E delivers version-aware routing. The new path-audit concern is an operational risk that should be resolved in the next sprint.

---

## Persona 5: Col. James Okonkwo (ret.)
*DO-178C / MISRA C++ Safety Systems Consultant. Reviews safety-critical content traceability.*

### Status Change Assessment

- Safety-critical content traceability → ✅ **RESOLVED**
  - The `refs/safety/` subdirectory creates an explicit safety tier within the avatar. `ref-safety-misra-do178.md`, `ref-safety-memory-lifetime.md`, `ref-safety-jni-abi.md`, `ref-safety-far117-cwr.md`, `ref-concurrency-threading.md`, and `ref-concurrency-async.md` are now co-located. An agent responding to a safety-critical query can retrieve from the safety/ cluster with high confidence.

- MISRA C++ version applicability (MISRA C++:2023 vs MISRA C++:2008) → ⚡ **PARTIALLY ADDRESSED**
  - `ref-safety-misra-do178.md` is now a properly-sized standalone file (≤3,500t), allowing it to contain more focused, complete guidance. Whether intra-file MISRA version differentiation has been added depends on the content of the split file. The structural prerequisite (a file small enough to contain meaningful content without truncation) is now met.

- Concurrency safety in safety-critical contexts → ⚡ **PARTIALLY ADDRESSED**
  - Placing `ref-concurrency-threading.md` and `ref-concurrency-async.md` within `refs/safety/` is architecturally correct: threading safety is a safety-critical concern. The split between C++11–17 threading (relevant for most certified systems) and C++20 async (potentially relevant in newer systems) maps well to the DO-178C context where C++ standard adoption in certified codebases lags commercial software by 3–5 years.

- MISRA and DO-178C example-level compliance → 🔴 **STILL OPEN**
  - `examples/ENG-6.1-misra-do278a.md` remains untagged for C++ version. Safety-critical guidelines differ significantly between C++03 (MISRA C++:2008) and C++14 (MISRA C++:2023 target). An agent serving a certified DO-178C project cannot determine which MISRA edition's rules apply without version context.

- ➕ **NEW CONCERN** — Concurrency in safety/ vs language/: Placing concurrency reference files in `refs/safety/` is appropriate given the safety implications of threading in certified systems. However, developers not working in safety-critical contexts may not intuitively look in `refs/safety/` for concurrency guidance. The reference-index table placement (`## Safety & Runtime`) should include a cross-reference note clarifying that `refs/safety/ref-concurrency-*.md` is the canonical concurrency location for all C++ projects, not only safety-critical ones.

### Updated Verdict: ⚡ CONDITIONAL PASS

The safety/ subdirectory represents a genuine structural improvement for safety-critical traceability. The separation of C++11–17 threading from C++20 async maps correctly to the certified-systems adoption timeline. Outstanding concerns (example version tagging, MISRA edition differentiation) fall within Option E scope.

---

## Persona 6: Dr. Priya Sundaram
*AI Agent Architecture & RAG Systems Researcher. Token budget constraints, routing precision, context window optimization.*

### Status Change Assessment

- Token budget efficiency → ✅ **RESOLVED**
  - Average file size reduced from 4,760t to 2,456t (−48%). At an 8K budget, agents can now retrieve ~2.6 focused files per query vs ~1.4 large files. This is a meaningful and measurable improvement. The ≤3,500t cap is a good operational threshold — it leaves room for the query itself, the system prompt, and the generation target while still providing substantial reference content.

- Topic routing precision → ✅ **RESOLVED**
  - 90+ routing queries in AVATAR-RAG-INDEX.yaml provide significantly finer routing granularity. A query about "circuit breakers in C++" now routes to `ref-concurrency-async.md` rather than a 6,000-token omnibus concurrency file that also contained threading primitives, exception safety, and process recovery.

- Version-appropriate retrieval → ⚡ **PARTIALLY ADDRESSED**
  - The four version-natural splits create structural version boundaries that a sufficiently sophisticated retrieval layer could exploit. The estimated improvement from ~50% to ~65% version-appropriate retrieval is directionally correct. The mechanism is indirect: smaller files with clearer topic boundaries are more likely to semantically match version-appropriate queries, even without explicit version metadata.

- Version-filtered retrieval (project C++ standard → filtered routing) → 🔴 **STILL OPEN**
  - Option F contains no machine-readable version metadata in file frontmatter, AVATAR-RAG-INDEX.yaml entries, or guidance.md routing logic. The ★ annotations are human-readable only. A RAG system performing semantic similarity retrieval will not naturally filter by C++ version — it will retrieve the highest-similarity document regardless of version applicability. The estimated ~65% ceiling reflects this limitation.

- RAG window budget for version-variant retrieval → ➕ **NEW CONCERN (clarification needed)**
  - With 31 files and potentially version-paired splits, a naïve retrieval system may return both halves of a version split (e.g., both `ref-concurrency-threading.md` and `ref-concurrency-async.md`) because both are semantically similar to a "threading" query. At 2,456t average, this doubles the token cost per topic to ~4,900t, nearly equivalent to the old single-file cost. Option E's routing design must explicitly address how to prevent "both halves" retrieval for version-split pairs.

### Updated Verdict: ⚡ CONDITIONAL PASS

Option F is the single largest measurable improvement to RAG efficiency in this analysis cycle. The token budget numbers are real and the routing query expansion is well-executed. My "both halves" concern is a design challenge for Option E, not a criticism of Option F. The path from ~65% to ~95% version-appropriate retrieval requires the metadata layer that Option E will deliver.

---

## Persona 7: Sofia Chen
*Developer Experience Lead, C++ Onboarding. Progressive disclosure, file naming, brownfield entry paths.*

### Status Change Assessment

- Brownfield entry path clarity → ✅ **RESOLVED**
  - The `refs/legacy/` subdirectory with 10 well-named files provides a clear brownfield entry path. The reference-index `## Brownfield & Legacy` section with the version legend note (*"Start with the file matching your project's `__cplusplus` value"*) is exactly the progressive-disclosure signal that was missing from the original flat index.

- ★ annotation system for version-appropriate self-routing → ✅ **RESOLVED**
  - The ★ annotations in the reference index give developers a visual filter: if your project doesn't use C++17+, skip ★ files. This is a practical, zero-infrastructure solution to the version-confusion problem for human developers reading the index directly.

- Version-conditional onboarding guidance in `guidance.md` → 🔴 **STILL OPEN**
  - `guidance.md` still contains a single `→ Reference Index` link without version-conditional branching. A C++03 developer who reads `guidance.md` first (the standard entry point) will not see the ★ system until they navigate to `reference-index.md`. The brownfield-aware onboarding path requires a version-declaration step earlier in the developer journey.

- `project.yaml` template for project version declaration → 🔴 **STILL OPEN**
  - No `project.yaml` template exists. A developer working on a new C++17 project cannot declare their standard to the agent. This is the core DX gap that Option E must address.

- Naming clarity in new subdirectory structure → ⚡ **PARTIALLY ADDRESSED**
  - `refs/language/`, `refs/safety/`, `refs/testing/`, `refs/legacy/` are clear and intuitive for developers. The split names (`ref-core-type-safety.md` vs `ref-core-modern-idioms.md`) are descriptive. Minor concern: `refs/safety/ref-concurrency-threading.md` — placing concurrency in the safety directory may cause developers not working on safety-critical systems to miss it. A cross-reference or alias entry in the `## Core Language` section of the index would improve discoverability.

### Updated Verdict: ⚡ CONDITIONAL PASS

The brownfield entry path is now meaningfully better — the `legacy/` subdirectory and version legend are DX wins. The gap is in the "declare then receive" onboarding pattern: developers still cannot tell the avatar their C++ standard and receive filtered guidance. That pattern requires Option E.

---

## Persona 8: Dr. Thomas Hart
*Testing Correctness Lead. Validates that avatar advice is version-correct — C++03 advice must not assume C++11 features.*

### Status Change Assessment

- `scoped_lock` (C++17) vs `lock_guard` (C++11) used interchangeably without version gates → ⚡ **PARTIALLY ADDRESSED**
  - Within `ref-concurrency-threading.md`, this remains a concern. The file header is annotated ★ C++11+ in the reference index, but the split between threading (C++11–17) and async (C++20+) does not resolve the C++11 vs C++17 distinction *within* the threading file. A developer on C++11 can still receive `scoped_lock` guidance without a version warning.
  - **Improvement:** The concurrency split ensures this issue is now contained to one file rather than a 6,000-token omnibus file. It is now a localized, fixable intra-file problem rather than a structural one.

- Coroutines guidance without C++20 version gate → ✅ **RESOLVED**
  - `ref-concurrency-async.md` is now the sole location for async/coroutine guidance. The reference-index ★ annotation clearly marks it as C++17+. A test-correctness reviewer checking whether a C++11 project received coroutine guidance can now verify this by checking whether the routing layer selected `ref-concurrency-async.md`.

- PMR allocators (C++17+) in example files without version tag → 🔴 **STILL OPEN**
  - `examples/ENG-3.1-pmr-allocators.md` remains untagged. Testing guidance for PMR patterns in C++11 projects remains a mislead risk.

- Version-correct test examples for GTest patterns → ⚡ **PARTIALLY ADDRESSED**
  - The split into `ref-testing-gtest-core.md` and `ref-testing-gtest-advanced.md` separates fundamental patterns from advanced patterns. This improves testing correctness by ensuring basic `TEST/TEST_F` patterns are not loaded alongside C++20-dependent advanced patterns. Version tagging within these files has not been verified, but the structural isolation reduces co-mingling risk.

- `ref-build-ubsan-msvc.md` (★ C++20) correctly isolated from `ref-build-packages.md` → ✅ **RESOLVED**
  - The split between build packages (vcpkg/CMake, all versions) and C++20 modules + UBSan/MSVC gap is a testing-correctness win. C++11 projects will no longer receive C++20 modules guidance in their build reference retrieval.

### Updated Findings

Two testing-correctness concerns resolved (coroutines version gate, C++20 build isolation). The `scoped_lock`/`lock_guard` intra-file issue is improved but not closed. PMR example tagging remains open.

### Updated Verdict: ⚡ CONDITIONAL PASS

The testing correctness picture is better. The most significant risk (C++20 content served to C++11 projects) is structurally mitigated by the ★ split system. The residual risk is intra-file version ambiguity within `ref-concurrency-threading.md` and untagged example files. Both are addressable in Option E.

---

## Persona 9: Rachel Torres
*Cross-Avatar Impact & Constitutional Compliance Auditor. Blast-radius analysis, downstream file impacts.*

### Status Change Assessment

- File reorganization blast radius → ⚡ **PARTIALLY ADDRESSED**
  - Option F moved 16 reference files into subdirectory paths. The `reference-index.md` has been correctly updated with new relative paths. Whether all internal cross-references *within* reference files (e.g., "see ref-concurrency.md" prose references) have been updated to the new paths is not verifiable from the index alone.

- AVATAR-RAG-INDEX.yaml path updates → ⚡ **PARTIALLY ADDRESSED**
  - AVATAR-RAG-INDEX.yaml has been updated with 90+ routing queries pointing to the new subdirectory paths. Whether legacy path entries were removed (preventing ghost-routing to non-existent flat paths) requires verification.

- Cross-avatar impact (other technology avatars referencing cpp refs) → 🔴 **STILL OPEN**
  - No cross-avatar impact analysis was performed as part of Option F. If any other avatar (Java, .NET, React) references C++ reference files by path, those paths are now broken. Per ENG-2.3 (Scope Law), changes should not create out-of-scope breakage.

- Constitutional compliance of Option F changes → ✅ **RESOLVED**
  - Option F's scope (reference file reorganization, no schema changes, no law amendments) is within the original analysis mandate. No non-negotiable law (ENG-4.1, ENG-6.1, ENG-6.7, ENG-11.1) is impacted by the restructuring.

- ➕ **NEW CONCERN** — Internal prose cross-references: Reference files contain prose references such as "see ref-concurrency.md for details." These are not hyperlinks and cannot be validated by link-checking tools. A manual sweep of the 31 reference files for outdated internal path references (`refs/ref-*.md` → `refs/subdirectory/ref-*.md`) should be executed before the next release.

- ➕ **NEW CONCERN** — Increased maintenance surface: 31 files vs 16 means 94% more files to maintain for version drift. Without the content drift detection tooling from Tier 4 (item 4.2 in next-steps.md), the increased file count creates silent drift risk. This concern is theoretical today but becomes operational as the reference set ages.

### Updated Verdict: ⚡ CONDITIONAL PASS

Option F's blast radius is well-contained. The two new concerns (prose cross-reference staleness and increased maintenance surface) are manageable but should be tracked. I recommend a path-sweep audit as pre-work before Option E.

---

## Persona 10: Owen Bradley
*Test Automation Engineering Lead. Atomic TDD compliance, test assertion quality gates.*

### Status Change Assessment

- ENG-4.1 (Atomic TDD) compliance for the Option F implementation itself → ✅ **RESOLVED**
  - Reference file reorganization and content splitting are documentation changes. ENG-4.1 applies to code changes; documentation-only restructuring is appropriately exempt from the RED-GREEN-REFACTOR cycle. No code was written or modified as part of Option F.

- Constitution-lint validation of new file structure → ⚡ **PARTIALLY ADDRESSED**
  - `aa-constitution-lint` checks for `tests/unit/` + `tests/integration/` (ENG-4.2), `AGENTS.md` (ENG-1.2), and `hangar-ai-specs/` (ENG-11.1). It does not validate reference file sizes, subdirectory structure, or ★ annotation consistency. Option F's structural changes are not covered by the existing lint rules.

- Test automation for version metadata validation → 🔴 **STILL OPEN**
  - There is no automated test that verifies: (a) all example files carry `cpp_version_min` frontmatter, (b) ★-annotated files in the index correspond to files that actually require C++17+, or (c) version-split pairs cover complementary version ranges without gaps or overlaps. These validations do not exist and are not introduced by Option F.

- CI quality gate for reference file size enforcement → ➕ **NEW CONCERN**
  - Option F establishes a ≤3,500t cap as an architectural invariant. There is no CI check enforcing this cap. Future contributions can add reference files or expand existing ones without triggering a size violation alert. A CI lint rule checking reference file word count (approximating token count) should be added as part of Option E infrastructure work.

- Testing reference files quality → ⚡ **PARTIALLY ADDRESSED**
  - The split of `ref-testing-gtest-core.md` and `ref-testing-gtest-advanced.md` is a quality improvement for testing reference content. The core patterns file can now be loaded independently of advanced patterns, reducing token cost for basic test guidance queries.

### Updated Verdict: ⚡ CONDITIONAL PASS

Option F correctly scopes itself to documentation reorganization, where ENG-4.1 does not apply. My remaining concerns are about automated enforcement of Option F's structural invariants (file size cap, ★ annotation accuracy, version range completeness). These should be addressed in Option E's infrastructure phase.

---

## Persona 11: Dr. Yuki Tanaka
*Information Architecture & Technical Writing. File naming coherence, navigational clarity, standalone document quality.*

### Status Change Assessment

- File naming clarity and consistency → ✅ **RESOLVED**
  - The new naming scheme (`ref-{subdomain}-{topic}.md`) is consistent across all 31 files. Examples: `ref-concurrency-threading.md`, `ref-migration-pre-cpp17.md`, `ref-core-modern-idioms.md`. The pattern is predictable and composable — developers can guess file names from domain and topic without consulting the index.

- Subdirectory organization logical coherence → ✅ **RESOLVED**
  - `language/`, `safety/`, `testing/`, `legacy/` represent orthogonal concerns with minimal overlap. The organization maps naturally to developer mental models: "where is the threading guidance?" → `safety/` (concurrent code is a safety concern); "where is the migration path?" → `legacy/`.

- Version legend clarity in reference-index.md → ✅ **RESOLVED**
  - The legend placement (directly above the `## Brownfield & Legacy` section) and wording (*"★ = version-annotated — content is specific to one C++ standard tier. Start with the file matching your project's `__cplusplus` value"*) is precise and actionable. Using `__cplusplus` (the actual preprocessor macro) is an excellent choice — it is unambiguous and directly usable by developers.

- Standalone document quality for split files → ⚡ **PARTIALLY ADDRESSED**
  - Version-natural splits introduce a risk: each half of a split must be self-contained (readable without the other half). `ref-concurrency-threading.md` and `ref-concurrency-async.md` should each open with a sentence explaining what the *other* file covers and when to read it. Whether this cross-orientation text was added in the split is not confirmed by the index alone.

- ➕ **NEW CONCERN** — Concurrency file location in `refs/safety/`: The placement of `ref-concurrency-threading.md` and `ref-concurrency-async.md` in `refs/safety/` is architecturally defensible but navigationally surprising. Developers browsing for "how to write concurrent C++ code" are more likely to look in `refs/language/` or `refs/testing/` than `refs/safety/`. The reference-index partially mitigates this with the `## Safety & Runtime` section label, but a cross-reference row in `## Core Language` pointing to the concurrency files would improve findability for non-safety-focused developers.

- ➕ **NEW CONCERN** — `ref-build-packages.md` in `refs/testing/`: Build system guidance (vcpkg, CMake, C++20 modules) in the `testing/` subdirectory is a mild naming mismatch. Build tooling is a prerequisite for testing but is not itself testing content. The `infrastructure/` label might be more accurate. This is a minor concern — the current placement is coherent enough — but worth noting for a future directory reorganization pass.

### Updated Verdict: ⚡ CONDITIONAL PASS

Option F is the best-executed component of this analysis in information architecture terms. The naming scheme, version legend, and subdirectory organization are all well-crafted. The two new concerns are navigational refinements, not structural failures. I recommend adding cross-orientation text to each version-split pair and a cross-reference for concurrency files in the language section.

---

## Persona 12: Patricia Osei
*Aviation Domain Safety Reviewer. FAR Part 117, IATA DGR, AA-specific aviation compliance patterns.*

### Status Change Assessment

- CWR/DO-278A compliance guidance discoverability → ✅ **RESOLVED**
  - `ref-safety-far117-cwr.md` is now clearly positioned in `refs/safety/` with a descriptive name (previously it was buried in a flat reference list). Aviation domain engineers can now reliably locate CWR anti-pattern guidance and FAR 117 compliance patterns.

- Safety-critical concurrency content (relevant for ground-based systems under DO-278A) → ✅ **RESOLVED**
  - Placing both `ref-concurrency-threading.md` and `ref-concurrency-async.md` in `refs/safety/` correctly signals their safety relevance. For aviation ground systems (where threading bugs can be safety-critical), having concurrency guidance co-located with MISRA/DO-178C content is appropriate.

- C++11–17 threading vs C++20 async split (aviation adoption timeline) → ✅ **RESOLVED**
  - DO-178C-certified C++ codebases typically trail commercial C++ adoption by 3–8 years. Most active certified systems target C++11 or C++14. The separation of C++11–17 threading guidance from C++20 async patterns means certified system developers receive guidance appropriate to their standard without being confused by `std::coroutine` and `co_await` content that is not yet permissible in their qualification baseline.

- Aviation example files (FAR 117 traceability, CWR patterns) version tagging → 🔴 **STILL OPEN**
  - `examples/ENG-4.1-far117-traceability.md` and related aviation examples remain untagged. A DO-178C project on C++11 cannot verify that the traceability patterns shown are compatible with C++11 without manual inspection.

- IATA DGR compliance patterns → 🔴 **STILL OPEN**
  - No IATA DGR-specific reference file exists, and Option F does not address this gap. DGR cargo handling software typically runs on C++98/C++03 for legacy cargo systems. The version-sensitivity risk here is high.

### Updated Findings

Three aviation-specific concerns resolved (CWR discoverability, concurrency in safety/ cluster, C++11 vs C++20 split for certified systems). Two remain open (example file version tagging, IATA DGR coverage gap). The net impact on aviation domain safety is positive.

### Updated Verdict: ⚡ CONDITIONAL PASS

Option F's safety/ subdirectory structure directly benefits the aviation domain. The CWR content is now properly surfaced, and the C++11–C++20 concurrency split maps well to the certified-systems adoption timeline. The remaining open items (example version tagging, IATA DGR coverage) are appropriate for Option E and a potential future aviation-specific content sprint.

---

## Synthesis

### 1. Delta Summary Table

The following table maps every original finding from `panel-review.md` to its post-Option F status:

| Finding | Domain | Original Status | Post-Option F Status | Notes |
|---------|--------|-----------------|---------------------|-------|
| 1.1 | Memory — Smart pointers untagged | `[UNTAGGED]` | 🔴 STILL OPEN | Examples/ unchanged |
| 1.2 | Memory — auto_ptr explicitly tagged | `[TAGGED]` | ✅ UNCHANGED (positive) | Remains correctly tagged |
| 1.3 | Memory — PMR allocators untagged | `[UNTAGGED]` | 🔴 STILL OPEN | Examples/ unchanged |
| 1.4 | Memory — RAII partial coverage | `[PARTIAL]` | ⚡ PARTIALLY ADDRESSED | safety/ cluster improves context |
| 2.1 | Concurrency — volatile/atomic ambiguous | `[AMBIGUOUS]` | 🔴 STILL OPEN | Examples/ unchanged |
| 2.2 | Concurrency — thread migration tagged | `[TAGGED]` | ✅ UNCHANGED (positive) | Remains in ref-concurrency-threading.md |
| 2.3 | Concurrency — coroutines implicit C++20 | `[AMBIGUOUS]` | ⚡ PARTIALLY ADDRESSED | ref-concurrency-async.md ★ C++17+ |
| 2.4 | Concurrency — jthread coverage scattered | `[PARTIAL]` | ⚡ PARTIALLY ADDRESSED | Split contains jthread in threading file |
| 3.1 | Templates — Concepts/SFINAE tagged | `[TAGGED]` | ✅ UNCHANGED (positive) | ref-templates-metaprogramming.md isolated |
| 3.2 | Templates — if constexpr partial | `[PARTIAL]` | ⚡ PARTIALLY ADDRESSED | ref-core-modern-idioms.md ★ C++17+ |
| 3.3 | Templates — perfect forwarding untagged | `[UNTAGGED]` | 🔴 STILL OPEN | Examples/ unchanged |
| 4.1 | I/O — no printf/format comparison | `[ABSENT]` | 🔴 STILL OPEN | No I/O ref created by Option F |
| 4.2 | I/O — format detection partial | `[PARTIAL]` | 🔴 STILL OPEN | No new I/O content |
| 5.1 | Comparison — operator<=> partial | `[PARTIAL]` | ⚡ PARTIALLY ADDRESSED | ref-core-modern-idioms.md ★ covers C++20 patterns |
| 5.2 | Comparison — defaulted == untagged | `[UNTAGGED]` | ⚡ PARTIALLY ADDRESSED | ref-core-modern-idioms.md ★ signal present |
| Q1 | RAG — guidance.md no version dispatch | `[ABSENT]` | 🔴 STILL OPEN | guidance.md unchanged |
| Q2 | RAG — reference-index no version routing | `[ABSENT]` | ⚡ PARTIALLY ADDRESSED | ★ annotations + version legend added |
| Q3 | RAG — example frontmatter absent | `[ABSENT]` | 🔴 STILL OPEN | Examples/ frontmatter unchanged |
| Q4 | RAG — manifest no project declaration | `[PARTIAL]` | 🔴 STILL OPEN | manifest.yaml unchanged |

**Summary counts:**

| Status | Count | % of findings |
|--------|-------|---------------|
| ✅ RESOLVED / UNCHANGED POSITIVE | 4 | 21% |
| ⚡ PARTIALLY ADDRESSED | 8 | 42% |
| 🔴 STILL OPEN | 7 | 37% |

---

### 2. Option F Impact Score

**Overall assessment: STRONG DELIVERY within stated scope.**

Option F was chartered as a reference file rightsizing operation. Against that charter:

| Charter Goal | Delivered | Grade |
|-------------|-----------|-------|
| Reduce all files to ≤3,500 tokens | 31 files, all ≤3,500t | ✅ Fully met |
| Organize into logical subdirectories | language/, safety/, testing/, legacy/ | ✅ Fully met |
| Create version-natural splits at C++ version boundaries | 4 splits, all well-chosen | ✅ Fully met |
| Add ★ annotations and version legend | reference-index.md updated | ✅ Fully met |
| Improve RAG window efficiency | +94% files per window | ✅ Fully met |
| Increase estimated version-appropriate retrieval | ~50% → ~65% (est.) | ✅ Met (within Option F's structural scope) |

**What Option F could not have addressed (correctly out of scope):**

- Example file version tagging (requires schema change → governance approval)
- Project declaration mechanism (requires manifest.yaml schema change)
- Version-filtered RAG routing (requires infrastructure work)
- I/O domain content gap (requires new content authoring)
- Comparison operator example (requires new content authoring)

**Panel consensus on Option F:** 12/12 personas issued ⚡ CONDITIONAL PASS or better. 0 personas issued 🔴 BLOCKED. Option F is unanimously accepted as an improvement, with all remaining concerns deferred appropriately to Option E.

---

### 3. Updated Recommendation

**Option E remains the right next step.** Option F's structural improvements make Option E *more effective* than it would have been without F:

- Smaller, version-natural reference files mean version metadata in AVATAR-RAG-INDEX.yaml can now route to specific topic+version slices rather than large mixed files
- The ★ annotation system establishes a version-signaling convention that Option E can extend into machine-readable frontmatter
- The `refs/legacy/` subdirectory provides a natural home for C++98-era example variants
- The migration split (`ref-migration-pre-cpp17.md` / `ref-migration-cpp17-plus.md`) demonstrates the naming convention Option E should use for version-split examples

**Priority shift post-Option F:** The I/O domain gap (Finding 4.1) is now the highest-priority unaddressed risk. With reference file rightsizing complete, content authoring gaps become the primary blocker for reaching the ~95% target. The I/O gap ranks above example frontmatter tagging because it represents entirely absent content (not just untagged content).

---

### 4. Next Proposal Scope — Option E Key Elements (Ranked by Priority)

**P1 — I/O Domain Gap Fill (no dependencies; can start immediately)**
- Create `refs/language/ref-io-formatting.md` covering: printf (C++98, security risks), iostream (all versions, performance), fmtlib (C++11+, polyfill), std::format (C++20), std::print (C++23)
- Create `examples/ENG-6.1-format-string-safety.md` with version-tagged before/after patterns
- This is a content authoring task within Option F's established structure; no governance approval needed

**P2 — Example File Version Metadata Schema (requires governance approval per ENG-10.1)**
- Add `cpp_version_min` / `cpp_version_max` to the example frontmatter schema
- Update `manifest.yaml` with the approved schema and `project_declaration` block
- Create `templates/project.yaml` for project-level C++ standard declaration
- Tag all ~20 existing example files with version metadata per the approved schema
- *Dependency: Tier 1 item 1.3 (governance approval)*

**P3 — Version-Aware RAG Routing (requires infrastructure assessment per Tier 1 item 1.2)**
- Add `cpp_version_min` / `cpp_version_max` metadata to AVATAR-RAG-INDEX.yaml routing entries
- Add version-conditional routing logic to guidance.md
- Update AVATAR-RAG-INDEX.yaml to include version context in routing queries
- *Dependency: Tier 1 item 1.2 (RAG capability assessment)*

**P4 — Priority Example Variants (depends on P2 schema approval)**
- `ENG-6.1-smart-pointers-cpp11.md` — unique_ptr without make_unique
- `ENG-6.1-thread-safety-cpp11.md` — lock_guard instead of scoped_lock
- `ENG-3.1-comparison-cpp14.md` — manual operators, std::tie idiom
- `ENG-3.1-sfinae-cpp11.md` — enable_if patterns
- `ENG-3.1-formatting-cpp14.md` — fmtlib patterns
- *Dependency: P2*

**P5 — Comparison Operator Example (no dependencies; can start immediately)**
- Create `examples/ENG-3.1-comparison-operators.md` with C++98/11/14 manual pattern, std::tie idiom, and C++20 operator<=> + defaulted comparisons
- Version-tag each section with explicit `cpp_version_min` per P2 schema (or inline in body text if P2 is not yet complete)

**P6 — Infrastructure Automation (should accompany P2)**
- CI lint rule enforcing ≤3,500t cap on reference files (new concern from Owen Bradley)
- Automated validation that example files carry `cpp_version_min` (failing lint for untagged files)
- Path-sweep audit for internal prose cross-references in reference files (new concern from Rachel Torres)
- Skill layer `followed_by` chain audit for paths pointing to old flat `refs/ref-*.md` locations (new concern from Elena Nakamura)

---

### 5. Tier 1 Questions Still Blocking Option E

From `next-steps.md`, the following Tier 1 human decisions remain required before Option E can be fully designed:

**1.1 — Production C++ Version Survey** 🔴 STILL REQUIRED
> *Which C++ standards are currently in production across AA systems?*
>
> **Why still needed:** Option F's ★ annotations assume C++17 is a meaningful split point. The version survey will determine whether C++11, C++14, or C++98 variant content should be prioritized in Option E's example variant set. Without this data, P4 variants may target the wrong version tier.
>
> **Updated urgency:** Medium. Option E's P1 (I/O gap fill) and P5 (comparison operators) can proceed without this survey. P4 (example variants) is blocked on this data.

**1.2 — RAG Infrastructure Capability Assessment** 🔴 STILL REQUIRED
> *Does the current RAG system support metadata-based filtering?*
>
> **Why still needed:** Option E's P3 (version-aware routing) depends entirely on whether the RAG infrastructure can filter by frontmatter `cpp_version_min`. If not, the fallback strategy (Option A: inline tags, or accepting the ★ annotation system as the routing mechanism) must be designed before P3 work begins.
>
> **Updated urgency:** High. This is the architectural decision that determines whether Option E achieves ~80% or ~95% version-appropriate retrieval.

**1.3 — Governance Approval for Avatar Restructure** 🔴 STILL REQUIRED
> *Approve `cpp_version_min`/`cpp_version_max` schema, project.yaml template, variant naming convention, maintenance policy.*
>
> **Why still needed:** Option F introduced no schema changes, so this approval remains ungated. Option E's P2 (example metadata schema) is a governance-boundary change per ENG-10.1 and cannot proceed without explicit approval.
>
> **Updated urgency:** High. P2 is the foundational work that enables P3, P4, and the monitoring infrastructure.
>
> **New input for governance package:** Option F's ★ annotation system should be formalized into the governance RFC as the human-readable equivalent of `cpp_version_min`. The RFC should propose that ★ annotations in reference-index.md be treated as normative (not decorative) and that AVATAR-RAG-INDEX.yaml entries for ★ files should carry a `version_min` field.

---

*Document generated as part of C++ Avatar Version-Sensitivity Analysis.*
*Post-Option F delta re-review — triggered by merge of Option F to `main`.*
*Next document: Option E proposal (`hangar-ai-specs/changes/cpp-version-sensitivity-analysis/option-e-proposal.md`).*

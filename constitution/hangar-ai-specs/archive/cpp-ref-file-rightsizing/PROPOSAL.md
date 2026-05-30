# Proposal: C++ Reference File Right-Sizing (Token Budget Compliance)

**Proposal ID:** cpp-ref-file-rightsizing
**Submitted:** April 25, 2026
**Status:** 🟢 REVIEW-CLEARED
**Source:** Version-sensitivity analysis session — `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/restructuring-options.md` Option F
**Prerequisite For:** Any version-sensitivity option (A–E) in the cpp-version-sensitivity-analysis change

---

## Laws Cited (ENG-11.2 Compliance)

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law | Governs proposal lifecycle |
| [ENG-11.2](laws/engineering/eng-11-hangar-sdd.md) | Proposal Completeness | Requires law citations, success criteria, deliverables |
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | RAG retrieval precision is a compliance metric; token target violations are structural defects |
| [ENG-4.1](laws/engineering/eng-4-testing.md) | Atomic TDD Law | All code changes follow RED–GREEN–REFACTOR |
| [ENG-6.7](laws/engineering/eng-6-security.md) | Audit Trail Law | Content routing must be traceable; index files are audit records |

---

## Problem Statement (Per PRD-1.2)

The `cpp-split-reference-architecture` proposal (now complete) split the original `full-reference.md` monolith into 16 topic-aligned reference files with a ≤3,500-token-per-file target. A subsequent token measurement of all 75 avatar files (April 2026) found that **14 of the 16 resulting reference files exceed that target** — some by nearly 2×.

### Measured Token Violations

> Token counts measured April 25, 2026 using actual character counts ÷ 4 (GPT-4 / Claude approximation for mixed prose + C++ code). Conversion factor is consistent with the approximation used when the original target was set.

| File | Tokens | Over Target | Overage |
|------|--------|-------------|---------|
| `ref-testing-ci.md` | 6,975 | +3,475 | +99% |
| `ref-brownfield-config.md` | 6,203 | +2,703 | +77% |
| `ref-migration-playbooks.md` | 5,483 | +1,983 | +57% |
| `ref-concurrency.md` | 5,261 | +1,761 | +50% |
| `ref-object-design.md` | 5,112 | +1,612 | +46% |
| `ref-advanced-cpp.md` | 5,100 | +1,600 | +46% |
| `ref-legacy-smells.md` | 4,809 | +1,309 | +37% |
| `ref-core-language.md` | 4,830 | +1,330 | +38% |
| `ref-domain-modeling.md` | 4,766 | +1,266 | +36% |
| `ref-legacy-mental-models.md` | 4,706 | +1,206 | +34% |
| `ref-build-toolchain.md` | 4,736 | +1,236 | +35% |
| `ref-safety-aviation.md` | 4,274 | +774 | +22% |
| `ref-safety-memory.md` | 4,251 | +751 | +21% |
| `ref-legacy-navigation.md` | 4,247 | +747 | +21% |
| `ref-getting-started.md` | 2,318 | within target | — |
| `ref-infrastructure.md` | 3,082 | within target | — |

**14 of 16 files exceed the target. Average overage: +1,480 tokens (+38%).**

### Impact on RAG Retrieval

At an 8K retrieval window with 1,517 anchor tokens consumed, only **~1.36 reference files fit** on average (6,483 usable ÷ 4,760 avg tokens). This means:

- A single query can load fewer than 1.5 reference files on average
- The probability of loading the version-appropriate reference for any given query is reduced by the large file sizes
- The 14 violations are a **structural defect** introduced during the split: the target was set but not verified post-implementation

---

## Solution

Split all 14 oversized reference files at natural H2 section boundaries into smaller files that individually comply with the ≤3,500-token target. Where a natural section boundary also aligns with a C++ version boundary, use that split — gaining partial version routing at no extra content cost.

**The total corpus size is unchanged.** Splitting redistributes content; it does not add or remove it.

### Split Plan (Measured Section-by-Section)

Files within target — **no change:**

| File | Tokens | Action |
|------|--------|--------|
| `ref-getting-started.md` | 2,318 | Keep as-is |
| `ref-infrastructure.md` | 3,082 | Keep as-is |

Files requiring splits:

| Current File | Tokens | Split | File A | Tokens A | File B | Tokens B | File C | Tokens C |
|---|---|---|---|---|---|---|---|---|
| `ref-testing-ci.md` | 6,975 | 3-way | `ref-testing-ci-policy.md` | 2,730 | `ref-testing-gtest-core.md` | 2,816 | `ref-testing-gtest-advanced.md` | 1,407 |
| `ref-brownfield-config.md` | 6,203 | 2-way | `ref-brownfield-adoption.md` | 2,996 | `ref-brownfield-project-config.md` | 3,183 | — | — |
| `ref-migration-playbooks.md` ★ | 5,483 | 2-way VERSION | `ref-migration-pre-cpp17.md` | 2,162 | `ref-migration-cpp17-plus.md` | 3,321 | — | — |
| `ref-object-design.md` | 5,112 | 2-way (H3) | `ref-object-design-rehabilitation.md` | ~3,443 | `ref-object-design-patterns.md` | ~1,548 | — | — |
| `ref-concurrency.md` ★ | 5,261 | 2-way VERSION | `ref-concurrency-threading.md` | 1,858 | `ref-concurrency-async.md` | 3,412 | — | — |
| `ref-advanced-cpp.md` | 5,100 | 2-way | `ref-templates-metaprogramming.md` | 2,351 | `ref-advanced-patterns.md` | 2,730 | — | — |
| `ref-core-language.md` ★ | 4,830 | 2-way VERSION | `ref-core-type-safety.md` | 2,701 | `ref-core-modern-idioms.md` | 2,108 | — | — |
| `ref-domain-modeling.md` | 4,766 | 2-way | `ref-domain-patterns.md` | 2,207 | `ref-domain-quality.md` | 2,530 | — | — |
| `ref-legacy-smells.md` | 4,809 | 2-way | `ref-legacy-smells-structural.md` | ~2,405 | `ref-legacy-smells-patterns.md` | ~2,404 | — | — |
| `ref-legacy-mental-models.md` | 4,706 | 2-way | `ref-mental-models-memory.md` | ~2,353 | `ref-mental-models-lang.md` | ~2,353 | — | — |
| `ref-build-toolchain.md` ★ | 4,736 | 2-way VERSION | `ref-build-packages.md` | 1,441 | `ref-build-ubsan-msvc.md` | 3,277 | — | — |
| `ref-safety-aviation.md` | 4,274 | 2-way | `ref-safety-jni-abi.md` | 1,035 | `ref-safety-far117-cwr.md` | 3,174 | — | — |
| `ref-safety-memory.md` | 4,251 | 2-way | `ref-safety-misra-do178.md` | 2,401 | `ref-safety-memory-lifetime.md` | 1,873 | — | — |
| `ref-legacy-navigation.md` | 4,247 | 2-way | `ref-legacy-navigation.md` (truncated) | ~1,694 | `ref-legacy-triage-playbook.md` | ~2,464 | — | — |

> ★ = Split boundary aligns with a C++ version boundary — version routing benefit gained at no extra cost.

### Version-Natural Splits (★ files)

| Split | File A covers | File B covers | Version boundary |
|-------|--------------|--------------|-----------------|
| `ref-migration-playbooks.md` | C++98→11, C++11→14, C++14→17 migrations | C++17→20, survival patterns, ActiveTest migration | C++17 |
| `ref-concurrency.md` | `std::thread`, `std::mutex`, `std::atomic`, `std::lock_guard` | Coroutines (`co_await`), `std::stop_token`, resiliency | C++20 |
| `ref-core-language.md` | Const correctness, cast governance, implicit conversions | Designated initializers (C++20), `std::variant` (C++17), null safety | C++17/20 |
| `ref-build-toolchain.md` | vcpkg, CMake, reproducible builds (all versions) | C++20 modules, UBSan/MSVC gap | C++20 |

### Post-Split Corpus State

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Reference file count | 16 | **31** | +15 files |
| Total reference tokens | 76,152 | 76,152 | **unchanged** |
| Average tokens per file | 4,760 | **2,456** | −48% |
| Files exceeding 3,500-token target | 14 of 16 | **0 of 31** | −14 violations |
| Reference files fitting in 8K RAG window | ~1.36 | **~2.64** | +94% |

---

## Directory Organization

After all 14 files are split (Phases 2–15), the 31 reference files are reorganized into four
topic subdirectories under `refs/`. This is performed as an atomic Phase 19 operation — files
are created flat during the split phases, then moved and all link paths finalized together.

### Subdirectory Structure

```
avatars/technology/cpp/
├── guidance.md                ← root — always-loaded RAG anchor (unchanged)
├── manifest.yaml              ← root — machine-readable config (unchanged)
├── reference-index.md         ← root — topic router, links updated to refs/ paths in Phase 19
├── examples/                  ← unchanged
└── refs/
    ├── language/              (9 files) — core language, templates, domain, object design
    ├── safety/                (6 files) — memory safety, aviation safety, concurrency
    ├── testing/               (6 files) — CI policy, GTest, build toolchain, infrastructure
    └── legacy/               (10 files) — legacy navigation, smells, mental models, brownfield, migration
```

### File-to-Subdirectory Mapping

| Subdirectory | Files |
|---|---|
| `refs/language/` | `ref-getting-started.md`, `ref-core-type-safety.md`, `ref-core-modern-idioms.md`, `ref-templates-metaprogramming.md`, `ref-advanced-patterns.md`, `ref-domain-patterns.md`, `ref-domain-quality.md`, `ref-object-design-rehabilitation.md`, `ref-object-design-patterns.md` |
| `refs/safety/` | `ref-safety-misra-do178.md`, `ref-safety-memory-lifetime.md`, `ref-safety-jni-abi.md`, `ref-safety-far117-cwr.md`, `ref-concurrency-threading.md`, `ref-concurrency-async.md` |
| `refs/testing/` | `ref-testing-ci-policy.md`, `ref-testing-gtest-core.md`, `ref-testing-gtest-advanced.md`, `ref-build-packages.md`, `ref-build-ubsan-msvc.md`, `ref-infrastructure.md` |
| `refs/legacy/` | `ref-legacy-navigation.md`, `ref-legacy-triage-playbook.md`, `ref-legacy-smells-structural.md`, `ref-legacy-smells-patterns.md`, `ref-mental-models-memory.md`, `ref-mental-models-lang.md`, `ref-brownfield-adoption.md`, `ref-brownfield-project-config.md`, `ref-migration-pre-cpp17.md`, `ref-migration-cpp17-plus.md` |

### Link Path Finalization (Phase 19)

`reference-index.md` and `avatars/AVATAR-RAG-INDEX.yaml` are updated **twice**:

1. **Phase 16/17 (intermediate):** All links point to flat `ref-*.md` paths. This passes lint and confirms correctness of the split content before reorganization.
2. **Phase 19 (final):** All links re-pointed to `refs/<group>/ref-*.md` subdirectory paths. Lint runs again to confirm the final state.

The two-pass approach keeps each split phase independent and makes Phase 19 the single source of truth for the final directory layout.

---

## Cross-Avatar Impact

This proposal modifies files **outside** `avatars/technology/cpp/`.

### Required Co-Change: `avatars/AVATAR-RAG-INDEX.yaml`

`AVATAR-RAG-INDEX.yaml` explicitly lists all 16 cpp reference files by name with token counts, and contains 40+ query routing examples pointing to them (e.g., `"C++ concurrency thread safety? → ref-concurrency.md"`). After this split:

- The 14 renamed/split source files no longer exist on disk
- `constitution-lint` `index_integrity` validation **will fail** unless `AVATAR-RAG-INDEX.yaml` is updated in the same change
- All 40+ routing examples must be re-pointed to the correct new file names
- Token counts in the index must be updated to post-split values

**This co-change is not optional** — it is a hard dependency. The two files must be updated in the same commit.

### Additional Files Outside `avatars/technology/cpp/` Affected

The cross-reference search (task 1.5) identified the following additional files that must be updated as part of Phase 16 / Phase 17:

| File | Impact | Phase |
|------|--------|-------|
| `avatars/AVATAR-RAG-INDEX.yaml` | **Must update** — file names, token counts, 40+ routing examples | Phase 17 |
| `docs/guides/avatars/split-reference-architecture.md` | **Must update** — File Structure listing enumerates all 14 old file names by name; Token Budget Design section needs post-split figures | Phase 16 |
| `tests/unit/test_cpp_avatar/test_phase10_standard_tiers.py` | **Must update** — hard-codes `ref-brownfield-config.md` path; file is removed by Phase 3 | Phase 3 |
| `tests/unit/test_cpp_avatar/test_phase11_migration_playbooks.py` | **Must update** — hard-codes `ref-migration-playbooks.md` path; file is removed by Phase 4 | Phase 4 |
| `tests/unit/test_cpp_avatar/test_rag_index.py` | **Must update** — asserts exactly 1 reference-index row for `ref-testing-ci.md`; after Phase 2 there are 3 rows | Phase 2 |
| `tools/constitution-lint/` | None — lint validates manifest keys (not names); index_integrity validates paths (handled by AVATAR-RAG-INDEX.yaml update) | — |
| `agent-skills/` | None — skills reference the cpp avatar, not individual ref files | — |
| `hangar-ai-specs/changes/folly-gtest-enrichment/` | **Coordination required** — references `ref-safety-aviation.md`, `ref-safety-memory.md`, `ref-testing-ci.md`, `ref-concurrency.md`, `ref-migration-playbooks.md` in a separate proposal stacked on top of this one; that proposal's maintainers must update references after this proposal merges | Post-merge |

---

## Deliverables

| # | Artifact | Description |
|---|----------|-------------|
| D1 | `ref-testing-ci-policy.md` | CI quality policy and toolchain governance |
| D2 | `ref-testing-gtest-core.md` | GoogleTest core patterns and fixtures |
| D3 | `ref-testing-gtest-advanced.md` | Advanced GTest: templates, concurrency, edge cases |
| D4 | `ref-brownfield-adoption.md` | Brownfield migration strategies and per-tier configs |
| D5 | `ref-brownfield-project-config.md` | Per-project brownfield configuration patterns |
| D6 | `ref-migration-pre-cpp17.md` | Migration playbooks: C++98→11, C++11→14, C++14→17 |
| D7 | `ref-migration-cpp17-plus.md` | Migration playbooks: C++17→20, ActiveTest, survival patterns |
| D8 | `ref-object-design-rehabilitation.md` | Object design anti-patterns 1–6: multiple inheritance, operator overloading, implicit conversions, copy semantics, virtual functions, move semantics |
| D9 | `ref-object-design-patterns.md` | Object design decisions: inheritance vs. composition vs. templates, protected/private inheritance, mixins, test isolation and mock boundaries |
| D10 | `ref-concurrency-threading.md` | Threading: `std::thread`, mutex, atomic, lock_guard |
| D11 | `ref-concurrency-async.md` | Async: coroutines, `co_await`, `std::stop_token`, resiliency |
| D12 | `ref-templates-metaprogramming.md` | Templates, SFINAE, concepts, ADL |
| D13 | `ref-advanced-patterns.md` | Lambdas, preprocessor, allocators, advanced idioms |
| D14 | `ref-core-type-safety.md` | Const correctness, cast governance, implicit conversions |
| D15 | `ref-core-modern-idioms.md` | Designated initializers, `std::variant`, null safety (C++17/20) |
| D16 | `ref-domain-patterns.md` | DDD patterns, DI, ownership models |
| D17 | `ref-domain-quality.md` | Code quality, anti-patterns, domain validation |
| D18 | `ref-legacy-smells-structural.md` | Structural code smells catalog |
| D19 | `ref-legacy-smells-patterns.md` | Pattern-level code smells and remediation |
| D20 | `ref-mental-models-memory.md` | Memory model mental model transitions (GC → C++) |
| D21 | `ref-mental-models-lang.md` | Language mental model transitions |
| D22 | `ref-build-packages.md` | vcpkg, CMake, reproducible builds (all versions) |
| D23 | `ref-build-ubsan-msvc.md` | C++20 modules, UBSan/MSVC gap |
| D24 | `ref-safety-jni-abi.md` | JNI safety and ABI stability |
| D25 | `ref-safety-far117-cwr.md` | FAR 117, CWR anti-patterns, DO-278A context |
| D26 | `ref-safety-misra-do178.md` | MISRA C++ rules and DO-178C compliance |
| D27 | `ref-safety-memory-lifetime.md` | Memory lifetime and FFI safety |
| D28 | `ref-legacy-navigation.md` (truncated) | Legacy codebase orientation: code archaeology, understanding patterns, safe modification, debugging, pitfalls, modernization entry points, skill development path |
| D29 | `ref-legacy-triage-playbook.md` | Legacy codebase triage: week-1 daily priorities, month-1 remediation plan, characterization tests, seam identification, metrics, priority matrix |
| D30 | `reference-index.md` rewrite (Phase 16) | Update from 16 → 31 file entries with flat paths; version boundary annotations for ★ files |
| D31 | `avatars/AVATAR-RAG-INDEX.yaml` update (Phase 17) | Re-point all 40+ query routing examples to new flat file names; update token counts |
| D32 | `avatars/technology/cpp/refs/` tree | Four subdirectories (`language/`, `safety/`, `testing/`, `legacy/`) created in Phase 19 |
| D33 | All 31 files moved into `refs/` subdirs | Each file relocated to its topic subdirectory in Phase 19 |
| D34 | `reference-index.md` path finalization (Phase 19) | All links updated from flat `ref-*.md` to `refs/<group>/ref-*.md` |
| D35 | `avatars/AVATAR-RAG-INDEX.yaml` path finalization (Phase 19) | All routing paths updated to `refs/<group>/ref-*.md`; lint gate confirms |

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| All 31 reference files ≤ 3,500 tokens | Character count ÷ 4 ≤ 3,500 per file |
| Zero content loss | Every section from all 14 source files present in exactly one output file |
| `reference-index.md` updated | All 31 files listed; ★ files annotated with version boundary |
| `AVATAR-RAG-INDEX.yaml` updated | All 40+ routing examples point to valid post-split file names; lint passes |
| Constitution-lint passes | `aa-constitution-lint .` — 0 failures including `index_integrity` |
| All tests pass | Full test suite green after restructure |
| Total reference corpus unchanged | Sum of all 31 reference file tokens = 76,152 ± 100 (rounding only) |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Section boundary cuts shared content | Medium | High | Cross-link split pairs with a "See Also" footer; do not duplicate — link only |
| `ref-legacy-navigation.md` split uses different H2 boundary than original plan | Low | Low | Measured split at `## Legacy Codebase Triage Playbook` (line 90) produces ~1,694 and ~2,464 tokens — both within target. Original split was factually incorrect (3,918 tokens does not meet ≤3,500-token target). Corrected boundary is verified against actual file content. |
| `AVATAR-RAG-INDEX.yaml` update missed or incomplete | Medium | High | Make AVATAR-RAG-INDEX.yaml update a blocking task gate — constitution-lint enforces it |
| Token estimates for H3-split files (4 files marked `~`) exceed target | Low | Medium | Re-measure after split; if any file exceeds 3,500t, split further at next H3 boundary |
| Split files lose navigational coherence for human readers | Low | Low | `reference-index.md` rewrite with clear version and topic annotations addresses this |
| Other proposals referencing old ref file names break | Medium | Medium | Search repo for all references to the 14 renamed files before closing the PR |

---

## Relationship to Other Proposals

| Proposal | Relationship |
|----------|-------------|
| `cpp-split-reference-architecture` | **Predecessor** — created the 16 reference files; this proposal right-sizes them to the token target that was established but not verified |
| `cpp-version-sensitivity-analysis` | **Prerequisite for** — this proposal must complete before any version-sensitivity option (A–E) is adopted; it raises the version-appropriate retrieval baseline from ~50% to ~65% |
| `cpp-avatar-phase18-remediation` | **Independent** — that proposal added missing example files and routing entries; this proposal does not change example files or manifest routing |
| `cpp-manifest-token-exception` | **Unaffected** — that proposal concerns manifest.yaml token budget; this proposal does not touch manifest.yaml |

---

## Taxonomy Gate (skill-30)

Per [skill-30: Taxonomy-Governed Avatar Enrichment](agent-skills/skills-by-domain/discovery-research/30-taxonomy-governed-avatar-enrichment.md):

| Gate | Question | Result | Rationale |
|------|----------|--------|-----------|
| Domain | Durable business capability independent of team names? | ✅ PASS | C++ reference content is a stable engineering capability |
| Boundary | No overlap with existing avatar? | ✅ PASS | Restructures within existing cpp avatar; no new avatar created |
| Stability | Remains valid if org structure changes? | ✅ PASS | Token budget compliance is law-based, not org-dependent |
| Retrieval | Improves RAG precision versus adding ambiguity? | ✅ PASS | +94% reference content per 8K query; 4 version-natural routing boundaries added |
| Scope | Fits within existing `avatars/technology/cpp/` scope? | ✅ PASS (with noted exception) | All content changes within cpp avatar; `AVATAR-RAG-INDEX.yaml` update is a required co-change outside that directory |

---

## Archival Instructions

When all tasks in `tasks.md` are complete and the PR is merged:

```bash
mv hangar-ai-specs/changes/cpp-ref-file-rightsizing \
   hangar-ai-specs/archive/$(date +%Y-%m-%d)-cpp-ref-file-rightsizing
```

Update `PROGRESS.md` status to `COMPLETE` before archiving.

# C++ Version-Sensitive Routing Guide

> **Purpose:** Explains why the C++ avatar routes differently depending on the project's
> declared C++ standard, how detection works, and how to maintain this system as it evolves.
>
> **Audience:** Avatar maintainers, constitution contributors, AI agents, team leads adopting the C++ avatar
>
> **Laws:** [ENG-10.1](../../laws/engineering/eng-10-constitution.md) (Constitution Compliance), [ENG-11.1](../../laws/engineering/eng-11-hangar-sdd.md) (Hangar SDD), [ENG-6.7](../../laws/engineering/eng-6-security.md) (Audit Trail)
>
> **Governing specs:**
> - Foundation (Phase 1): [`hangar-ai-specs/changes/cpp-version-routing-foundation/PROPOSAL.md`](../../../hangar-ai-specs/changes/cpp-version-routing-foundation/PROPOSAL.md)
> - Amendment 1 (Phase 2): [`hangar-ai-specs/changes/cpp-version-routing-foundation/PHASE2-PROPOSAL.md`](../../../hangar-ai-specs/changes/cpp-version-routing-foundation/PHASE2-PROPOSAL.md)
>
> **⚠️ Keep this guide current:** Each future amendment to the C++ version routing system
> must include a task to update this guide. See the amendment strategy note in
> [`tasks-amendment1.md`](../../../hangar-ai-specs/changes/cpp-version-routing-foundation/tasks-amendment1.md).

---

## The Problem This Solves

C++ spans nearly 30 years of language evolution. The gap between C++98 and C++23 is wider than
the gap between most entirely different languages:

| Era | Standard | Key difference from prior |
|-----|----------|--------------------------|
| Pre-modern | C++98 / C++03 | Manual memory management; no threading stdlib; POSIX/Win32 APIs |
| Early modern | C++11 / C++14 | `unique_ptr`, lambdas, `std::thread`, `std::mutex`, move semantics |
| Mid-modern | C++17 | `std::optional`, `std::variant`, `std::scoped_lock`, PMR allocators, filesystem |
| Modern | C++20 | Concepts, coroutines, `std::format`, designated initializers, `std::span`, `<semaphore>` |
| Latest | C++23 | `std::print`, `std::expected`, stackful coroutines improvements |

**The silent failure:** Without version-aware routing, the C++ avatar defaulted to C++20/23
guidance for every query — regardless of the project's actual standard. A developer in a
C++03 codebase received `std::scoped_lock`, concepts, and `std::expected` examples that
would not compile in their toolchain, with no warning.

### American Airlines Production Reality (Evidence Basis)

A production survey of AA's C++ portfolio (April 2026) found:

| Repository | Standard | LOC Share | Risk without routing |
|-----------|---------|-----------|---------------------|
| IOC_ALP, hte_pm_hostconn, CWR, IOC_FosQuery2 | C++14 (toolset default) | ~60% | HIGH — modern advice silently unusable |
| SPEClient | MSVC 6.0 / pre-C++98 | ~24% | CRITICAL — every modern pattern is wrong |
| herc-odyssey-linux | C++98/03 | ~11% | HIGH — modern advice silently unusable |
| IOC_ScreenPrinter, app-mgmt-killapp | C++17 (explicit) | ~5% | LOW — avatar well-matched |

**~95% of AA's C++ LOC was receiving systematically wrong guidance before this fix.**

---

## The Solution: Five-Tier Version Routing

The C++ avatar uses a **five-tier system** that maps C++ standards to named tiers. Each tier
has its own `prefer` and `avoid` lists in `AVATAR-RAG-INDEX.yaml`, directing the agent to
version-appropriate reference files and away from version-incompatible examples.

### Tier Definitions

| Tier | Standards | Routing posture |
|------|-----------|----------------|
| `legacy` | pre-C++98 (MSVC 6.0, `.dsp`/`.dsw` era) | Legacy navigation refs only; warn on any modern pattern |
| `brownfield` | C++98 / C++03 | POSIX/Win32 threading ref, brownfield adoption guide; avoid all C++11+ examples |
| `transitional` | C++11 / C++14 | Type safety, memory lifetime, C++11 threading; avoid C++17+ examples |
| `modern` | C++17 | Full modern ref set; avoid C++20+ coroutines and concepts |
| `greenfield` | C++20 / C++23 | No restrictions; coroutines and concepts refs preferred |

### Conservative Default Rule

If the project's standard is **unknown**, routing falls back to `legacy-safe`:
the agent warns the user and asks for their C++ version before recommending any
version-annotated (`★`) content. It does **not** assume C++14 or any other baseline.

---

## How the C++ Version Is Detected

The agent reads project signals in this priority order:

| Priority | Signal | Field / Pattern |
|----------|--------|----------------|
| 1 | `.copilot/project.yaml` | `cpp.standard` (highest trust — explicit declaration) |
| 2 | `CMakeLists.txt` | `CMAKE_CXX_STANDARD` |
| 3 | `*.vcxproj` / `*.props` | `<LanguageStandard>` element |
| 4 | `Makefile` | `-std=c++XX` compiler flag |
| 5 | `*.dsp` / `*.dsw` (presence alone) | → maps directly to `legacy` tier |

**Priority 1 is the only fully reliable signal.** Build files can contain multiple standards
(mixed-repo scenario), conditional flags, or generator expressions that the agent cannot
evaluate. See "Mixed-Repo Detection" below.

### The `.copilot/project.yaml` Template

Teams should copy `avatars/technology/cpp/templates/cpp-project.yaml` and declare their
standard explicitly:

```yaml
# .copilot/project.yaml — C++ project configuration
cpp:
  schema_version: "1"
  standard: "14"       # Actual C++ standard compiled with: 98 | 03 | 11 | 14 | 17 | 20 | 23
  idiom_level: "03"    # Actual coding idioms in use (may lag standard — e.g., CWR scenario)
  compiler: "gcc"      # msvc | gcc | clang | borland | objective-cpp
  toolset: "gcc-9"     # Optional: compiler version (e.g., MSVC v142, gcc-9, clang-14)
  notes: "CWR migration — standard is C++14 but idiom level is C++03 due to legacy patterns"
```

> **`idiom_level` matters:** A project compiled at C++14 may have been written entirely in
> C++03 idioms (raw pointers, manual memory management, no lambdas). The avatar uses
> `idiom_level` — not `standard` — to select example files when they diverge. This is the
> "CWR scenario" — named for the AA CWR codebase where this pattern was first documented.

### Mixed-Repo Detection

When multiple signals are present, detection uses the priority order above. The most common
mixed scenario:

- **CMakeLists.txt + legacy `.dsp` files**: CMakeLists.txt wins (Priority 2 > Priority 5).
  The `.dsp` files are residual from a migration and do not override the modern build system.
- **`.props` file without a root `.vcxproj`**: Treated as `transitional` (nested project);
  a `.props` file alone does not imply MSVC 6.0 era.

---

## Version Callout Markers in Reference Files

Reference files use `★ C++NN` markers to gate version-specific content within otherwise
multi-version files. There are two forms:

### Section-level callout (heading)

```markdown
## Designated Initializers ★ C++20

Designated initializers allow naming fields in aggregate initialization...
```

This marks the entire section as C++20+. The agent will not serve this section to a
project on C++14 or below.

### Inline callout (code comment)

```cpp
// std::span requires C++20
std::span<const int> view(data.data(), data.size());
```

Used within a multi-version code block to flag a specific line.

### Multi-version reference files

Some reference files (e.g., `ref-io-formatting.md`, `ref-migration-pre-cpp17.md`) intentionally
cover multiple C++ standards in a single file. This is **not** version leakage — it is correct
comprehensive reference behavior. The file's `cpp_version_min` frontmatter indicates the
**minimum required standard to use the file at all**; `★` markers indicate where newer features
begin within it.

---

## Ref File Frontmatter

Every reference file in `refs/**/*.md` must have YAML frontmatter declaring its minimum version:

```yaml
---
cpp_version_min: 11
cpp_version_note: "Primary examples require C++11 (std::thread, std::mutex, std::lock_guard). POSIX fallback provided for C++98/03."
avatar: cpp
---
```

Valid values for `cpp_version_min`: `98`, `11`, `14`, `17`, `20`, `23`.

This frontmatter is validated automatically by `test_phase2d_c4_ref_frontmatter.py` — any
new ref file added without it will fail the test suite.

---

## RAG Routing Architecture

The version routing layer sits **on top of** the split-reference architecture described in
[`split-reference-architecture.md`](split-reference-architecture.md). The combined flow:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Version-Aware RAG Query Flow                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  User: "How do I handle thread safety in this C++ service?"          │
│                                                                      │
│  Step 1 — Version Detection                                          │
│    Read .copilot/project.yaml → cpp.standard: "14"                   │
│    Map to tier: transitional                                         │
│                                                                      │
│  Step 2 — Tier Routing (AVATAR-RAG-INDEX.yaml)                       │
│    transitional.prefer → [ref-core-type-safety.md,                   │
│                            ref-safety-memory-lifetime.md,            │
│                            ref-concurrency-threading.md]             │
│    transitional.avoid  → [ENG-3.7-error-handling.md]                │
│                                                                      │
│  Step 3 — Semantic Routing (search_queries)                          │
│    "thread safety" → matches concurrency search_queries              │
│    Combined top-6 route: ref-concurrency-threading.md wins           │
│                                                                      │
│  Step 4 — Content Filtering                                          │
│    ref-concurrency-threading.md loaded; ★ C++17 scoped_lock          │
│    section is NOT served (project is C++14)                          │
│    Primary GOOD example uses std::lock_guard (C++11) ✓              │
│                                                                      │
│  Step 5 — Response                                                   │
│    Agent answers with C++11/14-compatible patterns only              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

### Token Budget Impact

Version routing adds approximately **0 additional tokens** to the guidance.md load because
the routing policy lives in `AVATAR-RAG-INDEX.yaml`, not in `guidance.md`. The Version Context
Protocol section added to `guidance.md` adds ~90 tokens (within the ≤450t ceiling).

---

## How the Test Suite Enforces This

The following test files validate the routing system:

| Test file | What it checks | Count |
|-----------|---------------|-------|
| `test_rag_index.py` | `version_routing_policy` structure, tier names, prefer/avoid file existence | ~14 tests |
| `test_phase2d_c4_ref_frontmatter.py` | All ref files have valid `cpp_version_min` frontmatter | 107 (auto-discovers) |
| `test_phase2d_d4_version_notes.py` | Version callout boxes present in key ref file sections | 7 tests |
| `test_phase2d_e1_same_tier_mismatch.py` | Same-tier exact-version mismatch warnings (e.g., C++11→C++14) | 22 tests |
| `test_phase2d_e2_mixed_repo_detection.py` | CMakeLists.txt beats .dsp in mixed repo; .props edge cases | 11 tests |
| `test_phase2d_e3_token_automation.py` | Token estimates in YAML within ±25% of actual `words×1.3` | 105 tests |
| `test_phase2_e4_rag_eval.py` | Full RAG routing evaluation: 30 scenarios, 4 metrics | 42 tests |

**Current score:** 30/30 (100%) across all 4 RAG metrics (routing accuracy, tier version
safety, answer coverage, no ungated leakage). Evidence: `cpp-version-sensitivity-analysis/restructuring-results.md`.

> **Token estimate formula:** `word_count × 1.3`. Do **not** use `char_count ÷ 4` — that
> formula overstates estimates by 25–45% and was corrected in Amendment 1 (E3).

---

## Maintaining This System

### Adding a New Reference File

1. Create the file in the appropriate `refs/` subdirectory.
2. Add YAML frontmatter with `cpp_version_min`, `cpp_version_note` (if version ≥ 17), and `avatar: cpp`.
3. Add to `AVATAR-RAG-INDEX.yaml`: entry in `refs_inventory`, search_queries, and the appropriate tier `prefer` list.
4. The `test_phase2d_c4_ref_frontmatter.py` will auto-detect the new file — no test changes needed.
5. Run `test_phase2d_e3_token_automation.py` to verify the token estimate is accurate.

### Adding a New C++ Standard Tier

1. Add a new `by_standard.<tier_name>` block in `AVATAR-RAG-INDEX.yaml`.
2. Add the corresponding tier name to the `## Version Context Protocol` section of `guidance.md`.
3. Update `test_version_routing_policy_has_all_tiers` and `test_routing_policy_tier_names_match_guidance`.
4. Update this guide's tier definitions table.
5. Create a formal amendment proposal in `hangar-ai-specs/changes/cpp-version-routing-foundation/`.

### Adding Version Callouts to a Ref File

1. Identify sections that require a version newer than the file's `cpp_version_min`.
2. Append `★ C++NN` to the section heading.
3. Update `SECTION_LAW_REQUIREMENTS` in `test_law_reference_coverage.py` if the heading is law-referenced.
4. Run the full test suite to verify no regressions.

### Updating Token Estimates

Run the token estimation check to find drifted estimates:

```bash
python -m pytest tests/unit/test_cpp_avatar/test_phase2d_e3_token_automation.py -v
```

Update stale estimates in `AVATAR-RAG-INDEX.yaml` using the `words×1.3` formula.

---

## Deferred Work (Amendment 2 Candidates)

The following items were deferred from Amendment 1 because they require changes outside
the C++ avatar directory. They are tracked in `PHASE2-PROPOSAL.md` Part B:

| Item | What | Where |
|------|------|-------|
| B1 | `schema_version` enforcement lint rule — fail when project.yaml lacks schema_version | `tools/constitution-lint/` |
| B2 | D3 ref-file existence lint rule — fail in adoption repos when prefer/avoid file missing | `tools/constitution-lint/` |
| B3 | Adoption workflow step — explicit C++ version declaration required in onboarding checklist | `docs/guides/adoption/` |
| B4 | Mixed-repo guidance note — clarify CMakeLists.txt wins in `guidance.md` | `guidance.md` (needs 10+ token headroom) |

These require a separate PR with constitution-lint or adoption guide authority.

---

## Amendment History

| Amendment | PR | Key deliverables |
|-----------|-----|-----------------|
| Foundation (Phase 1) | #47 (merged) | `version_routing_policy` in RAG index; `cpp_version_min` on all example files; Version Context Protocol in `guidance.md`; project template |
| Amendment 1 (Phase 2) | #48 (open) | Defect fixes (A1–A3); brownfield concurrency ref; coroutines extraction; 5 priority example variants; I/O ref; version callouts in 4 refs; token automation; RAG eval harness (30/30 100%) |

> **Updating this table:** Every future amendment must add a row here as part of its
> task list. This is the canonical amendment history for the C++ version routing system.

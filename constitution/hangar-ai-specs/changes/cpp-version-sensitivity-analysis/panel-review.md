# Panel Review — C++ Avatar Version-Sensitivity Analysis

> Two-pass protocol evidence records for all factual claims about avatar content.

---

## Protocol Overview

For every finding in this analysis, we applied a mandatory two-pass verification:
1. **Pass 1**: Initial assessment with quoted evidence
2. **Pass 2**: Independent re-read of source file section
3. **Resolution**: If passes agree → `[CONFIDENT]`; if they disagree → Pass 3 tiebreaker

---

## Domain 1: Memory Management

### Finding 1.1: Smart Pointer Guidance Version-Tagging

**Claim**: The avatar's smart pointer guidance does not explicitly tag which patterns apply to C++98/03 vs C++11+.

**Pass 1 Assessment**:
- Source: `examples/ENG-6.1-smart-pointers.md`
- Quoted: The file shows `std::make_unique<FlightPlan>()` with no version qualifier
- The frontmatter contains only `law_id: ENG-6.1` and `avatar: cpp` — no `cpp_version` field
- Conclusion: `[UNTAGGED]`

**Pass 2 Assessment**:
- Re-read `examples/ENG-6.1-smart-pointers.md` lines 1-30
- Confirmed: No version tags in frontmatter. Code examples assume C++14+ (`make_unique`)
- Only contextual note: "Java equivalent" provided but no C++ version context
- Conclusion: `[UNTAGGED]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — Smart pointer examples are version-untagged.

---

### Finding 1.2: auto_ptr Migration Example Has Explicit Version Context

**Claim**: The `auto_ptr` migration example explicitly mentions C++98 and C++11 contexts.

**Pass 1 Assessment**:
- Source: `examples/ENG-6.1-auto-ptr-migration.md`
- Quoted: "Apply this migration to **any C++98/03 codebase** being modernized"
- Also: "std::auto_ptr is **removed** in C++17 and was deprecated since C++11"
- Conclusion: `[TAGGED]` — explicit version context

**Pass 2 Assessment**:
- Re-read same file lines 10-20
- Confirmed: "When to Use: Apply this migration to **any C++98/03 codebase** being modernized"
- Section headers: "NON-COMPLIANT: auto_ptr (C++98)" and "COMPLIANT: unique_ptr (C++11+)"
- Conclusion: `[TAGGED]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — auto_ptr migration is explicitly version-tagged.

---

### Finding 1.3: PMR Allocators Implicitly Assume C++17+

**Claim**: PMR allocator guidance does not specify that `std::pmr` requires C++17.

**Pass 1 Assessment**:
- Source: `examples/ENG-3.1-pmr-allocators.md`
- Code uses `#include <memory_resource>` and `std::pmr::monotonic_buffer_resource`
- No version tag in frontmatter or body text
- Conclusion: `[UNTAGGED]` — C++17 requirement is implicit

**Pass 2 Assessment**:
- Re-read file header and introduction
- The "Java equivalent" note says "PMR is like writing your own garbage collector"
- No mention of C++17 requirement anywhere
- Conclusion: `[UNTAGGED]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — PMR guidance is implicitly C++17+ with no explicit version tagging.

---

### Finding 1.4: RAII Guidance Spans All Versions with Explicit C++98 Pattern

**Claim**: RAII guidance acknowledges C++98 limitations with workaround patterns.

**Pass 1 Assessment**:
- Source: `examples/ENG-6.1-raii-resources.md`
- No explicit version tagging in file
- But `ref-safety-aviation.md` lines 293-310 show "C++98-compatible RAII" patterns
- Quoted from ref-safety-aviation.md: "// COMPLIANT (C++98-compatible RAII)"
- Conclusion: `[PARTIAL]` — Some version-specific guidance exists in reference files but not example files

**Pass 2 Assessment**:
- Re-read `ref-safety-aviation.md` section "AP-6: FILE* Without RAII"
- Confirmed: Shows explicit "C++98-compatible" FileGuard RAII wrapper
- Example files don't carry this context
- Conclusion: `[PARTIAL]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — RAII guidance has partial version coverage; reference files mention C++98 but example files don't.

---

## Domain 2: Concurrency

### Finding 2.1: volatile vs atomic Guidance Explicitly Addresses Version Difference

**Claim**: The avatar clearly explains volatile vs atomic with Java-to-C++ comparison.

**Pass 1 Assessment**:
- Source: `examples/ENG-6.1-volatile-vs-atomic.md`
- Quoted: "This is the **#1 Java→C++ concurrency trap**"
- Table showing Java `volatile` vs C++ `volatile` vs C++ `std::atomic`
- Conclusion: `[TAGGED]` — but only for "Java vs C++", not for C++ version anchors

**Pass 2 Assessment**:
- Re-read file lines 10-30
- Confirmed: "std::atomic" requires C++11 but this is not stated
- The guidance assumes `std::atomic` availability without version qualification
- Conclusion: `[AMBIGUOUS]` — Java comparison tagged, but C++ version not tagged

**Resolution**: Disagreement → Pass 3 required

**Pass 3 Tiebreaker**:
- The file teaches *conceptual* difference (volatile vs atomic) but does not say "std::atomic requires C++11"
- A C++98 developer reading this would not know that `std::atomic` is unavailable to them
- Final ruling: `[AMBIGUOUS]` — conceptually sound but version-insensitive

---

### Finding 2.2: Thread Migration Example Has Strong Version Tagging

**Claim**: Thread migration guidance explicitly addresses C++98/C++11/C++20 differences.

**Pass 1 Assessment**:
- Source: `examples/ENG-6.1-thread-migration.md`
- Quoted: "**C++20+ (preferred):** `std::jthread`"
- Quoted: "**C++11-17:** `std::thread` with a RAII join guard"
- Quoted: "**Legacy C++98:** Keep `pthread_*` but wrap in RAII class"
- Conclusion: `[TAGGED]` — explicit multi-version guidance

**Pass 2 Assessment**:
- Re-read same file header section
- Confirmed all three version anchors are explicitly addressed with recommended patterns
- Conclusion: `[TAGGED]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — Thread migration is well-tagged across versions.

---

### Finding 2.3: Coroutines Guidance Notes C++20 Requirement

**Claim**: Coroutine example explicitly requires C++20.

**Pass 1 Assessment**:
- Source: `examples/ENG-3.1-coroutines.md`
- Code shows `#include <coroutine>` and `co_await`
- Header title includes "(C++20)" in context
- Quoted: "After the first `co_await`, the coroutine frame may resume on a different thread"
- No explicit "C++20 required" statement but features are C++20
- Conclusion: `[AMBIGUOUS]` — features imply C++20 but not explicitly stated

**Pass 2 Assessment**:
- Re-read the opening section
- Found: "Java equivalent: Java's `CompletableFuture` is the closest analogy"
- Found: "start with `std::async` + `std::future` instead" (simpler alternative)
- No explicit "requires C++20" statement
- Conclusion: `[AMBIGUOUS]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — Coroutines guidance is implicitly C++20 but not explicitly tagged.

---

### Finding 2.4: jthread/stop_token Guidance Embedded in Migration Playbook

**Claim**: `std::jthread` and `stop_token` (C++20) are covered in migration playbooks.

**Pass 1 Assessment**:
- Source: `ref-migration-playbooks.md` lines 94-120 (C++17→C++20 playbook)
- Quoted: "Priority 1: `std::span` ... Priority 7: Coroutines"
- `std::jthread` mentioned in thread examples but not in migration priority list
- Conclusion: `[PARTIAL]` — jthread is used in examples but not prominently in migration guidance

**Pass 2 Assessment**:
- Re-read playbook section on C++20
- Confirmed: `std::jthread` not in the priority feature list
- But `ref-concurrency.md` mentions jthread
- Conclusion: `[PARTIAL]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — jthread coverage is scattered, not centralized.

---

## Domain 3: Templates and Generic Programming

### Finding 3.1: Concepts Guidance is C++20-Only with SFINAE Migration Path

**Claim**: Concepts guidance explicitly addresses SFINAE migration from pre-C++20.

**Pass 1 Assessment**:
- Source: `examples/ENG-3.1-concepts.md`
- Quoted: "SFINAE produces unreadable errors. High cognitive complexity violates ENG-3.1 limits."
- Quoted: "Use concepts to constrain template parameters — similar to Java's `<T extends Comparable<T>>`"
- Also: `ref-advanced-cpp.md` has "SFINAE to Concepts Migration Path" table
- Conclusion: `[TAGGED]` — explicit migration path from SFINAE to concepts

**Pass 2 Assessment**:
- Re-read ref-advanced-cpp.md lines 127-140
- Found migration table: "Legacy (SFINAE) | Modern (Concepts) | Migration Notes"
- Shows `std::enable_if_t` → `template <std::integral T>` migration
- Conclusion: `[TAGGED]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — Concepts guidance includes explicit SFINAE migration.

---

### Finding 3.2: `if constexpr` (C++17) Not Explicitly Version-Tagged in Examples

**Claim**: `if constexpr` examples exist but without explicit C++17 tagging.

**Pass 1 Assessment**:
- Source: `ref-migration-playbooks.md` line 75
- Quoted: "Priority 4: `if constexpr` — Eliminates SFINAE for simple compile-time branching"
- This appears in C++14→C++17 migration section, so context is implicit
- No standalone example file for `if constexpr`
- Conclusion: `[PARTIAL]` — contextually tagged in migration playbook only

**Pass 2 Assessment**:
- Searched example files for `if constexpr` — not found as dedicated example
- Found in `ref-legacy-smells.md`: "Replace compile-time branches with `if constexpr` where possible (C++17)"
- Conclusion: `[PARTIAL]` — mentioned but not example-level coverage

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — `if constexpr` has reference-level coverage but no dedicated example.

---

### Finding 3.3: Perfect Forwarding Example Does Not State C++11 Requirement

**Claim**: Perfect forwarding guidance assumes C++11+ without explicit version statement.

**Pass 1 Assessment**:
- Source: `examples/ENG-3.1-perfect-forwarding.md`
- Quoted: "Java equivalent: None. Java passes objects by reference automatically"
- Uses `std::forward` and variadic templates — C++11 features
- No version statement in file
- Conclusion: `[UNTAGGED]`

**Pass 2 Assessment**:
- Re-read file introduction
- Confirmed: No mention that `std::forward` requires C++11
- A pre-C++11 developer would not understand availability constraints
- Conclusion: `[UNTAGGED]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — Perfect forwarding is untagged for version.

---

## Domain 4: I/O and Streams

### Finding 4.1: No Dedicated printf/iostream/std::format Comparison

**Claim**: The avatar lacks explicit guidance on `printf` vs `iostream` vs `std::format` across versions.

**Pass 1 Assessment**:
- Searched all example files: No `ENG-*-printf.md` or `ENG-*-format.md` file exists
- `ref-infrastructure.md` mentions spdlog but not `std::format` vs alternatives
- `ref-migration-playbooks.md` line 193 mentions `fmt::format` as polyfill but no comparison table
- Conclusion: `[ABSENT]` — no comprehensive I/O formatting guidance

**Pass 2 Assessment**:
- Re-searched reference files for "printf", "iostream", "std::format"
- Found in `ref-migration-playbooks.md`: "`fmt::format` → backport of `std::format` for pre-C++20"
- No explicit security/performance comparison between printf/iostream/format
- Conclusion: `[ABSENT]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — I/O formatting comparison is absent from avatar.

---

### Finding 4.2: Feature Detection Example Shows std::format Polyfill Pattern

**Claim**: Feature detection example shows how to conditionally use `std::format` vs `fmt`.

**Pass 1 Assessment**:
- Source: `examples/ENG-3.1-feature-detection.md`
- Quoted code:
  ```cpp
  #ifdef __has_include
    #if __has_include(<format>)
      #include <format>
      #define HAS_STD_FORMAT 1
    #else
      #include <fmt/format.h>
      #define HAS_STD_FORMAT 0
    #endif
  #endif
  ```
- Conclusion: `[PRESENT]` — conditional I/O formatting is demonstrated

**Pass 2 Assessment**:
- Re-read same file
- Confirmed: This is the only place in the avatar that addresses `std::format` availability
- However, it's a feature-detection technique, not a comparison of approaches
- Conclusion: `[PARTIAL]` — technique present but not comprehensive comparison

**Resolution**: Disagreement → Pass 3 required

**Pass 3 Tiebreaker**:
- The file shows *how* to detect format, not *why* to prefer format over printf
- No security guidance (e.g., format string injection in printf)
- Final ruling: `[PARTIAL]` — detection technique present but guidance incomplete

---

## Domain 5: Comparison and Operators

### Finding 5.1: No Dedicated operator<=> Example File

**Claim**: The avatar lacks a dedicated example for C++20 three-way comparison.

**Pass 1 Assessment**:
- Listed all example files — no `ENG-*-spaceship.md` or `ENG-*-comparison.md`
- Searched `ref-migration-playbooks.md` for "<=>" and "three-way"
- Found: "Priority 2: Three-way comparison (`<=>`) — Eliminates boilerplate comparison operators"
- Conclusion: `[ABSENT]` at example level but `[PRESENT]` at reference level

**Pass 2 Assessment**:
- Re-read migration playbook C++17→C++20 section
- Confirmed: Three-way comparison listed as Priority 2 feature
- No dedicated example file exists
- Conclusion: `[PARTIAL]` — migration mentioned but no example

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — operator<=> is mentioned but has no example.

---

### Finding 5.2: Defaulted Comparison Mentioned in Domain Modeling

**Claim**: `operator==() = default` pattern is shown in domain modeling reference.

**Pass 1 Assessment**:
- Source: `ref-domain-modeling.md` lines 60-80 (Value Object Pattern)
- Quoted: `bool operator==(const Money& other) const = default;`
- This is a C++20 feature but not version-tagged
- Conclusion: `[PRESENT]` but `[UNTAGGED]`

**Pass 2 Assessment**:
- Re-read the Money class example
- Confirmed: `operator== ... = default` shown
- No note that this requires C++20
- Conclusion: `[PRESENT]` but `[UNTAGGED]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — Defaulted comparison is shown but not version-tagged.

---

## RAG Routing Analysis Findings

### Q1: guidance.md Version Dispatch Logic

**Pass 1 Assessment**:
- Source: `guidance.md` (full file)
- Scanned entire file for "if project is", "C++98", "version", "standard"
- Found: No conditional routing based on C++ version
- The file links to `reference-index.md` without version filtering
- Conclusion: `[ABSENT]` — no version dispatch

**Pass 2 Assessment**:
- Re-read guidance.md
- Confirmed: Single link "→ **[Reference Index](reference-index.md)**"
- No conditional "if your project is C++98, see X" logic
- Conclusion: `[ABSENT]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — guidance.md lacks version dispatch.

---

### Q2: reference-index.md Version-Conditional Routing

**Pass 1 Assessment**:
- Source: `reference-index.md` (full file)
- Scanned for version-conditional links
- Found: Section headers by topic (Core Language, Testing, etc.) not by version
- Migration Playbooks section exists but is one link, not version-filtered
- Conclusion: `[ABSENT]` — no version-conditional routing

**Pass 2 Assessment**:
- Re-read reference-index.md
- Confirmed: All links are topic-based, not version-based
- A C++98 developer would load the same files as a C++23 developer
- Conclusion: `[ABSENT]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — reference-index lacks version filtering.

---

### Q3: Example File Version Metadata

**Pass 1 Assessment**:
- Sampled 8 example files from frontmatter
- All contain: `law_id:`, `avatar:` — no `cpp_version:` field
- Exception: `ENG-6.1-auto-ptr-migration.md` has version context in body text
- Conclusion: `[ABSENT]` — no frontmatter version metadata

**Pass 2 Assessment**:
- Re-checked same 8 files
- Confirmed: No `cpp_version`, `min_standard`, or similar field exists in any frontmatter
- Conclusion: `[ABSENT]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — Example files lack version metadata.

---

### Q4: Project Standard Declaration Mechanism

**Pass 1 Assessment**:
- Source: `manifest.yaml` (full file)
- Found `version_policy:` section with greenfield/brownfield guidance
- Quoted: "greenfield: C++20 minimum (mandatory); C++23 recommended"
- Quoted: "brownfield: Older standards permitted with documented modernization plan"
- No `cpp_standard` field for project-level declaration
- Conclusion: `[PARTIAL]` — policy exists but no project declaration mechanism

**Pass 2 Assessment**:
- Re-read manifest.yaml for `project.md` template or similar
- Found: `brownfield_cpp98:` and `brownfield_mfc_cpp98:` convention sections
- These describe patterns, not a declarative project config
- Conclusion: `[PARTIAL]`

**Resolution**: Pass 1 and Pass 2 agree → `[CONFIDENT]` — Version policy exists but no project declaration field.

---

## Summary of Panel Review

| Finding ID | Domain | Verdict | Confidence |
|------------|--------|---------|------------|
| 1.1 | Memory | `[UNTAGGED]` | `[CONFIDENT]` |
| 1.2 | Memory | `[TAGGED]` | `[CONFIDENT]` |
| 1.3 | Memory | `[UNTAGGED]` | `[CONFIDENT]` |
| 1.4 | Memory | `[PARTIAL]` | `[CONFIDENT]` |
| 2.1 | Concurrency | `[AMBIGUOUS]` | `[CONFIDENT]` (after Pass 3) |
| 2.2 | Concurrency | `[TAGGED]` | `[CONFIDENT]` |
| 2.3 | Concurrency | `[AMBIGUOUS]` | `[CONFIDENT]` |
| 2.4 | Concurrency | `[PARTIAL]` | `[CONFIDENT]` |
| 3.1 | Templates | `[TAGGED]` | `[CONFIDENT]` |
| 3.2 | Templates | `[PARTIAL]` | `[CONFIDENT]` |
| 3.3 | Templates | `[UNTAGGED]` | `[CONFIDENT]` |
| 4.1 | I/O | `[ABSENT]` | `[CONFIDENT]` |
| 4.2 | I/O | `[PARTIAL]` | `[CONFIDENT]` (after Pass 3) |
| 5.1 | Comparison | `[PARTIAL]` | `[CONFIDENT]` |
| 5.2 | Comparison | `[UNTAGGED]` | `[CONFIDENT]` |
| Q1 | RAG | `[ABSENT]` | `[CONFIDENT]` |
| Q2 | RAG | `[ABSENT]` | `[CONFIDENT]` |
| Q3 | RAG | `[ABSENT]` | `[CONFIDENT]` |
| Q4 | RAG | `[PARTIAL]` | `[CONFIDENT]` |

---

*Document generated as part of C++ Avatar Version-Sensitivity Analysis.*

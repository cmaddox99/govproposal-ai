# Session Prompt — C++ Avatar Version-Sensitivity Analysis

**Date:** 2026-04-25  
**Initiated by:** AA Engineering (via Copilot CLI session 4b65e7f5)  
**Change directory:** `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/`

---

## Subject: C++ Avatar Version-Sensitivity Analysis — Quality, RAG Routing, and Restructuring Recommendations

---

### Background & Concern

The current C++ avatar (`avatar-technology-cpp`) spans the entire C++ version spectrum — from C++98/03 through C++23 (and prospectively C++26 when ratified) — under a single document set. This is problematic because the language, standard library, idioms, and best practices change **substantially** across versions. Advice that is correct and idiomatic for C++98 (raw `new`/`delete`, manual RAII, `std::auto_ptr`, integer error codes) is **incorrect or deprecated** in C++20/23 (smart pointers, `std::expected`, coroutines, spaceship operator). In a large organization where deep C++ expertise is declining, the risk of an AI delivering version-inappropriate guidance — and that guidance going unrecognized as wrong — is significant.

The avatar already defines tiers (greenfield C++20/23, active brownfield C++14/17, legacy C++11, frozen C++98/03) and includes migration playbooks. The open question is whether the **RAG retrieval routing**, **example corpus**, and **guidance prose** are sufficiently version-aware to deliver correct, context-sensitive advice — or whether they collapse toward modern idioms regardless of the project's declared standard.

The C++ version to treat as "current maximum" in this analysis is **C++23** (ISO/IEC 14882:2024, widely supported as of 2025). C++26 is in active development; flag it where relevant but do not treat it as ratified.

---

### Task 1 — Avatar Quality Audit (Evidence Generation)

Comprehensively examine the current C++ avatar files (`avatars/technology/cpp/`) to produce **structured evidence** about version sensitivity across the following five problem domains. For each domain, analyze behavior at three version anchors: **C++98/03**, **C++14**, and **C++23**.

| # | Problem Domain | Key Constructs to Examine |
|---|---|---|
| 1 | **Memory Management** | `new`/`delete` vs `unique_ptr`/`shared_ptr` vs PMR allocators; `auto_ptr` deprecation; `make_unique`/`make_shared`; ownership transfer idioms |
| 2 | **Concurrency** | `volatile`+global flags vs `std::thread`+mutex vs `std::atomic` vs `std::jthread`+`stop_token`; coroutines (`co_await`/`co_yield`); `std::latch`/`std::barrier` |
| 3 | **I/O and Streams** | `printf`/`scanf` vs `iostream` vs `std::format` (C++20) vs `std::print` (C++23); stream locale pitfalls; format string injection risks |
| 4 | **Templates and Generic Programming** | SFINAE patterns vs `if constexpr` vs Concepts (`requires`); variadic macros vs variadic templates; `auto` function parameters (C++20) |
| 5 | **Comparison and Operators** | Manual `operator<`/`operator==` vs `operator<=>` (three-way comparison, C++20); defaulted comparisons; `std::strong_ordering` |

**For each domain × version anchor, determine:**
- What guidance does the current avatar provide (cite the specific file and section)?
- Is the guidance explicitly version-tagged, or is it version-ambiguous?
- Would the guidance mislead a developer working on a project at that version anchor?
- Is there a concrete example in the example corpus (`examples/`) for this version anchor?

**Evidence quality protocol:** For each finding that seems clear on first pass, generate a second independent assessment of the same file/section before recording the conclusion. If the two assessments conflict, generate a third as a tiebreaker and record all three with your final ruling. Mark findings as `[CONFIDENT]`, `[CONTESTED]`, or `[UNCERTAIN]` accordingly.

---

### Task 2 — RAG Routing Analysis

Analyze how the avatar's RAG retrieval structure routes queries to version-appropriate content. Specifically:

1. **Does the `guidance.md` anchor (always-loaded) contain version dispatch logic**, or does it load the same content regardless of project C++ standard?
2. **Does the `reference-index.md` provide version-conditional routing** (e.g., "for C++98 projects, see X; for C++20+ projects, see Y"), or is it version-agnostic?
3. **Do the example files carry version metadata** (frontmatter, headers, or labels) that a RAG retriever could use to filter by standard?
4. **How does a project's declared C++ standard propagate** into retrieval context? Is there a mechanism (e.g., `project.md`, manifest field, environment variable) for a project to declare its standard and have that affect which examples are retrieved?
5. **Assess token budget impact**: Given that the reference index points to ~15 reference files each sized at ≤3,500 tokens, what is the risk of version-inappropriate content being retrieved when a developer asks a question without specifying their C++ standard?

Apply the same two-pass evidence protocol from Task 1, with tiebreakers for contested findings.

---

### Task 3 — Restructuring Options

Based on the evidence from Tasks 1 and 2, evaluate the following restructuring strategies and produce a ranked recommendation with rationale:

| Option | Description | Key Trade-offs |
|---|---|---|
| **A — Inline Version Tags** | Add `[C++98]`/`[C++14]`/`[C++20+]` tags throughout existing files; update RAG routing to filter by declared standard | Minimal disruption; risk of tag drift |
| **B — Version-Segmented Sections** | Split each reference file into per-version sections with explicit routing rules in `reference-index.md` | Better structure; larger individual files; token budget pressure |
| **C — Separate Avatar Instances** | Create `avatar-technology-cpp98`, `avatar-technology-cpp14`, `avatar-technology-cpp20` as separate manifests sharing a common law core | Clean separation; higher maintenance overhead; clearer RAG routing |
| **D — Project-Standard Declaration** | Add a `cpp_standard` field to `project.md` / manifest; update RAG router to use it for conditional retrieval | Requires project adoption; no change to avatar files themselves |
| **E — Hybrid: Declaration + Segmented Examples** | Combine Option D (project declaration) with per-version example corpus (separate `examples/v98/`, `examples/v14/`, `examples/v20/`) | Best precision; highest restructuring effort |

Include a recommendation for how `project.md` (local project configuration files) should document the C++ standard decision and whether transitioning vs. non-transitioning projects should receive different guidance paths.

---

### Task 4 — Next Steps and Investigation Backlog

Produce a prioritized list of recommended next steps, including:
- Any questions that require human input (e.g., which C++ versions are actually in production at AA today)
- Proof-of-concept experiments needed to validate the RAG routing hypothesis
- Specific files that need to be updated if any restructuring option is adopted
- Governance questions (e.g., who approves a new avatar split)

---

### Recording Requirements

Maintain all session artifacts within `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/`. Record:

- This improved prompt (as `session-prompt.md`) ← **this file**
- The full evidence matrix from Task 1 (as `evidence-audit.md`)
- The RAG routing analysis from Task 2 (as `rag-routing-analysis.md`)
- The multi-pass review records including all panel responses and tiebreakers (as `panel-review.md`)
- The restructuring recommendations from Task 3 (as `restructuring-options.md`)
- The next-steps backlog from Task 4 (as `next-steps.md`)
- A running log of key prompts and responses in this session (as `session-log.md`)

---

### Operating Protocol

- **Treat this as a deep analysis task, not a timely one.** Thoroughness takes precedence over speed.
- **For any finding or recommendation you are uncertain about:** generate a second independent response, compare, and combine. If the two conflict, generate a third as a tiebreaker. Record all passes in `panel-review.md`.
- **Flag hallucination risk explicitly:** When citing avatar file contents, quote the actual text; do not paraphrase from memory.
- **Ask clarifying questions** before proceeding if any aspect of the scope is ambiguous.

---

*Original prompt submitted by user 2026-04-25. Improved by Copilot CLI (claude-sonnet-4.6) before execution.*

# Governance Decision Record: C++ Avatar Schema Extensions

**Record ID:** GDR-cpp-version-routing-foundation  
**Date Issued:** 2026-04-25  
**Status:** 🟢 CONDITIONS MET — APPROVED FOR IMPLEMENTATION  
**Parent Proposal:** `hangar-ai-specs/changes/cpp-version-routing-foundation/PROPOSAL.md`  
**Governing Law:** ENG-11.1 (Hangar SDD Law), ENG-11.2 (Proposal Completeness Law)

---

## Purpose

This document records the formal governance decisions required before implementation of the
`cpp-version-routing-foundation` proposal can begin. It identifies:

1. All new schema artifacts introduced by the proposal
2. The design decisions made for each artifact
3. The decision rationale and alternatives considered
4. The governance verdict (approved / rejected / deferred with conditions)

Three specific schema artifacts require governance approval because they introduce **new fields**
or **new artifact types** that have not previously existed in the avatar system:

| Artifact | Type | Scope | Law requiring approval |
|----------|------|-------|----------------------|
| `cpp_version_min` / `cpp_version_note` frontmatter | New fields on existing files | Avatar-internal | ENG-11.2 (completeness) |
| `.copilot/project.yaml` declaration mechanism | New artifact type in consuming repos | Cross-repo | ENG-11.1 (significant work) |
| `version_routing_policy` block in AVATAR-RAG-INDEX.yaml | New routing construct | Avatar infrastructure | ENG-11.2 (completeness) |

---

## Decision 1 — Example File Frontmatter: `cpp_version_min` and `cpp_version_note`

### Proposed Schema

```yaml
---
law_id: ENG-6.1
avatar: cpp
cpp_version_min: 17         # NEW: earliest C++ standard supporting all patterns in this file
cpp_version_note: |         # NEW: agent-visible warning when project is below cpp_version_min
  "Uses std::scoped_lock (C++17). For C++11–14, use std::lock_guard<std::mutex> instead."
---
```

### Design Decisions Made

**D1.1 — Single minimum, not a range**  
`cpp_version_min` stores the earliest compatible version (integer: 98, 11, 14, 17, 20, 23).
No `cpp_version_max` is introduced. If a pattern is superseded but still valid, the note
communicates that; we do not encode an upper bound as a hard filter.

*Rationale:* A max bound creates an exclusion risk — a file that works in C++17 still works in
C++23; blocking it by max would silently drop relevant content. The `cpp_version_note` handles
"prefer X instead in newer standards" guidance in prose, which is more informative.

*Alternative considered:* `cpp_version_range: [14, 23]` — rejected: encodes false ceiling.

**D1.2 — `cpp_version_note` is plain English, agent-rendered**  
The note is a human-readable string the agent surfaces when the project standard is below
`cpp_version_min`. It is NOT a code block, NOT a routing instruction, and NOT a link.

*Rationale:* The note is loaded only when relevant (version mismatch). Keeping it prose
maximizes semantic richness within a tight token budget.

**D1.3 — Files with `cpp_version_min: 11` or lower do NOT require `cpp_version_note`**  
C++11 is the floor of active AA brownfield toolchains. Files at `cpp_version_min: 11` are
appropriate for all non-legacy content. No note is needed for "everybody can use this."

*Rationale:* Reduces noise. A file like `ENG-7.2-circuit-breaker.md` (C++11 `std::atomic`)
needs no warning — CWR (C++14) and herc-odyssey (C++98/03) are the only cases below C++11.

**D1.4 — `cpp_version_min: 98` means "safe for C++98 and later ISO C++ standards"**  
One existing file (`ENG-2.3-rcptr-abi-stability.md`) uses C++98 RCPtr pattern and is
explicitly designed for legacy codebases. Its `cpp_version_min: 98` marks it as the most
broadly applicable content in the avatar *within the ISO C++ range*.

> **Note (B2 resolution):** This does NOT mean "safe for pre-C++98 (MSVC 6.0) projects."
> The `legacy` tier in the routing policy explicitly covers pre-C++98; files tagged `98`
> should be reviewed before serving to `standard: "pre98"` projects.

**D1.5 — Untagged files are treated as `cpp_version_min: 20` by the routing policy**  
Any example file lacking `cpp_version_min` frontmatter is assumed to require C++20+.
This is a conservative default that prevents silently serving unvalidated content to legacy
projects — it forces explicit opt-in to legacy compatibility.

*Risk:* Files added without frontmatter after this change will be invisible to C++14/17 projects
until tagged. This is intentional: the failure mode is "file not served" not "wrong file served."

### Open Questions for Panel

- OQ-1.1: Should `cpp_version_note` have a character limit? (Token budget consideration.)
- OQ-1.2: Should the field be named `cpp_version_min` or `min_cpp_standard`? Consistency with
  YAML naming conventions across the avatar system?
- OQ-1.3: Should C++11 files also receive `cpp_version_note` for the benefit of C++98/03
  projects (herc-odyssey, SPEClient)?

---

## Decision 2 — Project Declaration: `.copilot/project.yaml`

### Proposed Schema (Consuming Repository)

```yaml
# .copilot/project.yaml — placed in consuming repository root
cpp:
  standard: "14"        # Compiler standard: pre98 | 98 | 03 | 11 | 14 | 17 | 20 | 23
  idiom_level: "03"     # Actual idiom/pattern level (may differ from standard)
  compiler: "gcc"       # msvc | gcc | clang | other
  toolset: "7"          # GCC: major version | MSVC: v140–v143 | Clang: major version
  schema_version: "1"   # Template version — bump when schema changes
  notes: "C++14 compiler, but only C++03 idioms in use — no C++11 features yet adopted"
```

### Template Delivery

A canonical template is delivered at `avatars/technology/cpp/templates/cpp-project.yaml`
in this repository. Teams copy it to `.copilot/project.yaml` in their project root.

### Design Decisions Made

**D2.1 — `.copilot/` directory prefix, not project root**  
The file lives in `.copilot/project.yaml`, not `project.yaml`. The `.copilot/` prefix scopes
it as an AI tooling configuration file (parallel to `.github/` for CI), reducing the risk of
collisions with existing project files named `project.yaml` (CMake, VSCode, etc.).

*Alternative considered:* `project-cpp.yaml` at root — rejected: no scoping, collision risk.  
*Alternative considered:* `.hangar/project.yaml` — possible; `.copilot/` preferred because
GitHub Copilot context files already use this convention in some projects.

**D2.2 — `standard` vs `idiom_level` split: `standard` is required, `idiom_level` is optional**  
`standard` is a required field — the only field teams must fill in. `idiom_level` is optional
and defaults to the value of `standard` when absent. The split is the key insight for CWR:
C++14 compiler but C++03 idioms in use — routing must use `idiom_level` for pattern/idiom
questions and `standard` for feature-availability questions.

*Rationale:* The field is mandatory in concept (every project has a standard) but optional
in the file (defaults to standard). This resolves the panel's D2.2 inconsistency flag.

**D2.3 — Detection priority order (for projects without project.yaml)**  
When `.copilot/project.yaml` is absent, the agent falls back to:
1. `CMakeLists.txt`: `CMAKE_CXX_STANDARD` or `target_compile_features(cxx_std_NN)`
2. `.vcxproj`: `<LanguageStandard>stdcppNN</LanguageStandard>`  
3. `Makefile`: `-std=c++NN` in CXXFLAGS  
4. `.dsp` or `.dsw` presence: → MSVC 6.0 / pre-C++98 flag  
5. No detection: → default to `legacy-safe` content + agent prompts for version

**D2.4 — The template is versioned via avatar `manifest.yaml` version number**  
When the template schema changes, the avatar `manifest.yaml` version bumps. Consuming repos
are notified through normal avatar update channels. No separate template versioning needed.

**D2.5 — Opt-in, not required**  
Consuming repos are NOT required to add `.copilot/project.yaml`. The avatar functions without
it using the fallback detection chain in D2.3. The project.yaml provides a deterministic,
explicit override of the fallback detection.

*Risk:* Low adoption — most AA repos will not add this file initially. Fallback detection
handles the majority of cases; the file is most valuable when fallback detection is ambiguous
or wrong (e.g., SPEClient with its `.dsp` files).

### Open Questions for Panel

- OQ-2.1: Should `.copilot/project.yaml` be named `cpp-context.yaml` to be language-specific?
  (A future Java avatar might also want a project.yaml — namespace collision concern.)
- OQ-2.2: Should `compiler: "borland"` be in scope? supportATIS uses Borland VCL but it was
  classified as out-of-scope for the C++ avatar. Is the compiler field misleading for VCL?
- OQ-2.3: Is `.copilot/` the right directory? Are there existing AA conventions we should align to?

---

## Decision 3 — AVATAR-RAG-INDEX.yaml: `version_routing_policy` Block

### Proposed Schema Addition

```yaml
# Added to the cpp: section of AVATAR-RAG-INDEX.yaml
version_routing_policy:
  detection_order:
    - path: .copilot/project.yaml           # explicit project declaration (highest priority)
    - path: CMakeLists.txt                  # CMAKE_CXX_STANDARD or target_compile_features
    - glob: "*.vcxproj"                     # <LanguageStandard>stdcppNN</LanguageStandard>
    - path: Makefile                        # -std=c++NN in CXXFLAGS
    - glob_any: ["*.dsp", "*.dsw"]         # MSVC 6.0 / pre-C++98 indicator
  fallback: legacy-safe                     # when version is undetectable
  by_standard:
    legacy:                                 # pre-C++98 (MSVC 6.0, .dsp/.dsw present)
      prefer:
        - refs/legacy/ref-legacy-navigation.md
        - refs/legacy/ref-mental-models-lang.md
        - refs/legacy/ref-legacy-smells-structural.md
      avoid:
        - examples/ENG-3.7-error-handling.md
        - examples/ENG-6.1-thread-safety.md
        - examples/ENG-3.1-concepts.md
      warn: "⛔ Pre-C++98 toolchain detected (MSVC 6.0 / .dsp/.dsw). Modern C++ patterns are not applicable."
    brownfield:                             # C++98 / C++03
      prefer:
        - refs/legacy/ref-legacy-navigation.md
        - refs/legacy/ref-brownfield-adoption.md
        - refs/legacy/ref-brownfield-project-config.md
      avoid:
        - examples/ENG-3.7-error-handling.md
        - examples/ENG-3.1-concepts.md
        - examples/ENG-3.1-coroutines.md
    transitional:                           # C++11 / C++14
      prefer:
        - refs/language/ref-core-type-safety.md
        - refs/safety/ref-safety-memory-lifetime.md
        - refs/safety/ref-concurrency-threading.md
      avoid:
        - examples/ENG-3.7-error-handling.md
        - examples/ENG-3.1-concepts.md
        - examples/ENG-3.1-pmr-allocators.md
    modern:                                 # C++17
      prefer:
        - refs/language/ref-core-type-safety.md
        - refs/safety/ref-safety-memory-lifetime.md
        - refs/language/ref-advanced-patterns.md
      avoid:
        - examples/ENG-3.7-error-handling.md
        - examples/ENG-3.1-concepts.md
        - examples/ENG-3.1-coroutines.md
    greenfield:                             # C++20 / C++23
      prefer: []
      avoid: []
  unknown:
    strategy: legacy-safe
    agent_prompt: |
      "No C++ standard detected. Using conservative (legacy-safe) routing.
       Add .copilot/project.yaml to declare your project's C++ standard for precise routing."
```

### Design Decisions Made

**D3.1 — Five tiers, not one per standard**  
Version tiers map to advisory categories rather than each specific standard. This reduces
maintenance (6 standards × future growth) and avoids false precision. The tiers match the
`manifest.yaml` brownfield/greenfield split that already exists.

| Tier | Standards | AA Repositories |
|------|-----------|-----------------|
| legacy | pre-C++98 (MSVC 6.0) | SPEClient (~24% LOC) |
| brownfield | C++98, C++03 | herc-odyssey-linux (~11% LOC) |
| transitional | C++11, C++14 | IOC_ALP, hte_pm_hostconn, CWR, IOC_FosQuery2 (~60% LOC) |
| modern | C++17 | IOC_ScreenPrinter, app-mgmt-killapp (~5% LOC) |
| greenfield | C++20, C++23 | (new projects only) |

**D3.2 — `avoid` list is advisory, not a hard filter**  
The agent SHOULD NOT serve files in the `avoid` list for the detected tier, but this is a
routing preference, not a technical enforcement gate. The agent can override if a user
explicitly asks about a specific modern feature.

*Rationale:* Hard filtering would block valid queries like "explain C++20 concepts so I can
plan a future migration from C++14." The avoid list guides default routing; explicit questions
override it.

**D3.3 — `unknown` fallback is `legacy-safe`, not `greenfield`**  
When no version is detected, the system routes to conservative content and prompts the agent
to ask. This is a deliberate reversal of the current default (which assumes C++20).

*Rationale:* 95% of AA's C++ LOC is below C++20. A conservative default produces correct
guidance for 95% of cases without project.yaml; a modern default produces correct guidance
for only 5%.

### Open Questions for Panel

- OQ-3.1: Should `avoid` lists be per-`law_id` rather than per filename? (More stable as files
  are refactored or renamed.) 
- OQ-3.2: Is a 5-tier model sufficient, or is C++11 meaningfully different enough from C++14
  to warrant a split? (The CWR case: compiler is C++14 but `idiom_level` is C++03 — handled
  by `idiom_level` field, but the tier boundary may still matter.)
- OQ-3.3: Should the routing policy be in AVATAR-RAG-INDEX.yaml or in `guidance.md`? The
  index file is agent-read infrastructure; guidance.md is agent-executed instructions.
  Currently split between both — is this the right split?

---

## Governance Verdict (Completed — 2026-04-25; Conditions Met — 2026-04-25)

Panel review: `governance-panel-review.md`  
Remediation: B1–B5 all resolved in this document + `PROPOSAL.md` + `tasks.md`

| # | Decision | Status | Conditions Met |
|---|----------|--------|---------------|
| D1 | Example frontmatter: `cpp_version_min` / `cpp_version_note` | ✅ APPROVED | D1.4 semantics updated (pre98 ≠ cpp98); 240-char note limit added to tasks (1.13); version audit task added (4.21); ENG-6.7 corrected to C++20, ENG-7.1 corrected to C++11 |
| D2 | Project declaration: `.copilot/project.yaml` schema | ✅ APPROVED | `pre98` added to `standard` enum; `schema_version` field added; `borland` replaced with `other`; `idiom_level` clarified as optional |
| D3 | Routing policy: `version_routing_policy` block | ✅ APPROVED | All file refs replaced with real repo paths; tier vocabulary canonicalized (`legacy`/`brownfield`/`transitional`/`modern`/`greenfield`); "C++14 baseline" wording removed; `.dsp` detection structured |

**Implementation is UNBLOCKED. Proceed to Phase 1 (RED tests).**

---

## Panel Review Reference

See: `hangar-ai-specs/changes/cpp-version-routing-foundation/panel-review.md`

---

*Governance Record ID: GDR-cpp-version-routing-foundation*  
*Issued per ENG-11.1 (Hangar SDD Law), ENG-11.2 (Proposal Completeness Law)*

# Tier 1.2 — RAG Infrastructure Capability Assessment
## Can the Current System Deliver Version-Appropriate C++ Guidance?

**Purpose:** Determine what the current RAG infrastructure can and cannot do for
version-aware routing before designing Option E. Identifies capability gaps and
specifies what changes are feasible without external infrastructure investment.

**Method:** Structural analysis of `AVATAR-RAG-INDEX.yaml`, `AGENTS.md`, `guidance.md`,
`reference-index.md`, and the 31 C++ reference files. Supplemented by dual-pass
independent analysis of the two hardest questions (token budget and feasibility).

---

## Critical Architecture Finding: This Is Not Traditional RAG

Before answering the assessment questions, the architectural model must be understood
correctly.

**The hangar-ai-constitution does NOT use a vector database.**

Instead, it uses an **"agent-as-router" pattern**:

1. `AGENTS.md` custom instructions tell the AI agent to route via a **skill index first**,
   then load the matched skill, then load the matched avatar `guidance.md`
2. `AVATAR-RAG-INDEX.yaml` is a **declarative routing table** — a YAML file that
   describes query patterns → file paths + token estimates
3. The agent reads the index and **explicitly retrieves specific files** by path
4. There is no vector embedding, no cosine similarity search, no metadata filter API
5. The "recall" of a query depends entirely on the agent correctly matching the query
   to a routing entry and then reading the right file

**This matters for every assessment question below**, because:
- "Metadata filtering" means agent behavior, not infrastructure capability
- "Project context reading" means agent choice, not automatic injection
- "Token budget" is a design constraint, not a hard enforcement limit
- All improvements can be made as **repo-only configuration changes** — no external infrastructure investment required

---

## Assessment: Four Capability Questions

### Q1: Can the system filter by frontmatter metadata fields?

**Current state: NO at infrastructure level; POSSIBLE at agent level**

There is no vector database to receive a metadata filter like
`{cpp_version_min: {$lte: 14}}`. The agent CAN read frontmatter/metadata in files
(it reads the full file text), but there is no mechanism to:
- Pre-filter the corpus to only version-appropriate files before semantic matching
- Enforce that retrieved files satisfy version constraints
- Reject version-inappropriate files that match a semantic query

**What currently exists:**
- `reference-index.md` uses `★` annotations to flag version-specific content:
  - `★ C++17+` — content requires C++17
  - `★ C++98-C++17` — content covers legacy migration
  - `★ C++11+` — content requires C++11 minimum
- `AVATAR-RAG-INDEX.yaml` routing entries include these same annotations
- The reference-index.md includes the note: *"Start with the file matching your
  project's `__cplusplus` value"* — but this is **instructional text**, not enforcement

**Gap:** The agent can SEE version annotations, but there is no mandatory protocol
requiring it to CHECK project C++ version before routing. Without that check, the
agent routes based on query semantics alone, defaulting to the "C++ (Modern)" /
C++20 bias in the avatar name and manifest.

**Evidence of bias:**
```yaml
# manifest.yaml line 11
language: "C++20 / C++23"   # default assumption — not the production reality

# From Tier 1.1 survey: 60% of production LOC is C++14
```

**What IS possible with repo changes only:**
- Add `project.yaml` schema with `cpp_standard` field
- Add mandatory version-detection step to `AGENTS.md`
- Add version-conditional routing entries to `AVATAR-RAG-INDEX.yaml`

This would constitute **agent-level metadata filtering** — functionally equivalent
to vector-store filtering for this use case.

---

### Q2: Can the system read project context files?

**Current state: POSSIBLE but not happening — no protocol, no project.yaml files exist**

GitHub Copilot CAN read files from the working directory when explicitly instructed to.
The agent can open `CMakeLists.txt`, `.vcxproj`, `project.yaml`, or any other file
and extract version information from it.

**Current gap:** There is NO instruction in `AGENTS.md` to check for a project context
file before answering C++ questions. The `AGENTS.md` routing protocol is:
1. Route via skill index (`agent-skills/skills-by-domain/*/index.yaml`)
2. Load matched skill `.md` file
3. Load avatar guidance for stack context
4. Cite laws from skill frontmatter

There is no Step 0: "detect project C++ standard."

**Additional gap:** No `project.yaml` file exists in ANY of the 11 production
repositories identified in Tier 1.1. Without project context files, any detection
mechanism must fall back to build file inspection or be left as `unknown`.

**Feasibility of adding automatic detection from build files:**

| Build File | Detectable? | Method |
|-----------|------------|--------|
| `CMakeLists.txt` | ✅ Yes | Regex: `set\(CMAKE_CXX_STANDARD\s+(\d+)\)` |
| `.vcxproj` | ✅ Yes | XML: `<LanguageStandard>stdcpp17</LanguageStandard>` |
| `Makefile / CXXFLAGS` | ⚠️ Partial | Regex: `-std=c\+\+(\d+)` (absent = unknown) |
| `.dsp` (MSVC 6.0) | ✅ Special case | Presence of `.dsp` → flag as MSVC 6.0 / pre-C++98 |
| `SPECLIENT.dsp` + `msvcp60.dll` | ✅ Special case | MSVC 6.0 indicator |
| No project file | ❌ Unknown | Default to version-neutral content |

**Recommendation from Tier 1.1 findings:** Manual `project.yaml` files are more
reliable than build-file parsing for the AA portfolio, because:
- IOC_ALP/hte_pm_hostconn: CMakeLists.txt exists but has no `CMAKE_CXX_STANDARD`
- herc-odyssey-linux: Makefile has no `-std=` flag
- SPEClient: MSVC 6.0, no modern build file
- CWR: C++14 compiler but C++03 idioms — build file detection would miss the idiom gap

A 3-field `project.yaml` is more expressive than any build file:
```yaml
cpp_standard: "14"          # actual toolset standard  
cpp_idiom_level: "03"       # actual feature usage level (critical for CWR scenario)
compiler: "msvc"            # msvc | gcc | clang | borland | objective-cpp
```

---

### Q3: What is the current token budget per query?

**Answer: Effective budget is ~1,272–3,000t for content; context overhead is ~728t fixed**

From `AVATAR-RAG-INDEX.yaml` and corroborated by `split-reference-architecture.md`:

```
Always loaded (per C++ query):
  guidance.md                  ~310t   [always loaded as anchor]
  reference-index.md           ~418t   [co-loaded; "not counted" per index notation]
  ─────────────────────────────────────
  Fixed overhead               ~728t

Per-query budget remaining:    ~1,272–2,772t  (for 2,000–3,500t total)

Typical reference file sizes:
  Smallest ref files:         ~1,083t (ref-safety-jni-abi.md)
  Median ref files:           ~2,400t
  Largest ref files:          ~3,336t (ref-templates-metaprogramming.md)
  
  Average load = guidance + 1 ref = ~310 + 2,400 = ~2,710t per query
```

**Dual-pass finding on version context overhead:**

*Pass 1 (optimistic):* A `project.yaml` with 3-4 fields costs ~50-100t per query.
Within budget.

*Pass 2 (conservative):* Danger is not detection cost but **retrieval fan-out** — if
version routing adds content rather than replacing it, the budget is breached.

*Combined conclusion:* **Version context detection is affordable. Version-specific
content is only safe as a REPLACE strategy, not an ADDITIVE strategy.**

```
Current (version-unaware):
  query → 1 generic ref file (~2,400t) = WITHIN BUDGET

Wrong approach (additive):
  query → generic ref + version-specific ref (~4,800t) = BUDGET EXCEEDED

Correct approach (replacement):
  query → project.yaml (~75t) → EITHER cpp14-specific ref OR cpp20-specific ref
         = ~2,475t = WITHIN BUDGET
```

**Token budget implication for version-specific files:**
If we create per-version ref files, they MUST be sized to fit in a single query load:
- Maximum version-specific ref file: ~3,000t (with guidance overhead)
- Recommended: ~2,000t to leave headroom for project.yaml context

---

### Q4: Can filtering be added without major infrastructure changes?

**Answer: YES — all required changes are repo-only; no external infrastructure required**

**Dual-pass analysis:**

*Pass 1 (optimistic):*
The agent-as-router pattern is MORE flexible than vector-store filtering because:
- All behavior is controlled by repo files (AGENTS.md, AVATAR-RAG-INDEX.yaml)
- No external API, vector DB, or embedding pipeline to change
- Changes take effect immediately upon repository update
- The pattern already supports version annotations (`★ C++17+`) — just needs enforcement

*Pass 2 (skeptical):*
Agent-as-router is **best-effort, not reliable** without hardened protocols:
- `AGENTS.md` does not currently require a version-detection step
- No `project.yaml` exists in any production repository
- Routing table cannot execute conditional logic ("IF cpp_standard=14 THEN…")
- The C++ (Modern) default bias actively works against brownfield users

*Combined conclusion:*
- **CAN DO NOW** (repo-only changes): agent-mediated version detection + routing
- **NEEDS HARDENING**: mandatory detection protocol + fail-closed unknown handling

**The three-part solution set (all repo-only):**

| Component | Change Required | Effort |
|-----------|----------------|--------|
| `AGENTS.md` | Add Step 0: version detection before C++ routing | 1-2 days |
| `AVATAR-RAG-INDEX.yaml` | Add version-conditional routing entries | 2-3 days |
| New `project.yaml` schema | Define and document schema | 1 day |
| Production repos | Add `project.yaml` to each repo (opt-in adoption) | Per-team |

---

## Current Routing Gap Analysis

### Where Version-Aware Routing Already Exists

The routing table has SOME version-awareness built in — but it is **query-lexical**,
not **project-contextual**:

| Query Pattern | Routes To | Version-Appropriate? |
|--------------|-----------|---------------------|
| "C++ migrate standard version?" | ref-migration-pre-cpp17.md | ✅ Yes — lexical trigger |
| "C++ upgrade C++11 to C++17?" | ref-migration-pre-cpp17.md | ✅ Yes — lexical trigger |
| "C++ auto_ptr nullptr migration?" | ref-migration-pre-cpp17.md | ✅ Yes — lexical trigger |
| "C++ SFINAE to concepts migration?" | ref-templates-metaprogramming.md | ⚠️ Partial (concepts = C++20) |
| **"C++ smart pointers?"** | **skill-cpp-ownership-lifetime-safety.md** | ❌ **Modern only** |
| **"C++ memory management?"** | **ref-domain-patterns.md** | ❌ **Modern only** |
| **"C++ concurrency?"** | **ref-concurrency-threading.md** | ❌ **C++11+ assumed** |
| **"C++ error handling?"** | **examples/ENG-3.7-error-handling.md** | ❌ **C++23 std::expected** |

**The problem:** Generic C++ queries — the most common type — route to modern content
with no version check. A developer in a C++03 project asking "C++ smart pointers"
gets `skill-cpp-ownership-lifetime-safety.md` which recommends `std::unique_ptr`,
`std::shared_ptr`, `std::span`, `std::string_view` — features unavailable in C++03.

### What a Version-Aware Routing Entry Would Look Like

Proposed routing enhancement (no infrastructure changes needed):

```yaml
# Current (version-blind):
- C++ smart pointers ownership RAII? → skill-cpp-ownership-lifetime-safety.md (~600t)

# Proposed (version-aware, replacement strategy):
- C++ smart pointers ownership RAII? → 
    IF cpp_standard >= 17: skill-cpp-ownership-lifetime-safety.md (~600t)
    IF cpp_standard in [11,14]: ref-safety-memory-lifetime.md + version note
    IF cpp_standard <= 03: refs/legacy/ref-mental-models-memory.md (~2316t)
    IF unknown: refs/legacy/ref-mental-models-memory.md (~2316t) + ask for version
```

*Note: The routing table cannot literally execute IF logic — this would be implemented
as a versioned routing protocol in AGENTS.md with the routing table providing the
file-to-version mapping.*

---

## Current Token Budget Efficiency

```
Per-query token usage breakdown (current, typical C++ query):

  guidance.md                       310t  (always)
  reference-index.md                418t  (always)
  ──────────────────────────────────────
  Fixed overhead                    728t

  Retrieved ref file (median)     2,400t
  ──────────────────────────────────────
  Total                           3,128t

  Budget headroom before 3,500t:   +372t  (tight but within spec)
  Budget headroom before 4,000t:   +872t  (with any one large ref)

Adding version context (proposed):
  project.yaml reading overhead      ~75t
  ──────────────────────────────────────
  New total (same 1 ref file)      3,203t  (within 3,500t budget)
  
  Version detection is AFFORDABLE.
  Loading TWO ref files is NOT AFFORDABLE at median size.
```

---

## Capability Summary

| Question | Answer | Evidence |
|---------|--------|---------|
| Can RAG filter by frontmatter metadata? | **Agent-level: YES (with changes). Infrastructure: NO.** | No vector DB exists; agent reads files directly |
| Can RAG read project context files? | **YES technically; NOT happening today** | No AGENTS.md detection step; no project.yaml in any repo |
| Current token budget per query? | **~728t fixed + 1,272-2,772t content = ~2,000-3,500t total** | AVATAR-RAG-INDEX.yaml header, split-reference-architecture.md |
| Can filtering be added without infrastructure changes? | **YES — repo-only changes only; best-effort without hardened protocol** | All routing controlled by AGENTS.md + AVATAR-RAG-INDEX.yaml |

---

## Gaps That Require Option E to Address

Based on this assessment, the following gaps exist that Option E must close:

### Gap 1: No Mandatory Version Detection Step (CRITICAL)
**Current:** No step in `AGENTS.md` requires checking project C++ standard before routing
**Required:** Add Step 0 protocol to routing chain
**Scope:** AGENTS.md change + routing documentation

### Gap 2: No Project Context Schema (CRITICAL)
**Current:** No `project.yaml` exists in any production repo; no schema defined
**Required:** Define and document `project.yaml` schema with `cpp_standard`, `cpp_idiom_level`, `compiler`
**Scope:** New schema document + template file + adoption guide

### Gap 3: Generic Queries Return Modern Content (HIGH PRIORITY)
**Current:** "smart pointers", "memory management", "error handling" → modern C++20 content
**Required:** Version-conditional routing for top-20 generic queries
**Scope:** AVATAR-RAG-INDEX.yaml routing additions + version-aware entry conventions

### Gap 4: No Unknown-Version Fallback (HIGH PRIORITY)
**Current:** Unknown version → implicit modern bias
**Required:** Unknown version → version-neutral/legacy-safe content + version clarification prompt
**Scope:** AGENTS.md protocol + routing table fallback entries

### Gap 5: No Per-Version Content for High-Divergence Topics (MEDIUM)
**Current:** Single content file for topics that differ significantly across versions
(memory management, error handling, comparison operators, I/O)
**Required:** Version-specific ref files for high-divergence domains (replacement, not additive)
**Scope:** New ref files (already partially addressed in Tier 3 plan)

### Gap 6: Non-ISO C++ Projects Not Identified at Entry (MEDIUM)
**Current:** No guidance for Borland VCL or Objective-C++ projects — they would silently
receive ISO C++ guidance
**Required:** Detection of `#include <vcl\vcl.h>`, `.mm` files, `__fastcall` → avatar
deflection with explicit out-of-scope notice
**Scope:** AGENTS.md protocol + guidance.md disclaimer

---

## Recommended Changes (All Repo-Only, No Infrastructure Investment)

### Phase 1: Foundation (Required Before Option E Content Work)

**Change 1.A — Add Version Detection Protocol to AGENTS.md**
```
Before routing any C++ query, detect project C++ standard:
  1. Check for .copilot/project.yaml (cpp_standard field)
  2. Check for CMakeLists.txt (CMAKE_CXX_STANDARD)
  3. Check for .vcxproj (LanguageStandard element)  
  4. Check for Makefile (-std=c++ flag in CXXFLAGS)
  5. Check for .dsp/.dsw → MSVC 6.0 / pre-C++98
  6. If none found → unknown; use version-neutral routing
```

**Change 1.B — Define project.yaml Schema**
```yaml
# .copilot/project.yaml (to be created in each consuming project)
cpp:
  standard: "14"          # ISO standard year: 98 | 03 | 11 | 14 | 17 | 20 | 23
  idiom_level: "03"       # actual feature usage: same values (handles CWR scenario)
  compiler: "msvc"        # msvc | gcc | clang | borland | objective-cpp
  toolset: "v143"         # optional: MSVC toolset version
  out_of_scope: false     # true = Borland VCL or Objective-C++ (deflect)
```

**Change 1.C — Add Unknown-Version Fallback Entry to AVATAR-RAG-INDEX.yaml**
```yaml
# When cpp_standard is unknown, route to legacy-safe content:
unknown_version_fallback:
  preference: version-neutral or legacy-safe content
  avoid: files annotated ★ C++17+, ★ C++20+, ★ C++23+
  prompt: ask user for C++ standard if answer critically depends on version
```

### Phase 2: Version-Conditional Routing (Core Option E Content)

Add version-conditional routing entries for the top-20 generic C++ queries.
Each entry maps a query to the appropriate file based on `cpp_standard`:

| Query | C++03- | C++11-14 | C++17+ |
|-------|--------|----------|--------|
| "smart pointers" | ref-mental-models-memory.md | ref-safety-memory-lifetime.md | skill-cpp-ownership-lifetime-safety.md |
| "error handling" | (new) ref-error-handling-cpp14.md | (new) ref-error-handling-cpp14.md | ENG-3.7-error-handling.md |
| "comparison operators" | (new) ref-comparison-cpp14.md | (new) ref-comparison-cpp14.md | ref-core-type-safety.md |
| "concurrency" | ref-mental-models-lang.md | ref-concurrency-threading.md | ref-concurrency-async.md |
| "I/O formatting" | (new) ref-io-formatting.md | (new) ref-io-formatting.md | (new) ref-io-formatting.md |

---

## Answer to Next-Steps.md Q1.2 Deliverable

> **Q:** Does the current RAG system support metadata-based filtering?
> **A:** Not at the infrastructure level (no vector database). At the agent level,
>  filtering is possible via repository-controlled routing instructions but is not
>  currently enforced. All required changes are repo-only.

> **Q:** Can RAG read project context files?
> **A:** Technically yes. Practically no — no detection protocol exists and no
>  `project.yaml` files exist in any production repository.

> **Q:** What is the current token budget per query?
> **A:** ~3,000-3,500t total (728t fixed overhead + 1 ref file at ~2,400t median).
>  Version context detection adds ~75t overhead. Version-specific content routing
>  REPLACES one file with another — no budget increase if done correctly.

> **Q:** Can filtering be added without major infrastructure changes?
> **A:** YES. All changes are repo-only: AGENTS.md protocol + AVATAR-RAG-INDEX.yaml
>  routing + project.yaml schema definition. No vector DB, no embedding pipeline,
>  no external service changes required.

---

## Relationship to Option E Design

This assessment directly shapes Option E's implementation approach:

1. **The "project declaration" mechanism is feasible** — `project.yaml` can be
   adopted incrementally, starting with CWR (the primary focus repo)

2. **The routing enhancement is the critical path** — AGENTS.md + AVATAR-RAG-INDEX.yaml
   changes are more impactful than new content files, because they affect ALL queries

3. **Replace strategy, not Additive** — all version-specific content work must be
   sized to FIT in a single query load (≤3,000t per file)

4. **Unknown version should default to legacy-safe** — given the Tier 1.1 finding
   that 35% of LOC is C++03 or older, the "unknown version" default should be
   conservative (legacy-safe), not optimistic (modern)

5. **SPEClient and herc-odyssey-linux warrant explicit avatar warnings** — MSVC 6.0
   and C++98/no-CI projects should receive a prominent disclaimer before any
   guidance is provided

---

*Assessment completed: 2026-04-25 | Dual-pass analysis conducted for token budget and filtering feasibility*
*Committed to: `hangar-ai-specs/changes/cpp-version-sensitivity-analysis/rag-capability-assessment.md`*

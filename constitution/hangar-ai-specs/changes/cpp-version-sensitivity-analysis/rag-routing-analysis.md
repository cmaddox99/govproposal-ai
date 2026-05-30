# RAG Routing Analysis — C++ Avatar Version-Sensitivity

> Analysis of how RAG retrieval would handle version-sensitive C++ queries.
> Supporting evidence from panel-review.md and evidence-audit.md.

---

## Q1: Does `guidance.md` include version-dispatch logic?

### Answer: **NO**

### Evidence

From `avatars/technology/cpp/guidance.md` (lines 27-30):

```markdown
## Quick Start

**[→ Reference Index](reference-index.md)** — Topic-based navigation to all reference material.
```

The entire guidance.md content:
- Contains 32 lines total
- Provides a single entry point for ALL developers
- No version detection or branching
- Links directly to `reference-index.md` without any project context

### Expected Behavior

A well-designed version-dispatch would:
```yaml
# What guidance.md SHOULD have:
version_dispatch:
  - condition: "project.cpp_standard < 11"
    route: "ref-legacy-navigation.md"
    note: "Pre-modern C++ brownfield patterns"
  - condition: "project.cpp_standard >= 11 AND < 17"
    route: "ref-migration-playbooks.md"
    note: "Modernization-focused guidance"
  - condition: "project.cpp_standard >= 20"
    route: "reference-index.md"
    note: "Full modern C++ guidance"
```

### Verdict: `[CRITICAL GAP]`

---

## Q2: Does `reference-index.md` route by version or only by topic?

### Answer: **TOPIC ONLY**

### Evidence

From `avatars/technology/cpp/reference-index.md` (full content, 57 lines):

```markdown
## Core Language & Idioms
- **[ref-core-language.md](ref-core-language.md)** — Const correctness, casts, null safety, designated initializers

## Advanced C++ Features
- **[ref-advanced-cpp.md](ref-advanced-cpp.md)** — Templates, concepts, lambdas, coroutines, ranges

## Concurrency & Parallelism
- **[ref-concurrency.md](ref-concurrency.md)** — Threads, atomics, async/await patterns, coroutines

...
```

All 15 reference file links are organized by **topic category**:
1. Core Language & Idioms
2. Advanced C++ Features
3. Concurrency & Parallelism
4. Memory & Resource Safety
5. Object Design
6. Domain Modeling
7. Testing & CI
8. Build & Infrastructure
9. Aviation Safety
10. Legacy Codebase Navigation
11. Migration Playbooks
12. Brownfield Configuration

No categories like:
- "C++98 Brownfield Patterns"
- "C++17 Transition Guidance"
- "C++20+ Modern Practices"

### Impact on RAG

When a developer asks: *"How do I handle memory management in my C++11 project?"*

RAG would retrieve:
- `ref-safety-memory.md` (mixed C++11/14/17/20 content)
- `examples/ENG-6.1-smart-pointers.md` (C++14 `make_unique` without version tag)
- `ref-legacy-smells.md` (remediation assumes C++20 concepts)

Missing context: The developer's C++11 constraint.

### Verdict: `[CRITICAL GAP]`

---

## Q3: Do example files include version-identifying metadata?

### Answer: **NO (with rare exceptions)**

### Evidence

#### Typical Example Frontmatter

From `examples/ENG-6.1-smart-pointers.md`:
```yaml
---
law_id: ENG-6.1
avatar: cpp
---
```

From `examples/ENG-3.1-concepts.md`:
```yaml
---
law_id: ENG-3.1
avatar: cpp
---
```

From `examples/ENG-6.1-thread-safety.md`:
```yaml
---
law_id: ENG-6.1
avatar: cpp
---
```

#### Missing Fields

Expected version metadata that does NOT exist:
```yaml
---
law_id: ENG-6.1
avatar: cpp
cpp_version_min: 14          # MISSING
cpp_version_recommended: 20  # MISSING
replaces_pattern: "raw new"  # MISSING
---
```

#### Exceptions (Inline Version Notes)

From `examples/ENG-6.1-expected-errors.md` (rare inline note):
```markdown
Note: `std::expected` is C++23 — use `tl::expected` for C++17.
```

From `examples/ENG-6.1-thread-migration.md` (rare explicit versioning):
```markdown
**When to use which:**
- **Legacy C++98:** Keep `pthread_*` but wrap in RAII
- **C++11-17:** Use `std::thread` + `std::jthread` where available
- **C++20+:** Use `std::jthread` with `std::stop_token`
```

These are exceptions, not the norm.

### Statistics

| Metric | Count |
|--------|-------|
| Example files examined | ~20 |
| Files with `cpp_version` frontmatter | 0 |
| Files with inline version notes | 3-4 |
| Files assuming C++14+ without noting | ~15 |

### Verdict: `[MAJOR GAP]`

---

## Q4: Is there a project-level standard declaration mechanism?

### Answer: **PARTIAL (policy exists, declaration field absent)**

### Evidence

#### What EXISTS in `manifest.yaml`

Version policy (lines 11-18):
```yaml
version_policy:
  greenfield: "C++20 minimum (mandatory); C++23 recommended where toolchain supports it"
  brownfield: "C++11 minimum for new code within legacy modules; exceptions documented"
  rationale: |
    C++20 is required for greenfield because it offers concepts, ranges, coroutines,
    and std::format — all of which reduce defects and improve maintainability.
```

Compiler tiers (lines 30-35):
```yaml
compilers:
  recommended: "GCC 14+ or Clang 18+ (C++23 support)"
  required_greenfield: "GCC 12+ or Clang 14+ or MSVC 19.30+ (C++20 support)"
  active_brownfield: ["GCC 7+ (C++14/17)", "Clang 5+ (C++14/17)", "MSVC 19.14+ (VS 2017 15.7+)"]
  legacy: "GCC 4.8.1+ (C++11 partial)"
  frozen: "Any (no modifications permitted)"
```

#### What is MISSING

No mechanism for a project to declare its standard:
```yaml
# MISSING from manifest.yaml
project_declaration:
  cpp_standard_field: "project.cpp_standard"
  valid_values: [98, 11, 14, 17, 20, 23]
  default: 20
  discovery: ["CMakeLists.txt CMAKE_CXX_STANDARD", "project.yaml cpp_standard"]
```

No project template with standard declaration:
```yaml
# MISSING project.yaml template
project:
  name: "flight-pricing-engine"
  cpp_standard: 17
  migration_target: 20
  avatar: cpp
```

### Impact

RAG cannot:
1. Know what C++ standard a project uses
2. Filter guidance to version-appropriate content
3. Warn when recommending features above project's standard

### Verdict: `[PARTIAL — Policy exists, mechanism absent]`

---

## Q5: What is the RAG token-budget impact?

### Answer: **HIGH RISK — Content exceeds typical RAG window**

### Evidence

#### Token Estimates

From `reference-index.md` header comment:
```markdown
# Average ~3,500 tokens per file; total avatar ≈60,000 tokens
```

Manual calculation:
- 15 reference files × 3,500 tokens = 52,500 tokens
- ~20 example files × 1,500 tokens = 30,000 tokens
- manifest.yaml + guidance.md = ~2,000 tokens
- **Total: ~85,000 tokens**

#### Typical RAG Window Sizes

| System | Context Window | Usable for RAG |
|--------|----------------|----------------|
| GPT-4 | 128K | 8K-16K retrieved |
| Claude 3.5 | 200K | 16K-32K retrieved |
| Copilot | Variable | 8K-12K typical |

#### Fit Analysis

If RAG retrieves **10,000 tokens** per query:
- Only 12% of avatar content fits
- ~1.5 reference files OR ~6-7 example files
- Version-inappropriate content WILL be included

#### Worst-Case Scenario

Developer asks: *"How do I implement comparison operators?"*

RAG retrieves (unfiltered):
1. `ref-domain-modeling.md` — shows `operator== = default` (C++20)
2. `ref-migration-playbooks.md` — mentions `<=>` (C++20)
3. `ref-object-design.md` — shows defaulted comparisons (C++20)

Developer's project: C++14

Result: **100% of retrieved content is unusable**

### Mitigation Analysis

| Strategy | Effectiveness | Implementation Cost |
|----------|--------------|---------------------|
| Project standard declaration | High | Medium |
| Version-segmented examples | Medium-High | High |
| Inline version tags | Low | Low |
| Separate version avatars | High | Very High |

### Verdict: `[HIGH RISK — Requires version-aware routing]`

---

## Summary Matrix

| Question | Answer | Severity |
|----------|--------|----------|
| Q1: Version dispatch in guidance.md? | NO | `[CRITICAL]` |
| Q2: Version routing in reference-index? | NO | `[CRITICAL]` |
| Q3: Version metadata in examples? | NO | `[MAJOR]` |
| Q4: Project standard declaration? | PARTIAL | `[MEDIUM]` |
| Q5: Token budget risk? | HIGH | `[HIGH]` |

---

## Root Cause

The C++ avatar was designed with an implicit assumption:

> "All developers using this avatar are working on C++20+ greenfield or actively modernizing brownfield."

This assumption breaks when:
1. Brownfield projects are frozen at C++11/14/17
2. Aviation safety systems have long certification cycles (DO-178C)
3. Mixed codebases span multiple standards

---

## Recommended RAG Routing Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                         User Query                             │
│     "How do I handle smart pointers in my project?"            │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│              Project Context Detection (NEW)                    │
│  1. Read project.yaml → cpp_standard: 14                        │
│  2. Read CMakeLists.txt → CMAKE_CXX_STANDARD: 14               │
│  3. Infer from compiler flags → -std=c++14                     │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│              Version-Aware Retrieval (NEW)                      │
│  Filter: cpp_version_max <= 14                                  │
│  Boost: examples with explicit C++14 patterns                   │
│  Demote: examples assuming C++17+ features                      │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│              Retrieved Context                                  │
│  ✓ ENG-6.1-smart-pointer-migration.md (C++11/14 patterns)      │
│  ✓ ref-safety-memory.md §RAII (C++11+ patterns)                │
│  ✗ EXCLUDED: make_unique without C++14 note                    │
│  ✗ EXCLUDED: PMR allocators (C++17)                            │
└─────────────────────────────────────────────────────────────────┘
```

---

*Document generated as part of C++ Avatar Version-Sensitivity Analysis.*

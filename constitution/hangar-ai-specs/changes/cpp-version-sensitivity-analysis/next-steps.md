# Next Steps — C++ Avatar Version-Sensitivity Remediation

> Prioritized backlog for addressing version-sensitivity issues in the C++ avatar.
> Organized by tier: Human Input Required → PoC Experiments → Implementation → Monitoring.

---

## Summary

This document provides actionable next steps based on the findings from:
- `evidence-audit.md` — Domain × Version analysis
- `rag-routing-analysis.md` — RAG retrieval gap analysis
- `restructuring-options.md` — Option evaluation (Option E recommended)
- `panel-review.md` — Two-pass verification records

**Recommended Approach:** Option E (Hybrid: Project Declaration + Segmented Examples)

---

## Tier 1: Human Input Required

> These items require governance decisions or production system knowledge before proceeding.

### 1.1 Production C++ Version Survey

**Owner:** Engineering Leadership / Platform Team

**Question:** What C++ standards are currently in production across AA systems?

**Required Data:**
| System Category | Expected Standard | Count of Systems |
|-----------------|-------------------|------------------|
| Legacy mainframe interfaces | C++98/03 | ? |
| Active brownfield (MFC, Win32) | C++11/14 | ? |
| Modern services | C++17/20 | ? |
| Greenfield (new development) | C++20/23 | ? |

**Why Needed:**
- Determines which version variants to prioritize
- Informs token budget allocation
- Validates whether C++98 content is actually needed

**Deliverable:** Version distribution report

**Timeline:** 1-2 weeks

---

### 1.2 RAG Infrastructure Capability Assessment

**Owner:** AI Platform Team / Copilot Integration Team

**Question:** Does the current RAG system support metadata-based filtering?

**Required Information:**
- [ ] Can RAG filter by frontmatter metadata fields?
- [ ] Can RAG read project context files (project.yaml, CMakeLists.txt)?
- [ ] What is the current token budget per query?
- [ ] Can filtering be added without major infrastructure changes?

**Why Needed:**
- Option E requires version-aware retrieval
- If filtering unavailable, fallback to Option A (inline tags)

**Deliverable:** RAG capability assessment document

**Timeline:** 1 week

---

### 1.3 Governance Approval for Avatar Restructure

**Owner:** Constitution Governance Board

**Decision Required:**
- [ ] Approve addition of `cpp_version_min` / `cpp_version_max` to example schema
- [ ] Approve project declaration mechanism (`project.yaml` schema)
- [ ] Approve example file variant naming convention (`-cpp11`, `-cpp14`, etc.)
- [ ] Approve maintenance policy for version variants

**Reference:** Per ENG-10.1 (Documentation Law), schema changes require governance review.

**Deliverable:** Approved RFC or governance decision record

**Timeline:** 2-3 weeks (depends on meeting cadence)

---

## Tier 2: PoC Experiments

> Technical experiments to validate approach before full implementation.

### 2.1 Version Metadata Schema PoC

**Objective:** Validate the proposed frontmatter schema for version tagging.

**Tasks:**
1. Create sample example file with full version metadata:
   ```yaml
   ---
   law_id: ENG-6.1
   avatar: cpp
   cpp_version_min: 14
   cpp_version_max: null
   features_used:
     - std::make_unique
     - move semantics
   superseded_by: null
   ---
   ```
2. Test parsing with existing RAG tooling
3. Verify no breaking changes to current retrieval

**Success Criteria:**
- Schema parses correctly
- Existing (untagged) files continue to work
- New fields are retrievable

**Effort:** 2-3 days

**Dependencies:** None (can start immediately)

---

### 2.2 Project Standard Discovery PoC

**Objective:** Validate automatic C++ standard detection from project files.

**Tasks:**
1. Write detection logic for:
   - `CMakeLists.txt`: `CMAKE_CXX_STANDARD`, `target_compile_features`
   - `project.yaml`: `cpp_standard` field
   - `.copilot/project.yaml`: `cpp.standard` field
2. Test against 3-5 sample projects
3. Document detection priority order

**Sample Detection Patterns:**
```regex
# CMakeLists.txt patterns
set\(CMAKE_CXX_STANDARD\s+(\d+)\)
target_compile_features\(.*cxx_std_(\d+)\)
CXX_STANDARD\s+(\d+)

# project.yaml patterns
cpp_standard:\s*(\d+)
cpp:\s*\n\s*standard:\s*(\d+)
```

**Success Criteria:**
- Correctly detects standard from 80%+ of test projects
- Graceful fallback (default to C++20) when detection fails

**Effort:** 3-5 days

**Dependencies:** Access to sample project repositories

---

### 2.3 RAG Filtering PoC

**Objective:** Validate version-filtered retrieval improves relevance.

**Tasks:**
1. Tag 10 example files with version metadata
2. Create test queries with version context:
   - "How to manage memory?" @ C++11
   - "How to manage memory?" @ C++20
3. Compare retrieved content:
   - Without filtering: baseline relevance score
   - With filtering: filtered relevance score

**Test Matrix:**
| Query | Project Standard | Expected Top Result |
|-------|------------------|---------------------|
| "smart pointers" | C++11 | `smart-pointers-cpp11.md` |
| "smart pointers" | C++14 | `smart-pointers.md` |
| "comparison operators" | C++14 | `comparison-cpp14.md` |
| "comparison operators" | C++20 | `domain-modeling.md` (defaulted ==) |

**Success Criteria:**
- Filtered queries return version-appropriate content
- Relevance score improves by >20%

**Effort:** 1 week

**Dependencies:** 2.1, 2.2

---

## Tier 3: Implementation Work

> File changes and content updates.

### 3.1 Phase 1 — Metadata Infrastructure

**Objective:** Add version metadata schema to avatar.

**Tasks:**
1. Update `manifest.yaml` with project declaration schema:
   ```yaml
   project_declaration:
     cpp_standard:
       field: "project.cpp_standard"
       discovery: [...]
       valid_values: [98, 11, 14, 17, 20, 23]
       default: 20
   ```
2. Update `guidance.md` with version declaration instructions
3. Create `project.yaml` template for projects

**Files Modified:**
- `avatars/technology/cpp/manifest.yaml`
- `avatars/technology/cpp/guidance.md`
- NEW: `avatars/technology/cpp/templates/project.yaml`

**Effort:** 3-5 days

**Dependencies:** 1.3 (governance approval)

---

### 3.2 Phase 2 — Example Metadata Tagging

**Objective:** Add version metadata to all existing example files.

**Tasks:**
1. Create tagging checklist with version requirements per file
2. Update frontmatter in all ~20 example files
3. Run validation to ensure all files have version metadata

**Tagging Reference:**
| File | cpp_version_min | features_used |
|------|-----------------|---------------|
| smart-pointers.md | 14 | make_unique, move |
| thread-safety.md | 17 | scoped_lock |
| concepts.md | 20 | concepts, requires |
| expected-errors.md | 23 | std::expected |
| auto-ptr-migration.md | 11 | unique_ptr |
| ... | ... | ... |

**Effort:** 2-3 days

**Dependencies:** 3.1

---

### 3.3 Phase 3 — Priority Example Variants

**Objective:** Create version-specific example variants for high-impact domains.

**Priority Order:**

| Priority | New File | Domain | Content |
|----------|----------|--------|---------|
| P1 | `ENG-6.1-smart-pointers-cpp11.md` | Memory | unique_ptr without make_unique |
| P2 | `ENG-6.1-thread-safety-cpp11.md` | Concurrency | lock_guard instead of scoped_lock |
| P3 | `ENG-6.1-comparison-cpp14.md` | Comparison | Manual operators, std::tie idiom |
| P4 | `ENG-3.1-sfinae-cpp11.md` | Templates | enable_if patterns |
| P5 | `ENG-3.1-formatting-cpp14.md` | I/O | fmtlib patterns |

**Effort:** 2-3 days per variant (10-15 days total)

**Dependencies:** 3.2

---

### 3.4 Phase 4 — Reference File Version Notes

**Objective:** Add inline version notes to reference files where patterns differ by version.

**Files to Update:**
| File | Sections Needing Version Notes |
|------|-------------------------------|
| ref-concurrency.md | Lock guards (C++11 vs C++17) |
| ref-advanced-cpp.md | SFINAE (C++11) vs Concepts (C++20) |
| ref-safety-memory.md | PMR (C++17+) |
| ref-domain-modeling.md | Defaulted comparisons (C++20) |

**Format:**
```markdown
### Lock Guards

**C++11-16:** Use `std::lock_guard<std::mutex>` for single mutex.
```cpp
std::lock_guard<std::mutex> lock(mtx_);
```

**C++17+:** Prefer `std::scoped_lock` for any number of mutexes.
```cpp
std::scoped_lock lock(mtx_);  // single
std::scoped_lock lock(mtx1_, mtx2_);  // multiple, deadlock-free
```
```

**Effort:** 5-7 days

**Dependencies:** 3.3

---

### 3.5 Phase 5 — I/O Domain Coverage (Gap Fill)

**Objective:** Address the HIGH mislead risk gap in I/O domain.

**New Content:**
1. Create `ref-io-formatting.md` covering:
   - printf (C++98, security risks)
   - iostream (all versions, performance notes)
   - fmtlib (C++11+, recommended polyfill)
   - std::format (C++20)
   - std::print (C++23)

2. Create `ENG-6.1-format-string-safety.md`:
   - Format string vulnerabilities
   - Safe alternatives by version
   - AA-specific logging (spdlog integration)

**Effort:** 5-7 days

**Dependencies:** None (can parallelize with other phases)

---

### 3.6 Phase 6 — Comparison Domain Coverage (Gap Fill)

**Objective:** Address the HIGH mislead risk gap in comparison operators.

**New Content:**
1. Create `ENG-3.1-comparison-operators.md` covering:
   - C++98/11/14: Manual 6-operator pattern
   - C++98/11/14: std::tie idiom for operator<
   - C++20: operator<=> three-way comparison
   - C++20: Defaulted comparisons

**Effort:** 3-5 days

**Dependencies:** None (can parallelize with other phases)

---

## Tier 4: Monitoring and Validation

> Post-implementation validation and ongoing maintenance.

### 4.1 RAG Relevance Metrics

**Objective:** Measure improvement in RAG retrieval quality.

**Metrics:**
| Metric | Baseline | Target |
|--------|----------|--------|
| Version-appropriate retrieval % | ~60% | >90% |
| Developer satisfaction score | TBD | +20% |
| Misleading guidance incidents | TBD | -80% |

**Measurement Method:**
1. Create test query suite (20 queries across domains/versions)
2. Score retrieved content for version appropriateness
3. Run weekly; report monthly

**Effort:** Ongoing (2-3 hours/week)

---

### 4.2 Content Drift Detection

**Objective:** Ensure version variants stay synchronized.

**Tasks:**
1. Create CI check comparing variant files
2. Alert when base file changes without variant update
3. Quarterly review of superseded_by chains

**Implementation:**
```yaml
# .github/workflows/version-sync-check.yaml
- name: Check variant synchronization
  run: |
    python tools/check-variant-sync.py \
      --base examples/*.md \
      --variants examples/*-cpp*.md
```

**Effort:** Setup: 2-3 days; Ongoing: 1 hour/week

---

### 4.3 Version Coverage Dashboard

**Objective:** Track version coverage across avatar content.

**Dashboard Fields:**
| Domain | C++98 | C++11 | C++14 | C++17 | C++20 | C++23 |
|--------|-------|-------|-------|-------|-------|-------|
| Memory | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Concurrency | ✓ | ✓ | ✓ | ✓ | ✓ | - |
| Templates | - | ✓ | ✓ | ✓ | ✓ | ✓ |
| I/O | - | - | ✓ | ✓ | ✓ | ✓ |
| Comparison | - | - | ✓ | - | ✓ | ✓ |

**Target:** All cells ✓ for domains with significant version differences.

**Effort:** Setup: 1-2 days; Updates: per-release

---

## Implementation Timeline

```
Week 1-2:   Tier 1 — Human input gathering
            ├── 1.1 Production version survey
            ├── 1.2 RAG capability assessment
            └── 1.3 Governance approval (may extend)

Week 3:     Tier 2 — PoC experiments
            ├── 2.1 Version metadata schema PoC
            └── 2.2 Project standard discovery PoC

Week 4:     Tier 2 continued
            └── 2.3 RAG filtering PoC

Week 5-6:   Tier 3 — Implementation
            ├── 3.1 Metadata infrastructure
            ├── 3.2 Example metadata tagging
            └── 3.5/3.6 Gap fills (parallel)

Week 7-9:   Tier 3 continued
            ├── 3.3 Priority example variants
            └── 3.4 Reference file version notes

Week 10+:   Tier 4 — Monitoring
            ├── 4.1 RAG relevance metrics
            ├── 4.2 Content drift detection
            └── 4.3 Version coverage dashboard
```

---

## Quick Start for Agent

If you are an agent working on this remediation:

1. **Check Tier 1 status** — Do not proceed to Tier 3 without human decisions on 1.1-1.3
2. **Start with 2.1** — Version metadata schema PoC can begin immediately
3. **Parallelize gap fills** — 3.5 and 3.6 have no dependencies
4. **Use evidence-audit.md** — Contains all quoted evidence for each finding
5. **Follow ENG-4.1** — All changes require Atomic TDD cycle

**First Task:** Create PoC example file with proposed version metadata schema.

---

## Open Questions

1. **C++98 content scope:** Should the avatar support C++98 brownfield at all, or require migration to C++11 minimum?

2. **Version variant naming:** Is `-cpp11` suffix the right convention, or should we use `-legacy`, `-modern`, `-current`?

3. **RAG filtering priority:** If infrastructure changes are blocked, which fallback provides most value (Option A inline tags, or Option B version sections)?

4. **Maintenance ownership:** Who owns variant synchronization — original author, or a designated "version steward"?

---

*Document generated as part of C++ Avatar Version-Sensitivity Analysis.*

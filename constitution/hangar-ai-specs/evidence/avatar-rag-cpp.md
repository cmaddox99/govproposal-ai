# RAG Validation Evidence — C++ Technology Avatar

**Avatar:** `avatars/technology/cpp/`
**Version:** 2.0.0
**Scan Date:** 2026-04-13 (updated post-Phase 18 remediation)
**Required By:** Avatar Workflow Phase 5/6 Commit Gate
**Assessment:** `workflows/avatar-workflow.md` Mode 3 (Validate)

---

## Avatar Workflow — Validate Mode Assessment

> Assessed against: `docs/guides/avatar-model-schema.md`
> Mode: Validate (Mode 3) — Read-only. No files modified.
> Workflow: `workflows/avatar-workflow.md`

### Verdict: 🟡 CONDITIONAL PASS

---

## Phase 1 — Identify

| Field | Value | Status |
|-------|-------|--------|
| Mode | Validate (Mode 3) | ✅ |
| Avatar type | `technology` | ✅ |
| Domain slug | `cpp` | ✅ |
| Avatar path | `avatars/technology/cpp/` | ✅ exists |

---

## Phase 2 — Scan

### Safeguard 1 — Deduplication: ✅ PASS

`avatars/technology/cpp/` is the only C++ technology avatar. No semantic overlap with other technology avatars detected.

### Safeguard 2 — Law Domain Boundary: ✅ PASS

All 20 `specializes_laws` entries use `ENG-*` laws. No `PRD-*` or `BUS-*` found.

| Law | Status |
|-----|--------|
| ENG-2.1, ENG-2.2, ENG-3.1–3.7, ENG-4.1–4.4, ENG-5.2–5.5, ENG-6.1–6.7, ENG-7.1–7.5 | ✅ ENG-* only |

### Safeguard 3 — Product Taxonomy: ✅ N/A

Not a product-type avatar.

### Safeguard 4 — Law ID Validity: ✅ PASS

All 20+ law IDs validated against `laws/engineering/_domain.yaml` (72 IDs indexed). All present.

### Safeguard 5 — Shadow Governance: 🟡 WARNING (2 findings)

| Finding | Severity | Location | Resolution |
|---------|----------|----------|------------|
| `standard_tiers`, `dependencies`, `ci_toolchain`, `commands`, `conventions`, `project_structure` blocks in manifest | 🟡 WARNING — unknown blocks | `manifest.yaml` | Tracked as W-4/W-5 → deferred to `cpp-avatar-manifest-restructure` PR |
| `activates.brownfield_adoption`, `activates.skill_parity`, `activates.project_archetypes` sub-blocks | 🟡 WARNING — unknown activates sub-blocks | `manifest.yaml` | Same W-4/W-5 deferred PR |

No invented law IDs, no law overrides, no self-approval patterns, no authority assertions.

### activates.skills Existence (Safeguard 5): ✅ PASS

| Skill | File | Status |
|-------|------|--------|
| `06-atomic-tdd` | `agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md` | ✅ |
| `07-vertical-slice-dev` | `agent-skills/skills-by-domain/development-practices/07-vertical-slice-dev.md` | ✅ |
| `08-code-review` | `agent-skills/skills-by-domain/development-practices/08-code-review.md` | ✅ |
| `04-business-domain-modeling` | `agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md` | ✅ |
| `skill-cpp-jni-bridge` | `agent-skills/skills-by-domain/platform-engineering/skill-cpp-jni-bridge.md` | ✅ |

### Schema Completeness: 🟡 1 BLOCKING, 2 WARNINGS

| Check | Result | Detail |
|-------|--------|--------|
| manifest.yaml present | ✅ | |
| avatar.id matches slug convention | ✅ | `avatar-cpp` — consistent with all other avatars in `index.yaml` |
| avatar.type = technology | ✅ | |
| avatar.version semver | ✅ | `2.0.0` |
| stack block present | ✅ | |
| activates.skills ≥2 | ✅ | 5 skills |
| activates.workflows ≥1 | ✅ | 3 workflows |
| specializes_laws ≥1 non-negotiable | ✅ | ENG-4.1 present |
| all example_file references resolve | 🔴 BLOCKING | ENG-5.5 duplicate YAML key — see below |
| manifest tokens ≤150 | 🟡 WARNING | ~1,638 tokens (10.9×) — tracked W-4/W-5 deferred |
| guidance.md present | ✅ | |
| guidance.md Non-Negotiable Laws section | ✅ | |
| guidance.md tokens ≤450 | 🟡 WARNING | ~416 tokens (92% utilization — near limit) |
| examples/ directory present | ✅ | |
| examples/ count ≥ specializes_laws count | ✅ | 50 example files, 20 laws |
| each example ≤850 tokens | ✅ | All examples within budget |

#### 🔴 BLOCKING — Duplicate YAML Key: ENG-5.5 / ENG-6.5

Lines 299–303 of `manifest.yaml` contain a malformed YAML entry where `title` and `example_file` keys are duplicated under the single list item `id: ENG-5.5`:

```yaml
# CURRENT (broken):
  - id: ENG-5.5
    title: Observability Law
    example_file: examples/ENG-5.5-observability.md
    title: Input Validation                           # ← duplicate key
    example_file: examples/ENG-6.5-input-validation.md  # ← duplicate key — wins
```

**Effect:** PyYAML resolves to `ENG-5.5 → example_file: examples/ENG-6.5-input-validation.md` (wrong file).
**Secondary effect:** `ENG-6.5` (Input Validation) has no `id:` entry in `specializes_laws`.
**Impact:** ENG-5.5-observability.md exists on disk but is not reachable via the manifest.

**Fix:**
```yaml
# CORRECT:
  - id: ENG-5.5
    title: Observability Law
    example_file: examples/ENG-5.5-observability.md
  - id: ENG-6.5
    title: Input Validation
    example_file: examples/ENG-6.5-input-validation.md
```

---

---

## Phase 5 — RAG Validate

> All queries use the post-Phase 18 file state.
> `full-reference.md` (~20,000+ tokens) excluded from all query sets per `on_demand_only: true` in AVATAR-RAG-INDEX.yaml.

### Q1: "How do I write a GoogleTest for a C++ class with RAII ownership?"

| File Loaded | Token Est. | Relevance |
|-------------|-----------|-----------|
| `guidance.md` | ~416 | Always loaded — routing layer |
| `examples/ENG-4.1-atomic-tdd.md` | ~480 | GoogleTest RED-GREEN-REFACTOR pattern |
| `examples/ENG-3.1-complexity.md` | ~340 | RAII ownership complexity patterns |
| **Total** | **~1,236** | |

**Answerable:** ✅ Yes — GoogleTest setup, fixture patterns, RAII ownership fully covered.
**Verdict:** ✅ PASS (under 3,500 threshold)

---

### Q2: "What is the correct way to handle errors in C++ without exceptions?"

| File Loaded | Token Est. | Relevance |
|-------------|-----------|-----------|
| `guidance.md` | ~416 | Always loaded — routing layer |
| `examples/ENG-3.7-error-handling.md` | ~450 | `std::expected`, error codes, RAII, CWR path (created Phase 18 Phase 2) |
| **Total** | **~866** | |

**Answerable:** ✅ Yes — ENG-3.7 example file now present; `std::expected`, value-based error, exception boundaries all covered.
**Verdict:** ✅ PASS (under 3,500 threshold) ← *was 🔴 FAIL before Phase 18 Phase 2*

---

### Q3: "How do I migrate from raw pointers to unique_ptr in a C++03 brownfield codebase?"

| File Loaded | Token Est. | Relevance |
|-------------|-----------|-----------|
| `guidance.md` | ~416 | Always loaded — routing layer |
| `examples/ENG-6.1-smart-pointer-migration.md` | ~425 | Raw → smart pointer migration |
| `examples/ENG-6.1-auto-ptr-migration.md` | ~361 | auto_ptr → unique_ptr |
| **Total** | **~1,202** | |

**Answerable:** ✅ Yes — Both migration examples directly address the query.
**Verdict:** ✅ PASS (under 3,500 threshold)

---

### Q4: "What sanitizers are mandatory in CI for C++ under this constitution?"

| File Loaded | Token Est. | Relevance |
|-------------|-----------|-----------|
| `guidance.md` | ~416 | Always loaded — routing layer |
| `examples/ENG-5.2-cmake-governance.md` | ~369 | CI pipeline governance, sanitizer integration |
| **Total** | **~785** | |

**Answerable:** ✅ Yes — CMake governance example covers ASan/UBSan mandatory, TSan recommended.
**Verdict:** ✅ PASS (under 3,500 threshold)

---

### Q5: "How does the compliance rating score a C++ project for safety-critical posture?"

| File Loaded | Token Est. | Relevance |
|-------------|-----------|-----------|
| `guidance.md` | ~416 | Always loaded — routing layer |
| `skill-cpp-compliance-rating.md` | ~600 | 10-dimension scoring model with D10 (regulatory compliance) |
| **Total** | **~1,016** | |

**Answerable:** ✅ Yes — Compliance rating skill includes D10 safety-critical/regulatory dimension.
**Verdict:** ✅ PASS (under 3,500 threshold)

---

## RAG Validation Summary

| Metric | Threshold | Actual | Result |
|--------|-----------|--------|--------|
| Recall proxy | ≥95% (5/5) | 5/5 (100%) | ✅ PASS |
| Precision proxy | ≥90% | 100% — all loaded files relevant | ✅ PASS |
| Max query token load | ≤3,500 per query | ~1,236 (Q1) | ✅ PASS |
| Schema violations (BLOCKING) | 0 | 1 (duplicate YAML key ENG-5.5/ENG-6.5) | 🔴 BLOCKING |

**Overall RAG Validation:** 🟡 CONDITIONAL PASS

RAG queries all pass (recall 5/5, all under 3,500 token budget). One BLOCKING schema defect must be fixed before avatar can be marked `rag_validated: true` at next version.

---

## Overall Validate Mode Verdict

### 🟡 CONDITIONAL PASS

| Category | Status | Notes |
|----------|--------|-------|
| Deduplication (S1) | ✅ PASS | No overlap detected |
| Law Domain Boundary (S2) | ✅ PASS | ENG-* only — clean |
| Product Taxonomy (S3) | ✅ N/A | Technology avatar |
| Law ID Validity (S4) | ✅ PASS | All 20 law IDs valid |
| Shadow Governance (S5) | 🟡 WARNING | 9 unknown manifest blocks (W-4/W-5 deferred) |
| Schema Completeness | 🔴 1 BLOCKING | Duplicate YAML key ENG-5.5/ENG-6.5 |
| activates.skills existence | ✅ PASS | All 5 skills verified |
| guidance.md | 🟡 NEAR LIMIT | 416/450 tokens (92%) |
| RAG Recall | ✅ 5/5 | All queries answerable post-Phase 18 |
| RAG Token Budget | ✅ PASS | Max ~1,236 tokens/query |

### Required Changes Before `rag_validated: true`

| # | Severity | Item |
|---|----------|------|
| 1 | 🔴 BLOCKING | Fix duplicate YAML key in `manifest.yaml` lines 299–303: split ENG-5.5 and ENG-6.5 into separate `specializes_laws` entries |

### Already Tracked (Deferred)

| # | Severity | Item | Tracked In |
|---|----------|------|-----------|
| 2 | 🟡 WARNING | Manifest token budget (~1,638 vs 150) — 9 unknown blocks | `cpp-avatar-manifest-restructure` PR |
| 3 | 🟡 WARNING | guidance.md near 450-token limit | Future PATCH bump |

> **Note:** `full-reference.md` excluded from RAG retrieval per `on_demand_only: true` (AVATAR-RAG-INDEX.yaml). This correctly prevents the ~20,000+ token file from entering any RAG pipeline.

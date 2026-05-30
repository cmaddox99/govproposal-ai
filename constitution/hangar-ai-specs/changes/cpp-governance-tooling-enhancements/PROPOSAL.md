# Proposal: C++ Governance Tooling Enhancements

**Proposal ID:** cpp-governance-tooling-enhancements
**Submitted:** April 25, 2026
**Status:** 🟡 DRAFT — Awaiting governance review
**Source:** `hangar-ai-specs/changes/cpp-version-routing-foundation/` — post-merge advisory items
**Predecessor:** `cpp-version-routing-foundation` (PR #47, merge-ready)
**Authority boundary:** Changes in this proposal require modifications **outside** the C++ avatar directory tree and therefore require a separate pull request with broader review.

---

## Laws Cited (ENG-11.2 Compliance)

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law | Governs proposal lifecycle |
| [ENG-11.2](laws/engineering/eng-11-hangar-sdd.md) | Proposal Completeness | Requires law citations, success criteria, deliverables |
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | Lint rules enforce constitutional correctness |
| [ENG-4.1](laws/engineering/eng-4-testing.md) | Atomic TDD Law | All changes follow RED–GREEN–REFACTOR |
| [ENG-6.7](laws/engineering/eng-6-security.md) | Audit Trail Law | schema_version and ref-file existence are auditability concerns |

---

## Problem Statement (Per PRD-1.2)

The `cpp-version-routing-foundation` proposal (Phase 1) introduced three artifacts that
require governance tooling support to be fully auditable and enforceable:

1. **`schema_version` field** in `cpp-project.yaml` — teams copy the template and fill it
   in, but nothing enforces that consumers include `schema_version` or that its value is
   valid. Without enforcement, version drift between the template and deployed project files
   goes undetected.

2. **D3 prefer/avoid ref-file existence** — `AVATAR-RAG-INDEX.yaml` lists specific
   `refs/*.md` files in `version_routing_policy.by_standard.*.prefer` and `*.avoid` lists.
   If a referenced file is deleted or renamed, the policy silently degrades (the agent
   receives stale routing). The `test_routing_policy_file_refs_exist` test guards this, but
   the constitution-lint tool does not, meaning the check runs only in CI for this repo —
   not for downstream repositories that adopt the avatar.

3. **Mixed-repo `.dsp` / `.dsw` false-positive risk** — A large repo that has been
   partially migrated to CMake may contain legacy `.dsp` files alongside a root
   `CMakeLists.txt`. The current detection order (`CMakeLists.txt` before `*.dsp`) handles
   this correctly, but `guidance.md` does not explicitly warn developers of this edge case.
   Clarifying this in guidance.md would prevent misclassification in mixed-migration repos.
   This item is deferred from `cpp-version-routing-foundation` because `guidance.md` is at
   the 450-token ceiling and cannot absorb additional prose without a coordinated trim.

4. **Adoption workflow: explicit C++ version declaration** — The avatar adoption guide and
   any onboarding docs for teams joining the constitution governance should include a
   mandatory step to declare `cpp.standard` in `.copilot/project.yaml`. Without this step,
   teams adopt the C++ avatar but receive `legacy-safe` routing (the unknown-version
   fallback) rather than accurate tier-specific guidance. This check must be woven into the
   adoption checklist that lives **outside** the C++ avatar directory.

---

## Scope and Authority Boundary

| Item | Files Changed | Authority Required |
|------|--------------|-------------------|
| `schema_version` enforcement | `tools/constitution-lint/` | Cross-repo (lint tool) |
| D3 ref-file existence lint rule | `tools/constitution-lint/` | Cross-repo (lint tool) |
| Mixed-repo .dsp/.dsw clarification | `avatars/technology/cpp/guidance.md` (token-constrained) | C++ avatar — deferred; token budget must be freed first |
| Adoption workflow: C++ version step | `docs/guides/adoption/` or avatar adoption guide | Outside C++ avatar |

---

## Proposed Solution

### Item 1: `schema_version` Enforcement in constitution-lint

Add a new lint rule to `tools/constitution-lint/`:

```
rule: cpp_project_yaml_schema_version
check: if .copilot/project.yaml exists and contains `cpp:` block,
       assert schema_version key is present and value is a quoted string >= "1"
law: ENG-6.7 (audit trail requires versioned artifacts)
severity: FAIL
```

**Acceptance Criteria:**
- Lint fails with `[ENG-6.7]` message when `.copilot/project.yaml` has `cpp:` block but missing `schema_version`
- Lint passes when `schema_version: "1"` is present
- Lint warns (not fails) when `schema_version` value is an unquoted integer

### Item 2: D3 Ref-File Existence Lint Rule

Add a lint rule that traverses all `version_routing_policy.by_standard.*.prefer` and
`*.avoid` lists in `AVATAR-RAG-INDEX.yaml` and asserts each referenced path exists on disk
relative to the `avatars/technology/cpp/` root.

```
rule: avatar_rag_index_ref_files_exist
check: for each path in version_routing_policy prefer/avoid lists,
       assert file exists at avatars/technology/cpp/<path>
law: ENG-10.1 (constitution compliance — stale refs degrade guidance quality)
severity: FAIL
```

**Acceptance Criteria:**
- Lint fails with `[ENG-10.1]` message listing any missing ref files
- Lint passes when all files referenced in prefer/avoid lists exist on disk
- Rule is evaluated for all technology avatars that declare a `version_routing_policy`

### Item 3: Mixed-Repo `.dsp` / `.dsw` Clarification (guidance.md)

**Pre-condition:** `guidance.md` token budget must be reduced below 440 tokens before this
item can proceed. This requires a targeted trim of existing prose (likely the Reference Index
section footer, which duplicates `reference-index.md` content).

Once budget headroom is available, add a detection-order footnote:

> **Mixed migration note:** If `CMakeLists.txt` and `*.dsp` both exist (partial migration),
> CMake wins — apply the CMakeLists.txt-detected tier.

**Acceptance Criteria:**
- `guidance.md` word count × 1.3 ≤ 450 after the addition
- `test_guidance_md_within_token_budget` passes
- A new test `test_guidance_addresses_mixed_migration` asserts the footnote exists

### Item 4: Adoption Workflow — Explicit C++ Version Declaration

**Investigation needed (see § Open Questions):**
- Locate the canonical avatar adoption guide or onboarding checklist
- Determine if there is a per-technology adoption checklist or a single shared workflow
- Add a mandatory step: *"Declare your C++ standard in `.copilot/project.yaml`; copy the
  template from `avatars/technology/cpp/templates/cpp-project.yaml`"*

**Acceptance Criteria:**
- The adoption workflow (wherever it lives) includes a C++ version declaration step
- The step links to `cpp-project.yaml` template
- A constitution-lint rule or documentation test verifies the adoption guide references
  the template (stretch goal)

---

## Open Questions

1. **Adoption workflow location:** Where is the canonical adoption guide for teams onboarding
   to the constitution? Is it `docs/guides/adoption/`? Does it have per-language checklists?
   This must be investigated before Item 4 can be implemented.

2. **Token budget relief for guidance.md:** What prose can be trimmed to create 10+ token
   headroom for the mixed-migration note? The Extended Reference section (`## Extended
   Reference`) is a candidate — it partially duplicates `reference-index.md`. Trimming it
   would require a test update.

3. **constitution-lint architecture:** Does the lint tool already have a plugin/rule
   registration pattern for new rules? Review `tools/constitution-lint/` before
   implementing Items 1–2.

---

## Deliverables

| # | Deliverable | Item |
|---|------------|------|
| D1 | `schema_version` lint rule in `tools/constitution-lint/` | Item 1 |
| D2 | `avatar_rag_index_ref_files_exist` lint rule | Item 2 |
| D3 | Updated `guidance.md` with mixed-migration footnote | Item 3 |
| D4 | Adoption guide updated with C++ version declaration step | Item 4 |
| D5 | RED→GREEN tests for D1–D4 (ENG-4.1) | All |

---

## Success Criteria

| ID | Criterion | Verification |
|----|-----------|-------------|
| SC-1 | `schema_version` enforcement catches missing version | Lint test: missing key → FAIL |
| SC-2 | D3 ref-file existence checked at lint time | Lint test: deleted ref → FAIL |
| SC-3 | guidance.md mixed-migration note present and within token budget | `test_guidance_addresses_mixed_migration` + budget test |
| SC-4 | Adoption guide references `cpp-project.yaml` template | Documentation test or manual verification |
| SC-5 | All pre-existing 816 tests continue to pass | `python -m pytest tests/ -q` |
| SC-6 | constitution-lint reports 20/20 pass | `aa-constitution-lint .` |

---

## Relationship to cpp-version-routing-foundation

This proposal is the **direct successor** to `cpp-version-routing-foundation`. Phase 1 of
that proposal established the routing infrastructure (detection order, tier policy,
example frontmatter, project template). This proposal closes the three advisory items
(N3 was resolved in the predecessor PR) that required changes outside the C++ avatar scope
plus the adoption workflow gap that was identified as a systemic risk.

The mixed-repo clarification (Item 3) was deferred from the predecessor solely because
`guidance.md` was at the 450-token ceiling — not because it is low priority. It should be
the first item tackled in this proposal after token budget headroom is confirmed.

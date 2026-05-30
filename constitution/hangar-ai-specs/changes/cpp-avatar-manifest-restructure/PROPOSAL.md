# Proposal: C++ Avatar Manifest 150-Token Compliance (Contingency)

**Proposal ID:** cpp-manifest-150t-compliance
**Submitted:** April 14, 2026
**Status:** ⏸️ CONTINGENT — activated only if `cpp-manifest-token-exception` is rejected
**Parent PR:** #14 (c-plus-plus-avatar-enrichment)
**Depends On:** `cpp-split-reference-architecture` (must complete first — provides routing destinations)
**Contingent On:** `cpp-manifest-token-exception` rejection

---

## Laws Cited (ENG-11.2 Compliance)

| Law ID | Title | Relevance |
|--------|-------|-----------|
| [ENG-11.1](laws/engineering/eng-11-hangar-sdd.md) | Hangar SDD Law | Governs proposal lifecycle |
| [ENG-10.1](laws/engineering/eng-10-constitution.md) | Constitution Compliance | Avatar Model Schema §2 enforces ≤150t manifest budget |
| [ENG-4.1](laws/engineering/eng-4-testing.md) | Atomic TDD Law | All code changes follow RED–GREEN–REFACTOR |
| [ENG-6.7](laws/engineering/eng-6-security.md) | Audit Trail Law | Content routing must be traceable |

---

## Problem Statement

If the ENG-10.3 Exception Request (`cpp-manifest-token-exception`) is **rejected**, the C++ avatar must comply with the 150-token manifest budget defined in `avatar-model-schema.md §2`.

The manifest is currently ~985 tokens. All 8 remaining blocks are on the schema §3 allowlist, but only 3 are required. The other 5 optional blocks (~524t) plus excess detail in required blocks (~311t) must be routed to the split reference files created by `cpp-split-reference-architecture`.

> **This proposal is dormant.** It will only be activated if the exception request is denied. If the exception is granted, this proposal should be archived without implementation.

---

## Solution: Three-Phase Manifest Trim

### Phase A — Route Optional Allowlist Blocks (saves ~524t)

Remove 4 optional blocks and route content to split reference files:

| Block | Tokens | Destination |
|-------|--------|-------------|
| `dependencies` | ~105t | `ref-build-toolchain.md` |
| `commands` | ~150t | `ref-operational.md` |
| `conventions` | ~98t | `ref-core-patterns.md` |
| `project_structure` | ~171t | `ref-build-toolchain.md` |

Result: ~985t → ~461t

### Phase B — Trim `stack` to Required Fields (saves ~130t)

Keep only schema-required fields (`language`, `framework`, `testing`). Route to `ref-build-toolchain.md`:
- `compilers` matrix (4 tiers × 3 compilers)
- `version_policy` (greenfield/brownfield)
- `build` tools list
- `sanitizers` (mandatory/recommended)

Result: ~461t → ~331t

### Phase C — Trim `specializes_laws` to Non-Negotiable Subset (saves ~191t)

Keep 4 non-negotiable law entries:
- ENG-4.1 (Atomic TDD)
- ENG-6.1 (Security by Design)
- ENG-6.4 (Data Protection)
- ENG-6.7 (Audit Trail)

Move the full 21-entry law registry to `ref-operational.md` with a YAML comment in manifest:

```yaml
# Full law registry: see ref-operational.md § Law Specialization Registry
specializes_laws:
  - id: ENG-4.1
    title: Atomic TDD Law
    example_file: examples/ENG-4.1-atomic-tdd.md
  - id: ENG-6.1
    title: Security by Design
    example_file: examples/ENG-6.1-security-by-design.md
  - id: ENG-6.4
    title: Data Protection
    example_file: examples/ENG-6.4-data-protection.md
  - id: ENG-6.7
    title: Audit Trail
    example_file: examples/ENG-6.7-audit-trail.md
```

Result: ~331t → **~140t ✅** (under 150t budget)

---

## Deliverables

| # | Artifact | Description | Status |
|---|----------|-------------|--------|
| D1 | `manifest.yaml` Phase A | Remove optional blocks with routing comments | ⬜ Contingent |
| D2 | `manifest.yaml` Phase B | Trim stack to required fields | ⬜ Contingent |
| D3 | `manifest.yaml` Phase C | Trim specializes_laws to 4 non-negotiable entries | ⬜ Contingent |
| D4 | `ref-build-toolchain.md` update | Receive dependencies, project_structure, stack detail | ⬜ Contingent |
| D5 | `ref-operational.md` update | Receive commands, full law registry | ⬜ Contingent |
| D6 | `ref-core-patterns.md` update | Receive conventions | ⬜ Contingent |
| D7 | Test suite updates | Update tests asserting manifest structure | ⬜ Contingent |
| D8 | Token verification | Confirm manifest ≤ 150t | ⬜ Contingent |

---

## Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| `manifest.yaml` ≤ 150 tokens | `word_count × 1.3 ≤ 150` |
| Zero content loss | All manifest content present in corresponding `ref-*.md` file |
| All tests pass | Full test suite green after restructure |
| Manifest retains all required fields | `avatar`, `stack` (language/framework/testing), `activates`, `specializes_laws` (≥1 entry) |

---

## Activation Criteria

This proposal is activated **only if**:

1. `cpp-manifest-token-exception` is formally **REJECTED** by Constitution Governance Lead
2. `cpp-split-reference-architecture` is **COMPLETE** (split files exist as routing destinations)

If the exception is **GRANTED**, archive this proposal:
```bash
mv hangar-ai-specs/changes/cpp-manifest-150t-compliance \
   hangar-ai-specs/archive/$(date +%Y-%m-%d)-cpp-manifest-150t-compliance-not-needed
```

---

## Relationship to Other Proposals

| Proposal | Relationship |
|----------|-------------|
| `cpp-manifest-token-exception` | If granted → this proposal is archived. If rejected → this proposal is activated. |
| `cpp-split-reference-architecture` | Hard dependency — split files must exist before manifest content can be routed to them |

---

## Advisory: avatar.id Format Inconsistency

**Finding:** The avatar-workflow Phase 2 Step 2.1 checks that `avatar.id` matches the directory slug exactly. The CPP avatar's directory slug is `cpp`, which would imply `id: avatar-cpp`. The current value is `id: avatar-technology-cpp`.

**Scope:** This is NOT a CPP-only issue. The id format is inconsistent across the entire repo:
- Most avatars use `avatar-{slug}` (e.g., `avatar-angular`, `avatar-java-spring`)
- A few use `avatar-{type}-{slug}` (e.g., `avatar-technology-cpp`, `avatar-technology-azure-data-factory`)

The `index.yaml` and `AVATAR-RAG-INDEX.yaml` both register CPP as `avatar-technology-cpp` — so the manifest, index, and RAG index are mutually consistent. The mismatch is between the manifest value and the directory slug alone.

**Recommendation:** This is a **schema clarification** issue, not a CPP defect. The schema should be updated to explicitly permit `avatar-{type}-{slug}` as a valid `id` format. File a separate constitution amendment for `avatar-model-schema.md §3` rather than renaming the CPP avatar id (which would break index.yaml and all tests).

**Action if this proposal is activated:** Do NOT change `id: avatar-technology-cpp`. Add a schema clarification task to the amendment instead.

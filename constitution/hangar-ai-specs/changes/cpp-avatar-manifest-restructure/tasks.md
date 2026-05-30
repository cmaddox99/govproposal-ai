# Tasks: cpp-manifest-150t-compliance (Contingency)

**Proposal:** [PROPOSAL.md](PROPOSAL.md)
**PR:** #14
**Status:** ⏸️ CONTINGENT — activated only if `cpp-manifest-token-exception` is rejected
**Depends On:** `cpp-split-reference-architecture` must be COMPLETE before activation

---

## Progress Summary

- Total tasks: 10
- Completed: 1
- Remaining: 9

---

## Pre-Work (Already Completed)

- [x] Phase 0: Route 6 forbidden/unknown manifest blocks to constitutional locations (commit `8da07b5`) ✓

## Phase A: Route Optional Allowlist Blocks (contingent)

- [ ] A.1: Move `dependencies` block content to `ref-build-toolchain.md`
- [ ] A.2: Move `commands` block content to `ref-operational.md`
- [ ] A.3: Move `conventions` block content to `ref-core-patterns.md`
- [ ] A.4: Move `project_structure` block content to `ref-build-toolchain.md`
- [ ] A.5: Remove all 4 blocks from `manifest.yaml`; verify ~461t

## Phase B: Trim Stack to Required Fields (contingent)

- [ ] B.1: Move `compilers`, `version_policy`, `build`, `sanitizers` to `ref-build-toolchain.md`
- [ ] B.2: Keep only `language`, `framework`, `testing` in stack; verify ~331t

## Phase C: Trim specializes_laws (contingent)

- [ ] C.1: Move full 21-entry law registry to `ref-operational.md`
- [ ] C.2: Keep only ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7 in manifest; verify ≤150t

## Phase D: Test Updates (contingent)

- [ ] D.1: Update all tests asserting manifest structure; full suite green

# Tasks: Lint Law Integrity Checks

**Proposal:** [PROPOSAL.md](PROPOSAL.md)
**Spec ID:** `lint-law-integrity-checks`
**Status:** ✅ IMPLEMENTED (Phase 1-3 complete)

---

## Phase 1: LawTitleCoherenceRule (S1)

> **Goal:** Detect title mismatches between `_domain.yaml` registry comments and
> `.md` frontmatter titles. Currently 36 mismatches on `main`. Also distinguish
> law IDs with missing `_domain.yaml` comments as a separate diagnostic.

- [x] 1.1 Write ONE failing test: rule returns FAIL when `_domain.yaml` comment differs from `.md` frontmatter title (RED) ✓
- [x] 1.2 Implement `LawTitleCoherenceRule` ✓
- [x] 1.3 Refactor: extract shared cached parser (`law_parser.py`) ✓
- [x] 1.4 Run full test suite + `aa-constitution-lint .` ✓

## Phase 2: LawBodyExistenceRule (S2)

> **Goal:** Detect law IDs declared in `_domain.yaml` with no `.md` body content
> and no `status` field acknowledging the gap.

- [x] 2.1 Write ONE failing test: phantom article + deferred tolerance (RED) ✓
- [x] 2.2 Implement `LawBodyExistenceRule` ✓
- [x] 2.3 Refactor (minimal — uses shared parser) ✓
- [x] 2.4 Run full test suite + `aa-constitution-lint .` ✓

## Phase 3: DomainRegistrationCompletenessRule (S3)

> **Goal:** Detect law IDs in `.md` frontmatter that are not registered in any
> `_domain.yaml` article. Currently ENG-13.1, ENG-13.2, ENG-13.3 are orphans.
> Named `DomainRegistrationCompletenessRule` to disambiguate from the existing
> `LawsRegistryCompleteRule` (which checks `laws/index.yaml`).

- [x] 3.1 Write ONE failing test: orphan law detection (RED) ✓
- [x] 3.2 Implement `DomainRegistrationCompletenessRule` ✓
- [x] 3.3 Refactor (minimal — uses shared parser) ✓
- [x] 3.4 Run full test suite + `aa-constitution-lint .` ✓

## Phase 4: Integration Verification

- [x] 4.1 Run `aa-constitution-lint .` — confirmed 20 total rules (17 PASS + 3 WARNING) ✓
- [x] 4.2 Verified new rules report drift: 35 mismatches, 11 phantoms, 3 orphans ✓
- [x] 4.3 Verified 17 existing rules still PASS ✓

## Phase 5: Commit

- [x] 5.1 Committed: `5461a0b` — all 3 rules in single commit per combined TDD cycle ✓
- [ ] 5.4 Push branch and open PR targeting `main`

## Phase 6: Follow-Up Tracking

- [ ] 6.1 File tracked issue: promote WARNING → FAIL after data-fix reconciliation PR merges
- [ ] 6.2 File tracked issue: `_domain.yaml` ↔ `.md` non-negotiable flag sync linter rule (gap not covered by existing `NonnegLawsConsistentRule` which only checks `laws/index.yaml`)

---

## Progress Summary

| Phase | Tasks | Done |
|-------|-------|------|
| Phase 1: Title Coherence Rule | 4 | 4 |
| Phase 2: Body Existence Rule | 4 | 4 |
| Phase 3: Domain Registration Completeness Rule | 4 | 4 |
| Phase 4: Integration Verification | 3 | 3 |
| Phase 5: Commit | 2 | 1 |
| Phase 6: Follow-Up Tracking | 2 | 0 |
| **Total** | **19** | **16** |

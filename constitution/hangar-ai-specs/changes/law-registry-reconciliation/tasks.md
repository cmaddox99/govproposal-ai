# Tasks: Law Registry Reconciliation

**Proposal:** [PROPOSAL.md](PROPOSAL.md)
**Spec ID:** `law-registry-reconciliation`
**Status:** 📋 IN PROGRESS

---

## Phase 4a: Fix Business Domain Title Mismatches (S1)

> **File:** `laws/business/_domain.yaml` — 16 title comment fixes
> **Retire:** 4 pinning tests (BUS-3.2–3.5 title drift)

- [ ] 4a.1 Fix 16 inline comments to match .md frontmatter titles (including NN suffix)
- [ ] 4a.2 Retire 4 pinning tests: TestBusinessArticleIIITitleDrift
- [ ] 4a.3 VERIFY: linter title mismatches reduced; pinning tests updated
- [ ] 4a.4 COMMIT: `fix(laws): reconcile business _domain.yaml titles (law-registry-reconciliation/S1)`

## Phase 4b: Fix Engineering Domain Title Mismatches (S1)

> **File:** `laws/engineering/_domain.yaml` — 7 title comment fixes
> **Retire:** 4 pinning tests (ENG-10.1–10.4 title drift)

- [ ] 4b.1 Fix 7 inline comments to match .md frontmatter titles (including NN suffix)
- [ ] 4b.2 Retire 4 pinning tests: TestEngineeringArticleXTitleDrift
- [ ] 4b.3 VERIFY: linter title mismatches reduced; pinning tests updated
- [ ] 4b.4 COMMIT: `fix(laws): reconcile engineering _domain.yaml titles (law-registry-reconciliation/S1)`

## Phase 4c: Fix Product Domain Title Mismatches (S1)

> **File:** `laws/product/_domain.yaml` — 12 title comment fixes

- [ ] 4c.1 Fix 12 inline comments to match .md frontmatter titles (including NN suffix)
- [ ] 4c.2 VERIFY: LawTitleCoherenceRule returns PASS (0 mismatches)
- [ ] 4c.3 COMMIT: `fix(laws): reconcile product _domain.yaml titles (law-registry-reconciliation/S1)`

## Phase 4d: Defer Whole-Article Phantoms (S2a)

> **Files:** `laws/business/_domain.yaml`, `laws/engineering/_domain.yaml`, `DEFERRED_LAWS.md`

- [ ] 4d.1 Add `status: deferred` to BUS-X, ENG-VIII, ENG-IX
- [ ] 4d.2 Add disposition entries to DEFERRED_LAWS.md for all 3 articles
- [ ] 4d.3 VERIFY: linter phantom count reduced
- [ ] 4d.4 COMMIT: `fix(laws): defer 3 whole-article phantoms (law-registry-reconciliation/S2a)`

## Phase 4e: Remove Tail-Law Phantoms (S2b)

> **Files:** all 3 `_domain.yaml`, `DEFERRED_LAWS.md`

- [ ] 4e.1 Remove 9 phantom IDs from active articles
- [ ] 4e.2 Add "Removed Aspirational IDs" section to DEFERRED_LAWS.md
- [ ] 4e.3 VERIFY: LawBodyExistenceRule returns PASS (0 phantoms)
- [ ] 4e.4 COMMIT: `fix(laws): remove 9 phantom tail-law IDs (law-registry-reconciliation/S2b)`

## Phase 4f: Register ENG-13.x (S3)

> **File:** `laws/engineering/_domain.yaml`

- [ ] 4f.1 Add Article XIII with ENG-13.1, ENG-13.2, ENG-13.3
- [ ] 4f.2 VERIFY: DomainRegistrationCompletenessRule returns PASS
- [ ] 4f.3 COMMIT: `fix(laws): register ENG-13.x in Article XIII (law-registry-reconciliation/S3)`

## Phase 4g: Non-Negotiable Flag Sync (S4)

> **File:** `laws/engineering/_domain.yaml`
> **Retire:** 1 pinning test (ENG-10.1 NN flag sync)

- [ ] 4g.1 Add `non_negotiable: [ENG-10.1]` to Article X
- [ ] 4g.2 Retire pinning test: TestNonNegotiableFlagSync
- [ ] 4g.3 VERIFY: all 5 correctness tests PASS
- [ ] 4g.4 COMMIT: `fix(laws): sync ENG-10.1 non-negotiable flag (law-registry-reconciliation/S4)`

## Phase 5: Promote Linter Rules WARNING → FAIL

- [ ] 5.1 Change 3 integrity rules from WARNING to FAIL (scoped: not avatar citation rule)
- [ ] 5.2 VERIFY: `aa-constitution-lint .` → 20 passed, 0 warnings, 0 failed
- [ ] 5.3 COMMIT: `feat(lint): promote law integrity rules to FAIL severity`

## Phase 6: Certify

- [ ] 6.1 Run full governance + linter suite — confirm all green
- [ ] 6.2 Push branch and open PR

---

## Progress Summary

| Phase | Tasks | Done |
|-------|-------|------|
| 4a: Business titles | 4 | 0 |
| 4b: Engineering titles | 4 | 0 |
| 4c: Product titles | 3 | 0 |
| 4d: Defer phantoms (S2a) | 4 | 0 |
| 4e: Remove phantoms (S2b) | 4 | 0 |
| 4f: Register ENG-13.x (S3) | 3 | 0 |
| 4g: NN flag sync (S4) | 4 | 0 |
| 5: Promote to FAIL | 3 | 0 |
| 6: Certify | 2 | 0 |
| **Total** | **31** | **0** |

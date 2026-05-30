# Proposal: Law Registry Reconciliation

**Status:** 📋 IN PROGRESS
**Spec ID:** `law-registry-reconciliation`
**Workflow:** Legacy Rescue — Refactor Track (Phase 4: Remediate)
**Triggered by:** Constitution integrity audit (April 16, 2026) and
`lint-law-integrity-checks` linter rules now surfacing 3 WARNING categories.
**Depends on:** `lint-law-integrity-checks` (merged PR #33 — enforcement is in place).

---

## Problem Statement

The `.md` body files are the authoritative source of truth for law titles.
The `_domain.yaml` registry files were written independently and have drifted.
Categories of drift detected by `aa-constitution-lint`:

| Category | Count | Fix Location |
|----------|-------|-------------|
| Title mismatches (`_domain.yaml` comment ≠ `.md` frontmatter) | 35 | `_domain.yaml` inline comments |
| Whole-article phantoms (no `.md` body, no `status` field) | 3 articles, 15 law IDs | `_domain.yaml` `status:` field + `DEFERRED_LAWS.md` |
| Tail-law phantoms in active articles | 8 articles, 9 law IDs | Remove from `_domain.yaml` + document in `DEFERRED_LAWS.md` |
| Orphan authored laws (in `.md` but not in `_domain.yaml`) | 3 (ENG-13.1–13.3) | New Article XIII in `_domain.yaml` |
| Non-negotiable flag not propagated to registry | 1 (ENG-10.1) | Add `non_negotiable: [ENG-10.1]` to Article X |

**Principle:** `.md` body files are NOT modified. All fixes go to `_domain.yaml` and `DEFERRED_LAWS.md`.

### Forensic Finding

Git history forensics confirmed: **No law bodies were accidentally deleted.** All 24
phantom law IDs (across 11 unstatused articles) were planned-but-never-authored
placeholders from the initial commit. The `.md` files never contained sections for
these law IDs.

---

## Solution

### S1 — Fix 35 title mismatches

Update `_domain.yaml` inline `# comments` to match `.md` frontmatter titles.
NON-NEGOTIABLE laws get `(NON-NEGOTIABLE)` suffix per existing convention.

- `laws/business/_domain.yaml` — 16 fixes
- `laws/engineering/_domain.yaml` — 7 fixes
- `laws/product/_domain.yaml` — 12 fixes

### S2a — Defer 3 whole-article phantoms (Category B)

Add `status: deferred` to articles where ALL laws have no `.md` body:
- **BUS Article X** (Business Continuity Laws): BUS-10.1–10.5. Disposition: AUTHOR
- **ENG Article VIII** (Platform Integration Laws): ENG-8.1–8.5. Disposition: DELEGATE
- **ENG Article IX** (AI-Engineer Collaboration Laws): ENG-9.1–9.5. Disposition: AUTHOR

Update `DEFERRED_LAWS.md` with disposition entries for all 3.

### S2b — Remove 9 phantom tail-law IDs from active articles (Category C)

Remove never-authored placeholder IDs from `_domain.yaml`:
BUS-2.5, BUS-2.6, BUS-6.5, BUS-7.5, BUS-9.5, PRD-3.5, PRD-4.5, PRD-5.5, PRD-6.4.

Add "Removed Aspirational IDs" section to `DEFERRED_LAWS.md` documenting each
removal. Flag BUS-2.5 (SOX) and PRD-3.5 (Accessibility) for priority authoring.

### S3 — Register orphan laws ENG-13.1–13.3

Add new Article XIII to `laws/engineering/_domain.yaml`:
```yaml
  XIII:
    title: Artifact Rendering Laws
    laws:
      - ENG-13.1  # Artifact Rendering Standard
      - ENG-13.2  # Citation Transparency Law
      - ENG-13.3  # PDF Reproducibility Law
```

Note: ENG-13.1 is `non_negotiable: false` (RECOMMENDED status, not yet promoted).

### S4 — Non-negotiable flag sync

Add `non_negotiable: [ENG-10.1]` to Article X in `laws/engineering/_domain.yaml`.

---

## Design Decisions

### D1 — One commit per logical unit

Title fixes grouped by domain file; S2a, S2b, S3, S4 each get their own commit.
Pinning tests retired in the same commit that breaks them.

### D2 — Remove rather than defer Category C IDs

Panel 1 established that `status: deferred` at article level would incorrectly
mark active articles (with NON-NEGOTIABLE laws like BUS-2.1, BUS-7.1, BUS-9.3)
as deferred. Removal is semantically correct; `DEFERRED_LAWS.md` preserves
traceability per ENG-6.7.

### D3 — Phase 5 in scope

WARNING→FAIL promotion included in the same branch per Panel 1 B5. Scope limited
to the 3 law integrity rules only (not `AvatarManifestNonnegCitationRule`).

---

## Acceptance Criteria

| Criterion | Measure |
|-----------|---------|
| Zero title mismatches | `LawTitleCoherenceRule` returns PASS |
| Zero phantom articles | `LawBodyExistenceRule` returns PASS |
| Zero orphan laws | `DomainRegistrationCompletenessRule` returns PASS |
| All 20 linter rules PASS at FAIL severity | `aa-constitution-lint .` → 20 passed, 0 warnings, 0 failed |
| All 5 governance correctness tests PASS | `pytest tests/governance/test_correctness_drift.py` → 5 passed |
| No `.md` law files modified | Only `_domain.yaml`, `DEFERRED_LAWS.md`, and linter code changed |
| All removed IDs documented in DEFERRED_LAWS.md | Audit trail per ENG-6.7 |

---

## Panel Review Record

### Panel 1 (April 16, 2026) — APPROVE WITH CONDITIONS
5 blocking findings (B1–B5), all resolved in amended proposal:
- B1: S2 split into S2a+S2b (Category C cannot use article-level deferred)
- B2: S4 added (NN flag sync for ENG-10.1)
- B3: DEFERRED_LAWS.md entries required for Category B
- B4: Removed IDs must be documented per ENG-6.7
- B5: WARNING→FAIL promotion must be in scope

### Panel 2 (April 16, 2026) — APPROVE WITH CONDITIONS
3 blocking findings (all same root cause — S3 drafted from memory):
- B1/B2: ENG-13.2 title corrected to "Citation Transparency Law"; ENG-13.3 to "PDF Reproducibility Law"
- B3: ENG-13.1 `non_negotiable` removed (`.md` says false; RECOMMENDED status)

---

## Laws Cited

| Law | Relevance |
|-----|-----------|
| [ENG-10.1](../../laws/engineering/governance.md) | Constitution Metrics Collection — linter enforcement |
| [ENG-4.1](../../laws/engineering/testing.md) | Atomic TDD — one verifiable fix per commit |
| [ENG-6.7](../../laws/engineering/security.md) | Audit Trail — traceability for all changes |
| [ENG-11.1](../../laws/engineering/spec-driven-development.md) | Hangar SDD — proposal-driven lifecycle |
| [BUS-1.1](../../laws/business/foundations.md) | Priority Hierarchy — legal compliance first |

## References

- [lint-law-integrity-checks/PROPOSAL.md](../lint-law-integrity-checks/PROPOSAL.md) — enforcement rules
- [DEFERRED_LAWS.md](../../DEFERRED_LAWS.md) — deferred article status and dispositions

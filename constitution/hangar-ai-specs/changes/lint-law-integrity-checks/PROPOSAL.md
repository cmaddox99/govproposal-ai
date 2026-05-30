# Proposal: Lint Law Integrity Checks

**Status:** 📋 PROPOSED
**Spec ID:** `lint-law-integrity-checks`
**Triggered by:** Constitution integrity audit (April 16, 2026) — 36 title mismatches,
47 bodiless law IDs, and 3 orphan laws discovered between `_domain.yaml` registries
and `.md` body files. The existing linter (`aa-constitution-lint`) passes 17/17 but
does not check any of these integrity properties. The governance test suite
(`tests/governance/`) does check them — and currently shows 5 correctness failures —
but these tests are not wired into the linter or CI PR gate.

**Scope:**
1. Three new linter rules in `tools/constitution-lint/`
2. Unit tests for each rule
3. Linter rule registration

**Independent of:** The separate data-fix effort to reconcile `_domain.yaml` titles
with `.md` body content. This proposal builds the enforcement; the reconciliation
is a follow-up.

---

## Problem Statement

### P1 — Title Drift Is Invisible in CI

The `_domain.yaml` comment titles disagree with `.md` frontmatter titles for 36 of
118 laws (31% drift rate). Affected articles span all three domains:

| Domain | Drifted Articles | Count |
|--------|-----------------|-------|
| Engineering | VII (Resiliency), X (Governance) | 7 |
| Business | I, II, III, IV, VI, VII, IX | 18 |
| Product | II, III, IV, V, VI | 11 |

The mismatches are not typos — they are completely different law concepts under the
same ID (e.g., ENG-10.1: `_domain.yaml` says "Amendment Process Law," `.md` body says
"Constitution Metrics Collection Law"). Any PR citing a law ID may reference the wrong
concept depending on which file the author read.

The linter does not detect this. PRs with incorrect law citations pass CI.

### P2 — Bodiless Laws Are Not Flagged

47 law IDs exist in `_domain.yaml` with no corresponding `.md` section. Five articles
are already marked `status: deferred` in `DEFERRED_LAWS.md`, but the linter does not
enforce that unstatused articles with missing body content are violations. New phantom
articles could be introduced without detection.

### P3 — Orphan Laws Are Not Flagged

3 laws (ENG-13.1, ENG-13.2, ENG-13.3 in `artifact-rendering.md`) exist in `.md` body
files but are not registered in `_domain.yaml`. The linter does not detect this.

### P4 — Governance Tests Exist but Are Not in the Linter

`tests/governance/test_correctness_drift.py` already checks all five properties
(title coherence, NN flag sync, phantom detection, registration completeness, orphan
detection). But these are pytest-only — they do not run as linter rules, do not
produce `LawEvaluation` objects, and do not appear in the linter's CI summary.

The linter is the enforcement point that every PR must pass. The governance tests are
a development aid. Promoting these checks into linter rules closes the gap.

---

## Solution

### S1 — New Rule: `constitution.law_title_coherence`

**File:** `tools/constitution-lint/src/aa_constitution_lint/domain/rules/constitution.py`

For every law ID that appears in both a `_domain.yaml` article and a `.md` frontmatter
entry, the `_domain.yaml` comment title must contain (or be contained by) the `.md`
frontmatter title, after normalizing parenthetical suffixes and trailing punctuation.

Law IDs with no `_domain.yaml` inline comment are reported as **"comment missing"**
(a distinct diagnostic), not as title mismatches. This prevents inflating the mismatch
count and gives authors a clear remediation path.

**Logic:** Reuse the `_title_matches_comment()` normalization from `tests/governance/
test_correctness_drift.py`. Parse `_domain.yaml` raw text for `# comment` extraction
using a line-anchored regex (`^\s*-\s*["']?{law_id}["']?\s*#\s*(.*)$`) rather than
the looser `law_id in line and "#" in line` pattern from `conftest.py`, to avoid
false matches when a law ID appears in an unrelated YAML comment. Compare against
frontmatter titles from `.md` law files.

**Result:**
- PASS if zero mismatches and zero missing comments
- WARNING with list of `{law_id, article}` for each missing comment
- FAIL with list of `{law_id, registry_comment, law_file_title}` for each mismatch
- Tolerant of laws that exist in only one source (covered by S2/S3)

**Law:** ENG-10.1 (Constitution Metrics Collection Law)

### S2 — New Rule: `constitution.law_body_existence`

**File:** Same file as S1.

For every law ID declared in a `_domain.yaml` article, either:
- (a) a `.md` frontmatter entry for that ID exists in the same domain directory, OR
- (b) the article carries `status` in `{deferred, delegated, draft, superseded}`

Articles that declare IDs without law files AND without a status field produce FAIL.
Deferred articles produce PASS (the gap is acknowledged).

**Logic:** Adapted from `TestNoUnstatusedPhantoms` in `test_correctness_drift.py`.

**Law:** ENG-10.1

### S3 — New Rule: `constitution.domain_registration_completeness`

**Class:** `DomainRegistrationCompletenessRule`
**File:** Same file as S1.

For every law ID found in a `.md` frontmatter entry, that ID must appear in at least
one article's law list in the corresponding domain's `_domain.yaml`.

> **Naming note:** This rule is deliberately named `DomainRegistrationCompletenessRule`
> to distinguish it from the existing `LawsRegistryCompleteRule` in `index_integrity.py`,
> which checks `laws/index.yaml` ↔ `.md` frontmatter. This rule checks `_domain.yaml`
> ↔ `.md` frontmatter — a different registry.

**Logic:** Adapted from `TestEveryAuthoredLawIsRegistered` and
`TestNoOrphanAuthoredLaws` in `test_correctness_drift.py`.

**Law:** ENG-10.1

---

## Design Decisions

### D1 — Reuse governance test logic, don't import it

The governance test fixtures (`conftest.py`) contain parsing logic for `_domain.yaml`
and `.md` frontmatter. The linter rules should reuse the same _algorithms_ but must
not import from `tests/`. The parsing logic must live in the linter's domain layer as
a **shared cached helper module** (not inline in each rule). All three rules parse the
same `_domain.yaml` and `.md` files — without a shared caching layer, the same YAML
files are parsed 3× per lint run. The shared parser is a performance requirement, not
optional cleanup.

The governance tests then become the correctness regression layer — they assert the
same properties but via pytest fixtures rather than `LawEvaluation` objects.

### D2 — WARNING severity initially, promote to FAIL after reconciliation

Since 36 title mismatches and 3 orphans currently exist on `main`, the new rules
would immediately fail CI if set to FAIL, blocking all other PRs.

**Option A:** Ship the rules as FAIL-level. This creates urgency but blocks every
PR in the repository until the data-fix reconciliation lands.

**Option B:** Ship as WARNING-level initially. Allows drift to accumulate during
the window but avoids blocking the PR pipeline.

**Option C (recommended):** Ship as WARNING-level. Add a tracked follow-up task to
promote to FAIL once the data-fix reconciliation PR merges. This unblocks the
enforcement infrastructure without blocking the pipeline. The promotion is a
one-line severity change per rule — trivial to execute, but gated on the data fix.

### D3 — Existing rules are unmodified

The 17 existing linter rules are unchanged. The three new rules are additive.

---

## Deliverables

| # | Deliverable | Path | Notes |
|---|-------------|------|-------|
| D1 | `LawTitleCoherenceRule` | `tools/constitution-lint/src/.../rules/constitution.py` | New rule class |
| D2 | `LawBodyExistenceRule` | Same file | New rule class |
| D3 | `DomainRegistrationCompletenessRule` | Same file | New rule class (renamed to disambiguate from `LawsRegistryCompleteRule`) |
| D4 | Shared domain YAML / `.md` parser | `tools/constitution-lint/src/.../domain/` helper module | Cached per-run; required by all 3 rules |
| D5 | Rule registration | `tools/constitution-lint/src/.../cli.py` or rule factory | Wire into linter |
| D6 | Unit tests (3 rules × RED/GREEN) | `tests/unit/` or `tools/constitution-lint/tests/` | Atomic TDD |

---

## Acceptance Criteria

| Criterion | Measure |
|-----------|---------|
| Title coherence rule detects known mismatches | Rule returns WARNING with all title mismatches present on `main` at implementation time (currently 36) |
| Title coherence rule distinguishes missing comments | Missing `_domain.yaml` comments reported as distinct "comment missing" diagnostic, not as title mismatches |
| Body existence rule detects unstatused phantoms | Rule returns WARNING for articles with missing bodies and no `status` field |
| Body existence rule tolerates deferred articles | Rule returns PASS for `status:deferred` articles |
| Registration completeness rule detects orphans | Rule returns WARNING with ENG-13.1, ENG-13.2, ENG-13.3 when run against current `main` |
| All 17 existing rules still pass | `aa-constitution-lint .` shows ≥17 PASS (plus new rules) |
| Unit tests cover each rule | At least 1 test per rule with known-good and known-bad fixtures |
| Linter output count increases | Summary shows 20 total rules (17 existing + 3 new) |
| No overlapping error messages | New rule violations are distinguishable from existing `AvatarRagLawsValidRule` / `LawReferenceRule` output when the same law ID triggers both |

---

## Laws Cited

| Law | Relevance |
|-----|-----------|
| [ENG-10.1](../../laws/engineering/governance.md) | Constitution Metrics Collection — linter is the enforcement point for constitutional compliance metrics |
| [ENG-11.1](../../laws/engineering/spec-driven-development.md) | Hangar SDD — this proposal follows PROPOSE → IMPLEMENT → ARCHIVE |
| [ENG-11.2](../../laws/engineering/spec-driven-development.md) | Proposal Completeness — required sections present with law citations |
| [ENG-4.1](../../laws/engineering/testing.md) | Atomic TDD — new rules implemented via RED → GREEN → REFACTOR |

---

## Relationship to Existing Governance Tests

The `tests/governance/` suite will remain as the correctness regression layer:

| Property | Governance Test | Linter Rule (this proposal) |
|----------|----------------|----------------------------|
| Title coherence | `TestTitleCoherence` | `LawTitleCoherenceRule` (S1) |
| NN flag sync | `TestNonNegotiableFlagSync` | Out of scope — see note below |
| Phantom detection | `TestNoUnstatusedPhantoms` | `LawBodyExistenceRule` (S2) |
| Registration completeness | `TestEveryAuthoredLawIsRegistered` | `DomainRegistrationCompletenessRule` (S3) |
| Orphan detection | `TestNoOrphanAuthoredLaws` | `DomainRegistrationCompletenessRule` (S3) |

> **NN flag sync coverage note:** The existing `NonnegLawsConsistentRule` checks
> `laws/index.yaml` ↔ `.md` frontmatter. The `_domain.yaml` ↔ `.md` frontmatter
> NN sync gap (tested by `TestNonNegotiableFlagSync` in the governance tests) remains
> a future linter rule candidate and is not addressed by this proposal.

After the data-fix reconciliation lands:
- Governance correctness tests → all PASS
- Governance pinning tests → all FAIL (bugs fixed) → retire them
- Linter rules → all PASS on `main` (after promoting WARNING → FAIL)

---

## References

- [tests/governance/test_correctness_drift.py](../../tests/governance/test_correctness_drift.py) — existing correctness assertions
- [tests/governance/test_pinning_drift.py](../../tests/governance/test_pinning_drift.py) — pinning tests documenting current drift
- [tests/governance/conftest.py](../../tests/governance/conftest.py) — parsing fixtures for `_domain.yaml` and `.md` frontmatter
- [DEFERRED_LAWS.md](../../DEFERRED_LAWS.md) — deferred article status and disposition decisions
- [tools/constitution-lint/src/aa_constitution_lint/domain/rules/constitution.py](../../tools/constitution-lint/src/aa_constitution_lint/domain/rules/constitution.py) — existing rule classes (target file for new rules)
- [tools/constitution-lint/src/aa_constitution_lint/domain/rules/base.py](../../tools/constitution-lint/src/aa_constitution_lint/domain/rules/base.py) — Rule ABC

---

## Panel Review Record

**Date:** April 16, 2026
**Verdict:** APPROVE WITH CONDITIONS
**Panel:** Constitution Architect · Linter Engineer · DevOps/CI Gate Owner · Product Avatar Author · Skeptic/Red Team

### Blocking Findings (resolved in this revision)

| # | Panelist | Finding | Resolution |
|---|----------|---------|------------|
| 4 | DevOps | FAIL severity blocks all PRs with no reconciliation timeline | Adopted Option C: ship as WARNING, tracked promotion task in Phase 6 |
| 6 | Skeptic | `LawRegistrationCompletenessRule` name collides with existing `LawsRegistryCompleteRule` | Renamed to `DomainRegistrationCompletenessRule` |

### Non-Blocking Concerns (incorporated)

| # | Panelist | Finding | Resolution |
|---|----------|---------|------------|
| 1 | Architect | NN flag sync gap undocumented | Added coverage note in §Relationship table + Phase 6.2 follow-up |
| 2 | Linter Eng. | Comment extraction regex is fragile | S1 now specifies line-anchored regex |
| 3 | Linter Eng. | Three rules parse `_domain.yaml` independently | D1 now marks shared cached parser as a requirement; task 1.3 updated |
| 5 | Avatar Author | Overlapping error messages from multiple rules | Added acceptance criterion for distinct diagnostics |
| 7 | Skeptic | "≥36" acceptance criterion is fragile | Changed to "all mismatches present on `main` at implementation time" |
| 8 | Skeptic | Missing comments conflated with mismatches | S1 now distinguishes "comment missing" as a separate diagnostic |
| 9 | Skeptic | Rule registration tasks lack test coverage | Registration folded into GREEN step of each phase |

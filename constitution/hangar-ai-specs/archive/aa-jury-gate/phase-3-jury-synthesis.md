---
schema_version: 1
project: aa-jury-gate
phase: 3
artifact: phase-3-define.md
synthesizer: claude-opus-4.5
juror_count: 5
distinct_models_required: true
jurors:
  - id: J1
    model: claude-opus-4.6
    role: Domain Sceptic
    r1_verdict: NEEDS_REVISION
    r2_verdict: APPROVED
  - id: J2
    model: claude-sonnet-4.6
    role: Technical Expert
    r1_verdict: NEEDS_REVISION
    r2_verdict: NEEDS_REVISION
  - id: J3
    model: gpt-5.4
    role: Strategic/Product Lens
    r1_verdict: NEEDS_REVISION
    r2_verdict: CHALLENGED
  - id: J4
    model: gpt-5.2
    role: Defense Counsel
    r1_verdict: NEEDS_REVISION
    r2_verdict: NEEDS_REVISION
  - id: J5
    model: gpt-5.4-mini
    role: Devil's Advocate
    r1_verdict: NEEDS_REVISION
    r2_verdict: NEEDS_REVISION
rounds:
  r1_completed: true
  r2_completed: true
verdict: APPROVED
date: 2026-05-26
---

## Phase 3 — Define: Judicial Synthesis

**Synthesizer:** claude-opus-4.5
**Artifact:** `phase-3-define.md` (aa-jury-gate CLI)
**Date:** 2026-05-26

---

## Round 1 (R1) — Summary

All 5 jurors returned NEEDS_REVISION in R1. 15 correction IDs were applied across:
- YAML frontmatter extraction algorithm (§2)
- S08 split into S08a/S08b — 14 total checks
- --allow-no-git state matrix (§1.6)
- Security constraints §4 (symlink, DoS, atomic write, path safety)
- --output append semantics §5 (idempotency, sha256, write conditions)
- BDD expanded to 20 scenarios
- DETAIL field format spec (§1.4)

Citation audit post-R1: 19/19 PASS.

---

## Round 2 (R2) — Summary

| Juror | R2 Verdict | Key Items |
|-------|-----------|-----------|
| J1 (claude-opus-4.6) | APPROVED | All 10 J1 corrections confirmed; no residual gaps |
| J2 (claude-sonnet-4.6) | NEEDS_REVISION | sha256 volatility (blocking); BDD S08b coverage (conditional) |
| J3 (gpt-5.4) | CHALLENGED | --output append on exit 1 escalated to synthesizer |
| J4 (gpt-5.2) | NEEDS_REVISION | Temp file same-dir; --log-dir traversal precision |
| J5 (gpt-5.4-mini) | NEEDS_REVISION | --log-dir path resolution; synthesizer distinctness; sha256 doc |

---

## Judicial Synthesis — Adjudication Rulings

### Group 1: sha256 Semantics (RC-P3-J2-008 + RC-P3-J5-012)

**RULING: REQUIRED CHANGE — J2 Option A adopted**

Renamed `sha256_synthesis` → `content_sha256`. Computed after stripping `jury_gate:` key from frontmatter. Stable content-address across re-runs of unchanged synthesis. Operation order documented: exit-2 triggers precede hash computation.

### Group 2: --output append on exit 1 (RC-P3-J3-001 CHALLENGED)

**RULING: CHALLENGE DISMISSED — Current spec stands**

4:1 juror consensus (J1/J2/J4/J5 accepted). Audit trail rationale is sound; artifact-embedded state is durable where stdout/logs are ephemeral. Added CI worktree-cleanup note. J3's concern is valid UX feedback for v1.1, not a v1 blocker.

### Group 3: --log-dir path validation (RC-P3-J4-002 + RC-P3-J5-009)

**RULING: REQUIRED CHANGE — realpath algorithm adopted**

J5's realpath approach supersedes J4's string-check. Algorithm: expand `~` → `os.path.realpath()` (resolves symlinks) → verify result doesn't escape CWD. Reject with exit 2 if fails. String `..` checks removed.

### Group 4: Temp file same-dir (RC-P3-J4-001)

**RULING: REQUIRED CHANGE — same-directory requirement added**

§4 and §5 now specify `tempfile.NamedTemporaryFile(dir=target_dir, delete=False)`. Cross-filesystem `os.replace()` falls back to non-atomic copy; same-dir guarantees atomicity.

### Group 5: BDD coverage gaps (RC-P3-J2-010 + RC-P3-J5-011 + RC-P3-J3-002)

**RULING: REQUIRED CHANGE — BDD-F01 through BDD-F06 added**

6 new scenarios: schema_version absent (F01), S05 pass-through (F02), haiku-4.5 prohibition (F03), B03 missing heading (F04), exit-2 no write (F05), --allow-no-git inside repo (F06). Total: 26 scenarios.

### Group 6: Synthesizer model distinctness (RC-P3-J5-010)

**RULING: DEFERRED TO v2 — R1 decision reaffirmed**

J5 restated rather than introduced new evidence. PRD-2.6 "5 distinct jurors" is core; synthesizer distinctness is v2 hardening. Added to §11 Out of Scope for v1.

### Group 7: Advisory items

All 6 advisory items incorporated:
- RC-P3-J2-009a: `## R1.1` non-match note in §2.1
- RC-P3-J2-009b: `jury_gate:` key reordering note in §5.2
- RC-P3-J2-011: Exit-2 operation order note in §5.3
- RC-P3-J3-004: DETAIL column is informational, parsers must use exit code/CHECK_ID/RESULT
- RC-P3-J3-005: §11 "Out of scope for v1" section added
- RC-P3-J3-003 (security scope): configurable symlink policy deferred to v2; noted in §11

---

## Required Changes Applied

1. `sha256_synthesis` → `content_sha256` (computed post-strip, stable content-address)
2. `--log-dir` validation: realpath-based cwd-boundary algorithm
3. Temp file same-directory requirement for atomic `os.replace()`
4. BDD-F01–F06 added (26 total scenarios)
5. All 6 advisory notes incorporated
6. §5.4 CI worktree-cleanup note; DETAIL column contract

## Deferred to v2

- Synthesizer model distinctness validation (PRD-2.6 hardening)
- Configurable symlink-boundary policy
- `--dry-run`, JSON stdout, alternate failure-write modes

## Dismissed

- RC-P3-J3-001: `--output append` on exit 1 challenge DISMISSED (4:1 consensus, sound rationale)

---

## Synthesizer Re-Verification

All 6 required changes confirmed present in `phase-3-define.md`:

| Change | Location | Confirmed |
|--------|----------|-----------|
| content_sha256 rename + strip semantics | §5.1, §5.3, §6.2, §6.3, §9 | ✅ |
| realpath --log-dir algorithm | §4 | ✅ |
| Temp file same-dir (target_dir) | §4, §5.2 | ✅ |
| BDD-F01–F06 added | §7 | ✅ |
| Advisory notes §2.1, §5.2, §5.3, §5.4 | §2.1, §5.2, §5.3, §5.4 | ✅ |
| §11 Out of scope for v1 | §11 | ✅ |

Citation audit: 19/19 PASS. HTML rendered.

**VERDICT: APPROVED**

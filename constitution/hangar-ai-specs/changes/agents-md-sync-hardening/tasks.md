# Tasks — agents-md-sync-hardening

**Proposal:** AGENTS.md Sync Safety Hardening
**Spec:** PROPOSAL.md in this directory
**Scope:** Stage 1 (FIX-1–3 + IT-1–6) then Stage 2 (FIX-4–14 + IT-7–10)

Progress: 24 / 24 tasks complete + **Stage 1 jury APPROVED** (`8b97a5e`) 🎉

---

## Stage 1 Tasks (gate: FIX-1–3 + IT-1–6)

- [x] **TASK-1** — FIX-1: `_load_canonical_sections()` must surface parser errors ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/resolver.py` (or wherever template loading occurs)
  - Scenario: `fix-1-template-parser-errors-surface` — malformed template must raise, not silently return empty/partial sections
  - Priority: CRITICAL

- [x] **TASK-2** — FIX-2: CRLF handling in BEGIN_RE/END_RE ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/parser.py`
  - Scenario: `fix-2-crlf-markers-recognized` — `$` anchor must match before `\r\n`; use `re.MULTILINE` with `\r?$` or strip CRLFs before parse
  - Priority: CRITICAL

- [x] **TASK-3** — FIX-3: BOM stripping before parse ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/parser.py` (file read path)
  - Scenario: `fix-3-bom-stripped-before-parse` — UTF-8 BOM (`\ufeff`) at file start must be stripped so `^` anchor matches correctly
  - Priority: HIGH

- [x] **TASK-4** — IT-1: CRLF integration test ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-1-crlf-agents-md-markers-recognized` — real AGENTS.md with CRLF line endings; markers recognized; --check exits 0 when current
  - Depends on: TASK-2 (FIX-2)

- [x] **TASK-5** — IT-2: BOM integration test ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-2-bom-agents-md-parsed-correctly` — real AGENTS.md with UTF-8 BOM; BOM stripped; markers recognized correctly
  - Depends on: TASK-3 (FIX-3)

- [x] **TASK-6** — IT-3: Malformed template surfaces error ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-3-malformed-template-error-surfaces` — constitution template with broken markers; tool exits 1 with clear error message (not silent empty result)
  - Depends on: TASK-1 (FIX-1)

- [x] **TASK-7** — IT-4: `--check` on real AGENTS.md ✓ (pending commit) (this repo)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-4-check-on-real-agents-md` — runs `--check` against the actual AGENTS.md in this repo; exits 0 (current); no crash
  - Note: HANGAR_CONSTITUTION_PATH must be set to repo root

- [x] **TASK-8** — IT-5: Non-git directory guard ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-5-non-git-dir-exits-with-error` — tool run against AGENTS.md in a non-git temp directory; exits 1 with explicit error; no write attempted
  - Depends on: FIX-5 (TASK-11 in Stage 2 — BUT: current code returns None from is_git_dirty; test can validate current exit-1 behavior if already guarded, else this test drives FIX-5)
  - Note: If FIX-5 not yet applied, this test will be RED — that is correct and acceptable as a Stage 1 IT

- [x] **TASK-9** — IT-6: `--dry-run` produces unified diff output ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-6-dry-run-shows-unified-diff` — on a drifted AGENTS.md, `--dry-run` stdout contains unified diff markers (`---`, `+++`, `@@`)
  - Note: Tests existing behavior documented in synthesis-r2.md (C-9 correction already applied)

---

## Stage 2 Tasks (gate: all 14 fixes + IT-7–10 + 3-team dry-run review)

- [x] **TASK-10** — FIX-4: Downgrade guard ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/syncer.py`
  - Scenario: `fix-4-downgrade-rejected` — if incoming constitution version < current marker version, abort exit 1 with explicit message
  - Priority: HIGH

- [x] **TASK-11** — FIX-5: Non-git repo explicit guard (**PULLED FORWARD to TASK-8** ✓ no-op)
  - File: `tools/agents-md-sync/aa_agents_sync/git_utils.py`
  - Scenario: `fix-5-non-git-repo-explicit-error` — `is_git_dirty()` returns `None` for non-git dirs; write path must treat None as dirty (refuse write)
  - Priority: HIGH

- [x] **TASK-12** — FIX-6: Pre-write backup ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/syncer.py`
  - Scenario: `fix-6-pre-write-backup-created` — before atomic write, create `AGENTS.md.bak`; backup must exist after successful write
  - Priority: HIGH

- [x] **TASK-13** — FIX-7: Post-write verification + auto-restore ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/syncer.py`
  - Scenario: `fix-7-post-write-verify-and-restore` — after write, re-parse file; if parser error, auto-restore from `.bak` and exit 1
  - Priority: HIGH
  - Depends on: TASK-12 (FIX-6)

- [x] **TASK-14** — FIX-8: File locking ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/syncer.py`
  - Scenario: `fix-8-file-lock-prevents-concurrent-write` — concurrent invocations must not corrupt file; second invocation must wait or exit gracefully
  - Priority: MEDIUM

- [x] **TASK-15** — FIX-9: Resolver integrity check ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/resolver.py`
  - Scenario: `fix-9-resolver-rejects-wrong-constitution` — resolved constitution path must contain at least one valid section template; wrong sibling dir rejected with exit 1
  - Priority: MEDIUM

- [x] **TASK-16** — FIX-10: Version rollback detection ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/syncer.py`
  - Scenario: `fix-10-version-rollback-rejected` — if incoming section version < existing marker version, abort with explicit error (not silent overwrite)
  - Priority: MEDIUM

- [x] **TASK-17** — FIX-11: Idempotency guard ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/syncer.py`
  - Scenario: `fix-11-idempotent-write-skipped` — if content hash after substitution == existing file hash, skip write; exit 0
  - Priority: MEDIUM

- [x] **TASK-18** — FIX-12: Invert write default (`--apply` flag) ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py`
  - Scenario: `fix-12-apply-flag-required-to-write` — `aa-agents-sync AGENTS.md` without `--apply` must behave as dry-run (no write); write only when `--apply` explicitly passed
  - Priority: MEDIUM
  - Note: This is a BREAKING change to CLI behavior — update sync-troubleshooting.md and adoption.md accordingly

- [x] **TASK-19** — FIX-13: `agents-sync.yml` opt-out ✓ (pending commit) config
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py` + new `config.py`
  - Scenario: `fix-13-agents-sync-yml-disables-write` — if `agents-sync.yml` exists at repo root with `enabled: false`, tool exits 0 with "sync disabled" message; no write
  - Priority: LOW

- [x] **TASK-20** — FIX-14: `AGENTS_SYNC_DISABLED=1` kill switch ✓ (pending commit)
  - File: `tools/agents-md-sync/aa_agents_sync/cli.py`
  - Scenario: `fix-14-env-var-disables-all-writes` — if `AGENTS_SYNC_DISABLED=1` env var set, no write attempted under any flag combination; exit 0 with audit log entry
  - Priority: LOW

- [x] **TASK-21** — IT-7: Stale sibling constitution downgrade rejected ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-7-stale-sibling-constitution-downgrade-rejected` — sibling constitution with older version; --apply must refuse with exit 1
  - Depends on: TASK-10 (FIX-4)

- [x] **TASK-22** — IT-8: Race condition / concurrent invocation ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-8-concurrent-invocations-no-corruption` — two concurrent --apply runs; file not corrupted; at least one succeeds
  - Depends on: TASK-14 (FIX-8)

- [x] **TASK-23** — IT-9: `--apply` with backup + post-write verify ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-9-apply-creates-backup-and-verifies` — `--apply` on drifted file; `.bak` exists after; re-parse succeeds
  - Depends on: TASK-12 (FIX-6), TASK-13 (FIX-7), TASK-18 (FIX-12)

- [x] **TASK-24** — IT-10: `AGENTS_SYNC_DISABLED=1` prevents all writes ✓ (pending commit)
  - File: `tests/integration/test_agents_md_sync_hardening.py`
  - Scenario: `it-10-env-var-prevents-write-under-any-flag` — with `AGENTS_SYNC_DISABLED=1`, `--apply` and `--legacy-mode` both exit without writing
  - Depends on: TASK-20 (FIX-14)

---

## Phase Gate

After TASK-9 (Stage 1 complete): jury required before proceeding to Stage 2 tasks.
✅ **Stage 1 jury APPROVED** — synthesis-r1.md/html committed `8b97a5e`; Stage 2 unlocked.
After TASK-24 (Stage 2 complete): Build→Ship jury + 3-team dry-run review gate.

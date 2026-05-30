# Tasks — agents-md-session-preflight

**Proposal:** Constitutional Session Preflight — Auto-Triggering AGENTS.md Sync
**Spec:** PROPOSAL.md in this directory
**Scope:** Stage 0 (check-only) only — Stages 1–3 are in `agents-md-sync-hardening` proposal

Progress: 5 / 5 tasks complete ✓

---

## Task List

- [x] **TASK-1** — Add Section 0 Constitutional Preflight to `agent-skills/base/AGENT.md` ✓ `1aa1249`
  - Patched to check-only mode: `8c8b21f`
  - Spec: PROPOSAL.md § "Primary Trigger: Section 0 Constitutional Preflight in AGENT.md"
  - File: `agent-skills/base/AGENT.md`
  - Test scenario: `session-preflight-in-agent-md` — AGENT.md must contain a Section 0 block with NON-NEGOTIABLE framing, preflight steps, and fallback chain

- [x] **TASK-2** — Create `.githooks/post-merge` opt-in reference artifact ✓ `18a2251`
  - Spec: PROPOSAL.md § "Git Hook: Opt-In Accelerator Only"
  - File: `.githooks/post-merge` (chmod +x)
  - Note: hook runs `--check` only (not `--apply`) per Stage 0 policy
  - Test scenario: `post-merge-hook-runs-check` — hook script is executable, calls `aa-agents-sync --check` if installed, is silent on success (exit 0)

- [x] **TASK-3** — Migrate this repo's own AGENTS.md to versioned markers (manual) ✓ `8e7478b`
  - Spec: PROPOSAL.md Deliverable #3
  - File: `AGENTS.md` (constitution repo root)
  - ⚠️ Manual migration only — do NOT use `--apply` or auto-write path
  - Process: run `aa-agents-sync --legacy-mode --dry-run AGENTS.md` to generate diff,
    then manually apply the BEGIN/END markers around the 8-step protocol block
  - Test scenario: `constitution-agents-md-has-markers` — AGENTS.md must contain at
    least one valid BEGIN/END marker at current constitution version

- [x] **TASK-4** — Update `workflows/adoption.md` with aa-agents-sync and session preflight ✓ `79cf385`
  - Spec: PROPOSAL.md Deliverable #4
  - File: `workflows/adoption.md`
  - Test scenario: `adoption-workflow-references-sync` — adoption.md must reference
    aa-agents-sync install, A01 lint requirement, and session preflight

- [x] **TASK-5** — Create `docs/guides/adoption/sync-troubleshooting.md` ✓ (pending commit)
  - Spec: PROPOSAL.md Deliverable #5
  - File: `docs/guides/adoption/sync-troubleshooting.md`
  - Test scenario: `sync-troubleshooting-guide-exists` — guide must exist and cover:
    fallback behavior, manual install steps, Stage 0 check-only behavior

---

## Deferred to `agents-md-sync-hardening` Proposal

The following work is out of scope for this proposal (Stage 0). It is tracked in
`hangar-ai-specs/changes/agents-md-sync-hardening/`:

- 14 technical fixes (FIX-1 through FIX-14) — CRLF, BOM, downgrade guard, template
  parser errors, file locking, resolver integrity, etc.
- 10 integration tests (IT-1 through IT-10) — real-world file testing
- `agents-sync.yml` opt-out mechanism implementation
- `--apply` flag (inverted write default)
- `AGENTS_SYNC_DISABLED=1` kill switch
- Stages 1–3 rollout

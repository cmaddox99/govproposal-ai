# AGENTS.md Sync Troubleshooting

> **Related:** `workflows/adoption.md` § Step 3.4 · `agent-skills/base/AGENT.md` § Section 0  
> **Tool:** `aa-agents-sync` · **Lint rule:** A01

This guide covers what to do when `aa-agents-sync` reports drift, fails, or is not
installed — and explains the Stage 0 check-only behavior in detail.

---

## What Is Stage 0 (Check-Only) Behavior?

The current rollout stage is **Stage 0: check-only**. The tool and the agent session
preflight will:

- ✅ Detect whether `AGENTS.md` markers are current
- ✅ Tell you what command to run to preview or apply changes
- ❌ **Never write to your files automatically**
- ❌ **Never apply changes without explicit user approval**

This is intentional. The safety jury assessed the blast radius of automatic writes as
HIGH — a single bad write could corrupt `AGENTS.md` in every governed repo simultaneously.
See `hangar-ai-specs/changes/agents-md-session-preflight/safety-synthesis.md` for details.

Auto-write will be enabled in Stage 2, after 14 technical fixes and 10 integration tests
are complete. See `hangar-ai-specs/changes/agents-md-sync-hardening/PROPOSAL.md`.

---

## Quickstart: Common Commands

```bash
# Check if AGENTS.md is current (safe, read-only)
aa-agents-sync --check AGENTS.md

# Preview what would change (no writes)
aa-agents-sync --dry-run AGENTS.md

# Preview migration for a legacy AGENTS.md (no markers yet)
aa-agents-sync --legacy-mode --dry-run AGENTS.md

# Apply changes after reviewing the dry-run output
aa-agents-sync --apply AGENTS.md
```

Exit codes: `0` = current, `1` = error, `2` = drift detected (`--check`), `3` = synced

---

## Fallback Behavior

The session preflight (Section 0 of `agent-skills/base/AGENT.md`) handles each case:

| Situation | What the agent does |
|-----------|---------------------|
| `aa-agents-sync --check` exits 0 | Silently proceed — AGENTS.md is current |
| Exit 2 (drift detected) | Warn: "AGENTS.md is behind v{version}. Run `--dry-run` to preview, then `--apply` to sync." Wait for user approval. |
| Exit 1 (tool error) | Report error details. Do not proceed until resolved. |
| `aa-agents-sync` not installed | Fall back to inline version check (read marker vs `constitution-version.txt`). Warn if stale. |
| No markers in AGENTS.md (legacy) | Warn: "AGENTS.md has no version markers — legacy state. Run `aa-agents-sync --legacy-mode --dry-run AGENTS.md`." |
| `constitution-version.txt` missing | Cannot determine current version. Report and stop. |

---

## Installing aa-agents-sync

```bash
# Standard pip install
pip install aa-agents-sync

# Isolated install (recommended — avoids dependency conflicts)
pipx install aa-agents-sync

# Verify install
aa-agents-sync --version
```

### If install fails

```bash
# Ensure you're using Python 3.10+
python3 --version

# If behind a corporate proxy
pip install aa-agents-sync --trusted-host pypi.org --proxy http://your-proxy:port

# Install from the constitution repo directly (development)
pip install -e /path/to/hangar-ai-constitution/tools/agents-md-sync
```

---

## Diagnosing Drift

### "AGENTS.md is behind constitution vX.Y.Z"

The mandatory-protocol section in your AGENTS.md was authored against an older
constitution version. Preview and apply the update:

```bash
# Step 1: preview (required before applying)
aa-agents-sync --dry-run AGENTS.md

# Step 2: review the unified diff output carefully
# Step 3: apply only if the diff looks correct
aa-agents-sync --apply AGENTS.md
```

### "Cannot resolve constitution path"

The tool cannot find the constitution repo. Provide it explicitly:

```bash
# Option 1: environment variable (persistent for the session)
export HANGAR_CONSTITUTION_PATH=/path/to/hangar-ai-constitution
aa-agents-sync --check AGENTS.md

# Option 2: explicit flag
aa-agents-sync --check --constitution-path /path/to/hangar-ai-constitution AGENTS.md
```

Resolution order: CLI flag → `HANGAR_CONSTITUTION_PATH` env var → sibling directory
named `hangar-ai-constitution` → bundled fallback (may be stale).

### "AGENTS.md has no version markers" (legacy state)

Your AGENTS.md predates the versioned marker system. Run a legacy migration:

```bash
# Preview what markers would be added (legacy-mode is detect-only)
aa-agents-sync --legacy-mode --dry-run AGENTS.md

# Apply after reviewing (standard sync, not legacy-mode)
aa-agents-sync --apply AGENTS.md
```

Note: `--legacy-mode` is detect-only and requires `--dry-run`. The actual apply step
is a standard sync with `--apply`. The tool will wrap the existing 8-step mandatory
protocol block in BEGIN/END markers. All other content is preserved exactly.

### A01 lint failure in CI

If `aa-constitution-lint` reports an A01 failure:

```
A01 FAIL: AGENTS.md mandatory-protocol marker is v1.0.0 but constitution is v1.1.0
```

Run `aa-agents-sync --dry-run AGENTS.md`, review, then run `aa-agents-sync --apply AGENTS.md`.
Commit the updated `AGENTS.md`. The A01 rule requires markers to be at the current constitution version.

---

## Git Hook (Optional)

The `.githooks/post-merge` hook runs `--check` automatically after `git pull`.
It is **opt-in** — it does not activate until you configure it:

```bash
# Enable for this repo
git config core.hooksPath .githooks

# Disable
git config --unset core.hooksPath
```

The hook is check-only (Stage 0 policy) — it never writes.

---

## Known Limitations (Stage 0)

These are tracked in `hangar-ai-specs/changes/agents-md-sync-hardening/PROPOSAL.md`
and will be addressed before Stage 2 (auto-write with `--apply`):

| Limitation | Impact | Tracked as |
|-----------|--------|-----------|
| CRLF line endings (Windows-edited files) | Markers not recognized | FIX-2 |
| BOM-prefixed UTF-8 files | `^` anchor mismatch | FIX-3 |
| Malformed template errors silent | Bad template propagates | FIX-1 (CRITICAL) |
| No downgrade guard | Stale sibling constitution could silently downgrade | FIX-4 |
| No file locking | Race condition on concurrent agent sessions | FIX-8 |

Until these are fixed, always verify with `--check` after any sync operation.

---

## Getting Help

- Session preflight behavior: `agent-skills/base/AGENT.md` § Section 0
- Safety jury decisions: `hangar-ai-specs/changes/agents-md-session-preflight/safety-synthesis.md`
- Hardening roadmap: `hangar-ai-specs/changes/agents-md-sync-hardening/PROPOSAL.md`
- Adoption workflow: `workflows/adoption.md`

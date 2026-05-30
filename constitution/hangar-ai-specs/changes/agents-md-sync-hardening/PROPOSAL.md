---
id: agents-md-sync-hardening
title: AGENTS.md Sync Safety Hardening
status: in-progress
type: safety
laws: [ENG-4.1, ENG-6.1, ENG-6.7, ENG-11.1]
author: hangar-ai-constitution governance
date: "2026-05-28"
source: agents-md-session-preflight/safety-synthesis.md
depends-on: agents-md-session-preflight
---

# AGENTS.md Sync Safety Hardening

## Context

The `agents-md-drift-sync` tool (`aa-agents-sync`) ships with Stage 0 behavior: check-only,
no writes. Before auto-write is enabled (Stage 2), 14 technical fixes and 10 integration
tests must be implemented and verified.

This proposal is the gate for advancing from Stage 0 → Stage 1 → Stage 2. Stage 3
requires governance council approval and is out of scope here.

Full analysis: `hangar-ai-specs/changes/agents-md-session-preflight/safety-synthesis.md`

---

## Required Fixes (FIX-1 through FIX-14)

These are gating fixes — none may be skipped.

| ID | Priority | Description |
|----|----------|-------------|
| **FIX-1** | CRITICAL | `_load_canonical_sections()` must surface parser errors — malformed template must NOT silently propagate |
| **FIX-2** | CRITICAL | CRLF handling — `$` anchor in BEGIN_RE/END_RE doesn't match before `\r\n`; markers silently unrecognized on Windows-edited files |
| **FIX-3** | HIGH | BOM stripping — UTF-8 BOM at file start breaks `^` anchor match |
| **FIX-4** | HIGH | Downgrade guard — `section.version != constitution_version` is not monotonic; stale sibling constitution must be rejected |
| **FIX-5** | HIGH | Non-git repo guard — `is_git_dirty()` returns `None`; tool must not write when git status is unknown |
| **FIX-6** | HIGH | Pre-write backup — atomic write must create `.bak` before replace |
| **FIX-7** | HIGH | Post-write verification — re-parse file after write; auto-restore from backup on parser error |
| **FIX-8** | MEDIUM | File locking — parallel agent sessions can race on same file; use `fcntl.flock` or equivalent |
| **FIX-9** | MEDIUM | Resolver integrity check — resolved constitution path must contain expected marker IDs; wrong sibling silently injects bad content |
| **FIX-10** | MEDIUM | Version rollback detection — if incoming version < current marker version, abort with explicit error (not silent overwrite) |
| **FIX-11** | MEDIUM | Idempotency guard — track write hash; skip write if content would not change |
| **FIX-12** | MEDIUM | Invert write default — dry-run must be the default; `--apply` flag required for any file modification |
| **FIX-13** | LOW | `agents-sync.yml` opt-out config — structured YAML at repo root; supports time-boxed version pins |
| **FIX-14** | LOW | `AGENTS_SYNC_DISABLED=1` kill switch — env var must prevent any writes; check before executing any write path |

**Stage 1 gate (FIX-1–3):** Parser errors + CRLF + BOM only
**Stage 2 gate (all 14 fixes):** Full hardening complete

---

## Required Integration Tests (IT-1 through IT-10)

All integration tests use real files (not synthetic fixtures).

| ID | Stage Gate | Description |
|----|-----------|-------------|
| **IT-1** | Stage 1 | CRLF-terminated AGENTS.md — markers recognized correctly |
| **IT-2** | Stage 1 | BOM-prefixed AGENTS.md — BOM stripped before parse |
| **IT-3** | Stage 1 | Malformed template in constitution repo — error surfaces to caller |
| **IT-4** | Stage 1 | `--check` on real AGENTS.md (this repo) — exits 0 or 2, no crash |
| **IT-5** | Stage 1 | Non-git directory — tool exits with explicit error, no write |
| **IT-6** | Stage 1 | `--dry-run` output matches actual diff (unified diff format) |
| **IT-7** | Stage 2 | Stale sibling constitution (older version) — downgrade rejected |
| **IT-8** | Stage 2 | Race condition simulation — concurrent invocations; last write wins, no corruption |
| **IT-9** | Stage 2 | `--apply` with backup+verify — backup created, post-write re-parse succeeds |
| **IT-10** | Stage 2 | `AGENTS_SYNC_DISABLED=1` — no write attempted under any flag combination |

---

## Governance Controls (to implement)

These controls are required before Stage 2:

1. **`agents-sync.yml` opt-out** (FIX-13) — structured config at repo root
   ```yaml
   # agents-sync.yml
   enabled: true  # set to false to disable
   version-pin:
     section: mandatory-protocol
     pinned-version: "1.0.0"
     expires: "2026-09-01"  # must be time-boxed; governance approval required
     reason: "Migration in progress"
   ```

2. **`--apply` flag** (FIX-12) — inverts current default
   - `aa-agents-sync AGENTS.md` → dry-run (shows diff, no write)
   - `aa-agents-sync --apply AGENTS.md` → writes
   - AGENT.md Section 0 updated only when Stage 2 gate is met

3. **`AGENTS_SYNC_DISABLED=1` kill switch** (FIX-14)
   - Checked in `cli.py` before any I/O
   - Logged to audit trail when triggered

---

## Staged Rollout Gate Criteria

See `agents-md-session-preflight/safety-synthesis.md` § "Staged Rollout" for full criteria.

| Stage | Required |
|-------|---------|
| Stage 1 | FIX-1, FIX-2, FIX-3, IT-1–IT-6 |
| Stage 2 | All 14 fixes + IT-1–IT-10 + 3 teams reviewed dry-run output |
| Stage 3 | 12 weeks clean at Stage 2 + governance council approval + canary repo |

---

## Non-Goals

- Auto-migration of all governed repos at once (blast radius too high)
- Removing manual `--apply` flag after Stage 3 (remains as explicit opt-in permanently)
- Bypassing governance council for Stage 3 gate

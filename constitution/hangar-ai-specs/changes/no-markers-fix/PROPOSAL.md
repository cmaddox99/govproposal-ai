---
id: no-markers-fix
title: aa-agents-sync No-Markers State Correctness
status: in-progress
type: bug-fix
laws: [ENG-4.1, ENG-6.7, ENG-1.2]
author: hangar-ai-constitution governance
date: "2026-05-28"
depends-on: agents-md-sync-hardening
---

# aa-agents-sync No-Markers State Correctness

## Context

`aa-agents-sync` silently misreports AGENTS.md files that contain **no**
`<!-- BEGIN hangar-ai-constitution:... -->` markers as "current". This is
caused by `any([]) == False` in `checker.py` — an empty sections list looks
identical to a fully-current file.

Exposed by real-world usage: an Android repo's AGENTS.md (compact inline
`Mandatory Protocol (ENG-4.1):` reference) had no markers. `--check` exited 0;
`--apply` said "already current". `--legacy-mode --dry-run` exited 2 with no
actionable path forward. The developer was completely stuck.

**Design jury:** 5-juror jury returned APPROVED after resolving the auto-insert
vs. warn-and-error tension (4-of-5: auto-insert at EOF is safe given existing
backup/restore guards).

---

## Bugs Fixed

| ID | Command | Current (wrong) | Correct |
|----|---------|-----------------|---------|
| **NM-BUG-1** | `--apply` (no markers) | Exit 0 "OK: already current" | Exit 3 "SYNCED: Inserted N section(s)" |
| **NM-BUG-2** | `--legacy-mode --apply` | Exit 1 "requires --dry-run" | **Stays blocked** (deferred) |
| **NM-BUG-3** | `--legacy-mode --dry-run` (not found) | Exit 2, unhelpful WARN | Exit 2 + template path + `--apply` hint |
| **NM-BUG-4** | `--check` (no markers) | Exit 0 "OK: current" | Exit 2 "MISSING: no markers" |

---

## Root Cause

In `tools/agents-md-sync/aa_agents_sync/checker.py`:

```python
# BEFORE (the bug):
has_drift = any(s.version != constitution_version for s in sections)
# any([]) == False → empty sections list appears current

# AFTER:
has_drift = (not sections) or any(s.version != constitution_version for s in sections)
```

---

## Model Changes

`CheckResult` gains a `has_markers: bool` field:
- `True` when `parse_markers()` returns at least one section
- `False` when sections list is empty (no markers in file)

This enables the syncer to route no-markers files to the **insertion path**
rather than the replacement path.

---

## New Capability: Canonical Section Insertion

When `has_markers=False` and `--apply` is requested:
1. Load canonical sections from `templates/agents-md-sections/*.md`
2. Append each canonical section to the file (with trailing newline separator)
3. Atomic write with existing backup/restore guards (FIX-6/FIX-7)
4. Re-parse to verify markers present after write
5. Exit 3 (SYNCED)

The dry-run path shows a diff of what would be appended.

---

## What Is NOT Changed

- `--legacy-mode --apply` remains blocked (separate proposal when legacy
  detection is hardened to handle compact/custom patterns)
- A01 lint rule remains WARNING (not FAIL) for no-markers — migration window
  still open for brownfield repos
- Exit code contract (0/1/2/3) unchanged in meaning

---

## Required Tasks (NM-1 through NM-12)

All tasks follow ENG-4.1 Atomic TDD: one test per cycle.

| ID | Scenario ID | Description |
|----|-------------|-------------|
| **NM-1** | `nm-chk-01` | `check_drift()` returns `has_drift=True` for no-markers AGENTS.md |
| **NM-2** | `nm-chk-02` | `CheckResult` has `has_markers: bool` field |
| **NM-3** | `nm-chk-03` | `check_drift()` sets `has_markers=False` when no sections found |
| **NM-4** | `nm-chk-04` | `check_drift()` sets `has_markers=True` when sections exist |
| **NM-5** | `nm-cli-01` | `--check AGENTS.md` (no markers) exits 2 |
| **NM-6** | `nm-cli-02` | `--check AGENTS.md` (no markers) prints `MISSING:` prefix |
| **NM-7** | `nm-syn-01` | `sync_agents_md()` inserts canonical sections when `has_markers=False` |
| **NM-8** | `nm-syn-02` | Existing content preserved above inserted sections |
| **NM-9** | `nm-cli-03` | `--apply AGENTS.md` (no markers) exits 3 |
| **NM-10** | `nm-cli-04` | `--apply AGENTS.md` (no markers) prints `Inserted N canonical section(s)` |
| **NM-11** | `nm-dry-01` | `--dry-run` with no markers shows insertion diff, exits 0 |
| **NM-12** | `nm-leg-01` | `--legacy-mode --dry-run` (not found) message includes template path + `--apply` hint |

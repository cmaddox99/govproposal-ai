---
id: doc-cli-consistency
title: Doc↔CLI Consistency — Canonical Commands Reference
status: stub
type: tooling
laws: [ENG-6.7, ENG-10.1, ENG-1.2]
author: hangar-ai-constitution governance
date: "2026-05-28"
---

# Doc↔CLI Consistency — Canonical Commands Reference

## Problem

Every `aa-agents-sync` behavior change has an invisible blast radius across
manually-duplicated command examples in prose docs:

- `sync-troubleshooting.md`
- `workflows/adoption.md`
- `agent-skills/base/AGENT.md`
- A01 lint rule warning messages
- PROPOSAL.md files and other spec docs

When CLI flags change (e.g., FIX-12 `--apply`, NM fixes), all these
duplicates must be manually hunted. No automated gate catches a stale
`--legacy-mode --dry-run` in a warning message. Juries catch stragglers
reactively — only within whatever scope is defined.

Every "minor doc fix" after a ship is the same structural failure repeating.

## Root Cause

**Docs are agentic code.** A stale command example in AGENT.md is a
runtime bug — an agent will execute the wrong command. There is no
lint gate that validates prose command examples against actual CLI behavior.

## Proposed Solution (to be designed)

Two complementary approaches:

### Approach A — Canonical Commands Reference
A single source of truth file (e.g., `docs/reference/aa-agents-sync-commands.md`)
that all other docs **link to rather than duplicate**. When CLI changes,
one file changes. All other docs reference it.

### Approach B — Doc Lint Rule (A02 or new tool)
A lint rule that:
1. Extracts the actual CLI help text (`aa-agents-sync --help`)
2. Scans prose docs for code blocks containing `aa-agents-sync` commands
3. FAILs if a flag used in docs does not exist in the CLI help

This is the same principle as `aa-agents-sync --check` for marker versions —
but for command syntax.

### Approach C — Both
Canonical reference file + lint rule that validates the reference file
itself against the CLI, and all other docs link to the reference.

## What Is NOT in Scope Here

- Linting command correctness in arbitrary free-form prose (too hard)
- Replacing all prose examples with auto-generated output (too fragile)
- Fixing the A01 warning message straggler from NM-12 (do that now, separately)

## Known Stragglers (as of 2026-05-28)

- [x] A01 lint rule warning message still says `--legacy-mode --dry-run`
      **Fixed in MF-02** (`6422d1e`) — now says `--apply AGENTS.md`.

## Deferred Issues (R5–R10) — Jury findings, not yet implemented

These were surfaced by the 5-juror review jury (2026-05-28) that produced R1–R4.
Each is captured here pending a design session when this proposal is activated.

### R5 — `_write_version_pin` non-atomic write (Medium)

**File**: `tools/agents-md-sync/aa_agents_sync/syncer.py`

`_write_version_pin` uses `path.write_text()` directly. If the process dies
mid-write (SIGKILL, disk-full after partial write), the pin file is corrupt or
truncated. A01 will then fail with an unreadable version string.

**Fix**: Replace `write_text` with the existing `_atomic_write` helper (write to
a temp file, then `os.replace`). This is already used for AGENTS.md writes.

**Risk if deferred**: Low probability but non-zero data corruption on CI runners
under memory pressure.

---

### R6 — Dead A01 SKIP branch in lint rule (Medium)

**File**: `tools/constitution-lint/src/aa_constitution_lint/domain/rules/agents_md_sync.py`

The code path `constitution_version is None AND not sections → SKIP` is unreachable.
The `if not sections: return [WARNING]` guard fires first, so the version check
only runs when markers ARE present. There is no state where "no markers + no
version source" reaches the SKIP path.

**Fix**: Remove the dead branch; add a comment explaining the guard order.

**Risk if deferred**: No runtime impact. Misleading dead code could confuse future
maintainers reading the rule logic.

---

### R7 — Wrong env var name in error message (Medium)

**File**: `tools/constitution-lint/src/aa_constitution_lint/cli.py` (approx. line 128)

When `AA_CONSTITUTION_PATH` is set to a non-existent path, the error message
may reference `HANGAR_CONSTITUTION_PATH` (old name) instead of the current
`AA_CONSTITUTION_PATH`. Agents reading the error will set the wrong env var
and remain stuck.

**Fix**: Audit all error/warning messages in the lint CLI for env var name
accuracy. Add a regression test asserting the correct name appears.

**Risk if deferred**: Agents in CI environments with bad paths will get incorrect
remediation instructions.

---

### R8 — `--dry-run` does not preview pin file side effect (Low)

**File**: `tools/agents-md-sync/aa_agents_sync/cli.py`

`--dry-run` reports which sections are stale but does not mention that
`--apply` will also write `constitution-version.txt`. An agent reviewing
dry-run output does not know a new untracked file will appear. This causes
R1-style "surprise commit" for the pin file even after looking at the preview.

**Fix**: When `--dry-run` detects drift (or detects pin missing), add a line:
`  [DRY-RUN] Would write: constitution-version.txt`.

**Risk if deferred**: Low; agents learn about the pin file from R1 messaging
at apply time. But dry-run output is misleading.

---

### R9 — `--check --apply` silently ignores `--apply` (Low)

**File**: `tools/agents-md-sync/aa_agents_sync/cli.py`

Passing both `--check` and `--apply` together does not error out. `--apply`
is silently ignored when `--check` is present. An agent constructing flags
programmatically might combine both, expecting apply behavior, and get
check-only behavior with no warning.

**Fix**: Validate that `--check` and `--apply` are mutually exclusive;
emit an error and exit non-zero if both are provided.

**Risk if deferred**: Low; mostly a DX concern. No correctness risk in normal
usage.

---

### R10 — `--dry-run` overcounts sections in output (Low)

**File**: `tools/agents-md-sync/aa_agents_sync/cli.py`

`--dry-run` reports ALL sections found in AGENTS.md (e.g., "3 sections"),
not just the stale ones. When 1 of 3 sections is drifted, the output implies
all 3 would be updated, misleading agents about the scope of `--apply`.

**Fix**: Count and report only stale sections in dry-run output:
`Would update 1 of 3 sections (mandatory-protocol)`.

**Risk if deferred**: Low; cosmetic confusion only.

---

## Next Steps (when this proposal is activated)

1. Design jury to choose between Approach A, B, or C for the canonical
   commands reference
2. Resolve R5–R10 items above (ordered by risk: R5 → R7 → R6 → R8 → R9 → R10)
3. Identify all prose locations that embed `aa-agents-sync` commands
4. Implement chosen approach under ENG-4.1 TDD cycle
5. Add to adoption Phase 3 checklist

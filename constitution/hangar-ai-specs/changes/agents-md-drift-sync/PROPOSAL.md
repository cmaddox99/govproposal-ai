---
id: agents-md-drift-sync
title: AGENTS.md Drift Prevention and Sync Architecture
status: proposed
type: architecture
laws: [ENG-1.2, ENG-10.1, ENG-11.1]
author: hangar-ai-constitution governance
date: "2026-05-27"
---

# AGENTS.md Drift Prevention and Sync Architecture

## Problem Statement

When a repo adopts the hangar-ai-constitution, it creates a local `AGENTS.md` from
a template. That file **embeds** canonical protocol content (the 8-step Mandatory
Agent Protocol, the Phase Gate Sub-Protocol, tool install paths, etc.).

When the constitution evolves — as it did today with 7 correctness fixes (C1–C7) —
every existing adopting repo silently drifts. The adopter may have adopted this
morning and already be out of step.

There is currently no mechanism to detect or repair this drift.

## Constraint (User-Specified)

> "The fix needs to apply to all current repos with constitutional adoption
> (AGENTS.md etc) the next time a user does a constitutional git pull and
> begins constitutional work in it."

"Constitutional git pull and begins constitutional work" = the adoption workflow
check phase, which already runs conditionally **at the start of every other
Hangar AI workflow**. This is the primary trigger.

**Trigger enforcement (C4):** The adoption workflow trigger is an AI-agent
convention. To harden it into a guarantee, `aa-constitution-lint` check A01
will be a **required CI check** (FAIL, not WARN) in adopting repos once markers
are present. Additionally, `aa-agents-sync --check` (dry-run drift detection)
is suitable for pre-commit hooks. These hard gates ensure drift is caught even
when the AI workflow is not explicitly invoked.

## Proposed Architecture: Option A — Versioned Sections + Sync Tool

### Marker Syntax Contract (C5)

Markers use the following exact regex patterns:

```
BEGIN: ^<!-- BEGIN hangar-ai-constitution:([a-z][a-z0-9-]+) v(\d+\.\d+\.\d+) -->$
END:   ^<!-- END hangar-ai-constitution:([a-z][a-z0-9-]+) -->$
```

Valid section name enum (MVP — see Canonical Sections below):
- `mandatory-protocol`

Rules:
- Section names must match the enum exactly (unrecognized names → error)
- BEGIN without matching END → error, abort
- END section name MUST match the BEGIN section name (mismatch → error, abort)
- Nested markers are not permitted
- A file may contain multiple non-overlapping sections

### `constitution-version.txt` Policy (C6)

- Located at the constitution repo root
- Semver format: `MAJOR.MINOR.PATCH`
- Bump policy: **CI-enforced** — any change to a file under `templates/agents-md-sections/` triggers an automated semver patch bump via CI job; minor bumps on new sections added; major bumps on breaking section renames
- `aa-agents-sync` reads this file as the source of truth for "current version"
- Adopting repos pin the version in their markers; drift = marker version < `constitution-version.txt`

### Core Mechanism

Canonical sections in project AGENTS.md are bounded by version markers:

```markdown
<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.5.0 -->
... 8-step cycle, Phase Gate Sub-Protocol, install paths ...
<!-- END hangar-ai-constitution:mandatory-protocol -->
```

The constitution publishes:
- A `constitution-version.txt` at repo root (e.g. `1.5.0`)
- A `templates/agents-md-sections/` directory containing the canonical embeddable blocks

### New Tool: `aa-agents-sync`

Located at `tools/agents-md-sync/`.

```
aa-agents-sync <project-agents-md-path> [--constitution-path <path>] [--dry-run] [--force] [--check] [--legacy-mode]
```

**Constitution path resolution order (C2):**
1. `--constitution-path <path>` (explicit)
2. `HANGAR_CONSTITUTION_PATH` environment variable
3. Sibling directory named `hangar-ai-constitution` relative to the project root
4. Installed package data (if `aa-constitution-lint` is pip-installed)
5. Fail with actionable error: "Cannot locate constitution. Set HANGAR_CONSTITUTION_PATH or pass --constitution-path."

**Modes:**
- `--check` — report drift without writing (exit 0 = current, exit 2 = drift detected, exit 1 = error). Suitable for CI and pre-commit hooks.
- `--dry-run` — print a unified diff of what would change; do not write
- `--force` — write even if git working tree is dirty (default: refuse if dirty). Does NOT bypass legacy-mode ambiguity safeguard; use `--force-legacy-ambiguous` for that.
- `--legacy-mode` — detect and migrate legacy AGENTS.md (no markers). **Requires `--dry-run` to be passed; CLI refuses if `--dry-run` is absent** (exit 1 with error: "Legacy mode requires --dry-run to be passed explicitly. Review the diff before writing.")
- default (no flags) — safe mode: refuse if working tree is dirty; write and report changes

**Behaviour (safe mode):**
1. Resolve constitution path (order above)
2. Read `constitution-version.txt`
3. Check git working tree of project AGENTS.md — **refuse if dirty** (uncommitted changes); instruct user to commit or stash first
4. Scan project AGENTS.md for `<!-- BEGIN hangar-ai-constitution:* -->` markers (per syntax contract above)
5. For each bounded section, diff content against canonical block
6. If changes exist: write atomically (write temp file → fsync → rename over original)
7. Report: sections checked, sections updated, old version → new version
8. Exit codes: 0 = already current (no-op); 3 = changes written successfully; 1 = error
   - `--check` mode: 0 = current, 2 = drift detected, 1 = error
   - `--legacy-mode` (detection only): 0 = pattern found+written, 2 = pattern not detected, 1 = error

**Same-session visibility (C — J5-B4):**
`aa-agents-sync` modifies the AGENTS.md file on disk. The running agent's context
window already loaded the old content. Updated content takes effect in the **next
agent session** after the file is written. The adoption workflow must instruct the
agent to inform the user: "AGENTS.md has been updated — please start a new session
to ensure the agent operates with current protocol."

### aa-constitution-lint: New Check A01

```
A01  AGENTS.md sections match current constitution version
     FAIL: any bounded section version < current constitution-version.txt
     FAIL: markers present but section name not in valid enum
     WARN: no markers present (legacy — prompts user to run aa-agents-sync --legacy-mode)
     PASS: all bounded sections current
```

A01 is a **required CI check** (FAIL blocks merge) once any markers are present.
For repos with no markers, A01 emits WARN only until `--legacy-mode` migration
is run. A01 WARN becomes FAIL after constitution version `2.0.0` (sunset date).

### Adoption Workflow Integration (the "next git pull" trigger)

The adoption workflow Phase 1 Check already tests for stale AGENTS.md state:

| Existing condition | Action |
|---|---|
| AGENTS.md references old brownfield guide | Update |
| AGENTS.md missing avatar | Update |

**Add new conditions:**

| New condition | Action |
|---|---|
| AGENTS.md has stale version markers (A01 FAIL) | Run `aa-agents-sync --dry-run` to show diff; confirm with user; then run `aa-agents-sync`; commit; re-verify |
| AGENTS.md has no version markers (legacy) | Run `aa-agents-sync --legacy-mode --dry-run`; confirm with user; then run `aa-agents-sync --legacy-mode`; commit; re-verify |

**User confirmation is required before writing (C1/C3).** The adoption workflow
must present the dry-run diff and ask the user to confirm before `aa-agents-sync`
writes. After sync, the workflow must instruct the user to **start a new agent
session** before continuing constitutional work (same-session refresh gap).

If `aa-agents-sync` exits 1 (error): Phase 2 halts; report error to user; do not proceed.

### Canonical Sections — MVP Scope (C7)

**MVP ships ONE section only:**

| Section name | Content |
|---|---|
| `mandatory-protocol` | The 8-step Mandatory Agent Protocol box |

All other sections are **deferred to v1.1** after MVP proves out the mechanism:

| Section (deferred) | Notes |
|---|---|
| `phase-gate-subprotocol` | High value; deferred to reduce first-ship blast radius |
| `prohibited-actions` | Deferred |
| `non-negotiable-laws` | Deferred |
| `self-check-protocol` | Added per J2-N5; deferred |
| `tool-install-paths` | Advisory only — paths vary by constitution deployment model; may never be auto-synced |

Project-specific content (authority hierarchy, project name, domain, stack,
project-rules.md extensions) lives OUTSIDE the markers and is never touched
by `aa-agents-sync`.

### What Is NOT Bounded (never auto-synced)

- Authority hierarchy declaration (project-specific)
- Project name, domain, stack
- Custom workflow sections added by the project
- `project-rules.md` reference

### Migration Path for Existing Repos (C3)

**Legacy mode** (`aa-agents-sync --legacy-mode`):

Detection uses exact string anchors (not fuzzy patterns):
- Looks for the literal string `MANDATORY AGENT PROTOCOL (Per ENG-4.1` inside a fenced code block
- If found with high confidence (exact anchor present): wraps with markers, replaces with canonical version
- If not found: reports "Legacy pattern not detected — manual marker insertion required" and exits 2
- If partial match (anchor found but surrounding structure ambiguous): reports warning, requests `--force` to proceed, defaults to exit 2

**Never silently overwrites.** `--legacy-mode` requires `--dry-run` to be passed explicitly — the CLI tool enforces this and exits 1 if `--dry-run` is absent.

For repos that have never adopted (no AGENTS.md):
- No change — full adoption workflow creates a fresh AGENTS.md with markers

## Deliverables

1. `constitution-version.txt` — version file at constitution repo root
2. `templates/agents-md-sections/` — canonical embeddable section files
3. `tools/agents-md-sync/` — `aa-agents-sync` CLI tool
4. `aa-constitution-lint` check A01 — version marker freshness
5. `workflows/adoption.md` Phase 1 — add stale-section detection
6. `workflows/adoption.md` Phase 2 — add `aa-agents-sync` repair step
7. `docs/guides/adoption/how-to-adopt-constitution.md` — update AGENTS.md template to include markers

## Laws

- ENG-1.2: AGENTS.md required and must be current
- ENG-10.1: Law references must be valid
- ENG-11.1: hangar-ai-specs/ required — change tracked here per SDD

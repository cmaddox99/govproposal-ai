---
id: agents-md-session-preflight
title: Constitutional Session Preflight — Auto-Triggering AGENTS.md Sync
status: shipped
type: architecture
laws: [ENG-1.2, ENG-10.1, ENG-11.1]
author: hangar-ai-constitution governance
date: "2026-05-27"
jury: 5/5 deliberated (J1=claude-opus-4.6, J2=claude-sonnet-4.6, J3=gpt-5.4, J4=gpt-5.2, J5=gpt-5.4-mini; synthesizer=claude-opus-4.5)
safety-jury: 5/5 deliberated — blast radius HIGH, check-only confirmed correct; see safety-synthesis.md
---

# Constitutional Session Preflight — Auto-Triggering AGENTS.md Sync

## Problem Statement

`aa-agents-sync` was shipped (PR #82) as the mechanism to detect and repair stale
AGENTS.md versioned markers. However, it requires **manual invocation** — nobody
will type `aa-agents-sync` unprompted. Every adopting repo is silently running with
stale AGENTS.md files, including repos that adopted the constitution today.

The drift-sync tooling solves the repair problem; this proposal solves the
**trigger problem**.

## User Requirement

> "The fix needs to apply to all current repos with constitutional adoption
> (AGENTS.md etc) the next time a user does a constitutional git pull and
> begins constitutional work in it."
>
> "Anytime I do work aided by an agent referring to the constitution for the
> first time in a session, the adoption workflow quickly runs."

The moment of "begins constitutional work" is precisely when the AI agent reads
`AGENTS.md` at session start. This is the trigger point.

## Jury Deliberation Summary

A PRD-2.6 design jury of 5 jurors deliberated on 6 trigger options (A through F).
Unanimous consensus: **agent-native preflight is the correct primary trigger.**

**Decisive insight (J2, upheld by synthesizer):** The AI agent is the **only
infrastructure guaranteed present in every adopting repo**. A single change to
`agent-skills/base/AGENT.md` propagates to ALL existing stale repos at the next
session start — no manual action, no per-repo setup, no git hook configuration.

Git hooks (Option B) require manual `git config core.hooksPath` per repo and
**cannot retroactively reach existing repos** — they are opt-in accelerators, not
primary triggers.

## Proposed Architecture: Option A/F Hybrid

### Primary Trigger: Section 0 Constitutional Preflight in AGENT.md

Add a new **Section 0** to `agent-skills/base/AGENT.md` that executes before any
other action at every session start:

```
Section 0: Constitutional Preflight (NON-NEGOTIABLE)
1. Read constitution-version.txt (source of truth)
2. Read version from AGENTS.md marker (if present)
3. Compare versions:
   - Match → proceed immediately
   - Mismatch or marker absent → enter repair flow
4. Repair flow (CHECK-ONLY — see Staged Rollout below):
   a. Run: aa-agents-sync --check AGENTS.md
   b. If drift detected: report to user, suggest aa-agents-sync --dry-run AGENTS.md
   c. Do NOT auto-write without explicit user approval (Stage 0 policy)
5. Log preflight result before proceeding to user request
```

The AGENTS.md markers are **self-describing** (Option F insight): the AI reads the
file, the file carries its own version, and the AI can detect staleness inline
without any external tooling. The CLI tool is the preferred repair mechanism but
is not required for detection.

### Fallback Chain (Stage 0 — Check Only)

```
Session Start
    │
    ▼
Run: aa-agents-sync --check AGENTS.md
    │
    ├─ Exit 0 (current) ──→ PROCEED
    │
    ├─ Exit 2 (drift) ──→ WARN user
    │                      "Run: aa-agents-sync --dry-run AGENTS.md to preview"
    │                      Wait for explicit user approval before any write
    │
    └─ Exit 1 (error) ──→ Report error, do not proceed
    
    If aa-agents-sync not installed:
    ├─ Markers present → compare versions inline, WARN if stale
    └─ No markers → WARN legacy state, suggest --legacy-mode --dry-run
```

### Handling Existing Stale Repos

The agent-native approach is the only mechanism that reaches existing repos:
- One commit to `agent-skills/base/AGENT.md`
- All adopting repos get the preflight at their next session start
- No human action required in any adopting repo
- 100% coverage of AI-assisted workflows

### Git Hook: Opt-In Accelerator Only

Ship `.githooks/post-merge` as a reference artifact for teams running human-only
workflows (no AI agent). This is NOT load-bearing — it cannot reach existing repos
without manual `git config core.hooksPath .githooks` per repo. Document it in the
adoption runbook as an optional enhancement.

```bash
#!/usr/bin/env bash
# Optional accelerator: runs check after git pull.
# Install: git config core.hooksPath .githooks
command -v aa-agents-sync &>/dev/null && aa-agents-sync --check "$PWD/AGENTS.md"
```

## Deliverables

| # | File | Change |
|---|------|--------|
| 1 | `agent-skills/base/AGENT.md` | Add Section 0: Constitutional Preflight (NON-NEGOTIABLE block) |
| 2 | `.githooks/post-merge` | Create opt-in git hook reference artifact (chmod +x) |
| 3 | `AGENTS.md` (this repo) | Manual migration to versioned markers (human-reviewed, NOT via auto-apply) |
| 4 | `workflows/adoption.md` | Document `aa-agents-sync` install + A01 lint requirement + session preflight |
| 5 | `docs/guides/adoption/sync-troubleshooting.md` | Fallback behavior, manual install, HARD STOP resolution |

## Exit Codes Propagated from aa-agents-sync

| Code | Meaning | Preflight action |
|------|---------|-----------------|
| 0 | Current / just synced | Proceed |
| 1 | Error (syntax, missing file) | Report error, HARD STOP |
| 2 | Drift detected (--check mode) | Run repair |
| 3 | Sync completed (sections updated) | Report "synced to vX.Y.Z", proceed |

## Staged Rollout (Safety Jury Decision)

A constitutional safety jury (5 jurors + synthesizer, 2026-05-28) assessed the blast
radius of automatic writes as **HIGH**. See `safety-synthesis.md` for full analysis.

**This proposal ships Stage 0 only.** Stages 1–3 are gated behind a separate safety
hardening proposal (`agents-md-sync-hardening`).

| Stage | Behavior | Gate Criteria |
|-------|----------|---------------|
| **0 (this proposal)** | Check-only — detect drift, report, user decides | ✅ Live |
| **1** | Show dry-run diff automatically, no write | FIX-1–3 (template parser, CRLF, BOM) + IT-1–IT-6 passing |
| **2** | Write with explicit `--apply` flag | All 14 fixes + IT-1–IT-10 + 3 teams reviewed dry-run |
| **3** | Fully automatic | 12 weeks clean at Stage 2 + governance council approval + canary repo |

## Governance Controls (Safety Jury Decisions)

These are architectural decisions ratified by the safety jury and enforced from Stage 1+:

| Control | Decision |
|---------|---------|
| **Opt-out mechanism** | `agents-sync.yml` at repo root — structured config, supports time-boxed version pins with governance approval required |
| **Write default** | Dry-run is the default; `--apply` flag required for any file modification |
| **Emergency kill switch** | `AGENTS_SYNC_DISABLED=1` environment variable — instant, no commit needed |
| **Audit trail** | Per ENG-6.7: git commit hash + governance event on every write |
| **Version pinning** | Allowed only with time-boxed expiry + governance approval |
| **Write rate limiting** | Once per constitution version per repo (idempotent) |

## Non-Goals

- This proposal does NOT change the `aa-agents-sync` CLI behavior
- This proposal does NOT make git hooks mandatory (they remain opt-in)
- This proposal does NOT add GitHub Actions enforcement (A01 lint already covers CI)
- This proposal does NOT version additional AGENTS.md sections (separate proposal)

## Constitutional Compliance

- **ENG-1.2** (AGENTS.md required and current): Preflight enforces this at the
  exact moment it matters — before any constitutional work begins
- **ENG-4.1** (Atomic TDD): All implementation follows RED-GREEN-REFACTOR
- **ENG-11.1** (Hangar SDD): This PROPOSAL.md is the spec; tasks.md drives TDD cycles
- **ENG-12.1** (Phase gates): Build→Ship jury required before merging

## Progress Log

| Date | Event |
|------|-------|
| 2026-05-27 | Proposal scaffolded; design jury 5/5 unanimous on agent-native preflight |
| 2026-05-27 | TASK-1: Section 0 added to AGENT.md — originally with auto-write |
| 2026-05-28 | **Safety jury convened** — blast radius HIGH; auto-write patched out; check-only confirmed safe |
| 2026-05-28 | TASK-1 patched to check-only mode `8c8b21f`; safety-synthesis.md authored (497 lines) |
| 2026-05-28 | PROPOSAL.md + tasks.md updated with 4-stage rollout and governance controls `1468f58` |
| 2026-05-28 | `agents-md-sync-hardening` proposal scaffolded (backlog) with FIX-1–14 + IT-1–10 |
| 2026-05-28 | TASK-2: `.githooks/post-merge` (check-only) `18a2251` |
| 2026-05-28 | TASK-3: AGENTS.md manually migrated to versioned markers `8e7478b` |
| 2026-05-28 | TASK-4: workflows/adoption.md updated with sync docs `79cf385` |
| 2026-05-28 | TASK-5: sync-troubleshooting.md created `3dc179c` |
| 2026-05-28 | Build→Ship jury: 3 APPROVED / 2 CHALLENGED; synthesizer APPROVED; aa-jury-gate 16/16 PASS |
| 2026-05-28 | Pre-ship fixes: PS-1 (hook exit 0), PS-2 (TASK-2 test label) `ea756f3` |
| 2026-05-28 | **SHIPPED** — pushed to origin/main; human approved phase advance |

## Tasks

See `tasks.md` in this directory. All 5 tasks complete — proposal shipped.

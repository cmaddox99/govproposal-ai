---
schema_version: 1
proposal_id: agents-md-session-preflight
phase_gate: build-to-ship
verdict: APPROVED
jurors:
  - id: J1
    model: claude-opus-4.6
    verdict: APPROVED
  - id: J2
    model: claude-sonnet-4.6
    verdict: APPROVED
  - id: J3
    model: gpt-5.4
    verdict: CHALLENGED
  - id: J4
    model: gpt-5.2
    verdict: APPROVED
  - id: J5
    model: gpt-5.4-mini
    verdict: CHALLENGED
juror_count: 5
synthesizer: claude-opus-4.5
rounds:
  r1_completed: true
  r2_completed: true
---

# Jury Synthesis — agents-md-session-preflight Build→Ship Gate

## R1 Jury Deliberation

### J1 (claude-opus-4.6) — APPROVED

J1 affirms that Stage 0 correctly solves the **trigger problem** (the core user requirement). The insight that agent-native preflight retroactively reaches all repos with zero human action is the decisive architectural advantage. J1 notes check-only is the correct posture for Stage 0 given the safety jury's blast-radius assessment. Non-blocking concerns about `constitution-version.txt` discoverability in adopting repos and reliance on user discipline are acknowledged but appropriate for Stage 0, with A01 CI lint providing the real enforcement backstop.

### J2 (claude-sonnet-4.6) — APPROVED

J2 validates all deliverables as technically sound with three non-blocking issues. **NB-1** (most significant): `.githooks/post-merge` propagates exit code 2 on drift, causing git to report the hook as "failed" — confusing UX that should be fixed by appending `; exit 0`. **NB-2**: Test grouping label mismatch (TASK-2 test under TASK-3 section) creates a traceability gap. **NB-3**: Section 0.1's manual fallback lacks guidance for governed project repos where `constitution-version.txt` doesn't exist locally. **S-1**: Exit code 3 ("synced") is absent from Section 0 documentation, which is correct (check mode never returns 3) but undocumented.

### J3 (gpt-5.4) — CHALLENGED

J3 raises two blocking challenges. **C-1**: Stage 0 doesn't satisfy the user requirement because it's "detection-only, not a completed sync loop." **C-2**: Teams without `aa-agents-sync` installed have no guaranteed completion path — warning-and-proceed is "too soft." Non-blocking concerns: discoverability weak at warning moment (no troubleshooting doc reference), stage numbering inconsistency between PROPOSAL.md ("Stage 0") and safety-synthesis.md ("Stage 1 CURRENT").

### J4 (gpt-5.2) — APPROVED

J4 emphasizes that Stage 0's blast radius is zero (read-only) and worst-case impact is user annoyance, not repo damage. The 4-stage rollout is a sound risk ladder. Non-blocking recommendations: make preflight skippable/quiet in appropriate contexts, confirm preflight never prints sensitive file contents, document hook uninstall procedure, and manage false positive UX.

### J5 (gpt-5.4-mini) — CHALLENGED

J5 raises one blocking challenge. **C-1**: The drift warning doesn't give users a complete remediation path (preview → apply sequence is unclear). Non-blocking: terminology is overloaded (Stage 0/check-only/preflight/drift/markers creates confusion), and AGENTS.md marker format is fragile to user editing.

## R2 Corrections Applied

**No blocking corrections required.** The J3/J5 challenges are resolved as scope misalignment (see Synthesis below). The following **pre-ship minor fixes** are required:

| ID | Fix | Owner | Rationale |
|----|-----|-------|-----------|
| PS-1 | Append `; exit 0` to `.githooks/post-merge` | Pre-ship | J2-NB-1: Git reports exit 2 as hook failure. Hook should report drift via stdout but exit 0 so git doesn't show scary error. |
| PS-2 | Fix test section label (TASK-2 under TASK-3) | Pre-ship | J2-NB-2: Traceability gap. Minor comment fix. |

**Post-ship backlog** (Stage 1 hardening):

| ID | Fix | Owner | Rationale |
|----|-----|-------|-----------|
| BL-1 | Add `$HANGAR_CONSTITUTION_PATH` reference to Section 0.1 | Stage 1 | J2-NB-3: Fallback ambiguous for governed repos without local constitution-version.txt |
| BL-2 | Add troubleshooting doc reference to warning text | Stage 1 | J3-NB: Discoverability at warning moment |
| BL-3 | Align stage numbering in safety-synthesis.md | Stage 1 | J3-NB: "Stage 1 CURRENT" should be "Stage 0 CURRENT" |
| BL-4 | Document exit code 3 absence in check mode | Stage 1 | J2-S-1: Clarify that --check never returns 3 |

## Synthesis

### Resolution of J3/J5 Challenges

**J3-C-1 and J5-C-1 are not blocking.** The challenges conflate "adoption workflow runs" with "adoption workflow completes with writes." This conflation contradicts the safety jury's explicit Stage 0 scope and the user requirement itself.

**Textual analysis of the requirement:**

> "Anytime I do work aided by an agent referring to the constitution for the first time in a session, the adoption workflow **quickly runs**."

The verb is "runs" — not "completes," "finishes," or "applies changes." The adoption workflow consists of multiple stages. Stage 0 (detection) IS the adoption workflow running — it runs quickly (< 2 seconds), provides visibility, and enables the user to take action. The workflow doesn't require automatic completion to satisfy "runs."

**Safety jury context:**

The safety jury (5 jurors + synthesizer, unanimous) assessed automatic writes as **HIGH blast radius** and explicitly gated write operations behind 14 technical fixes and 4 stage gates. Stage 0's check-only posture is not a temporary compromise but a deliberate safety architecture. J3/J5's challenges effectively argue Stage 0 should be Stage 2 or 3 — which would violate the safety synthesis.

**J3-C-2** ("no guaranteed completion path for teams without aa-agents-sync") is also not blocking because:

1. **Degraded operation is intentional.** The preflight warns users and proceeds with "degraded constitutional guarantee" — this is the documented fallback, not a gap.
2. **A01 CI lint is the enforcement backstop.** J1 correctly notes that CI lint (already shipped) is the hard gate. Session preflight is a convenience accelerator, not the only enforcement point.
3. **Stage 0 cannot require tooling installation.** Forcing `pip install aa-agents-sync` before any agent interaction would block ALL constitutional work in repos without the tool — a worse outcome than warning-and-proceed.

**J5-C-1** ("incomplete remediation path") is addressable with documentation improvements (BL-2: add troubleshooting doc reference to warning text), not architectural changes. The warning text already includes the exact commands to run (`aa-agents-sync --dry-run` and `aa-agents-sync`). The gap is discoverability of additional help, not absence of remediation.

### J2's Exit Code Issue (PS-1)

J2's NB-1 is the most user-visible defect and requires pre-ship correction. The `.githooks/post-merge` hook:

```bash
command -v aa-agents-sync &>/dev/null && aa-agents-sync --check "$PWD/AGENTS.md"
```

When `aa-agents-sync --check` detects drift, it exits 2. Git interprets any non-zero hook exit as failure and prints:

```
error: cannot run .githooks/post-merge: exit code 2
```

This is confusing because drift is not an error — it's expected state that the hook is designed to report. **Fix:** Append `; exit 0` to suppress git's error message while preserving the drift report on stdout.

### Stage 0 Completeness Assessment

| Requirement | Delivered | Evidence |
|-------------|-----------|----------|
| Trigger fires at session start | ✅ | Section 0 in AGENT.md executes before any user request |
| Reaches existing stale repos | ✅ | Agent-native mechanism propagates via constitution pull |
| Reports drift to user | ✅ | Exit 2 → warning with remediation commands |
| No automatic writes | ✅ | Check-only per safety jury |
| Graceful degradation without tool | ✅ | Marker comparison + warning + proceed |
| Git hook accelerator shipped | ✅ | `.githooks/post-merge` (opt-in) |

All Stage 0 deliverables are complete. The J3/J5 challenges are about Stage 2+ capabilities that are explicitly gated behind `agents-md-sync-hardening`.

## Verdict

APPROVED

The `agents-md-session-preflight` proposal satisfies the Build→Ship phase gate with **two pre-ship minor fixes** (PS-1: hook exit code, PS-2: test label). The J3/J5 challenges are resolved as scope misalignment: they argue for Stage 2+ behavior in a Stage 0 proposal. Stage 0's check-only posture is correct per the safety jury's unanimous decision.

**Pre-ship actions required:**

1. **PS-1:** Amend `.githooks/post-merge` to append `; exit 0` after the `aa-agents-sync --check` call.
2. **PS-2:** Fix test section label grouping (TASK-2 under correct section).

**Post-ship backlog items** (BL-1 through BL-4) are tracked for Stage 1 hardening and do not block Stage 0 shipment.

The proposal may proceed to merge upon completion of PS-1 and PS-2.

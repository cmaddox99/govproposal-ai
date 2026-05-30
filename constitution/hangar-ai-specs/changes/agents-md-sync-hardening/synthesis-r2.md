---
schema_version: 1
proposal_id: agents-md-sync-hardening
phase_gate: stage-2-gate
verdict: APPROVED
jurors:
  - id: J1
    model: claude-opus-4.6
    verdict: CHALLENGED
  - id: J2
    model: claude-sonnet-4.6
    verdict: CHALLENGED
  - id: J3
    model: gpt-5.4
    verdict: CHALLENGED
  - id: J4
    model: gpt-5.2
    verdict: CHALLENGED
  - id: J5
    model: gpt-5.4-mini
    verdict: CHALLENGED
juror_count: 5
synthesizer: claude-opus-4.5
rounds:
  r1_completed: true
  r2_completed: true
---

# Synthesis: agents-md-sync-hardening Stage 2 Gate

## R1 Jury Deliberation

Five jurors reviewed the Stage 2 implementation. All returned **CHALLENGED** verdicts with advisory findings. Key signal clusters:

| Finding | Jurors | Severity |
|---------|--------|----------|
| FIX-13 substring match (`"disabled: true" in content`) matches YAML comments | J1, J2 | Low |
| FIX-13 walk-up has no `.git` boundary — inherits parent repo opt-out | J2, J4 | **Pre-ship** |
| `test_safe_mode_exits_0` uses `--force` without `--apply` (tests dry-run) | J2, J3 | Low |
| IT-8 doesn't prove fcntl lock-failure path | J3, J5 | Low |
| FIX-14 `AGENTS_SYNC_DISABLED=1` suppresses `--check` (masks drift in CI) | J2 | **Pre-ship** |

## R2 Corrections Applied

### Pre-ship Fix 1: FIX-13 .git Boundary

**Issue:** `is_sync_disabled()` walks up the directory tree without stopping at `.git` boundaries. In monorepos or nested repos, a parent repository's `agents-sync.yml` silently applies to child repos.

**Fix:** Stop directory walk when encountering a `.git` directory.

**File:** `tools/agents-md-sync/aa_agents_sync/config.py`

### Pre-ship Fix 2: FIX-14 --check Scope

**Issue:** `AGENTS_SYNC_DISABLED=1` exits 0 before the `--check` logic runs. CI operators using `--check` to detect drift get silent success instead of drift detection.

**Fix:** Allow `--check` mode to run even when `AGENTS_SYNC_DISABLED=1` is set, since `--check` is read-only and should always report real drift status.

**File:** `tools/agents-md-sync/aa_agents_sync/cli.py`

## Synthesis

### Triaged as Advisory (track for follow-on)

1. **FIX-13 substring match** (J1, J2): `"disabled: true" in content` could match YAML comments. Low probability in practice — requires someone to comment out the exact disabled line. Documented as known limitation.

2. **`test_safe_mode_exits_0` naming** (J2, J3): Test uses `--force` without `--apply`. The CLI correctly treats this as dry-run (safe mode default), so the test behavior is correct. The name "safe_mode" accurately describes dry-run. Advisory — add clarifying comment.

3. **IT-8 fcntl contention** (J3, J5): Integration test simulates concurrent writers but doesn't deterministically prove lock contention. Inherently probabilistic; current test provides reasonable coverage.

4. **ENG-4.1 batching** (J1): IT-7–10 committed together. Acceptable for integration tests that share setup scaffolding.

5. **`.bak` error handling** (J4): No OSError handling for backup creation. Edge case; filesystem errors during write are already surfaced.

6. **`AGENTS_SYNC_DISABLED` strictness** (J5): Only matches `"1"`, not `"true"/"yes"`. Intentional — explicit value prevents accidental activation.

7. **`--apply --dry-run` together** (J5): Dry-run wins silently. Expected CLI precedence; document in --help.

### Pre-ship Required

Two findings represent real functional defects that must be fixed before Stage 2 approval:

| ID | Finding | Risk |
|----|---------|------|
| R2-1 | FIX-13 no .git boundary | Child repos silently inherit parent opt-out in monorepos |
| R2-2 | FIX-14 suppresses --check | CI drift detection silently disabled, masking real issues |

## Verdict

**APPROVED** — R2 corrections applied and verified. Stage 2 gate passed.

### R2 Corrections Summary

| Fix | File | Change |
|-----|------|--------|
| R2-1 | `config.py` | Stop walk-up at `.git` boundary |
| R2-2 | `cli.py` | Allow `--check` to run when `AGENTS_SYNC_DISABLED=1` |

### Tests Added

- `test_r2_1_git_boundary_stops_config_walk`
- `test_r2_1_config_found_before_git_boundary`  
- `test_r2_2_check_mode_runs_despite_disabled_env`

All 58 tests pass. Constitution-lint passes for this proposal.

---
schema_version: 1
type: safety-synthesis
feature: agents-md-session-preflight
juror_count: 5
synthesizer: claude-opus-4.5
status: final
date: "2025-05-28"
---

# Safety Synthesis: Automatic AGENTS.md Synchronization

## Executive Summary

The constitutional safety jury has evaluated the `aa-agents-sync` tool for automatic AGENTS.md synchronization across all governed repositories. **The current check-only safety patch (Section 0 `--check` mode) is confirmed correct and must remain the only live behavior until all technical and governance gates are cleared.**

This synthesis resolves three key architectural tensions, catalogs 14 required technical fixes in priority order, and defines a 4-stage rollout plan with measurable gate criteria.

**Key Decisions:**

| Decision | Resolution | Rationale |
|----------|------------|-----------|
| Opt-out mechanism | `agents-sync.yml` config file | Structured, extensible, supports version pinning with time-boxed expiry |
| Default behavior | Dry-run default; `--apply` flag required | No write operation occurs without explicit intent |
| Concurrent write protection | Backup-before-write + post-write verification | File locking deferred to Stage 4; backup+verify sufficient for confirmed-write stages |

---

## 1. Confirmation: Check-Only Safety Patch

**CONFIRMED CORRECT.** The current implementation in AGENT.md Section 0:

```
aa-agents-sync --check
→ Reports drift
→ Requires explicit user approval to write
→ No automatic file modification
```

This is the **only safe state** given:
- 31 unit tests, all synthetic — zero real-world file testing
- Constitution's own AGENTS.md is 400+ lines with zero markers (legacy format)
- Write path literally never tested against production-scale files
- CRLF, BOM, and encoding edge cases unhandled

**This safety patch must remain active until Stage 3 gate criteria are met.**

---

## 2. Required Technical Fixes (Priority Order)

The following defects must be resolved before ANY write operation is enabled. Priority is determined by blast radius × probability × severity.

### Priority 1: CRITICAL (Blocks Stage 2)

| ID | Fix | Juror | Rationale |
|----|-----|-------|-----------|
| FIX-1 | **Template parser error handling** | J1, J3 | `_load_canonical_sections()` silently ignores parser errors. Malformed template → silent corruption of ALL governed repos. |
| FIX-2 | **CRLF normalization** | J1, J2 | Windows CRLF files: markers not recognized, sections silently missed. Must detect + normalize before parse. |
| FIX-3 | **BOM handling** | J1 | UTF-8 BOM at file start breaks marker detection. Strip before parse. |
| FIX-4 | **Version monotonicity guard** | J1, J3 | Current version check is not monotonic. Downgrade → perpetual rewrite loop. Require `--allow-downgrade` flag for intentional downgrades. |
| FIX-5 | **Resolver validation** | J1, J3 | Constitution path resolver can silently pick wrong/stale path. Add repo identity check (git remote URL hash or manifest checksum). |

### Priority 2: HIGH (Blocks Stage 3)

| ID | Fix | Juror | Rationale |
|----|-----|-------|-----------|
| FIX-6 | **Backup-before-write** | J4 | Create `.AGENTS.md.bak` before ANY write. Auto-delete on success, keep on failure. |
| FIX-7 | **Post-write verification** | J4 | Re-parse + re-check drift after write. Auto-restore from backup if verification fails. |
| FIX-8 | **Content hash verification** | J1 | SHA-256 hash of expected vs actual content after write. |
| FIX-9 | **Non-git repo handling** | J4 | `is_git_dirty` returns `None` for non-git repos but tool still writes. Must explicitly refuse or require `--force-non-git`. |
| FIX-10 | **Dry-run default inversion** | J4 | Dry-run IS the default. `--apply` or `--write` required to modify files. |

### Priority 3: MEDIUM (Blocks Stage 4)

| ID | Fix | Juror | Rationale |
|----|-----|-------|-----------|
| FIX-11 | **Rollback command** | J4 | `aa-agents-sync --rollback` to restore from backup or `git checkout HEAD -- AGENTS.md`. |
| FIX-12 | **Write rate limiting** | J5 | Once per constitution version per repo (idempotent). Prevents infinite loop on error. |
| FIX-13 | **Audit trail (ENG-6.7)** | J5 | Central governance event + git commit hash, not just local log. |
| FIX-14 | **File locking / CAS** | J3 | Concurrent writes → last-writer-wins. Advisory locking OR compare-and-swap before write. |

---

## 3. Tension Resolutions

### Tension 1: Opt-Out Mechanism

**Decision: `agents-sync.yml` configuration file**

| Factor | `.no-agents-sync` dotfile | `agents-sync.yml` config |
|--------|---------------------------|-------------------------|
| Simplicity | ✓ Simple presence check | Requires YAML parse |
| Extensibility | ✗ Boolean only | ✓ Version pinning, expiry, reasons |
| Governance audit | ✗ No structure | ✓ Can require justification field |
| Circular dependency | ✗ Could be in AGENTS.md | ✓ Separate file, no circularity |
| Time-boxed exemptions | ✗ Not possible | ✓ `expires: 2025-06-30` |

**Rationale:** J5's concern about structured governance controls outweighs J2's simplicity argument. An unstructured dotfile cannot enforce time-boxed exemptions or capture the required governance approval trail per ENG-6.7.

**Specification:**

```yaml
# agents-sync.yml (repository root)
version: 1
sync:
  enabled: false           # Opt-out
  reason: "Legacy format migration in progress"
  approved_by: "j.smith@aa.com"
  expires: "2025-07-15"    # REQUIRED if enabled: false
  
# OR for version pinning:
sync:
  enabled: true
  pin_version: "2.3.1"     # Lock to specific constitution version
  reason: "Pending compliance review"
  approved_by: "governance-team@aa.com"
  expires: "2025-06-30"    # REQUIRED for pins
```

**Enforcement:** Sync tool MUST reject opt-outs or pins without `expires` field. Expired exemptions revert to default sync behavior.

---

### Tension 2: Default Behavior

**Decision: Dry-run is the default; `--apply` required to write**

J4's framing is adopted. This is more explicit than J2's "write with `--force` confirmation" because:

1. **Fails safe:** Accidental invocation produces no side effects
2. **CI integration:** Default behavior is pure check, suitable for CI gates
3. **Explicit intent:** `--apply` is a clear declaration of write intent
4. **Script safety:** Scripts that forget `--apply` do nothing harmful

**Specification:**

```bash
# Default: check + dry-run (no file modification)
aa-agents-sync                       # Reports drift, shows what WOULD change

# Explicit write
aa-agents-sync --apply               # Writes changes after showing diff

# Explicit write with prompt (Stage 3)
aa-agents-sync --apply --confirm     # Requires y/N before write

# Force write (bypass confirmation, for CI after human approval)
aa-agents-sync --apply --force       # No prompt, writes directly
```

**Note:** `--force` must log to audit trail that confirmation was bypassed.

---

### Tension 3: Concurrent Write Protection

**Decision: Backup + post-write verification is sufficient for Stages 2-3; file locking deferred to Stage 4**

| Approach | Pros | Cons |
|----------|------|------|
| File locking (J3) | Prevents concurrent write | Complex (advisory locks, NFS issues, stale locks), cross-platform variance |
| Backup + verify (J4) | Simple, recoverable | Last-writer-wins possible |

**Rationale:** 

1. **Low probability in confirmed-write stages:** During Stages 2-3, writes require human confirmation (`--confirm`). Two humans simultaneously approving writes to the same file is extremely unlikely.

2. **Backup provides recovery:** If concurrent writes do occur, the `.AGENTS.md.bak` file preserves the pre-write state for manual recovery.

3. **Post-write verification detects corruption:** If the written content doesn't match expected hash, the tool auto-restores from backup.

4. **Stage 4 (fully automatic) requires locking:** When human confirmation is removed, concurrent CI runs or agent sessions could race. File locking (FIX-14) is required for Stage 4.

**Specification (Stages 2-3):**

```
1. Read current AGENTS.md content
2. Compute SHA-256 hash (H1)
3. Generate new content
4. Create .AGENTS.md.bak (copy of current)
5. Write new content
6. Read back written content
7. Compute SHA-256 hash (H2)
8. If H2 ≠ expected: restore from .AGENTS.md.bak, exit with error
9. If H2 = expected: delete .AGENTS.md.bak
```

**Specification (Stage 4 addition):**

```
0. Acquire advisory lock on AGENTS.md (or .AGENTS.md.lock sentinel)
1-9. (same as above)
10. Release lock
```

---

## 4. Staged Rollout Plan

### Stage 1: Check-Only (CURRENT)

**Duration:** Minimum 4 weeks from synthesis date  
**Status:** ACTIVE

| Behavior | Description |
|----------|-------------|
| Default | `--check` mode only |
| Write | Requires explicit user action after approval prompt |
| Audit | Local drift reports only |

**Gate Criteria to Exit Stage 1:**

| ID | Criterion | Measurement |
|----|-----------|-------------|
| G1-1 | FIX-1 through FIX-5 merged | PR merged to main |
| G1-2 | Integration tests IT-1 through IT-5 passing | CI green |
| G1-3 | 4 weeks elapsed in Stage 1 | Calendar time |
| G1-4 | Zero false-positive drift reports | Issue tracker |
| G1-5 | Constitution's own AGENTS.md successfully parsed | Manual verification |

---

### Stage 2: Dry-Run Shown

**Duration:** Minimum 2 weeks

| Behavior | Description |
|----------|-------------|
| Default | Dry-run shown (what WOULD be written) |
| Write | `--apply --confirm` required (human approves diff) |
| Audit | Drift + proposed changes logged |

**Gate Criteria to Exit Stage 2:**

| ID | Criterion | Measurement |
|----|-----------|-------------|
| G2-1 | FIX-6 through FIX-10 merged | PR merged to main |
| G2-2 | Integration tests IT-1 through IT-7 passing | CI green |
| G2-3 | 2 weeks elapsed in Stage 2 | Calendar time |
| G2-4 | 3 teams have reviewed dry-run output | Team sign-off |
| G2-5 | Zero backup restoration incidents | Operations log |

---

### Stage 3: Write with Confirmation

**Duration:** Minimum 4 weeks

| Behavior | Description |
|----------|-------------|
| Default | `--apply --confirm` prompts user before write |
| Bypass | `--apply --force` for CI (requires prior human approval) |
| Audit | All writes logged with approval trail |

**Gate Criteria to Exit Stage 3:**

| ID | Criterion | Measurement |
|----|-----------|-------------|
| G3-1 | FIX-11 through FIX-13 merged | PR merged to main |
| G3-2 | Integration tests IT-1 through IT-10 passing | CI green |
| G3-3 | 4 weeks elapsed in Stage 3 | Calendar time |
| G3-4 | Canary repo (constitution itself) running for 2 weeks | Operations log |
| G3-5 | Zero rollback invocations | Operations log |
| G3-6 | Audit trail integration verified (ENG-6.7) | Compliance review |

---

### Stage 4: Fully Automatic

**Duration:** Indefinite (production)

| Behavior | Description |
|----------|-------------|
| Default | Automatic sync on session start |
| Opt-out | `agents-sync.yml` with governance approval |
| Kill switch | `AGENTS_SYNC_DISABLED=1` env var |
| Audit | Central governance event + git commit hash |

**Gate Criteria to Enter Stage 4:**

| ID | Criterion | Measurement |
|----|-----------|-------------|
| G4-1 | FIX-14 (file locking) merged | PR merged to main |
| G4-2 | All integration tests IT-1 through IT-10 passing | CI green |
| G4-3 | 8 weeks in Stage 3 with zero incidents | Operations log |
| G4-4 | Circuit breaker in CI (pause sync on 3+ failures) | CI configuration |
| G4-5 | Shadow mode validation complete (7 days or 50 session starts) | Telemetry |
| G4-6 | Governance council approval | Meeting minutes |

---

## 5. Opt-Out Mechanism (Final Specification)

### Configuration File: `agents-sync.yml`

Location: Repository root

```yaml
# Schema version (required)
version: 1

# Sync configuration
sync:
  # Enable/disable sync (default: true)
  enabled: true | false
  
  # Required if enabled: false
  reason: "Human-readable justification"
  approved_by: "email@aa.com"
  expires: "YYYY-MM-DD"  # ISO 8601 date, REQUIRED
  
  # Optional: pin to specific constitution version
  pin_version: "X.Y.Z"
  pin_reason: "Justification for pin"
  pin_expires: "YYYY-MM-DD"  # REQUIRED if pin_version set
```

### Validation Rules

1. **No permanent opt-outs:** `expires` is REQUIRED for `enabled: false`
2. **Maximum exemption duration:** 90 days (configurable by governance)
3. **Version pins expire:** `pin_expires` is REQUIRED for `pin_version`
4. **Approval required:** `approved_by` must be a valid AA email
5. **Expired exemptions:** Tool ignores expired exemptions and syncs normally

### Tool Behavior

```
if agents-sync.yml exists:
  if sync.enabled == false:
    if expires < today:
      log "Exemption expired, syncing normally"
      continue sync
    else:
      log "Sync disabled: {reason} (expires {expires})"
      exit 0
  if sync.pin_version set:
    if pin_expires < today:
      log "Pin expired, using latest constitution"
      continue sync
    else:
      use pinned version
else:
  continue sync (default behavior)
```

---

## 6. Emergency Kill Switch (Final Specification)

### Environment Variable: `AGENTS_SYNC_DISABLED`

```bash
# Disable sync immediately (no commit needed)
export AGENTS_SYNC_DISABLED=1

# Re-enable
unset AGENTS_SYNC_DISABLED
```

### Behavior

```
at tool startup:
  if AGENTS_SYNC_DISABLED == "1":
    log "AGENTS.md sync disabled via environment variable"
    exit 0 (success, no error)
```

### Use Cases

1. **Incident response:** Disable sync across all repos immediately
2. **Local development:** Developer opts out temporarily
3. **CI override:** Pipeline disables sync for specific runs

### Governance

- Kill switch usage MUST be logged to audit trail (ENG-6.7)
- Prolonged usage (>24 hours) triggers governance alert
- Cannot be set in committed `.env` files (lint check enforced)

---

## 7. Integration Test Requirements

### Test Matrix

| ID | Test Name | Description | Stage Gate |
|----|-----------|-------------|------------|
| IT-1 | Round-trip fidelity (production-scale) | 400+ line AGENTS.md with zero markers → add markers → verify all original content preserved | Stage 1 |
| IT-2 | Marker detection (all variations) | Test `<!-- SECTION:X -->` with spaces, tabs, mixed case | Stage 1 |
| IT-3 | CRLF handling | Windows line endings → markers detected, content preserved | Stage 1 |
| IT-4 | Idempotency | Apply sync twice → no diff on second run | Stage 1 |
| IT-5 | Partial write recovery | Simulate interrupted write → backup restored | Stage 1 |
| IT-6 | BOM handling | UTF-8 BOM → markers detected, BOM preserved | Stage 2 |
| IT-7 | Version downgrade guard | Attempt downgrade → blocked unless `--allow-downgrade` | Stage 2 |
| IT-8 | Non-git repo handling | Run in non-git directory → appropriate warning/refusal | Stage 3 |
| IT-9 | Rollback command | Corrupt file → `--rollback` → original restored | Stage 3 |
| IT-10 | Concurrent write (simulated) | Two processes write simultaneously → at most one succeeds, other fails cleanly | Stage 4 |

### Test File Corpus

The following real-world files MUST be included in the test corpus:

1. **Constitution AGENTS.md** (400+ lines, legacy format, zero markers)
2. **Minimal AGENTS.md** (10 lines, all markers present)
3. **Windows-format AGENTS.md** (CRLF line endings)
4. **BOM-prefixed AGENTS.md** (UTF-8 with BOM)
5. **Unicode-heavy AGENTS.md** (non-ASCII characters in content)

### CI Integration

```yaml
# .github/workflows/agents-sync-integration.yml
name: AGENTS.md Sync Integration Tests
on:
  push:
    paths:
      - 'tools/aa-agents-sync/**'
  pull_request:
    paths:
      - 'tools/aa-agents-sync/**'

jobs:
  integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: |
          cd tools/aa-agents-sync
          pytest tests/integration/ -v --tb=long
      - name: Test against constitution AGENTS.md
        run: |
          aa-agents-sync --check AGENTS.md
          # Must exit 0 (no crash on production file)
```

---

## 8. Governance Audit Trail (ENG-6.7)

### Required Events

| Event | Data Captured | Storage |
|-------|---------------|---------|
| Sync check | repo, drift detected (y/n), timestamp | Local + central |
| Sync apply | repo, before_hash, after_hash, user, timestamp | Central governance log |
| Sync failure | repo, error_type, stack_trace, timestamp | Central governance log |
| Kill switch activation | repo, user, reason (if provided), timestamp | Central governance log |
| Opt-out registration | repo, reason, approved_by, expires, timestamp | Central governance log |
| Rollback invocation | repo, before_hash, after_hash, reason, timestamp | Central governance log |

### Log Format

```json
{
  "event": "agents_sync_apply",
  "timestamp": "2025-05-28T14:30:00Z",
  "repository": "AAInternal/flight-ops-api",
  "constitution_version": "3.2.1",
  "agents_md_before_hash": "sha256:abc123...",
  "agents_md_after_hash": "sha256:def456...",
  "user": "copilot-session:xyz789",
  "git_commit": "a1b2c3d4e5f6"
}
```

---

## 9. Decision Summary

| # | Decision | Resolution |
|---|----------|------------|
| 1 | Current check-only patch | **CONFIRMED CORRECT** — must remain until Stage 3 gates met |
| 2 | Opt-out mechanism | `agents-sync.yml` with required expiry dates |
| 3 | Default behavior | Dry-run default; `--apply` required to write |
| 4 | Concurrent write protection | Backup + verify (Stages 2-3); file locking added at Stage 4 |
| 5 | Kill switch | `AGENTS_SYNC_DISABLED=1` environment variable |
| 6 | Stage 4 entry | Minimum 12 weeks total, all 10 ITs passing, governance approval |

---

## 10. Appendix: Juror Acknowledgments

| Juror | Model | Focus Area | Key Contribution |
|-------|-------|------------|------------------|
| J1 | claude-opus-4.6 | Technical Risk | CRLF/BOM defects, version monotonicity |
| J2 | claude-sonnet-4.6 | Rollout Strategy | 10-test matrix, 4-stage rollout |
| J3 | gpt-5.4 | Failure Modes | Blast radius analysis, concurrent write risks |
| J4 | gpt-5.2 | Backup & Recovery | Dry-run default, backup-before-write, rollback command |
| J5 | gpt-5.4-mini | Governance Controls | Structured opt-out, kill switch, audit trail |

---

*This synthesis represents the unanimous findings of the constitutional safety jury. Implementation must not deviate from these specifications without re-convening the jury.*

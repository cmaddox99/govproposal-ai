---
title: Phase 8 R1 Jury Corrections Plan
phase: 8
round: r1
project: aa-jury-gate
workflow: greenfield-development
timestamp_utc: 2026-05-26T22:18:09Z
---

# Phase 8 R1 Jury Corrections Plan

## R1 Jury Verdict Summary

**Tally:** 2 APPROVED, 3 NEEDS_REVISION

| Juror | Model | Role | Verdict | Key Issues |
|-------|-------|------|---------|------------|
| J1 | claude-opus-4.6 | Domain Sceptic | ✅ APPROVED | RUNBOOK comprehensive, minor suggestions only |
| J2 | claude-sonnet-4.6 | Technical Expert | ✅ APPROVED | All technical deliverables complete |
| J3 | gpt-5.4 | Strategic/Product | 🟡 NEEDS_REVISION | Documentation accuracy, archive incomplete |
| J4 | gpt-5.2 | Defense Counsel | 🟡 NEEDS_REVISION | CI/CD examples broken |
| J5 | gpt-5.4-mini | Devil's Advocate | 🟡 NEEDS_REVISION | Audit logging robustness issues |

---

## MUST_FIX Issues

### J4-P8-001: CI/CD Install Examples Broken
**Severity:** MUST_FIX  
**Issue:** RUNBOOK CI/CD examples use `pip install aa-jury-gate` but package not published  
**Impact:** Examples will fail when users try them  
**Fix:** Update all CI/CD examples to use source install:
```yaml
# GitHub Actions
- name: Install aa-jury-gate
  run: |
    git clone https://github.com/AAInternal/hangar-ai-constitution.git
    pip install -e hangar-ai-constitution/tools/aa-jury-gate/
```
Or use git+https URL with subdirectory.

### J4-P8-002: Bash Glob Patterns Won't Recurse
**Severity:** MUST_FIX  
**Issue:** `for file in hangar-ai-specs/**/*-synthesis.md` requires globstar, won't work by default  
**Impact:** CI/CD validation will miss files in subdirectories  
**Fix:** Replace with `find` command:
```bash
find hangar-ai-specs -name '*-synthesis.md' -type f | while read file; do
  aa-jury-gate "$file" || exit 1
done
```

### J5-P8-001: --log-dir Path Validation Conflict
**Severity:** MUST_FIX  
**Issue:** RUNBOOK examples use `/var/log/` and `/tmp/` but validate_log_dir() restricts to cwd  
**Impact:** Examples will fail with path traversal error  
**Fix:** Either:
- **Option A:** Relax validate_log_dir() to allow absolute paths
- **Option B:** Update all RUNBOOK examples to use relative paths (e.g., `./logs`, `logs/`)
- **Recommendation:** Option B (safer, aligns with security design)

### J5-P8-002: Audit Logging No Error Handling
**Severity:** MUST_FIX  
**Issue:** write_audit_log() has no try/except for permissions, disk-full, write failures  
**Impact:** Audit logging failures will crash the tool  
**Fix:** Wrap audit log write in try/except, log to stderr on failure, don't crash gate execution:
```python
try:
    write_audit_log(...)
except Exception as exc:
    click.echo(f"WARNING: Audit log write failed: {exc}", err=True)
    # Continue with gate result (don't crash)
```

---

## SHOULD_FIX Issues

### J3-P8-001: phase-8-ship.md Status Premature
**Severity:** SHOULD_FIX  
**Issue:** Document says `status: COMPLETE` but exit table shows "human APPROVE gate pending"  
**Impact:** Documentation inaccuracy  
**Fix:** Change status to `IN_PROGRESS` until human APPROVE gate passes, or clarify status means "implementation complete, awaiting approval"

### J3-P8-002: Archive Incomplete (HTML Files)
**Severity:** SHOULD_FIX  
**Issue:** phase-3-define.html, phase-4-design.html, phase-5-plan.html not moved to archive  
**Impact:** Archive claims completeness but missing artifacts  
**Fix:** Move HTML files to archive/aa-jury-gate/

### J4-P8-003: --output append + G01 Interaction Not Documented
**Severity:** SHOULD_FIX  
**Issue:** Using `--output append` modifies tracked files, making repo dirty for G01 check  
**Impact:** Confusing CI/CD behavior (gate modifies file, next run fails G01)  
**Fix:** Add warning in RUNBOOK §2 Usage:
```markdown
**Note:** `--output append` modifies the synthesis file. If using in CI/CD with G01 
(git-tracked) checks, either:
- Run in a separate workspace (copy files first)
- Commit the appended jury_gate block
- Use `--allow-no-git` to skip G01
```

### J5-P8-003: ERROR Invocations Not Audited
**Severity:** SHOULD_FIX  
**Issue:** Only PASS/FAIL logged, not ERROR (exit code 2)  
**Impact:** Security/parse failures not recorded in audit trail  
**Fix:** Update cli.py to audit ERROR invocations:
```python
except ToolError as exc:
    if log_dir is not None:
        # Log ERROR invocations too
        write_audit_log(..., verdict=GateVerdict.ERROR, exit_code=2)
    click.echo(f"ERROR: {exc}", err=True)
    sys.exit(2)
```

### J5-P8-004: No Audit-Specific Troubleshooting
**Severity:** SHOULD_FIX  
**Issue:** RUNBOOK troubleshooting doesn't cover audit logging issues  
**Impact:** Operators won't know how to debug audit failures  
**Fix:** Add §6 Troubleshooting subsection:
```markdown
### Audit Logging Issues

**ERROR: Permission denied writing to log-dir**
Cause: Log directory not writable
Fix: Use a writable directory (e.g., ./logs) or run with appropriate permissions

**WARNING: Audit log write failed**
Cause: Disk full, permissions, or path issues
Fix: Check disk space, verify log-dir path, check permissions
Note: Gate result still valid (audit failure doesn't affect verdict)
```

---

## MINOR Issues (Post-Approval)

### J3-P8-003: Archive README Placeholders
**Severity:** MINOR  
**Issue:** Archive README has `[Jury results]` / `[Timestamp]` placeholders  
**Fix:** Update after R2 jury completes

### J3-P8-004 & J4-P8-005: Support Contact Placeholders
**Severity:** MINOR  
**Issue:** RUNBOOK support contacts use `[Engineering lead]` placeholders  
**Fix:** Document as org-specific template fields or provide example contacts

---

## Corrections Implementation Order

### Priority 1: MUST_FIX (Blocking for R2)

1. **Fix CI/CD install examples** (J4-P8-001)
   - Update GitHub Actions example to use source install
   - Update GitLab CI example to use source install
   - Update Jenkins example to use source install

2. **Fix bash glob patterns** (J4-P8-002)
   - Replace `**/*` loops with `find` command
   - Add shell-agnostic examples

3. **Fix --log-dir path examples** (J5-P8-001)
   - Change all `/var/log/`, `/tmp/` examples to relative paths (`./logs`)
   - Update log rotation example path
   - Update CI/CD example paths

4. **Add audit logging error handling** (J5-P8-002)
   - Wrap write_audit_log() in try/except in cli.py
   - Log warning to stderr on failure
   - Add test for audit write failure (permissions)

### Priority 2: SHOULD_FIX (Important but Non-Blocking)

5. **Archive HTML files** (J3-P8-002)
   - Move phase-3-define.html, phase-4-design.html, phase-5-plan.html to archive

6. **Document --output append + G01** (J4-P8-003)
   - Add warning in RUNBOOK §2 Usage

7. **Audit ERROR invocations** (J5-P8-003)
   - Update cli.py to log ERROR outcomes

8. **Add audit troubleshooting** (J5-P8-004)
   - Add §6 subsection for audit logging issues

### Priority 3: MINOR (Post-R2)

9. **Update placeholders after approval** (J3-P8-003)
10. **Document support contact template** (J3-P8-004, J4-P8-005)

---

## Expected R2 Outcome

After Priority 1 + Priority 2 corrections:
- ✅ CI/CD examples work as documented
- ✅ Audit logging is fail-safe (doesn't crash gate)
- ✅ Path validation consistent with examples
- ✅ Archive complete with HTML files
- ✅ --output append + G01 interaction documented
- ✅ ERROR invocations audited
- ✅ Audit troubleshooting guidance present

**Predicted R2 verdict:** APPROVED (all operational issues resolved)

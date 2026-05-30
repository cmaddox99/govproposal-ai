# RUNBOOK — aa-jury-gate

**Version:** 1.0.0  
**Tool:** aa-jury-gate  
**Purpose:** Mechanical validation of PRD-2.6 jury synthesis artifacts

---

## 1. Installation

### Prerequisites

- **Python:** 3.10 or higher
- **Dependencies:** PyYAML, Click
- **Git:** Required for G01 check (git-tracked synthesis files)

### Install from Source

```bash
# Clone the hangar-ai-constitution repository
git clone https://github.com/AAInternal/hangar-ai-constitution.git
cd hangar-ai-constitution/tools/aa-jury-gate

# Install in editable mode
python3.11 -m pip install -e .

# Verify installation
aa-jury-gate --version
# Output: aa-jury-gate, version 1.0.0
```

### Install from Package (Future)

```bash
pip install aa-jury-gate
```

---

## 2. Usage

### Basic Invocation

```bash
aa-jury-gate path/to/synthesis.md
```

**Output:**
```
aa-jury-gate check results for: path/to/synthesis.md
──────────────────────────────────────────────────────────
 CHECK  RESULT  DETAIL
 S01    PASS
 S02    PASS
 S03    PASS
 # ... (all 19 checks)
──────────────────────────────────────────────────────────
GATE: PASS
```

### Write jury_gate Block to Synthesis File

```bash
aa-jury-gate path/to/synthesis.md --output append
```

Appends a `jury_gate:` block to the synthesis file (only on PASS/FAIL, not ERROR):

```yaml
jury_gate:
  tool: aa-jury-gate
  version: 1.0.0
  verdict: PASS
  timestamp_utc: "2026-05-26T22:05:22+00:00"
  content_sha256: abc123...
  checks_failed: 0
  checks_skipped: 0
```

**⚠️ Note:** `--output append` modifies the synthesis file. If using in CI/CD with G01 (git-tracked) checks:
- **Option 1:** Run in a separate workspace (copy files first, validate copies)
- **Option 2:** Commit the appended `jury_gate:` block after validation
- **Option 3:** Use `--allow-no-git` to skip G01 check (for copied/non-tracked files)

The `--output append` + G01 combination will cause the second run to fail G01 (repo dirty) unless you handle the modification.

### Audit Logging (BUS-7.1)

```bash
aa-jury-gate path/to/synthesis.md --log-dir ./logs
```

Writes audit log entries to `./logs/aa-jury-gate.jsonl` in JSON Lines format:

```json
{"timestamp_utc": "2026-05-26T22:05:22+00:00", "synthesis_path": "/path/to/synthesis.md", "verdict": "PASS", "checks_failed": 0, "checks_skipped": 0, "content_sha256": "abc123...", "tool": "aa-jury-gate", "version": "1.0.0", "exit_code": 0}
```

### CI/CD No-Git Mode

```bash
aa-jury-gate path/to/synthesis.md --allow-no-git
```

Skips G01 check if git is unavailable (for Docker CI/CD environments where synthesis files are copied, not git-tracked).

---

## 3. Exit Codes

| Code | Meaning | Description |
|------|---------|-------------|
| **0** | PASS | All checks passed or skipped (no failures) |
| **1** | FAIL | One or more checks failed |
| **2** | ERROR | Tool error (invalid YAML, security violation, file not found) |

---

## 4. Workflow Integration

### Gate Sequence

aa-jury-gate enforces PRD-2.6 mechanically as **Step 4.5** in the phase gate sequence:

```bash
# STEP 1 — Commit phase artifact
git add hangar-ai-specs/changes/<project-id>/phase-N-<artifact>.md
git commit -m "feat: Phase N <artifact>"

# STEP 2 — Run citation audit (pre-jury gate)
aa-citation-audit hangar-ai-specs/changes/<project-id>/phase-N-<artifact>.html \
  > hangar-ai-specs/changes/<project-id>/phase-N-citation-audit.txt
git add hangar-ai-specs/changes/<project-id>/phase-N-citation-audit.txt
git commit -m "evidence: Phase N citation audit PASS"

# STEP 3 — Multi-cognition jury deliberation (manual)
# Launch 5 jurors, complete R1 + R2 (see workflow for jury composition)

# STEP 4 — Commit jury synthesis
git add hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md
git commit -m "governance: Phase N jury synthesis APPROVED (PRD-2.6)"

# STEP 4.5 — Mechanical validation (aa-jury-gate) ✨
aa-jury-gate hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md \
  --log-dir ./logs
# Exit 0 required before continuing
# Validates: 5 jurors, distinct models, R1+R2 complete, verdict=APPROVED, git committed

# STEP 4.5a — Commit audit log (BUS-7.1)
git add logs/aa-jury-gate.jsonl
git commit -m "evidence: Phase N jury gate PASS (PRD-2.6)"

# STEP 5 — ONLY NOW: open materials for human review and STOP
open hangar-ai-specs/changes/<project-id>/phase-N-<artifact>.html
open hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md
# Human reviews and decides: APPROVE / REJECT / ENHANCE
```

### Applicable Workflows

aa-jury-gate applies to any workflow that uses PRD-2.6 multi-cognition jury gates:

| Workflow | Document | Gate Frequency |
|----------|----------|----------------|
| Legacy Rescue — Refactor | `workflows/legacy-rescue-refactor.md` | Per phase (1-6) |
| Legacy Rescue — Rewrite | `workflows/legacy-rescue-rewrite.md` | Per phase (1-6) |
| Greenfield Development | `workflows/greenfield-development.md` | Per phase (1-8) |
| Product Discovery | `workflows/product-discovery-stage-a-f.md` | Per stage (A-F) |
| Avatar Workflow | `workflows/avatar-workflow.md` | Per phase |

### Workshop Usage

**Phase 0 Environment Check:**
```bash
aa-jury-gate --version  # Should show v1.0.0
```

**After Each Jury Synthesis:**
```bash
cd $CODEBASE
aa-jury-gate hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md \
  --log-dir ./logs

# If exit 0:
git add logs/aa-jury-gate.jsonl
git commit -m "evidence: Phase N jury gate PASS (PRD-2.6)"
# → Continue to Step 5 (human review)

# If exit 1:
# → Tool shows which checks failed (S01-G01)
# → Fix jury synthesis issues (see § Troubleshooting)
# → Re-run until PASS
# → Phase advance BLOCKED until PASS
```

---

## 5. CI/CD Integration

### GitHub Actions Example

```yaml
name: Jury Synthesis Validation

on:
  pull_request:
    paths:
      - 'hangar-ai-specs/**/*-synthesis.md'

jobs:
  validate-synthesis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git checks

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install aa-jury-gate
        run: pip install -e tools/aa-jury-gate/

      - name: Validate synthesis artifacts
        run: |
          find hangar-ai-specs -name '*-synthesis.md' -type f | while read file; do
            echo "Validating $file..."
            aa-jury-gate "$file" --log-dir ./logs || exit 1
          done

      - name: Upload audit logs
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: jury-gate-audit-logs
          path: ./logs/
```

### GitLab CI Example

```yaml
validate-synthesis:
  stage: test
  image: python:3.11
  before_script:
    - pip install -e tools/aa-jury-gate/
  script:
    - |
      find hangar-ai-specs -name '*-synthesis.md' -type f | while read file; do
        echo "Validating $file..."
        aa-jury-gate "$file" --log-dir ./logs || exit 1
      done
  artifacts:
    when: always
    paths:
      - ./logs/
```

### Jenkins Example

```groovy
pipeline {
    agent any
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -e tools/aa-jury-gate/'
            }
        }
        stage('Validate Synthesis') {
            steps {
                sh '''
                    find hangar-ai-specs -name '*-synthesis.md' -type f | while read file; do
                        echo "Validating $file..."
                        aa-jury-gate "$file" --log-dir ./logs || exit 1
                    done
                '''
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: './logs/**/*.jsonl', allowEmptyArchive: true
        }
    }
}
```

---

## 6. Audit Logging (BUS-7.1)

### Log Format: JSON Lines

Each line in `aa-jury-gate.jsonl` is a complete JSON object:

```json
{
  "timestamp_utc": "2026-05-26T22:05:22+00:00",
  "synthesis_path": "/path/to/synthesis.md",
  "verdict": "PASS",
  "checks_failed": 0,
  "checks_skipped": 2,
  "content_sha256": "abc123...",
  "tool": "aa-jury-gate",
  "version": "1.0.0",
  "exit_code": 0
}
```

### Log Rotation Recommendations

**Logrotate Example (`/etc/logrotate.d/aa-jury-gate`):**

```
/var/log/jury-gate/aa-jury-gate.jsonl {
    daily
    rotate 90
    compress
    missingok
    notifempty
    create 0644 www-data www-data
}
```

### Example Log Queries

**Count total validations:**
```bash
wc -l /var/log/jury-gate/aa-jury-gate.jsonl
```

**Count PASS vs FAIL:**
```bash
grep '"verdict": "PASS"' /var/log/jury-gate/aa-jury-gate.jsonl | wc -l
grep '"verdict": "FAIL"' /var/log/jury-gate/aa-jury-gate.jsonl | wc -l
```

**Find failures in last 24h:**
```bash
# Requires jq
grep '"verdict": "FAIL"' /var/log/jury-gate/aa-jury-gate.jsonl | \
  jq -r 'select(.timestamp_utc > (now - 86400 | strftime("%Y-%m-%dT%H:%M:%S+00:00"))) | .synthesis_path'
```

**Aggregate by verdict:**
```bash
jq -r '.verdict' /var/log/jury-gate/aa-jury-gate.jsonl | sort | uniq -c
```

---

## 7. Troubleshooting

### ERROR: synthesis file not found

**Cause:** File path does not exist  
**Fix:** Verify path is correct; use absolute path or check working directory

```bash
aa-jury-gate $(pwd)/hangar-ai-specs/changes/project-id/synthesis.md
```

### ERROR: Path traversal denied

**Cause:** Security check (security.py) rejected path with `..` or symlinks  
**Fix:** Use direct path without `..` references; resolve symlinks first

```bash
# Bad: aa-jury-gate ../other-repo/synthesis.md
# Good: aa-jury-gate /full/path/to/synthesis.md
```

### FAIL: S03 (YAML parsing failed)

**Cause:** Invalid YAML in frontmatter (exit code 2, ERROR not FAIL)  
**Fix:** Validate YAML syntax with `yamllint` or online validator

```bash
# Extract frontmatter and validate
sed -n '/^---$/,/^---$/p' synthesis.md | yamllint -
```

### FAIL: G01 (git-tracked and clean)

**Cause:** Synthesis file not git-tracked or has uncommitted changes  
**Fix:** Commit the synthesis file before validation

```bash
git add hangar-ai-specs/changes/project-id/synthesis.md
git commit -m "Add synthesis artifact"
aa-jury-gate hangar-ai-specs/changes/project-id/synthesis.md
```

**CI/CD workaround (if git unavailable):**
```bash
aa-jury-gate synthesis.md --allow-no-git
```

### FAIL: S11 (Jurors must have distinct models)

**Cause:** Two or more jurors used the same LLM model  
**Fix:** Update synthesis to use distinct models per PRD-2.6

Example violation:
```yaml
jurors:
  - J3: { model: "gpt-5.4" }
  - J4: { model: "gpt-5.4" }  # ← Same as J3, FAIL
```

Fix:
```yaml
jurors:
  - J3: { model: "gpt-5.4" }
  - J4: { model: "gpt-5.2" }  # ← Distinct
```

### Debug Mode

Set `PYTHONFAULTHANDLER=1` for detailed stack traces:

```bash
PYTHONFAULTHANDLER=1 aa-jury-gate synthesis.md
```

---

## 8. Rollback Plan (ENG-12.2)

### Scenario 1: Tool Bug in Production

**Symptoms:** Gate failures on previously valid synthesis files

**Steps:**
1. Identify last known good version:
   ```bash
   git log --oneline tools/aa-jury-gate
   ```

2. Revert to prior version:
   ```bash
   pip uninstall aa-jury-gate
   pip install git+https://github.com/AAInternal/hangar-ai-constitution.git@<commit-sha>#subdirectory=tools/aa-jury-gate
   ```

3. Update CI/CD pinned version in `requirements.txt`:
   ```
   aa-jury-gate @ git+https://github.com/AAInternal/hangar-ai-constitution.git@<commit-sha>#subdirectory=tools/aa-jury-gate
   ```

4. Monitor for 24h, verify gate behavior on sample repos

### Scenario 2: Breaking Change in PRD-2.6 Spec

**Symptoms:** Widespread failures on PRD-2.6-compliant synthesis files

**Steps:**
1. Assess impact: Which synthesis files fail?
   ```bash
   find hangar-ai-specs -name "*-synthesis.md" -exec aa-jury-gate {} \; 2>&1 | tee gate-audit.log
   ```

2. If widespread (>10% failure rate):
   - **Disable gate in CI/CD:** Set exit code to 0 (warning mode)
     ```yaml
     - run: aa-jury-gate synthesis.md || echo "WARN: Gate failed, continuing"
     ```
   - **Emergency PR:** Fix spec or tool as appropriate
   - **Gradual rollout:** Test on 5 sample repos before full deployment

3. Communication:
   - Notify teams via Slack `#constitution-alerts`
   - Document workaround in `#constitution-faq`

### Scenario 3: Emergency Disable

**Symptoms:** Critical production incident, need immediate disable

**Steps:**
1. **CI/CD:** Comment out `aa-jury-gate` step in pipeline YAML:
   ```yaml
   # DISABLED 2026-05-26: Emergency incident INC-12345
   # - run: aa-jury-gate synthesis.md
   ```

2. **Local:** Uninstall package:
   ```bash
   pip uninstall aa-jury-gate
   ```

3. **Hotfix window:** 4 hours to resolution or full rollback

4. **Communication:**
   - Primary: [Engineering lead] — Slack DM + Email
   - Secondary: [Constitution maintainer] — Slack `#constitution-alerts`
   - Emergency: [On-call SRE] — PagerDuty escalation

### Rollback Verification Checklist

After rollback:
- [ ] Verify gate behavior on 5 sample synthesis files (3 PASS, 2 FAIL expected)
- [ ] Check CI/CD pipelines for unexpected failures
- [ ] Monitor audit logs for 24h (`/var/log/jury-gate/`)
- [ ] Document incident in `docs/incidents/INC-XXXXX.md`
- [ ] Update rollback playbook with lessons learned

---

## 9. Support Contacts

| Role | Contact | Method |
|------|---------|--------|
| **Primary** | Engineering Lead | Slack DM, Email |
| **Secondary** | Constitution Maintainer | Slack `#constitution-support` |
| **Emergency** | On-call SRE | PagerDuty escalation |
| **Documentation** | [GitHub Issues](https://github.com/AAInternal/hangar-ai-constitution/issues) | Bug reports, feature requests |

---

## 10. Appendix: Check Reference

| Check ID | Description | Verdict |
|----------|-------------|---------|
| **S01** | YAML frontmatter present | PASS/FAIL |
| **S02** | `verdict` field present | PASS/FAIL |
| **S03** | YAML parses successfully | ERROR (exit 2) if fail |
| **S04** | Root is dict | PASS/FAIL |
| **S05** | `verdict` is string | PASS/FAIL |
| **S06** | `verdict` in approved list | PASS/FAIL |
| **S07** | `jurors` list present (multi) | PASS/SKIP |
| **S08** | Jurors is list (multi) | PASS/SKIP |
| **S09** | 5 jurors (multi) | PASS/SKIP |
| **S10** | Juror format valid (multi) | PASS/SKIP |
| **S11** | Juror models distinct (multi) | PASS/SKIP |
| **B01** | `round` field present | PASS/FAIL |
| **B02** | `round` value valid | PASS/FAIL |
| **B03** | No `CHALLENGED` verdict | PASS/FAIL |
| **G01** | Git-tracked and clean | PASS/SKIP |

**Legend:**
- **PASS:** Check passed
- **FAIL:** Check failed (exit code 1)
- **SKIP:** Check skipped (e.g., `--allow-no-git` for G01, single-cognition for S07-S11)
- **ERROR:** Tool error (exit code 2, only S03 for YAML parse failure)

---

**Document Version:** 1.0.0  
**Last Updated:** 2026-05-26  
**Tool Version:** aa-jury-gate 1.0.0

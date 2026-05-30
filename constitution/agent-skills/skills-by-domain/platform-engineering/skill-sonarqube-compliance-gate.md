---
skill:
  id: skill-sonarqube-compliance-gate
  name: SonarQube Compliance Gate
  domain: platform-engineering
  laws: [ENG-6.1, ENG-6.4, ENG-6.7, ENG-3.1, ENG-4.6, BUS-7.1]
  triggers:
    - "Run SonarQube gate"
    - "Check compliance metrics"
    - "What does SonarQube say?"
    - "Verify compliance before merge"
    - "SonarQube quality check"
    - "Run compliance radiator"
    - "Check SonarQube before advancing"
    - "Objective compliance check"
  followed_by:
    - skill-09-refactoring         # when code smells or complexity gate fires
    - skill-10-security-review     # when HARD_BLOCK on vulnerabilities fires
    - skill-spec-governance        # to archive gate result as evidence (BUS-7.1)
  version: "1.0.0"
  created: "2026-03-31"
---

# Skill: SonarQube Compliance Gate

> **Purpose:** Replace agent self-assessment of code quality and security with objective, API-verified measures from SonarQube. The same model that introduced a violation cannot be trusted to assess whether it is resolved. SonarQube gates make constitution law thresholds externally authoritative.
> **Workflow:** See `workflows/legacy-rescue-refactor.md` (phases 1/3/4/5/6), `workflows/legacy-rescue-rewrite.md` (phases 1/4/5/6), `workflows/legacy-rescue-decision-track.md` (phases 1/3/6), `workflows/greenfield-development.md` (phases 6/7/8).

---

## Prerequisites

```bash
# User must set these in their shell or CI secrets — NEVER commit
export SONARQUBE_TOKEN=<your-personal-or-ci-token>
export SONARQUBE_URL=https://sonar.your-domain.com
export PROJECT_KEY=<your-sonarqube-project-key>
```

**Guard — always run before any API call:**

```bash
if [ -z "$SONARQUBE_TOKEN" ] || [ -z "$SONARQUBE_URL" ] || [ -z "$PROJECT_KEY" ]; then
  echo "ERROR: SONARQUBE_TOKEN, SONARQUBE_URL, and PROJECT_KEY must be set as environment variables."
  echo "       Never commit token values — set them in your shell or CI/CD secrets."
  exit 1
fi
```

---

## API Call Pattern

```bash
# Fetch all constitution-mapped metrics in a single call
curl -s \
  -H "Authorization: Bearer $SONARQUBE_TOKEN" \
  "$SONARQUBE_URL/api/measures/component\
?component=$PROJECT_KEY\
&metricKeys=vulnerabilities,security_hotspots_reviewed,security_rating,\
security_hotspots,blocker_violations,critical_violations,cognitive_complexity,\
complexity,duplicated_lines_density,code_smells,coverage,new_coverage,\
line_coverage,reliability_rating,bugs,sqale_debt_ratio,ncloc" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); \
    [print(f\"{m['metric']}: {m.get('value','N/A')}\") \
     for m in d.get('component',{}).get('measures',[])]"
```

**Handle API errors:**
- `401 Unauthorized` → token missing, expired, or revoked — rotate via SonarQube admin
- `403 Forbidden` → project access not granted for this token
- `404 Not Found` → wrong `PROJECT_KEY` — verify in SonarQube project settings
- Network timeout → retry with `--max-time 30`; if persistent, check SonarQube server health

**Audit log entry (token-safe — no credential in log):**

```bash
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] SonarQube gate: component=$PROJECT_KEY phase=${PHASE} result=${GATE_RESULT} metric=${METRIC} value=${VALUE} threshold=${THRESHOLD}" >> sonarqube-audit.log
```

---

## Gate Classification

All metrics are classified per `docs/guides/constitution/sonarqube-law-mapping.md`:

### 🚨 HARD_BLOCK (NON-NEGOTIABLE — phase cannot advance)

| Metric | Law | Threshold | Action |
|---|---|---|---|
| `vulnerabilities` | ENG-6.1 | = 0 | Fix all before any phase advance. Invoke `skill-10-security-review`. |
| `security_hotspots_reviewed` | ENG-6.1 | = 100% | Review all hotspots in SonarQube UI. Do not mark as safe without investigation. |
| `security_rating` | ENG-6.1 | = A | All vulnerabilities must be resolved; rating auto-updates. |
| `security_hotspots` (pii-tagged) | ENG-6.4 | = 0 unreviewed | Review every PII-tagged hotspot before phase advance. |
| `blocker_violations` | ENG-6.7 | = 0 | Fix all blocker rule violations. |
| `critical_violations` | ENG-6.1 | = 0 | Fix all Critical-severity issues. **SonarQube Critical ≠ security-only**: includes code quality issues (duplicate literals `S1192`, empty methods `S1186`, wildcard types `S1452`) — fix in Phase 4; cognitive complexity `S3776` — fix in Phase 5. Must be 0 by Phase 5 close. |
| `reliability_rating` | ENG-6.7 | = A (0 bugs) | **Computed from static analysis — no tests needed.** Fix all SonarQube-detected bugs. This condition ensures Phase 1 gate is RED on legacy code. Only turns GREEN after Phase 4 remediation removes all bugs. |

> 🚨 **If any HARD_BLOCK metric is violated: stop. Do not advance the workflow phase. Do not override. Fix the violation and re-run this gate.**

### 🔴 PHASE_GATE (must meet threshold to advance; exception requires written justification)

| Metric | Law | Threshold | Exception path |
|---|---|---|---|
| `coverage` | ENG-4.6 | ≥ 80% | Named approver + justification in `hangar-ai-specs/changes/[id]/` |
| `new_coverage` | ENG-4.6 | ≥ 90% (new code) | Same — invoke `skill-06-atomic-tdd` to add missing tests |
| `line_coverage` | ENG-4.6 | ≥ 80% | Same |
| `new_reliability_rating` | BUS-7.1 | = A (0 new bugs) | New code must not introduce bugs — `new_reliability_rating` must be A |
| `bugs` | correctness | = 0 (Certify) | Same — fix bugs before certifying |

> **Note on Phase 1:** When the first scan has no test coverage data (no tests yet), `coverage` may be N/A and the condition is **skipped** by SonarQube. The `reliability_rating` HARD_BLOCK (HB-5) is the reliable Phase 1 fail signal because it is computed from static analysis, not test execution.

### ⚠️ WARNING (visible; does not block; must trend downward)

| Metric | Law | Target | Action |
|---|---|---|---|
| `cognitive_complexity` (per fn) | ENG-3.1 | ≤ 10 | Log warning; invoke `skill-09-refactoring` if > 10 |
| `complexity` (cyclomatic, per fn) | ENG-3.1 | ≤ 10 | Same |
| `duplicated_lines_density` | ENG-3.1 | ≤ 3% | Log warning; reduce duplication per phase |
| `code_smells` | ENG-3.1 | Δ ≤ 0 per phase | Smells must not increase phase-over-phase |

### 📊 RADIATOR (always shown; never blocks)

| Metric | Purpose |
|---|---|
| `sqale_debt_ratio` | Tech debt as % of build cost — team visibility |
| `ncloc` | Lines of code — growth trend awareness |

---

## Evidence Artifacts

After each gate run, persist results using the templates in `docs/templates/`:

| Gate event | Template | Trigger |
|---|---|---|
| Phase 1 baseline snapshot | `docs/templates/sonarqube-baseline.md` | First run on project |
| Mid-workflow phase gate | `docs/templates/sonarqube-gate.md` | Each phase gate check |
| Certify phase final delta | `docs/templates/sonarqube-delta.md` | Final phase before archive |

Store artifacts in `hangar-ai-specs/changes/[proposal-id]/evidence/` per BUS-7.1.

---

## Integration Checklist

Before invoking this skill, confirm:

- [ ] `SONARQUBE_TOKEN` set in shell/CI (not committed)
- [ ] `SONARQUBE_URL` set in shell/CI (not committed)
- [ ] `PROJECT_KEY` known (check SonarQube project settings)
- [ ] SonarQube scan has run on the current branch/commit
- [ ] You know the workflow phase you are gating

After gate result:

- [ ] If 🚨 HARD_BLOCK: stop; fix; do not advance phase
- [ ] If 🔴 PHASE_GATE failure: either fix or get named approval + write justification
- [ ] Log result with `echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ..."` to audit log (BUS-7.1)
- [ ] Save gate artifact to `hangar-ai-specs/changes/[id]/evidence/`

---

## Common Failure Patterns

| SonarQube finding | Constitution law | Remediation |
|---|---|---|
| New vulnerability (OWASP Top 10) | ENG-6.1 HARD_BLOCK | Invoke `skill-10-security-review`; fix before any other work |
| Unreviewed security hotspot | ENG-6.1 HARD_BLOCK | Review in SonarQube UI; document disposition in evidence artifact |
| `new_coverage` < 90% | ENG-4.6 PHASE_GATE | Invoke `skill-06-atomic-tdd`; add tests for uncovered lines |
| Cognitive complexity > 10 | ENG-3.1 WARNING | Invoke `skill-09-refactoring`; extract methods/strategies |
| Duplicated block | ENG-3.1 WARNING | Extract shared function/module in refactor phase |
| Blocker rule violation | ENG-6.7 HARD_BLOCK | Fix rule violation; re-run scan to verify resolution |
| `reliability_rating` > A (bugs present) | ENG-6.7 HARD_BLOCK | Fix all SonarQube-detected bugs. **In Legacy Rescue Phase 1 this is EXPECTED — document as baseline. Must be resolved before Phase 5 gate.** Static analysis only — no tests needed for detection. |
| Phase 1 gate is GREEN unexpectedly | ENG-12.1 | Verify Hangar AI Constitution Gate v1.2.0+ is assigned (not "Sonar Way"). Run `./tools/sonarqube-gate/provision.sh --project-key=<key>` and re-scan. |

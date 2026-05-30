# SonarQube Baseline Snapshot

> **Template:** `docs/templates/sonarqube-baseline.md`  
> **When to use:** Phase 1 of any legacy rescue workflow, or start of Phase 6 (Build) in greenfield development.  
> **Storage:** `hangar-ai-specs/changes/[proposal-id]/evidence/sonarqube-baseline.md`

---

## Project Information

| Field | Value |
|---|---|
| **Project Key** | `<PROJECT_KEY>` |
| **SONARQUBE_URL** | `<set via $SONARQUBE_URL env var — never commit literal URL if internal>` |
| **Scan Date** | `YYYY-MM-DDTHH:MM:SSZ` |
| **Git Commit** | `<sha>` |
| **Branch** | `<branch-name>` |
| **Workflow** | `<legacy-rescue-refactor / legacy-rescue-rewrite / legacy-rescue-decision-track / greenfield-development>` |
| **Phase** | `Phase 1 — Assess / Archaeology` |
| **Bounded Context** | `<context name if per-context baseline>` |

---

## Baseline Metrics

| SonarQube Metric | Value | Law | Gate Type | Threshold | Status |
|---|---|---|---|---|---|
| `vulnerabilities` | — | ENG-6.1 | 🚨 HARD_BLOCK | = 0 | — |
| `security_hotspots_reviewed` | — | ENG-6.1 | 🚨 HARD_BLOCK | = 100% | — |
| `security_rating` | — | ENG-6.1 | 🚨 HARD_BLOCK | = A | — |
| `security_hotspots` | — | ENG-6.4 | 🚨 HARD_BLOCK | = 0 unreviewed | — |
| `blocker_violations` | — | ENG-6.7 | 🚨 HARD_BLOCK | = 0 | — |
| `coverage` | — | ENG-4.6 | 🔴 PHASE_GATE | ≥ 80% | — |
| `new_coverage` | — | ENG-4.6 | 🔴 PHASE_GATE | ≥ 90% | — |
| `line_coverage` | — | ENG-4.6 | 🔴 PHASE_GATE | ≥ 80% | — |
| `critical_violations` | — | BUS-7.1 | 🔴 PHASE_GATE | = 0 | — |
| `reliability_rating` | — | BUS-7.1 | 🔴 PHASE_GATE | = A | — |
| `bugs` | — | correctness | 🔴 PHASE_GATE | = 0 (Certify) | — |
| `cognitive_complexity` | — | ENG-3.1 | ⚠️ WARNING | ≤ 10/fn | — |
| `complexity` | — | ENG-3.1 | ⚠️ WARNING | ≤ 10/fn | — |
| `duplicated_lines_density` | — | ENG-3.1 | ⚠️ WARNING | ≤ 3% | — |
| `code_smells` | — | ENG-3.1 | ⚠️ WARNING | Δ ≤ 0 | — |
| `sqale_debt_ratio` | — | — | 📊 RADIATOR | — | — |
| `ncloc` | — | — | 📊 RADIATOR | — | — |

---

## Law Compliance Status at Baseline

| Law | Compliant at Baseline? | Notes |
|---|---|---|
| ENG-6.1 — Security by Design | ✅ / ❌ | |
| ENG-6.4 — PII / Sensitive Data | ✅ / ❌ | |
| ENG-6.7 — Audit Trail | ✅ / ❌ | |
| ENG-4.6 — Coverage | ✅ / ❌ | |
| ENG-3.1 — Complexity | ✅ / ❌ | |
| BUS-7.1 — Compliance Evidence | ✅ / ❌ | |

---

## Fetch Command

```bash
# Set env vars in your shell (never commit)
# export SONARQUBE_TOKEN=<your-token>
# export SONARQUBE_URL=https://sonar.your-domain.com

if [ -z "$SONARQUBE_TOKEN" ] || [ -z "$SONARQUBE_URL" ]; then
  echo "ERROR: SONARQUBE_TOKEN and SONARQUBE_URL must be set as environment variables"
  exit 1
fi

curl -s \
  -H "Authorization: Bearer $SONARQUBE_TOKEN" \
  "$SONARQUBE_URL/api/measures/component?component=${PROJECT_KEY}&metricKeys=vulnerabilities,security_hotspots_reviewed,security_rating,security_hotspots,blocker_violations,critical_violations,cognitive_complexity,complexity,duplicated_lines_density,code_smells,coverage,new_coverage,line_coverage,reliability_rating,bugs,sqale_debt_ratio,ncloc"
```

---

## Notes

_Add any observations about the baseline state, known legacy debt, or compliance risks identified during Phase 1._

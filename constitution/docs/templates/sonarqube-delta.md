# SonarQube Certify Delta Report

> **Template:** `docs/templates/sonarqube-delta.md`  
> **When to use:** Final Certify phase of any workflow — compares current state against Phase 1 baseline.  
> **Storage:** `hangar-ai-specs/changes/[proposal-id]/evidence/sonarqube-delta.md`

---

## Delta Context

| Field | Value |
|---|---|
| **Project Key** | `<PROJECT_KEY>` |
| **Certify Scan Date** | `YYYY-MM-DDTHH:MM:SSZ` |
| **Certify Git Commit** | `<sha>` |
| **Baseline Scan Date** | `<from sonarqube-baseline.md>` |
| **Baseline Git Commit** | `<sha>` |
| **Workflow** | `<workflow-id>` |
| **Proposal** | `hangar-ai-specs/changes/<proposal-id>/` |

---

## Metrics Delta

| Metric | Law | Gate Type | Before | After | Delta | Threshold | Final Status |
|---|---|---|---|---|---|---|---|
| `vulnerabilities` | ENG-6.1 | 🚨 HARD_BLOCK | — | — | — | = 0 | ✅ / 🚨 |
| `security_hotspots_reviewed` | ENG-6.1 | 🚨 HARD_BLOCK | — | — | — | = 100% | ✅ / 🚨 |
| `security_rating` | ENG-6.1 | 🚨 HARD_BLOCK | — | — | — | = A | ✅ / 🚨 |
| `security_hotspots` (pii) | ENG-6.4 | 🚨 HARD_BLOCK | — | — | — | = 0 unreviewed | ✅ / 🚨 |
| `blocker_violations` | ENG-6.7 | 🚨 HARD_BLOCK | — | — | — | = 0 | ✅ / 🚨 |
| `coverage` | ENG-4.6 | 🔴 PHASE_GATE | — | — | **+?%** | ≥ 80% | ✅ / 🔴 |
| `new_coverage` | ENG-4.6 | 🔴 PHASE_GATE | — | — | — | ≥ 90% | ✅ / 🔴 |
| `line_coverage` | ENG-4.6 | 🔴 PHASE_GATE | — | — | **+?%** | ≥ 80% | ✅ / 🔴 |
| `critical_violations` | BUS-7.1 | 🔴 PHASE_GATE | — | — | — | = 0 | ✅ / 🔴 |
| `reliability_rating` | BUS-7.1 | 🔴 PHASE_GATE | — | — | — | = A | ✅ / 🔴 |
| `bugs` | correctness | 🔴 PHASE_GATE | — | — | — | = 0 | ✅ / 🔴 |
| `cognitive_complexity` | ENG-3.1 | ⚠️ WARNING | — | — | — | ≤ 10/fn | ✅ / ⚠️ |
| `complexity` | ENG-3.1 | ⚠️ WARNING | — | — | — | ≤ 10/fn | ✅ / ⚠️ |
| `duplicated_lines_density` | ENG-3.1 | ⚠️ WARNING | — | — | — | ≤ 3% | ✅ / ⚠️ |
| `code_smells` | ENG-3.1 | ⚠️ WARNING | — | — | — | Δ ≤ 0 | ✅ / ⚠️ |
| `sqale_debt_ratio` | — | 📊 RADIATOR | — | — | — | — | — |
| `ncloc` | — | 📊 RADIATOR | — | — | — | — | — |

---

## Law Compliance Change Summary

| Law | Before | After | Improvement |
|---|---|---|---|
| ENG-6.1 — Security by Design | ✅/❌ | ✅/❌ | |
| ENG-6.4 — PII / Sensitive Data | ✅/❌ | ✅/❌ | |
| ENG-6.7 — Audit Trail | ✅/❌ | ✅/❌ | |
| ENG-4.6 — Coverage | ✅/❌ | ✅/❌ | |
| ENG-3.1 — Complexity | ✅/❌ | ✅/❌ | |
| BUS-7.1 — Compliance Evidence | ✅/❌ | ✅/❌ | |

---

## Certify Verdict

> **🚨 HARD_BLOCK metrics at threshold: ✅ YES / ❌ NO**  
> **🔴 PHASE_GATE metrics at threshold: ✅ YES / ❌ NO**  
> **Overall certify: ✅ CERTIFIED / 🚨 BLOCKED**

_If any HARD_BLOCK metric is not at threshold, certification cannot proceed._

---

## Audit Log Entry

```
[YYYY-MM-DDTHH:MM:SSZ] SonarQube certify-delta: component=<PROJECT_KEY> proposal=<proposal-id> result=<CERTIFIED|BLOCKED> coverage_delta=+?% vulnerabilities_before=? vulnerabilities_after=0
```

---

## Notes

_Add narrative summary of compliance improvement achieved during this proposal._

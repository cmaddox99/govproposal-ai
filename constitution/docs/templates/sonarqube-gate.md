# SonarQube Phase Gate Result

> **Template:** `docs/templates/sonarqube-gate.md`  
> **When to use:** Each phase gate check (Phase 3, 4, 5, 6, 7, 8 depending on workflow).  
> **Storage:** `hangar-ai-specs/changes/[proposal-id]/evidence/sonarqube-gate-phase-[N].md`

---

## Gate Context

| Field | Value |
|---|---|
| **Project Key** | `<PROJECT_KEY>` |
| **Scan Date** | `YYYY-MM-DDTHH:MM:SSZ` |
| **Git Commit** | `<sha>` |
| **Branch** | `<branch-name>` |
| **Workflow** | `<workflow-id>` |
| **Phase** | `Phase N — <Phase Name>` |
| **Triggered By** | `<agent/engineer name>` |

---

## Gate Verdict

> **Overall result: ✅ PASS / 🚨 HARD_BLOCK / 🔴 PHASE_GATE FAIL**

_Replace with actual verdict. If HARD_BLOCK or PHASE_GATE FAIL, workflow phase cannot advance._

---

## Metric Results

| Metric | Law | Gate Type | Threshold | Actual Value | Result |
|---|---|---|---|---|---|
| `vulnerabilities` | ENG-6.1 | 🚨 HARD_BLOCK | = 0 | — | ✅ / 🚨 |
| `security_hotspots_reviewed` | ENG-6.1 | 🚨 HARD_BLOCK | = 100% | — | ✅ / 🚨 |
| `security_rating` | ENG-6.1 | 🚨 HARD_BLOCK | = A | — | ✅ / 🚨 |
| `security_hotspots` (pii) | ENG-6.4 | 🚨 HARD_BLOCK | = 0 unreviewed | — | ✅ / 🚨 |
| `blocker_violations` | ENG-6.7 | 🚨 HARD_BLOCK | = 0 | — | ✅ / 🚨 |
| `coverage` | ENG-4.6 | 🔴 PHASE_GATE | ≥ 80% | — | ✅ / 🔴 |
| `new_coverage` | ENG-4.6 | 🔴 PHASE_GATE | ≥ 90% | — | ✅ / 🔴 |
| `critical_violations` | BUS-7.1 | 🔴 PHASE_GATE | = 0 | — | ✅ / 🔴 |
| `reliability_rating` | BUS-7.1 | 🔴 PHASE_GATE | = A | — | ✅ / 🔴 |
| `cognitive_complexity` | ENG-3.1 | ⚠️ WARNING | ≤ 10/fn | — | ✅ / ⚠️ |
| `code_smells` | ENG-3.1 | ⚠️ WARNING | Δ ≤ 0 | — | ✅ / ⚠️ |
| `duplicated_lines_density` | ENG-3.1 | ⚠️ WARNING | ≤ 3% | — | ✅ / ⚠️ |

---

## Blocking Issues (if any)

_List all 🚨 HARD_BLOCK and 🔴 PHASE_GATE failures. Phase cannot advance until resolved._

| Issue | Metric | Actual | Required | Remediation Skill |
|---|---|---|---|---|
| — | — | — | — | — |

---

## Exception Record (PHASE_GATE only — requires named approver)

> If advancing despite a PHASE_GATE failure, document here. HARD_BLOCK exceptions are not permitted.

| Metric | Actual value | Approver | Justification | Date |
|---|---|---|---|---|
| — | — | — | — | — |

---

## Audit Log Entry

```
[YYYY-MM-DDTHH:MM:SSZ] SonarQube gate: component=<PROJECT_KEY> phase=Phase-N result=<PASS|HARD_BLOCK|PHASE_GATE_FAIL> triggered_by=<name>
```

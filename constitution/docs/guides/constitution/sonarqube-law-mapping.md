# SonarQube ↔ Constitution Law Mapping

> **Version:** 1.0.0 — 2026-03-31  
> **Change control:** Updates to this mapping require a governance review (`govern_task` at `define` phase).  
> **Purpose:** Authoritative reference for all workflow phase gates and the `skill-sonarqube-compliance-gate`.  
> **Token handling:** `SONARQUBE_TOKEN` and `SONARQUBE_URL` are **always** user-provided environment variables. They must **never** appear as literal values in any committed file.

---

## Gate Classification Definitions

| Classification | Symbol | Meaning | Workflow behavior |
|---|---|---|---|
| **HARD_BLOCK** | 🚨 | Law is NON-NEGOTIABLE. Gate cannot pass while metric is violated. | Phase **cannot advance**. Workflow stops until metric threshold is met. No exception permitted. |
| **PHASE_GATE** | 🔴 | Law requires objective threshold. Gate blocks phase progression. | Phase **must not advance** until threshold met. Exception requires named approver + written justification in `hangar-ai-specs/`. |
| **WARNING** | ⚠️ | Law recommends improvement. Metric visible but does not block. | Phase **may advance** with warning logged. Metric must trend downward per-phase. |
| **RADIATOR** | 📊 | Visibility metric. No threshold — team awareness only. | Always shown. Never blocks. |

---

## Law → SonarQube Metric Mapping Table

| Law ID | Law Name | SonarQube Metric Key(s) | Threshold | Gate Type | Remediation Skill |
|---|---|---|---|---|---|
| **ENG-6.1** | Security by Design (NON-NEGOTIABLE) | `vulnerabilities` | = 0 | 🚨 HARD_BLOCK | `skill-10-security-review` |
| **ENG-6.1** | Security by Design (NON-NEGOTIABLE) | `security_hotspots_reviewed` | = 100% | 🚨 HARD_BLOCK | `skill-10-security-review` |
| **ENG-6.1** | Security by Design (NON-NEGOTIABLE) | `security_rating` | = A | 🚨 HARD_BLOCK | `skill-10-security-review` |
| **ENG-6.4** | PII & Sensitive Data (NON-NEGOTIABLE) | `security_hotspots` (tagged `pii`) | = 0 unreviewed | 🚨 HARD_BLOCK | `skill-10-security-review` |
| **ENG-6.7** | Audit Trail (NON-NEGOTIABLE) | `blocker_violations` | = 0 | 🚨 HARD_BLOCK | `skill-spec-governance` |
| **ENG-3.1** | Complexity Limits | `cognitive_complexity` (per function) | ≤ 10 | ⚠️ WARNING | `skill-09-refactoring` |
| **ENG-3.1** | Complexity Limits | `complexity` (cyclomatic, per function) | ≤ 10 | ⚠️ WARNING | `skill-09-refactoring` |
| **ENG-3.1** | Complexity Limits | `duplicated_lines_density` | ≤ 3% | ⚠️ WARNING | `skill-09-refactoring` |
| **ENG-3.1** | Complexity Limits | `code_smells` | Δ ≤ 0 per phase | ⚠️ WARNING | `skill-09-refactoring` |
| **ENG-4.6** | Coverage Requirements | `coverage` (overall) | ≥ 80% | 🔴 PHASE_GATE | `skill-06-atomic-tdd` |
| **ENG-4.6** | Coverage Requirements | `new_coverage` (new code) | ≥ 90% | 🔴 PHASE_GATE | `skill-06-atomic-tdd` |
| **ENG-4.6** | Coverage Requirements | `line_coverage` | ≥ 80% | 🔴 PHASE_GATE | `skill-06-atomic-tdd` |
| **ENG-4.11** | Mutation Testing (general code) | `mutation_score` | ≥ 70% | 🔴 PHASE_GATE | `skill-11-mutation-testing` |
| **ENG-4.11** | Mutation Testing (critical paths) | `mutation_score` (critical) | ≥ 85% | 🚨 HARD_BLOCK | `skill-11-mutation-testing` |
| **ENG-4.11** | Mutation Testing (equivalent mutants) | `equivalent_mutant_ratio` | ≤ 10% | ⚠️ WARNING | `skill-11-mutation-testing` |
| **BUS-7.1** | Compliance Evidence | `critical_violations` | = 0 | 🔴 PHASE_GATE | `skill-spec-governance` |
| **BUS-7.1** | Compliance Evidence | `reliability_rating` | = A | 🔴 PHASE_GATE | `skill-09-refactoring` |
| **ENG-3.1** (drift) | Complexity Limits (delta) | `bugs` | = 0 (Certify phase) | 🔴 PHASE_GATE | `skill-09-refactoring` |
| — | Visibility | `sqale_debt_ratio` (tech debt ratio) | — | 📊 RADIATOR | — |
| — | Visibility | `ncloc` (lines of code) | — | 📊 RADIATOR | — |

---

## SonarQube API Call Pattern

```bash
# Environment variables — NEVER commit literal values
# User provides: export SONARQUBE_TOKEN=<your-token>
# User provides: export SONARQUBE_URL=https://sonar.example.com

curl -s \
  -H "Authorization: Bearer $SONARQUBE_TOKEN" \
  "$SONARQUBE_URL/api/measures/component\
?component=$PROJECT_KEY\
&metricKeys=vulnerabilities,security_hotspots_reviewed,security_rating,\
security_hotspots,blocker_violations,critical_violations,cognitive_complexity,\
complexity,duplicated_lines_density,code_smells,coverage,new_coverage,\
line_coverage,reliability_rating,bugs,sqale_debt_ratio,ncloc"
```

**Guard pattern (required in all invocations):**

```bash
if [ -z "$SONARQUBE_TOKEN" ] || [ -z "$SONARQUBE_URL" ]; then
  echo "ERROR: SONARQUBE_TOKEN and SONARQUBE_URL must be set as environment variables"
  echo "       Never commit these values — set them in your shell or CI secrets"
  exit 1
fi
```

**Audit log entry (token-safe — no credential in log):**

```
[2026-03-31T14:00:00Z] SonarQube gate: component=my-project phase=Phase-4 result=HARD_BLOCK metric=vulnerabilities value=2 threshold=0
```

---

## Per-Phase Gate Schedule

### `legacy-rescue-refactor`
| Phase | Gate type | Metrics checked | Pass condition |
|---|---|---|---|
| 1 — Assess | 📊 RADIATOR (baseline) | All metrics | Snapshot captured in `sonarqube-baseline.md` |
| 3 — Characterize | 🔴 PHASE_GATE | `coverage`, `line_coverage`, `mutation_score` | `coverage` ≥ 50%; `mutation_score` ≥ 70% (ENG-4.11) |
| 4 — Remediate | 🚨 HARD_BLOCK | `vulnerabilities`, `security_hotspots_reviewed`, `security_rating` | All three at threshold |
| 5 — Refactor | ⚠️ WARNING + 🔴 PHASE_GATE | `cognitive_complexity`, `code_smells`, `coverage`, `mutation_score` | `coverage` ≥ 80%; `mutation_score` ≥ 70%; complexity trend ↓ |
| 6 — Certify | 🚨 HARD_BLOCK + 🔴 PHASE_GATE | All mapped metrics | Critical paths `mutation_score` ≥ 85% (ENG-4.11 HARD_BLOCK); other thresholds met; delta in `sonarqube-delta.md` |

### `legacy-rescue-rewrite`
| Phase | Gate type | Metrics checked | Pass condition |
|---|---|---|---|
| 1 — Assess | 📊 RADIATOR (baseline) | All metrics | Snapshot captured |
| 4 — Build | 🚨 HARD_BLOCK + 🔴 PHASE_GATE | `vulnerabilities`, `security_rating`, `new_coverage`, `mutation_score` | Per-cycle: `new_coverage` ≥ 90%; `mutation_score` ≥ 70% (ENG-4.11) |
| 5 — Validate Parity | 🔴 PHASE_GATE | `coverage`, `bugs`, `reliability_rating`, `mutation_score` | `coverage` ≥ 80%; `bugs` = 0; `mutation_score` ≥ 70% |
| 6 — Certify | All gates | All mapped metrics | Critical paths `mutation_score` ≥ 85% (ENG-4.11 HARD_BLOCK); full delta report vs. Phase 1 baseline |

### `legacy-rescue-decision-track`
| Phase | Gate type | Metrics checked | Pass condition |
|---|---|---|---|
| 1 — Archaeology | 📊 RADIATOR (per-context baseline) | All metrics per bounded context | Baseline per context in `sonarqube-baseline.md` |
| 3 — Deliberate | 📊 RADIATOR → decision input | `cognitive_complexity`, `coverage`, `code_smells`, `duplicated_lines_density`, `mutation_score` | Metrics feed REFACTOR/REWRITE decision: complexity>10 → REWRITE signal; coverage<50% → REWRITE signal; low mutation_score informs refactoring depth |
| 6 — Certify | 🔴 PHASE_GATE | `coverage`, `blocker_violations`, `reliability_rating`, `mutation_score` | General code `mutation_score` ≥ 70%; critical paths ≥ 85% (ENG-4.11); delta vs. baseline proves improvement |

### `greenfield-development`
| Phase | Gate type | Metrics checked | Pass condition |
|---|---|---|---|
| 6 — Build | 🔴 PHASE_GATE (per vertical slice) | `new_coverage`, `bugs`, `mutation_score` | `new_coverage` ≥ 90%; `mutation_score` ≥ 70% on each slice (ENG-4.11) |
| 7 — Review | 🚨 HARD_BLOCK | `vulnerabilities`, `security_hotspots_reviewed`, `security_rating`, `mutation_score` (critical paths) | All security gates at threshold; critical path `mutation_score` ≥ 85% (ENG-4.11 HARD_BLOCK) |
| 8 — Ship | All gates | All mapped metrics | Full gate result in `sonarqube-gate.md`; delta vs. Phase 6 start; mutation test evidence in `sonarqube-delta.md` |

---

## Non-Negotiable Law Enforcement

The following laws are **NON-NEGOTIABLE** in the constitution. Their SonarQube mappings are **HARD_BLOCK** — no exception, no override, no phase advancement while violated:

| Law | NON-NEGOTIABLE requirement | SonarQube enforcement |
|---|---|---|
| **ENG-6.1** | Zero security vulnerabilities; all hotspots reviewed | `vulnerabilities=0`, `security_hotspots_reviewed=100%`, `security_rating=A` |
| **ENG-6.4** | No unreviewed PII-tagged hotspots | `security_hotspots` (pii-tagged) = 0 unreviewed |
| **ENG-6.7** | Zero blocker violations in audit trail | `blocker_violations=0` |
| **ENG-4.1** | Test-first — new code must have coverage | `new_coverage≥90%` at build phase (PHASE_GATE, escalates to HARD_BLOCK at Certify) |
| **ENG-4.11** | Critical path mutation effectiveness | `mutation_score` (critical paths) ≥ 85%; crew scheduling, dispatch safety, maintenance compliance (HARD_BLOCK non-negotiable) |

---

## Change Control

Any change to this mapping (adding laws, changing thresholds, reclassifying gate types) requires:
1. `govern_task` at `define` phase citing the law being changed
2. Approval from reviewer + sentinel roles
3. Version field incremented in this file header
4. PROGRESS.md entry in the affected proposal

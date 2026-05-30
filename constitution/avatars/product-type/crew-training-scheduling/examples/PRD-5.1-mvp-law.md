---
law_id: PRD-5.1
avatar: crew-training-scheduling
---

# PRD-5.1: MVP Law Examples for Crew Training Scheduling

> **Law:** MVPs SHALL be the smallest experiment to validate learning — not a crappy first
> version and not a fully-featured product. For optimization engines, the MVP is the
> smallest set of capabilities that proves the core hypothesis.

---

## COMPLIANT: MVP Definition for JOSE

```markdown
## JOSE MVP — Core Hypothesis Validation

### Hypothesis
An automated MIP-based optimizer can recover open blocked sequences faster and
at lower cost than the current manual scheduling process.

### Riskiest Assumption
Schedulers will trust and act on machine-generated recommendations for pilot
training assignments — a safety-adjacent scheduling decision.

### MVP Scope (minimum to test the hypothesis)

✅ IN — required to test the hypothesis:
  - Fetch student schedules from FSA API
  - Generate feasible options (constraint-respecting permutations)
  - Solve MIP model with standard scoring profile
  - Produce SolutionRecommendation.xlsx with before/after schedules
  - Respect the 6-day freeze window (scheduler safety requirement)
  - Log solver status and objective value (trust + reproducibility)

❌ OUT — not required to test the hypothesis:
  - Email notification (scheduler can check Blob Storage manually)
  - Sequential open-blkd-seq run (enhancement)
  - Limited-moves variant (enhancement)
  - Tableau dashboard (enhancement — manual Excel review is sufficient to test trust)
  - Teams notifications (enhancement)
  - QLA integration (enhancement)

### Success Metric
≥ 2 schedulers accept optimizer recommendations for ≥ 3 consecutive runs
without fully overriding them.

### Timeline
4-week pilot with 320 fleet at DFW base.
```

**Why compliant:** The MVP contains exactly what is needed to test whether schedulers will trust machine recommendations. Everything else is an enhancement that adds complexity without testing the hypothesis. Per PRD-5.1, MVP is the smallest experiment — not the smallest product.

---

## COMPLIANT: Incremental Feature Hypothesis After MVP

```markdown
## Feature Hypothesis: Limited-Moves Run

### Context
MVP validated: schedulers accept recommendations. Now we want to improve
solution stability — reduce the number of students who move each run.

### Hypothesis
A second solver pass with a restrictMoves constraint will produce solutions
that are easier for schedulers to review and approve, reducing review time
by ≥ 25%.

### MVP for this Feature
- Add `restrictMoves: true` config flag
- Add `limitedMoves` scoring profile (disincentivises large swaps)
- Run solver twice: standard pass first, then limited-moves pass
- Report both solutions in SelectedStudentOptions.xlsx

### Success Metric
Scheduler review time per run < 15 minutes (baseline: 25 minutes measured
over last 6 runs).

### What We're NOT Building Yet
- Configurable move limit per student (enhancement — limit count is fine for now)
- Per-base move restrictions (enhancement)
```

**Why compliant:** Each new feature gets its own MVP hypothesis. The limited-moves run is validated by a time-to-review metric before the move-limit-per-student enhancement is considered.

---

## VIOLATION: Building Full Feature Set Before Validating Core Hypothesis

```markdown
## VIOLATES PRD-5.1 — Big-Bang Feature Plan

Sprint 1: FSA API integration + CCS API integration
Sprint 2: Option generation algorithm (full constraint set)
Sprint 3: MIP model (all 3 constraints + objective)
Sprint 4: Standard + limitedMoves + experimental scoring profiles
Sprint 5: Sequential run mode
Sprint 6: SolutionRecommendation + SelectedStudentOptions Excel output
Sprint 7: Email notifications + Teams integration
Sprint 8: Tableau dashboard integration via Mosaic
Sprint 9: QLA integration for legal validation
Sprint 10: Pilot with schedulers

Estimated: 10 sprints (5 months) before first user validation
```

**Why violates PRD-5.1:** The riskiest assumption — "will schedulers trust the recommendations?" — is not tested until sprint 10. Five months of development could be wasted if schedulers reject the concept. Per PRD-5.1, validate the riskiest assumption first with the smallest possible build.

**Correct approach:** Run the MVP (sprints 1-4 above reduced to bare essentials) with one base, one fleet, and a manual Excel handoff in 4-6 weeks. Validate trust before building notifications, dashboards, and QLA integration.

---

## COMPLIANT: MVP Instrumentation (Per PRD-5.2 Build-Measure-Learn)

```markdown
## Instrumentation Plan — MVP Metrics

To measure whether the hypothesis is validated, capture per run:

| Metric | How Captured | Target |
|--------|-------------|--------|
| Solution acceptance rate | Manual survey post-run (5 min) | ≥ 60% accepted |
| Override count per run | Scheduler feedback form | < 3 overrides/run |
| Time to review | Scheduler self-report | < 20 min/run |
| Open blkd seq saved | Metrics sheet (automated) | ≥ 50% of available |
| Run-to-delivery time | Timestamp in logs | < 10 minutes |

Without this instrumentation, we cannot determine if the MVP validated
the hypothesis or not. Per PRD-5.2, BUILD without MEASURE is waste.
```

**Why compliant:** Instrumentation is defined before the MVP is built. Success criteria are specific and measurable, not qualitative. This closes the Build-Measure-Learn loop.


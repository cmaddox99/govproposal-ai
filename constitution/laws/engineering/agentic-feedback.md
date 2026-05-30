---
domain: engineering
article: XII
title: Agentic Compliance Feedback Loop Laws
laws:
  - id: ENG-12.1
    title: Agentic Phase Gate Law
    non_negotiable: true
    summary: Each phase transition MUST produce jury-validated evidence artifacts reviewed by a human before the agent advances; jury synthesis verdict is the gate — agent cannot self-declare phase complete
  - id: ENG-12.2
    title: Human-First Evidence Review Law
    summary: Phase evidence artifacts (jury synthesis, coverage reports, mutation results) MUST be presented for human review before phase transition; human exercises judgment on jury findings
  - id: ENG-12.3
    title: Multi-Cognition Jury Referee Law
    summary: The authoring LLM cannot self-certify compliance; the multi-cognition jury (PRD-2.6 — 5 jurors with distinct LLM models) provides the external referee function — different model substrate cannot be gamed by the authoring model
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article XII: Agentic Compliance Feedback Loop Laws

> The multi-cognition jury is the human-in-the-loop contract for agentic development.  
> The agent does the work. The jury deliberates with rigor. The human reviews and approves.  
> These laws make that contract non-negotiable.

---

## ENG-12.1: Agentic Phase Gate Law

**Law ID:** `ENG-12.1` | **Status:** NON-NEGOTIABLE

Each phase gate MUST produce jury-validated evidence artifacts that a human reviews and approves before the agent advances to the next phase.

1. **Before each phase transition:** Agent produces a phase artifact (capture, define, design, plan, build evidence, etc.)
2. **Jury deliberation:** Multi-cognition jury (PRD-2.6 — 5 jurors, 2 rounds) deliberates on the artifact; judicial synthesizer renders verdict
3. **Jury APPROVED verdict is required** before human is asked to approve phase advance
4. **Human reviews jury synthesis findings** — jury rationale, contested findings, corrections applied — before approving phase advance
5. **Agent cannot advance** if judicial synthesis is REJECTED, regardless of the agent's own assessment

```
Phase Gate Flow (ENG-12.1):
  Agent produces phase artifact
    → aa-citation-audit runs (ENG-14.1 — pre-jury citation gate)
    → Multi-cognition jury R1 deliberates (PRD-2.6)
    → Corrections applied
    → Multi-cognition jury R2 deliberates
    → Judicial synthesis renders APPROVED | REJECTED
    → HUMAN reviews synthesis findings ← THE CHECKPOINT
    → Human approves phase advance
    → Agent proceeds to next phase
```

> **Why:** The jury synthesis is not a rubber stamp. Five distinct LLM models (PRD-2.6) each apply independent judgment across different cognitive lenses. Their convergence — or contestation — is the signal the human reviews. Human judgment is exercised on evidence, not on the agent's assertions.

| Trigger | Required Human Action |
|---|---|
| Phase artifact complete | Review jury synthesis findings before approving advance |
| Judicial synthesis REJECTED | Human must direct corrections before re-jury |
| Contested finding in synthesis | Human resolves with explicit decision |
| Phase 8 Ship | Human APPROVE gate on final evidence + Article XIV merge |

---

## ENG-12.2: Human-First Evidence Review Law

**Law ID:** `ENG-12.2`

Phase evidence artifacts MUST be available for human review before phase transition. The human exercises judgment — not the agent.

1. **Phase artifact committed** to `hangar-ai-specs/changes/` before jury is invoked
2. **Jury synthesis committed** after APPROVED verdict — human can inspect git history
3. **Coverage and mutation evidence** (pytest-cov ≥90%, mutmut ≥85% on critical modules) committed as part of Phase 6 Build slice evidence before jury advance
4. **Human reviews evidence artifacts** — jury synthesis, coverage report, mutation score — before approving each phase gate

```
Evidence Review Checklist (per phase):
  [ ] Phase artifact committed to hangar-ai-specs/changes/
  [ ] Jury synthesis verdict: APPROVED
  [ ] Contested findings resolved (if any)
  [ ] Phase 6 slices: pytest-cov report + mutmut score committed
  [ ] Human has read jury synthesis before approving
```

> **Why:** Evidence-based governance. The human does not need a dashboard to stay in the loop — they need the jury synthesis in front of them. Git history + jury artifacts IS the audit trail.

---

## ENG-12.3: Multi-Cognition Jury Referee Law

**Law ID:** `ENG-12.3`

The authoring LLM cannot self-certify compliance. The multi-cognition jury (PRD-2.6) provides the external referee function — distinct model substrate prevents self-certification.

1. **Self-reported compliance is not compliance.** Agent assertions without jury backing are inadmissible
2. **The multi-cognition jury is the referee** — 5 distinct LLM models (J1=claude-opus-4.6, J2=claude-sonnet-4.6, J3=gpt-5.4, J4=gpt-5.2, J5=gpt-5.4-mini) + Synthesizer (claude-opus-4.5) provide independent verdicts
3. **The agent must cite the jury synthesis commit** when claiming phase passage
4. **CHALLENGED verdicts cannot be waived by the agent** — corrections must be applied and re-juried

| Claim | Admissibility |
|---|---|
| "I believe this phase artifact is correct" | ❌ Inadmissible — no jury backing |
| "The jury returned QUALIFIED" | ⚠️ Insufficient — corrections required; R2 jury needed |
| "Judicial synthesis APPROVED at commit `<sha>`" | ✅ Admissible — ENG-12.3 satisfied |
| "I waived the jury because the change was minor" | ❌ Inadmissible — PRD-2.6 is NON-NEGOTIABLE |

> **Why:** *"The same model that authored the artifact cannot be trusted to assess whether it meets the constitution."* Different LLM models with different training substrates are the external referee. The citation auditor (ENG-14.1) adds a second layer — tooling before the jury, judge in the jury.

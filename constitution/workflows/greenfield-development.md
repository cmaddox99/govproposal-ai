---
workflow:
  id: greenfield-development
  name: Greenfield Development — 8-Phase Build
  avatar_context: [engineering, product]
  laws: [PRD-2.1, PRD-2.3, PRD-2.6, ENG-1.5, ENG-2.1, ENG-2.3, ENG-4.1, ENG-4.6, ENG-4.11, ENG-6.1, ENG-6.4, ENG-6.7, BUS-7.1, ENG-11.1, ENG-12.1, ENG-12.2, ENG-12.3, ENG-14.1, ENG-14.2]
  skills: [skill-02-user-journey-mapping, skill-03-executable-spec, skill-04-business-domain-modeling, skill-06-atomic-tdd, skill-07-vertical-slice-dev, skill-10-security-review, skill-11-mutation-testing, skill-12-api-design, skill-spec-governance]
  preceded_by: adoption
---

# Workflow: Greenfield Development — 8-Phase Build

> **Laws enforced:** ENG-4.1 (NON-NEGOTIABLE), ENG-6.1 (NON-NEGOTIABLE), ENG-6.4 (NON-NEGOTIABLE), **PRD-2.6 (NON-NEGOTIABLE)**, BUS-7.1, ENG-11.1, ENG-12.1 (NON-NEGOTIABLE)
> **Skills:** `skill-06-atomic-tdd`, `skill-07-vertical-slice-dev`, `skill-spec-governance`

---

## Prerequisites — Phase Gate Requirements (ENG-12.1 NON-NEGOTIABLE)

**Before Phase 1 begins, the multi-cognition jury infrastructure MUST be available and the project must be registered in `hangar-ai-specs/changes/`. (ENG-12.1 NON-NEGOTIABLE)**

Each phase gate requires:
1. Phase artifact committed to `hangar-ai-specs/changes/<project-id>/`
2. `aa-citation-audit` run on the artifact (ENG-14.1 — pre-jury citation gate)
3. Multi-cognition jury R1 + R2 deliberation (PRD-2.6 — 5 jurors, distinct LLM models)
4. Judicial synthesis APPROVED verdict committed
5. `aa-jury-gate` mechanical validation PASS (PRD-2.6 enforcement)
6. **Human reviews jury synthesis findings before approving phase advance** ← THE CHECKPOINT

> **ENG-12.1 (NON-NEGOTIABLE):** Agent cannot advance to a new phase without a human reviewing jury synthesis findings. Jury APPROVED verdict required — agent cannot self-declare phase complete.
> **ENG-12.3:** The multi-cognition jury (5 distinct LLM models) is the external referee. The authoring LLM cannot self-certify compliance.

---

## Multi-Cognition Jury Gate — Per Phase (PRD-2.6 NON-NEGOTIABLE)

Every phase in this workflow requires a completed two-round, five-juror jury deliberation before the phase artifact is presented to a human and the workflow advances. The human MUST only ever see the jury-corrected artifact.

```
Phase artifact drafted
    ↓
JURY ROUND 1 (PRD-2.6) — 5 jurors in parallel, each with distinct model
    ↓  corrections assigned sequential IDs (C-[phase]-NNN)
Corrections applied to artifact
    ↓
JURY ROUND 2 (PRD-2.6) — 5 jurors re-deliberate; each acknowledges Round 1 corrections by ID
    ↓
JUDICIAL SYNTHESIS — confirms zero unresolved CHALLENGED verdicts
    ↓
Phase artifact rendered as HTML (ENG-13.1) → human sees jury-corrected artifact
    ↓
Human APPROVE → phase advances
```

### Jury Composition (all 8 phases)

| Role | **Canonical Model** | What they challenge |
|------|----------------|---------------------|
| **J1 — Domain Sceptic** | `claude-opus-4.6` | Evidence methodology, source reliability, sample bias |
| **J2 — Technical Expert** | `claude-sonnet-4.6` | Causal claims, architecture soundness, absolute language |
| **J3 — Strategic / Product Lens** | `gpt-5.4` | Framing, scope accuracy, audience-readiness |
| **J4 — Defense Counsel** | `gpt-5.2` | Minimum defensible version; surfaces where artifact is too weak |
| **J5 — Devil's Advocate** | `gpt-5.4-mini` | Implicit assumptions never tested; disconfirming evidence; framing challenges |
| **J6 — Citation Auditor** | `aa-citation-audit` | Verifies all law IDs in the artifact are registered and correctly represented (ENG-14.1) |
| **Judicial Synthesizer** | `claude-opus-4.5` | Gate-locking synthesis — MUST be distinct from all 5 juror models |

> **PRD-2.6 HARD REQUIREMENT:** No two jurors (J1–J5) may share the same model ID in the same jury panel. Running J3 and J4 on the same model collapses two cognitive perspectives into one and constitutes a 4-juror panel — non-compliant. The Judicial Synthesizer must also be distinct from all five juror models.
>
> **Known model limitation:** `claude-haiku-4.5` consistently breaks juror role assignment and refuses to deliberate. Do NOT assign any juror role to `claude-haiku-4.5`. Use `gpt-5.4-mini` as the fast/cheap juror instead.
>
> Models may be updated as newer versions are released — update this table and keep all 6 slots distinct.

### Per-Phase Jury Focus

| Phase | Primary claims to challenge |
|-------|-----------------------------|
| 1 — Capture | Problem statement accuracy; persona completeness; compliance scope |
| 2 — Discover | Law applicability; non-negotiable identification; avatar relevance |
| 3 — Define | Contract completeness; data model correctness; BDD coverage of edge cases |
| 4 — Design | Architecture tradeoffs; threat model completeness; unmitigated risks |
| 5 — Plan | Slice independence; dependency accuracy; test pyramid balance; estimate realism |
| 6 — Build | Per-slice: TDD cycle compliance; coverage accuracy; mutation score validity |
| 7 — Review | Constitution compliance completeness; OWASP gap analysis; mutation evidence |
| 8 — Ship | Runbook completeness; rollback plan; gate evidence accuracy |

> **Prohibited:** Presenting a pre-jury artifact for human APPROVE. A phase with any unresolved
> CHALLENGED verdict CANNOT advance. Jury conducted after advancement is a constitutional violation.

---

## Phase Table

| Phase | Name | Key Activities | Jury Gate (PRD-2.6) | Constitutional Gate |
|---|---|---|---|---|
| 1 | Capture | Requirements elicitation; persona identification; compliance discovery | ✅ 5-juror 2-round jury on phase artifact before human review | Problem validated (PRD-2.1); personas documented |
| 2 | Discover | Constitution laws surfaced; non-negotiable constraints identified; avatar activated | ✅ 5-juror 2-round jury on phase artifact before human review | Avatar manifest loaded; applicable laws listed |
| 3 | Define | API contracts (ENG-1.5); data model with classification (ENG-6.4); BDD acceptance criteria (ENG-4.4) | ✅ 5-juror 2-round jury on phase artifact before human review | All critical paths have Gherkin scenarios |
| 4 | Design | Architecture decisions with law citations; security threat model (ENG-6.1); ADR filed in `hangar-ai-specs/` | ✅ 5-juror 2-round jury on phase artifact before human review | No unmitigated HIGH threats |
| 5 | Plan | Vertical slices with dependency graph (ENG-2.3); complexity estimates; test pyramid strategy | ✅ 5-juror 2-round jury on PROPOSAL before human review | Implementation proposal in `hangar-ai-specs/changes/` approved |
| 6 | Build | Atomic TDD per vertical slice (ENG-4.1 NON-NEGOTIABLE): RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT | ✅ Per-slice jury on slice completion evidence before advancing to next slice | All slices green; **pytest-cov ≥90% (ENG-4.6); mutmut ≥85% on critical modules (ENG-4.11); ruff bugs=0** — committed as slice evidence |
| 7 | Review | Constitution compliance review; OWASP Top 10 (ENG-6.1); test coverage analysis; mutation testing verification (ENG-4.11); audit trail (BUS-7.1) | ✅ 5-juror 2-round jury on review findings before human sign-off | Zero P0 violations; **jury attests: 0 critical findings; OWASP Top 10 reviewed; mutation_score ≥85% evidence committed (ENG-4.11)** |
| 8 | Ship | IaC deployment; API docs; runbook; proposal archived in `hangar-ai-specs/archive/` | ✅ Final 5-juror 2-round jury on ship readiness evidence | Proposal archived (ENG-11.1); **coverage and mutation evidence artifacts reviewed by human; Phase 8 human APPROVE gate** |

> 🎨 **Render as HTML (Phase 5 — PROPOSAL):** `aa-artifact-render hangar-ai-specs/changes/[id]/PROPOSAL.md --laws-dir laws`  
> Add `--pdf` to also generate a PDF. This embeds law citation tooltips from the constitution.


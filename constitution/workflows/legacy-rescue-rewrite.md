---
workflow:
  id: legacy-rescue-rewrite
  name: Legacy Rescue — Rewrite Track
  avatar_context: [engineering, business, product]
  laws: [ENG-4.1, ENG-4.6, ENG-4.9, ENG-4.11, ENG-6.1, ENG-6.7, ENG-7.6, BUS-2.1, BUS-2.2, BUS-2.4, BUS-7.1, ENG-11.1, ENG-12.1, ENG-12.2, ENG-12.3]
  skills: [skill-27-constitution-compliance, skill-04-business-domain-modeling, skill-03-executable-spec, skill-06-atomic-tdd, skill-10-security-review, skill-11-mutation-testing, skill-12-api-design, skill-spec-governance]
  preceded_by: adoption
---

# Workflow: Legacy Rescue — Rewrite Track

> **Laws enforced:** ENG-4.1 (NON-NEGOTIABLE), ENG-6.1 (NON-NEGOTIABLE), ENG-6.7 (NON-NEGOTIABLE), BUS-7.1, ENG-11.1
> **Skills:** `skill-06-atomic-tdd`, `skill-12-api-design`, `skill-spec-governance`

---

## Prerequisites — Phase Gate Prerequisites (ENG-12.1)

Each phase gate requires:
1. Phase artifact committed to `hangar-ai-specs/changes/<project-id>/`
2. `aa-citation-audit` run on the artifact (ENG-14.1 — pre-jury citation gate)
3. Multi-cognition jury R1 + R2 deliberation (PRD-2.6 — 5 jurors, distinct LLM models)
4. Judicial synthesis APPROVED verdict committed
5. `aa-jury-gate` mechanical validation PASS (PRD-2.6 enforcement)
6. **Human reviews jury synthesis findings before approving phase advance** ← THE CHECKPOINT

> **ENG-12.1 (NON-NEGOTIABLE):** Agent cannot advance to a new phase without a human reviewing jury synthesis findings. Jury APPROVED verdict required — agent cannot self-declare phase complete.

---

## Phase Table

| Phase | Name | Key Activities | Constitutional Gate |
|---|---|---|---|
| 1 | Assess | Legacy violation inventory; dependency mapping; behavioral contract discovery; **compliance assessment: identify applicable regulations per bounded context (FAA, DOT, PCI, GDPR) via `skill-27-constitution-compliance`** | Violation list with law IDs; dependency graph complete; regulatory scope confirmed (BUS-2.1); **Phase 1 assessment artifact committed; jury synthesis APPROVED** |
| 2 | Govern | `hangar-ai-specs/` initialized; rewrite proposal; parity test plan | Proposal approved; parity scaffold committed |
| 3 | Extract Spec | Document legacy business rules and edge cases; golden-file inputs/outputs; contract tests (ENG-4.9) | Behavioral contracts documented; golden files committed |
| 4 | Build | Governed build cycles: RED → GREEN → REFACTOR → REVIEW → APPROVE/BLOCK (ENG-4.1 NON-NEGOTIABLE); blocked cycles resolved before next | All cycles APPROVED; parity tests passing; **pytest-cov ≥90% (ENG-4.6); mutmut ≥85% on critical modules (ENG-4.11); ruff bugs=0** |
| 5 | Validate Parity | Run golden-file test suite; legacy vs. rewrite outputs; document intentional divergences | Parity report in `hangar-ai-specs/`; ≥95% golden-file match; **pytest-cov ≥80%; mutmut ≥70% (ENG-4.11); ruff bugs=0** |
| 6 | Certify | Regulatory docs; before/after compliance; legacy decommission plan; proposal archived (BUS-7.1) | Evidence complete; zero regression; **mutmut ≥85% on critical paths (ENG-4.11 NON-NEGOTIABLE); coverage and mutation evidence committed as Phase 6 artifacts** |

> 🎨 **Render as HTML (Phase 2 — Proposal):** `aa-artifact-render hangar-ai-specs/changes/[id]/PROPOSAL.md --laws-dir laws`  
> Add `--pdf` to also generate a PDF. This embeds law citation tooltips from the constitution.

---

## Build Cycle Template

```
Cycle N: [Feature/Concern Name]
  → RED:    Write parity test (input from golden file, assert expected output)
  → GREEN:  Implement minimum code to pass
  → REVIEW: Law violation check (cite specific law ID if blocked)
  → APPROVE: All laws satisfied + coverage/mutation gates passed — commit and proceed
  → BLOCK:   Violation cited — fix required before proceeding
```

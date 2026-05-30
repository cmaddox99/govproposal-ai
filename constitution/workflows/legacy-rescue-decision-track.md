---
workflow:
  id: legacy-rescue-decision-track
  name: Legacy Rescue — Decision Track
  avatar_context: [engineering, business, product]
  laws: [ENG-3.1, ENG-4.1, ENG-4.6, ENG-4.11, ENG-2.4, PRD-2.2, BUS-2.1, BUS-2.2, BUS-2.4, BUS-7.1, ENG-11.1, ENG-12.1, ENG-12.2, ENG-12.3]
  skills: [skill-27-constitution-compliance, skill-04-business-domain-modeling, skill-14-technical-debt, skill-09-refactoring, skill-08-code-review, skill-11-mutation-testing, skill-spec-governance]
  preceded_by: adoption
---

# Workflow: Legacy Rescue — Decision Track

> **Laws enforced:** ENG-4.1 (NON-NEGOTIABLE), BUS-7.1, ENG-11.1, ENG-3.1, ENG-2.4
> **Skills:** `skill-04-business-domain-modeling`, `skill-14-technical-debt`, `skill-spec-governance`

---

## Prerequisites — Phase Gate Prerequisites (ENG-12.1)

Each phase gate requires:
1. Phase artifact committed to `hangar-ai-specs/changes/<project-id>/`
2. `aa-citation-audit` run on the artifact (ENG-14.1 — pre-jury citation gate)
3. Multi-cognition jury R1 + R2 deliberation (PRD-2.6 — 5 jurors, distinct LLM models)
4. Judicial synthesis APPROVED verdict committed
5. **Human reviews jury synthesis findings before approving phase advance** ← THE CHECKPOINT

> **ENG-12.1 (NON-NEGOTIABLE):** Agent cannot advance to a new phase without a human reviewing jury synthesis findings. Jury APPROVED verdict required — agent cannot self-declare phase complete.

---

## Phase Table

| Phase | Name | Key Activities | Constitutional Gate |
|---|---|---|---|
| 1 | Archaeology | Map bounded contexts (ENG-2.4); per-context complexity scores (ENG-3.1); tech debt inventory; vendor lock-in; **compliance assessment: identify applicable regulations per bounded context (FAA, DOT, PCI, GDPR) via `skill-27-constitution-compliance`**; **📊 Phase 1 per-context assessment** (one `phase-1-assessment.md` per bounded context) | Bounded context map in `hangar-ai-specs/`; debt inventory complete; regulatory scope confirmed (BUS-2.1); **Phase 1 assessment artifact with per-context violation inventories committed; jury synthesis APPROVED** |
| 2 | Govern | `hangar-ai-specs/` initialized; decision proposal; decision criteria defined | Decision criteria in `hangar-ai-specs/changes/` |
| 3 | Deliberate | Per-context: REFACTOR (low complexity, high coverage) / REWRITE (high violations, low coverage) / HYBRID; constitutional evidence per decision; consensus recorded; **📊 Phase 3 decision metrics: cognitive complexity >10 → REWRITE signal; pytest-cov <50% → REWRITE signal; mutmut score informs refactoring depth (ENG-4.11); code smell delta trend** | Decision matrix with law citations; ADR filed; **pytest-cov and mutmut metrics included as objective evidence in REFACTOR/REWRITE verdict (ENG-4.6, ENG-4.11)** |
| 4 | Extract | First vertical slice per chosen track per bounded context (ENG-4.1, ENG-2.3) | First slice delivered with characterization tests and parity proof |
| 5 | Document | Maintenance guidelines per context; pattern library | Pattern library in `docs/`; `hangar-ai-specs/` updated |
| 6 | Certify | Tech debt reduction metrics; phased migration roadmap; before/after compliance; proposal archived (BUS-7.1) | Roadmap approved; evidence complete; **pytest-cov improved vs. baseline; mutmut ≥70% (general)/≥85% (critical paths, ENG-4.11); ruff bugs=0; jury attests 0 critical findings; coverage and mutation evidence artifacts committed** |

> 🎨 **Render as HTML (Phase 3 — ADR):** `aa-artifact-render hangar-ai-specs/changes/[id]/adr.md --laws-dir laws`  
> Add `--pdf` to also generate a PDF. This embeds law citation tooltips from the constitution.

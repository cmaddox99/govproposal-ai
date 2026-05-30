# Progress: ORAA Brownfield Enrichment Governance

**Last Updated:** March 9, 2026

---

## Status Summary

| Phase | Status | Description |
|---|---|---|
| Phase 0: Discovery baseline | ✅ Complete | ORAA repo stack/domain analysis completed |
| Phase 1: Taxonomy governance assets | ✅ Complete | Skill, guide, workflow, and AGENTS routing wired |
| Phase 2: Product avatar enrichment | ✅ Complete | Network Planning Optimization avatar created |
| Phase 3: Tech avatar enrichment | ✅ Complete | Python Streamlit technology avatar created |
| Phase 4: Legacy ML interop enrichment | ✅ Complete | R/PySpark/notebook compatibility avatar created |
| Phase 5: Brownfield governance updates | ✅ Complete | Non-rewrite default policy + migration parity gates documented |

**Overall:** 100% complete (all avatars created, registries updated, brownfield policy documented).

---

## Completed

1. Established root-cause position for reported rewrite behavior:
   - Missing enrichment can plausibly cause default routing to generic Python patterns.
2. Defined enrichment scope without violating model principles:
   - Product specificity belongs in avatars.
   - Skills remain domain-general.
3. Created Hangar SDD proposal package for execution planning.
4. Added reusable taxonomy governance assets:
   - `skill-30-taxonomy-governed-avatar-enrichment`
   - Product taxonomy governance guide (`docs/guides/avatars/product-taxonomy-governance.md`)
   - Taxonomy-aligned enrichment workflow guide (`docs/guides/adoption/taxonomy-aligned-avatar-enrichment-workflow.md`)
   - AGENTS routing update for enrichment prompts
5. Created product avatar: `avatars/product-type/network-planning-optimization/`
   - manifest.yaml (domain, personas, laws, workflows, brownfield_context)
   - guidance.md (PRD law applications, brownfield integration, metrics)
   - examples/personas.md (Lisa, Marcus, Rachel, David)
   - use-cases/route-profitability-analysis.md (MVP workflow, TDD, preservation strategy)
   - ADOPTION.md (brownfield adoption process, validation gates, workflow)
6. Created technology avatar: `avatars/technology/python-streamlit/`
   - manifest.yaml (stack, dependencies, laws, brownfield_context)
   - guidance.md (layered architecture, TDD for dashboards, brownfield integration)
7. Created technology avatar: `avatars/technology/legacy-ml-interop/`
   - manifest.yaml (preservation strategies, containerization, API wrappers)
   - guidance.md (R/PySpark containerization, regression testing, decision framework)
8. Updated registries:
   - `avatars/product-type/index.yaml` (added network-planning-optimization entry)
   - `avatars/index.yaml` (added python-streamlit and legacy-ml-interop entries)
   - `avatars/AVATAR-RAG-INDEX.yaml` (added RAG routing for all 3 avatars)
9. Created brownfield code preservation policy:
   - `docs/guides/adoption/brownfield-code-preservation.md` (preserve-first strategy, migration gates)

---

## Pending Work

1. Dry-run validation test against ORAA repo context to confirm no language rewrite default

---

## Exit Criteria

- ✅ New avatars are created and indexed
- ✅ Brownfield guide has explicit no-rewrite default policy
- ✅ Migration approval and parity-gate criteria documented
- ⬜ Dry-run prompt against ORAA repo context does not default to language rewrite (validation pending)

# Workflows

Index of all governed AI workflows. Each workflow enforces constitutional laws at every phase gate.

> **Phase 0 (Conditional):** The `adoption` workflow runs automatically before any other workflow.
> If the codebase is already adopted and current, it skips silently. Otherwise it runs first.

| Workflow | Description | Laws | Skills |
|---|---|---|---|
| [adoption.md](adoption.md) | **Constitutional Adoption (Phase 0)** — Establish or update governance: fresh adoption, stale update, or openspec/ migration | ENG-1.2, ENG-10.1, ENG-11.1 | skill-spec-governance |
| [product-discovery-stage-a-f.md](product-discovery-stage-a-f.md) | Product Discovery — Stage A through F sequential gate process | PRD-2.1, PRD-2.2, PRD-2.3, PRD-2.4, PRD-2.5, PRD-3.1, PRD-3.2, PRD-4.1, PRD-4.2, BUS-7.1, ENG-11.1 | skill-product-discovery-orchestration, skill-02-user-journey-mapping, skill-03-executable-spec, skill-01-roadmapping, skill-spec-governance |
| [greenfield-development.md](greenfield-development.md) | Greenfield Development — 8-Phase Build from blank canvas to governed ship | PRD-2.1, PRD-2.3, ENG-1.5, ENG-2.1, ENG-2.3, ENG-4.1, ENG-6.1, ENG-6.4, ENG-6.7, BUS-7.1, ENG-11.1 | skill-02-user-journey-mapping, skill-03-executable-spec, skill-04-business-domain-modeling, skill-06-atomic-tdd, skill-07-vertical-slice-dev, skill-10-security-review, skill-spec-governance |
| [legacy-rescue-refactor.md](legacy-rescue-refactor.md) | Legacy Rescue — Refactor Track for constitutional remediation without full rewrite | ENG-3.1, ENG-4.1, ENG-4.3, ENG-6.1, ENG-6.7, BUS-7.1, ENG-11.1 | skill-09-refactoring, skill-06-atomic-tdd, skill-10-security-review, skill-14-technical-debt, skill-08-code-review, skill-spec-governance |
| [legacy-rescue-rewrite.md](legacy-rescue-rewrite.md) | Legacy Rescue — Rewrite Track for full behavioral-parity governed rewrites | ENG-4.1, ENG-4.9, ENG-6.1, ENG-6.7, ENG-7.6, BUS-7.1, ENG-11.1 | skill-04-business-domain-modeling, skill-03-executable-spec, skill-06-atomic-tdd, skill-10-security-review, skill-12-api-design, skill-spec-governance |
| [legacy-rescue-decision-track.md](legacy-rescue-decision-track.md) | Legacy Rescue — Decision Track for per-bounded-context refactor/rewrite/hybrid analysis | ENG-3.1, ENG-4.1, ENG-2.4, PRD-2.2, BUS-7.1, ENG-11.1 | skill-04-business-domain-modeling, skill-14-technical-debt, skill-09-refactoring, skill-08-code-review, skill-spec-governance |
| [avatar-workflow.md](avatar-workflow.md) | **Avatar Workflow** — Governed 6-mode lifecycle for creating, assessing, correcting, validating, enriching, and PR-reviewing Hangar AI Constitution avatars (technology and product type) | ENG-11.1, ENG-11.2, ENG-1.2, ENG-6.7, ENG-10.3 | skill-avatar-workflow, skill-spec-governance |

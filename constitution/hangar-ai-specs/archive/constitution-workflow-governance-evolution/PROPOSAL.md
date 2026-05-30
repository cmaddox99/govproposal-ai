# Proposal: Constitution Workflow Governance Evolution

**Proposal ID:** constitution-workflow-governance-evolution  
**Submitted:** March 22, 2026  
**Last Updated:** March 31, 2026  
**Status:** IN PROGRESS — Phases 7, 8, 9 scoped; implementation pending  
**Execution Order:** Phase 1 of 2 (execute before `hangar-ai-workshop-program`)

---

## Problem

Four gaps currently block the Hangar AI Constitution from governing end-to-end product and engineering work at American Airlines:

**1. No workflows defined.**  
The `agent-skills/workflows/` folder was removed as premature structure. Skills exist, but there is no governed, constitution-cited sequence telling agents *how* to progress through a discovery, greenfield build, or legacy rescue engagement. Agents operate with skills but no orchestrating workflow.

**2. OpenSpec tool dependency creates lock-in and team friction.**  
The constitution adopted the OpenSpec methodology from `github.com/Fission-AI/OpenSpec` — its proposal lifecycle, changeset management, and spec folder structure are genuinely useful. However, the Hangar SDD tool itself (`openspec validate`, ``, ``) is a third-party dependency that AA engineers have rejected. References to the tool appear in AGENTS.md files, the `00-openspec.md` skill, and downstream workshop guides. The methodology must be preserved; the tool dependency must be removed.

**3. The `openspec/` folder name signals an external product, not an AA-native process.**  
Every project that adopts the constitution gets an `openspec/` folder. This communicates "use this third-party tool" rather than "follow the Hangar SDD (Spec-Driven Development) process." Renaming to `hangar-ai-specs/` makes this clearly an AA-native governance structure.

**4. The product discovery workflow (Stage A–F) has no constitutional backing.**  
The AA Hangar Product Discovery Agent implements a Stage A–F discovery lifecycle, but this workflow is not codified in the constitution, not cited by skills, and not supported by governing laws. The workflow lives only in the agent's implementation code. For the constitution to govern discovery work — and for other teams to follow the same process — the workflow must be canonized here with compliant skills and governing laws.

---

## Solution

Five changes to the AA Hangar AI Constitution, plus downstream updates to three repos:

1. **Rename `openspec/` → `hangar-ai-specs/`** across the constitution and all downstream repos. Strip all Hangar SDD tool references. Document the Hangar SDD process as a methodology in an updated skill.
2. **Add `workflows/` directory** to the constitution with five governed workflow definitions.
3. **Update the `00-openspec.md` skill** — rename to `spec-governance.md`, remove tool references, define the `hangar-ai-specs/` folder lifecycle as the Hangar SDD process.
4. **Add `product-discovery-orchestration.md` skill** to `discovery-research/` — governs Stage A–F progression with constitutional law citations.
5. **Add two new laws** to close governance gaps:
   - `PRD-2.5`: Discovery Stage-Gate Law — evidence required before each stage transition  
   - New article in engineering: `ENG-11` — Spec-Driven Development Law — governs `hangar-ai-specs/` lifecycle
6. **Update three downstream repos** so adoption guides and workshop materials reference the new constitution workflows.

---

## What Will Be Delivered

### Phase 1: Decouple from OpenSpec Tool

**1a. Rename `openspec/` → `hangar-ai-specs/` in the Constitution itself**

```
governance/hangar-ai-constitution/
  hangar-ai-specs/           ← renamed from openspec/
    changes/                 ← active proposals (unchanged)
    archive/                 ← completed proposals (unchanged)
    README.md                ← updated to describe Hangar SDD process
```

**1b. Strip all Hangar SDD references from:**
- `AGENTS.md` — remove `openspec validate`, ``, `` commands; replace with plain file operations and Hangar SDD instructions
- `agent-skills/skills-by-domain/discovery-research/00-openspec.md` — renamed and rewritten (see Phase 3)
- `docs/guides/` — scan and update all references to OpenSpec tool or `openspec/` folder name
- `docs/slides/` — update any presentation references

**1c. Update the constitution `README.md`** — introduce "Hangar SDD" by name, explain `hangar-ai-specs/` structure

---

### Phase 2: Add Five Governed Workflows

New directory: `workflows/` at the constitution root.

Each workflow file is token-optimized markdown: a header block citing governing laws and activating skills, followed by numbered phases with decision gates. No prose padding.

---

#### Workflow 1: `product-discovery-stage-a-f.md`

**Purpose:** Govern the Stage A–F product discovery lifecycle from problem identification through roadmap lock.  
**Avatar context:** Product, Business  
**Skills activated:** `product-discovery-orchestration`, `02-user-journey-mapping`, `03-executable-spec`, `01-roadmapping`  
**Laws cited:** `PRD-2.1`, `PRD-2.2`, `PRD-2.3`, `PRD-2.4`, `PRD-2.5` (new), `PRD-3.1`, `PRD-3.2`, `PRD-4.1`, `PRD-4.2`, `BUS-7.1`, `ENG-11.1` (new)

| Stage | Name | Entry Gate | Key Activities | Exit Gate |
|---|---|---|---|---|
| A | Initialize | Product need identified | Activate constitution; create `hangar-ai-specs/`; assign Product + Business avatars; define problem statement | Problem statement approved; `hangar-ai-specs/changes/[discovery-id]/` scaffolded |
| B | Public Field Study | Stage A complete | Market research; competitive analysis (PRD-2.4); user interviews (PRD-3.1); JTBD framing (PRD-2.3) | ≥3 validated user insights; competitive landscape documented |
| C | Code Evidence | Stage B complete | Repository ingestion; codebase assessment; domain model extraction; tech debt inventory (ENG-3.1) | Evidence report filed in `hangar-ai-specs/`; no unreviewed critical findings |
| D | Internal Validation | Stage C complete | Stakeholder review; assumption mapping (PRD-2.2); problem validation (PRD-2.1); blocker resolution | All blockers resolved; DVFT matrix complete |
| E | Metric Rebaseline | Stage D complete | Define success metrics; establish baselines; set PMF targets (PRD-6.1); confirm measurability | Metrics spec complete in `hangar-ai-specs/specs/` |
| F | Roadmap Lock | Stage E complete | Now/Next/Later roadmap (PRD-4.2); outcome-based framing (PRD-4.1); vertical slices defined; implementation proposal created | Roadmap approved; `hangar-ai-specs/changes/[impl-proposal]/` scaffolded; audit trail complete (BUS-7.1) |

**Governance rules:**
- Stages are sequential. No skipping.
- Each stage transition requires evidence documented in `hangar-ai-specs/`.
- Stage F produces an implementation proposal as the next `hangar-ai-specs` changeset.
- All decisions are auditable per `BUS-7.1`.

---

#### Workflow 2: `greenfield-development.md`

**Purpose:** Govern new product development from requirements capture through production deployment.  
**Avatar context:** Engineering, Product  
**Skills activated:** `02-user-journey-mapping`, `03-executable-spec`, `04-business-domain-modeling`, `06-atomic-tdd`, `07-vertical-slice-dev`, `10-security-review`, `spec-governance`  
**Laws cited:** `PRD-2.1`, `PRD-2.3`, `ENG-1.5`, `ENG-2.1`, `ENG-2.3`, `ENG-4.1`, `ENG-4.2`, `ENG-6.1`, `ENG-6.4`, `ENG-6.7`, `BUS-7.1`, `ENG-11.1` (new)

| Phase | Name | Key Activities | Constitutional Gate |
|---|---|---|---|
| 1 | Capture | Requirements elicitation; persona identification; compliance discovery | Problem validated (PRD-2.1); personas documented |
| 2 | Discover | Governance laws surfaced; non-negotiable constraints identified; avatar activated | Avatar manifest loaded; applicable laws listed |
| 3 | Define | API contracts (ENG-1.5); data model with classification (ENG-6.4); BDD acceptance criteria (ENG-4.4) | All critical paths have Gherkin scenarios |
| 4 | Design | Architecture decisions with law citations; security threat model (ENG-6.1); RBAC design | ADR filed in `hangar-ai-specs/`; no unmitigated HIGH threats |
| 5 | Plan | Vertical slices with dependency graph (ENG-2.3); complexity estimates; test pyramid strategy (ENG-4.2) | Implementation proposal in `hangar-ai-specs/changes/` approved |
| 6 | Build | Atomic TDD per vertical slice (ENG-4.1 NON-NEGOTIABLE): RED → GREEN → REFACTOR → VERIFY → COMMIT → REPEAT | All slices green; coverage ≥90% new code (ENG-4.6) |
| 7 | Review | Constitution compliance review; OWASP Top 10 (ENG-6.1); test coverage analysis; audit trail verification (BUS-7.1) | Zero P0 violations; security sign-off |
| 8 | Ship | Deployment config (IaC per ENG-5.1); API docs; runbook; regulatory certification | Proposal archived in `hangar-ai-specs/archive/` |

---

#### Workflow 3: `legacy-rescue-refactor.md`

**Purpose:** Govern systematic refactoring of a legacy codebase with characterization tests and constitutional remediation.  
**Avatar context:** Engineering  
**Skills activated:** `09-refactoring`, `06-atomic-tdd`, `10-security-review`, `14-technical-debt`, `08-code-review`, `spec-governance`  
**Laws cited:** `ENG-3.1`, `ENG-4.1`, `ENG-4.3`, `ENG-6.1`, `ENG-6.7`, `BUS-7.1`, `ENG-11.1` (new)

| Phase | Name | Key Activities | Constitutional Gate |
|---|---|---|---|
| 1 | Assess | Constitution audit; violation inventory; compliance risk classification | Violations documented with law IDs in `hangar-ai-specs/` |
| 2 | Govern | Create `hangar-ai-specs/` structure; activate avatars; define remediation proposal | Proposal approved in `hangar-ai-specs/changes/` |
| 3 | Characterize | Write characterization tests that lock existing behavior before any change (ENG-4.3) | All critical paths covered by characterization tests; CI green |
| 4 | Remediate | Fix violations in priority order (Security > Correctness > Reliability); one violation per commit; re-run characterization tests | All P0 violations resolved; no regression |
| 5 | Refactor | Reduce complexity (ENG-3.1); extract domain objects (ENG-2.1); Boy Scout commits (ENG-1.3) | Complexity ≤10; coverage ≥80% |
| 6 | Certify | Final compliance report; audit evidence package (BUS-7.1); proposal archived | Zero open violations; evidence in `hangar-ai-specs/archive/` |

---

#### Workflow 4: `legacy-rescue-rewrite.md`

**Purpose:** Govern full behavioral-parity rewrite of a legacy system with specification extraction and governed build cycles.  
**Avatar context:** Engineering  
**Skills activated:** `04-business-domain-modeling`, `03-executable-spec`, `06-atomic-tdd`, `10-security-review`, `12-api-design`, `spec-governance`  
**Laws cited:** `ENG-4.1`, `ENG-4.9`, `ENG-6.1`, `ENG-6.7`, `ENG-7.6`, `BUS-7.1`, `ENG-11.1` (new)

| Phase | Name | Key Activities | Constitutional Gate |
|---|---|---|---|
| 1 | Assess | Legacy violation inventory; dependency mapping; behavioral contract discovery | Violation list with law IDs; dependency graph complete |
| 2 | Govern | `hangar-ai-specs/` initialized; rewrite proposal created; parity test plan defined | Proposal approved; parity test scaffold committed |
| 3 | Extract Spec | Document legacy business rules and edge cases; create golden-file inputs/outputs; define contract tests (ENG-4.9) | Behavioral contracts documented; golden files committed |
| 4 | Build | Governed build cycles: each cycle is RED → GREEN → REFACTOR → ENSEMBLE REVIEW → APPROVE/BLOCK; blocked cycles resolved before next cycle (ENG-4.1 NON-NEGOTIABLE) | All cycles APPROVED; parity tests passing |
| 5 | Validate Parity | Run golden-file test suite; compare legacy outputs vs. rewrite outputs; document any intentional divergences | Parity report in `hangar-ai-specs/`; ≥95% golden-file match |
| 6 | Certify | Regulatory documentation; before/after compliance comparison; legacy decommission plan; proposal archived (BUS-7.1) | Compliance evidence complete; zero regression |

**Build Cycle Template:**
```
Cycle N: [Feature/Concern Name]
  → RED:    Write parity test (input from golden file, assert expected output)
  → GREEN:  Implement minimum code to pass
  → REVIEW: Law violation check (cite specific law ID if blocked)
  → APPROVE: All laws satisfied — commit and proceed
  → BLOCK:   Violation cited — fix required before proceeding
```

---

#### Workflow 5: `legacy-rescue-decision-track.md`

**Purpose:** Govern strategic decision-making for large legacy estates where the right path (refactor vs. rewrite vs. hybrid) is not obvious.  
**Avatar context:** Engineering, Business  
**Skills activated:** `04-business-domain-modeling`, `14-technical-debt`, `09-refactoring`, `08-code-review`, `spec-governance`  
**Laws cited:** `ENG-3.1`, `ENG-4.1`, `ENG-2.4`, `PRD-2.2`, `BUS-7.1`, `ENG-11.1` (new)

| Phase | Name | Key Activities | Constitutional Gate |
|---|---|---|---|
| 1 | Archaeology | Map bounded contexts (ENG-2.4); per-context complexity scores (ENG-3.1); tech debt inventory; vendor lock-in assessment | Bounded context map in `hangar-ai-specs/`; debt inventory complete |
| 2 | Govern | `hangar-ai-specs/` initialized; decision proposal scaffolded; decision criteria defined | Decision criteria documented in `hangar-ai-specs/changes/` |
| 3 | Deliberate | Per-context decision: REFACTOR (low complexity, high test coverage) / REWRITE (high violations, low coverage) / HYBRID (partial extraction); constitutional evidence for each decision; consensus recorded | Decision matrix with law citations in `hangar-ai-specs/`; ADR filed |
| 4 | Extract | First vertical slice executed under the chosen track for each bounded context (ENG-4.1, ENG-2.3) | First slice delivered with characterization tests and parity proof |
| 5 | Document | Maintenance guidelines per context; pattern library (reusable heuristics from this engagement) | Pattern library in `docs/`; updated `hangar-ai-specs/` |
| 6 | Certify | Tech debt reduction metrics; phased migration roadmap; before/after compliance; proposal archived (BUS-7.1) | Roadmap approved; evidence complete |

---

### Phase 3: Update Skills

#### 3a. Rename and Rewrite `00-openspec.md` → `spec-governance.md`

**Location:** `agent-skills/skills-by-domain/discovery-research/spec-governance.md`

**Changes:**
- Remove all Hangar SDD commands (`openspec validate`, ``, ``)
- Rename skill ID: `skill-00-openspec` → `skill-spec-governance`
- Rename skill: "OpenSpec Orchestration" → "Hangar SDD: Spec Governance"
- Document the `hangar-ai-specs/` folder lifecycle as the Hangar SDD (Spec-Driven Development) process
- Add citation to new `ENG-11.1` (Spec-Driven Development Law)
- Define the three lifecycle operations as plain file operations:
  - **Create proposal**: scaffold `hangar-ai-specs/changes/[verb-noun-id]/` with `PROPOSAL.md`, `tasks.md`, optional `design.md`, `SPEC.md`
  - **Manage progress**: update `PROGRESS.md`; mark tasks complete in `tasks.md`
  - **Archive proposal**: move completed folder to `hangar-ai-specs/archive/YYYY-MM-DD-[id]/`

**`hangar-ai-specs/` folder contract (tool-independent):**
```
hangar-ai-specs/
  changes/                    ← active proposals (in-flight work)
    [verb-noun-id]/
      PROPOSAL.md             ← problem, solution, deliverables, success criteria
      tasks.md                ← work breakdown with checkbox status
      design.md               ← (optional) architecture and design decisions
      SPEC.md                 ← (optional) detailed technical specification
      PROGRESS.md             ← implementation tracking (phases, blockers, notes)
  archive/                    ← completed proposals
    YYYY-MM-DD-[id]/          ← renamed on archive; contains all above files
  specs/                      ← current truth documents (not proposals)
    [domain]/                 ← living specs updated as system evolves
```

**Laws cited in updated skill:** `PRD-2.1`, `ENG-10.1`, `ENG-11.1` (new), `BUS-7.1`

---

#### 3b. Add New Skill: `product-discovery-orchestration.md`

**Location:** `agent-skills/skills-by-domain/discovery-research/product-discovery-orchestration.md`

**Purpose:** Orchestrate the Stage A–F product discovery workflow. Tells agents how to initiate, progress, and complete a discovery engagement.

**Laws cited:** `PRD-2.1`, `PRD-2.2`, `PRD-2.3`, `PRD-2.4`, `PRD-2.5` (new), `PRD-3.1`, `PRD-3.2`, `PRD-4.1`, `PRD-4.2`, `BUS-7.1`, `ENG-11.1` (new)

**Key behaviors:**
1. **Initialize discovery** — create `hangar-ai-specs/changes/[discovery-id]/`; load product + business avatars
2. **Gate each stage transition** — validate PRD-2.5 evidence requirements before advancing
3. **Surface relevant laws per stage** — cite law IDs in every recommendation
4. **Track audit trail** — every stage transition logged (BUS-7.1)
5. **Produce Stage F output** — roadmap as outcome statements (PRD-4.1) + an implementation proposal in `hangar-ai-specs/changes/`

---

### Phase 4: Add Two New Laws

#### 4a. Add `PRD-2.5` to `laws/product/discovery.md`

**Law ID:** `PRD-2.5`  
**Title:** Discovery Stage-Gate Law  
**Status:** NON-NEGOTIABLE  

```
Discovery work SHALL progress through stages sequentially.
No stage may begin until its entry gate is satisfied with documented evidence
filed in hangar-ai-specs/.

Stage transitions require:
  - Written evidence artifact in hangar-ai-specs/changes/[id]/
  - All blockers from prior stage resolved
  - Audit event logged (BUS-7.1)

Anti-patterns prohibited:
  - Skipping stages to reach implementation faster
  - Beginning Stage F (Roadmap Lock) without validated metrics (Stage E)
  - Treating discovery as optional for new product initiatives
```

---

#### 4b. Add New Engineering Article `ENG-11` to `laws/engineering/`

**New file:** `laws/engineering/spec-driven-development.md`  
**Article:** XI  
**Title:** Spec-Driven Development Laws

**ENG-11.1 — Hangar SDD Law (NON-NEGOTIABLE)**  
```
All significant engineering and product work SHALL be governed by the
Hangar SDD (Spec-Driven Development) process using the hangar-ai-specs/
folder structure.

Requirements:
  - Every project adopting the constitution MUST have a hangar-ai-specs/ root folder
  - New features/changes of significant scope MUST have a PROPOSAL.md before implementation
  - Completed proposals MUST be archived with implementation notes
  - No reference to external spec-management tools (e.g., Hangar SDD) is permitted;
    hangar-ai-specs/ is tool-independent and governed by this law

The three-stage lifecycle is:
  PROPOSE → IMPLEMENT → ARCHIVE
```

**ENG-11.2 — Proposal Completeness Law**  
```
PROPOSAL.md SHALL include: problem statement, solution, deliverables,
success criteria, and references to governing laws.
Proposals without law citations SHALL be rejected.
```

**ENG-11.3 — Spec Freshness Law**  
```
Specs in hangar-ai-specs/specs/ SHALL reflect current system truth.
Stale specs that contradict the codebase are a compliance violation.
```

---

### Phase 5: Downstream Repo Updates

#### 5a. AA Hangar Product Discovery Agent

| File | Change |
|---|---|
| `openspec/` folder | Rename to `hangar-ai-specs/` |
| `AGENTS.md` | Update `hangar-ai-specs/` reference; link to `constitution-workflow-governance-evolution` workflow |
| `docs/pilot-deployment-runbook.md` | Update `openspec/` folder references |
| `docs/constitutional-handoff-package.md` | Update references |

#### 5b. AA Hangar Agentic SDLC Workshop

| File | Change |
|---|---|
| `WORKSHOP-GUIDE.md` | Add "Workflows" section linking to `greenfield-development.md`; update Step-by-Step track to reference workflow phases |
| `docs/` adoption guides | Update `openspec/` → `hangar-ai-specs/`; add workflow phase references |
| Workshop template files | Update `openspec/` folder template to `hangar-ai-specs/` |

#### 5c. AA Hangar Constitution Adoption Test

| File | Change |
|---|---|
| `docs/adoption-prompt.md` | Update verification checklist: `openspec/` → `hangar-ai-specs/`; add workflow activation check |
| `backup/back-up-app/` | Confirm no `openspec/` folder in baseline (correct starting state) |
| `loyalty-service-legacy/` | Verify AI adoption creates `hangar-ai-specs/` (not `openspec/`) during test |

---

### Phase 6: Workflow Model Integrity Hardening

**Trigger:** Post-implementation audit (2026-03-31) revealed four law coverage gaps and four missing RAG cross-references across the five new workflows. The constitution's model requires: Laws → Skills (cite laws) → Workflows (compose skills + cite laws). Gaps break law enforcement authority at runtime and prevent bidirectional RAG traversal.

#### 6a. Law Coverage Gaps — Skill Frontmatter Fixes

Four laws are cited in workflow frontmatter but not enforced by any composed skill:

| Task | Law | Issue | Fix |
|---|---|---|---|
| 6.1 | `ENG-6.7` Audit Trail (**NON-NEGOTIABLE**) | Cited in `greenfield`, `refactor`, `rewrite` workflows. `skill-10-security-review` law list ends at ENG-6.5. | Add `ENG-6.7` to `skill-10-security-review` law block |
| 6.2 | `ENG-7.6` Idempotency | Cited in `rewrite` workflow. `skill-12-api-design` is composed in that workflow but doesn't cite ENG-7.6. | Add `ENG-7.6` to `skill-12-api-design` law block |
| 6.3 | `PRD-2.2` Assumption Mapping | Cited in `decision-track` workflow Phase 3 (Deliberate). No skill in that workflow covers it. | Add `PRD-2.2` to `skill-04-business-domain-modeling` law block — assumption validation is inherent to bounded context analysis |

#### 6b. Missing Skill in Workflow Composition

| Task | Workflow | Law | Issue | Fix |
|---|---|---|---|---|
| 6.4 | `greenfield-development.md` | `ENG-1.5` API-First Design | Phase 3 (Define) requires API contracts per ENG-1.5. `skill-12-api-design` enforces this law but is absent from the workflow's `skills:` list. | Add `skill-12-api-design` to `greenfield-development.md` frontmatter |

#### 6c. Missing Skill→Workflow RAG Cross-References

Only `skill-product-discovery-orchestration` references its workflow file in its body. The other four workflows have no primary skill linking back, breaking bidirectional RAG traversal: an agent retrieving a skill cannot surface the governing workflow.

| Task | Skill | Workflow Reference to Add |
|---|---|---|
| 6.5 | `skill-07-vertical-slice-dev` | `See workflows/greenfield-development.md` |
| 6.6 | `skill-14-technical-debt` | `See workflows/legacy-rescue-decision-track.md` |
| 6.7 | `skill-09-refactoring` | `See workflows/legacy-rescue-refactor.md` |
| 6.8 | `skill-06-atomic-tdd` | `See workflows/legacy-rescue-rewrite.md` |

---

### Phase 7: Compliance Coverage & Avatar-Workflow Wiring

**Trigger:** Post-Phase 6 gap analysis (2026-03-31) found two related problems:

1. **Legacy rescue workflows have no business/product compliance coverage.** `avatar_context: [engineering]` means business compliance avatars never activate. BUS-2.x (Regulatory Mapping, Control Framework, Compliance Monitoring, Evidence Collection), BUS-4.x (Privacy), and BUS-6.x (Risk) laws are not cited in any legacy rescue workflow and no skill enforcing them is composed in. `skill-27-constitution-compliance` exists and contains FAA/TSA/DOT-specific guidance but is never composed into legacy rescue.

2. **All avatar manifests reference stale, non-existent workflow IDs.** Every product-type, technology, and industry avatar currently wires to: `workflow-discovery-to-delivery`, `workflow-sdd-lifecycle`, `workflow-brownfield-adoption`, `workflow-ux-to-implementation` — none of which exist in the constitution's `workflows/` directory. This breaks avatar-to-workflow RAG retrieval entirely. Avatars carry AA domain knowledge (FAA DO-178C levels, DOT compliance, PCI, GDPR, crew scheduling rules) that must flow into the governed workflows to produce domain-aware remediation plans.

#### 7a — Compliance Law & Skill Coverage in Legacy Rescue Workflows

**Missing BUS law coverage (no skill enforces these in legacy rescue):**

| Law | Domain | Missing From |
|---|---|---|
| `BUS-2.1` Regulatory Mapping | Compliance | All 3 legacy rescue workflows |
| `BUS-2.2` Control Framework | Compliance | All 3 legacy rescue workflows |
| `BUS-2.3` Compliance Monitoring | Compliance | All 3 legacy rescue workflows |
| `BUS-2.4` Evidence Collection | Compliance | All 3 legacy rescue workflows |
| `BUS-4.x` Privacy (PII/GDPR/PCI) | Privacy | refactor + rewrite |
| `BUS-6.x` Business Risk | Risk | All 3 legacy rescue workflows |

**Fix:** Add `skill-27-constitution-compliance` to the skills composition of all three legacy rescue workflows. Add BUS-2.1, BUS-2.2, BUS-2.4 to the `laws:` frontmatter. This skill already contains FAA/TSA/DOT-specific guidance and maps to BUS-2.x laws.

**Fix:** Add `avatar_context: [engineering, business, product]` to refactor and rewrite workflows (currently `[engineering]` only). Business avatars carry compliance domain knowledge that must activate during a compliance remediation phase.

**Fix:** Add a `## Compliance Assessment` gate to Phase 1 (Assess) of refactor and rewrite workflows: identify applicable regulations (FAA, DOT, PCI, GDPR) per bounded context before any remediation begins.

#### 7b — Avatar Manifest Workflow ID Update

All 35+ avatar manifests currently reference stale workflow IDs. The mapping to new governed workflow IDs:

| Old Workflow ID | New Workflow ID | Applies To |
|---|---|---|
| `workflow-discovery-to-delivery` | `product-discovery-stage-a-f` | Product/business avatars |
| `workflow-sdd-lifecycle` | `greenfield-development` | Technology avatars |
| `workflow-brownfield-adoption` | `legacy-rescue-decision-track` | Legacy/brownfield avatars |
| `workflow-brownfield-adoption` | `legacy-rescue-refactor` | Refactor-track avatars |
| `workflow-ux-to-implementation` | `greenfield-development` | UX/frontend avatars |

**Fix:** Update `activates: workflows:` in every avatar manifest to reference the correct new workflow IDs. This restores the avatar→workflow RAG traversal chain: a prompt in the context of a `loyalty-aadvantage` avatar will now surface `legacy-rescue-decision-track` or `greenfield-development` as appropriate.

**Fix:** `aviation-faa` industry avatar currently has only `ADOPTION.md` — no `manifest.yaml`. Create `avatars/industry/aviation-faa/manifest.yaml` with DO-178C, FAR Part 121, DOT compliance specializations and activate it on `legacy-rescue-refactor` and `legacy-rescue-rewrite` workflows so FAA compliance gates are enforced during aviation software remediation.

**Fix:** Update `skill-27-constitution-compliance` `## Workflow Integration` section — replace stale `workflow-aviation-compliance`, `workflow-constitution-observability-setup`, `workflow-sdd-lifecycle` references with the new governed workflow IDs.

---

### Phase 8: Business Avatar Enrichment & Manifest Creation

**Trigger:** Avatar model integrity audit (2026-03-31) found 5 stub avatars with no `manifest.yaml` and 4 manifested avatars with critical compliance law gaps. Product-type avatars are the primary mechanism for bringing AA domain knowledge (FAA regulations, DOT passenger rights, PCI-DSS, GDPR/CCPA) into governed workflows. Without correct law citations and skill activations, a governed workflow operating in the context of a loyalty, cargo, or passenger booking system will produce engineering-only remediation plans that miss their most serious regulatory obligations.

#### 8a — Create Missing Manifests (5 stubs → full manifests)

| Avatar | Domain | Key Compliance Scope | Priority |
|---|---|---|---|
| `passenger-booking` | Flight search, reservations, payment | PCI-DSS (card data), DOT refund/rebooking rights, GDPR (EU passengers), GDS API contracts | 🔴 Highest |
| `crew-training-scheduling` | Pilot OE training optimization (JOSE) | FAR Part 117 (crew rest/duty), DO-178C (safety-critical software), FAA OE mandates | 🔴 Highest |
| `airport-operations` | Gate management, ground handling, IROP recovery | FAR Part 139 (airport certification), DOT IROP consumer rules, TSA checkpoint coordination | 🟡 High |
| `customer-service` | Rebooking, refunds, complaints, compensation | DOT Part 250 (denied boarding), DOT refund timelines (7/20-day rules), DOT 14 CFR 259 | 🟡 High |
| `internal-productivity` | Content transformation, workflow automation, brand tools | PII handling (GDPR/CCPA for employee data), BUS-3.x data governance | 🟢 Standard |

Each manifest must follow the full avatar schema:
- `avatar:` block with id, type, name, version
- `domain:` block with personas and core journeys
- `activates: skills:` — minimum: `skill-spec-governance`, `skill-27-constitution-compliance`, `skill-10-security-review` + domain-relevant skills
- `activates: workflows:` — new governed workflow IDs (not stale IDs)
- `specializes_laws:` — PRD + ENG + BUS compliance laws relevant to domain with `example_file:` links
- `dependencies:` — key AA systems this avatar integrates with
- `tags:` — domain taxonomy

#### 8b — Enrich Existing Manifests (4 avatars missing compliance laws)

| Avatar | Gap | Laws to Add | Skills to Add |
|---|---|---|---|
| `loyalty-aadvantage` | No compliance laws | `BUS-2.2` (Control Framework), `BUS-4.1` (Privacy/PII), `BUS-4.3` (Consent), `ENG-6.4` (Data Protection) | `skill-27-constitution-compliance`, `skill-10-security-review` |
| `cargo-freight` | No compliance laws | `BUS-2.1` (Regulatory Mapping), `BUS-2.4` (Evidence Collection), `ENG-6.1` (Security by Design), `ENG-6.7` (Audit Trail) | `skill-27-constitution-compliance` |
| `check-in-travel` | No compliance laws | `BUS-2.1`, `BUS-2.2`, `BUS-2.4`, `ENG-6.4` (Data Protection for APIS/passport), `ENG-6.7` | `skill-27-constitution-compliance`, `skill-10-security-review` |
| `network-planning-optimization` | No BUS compliance laws | `BUS-2.1`, `BUS-2.4`, `ENG-6.7` | `skill-27-constitution-compliance` |

#### 8c — Add Legacy Rescue Workflow Wiring to All Product-Type Avatars

Currently all product-type avatar manifests only wire to product/greenfield workflows. No avatar activates a legacy rescue workflow — meaning when an agent is operating in avatar context and the user says "refactor this service," the avatar's domain knowledge never flows into the remediation workflow. Every product-type avatar `activates: workflows:` must include the appropriate legacy rescue workflow based on the avatar's brownfield exposure:

| Avatar Characteristic | Add Workflow |
|---|---|
| Has existing codebase with tech debt | `legacy-rescue-decision-track` |
| Handles regulated data (PCI, PII, FAA) | `legacy-rescue-refactor` |
| System likely to be fully rewritten | `legacy-rescue-rewrite` |

Most AA product-type avatars qualify for all three given the age of AA's systems.

---

### Phase 9: SonarQube Compliance Radiator Integration

**Trigger:** Governed workflows currently rely on the coding agent's self-assessment for quality gates ("coverage ≥90%", "complexity ≤10", "zero P0 violations"). Self-reported compliance is not an objective measure — the same model that introduced a violation is also judging whether it's resolved. SonarQube provides externally-authoritative, API-accessible metrics that give compliance radiators independent from the agent, making constitution law enforcement objectively verifiable rather than agent-asserted.

**Design principle:** The agent calls the SonarQube API to *read* objective measures. It does not self-certify. A phase gate does not pass unless SonarQube confirms it passes.

#### 9a — Constitution Law → SonarQube Metric Mapping

The following mapping is the authoritative alignment between constitution laws and SonarQube measures. This becomes the enforcement table used in the new skill and all workflow phase gates:

| Constitution Law | SonarQube Metric | Threshold | Blocking? |
|---|---|---|---|
| `ENG-3.1` Complexity Limits | `cognitive_complexity`, `complexity` | Cyclomatic ≤10, Cognitive ≤7 per function | ✅ Phase gate |
| `ENG-3.4` Single Responsibility | `complexity` per class + file size | Complexity ≤10 per class | ✅ Phase gate |
| `ENG-4.6` Coverage Requirements | `coverage`, `new_coverage` | Overall ≥80%, New code ≥90% | ✅ Phase gate |
| `ENG-4.1` Atomic TDD (no regression) | `new_bugs`, `reliability_rating` | 0 new bugs, Rating A | ✅ Phase gate |
| `ENG-6.1` Security by Design (**NON-NEG**) | `vulnerabilities`, `security_rating` | 0 vulnerabilities, Rating A | 🚨 Hard block |
| `ENG-6.4` Data Protection (**NON-NEG**) | `security_hotspots_reviewed` | 100% reviewed | 🚨 Hard block |
| `ENG-6.5` Input Validation | `vulnerabilities` (injection types) | 0 injection vulnerabilities | 🚨 Hard block |
| `ENG-6.7` Audit Trail (**NON-NEG**) | `security_hotspots` (auth/logging) | 0 unreviewed hotspots | 🚨 Hard block |
| `ENG-3.x` Code Quality | `code_smells`, `sqale_rating` | Rating A (≤5% debt ratio) | ⚠️ Warning gate |
| `ENG-3.x` Duplication | `duplicated_lines_density` | <3% duplication | ⚠️ Warning gate |
| `PRD-7.2` Technical Debt | `sqale_index` (minutes of debt) | Tracked — delta vs. baseline | 📊 Radiator |
| `ENG-4.6` Coverage overall | `line_coverage`, `branch_coverage` | ≥80% both | ✅ Phase gate |

**Hard blocks (🚨)** abort the workflow phase — the agent cannot proceed until SonarQube confirms the metric is cleared.  
**Phase gates (✅)** must pass before the workflow advances to the next phase.  
**Warning gates (⚠️)** are surfaced to the user but do not block — they are tracked in `hangar-ai-specs/`.  
**Radiators (📊)** are reported at every phase for trend visibility.

#### 9b — New Skill: `skill-sonarqube-compliance-gate`

Create `agent-skills/skills-by-domain/platform-engineering/skill-sonarqube-compliance-gate.md`

**Responsibilities:**
- Call SonarQube Web API (`/api/measures/component`) with user-provided API token to retrieve project metrics
- Map retrieved metrics to constitution law IDs using the table in 9a
- Classify findings as HARD_BLOCK / PHASE_GATE / WARNING / RADIATOR
- Generate a `sonarqube-gate-report.md` artifact in `hangar-ai-specs/changes/[id]/` with before/after comparison
- Surface the SonarQube project dashboard URL in the report for human verification

**API token handling:**
- Token is user-provided via environment variable `SONARQUBE_TOKEN` — NEVER committed to source
- SonarQube base URL is user-provided via `SONARQUBE_URL` (e.g. `https://sonarqube.aa.com`)
- Project key is derived from the repo name or explicitly provided
- Skill includes setup instructions for first-time token configuration

**Law citations:** `ENG-3.1`, `ENG-4.6`, `ENG-6.1`, `ENG-6.4`, `ENG-6.7`, `BUS-7.1`  
**Triggers:** `"Run SonarQube gate"`, `"Check compliance metrics"`, `"SonarQube quality check"`, `"What does SonarQube say?"`, `"Verify compliance before merge"`  
**Followed by:** `skill-09-refactoring` (if smells), `skill-10-security-review` (if security block), `skill-spec-governance` (to archive evidence)

#### 9c — Workflow Phase Gate Integration

Each workflow gets SonarQube gate checkpoints at specific phases. The agent calls `skill-sonarqube-compliance-gate` at these points — the phase gate does not pass on agent assertion alone:

**`legacy-rescue-refactor.md`**
| Phase | SonarQube Gate | Metrics Checked |
|---|---|---|
| Phase 1 — Assess | 📸 **Baseline snapshot** | All metrics — establish before-state in `sonarqube-baseline.md` |
| Phase 3 — Characterize | ✅ **Coverage gate** | `coverage` ≥ existing baseline (no regression from characterization) |
| Phase 4 — Remediate | 🚨 **Security hard block** | `vulnerabilities=0`, `security_rating=A`, `security_hotspots_reviewed=100%` |
| Phase 5 — Refactor | ✅ **Quality gate** | `code_smells` ≤ baseline, `complexity` ≤10, `duplicated_lines_density` <3% |
| Phase 6 — Certify | ✅ **Final gate + delta report** | All metrics vs. baseline — delta archived as evidence |

**`legacy-rescue-rewrite.md`**
| Phase | SonarQube Gate | Metrics Checked |
|---|---|---|
| Phase 1 — Assess | 📸 **Baseline snapshot** | Legacy project metrics as violation evidence |
| Phase 4 — Build (each cycle) | ✅ **Per-cycle gate** | `new_bugs=0`, `new_coverage≥90%`, `new_code_smells` tracked |
| Phase 5 — Validate Parity | ✅ **Parity quality gate** | Rewrite metrics must match or improve all baseline metrics |
| Phase 6 — Certify | ✅ **Final gate + delta report** | Before/after comparison in `sonarqube-delta.md` |

**`legacy-rescue-decision-track.md`**
| Phase | SonarQube Gate | Metrics Checked |
|---|---|---|
| Phase 1 — Archaeology | 📸 **Per-context baseline** | Per-bounded-context metrics — feeds REFACTOR/REWRITE decision |
| Phase 3 — Deliberate | 📊 **Decision input** | Coverage <60% + complexity >10 → weight toward REWRITE; otherwise REFACTOR |
| Phase 6 — Certify | ✅ **Final gate** | All contexts meet law thresholds |

**`greenfield-development.md`**
| Phase | SonarQube Gate | Metrics Checked |
|---|---|---|
| Phase 6 — Build (per slice) | ✅ **Per-slice gate** | `new_bugs=0`, `new_coverage≥90%`, no new critical smells |
| Phase 7 — Review | 🚨 **Security hard block** | `vulnerabilities=0`, `security_rating=A` before review passes |
| Phase 8 — Ship | ✅ **Final gate** | All metrics — archived in `sonarqube-final.md` before proposal archived |

**`product-discovery-stage-a-f.md`**  
No code changes occur during discovery — SonarQube not applicable to Stages A–F.

#### 9d — Evidence Artifacts

Every SonarQube gate call produces a structured evidence file in `hangar-ai-specs/changes/[proposal-id]/`:

```
sonarqube-baseline.md      ← Phase 1 snapshot (legacy rescue only)
sonarqube-gate-[phase].md  ← Per-phase gate result
sonarqube-delta.md         ← Final before/after comparison (Certify phase)
```

Each file includes: timestamp, SonarQube project URL, metrics table, law-mapped compliance status, PASS/FAIL verdict. These are the objective compliance audit trail required by `BUS-7.1` and `ENG-6.7`.

---

## Success Criteria

| Criteria | Target |
|---|---|
| Zero `openspec` tool references across all 4 repos | ✅ 0 (grepped and confirmed) |
| `hangar-ai-specs/` used in all constitution-adjacent project folders | ✅ 100% |
| All 5 workflows present in `workflows/` | ✅ 5 |
| Each workflow cites ≥3 laws | ✅ all 5 |
| Each workflow activates ≥2 skills | ✅ all 5 |
| `spec-governance.md` skill replaces `00-openspec.md` | ✅ |
| `product-discovery-orchestration.md` skill added | ✅ |
| `PRD-2.5` added to `laws/product/discovery.md` | ✅ |
| `ENG-11` article added to `laws/engineering/` | ✅ (3 laws) |
| Downstream repos updated | ✅ 3 repos |
| RAG pipeline integrity scan passes | ✅ 0 real broken refs |
| Every law cited in a workflow is enforced by ≥1 composed skill | ✅ Phase 6 — 4 gaps → 0 |
| Every new workflow has a primary skill with a body cross-reference | ✅ Phase 6 — 4 missing → 0 |
| BUS-2.x compliance laws covered in all 3 legacy rescue workflows | Phase 7 — 0 → covered |
| `skill-27-constitution-compliance` composed in legacy rescue workflows | Phase 7 — missing → added |
| Legacy rescue refactor + rewrite activate business + product avatars | Phase 7 — engineering only → all 3 |
| All avatar manifests reference new governed workflow IDs | Phase 7 — 35 stale refs → 0 |
| `aviation-faa` avatar has `manifest.yaml` with new workflow wiring | Phase 7 — ADOPTION.md only → manifest added |
| 5 stub product-type avatars have full `manifest.yaml` | Phase 8 — 0 → 5 |
| 4 manifested avatars enriched with compliance laws + `skill-27` | Phase 8 — missing → covered |
| All product-type avatars activate ≥1 legacy rescue workflow | Phase 8 — 0 of 14 → 14 of 14 |
| `passenger-booking` manifest includes PCI-DSS + DOT law specializations | Phase 8 — stub → governed |
| `crew-training-scheduling` manifest includes FAR Part 117 + DO-178C | Phase 8 — stub → governed |
| `skill-sonarqube-compliance-gate` created with law→metric mapping | Phase 9 — missing → added |
| SonarQube phase gates integrated in 4 of 5 workflows | Phase 9 — 0 → 4 workflows gated |
| Per-phase SonarQube evidence artifacts defined (`sonarqube-*.md`) | Phase 9 — none → BUS-7.1 compliant |
| Security hard blocks (ENG-6.1 NON-NEG) enforced by SonarQube API | Phase 9 — agent-asserted → externally verified |
| Constitution law thresholds align with SonarQube quality gate config | Phase 9 — diverged → aligned |

---

## Open Questions

1. **Constitution's own `hangar-ai-specs/` folder** — The current `openspec/` folder at the constitution root will be renamed. This means the *this proposal* lives inside the folder being renamed. The rename should happen as the first git commit in Phase 1, and all subsequent work references the new path.
2. **ENG-11 article numbering** — Article XI is proposed. Confirm articles VIII and IX do not already exist in `laws/engineering/` to avoid collision. If they do, renumber accordingly.
3. **Greenfield and legacy rescue workflow avatars** — The AA-specific avatars (Cargo, Loyalty, Passenger Booking) should be reviewed to confirm they activate the correct workflows. Avatar manifest updates may be needed.

---

## References

- [Product Discovery Laws](../../laws/product/discovery.md)
- [Roadmap Laws](../../laws/product/roadmap.md)
- [Testing Laws](../../laws/engineering/testing.md)
- [Governance Laws](../../laws/engineering/governance.md)
- [Audit Laws](../../laws/business/audit.md)
- [Current OpenSpec Skill](../../agent-skills/skills-by-domain/discovery-research/00-openspec.md)
- [AA Hangar Product Discovery Agent](../../../aa-hangar-labs/aa-hangar-product-discovery-agent/)
- [AA Hangar Agentic SDLC Workshop](../../hangar-ai-constitution-greenfield/)
- [AA Hangar Constitution Adoption Test](../../hangar-ai-constitution-brownfield/)

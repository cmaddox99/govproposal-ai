# Tasks: constitution-workflow-governance-evolution

**Branch:** `feature/hangar-ai-governance-evolution`  
**Laws governing this work:** `ENG-4.1`, `ENG-11.1` (new), `PRD-2.5` (new), `BUS-7.1`

## Progress Summary

- Completed: 30 / 30 (Phases 1–6 done; all governance reviews complete)
- In Progress: Phases 7, 8, 9 scoped — implementation pending
- Blocked: 0 — pre-existing ENG-10.1 archive violation unchanged (not introduced by this work)

---

## Phase 1: Decouple from OpenSpec Tool

- [x] 1.1 `git mv openspec hangar-ai-specs` — rename governance folder in constitution
- [x] 1.2 Update `AGENTS.md` — remove Hangar SDD commands, update folder refs to `hangar-ai-specs/`, strip external tool references, introduce Hangar SDD terminology
- [x] 1.3 Update `README.md` — introduce Hangar SDD, update structure diagram
- [x] 1.4 **TDD** — Update `structure.py` linter rule: `OpenSpecDirRule` → `HangarAiSpecsDirRule` checking `hangar-ai-specs/` (RED → GREEN → REFACTOR → VERIFY per ENG-4.1)
- [x] 1.5 Update all `docs/guides/` references: `openspec/` → `hangar-ai-specs/`, remove Hangar SDD commands
- [x] 1.6 Update `agent-skills/base/AGENT.md` — remove Hangar SDD refs

## Phase 2: Add Five Governed Workflows

- [x] 2.1 Create `workflows/` directory with `README.md` index
- [x] 2.2 Create `workflows/product-discovery-stage-a-f.md`
- [x] 2.3 Create `workflows/greenfield-development.md`
- [x] 2.4 Create `workflows/legacy-rescue-refactor.md`
- [x] 2.5 Create `workflows/legacy-rescue-rewrite.md`
- [x] 2.6 Create `workflows/legacy-rescue-decision-track.md`

## Phase 3: Update Skills

- [x] 3.1 `git mv` `agent-skills/skills-by-domain/discovery-research/00-openspec.md` → `spec-governance.md`; rewrite content
- [x] 3.2 Create `agent-skills/skills-by-domain/discovery-research/product-discovery-orchestration.md`
- [x] 3.3 Update `agent-skills/skills-by-domain/discovery-research/index.yaml` — reflect renames and new skill

## Phase 4: Add New Laws

- [x] 4.1 Add `PRD-2.5` (Discovery Stage-Gate Law, NON-NEGOTIABLE) to `laws/product/discovery.md`
- [x] 4.2 Create `laws/engineering/spec-driven-development.md` (Article XI: ENG-11.1, ENG-11.2, ENG-11.3)
- [x] 4.3 Update `laws/index.yaml` — add `spec-driven-development.md` to engineering files list; add PRD-2.5 to product article index

## Phase 5: Downstream Repo Updates

- [x] 5.1 **AA Hangar Product Discovery Agent** — `git mv openspec hangar-ai-specs` ✅; `AGENTS.md` updated; `docs/` text refs clean
- [x] 5.2 **AA Hangar Agentic SDLC Workshop** — Fast Track/Weather Dashboard removed from guide, OpenSpec CLI prereq replaced, `openspec/` → `hangar-ai-specs/`, greenfield workflow header added
- [x] 5.3 **AA Hangar Constitution Adoption Test** — `git mv openspec hangar-ai-specs` ✅; `docs/adoption-prompt.md` updated, `README.md` updated, violation inventory and sample tests added

## Phase 6: Workflow Model Integrity Hardening

> **Why:** Post-implementation audit found 4 law coverage gaps and 4 missing RAG cross-references. Every law cited in a workflow must be enforced by at least one composed skill. Every workflow must have a primary skill with a body reference for bidirectional RAG traversal.

### 6a — Law Coverage Fixes (Skill Frontmatter)

- [x] 6.1 `skill-10-security-review` — add `ENG-6.7` (Audit Trail, NON-NEGOTIABLE) to law block; enforced by greenfield, refactor, rewrite workflows
- [x] 6.2 `skill-12-api-design` — add `ENG-7.6` (Idempotency) to law block; enforced by rewrite workflow
- [x] 6.3 `skill-04-business-domain-modeling` — add `PRD-2.2` (Assumption Mapping) to law block; enforced by decision-track workflow Phase 3

### 6b — Missing Skill in Workflow Composition

- [x] 6.4 `workflows/greenfield-development.md` — add `skill-12-api-design` to `skills:` frontmatter list (ENG-1.5 API-First Design must be enforced in Phase 3)

### 6c — Skill→Workflow RAG Cross-References

- [x] 6.5 `skill-07-vertical-slice-dev` — add `See workflows/greenfield-development.md` reference in body
- [x] 6.6 `skill-14-technical-debt` — add `See workflows/legacy-rescue-decision-track.md` reference in body
- [x] 6.7 `skill-09-refactoring` — add `See workflows/legacy-rescue-refactor.md` reference in body
- [x] 6.8 `skill-06-atomic-tdd` — add `See workflows/legacy-rescue-rewrite.md` reference in body

## Phase 7: Compliance Coverage & Avatar-Workflow Wiring

> **Why:** Legacy rescue workflows lack business compliance coverage (BUS-2.x, BUS-4.x, BUS-6.x) and only activate engineering avatars. All 35+ avatar manifests reference stale workflow IDs from pre-governance-evolution, breaking avatar→workflow RAG traversal. Aviation-FAA avatar has no manifest.yaml.

### 7a — Compliance Law & Skill Coverage

- [x] 7.1 Add `skill-27-constitution-compliance` to `skills:` list in all 3 legacy rescue workflows (`decision-track`, `refactor`, `rewrite`)
- [x] 7.2 Add `BUS-2.1`, `BUS-2.2`, `BUS-2.4` to `laws:` frontmatter of `legacy-rescue-refactor.md` and `legacy-rescue-rewrite.md`
- [x] 7.3 Add `BUS-2.1`, `BUS-2.2`, `BUS-2.4` to `laws:` frontmatter of `legacy-rescue-decision-track.md`
- [x] 7.4 Update `avatar_context:` in `legacy-rescue-refactor.md` and `legacy-rescue-rewrite.md` from `[engineering]` → `[engineering, business, product]`
- [x] 7.5 Add `## Compliance Assessment` gate to Phase 1 (Assess) of refactor and rewrite workflows — identify applicable regulations (FAA, DOT, PCI, GDPR) per bounded context before remediation
- [x] 7.6 Add `skill-27-constitution-compliance` `> **Workflow:**` cross-references for all 3 legacy rescue workflows (bidirectional RAG)
- [x] 7.7 Update `skill-27-constitution-compliance` `## Workflow Integration` section — replace stale workflow IDs with new governed workflow IDs

### 7b — Avatar Manifest Workflow ID Update

- [x] 7.8 Create `avatars/industry/aviation-faa/manifest.yaml` — DO-178C, FAR Part 121, DOT compliance specializations; activate on `legacy-rescue-refactor` and `legacy-rescue-rewrite`
- [x] 7.9 Update all **product-type** avatar manifests — replace `workflow-discovery-to-delivery` → `product-discovery-stage-a-f`; replace `workflow-brownfield-adoption` → `legacy-rescue-decision-track`
- [x] 7.10 Update all **technology** avatar manifests — replace `workflow-sdd-lifecycle` → `greenfield-development`; replace `workflow-brownfield-adoption` → `legacy-rescue-decision-track`; replace `workflow-ux-to-implementation` → `greenfield-development`
- [x] 7.11 Update `avatars/index.yaml` — reflect new workflow ID references
- [x] 7.12 **Validation** — grep for all 4 stale workflow IDs: zero remaining references in `avatars/`
- [x] 7.13 **Linter run** — `tools/constitution-lint/` 5/5 post-Phase 7

## Phase 8: Business Avatar Enrichment & Manifest Creation

> **Why:** 5 product-type avatars have no `manifest.yaml` (pure stubs). 4 manifested avatars are missing all compliance law citations. No product-type avatar activates a legacy rescue workflow — AA domain knowledge never flows into remediation workflows. Each avatar is the mechanism that makes governed workflows AA-specific; without correct law citations and skill activations, workflows produce generic engineering plans that miss regulatory obligations.

### 8a — Create Missing Manifests (priority order)

- [x] 8.1 Create `avatars/product-type/passenger-booking/manifest.yaml` — PCI-DSS (card data in search/booking), DOT 14 CFR 250 (denied boarding), DOT refund rules, GDPR (EU passengers), GDS/Sabre API contracts; activate `legacy-rescue-decision-track`, `legacy-rescue-refactor`, `product-discovery-stage-a-f`
- [x] 8.2 Create `avatars/product-type/crew-training-scheduling/manifest.yaml` — FAR Part 117.23/25 (duty/rest), DO-178C (safety-critical software assurance), FAA OE mandate, crew fatigue risk; activate `legacy-rescue-decision-track`, `legacy-rescue-rewrite`, `greenfield-development`; cross-reference `aviation-faa` industry avatar
- [x] 8.3 Create `avatars/product-type/airport-operations/manifest.yaml` — FAR Part 139 (airport certification), DOT IROP consumer protection, TSA coordination, gate assignment constraints; activate `legacy-rescue-decision-track`, `legacy-rescue-refactor`, `product-discovery-stage-a-f`
- [x] 8.4 Create `avatars/product-type/customer-service/manifest.yaml` — DOT Part 250 (denied boarding/IDB/VDB), DOT 7-day/20-day refund rules, 14 CFR 259 customer service plan, CCPA complaint data; activate `legacy-rescue-refactor`, `product-discovery-stage-a-f`
- [x] 8.5 Create `avatars/product-type/internal-productivity/manifest.yaml` — BUS-3.x data governance (employee PII), GDPR/CCPA (workforce data), brand compliance, content classification; activate `greenfield-development`, `legacy-rescue-refactor`

### 8b — Enrich Existing Manifests (compliance law + skill gaps)

- [x] 8.6 Enrich `avatars/product-type/loyalty-aadvantage/manifest.yaml` — add `BUS-2.2`, `BUS-4.1`, `BUS-4.3`, `ENG-6.4` to `specializes_laws:`; add `skill-27-constitution-compliance`, `skill-10-security-review` to `activates: skills:`
- [x] 8.7 Enrich `avatars/product-type/cargo-freight/manifest.yaml` — add `BUS-2.1`, `BUS-2.4`, `ENG-6.1`, `ENG-6.7` to `specializes_laws:`; add `skill-27-constitution-compliance` to `activates: skills:`
- [x] 8.8 Enrich `avatars/product-type/check-in-travel/manifest.yaml` — add `BUS-2.1`, `BUS-2.2`, `BUS-2.4`, `ENG-6.4`, `ENG-6.7` to `specializes_laws:`; add `skill-27-constitution-compliance`, `skill-10-security-review` to `activates: skills:`
- [x] 8.9 Enrich `avatars/product-type/network-planning-optimization/manifest.yaml` — add `BUS-2.1`, `BUS-2.4`, `ENG-6.7` to `specializes_laws:`; add `skill-27-constitution-compliance` to `activates: skills:`

### 8c — Legacy Rescue Workflow Wiring for All Product-Type Avatars

- [x] 8.10 Add `legacy-rescue-decision-track` to `activates: workflows:` in all product-type avatar manifests that don't already have it
- [x] 8.11 Add `legacy-rescue-refactor` to `activates: workflows:` in all regulated-domain avatars (loyalty, cargo, check-in, passenger-booking, airport-ops, customer-service)
- [x] 8.12 Add `legacy-rescue-rewrite` to `activates: workflows:` in avatars where full behavioral rewrite is likely (crew-training-scheduling, legacy-heavy systems)

### 8d — Validation

- [x] 8.13 **Manifest schema check** — all 14 product-type avatars have `manifest.yaml` with `activates:`, `specializes_laws:`, `dependencies:` populated
- [x] 8.14 **Compliance law coverage** — all 14 avatars cite ≥1 BUS law or industry-specific compliance law
- [x] 8.15 **Legacy rescue wiring** — all 14 avatars activate ≥1 legacy rescue workflow
- [x] 8.16 **Linter run** — `tools/constitution-lint/` 5/5 post-Phase 8

## Phase 9: SonarQube Compliance Radiator Integration

> **Why:** Workflow phase gates currently rely on agent self-assessment. The same model that introduced a violation is also judging whether it is resolved. SonarQube provides API-accessible, externally-authoritative metrics that make constitution law thresholds objectively verifiable. Phase gates do not pass on agent assertion alone — they pass when SonarQube confirms they pass.
>
> **Token handling:** `SONARQUBE_TOKEN` and `SONARQUBE_URL` are user-provided environment variables — never committed to source. User provides their token when invoking the skill.

### 9a — Constitution Law → SonarQube Metric Mapping (reference table in PROPOSAL.md)

- [x] 9.1 Define authoritative law→metric mapping in `docs/guides/constitution/sonarqube-law-mapping.md` — the canonical reference for all workflow gates and the new skill

### 9b — New Skill

- [x] 9.2 Create `agent-skills/skills-by-domain/platform-engineering/skill-sonarqube-compliance-gate.md`
  - Frontmatter: laws `ENG-3.1`, `ENG-4.6`, `ENG-6.1`, `ENG-6.4`, `ENG-6.7`, `BUS-7.1`
  - Triggers: `"Run SonarQube gate"`, `"Check compliance metrics"`, `"What does SonarQube say?"`, `"Verify compliance before merge"`, `"SonarQube quality check"`
  - Followed by: `skill-09-refactoring` (smells), `skill-10-security-review` (security block), `skill-spec-governance` (archive evidence)
  - Workflow cross-ref: `See workflows/legacy-rescue-refactor.md`, `See workflows/greenfield-development.md`
  - Body: API call pattern (`/api/measures/component`), HARD_BLOCK/PHASE_GATE/WARNING/RADIATOR classification, evidence artifact template

### 9c — Workflow Phase Gate Updates

- [x] 9.3 Update `workflows/legacy-rescue-refactor.md` — add SonarQube gates at Phase 1 (baseline snapshot), Phase 3 (coverage gate), Phase 4 (security hard block), Phase 5 (quality gate), Phase 6 (final gate + delta)
- [x] 9.4 Update `workflows/legacy-rescue-rewrite.md` — add SonarQube gates at Phase 1 (baseline), Phase 4 (per-cycle gate), Phase 5 (parity quality gate), Phase 6 (final delta)
- [x] 9.5 Update `workflows/legacy-rescue-decision-track.md` — add SonarQube gates at Phase 1 (per-context baseline), Phase 3 (decision input: coverage/complexity feeds REFACTOR/REWRITE verdict), Phase 6 (final gate)
- [x] 9.6 Update `workflows/greenfield-development.md` — add SonarQube gates at Phase 6/Build (per-slice gate), Phase 7/Review (security hard block), Phase 8/Ship (final gate)
- [x] 9.7 Add `skill-sonarqube-compliance-gate` to `skills:` frontmatter of all 4 updated workflows

### 9d — Evidence Artifact Templates

- [x] 9.8 Create `docs/templates/sonarqube-baseline.md` — Phase 1 snapshot template (project URL, timestamp, metrics table, law compliance status)
- [x] 9.9 Create `docs/templates/sonarqube-gate.md` — per-phase gate result template (PASS/FAIL verdict, law → metric → value → threshold, blocking/warning classification)
- [x] 9.10 Create `docs/templates/sonarqube-delta.md` — Certify phase before/after comparison template (all metrics, delta column, improvement %, law compliance change)

### 9e — Validation

- [x] 9.11 **Skill structure check** — `skill-sonarqube-compliance-gate` has triggers, followed_by, law citations, workflow cross-refs
- [x] 9.12 **Workflow gate check** — all 4 updated workflows have ≥1 SonarQube gate per phase that was previously agent-asserted
- [x] 9.13 **Hard block verification** — ENG-6.1, ENG-6.4, ENG-6.7 (all NON-NEGOTIABLE) are mapped to HARD_BLOCK classification in the skill
- [x] 9.14 **Token security check** — grep confirms `SONARQUBE_TOKEN` never appears as a literal value in any committed file
- [x] 9.15 **Linter run** — `tools/constitution-lint/` 5/5 post-Phase 9

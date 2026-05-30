# Tasks: Hangar AI Constitution — Complete Adoption Guide

**Changeset:** `build-adoption-guide-2026-001`
**Authority:** ENG-11.1 ⛔ — all tasks require jury UNANIMOUS APPROVE before execution
**Alexandra Pierce:** Active monitor — VETO on any non-negotiable violation
**Version:** 2.0 — atomized per Round 1 remediation (2026-05-01)

---

## Phase 0 — Pre-Deliberation Rendering Gates (ENG-13.1 ⛔, ENG-13.3)

These tasks are prerequisites for ANY jury deliberation. No jury session may begin before both are complete.

- [x] **T0.1** Render `PROPOSAL.md` to `PROPOSAL.html` via `aa-artifact-render PROPOSAL.md --artifact-type proposal --laws-dir laws/`
- [x] **T0.2** Render `PROPOSAL.md` to `PROPOSAL.pdf` via `aa-artifact-render PROPOSAL.md --artifact-type proposal --laws-dir laws/ --pdf`
- [x] **T0.3** Render `tasks.md` to `tasks.html` via `aa-artifact-render tasks.md --artifact-type tasks --laws-dir laws/`
- [x] **T0.4** Render `tasks.md` to `tasks.pdf` via `aa-artifact-render tasks.md --artifact-type tasks --laws-dir laws/ --pdf`
- [x] **T0.5** Verify `PROPOSAL.html` and `tasks.html` are present in folder contract before Round 2 jury deliberation — **Alexandra Pierce Round 2 APPROVE (2026-05-01) satisfies this gate**

---

## Phase 1 — Compliance Artifact Creation (BUS-1.3, BUS-2.x, BUS-3.1 ⛔, BUS-6.1 ⛔, ENG-6.1 ⛔, BUS-9.3 ⛔)

These artifacts are required before Stage C begins (Gates G5, G6, G7). They are authored by the agent and reviewed by Carlos Mendez and Alexandra Pierce.

- [ ] **T1.1** Create `compliance/` directory under `hangar-ai-specs/changes/build-adoption-guide-2026-001/`
- [ ] **T1.2** Author `compliance/regulatory-scope.md` — BUS-2.x scoping per §9 PROPOSAL.md
  - [ ] T1.2a BUS-2.1 (FAA) in/out scope determination with rationale
  - [ ] T1.2b BUS-2.2 (Control Framework) control mapping
  - [ ] T1.2c BUS-2.3 (DOT / accessibility) scope determination with AA legal reference
  - [ ] T1.2d BUS-2.4 (Evidence Collection) retention confirmation
  - [ ] T1.2e Carlos Mendez + Alexandra Pierce review — APPROVE required
- [ ] **T1.3** Author `compliance/data-classification.md` — BUS-3.1 ⛔ table per §10 PROPOSAL.md
  - [ ] T1.3a Classify all data assets (proposal docs, evidence files, deliberation log, sonarqube delta, analytics events)
  - [ ] T1.3b Define retention schedule per asset
  - [ ] T1.3c Carlos Mendez + Alexandra Pierce review — APPROVE required
- [ ] **T1.4** Author `compliance/threat-model.md` — ENG-6.1 ⛔ threat model
  - [ ] T1.4a Define trust boundaries for the adoption guide system
  - [ ] T1.4b Identify threat actors (unauthorized amendment, guide tampering, stale guide shipped)
  - [ ] T1.4c Map threats to controls (branch protection, ENG-11.3 freshness, ENG-13.1 rendering gate)
  - [ ] T1.4d Tomás Reyes + Alexandra Pierce review — APPROVE required
- [ ] **T1.5** Author `compliance/risk-register.md` — BUS-6.1 ⛔ per §12 PROPOSAL.md
  - [ ] T1.5a Document all risks from §12 table with full assessment fields
  - [ ] T1.5b Add registry integrity anomaly (BUS-2.2 / BUS-6.1 comment mismatch) as confirmed risk — escalation to constitution maintainer
  - [ ] T1.5c Carlos Mendez + Alexandra Pierce review — APPROVE required
- [ ] **T1.6** Author `compliance/raci.md` — BUS-1.3 RACI matrix per §11 PROPOSAL.md
  - [ ] T1.6a Accountability matrix for all compliance obligations
  - [ ] T1.6b Carlos Mendez review — APPROVE required
- [ ] **T1.7** Author `compliance/incident-response.md` — BUS-9.3 ⛔ incident response plan
  - [ ] T1.7a Incident classification (P1–P4 per BUS-9.1)
  - [ ] T1.7b Response process (Preparation, Detection, Containment, Eradication, Recovery, Lessons Learned per BUS-9.2)
  - [ ] T1.7c 72-hour GDPR breach notification window and DPO contact chain per BUS-9.3 ⛔
  - [ ] T1.7d Carlos Mendez + Alexandra Pierce review — APPROVE required
- [ ] **T1.8** Initialize `compliance/evidence-manifest.sha256` — BUS-7.2 SHA-256 hash manifest
  - [ ] T1.8a Generate SHA-256 hashes for all currently filed evidence files
  - [ ] T1.8b Commit manifest; update at every stage gate transition going forward
- [ ] **T1.9** Jury deliberation: Phase 1 compliance artifacts — UNANIMOUS APPROVE across all 6 jurors

---

## Phase 2 — Discovery Gates (PRD-2.5 ⛔)

No stage may begin without prior stage exit criteria met and evidence filed.

- [x] **T2.1** Stage A: Problem Framing — COMPLETE (`stage-a-evidence.md` + `stage-a-evidence.html` filed)
- [ ] **T2.2** Stage B: Assumption Mapping
  - [ ] T2.2a Map all adopter assumptions (what do we assume is true about each persona's pain and workflow?)
  - [ ] T2.2b Conduct ≥ 3 structured interviews with technical coaches who have onboarded teams
  - [ ] T2.2c Conduct competitive analysis — what other adoption guides or constitution references exist? (PRD-2.4)
  - [ ] T2.2d Reclassify evidence: WEAK → Moderate or Strong (or STOP and reassess problem if evidence contradicts §1)
  - [ ] T2.2e Author `stage-b-evidence.md` with all interview findings and classification rationale
  - [ ] T2.2f Jury deliberation: Stage B evidence — UNANIMOUS APPROVE required before Stage C begins (G3)
- [ ] **T2.3** Stage C: Jobs-To-Be-Done *(BLOCKED until T2.2f passes)*
  - [ ] T2.3a Frame adopter needs as jobs for all 3 personas (Technical Coach, Senior Architect, Engineer)
  - [ ] T2.3b Validate 5+ interview contacts per persona per PRD-3.1 (or document exception with evidence)
  - [ ] T2.3c Author journey maps per PRD-3.2 for each persona
  - [ ] T2.3d Author `stage-c-evidence.md`
  - [ ] T2.3e Jury deliberation: Stage C evidence — UNANIMOUS APPROVE required before Stage D
- [ ] **T2.4** Stage D: Solution Exploration *(BLOCKED until T2.3e passes)*
  - [ ] T2.4a Present full 10-page IA design to jury — confirm architecture is the right solution to validated JTBD
  - [ ] T2.4b Define page contracts: inputs / outputs / law bindings / learning outcomes for each of P1–P10
  - [ ] T2.4c Define experience principles (PRD-3.4)
  - [ ] T2.4d **Author user stories** — for each persona path (Technical Coach, Senior Architect, Engineer), write user stories per PRD-3.3 standard format: "As a [persona], I want [action] so that [outcome]" with testable acceptance criteria. Minimum 3 stories per persona path covering the primary JTBD identified in Stage C. Stories must have AC that can be verified against the delivered pages.
  - [ ] T2.4e Author `stage-d-evidence.md`
  - [ ] T2.4f Jury deliberation: Stage D IA design — UNANIMOUS APPROVE required before Stage E
- [ ] **T2.5** Stage E: Prototype Validation *(BLOCKED until T2.4e passes)*
  - [ ] T2.5a Build P1 Landing Page + P3 Quick Start (Technical Coach + Senior Architect paths) as MVP
  - [ ] T2.5b Conduct ≥ 3 facilitator-observed MVP walkthroughs (stopwatch first-successful-task measurement)
  - [ ] T2.5c Measure retention signal at 2-week follow-up
  - [ ] T2.5d Author `stage-e-evidence.md` with walkthrough results
  - [ ] T2.5e Jury deliberation: Stage E prototype — UNANIMOUS APPROVE required before Stage F
- [ ] **T2.6** Stage F: Go/No-Go Decision *(BLOCKED until T2.5e passes)*
  - [ ] T2.6a Jury votes on full 10-page implementation — UNANIMOUS APPROVE required
  - [ ] T2.6b If NO-GO: pivot scope per PRD-5.2 BML trigger; re-enter Stage D
  - [ ] T2.6c Author `stage-f-evidence.md`

---

## Phase 3 — Foundation (ENG-12.1 ⛔ Gate Setup)

*BLOCKED until Stage F Go/No-Go APPROVE and Gate G2 met.*

- [ ] **T3.0** Set up CI/CD freshness workflow (ENG-11.3, §3 spec — OR-logic staleness detection)
  - [ ] T3.0a Create `.github/workflows/freshness-check.yml` per spec in PROPOSAL.md §3; staleness condition is OR-logic: fail if source SHA changed since last render **OR** embedded timestamp > 30 days old (both conditions are independently blocking)
  - [ ] T3.0b Verify workflow fires on PR and push to `main`
  - [ ] T3.0c Add `freshness-check` as required status check in branch protection settings
  - [ ] T3.0d Jordan Ellis verification — workflow passes on clean repo state before first HTML commit
- [ ] **T3.1** Provision SonarQube instance for this project
  - [ ] T3.1a Add `.sonar-token` to `.gitignore` before any code is written
  - [ ] T3.1b Open SonarQube dashboard — confirm it is reachable before Phase 3 IMPLEMENT begins
  - [ ] T3.1c Jordan Ellis verification — Gate G2 PASS confirmation
- [ ] **T3.2** Register P2 (Constitutional AI Model Viz) in adoption guide navigation
  - [ ] T3.2a Add back-navigation link from P2 to P1 Landing Page
  - [ ] T3.2b Verify P2 is ENG-13.1 self-contained (no external dependencies)
  - [ ] T3.2c Verify P2 contains a "Questions to Explore" block with 3–5 open-ended coaching prompts and no predefined answers, per §3 Socratic Design Requirement (SHALL — applies to all 10 pages); if block is absent, add it before T3.2d
  - [ ] T3.2d Jury deliberation: P2 registration — UNANIMOUS APPROVE
- [ ] **T3.3** Set up JS test infrastructure (ENG-4.1 ⛔, §3 JS Test Infrastructure spec)
  - [ ] T3.3a Install Vitest: `npm init -y && npm install -D vitest`
  - [ ] T3.3b Create `p4-search.test.js` and `p6-wizard.test.js` stub files with one failing test each
  - [ ] T3.3c Verify `npx vitest run` fails on stubs (confirms test harness is wired)
  - [ ] T3.3d Add `npx vitest run` as CI step in `.github/workflows/freshness-check.yml` or a separate `test.yml`
  - [ ] T3.3e Jordan Ellis verification — Gate G4 infrastructure confirmed before Phase 4
  - [ ] T3.3f Install Stryker mutation testing: `npm install -D @stryker-mutator/core @stryker-mutator/vitest-runner` — required before Phase 5 T5.3i and Phase 6 T6.5g mutation gates (ENG-4.11)

---

## Phase 4 — MVP Pages (P1 + P3)

*BLOCKED until T3.1c (G2) and T2.6 (Stage F) pass.*

### P1: Landing Page

- [ ] **T4.1** Source data extraction
  - [ ] T4.1a Extract constitution overview from `laws/index.yaml` (version, domain counts, law counts, NN counts)
  - [ ] T4.1b Extract persona entry points (3 personas: Technical Coach, Senior Architect, Engineer)
  - [ ] T4.1c Extract navigation structure (links to P2–P10 + P2 existing path)
- [ ] **T4.2** Build P1 HTML — self-contained, ENG-13.1 ⛔ compliant
- [ ] **T4.3** Apply ENG-13.2 citation tooltips to all law citations in P1
- [ ] **T4.4** Add "Questions to Explore" coaching block (3–5 prompts, no predefined answers per Socratic design)
- [ ] **T4.5** ENG-13.1 self-containment check — no external CSS/JS/font dependencies
- [ ] **T4.6** Render P1 via `aa-artifact-render` (HTML + PDF) before jury deliberation
- [ ] **T4.7** Jury deliberation: P1 — UNANIMOUS APPROVE across all 6 jurors

### P3: Quick Start Guide (Technical Coach + Senior Architect paths — MVP scope)

- [ ] **T4.8** Source data extraction
  - [ ] T4.8a Extract Technical Coach path: Socratic guidance pattern (AGENT.md §1.2–1.3) + Discovery and Planning operating modes (AGENT.md §4.1, §4.2) as primary onboarding modes + coaching-specific skill triggers
  - [ ] T4.8b Extract Senior Architect path: AGENT.md §3.3 Guardrail Enforcement Protocol (Stop→Cite→Explain→Guide→Verify) as the primary enforcement sequence for architects evaluating constitutional alignment + architecture-specific skill triggers (ENG-2.x DDD, ENG-6.x security)
  - [ ] T4.8c Map operating modes from AGENT.md §4 (Discovery: §4.1, Planning: §4.2, Implementation: §4.3, Review: §4.4) to each persona — note which modes are primary for each persona path
- [ ] **T4.9** Build P3 HTML — Technical Coach and Senior Architect paths only (Engineer path in Phase 6)
- [ ] **T4.10** Apply ENG-13.2 citation tooltips to all law citations in P3
- [ ] **T4.11** Add "Questions to Explore" coaching block per persona path
- [ ] **T4.12** Add learning outcome statement at top of each path ("After completing this path you will be able to…")
- [ ] **T4.13** ENG-13.1 self-containment check
- [ ] **T4.14** Render P3 via `aa-artifact-render` (HTML + PDF) before jury deliberation
- [ ] **T4.15** Jury deliberation: P3 MVP — UNANIMOUS APPROVE across all 6 jurors

### MVP Validation Gate

- [ ] **T4.16** Conduct ≥ 3 facilitator-observed walkthroughs of P1 + P3 (stopwatch measurement)
- [ ] **T4.17** Measure retention signal at 2-week follow-up
- [ ] **T4.18** File `stage-e-evidence.md` with walkthrough results (if not already filed in Stage E)
- [ ] **T4.19** SonarQube delta review at end of Phase 4 — file `hangar-ai-specs/evidence/sonarqube-delta.md` (G11)
- [ ] **T4.20** Jury deliberation: MVP validation results — UNANIMOUS APPROVE before Phase 5

---

## Phase 5 — Core Reference Pages (P4 + P5)

*BLOCKED until T4.20 (MVP validation APPROVE).*

### P4: Laws Reference

- [ ] **T5.1** Source: confirm `laws/index.yaml` is current (ENG-11.3 staleness check)
- [ ] **T5.2** Extract all 168 law IDs with titles, summaries, NN flags from `laws/index.yaml` + law file YAML frontmatter
- [ ] **T5.3** Write search JavaScript — atomic TDD required (ENG-4.1 ⛔, Gate G4)
  - [ ] T5.3a Write failing test for search by law ID
  - [ ] T5.3b Implement — pass test
  - [ ] T5.3c Write failing test for search by title keyword
  - [ ] T5.3d Implement — pass test
  - [ ] T5.3e Write failing test for filter by domain (ENG / PRD / BUS)
  - [ ] T5.3f Implement — pass test
  - [ ] T5.3g Write failing test for NN flag filter
  - [ ] T5.3h Implement — pass test
  - [ ] T5.3i Mutation test score ≥ 70% overall baseline (ENG-4.11)
- [ ] **T5.4** Build P4 HTML — searchable, filterable, all 168 laws, zero manually entered law entries
- [ ] **T5.5** Apply ENG-13.2 citation tooltips
- [ ] **T5.6** Add "Questions to Explore" coaching block
- [ ] **T5.7** ENG-13.1 self-containment check — search JS inlined
- [ ] **T5.8** Render P4 via `aa-artifact-render` (HTML + PDF)
- [ ] **T5.9** Alexandra Pierce: verify zero invented laws — required before jury deliberation
- [ ] **T5.10** Jury deliberation: P4 — UNANIMOUS APPROVE

### P5: Skills Catalog

- [ ] **T5.11** Source: confirm all `agent-skills/*/index.yaml` files are current
- [ ] **T5.12** Extract all skills: trigger phrases, law bindings, chaining relationships, operating mode mappings
- [ ] **T5.13** Build P5 HTML — all 29+ skills, filterable by operating mode
- [ ] **T5.14** Apply ENG-13.2 citation tooltips to all skill law bindings
- [ ] **T5.15** Add "Questions to Explore" coaching block
- [ ] **T5.16** ENG-13.1 self-containment check
- [ ] **T5.17** Render P5 via `aa-artifact-render` (HTML + PDF)
- [ ] **T5.18** Jury deliberation: P5 — UNANIMOUS APPROVE
- [ ] **T5.19** SonarQube delta review at end of Phase 5 — update `hangar-ai-specs/evidence/sonarqube-delta.md` (G11)

---

## Phase 6 — Advanced Guide Pages (P6 + P7 + P8 + P9 + P10 + P3 Engineer path)

*BLOCKED until Phase 5 APPROVE.*

### P3 Engineer Path (appended to existing P3)

- [ ] **T6.1** Extract Engineer path: AGENT.md §1.4 Teaching Feedback Loop (Observe→Guide→Explain→Demonstrate→Verify→Reinforce — 6 steps) as the primary operating sequence for engineers working under the constitution + engineering-specific skill triggers (TDD gates, SonarQube, SDD workflow). Note: §1.4 is 6 steps, not 5; the earlier T4.8b reference to §3.3 is the Architect enforcement sequence (Stop→Cite→Explain→Guide→Verify — 5 steps); these are distinct AGENT.md sections for distinct personas.
- [ ] **T6.2** Add Engineer path to P3 HTML
- [ ] **T6.3** Jury deliberation: P3 Engineer path addition — UNANIMOUS APPROVE

### P6: Avatar Selection Wizard

- [ ] **T6.4** Source: confirm `AVATAR-RAG-INDEX.yaml` and `avatars/` are current
- [ ] **T6.5** Write wizard JavaScript — atomic TDD required (ENG-4.1 ⛔, Gate G4)
  - [ ] T6.5a Write failing test for selection state machine (industry → product-type → tech-stack)
  - [ ] T6.5b Implement — pass test
  - [ ] T6.5c Write failing test for avatar recommendation logic
  - [ ] T6.5d Implement — pass test
  - [ ] T6.5e Write failing test for laws + skills surfacing per selection
  - [ ] T6.5f Implement — pass test
  - [ ] T6.5g Mutation test score ≥ 70%
- [ ] **T6.6** Build P6 HTML — interactive wizard, all inputs inline, ENG-13.1 ⛔ compliant
- [ ] **T6.7** Apply ENG-13.2 citation tooltips
- [ ] **T6.8** Add "Questions to Explore" coaching block
- [ ] **T6.9** ENG-13.1 self-containment check — wizard JS inlined
- [ ] **T6.10** Render P6 via `aa-artifact-render` (HTML + PDF)
- [ ] **T6.11** Jury deliberation: P6 — UNANIMOUS APPROVE

### P7: SDD Workflow Guide

- [ ] **T6.12** Source: confirm ENG-11.1 ⛔ law text and folder contract spec are current
- [ ] **T6.13** Build P7 HTML: PROPOSE→IMPLEMENT→ARCHIVE flow, annotated folder contract, ENG-11.2 checklist
- [ ] **T6.14** Apply ENG-13.2 citation tooltips
- [ ] **T6.15** Add "Questions to Explore" coaching block
- [ ] **T6.16** ENG-13.1 self-containment check
- [ ] **T6.17** Render P7 via `aa-artifact-render` (HTML + PDF)
- [ ] **T6.18** Jury deliberation: P7 — UNANIMOUS APPROVE

### P8: Compliance Checklist

- [ ] **T6.19** Source: confirm ENG-12.1 ⛔, ENG-12.2, ENG-12.3 law text current
- [ ] **T6.20** Build P8 HTML: phase gate criteria, SonarQube gate protocol, ENG-12.1 human-review requirement
- [ ] **T6.21** Apply ENG-13.2 citation tooltips
- [ ] **T6.22** Add "Questions to Explore" coaching block
- [ ] **T6.23** ENG-13.1 self-containment check
- [ ] **T6.24** Render P8 via `aa-artifact-render` (HTML + PDF)
- [ ] **T6.25** Jury deliberation: P8 — UNANIMOUS APPROVE

### P9: Agentic Feedback Loop Guide

- [ ] **T6.26** Source: confirm `laws/engineering/agentic-feedback.md` HARD_BLOCK conditions current
- [ ] **T6.27** Build P9 HTML: human-in-the-loop contract, HARD_BLOCK conditions table, gate flow diagram
- [ ] **T6.28** Apply ENG-13.2 citation tooltips
- [ ] **T6.29** Add "Questions to Explore" coaching block
- [ ] **T6.30** ENG-13.1 self-containment check
- [ ] **T6.31** Render P9 via `aa-artifact-render` (HTML + PDF)
- [ ] **T6.32** Jury deliberation: P9 — UNANIMOUS APPROVE

### P10: Amendment Process

- [ ] **T6.33** Source: confirm ENG-10.1 ⛔ through ENG-10.5 law text current
- [ ] **T6.34** Build P10 HTML: ENG-10.x governance hierarchy, law precedence table, NN amendment path (executive approval required)
- [ ] **T6.35** Apply ENG-13.2 citation tooltips (critical: ENG-10.2 = Enforcement Tracking Law; ENG-10.3 = Compliance Reporting Law)
- [ ] **T6.36** Add "Questions to Explore" coaching block
- [ ] **T6.37** ENG-13.1 self-containment check
- [ ] **T6.38** Render P10 via `aa-artifact-render` (HTML + PDF)
- [ ] **T6.39** Jury deliberation: P10 — UNANIMOUS APPROVE
- [ ] **T6.40** SonarQube delta review at end of Phase 6 — update `hangar-ai-specs/evidence/sonarqube-delta.md` (G11)

---

## Phase 7 — Pre-Release Gates

*BLOCKED until all Phase 6 APPROVE.*

- [ ] **T7.1** WCAG 2.1 AA accessibility audit — all 10 pages (Gate G8, BUS-1.1 ⛔)
  - [ ] T7.1a Automated audit (axe-core or equivalent) on all 10 pages
  - [ ] T7.1b Manual screen reader walkthrough (at minimum P1, P3, P4)
  - [ ] T7.1c Obtain ADA / Section 508 / 14 CFR Part 382 legal determination from AA Legal
  - [ ] T7.1d Carlos Mendez sign-off — APPROVE required
- [ ] **T7.2** Full ENG-13.1 compliance audit — Alexandra Pierce code review all 10 pages (no external deps)
- [ ] **T7.3** Full ENG-13.2 tooltip audit — automated span count vs citation count on all 10 pages
- [ ] **T7.4** Law citation accuracy audit — all 10 pages verified against `laws/index.yaml` v2.0.0 by Alexandra Pierce
- [ ] **T7.5** SonarQube gate final run — ENG-12.1 ⛔ (Gate G10)
  - [ ] T7.5a Human opens SonarQube dashboard and reviews results
  - [ ] T7.5b PASS confirmed before archive
  - [ ] T7.5c File final `hangar-ai-specs/evidence/sonarqube-delta.md`
- [ ] **T7.6** Jury final review — all 10 pages as a complete guide — UNANIMOUS APPROVE across all 6 jurors

---

## Phase 8 — Archive (ENG-11.1 ⛔)

- [ ] **T8.1** Update `PROGRESS.md` to COMPLETE with all gate evidence links
- [ ] **T8.2** Update `compliance/evidence-manifest.sha256` with SHA-256 hashes of all final artifacts
- [ ] **T8.3** Move changeset folder to `hangar-ai-specs/archive/2026-MM-DD-build-adoption-guide-2026-001/`
- [ ] **T8.4** Schedule internal audit per BUS-7.4 for 30 days post-release

---

*All tasks blocked on UNANIMOUS jury approval · Alexandra Pierce monitoring active · v2.5 — atomized per Round 6 jury findings (2026-05-01)*

# PROPOSAL: Hangar AI Constitution — Complete Adoption Guide

**Changeset ID:** `build-adoption-guide-2026-001`
**SDD Phase:** PROPOSE
**Authority:** ENG-11.1 ⛔ (NON-NEGOTIABLE)
**Status:** APPROVED — ADVANCE TO IMPLEMENT
**Version:** 2.6 — SD-OBL-4 amendment (2026-05-07): `< 20 min` → `< 60 min` per Stage B interview evidence | Jury-cleared 2026-05-07
**Round 1 Summary:** 79 objections across 6 jurors; 1 active BLOCK (ENG-13.1); 10 missing NN citations; 4 fabricated law titles; 3 misapplications; structural gaps in MVP scoping, personas, and compliance. All items remediated in v2.0.
**Round 2 Summary:** 5 OBJECT / 1 APPROVE. 17 findings. All remediated in v2.1 (Teaching Loop, P3 outcome, coach mode, ENG-2.3, ENG-6.7 audit arch, PRD-5.1 Timeline, PRD-5.3 full experiment design, PRD-3.3 user story task, BUS-3.6 scoped out, BUS-3.3 calendar minimums, BUS-9.3 DPO Stage B, R-08 BUS-3.1 added, evidence rubric, sonarqube-delta-schema.md, CI/CD spec, Vitest, Phase 0 gates closed, PRD-6.3 cited).
**Round 3 Summary:** 4 OBJECT / 2 APPROVE. 6 findings. Remediated in v2.2: PRD-5.1 ⛔ kill-if contradiction resolved; ENG-11.3 freshness check OR-logic; ENG-6.7 ⛔ SIEM scope-out; T3.2d added; T3.3f added; T4.8b clarified; crosswalk note P10; ENG-1.4 added; citation count 72; BUS-3.6 in R-08.
**Round 4 Summary:** 2 OBJECT / 4 APPROVE. Remediated in v2.3: T6.1 §1.4 specified; ENG-2.1/2.2 scope-outs added; §2 MVT guardrail AND condition added; §12 R-08 updated to 6 anomalies; raci.md BUS-1.3 deferral; ENG-10.1/ENG-11.1 titles confirmed; citation count 74.
**Round 5 Summary:** 1 OBJECT / 5 APPROVE. Remediated in v2.4: §2 MVT quantifier "2 of 3" → "≥ 2 of 3" in both legs; §8 NOW bullet dual-condition added; R-08 escalation updated with 7th anomaly (ENG-12.x absent from law_ids.engineering).
**Round 6 Summary:** 1 OBJECT / 5 APPROVE. Remediated in v2.5: §12 inline risk table row updated to "7 anomalies total" with ENG-12.x enumerated — body now consistent with the Round 5 Summary header declaration and the full risk-register.md escalation.
**Round 7 Summary:** UNANIMOUS 6/6 APPROVE (2026-05-02). Alexandra Pierce constitutional clearance granted — all 23 NNs verified, all law titles confirmed non-fabricated, §12 body/escalation fully consistent. Proposal cleared to ADVANCE TO IMPLEMENT per ENG-11.1 ⛔, ENG-11.2, BUS-6.1 ⛔, BUS-1.1 ⛔.

---

## 1. Problem Statement (PRD-1.2 ⛔)

Engineers, technical coaches, and senior architects adopting the Hangar AI Constitution encounter a fragmented onboarding experience. The laws, skills, avatars, and RAG model exist as isolated artifacts across `laws/`, `agent-skills/`, `avatars/`, and `docs/` — but there is no unified, navigable, persona-aware entry point connecting all components into a coherent adoption path.

**Evidence Classification (PRD-1.5 ⛔):** WEAK — repository structural inspection only; no customer interviews on file at time of proposal. This is a known weak-evidence submission per PRD-1.5. A validation plan is provided below. Stage C (JTBD) WILL NOT begin until evidence is reclassified to Moderate (3+ structured interviews or equivalent quantitative proxy).

**Observed Evidence (Repository Inspection):**

- No landing page exists — `README.md` is the only structural index
- No persona-based quick start exists for distinct adopter types
- The RAG model visualization has no parent navigation or guide context
- Technical coaches cannot present a single URL that walks a new team through adoption
- The SDD workflow guide (PROPOSE→IMPLEMENT→ARCHIVE) has no interactive reference format
- The 168 laws are navigable only by reading raw markdown files
- Avatar selection requires manual exploration of `avatars/` — no wizard or decision path

**PRD-1.2 Problem Template:**
- **Who:** Technical coaches and senior architects onboarding new engineering teams to the Hangar AI Constitution
- **Problem:** No unified, navigable, persona-aware entry point; adopters must manually explore 10+ fragmented entry points
- **Evidence:** Repository inspection (WEAK — see validation plan below)
- **Frequency:** Every new team onboarding; estimated 3–5 engagements per quarter per coach
- **Severity:** HIGH — adoption friction compounds across every new team and project engagement

**Validation Plan (PRD-1.5 Weak Exception):**
- Stage B task: Conduct 3+ structured interviews with technical coaches who have onboarded teams to the constitution
- Stage B task: Collect quantitative proxy evidence from existing adoption logs, support channels, or ticket trackers
- Evidence artifact: `hangar-ai-specs/changes/build-adoption-guide-2026-001/stage-b-evidence.md`
- Gate: Stage C WILL NOT begin until `stage-b-evidence.md` is filed AND jury-validated at Moderate or Strong

---

## 2. MVP Definition (PRD-5.1 ⛔)

> *"MVPs SHALL be the smallest experiment to validate learning, not a crappy first version." — PRD-5.1*

**Riskiest Assumption:** A unified landing page with persona-aware quick start paths (Technical Coach + Senior Architect) will meaningfully reduce time-to-first-successful-task compared to the current README-only entry point.

**MVP Hypothesis:** If we ship P1 (Landing Page) + P3 (Quick Start — Technical Coach and Senior Architect paths only), then first-successful-task time will decrease from the Stage B baseline (2–3 hours with README-only entry point) to < 60 minutes, measured during 3+ facilitator-observed walkthroughs with real adopters. *(SD-OBL-4 amendment: original `< 20 min` replaced by `< 60 min` based on Stage B interview data — Jay Turpin: 2–3 hrs, Wyatt Sutherland: 1–3 hrs, Kenneth Robinson: 2 hrs. Evidence in stage-b-evidence.md §3.)*

**MVP Scope (NOW horizon only):**
- P1: Landing Page — navigation hub, 3-persona entry points
- P3: Quick Start Guide — Technical Coach and Senior Architect paths only
- P2: Registered (already built — connect landing navigation)

**Out of MVP Scope (NEXT/LATER — pending MVP validation):**
- P4–P10 (deferred pending MVP validation signal)
- Engineer persona quick start path (deferred to NEXT)
- All analytics / behavioral telemetry (deferred behind BUS-4.5 PIA — LATER only)

**Minimum Validation Threshold:** MVP is considered validated when ≥ 2 of 3 observed walkthroughs achieve first-successful-task in < 60 minutes without facilitator prompting AND ≥ 2 of 3 adopters pass the guardrail metric (no misidentification of a non-negotiable law post-walkthrough). Both conditions must hold; task time alone is not sufficient. *(SD-OBL-4: `< 20 min` → `< 60 min` per Stage B evidence.)*

**Timeline (PRD-5.1 ⛔ — sixth required field):** The MVP experiment runs for 4 weeks after P1 + P3 ship. Walkthroughs are conducted within the first 2 weeks of ship. Retention signal is measured at Week 4 (2 weeks post-walkthrough). The go/no-go call is made at Week 4 — no later. The scheduling-failure kill trigger in the experiment table below is the sole governing rule for what happens if walkthroughs cannot be scheduled; see kill-if row.

**Experiment Design (PRD-5.3):**

| Field | Value |
|-------|-------|
| **Hypothesis** | If we ship P1 + P3 (Technical Coach and Senior Architect paths), then first-successful-task time will decrease from the Stage B baseline (2–3 hrs) to < 60 min, for ≥ 2 of 3 real adopters |
| **Experiment type** | Concierge — facilitator-observed walkthroughs with real Technical Coaches and Senior Architects using the live guide |
| **Control condition** | Current `README.md`-only entry point — baseline task time formally measured in Stage B as part of assumption mapping; used as the comparison denominator in Stage E |
| **Primary metric** | First-successful-task time (stopwatch: landing page load → adopter declares task complete, without facilitator prompt) |
| **Secondary metric** | Adopter retention signal: returns to guide ≥ 2 times within 2 weeks of walkthrough (self-reported) |
| **Guardrail metric** | Adopter does not misidentify a non-negotiable (⛔) law — verified by Technical Coach juror post-walkthrough verbal check. A walkthrough that passes on task time but produces NN law misconceptions is not counted as a success. |
| **Sample** | n ≥ 3 real adopters (Technical Coaches or Senior Architects); n=3 is below statistical significance threshold — this is explicitly acknowledged; the experiment tests for signal, not significance |
| **Segments** | Included: Technical Coaches and Senior Architects who have worked on at least one AA project under the constitution. Excluded: Engineers (path not in MVP scope), adopters with < 1 week familiarity with the constitution |
| **Ship if** | ≥ 2 of 3 walkthroughs achieve task time < 60 min AND ≥ 2 of 3 adopters pass the guardrail metric |
| **Iterate if** | 1 of 3 walkthroughs succeed on task time; or all pass task time but 1 fails guardrail — team narrows scope or revises P3 path structure, then re-runs 1 additional walkthrough |
| **Kill if** | (a) 0 of 3 walkthroughs achieve task time < 60 min; or (b) 2 of 3 fail the guardrail metric; or (c) walkthroughs cannot be scheduled within 2 weeks of P1+P3 ship date — one-time 1-week extension is permitted if a scheduling blocker is documented in the risk register; if walkthroughs still cannot begin by week 3, kill fires. When any kill criterion fires, the team re-enters Stage D and re-validates IA design before any new build. No further extensions permitted. |
| **Minimum detectable effect** | Not statistically computable at n=3. Effect size must be directionally large (> 50% reduction in task time) to be meaningful at this sample size. A reduction from 45 min to 44 min is not a signal. |

**Build-Measure-Learn Trigger (PRD-5.2):** If kill criteria are met, the team pivots scope (narrow persona paths or restructure information architecture) before proceeding to P4–P10. Pivot path: re-enter Stage D; file `stage-d-evidence.md` v2; jury deliberation before new build.

**Pivot Criteria (PRD-6.3):** The experiment is killed and scope is pivoted if: (a) kill-if criteria are met per table above; or (b) Stage B interviews reveal the problem as stated in §1 is not validated — in this case the team returns to Stage B and re-files `stage-b-evidence.md` with updated problem framing before proceeding.

---

## 3. Full Solution Vision (Stage D — Aspirational, Pending MVP Validation)

Build a **10-page self-contained HTML adoption guide** that serves as the authoritative, navigable front-door to the Hangar AI Constitution for technical coaches and senior architects onboarding new teams.

### Personas (PRD-3.1 — Minimum 5 Interviews Required Before Stage C)

Three human personas are defined. All three require evidence-based validation (5+ interviews per persona per PRD-3.1) before information architecture is confirmed in Stage C.

| Persona | Primary Need | Entry Point |
|---------|-------------|-------------|
| **Technical Coach** | Facilitate team onboarding; present a single URL; apply Socratic guidance (AGENT.md §1.2–1.3) to lead engineers to discovery; use Discovery and Planning operating modes (AGENT.md §4.1, §4.2) as primary onboarding modes | P1 → P3 (Coach path) → P7, P8 |
| **Senior Architect** | Evaluate architectural alignment; understand law precedence; map DDD patterns to constitution | P1 → P3 (Architect path) → P2, P4, P10 |
| **Engineer** | Implement constitutionally; quick start on TDD gates, skill triggers, SDD workflow | P1 → P3 (Engineer path) → P5, P7, P8, P9 |

> **AI Agent is NOT a learning persona.** An AI agent is an operating mode defined in AGENT.md §4 — it is a system component in the RAG model, not a human adopter navigating a guide. (Round 1 finding: Maya Chen OBJECT-3.)
>
> **New Project is NOT a persona.** It is a context or trigger, not a person with goals and jobs-to-be-done. (Round 1 finding: Maya Chen OBJECT-4.)

### ENG-13.1 Architecture Decision

All pages are self-contained HTML with no external stylesheet or script dependencies. Shared navigation, design tokens, and the AA gradient bar are inlined per `aa-artifact-render` production. No shared CSS files. This is a constitutional requirement, not an implementation preference.

### ENG-13.2 Requirement — Citation Transparency on All Pages

Every law citation across all 10 pages SHALL use the `<span class="law-cite">` tooltip pattern, sourcing law title, NN status, and summary from `laws/index.yaml` YAML frontmatter. The `aa-artifact-render` tool handles this automatically when invoked with the `--laws-dir` flag.

### JavaScript Test Infrastructure (ENG-4.1 ⛔, Jordan OBJECT-16)

Pages P4 (search JS) and P6 (wizard JS) contain inline JavaScript that must be tested per ENG-4.1 ⛔ Atomic TDD before ship.

- **Test framework:** [Vitest](https://vitest.dev/) — chosen for zero-config setup, ES module support, and compatibility with inline-script extraction from HTML files
- **Runner invocation:** `npx vitest run` — runs once; exits with non-zero code on failure; suitable for CI
- **Test-to-inline-HTML pipeline:** Test files live alongside source (`p4-search.test.js`, `p6-wizard.test.js`). The build step extracts the inline `<script>` content from each HTML file into a separate module-compatible `.js` file, runs tests against that module, then re-inlines the verified script into the final HTML. The extracted `.js` files are build artifacts — not committed to the repository.
- **Gate G4 enforcement:** CI runs `npx vitest run` before the HTML is finalized. A failing test blocks the render. Setup task: added to Phase 3 in tasks.md (T3.3).

### Generation Pipeline (ENG-11.3 — Spec Freshness)

| Component | Source | Max Staleness | Trigger |
|-----------|--------|--------------|---------|
| P4 Laws Reference | `laws/index.yaml` + all `laws/*/*.md` frontmatter | 30 days or on any law registry change | GitHub Actions on push to `laws/` |
| P5 Skills Catalog | `agent-skills/*/index.yaml` + `AVATAR-RAG-INDEX.yaml` | 30 days or on skill index change | GitHub Actions on push to `agent-skills/` |
| P2 AI Model Viz | `laws/index.yaml`, `AGENT.md`, all skill `index.yaml`, `AVATAR-RAG-INDEX.yaml` | 30 days or on any RAG source change | GitHub Actions on push to any source |
| P6 Avatar Wizard | `AVATAR-RAG-INDEX.yaml` + `avatars/` | 30 days or on avatar index change | GitHub Actions on push to `avatars/` |
| P1, P3, P7–P10 | Manual source — law IDs verified against registry | 30 days or on registry version bump | Manual with freshness check gate |

CI/CD enforcement: A GitHub Actions workflow validates source freshness on every PR. PRs that would advance a page beyond its staleness threshold are blocked until re-generated.

**CI/CD Freshness Workflow Specification (ENG-11.3, Jordan OBJECT-15):**

- **Workflow filename:** `.github/workflows/freshness-check.yml`
- **Trigger:** Every PR and every push to `main`
- **Staleness detection mechanism:** Each generated page (P2, P4, P5, P6) embeds a `data-source-commit` HTML attribute containing the git SHA of the source file at generation time. The workflow reads this attribute and compares it to the current HEAD SHA of the source. **The check fails if the source SHA has changed since last render OR if the page's embedded timestamp is > 30 days old** — these are independent failure conditions (OR-logic). A source change invalidates the page immediately, regardless of age; and a page not regenerated within 30 days is stale regardless of whether the source changed. This ensures ENG-11.3 compliance: no stale auto-generated page can merge even within the first 30 days after a source update.
- **PR-blocking spec:** The workflow exits with a non-zero status code on staleness failure. The repository's branch protection rule on `main` includes `freshness-check` as a required status check — PRs cannot be merged with a failing freshness check.
- **Manual page coverage (P1, P3, P7–P10):** These pages have no auto-generated source. The workflow checks whether `laws/index.yaml` version has bumped since the page was last rendered (by reading a `data-registry-version` attribute). If the registry version changed, the workflow posts a PR comment flagging the page for manual review and fails the check until a re-render is committed.
- **CI/CD setup task:** Added to Phase 3 in tasks.md (T3.0 — before SonarQube provisioning).

### Learning Arc (ENG-1.2 — Teaching Loop, AGENT.md §1.4)

The full guide follows the constitutional Teaching Feedback Loop as defined in AGENT.md §1.4. The six canonical stages are applied to the guide's page sequence:

| Stage (AGENT.md §1.4) | Pages | Teaching Loop Application |
|----------------------|-------|--------------------------|
| **Observe** — Identify what the adopter is trying to accomplish | P1 | Adopter sees the full system at a glance; coach identifies adopter's entry goal |
| **Guide** — Ask questions to lead to discovery | P3 | Adopter selects their persona path; Socratic coaching questions (per §1.3) replace prescriptive instructions |
| **Explain** — Provide constitutional context and rationale | P2, P4, P5 | RAG model authority hierarchy, 168 laws with rationale, skills and their law bindings explained |
| **Demonstrate** — Show good vs. bad examples | P6, P7 | Avatar wizard shows correct vs. incorrect selection; SDD workflow annotates compliant vs. non-compliant folder structures |
| **Verify** — Confirm understanding before proceeding | P8, P9 | Adopter self-certifies compliance checklist; HARD_BLOCK conditions require adopter to articulate the correct response |
| **Reinforce** — Connect to broader principles for lasting learning | P10 | Amendment process connects current law to constitutional evolution; adopter sees how their daily work feeds the governance system |

> **Note on crosswalk:** This application maps the Teaching Loop to a documentation guide context. The canonical loop is designed for agent–engineer pair interactions (AGENT.md §1.4). Pages P3, P8, and P10 are the most direct equivalents — the coach actively applies Guide, Verify, and Reinforce steps in facilitated walkthroughs.

**Socratic Design Requirement:** Every page SHALL include a "Questions to Explore" block with 3–5 open-ended coaching prompts. These prompts SHALL have no predefined answers within the page — they are discussion starters for a Technical Coach to use with their team.

### Deliverables — 10-Page Guide

| Page | Title | Purpose | Teaching Loop Stage | Primary Laws | Per-Page Learning Outcome |
|------|-------|---------|---------------------|-------------|--------------------------|
| P1 | Landing Page | Navigation hub, constitution overview, 3-persona entry points | Observe | ENG-13.1 ⛔, PRD-1.1, ENG-13.2 | Adopter identifies their persona and navigates to their entry point |
| P2 | Constitutional AI Model Viz | RAG model, authority hierarchy, skill system, feedback loop *(BUILT)* | Explain | ENG-13.1 ⛔, ENG-13.2 | Adopter describes all 5 RAG components and their authority relationships |
| P3 | Quick Start Guide | Persona-based entry: Technical Coach / Senior Architect / Engineer | Guide | ENG-1.2, ENG-11.1 ⛔, ENG-13.2 | Adopter identifies the first constitutional principle relevant to their context and can explain WHY it applies (not just WHAT it says) |
| P4 | Laws Reference | Searchable 168 laws, 3 domains, NN flags, article structure | Explain | ENG-10.1 ⛔, ENG-4.1 ⛔ (search JS), ENG-13.2 | Adopter locates any law by ID, title, or keyword and interprets NN status |
| P5 | Skills Catalog | 29+ skills, trigger phrases, law bindings, operating modes | Explain | ENG-11.1 ⛔, ENG-13.2 | Adopter identifies 3+ skills relevant to their project context and finds their triggers |
| P6 | Avatar Selection Wizard | Interactive: tech stack → laws + skills | Demonstrate | ENG-4.1 ⛔ (wizard JS), ENG-13.2 | Adopter selects appropriate avatar and justifies selection against RAG model |
| P7 | SDD Workflow Guide | PROPOSE→IMPLEMENT→ARCHIVE folder contract, ENG-11.2 checklist | Demonstrate | ENG-11.1 ⛔, ENG-11.2, ENG-13.2 | Adopter scaffolds a compliant PROPOSE artifact with zero external help |
| P8 | Compliance Checklist | Phase gates, SonarQube protocol, ENG-12.1 feedback loop | Verify | ENG-12.1 ⛔, ENG-12.2, ENG-12.3, ENG-13.2 | Adopter completes a full phase gate without facilitator prompting |
| P9 | Agentic Feedback Loop Guide | Human-in-the-loop contract, HARD_BLOCK conditions, gate diagrams | Verify | ENG-12.1 ⛔, ENG-13.2 | Adopter recognizes a HARD_BLOCK condition and executes the correct response |
| P10 | Amendment Process | ENG-10.x governance, law precedence, NN amendment path | Reinforce | ENG-10.1 ⛔, ENG-10.2, ENG-10.3, ENG-10.4, ENG-10.5, ENG-13.2 | Adopter describes the amendment process and which laws require executive approval |

---

## 4. Success Criteria (PRD-1.3 — Outcome-Driven)

### Process Gates — All Required Before Phase Advances

| Gate | Requirement | Law Authority |
|------|-------------|--------------|
| **G1** | `PROPOSAL.md` and `tasks.md` rendered as HTML+PDF via `aa-artifact-render` before any jury deliberation | ENG-13.1 ⛔, ENG-13.3 |
| **G2** | SonarQube provisioned, `.sonar-token` in `.gitignore`, dashboard open before Phase 1 IMPLEMENT begins | ENG-12.1 ⛔ |
| **G3** | `stage-b-evidence.md` filed and jury-validated at Moderate evidence before Stage C begins | PRD-2.5 ⛔, PRD-1.5 ⛔ |
| **G4** | Atomic TDD cycles confirmed for all JavaScript in P4 (search) and P6 (wizard) before ship | ENG-4.1 ⛔ |
| **G5** | Threat model filed in `compliance/threat-model.md` before Stage C | ENG-6.1 ⛔ |
| **G6** | Data classification table filed in `compliance/data-classification.md` before Stage C | BUS-3.1 ⛔, ENG-6.4 ⛔ |
| **G7** | Risk assessment filed in `compliance/risk-register.md` before Stage C | BUS-6.1 ⛔ |
| **G8** | WCAG 2.1 AA accessibility audit + ADA / Section 508 / 14 CFR Part 382 determination obtained before final release | BUS-1.1 ⛔, BUS-2.3 ⛔ |
| **G9** | Privacy Impact Assessment (PIA) completed and filed before any analytics feature ships | BUS-4.5, BUS-4.3 ⛔ |
| **G10** | SonarQube gate PASS + `hangar-ai-specs/evidence/sonarqube-delta.md` filed before archive | ENG-12.1 ⛔ |
| **G11** | `sonarqube-delta.md` filed at end of every session in `hangar-ai-specs/evidence/` | ENG-12.1 ⛔ |

### Evidence Strength Rubric (PRD-1.5 ⛔, PRD-2.5 ⛔)

The following rubric governs evidence classification at each stage gate. The G3 gate (Stage B exit) requires Moderate or Strong before Stage C begins. This rubric is non-negotiable — a juror may challenge any classification that does not meet the criteria.

| Classification | Criteria | Example |
|---------------|---------|---------|
| **Weak** | Repository / structural inspection only; no direct contact with real adopters; no interview on file; or: fewer than 3 interviews conducted; or: interviews conducted but findings not corroborated across participants | Stage A: README gap analysis (current stage) |
| **Moderate** | 3–5 structured interviews conducted with real adopters from the target persona group; findings documented and internally consistent across ≥ 3 participants; OR a compelling quantitative proxy corroborating the qualitative gap (e.g., ≥ 20 support tickets with identical pattern); jury-validated by Priya Kapoor at Stage B gate | Stage B target: 3+ Technical Coach interviews with consistent "no single URL" finding |
| **Strong** | 5+ structured interviews per persona; consistent themes confirmed across multiple data sources (qualitative + quantitative); no material contradictions across interview participants; quantitative evidence directionally agrees with qualitative findings | Stage C target: 5+ interviews per persona + ticket/log proxy + consistent JTBD framing |

> Evidence classification decisions are made by Priya Kapoor (Product Owner) and ratified by the full jury at each stage gate. The agent cannot self-classify above Weak without at least one real adopter interview on file.

### SonarQube Delta Schema (ENG-12.1 ⛔, Gates G10/G11)

The `hangar-ai-specs/evidence/sonarqube-delta.md` file MUST conform to the following schema at every session-end filing. The schema is defined in `compliance/sonarqube-delta-schema.md`. Required fields:

| Field | Type | Description |
|-------|------|-------------|
| `scan-id` | UUID | Unique identifier for the SonarQube scan run |
| `timestamp` | ISO 8601 | Date and time of scan execution |
| `gate-result` | `PASS` or `FAIL` | SonarQube quality gate result |
| `delta-summary` | Dict | Changed metrics vs. previous scan (coverage %, new issues, resolved issues, code smells added/removed) |
| `human-reviewer` | String | Name of the person who opened the SonarQube dashboard and reviewed results |
| `sign-off` | Boolean + ISO 8601 timestamp | Human reviewer confirmation that results were reviewed before proceeding |
| `session-context` | String | Which phase/task was in progress at time of scan |

Filing a `sonarqube-delta.md` with missing required fields is equivalent to not filing it — Gate G11 is not satisfied until all fields are present.

### Outcome Metrics

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| First-successful-task time — adopter independently scaffolds a constitutionally valid task without facilitator prompt | < 60 min from landing page *(SD-OBL-4: `< 20 min` → `< 60 min` per Stage B)* | 3+ facilitator-observed walkthroughs; stopwatch start = landing page load, stop = adopter declares task complete |
| Per-page learning outcome met (adopter articulates outcome statement unprompted) | ≥ 8 of 10 pages pass | Post-walkthrough verbal assessment by Technical Coach juror |
| ENG-13.1 compliance — all 10 pages self-contained HTML (no external dependencies) | 10 / 10 | Alexandra Pierce code review before release |
| Law citation accuracy — zero invented laws across all 10 pages | 100% | Verified against `laws/index.yaml` v2.0.0 by Alexandra Pierce |
| ENG-13.2 tooltip coverage — all citations have inline tooltips with correct law metadata | 100% | Automated count: span.law-cite count ≥ citation ID count in source |
| All 168 laws present in P4 Laws Reference | 100% | Code-generated diff against `laws/index.yaml`; zero manual entries |
| Adopter retention signal — adopter returns to guide for reference ≥ 2 times within 2 weeks of MVP walkthrough | ≥ 2 of 3 MVP participants | Self-reported follow-up at Week 2 (no tracking pixels or analytics in MVP) |
| Jury unanimous approval | Required — ALL 6 jurors | See §6 |

---

## 5. ENG-10.1 Compliance Instrumentation (Constitution Metrics Collection)

The adoption guide is a governed system artifact. Metrics collection instrumented per ENG-10.1 ⛔ requirements:

1. **Compliance rate per law / team / project** — tracked via structured walkthrough observation forms (not behavioral analytics, avoiding PIA dependency in MVP)
2. **Naming conventions** — all metric event names SHALL use the `aa.adoption_guide.<page>.<event>` pattern, consistent with org-wide telemetry conventions
3. **Real-time collection** — metrics collected at the time of enforcement (walkthrough observation), not batched retroactively
4. **PII exclusion** — no PII in metric dimensions; session IDs are ephemeral and non-identifiable
5. **Production analytics** (LATER horizon only) — gated behind BUS-4.5 PIA; page-level events (load, navigation) classified as Internal per BUS-3.1; full analytics spec requires BUS-4.5 PIA before instrumentation

---

## 6. Jury — Deliberation Panel

All tasks require **UNANIMOUS approval** across all 6 jury members before progressing.
**Alexandra Pierce holds BLOCKING VETO authority** on any non-negotiable law violation.

| # | Juror | Role | Constitution Focus | Veto |
|---|-------|------|--------------------|------|
| 1 | **Tomás Reyes** | Senior Architect | ENG-2.x: DDD, layered architecture, vertical slice integrity | — |
| 2 | **Maya Chen** | Technical Coach | ENG-1.2: Teaching-first, skill alignment, pedagogical clarity | — |
| 3 | **Jordan Ellis** | Staff Engineer / DevX | Developer experience, quick-start usability, adoption friction | — |
| 4 | **Priya Kapoor** | Product Owner | PRD-1.2 ⛔, PRD-1.5 ⛔, PRD-1.3: Outcome-Driven | — |
| 5 | **Carlos Mendez** | Compliance Officer | BUS-1.1 ⛔, BUS-7.1 ⛔, aviation regulations, data governance | — |
| 6 | **Alexandra Pierce** | Constitutional Lawyer *(Sub-Agent)* | ALL domains — NON-NEGOTIABLE watchdog. Active session monitor. | **⛔ VETO** |

### Deliberation Protocol

1. Agent presents completed deliverable to jury; artifacts pre-rendered per ENG-13.1 ⛔ and ENG-13.3 before jury sees them
2. Each juror reviews cold against their constitutional domain — no prior context, no checklists pre-loaded
3. Alexandra Pierce monitors ALL tasks continuously for NN violations; active at all times
4. **APPROVE** — Deliverable meets all relevant laws → unanimous across all 6 → proceed
5. **OBJECT** — Fixable deficiency found → agent remediates → re-deliberates
6. **BLOCK (Alexandra Pierce only)** — NON-NEGOTIABLE violation detected → agent MUST stop, cite violated law, remediate fully, re-present to full jury
7. Minimum 2 deliberation rounds required — unanimous first-round APPROVE is constitutionally invalid
8. Deliberation log maintained per BUS-7.1 ⛔

### Deliberation Log Specification (BUS-7.1 ⛔)

Each log entry MUST capture all 6 required fields:

| Field | Content |
|-------|---------|
| **Who** | Juror name and role |
| **What** | Verdict (APPROVE / OBJECT / BLOCK) and action taken |
| **When** | ISO 8601 timestamp |
| **Where** | Proposal ID + stage/task identifier |
| **Why** | Law citation(s) and reasoning |
| **Outcome** | Net result (proceed / remediating / blocked) |

**Immutability mechanism (BUS-7.1 ⛔ — corrected):** Git branch protection policy MUST be configured with:
- Force-push disabled on `main` / `trunk`
- Branch deletion disabled on protected branches
- Signed commits required or SHA-256 commit signing enforced via CI
- No self-merge (require 1+ reviewer per PR)
- 7-year archival SLA: deliberation records in `hangar-ai-specs/archive/` are append-only under branch protection

**Evidence integrity (BUS-7.2):** A SHA-256 hash manifest (`compliance/evidence-manifest.sha256`) SHALL be maintained for all stage evidence files. Updated at each stage gate transition.

---

## 7. Discovery Stage-Gate Status (PRD-2.5 ⛔)

| Stage | Name | Status | Exit Artifact |
|-------|------|--------|--------------|
| A | Problem Framing | ✅ COMPLETE | `stage-a-evidence.md` + `stage-a-evidence.html` filed |
| B | Assumption Mapping | 🔴 BLOCKED — stage-b-evidence.md does not yet exist | `stage-b-evidence.md` (required) |
| C | Jobs-To-Be-Done | ⏳ PENDING Stage B exit | `stage-c-evidence.md` |
| D | Solution Exploration | ⏳ PENDING Stage C exit | `stage-d-evidence.md` |
| E | Prototype / Validation | ⏳ PENDING Stage D exit | `stage-e-evidence.md` |
| F | Go/No-Go Decision | ⏳ PENDING all prior stages | `stage-f-evidence.md` |

> Stage B deliberation CANNOT begin before `stage-b-evidence.md` is filed. The sequencing gate is a hard constitutional requirement per PRD-2.5 ⛔ — jury deliberation on a stage is not a substitute for the evidence artifact.

---

## 8. Roadmap (PRD-4.1 / PRD-4.2 — Outcome-Based, Now / Next / Later)

**NOW — MVP Validation**
*Problem hypothesis: fragmented entry points cause measurable adoption friction*
- Outcome: ≥ 2 of 3 coached adopters complete first-successful-task in < 60 minutes unprompted AND ≥ 2 of 3 pass the guardrail metric (no NN law misconceptions) — see §2 Minimum Validation Threshold for full dual-condition gate *(SD-OBL-4: updated from `< 20 min` per Stage B evidence)*
- Retention signal: ≥ 2 of 3 MVP participants return to guide for reference within 2 weeks
- Work: Stage B (assumption mapping + interviews) → Stage C (JTBD) → Stage D (IA design) → P1 + P3 (Tech Coach + Architect paths) built
- Compliance gates: G2, G3, G4, G5, G6, G7 must all pass before P1/P3 IMPLEMENT begins

**NEXT — Full Guide**
*Condition: MVP validation threshold met (adoption friction confirmed, retention signal positive)*
- Outcome: Technical Coach can deliver a complete team onboarding session using the guide as the sole resource, without any manual document lookups
- Work: P4 (Laws Reference), P5 (Skills Catalog), P6 (Avatar Wizard), P7 (SDD Workflow), P8 (Compliance Checklist), P9 (Agentic Feedback Loop), P10 (Amendment Process)
- Engineer persona quick start path added to P3
- Gate: MVP retention signal met; SonarQube gate PASS; G8 (accessibility) must pass before NEXT release

**LATER — Continuous Evolution**
*Condition: Full guide in production; at least one full adoption cycle observed*
- Outcome: Guide stays current with constitution amendments without manual intervention; zero adopter-observed staleness incidents per quarter
- Work: CI-driven source freshness (ENG-11.3 auto-regeneration triggers); amendment process auto-update
- Analytics: page-level behavioral telemetry — ONLY after BUS-4.5 PIA is completed and filed; NOT before

---

## 9. Regulatory Scope Declaration (BUS-2.x)

This declaration is required before Stage C per BUS-2.1 ⛔, BUS-2.2 ⛔, BUS-2.3 ⛔.

| Law | Scope Decision | Rationale |
|-----|---------------|-----------|
| **BUS-2.1 ⛔** FAA Compliance Law (FAR Part 25, FAR Part 117, DO-178C) | **OUT OF SCOPE** for guide content itself. The guide documents the Hangar AI Constitution governance system — it does not control avionics software or crew scheduling software directly. Projects using the guide that produce avionics-adjacent software remain bound by FAR Part 117 / DO-178C through their own SDD proposals. | The adoption guide is a documentation artifact, not a flight-critical or crew-scheduling software system. |
| **BUS-2.2 ⛔** Control Framework Law | **IN SCOPE** — Controls governing the adoption guide's own change process (jury approval, branch protection, evidence filing) are documented and mapped in `compliance/raci.md` and `compliance/risk-register.md`. | Every artifact produced under the constitution is subject to the control framework. |
| **BUS-2.3 ⛔** DOT Consumer Protection Law (refund obligations, accessibility, denied boarding) | **ACCESSIBILITY IN SCOPE** — 14 CFR Part 382 (nondiscrimination for air travelers with disabilities) applies to American Airlines customer-facing digital products. The adoption guide is an internal-only artifact; however, accessibility compliance (WCAG 2.1 AA) is required per BUS-1.1 ⛔ Priority Hierarchy (Legal first). Gate G8 mandates an ADA / Section 508 / Part 382 determination before final release. Other DOT consumer protection provisions (refunds, fare transparency, denied boarding) are out of scope for a governance guide. | Internal artifact; fare/refund/boarding provisions inapplicable. Accessibility provision applies to all digital surfaces at AA per legal guidance. |
| **BUS-2.4** Evidence Collection Law | **IN SCOPE** — Compliance evidence for this proposal (stage evidence files, deliberation log, SonarQube delta) is retained in `hangar-ai-specs/` per ENG-11.1 ⛔ and archived per BUS-7.1 ⛔. | Standard evidence retention applies. |

Full regulatory scope document: `compliance/regulatory-scope.md` (to be filed before Stage C, per G5/G6/G7)

---

## 10. Data Classification Plan (BUS-3.1 ⛔)

All data assets produced or processed by this project are classified below per BUS-3.1 ⛔.

| Data Asset | Classification | Rationale | Retention |
|-----------|---------------|-----------|----------|
| PROPOSAL.md, tasks.md, PROGRESS.md | Internal | Internal governance documents; no PII; not for external publication | Minimum 3 years post-archive per BUS-2.4; deleted no earlier than 3 years after `hangar-ai-specs/archive/` move |
| Stage evidence files (stage-a through stage-f) | Internal | Interview notes may include attributed quotes (de-identified before filing) | Minimum 3 years post-archive per BUS-2.4 |
| Jury deliberation log (SQL session DB) | Internal | Contains juror names (personas) and verdict reasoning; no real PII | Online: SDD lifecycle + 1 year; Archived: 7 years per BUS-7.1 ⛔ minimum, append-only in `hangar-ai-specs/archive/` under branch protection |
| SonarQube delta evidence | Internal | Code quality metrics; no PII | 7 years per BUS-7.1 ⛔ evidence policy (governs all compliance evidence for this project) |
| walkthrough observation forms (MVP measurement) | Internal | De-identified; no names recorded; adopter is identified only by role | 90 days post-MVP validation |
| Production analytics events (LATER horizon) | **Internal / Confidential** (TBD — requires PIA) | Behavioral page events; potential PII if user is logged in | TBD pending PIA |
| Compliance artifacts (threat model, risk register, RACI) | Confidential | Contains organizational risk posture information | Minimum 3 years post-archive per BUS-2.4; threat model and risk register: 7 years per BUS-7.3 audit readiness |

Full data inventory: `compliance/data-classification.md` (to be filed before Stage C per Gate G6)

---

## 11. Compliance Ownership & RACI (BUS-1.3)

Every compliance obligation under this proposal has a named accountable owner per BUS-1.3.

| Obligation | Accountable Owner | Responsible | Consulted | Informed |
|-----------|-------------------|-------------|-----------|---------|
| Constitutional compliance (all NN laws) | Alexandra Pierce (sub-agent) | Agent | All 6 jurors | Constitution maintainer |
| Privacy / data subject rights (BUS-4.3 ⛔, BUS-4.5) | Carlos Mendez (Compliance Officer) | Agent | Alexandra Pierce | DPO |
| Accessibility gate (BUS-2.3 ⛔, G8) | Carlos Mendez | Agent | BUS-1.1 authority | AA Legal |
| Audit trail integrity (BUS-7.1 ⛔) | Carlos Mendez | Agent | Alexandra Pierce | Repo admin |
| MVP outcome measurement (PRD-5.1 ⛔, PRD-6.2 ⛔) | Priya Kapoor | Agent | Jordan Ellis | Tech Coach stakeholders |
| Evidence evidence quality (PRD-1.5 ⛔) | Priya Kapoor | Agent | Maya Chen | Constitution maintainer |
| Pedagogical quality (ENG-1.2) | Maya Chen | Agent | Priya Kapoor | Tech Coach community |
| Architecture compliance (ENG-4.1 ⛔, ENG-6.1 ⛔) | Tomás Reyes | Agent | Alexandra Pierce | Platform team |
| SonarQube gate (ENG-12.1 ⛔) | Jordan Ellis | Agent | Tomás Reyes | CI/CD owner |

Full RACI matrix: `compliance/raci.md` (to be filed before Stage C per Gate G7)

---

## 12. Risk Assessment Reference (BUS-6.1 ⛔)

Project-specific risks identified at PROPOSE stage. Full assessment in `compliance/risk-register.md`.

| Risk | Likelihood | Impact | Control |
|------|-----------|--------|---------|
| Weak evidence prevents Stage C advancement; MVP scope under-validated | HIGH | HIGH | Stage B gate (G3) is hard-blocking; minimum 3 interviews before Stage C |
| P4 search JS or P6 wizard JS contains untested code paths | MEDIUM | HIGH | ENG-4.1 ⛔ TDD gate (G4); mutation testing before ship |
| analytics feature shipped without PIA | MEDIUM | CRITICAL | G9 hard-blocks analytics; all analytics in LATER horizon only |
| Law registry staleness causes incorrect citations in guide | MEDIUM | HIGH | ENG-11.3 generation pipeline; CI freshness check on every PR |
| Jury deliberation log tampered or lost | LOW | HIGH | BUS-7.2 SHA-256 manifest + branch protection policy (BUS-7.1 ⛔) |
| Accessibility defect discovered post-release | LOW | HIGH | G8 mandatory before final release; not in LATER |
| Constitution amendment during IMPLEMENT causes guide staleness | MEDIUM | MEDIUM | ENG-11.3 freshness trigger; 30-day max staleness window |
| Registry integrity anomaly (BUS-2.2 / BUS-3.1 / BUS-6.1 comment mismatch + ENG-10.1 / ENG-11.1 comment mismatch in laws/index.yaml; BUS-3.6 absent from law_ids.business; ENG-12.x series absent from law_ids.engineering) | CONFIRMED | MEDIUM | Escalated to constitution maintainer; tracked in risk register (R-08, 7 anomalies total) |

Full risk register: `compliance/risk-register.md` (to be filed before Stage C per Gate G7)

---

## 13. Law Citations (ENG-11.2 — Required)

All citations verified against `laws/index.yaml` v2.0.0. Zero fabricated titles. 74 laws cited.

### Engineering Constitution

| Law ID | Title | Class | Role in This Proposal |
|--------|-------|-------|-----------------------|
| `ENG-1.2` | AI-Engineer Pairing Law | Standard | Guide embodies teaching-first — every page coaches, not just informs; learning arc required |
| `ENG-1.4` | Incremental Improvement Law | Standard | The NOW/NEXT/LATER phased delivery directly implements the foundational slice mandate: MVP slice (P1+P3) must be independently validated before NEXT slice (P4–P7) begins; each slice delivers complete adopter value without requiring subsequent slices |
| `ENG-2.1` | Domain-Driven Design Law | Standard | **SCOPED OUT for P4/P6 JS components.** P4 (search/filter utility) and P6 (persona wizard) are single-concern inline utility scripts embedded in static HTML pages — each is < 200 lines, has no domain model, no aggregates, and no service layer. ENG-2.1's DDD tactical patterns (aggregates, repositories, value objects, domain events) are architecturally disproportionate to this scope. Scope-out rationale: bounded-context isolation is achieved structurally (one HTML file per page, no shared state across pages) without requiring explicit DDD artifacts. |
| `ENG-2.2` | Layered Architecture Law | Standard | **SCOPED OUT for P4/P6 JS components** (same rationale as ENG-2.1). Formal presentation/application/domain/infrastructure layer separation is disproportionate for single-concern inline scripts. The functional separation between data (law registry JSON), logic (filter/wizard functions), and rendering (DOM manipulation) provides the intent of layer separation within the inline-script constraint. |
| `ENG-2.3` | Vertical Slice Architecture Law | Standard | The phased MVP delivery (P1+P3 as a fully validated, independently shippable slice before P4–P10) is the vertical slice pattern applied to a documentation project. Each slice (MVP slice: P1+P3; NEXT slice: P4–P7; LATER: P8–P10) delivers end-to-end adopter value without requiring subsequent slices to be useful. The MVP slice is tested and jury-approved before the next slice begins — this is the constitutional vertical slice principle. (Removed in v2.0 — re-added per Tomás Reyes Round 2 OBJECT-13: deletion without scoping rationale is not permitted.) |
| `ENG-4.1` | Atomic TDD Law | ⛔ NN | P4 (search JS) and P6 (wizard JS) are software — TDD atomic cycles required; Gate G4 |
| `ENG-6.1` | Security by Design Law | ⛔ NN | Threat model required before Stage C; guide exposes amendment paths, HARD_BLOCK conditions, SonarQube gate protocol; Gate G5 |
| `ENG-6.4` | Data Protection Law | ⛔ NN | Analytics forward commitment requires data classification; all data assets classified §10; Gate G6 |
| `ENG-6.7` | Audit Trail Law | ⛔ NN | **Audit architecture for this pipeline context:** Logged operations: phase gate transitions (G1–G11), `aa-artifact-render` invocations, stage evidence file creation/update, jury deliberation entries, git commit signing events. Storage: git history (append-only under branch protection — force-push disabled, force-delete disabled per §6) + SQL session checkpoint archive (session store). Record structure per audit event: `{ timestamp: ISO 8601, operation: string, actor: juror-id or "agent" or "ci", artifact-id: changeset + filename, outcome: "PASS"/"FAIL"/"APPROVE"/"OBJECT"/"BLOCK", correlation-id: UUID linking related gate events }`. Immutability: branch protection prevents git history rewrite; SHA-256 manifest (`compliance/evidence-manifest.sha256`) verifies artifact integrity at each gate. **SIEM scope-out (explicit):** Centralized SIEM log aggregation is not warranted for this bounded internal governance documentation pipeline. Rationale: (1) no user-facing sensitive operations occur in the audit stream — all actors are enumerated (agent, CI, named juror personas); (2) no privileged authentication events are logged — access control is governed by GitHub repository permissions, not by this pipeline; (3) no regulated personal data appears in the audit stream — PII is excluded from all metric dimensions per §5 ENG-10.1; (4) no real-time threat detection requirement exists — this is not a production application; (5) git's native DAG structure (each commit SHA cryptographically incorporates its parent's SHA) provides an append-only, tamper-evident hash chain that satisfies ENG-6.7's log aggregation requirement within the bounded scope of a documentation pipeline; (6) the SHA-256 manifest adds a second independent integrity layer. This scoping decision is recorded in `compliance/risk-register.md` under the project risk register. Scope boundary: explicitly distinct from BUS-7.1's deliberation log obligation (which governs jury records specifically). |
| `ENG-10.1` | Constitution Metrics Collection Law | ⛔ NN | Adoption guide is a governed system artifact; compliance tracking instrumented per §5: naming conventions, real-time collection, no PII in dimensions |
| `ENG-10.2` | Enforcement Tracking Law | Standard | P10 Amendment Process sources enforcement tracking requirements from this law |
| `ENG-10.3` | Compliance Reporting Law | Standard | P10 Amendment Process sources compliance reporting cadence from this law |
| `ENG-10.4` | Constitution Health Dashboard Law | Standard | P10 references health dashboard requirements |
| `ENG-10.5` | Law Effectiveness Measurement Law | Standard | P10 references effectiveness measurement requirements |
| `ENG-11.1` | Hangar SDD Law | ⛔ NN | This PROPOSAL.md IS the PROPOSE stage of ENG-11.1; `hangar-ai-specs/` folder contract defined §14 |
| `ENG-11.2` | Proposal Completeness Law | Standard | This §13 satisfies the law citation requirement |
| `ENG-11.3` | Spec Freshness Law | Standard | Guide must reflect current constitution state; generation pipeline defined §3; max staleness 30 days |
| `ENG-12.1` | Agentic Feedback Loop Law | ⛔ NN | SonarQube MUST be provisioned before Phase 1 IMPLEMENT begins; dashboard reviewed at every phase transition; session-end `sonarqube-delta.md` filed; Gate G2, G10, G11 |
| `ENG-12.2` | Dashboard-First Development Law | Standard | SonarQube dashboard open throughout each session; not just at API call |
| `ENG-12.3` | External Referee Law | Standard | Agent cannot self-certify compliance; SonarQube provides objective verdict |
| `ENG-13.1` | Artifact Rendering Standard | ⛔ NN | All 10 pages and this PROPOSAL.md rendered via `aa-artifact-render` before deliberation; `tasks.md` also rendered (active BLOCK resolved) |
| `ENG-13.2` | Citation Transparency Law | Standard | All law citations across all 10 pages use `<span class="law-cite">` tooltip pattern sourced from law YAML frontmatter |
| `ENG-13.3` | PDF Reproducibility Law | Standard | Gate reviews use `aa-artifact-render --pdf`; browser-print PDFs not acceptable; Gate G1 |

### Product Constitution

| Law ID | Title | Class | Role in This Proposal |
|--------|-------|-------|-----------------------|
| `PRD-1.1` | Customer-Centric Law | Standard | P1 Landing Page anchored in adopter needs, not internal preferences |
| `PRD-1.2` | Problem-First Law | ⛔ NN | §1 validates problem before solution; solution architecture deferred to Stage D |
| `PRD-1.3` | Outcome-Driven Law | Standard | Success criteria in §4 defined as outcomes, not feature counts |
| `PRD-1.4` | Continuous Discovery Law | Standard | Discovery is never complete; Stage F Go/No-Go is not the end of learning |
| `PRD-1.5` | Evidence-Based Decision Law | ⛔ NN | Weak evidence acknowledged in §1; validation plan filed; Stage C gated on Moderate evidence |
| `PRD-2.1` | Problem Validation Law | Standard | Problem must be jury-validated before IA design in Stage D |
| `PRD-2.2` | Assumption Mapping Law | Standard | Stage B maps all adopter assumptions; filed in `stage-b-evidence.md` |
| `PRD-2.3` | Jobs-to-be-Done Law | Standard | Stage C frames adopter needs as jobs for 3 personas |
| `PRD-2.4` | Competitive Analysis Law | Standard | Stage B includes alternatives analysis (existing README, other constitution guides) |
| `PRD-2.5` | Discovery Stage-Gate Law | ⛔ NN | Stages A→F tracked in §7; Stage B hard-blocking gate (G3) |
| `PRD-3.1` | Persona Development Law | Standard | 3 human personas; evidence-based (5+ interviews each) required before Stage C |
| `PRD-3.2` | Journey Mapping Law | Standard | Journey maps required before IA design in Stage D |
| `PRD-3.3` | User Story Law | Standard | Stories with acceptance criteria required in Stage D |
| `PRD-3.4` | Experience Principles Law | Standard | Guiding experience principles defined in Stage D |
| `PRD-4.1` | Outcome-Based Roadmap Law | Standard | §8 roadmap communicates outcomes per horizon, not feature lists |
| `PRD-4.2` | Now/Next/Later Framework Law | Standard | §8 uses Now/Next/Later time horizons, not fixed dates |
| `PRD-4.3` | Dependency Management Law | Standard | Stage gate dependencies explicitly documented in §7 and tasks.md |
| `PRD-4.4` | Roadmap Communication Law | Standard | §8 roadmap is appropriate for technical coaches + architects audience |
| `PRD-5.1` | MVP Law | ⛔ NN | §2 defines MVP: riskiest assumption, smallest experiment, validation threshold |
| `PRD-5.2` | Build-Measure-Learn Law | Standard | BML trigger defined in §2: if MVP threshold not met, pivot before P4–P10 |
| `PRD-5.3` | Experiment Design Law | Standard | Full experiment design in §2: hypothesis, experiment type (Concierge), control condition (README baseline), primary/secondary/guardrail metrics, sample, segments, ship-if, iterate-if, kill-if, minimum detectable effect |
| `PRD-6.1` | PMF Definition Law | Standard | Adoption-market fit to be measured post-MVP, not assumed |
| `PRD-6.2` | Retention Over Acquisition Law | ⛔ NN | Retention signal defined in §4: ≥ 2 of 3 MVP participants return within 2 weeks |
| `PRD-6.3` | Pivot Criteria Law | Standard | Pivot criteria defined in §2: kill-if conditions trigger Stage D re-entry; stage B contradiction triggers problem revalidation before any build proceeds |

### Business Constitution

| Law ID | Title | Class | Role in This Proposal |
|--------|-------|-------|-----------------------|
| `BUS-1.1` | Priority Hierarchy Law | ⛔ NN | Legal > Safety > Privacy > Security > Business Continuity > Efficiency honored across all deliverables; accessibility pre-release (Gate G8), not deferred |
| `BUS-1.2` | Risk-Based Approach Law | Standard | Governance decisions proportionate to risk; risk-based triage in §12 |
| `BUS-1.3` | Accountability Law | Standard | Named compliance owners defined in §11; RACI in `compliance/raci.md` |
| `BUS-1.4` | Transparency Law | Standard | Compliance gaps documented in §12 and `compliance/risk-register.md` |
| `BUS-2.1` | FAA Compliance Law | ⛔ NN | Scoped OUT for guide content; scoped IN for projects built using the guide — see §9 |
| `BUS-2.2` | Control Framework Law | ⛔ NN | Controls documented in `compliance/raci.md`; jury approval is a control; branch protection is a control |
| `BUS-2.3` | DOT Consumer Protection Law | ⛔ NN | Accessibility (14 CFR Part 382) in scope; Gate G8 mandatory; other provisions out of scope for internal guide |
| `BUS-2.4` | Evidence Collection Law | Standard | All stage evidence retained in `hangar-ai-specs/`; SHA-256 manifest in `compliance/evidence-manifest.sha256` |
| `BUS-3.1` | Data Classification Law | ⛔ NN | All data assets classified in §10; full table in `compliance/data-classification.md` |
| `BUS-3.2` | Data Inventory Law | Standard | Data inventory in `compliance/data-classification.md` with owner, location, retention |
| `BUS-3.3` | Data Retention Law | Standard | Retention schedule with explicit calendar minimums per asset defined in §10 table; deliberation log: 7-year archive per BUS-7.1 ⛔; SDD artifacts: 3-year minimum per BUS-2.4 |
| `BUS-3.6` | Monetary Precision Law | ⛔ NN | **SCOPED OUT — NOT APPLICABLE.** The adoption guide is a 10-page static HTML governance documentation artifact. It contains no monetary computations, no loyalty-currency values (AAdvantage miles, EQDs, points), no fare arithmetic, no revenue figures, and no financial or loyalty quantities of any kind across P1–P10. BUS-3.6's decimal precision and rounding requirements do not apply. Explicitly scoped out per compliance record requirements. |
| `BUS-4.1` | Privacy by Design Law | Standard | Analytics uses Privacy by Design 7 principles if/when shipped (LATER horizon) |
| `BUS-4.2` | Consent Management Law | Standard | Analytics consent mechanism required before production analytics ship |
| `BUS-4.3` | Data Subject Rights Law | ⛔ NN | Behavioral analytics data (LATER) subject to access, rectification, erasure, portability rights; Gate G9 |
| `BUS-4.4` | Privacy Notice Law | Standard | Notice required before any analytics feature ships |
| `BUS-4.5` | Privacy Impact Assessment Law | Standard | PIA required before analytics ships; Gate G9; LATER horizon only |
| `BUS-6.1` | Risk Assessment Law | ⛔ NN | Project-specific risk assessment in §12; full register in `compliance/risk-register.md`; Gate G7 |
| `BUS-6.2` | Risk Register Law | Standard | Risk register maintained in `compliance/risk-register.md` |
| `BUS-7.1` | Audit Trail Law | ⛔ NN | Deliberation log maintained per §6; branch protection policy required for immutability claim |
| `BUS-7.2` | Evidence Integrity Law | Standard | SHA-256 hash manifest in `compliance/evidence-manifest.sha256` |
| `BUS-7.3` | Audit Readiness Law | Standard | Documentation current; archive policy per ENG-11.1 ⛔ |
| `BUS-7.4` | Internal Audit Law | Standard | Post-release audit scheduled; findings tracked in `PROGRESS.md` |
| `BUS-9.1` | Incident Classification Law | Standard | Incidents classified P1–P4 per response plan in `compliance/incident-response.md` |
| `BUS-9.2` | Incident Response Law | Standard | Defined response process in `compliance/incident-response.md` |
| `BUS-9.3` | Breach Notification Law | ⛔ NN | 72-hour GDPR reporting window documented; DPO contact chain in `compliance/incident-response.md` |
| `BUS-9.4` | Post-Incident Review Law | Standard | Post-mortems required for all significant incidents; findings feed risk register |

---

## 14. SDD Folder Contract (ENG-11.1)

```
hangar-ai-specs/changes/build-adoption-guide-2026-001/
├── PROPOSAL.md                   ← This document (PROPOSE stage artifact)
├── PROPOSAL.html                 ← Rendered per ENG-13.1 ⛔ (aa-artifact-render)
├── PROPOSAL.pdf                  ← Rendered per ENG-13.3 (aa-artifact-render --pdf)
├── tasks.md                      ← Atomic task breakdown with checkboxes
├── tasks.html                    ← Rendered per ENG-13.1 ⛔
├── tasks.pdf                     ← Rendered per ENG-13.3
├── PROGRESS.md                   ← Phase tracking and gate evidence
├── stage-a-evidence.md           ← ✅ Stage A exit artifact (PRD-2.5 ⛔)
├── stage-a-evidence.html         ← ✅ Rendered
├── stage-b-evidence.md           ← 🔴 NOT YET FILED — Stage B gate blocks Stage C
└── compliance/                   ← BUS-1.3, BUS-2.x, BUS-3.1, BUS-6.1, ENG-6.1 artifacts
    ├── regulatory-scope.md       ← BUS-2.x declaration (Gate G5 dependency)
    ├── data-classification.md    ← BUS-3.1 ⛔ classification table (Gate G6)
    ├── threat-model.md           ← ENG-6.1 ⛔ threat model (Gate G5)
    ├── risk-register.md          ← BUS-6.1 ⛔ risk register (Gate G7)
    ├── raci.md                   ← BUS-1.3 accountability matrix
    ├── incident-response.md      ← BUS-9.3 ⛔ incident response + DPO contact chain
    └── evidence-manifest.sha256  ← BUS-7.2 SHA-256 hash manifest

hangar-ai-specs/evidence/
└── sonarqube-delta.md            ← ENG-12.1 ⛔ session-end gate evidence (Gate G10, G11)
```

Upon completion: move to `hangar-ai-specs/archive/YYYY-MM-DD-build-adoption-guide-2026-001/`

---

*Proposal v2.5 — APPROVED 2026-05-02 — unanimous 6/6 jury clearance across 7 rounds*
*74 law citations — all verified against `laws/index.yaml` v2.0.0 — zero fabricated titles*
*Cleared per ENG-11.1 ⛔ / ENG-11.2 · Alexandra Pierce constitutional sign-off recorded · ADVANCE TO IMPLEMENT*

# Constitutional Cross-Reference Audit Report

**Subject files audited:**
- `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md` (1,862 lines) — the main skill
- `agent-skills/skills-by-domain/development-practices/02-adoption-setup.md` (539 lines) — the supplement

**Corpus read in full:** Laws (index + all 24 domain files), all 5 skill indexes, 68 skill/MD files, AGENT.md, avatars/index.yaml, all 40 docs/guides files

---

## TYPE 1 — Duplication / Already Covered

---

### F-1.1 — Inline Correction-Prompts Table

**(a)** `02-constitutional-companion.md`, lines 186–205 — 13-row table of AI correction prompts with "Symptom → What to say" columns.

**(b)** `docs/guides/adoption/ai-correction-prompts.md` — a dedicated 180+ line guide that contains every one of these prompts in expanded form, with context explanations. The companion skill even cites this file at line 204: *"Full correction guide with detailed explanations and longer prompts: `docs/guides/adoption/ai-correction-prompts.md`"* — making the table a partial extraction from a file it already links.

**(c)** Replace the 13-row table with a 3-row quick-reference for the three most critical failure modes and a callout: *"For the complete correction guide with detailed explanations, see `docs/guides/adoption/ai-correction-prompts.md`."*

**(d)** **HIGH** — removes ~18 duplicated lines; the table is actively maintained in two places.

---

### F-1.2 — Full 8-Step TDD Protocol Embedded in AGENTS.md Template

**(a)** `02-adoption-setup.md`, lines 117–128 — the mandatory 8-step TDD cycle is reproduced verbatim inside the AGENTS.md template that the supplement creates.

**(b)** `laws/engineering/testing.md` §4.1 (ENG-4.1); `docs/guides/constitution/atomic-tdd-law.md`; `docs/guides/testing/atomic-tdd-workflow.md`; the global `AGENTS.md` custom instructions block (in the repo's AGENTS.md) — all define the same cycle. The AGENTS.md template in `docs/guides/adoption/brownfield-adoption.md` also embeds it.

**(c)** The AGENTS.md template should reference the law by ID (`ENG-4.1`) and link to `docs/guides/constitution/atomic-tdd-law.md` instead of inlining all 8 steps; the steps are the authoritative content of ENG-4.1 and embedding them in a template creates a secondary authoritative copy that can drift.

**(d)** **HIGH** — removes ~12 duplicated lines from the supplement; eliminates drift risk between law text and embedded template.

---

### F-1.3 — GRASP / SOLID / DDD Tables

**(a)** `02-constitutional-companion.md`, lines 1509–1551 — three full reference tables: GRASP patterns (9 rows, lines 1513–1523), SOLID principles (5 rows, lines 1529–1535), DDD tactical concepts (7 rows, lines 1543–1551).

**(b)** `laws/engineering/architecture.md` §2.1 (ENG-2.1, DDD); `laws/engineering/quality.md` §3.4 (ENG-3.4, SRP); `docs/guides/constitution/ddd-law.md` (full DDD guide with Entity/Value Object/Aggregate/Service tables); `agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md` (DDD patterns). GRASP is not covered elsewhere in the corpus (see F-3.8).

**(c)** Replace the DDD and SOLID tables with single-line cross-references to their canonical homes; retain GRASP as the only novel content — or elevate GRASP to `laws/engineering/architecture.md` §3.4 so the companion can reference it there.

**(d)** **HIGH** — DDD/SOLID tables (25+ lines) can be replaced with 2-line callouts; GRASP table (12 lines) is unique and should either stay or be canonicalized first.

---

### F-1.4 — Seam Theory Definitions (Glossary + Feathers Seam Types)

**(a)** `02-constitutional-companion.md`, lines 551–598 — glossary table (lines 551–558), Feathers seam definition with size table (lines 561–579), mock-necessity test (lines 582–589), Sensing vs Separation seam definitions (lines 591–597).

**(b)** `docs/guides/testing/characterization-testing.md` — the dedicated characterization testing guide. It covers no-mocking (Rule #1), sociable testing, test behavior not structure (Rule #2), and step-by-step characterization. It is the canonical home for all Feathers-pattern content. `agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md` and `docs/guides/testing/atomic-tdd-workflow.md` also cover TDD and mock boundaries.

**(c)** Move the seam size table, mock-necessity test, and sensing/separation definitions to `docs/guides/testing/characterization-testing.md` (they belong there per ENG-4.10), and replace the companion's ~38-line block with: *"Seam types, sizing heuristics, and Feathers' Sensing/Separation distinction: see `docs/guides/testing/characterization-testing.md` §Seam Selection."*

**(d)** **HIGH** — ~38 lines can be replaced with a 2-line callout once the content is canonicalized in the characterization guide.

---

### F-1.5 — SonarQube Setup Dialog (3 Options + Blocking/Deferral Logic)

**(a)** `02-adoption-setup.md`, lines 449–531 — complete SonarQube first-time setup dialog: 5 options (Server / Docker / IDE / Blocked / Next Session), walkthrough steps, dual-credential handling, Option D/E deferred state logic, recording to `project-rules.md`.

**(b)** `agent-skills/skills-by-domain/platform-engineering/skill-sonarqube-compliance-gate.md` — the dedicated SonarQube skill which defines the full compliance gate workflow; `laws/engineering/agentic-feedback.md` ENG-12.1/12.2/12.3 (Agentic Feedback Loop Laws requiring SonarQube provisioning); `docs/guides/adoption/adoption-compliance-checklist.md`.

**(c)** Reduce Phase 3d in the supplement to a 5-line routing block that checks `sonarqube_status` and delegates to `skill-sonarqube-compliance-gate` for the actual setup dialog; the setup logic already lives there.

**(d)** **MED** — the supplement's Phase 3d dialog (~83 lines) can be reduced to a routing stub; however there is unique "adoption context" logic (blocked-per-iteration check-in pattern, Option E remind-next-session) not in the sonarqube skill, so it cannot be fully deleted without that skill being updated first.

---

### F-1.6 — Violation Tier Table (HARD_BLOCK / PHASE_GATE / WARNING)

**(a)** `02-constitutional-companion.md`, lines 753–760 — three-row table defining violation tiers with rules.

**(b)** `docs/guides/adoption/brownfield-adoption.md` §"CRITICAL: Required Adoption Structure" and §"Violation Tier" sections; `agent-skills/skills-by-domain/platform-engineering/skill-sonarqube-compliance-gate.md` defines these same tiers. The same classification appears in at least three corpus files.

**(c)** Replace the tier table with a one-line reference: *"Violation tiers (HARD_BLOCK / PHASE_GATE / WARNING) — see `docs/guides/adoption/brownfield-adoption.md` §Violation Tiers."*

**(d)** **MED** — 8 lines become 1 line; prevents three-way drift.

---

### F-1.7 — PROPOSAL.md Refactoring Template (Full Inline)

**(a)** `02-constitutional-companion.md`, lines 1155–1194 — full inline PROPOSAL.md template for per-refactoring proposals (ID, Status, Seam, Backlog, Problem, Proposed Design, Alternatives table, Scope and Safety Net).

**(b)** `agent-skills/skills-by-domain/discovery-research/spec-governance.md` defines the canonical PROPOSAL.md schema per ENG-11.2 (Proposal Completeness Law); `laws/engineering/spec-driven-development.md` §11.2 states required sections. The companion template adds adoption-specific fields (Seam, Backlog ID, characterization baseline) that are extensions, not covered by spec-governance.

**(c)** Move the adoption-specific PROPOSAL.md template into `agent-skills/skills-by-domain/discovery-research/spec-governance.md` as a "refactoring proposal variant" and replace the companion's inline block with a single reference; this unifies all proposal templates in one skill.

**(d)** **MED** — ~40 lines in the companion can become a 2-line reference; the template needs to be added to spec-governance first.

---

### F-1.8 — "Key Files — What Was Created and Why" Reference Section

**(a)** `02-constitutional-companion.md`, lines 1767–1812 — explanatory section covering what AGENTS.md, project-rules.md, `hangar-ai-specs/`, and change proposal directories do; how skill routing works; how the authority hierarchy works; how a change proposal lifecycle works.

**(b)** `docs/guides/adoption/how-to-adopt-constitution.md` Steps 2–4 (authority hierarchy, AGENTS.md purpose, spec structure); `agent-skills/base/AGENT.md` §2 (authority hierarchy); `docs/guides/constitution/constitution-overview.md` (full overview); `agent-skills/skills-by-domain/discovery-research/spec-governance.md` (proposal lifecycle).

**(c)** Replace this section with a quick-reference table of 4–5 files with one-line descriptions and direct links to their deep-dive guides, pointing to the corpus documents that already cover this content in full.

**(d)** **LOW** — saves ~45 lines; the section is useful for first-time users and is the only place in the skill that consolidates cross-references, so partial retention is justified.

---

### F-1.9 — "What's Next After Adoption" Section

**(a)** `02-constitutional-companion.md`, lines 1816–1862 — "What's Next" section including a 5-row table of next steps with links, a starter prompt template, and four bullet points about what the constitution gives you.

**(b)** `docs/guides/adoption/how-to-adopt-constitution.md` Step 4–5 (post-adoption workflow); `docs/guides/adoption/pragmatic-adoption.md` (full ongoing guide); `docs/guides/adoption/greenfield-mvp.md` (greenfield path). The companion already points to `docs/guides/adoption/how-to-adopt-constitution.md` Step 5 in row 5 of the table.

**(c)** Reduce to 3 lines + the starter prompt template, pointing to `docs/guides/adoption/how-to-adopt-constitution.md` for the full "what's next" walkthrough.

**(d)** **LOW** — ~45 lines; the section is helpful for users landing here after adoption but duplicates the guide.

---

## TYPE 2 — Content That Belongs Elsewhere

---

### F-2.1 — ENG-3.1 Interpretation Policy ("Design Signal, Not a Counting Rule")

**(a)** `02-constitutional-companion.md`, lines 1499–1506 (Step 5 intro block) and lines 1742–1755 (project-rules.md template block `## ENG-3.1 Interpretation Policy`). The text "ENG-3.1 limits are subservient to good object design. If a correct design produces a method longer than 50 lines… prefer the correct design and document the exception" is an authoritative interpretation of the law.

**(b)** `laws/engineering/quality.md` §3.1 (ENG-3.1, Complexity Limits) — the current law text says only "Refactor immediately: Decompose large operations…" with no acknowledgment of design-priority exceptions. This interpretation should be added to ENG-3.1 itself, with a note that line count is a trailing indicator of good design, not a target.

**(c)** Add a "Design-First Interpretation" subsection to `laws/engineering/quality.md` §3.1 containing this policy, then replace the companion's two blocks with: *"Per ENG-3.1 design-first interpretation: line counts follow good design — see `laws/engineering/quality.md` §3.1."*

**(d)** **HIGH** — the interpretation currently exists only in an adoption skill; if a team reads ENG-3.1 directly they will not see this critical nuance, and it risks being applied mechanically (which the companion explicitly warns against).

---

### F-2.2 — Seam-Wide Sociable Testing Invariant (No-Mock Boundary)

**(a)** `02-constitutional-companion.md`, lines 787–800 — the "seam-wide sociable testing invariant": no collaborator within the seam boundary is mocked; mocking only at I/O boundaries (database, HTTP, clock, random, messaging); Spring Boot note about @Service vs @RestController entry point.

**(b)** `laws/engineering/testing.md` §4.8 (ENG-4.8, Mock Boundaries Law): "Mocking SHALL only occur at I/O boundaries." This is the correct law, but the law text is one line — it gives no seam-context for what counts as a "boundary" during characterization. `docs/guides/testing/characterization-testing.md` Rule #1 covers "No Mocking" with examples but does not define the seam boundary as the unit of sociability. `agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md` is silent on seam-level mock rules.

**(c)** Add the sociable-seam invariant (seam = no-mock boundary; widen seam if mock would be needed inside it) to `laws/engineering/testing.md` §4.8 as an implementation note, then reference it from the companion in one sentence.

**(d)** **HIGH** — the sociable testing invariant is a foundational characterization-testing constraint; it should be a first-class testing law annotation, not only in the adoption skill.

---

### F-2.3 — God Class Definition and Decomposition Guidance

**(a)** `02-constitutional-companion.md`, line 557 (glossary) and lines 334–350 (Phase 3b, Gate 2 — god class detection and Target Architecture format), and lines 629 (Learning-Rich seam heuristics referencing god class).

**(b)** `laws/engineering/quality.md` §3.4 (ENG-3.4, SRP) mentions "one reason to change" but does not name the god class pattern. `laws/engineering/architecture.md` §2.1 (ENG-2.1, DDD) is silent on this. `agent-skills/skills-by-domain/development-practices/09-refactoring.md` Step 2 identifies "Large Class" as a code smell and prescribes "Extract Class" but does not name the god class pattern or provide a decomposition framework. No corpus document defines "god class" as a named pattern or provides the Target Architecture table format.

**(c)** Add "God Class (Low Cohesion + SRP violation — class with >1 responsibility cluster)" to `laws/engineering/quality.md` §3.4 with a note that decomposition uses GRASP Information Expert + Creator pattern applied leaf-first; replace the companion's glossary entry with a citation.

**(d)** **HIGH** — the concept is important enough to be a named violation in the quality laws; it currently has no canonical home.

---

### F-2.4 — Checkpoint Dialog Standard Format

**(a)** `02-constitutional-companion.md`, lines 471–487 — defines the exact format for ALL AI checkpoint dialogs (✅ [Phase name] / 📋 Coming up next / → Type `continue` / → Type `stop here` / → Ask questions). Declares "at every ⛔ STOP or await human confirmation point, the agent MUST present this exact format."

**(b)** `agent-skills/base/AGENT.md` §3 (Guardrails) and §5 (Communication protocols) define general communication standards but do not specify this checkpoint dialog format. ENG-1.2 (AI-Engineer Pairing Law) mandates human confirmation checkpoints but gives no format standard.

**(c)** Add the checkpoint dialog standard to `agent-skills/base/AGENT.md` §5 as a universal AI communication protocol, so all skills can reference it rather than each skill defining or assuming its own format.

**(d)** **MED** — the format is used across multiple phases of this skill; making it a base protocol prevents protocol fragmentation as new skills are added.

---

### F-2.5 — Design Rationale File Format (Two Mandatory Sections)

**(a)** `02-constitutional-companion.md`, lines 1339–1360 — defines mandatory `design-rationale.md` structure: two sections (Overview for team leads; Detailed Explanation for junior/mid devs), alternatives discussion mandatory for non-trivial changes, pattern name required in every decision.

**(b)** `laws/engineering/governance.md` §ENG-6.7 (Audit Trail) requires logging; `agent-skills/skills-by-domain/discovery-research/spec-governance.md` (skill-spec-governance) defines PROPOSAL.md and tasks.md structure but does not define `design-rationale.md` format. ENG-11.2 (Proposal Completeness) defines PROPOSAL.md sections but not design-rationale.

**(c)** Add `design-rationale.md` as a formally defined artifact in `agent-skills/skills-by-domain/discovery-research/spec-governance.md` with its two-section format, and reference it from the companion with one line.

**(d)** **MED** — the design-rationale.md format is an audit-trail artifact (ENG-6.7) that should have a spec-governance home; currently it only exists in the adoption companion.

---

### F-2.6 — R4b Mutation Delta Offer (Mandatory Before R5)

**(a)** `02-constitutional-companion.md`, lines 1217–1234 — the R4b mutation delta offer rule: mandatory after all characterization tests pass, before R5 commit; describes exact offer text and framing. Lines 1232–1234 explicitly call it "mandatory — do not proceed to R5 without presenting it."

**(b)** `agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md` — the Atomic TDD skill defines 5 steps (RED/GREEN/REFACTOR/VERIFY/COMMIT) but has no R4b step and no mutation delta offer. `agent-skills/skills-by-domain/development-practices/11-mutation-testing.md` covers when to invoke mutation testing but not the R4b-as-mandatory-offer protocol.

**(c)** Add an explicit R4b sub-step to the TDD cycle in `agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md` VERIFY phase — "After all characterization tests pass, offer a scoped mutation delta before committing (informational; not a gate)" — so every TDD practitioner sees this protocol, not just adoption companion users.

**(d)** **MED** — R4b is described as mandatory but only defined in the adoption skill; any team using skill-06 directly misses it.

---

### F-2.7 — Constitution Freshness Pre-Flight (git fetch Check)

**(a)** `02-constitutional-companion.md`, lines 214–238 — the "silent pre-flight — constitution freshness check": runs `git fetch`, checks `[behind N]`, warns if behind, handles network failure, silently continues if AGENTS.md not found.

**(b)** This pre-flight behavior is not defined in `agent-skills/base/AGENT.md`, ENG-1.2, or any other corpus file. The closest context is `laws/engineering/spec-driven-development.md` §11.3 (Spec Freshness Law) which covers spec files going stale in the project, not the constitution repo itself.

**(c)** Add a "Constitution Repo Freshness" requirement to `agent-skills/base/AGENT.md` §3.2 (ALWAYS Do List) — "Before any governed workflow, silently check that the local constitution repo is current (per ENG-11.3)" — and remove the inline procedure from the companion, replacing it with a base-AGENT.md reference.

**(d)** **MED** — every skill should run this check, not just the companion; centralizing it in AGENT.md prevents it being skipped when users invoke other skills directly.

---

### F-2.8 — Ambiguous-Response Handling Rule (Re-Prompt Exactly Once)

**(a)** `02-constitutional-companion.md`, lines 362–368 — rule for Path A/B selection: "if the user's reply does not clearly indicate Path A or Path B (e.g., idioms, jokes, oblique agreement), do NOT infer a path. Re-prompt exactly once."

**(b)** `agent-skills/base/AGENT.md` §3.2 (ALWAYS Do List) and §5 define communication standards but do not specify the "re-prompt exactly once then escalate" rule for ambiguous confirmation responses. ENG-1.2 mandates human confirmation checkpoints but gives no ambiguity-handling protocol.

**(c)** Add "ambiguous confirmation → re-prompt once, never infer" as a guard to `agent-skills/base/AGENT.md` §3 (Guardrails), making it a universal protocol that all confirmation-gated skills inherit.

**(d)** **LOW** — a general protocol currently defined only in one skill; low risk of divergence but improves constitutional completeness.

---

## TYPE 3 — Gaps the Skill Fills That the Constitution Does Not

---

### F-3.1 — Adoption State Priority Matrix (4-Priority Routing Logic)

**(a)** `02-constitutional-companion.md`, lines 270–277 — the four-priority adoption status routing table: P1=Resume in-progress proposal, P2=Companion Mode (already adopted), P3=Update context (partial artifacts), P4=Full gateway (clean slate). With detailed resume protocol for P1 (read tasks.md → find last [x] line → find first [ ] → read phase doc → present resume prompt).

**(b)** No corpus file defines an adoption state machine or routing logic. `laws/engineering/spec-driven-development.md` §11.1 defines the PROPOSE→IMPLEMENT→ARCHIVE lifecycle but not session-resume detection. `agent-skills/skills-by-domain/discovery-research/spec-governance.md` defines the lifecycle but not priority-ordered state detection.

**(c)** Formalize the 4-priority routing table as a `session-state-detection` protocol in `agent-skills/skills-by-domain/discovery-research/spec-governance.md` — this is a reusable pattern any spec-governed skill would benefit from for session continuity.

**(d)** **HIGH** — this is the only place in the constitution where the session-resume problem is systematically solved; it is valuable enough to be a canonical protocol.

---

### F-3.2 — Refactoring Backlog Schema and Status State Machine

**(a)** `02-constitutional-companion.md`, lines 392–415 (Phase 3b section in supplement) and lines 997–999, 1090–1106, 1421–1425 — `refactoring-backlog.md` schema with columns (ID, Seam, Characterized?, Type, Refactoring/Task, Pattern/Law, Status); status states BLOCKED→PROPOSED→IN PROGRESS→COMPLETE; MUTATION entry auto-add rules; backlog presentation grouped by seam.

**(b)** `agent-skills/skills-by-domain/discovery-research/spec-governance.md` defines PROPOSAL.md and tasks.md but not the refactoring-backlog.md artifact. `laws/engineering/spec-driven-development.md` §11.1 does not mention the refactoring backlog. ENG-6.7 (Audit Trail) requires all operations to be logged but doesn't define the backlog format. No corpus file defines this living artifact or its status transitions.

**(c)** Add `refactoring-backlog.md` as a formally specified artifact in `agent-skills/skills-by-domain/discovery-research/spec-governance.md` with its schema, state machine (BLOCKED→PROPOSED→IN PROGRESS→COMPLETE), and MUTATION-entry auto-add trigger rule (score < 70% → add MUTATION row per ENG-4.11).

**(d)** **HIGH** — this is a central operational artifact of Phase 4 that exists only in the adoption companion; any team building new skills around the refactoring loop would have no canonical schema to reference.

---

### F-3.3 — Trust Ramp (4-Rung AI Autonomy Calibration Model)

**(a)** `02-constitutional-companion.md`, lines 1601–1630 — Trust Ramp with 4 rungs (Observe / Draft Test / Pair / Accelerate), rules for rung progression (developer chooses, AI never suggests moving up, explicit consent required), default rung (Rung 2).

**(b)** `laws/engineering/foundations.md` §1.2 (ENG-1.2, AI-Engineer Pairing Law) says "AI assistants SHALL act as teaching partners" and lists 5 abstract principles (Follow Constitution, Explain WHY, Build mental models, Develop judgment, Enable independence). The law is correct in intent but gives no operational model for _how_ to calibrate AI autonomy. `agent-skills/base/AGENT.md` §1.2 (Teaching-First Mindset) and §1.4 (Teaching Feedback Loop) are philosophical but give no rung-based autonomy model. No corpus file defines a structured AI trust calibration model.

**(c)** Add the Trust Ramp (4 rungs) to ENG-1.2's law detail in `laws/engineering/foundations.md` as the canonical implementation of "Enable independence" — the rung model is the concrete operationalization of ENG-1.2 and should be authoritative, not adoption-skill-local.

**(d)** **HIGH** — ENG-1.2 is one of the most-cited laws in the corpus; the Trust Ramp is the only place it becomes operationally concrete. Every skill that invokes ENG-1.2 should be able to reference the same model.

---

### F-3.4 — Cross-Bounded-Context Seam Conflict Protocol

**(a)** `02-constitutional-companion.md`, lines 680–700 — when a confirmed seam contains files from multiple bounded contexts: three options (A=expand scope, B=truncate seam at boundary with note, C=defer seam and pick another), with mandatory stop-and-present behavior.

**(b)** `laws/engineering/architecture.md` §2.4 (ENG-2.4, Bounded Context Law) says "Systems SHALL be decomposed into bounded contexts with well-defined interfaces" but gives no protocol for the seam-crossing conflict during adoption. `agent-skills/skills-by-domain/development-practices/07-vertical-slice-dev.md` addresses vertical slicing but not bounded context collision during archaeology.

**(c)** Add a "Cross-Boundary Seam Conflict" note to ENG-2.4 in `laws/engineering/architecture.md` — or add it to `docs/guides/adoption/brownfield-adoption.md` as a "Seam Scope Conflicts" section — so the three-option protocol has a canonical home.

**(d)** **MED** — this is a real and common adoption problem; it currently has no resolution protocol anywhere else.

---

### F-3.5 — Dead Code Exemption and Structurally-Blocked Coverage Protocols

**(a)** `02-constitutional-companion.md`, lines 892–920 — two distinct coverage exception protocols: (1) Dead code exemption: list lines + mark with exclusion annotation + do NOT modify; (2) Structurally-blocked lines: list coupling reason + add REFACTOR backlog entry for DI extraction + record partial coverage with note. Both define exact file formats for `phase-3-characterize.md`.

**(b)** `laws/engineering/testing.md` §4.6 (ENG-4.6, Coverage Requirements) states "100% coverage for critical paths" and lists thresholds but gives no exception handling for legitimately unreachable code. `docs/guides/testing/characterization-testing.md` does not cover coverage exceptions. No corpus file defines the distinction between dead code and structurally-blocked code or how to handle either.

**(c)** Add a "Coverage Exception Protocols" subsection to `laws/engineering/testing.md` §4.6 (or to `docs/guides/testing/characterization-testing.md`) defining both exception types, their documentation requirements, and the prohibition on modifying unreachable code during Phase 3c.

**(d)** **MED** — the distinction between dead code and coupled-untestable code is a real and subtle testing concern that should be a constitutional reference; currently only teams using the adoption companion know about it.

---

### F-3.6 — Phase 4 Backlog Inconsistency / Session-Resume Consistency Check

**(a)** `02-constitutional-companion.md`, lines 1057–1077 — silently runs `git log --oneline -5`, cross-checks backlog Status vs committed ref-{id} commits to detect "committed but backlog not updated" inconsistency; auto-corrects COMPLETE rows before presenting the backlog.

**(b)** `agent-skills/skills-by-domain/discovery-research/spec-governance.md` covers the PROPOSE→IMPLEMENT→ARCHIVE lifecycle but has no session-resume inconsistency detection. ENG-6.7 (Audit Trail) requires traceability but does not define a repair protocol. No corpus document covers recovery from a partial session crash.

**(c)** Add a "Session Resume Protocol" to `agent-skills/skills-by-domain/discovery-research/spec-governance.md` — check git log vs proposal/backlog state before presenting open work — making it available to any SDD-governed workflow, not only the adoption companion.

**(d)** **MED** — crash/resume resilience is a constitutional quality that every governed workflow should exhibit; centralizing this protocol prevents it being re-invented per skill.

---

### F-3.7 — Minimum Viable Session Model (Time-Boxed Adoption Cadence)

**(a)** `02-constitutional-companion.md`, lines 1634–1661 — five-row table mapping time slots (15/30/60 min/2h/4h) to specific constitutional activities, plus four low-bandwidth adoption rules and a project-rules.md template section.

**(b)** `docs/guides/adoption/pragmatic-adoption.md` Part 7 covers "Minimum Viable Session" and cross-references it in the table of contents; the companion's table is either the source or a parallel version. The guide mentions 15–60 min sessions in its TOC but its actual content was not fully readable in this audit run. `docs/guides/adoption/brownfield-adoption.md` does not address time-boxing.

**(c)** Verify that `docs/guides/adoption/pragmatic-adoption.md` §Part 7 contains this table; if so, replace the companion's section with a 2-line callout. If not, add it to the guide as Part 7's content and reference it.

**(d)** **MED** — likely duplicated in the guide file; the companion should point to the guide for this content.

---

### F-3.8 — GRASP Pattern Table (No Canonical Home in Corpus)

**(a)** `02-constitutional-companion.md`, lines 1509–1523 — 9-row GRASP table: Information Expert, Creator, Controller, Low Coupling, High Cohesion, Polymorphism, Pure Fabrication, Indirection, Protected Variations — with "Ask This" and "Assign Responsibility To" columns.

**(b)** No corpus file defines GRASP patterns. `laws/engineering/architecture.md` ENG-2.1 (DDD) and ENG-3.4 (SRP) reference design concepts; `agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md` covers DDD but not GRASP. `agent-skills/skills-by-domain/development-practices/09-refactoring.md` covers code smells and Fowler catalog refactorings but not GRASP. The constitution corpus has a complete gap on GRASP.

**(c)** Add the GRASP table (all 9 patterns) to `laws/engineering/architecture.md` §2.1 as "Responsibility Assignment" guidance, or create a new `docs/guides/constitution/grasp-patterns.md` guide, so the companion can replace its inline table with a reference.

**(d)** **MED** — GRASP is named in multiple laws (ENG-3.4, ENG-2.3) and is central to the Phase 3b Target Architecture design process; its absence from the corpus means it cannot be cited by ID from any other skill or law.

---

### F-3.9 — SonarQube Dual-Credential Requirement (Analysis Token vs Read Token)

**(a)** `02-adoption-setup.md`, lines 483–497 — the specific insight that `PROJECT_ANALYSIS_TOKEN` can push results but cannot read metrics from the SonarQube API; teams need both a scan token and a separate read/admin token; exact prompt to ask for both upfront.

**(b)** `agent-skills/skills-by-domain/platform-engineering/skill-sonarqube-compliance-gate.md` — covers SonarQube gate operations but contains no credential-type guidance. No corpus document warns about this operational SonarQube distinction.

**(c)** Add the dual-credential requirement note to `agent-skills/skills-by-domain/platform-engineering/skill-sonarqube-compliance-gate.md` §Setup, and reference it from the adoption supplement's Phase 3d section.

**(d)** **LOW** — a specific operational gotcha that causes real adoption friction; warrants a one-paragraph addition to the sonarqube skill.

---

### F-3.10 — `CHARACTERIZE-ONLY` Verdict → Records as `REFACTOR — DEFERRED`

**(a)** `02-adoption-setup.md`, lines 366–383 — the convention that a CHARACTERIZE-ONLY verdict is recorded in `phase-2-decision.md` as `REFACTOR — DEFERRED`; the backlog entry uses `REFACTOR — DEFERRED` as Status; when the user returns later, Phase 3b Gate 2 (Target Architecture) is presented before refactoring begins; PROPOSAL.md Approach line records `CHARACTERIZE-ONLY — verdict deferred`.

**(b)** No corpus document defines this three-way verdict system (REFACTOR/REWRITE/CHARACTERIZE-ONLY) or the recording convention for the deferred path. `laws/engineering/testing.md` §4.10 (ENG-4.10, Test Evolution Law) says characterization tests are "transitional scaffolding" but gives no protocol for the deferred-design pattern.

**(c)** Add the three-verdict decision framework (REFACTOR/REWRITE/CHARACTERIZE-ONLY with their recording conventions) to `agent-skills/skills-by-domain/discovery-research/spec-governance.md` as an "Adoption Verdict" sub-protocol, making the deferred-design pattern a constitutionally defined concept.

**(d)** **LOW** — this is a legitimate constitutional concept (defer design decisions while still building a safety net) that has no home outside the supplement; elevating it increases its visibility and prevents ad-hoc reinvention.

---

### F-3.11 — Environment Notes Recording Rule (project-rules.md ##Environment Notes)

**(a)** `02-constitutional-companion.md`, lines 817–826 — rule: if the test run requires a non-default environment setting (JAVA_HOME, build flag, env variable), record it in `project-rules.md ## Environment Notes` before continuing, with exact format.

**(b)** `laws/engineering/devops.md` covers CI/CD but not local environment documentation. No corpus document mandates recording environment workarounds in project-rules.md. `docs/guides/adoption/adoption-compliance-checklist.md` does not include an Environment Notes check.

**(c)** Add "Environment workarounds MUST be recorded in `project-rules.md ## Environment Notes`" to ENG-11.1's Hangar SDD Law requirements or to the adoption compliance checklist, making it a formal governance obligation.

**(d)** **LOW** — a minor but operationally important rule; currently only teams using the companion know about it.

---

## Summary Table

| # | Type | Priority | One-line Description | File + Line Range |
|---|------|----------|---------------------|-------------------|
| F-1.1 | 1 — Duplicate | **HIGH** | Correction-prompts table duplicates `ai-correction-prompts.md` | companion 186–205 |
| F-1.2 | 1 — Duplicate | **HIGH** | 8-step TDD cycle embedded in AGENTS.md template | setup 117–128 |
| F-1.3 | 1 — Duplicate | **HIGH** | Seam glossary + Feathers types duplicate characterization guide | companion 551–598 |
| F-1.4 | 1 — Duplicate | **HIGH** | GRASP/SOLID/DDD tables duplicate ddd-law.md and architecture law | companion 1509–1551 |
| F-1.5 | 1 — Duplicate | **MED** | SonarQube setup dialog duplicates skill-sonarqube-compliance-gate | setup 449–531 |
| F-1.6 | 1 — Duplicate | **MED** | Violation tier table duplicates brownfield-adoption.md and sonarqube skill | companion 753–760 |
| F-1.7 | 1 — Duplicate | **MED** | Refactoring PROPOSAL.md template duplicates spec-governance schema | companion 1155–1194 |
| F-1.8 | 1 — Duplicate | **LOW** | "Key Files" section duplicates how-to-adopt-constitution.md Steps 2–4 | companion 1767–1812 |
| F-1.9 | 1 — Duplicate | **LOW** | "What's Next" section duplicates pragmatic-adoption.md + greenfield guide | companion 1816–1862 |
| F-2.1 | 2 — Belongs Elsewhere | **HIGH** | ENG-3.1 "design signal not counting rule" interpretation belongs in quality law | companion 1499–1506, 1742–1755 |
| F-2.2 | 2 — Belongs Elsewhere | **HIGH** | Sociable testing invariant (seam = no-mock boundary) belongs in testing law §4.8 | companion 787–800 |
| F-2.3 | 2 — Belongs Elsewhere | **HIGH** | God class definition + Target Architecture format belong in quality/architecture laws | companion 557, 334–350 |
| F-2.4 | 2 — Belongs Elsewhere | **MED** | Checkpoint dialog standard format belongs in AGENT.md §5 | companion 471–487 |
| F-2.5 | 2 — Belongs Elsewhere | **MED** | design-rationale.md two-section format belongs in spec-governance | companion 1339–1360 |
| F-2.6 | 2 — Belongs Elsewhere | **MED** | R4b mandatory mutation delta offer belongs in skill-06-atomic-tdd | companion 1217–1234 |
| F-2.7 | 2 — Belongs Elsewhere | **MED** | Constitution freshness git-fetch check belongs in AGENT.md §3.2 | companion 214–238 |
| F-2.8 | 2 — Belongs Elsewhere | **LOW** | Ambiguous-response re-prompt-once rule belongs in AGENT.md §3 | companion 362–368 |
| F-3.1 | 3 — Gap | **HIGH** | Adoption state priority matrix (4-priority routing) not in corpus | companion 270–277 |
| F-3.2 | 3 — Gap | **HIGH** | Refactoring backlog schema + status state machine not in spec-governance | companion 392–415, setup 397–415 |
| F-3.3 | 3 — Gap | **HIGH** | Trust Ramp (4-rung AI autonomy model) not in ENG-1.2 | companion 1601–1630 |
| F-3.4 | 3 — Gap | **MED** | Cross-bounded-context seam conflict protocol not in ENG-2.4 | companion 680–700 |
| F-3.5 | 3 — Gap | **MED** | Dead code + structurally-blocked coverage exception protocols not in testing laws | companion 892–920 |
| F-3.6 | 3 — Gap | **MED** | Session-resume backlog consistency check not in spec-governance | companion 1057–1077 |
| F-3.7 | 3 — Gap | **MED** | Minimum Viable Session time-box model not confirmed in guide | companion 1634–1661 |
| F-3.8 | 3 — Gap | **MED** | GRASP pattern table has no canonical home anywhere in the corpus | companion 1509–1523 |
| F-3.9 | 3 — Gap | **LOW** | SonarQube dual-credential gotcha not in sonarqube compliance skill | setup 483–497 |
| F-3.10 | 3 — Gap | **LOW** | CHARACTERIZE-ONLY → `REFACTOR — DEFERRED` recording convention not in corpus | setup 366–383 |
| F-3.11 | 3 — Gap | **LOW** | Environment Notes recording rule not in Hangar SDD Law | companion 817–826 |

---

## Net Size Impact Estimate (HIGH-Priority Findings Only)

If all **HIGH**-priority findings were acted on:

| Finding | Lines in subject file | Lines after change | Saved |
|---------|----------------------|--------------------|-------|
| F-1.1 Correction prompts table | ~20 | 5 | ~15 |
| F-1.2 8-step TDD in AGENTS.md template | ~12 | 2 | ~10 |
| F-1.3 Seam theory / Feathers definitions | ~48 | 5 | ~43 |
| F-1.4 GRASP/SOLID/DDD tables | ~45 | 8 | ~37 |
| F-2.1 ENG-3.1 interpretation (2 locations) | ~20 | 3 | ~17 |
| F-2.2 Sociable testing invariant | ~14 | 3 | ~11 |
| F-2.3 God class definition/Target Arch | ~20 | 4 | ~16 |
| F-3.1 Adoption state matrix (no removal) | — | — | — |
| F-3.2 Backlog schema (no removal) | — | — | — |
| F-3.3 Trust Ramp (no removal — stays as companion procedure; law gets augmented) | — | — | — |

**Estimated reduction from HIGH findings: ~149 lines** (~8% of the combined 2,401-line subject file total). This is a conservative estimate; if the GRASP table is canonicalized (F-3.8, MED), an additional ~12 lines could be replaced with a reference. Applying all MED-priority duplicates (F-1.5 through F-1.7) would save a further ~160 lines.

**Total potential reduction (HIGH + MED duplicates): ~310 lines** (~13% of total).

---

## Top 5 Recommendations

**1. Canonicalize the Trust Ramp in ENG-1.2** *(F-3.3, HIGH)*
ENG-1.2 is cited in dozens of corpus files as "AI-Engineer Pairing Law" but has no operational model for *how* to calibrate AI autonomy. The Trust Ramp is the single best implementation of that law. Adding it to `laws/engineering/foundations.md` §1.2 transforms the law from philosophy into an executable protocol — every skill that invokes ENG-1.2 can reference the same 4-rung model, and the law becomes self-enforcing rather than aspirational.

**2. Promote the Refactoring Backlog Schema to spec-governance** *(F-3.2, HIGH)*
The `refactoring-backlog.md` schema (BLOCKED→PROPOSED→IN PROGRESS→COMPLETE state machine, MUTATION auto-add rule, seam/characterization tracking) is the central artifact of Phase 4 and has no canonical home. Adding it to `agent-skills/skills-by-domain/discovery-research/spec-governance.md` makes it a first-class SDD artifact alongside PROPOSAL.md and tasks.md — enabling future skills to reuse the same backlog protocol without re-inventing it.

**3. Move the ENG-3.1 "design signal" interpretation into the law** *(F-2.1, HIGH)*
The interpretation that "ENG-3.1 limits are subservient to good object design" is the single most important constitutional nuance for preventing mechanical compliance. It currently lives only in the adoption companion, meaning developers reading ENG-3.1 directly encounter a hard line-count rule with no design-first context. One paragraph added to `laws/engineering/quality.md` §3.1 makes this nuance canonical and allows the companion to cite the law rather than re-state the interpretation.

**4. Add the Sociable Testing Invariant to ENG-4.8** *(F-2.2, HIGH)*
The rule that "the seam boundary = the no-mock boundary" is the practical implementation of ENG-4.8 (Mock Boundaries Law). Without it, a developer reading ENG-4.8 knows to mock "only at I/O boundaries" but has no definition of what counts as "inside the seam" during characterization. One implementation note in `laws/engineering/testing.md` §4.8 closes this gap and makes the seam concept load-bearing in the testing law — not just in the adoption companion.

**5. Replace GRASP/DDD/SOLID inline tables with corpus references** *(F-1.4 + F-3.8, HIGH/MED)*
The three design-principles tables (GRASP 9-row, SOLID 5-row, DDD 7-row) in the companion's Step 5 are 45 lines of reference content that belong in canonical homes. DDD is in `docs/guides/constitution/ddd-law.md` and `laws/engineering/architecture.md`. SOLID maps to `laws/engineering/quality.md` §3.4. GRASP has no home — adding it to `laws/engineering/architecture.md` §2.1 as "Responsibility Assignment" is a one-time 15-line addition. Once canonicalized, the companion's Step 5 becomes 3 citation lines and a one-sentence pattern-application rule, reducing both the maintenance burden and the risk that the companion's table drifts from canonical guidance.
---

## TYPE 4 — Missing Law Citations

The skill has **52 constraint lines** (`⛔`, `MUST`, `SHALL`, mandatory, forbidden) but only **3 cite a law ID**. Rules asserted without constitutional authority are harder for AI agents to apply correctly (they apply the letter, not the spirit) and harder to amend if a law changes.

| Rule (paraphrased) | Companion line | Should cite |
|---|---|---|
| MUST NOT start refactoring until human explicitly chooses to | 519 | ENG-1.2 |
| Seam-wide sociable testing invariant — no mocks inside seam boundary | 787 | ENG-4.8 |
| Coverage gates apply to seam files — not the entire codebase | 830 | ENG-4.6 |
| Do NOT change any logic in Phase 3c — characterization tests only | 959 | ENG-4.1 |
| If any characterization test goes RED: fix the code, not the test | 1191 | ENG-4.1 |
| SHOW the test run output before proceeding — do not summarize | 1206 | ENG-4.1 |
| R4b offer is mandatory — do not proceed to R5 without presenting it | 1232 | ENG-4.11 |
| Prohibited: mechanically splitting a method at line 50 without design | 1501 | ENG-3.1 |
| Agent MUST NOT scan files outside the declared bounded context | 1693 | ENG-2.3 / ENG-2.4 |
| Each iteration MUST NOT add new violations | 1706 | ENG-4.2 / ENG-12.1 |
| Checkpoint dialog standard format MUST be used at every gate | 473 | ENG-1.2 |
| Mutation baseline guard before seam-clean detection | 1367 | ENG-4.11 |
| Commit message MUST reference spec scenario ID | (tasks template) | ENG-6.7 |
| All refactorings MUST be logged in refactoring-backlog.md | 997–999 | ENG-6.7 |

**Root pattern:** The laws exist — they just weren't cited when the rules were written. Adding `(ENG-X.X)` to each constraint is mechanical once the law mapping is known (see table above).

**Recommended approach:** When implementing any of the Type 1–3 findings above, add the missing citation at the same time. This does not require a separate amendment — it is a quality improvement that happens as a side effect of the canonicalization work.

---

## Audit Metadata

- **Conducted:** 2026-05-13
- **Corpus size read:** Laws (24 files), skills (68 files), avatars (index), guides (40 files)
- **Subject file versions:** `02-constitutional-companion.md` v2.25.0; `02-adoption-setup.md` (no separate version)
- **Total findings:** 30 (9 HIGH, 14 MED, 7 LOW)
- **Estimated line reduction if all HIGH findings acted on:** ~149 lines (~6% of 2,401 combined)
- **Estimated line reduction if HIGH + MED duplicates acted on:** ~310 lines (~13% of combined)

---

## Appendix — Analysis Prompt

The following prompt was used to generate this audit (Types 1–3). Type 4 (missing law citations) was added as a separate manual pass after the agent completed.

---

> Perform a constitutional cross-reference audit. Read every file listed below thoroughly before forming any conclusions. Thoroughness matters more than speed.
>
> ## Files to audit (the subject)
> - `agent-skills/skills-by-domain/development-practices/02-constitutional-companion.md`
> - `agent-skills/skills-by-domain/development-practices/02-adoption-setup.md`
>
> ## Files to read as the constitutional reference corpus
> Read ALL of these:
> - All YAML files: `laws/index.yaml`, `laws/engineering/*.yaml`, `laws/product/*.yaml`, `laws/business/*.yaml`
> - All skill index files: `agent-skills/skills-by-domain/*/index.yaml`
> - All skill markdown files: `agent-skills/skills-by-domain/**/*.md` (excluding the subject files above)
> - `agent-skills/base/AGENT.md`
> - `avatars/index.yaml`
> - All guide files: `docs/guides/**/*.md`
>
> ## What to find
>
> ### Finding Type 1 — Duplication / Already Covered
> Passages in the companion skill (or supplement) that are substantially covered by an existing law, skill, avatar, or guide. For each:
> - What does the companion skill say (file + approximate line range)
> - What existing artifact covers the same ground (file + section)
> - Could the skill replace its prose with a callout/cross-reference to that artifact?
> - What would that callout look like (one sentence)?
>
> ### Finding Type 2 — Content That Belongs Elsewhere
> Passages in the companion skill that contain governance content — design principles, law interpretations, test rules, audit requirements, GRASP/SOLID principles — that should be canonical in a law or base skill rather than buried in a single adoption skill. For each:
> - What is the content (file + line range)
> - Where should it live (specific law ID, skill name, or new law/skill to create)
> - What minimum change to the constitution artifact would allow the companion skill to replace that section with a one-line reference?
>
> ### Finding Type 3 — Gaps the Skill Fills That the Constitution Does Not
> Passages in the companion skill that teach or enforce something with no counterpart anywhere else in the constitution. These are candidates for new or amended laws/skills. For each:
> - What is the content (file + line range)
> - Which existing law or skill is the closest home, OR what new law/skill should own it
> - What is the minimum addition needed to that artifact?
>
> ## Output format
> For each finding:
> - **(a)** File + approximate line range in the companion skill
> - **(b)** Counterpart location or proposed new home in the constitution
> - **(c)** One-sentence recommendation
> - **(d)** Priority: **HIGH** / **MED** / **LOW**
>
> Group findings by type (1, 2, 3). Within each group, sort by priority HIGH → MED → LOW.
>
> At the end, provide:
> - A **summary table** of all findings
> - A **net size impact estimate** if all HIGH-priority findings were acted on
> - A **top 5 recommendations**
>
> Be thorough. Do not skim or skip sections.

---

### Type 4 prompt (added after agent run — manual pass)

> Scan `02-constitutional-companion.md` for all constraint lines (`⛔`, `MUST`, `SHALL`, `mandatory`, `forbidden`, `prohibited`). For each that does NOT already cite a law ID (e.g., `ENG-4.1`), identify which law in the corpus should be cited. Produce a table: rule (paraphrased) | line number | law that should be cited.
>
> Context: the skill has ~52 constraint lines but only 3 cite a law ID. Adding citations makes rules traceable, helps AI agents apply them in spirit not just letter, and makes law amendments automatically visible in the skill.


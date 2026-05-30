# Stage C: Jobs-To-Be-Done — Evidence Artifact

**Changeset:** `build-adoption-guide-2026-001`
**Stage:** C — Jobs-To-Be-Done (PRD-2.3, PRD-3.1, PRD-3.2)
**Authority:** PRD-2.5 ⛔ (Discovery Stage-Gate Law), PRD-2.3 (Jobs-to-be-Done Law), PRD-3.1 (Persona Development Law), PRD-3.2 (Journey Mapping Law)
**Status:** v1.2 — 2026-05-06 — JURY-CLEARED. DC-07 (Human Agency & Adaptive Scope) ratified 6/6 APPROVE (2 rounds). All 7 design constraints binding on IMPLEMENT.
**Gate:** Stage D entry — ✅ OPEN for Coach path vertical slice | Architect path BLOCKED until SD-OBL-1 / SC-OBL-2 satisfied

---

## Pre-Stage C Gate Verification

| Gate | Requirement | Status |
|------|------------|--------|
| **G3** | `stage-b-evidence.md` jury-validated at Moderate before Stage C | ✅ CLEARED — unanimous Round 2, 2026-05-05 |
| **G5** | `compliance/threat-model.md` filed (ENG-6.1 ⛔) | ✅ FILED v1.0 — awaiting Tomás Reyes + Alexandra Pierce APPROVE before IMPLEMENT |
| **G6** | `compliance/data-classification.md` filed (BUS-3.1 ⛔, ENG-6.4 ⛔) | ✅ FILED v1.0 — awaiting Carlos Mendez + Alexandra Pierce APPROVE before IMPLEMENT |
| **G7** | `compliance/risk-register.md` filed (BUS-6.1 ⛔) | ✅ FILED v1.0 — awaiting Carlos Mendez + Alexandra Pierce APPROVE before IMPLEMENT |

> **Note:** G5/G6/G7 gates require FILED before Stage C begins; jury APPROVE on these compliance artifacts is required before Stage D IMPLEMENT begins. This is a Stage D entry obligation — not a Stage C blocker.

---

## §1. Persona Definitions (PRD-3.1)

### How to Read This Section

Personas are evidence-based per PRD-3.1. Each includes:
- **Evidence basis** — interview count and data source
- **Behavioral attributes** — goals, frustrations, context
- **PRD-3.1 exception note** — where fewer than 5 interviews are on file

---

### Persona 1 — Technical Coach

```
Persona Name: Technical Coach (internal AA AI governance coach)

Who they are:
- Role/context: Internal American Airlines engineers or architects who have been
  designated to onboard and coach engineering teams on Hangar AI Constitution adoption.
  They run onboarding sessions, guide teams through the adoption workflow, and serve
  as the primary point of human escalation when teams have governance questions.
- Goals:
  - Complete a full constitutional adoption session in under 60 minutes
  - Ensure teams can operate independently after the first session
  - Build AI trust in teams skeptical of agent-generated code
  - Give teams a concrete artifact (URL, prompt) they can act on immediately
- Frustrations:
  - No single URL — must share multi-step clone instructions via Teams message
  - Explaining what the agent is doing takes the most time in every session
  - Teams adopt (run the workflow) but most never complete a constitutionally-governed task
  - Amendment process, multi-repo handling, and upgrade path questions surface unexpectedly in session

Evidence base:
- Interviews: 4 conducted (Jay Turpin, Steve Fraser, Wyatt Sutherland, Kenneth Robinson)
  Combined: 27+ adoptions across 12+ teams
- PRD-3.1 exception: PRD-3.1 requires minimum 5 interviews per persona. 4 were received.
  Exception is documented: the 4 respondents represent 27+ combined adoptions (substantially
  richer than 5 minimal interviews). Qualitative saturation is evident — findings are consistent
  across all 4 respondents on DA-01, DA-06, NF-02, and DA-03 invalidation. One additional
  interview would not materially change the JTBD framing. Jury ratification required at T2.3e.

Key jobs to be done:
1. (Core) Get a new team from "never heard of constitution" to first governed task — fast
2. Answer "what is the agent doing?" without breaking session flow
3. Provide upgrade path and amendment process answers on-the-spot
4. Conduct a 15-min foothold session when teams are time-constrained
5. Share ready-to-run Teams prompt templates per adoption phase

Success looks like:
Team completes at least one constitutionally-governed task within 2 weeks of onboarding.
Coach can run the next session with a different team using the same single URL.
```

---

### Persona 2 — Senior Architect

```
Persona Name: Senior Architect

Who they are:
- Role/context: Senior engineers or architects responsible for evaluating whether
  AI-governed development aligns with existing architectural standards (DDD, layered
  architecture, vertical slice). They may be asked by leadership or team leads to
  provide a go/no-go recommendation on constitutional adoption.
- Goals:
  - Map Hangar AI laws to architectural patterns they already know
  - Determine law precedence and NN status without asking a constitution maintainer
  - Understand constitutional authority chain for amendment escalation
- Frustrations:
  - Law-to-skill-to-enforcement connection requires cross-referencing 3+ files (CA-06)
  - P2 (Constitutional AI Model Viz) is orphaned — no navigational parent (CA-03)
  - No architectural alignment view — cannot quickly evaluate DDD compliance posture

Evidence base:
- Interviews: 0 direct (all Stage B respondents were Technical Coaches)
- Evidence basis: Repository inspection (CA-06, CA-03), PROPOSAL.md Tomás Reyes persona
  notes (Rounds 1–7), DA-04 assumption (INSUFFICIENT DATA per §3.3 stage-b-evidence.md)
- ⚠️ SC-OBL-2 OBLIGATION: ≥ 2 Senior Architect or Engineer interviews required before
  Stage D IA design for P4 and the Architect path of P3. JTBDs below are HYPOTHESES
  pending SC-OBL-2 validation. Stage D IA for P4 and Architect path WILL NOT begin
  until these JTBDs are confirmed or revised based on real respondent data.

Key jobs to be done (HYPOTHESIS — pending SC-OBL-2):
1. Evaluate constitutional law-to-DDD alignment before recommending adoption to team
2. Determine NN law precedence and amendment authority for a given edge case
3. Communicate architectural governance posture to leadership with one artifact

Success looks like:
Architect can complete their evaluation in a single session and produce a written
recommendation without asking the constitution maintainer for clarification.
```

---

### Persona 3 — Engineer

```
Persona Name: Engineer (constitutionally-governed implementer)

Who they are:
- Role/context: Software engineers implementing features under constitutional governance.
  They use the agent to propose, implement, and archive governed tasks.
- Goals:
  - Know exactly what to do next for their first governed task
  - Look up a specific law by keyword mid-task without leaving the IDE
  - Trust that the agent's output is constitutionally correct
- Frustrations:
  - Laws feel abstract and disconnected from daily implementation decisions
  - SDD workflow (PROPOSE→IMPLEMENT→ARCHIVE) is written for agents, not human engineers
  - Unclear which law applies to a specific implementation scenario

Evidence base:
- Interviews: 0 direct
- Evidence basis: Inference from Technical Coach observations (Steve: engineers need
  basic coding skills to verify AI output; Jay: teams ask "how do we verify it's using
  all the laws?"; NF-02: agent comprehension bottleneck affects engineers directly)
- ⚠️ DEFERRED PERSONA: Engineer quick start path is NOT in MVP scope. Per PROPOSAL.md,
  the Engineer path is in NEXT slice (P4–P7). JTBDs documented here for completeness;
  Stage C validation for Engineer path is not required before Stage D MVP begin.
  ≥ 2 Engineer interviews required before Engineer path enters Stage D IA design.

Key jobs to be done (DEFERRED — Engineer path is NEXT slice):
1. Complete first governed task without coach help: know exactly what step comes next
2. Look up any law mid-task by keyword in under 30 seconds
3. Understand what the agent just proposed and why before approving it

Success looks like:
Engineer completes first governed PR independently and can explain the constitutional
rationale for every law cited in the agent's proposal.
```

---

## §2. Jobs-To-Be-Done (PRD-2.3)

### JTBD Format (per PRD-2.3)

```
When [situation],
I want to [motivation],
So I can [expected outcome].
```

---

### 2.1 Technical Coach JTBDs (Evidence-Backed)

---

**JTBD-TC-01 — Core Adoption Job**

> When I sit down with a new engineering team that has never seen the Hangar AI Constitution,
> I want to open a single URL that immediately shows the constitution's value and gives the team a clear first action,
> So I can complete their initial adoption session in under 60 minutes without improvising or switching tabs.

**Evidence:** DA-01 CONFIRMED 4/4 (no single URL exists). DA-06 CONFIRMED 3/4 (baseline 1–3 hours). Jay: *"Clone the constitution... read adoption-workflow... follow the guidance"* — this is 4 steps before any value is shown. Wyatt: teams are "blown away" once they see it — the problem is friction to that moment.

**Functional job:** Navigate a new team to the constitution's entry point and first action.
**Emotional job:** Feel prepared and confident — not improvising on the spot.
**Social job:** Be seen as the person who made AI governance accessible, not the person who handed them a wall of docs.

---

**JTBD-TC-02 — Agent Comprehension Job**

> When an engineer on my team asks "what is the agent actually doing right now?" during an onboarding session,
> I want a clear, plain-language explanation of each step in the agent's workflow,
> So I can answer confidently and maintain team trust without breaking session flow.

**Evidence:** NF-02 (3/4): Jay: *"just explaining what the agent is doing"*; Steve: *"trusting the AI, how to prompt correctly"*; Kenneth: *"the agent work"* — this is the PRIMARY time sink identified by 3 of 4 coaches independently.

**Functional job:** Explain agent behavior at each step without consulting the AGENT.md raw file.
**Emotional job:** Feel like an expert, not a translator reading from a manual.
**Social job:** Be perceived as someone who deeply understands the tool — not someone struggling to explain it.

---

**JTBD-TC-03 — Constitutional Questions Job**

> When a team asks unpredictable questions about the constitution (upgrade path, multi-repo handling, law verification, amendment process),
> I want quick-reference answers immediately available at the right moment in the session,
> So I can answer authoritatively without deferring to a future follow-up.

**Evidence:** NF-04 (amendment process surfaces unprompted in first session, Jay Q2). NF-05 (multi-repo and upgrade path questions surface in first session, Jay Q2). These questions are consistent across sessions — they are predictable unprompted needs.

**Functional job:** Answer first-session edge case questions on the spot.
**Emotional job:** Feel authoritative rather than exposed.
**Social job:** Demonstrate mastery of the constitution's governance model to skeptical architects.

---

**JTBD-TC-04 — Minimal Viable Adoption Job**

> When a team is under delivery pressure and tells me they cannot commit 3 hours today,
> I want a 15-minute sprint path that demonstrates real value with zero setup,
> So I can establish a foothold for a full adoption session without losing the team entirely.

**Evidence:** NF-03: Steve: *"These teams are completely overwhelmed with work and have no time to make themselves faster."* Steve's data: 9/12 teams adopted but most never completed a governed task — org bandwidth is co-equal to documentation friction as a blocker (VA-01 partially challenged).

**Functional job:** Run a meaningful constitutional demonstration in < 15 minutes.
**Emotional job:** Feel that the session was not wasted even when time is short.
**Social job:** Respect the team's bandwidth constraints and be seen as a practical, not dogmatic, coach.

---

**JTBD-TC-05 — Prompt Template Sharing Job**

> When I'm preparing for an onboarding session or sending a follow-up to a team,
> I want a library of copy-paste-ready Teams prompt templates for each adoption phase,
> So I can give the team something concrete to run without asking them to read documentation first.

**Evidence:** NF-06: Jay Q3 (shares a ready-to-run multi-step prompt); Steve Q3 (sends Teams prompt template for modification). This is the CURRENT primary artifact coaches use — the guide must provide this, not replace it with a web UI.

**Functional job:** Access and share phase-specific prompt templates instantly.
**Emotional job:** Feel efficient — not spending 20 minutes composing a Teams message from scratch.
**Social job:** Appear organized and well-prepared rather than improvising each session.

---

### 2.2 Senior Architect JTBDs (Hypothesis — SC-OBL-2 Pending)

> ⚠️ All Senior Architect JTBDs are HYPOTHESES derived from repository inspection and PROPOSAL.md juror notes. They are NOT evidence-backed. Stage D IA design for the Architect path WILL NOT begin until SC-OBL-2 is satisfied (≥ 2 architect/engineer interviews confirming or revising these JTBDs).

---

**JTBD-SA-01 — Architectural Alignment Evaluation Job (HYPOTHESIS)**

> When I am asked to evaluate whether AI-governed development practices align with our DDD and layered architecture standards,
> I want a structured map of how Hangar AI laws correspond to architectural patterns I already know,
> So I can produce a recommendation without reverse-engineering the entire law file structure.

---

**JTBD-SA-02 — Law Precedence + NN Resolution Job (HYPOTHESIS)**

> When I encounter a situation where two laws appear to conflict, or when I need to determine if a law is non-negotiable,
> I want a clear precedence view that shows law hierarchy, NN status, and amendment authority,
> So I can resolve the conflict without needing to consult a constitution maintainer for every edge case.

---

**JTBD-SA-03 — Amendment Authority Communication Job (HYPOTHESIS)**

> When a team proposes an exception to a non-negotiable law and asks for my approval,
> I want to immediately know what constitutional authority is required to approve or reject the exception,
> So I can give a correct, defensible answer without creating a governance inconsistency.

---

### 2.3 Engineer JTBDs (Deferred — NEXT Slice)

> ⚠️ Engineer path is DEFERRED to NEXT slice per PROPOSAL.md. JTBDs documented for completeness; Stage C validation is not required before Stage D MVP begin.

**JTBD-ENG-01 — First Task Completion Job (DEFERRED)**

> When I've been introduced to the constitution and need to complete my first governed task,
> I want step-by-step instructions on which law applies, what the agent will propose, and what a successful output looks like,
> So I can complete the task without asking my Technical Coach at every step.

**JTBD-ENG-02 — Mid-Task Law Lookup Job (DEFERRED)**

> When I'm mid-implementation and need to verify my approach satisfies a specific constitutional law,
> I want to find the relevant law by keyword in under 30 seconds,
> So I can verify compliance and keep momentum without context-switching out of my work.

**JTBD-ENG-03 — Agent Output Comprehension Job (DEFERRED)**

> When the agent produces a proposal, I want to understand exactly what it proposed and why each law was applied,
> So I can approve it confidently — not blindly accept output I don't understand.

---

## §3. Journey Maps (PRD-3.2)

### Journey Map — Technical Coach (MVP Focus, Evidence-Backed)

| Stage | **1 — FIRST CONTACT** | **2 — ORIENTATION** | **3 — FIRST GOVERNED TASK** | **4 — FOLLOW-UP** | **5 — INDEPENDENT GOVERNANCE** |
|-------|----------------------|--------------------|-----------------------------|-------------------|-------------------------------|
| **Situation** | Coach introduces constitution to new team; session just starting | Team on P1 landing page; selecting their path | Team running first adoption prompt with agent guidance | Coach checks in 1–7 days later; team has questions | Team operates independently; coach in background |
| **Actions** | Coach opens guide URL; team encounters landing page for first time | Coach walks team through P1; team identifies their role | Coach guides team through P3 direct-instruction path; team runs prompt; reviews agent output | Team asks about upgrade path, amendment process; coach answers (or cannot) | Engineers look up laws mid-task; check SDD workflow; file PRs |
| **Touchpoints** | P1 (Landing Page) | P1 persona entry points | P3 (Quick Start — Coach path), Agent, Teams prompt template | P8 (Compliance Checklist), P10 (Amendment), Teams DM | P4 (Laws Reference), P7 (SDD Workflow), P8 (Compliance) |
| **Emotions** | Hopeful; slightly anxious ("will this land?") | Curious; evaluating ("is this actually useful?") | Engaged but uncertain; "what is the agent doing?" moment occurs here | "I want to continue but I'm not sure what to do next" | Coach: "Are they actually using it?" Engineer: "Do I have to do this every time?" |
| **Pain Today** | No single URL; must share multi-step clone instructions via Teams | README has no persona filtering; coach must narrate context manually | P3 doesn't exist; coach improvises; agent comprehension bottleneck kills momentum | Teams adopted but 9/12 never complete a governed task (Steve); no follow-up path | No self-service law reference; law lookup requires grep or reading 1,320-line guide |
| **Opportunity** | P1 opens at single URL; persona-based landing shows immediate value | P1 surfaces the right path instantly for each role | P3 direct-instruction-first (SC-OBL-1) with Agent Role Explainer embedded (NF-02); Teams prompt template included | P3 "What's Next" section + P8 quick-check + P10 amendment reference | P4 searchable law reference + P7 SDD workflow guide + P8 self-check |

---

### Journey Map — Senior Architect (MVP Focus, Hypothesis-Basis)

> ⚠️ Journey map is hypothesis-derived. SC-OBL-2 validation required before Stage D Architect IA design.

| Stage | **1 — EVALUATION REQUEST** | **2 — ARCHITECTURAL REVIEW** | **3 — RECOMMENDATION** | **4 — ONGOING OVERSIGHT** |
|-------|---------------------------|-----------------------------|-----------------------|--------------------------|
| **Situation** | Architect is asked to evaluate AI governance alignment with existing architecture standards | Architect deep-dives into laws, DDD mapping, NN precedence | Architect produces go/no-go recommendation for leadership | Architect monitors ongoing compliance; fields exception requests |
| **Actions** | Opens guide; looks for architectural entry point | Maps laws to known DDD patterns; checks NN precedence; evaluates amendment authority | Writes recommendation; needs one-artifact summary | Reviews exception requests; determines amendment authority |
| **Touchpoints** | P1 (persona entry for Senior Architect), P3 (Architect path) | P3 (Architect path), P2 (Constitutional AI Model Viz), P4 (Laws Reference) | P2 (architectural visualization), P10 (Amendment Process) | P10 (Amendment Process), P4 (Laws Reference) |
| **Emotions** | Skeptical: "Is this real governance or theater?" | Methodical; wants structured evidence; frustrated by manual cross-referencing | Confident (if evidence is there); frustrated (if law-to-DDD map is absent) | Cautious; does not want exceptions creeping in without authority |
| **Pain Today** | P2 is orphaned (CA-03); no architectural entry point in any guide | CA-06: law-to-skill-to-enforcement requires 3+ files; no DDD alignment view | No single artifact presents the constitution's governance authority chain | Amendment process not documented anywhere; constitution maintainer must be consulted |
| **Opportunity** | P1 → P3 Architect path surfaces DDD law-to-pattern mapping immediately | P3 Architect path + P4 law lookup + P2 architectural model = one coherent evaluation path | P2 + P10 combination provides architectural governance communication artifact | P10 amendment process provides self-service authority chain |

---

### Journey Map — Engineer (DEFERRED to NEXT slice)

> Engineer journey map is DEFERRED. Will be authored in NEXT slice Stage C/D cycle when Engineer path is in scope.

---

## §4. Design Constraints (SC-OBL-1 — DA-03 Pivot Resolution)

These constraints are constitutionally binding on Stage D IA design. They are the formal resolution of SC-OBL-1 from `stage-b-evidence.md` §5.1. Stage D IA design WILL NOT produce a P3 wireframe that violates these constraints.

---

### DC-01 — P3 Technical Coach Path: Direct-Instruction-First

**Constraint:** The P3 Technical Coach quick start path MUST lead with explicit, prescriptive step-by-step instructions. The primary interaction model is: "Do this, then do this, then do this."

**Rationale:** DA-03 INVALIDATED (3/4 coaches prefer direct answers for new teams). Steve: *"The Socratic method does not correct people about to fall off a cliff."* Jay: *"I liked using the agent to prompt the student along the way"* — confirms the agent does the Socratic work; the guide should not replicate the agent's role.

**Prohibited in P3 primary flow:** Open-ended questions as the leading interaction ("What do you want to achieve today?"); "Questions to Explore" blocks before the user has completed the first step; implicit navigation without explicit next action.

**Permitted in P3:** Optional "Coaching Notes" sections (clearly marked, collapsed by default) for advanced coaches who want to apply a Socratic layer after the direct path is completed.

---

### DC-02 — P3 Senior Architect Path: Structured Evaluation Checklist

**Constraint:** The P3 Senior Architect path MUST be structured as an evaluation checklist with direct items (e.g., "✅ Check that team has set avatar in AGENTS.md — [link]") not as a discussion guide.

**Rationale:** Architects are evaluating for compliance — they need a checklist, not a conversation. Socratic prompts are appropriate for teaching; architects are assessing, not learning.

---

### DC-03 — Agent Role Explainer: Required on P3

**Constraint:** P3 MUST include an "Agent Role Explainer" section (or dedicated visual element) that answers, per step: "What is the agent doing here? Why is it writing a proposal? What happens next?" This section must precede the "What's Next" section.

**Rationale:** NF-02 (3/4 coaches): agent comprehension is the primary time sink in every session. This is NOT a nice-to-have — it is the single highest-ROI addition to the guide based on all 4 interview responses.

---

### DC-04 — Minimal Viable Adoption Path: Required on P3

**Constraint:** P3 MUST include a "15-Minute Sprint" path visually distinct from the full adoption path. This path delivers the minimum constitutional demonstration for teams with no available time.

**Rationale:** NF-03 (Steve's data): 9/12 teams adopted but most never completed a governed task. Org bandwidth is a co-equal blocker. A full 3-hour path that overwhelmed teams skip entirely produces zero value; a 15-minute path with immediate value creates a foothold for deeper adoption.

---

### DC-05 — Teams Prompt Template Library: Required in Changeset

**Constraint:** The changeset MUST include a `prompt-templates/` directory (or equivalent) containing ready-to-use Teams-deliverable prompt templates per adoption phase. This is NOT a P3 page feature — it is a standalone artifact the guide links to.

**Rationale:** NF-06 (2/4 coaches explicitly): Teams prompts are the CURRENT primary onboarding artifact. The guide must match and enhance the workflow coaches already use, not replace it with a web UI that coaches must then translate back into Teams messages.

---

### DC-06 — Socratic Elements: Scope and Placement

**Constraint:** Socratic coaching prompts (per ENG-1.2 and PROPOSAL.md §3) are PERMITTED ONLY in:
1. Optional "Coaching Notes" sections on P3 (marked clearly as advanced, collapsed by default)
2. P10 (Amendment Process) — returning/advanced users only
3. P8 (Compliance Checklist) — "reflection" section at the end, after all direct steps are complete

Socratic prompts MUST NOT appear as the primary interaction on any page in the MVP (P1 or P3). They MUST NOT precede the direct instruction path on any page.

---

### DC-07 — Human Agency & Adaptive Scope Explainer: Required on P3

**Added:** 2026-05-06 · **Authority:** Stage D amendment per supplemental practitioner evidence (Steve Fraser, post-Stage B field report)

**Constraint:** P3 MUST include a dedicated "How Agentic Workflows Work" section that is **part of the primary flow** (NOT hidden in Coaching Notes). It must appear before or immediately alongside the Full Adoption Path. This section teaches six things in plain English:

1. **Non-determinism.** Constitutional workflows (adoption, legacy rescue, greenfield) are probabilistic guidance systems, not deterministic scripts. The agent reads the constitution and your context, then proposes a path. The same prompt run twice can yield different proposals. This is by design.

2. **You control batch size.** The AI will always propose the full scope it can see. You are not obligated to accept the full proposal. At every gate (APPROVE / OBJECT), you can reduce scope, split the proposal into chunks, or defer sections to a later session. The constitution expects iteration.

3. **Adoption is compositional.** You can adopt the constitution in parts, in any order:
   - Setup + AGENTS.md only → commit → stop
   - Code analysis + recommendations → review → stop
   - SonarQube adoption → run in a future session
   - Product avatar creation → run when the team is ready
   Each part is a valid, complete adoption outcome on its own.

4. **SonarQube gate = no new debt, not zero debt.** The SonarQube constitutional gate enforces: *new code introduced during this changeset must not add new issues*. It does NOT require fixing all pre-existing issues. Large codebases with existing technical debt can adopt constitutionally without first resolving every prior violation.

5. **ENG-3.1 LOC — Open Question (tracked, not yet guidance).** Steve Fraser flagged that the ENG-3.1 line-of-code requirement may cause AI agents to optimise for LOC reduction at the expense of good object design. This concern is noted but requires dedicated law analysis before any coaching guidance can be issued. Workaround prompts MUST NOT appear in the guide until the analysis is complete. See Risk Register R-12.

   > ⚠️ **DC-07 SCOPE EXCLUSION:** Point 5 is a tracked risk item — NOT a prescriptive tip for coaches. Implementers MUST NOT add an ENG-3.1 coaching tip to P3 until R-12 analysis is complete and any required law amendment is jury-ratified.

6. **Bounded context.** You can scope any workflow — legacy rescue, greenfield, adoption — to a single module, package, or bounded context. Running legacy rescue on `com.aa.loyalty.mileage` is a complete, valid run. You do not have to process the entire codebase in one session.

**Rationale:** Steve Fraser (14 adoptions, 12 teams) identified non-determinism and scope misunderstanding as the #1 post-adoption failure mode: *"Teams get a big proposal but what they need is adoption done in smaller chunks so they can do them in sequence iteratively."* This is not a coaching preference — it is a structural cognitive gap that the guide must close at first contact. P9 (Agentic Feedback Loop Guide, LATER slice) is too late; the coach needs this framing before running their first session.

**Prohibited:** Embedding this content only in Coaching Notes or a collapsed `<details>` element. The section must be visible without interaction on page load.

---

## §5. Stage C Evidence Classification (PRD-1.5 ⛔)

| Component | Status | Classification | Rationale |
|-----------|--------|----------------|-----------|
| Persona 1 (Technical Coach) | ✅ EVIDENCE-BACKED | Moderate | 4 interviews; qualitative saturation on key JTBDs; PRD-3.1 exception documented |
| Persona 2 (Senior Architect) | ⚠️ HYPOTHESIS | Weak | 0 interviews; SC-OBL-2 pending; JTBDs are inference-based |
| Persona 3 (Engineer) | ⚠️ DEFERRED | N/A | NEXT slice; not required for Stage D MVP begin |
| Journey Map — Technical Coach | ✅ EVIDENCE-BACKED | Moderate | Pain points and opportunities sourced from 4 interviews |
| Journey Map — Senior Architect | ⚠️ HYPOTHESIS | Weak | Hypothesis-basis; CA-06/CA-03 from repo inspection |
| Design Constraints (SC-OBL-1) | ✅ EVIDENCE-BACKED | Moderate | 3/4 interview data; DA-03 invalidation is strong and consistent |

**MVP classification (P1 + P3 Technical Coach path): MODERATE** — evidence sufficient for Stage D IA design of P3 Coach path.
**Architect path classification: WEAK** — SC-OBL-2 must be satisfied before Stage D Architect IA design.

---

## §6. Stage C Exit Criteria (PRD-2.5 ⛔)

| Criterion | Status | Notes |
|-----------|--------|-------|
| JTBD framing for all personas (T2.3a) | ✅ COMPLETE | §2 above — 5 JTBDs for Coach (evidence-backed); 3 for Architect (hypothesis); 3 for Engineer (deferred) |
| PRD-3.1 interview evidence or exception (T2.3b) | ✅ DOCUMENTED | Coach: 4 interviews + PRD-3.1 exception; Architect: SC-OBL-2 pending; Engineer: deferred |
| Journey maps (T2.3c) | ✅ COMPLETE | §3 above — Coach and Architect journey maps; Engineer deferred |
| Design constraints from DA-03 pivot (SC-OBL-1) | ✅ COMPLETE | §4 above — 6 binding design constraints (DC-01 through DC-06) |
| `stage-c-evidence.md` filed (T2.3d) | ✅ FILED v1.0 | This document |
| Jury deliberation: Stage C (T2.3e) | ⏳ PENDING | 6-person jury on this artifact required before Stage D |

---

## §6.1 Stage D Entry Obligations (Binding per PRD-2.5 ⛔)

### SD-OBL-1 — SC-OBL-2 Completion Before Architect IA Design (ENG-2.3 Vertical Slice Gate)

Stage D IA design for P4 (Laws Reference) and the Architect path of P3 uses a separate vertical slice from the Coach path (per ENG-2.3). The two slices are sequenced as follows:

**Coach path vertical slice (Stage D can begin immediately):**
- P1 (Landing Page) IA design and P3 Coach path IA design may begin as soon as Stage C jury clears.
- No SC-OBL-2 dependency.

**Architect path vertical slice (BLOCKED until SC-OBL-2 is cleared):**
- P3 Architect path IA design and P4 (Laws Reference) IA design WILL NOT produce any deliverable until ALL of the following are satisfied:
  1. ≥ 2 structured interviews with Senior Architects or Engineers completed
  2. Findings confirm or revise JTBD-SA-01, JTBD-SA-02, JTBD-SA-03
  3. Results documented in `stage-c-addendum.md`
  4. `stage-c-addendum.md` jury-validated (Tomás Reyes + Priya Kapoor + Alexandra Pierce minimum)
- If SC-OBL-2 cannot be satisfied before the Coach path Stage D cycle completes, the Architect path is formally deferred to NEXT slice and `stage-c-addendum.md` is filed as a NEXT-slice evidence artifact.

**Non-bypass clause:** No partial Architect IA design deliverable (wireframe, content model, page structure) may be produced speculatively before SC-OBL-2 is cleared, even if labelled as a draft. Speculation without evidence violates PRD-2.3 and PRD-3.1.

### SD-OBL-2 — G5/G6/G7 Jury Approval Before IMPLEMENT

`compliance/threat-model.md`, `compliance/data-classification.md`, and `compliance/risk-register.md` are currently DRAFT status. They MUST receive:
- Tomás Reyes + Alexandra Pierce APPROVE on threat-model.md (ENG-6.1 ⛔)
- Carlos Mendez + Alexandra Pierce APPROVE on data-classification.md and risk-register.md

This must happen before Stage D IMPLEMENT begins, not before Stage D design.

### SD-OBL-3 — Design Constraints Honoured in All IA Artifacts

All Stage D information architecture artifacts (wireframes, page structure, content model) MUST demonstrate compliance with DC-01 through DC-06 (§4 above). Jordan Ellis must review Stage D IA artifacts against these constraints as part of Stage D jury deliberation.

---

## §8. MVP Hypothesis Update (PRD-5.3 — Priya Kapoor OBJECT-C2 Remediation)

### Why the Hypothesis Must Be Updated Here

PROPOSAL.md §2 states the MVP hypothesis:
> *"If we ship P1 + P3, then first-successful-task time will decrease from estimated 45+ minutes (current baseline) to < 20 minutes."*

Stage B interview data (stage-b-evidence.md §3.3) definitively revised the baseline:
- Jay Turpin: 2–3 hours
- Wyatt Sutherland: 1–3 hours
- Kenneth Robinson: 2 hours
- Steve Fraser: most teams never complete a task at all

The 45-minute baseline was an inference-only estimate made at PROPOSAL.md v1.0 before any interviews were conducted. The actual baseline is **1–3 hours**. The < 20-minute target was calibrated against the estimated (wrong) baseline. Stage C JTBD work — which reveals that the primary bottleneck is agent comprehension (NF-02) and org bandwidth (NF-03), not just documentation navigation — further confirms that < 20 minutes was overambitious.

### Revised MVP Hypothesis

**Previous (PROPOSAL.md §2 — outdated):**
> First-successful-task time: < 20 minutes for ≥ 2 of 3 walkthroughs

**Revised (stage-c-evidence.md §8 — authoritative from this point forward):**
> If we ship P1 + P3 (Technical Coach path with Agent Role Explainer, 15-Minute Sprint path, and Teams prompt template library), then first-successful-task time will decrease from the measured baseline of 1–3 hours to **< 60 minutes** for ≥ 2 of 3 facilitator-observed walkthroughs with real adopters.

### Kill-If Criterion Revision

**Previous:** 0 of 3 walkthroughs achieve task time < 20 min  
**Revised:** 0 of 3 walkthroughs achieve task time < 60 min; or 2 of 3 fail the guardrail metric (coach does not misidentify a NN law)

### Required PROPOSAL.md Amendment

This revision requires a formal PROPOSAL.md amendment before Stage D begins. The amendment must update:
- §2 hypothesis table (time target row): `< 20 min` → `< 60 min`
- §2 kill-if criterion: `< 20 min` → `< 60 min`
- §1 MVP Hypothesis paragraph: `45+ minutes` → `1–3 hours (measured)`

**Gate blocker (SD-OBL-4):** The PROPOSAL.md amendment must be jury-validated before Stage F walkthroughs begin. It may be deferred until the end of Stage D, but must complete before Stage E (Metrics Baseline) begins.

---

## §9. Status Log (Updated)

| Date | Action | Status |
|------|--------|--------|
| 2026-05-05 | Stage C began — G3 cleared (commit 521ade7) | ✅ |
| 2026-05-05 | Persona definitions authored (T2.3a/b) | ✅ |
| 2026-05-05 | JTBD framing complete (T2.3a) | ✅ |
| 2026-05-05 | Journey maps authored (T2.3c) | ✅ |
| 2026-05-05 | Design constraints filed (DC-01 through DC-06) | ✅ |
| 2026-05-05 | stage-c-evidence.md v1.0 filed (T2.3d) | ✅ |
| 2026-05-05 | Jury Round 1: 3 APPROVE / 3 OBJECT (Tomás, Priya, Alexandra) | ✅ |
| 2026-05-05 | v1.1 remediation: SD-OBL-1 vertical slice gate strengthened; §8 MVP hypothesis update added | ✅ |
| Next | Jury Round 2 — 6/6 UNANIMOUS APPROVE — Stage D (Coach path) OPEN | ✅ CLEARED |

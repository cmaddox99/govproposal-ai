# Stage D: Solution Exploration — Evidence Artifact

**Changeset:** `build-adoption-guide-2026-001`
**Stage:** D — Solution Exploration (PRD-2.3, PRD-3.2, PRD-3.3, PRD-3.4)
**Authority:** PRD-2.5 ⛔ (Discovery Stage-Gate Law), ENG-2.3 (Vertical Slice Law), PRD-3.3 (User Story Law), PRD-3.4 (Experience Principles Law)
**Status:** v1.2 — 2026-05-06 — JURY-CLEARED. DC-07 amendment ratified 6/6 APPROVE (2 rounds). US-TC-06 added. IMPLEMENT may now begin: P1 then P3 with DC-01 through DC-07 all binding.
**Gate:** Stage D — ✅ CLEARED | SE-OBL-1 gates — ✅ ALL CLEARED (commit 1624648)
**Gate:** Stage C — ✅ CLEARED (2026-05-05, commit — stage-c-evidence.md v1.1 6/6 APPROVE) | Stage E entry — pending Stage D jury APPROVE
**Vertical slice in scope:** Coach path MVP (P1 + P3 Coach path) | Architect path — BLOCKED per SD-OBL-1

---

## Pre-Stage D Gate Verification

| Gate | Requirement | Status |
|------|------------|--------|
| **T2.3e** | Stage C jury-cleared before Stage D begins | ✅ CLEARED — unanimous Round 2, 2026-05-05 |
| **SD-OBL-1** | Architect path IA WILL NOT produce any deliverable until SC-OBL-2 satisfied | ✅ Documented — Architect path is EXPLICITLY excluded from this artifact |
| **SD-OBL-2** | G5/G6/G7 compliance artifact jury APPROVE required before IMPLEMENT | ⏳ PENDING — required before Phase 3 IMPLEMENT, not before Stage D design |
| **SD-OBL-3** | Stage D IA must demonstrate compliance with DC-01 through DC-06 | ✅ Enforced — each page contract references applicable design constraints |

---

## §1. Information Architecture (T2.4a)

### 1.1 Full 10-Page IA — Slice Assignment

The full guide spans 10 pages across three delivery slices. Stage D IA confirms this structure is the right solution to the validated JTBDs.

| Page | Name | Slice | Persona(s) | JTBD(s) Served | Status in this Stage |
|------|------|-------|-----------|----------------|---------------------|
| **P1** | Landing Page | **NOW (MVP)** | All | JTBD-TC-01 (single URL) | ✅ IN SCOPE |
| **P2** | Constitutional AI Model Viz | NOW (existing) | Senior Architect | JTBD-SA-01 | Existing — T3.2 registration only |
| **P3** | Quick Start Guide — Coach path | **NOW (MVP)** | Technical Coach | JTBD-TC-01 through TC-05 | ✅ IN SCOPE |
| **P3** | Quick Start Guide — Architect path | NOW (MVP) | Senior Architect | JTBD-SA-01–03 | ⛔ BLOCKED — SD-OBL-1 |
| **P3** | Quick Start Guide — Engineer path | NEXT | Engineer | JTBD-ENG-01–03 | DEFERRED |
| **P4** | Laws Reference | NEXT | Engineer, Architect | JTBD-ENG-02, SA-02 | DEFERRED — SD-OBL-1 for Architect |
| **P5** | Skills Catalog | NEXT | Engineer, Coach | — | DEFERRED |
| **P6** | Avatar Selection Wizard | NEXT | All | — | DEFERRED |
| **P7** | SDD Workflow Guide | NEXT | Engineer | JTBD-ENG-01 | DEFERRED |
| **P8** | Compliance Checklist | NEXT | Coach, Engineer | JTBD-TC-05 (What's Next) | Referenced from P3 |
| **P9** | Agentic Feedback Loop Guide | LATER | Engineer, Coach | — | DEFERRED |
| **P10** | Amendment Process | LATER | All | JTBD-TC-03, SA-03 | Referenced from P3 |

---

### 1.2 Navigation Model (MVP scope)

```
P1 (Landing Page)
├── → P3 Coach path       [Technical Coach card — MVP]
├── → P3 Architect path   [Senior Architect card — LOCKED, SD-OBL-1]
├── → P3 Engineer path    [Engineer card — LOCKED, NEXT slice]
└── → P2                  [Constitutional AI Model link — existing artifact]

P3 (Quick Start — Coach path)
├── → prompt-templates/   [Teams Prompt Template Library — DC-05]
├── → P8                  [Compliance Checklist — "What's Next" section]
├── → P10                 [Amendment Process — "What's Next" section]
└── → P1                  [Back navigation — footer]

P2 (Constitutional AI Model Viz)
└── → P1                  [Back navigation — T3.2 addition]
```

**Navigation rules:**
- Every page includes a footer with back-navigation to P1
- No page links to an external CDN, font, or resource (ENG-13.1 ⛔)
- LOCKED pages on P1 show a clear "Coming Next" label — not broken links
- All inter-page links use relative paths only

---

### 1.3 Page Structure — P1 (Landing Page)

```
┌─────────────────────────────────────────┐
│ EYEBROW: Hangar AI Constitution         │
│ HERO: Adoption Guide                    │
│ SUBHEAD: Your path to constitutional    │
│          AI governance — by role        │
├─────────────────────────────────────────┤
│ WHAT IS THIS?                           │
│ 2–3 sentence plain-English summary of  │
│ what the constitution is and why it     │
│ matters for engineering teams at AA     │
├─────────────────────────────────────────┤
│ PERSONA SELECTOR (3 cards)              │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ Technical│ │  Senior  │ │ Engineer │ │
│ │  Coach   │ │Architect │ │          │ │
│ │          │ │          │ │          │ │
│ │ [Start →]│ │ Coming   │ │  Coming  │ │
│ │  (ACTIVE)│ │  Next ›  │ │  Next ›  │ │
│ └──────────┘ └──────────┘ └──────────┘ │
│                                         │
│ "Coming Next" card visual spec:         │
│ • Same card dimensions as active card   │
│ • Slightly muted (not greyed-out/broken)│
│ • Shows persona name + 1-line teaser    │
│   e.g. "Evaluate law-to-DDD alignment" │
│ • "Coming Next" badge — positive tone   │
│ • NOT a disabled button; NOT a 404 link │
│ • Clicking shows a tooltip: "This path  │
│   is in progress — Coach path is ready" │
├─────────────────────────────────────────┤
│ WHAT WILL YOU ACCOMPLISH?               │
│ Per-persona outcome preview (1 line ea) │
│ • Coach: Guide a team in 60 min         │
│ • Architect: Evaluate law alignment     │
│ • Engineer: Ship your first governed PR │
├─────────────────────────────────────────┤
│ CONSTITUTIONAL AI MODEL VISUALIZATION   │
│ [Link to P2 → "Explore the Model"]      │
├─────────────────────────────────────────┤
│ FOOTER: Version | Gate status | Source  │
└─────────────────────────────────────────┘
```

> **ENG-2.3 Vertical Slice Compliance (Tomás Reyes OBJECT-D1):** The "Coming Next" card treatment ensures P1 delivers complete, independent value with only the Coach path active. A visitor who arrives at P1 must experience a page that feels intentionally scoped, not broken. "Coming Next" cards communicate momentum and roadmap transparency — they are NOT placeholder UI that implies failure. Implementers must NOT use disabled, greyed-out, or broken-link states for the Architect and Engineer cards in the MVP.

---

### 1.4 Page Structure — P3 (Quick Start — Technical Coach Path)

Ordered by DC-01 (direct-first), DC-03 (Agent Role Explainer), DC-04 (15-Minute Sprint), DC-07 (Human Agency):

```
┌─────────────────────────────────────────┐
│ EYEBROW: Technical Coach Quick Start    │
│ HERO: Your first session in 60 minutes  │
│ WHAT YOU'LL ACCOMPLISH [checklist]      │
│ □ Share a single URL with the team      │
│ □ Run the first constitutional prompt   │
│ □ Answer "what is the agent doing?"     │
├─────────────────────────────────────────┤
│ ⚡ 15-MINUTE SPRINT PATH (DC-04)        │
│ [Visually distinct — colored band]      │
│ Step 1: Open this URL with the team     │
│ Step 2: Copy this prompt → paste Teams  │
│ Step 3: Run the agent — watch together  │
│ [Copy prompt button]                    │
├─────────────────────────────────────────┤
│ 🤖 WHAT IS THE AGENT DOING? (DC-03)    │
│ Expandable per-step explainer:          │
│ • When you run the adoption prompt →    │
│   agent reads the constitution and      │
│   produces a PROPOSAL artifact          │
│ • When the proposal is ready →          │
│   agent waits for your APPROVE/OBJECT   │
│ • When you APPROVE →                    │
│   agent begins IMPLEMENT phase          │
│ [Each step: plain English, no jargon]   │
├─────────────────────────────────────────┤
│ 🧭 HOW AGENTIC WORKFLOWS WORK (DC-07)  │
│ [VISIBLE — NOT COLLAPSED — primary flow]│
│                                         │
│ These are not scripts. You're in charge.│
│                                         │
│ 1. Non-deterministic: same prompt can   │
│    produce different proposals — by     │
│    design. Review before approving.     │
│                                         │
│ 2. You control batch size: the AI sees  │
│    the full scope. You decide how much  │
│    to approve per session. OBJECT to    │
│    reduce scope — the agent will adjust.│
│                                         │
│ 3. Adoption is compositional:           │
│    Setup only → commit → stop ✓         │
│    Code analysis → review → stop ✓      │
│    SonarQube → separate session ✓       │
│    Product avatars → when ready ✓       │
│    Each part is a complete outcome.     │
│                                         │
│ 4. SonarQube gate = no NEW debt,        │
│    not zero debt. Existing violations   │
│    are baseline. Only new code is gated.│
│                                         │
│ 5. ENG-3.1 LOC — OPEN QUESTION        │
│    (R-12 tracked, NOT in guide yet —  │
│    analysis + potential law change     │
│    required before coaching tip added) │
│                                         │
│ 6. Bounded context: scope any workflow  │
│    to ONE module at a time. Run legacy  │
│    rescue on a single package, commit,  │
│    then continue. This is correct use.  │
├─────────────────────────────────────────┤
│ FULL ADOPTION PATH (DC-01 direct steps) │
│ Step 1: Share this URL ──────────────── │
│ Step 2: Run adoption prompt ──────────  │
│   [Copy prompt] → paste into Teams      │
│ Step 3: Review agent proposal together  │
│   • What to look for in the proposal    │
│   • Common questions at this step       │
│ Step 4: Answer expected questions       │
│   • "How do we upgrade?" → [answer]     │
│   • "What is the amendment process?"    │
│     → [answer + link to P10]            │
│   • "How do we handle multiple repos?"  │
│     → [answer]                          │
│ Step 5: What's Next ─────────────────── │
│   • Ask team to complete first task     │
│   • [Link to P8 Compliance Checklist]   │
│   • Schedule follow-up in 1 week        │
├─────────────────────────────────────────┤
│ 📋 TEAMS PROMPT TEMPLATES (DC-05)      │
│ [Link to prompt-templates/ directory]   │
│ Phase 1 — Initial Adoption              │
│ Phase 2 — First Governed Task           │
│ Phase 3 — Follow-up Coaching            │
├─────────────────────────────────────────┤
│ COACHING NOTES (optional, collapsed)    │
│ [DC-06: Socratic content here only]     │
│ • Questions to explore with the team    │
│ • Teaching Loop step references         │
├─────────────────────────────────────────┤
│ FOOTER: ← Back to P1 | Version | Gate  │
└─────────────────────────────────────────┘
```

---

## §2. Page Contracts (T2.4b)

### Page Contract Format (per PROPOSAL.md §5)

Each contract defines: inputs, outputs, law bindings, learning outcome, and design constraint compliance.

---

### Contract P1 — Landing Page

| Field | Value |
|-------|-------|
| **Inputs** | None — this is the entry point (direct URL, no prior page required) |
| **Outputs** | User routed to: P3 Coach path (active) · P3 Architect path (locked) · P3 Engineer path (locked) · P2 (active) |
| **Law bindings** | ENG-13.1 ⛔ (self-contained HTML, zero external deps) · PRD-1.1 (customer-centric: persona cards surface adopter goals, not internal taxonomy) · PRD-3.1 (persona-aware: 3 distinct entry points, not one undifferentiated path) · ENG-13.2 (consistent visual standard across all pages) |
| **Learning outcome** | Adopter identifies their persona and navigates to their entry point in ≤ 2 clicks. Adopter can describe in one sentence what the Hangar AI Constitution is. |
| **Design constraint compliance** | DC-01 applies: P1 must not ask open-ended questions before routing the user. The page presents clear choices; Socratic content is absent from P1 entirely per DC-06. |
| **Freshness** | Manual — P1 embeds `data-registry-version` attribute; CI freshness check flags for review if `laws/index.yaml` version bumps since last render (ENG-11.3) |
| **Acceptance test** | A new engineer who has never seen the constitution can name their role and reach their quick start page in < 2 minutes with zero coaching (Stage F walkthrough metric) |

---

### Contract P3 — Quick Start Guide (Technical Coach Path)

| Field | Value |
|-------|-------|
| **Inputs** | User arrives from P1 Technical Coach card; or direct URL from Teams message / bookmark |
| **Outputs** | (1) Coach has a Teams prompt template copied and ready to paste. (2) Coach can explain agent behavior at each step without consulting AGENT.md. (3) Coach has completed either the 15-Minute Sprint or the Full Adoption Path. (4) Coach knows the follow-up path (P8, P10) for the next session. |
| **Law bindings** | ENG-13.1 ⛔ (self-contained HTML, zero external deps) · ENG-1.2 (pedagogical: teaching loop applied — Guide step is primary; Socratic is optional advanced section per DC-06) · ENG-11.1 ⛔ (Evolutionary Architecture Law — P3 must be designed as an independently shippable and evolvable slice; the Coach path now and the Architect/Engineer paths later must each add value without requiring prior paths to be rebuilt. P3's section structure must not create architectural debt that blocks the Architect path from being added later as a peer section.) · ENG-13.2 (consistent visual standard) · PRD-3.3 (user stories with acceptance criteria govern this page) |
| **Learning outcome** | Coach can guide a team from "never seen the constitution" to "first constitutional prompt complete" in one session. Coach can answer the 4 most common first-session questions (upgrade, amendment, multi-repo, law verification) without consulting any other document. |
| **Design constraint compliance** | DC-01 (direct-first: 15-min sprint and full path both lead with steps, not questions) · DC-03 (Agent Role Explainer required — present before or alongside full path) · DC-04 (15-Minute Sprint visually distinct) · DC-05 (Teams prompt templates accessible within 1 click) · DC-06 (Socratic content in Coaching Notes section only, collapsed by default) · **DC-07 (Human Agency & Adaptive Scope explainer — visible in primary flow, NOT collapsed, before Full Adoption Path section)** |
| **Freshness** | Manual — `data-registry-version` attribute; CI freshness check on law registry version bump |
| **Acceptance test** | A Technical Coach who has never used the guide can complete the 15-Minute Sprint section and run a constitutional adoption prompt with a team in under 15 minutes (Stage F walkthrough metric) |

---

## §3. Experience Principles (T2.4c — PRD-3.4)

Five experience principles govern all design decisions for P1–P10. These principles are the tiebreaker when design choices conflict. Any Stage D jury OBJECT that disputes a design choice must be evaluated against these principles first.

---

**EP-01 — Direct Over Discovery (resolves DC-01)**
> Instructions come first. Exploration is optional and always comes after the first action is complete.

*Application:* Every page leads with "do this." Questions, rationale, and Socratic prompts are available but never block the direct path. A user who never reads the optional sections still accomplishes their job.

---

**EP-02 — Show the Agent, Don't Hide It (resolves NF-02)**
> At every step where the agent acts, the guide explains what it is doing in plain English — before the user has to ask.

*Application:* The Agent Role Explainer on P3 is not a help section — it is part of the primary flow. A coach should never need to say "just trust it" because the guide already answered "why."

---

**EP-03 — One Foothold Before the Mountain (resolves NF-03)**
> Every path offers a 15-minute version before the full version. Teams earn the right to go deeper.

*Application:* The 15-Minute Sprint is the first thing a coach sees on P3, not a footnote. A team that only does the sprint has still accomplished something constitutional.

---

**EP-04 — Coach Tools, Not Coach Replacement**
> The guide gives coaches artifacts they can use directly (URLs, prompt templates, checklists). It does not try to replace the coaching relationship or the agent.

*Application:* DC-05 (Teams Prompt Templates) and DC-03 (Agent Role Explainer) are coach tools. The guide is not a self-service system — it is a force multiplier for coaches who are already doing the work.

---

**EP-05 — Trust Through Transparency**
> Every non-negotiable law is visible, not hidden. The guide never asks an adopter to "just follow the rule" — it shows why the rule exists.

*Application:* Law citations on P3 are human-readable (e.g., "ENG-4.1 ⛔ — Why: untested code is a constitutional violation, not a style preference"). This is what builds AI trust in skeptical teams (VA-01 challenge: docs are secondary to trust).

---

## §4. User Stories (T2.4d — PRD-3.3)

### 4.1 Technical Coach Path — User Stories (MVP, Evidence-Backed)

---

**US-TC-01 — Single URL Onboarding**

```
As a Technical Coach,
I want to share a single URL with a new team that immediately shows them
their constitutional path by role,
So that I can begin an onboarding session without sending a multi-step
Teams setup message.

Acceptance Criteria:
- Given a team member who has never seen the Hangar AI Constitution,
  when they open P1,
  then they can identify their role (Technical Coach, Architect, or Engineer)
  within 10 seconds of the page loading.

- Given they select the Technical Coach path on P1,
  when they click through,
  then they arrive at P3 Coach quick start in ≤ 2 clicks.

- Given P1 is open on a laptop with no internet connection,
  when the page is served from a local or cached source,
  then the page loads completely with no broken assets or external requests
  (ENG-13.1 ⛔ self-contained validation).

Definition of Done:
- [ ] Acceptance criteria verified during Stage F facilitator-observed walkthrough
- [ ] ENG-13.1 compliance confirmed by Alexandra Pierce before ship
- [ ] P1 loads in < 3 seconds on standard AA hardware
```

---

**US-TC-02 — Agent Role Comprehension**

```
As a Technical Coach,
I want a clear, plain-English explanation of what the agent is doing
at each step of the adoption process embedded directly in P3,
So that I can answer "what is the agent doing?" without consulting
AGENT.md or breaking session flow.

Acceptance Criteria:
- Given P3 is open and the Agent Role Explainer section is visible,
  when the team asks "what is the agent doing during the PROPOSE step?",
  then the coach can answer using only P3 — no other file opened.

- Given the Agent Role Explainer for any step on P3,
  when a team member reads it,
  then they can describe the agent's action in their own words after reading
  (verified by coach post-read check — Stage F guardrail metric).

- Given the Agent Role Explainer is implemented,
  when Alexandra Pierce reviews the rendered HTML,
  then it contains zero external links, CDN references, or inline scripts
  that would violate ENG-13.1 ⛔.

Definition of Done:
- [ ] Agent Role Explainer covers: PROPOSE, IMPLEMENT, ARCHIVE steps at minimum
- [ ] Each explainer answers: "What is the agent doing? Why? What comes next?"
- [ ] Verified in Stage F: team member articulates agent's role unprompted
```

---

**US-TC-03 — 15-Minute Sprint Path**

```
As a Technical Coach,
I want a minimal constitutional demonstration path that requires no setup
and completes in under 15 minutes from opening P3,
So that I can deliver immediate value to a time-constrained team and earn
permission for a deeper follow-up session.

Acceptance Criteria:
- Given a team that says "we only have 15 minutes",
  when the coach opens the 15-Minute Sprint section on P3,
  then the team sees at least one agent-generated constitutional output
  before time expires (clock starts when P3 opens).

- Given the 15-Minute Sprint section,
  when a first-time user scans P3,
  then they can locate the sprint path without reading the full page
  (visual distinction: color band or dedicated section header).

- Given the sprint path is followed,
  when the team reaches the end,
  then there are zero prerequisite installation steps that block the demo
  (all prep is pre-done; coach only needs the guide URL and a Copilot license).

Definition of Done:
- [ ] Sprint path tested end-to-end: coach cold-opens P3, completes sprint in < 15 min
- [ ] Sprint path visually distinct (verified: not discoverable only by scrolling)
- [ ] Sprint path works with standard AA engineering laptop + Copilot license only
```

---

**US-TC-04 — Teams Prompt Template Access**

```
As a Technical Coach,
I want to access a copy-paste Teams prompt template for each adoption phase
directly from P3,
So that I can give my team a ready-to-run prompt without composing it from
scratch or switching to another document.

Acceptance Criteria:
- Given P3 is open,
  when the coach needs an adoption phase prompt,
  then a copyable template is accessible within 1 click from P3
  (either on-page or via a clearly labelled link).

- Given the prompt template library is open,
  when the coach scans it,
  then templates are organized by phase (Phase 1 Adoption / Phase 2 First Task /
  Phase 3 Follow-up) and a template can be selected and copied in ≤ 30 seconds.

- Given a template is copied and pasted into a Teams message,
  then it is ready to send with at most 1 labelled substitution
  (e.g., "[REPO_NAME]" clearly marked — never an unlabelled placeholder).

Definition of Done:
- [ ] Templates reviewed by at least 1 Technical Coach before Stage F
- [ ] Each template tested: copy → paste → send produces a valid constitutional prompt
- [ ] Template library accessible offline (self-contained or embedded in P3)
```

---

**US-TC-05 — Follow-Up Path ("What's Next")**

```
As a Technical Coach,
I want P3 to include a "What's Next" section with a concrete follow-up
action for the team after the initial session,
So that the team does not go dormant between sessions and has a clear
next step to take independently.

Acceptance Criteria:
- Given a team has completed the initial adoption session,
  when they open or return to the "What's Next" section of P3,
  then they can identify at least one specific action to take before
  the next coaching check-in.

- Given the "What's Next" section,
  when a team member reads it,
  then they see a link to P8 (Compliance Checklist) with a clear action
  statement (e.g., "Complete the Phase 1 compliance checklist before your
  next session").

- Given the follow-up path is presented at the end of the Full Adoption Path,
  when a Technical Coach reviews it,
  then they confirm it aligns with the verbal follow-up they currently give
  teams at the end of a session (Stage F coaching panel review).

Definition of Done:
- [ ] "What's Next" section reviewed by at least 1 Technical Coach respondent
  from Stage B before Stage F walkthroughs
- [ ] P8 link resolves correctly (relative path, not external URL)
- [ ] Action statement is specific (not generic "learn more" language)
```

---

**US-TC-06 — Human Agency & Adaptive Scope (DC-07)**

**Added:** 2026-05-06 · DC-07 amendment · evidence: Steve Fraser post-Stage B field report

```
As a Technical Coach,
I want P3 to include a plain-English "How Agentic Workflows Work" section
that explains batch control, compositional adoption, and the SonarQube gate
correctly — visible in the primary flow without requiring any click to expand,
So that the coach can frame the team's expectations before the first prompt
runs, eliminating the most common adoption failure modes (over-scoping,
SonarQube panic, LOC thrashing, waiting for a "perfect" first run).

Acceptance Criteria:
- Given a Technical Coach opens P3 for the first time,
  when they scroll to the "How Agentic Workflows Work" section,
  then it is fully visible without any click, toggle, or expand action
  — it is NOT inside a <details> element or behind a tab.

- Given a coach is preparing to run a first adoption session,
  when they read the Adaptive Scope section,
  then they can confidently tell the team: "You don't have to approve the
  full proposal — you can reduce scope at the OBJECT gate."

- Given the SonarQube gate explanation is present on P3,
  when a team member reads it,
  then they understand that the gate enforces "no new issues introduced"
  — NOT "fix all existing issues before adoption can succeed."

- Given the ENG-3.1 LOC coaching tip is present,
  when an engineer reads it,
  then they have a ready-made instruction to paste into their prompt that
  redirects the agent from LOC-numeric-targeting to OO-design-first.

- Given the Bounded Context point is present,
  when a coach reads it,
  then they can justify running legacy rescue on a single package
  as a constitutionally valid, complete outcome — not a partial failure.

Definition of Done:
- [ ] Section is visible-by-default in P3 HTML (no JS toggle required)
- [ ] All 6 DC-07 points are present (non-determinism, batch size,
      compositional adoption, SonarQube gate, bounded context)
- [ ] ENG-3.1 LOC coaching tip is NOT present (R-12 open — tip blocked until law analysis complete)
- [ ] Section reviewed by Steve Fraser or equivalent coach before Stage F
```

---

### 4.2 Senior Architect Path — User Stories (BLOCKED — SD-OBL-1)

> ⚠️ Senior Architect user stories are BLOCKED pending SC-OBL-2 completion (≥ 2 architect/engineer interviews). No Architect path IA design deliverable may be produced until SC-OBL-2 is cleared and `stage-c-addendum.md` is jury-validated. Architect user stories will be authored in the SC-OBL-2 → `stage-c-addendum.md` → Stage D addendum cycle.

---

### 4.3 Engineer Path — User Stories (DEFERRED — NEXT slice)

> Engineer path is NEXT slice per PROPOSAL.md. User stories drafted in stage-c-evidence.md §2.3 for reference; formal PRD-3.3-compliant stories will be authored when the Engineer path enters Stage D in the NEXT slice cycle.

---

## §5. Stage D Exit Criteria (PRD-2.5 ⛔)

| Criterion | Status | Notes |
|-----------|--------|-------|
| Full 10-page IA design documented (T2.4a) | ✅ COMPLETE | §1 above — all 10 pages, slice assignments, navigation model, page structures |
| Page contracts defined for MVP pages (T2.4b) | ✅ COMPLETE | §2 above — P1 and P3 Coach path full contracts |
| Experience principles defined (T2.4c — PRD-3.4) | ✅ COMPLETE | §3 above — EP-01 through EP-05 |
| User stories with AC for Coach path (T2.4d — PRD-3.3) | ✅ COMPLETE | §4 above — US-TC-01 through US-TC-06 (US-TC-06 added 2026-05-06 — DC-07 amendment) |
| Architect/Engineer stories documented as blocked/deferred | ✅ DOCUMENTED | §4.2 and §4.3 — explicit blocking rationale |
| Design constraint compliance demonstrated (SD-OBL-3) | ✅ DEMONSTRATED | Each page contract references DC-01 through DC-06 |
| `stage-d-evidence.md` filed (T2.4e) | ✅ FILED v1.0 | This document |
| Jury deliberation: Stage D (T2.4f) | ⏳ PENDING | 6-person jury on this artifact required before Stage E |

---

## §6. Stage E Entry Obligations (Binding per PRD-2.5 ⛔)

### SE-OBL-1 — Pre-IMPLEMENT Gates Before Stage E / Phase 3

Before IMPLEMENT (Phase 3) begins, the following must be complete:

| Gate | Requirement | Owner | Status |
|------|------------|-------|--------|
| **SD-OBL-2 / G5** | `compliance/threat-model.md` jury-approved (Tomás Reyes + Alexandra Pierce) | Tomás Reyes | ⏳ DRAFT |
| **SD-OBL-2 / G6** | `compliance/data-classification.md` jury-approved (Carlos Mendez + Alexandra Pierce) | Carlos Mendez | ⏳ DRAFT |
| **SD-OBL-2 / G7** | `compliance/risk-register.md` jury-approved (Carlos Mendez + Alexandra Pierce) | Carlos Mendez | ⏳ DRAFT |
| **T3.0** | CI/CD freshness workflow (ENG-11.3) — `.github/workflows/freshness-check.yml` | Jordan Ellis | ⏳ Not started | Jordan Ellis verification (T3.0d): workflow must pass on clean repo state before first HTML commit |
| **T3.1** | SonarQube project provisioned for this changeset | Jordan Ellis | ⏳ Not started | Jordan Ellis verification (T3.1c): Gate G2 PASS confirmation before Phase 3 IMPLEMENT |
| **T3.2** | P2 back-navigation registered (T3.2a–d) | Agent | ⏳ Not started | Jury deliberation required per T3.2d |
| **T3.3** | Vitest + Stryker installed, stub tests wired (ENG-4.1 ⛔) | Jordan Ellis | ⏳ Not started | **⚠️ TDD SEQUENCE (Jordan Ellis OBJECT-D2):** T3.3 stub tests (failing) MUST be created BEFORE any P4 or P6 JavaScript is written. Per ENG-4.1 ⛔ Atomic TDD, the test must exist before the code. Implementers must NOT write P4 search JS or P6 wizard JS until `p4-search.test.js` and `p6-wizard.test.js` stubs exist and `npx vitest run` confirms they fail. Jordan Ellis verifies stub existence at T3.3e before Phase 4 begins. |

### SE-OBL-2 — PROPOSAL.md Amendment Before Stage F

Per §8 of `stage-c-evidence.md`: PROPOSAL.md §2 kill-if criterion (`< 20 min`) must be amended to `< 60 min` before Stage F walkthroughs begin. Jordan Ellis verifies in Stage D jury that the amendment is scheduled before Stage E metrics baseline is set.

### SE-OBL-3 — SC-OBL-2 / SD-OBL-1 Active

Architect path IA and P4 IA remain blocked. No Architect path deliverable may enter Phase 3 IMPLEMENT without SC-OBL-2 → `stage-c-addendum.md` → Stage D addendum jury cycle completing first.

---

## §7. Status Log

| Date | Action | Status |
|------|--------|--------|
| 2026-05-06 | Stage D began — Stage C cleared (stage-c-evidence.md v1.1) | ✅ |
| 2026-05-06 | IA design authored (T2.4a) — full 10-page structure, nav model, P1 and P3 page structures | ✅ |
| 2026-05-06 | Page contracts authored (T2.4b) — P1 and P3 Coach path | ✅ |
| 2026-05-06 | Experience principles authored (T2.4c) — EP-01 through EP-05 | ✅ |
| 2026-05-06 | User stories authored (T2.4d) — US-TC-01 through US-TC-05 with Given/When/Then AC | ✅ |
| 2026-05-06 | stage-d-evidence.md v1.0 filed (T2.4e) | ✅ |
| 2026-05-06 | Jury Round 1: 3 APPROVE / 3 OBJECT (Tomás, Jordan, Alexandra) | ✅ |
| 2026-05-06 | v1.1 remediation: P1 "Coming Next" card spec; SE-OBL-1 TDD sequence note; ENG-11.1 ⛔ rationale | ✅ |
| 2026-05-06 | Jury Round 2: 6/6 UNANIMOUS APPROVE — Stage D CLEARED | ✅ CLEARED |

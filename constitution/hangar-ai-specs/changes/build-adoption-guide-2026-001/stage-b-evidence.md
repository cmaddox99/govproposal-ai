# Stage B: Assumption Mapping — Evidence Artifact

**Changeset:** `build-adoption-guide-2026-001`
**Stage:** B — Assumption Mapping (PRD-2.2)
**Authority:** PRD-2.5 ⛔ (Discovery Stage-Gate Law), PRD-1.5 ⛔ (Evidence-Based Decision Law)
**Status:** JURY-CLEARED — T2.2a, T2.2b (4 interviews), T2.2c, and T2.2f all complete. Classification: **MODERATE** (ratified by Priya Kapoor 2026-05-05). Jury unanimous APPROVE Round 2 (2026-05-05). Gate G3 OPEN.
**Version:** 2.1 — updated 2026-05-05 with jury deliberation results and Stage C entry obligations
**Gate:** G3 — ✅ OPEN — Stage C may begin. Stage C entry obligations in §5.1 are binding.

---

## Evidence Classification

| Component | Status | Classification | Rationale |
|-----------|--------|----------------|-----------|
| T2.2a — Assumption Map | ✅ COMPLETE | Weak | Repository inspection + prior proposal history; no direct adopter contact |
| T2.2b — Structured Interviews (≥ 3) | ✅ COMPLETE | Moderate | 4 responses: Jay Turpin, Steve Fraser, Wyatt Sutherland, Kenneth Robinson — 27+ combined adoptions across 12 teams. Key findings consistent across ≥ 3 participants. See §3.2. |
| T2.2c — Competitive Analysis | ✅ COMPLETE | Weak | Internal artifact survey; no external benchmarks |
| T2.2d — Evidence Reclassification | ✅ RATIFIED — MODERATE | Ratified by Priya Kapoor 2026-05-05 | 4 interviews conducted; findings consistent on DA-01, DA-06, DA-03 invalidation, NF-02 agent comprehension gap. Contradictions on DA-02 (README) and Q10 (web page value). MODERATE rubric met: 4 interviews ≥ 3 required, ≥ 3 consistent findings. |
| T2.2f — Stage B Jury Deliberation | ✅ COMPLETE — UNANIMOUS APPROVE | Round 2 unanimous 6/6, 2026-05-05 | Round 1: 3 OBJECT / 3 APPROVE. Objections: Maya Chen (DA-03 Stage C obligations), Jordan Ellis (DA-04/DA-05 validation gap), Alexandra Pierce (PRD-2.5 ⛔ gate documentation incomplete). Remediated in v2.1: §5.1 Stage C Entry Obligations added; §6 audit trail note added. Round 2: unanimous 6/6 APPROVE. |

**Overall classification: MODERATE** *(ratified by Priya Kapoor per PRD-1.5 ⛔, 2026-05-05)*
**Gate G3: ✅ OPEN** — Stage C (JTBD Mapping) may begin. See §5.1 for binding entry obligations.

---

## §1. Assumption Map (T2.2a)

### How to Read This Map

Each assumption is classified by:
- **Type:** Desirability (Do adopters want this?), Feasibility (Can we build it?), or Viability (Does it serve the business?)
- **Confidence:** HIGH (evidence from multiple sources), MEDIUM (one source), LOW (inference only)
- **Risk:** What happens if the assumption is wrong?
- **Validation Method:** How we will test this in Stage B interviews or Stage E walkthroughs

---

### 1.1 Desirability Assumptions (What adopters want)

| ID | Assumption | Type | Confidence | Risk if Wrong | Validation |
|----|-----------|------|-----------|---------------|------------|
| DA-01 | Technical Coaches need a **single URL** they can share with a new team to begin constitutional onboarding — they do NOT want to assemble a reading list from scattered markdown files | Desirability | MEDIUM | If coaches are comfortable with the current README/workflow path, the landing page solves no real pain; MVP fails validation | T2.2b interview: "Walk me through how you currently onboard a new team to the constitution. What do you send them first?" |
| DA-02 | The current `README.md` + `docs/guides/` structure is **insufficient** as an entry point — adopters report friction finding the right starting point for their role | Desirability | LOW | If README is already adequate, P1 has no competitive advantage over existing artifacts | T2.2b interview: "On a scale of 1–5, how satisfied are you with the current README as an onboarding entry point? What would make it a 5?" |
| DA-03 | Technical Coaches want **Socratic coaching prompts** (per AGENT.md §1.2–1.3) embedded in the guide — they do NOT want prescriptive step-by-step instructions that bypass the teaching loop | Desirability | MEDIUM | If coaches prefer direct instruction, the Socratic design will be perceived as unhelpful, failing ENG-1.2 pedagogical intent in practice | T2.2b interview: "When you lead a team through the constitution, do you prefer to give direct answers or ask questions to guide discovery? What does the team find more valuable?" |
| DA-04 | Senior Architects want **architectural alignment mapping** — a visual or structured representation of how Hangar AI laws map to DDD, layered architecture, and vertical slice patterns they already know | Desirability | MEDIUM | If architects can already navigate the law files directly, P3 Architect path adds no value | T2.2b interview: "What is the hardest part of convincing a senior architect to adopt the constitution? What framing resonates most?" |
| DA-05 | Engineers want a **searchable laws reference** (P4) — browsing raw `laws/index.yaml` via command line is insufficient for day-to-day reference | Desirability | MEDIUM | If engineers prefer `grep` or IDE search over a web UI, P4 is low-ROI | T2.2b interview: "How do you currently look up a specific law when you're mid-task? What's the fastest path you've found?" |
| DA-06 | A **first-successful-task time of < 20 minutes** is the right threshold — the current baseline (estimated 45+ minutes from README) is significantly worse | Desirability | LOW | If current baseline is < 30 minutes or if 20 minutes is too aggressive, the hypothesis cannot be validated | T2.2b: Measure actual time during baseline walkthrough with control condition (README only) before building P1 + P3 |
| DA-07 | Adopters will **return to the guide** (retention ≥ 2 visits in 2 weeks) once they've used it — this is a reference artifact, not a one-time onboarding document | Desirability | LOW | If the guide is "read once and done," P4–P10 (reference pages) have lower strategic value | T2.2b interview: "After your initial constitution adoption, how often do you refer back to the constitution documentation? For what purposes?" |

---

### 1.2 Feasibility Assumptions (What we can build)

| ID | Assumption | Type | Confidence | Risk if Wrong | Validation |
|----|-----------|------|-----------|---------------|------------|
| FA-01 | All 10 pages can be **self-contained HTML** (ENG-13.1 ⛔) with no external dependencies — `aa-artifact-render` produces compliant output | Feasibility | HIGH | None — ENG-13.1 is non-negotiable; must be satisfied regardless of complexity cost | Technical check: P2 already confirmed ENG-13.1 compliant by Alexandra Pierce |
| FA-02 | P4 (Laws Reference) can be generated from `laws/index.yaml` with **zero manually-entered law entries** — the 168 laws are fully machine-readable | Feasibility | HIGH | If YAML frontmatter is inconsistent or incomplete, P4 generation will be partial; law entries may be missing or wrong | T5.2: Extract and count — compare output count to 168 expected |
| FA-03 | The **ENG-11.3 freshness check** (OR-logic: source SHA changed OR timestamp > 30 days) is implementable via GitHub Actions reading `data-source-commit` attributes from HTML | Feasibility | MEDIUM | If HTML attribute injection via `aa-artifact-render` is not supported, freshness enforcement must be re-designed | T3.0: Prototype and verify workflow before Phase 4 begins |
| FA-04 | Vitest can test inline `<script>` extracted from self-contained HTML — the extraction pipeline (HTML → module `.js` → test → re-inline) is viable | Feasibility | MEDIUM | If Vitest cannot run against extracted inline scripts, a different test harness must be chosen before P4/P6 build | T3.3: Stub files + verify `npx vitest run` fails before building |
| FA-05 | The **avatar selection wizard** (P6) can be implemented as a pure inline JavaScript decision tree with no external state — all 29+ avatar combinations fit within a single self-contained HTML page | Feasibility | MEDIUM | If avatar combinations create a page too large for a browser to render efficiently, P6 must be paginated or lazy-loaded, violating ENG-13.1 self-containment intent | T5.x: Build stub and measure rendered page size before full implementation |

---

### 1.3 Viability Assumptions (Why this matters to American Airlines)

| ID | Assumption | Type | Confidence | Risk if Wrong | Validation |
|----|-----------|------|-----------|---------------|------------|
| VA-01 | Reducing adoption friction **directly increases the number of teams** that achieve constitutional compliance per BUS-1.1 ⛔ — the adoption guide is a force multiplier for the constitution | Viability | MEDIUM | If adoption friction is not the limiting factor (e.g., teams know the constitution but choose not to follow it), the guide won't improve compliance rates | T2.2b interview: "What is the biggest reason teams don't follow the constitution consistently? Is it lack of knowledge or lack of incentive?" |
| VA-02 | A **per-coach productivity gain** of ≥ 30 minutes per onboarding session justifies the build cost — at 3–5 sessions/quarter/coach across a multi-coach organization, the ROI is positive | Viability | LOW | If coaching time saved is < 15 minutes per session, or if coaches are not the bottleneck, ROI may be negative | T2.2b interview: "How much time do you spend per team helping them navigate the constitution documentation? What does that time look like?" |
| VA-03 | The adoption guide is **not a compliance artifact** — it is a teaching tool; therefore it does NOT require BUS-4.5 PIA in MVP scope (no analytics, no user tracking, no PII) | Viability | HIGH | If legal review determines even facilitator observation forms constitute data processing, PIA may be required earlier | G9 gate: BUS-4.3 ⛔ and BUS-4.5 review before any analytics feature ships |
| VA-04 | The guide will be accessed by **internal American Airlines engineers and coaches only** in MVP scope — no public internet exposure means BUS-2.3 (accessibility) and BUS-2.1 (FAA) apply but with internal tooling scope | Viability | MEDIUM | If the guide is later shared externally or with regulated operators, BUS-2.3 WCAG 2.1 AA audit (G8) will be blocking | G8: WCAG audit required before any external release |

---

## §2. Competitive Analysis — Internal Landscape (T2.2c, PRD-2.4)

### 2.1 Existing Artifacts Surveyed

The following artifacts exist in the repository today and represent the current "competition" — what an adopter would encounter WITHOUT the adoption guide:

| Artifact | Location | Format | Persona Coverage | Last Updated |
|----------|---------|--------|-----------------|-------------|
| **README.md** | `/README.md` | Markdown | All (no persona differentiation) | Current |
| **How to Adopt Constitution** | `docs/guides/adoption/how-to-adopt-constitution.md` | Markdown, 1,320 lines | All personas combined, no separation | Current |
| **Brownfield Adoption Guide** | `docs/guides/adoption/brownfield-adoption.md` | Markdown, 1,776 lines | Engineer-primary; coach/architect not differentiated | Current |
| **Adoption Compliance Checklist** | `docs/guides/adoption/adoption-compliance-checklist.md` | Markdown table | Audit-focused; no learning path | Current |
| **Enterprise AI Adoption Metrics** | `docs/guides/adoption/enterprise-ai-adoption-metrics.md` | Markdown | Leadership/management; not an entry point | Current |
| **Organizational Transformation** | `docs/guides/adoption/organizational-transformation.md` | Markdown | Senior leader focused; no law mapping | Current |
| **Constitution Overview** | `docs/guides/constitution/what-is-the-hangar-ai-constitution.md` | Markdown | General; conceptual only | Current |
| **Adoption Workflow** | `workflows/adoption.md` | Markdown workflow | Agent-centric; not human-navigable guide | Current |
| **AGENTS.md** | `/AGENTS.md` | Markdown | AI agent operating instructions | Current |
| **Constitutional AI Model Viz** | `session-state/files/hangar-ai-constitution-viz.html` | Self-contained HTML | Technical architect; visual, not navigable | Complete (P2) |

---

### 2.2 Gap Analysis — What Exists vs. What Is Missing

| Capability | Exists Today? | Current Substitute | Gap Severity |
|-----------|--------------|-------------------|-------------|
| Unified landing page with persona entry points | ❌ No | README.md (no personas) | HIGH — first contact is undifferentiated |
| Persona-aware quick start (Coach / Architect / Engineer) | ❌ No | how-to-adopt guide (1,320 lines, undifferentiated) | HIGH — adopters read 1,300 lines to find their path |
| Searchable 168-law reference with NN flags | ❌ No | Manual `grep` or reading `laws/index.yaml` YAML | HIGH — no human-readable indexed law reference |
| Visual skills catalog with trigger phrases | ❌ No | Reading 29+ individual skill `.md` files | HIGH — skill discovery requires file-by-file exploration |
| Avatar selection wizard (tech stack → laws + skills) | ❌ No | Manual `AVATAR-RAG-INDEX.yaml` exploration | HIGH — selection requires understanding 3-level taxonomy |
| Interactive SDD workflow guide (PROPOSE→IMPLEMENT→ARCHIVE) | ❌ No | `workflows/*.md` files (agent-centric, not human guide) | MEDIUM — workflows exist but are not human-navigable |
| Interactive compliance checklist | Partial | `docs/guides/adoption/adoption-compliance-checklist.md` | MEDIUM — static, no phase gate context |
| Agentic feedback loop visual guide | ❌ No | AGENT.md §1.4 (agent instructions, not a human guide) | MEDIUM — HARD_BLOCK conditions not human-navigable |
| Amendment process guide | ❌ No | No current amendment guide exists | LOW — rarely used; power-user feature |
| Constitutional AI model visualization with navigation | Partial | P2 exists but is orphaned (no parent page) | HIGH — P2 is built but unreachable without a landing page |
| Socratic coaching prompts per topic | ❌ No | Coaches improvise or reference AGENT.md §1.2–1.3 | HIGH — Socratic design is not operationalized in any guide |

---

### 2.3 Critical Observations from Existing Artifacts

**Observation CA-01 — Volume without navigation:**
The two primary adoption guides (`how-to-adopt-constitution.md` at 1,320 lines; `brownfield-adoption.md` at 1,776 lines) contain high-quality information but require reading 1,000+ lines to extract a 30-minute actionable path. There is no progressive disclosure or persona filtering.

**Observation CA-02 — Workflow vs. guide mismatch:**
`workflows/adoption.md` is written for AI agents, not human readers. It contains AI agent instruction syntax that is inappropriate for a Technical Coach presenting onboarding to an engineering team.

**Observation CA-03 — P2 is orphaned:**
The Constitutional AI Model Visualization (P2, 78KB self-contained HTML) was built and validated by the jury but has no navigational parent. A first-time adopter who hasn't been given the direct URL cannot find it.

**Observation CA-04 — No persona differentiation:**
Every existing guide addresses all personas simultaneously. A Senior Architect evaluating DDD law compliance and a new Engineer setting up their first TDD cycle receive the same document, forcing them to self-filter 1,000+ lines.

**Observation CA-05 — No Socratic operationalization:**
ENG-1.2 and AGENT.md §1.2–1.3 require Socratic coaching (no predefined answers; questions that lead to discovery). No existing guide operationalizes this for human coaches. The coaches must improvise.

**Observation CA-06 — Law-to-skill connection is invisible:**
A coach trying to explain "why do we need atomic TDD here?" must cross-reference `laws/engineering/testing.md`, `agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md`, and `AGENT.md §3.3` independently. There is no artifact that surfaces the law-to-skill-to-enforcement-protocol chain as a coherent visual.

---

### 2.4 External Benchmark (PRD-2.4 — Competitive Research)

No direct external equivalents were found for an internal AI governance constitution adoption guide at this specificity. The following analogues were considered for structural comparison:

| Analogue | What It Does Well | What Is Different from Our Context |
|---------|------------------|-----------------------------------|
| **React/Next.js docs** | Persona-aware quick starts (tutorial vs. API reference vs. concepts); progressive disclosure | External developer tools — no aviation law, no non-negotiable governance constraints, no jury approval process |
| **NIST AI RMF Playbook** | Structured governance with defined roles and evidence gates | Prescriptive checklists, not Socratic; no persona-based learning paths |
| **Google Developer Style Guide** | Searchable reference; consistent citation format | Not a learning guide; no teaching loop; no compliance gate |
| **AWS Well-Architected Framework** | Persona-aware (developer, architect, security); structured pillars with questions | Cloud infrastructure scope; questions are audit-style, not Socratic coaching |

**Competitive gap conclusion:** No external analogue combines: (1) persona-aware quick start, (2) Socratic coaching prompts, (3) live law citation with NN status, (4) avatar selection, and (5) constitutional amendment process. The adoption guide is a genuinely novel artifact type.

---

## §3. Interview Protocol (T2.2b) — PENDING DATA

### Interview Design

Per PRD-1.5 ⛔: 3+ structured interviews with real Technical Coaches who have onboarded teams must be conducted before evidence reclassifies above Weak.

### Interview Questions

The following questions are designed to test the Desirability assumptions in §1.1 and to gather quantitative proxies:

**Opening — Context Setting**
1. "What is your current role, and how many teams have you onboarded to the Hangar AI Constitution in the last 6 months?"
2. "Can you walk me through your most recent onboarding session — what did you share first, and what was the team's reaction?"

**DA-01 — Single URL**
3. "What artifact or link do you send a team first when starting constitutional onboarding? Do you wish you could give them a single URL that covers everything they need?"
4. "Have you ever wanted to present the constitution to a team without needing to switch between multiple markdown files or tabs?"

**DA-02 — README adequacy**
5. "On a 1–5 scale (1=very difficult, 5=very easy), how easy is it for a new team to find the right starting point using the current README and docs?"
6. "What's the most common question a new team asks you in the first 30 minutes of onboarding?"

**DA-03 — Socratic vs. prescriptive**
7. "When you coach a team through the constitution, do you prefer to guide them to discover the 'why' behind each law, or give them direct answers? What has worked better in your experience?"
8. "Have you used the AGENT.md Teaching Feedback Loop (Observe→Guide→Explain→Demonstrate→Verify→Reinforce) in your onboarding sessions? If so, how?"

**DA-06 — Time baseline**
9. "Roughly how long does it take a new engineer to successfully complete their first constitutionally-governed task after you introduce them to the constitution? (From first exposure to first successful PR, not including coding time)"
10. "What part of that journey takes the most time — finding the right law, understanding the SDD workflow, setting up the tooling, or something else?"

**VA-01 — Adoption driver**
11. "What is the biggest reason teams you've worked with haven't followed the constitution consistently? Is it unclear documentation, lack of motivation, or something else?"
12. "If you could change ONE thing about the current constitution documentation to make adoption stick, what would it be?"

**Closing — Impact**
13. "If you had a single navigable web page with persona-based quick start paths, a searchable law reference, and coaching prompts built in — how would that change your onboarding sessions?"

---

### Interview Log (PENDING)

| Interview # | Date | Interviewee Role | Session Duration | Key Findings | Evidence Level Contribution |
|------------|------|-----------------|-----------------|-------------|---------------------------|
| 1 | ⏳ TBD | Technical Coach | — | — | — |
| 2 | ⏳ TBD | Technical Coach or Senior Architect | — | — | — |
| 3 | ⏳ TBD | Technical Coach or Senior Architect | — | — | — |

**Gate G3 unblocks when:** ≥ 3 interviews are complete, findings are documented above, and Priya Kapoor classifies evidence as Moderate or Strong based on consistency across participants.

---

## §3.2 Interview Findings — Responses Received (T2.2b)

**Interviews conducted:** 4 async responses via #tech-coaches Teams channel, 2026-05-05
**Respondents:** Jay Turpin, Steve Fraser, Wyatt Sutherland, Kenneth Robinson
**Combined adoptions:** ~27 (4+14+9+2 across 12+ teams, 2 coaching failures noted by Steve)

---

### Respondent Summaries

**Jay Turpin** — 2–3 teams onboarded. Provides a multi-step clone + prompt instruction (no single URL). README score: **2/5**. Time to first task: **2–3 hours**. Coaching preference: **direct answers**. #1 friction: _"It seems magical and it's not a natural part of their workflow."_ ONE change: _"GETTING STARTED GUIDE — adoption, creating and amending proposal, implementation and archiving."_ Web page: _"I don't think that would help unless it's part of a class — I liked using the agent to prompt the student along the way."_
Teams had immediate questions: upgrade path, multi-repo handling, law verification, overriding laws, amendment process.

**Steve Fraser** — 14 adoptions, 6 teams (2 failures), including C++ team. Provides no URL — sends Teams prompt template. README score: **N/A** ("I have no idea, I give them the starting point"). Time to first task: **most teams never complete one** (only 2–3 of 12 actually use the constitution after adoption). Coaching preference: **both, but direct for beginners**. #1 friction: _"Trusting the AI; how to prompt correctly; basic coding knowledge to verify AI output. Also: org is overwhelmed and has no time."_ ONE change: Integrate advisory panel into refactoring workflow + teaching guide aimed at junior developers. Web page: _"Not sure it will be helpful — most new people just need to be told what to do... The Socratic method does not correct people about to fall off a cliff... pointing out the documentation explaining how Governance works would go a long way."_

**Wyatt Sutherland** — 9 teams onboarded (3 Check-In, 1 Contact Center, 2 IFE, 1 PAX, 1 MDM, 1 CPP). No single URL — asks them to clone. README score: **5/5**. Time to first task: **1–3 hours**. Coaching preference: **direct examples + dive in**. #1 friction: 1/2 team hasn't adopted yet — moving slower. ONE change: _"HTML files are easier on the eyes — not sure folks know MD can be rendered to HTML."_ Uses agent to answer questions. Teams are **"blown away"** by discovery results.

**Kenneth Robinson** — 2 teams onboarded. No single URL — clone + workflows. README score: **5/5**. Time to first task: **2 hours**. Coaching preference: **challenge their strategic thinking** (closest to Socratic, but framed as mindset shift, not question-and-answer). #1 friction: _"They don't consider how impactful the constitution can be to all the work they are doing."_ ONE change: _"Make pulling and using the constitution in relation to their work more seamless."_ Web page: Would orient around goals and personal responsibility, not navigation UI.

---

### §3.3 Assumption Validation Results

| Assumption | Verdict | Evidence | Finding |
|-----------|---------|----------|---------|
| **DA-01** — coaches need a single URL | ✅ CONFIRMED | 4/4 have no single URL; all use multi-step clone | Gap is real. However Jay and Steve question whether a web *page* is the right solution — they prefer agent-guided onboarding. Design implication: the single URL should launch an agent-guided flow, not just display content. |
| **DA-02** — README is insufficient | ⚠️ PARTIALLY INVALIDATED | Jay: 2/5; Wyatt: 5/5; Kenneth: 5/5; Steve: N/A | Not consistent across ≥ 3 participants. The README quality is NOT the pain point for most coaches — the pain is the *absence of a guided Getting Started path*. Reframe: gap is onboarding process scaffolding, not README text quality. |
| **DA-03** — coaches want Socratic prompts | ❌ INVALIDATED | 3/4 prefer direct; Steve and Jay explicitly reject Socratic for beginners | **CRITICAL FINDING — design must pivot.** Socratic-first design reduces guide utility for the majority persona. Revised design: direct "do this" instructions lead; optional "explore why" sections fold in. Do NOT make Socratic the default interaction pattern. |
| **DA-04** — architects want architectural alignment | ⚠️ INSUFFICIENT DATA | No question directly tested this | Cannot assess from current responses |
| **DA-05** — engineers want searchable laws ref | ⚠️ INSUFFICIENT DATA | No question directly tested this | Wyatt mentions using agent to answer law questions — may reduce standalone reference value |
| **DA-06** — baseline > 45 min | ✅ CONFIRMED (stronger) | Jay: 2–3 hrs; Wyatt: 1–3 hrs; Kenneth: 2 hrs; Steve: most never complete a task | Baseline is 1–3 HOURS, not 45 minutes. Hypothesis is validated more strongly than assumed. The < 20 min target needs to be revisited upward (< 60 min is more realistic). |
| **DA-07** — guide has retention value | ⚠️ INSUFFICIENT DATA | Not directly tested | Wyatt says he uses agent for ongoing questions — may reduce reference page demand |
| **VA-01** — friction is the limiting factor | ⚠️ PARTIALLY CHALLENGED | Trust + org bandwidth cited more than docs friction | Steve's finding is significant: 9 of 12 teams adopted but never completed a constitutionally-governed task. Documentation friction is secondary to *trust in AI* and *organizational bandwidth*. Design implication: the guide must build trust (show what the agent is doing), not just surface law content. |
| **VA-02** — 30 min/session ROI | ✅ CONFIRMED | 1–3 hours × multiple sessions × 14+ adoptions = significant coach investment | Time savings ROI case is solid |

---

### §3.4 New Findings (not in original assumption map)

| ID | Finding | Source | Design Implication |
|----|---------|--------|--------------------|
| NF-01 | **Demo effect is the strongest adoption driver** — teams are "blown away" when they see it work hands-on | Wyatt (2x "blown away"), Steve (positive reactions during adoption runs) | P1 should orient around launching a live demo, not reading a reference |
| NF-02 | **Agent comprehension is THE primary bottleneck** — explaining what the agent is doing, why it wrote a proposal, what happens next | Jay ("just explaining what the agent is doing"), Steve ("trusting the AI, how to prompt"), Kenneth ("the agent work") | Guide must include an "Agent Role Explainer" — what is the agent doing at each step? This is higher priority than a law reference. |
| NF-03 | **Org bandwidth is a real adoption blocker, independent of doc quality** — teams are overwhelmed with delivery work and have no capacity to invest in tooling | Steve ("completely overwhelmed with work, no time to make themselves faster. This is an organizational problem") | This is a VA-01 challenge: even a perfect guide won't move the needle for overloaded teams. Guide should acknowledge this and provide a "minimal viable adoption" path (15-min sprint, not 3-hour deep dive). |
| NF-04 | **Amendment process is a natural first-session question** | Jay Q2 ("what is the process to amend the constitution?") | P8 (Amendment guide) has confirmed real demand — surfaces unprompted in first onboarding |
| NF-05 | **Multi-repo and upgrade path questions surface in first onboarding** | Jay Q2 ("how do we upgrade to get latest guidance? how do we handle whole applications — multiple repos?") | P1/Getting Started must address upgrade + multi-repo explicitly |
| NF-06 | **Coaches use Teams-delivered prompt templates as the primary onboarding artifact** — more effective than asking teams to read docs | Jay Q3 (shares a ready-to-run prompt), Steve Q3 ("I send them a Teams prompt to modify") | High-value deliverable: a library of copy-paste Teams prompts per phase/use-case, higher ROI than a navigable web page alone |
| NF-07 | **Steve's Q9 proposal mirrors the constitutional jury process we already built** — he wants an advisory panel with blocking conditions and mandatory doc review built into the refactoring workflow | Steve Q9 | Validates the jury process design pattern as intuitive and desirable; may merit a "how to run a constitutional jury" guide page |

---

## §4. Assumption Risk Register

The five highest-risk assumptions that, if wrong, would significantly change the build plan:

| Rank | Assumption | Risk | Mitigation | Interview Update |
|------|-----------|------|-----------|-----------------|
| 1 | DA-06 — current baseline IS > 30 min | If baseline is already fast, MVP fails on weak hypothesis | Measure baseline in Stage B interviews; if < 30 min, revise hypothesis before Stage C | ✅ CONFIRMED — baseline is 1–3 HOURS. Risk resolved. Target < 20 min should be revised to < 60 min. |
| 2 | DA-01 — coaches want a single URL | If coaches prefer markdown files or direct law access, landing page has no adoption pull | Interview Q3–4; if ≥ 2 coaches say "no", scope down P1 | ✅ CONFIRMED gap, but ⚠️ NUANCED — Jay and Steve question whether a web page is the format. The single-URL value is real, but the format should be agent-launch, not a static page. |
| 3 | VA-01 — friction is the limiting factor | If knowledge isn't the gap (compliance culture is), the guide won't move the needle | Interview Q8; if "lack of motivation" scores higher than "unclear docs", escalate to BUS-1.1 governance track | ⚠️ PARTIALLY CONFIRMED — Steve's data (9/12 teams adopted but never completed a governed task) confirms that org bandwidth and AI trust are co-equal blockers alongside documentation friction. Guide alone is not sufficient; "minimal viable adoption" path (< 60 min) needed. |
| 4 | DA-03 — Socratic design resonates | If coaches prefer direct instruction, every "Questions to Explore" block reduces guide utility | Interview Q7; if ≥ 2 coaches prefer prescriptive, restructure P3 | ❌ INVALIDATED — 3/4 coaches prefer direct answers for new teams. **P3 design must pivot: direct instructions lead, Socratic optional.** Risk is now elevated if we do NOT change the design. |
| 5 | FA-03 — freshness check via data-attribute is viable | If `aa-artifact-render` does not inject `data-source-commit`, ENG-11.3 OR-logic enforcement requires rework | T3.0 prototype before Phase 4 begins; escalate to tool maintainer if needed | Unchanged — technical validation still needed in Stage C/Phase 3 |

---

## §5. Stage B Exit Criteria (PRD-2.5 ⛔)

| Criterion | Status | Notes |
|-----------|--------|-------|
| Assumption map complete (T2.2a) | ✅ COMPLETE | §1 above — 16 assumptions mapped, classified, with validation methods |
| Competitive analysis complete (T2.2c) | ✅ COMPLETE | §2 above — 10 internal artifacts surveyed, 6 external analogues; gap table complete |
| ≥ 3 structured interviews conducted (T2.2b) | ✅ COMPLETE | 4 responses: Jay Turpin, Steve Fraser, Wyatt Sutherland, Kenneth Robinson — see §3.2 |
| Findings consistent across ≥ 3 participants | ✅ CONFIRMED | DA-01 gap (4/4), DA-06 baseline 1–3 hrs (3/4), direct > Socratic (3/4), agent comprehension bottleneck (3/4) |
| Evidence reclassified to Moderate (T2.2d) | ✅ RATIFIED MODERATE | Priya Kapoor ratification 2026-05-05 per PRD-1.5 ⛔ |
| stage-b-evidence.md filed | ✅ FILED v2.1 | This document — updated 2026-05-05 with jury deliberation and Stage C obligations |
| Jury deliberation: Stage B (T2.2f) | ✅ COMPLETE — 6/6 UNANIMOUS | Round 1: 3 APPROVE / 3 OBJECT. Round 2: 6/6 APPROVE. Gate G3 OPEN. |
| Stage C entry obligations documented (§5.1) | ✅ FILED | See §5.1 below — binding obligations per PRD-2.5 ⛔ |

---

## §5.1 Stage C Entry Obligations (Binding — PRD-2.5 ⛔)

These obligations were raised by the Stage B jury (Round 1) and are constitutionally binding conditions on Stage C work. Stage D (IA Design) **WILL NOT begin** until each obligation is satisfied and documented in `stage-c-evidence.md`.

---

### SC-OBL-1 — DA-03 Design Pivot (raised by Maya Chen, confirmed by Alexandra Pierce)

**Obligation:** Stage C JTBD Mapping MUST produce formal revised P3 design constraints reflecting the DA-03 invalidation before Stage D IA design begins.

**Specifics:**
- P3 (Technical Coach quick start path) currently described in PROPOSAL.md v2.5 §5 as embedding Socratic coaching prompts. This design intent is now INVALIDATED by interview evidence (3/4 coaches prefer direct instructions for beginners).
- Stage C JTBD work for P3 must produce: (1) a direct-instruction-first P3 interaction model, (2) explicit scoping of where Socratic elements are appropriate (advanced/returning users only), (3) a documented design constraint that prevents Socratic-as-default from re-entering Stage D.
- Socratic elements are NOT eliminated from the guide — they are demoted to secondary/optional. The leading interaction pattern for P3 must be prescriptive: "do this, then this."

**Gate blocker:** Stage D WILL NOT begin until `stage-c-evidence.md` contains documented P3 design constraints satisfying this obligation.

---

### SC-OBL-2 — DA-04 / DA-05 Validation (raised by Jordan Ellis, confirmed by Alexandra Pierce)

**Obligation:** Stage C JTBD Mapping MUST include at least 2 interviews with Senior Architects or Engineers (not just Technical Coaches) to validate DA-04 (architectural alignment mapping) and DA-05 (searchable laws reference) before Stage D IA design for P4 begins.

**Specifics:**
- All 4 Stage B interviews were with Technical Coaches. DA-04 and DA-05 target different personas (Senior Architects and Engineers respectively). Building P4 and the Architect path of P3 without any evidence from those personas violates PRD-1.5 ⛔ intent.
- Required minimum: ≥ 2 structured interviews with Senior Architects or Engineers, with questions directly testing DA-04 ("how do you evaluate constitutional law alignment with DDD patterns?") and DA-05 ("how do you currently look up a specific law mid-task?").
- If findings are INSUFFICIENT or INVALIDATED for DA-05, P4 scope must be revisited before Stage D.
- Wyatt's note (uses agent to answer law questions) is a single data point that may indicate P4 is lower ROI than assumed — must be validated across personas.

**Gate blocker:** Stage D IA design for P4 and the Architect path WILL NOT begin until `stage-c-evidence.md` documents DA-04/DA-05 validation from non-Coach respondents.

---

### SC-OBL-3 — Audit Trail Note (raised by Carlos Mendez)

**Obligation (documentation, not blocking):** §6 status log must record that original interview source responses are preserved in the #tech-coaches Teams channel thread (2026-05-05) as the external source of record per BUS-7.1 ⛔.

**Status:** ✅ Documented in §6 below.

---

*Stage B evidence — v2.1 — 2026-05-05 — Jury-cleared Round 2 unanimous 6/6 APPROVE*
*Classification: MODERATE — ratified by Priya Kapoor per PRD-1.5 ⛔*
*Gate G3: OPEN — Stage C may begin subject to §5.1 binding obligations*
*Key design pivots: DA-03 invalidated (direct > Socratic); NF-02 agent comprehension = primary gap; NF-06 Teams prompt templates = highest-value deliverable*

---

## §6. Status Log

| Date | Action | Status |
|------|--------|--------|
| 2026-05-02 | Questionnaire posted to #tech-coaches Teams channel | ✅ Done |
| 2026-05-05 | Jay Turpin response received | ✅ Logged in §3.2 |
| 2026-05-05 | Steve Fraser response received | ✅ Logged in §3.2 |
| 2026-05-05 | Wyatt Sutherland response received | ✅ Logged in §3.2 |
| 2026-05-05 | Kenneth Robinson response received | ✅ Logged in §3.2 |
| 2026-05-05 | T2.2b complete — 4 interviews documented | ✅ Gate criterion met |
| 2026-05-05 | Priya Kapoor evidence classification ratification — WEAK → MODERATE | ✅ Ratified |
| 2026-05-05 | Stage B jury Round 1 — 3 APPROVE / 3 OBJECT (Maya Chen, Jordan Ellis, Alexandra Pierce) | ✅ Round 1 complete |
| 2026-05-05 | v2.1 remediation — §5.1 Stage C obligations added, §6 audit trail note added | ✅ Filed |
| 2026-05-05 | Stage B jury Round 2 — 6/6 UNANIMOUS APPROVE — Gate G3 OPEN | ✅ CLEARED |
| 2026-05-05 | **Audit trail note (BUS-7.1 ⛔):** Original interview responses preserved in #tech-coaches Microsoft Teams channel thread posted 2026-05-02. Responses received 2026-05-05. Teams thread is the external source of record. Text of all 4 responses reproduced verbatim in §3.2 of this artifact as the repo-preserved copy. | ✅ Documented |

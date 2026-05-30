---
type: proposal
title: "Hangar AI Workshop Catalog — Learning Hub Publication"
status: PROPOSED
spec_id: LHW-001
triggered_by: "Strategic initiative to scale constitutional AI adoption across American Airlines engineering teams via self-service Learning Hub curriculum"
scope: "Four workshops covering the full Hangar AI Constitution workflow portfolio: Greenfield Development, Legacy Rescue (2 parts), Avatar Workflow, and Product Discovery"
laws_applied:
  - ENG-13.1
  - ENG-11.1
  - ENG-10.1
  - BUS-7.1
  - PRD-2.5
owners:
  - The Hangar AI Team
audience:
  - Engineering Managers
  - Senior Developers
  - Architects
  - Product Managers
  - AI Platform Leads
---

# Hangar AI Workshop Catalog — Learning Hub Publication

## 1. Problem Statement

The Hangar AI Constitution defines a complete governed SDLC — from greenfield development through legacy rescue, product discovery, and the creation of constitutional avatars. Engineering teams know it exists; far fewer know how to apply it. The gap is not documentation — the constitution is comprehensive. The gap is **lived experience**: developers need to build the muscle memory of constitutional AI-assisted development before they can apply it on their own codebases.

Learning Hub workshops are the primary path to closing that gap at scale. They are self-service: a developer can enroll, complete a workshop on their own schedule with their AI coding agent as the guide, and emerge with durable artifacts committed to a real repository. No instructor required. No scheduled cohort. No waiting.

This proposal defines the four-workshop curriculum that covers the complete constitutional workflow portfolio, establishes the course details, learning outcomes, and positioning for each, and submits the catalog for ensemble deliberation before Learning Hub publication.

---

## 2. The Four Workshops

### Workshop 1 — Greenfield Development: Agentic SDLC in Practice

**Course ID:** HAW-GF-001  
**Duration:** 1 part · 3 hours  
**Format:** Self-service · AI-agent orchestrated · Hands-on  
**Audience:** Developers, engineers, hands-on practitioners building new systems

#### Course Description

You are starting a new system. You have an AI coding agent and an empty repository. Without a constitution, your agent will generate code that works today and breaks tomorrow — inconsistent quality, no test coverage, no law citations, no audit trail.

This workshop changes that. In three hours you adopt the Hangar AI Constitution, select the product and technology avatars that match your domain, generate a formal constitutional proposal with vertical slices and BDD acceptance criteria, and then implement your first working feature using Atomic TDD — where your AI agent enforces the RED → GREEN → REFACTOR → VERIFY → COMMIT cycle at every step.

You leave with a working implementation, not a slide deck.

#### What You Will Learn

- How the Authority Hierarchy works: Constitution Laws → Agent Skills → Project Extensions — and why the constitution is never overridden
- How to adopt the constitution against any new repository in under 15 minutes (`AGENTS.md`, `hangar-ai-specs/`, `aa-constitution-lint`)
- How to select the right **product avatar** (Loyalty, Cargo, Booking, Crew Scheduling, and 13 others) and **technology avatar** (Python/FastAPI, Java/Spring Boot, React/TypeScript, and 30 others) for your system
- How to generate a constitutional **proposal** with design rationale, BDD acceptance criteria, and vertical slice breakdown — all traced to law
- How to implement 2–3 vertical slices using **Atomic TDD** with your AI agent as a teaching partner, not a code factory
- How to verify compliance: `aa-constitution-lint`, 90%+ test coverage, no unaddressed constitutional violations

#### What You Will Leave With

| Artifact | Description |
|----------|-------------|
| `AGENTS.md` | Constitutional binding document activating law and avatars for your AI agent |
| `hangar-ai-specs/changes/[spec-id]/PROPOSAL.md` | Full constitutional proposal for your feature |
| `openspec/` | BDD specifications and vertical slice definitions |
| Working implementation | 2–3 implemented slices with tests, coverage, and compliance |
| `evidence/adoption-verified.md` | Linter gate PASS — your constitutional compliance record |

#### What Makes This Workshop Different

This workshop is orchestrated entirely by your AI coding agent. You give it one prompt. It guides you through every phase, enforces the constitutional cycle, and refuses to let you skip gates. The experience is not reading about constitutional development — it is doing constitutional development, with the constitution enforced live.

---

### Workshop 2 — Legacy Rescue: Governed Transformation of Production Systems

**Course ID:** HAW-LR-001  
**Duration:** 2 parts · 3 hours each · 6 hours total  
**Format:** Self-service (or facilitated cohort) · AI-agent paired · Hands-on  
**Audience:** Developers and engineers managing or inheriting legacy codebases with compliance debt

#### Course Description

You have inherited a legacy system. The SonarQube dashboard is red. Coverage is at 4%. There are security hotspots that nobody has touched in years. The compliance debt is real, but you do not know where to start or whether to refactor versus rewrite.

This workshop gives you the complete governed rescue playbook across two sessions. In Session 1 you adopt the constitution, analyze the AAdvantage Loyalty Platform — an intentionally messy but bounded multi-module system — map every violation to a law ID, deliberate with your AI agent on the refactor-versus-rewrite decision for each bounded context, and file a formal ADR. You end Session 1 mid-refactor, gate still failing.

In Session 2 you close the refactor track (gate passes), complete the rewrite track on a second module, and finish with both SonarQube dashboards showing green. You then walk through the Application Guide — the take-home playbook for applying the same method to your own system.

#### Session 1: Decide and Start (3 hours)

| Time | Activity |
|------|----------|
| 0:05–0:15 | Phase 0: Constitutional Adoption — adopt against the sample codebase; linter gate PASS |
| 0:15–0:30 | SonarQube baseline — bring up the platform, run the full scan, inspect the violation inventory |
| 0:30–1:10 | Decision track — archaeology, bounded context mapping, violation classification, four-perspective deliberation with your AI agent, governed ADR |
| 1:10–2:00 | Refactor track begins — characterization tests lock existing behaviour before any change |
| 2:10–3:00 | Compliance remediation — PII handling, complexity reduction, security fixes; Session 1 ends here, gate still failing |

#### Session 2: Gate Passes and Application (3 hours)

| Time | Activity |
|------|----------|
| 0:00–0:30 | Close the refactor — cover the remaining gap; `make gate-tiers` → PASS |
| 0:30–1:20 | Rewrite track — behavioral spec extraction, contract tests, governed TDD rebuild |
| 1:30–2:20 | Rewrite track — security remediation, parity validation, `make gate-accrual` → PASS |
| 2:30–3:00 | Application Guide walkthrough — identify your first target module on your own codebase; cohort close |

#### What You Will Learn

- How to classify a legacy codebase using constitutional law IDs — not intuition
- How to map violations to bounded contexts and build an archaeology report that law citations make reviewable
- How to run a structured **four-perspective deliberation** (correctness, security, complexity, testability) with your AI agent to produce a refactor-versus-rewrite verdict
- How to write characterization tests that lock existing behaviour before touching a single line of production code (ENG-4.3)
- How to execute the full **refactor track**: remediate in priority order (Security → Correctness → Reliability), one violation per commit, gate at every phase
- How to execute the full **rewrite track**: extract behavioral spec, set up parity tests, TDD rebuild under constitutional constraints
- How to drive a failing SonarQube gate (4% coverage, multiple blockers) to a full gate pass in a single session

#### What You Will Leave With

| Artifact | Description |
|----------|-------------|
| Refactored module | Fully remediated loyalty-tiers with `gate-tiers` PASS |
| Rewritten module | Governed TDD rebuild of loyalty-accrual with `gate-accrual` PASS |
| Decision ADR | Formal Architecture Decision Record with law citations and bounded context rationale |
| `sonarqube-delta.md` | Before/after compliance evidence comparing baseline to gate pass |
| `adoption-verified.md` | Constitutional lint PASS evidence |
| Application Guide | Take-home playbook for running the same rescue on your own system |

---

### Workshop 3 — Avatar Workflow: Building the Constitutional AI for Your Domain

**Course ID:** HAW-AW-001  
**Duration:** 1 part · 3 hours  
**Format:** Self-service · AI-agent orchestrated · Hands-on  
**Audience:** Senior developers, architects, platform engineers, and team leads who are responsible for configuring constitutional AI for their team's domain

#### Course Description

Avatars are the constitutional AI's domain intelligence. When you tell your AI agent you are working on Loyalty, or that you are building in Java/Spring Boot, the constitution activates the right laws, the right constraints, and the right behavioral expectations for that context. That intelligence lives in avatars — and avatars must be created, validated, and kept current.

This workshop teaches you the complete avatar lifecycle. You work with the constitutional avatar schema, generate or assess a product-type avatar and a technology avatar for a real domain, run RAG validation to verify that your AI agent can actually retrieve the right guidance, enrich the avatar from codebase evidence, and commit a fully compliant avatar that will serve your team from that day forward.

When you finish, your team's AI agents have a domain-specific operating context — not generic advice, but constitutional intelligence shaped to your technology stack and product domain.

#### What You Will Learn

- What avatars are and why they exist: the difference between a constitution (universal laws) and an avatar (domain-specific application of those laws)
- The **five avatar lifecycle operations**: Generate, Assess, Correct, Validate, Enrich — and when each is invoked
- How to read the avatar schema and understand every field: persona definitions, law bindings, technology constraints, example outputs
- How to **generate a new avatar** from scratch using constitutional guidelines, for both a product-type domain and a technology stack
- How to **assess an existing avatar** for compliance gaps: missing law bindings, stale technology references, thin persona definitions
- How to run **RAG validation** (`aa-rag-eval`) to verify that your AI agent retrieves the correct avatar context for domain-specific queries — and how to interpret the pass/fail threshold
- How to **enrich an avatar from a real codebase**: pull existing patterns, domain objects, and architectural decisions into the avatar so it reflects how your team actually builds
- How the avatar registry (`AVATAR-RAG-INDEX.yaml`) works and how to register your avatar for global retrieval

#### What You Will Leave With

| Artifact | Description |
|----------|-------------|
| New or corrected product avatar | Fully schema-compliant domain avatar with personas, law bindings, and domain guidance |
| New or corrected technology avatar | Stack-specific avatar with constraints, patterns, and constitutional guardrails |
| RAG validation report | Evidence that the AI agent retrieves the correct avatar at the right confidence threshold |
| Codebase enrichment evidence | Structured patterns extracted from a real codebase committed into the avatar |
| `AVATAR-RAG-INDEX.yaml` registration | Your avatar discoverable by any agent working in this domain |

---

### Workshop 4 — Product Discovery: Stage A through F with Constitutional AI

**Course ID:** HAW-PD-001  
**Duration:** 1 part · 3 hours  
**Format:** Self-service · AI-agent orchestrated · Hands-on  
**Audience:** Product managers, engineers, business analysts, and product teams initiating new product initiatives under constitutional governance

#### Course Description

Product decisions made without evidence are the most expensive mistakes an engineering organisation makes. Features get built for users who do not exist. Problems get solved that nobody had. Metrics get defined after the build — which means they always confirm the conclusion.

The Hangar AI Constitution defines a six-stage discovery process (Stages A through F) that prevents this. Each stage has a constitutional gate. You cannot move to Stage B without Stage A evidence committed. You cannot file an implementation proposal without Stage E metrics locked. The gates are enforced by your AI agent — not by a meeting, not by a calendar, not by goodwill.

This workshop walks you through all six stages using a real product scenario drawn from the American Airlines domain. You will generate evidence artifacts at each stage, your AI agent will enforce the gate criteria, and you will close Stage F with a formal, constitutionally compliant implementation proposal that is ready to hand to an engineering team.

#### The Six Stages

| Stage | Name | Constitutional Gate |
|-------|------|-------------------|
| A | Initialize | Problem statement approved; `hangar-ai-specs/changes/[discovery-id]/` scaffolded |
| B | Public Field Study | ≥3 validated user insights; competitive landscape documented |
| C | Code Evidence | Evidence report in `hangar-ai-specs/`; no unreviewed critical findings |
| D | Internal Validation | All blockers resolved; DVFT assumption matrix complete |
| E | Metric Rebaseline | Metrics spec in `hangar-ai-specs/specs/`; PMF targets confirmed |
| F | Roadmap Lock | Roadmap approved; implementation proposal scaffolded; audit event logged |

#### What You Will Learn

- Why sequential, gated discovery eliminates the most common causes of failed product initiatives — and what constitutional law makes this non-negotiable (PRD-2.5)
- How to activate the right **product avatar** for your discovery scenario and how the avatar shapes every evidence artifact your AI agent produces
- How to conduct a constitutionally governed **Stage B field study**: user interview synthesis, JTBD framing, competitive analysis mapped to law
- How to commission and interpret **Stage C code evidence**: codebase archaeology, domain model extraction, and tech debt inventory as product signal
- How to run **Stage D internal validation**: assumption mapping, blocker classification, and the DVFT (Desirability / Viability / Feasibility / Testability) matrix
- How to define **Stage E success metrics** with baselines, PMF targets, and measurability confirmation — all committed as durable evidence
- How to write a **Stage F implementation proposal** that vertical slice teams can execute without ambiguity — with law citations, personas, and BDD acceptance criteria embedded

#### What You Will Leave With

| Artifact | Description |
|----------|-------------|
| Stage A–F evidence chain | All six stage evidence artifacts committed to `hangar-ai-specs/` as a durable discovery record |
| `hangar-ai-specs/changes/[discovery-id]/PROPOSAL.md` | Constitutional proposal covering background, scope, laws applied, and vertical slice plan |
| DVFT assumption matrix | Stage D internal validation record with all blockers resolved |
| Metrics spec | Stage E success metrics with baselines and PMF targets |
| Roadmap | Now/Next/Later outcome roadmap with vertical slices defined |
| Audit event | BUS-7.1-compliant discovery record for governance and compliance purposes |

---

## 3. Workshop Sequencing and Learning Path

The workshops are self-contained — a learner can take any single workshop and extract full value. However, there is a natural progression for teams building constitutional AI fluency from scratch:

```
Recommended Learning Path
─────────────────────────
Start here if you are new to the constitution:

  [1] Greenfield Workshop (HAW-GF-001)
      └─ Builds constitutional foundation: adoption, avatars, TDD cycle

  [2] Legacy Rescue Workshop (HAW-LR-001, Parts 1 + 2)
      └─ Applies constitutional workflow to the hardest real-world case

  [3] Avatar Workflow Workshop (HAW-AW-001)
      └─ Teaches teams how to configure constitutional AI for their domain

  [4] Product Discovery Workshop (HAW-PD-001)
      └─ Closes the loop: product evidence → implementation proposal → engineering team

All four workshops together = complete constitutional SDLC fluency
Total time investment: 12 hours across 4 workshops
```

---

## 4. Self-Service Mechanics

All four workshops are designed to be completed without an instructor. The mechanics that make this work:

| Mechanism | How It Works |
|-----------|-------------|
| **AI agent as orchestrator** | Learner gives a single bootstrap prompt; the agent reads the workshop guide and drives the entire experience |
| **Constitutional lint as gate** | `aa-constitution-lint` runs at every phase — the agent enforces exit criteria, not self-report |
| **Sample codebases** | Pre-built, intentionally messy codebases (AAdvantage Loyalty Platform) give every learner the same starting state |
| **Session output isolation** | All learner work goes into `session-output/` — prevents contamination of workshop materials |
| **Durable artifacts** | Every workshop produces committed artifacts — learners have evidence of completion, not just memory |
| **Application Guide** | Every workshop closes with a take-home guide for applying the same workflow to the learner's own system |

---

## 5. Laws Applied

| Law ID | Title | Relevance |
|--------|-------|-----------|
| ENG-13.1 | Artifact Rendering Standard | All workshop governance artifacts rendered as HTML with citation tooltips |
| ENG-11.1 | SDD Lifecycle Governance | Workshops teach and demonstrate the governed SDD lifecycle |
| ENG-10.1 | Constitutional Compliance Verification | `aa-constitution-lint` as exit gate in every workshop |
| ENG-4.1 | Atomic TDD | RED → GREEN → REFACTOR cycle enforced in Greenfield and Legacy Rescue workshops |
| ENG-4.3 | Characterization Testing | Characterization-first approach in Legacy Rescue refactor track |
| BUS-7.1 | Audit Trail | All workshop evidence artifacts form a durable audit trail |
| PRD-2.5 | Sequential Stage Gates | Product Discovery stages enforced sequentially, no skipping |

---

## 6. Acceptance Criteria

- [ ] Each workshop has a Learning Hub course page with title, description, duration, audience, and outcomes
- [ ] Each workshop is accessible via a single URL from Learning Hub
- [ ] Self-service mechanics verified: AI agent can complete each workshop without an instructor
- [ ] All four workshops produce the defined evidence artifacts in the learner's repository
- [ ] Ensemble deliberation completed and verdict recorded — APPROVED before publication
- [ ] `aa-artifact-render` used to produce HTML version of this proposal and the deliberation record

---

## 7. Open Questions for Ensemble Deliberation

1. **Legacy Rescue positioning:** Should the two sessions be purchasable/enrollable separately, or only as a pair? A learner completing only Session 1 has incomplete artifacts.
2. **Prerequisite enforcement:** Should the learning path be recommended-only, or should the Learning Hub gate Avatar Workflow behind Greenfield completion?
3. **Avatar Workshop audience split:** The avatar workshop serves both practitioners (who generate avatars) and consumers (who use avatars). Should there be two tracks, or is the single track sufficient?
4. **Product Discovery audience:** Product managers typically do not operate AI coding agents. Is the self-service format appropriate, or does the Product Discovery workshop need a facilitated variant?
5. **Certification:** Should completion of all four workshops yield a recognisable certification or badge on Learning Hub? What does the evidence artifact chain constitute as proof?

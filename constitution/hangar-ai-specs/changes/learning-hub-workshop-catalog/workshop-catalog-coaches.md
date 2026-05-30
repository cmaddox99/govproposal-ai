---
type: evidence
title: "Hangar AI Workshop Program — Course Catalog for Technical Coaches"
status: CURRENT
confidence: High
date: 2026-04-10
authors:
  - The Hangar AI Team
audience:
  - Technical Coaches
  - Engineering Managers
  - Learning & Development Leads
---

# Hangar AI Workshop Program
## Course Catalog for Technical Coaches

This document describes the four workshops that make up the Hangar AI Workshop Program. It is intended for technical coaches sharing the program with engineering teams and leadership.

---

## Program Overview

The Hangar AI Workshop Program is a four-workshop self-service curriculum that covers the complete Hangar AI Constitution workflow portfolio. Each workshop is hands-on: participants work through a real codebase with an AI coding agent as their guide, and leave with committed artifacts — not just notes.

| # | Workshop | Course ID | Duration | Format |
|---|----------|-----------|----------|--------|
| 1 | Greenfield Development: Agentic SDLC in Practice | HAW-GF-001 | 1 part · 3 hours | Self-service |
| 2 | Legacy Rescue: Governed Transformation of Production Systems | HAW-LR-001 | 2 parts · 6 hours | Self-service |
| 3 | Avatar Workflow: Designing Constitutional AI for Your Domain | HAW-AW-001 | 1 part · 3 hours | Self-service |
| 4 | Product Discovery: Constitutional Evidence-Based Discovery | HAW-PD-001 | 1 part · 3 hours | Self-service |

**Total program:** 4 workshops · 15 hours · Complete constitutional SDLC fluency

### Recommended Learning Path

For teams new to the Hangar AI Constitution, the recommended progression is:

```
 [1] Greenfield (3h)  →  [2] Legacy Rescue (6h)  →  [3] Avatar Workflow (3h)  →  [4] Product Discovery (3h)
  Build the foundation      Apply to the hardest         Configure AI for            Close the loop:
  adoption, avatars,        real-world case              your own domain             evidence → proposal
  TDD cycle
```

All four workshops are **self-contained** — a team can start with any single workshop and extract full value. The learning path is a recommendation, not a hard requirement.

---

## Workshop 1 — Greenfield Development: Agentic SDLC in Practice

**Course ID:** HAW-GF-001 · **Duration:** 3 hours · **Audience:** Developers, engineers building new systems

### Description

You are starting a new system. You have an AI coding agent and an empty repository. Without a constitution, your agent will generate code that works today and breaks tomorrow — inconsistent quality, no test coverage, no law citations, no audit trail.

This workshop changes that. In three hours, participants adopt the Hangar AI Constitution, select the product and technology avatars that match their domain, generate a formal constitutional proposal, and implement their first working feature using Atomic TDD — where the AI agent enforces the RED → GREEN → REFACTOR → VERIFY → COMMIT cycle at every step.

Participants leave with a working implementation, not a slide deck.

### What Participants Will Learn

- How the Hangar AI Constitution's Authority Hierarchy works — and why it is never overridden
- How to adopt the constitution against any new repository in under 15 minutes
- How to select the right **product avatar** (Loyalty, Cargo, Booking, Crew Scheduling, and 13 others) and **technology avatar** (Python/FastAPI, Java/Spring Boot, React/TypeScript, and 30 others)
- How to generate a constitutional **proposal** with design rationale, BDD acceptance criteria, and vertical slice breakdown — all traced to law
- How to implement 2–3 vertical slices using **Atomic TDD** with the AI agent as a teaching partner
- How to verify compliance: `aa-constitution-lint`, 90%+ test coverage, no unaddressed violations

### What Participants Will Leave With

| Artifact | What It Is |
|----------|-----------|
| `AGENTS.md` | Constitutional binding document — activates law and avatars for the AI agent |
| `PROPOSAL.md` | Full constitutional proposal with BDD acceptance criteria |
| Working implementation | 2–3 implemented slices with tests, coverage, and compliance |
| `adoption-verified.md` | Constitution linter gate PASS — the completion credential |

### Who Should Attend

- Software engineers and developers building new services or features
- Technical leads establishing engineering standards for a new team
- Engineers who have heard about the Hangar AI Constitution but haven't applied it yet
- Anyone whose AI agent currently produces code without constitutional governance

---

## Workshop 2 — Legacy Rescue: Governed Transformation of Production Systems

**Course ID:** HAW-LR-001 · **Duration:** 2 sessions × 3 hours · **Audience:** Developers and leads working with production legacy codebases

### Description

Most codebases are not new. They have accumulated years of technical debt, inconsistent patterns, missing tests, and architectural decisions made before the Hangar AI Constitution existed. Legacy Rescue teaches the governed approach to transforming these systems — without breaking them.

The workshop uses a pre-built codebase (`loyalty-service-legacy`) — an intentionally messy production-style system with failing SonarQube gates, absent tests, and mixed architectural concerns. Participants work through it in two sessions, each with a clear constitutional gate before proceeding.

**Session 1 (3h) — Characterization:** Inspect the codebase, surface violations with law citations, and commit characterization tests that document current behaviour. No changes to production logic.

**Session 2 (3h) — Transformation:** Choose the constitutional track (Refactor or Rewrite), implement the transformation using the governed workflow, and verify that all gates pass on the transformed system.

### What Participants Will Learn

- How to surface architecture and code quality violations using the constitution's inspection workflow
- What characterization tests are, why they come first, and how to write them against an unfamiliar codebase
- How to choose between the **Refactor track** (preserve structure, improve quality) and the **Rewrite track** (constitutional rebuild with parity tests)
- How to apply **Atomic TDD** in the context of transformation — not just greenfield development
- How to produce a governed transformation proposal that a team can execute without ambiguity

### What Participants Will Leave With

| Artifact | What It Is |
|----------|-----------|
| Characterization test suite | Tests documenting current behaviour, committed before any changes |
| `PROPOSAL.md` | Transformation proposal: violations catalogued, track selected, slices defined |
| Transformed codebase | Refactored or rewritten system with improved test coverage and lint gate PASS |
| `refactor-plan.md` or `rewrite-plan.md` | Governing document for the transformation track chosen |

### Who Should Attend

- Developers who own or maintain legacy production services
- Technical leads planning a rescue or modernisation initiative
- Architects evaluating whether to refactor or rewrite a system
- Teams where SonarQube gates are currently failing

> **Note for coaches:** Sessions 1 and 2 are delivered as a single enrollment. Participants may take a break between sessions — their work is preserved in the repository.

---

## Workshop 3 — Avatar Workflow: Designing Constitutional AI for Your Domain

**Course ID:** HAW-AW-001 · **Duration:** 3 hours · **Audience:** Platform engineers, architects, and AI tooling leads (builders); any developer using avatars (consumers)

### Description

Avatars are the mechanism by which the Hangar AI Constitution is made domain-specific. A product avatar knows the business context of its domain — Loyalty, Cargo, Crew Scheduling. A technology avatar knows the engineering patterns of its stack — Python/FastAPI, Java/Spring Boot, React/TypeScript. Together, they give the AI agent the focused expertise to produce constitutionally governed, domain-correct output on the first attempt.

This workshop teaches both sides of the avatar lifecycle: how to **design and register** new avatars (for platform engineers and architects building the platform), and how to **invoke and verify** existing avatars correctly (for developers using the platform every day).

### What Participants Will Learn

**For avatar builders:**
- How to design a product or technology avatar: domain scope, law citations, trigger phrases, and constitutional constraints
- How to register an avatar in the AVATAR-RAG-INDEX and pass the constitution linter
- How to test RAG routing: verifying that the right avatar activates for the right prompt

**For avatar consumers:**
- How to reference avatars in `AGENTS.md` and what behaviours they activate in the AI agent
- How to verify that an avatar has activated correctly before beginning implementation
- How to debug avatar misfires and escalate via the constitution's review workflow

### What Participants Will Leave With

| Artifact | What It Is |
|----------|-----------|
| New avatar registration | Product or technology avatar registered and lint-verified (builders) |
| Updated `AGENTS.md` | Correct avatar bindings for the participant's domain (consumers) |
| RAG routing test cases | Verification that the avatar routes correctly under representative prompts |
| Constitutional review record | Evidence artifact documenting the avatar lifecycle review |

### Who Should Attend

**Builders:** Platform engineers building or extending the Hangar AI Constitution avatar catalog; architects defining domain-specific constitutional constraints

**Consumers:** Any developer using the Hangar AI Constitution who wants to understand how to get the most accurate and domain-appropriate output from their AI agent

---

## Workshop 4 — Product Discovery: Constitutional Evidence-Based Discovery

**Course ID:** HAW-PD-001 · **Duration:** 3 hours · **Audience:** Technical product managers, product-minded senior engineers, and architects conducting pre-initiative discovery

### Description

The Hangar AI Constitution's Product Discovery workflow defines six sequential stages (A through F) that must be completed before any implementation proposal is approved. Each stage gates the next — no skipping. This is not bureaucracy; it is the mechanism that eliminates the most common cause of failed product initiatives: building before understanding.

This workshop teaches participants to conduct a constitutionally governed discovery from start to finish, using a provided sample initiative as the working scenario. Every stage produces a committed evidence artifact. By the end, participants have a complete Stage A–F evidence chain and an implementation proposal that engineering teams can execute without ambiguity.

### What Participants Will Learn

- Why sequential, gated discovery eliminates the most common causes of failed initiatives — and what constitutional law makes this non-negotiable
- How to conduct a **Stage B field study**: user interview synthesis, Jobs-to-be-Done framing, competitive analysis mapped to law
- How to commission and interpret **Stage C code evidence**: codebase archaeology, domain model extraction, and tech debt inventory as product signal
- How to run **Stage D internal validation**: assumption mapping, blocker classification, and the DVFT (Desirability / Viability / Feasibility / Testability) matrix
- How to define **Stage E success metrics** with baselines, PMF targets, and measurability confirmation
- How to write a **Stage F implementation proposal** that vertical slice teams can execute without ambiguity

### What Participants Will Leave With

| Artifact | What It Is |
|----------|-----------|
| Stage A–F evidence chain | All six stage evidence artifacts committed as a durable discovery record |
| `PROPOSAL.md` | Constitutional implementation proposal with law citations, personas, and BDD acceptance criteria |
| DVFT assumption matrix | Internal validation record with all blockers resolved |
| Metrics spec | Stage E success metrics with baselines and PMF targets |

### Who Should Attend

- Technical product managers working on initiatives that will be implemented by AI-assisted engineering teams
- Senior engineers and architects conducting discovery for major features or system redesigns
- Anyone responsible for translating product intent into engineering proposals

> **Note for coaches:** A facilitated variant designed for non-technical product managers is on the roadmap. The current self-service format is best suited to technical practitioners.

---

## Self-Service Mechanics

All four workshops are designed to be completed by a developer and their AI coding agent — no instructor required, no scheduled cohort, no waiting.

| Mechanism | How It Works |
|-----------|-------------|
| **AI agent as orchestrator** | Participant gives a single bootstrap prompt; the agent reads the workshop guide and drives the entire session |
| **Constitutional lint as gate** | `aa-constitution-lint` runs at every phase boundary — the agent enforces the exit criteria |
| **Sample codebases** | Pre-built, intentionally realistic codebases give every participant the same starting state |
| **Session isolation** | All participant work goes into `session-output/` — no contamination of workshop materials |
| **Durable artifacts** | Every workshop produces committed evidence artifacts — proof of completion, not just memory |
| **Application Guide** | Every workshop closes with a take-home guide for applying the same workflow to the participant's own system |

---

## Certification

Completion of all four workshops, combined with the submission of one real-codebase `adoption-verified.md` artifact (not from the workshop sample codebase), earns the **Hangar AI Constitutional Fluency** credential on the Learning Hub.

This distinguishes practitioners who have applied the constitution to real work from those who have completed the exercises alone.

---

## For Coaches: Sharing This Program

When introducing this program to an engineering team or leadership group, the recommended framing is:

1. **Start with the problem** — most teams using AI coding agents today have no constitutional governance. Code is produced fast, but it degrades fast too. The workshops are the path to closing that gap.

2. **Lead with Workshop 1** — the greenfield workshop is the lowest barrier to entry and the fastest path to a constitutional win. Three hours, one AI agent, one working feature, fully governed.

3. **Use the artifact chain as the sell** — every workshop produces committed evidence. Engineers leave with something in the repository, not just something in their head. That is a fundamentally different learning model.

4. **For legacy teams, Workshop 2 is the anchor** — most engineers work on production systems, not greenfield. Legacy Rescue speaks directly to their day-to-day reality.

5. **Certification is the capstone** — the Hangar AI Constitutional Fluency credential gives teams a shared, referenceable milestone to work toward together.

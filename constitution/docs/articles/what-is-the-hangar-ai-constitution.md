# What Is the Hangar AI Constitution?

> A governance framework for AI-assisted software development at American Airlines

**Date:** 2026-03-05  
**Author:** The Hangar AI Team  
**Related:** [README](../../README.md) | [How to Adopt](../guides/adoption/how-to-adopt-constitution.md)

---

## Executive Summary

The **AA Hangar AI Constitution** is a comprehensive governance framework that establishes the laws, guardrails, and best practices governing how AI agents operate at American Airlines—both in *how* teams build software and *what* they build for customers.

It is **not a tool**. It is a **system of principles** encoded as structured documents that any AI assistant (GitHub Copilot, Cursor, Claude, etc.) can read and follow. Think of it like a constitution for a country: it sets the supreme law of the land that all other rules must respect.

---

## Why It Exists

Modern AI coding assistants are powerful, but without guardrails they produce inconsistent results. Two engineers using the same AI tool can get very different quality outputs. The Constitution solves this by making the rules explicit, teachable, and non-negotiable.

```
┌─────────────────────────────────────────────────────────────────┐
│  Without a Constitution           With a Constitution           │
│  ─────────────────────            ──────────────────            │
│  "It depends on context"          "Test-first. Period."         │
│  Quality varies by person         Quality is consistent         │
│  Knowledge in people's heads      Knowledge in skill files      │
│  AI makes ad-hoc decisions        AI follows explicit laws      │
└─────────────────────────────────────────────────────────────────┘
```

The result: **consistent, high-quality, auditable AI-assisted development** across every team at American Airlines.

---

## The Three Constitutions

Effective AI governance requires laws across three dimensions. Each constitution answers a different question:

| Constitution | Question | Scope |
|---|---|---|
| **Engineering** | **HOW** do we build? | Code quality, testing, architecture, DevOps |
| **Product** | **WHAT** do we build? | User journeys, metrics, accessibility, experimentation |
| **Business** | **WHY** and under what constraints? | Compliance, domain rules, data governance, aviation regulations |

### Engineering Constitution

The Engineering Constitution governs the technical craft of building software. Its most important law is the **Atomic TDD Law (ENG-4.1)**: every change to production code must be driven by a failing test. No exceptions.

Key engineering principles include:

- **8-Step Atomic TDD Cycle** — RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT
- **Test Pyramid** — 70–80% unit tests, 15–25% integration tests, 5–10% end-to-end tests
- **Code Quality Thresholds** — cyclomatic complexity ≤ 10, test coverage ≥ 90%, method length ≤ 20 lines
- **Vertical Slice Development** — ship thin, end-to-end increments rather than horizontal layers

### Product Constitution

The Product Constitution ensures teams build things that matter to users. Its core principle is **Problem-First (PRD-1.2)**: no feature may be built without a clearly defined user problem.

Key product principles include:

- Every feature traces to a user problem, not a solution request
- Success metrics must be defined before implementation begins
- Accessibility is non-negotiable (WCAG 2.1 AA minimum)
- Experimentation (A/B testing) governs uncertain outcomes

### Business Constitution

The Business Constitution ensures software operates safely and legally within American Airlines' highly regulated environment.

Key business principles include:

- **Aviation compliance** — FAA Part 121, DO-178C (airborne software), DO-326A (airborne cybersecurity), TSA, DOT consumer protection
- **Data governance** — PII follows privacy-by-design; audit trails for all financial transactions
- **Priority hierarchy (BUS-1.1)** — Legal compliance always comes first, with no exceptions

---

## The Constitutional Hierarchy

Laws are applied in layers, from universal principles down to specific contexts:

```
┌─────────────────────────────────────────────────────────────────┐
│                      BASE CONSTITUTIONS                         │
│           Engineering + Product + Business Laws                 │
│                (Apply to ALL AA software)                       │
├─────────────────────────────────────────────────────────────────┤
│                     INDUSTRY ADOPTION                           │
│              Aviation: FAA, DO-178C, TSA, DOT                   │
│           (Aviation-specific compliance requirements)           │
├─────────────────────────────────────────────────────────────────┤
│                    PRODUCT-TYPE ADOPTION                        │
│      Booking | Cargo | Loyalty | Operations | Service           │
│              (Domain-specific patterns & rules)                 │
├─────────────────────────────────────────────────────────────────┤
│                    TECHNOLOGY ADOPTION                          │
│          Java/Spring | React | Python | .NET | etc.             │
│               (Stack-specific implementations)                  │
└─────────────────────────────────────────────────────────────────┘
```

A lower layer can *extend* an upper layer but can **never override** it. An engineering team's project-specific rules cannot contradict the base Engineering Constitution.

---

## How It Works in Practice

### Avatars: Context-Specific Guidance

Because American Airlines builds software in many different technology stacks and product domains, the Constitution uses **avatars** to apply universal laws in specific contexts:

- **Technology Avatars** — Java/Spring Boot, React/TypeScript, Python/FastAPI, .NET Core, and more. Each provides stack-specific patterns that satisfy the base laws.
- **Industry Avatar** — The aviation/FAA adoption adds regulatory requirements on top of the base laws for all AA software.
- **Product-Type Avatars** — Passenger Booking, Cargo & Freight, Loyalty (AAdvantage), Airport Operations, Check-In & Travel, and Customer Service each have their own domain-specific rules.

### Agent Skills: Reusable Capabilities

The Constitution ships with **29 agent skills** organized across five domains:

| Domain | Examples |
|---|---|
| Development Practices | Atomic TDD, Vertical Slice Dev, Code Review |
| Discovery & Research | User Journey Mapping, Spec Governance |
| Product Planning | Roadmapping, Executable Spec |
| Platform Engineering | DevOps, infrastructure patterns |
| ML/AI | Model governance, AI safety guardrails |

An AI agent invokes a skill by reading its structured Markdown file. The skill defines the procedure step-by-step, citing the laws it implements. This keeps the agent's behavior consistent and auditable.

### The Spec-Driven Development (SDD) Lifecycle

The Constitution operationalizes a full software development lifecycle:

```
Discovery → Specification → Planning → Implementation → Review → Deployment
    ↑                                                              |
    └──────────────────── Feedback Loop ───────────────────────────┘
```

Each phase has one or more skills that guide the AI agent through it. Specifications are written before code; tests are written before implementation; reviews check Constitutional compliance.

---

## What It Is Not

| Misconception | Reality |
|---|---|
| "It's a plugin or extension" | It's a set of documents—readable by any AI tool |
| "It only applies to GitHub Copilot" | It's portable: Copilot, Cursor, Claude, ChatGPT, etc. |
| "It slows teams down" | It eliminates ambiguity, which accelerates consistent delivery |
| "It replaces engineering judgment" | It encodes engineering judgment so it can be reused |
| "It's just a style guide" | It's a governance framework with non-negotiable laws |

---

## Non-Negotiable Laws

These laws require executive approval to amend and may never be overridden by project-level rules:

| Law | Description |
|---|---|
| ENG-4.1 | Atomic TDD — all code changes must follow RED-GREEN-REFACTOR |
| ENG-6.1 | Security by Design — security is built in, not bolted on |
| ENG-6.4 | Data Protection — PII and sensitive data handled by design |
| ENG-6.7 | Audit Trail — all significant actions are logged and traceable |
| PRD-1.2 | Problem-First — no feature without a defined user problem |
| PRD-5.1 | MVP Law — ship the minimum viable product, learn, iterate |
| BUS-1.1 | Priority Hierarchy — Legal compliance always comes first |
| BUS-7.1 | Business Audit Trail — financial and compliance actions logged |
| BUS-9.3 | Breach Notification — security incidents reported per regulation |

---

## Quick Reference: Getting Started

### For Engineers
1. Read the three base law sets: [Engineering](../../laws/engineering/), [Product](../../laws/product/), [Business](../../laws/business/)
2. Study the [Atomic TDD Skill](../../agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md)
3. Review your [product domain adoption](../../avatars/product-type/)

### For AI Agents
1. Load [AGENT.md](../../agent-skills/base/AGENT.md) — establishes persona and guardrails
2. Apply all three law sets as the authority hierarchy
3. Apply the technology avatar for your stack (e.g., [Java/Spring](../../avatars/technology/java-spring/))
4. Apply the product-type adoption for your domain
5. Cite laws when enforcing them (e.g., "Per ENG-4.1...")

### For New Projects
1. Initialize the Hangar SDD structure using the [Spec Governance Skill](../../agent-skills/skills-by-domain/discovery-research/spec-governance.md)
2. Create a root `AGENTS.md` that references the hangar-ai-constitution
3. Select appropriate avatars (industry, product-type, technology)
4. Follow the [Adoption Guide](../guides/adoption/how-to-adopt-constitution.md) for a step-by-step walkthrough

---

## Summary

The Hangar AI Constitution is the answer to a fundamental challenge: **how do you get consistent, high-quality, safe output from AI coding assistants at scale?**

The answer is governance. By encoding engineering wisdom, product principles, and business compliance requirements into structured laws—and by giving AI agents skills and workflows to follow those laws—the Constitution turns AI-assisted development from an unpredictable experiment into a disciplined, repeatable practice.

It is **18 months of research** distilled into a portable governance framework, purpose-built for American Airlines, and designed to grow with the teams that use it.

---

*For questions or contributions, open an issue in [AAInternal/hangar-ai-constitution](https://github.com/AAInternal/hangar-ai-constitution).*

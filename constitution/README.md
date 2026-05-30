# American Airlines Hangar AI Constitution

A comprehensive governance framework for Agentic AI at American Airlines. This Constitution establishes the laws, guardrails, and best practices that govern how AI agents operate—both in **how we build software** and **what we build for customers**.

## Vision: Two Value Streams

This Constitution serves two complementary purposes:

### Team Value Stream: Spec-Driven Development (Current Focus)

AI agents assist engineering teams in building software through **Spec-Driven Development (SDD)**—a disciplined approach where specifications drive implementation, tests precede code, and quality is built-in from the start.

```
Discovery → Specification → Planning → Implementation → Review → Deployment
    ↑                                                              |
    └──────────────────── Feedback Loop ───────────────────────────┘
```

**Key capabilities:** Roadmapping, user journey mapping, executable specs, atomic TDD, vertical slice development, code review.

### Product Value Stream: Agentic AI in Products (Future Focus)

AI agents embedded in American Airlines products to serve customers directly—intelligent rebooking, proactive travel assistance, cargo optimization, and personalized loyalty experiences.

**Key concerns:** Safety guardrails, regulatory compliance, customer trust, auditability, graceful degradation.

---

## The Three Constitutions

Effective AI governance requires laws across three dimensions. Each constitution answers a different question:

| Constitution | Question | Scope |
|--------------|----------|-------|
| [**Engineering**](laws/engineering/) | **HOW** do we build? | Code quality, testing, architecture, DevOps |
| [**Product**](laws/product/) | **WHAT** do we build? | User journeys, metrics, accessibility, experimentation |
| [**Business**](laws/business/) | **WHY** and under what constraints? | Compliance, domain rules, data governance, aviation regulations |

### Why All Three Matter

**Without Engineering Laws:** Code becomes unmaintainable, untestable, and unreliable. AI agents produce inconsistent, low-quality output.

**Without Product Laws:** Features solve the wrong problems, ignore user needs, and lack measurable outcomes. AI agents optimize for the wrong goals.

**Without Business Laws:** Software violates regulations, mishandles sensitive data, and creates compliance risk. AI agents make decisions that harm customers or the business.

**Together:** The three constitutions create a complete framework where AI agents build the *right thing* (Product), build it *right* (Engineering), and build it *safely* (Business).

---

## Constitutional Hierarchy

Laws are applied in layers, from universal principles to specific contexts:

```
┌─────────────────────────────────────────────────────────────┐
│                    BASE CONSTITUTIONS                        │
│         Engineering + Product + Business Laws                │
│              (Apply to ALL AA software)                      │
├─────────────────────────────────────────────────────────────┤
│                   INDUSTRY ADOPTION                          │
│            Aviation: FAA, DO-178C, TSA, DOT                 │
│         (Aviation-specific compliance requirements)          │
├─────────────────────────────────────────────────────────────┤
│                  PRODUCT-TYPE ADOPTION                       │
│      Booking | Cargo | Loyalty | Operations | Service        │
│            (Domain-specific patterns & rules)                │
├─────────────────────────────────────────────────────────────┤
│                  TECHNOLOGY ADOPTION                         │
│        Java/Spring | React | Python | .NET | etc.           │
│            (Stack-specific implementations)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Product Domains

This Constitution includes adoptions for American Airlines' core product domains:

| Domain | Description | Key Concerns |
|--------|-------------|--------------|
| [Passenger Booking](avatars/product-type/passenger-booking/) | Flight search, booking, ancillaries | DOT fare transparency, PCI compliance |
| [Check-In & Travel](avatars/product-type/check-in-travel/) | Check-in, boarding, flight status | TSA compliance, real-time updates |
| [Cargo & Freight](avatars/product-type/cargo-freight/) | PAL applications, AWB, iCargo | TSA vetting, dangerous goods |
| [Loyalty (AAdvantage)](avatars/product-type/loyalty-aadvantage/) | Miles, status, awards | Financial accuracy, audit trails |
| [Airport Operations](avatars/product-type/airport-operations/) | Gate management, crew, IROP | FAR Part 117, real-time safety |
| [Customer Service](avatars/product-type/customer-service/) | Rebooking, refunds, complaints | DOT refund timelines |

## Repository Structure

```
hangar-ai-constitution/
├── laws/                           # WHAT laws govern
│   ├── engineering/                # Code quality, testing, architecture
│   ├── product/                    # User journeys, metrics, accessibility
│   └── business/                   # Compliance, domain rules, data governance
│
├── avatars/                         # HOW to apply in different contexts
│   ├── industry/aviation-faa/      # FAA, DO-178C, TSA compliance
│   ├── product-type/               # Passenger Booking, Cargo, Loyalty, etc.
│   └── technology/                 # Java, Python, React, .NET, etc.
│
├── agent-skills/                    # Agent operating system & skills
│   ├── base/AGENT.md               # Core agent operating system
│   └── skills-by-domain/           # 29 modular capabilities in 5 domains
│
├── tools/                           # CLI tools for constitution enforcement
│   ├── constitution-lint/           # aa-constitution-lint — validates law files and indexes
│   ├── artifact-renderer/           # aa-artifact-render — renders artifacts as HTML/PDF with law tooltips
│   ├── sonarqube-gate/              # sonarqube-gate — code quality gate enforcement
│   └── rag-eval/                    # RAG quality evaluation harness
│
└── docs/                           # Learning resources
    ├── articles/                   # Deep-dive explanations
    ├── guides/                     # Adoption strategies
    └── slides/                     # Presentation materials
```

### Tools

| Tool | Command | Purpose |
|------|---------|---------|
| [Constitution Lint](tools/constitution-lint/) | `aa-constitution-lint .` | Validates law files, skill indexes, and law ID references across the entire constitution |
| [Artifact Renderer](tools/artifact-renderer/) | `aa-artifact-render ARTIFACT.md` | Renders governance artifacts (proposals, ADRs, evidence, tasks) as self-contained HTML with interactive law citation tooltips; optional PDF via `--pdf` |
| [SonarQube Gate](tools/sonarqube-gate/) | `sonarqube-gate` | Enforces code quality gates per ENG-4.x laws |
| [RAG Eval](tools/rag-eval/) | `python tools/rag-eval/evaluate.py` | Evaluates constitution RAG retrieval quality |

## Quick Start

### For Engineers

1. **Understand the framework:** Read all three base laws
   - [Engineering Laws](laws/engineering/) - Code quality, testing, architecture
   - [Product Laws](laws/product/) - User-centric design, metrics, accessibility
   - [Business Laws](laws/business/) - Compliance, domain rules, data governance
2. **Learn the practices:** Review the [Atomic TDD Skill](agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md)
3. **Know your domain:** Study your [product domain adoption](avatars/product-type/)

### For AI Agents (GitHub Copilot)

1. Load the base [AGENT.md](agent-skills/base/AGENT.md) - establishes persona and guardrails
2. Apply all three laws as authority hierarchy
3. Apply technology adoption (e.g., [Java/Spring](avatars/technology/java-spring/))
4. Apply product adoption (e.g., [Cargo](avatars/product-type/cargo-freight/))
5. Follow Constitutional laws strictly—cite articles when enforcing

### For New Projects

1. Initialize Hangar SDD structure using the [Spec Governance Skill](agent-skills/skills-by-domain/discovery-research/spec-governance.md)
2. Copy all three base constitutions to `hangar-ai-specs/specs/constitution/`
3. Select appropriate adoptions (industry, product-type, technology)
4. Configure AI assistants with Constitution references
5. Establish project-specific AGENTS.md if needed

## Key Principles by Constitution

### Engineering Constitution: How We Build

**8-Step Atomic TDD Cycle**
```
RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT
```

**Test Pyramid**
| Level | Coverage | Purpose |
|-------|----------|---------|
| Unit | 70-80% | Fast, isolated, no Spring context |
| Integration | 15-25% | Controller layer, database |
| E2E | 5-10% | Critical user journeys |

**Code Quality Thresholds**
| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Cyclomatic Complexity | ≤ 10 | Maintainability |
| Cognitive Complexity | ≤ 7 | Readability |
| Test Coverage | ≥ 90% | Reliability |
| Method Length | ≤ 20 lines | Single responsibility |

### Product Constitution: What We Build

**User-Centric Design**
- Every feature traces to a user problem (not a solution request)
- User journeys documented before implementation
- Accessibility is non-negotiable (WCAG 2.1 AA minimum)

**Outcome-Based Development**
- Features require success metrics before building
- Experimentation (A/B testing) for uncertain outcomes
- Data-informed iteration over opinion-driven changes

**Product Metrics**
| Category | Examples |
|----------|----------|
| Engagement | Task completion rate, time on task |
| Satisfaction | NPS, CSAT, effort score |
| Business | Conversion, revenue impact, cost reduction |

### Business Constitution: Why We Build (Safely)

**Aviation Compliance**
| Regulation | Scope |
|------------|-------|
| FAA Part 121 | Air carrier certification |
| DO-178C | Airborne software assurance levels |
| DO-326A | Airborne cybersecurity |
| TSA | Security screening and vetting |
| DOT | Consumer protection, refund timelines |

**Domain-Driven Design**
- Ubiquitous language enforced across code and conversation
- Bounded contexts prevent domain pollution
- Business rules explicit, testable, and traceable

**Data Governance**
- PII handling follows privacy-by-design
- Audit trails for financial transactions (miles, refunds)
- Data retention aligned with regulatory requirements

## Agent Skills

The AI agent has 8 core skills for the full development lifecycle:

| Skill | Purpose |
|-------|---------|
| [Roadmapping](agent-skills/skills-by-domain/product-planning/01-roadmapping.md) | Outcome-based planning |
| [User Journey Mapping](agent-skills/skills-by-domain/discovery-research/02-user-journey-mapping.md) | Problem-first journey design |
| [Executable Spec](agent-skills/skills-by-domain/product-planning/03-executable-spec.md) | BDD/Gherkin specifications |
| [Business Domain Modeling](agent-skills/skills-by-domain/development-practices/04-business-domain-modeling.md) | DDD patterns |
| [Business Rules](agent-skills/skills-by-domain/development-practices/05-business-rules.md) | Rule documentation |
| [Atomic TDD](agent-skills/skills-by-domain/development-practices/06-atomic-tdd.md) | Test-first development |
| [Vertical Slice Dev](agent-skills/skills-by-domain/development-practices/07-vertical-slice-dev.md) | End-to-end increments |
| [Code Review](agent-skills/skills-by-domain/development-practices/08-code-review.md) | Constitutional compliance |

## Technology Avatars

| Stack | Adoption Guide |
|-------|----------------|
| Java/Spring Boot | [avatars](avatars/technology/java-spring/) |
| Python/FastAPI | [avatars](avatars/technology/python-fastapi/) |
| React/TypeScript | [avatars](avatars/technology/react-typescript/) |
| Node.js/TypeScript | [avatars](avatars/technology/nodejs-typescript/) |
| .NET Core | [avatars](avatars/technology/dotnet-core/) |
| Angular | [avatars](avatars/technology/angular/) |
| React Native | [avatars](avatars/technology/mobile-react-native/) |
| iOS/Android Native | [avatars](avatars/technology/mobile-native/) |
| ML/Analytics | [avatars](avatars/technology/ml-analytics/) |
| Data Engineering | [avatars](avatars/technology/data-engineering/) |

- [aacargo-multi-api](https://github.com/AAInternal/aacargo-multi-api) - Reference implementation
- [Agent Skills](agent-skills/skills-by-domain/) - Modular agent capabilities by domain

## Contributing

This repository is maintained by The Hangar AI team. For questions, suggestions, or contributions:

1. Open an issue describing the proposed change
2. Reference the relevant Constitution articles
3. Include good/bad examples where applicable

---

**Maintained by:** The Hangar, American Airlines IT

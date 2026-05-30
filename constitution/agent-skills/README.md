# Agent Skills Framework

> **Purpose:** Operational guidance for AI agents following American Airlines Hangar's Constitutional Coding methodology.

This framework defines HOW AI agents operate when building software under Constitutional governance. While the [Laws](../laws/) define WHAT laws must be followed, Agent Skills define HOW to follow them.

---

## Quick Start

### For AI Agents (GitHub Copilot)
1. Load `base/AGENT.md` as your core operating system
2. Reference skills from `skills-by-domain/` based on the task at hand (see domain `index.yaml` files)
3. Apply relevant avatars from `avatars/` for stack-specific behaviors (see `avatars/index.yaml`)

### For Developers
1. Initialize your project with the [Spec Governance Skill](skills-by-domain/discovery-research/spec-governance.md)
2. Configure GitHub Copilot to reference these instructions
3. Use skills as a shared vocabulary with your AI pair programmer

---

## Framework Architecture

```
agent-skills/
├── base/
│   └── AGENT.md              # Core operating system - start here
├── skills-by-domain/          # Discrete agent capabilities by domain
│   ├── development-practices/ # TDD, code review, refactoring, DDD
│   │   └── index.yaml
│   ├── discovery-research/    # Spec Governance, user journeys
│   │   └── index.yaml
│   ├── ml-ai/                 # ML pipelines, RAG, prompt engineering
│   │   └── index.yaml
│   ├── platform-engineering/  # Security, observability, API design
│   │   └── index.yaml
│   └── product-planning/      # Roadmapping, specs, documentation
│       └── index.yaml
└── README.md                  # This file
```

---

## Multi-RAG Architecture

The constitution uses a multi-RAG (Retrieval-Augmented Generation) system:

| Registry | Purpose | Location |
|----------|---------|----------|
| **Laws Index** | Master law catalog | `laws/index.yaml` |
| **Domain YAMLs** | Law metadata by domain | `laws/{domain}/_domain.yaml` |
| **Skills Indices** | Skill-to-law mappings per domain | `agent-skills/skills-by-domain/{domain}/index.yaml` |
| **Avatars Index** | Context specialization | `avatars/index.yaml` |

This enables AI agents to:
- Query laws by ID or category
- Find skills that implement specific laws
- Apply context-specific patterns via avatars

---

## Relationship to Constitution

| Aspect | Constitution | Agent Instructions |
|--------|--------------|-------------------|
| **Focus** | Laws and principles | Operations and methods |
| **Question** | WHAT must be followed? | HOW do we follow it? |
| **Authority** | Absolute (must comply) | Guidance (how to comply) |
| **Format** | Articles, sections, laws | Skills, templates |
| **Examples** | Principles and rationale | Step-by-step with artifacts |

---

## Skills Index

### Foundational Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [Spec Governance](skills-by-domain/discovery-research/spec-governance.md) | Hangar SDD lifecycle with constitutional compliance | Compliant proposals with task tracking |

### Product & Discovery Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [01-Roadmapping](skills-by-domain/product-planning/01-roadmapping.md) | Outcome-based product planning | Roadmap with Now/Next/Later |
| [02-User Journey Mapping](skills-by-domain/discovery-research/02-user-journey-mapping.md) | Understanding user problems | Journey canvas with pain points |

### Specification Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [03-Executable Spec](skills-by-domain/product-planning/03-executable-spec.md) | Business-readable specifications | Gherkin feature files |
| [04-Business Domain Modeling](skills-by-domain/development-practices/04-business-domain-modeling.md) | DDD strategic/tactical design | Domain model with aggregates |
| [05-Business Rules](skills-by-domain/development-practices/05-business-rules.md) | Explicit rule documentation | Business rules catalog |

### Implementation Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [06-Atomic TDD](skills-by-domain/development-practices/06-atomic-tdd.md) | Test-first development cycle | Verified, tested code |
| [07-Vertical Slice Dev](skills-by-domain/development-practices/07-vertical-slice-dev.md) | End-to-end increments | Deployable vertical slices |
| [08-Code Review](skills-by-domain/development-practices/08-code-review.md) | Constitutional compliance | Review feedback with citations |

### Quality & Operations Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [09-Refactoring](skills-by-domain/development-practices/09-refactoring.md) | Code improvement without behavior change | Cleaner, simpler code |
| [10-Security Review](skills-by-domain/platform-engineering/10-security-review.md) | Threat modeling and OWASP compliance | Secure, hardened systems |
| [11-Incident Response](skills-by-domain/platform-engineering/11-incident-response.md) | Production incident handling | Resolved incidents, postmortems |
| [12-API Design](skills-by-domain/platform-engineering/12-api-design.md) | RESTful API patterns | Consistent, evolvable APIs |

### Enterprise Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [13-Observability](skills-by-domain/platform-engineering/13-observability.md) | Logs, metrics, and distributed tracing | Observable, debuggable systems |
| [14-Technical Debt](skills-by-domain/platform-engineering/14-technical-debt.md) | Debt identification and management | Sustainable codebase velocity |
| [15-Data Modeling](skills-by-domain/platform-engineering/15-data-modeling.md) | Database schema design | Performant, evolvable schemas |
| [16-Documentation](skills-by-domain/product-planning/16-documentation.md) | ADRs, runbooks, API docs | Preserved knowledge, fast onboarding |

### MLOps Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [17-ML Pipeline](skills-by-domain/ml-ai/17-ml-pipeline.md) | End-to-end ML pipeline design | Reproducible, automated pipelines |
| [18-Experiment Tracking](skills-by-domain/ml-ai/18-experiment-tracking.md) | Model training & experimentation | Reproducible experiments, model registry |
| [19-Model Serving](skills-by-domain/ml-ai/19-model-serving.md) | Model deployment & inference | Scalable, versioned model serving |
| [20-ML Monitoring](skills-by-domain/ml-ai/20-ml-monitoring.md) | Model & data drift detection | Reliable models in production |

### AI Development Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [21-Prompt Engineering](skills-by-domain/ml-ai/21-prompt-engineering.md) | LLM prompting patterns | Effective, consistent AI interactions |
| [22-RAG Architecture](skills-by-domain/ml-ai/22-rag-architecture.md) | Retrieval-augmented generation | Grounded, accurate AI responses |
| [23-AI Agents](skills-by-domain/ml-ai/23-ai-agents.md) | AI agent design patterns | Reliable, controllable agents |
| [24-AI Safety](skills-by-domain/ml-ai/24-ai-safety.md) | Responsible AI & guardrails | Safe, aligned AI systems |

### UX Design Skills
| Skill | Purpose | Key Output |
|-------|---------|------------|
| [25-UX Design](skills-by-domain/development-practices/25-ux-design.md) | Design systems and Figma workflows | Consistent, accessible designs |
| [26-Design to Code](skills-by-domain/development-practices/26-design-to-code.md) | Figma MCP, Locofy, design handoff | Production-ready components |

---

## Technology Avatars

Select the adoption matching your technology stack:

| Stack | Adoption |
|-------|----------|
| Java/Spring Boot | [java-spring](../avatars/technology/java-spring/) |
| Python/FastAPI | [python-fastapi](../avatars/technology/python-fastapi/) |
| React/TypeScript | [react-typescript](../avatars/technology/react-typescript/) |
| .NET Core | [dotnet-core](../avatars/technology/dotnet-core/) |
| Node.js/TypeScript | [nodejs-typescript](../avatars/technology/nodejs-typescript/) |
| Angular | [angular](../avatars/technology/angular/) |
| React Native | [mobile-react-native](../avatars/technology/mobile-react-native/) |
| iOS/Android Native | [mobile-native](../avatars/technology/mobile-native/) |
| ML/Analytics | [ml-analytics](../avatars/technology/ml-analytics/) |
| Data Engineering | [data-engineering](../avatars/technology/data-engineering/) |

---

## Authority Hierarchy

When operating, AI agents follow this priority order:

1. **Constitution Laws** - Absolute authority, must be followed
2. **AGENT.md Instructions** - Core operational guidance
3. **Project AGENTS.md** - Project-specific context and overrides
4. **Hangar SDD Proposals** - Current work context

---

## Getting Help

- **Constitution Deep-Dives:** See [Constitution Guides](../docs/guides/constitution/)
- **Adoption Strategies:** See [Adoption Guides](../docs/guides/adoption/)
- **Prompt Patterns:** See [Prompt Guides](../docs/guides/prompts/)

---

**Maintained by:** The Hangar, American Airlines IT

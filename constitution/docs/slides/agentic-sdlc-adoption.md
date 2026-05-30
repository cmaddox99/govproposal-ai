<!-- slide 1 -->

# 🛫 Agentic SDLC Adoption at American Airlines

### The AA Hangar AI Constitution

**From AI Autocomplete to Constitutional AI Development**

Hangar Leadership & Coaches | 60 Minutes | January 2026




---

<!-- slide 2 -->

# 📦 Wave 2 Experiment: AA Cargo in 5 Hours

## Constitutional AI Framework in Action

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE (Baseline)                  AFTER (5-Hour Session)      │
│  ─────────────────                  ──────────────────────      │
│  • 30% code coverage                • 91% code coverage ✅      │
│  • Inverted test pyramid            • Healthy test pyramid      │
│  • 2 unit tests                     • 63+ characterization tests│
│  • 85% integration tests            • 70%+ unit tests           │
│  • No safety net for refactoring    • Full refactoring enabled  │
└─────────────────────────────────────────────────────────────────┘
```

**What We Did:**
- Adopted the **Constitutional Framework** (OpenSpec + CONSTITUTION.md)
- Applied **Atomic TDD** (8-step cycle: RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT)
- AI agent followed **explicit engineering laws** from the Constitution
- Junior engineer paired with AI mentor achieved **senior-level output**

**Key Insight:**
> "In 5 hours, we achieved what would take weeks with traditional approaches—
> because the AI had explicit standards to follow, not just code to generate."




---

<!-- slide 3 -->

# ⚡ The Paradigm Shift

## Traditional AI vs. Constitutional AI

```
┌─────────────────────────────────────────────────────────────────┐
│  TRADITIONAL AI CODING              CONSTITUTIONAL AI           │
│  ─────────────────────              ─────────────────           │
│  • AI generates code                • AI follows explicit laws  │
│  • Human fixes batch errors         • Human guides direction    │
│  • Inconsistent quality             • Production-ready output   │
│  • No learning transfer             • AI teaches as it builds   │
│  • "Autocomplete on steroids"       • "Teaching partner"        │
└─────────────────────────────────────────────────────────────────┘
```

**The Core Insight:**
> Without explicit standards, AI produces prototype-quality code.
> With a Constitution, AI produces consistent, production-quality output.




---

<!-- slide 4 -->

# 🎬 Live Demo: Agentic SDLC in Action

## Weather Search App Workshop

We'll execute the **Fast Track Workshop** to see:
- How the agent loads and applies the Constitution
- The difference between vanilla AI and Constitutional AI
- Atomic TDD in action
- A working app built with AI pairing

**Trigger:**
```
Help me run the AI Spec-Driven Development Workshop 
from ~/repos/weather-search-app/WORKSHOP-GUIDE.md
```

> The agent will explain the "why" as it builds.




---

<!-- DEMO EXECUTION - START EARLY -->

---

<!-- slide 5 -->

# 🧠 What is Constitutional AI?

## The Science Behind the Approach

Based on Anthropic's research on **Constitutional AI: Harmlessness from AI Feedback**:

> AI systems can be trained to follow explicit principles and self-correct 
> against those principles, resulting in safer and more aligned outputs.

**Our Application:**
- **Principles** → Engineering Laws, Product Laws, Business Laws
- **Self-correction** → Agent checks work against Constitution
- **Alignment** → Code aligns with AA standards, not random patterns

📄 [Anthropic Constitutional AI Paper](https://arxiv.org/abs/2212.08073)




---

<!-- slide 6 -->

# 📜 The Constitution Framework

## A Knowledgebase for Humans AND Agents

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    BASE CONSTITUTIONS (Universal Laws)                  │
├───────────────────────┬───────────────────────┬─────────────────────────┤
│      ENGINEERING      │        PRODUCT        │        BUSINESS         │
│      CONSTITUTION     │      CONSTITUTION     │      CONSTITUTION       │
├───────────────────────┼───────────────────────┼─────────────────────────┤
│ HOW we build          │ WHAT we build         │ WHERE we operate        │
├───────────────────────┼───────────────────────┼─────────────────────────┤
│ • Architecture        │ • Discovery           │ • Compliance            │
│ • Code Quality        │ • User Journey        │ • Data Governance       │
│ • Testing (TDD)       │ • Roadmap             │ • Privacy               │
│ • DevOps              │ • MVP/PMF             │ • Risk Management       │
│ • AI-Engineer Pairing │ • Metrics             │ • Audit                 │
└───────────────────────┴───────────────────────┴─────────────────────────┘
```

**Key Point:** Same documents train AI agents AND educate human engineers.

📄 [constitution/README.md](https://github.com/AAInternal/hangar-ai-constitution/blob/main/constitution/README.md)




---

<!-- slide 7 -->

# ⚙️ How the Constitution Works

## Agent Reads → Applies → Cites

```
┌────────────────────────────────────────────────────────────────┐
│  1. LOAD CONSTITUTION                                          │
│     └─ Agent reads engineering laws before any code            │
│                                                                │
│  2. UNDERSTAND CONTEXT                                         │
│     └─ Load relevant tech stack adoption + product domain      │
│                                                                │
│  3. APPLY PRINCIPLES                                           │
│     └─ Every decision references constitutional articles       │
│                                                                │
│  4. SELF-CORRECT                                               │
│     └─ Agent checks output against laws before presenting      │
│                                                                │
│  5. CITE & TEACH                                               │
│     └─ "Per Article IV, Section 4.1..." as it explains         │
└────────────────────────────────────────────────────────────────┘
```




---

<!-- slide 8 -->

# 📋 OpenSpec: The Specification Framework

## Adopt Constitution → Generate Constitutional Proposals

```
┌─────────────────────────────────────────────────────────────────┐
│                      OPENSPEC STRUCTURE                         │
├─────────────────────────────────────────────────────────────────┤
│  openspec/                                                      │
│  ├── project.md           ← Project context & goals             │
│  ├── CONSTITUTION.md      ← ADOPTED constitution for codebase   │
│  ├── AGENTS.md            ← Project-specific agent rules        │
│  └── changes/             ← CONSTITUTIONAL proposals            │
│      └── add-feature-x/                                         │
│          ├── proposal.md  ← What we're building & why           │
│          └── tasks.md     ← TDD task breakdown                  │
└─────────────────────────────────────────────────────────────────┘
```

**The Flow:**
1. **Adopt Constitution** into your codebase (`CONSTITUTION.md`)
2. **Generate proposals** - Agent reads Constitution FIRST
3. **Proposals are constitutional** - Tasks follow TDD, cite articles
4. **Code emerges** from test-first, principle-driven development

> Without adopted Constitution = vanilla proposals (prototype quality)
> With adopted Constitution = constitutional proposals (production quality)

📄 [openspec/ in weather-search-app](https://github.com/AAInternal/weather-search-app/tree/main/openspec)




---

<!-- slide 9 -->

# 🤖 Agent Instructions

## The Second Layer: Training the Agent

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHORITY HIERARCHY                          │
├─────────────────────────────────────────────────────────────────┤
│  1. CONSTITUTION (Highest)     ← Universal engineering laws    │
│  2. AGENT.md                   ← Agent identity & guardrails   │
│  3. Project AGENTS.md          ← Project-specific rules        │
│  4. OpenSpec / Proposals       ← Current work context          │
└─────────────────────────────────────────────────────────────────┘
```

**AGENT.md defines:**
- Agent's identity (Senior XP Engineer persona)
- Teaching-first mindset
- Guardrails (NEVER/ALWAYS lists)
- Operating modes (Discovery, Planning, Implementation, Review)

📄 [agent-skills/README.md](https://github.com/AAInternal/hangar-ai-constitution/blob/main/agent-skills/README.md)




---

<!-- slide 10 -->

# 🎯 Trained Agent Skills

## Capabilities We've Trained

| Skill | Purpose |
|-------|---------|
| **01-Roadmapping** | Strategic planning & sequencing |
| **02-User Journey Mapping** | End-to-end user experience design |
| **03-Executable Spec** | Living documentation (OpenSpec) |
| **04-Business Domain Modeling** | DDD & bounded contexts |
| **05-Business Rules** | Codifying business logic |
| **06-Atomic TDD** | Test-first, one behavior at a time |
| **07-Vertical Slice Dev** | Full-stack feature delivery |
| **08-Code Review** | Quality gates & feedback |

📄 [agent-skills/skills-by-domain/](https://github.com/AAInternal/hangar-ai-constitution/tree/main/agent-skills/skills-by-domain)




---

<!-- slide 11 -->

# 🛡️ Safety Built Into Instructions

## Guardrails in AGENT.md

```
┌─────────────────────────────────────────────────────────────────┐
│  NEVER (Hard Guardrails)                                        │
│  ├─ Write production code without a failing test                │
│  ├─ Skip test verification steps                                │
│  ├─ Implement beyond current acceptance criteria                │
│  ├─ Assume requirements - ASK                                   │
│  ├─ Batch multiple behaviors in one test                        │
│  └─ Proceed when tests are failing                              │
├─────────────────────────────────────────────────────────────────┤
│  ALWAYS (Required Actions)                                      │
│  ├─ Run tests after every code change                           │
│  ├─ Cite Constitution articles when making decisions            │
│  ├─ Explain WHY, not just WHAT                                  │
│  ├─ Ask for clarification on ambiguous requirements             │
│  └─ Commit working code atomically                              │
└─────────────────────────────────────────────────────────────────┘
```

**Principle:** Safety through explicit constraints, not implicit assumptions.




---

<!-- slide 12 -->

# 🔧 Adoption Framework

## Technology + Product + Industry

```
TECHNOLOGY ADOPTIONS          PRODUCT ADOPTIONS           INDUSTRY ADOPTION
────────────────────          ─────────────────           ─────────────────
• Java/Spring Boot            • Passenger Booking         • Aviation/FAA
• Python/FastAPI              • Check-In & Travel           - DO-178C
• React/TypeScript            • Cargo & Freight             - AS9100
• .NET Core                   • Loyalty (AAdvantage)        - TSA compliance
• Node.js/TypeScript          • Airport Operations
• Angular                     • Customer Service
• Mobile (React Native)
• ML/Analytics
• Data Engineering
```

📄 [constitution/README.md](https://github.com/AAInternal/hangar-ai-constitution/blob/main/constitution/README.md) *(includes all adoption links)*




---

<!-- slide 13 -->

# 📚 Repository Guides

## Knowledge for Humans & Agents

| Guide | Purpose | Audience |
|-------|---------|----------|
| **Adoption Guide** | How to adopt in your team | Coaches, Tech Leads |
| **Testing Guide** | Test pyramid, mutation testing | Developers |
| **Constitution Guide** | Understanding the articles | Everyone |
| **Prompts Guide** | Effective AI pairing | Developers |
| **Metrics Guide** | Measuring adoption success | Leadership |

**Key Insight:** These guides serve dual purpose:
1. **Human training** - Engineers read and learn
2. **Agent context** - AI loads and applies

📄 [guides/index.md](https://github.com/AAInternal/hangar-ai-constitution/blob/main/guides/index.md)




---

<!-- slide 14 -->

# 🏩 Engineering Laws Repository

## Governance & Practice Guides

**Separate repo for governance:** `aa-engineering-laws`

```
aa-engineering-laws/
├── laws/
│   └── ENGINEERING-LAWS.md       ← Core engineering laws
├── practice-guides/              ← Detailed methodology
│   ├── atomic-tdd/
│   ├── ddd/
│   ├── vertical-slice/
│   ├── code-quality/
│   ├── test-pyramid/
│   └── ai-pairing/
├── amendments/                   ← RFC process
│   ├── proposals/
│   └── voting/
├── committee/                    ← Governance
│   └── CHARTER.md
└── technology-adoptions/         ← Stack-specific guides
```

📄 [github.com/AAInternal/aa-engineering-laws](https://github.com/AAInternal/aa-engineering-laws)




---

<!-- slide 15 -->

# 🗳️ Amendment Process

## Laws Evolve Through Evidence

```
┌─────────────────────────────────────────────────────────────────┐
│                     AMENDMENT LIFECYCLE                         │
├─────────────────────────────────────────────────────────────────┤
│  1. RFC PROPOSAL                                                │
│     └─ Any engineer submits Request for Comment                 │
│                                                                 │
│  2. DISCUSSION PERIOD (2 weeks)                                 │
│     └─ Community feedback, questions, refinement                │
│                                                                 │
│  3. EVIDENCE GATHERING                                          │
│     └─ Pilot with teams, collect metrics, document outcomes     │
│                                                                 │
│  4. COMMITTEE REVIEW                                            │
│     └─ Technical evaluation, alignment check                    │
│                                                                 │
│  5. VOTING                                                      │
│     └─ Supermajority required (2/3)                             │
│                                                                 │
│  6. RATIFICATION                                                │
│     └─ Update Constitution, notify all teams                    │
└─────────────────────────────────────────────────────────────────┘
```

**Principle:** Laws change through evidence, not opinion.




---

<!-- slide 16 -->

# 🚀 The Vision

## From Hangar Experiment to AA Standard

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  WAVE 1 (Now)          WAVE 2                WAVE 3             │
│  ───────────           ──────                ──────             │
│  Hangar Pilots         Broader Adoption      Enterprise Scale   │
│                                                                 │
│  • Test with           • Expand to more      • Formal AA AI     │
│    willing teams         tech stacks           Constitution     │
│  • Gather evidence     • Refine through      • Due process      │
│  • Mature the            amendment process     ratification     │
│    Constitution        • Build coach         • Full governance  │
│  • Train coaches         expertise             structure        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Goal:** This Constitution becomes the **AA AI Constitution** through due process and demonstrated value.




---

<!-- slide 17 -->

# 📊 Measuring Adoption Success

## The Core Question

> **"Are developers becoming better engineers WITH AI, or dependent ON AI?"**

### Critical Metrics

| Metric | What It Tells You |
|--------|-------------------|
| **Defect Escape Rate** | Quality outcome, not vanity |
| **Time to Developer Productivity** | Learning acceleration |
| **TDD/Constitution Compliance** | Internalization of principles |
| **"AI Off" Competency Score** | No dependency created |

**Success Formula:**
```
defects ↓ + compliance ↑ + competency maintained = AI AMPLIFYING engineers ✅
defects ↑ OR compliance ↓ OR competency drops = AI REPLACING thinking ❌
```

📄 [enterprise-ai-adoption-metrics.md](https://github.com/AAInternal/hangar-ai-constitution/blob/main/guides/adoption/enterprise-ai-adoption-metrics.md)




---

<!-- slide 18 -->

# 🤝 Help Needed from Coaches

## Areas for Enrichment

### Technical Coaches
- [ ] Validate technology stack adoptions
- [ ] Identify missing stacks in your portfolio
- [ ] Test agent skills with your teams
- [ ] Submit RFCs for improvements

### Product Coaches
- [ ] Enrich product domain adoptions
- [ ] Add user journey patterns for your domains
- [ ] Document business rules specific to your areas
- [ ] Help train product-focused agent skills

**Every adoption guide you enrich makes the AI smarter for your teams.**




---

<!-- slide 19 -->

# 🎬 Call to Action

## Building & Testing the Process

### Immediate Actions
1. **Identify a pilot team** in your portfolio
2. **Run the workshop** with them (Fast Track or Step-by-Step)
3. **Collect feedback** on gaps and improvements
4. **Submit RFCs** for any needed changes

### The Machine Learning Principle

Per Constitutional AI research:
> By providing explicit principles and allowing self-correction,
> we improve safety through iteration, not restriction.

Each team that uses the Constitution provides feedback that improves it.
**Your pilots train the system.**

📄 [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)




---

<!-- slide 20 -->

# 🔗 Resources

## Quick Reference

| Resource | Link |
|----------|------|
| **AA Hangar AI Constitution** | [github.com/AAInternal/hangar-ai-constitution](https://github.com/AAInternal/hangar-ai-constitution) |
| **Engineering Laws & Amendments** | [github.com/AAInternal/aa-engineering-laws](https://github.com/AAInternal/aa-engineering-laws) |
| **Adoption Metrics Guide** | [guides/adoption/enterprise-ai-adoption-metrics.md](https://github.com/AAInternal/hangar-ai-constitution/blob/main/guides/adoption/enterprise-ai-adoption-metrics.md) |
| **Workshop Application** | `~/repos/weather-search-app/` |
| **Anthropic Constitutional AI** | [arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073) |

### Workshop Trigger
```
Help me run the AI Spec-Driven Development Workshop 
from ~/repos/weather-search-app/WORKSHOP-GUIDE.md
```




---

<!-- slide 21 -->

# 💬 Discussion

## Key Questions

1. **What teams in your portfolio could pilot this?**
2. **What technology or product adoptions are missing?**
3. **How can we measure success in your context?**
4. **What barriers do you anticipate?**




---

<!-- slide 22 -->

# 🌟 Thank You

## The Constitution transforms AI from code generator to teaching partner.

**Next Steps:**
- Pick a pilot team
- Run the workshop
- Share feedback
- Submit RFCs

**Together we'll build the AA AI Constitution.**

🛫

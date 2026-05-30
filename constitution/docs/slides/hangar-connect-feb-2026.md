<!-- slide 1 -->

# 🛫 Introducing the Hangar AI Constitution

### Pathway to Agentic SDLC

**How We're Learning to Practice 100% AI-Assisted Coding at the Hangar**

Adeel Ali | AI Coach & Advisor | Hangar Connect | February 10, 2026









---

<!-- slide 2 -->

# 👋 About Your Presenter

## Adeel Ali

**AI Coach & Advisor, The Hangar Team**

- Not new to American Airlines - previously served as Tech Lead / Tech Coach
- Passionate about software craftsmanship and AI-human collaboration
- Proud Executive Platinum member for close to a decade
- Exclusively flies American Airlines ✈️

> "The Hangar has always felt like home."









---

<!-- slide 3 -->

# 📋 Agenda

## What We'll Cover Today

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. THE GIFT                                                    │
│     └─ What is the Hangar AI Constitution?                      │
│                                                                 │
│  2. THE FRAMEWORK                                               │
│     └─ Laws, avatars, skills - how it all fits together         │
│                                                                 │
│  3. THE PRINCIPLES                                              │
│     └─ AI-Engineer Pairing, Atomic TDD, Accountability          │
│                                                                 │
│  4. LIVE DEMO                                                   │
│     └─ Watch Constitutional adoption in action                  │
│                                                                 │
│  5. REAL RESULTS                                                │
│     └─ Cargo & Check-In POC outcomes                            │
│                                                                 │
│  6. THE PATH FORWARD                                            │
│     └─ Upcoming waves, what we're building, your move           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```






---

<!-- slide 4 -->

# ⚠️ The Problem with Traditional AI Coding

## Why We Need a Constitution

```
┌─────────────────────────────────────────────────────────────────┐
│  TRADITIONAL AI CODING                                          │
│  ─────────────────────                                          │
│                                                                 │
│  Engineer prompts → AI generates code → Copy/paste → Hope → 🤞  │
│                                                                 │
│  What Goes Wrong:                                               │
│  ────────────────                                               │
│  • Every response is different (no consistency)                 │
│  • AI loses context between sessions                            │
│  • Prototype-quality code shipped to production                 │
│  • Humans must debug and fix AI-created errors                  │
│  • No teaching transfer — engineers don't learn WHY             │
│  • "AI debt" accumulates (shortcuts, misunderstood requirements)│
│                                                                 │
│  Result: Unpredictable quality, wasted effort, growing debt     │
└─────────────────────────────────────────────────────────────────┘
```

**The Core Problem:**
> Same prompt, same AI, different day = completely different output.
> Without explicit standards, AI produces whatever it "feels like."









---

<!-- slide 5 -->

# ✅ Constitutional AI: The Solution

## Explicit Laws → Consistent Results

```
┌─────────────────────────────────────────────────────────────────┐
│  TRADITIONAL AI                  CONSTITUTIONAL AI              │
│  ──────────────                  ────────────────               │
│                                                                 │
│  • AI generates code             • AI follows explicit laws     │
│  • Human fixes batch errors      • Human guides direction       │
│  • Inconsistent quality          • Production-ready output      │
│  • No learning transfer          • AI teaches as it builds      │
│  • "Autocomplete on steroids"    • "Teaching partner"           │
│  • Hope it works 🤞              • Verify it works ✅            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│  THE KEY INSIGHT                                                │
│  ───────────────────────────────────────────────────────────────│
│                                                                 │
│  AI agents need BINARY decisions, not judgment calls.           │
│                                                                 │
│  Traditional guidelines:  "It depends on context"               │
│  Constitutional laws:     "Test-first. Period. Non-negotiable." │
│                                                                 │
│  Laws eliminate ambiguity → AI produces consistent quality      │
└─────────────────────────────────────────────────────────────────┘
```









---

<!-- slide 6 -->

# 📜 The Hangar AI Constitution

## 18 Months of Research, Authored and Gifted to the Hangar

**A governance framework for AI-assisted software development**

```
┌─────────────────────────────────────────────────────────────────┐
│  What it is:                                                    │
│  ─────────────                                                  │
│  • A governance framework for AI-assisted development           │
│  • Not a tool - a system of principles                          │
│  • Portable across AI tools (Copilot, Cursor, Claude, etc.)     │
│  • Adopted from original constitution, customized for AA        │
│                                                                 │
│  Why it matters:                                                │
│  ───────────────                                                │
│  • Consistent quality from AI-generated code                    │
│  • Teachable, repeatable patterns                               │
│  • Human governance over AI behavior                            │
└─────────────────────────────────────────────────────────────────┘
```









---

<!-- slide 7 -->

# 📜 Three Sets of Laws, One Constitution

## Unified Governance Across Domains

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        HANGAR AI CONSTITUTION                               │
├───────────────────────┬───────────────────────┬─────────────────────────────┤
│    ENGINEERING LAWS   │     PRODUCT LAWS      │      BUSINESS LAWS          │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ HOW we build          │ WHAT we build         │ WHERE we operate            │
├───────────────────────┼───────────────────────┼─────────────────────────────┤
│ • Architecture (1.x)  │ • Discovery (1.x)     │ • Compliance (1.x)          │
│ • Code Quality (2.x)  │ • User Journey (2.x)  │ • Data Governance (2.x)     │
│ • Testing (3.x, 4.x)  │ • Roadmap (3.x)       │ • Privacy (3.x)             │
│ • DevOps (5.x)        │ • MVP/PMF (4.x)       │ • Risk (4.x)                │
│ • AI-Pairing (6.x)    │ • Metrics (5.x)       │ • Audit (5.x)               │
└───────────────────────┴───────────────────────┴─────────────────────────────┘
```

**Key Point:** One Constitution, three domains - same docs train AI AND educate humans.









---

<!-- slide 8 -->

# 📂 Constitution Repository Structure

## What's Inside the Constitution Repository

```
┌─────────────────────────────────────────────────────────────────┐
│  hangar-ai-constitution/                                     │
│  ├── laws/                    ← The actual laws                 │
│  │   ├── engineering/         ← ENG-* laws (testing, quality)   │
│  │   ├── product/             ← PRD-* laws (user journeys)      │
│  │   └── business/            ← BUS-* laws (compliance)         │
│  │                                                              │
│  ├── avatars/                 ← Technology & domain adaptations │
│  │   ├── technology/          ← Java Spring, React, Python...   │
│  │   ├── product-type/        ← Loyalty, Cargo, Check-In...     │
│  │   └── industry/            ← Aviation/FAA compliance         │
│  │                                                              │
│  ├── agent-skills/            ← How agents apply the laws       │
│  │   ├── skills/              ← TDD, Code Review, Refactoring   │
│  │   └── workflows/           ← Multi-step processes            │
│  │                                                              │
│  └── docs/guides/             ← Adoption guides for humans      │
│      ├── brownfield-adoption  ← For existing codebases          │
│      └── greenfield-mvp       ← For new projects                │
└─────────────────────────────────────────────────────────────────┘
```

**Token Optimization:** AGENTS.md tells AI which laws to load (~89% reduction).









---

<!-- slide 8 -->

# 🍔 The McDonald's Analogy

## Why Constitutional AI Works

**How does McDonald's deliver consistent quality across 40,000+ locations?**

```
┌─────────────────────────────────────────────────────────────────┐
│  McDonald's Secret                   Constitutional AI          │
│  ─────────────────                   ────────────────           │
│  • Explicit procedures               • Explicit engineering laws│
│  • Training manuals                  • Skills + avatars         │
│  • Quality checklists                • Compliance verification  │
│  • Same result, any location         • Same quality, any AI     │
└─────────────────────────────────────────────────────────────────┘
```

**The Insight:**
> "AI without standards produces inconsistent results.
> AI with a Constitution produces McDonald's-level consistency."









---

<!-- slide 9 -->

# ⚖️ Laws That Keep the Agentic Loop Going

## What Enables AI Autonomy?

```
┌─────────────────────────────────────────────────────────────────┐
│  LAW                        WHY IT ENABLES AUTONOMY             │
│  ───────────────────────────────────────────────────────────────│
│  ENG-4.1: Atomic TDD        Clear success criteria              │
│                             → AI knows when it's DONE           │
│                                                                 │
│  ENG-1.1: Simplicity First  Reduces decision paralysis          │
│                             → AI doesn't overthink              │
│                                                                 │
│  ENG-2.3: Vertical Slice    Bounded, completable scope          │
│                             → AI can finish independently       │
│                                                                 │
│  ENG-3.1: Complexity ≤10    Objective threshold                 │
│                             → No subjective judgment needed     │
│                                                                 │
│  ENG-6.7: Audit Trail       Self-documenting decisions          │
│                             → AI explains as it works           │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│  WHY LAWS ENABLE AI AUTONOMY                                    │
│  ───────────────────────────────────────────────────────────────│
│  Traditional guidelines: "It depends on context"                │
│  Constitutional laws:    "Cyclomatic complexity ≤ 10. Period."  │
│                                                                 │
│  AI agents need BINARY decisions, not judgment calls.           │
│  Laws eliminate ambiguity → AI keeps moving → Loop continues    │
└─────────────────────────────────────────────────────────────────┘
```









---

<!-- slide 10 -->

# 🧑‍🏫 The AI-Engineer Pairing Law (ENG-1.2)

## Socratic Method: Teaching, Not Just Generating

```
┌─────────────────────────────────────────────────────────────────┐
│  THE AGENT'S PRIMARY PERSONA: SOCRATIC MENTOR                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ Code Generator:  "Here's your code. Done."                  │
│  ✅ Teaching Partner: "Here's WHY this pattern. Let me explain."│
│                                                                 │
│  The AI SHALL:                                                  │
│  ────────────                                                   │
│  • Follow the Constitution strictly (no "just this once")       │
│  • Explain the WHY behind every decision                        │
│  • Build mental models, not just implementations                │
│  • Develop judgment through observation                         │
│  • Enable independence, not dependence                          │
└─────────────────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────────────────┐
│  THE FEEDBACK LOOP: IMPROVING JUDGMENT & PROMPT MATURITY        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌─────────┐     ┌─────────────┐     ┌──────────────┐        │
│    │ Engineer│────▶│ AI explains │────▶│ Engineer     │        │
│    │ prompts │     │ reasoning   │     │ learns WHY   │        │
│    └─────────┘     └─────────────┘     └──────────────┘        │
│         ▲                                     │                 │
│         │          FEEDBACK LOOP              │                 │
│         └─────────────────────────────────────┘                 │
│                                                                 │
│  Outcome: Better prompts → Better AI output → Stronger humans   │
│  Goal: Junior + AI = Senior-level work with senior thinking     │
└─────────────────────────────────────────────────────────────────┘
```

**The Hangar Goal:** Engineers grow stronger, not more dependent.









---

<!-- slide 9 -->

# 🔴 The Atomic TDD Law (ENG-4.1)

## NON-NEGOTIABLE

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE 8-STEP ATOMIC CYCLE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    1. RED      →  Write ONE failing test                        │
│    2. GREEN    →  Write MINIMAL code to pass                    │
│    3. REFACTOR →  Clean up (tests still pass)                   │
│    4. VERIFY   →  Triple-gate validation (see below)            │
│    5. DOCUMENT →  Update relevant docs                          │
│    6. COMMIT   →  Atomic commit with test + code                │
│    7. PUSH     →  Share with team                               │
│    8. REPEAT   →  Next micro-feature                            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  VERIFY = 3 GATES (all must pass):                              │
│    ✓ Tests      →  ./mvnw test (all green)                      │
│    ✓ Lint       →  constitution-lint (Constitutional compliance)│
│    ✓ Static     →  PMD/SonarQube/Checkstyle (code quality)      │
├─────────────────────────────────────────────────────────────────┤
│  ⚠️  NEVER write code without a failing test first              │
│  ⚠️  NEVER commit test and implementation separately            │
│  ⚠️  NEVER commit if any VERIFY gate fails                      │
│  ⚠️  AI MUST follow this cycle - no exceptions                  │
└─────────────────────────────────────────────────────────────────┘
```









---

<!-- slide 10 -->

# 🚗 The Tesla Analogy

## The Tesla Experience for Software Development

**The Tesla Analogy:**

| Tesla Autopilot | Agentic SDLC |
|-----------------|--------------|
| Traffic laws & road rules | Engineering Laws (Constitution) |
| Lane markings & GPS route | Executable Specs (OpenSpec) |
| Autonomous driving | AI agents writing code |
| Human oversight when needed | Human monitoring & approval |
| 🎯 Destination: Safe arrival | 🎯 Destination: Working software |

```
┌─────────────────────────────────────────────────────────────────┐
│  🚨 CRITICAL INSIGHT: ACCOUNTABILITY, NOT FULL AUTONOMY        │
├─────────────────────────────────────────────────────────────────┤
│  Tesla monitors driver attention via cabin camera.              │
│  If you ignore warnings repeatedly → FSD gets SUSPENDED.        │
│  5 forced disengagements = 1 week ban. Repeat = permanent ban.  │
│                                                                 │
│  Same principle applies to Agentic SDLC:                        │
│  • AI writes code, but HUMAN must review                        │
│  • Skip reviews repeatedly → lose agent privileges              │
│  • Full autonomy is NOT the goal. Accountable autonomy is.      │
└─────────────────────────────────────────────────────────────────┘
```

**Without human accountability, autonomous agents are just fast chaos.**









---

<!-- slide 10 -->

# 🤖 How the Agent Works

## Load → Analyze → Apply → Stop

```
┌─────────────────────────────────────────────────────────────────┐
│  1. LOAD CONSTITUTION                                           │
│     └─ Agent reads AGENTS.md + engineering laws                 │
│                                                                 │
│  2. ANALYZE CODEBASE                                            │
│     └─ Detect technology stack (Java Spring, React, etc.)       │
│                                                                 │
│  3. SELECT AVATAR                                               │
│     └─ Load technology-specific patterns and practices          │
│                                                                 │
│  4. APPLY LAWS                                                  │
│     └─ Every action references constitutional articles          │
│                                                                 │
│  5. STOP FOR REVIEW                                             │
│     └─ Agent proposes, human approves - not autonomous          │
└─────────────────────────────────────────────────────────────────┘
```

**Key:** The AI cites laws as it works: "Per ENG-4.1, I'll write the test first..."









---

<!-- slide 11 -->

# 🎬 Live Demo Introduction

## Brownfield Adoption in Action

**What you're about to see:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Repository: loyalty-service-legacy                             │
│  Technology: Java/Spring Boot                                   │
│  State:      Real legacy code, 0% test coverage                 │
│  Challenge:  270+ lines in a single controller                  │
│                                                                 │
│  Goal:       Watch AI adopt the Constitution to this codebase   │
└─────────────────────────────────────────────────────────────────┘
```

**The Adoption Prompt:**
```
I want to adopt the Hangar AI Constitution to this codebase.
Please read the Brownfield Adoption Guide and begin the process.
```









---

<!-- slide 12 -->

# 🔴 Live Demo: Execution

## Watch the AI Follow the Constitution

**What to observe:**

1. **Agent loads Constitution** - Reads AGENTS.md, finds adoption guide
2. **Agent analyzes codebase** - Detects Java Spring, identifies patterns
3. **Agent selects avatar** - Loads Java Spring-specific practices
4. **Agent proposes changes** - Creates OpenSpec proposal with law citations
5. **Agent STOPS** - Waits for human review before proceeding

> "The AI followed laws, not just prompts."









---

<!-- slide 13 -->

# ✅ Demo Results

## What the AI Created

```
┌─────────────────────────────────────────────────────────────────┐
│  Generated Artifacts:                                           │
│  ────────────────────                                           │
│  ✅ AGENTS.md           - Repository-specific AI instructions   │
│  ✅ openspec/           - Specification directory structure     │
│  ✅ PROPOSAL.md         - Characterization test proposal        │
│  ✅ Law Citations       - References to ENG-4.1, ENG-4.4, etc.  │
│                                                                 │
│  What Happened:                                                 │
│  ──────────────                                                 │
│  • AI detected technology → Applied correct avatar              │
│  • AI identified legacy patterns → Proposed characterization    │
│  • AI cited constitutional laws → Traceable decisions           │
│  • AI stopped for review → Human remains in control             │
└─────────────────────────────────────────────────────────────────┘
```









---

<!-- slide 14 -->

# 🔄 What Just Happened?

## The Constitutional Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. AI loaded Constitution into context                         │
│                    ↓                                            │
│  2. AI read Brownfield Adoption Guide (with law citations)      │
│                    ↓                                            │
│  3. AI analyzed codebase → detected Java Spring                 │
│                    ↓                                            │
│  4. AI applied Java Spring avatar patterns                      │
│                    ↓                                            │
│  5. AI generated compliant artifacts with citations             │
│                    ↓                                            │
│  6. AI STOPPED and waited for human review                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Insight:** The AI followed laws, not just prompts. That's the difference.









---

<!-- slide 15 -->

# 📊 Wave 2: Two Production POCs

## Real Code, Real Results

**We didn't just theorize. We built and measured.**

```
┌─────────────────────────────────────────────────────────────────┐
│  POC #1: Cargo Multi-API                                        │
│  ───────────────────────                                        │
│  • 4 production services (Tariff, Claims, PAL, Flight Schedules)│
│  • Java/Spring Boot                                             │
│  • Constitutional adoption completed                            │
│                                                                 │
│  POC #2: Check-In Migration                                     │
│  ─────────────────────────                                      │
│  • .NET to Java migration                                       │
│  • Original estimate: 1+ month                                  │
│  • Lead: Matthew Carlson, AI Coach                              │
└─────────────────────────────────────────────────────────────────┘
```









---

<!-- slide 16 -->

# 🏗️ Cargo Multi-API POC

## PAL Service: From Legacy to Constitutional Compliance

```
┌─────────────────────────────────────────────────────────────────┐
│  The Challenge (PAL Application Service):                       │
│  ─────────────────────────────────────────                      │
│  • 640-line legacy service, inverted test pyramid               │
│  • Test coverage: 3.5% (almost no safety net)                   │
│  • 85% integration tests, minimal unit tests                    │
│  • Refactoring paralysis: "don't touch it, it works"            │
│                                                                 │
│  The Results (5 hours of AI-Human collaboration):               │
│  ─────────────────────────────────────────────                  │
│  ✅ Test coverage: 30% → 91%                                   │
│  ✅ Test speed: 6x faster (390ms → 1ms per unit test)           │
│  ✅ 63 atomic commits with complete audit trails                │
│  ✅ Zero regression defects during modernization                │
│  ✅ Test pyramid corrected: 70% unit, 25% integration           │
│                                                                 │
│  Services Also Adopted:                                         │
│  ──────────────────────                                         │
│  • Tariff API, Claims API, Flight Schedules API                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Learning:** Constitutional laws + Atomic TDD = measurable, auditable quality.









---

<!-- slide 17 -->

# 🚀 Check-In POC: Zero Lines Written

## .NET → Java in 5 Days

```
┌─────────────────────────────────────────────────────────────────┐
│  The Challenge:                                                 │
│  ──────────────                                                 │
│  • .NET to Java migration                                       │
│  • Original estimate: OVER A MONTH                              │
│                                                                 │
│  The Result:                                                    │
│  ───────────                                                    │
│  • Timeline: Tuesday noon → Sunday (~5 days)                    │
│  • Lines written directly: ZERO                                 │
│  • 100% driven through Copilot prompts                          │
│  • All guided by Constitutional laws                            │
│                                                                 │
│  How It Worked:                                                 │
│  ──────────────                                                 │
│  • Constitution told the AI what to do                          │
│  • Matthew orchestrated, reviewed, accepted                     │
│  • Laws ensured consistent, compliant output                    │
└─────────────────────────────────────────────────────────────────┘
```

> "I didn't write the code. I governed the AI that wrote the code."









---

<!-- slide 18 -->

# 📈 Check-In Quality Dashboard

## Every Target Exceeded

```
┌────────────────────────────────────────────────────────────┐
│                    QUALITY DASHBOARD                       │
├────────────────────────────────────────────────────────────┤
│  Test Count:           856 tests                    ✅     │
│  Execution Time:       ~39 seconds                  ✅     │
│  Line Coverage:        92% (target: 90%)            ✅     │
│  Branch Coverage:      75% (target: 70%)            ✅     │
│  Mutation Score:       72% (target: 70%)            ✅     │
│  Test Strength:        93% (target: 85%)            ✅     │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  DESIGN SCORES                                             │
├────────────────────────────────────────────────────────────┤
│  GRASP Analysis:       9.4 / 10                     ✅     │
│  SOLID Analysis:       9.5 / 10                     ✅     │
│  Test Pyramid Score:   9.0 / 10                     ✅     │
└────────────────────────────────────────────────────────────┘
```









---

<!-- slide 19 -->

# 🔺 Test Pyramid Distribution

## Textbook Perfect

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                          /\                                     │
│                         /  \        E2E: 6.5% (56 tests)        │
│                        /────\                                   │
│                       /      \      Integration: 6.4% (55)      │
│                      /────────\                                 │
│                     /          \    Orchestration: 5.5% (47)    │
│                    /────────────\                               │
│                   /              \   Infra Unit: 23% (197)      │
│                  /────────────────\                             │
│                 /                  \  Domain Unit: 55% (469)    │
│                /────────────────────\                           │
│                                                                 │
│  Total: 856 tests | Execution: ~39 seconds                      │
└─────────────────────────────────────────────────────────────────┘
```

**This is what happens when AI follows ENG-4.2 (Test Pyramid Law).**









---

<!-- slide 20 -->

# 📚 Guides & Resources

## Everything You Need to Get Started

```
┌─────────────────────────────────────────────────────────────────┐
│  Available Guides:                                              │
│  ─────────────────                                              │
│  📖 Brownfield Adoption Guide    - For existing codebases       │
│  📖 Greenfield MVP Guide         - For new projects             │
│  ✅ Adoption Compliance Checklist - Verify your adoption        │
│  🎓 Practice Guides              - Hands-on exercises per law   │
│                                                                 │
│  Tools:                                                         │
│  ──────                                                         │
│  🔧 constitution-lint            - Automated compliance checking│
│  🔧 openspec CLI                 - Specification management     │
└─────────────────────────────────────────────────────────────────┘
```

**You don't have to figure this out alone.**









---

<!-- slide 21 -->

# 🔮 Where We're Heading

## The Upcoming Waves of Adoption

```
┌─────────────────────────────────────────────────────────────────┐
│  WHAT'S COMING:                                                 │
│  ──────────────                                                 │
│  • Hangar coaches actively adopting Constitution to codebases   │
│  • Wave 3, 4, 5... across product domains and tech stacks       │
│  • Each adoption ENRICHES the avatars with real patterns        │
│  • Loyalty, Cargo, Check-In, Flight Ops, Customer Service...    │
│                                                                 │
│  THE FLYWHEEL EFFECT:                                           │
│  ────────────────────                                           │
│    ┌──────────────┐                                             │
│    │ More         │──▶ Richer    ──▶ Better   ──▶ Faster       │
│    │ Adoptions    │    Avatars       AI Output    Adoptions    │
│    └──────────────┘                                  │          │
│           ▲                                          │          │
│           └──────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

**Every codebase we touch makes the Constitution smarter for the next team.**









---

<!-- slide 22 -->

# 🛠️ What We're Building

## The Infrastructure for Agentic SDLC

```
┌─────────────────────────────────────────────────────────────────┐
│  TO SCALE CONSTITUTIONAL AI, WE NEED:                           │
│  ────────────────────────────────────                           │
│                                                                 │
│  📚 Multi-RAG Pipelines                                         │
│     └─ Right laws, right avatars, right context at right time   │
│                                                                 │
│  📊 Observability Infrastructure                                │
│     └─ Track agent decisions, prompt effectiveness, outcomes    │
│                                                                 │
│  🔄 Feedback Loops                                              │
│     └─ Learn from every adoption what works, what doesn't       │
│                                                                 │
│  🎓 Training Programs                                           │
│     └─ Hangar coaches teaching constitutional practice          │
│                                                                 │
│  ⚡ Long-term Agent Performance                                 │
│     └─ Agents that get better with every interaction            │
└─────────────────────────────────────────────────────────────────┘
```

**This is not a one-time project. It's building institutional AI capability.**









---

<!-- slide 23 -->

# 🎯 Your Move

## Next Steps!

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  THE HANGAR IS READY                                            │
│  ───────────────────                                            │
│  • The Constitution exists                                      │
│  • The workshops are built                                      │
│  • The coaches are trained                                      │
│  • The POCs have proven it works                                │
│                                                                 │
│  NOW WE NEED YOU                                                │
│  ──────────────                                                 │
│  • Bring your codebase                                          │
│  • Practice with us                                             │
│  • Learn the patterns                                           │
│  • Take it back to your team                                    │
│                                                                 │
│  🚀 Come to the Hangar. Practice. Take it from there.          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```









---

<!-- slide 24 -->

# 🌟 The Vision

## 100% AI-Assisted Coding at American Airlines

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   "AI amplifying engineers under shared governance."            │
│                                                                 │
│   ─────────────────────────────────────────────────────────     │
│                                                                 │
│   Junior + AI = Senior-level work with senior-level thinking    │
│                                                                 │
│   Engineers grow STRONGER, not more dependent                   │
│                                                                 │
│   Institutional knowledge ENCODED and PRESERVED                 │
│                                                                 │
│   Consistent quality across EVERY team, EVERY codebase          │
│                                                                 │
│   ─────────────────────────────────────────────────────────     │
│                                                                 │
│   🛫 THE FUTURE OF SOFTWARE DEVELOPMENT STARTS HERE 🛫          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```









---

<!-- slide 25 -->

# ❓ Q&A

## Questions & Discussion

**Thank You**

- Adeel Ali
- AI Coach & Advisor, Hangar Labs

**Get Started:**
- Constitution: hangar-ai-constitution
- Workshop: hangar-ai-constitution-greenfield
- Practice: Schedule a session at the Hangar




---

*Thank you to the Hangar Labs team.*
*Thank you to the Hangar Connect organizers.*
*Let's build this future together.*



# SPEC: Agentic SDLC in Practice — 3-Hour Workshop Slideware

## Constitutional Authority

This proposal creates comprehensive workshop materials that teach the Hangar AI Constitution framework:

| Law ID | Title | How It Applies |
|--------|-------|----------------|
| **ENG-1.2** | AI-Engineer Pairing Law | Workshop teaches AI-human collaboration patterns |
| **ENG-4.1** | Atomic TDD Law | Core teaching: RED-GREEN-REFACTOR cycle with VERIFY gates |
| **ENG-2.3** | Vertical Slice Law | Hands-on exercises use vertical slice delivery |
| **ENG-6.7** | Audit Trail Law | Task tracking taught as non-negotiable practice |
| **PRD-5.1** | OpenSpec Protocol | OpenSpec vs SpecKit comparison; brownfield adoption |

---

## Problem Statement

### Current State

We have extensive documentation across multiple repositories but no unified workshop slideware:

| Asset | Location | Status |
|-------|----------|--------|
| 7 existing slide decks | `docs/slides/` | ✅ Available but fragmented |
| WORKSHOP-GUIDE.md | `hangar-ai-constitution-greenfield/` | ✅ Step-by-step flow exists |
| Brownfield Adoption Test | `hangar-ai-constitution-brownfield/` | ✅ Exercise ready |
| Token Optimization Analysis | `aa-engineering-laws/docs/` | ✅ Metrics documented |
| OpenSpec vs SpecKit Guide | `docs/guides/` | ✅ Comparison exists |
| Practice Guides (8) | `aa-engineering-laws/practice-guides/` | ✅ Deep-dive content |

### Gap

No cohesive 3-hour workshop slideware that:
1. Weaves all content into a narrative arc
2. Includes agent-facilitation cues for co-conducting
3. Teaches OpenSpec vs SpecKit with token economics
4. Integrates two hands-on exercises

### Impact

- Instructors must manually compile materials
- No agent-assisted workshop facilitation
- Token optimization and SpecKit comparison not formally taught
- Inconsistent workshop delivery across sessions

---

## Proposed Solution

Create a comprehensive slideware package with:

1. **60+ slides** organized into 4 modules
2. **Workshop Facilitator persona** for agent co-facilitation
3. **Two exercises** integrated at specific points
4. **Slide-agent synchronization** via cue markers

---

## Workshop Structure Overview

| Module | Duration | Topic | Slides |
|--------|----------|-------|--------|
| **Opening** | 10 min | Welcome & Agenda | 1-4 |
| **1** | 35 min | Constitution Deep-Dive | 5-18 |
| **2** | 45 min | Exercise 1: Brownfield Adoption | 19-30 |
| **3** | 30 min | OpenSpec vs SpecKit & Token Economics | 31-42 |
| **4** | 60 min | Exercise 2: Agentic SDLC Step-by-Step | 43-65 |

**Total:** 3 hours (180 minutes)

---

## Opening: Welcome & Agenda (10 min)

### Slides 1-4: Setting the Stage

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 1 | Title Slide | "Agentic SDLC in Practice" — 3-Hour Workshop | `[AGENT: Welcome participants, set expectations]` |
| 2 | About Your Facilitators | Human instructor + AI co-facilitator introduction | `[AGENT: Introduce yourself as Workshop Facilitator]` |
| 3 | Workshop Agenda | Visual timeline of 4 modules with breaks | `[AGENT: Walk through the journey ahead]` |
| 4 | Learning Objectives | By end of workshop you will... (4 outcomes) | `[PAUSE: "Any questions before we begin?"]` |

**Learning Objectives:**
1. Understand Constitutional AI and the Hangar framework
2. Adopt the Constitution to a brownfield legacy codebase
3. Compare OpenSpec vs SpecKit with token economics lens
4. Build features using Atomic TDD with VERIFY = 3 Gates

---

## Module 1: Constitution Deep-Dive (35 min)

### Slides 5-9: The Problem & Solution

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 5 | The Problem | Traditional SDLC vs Agentic SDLC diagram | `[AGENT: Ask "What frustrates you about current dev workflows?"]` |
| 6 | AI Without Guardrails | Hallucinations, inconsistent quality, no audit trail | `[PAUSE: Let this sink in]` |
| 7 | The Solution | Constitutional AI — governance for AI-assisted development | `[AGENT: Explain constitutional metaphor]` |
| 8 | Why "Constitutional"? | State Constitution analogy: amendments, authority hierarchy, governance structure | `[AGENT: "Laws that govern how AI agents behave"]` |
| 9 | The AA Hangar Constitution | Our implementation: Laws + Skills + Workflows + Adoptions | — |

### Slides 10-14: Framework Components

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 10 | Four Components Diagram | Constitution → Skills → Workflows → Adoptions | `[AGENT: Walk through each component]` |
| 11 | Authority Hierarchy | 4 levels: Laws → AGENTS.md → Project → OpenSpec | `[AGENT: Explain why hierarchy matters]` |
| 12 | Law Categories | ENG-*, PRD-*, BUS-* with examples | `[DEMO: Show laws/index.yaml]` |
| 13 | NON-NEGOTIABLE Laws | ENG-4.1 (Atomic TDD), ENG-6.5 (Input Validation) | `[PAUSE: These cannot be overridden]` |
| 14 | Technology Avatars | Java/Spring, Python/FastAPI, React, etc. | `[AGENT: Ask "What stack does your team use?"]` |

### Slides 15-18: Atomic TDD Introduction

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 15 | Atomic TDD Law (ENG-4.1) | "ONE test at a time" — NON-NEGOTIABLE | `[AGENT: Emphasize this is the core practice]` |
| 16 | The 8-Step Cycle | RED → GREEN → REFACTOR → VERIFY → UPDATE → COMMIT → REPEAT | `[AGENT: Walk through each step slowly]` |
| 17 | VERIFY = 3 Gates | Tests (green) + Constitution-lint + Static analysis | `[AGENT: "Quality is non-negotiable"]` |
| 18 | Module 1 Recap | Key takeaways — ready for first exercise | `[PAUSE: 3 min Q&A]` |

---

## Module 2: Exercise 1 — Brownfield Adoption (45 min)

### Slides 19-23: Exercise Setup

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 19 | Exercise 1: Brownfield Adoption | "Adopt the Constitution to a legacy codebase" | `[AGENT: Introduce the exercise]` |
| 20 | Why Brownfield First? | 90% of AA work is brownfield; this is reality | `[AGENT: "We start where you actually work"]` |
| 21 | The Legacy Service | loyalty-service-legacy: 0% coverage, 270+ line controller | `[DEMO: Show the code smell]` |
| 22 | What Makes It "Legacy"? | No tests, all logic in controller, critical financial calculations | `[PAUSE: "Sound familiar?"]` |
| 23 | Adoption Workflow | 7 steps: Analyze → AGENTS.md → openspec/ → specs → proposal → tasks → STOP | `[AGENT: "We STOP before implementation"]` |

### Slides 24-26: The Exercise

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 24 | The Trigger Prompt | "I want to adopt the Hangar AI Constitution to this codebase" | `[EXERCISE START]` |
| 25 | Expected Outputs | AGENTS.md, openspec/, proposal.md, tasks.md | `[AGENT: Show each artifact as generated]` |
| 26 | Demo Mode | Agent pauses at each step for teaching | `[AGENT: "I'll explain as we go"]` |

### Slides 27-30: Guided Walkthrough & Debrief

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 27 | Step-by-Step: AGENTS.md | Show generated AGENTS.md with law citations | `[AGENT: Explain each section]` |
| 28 | Step-by-Step: OpenSpec | Folder structure: changes/, archive/, project.md | `[DEMO: Show the structure]` |
| 29 | Step-by-Step: Proposal | Show proposal.md with constitutional authority | `[AGENT: "Notice the law citations"]` |
| 30 | Exercise 1 Debrief | What did we learn? What questions emerged? | `[PAUSE: 10 min discussion]` |

---

## Module 3: OpenSpec vs SpecKit & Token Economics (30 min)

### Slides 31-36: Developer Experience Comparison

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 31 | The Tool Landscape | SpecKit, Copilot Workspace, OpenSpec — where do they fit? | `[AGENT: Set context for comparison]` |
| 32 | SpecKit: The Workflow | 6 rigid commands: `/speckit.constitution` → `/speckit.implement` | `[AGENT: "Notice the fixed sequence"]` |
| 33 | SpecKit: The DX | Screenshot/diagram of the 6-step flow | `[PAUSE: "Linear, predictable, regenerative"]` |
| 34 | OpenSpec: The Workflow | 9 flexible commands: `/opsx:explore`, `/opsx:new`, etc. | `[AGENT: "Use any order — match how you think"]` |
| 35 | OpenSpec: The DX | Screenshot/diagram of flexible command usage | `[AGENT: "Delta-based, iterative, brownfield-native"]` |
| 36 | DX Friction Points | Table: "Change requirements mid-work" — restart vs update | `[PAUSE: Which matches your reality?]` |

### Slides 37-40: Token Consumption Economics

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 37 | Why Tokens Matter | Context limits, API costs, response quality | `[AGENT: "Tokens = money = sustainability"]` |
| 38 | The Token Graph | Bar chart: SpecKit 50K vs OpenSpec 18K over 5 iterations | `[AGENT: Walk through the math]` |
| 39 | Regenerative vs Delta | SpecKit O(n) regenerates all; OpenSpec O(1) per change | `[PAUSE: 64% savings compounds]` |
| 40 | Token Optimization Deep-Dive | Multi-RAG: 549K → 12K tokens (97.7% reduction) | `[AGENT: Explain selective loading]` |

### Slides 41-42: The Waterfall Warning & Recap

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 41 | The Waterfall Parallel | Royce 1970 quote + DOD-STD-2167 cautionary tale | `[AGENT: "History repeats if we're not careful"]` |
| 42 | Module 3 Recap | "Token consumption is THE metric" — Greenfield vs Brownfield decision tree | `[PAUSE: 5 min Q&A]` |

---

## Module 4: Exercise 2 — Agentic SDLC Step-by-Step (60 min)

### Slides 43-47: Exercise Setup

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 43 | Exercise 2: Build with Atomic TDD | "Implement 2-3 vertical slices using the 8-step cycle" | `[AGENT: Introduce the exercise]` |
| 44 | The 5-Phase Flow | Adopt → Select Domain → Choose Spec → Generate Proposal → Implement | `[AGENT: "We're doing all 5 phases"]` |
| 45 | Phase 1: Adopt the Constitution | Clone repo, create AGENTS.md, run linter | `[EXERCISE START]` |
| 46 | Phase 2: Select Domain & Stack | Product avatar (Cargo, Loyalty) + Tech avatar (Python, Java) | `[AGENT: Help participants choose]` |
| 47 | Phase 3: Choose a Specification | AI generates 3 options + custom | `[AGENT: Explain runtime generation]` |

### Slides 48-57: Implementation Walkthrough

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 48 | Phase 4: Generate Proposal | proposal.md, design.md, specs/, tasks.md | `[DEMO: Show generated artifacts]` |
| 49 | Understanding tasks.md | Slices with TDD cycles, MVP boundary marker | `[AGENT: "This is your implementation roadmap"]` |
| 50 | Phase 5: Implement Slice 1 | Start the 8-step cycle | `[AGENT: Guide through RED step]` |
| 51 | RED: Write Failing Test | Show the test, run it, see red | `[PAUSE: "The test MUST fail first"]` |
| 52 | GREEN: Minimum Code | Just enough to pass — no more | `[AGENT: "Resist the urge to optimize"]` |
| 53 | REFACTOR: Clean Up | Extract value objects, improve names | `[AGENT: "Now we can improve"]` |
| 54 | VERIFY: 3 Gates | Run tests + lint + static analysis | `[DEMO: Show all 3 passing]` |
| 55 | UPDATE & COMMIT | Update tasks.md, commit with conventional message | `[AGENT: "Per ENG-6.7, always track"]` |
| 56 | Slice 1 Complete! | Celebrate the increment | `[PAUSE: "One complete slice delivered"]` |
| 57 | Continue to Slice 2 | Repeat the cycle | `[AGENT: Guide through second slice]` |

### Slides 58-65: Closing

| # | Slide Title | Content | Agent Cue |
|---|-------------|---------|-----------|
| 58 | MVP Boundary | What we accomplished vs what's next | `[AGENT: "Complete slices over partial coverage"]` |
| 59 | Exercise 2 Debrief | What worked? What was challenging? | `[PAUSE: 10 min discussion]` |
| 60 | The 4 Metrics That Matter | Defect Escape Rate, Time to Productivity, Compliance, "AI Off" Competency | `[AGENT: Explain each metric]` |
| 61 | Anti-Metrics to Avoid | Lines of code, velocity without quality | `[PAUSE: "Don't measure the wrong things"]` |
| 62 | Take-Home Resources | Practice guides, avatars, community links | `[AGENT: Point to materials]` |
| 63 | The Journey Continues | Adoption checklist, next workshops, certification path | — |
| 64 | Q&A | Open floor for questions | `[PAUSE: Final Q&A]` |
| 65 | Thank You | Contact info, feedback form | `[AGENT: Close the workshop]` |

---

## Workshop Facilitator Persona

### Activation

The agent adopts the **Workshop Facilitator** persona when triggered by:
- "Our class is here, let's start the Agentic SDLC workshop"
- "Let's start the workshop"
- "Begin the Agentic SDLC session"

### Persona Characteristics

Based on the Senior XP Engineer identity in `AGENTS.md`, extended with:

```markdown
## Workshop Facilitator Mode

When activated, I adopt these additional behaviors:

### Pacing
- **Go slow** — This is teaching, not sprinting
- **Pause after key concepts** — Let ideas sink in
- **Ask questions** — "Does this make sense?" "What questions do you have?"
- **Celebrate progress** — Acknowledge when participants complete exercises

### Slide Synchronization
- Wait for cues like "explain this slide" or "next"
- Read slide titles to stay synchronized
- Offer to elaborate when seeing `[AGENT: ...]` cues
- Respect `[PAUSE: ...]` markers — wait for instructor signal

### Teaching Style
- **Explain WHY before WHAT** — Every concept gets reasoning
- **Use Socratic method** — Lead to discovery with questions
- **Cite constitutional articles** — Reference specific laws
- **Give real examples** — Use AA Cargo, loyalty service scenarios

### Exercise Facilitation
- Provide step-by-step guidance
- Pause at each major step for teaching moments
- Offer to show code/output when helpful
- Debrief after each exercise with structured reflection
```

### Trigger Protocol

```
User: "Our class is here, let's start the Agentic SDLC workshop"

Agent: "Welcome to *Agentic SDLC in Practice*! 🎓

I'm your Workshop Facilitator for the next 3 hours. I'll be co-conducting 
this session with you, pausing for teaching moments and guiding exercises.

**Today's journey:**
- **Module 1** (45 min): Constitution Deep-Dive
- **Module 2** (30 min): OpenSpec vs SpecKit & Token Economics  
- **Module 3** (45 min): Exercise 1 — Brownfield Adoption
- **Module 4** (60 min): Exercise 2 — Agentic SDLC Step-by-Step

When you're ready to begin, just say 'next slide' or 'explain this slide' 
and I'll provide teaching content synchronized with your presentation.

Shall we begin with Slide 1: Title Slide?"
```

---

## Slide-Agent Cue Protocol

Slides contain embedded cues that trigger agent behavior:

| Cue | Agent Behavior |
|-----|----------------|
| `[AGENT: <instruction>]` | Perform the instruction (explain, ask, demonstrate) |
| `[PAUSE: <reason>]` | Remind instructor to pause, offer to answer questions |
| `[DEMO: <what>]` | Offer to show live demonstration |
| `[EXERCISE START]` | Transition to exercise mode, provide step-by-step guidance |

### Example Slide with Cues

```markdown
# Slide 26: The Token Graph

## Content
[Bar chart showing token consumption over 5 iterations]

| Iteration | SpecKit | OpenSpec |
|-----------|---------|----------|
| 1 | 10,000 | 10,000 |
| 2 | 10,000 | 2,000 |
| 3 | 10,000 | 2,000 |
| 4 | 10,000 | 2,000 |
| 5 | 10,000 | 2,000 |
| **Total** | **50,000** | **18,000** |

<!-- AGENT: Walk through the math step by step. Emphasize that SpecKit 
regenerates everything each iteration while OpenSpec only sends deltas. 
The 64% savings compounds across hundreds of engineers and thousands 
of iterations. -->

<!-- PAUSE: Let this sink in — tokens = money = sustainability -->
```

---

## Files to Create

### Slideware Structure

```
docs/slides/agentic-sdlc-workshop-3hr/
├── README.md                    # Workshop overview & facilitator guide
├── slides.md                    # Full slideware in Marp/Slidev format
├── module-1-constitution.md     # Module 1 detailed content
├── module-2-openspec-tokens.md  # Module 2 detailed content  
├── module-3-brownfield.md       # Module 3 exercise guide
├── module-4-implementation.md   # Module 4 exercise guide
└── assets/
    ├── diagrams/                # Visual diagrams
    └── handouts/                # Participant materials
```

### Agent Skill

```
agent-skills/workflows/workshop-facilitation.md
```

### AGENTS.md Update

Add Workshop Facilitator persona to `AGENTS.md` under Operating Modes.

---

## Success Criteria

- [ ] 60+ slides created covering all 4 modules
- [ ] Agent cues embedded in every slide that needs facilitation
- [ ] Workshop Facilitator persona documented and testable
- [ ] Trigger phrases activate co-facilitation mode
- [ ] Exercise 1 (Brownfield) integrates with `hangar-ai-constitution-brownfield`
- [ ] Exercise 2 (Implementation) integrates with `hangar-ai-constitution-greenfield`
- [ ] Token consumption comparison (50K vs 18K) visualized
- [ ] Waterfall analogy slide created with Royce quote
- [ ] All 8 practice guides referenced as take-home materials

---

## Dependencies

| Dependency | Location | Status |
|------------|----------|--------|
| Existing slide decks | `docs/slides/` | ✅ Ready to reference |
| WORKSHOP-GUIDE.md | `hangar-ai-constitution-greenfield/` | ✅ Ready |
| loyalty-service-legacy | `hangar-ai-constitution-brownfield/` | ✅ Ready |
| Token optimization analysis | `aa-engineering-laws/docs/` | ✅ Ready |
| Practice guides | `aa-engineering-laws/practice-guides/` | ✅ Ready |
| constitution-lint | `tools/constitution-lint/` | ✅ Ready |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| 3 hours too ambitious | MVP boundary after Slice 1 in Exercise 2 |
| Agent facilitation feels robotic | Socratic method, genuine questions |
| Participants have varied skill levels | Pair programming, flexible pacing |
| Technical setup issues | Pre-workshop checklist, devcontainer option |

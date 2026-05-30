# 🛠️ Agentic SDLC in Practice — 3-Hour Workshop

> **Self-Paced Learning Guide & Facilitator Manual**

---

## 🎯 How to Use This Guide

This workshop can be run in **three modes**:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  🎓 MODE 1: INSTRUCTOR-LED (In-Class)                          │
│  ────────────────────────────────────                          │
│  Human instructor + AI co-facilitator                          │
│  Trigger: "Our class is here, let's start the Agentic SDLC     │
│           workshop"                                            │
│                                                                 │
│  📖 MODE 2: SELF-PACED LEARNING (Solo)                         │
│  ────────────────────────────────────                          │
│  You + AI tutor working through material                       │
│  Trigger: "Help me learn this workshop"                        │
│                                                                 │
│  🔄 MODE 3: REVIEW/PRACTICE (Post-Workshop)                    │
│  ─────────────────────────────────────────                     │
│  Revisit specific modules or exercises                         │
│  Trigger: "Help me practice [module name]"                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Self-Learning)

### Step 1: Setup Your Environment

```bash
# Clone the required repositories
git clone <hangar-ai-constitution-repo>
git clone <hangar-ai-constitution-brownfield-repo>
git clone <hangar-ai-constitution-greenfield-repo>

# Install constitution-lint
npm install -g @anthropic/constitution-lint

# Verify installation
npx constitution-lint --version
```

### Step 2: Open This Folder in VS Code/Cursor

```bash
cd hangar-ai-constitution
code .
```

### Step 3: Start Learning!

Say this to your AI assistant (GitHub Copilot, Claude, etc.):

```
Help me learn this workshop
```

Or be more specific:

```
Help me learn this workshop - I want to understand Constitutional AI
and practice the Atomic TDD cycle. Guide me through the material at
my own pace, pausing to check my understanding.
```

**The AI will:**
- Walk you through each module
- Explain concepts with examples
- Guide you through hands-on exercises
- Quiz you on key concepts
- Adjust pace based on your responses

---

## 📋 Workshop Overview

| Attribute | Value |
|-----------|-------|
| **Duration** | ~3 hours (flexible for self-paced) |
| **Audience** | Developers, Tech Leads, Architects |
| **Prerequisites** | Basic Git, IDE familiarity |
| **Mode** | Instructor-led OR Self-paced |

---

## 🎯 Learning Objectives

By the end of this workshop, you will:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1️⃣  UNDERSTAND Constitutional AI                               │
│      └─ The Hangar framework: Laws → Skills → Workflows         │
│      └─ Authority hierarchy & NON-NEGOTIABLE laws               │
│                                                                 │
│  2️⃣  ADOPT the Constitution to Brownfield Code                  │
│      └─ 7-step adoption workflow                                │
│      └─ Generate constitutional artifacts with law citations    │
│                                                                 │
│  3️⃣  COMPARE OpenSpec vs SpecKit                                │
│      └─ Developer experience & token economics                  │
│      └─ When to use which (greenfield vs brownfield)            │
│                                                                 │
│  4️⃣  BUILD with Atomic TDD                                      │
│      └─ The 8-step cycle: RED → GREEN → REFACTOR → VERIFY       │
│      └─ VERIFY = 3 Gates (Tests + Lint + Static Analysis)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 Agenda & Module Map

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ⏱️  OPENING                                            10 min  │
│      └─ Welcome, introductions, learning objectives             │
│                                                                 │
│  📜 MODULE 1: Constitution Deep-Dive                    35 min  │
│      └─ Laws, skills, workflows, authority hierarchy            │
│      └─ Atomic TDD & VERIFY = 3 Gates                           │
│                                                                 │
│  🛠️  MODULE 2: Brownfield Adoption                      45 min  │
│      └─ EXERCISE: Adopt Constitution to legacy service          │
│      └─ Generate AGENTS.md, openspec/, proposal                 │
│                                                                 │
│  ☕ BREAK                                                10 min  │
│                                                                 │
│  ⚖️  MODULE 3: OpenSpec vs SpecKit                      30 min  │
│      └─ DX comparison, token economics (50K vs 18K)             │
│      └─ The Waterfall parallel & why tokens matter              │
│                                                                 │
│  🚀 MODULE 4: Agentic SDLC Step-by-Step                 50 min  │
│      └─ EXERCISE: Build 2 vertical slices                       │
│      └─ RED → GREEN → REFACTOR → VERIFY → COMMIT                │
│                                                                 │
│  🎯 CLOSING                                              5 min  │
│      └─ Metrics that matter, next steps, Q&A                    │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  TOTAL DURATION                                       ~3 hours  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🖥️ Pre-Workshop Setup

### Required Software

```markdown
- [ ] VS Code or Cursor installed
- [ ] GitHub Copilot or Claude extension configured
- [ ] Git installed and configured
- [ ] Node.js 18+ (for constitution-lint)
```

### Required Repositories

```markdown
- [ ] hangar-ai-constitution (this repo)
- [ ] hangar-ai-constitution-brownfield (for Exercise 1)
- [ ] hangar-ai-constitution-greenfield (for Exercise 2)
```

### Verify Setup

```bash
# Check Node.js
node --version  # Should be 18+

# Check constitution-lint
npx constitution-lint --version

# Check repositories
ls -la hangar-ai-constitution
ls -la hangar-ai-constitution-brownfield
ls -la hangar-ai-constitution-greenfield
```

---

## 🤖 AI Trigger Phrases

### Starting the Workshop

| Mode | Trigger Phrase |
|------|----------------|
| **Instructor-Led** | "Our class is here, let's start the Agentic SDLC workshop" |
| **Self-Paced** | "Help me learn this workshop" |
| **Specific Module** | "Help me learn Module 1: Constitution Deep-Dive" |
| **Exercise Only** | "Help me practice the Brownfield Adoption exercise" |
| **Review** | "Quiz me on Constitutional AI concepts" |

### During the Workshop

| Command | What Happens |
|---------|--------------|
| "Explain this more" | Deeper dive on current topic |
| "Show me an example" | Concrete code example |
| "Let's do the exercise" | Start hands-on practice |
| "Quiz me" | Test your understanding |
| "Next topic" | Move to next section |
| "Go back" | Review previous concept |
| "I'm confused about X" | Clarification and re-explanation |
| "Skip to Module N" | Jump to specific module |

---

## 📖 Self-Learning Path

### Recommended Approach

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  DAY 1: FOUNDATIONS (1.5 hours)                                │
│  ─────────────────────────────                                 │
│  • Module 1: Constitution Deep-Dive (35 min)                   │
│  • Module 3: OpenSpec vs SpecKit (30 min)                      │
│  • Review & Quiz (20 min)                                      │
│                                                                 │
│  DAY 2: HANDS-ON PRACTICE (1.5 hours)                          │
│  ──────────────────────────────────────                        │
│  • Module 2: Brownfield Adoption Exercise (45 min)             │
│  • Module 4: Agentic SDLC Exercise (45 min)                    │
│                                                                 │
│  OPTIONAL: DEEP DIVE (30 min each)                             │
│  ─────────────────────────────────                             │
│  • Token Optimization practice guide                           │
│  • Atomic TDD practice guide                                   │
│  • Vertical Slice practice guide                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Per-Module Self-Study Prompts

**Module 1: Constitution Deep-Dive**
```
Help me learn Module 1 of the Agentic SDLC workshop.
Explain Constitutional AI, the Hangar framework components,
and the authority hierarchy. Show me the actual law files
and explain how they work together.
```

**Module 2: Brownfield Adoption**
```
Help me practice the Brownfield Adoption exercise.
Guide me through adopting the Constitution to the
loyalty-service-legacy codebase step by step.
Pause after each artifact so I understand what was generated.
```

**Module 3: OpenSpec vs SpecKit**
```
Help me understand Module 3: OpenSpec vs SpecKit.
Explain the token economics, show me the comparison,
and help me understand when to use each tool.
```

**Module 4: Agentic SDLC**
```
Help me practice the Agentic SDLC exercise.
Walk me through the 5-phase workflow and guide me
through implementing 2 vertical slices using Atomic TDD.
```

---

## 🧪 Knowledge Checkpoints

After each module, test your understanding:

### Module 1 Checkpoint
```
Quiz me on these concepts:
- What are the 4 components of the Hangar Constitution?
- What does NON-NEGOTIABLE mean?
- What is the authority hierarchy?
- What are the 3 VERIFY gates?
```

### Module 2 Checkpoint
```
Quiz me on Brownfield Adoption:
- What are the 7 steps of adoption?
- Why do we STOP before implementation?
- What goes in AGENTS.md?
- What is constitutional authority in a proposal?
```

### Module 3 Checkpoint
```
Quiz me on OpenSpec vs SpecKit:
- What's the token consumption difference?
- What does "regenerative" vs "delta" mean?
- When should I use SpecKit vs OpenSpec?
- Why does token consumption matter?
```

### Module 4 Checkpoint
```
Quiz me on Atomic TDD:
- What are the 8 steps in the cycle?
- What does RED mean?
- What are the 3 VERIFY gates?
- What is a vertical slice?
```

---

## 📂 Module Details (For Facilitators & Self-Learners)

### 📜 Module 1: Constitution Deep-Dive (35 min)

**Key Concepts:**
- Traditional vs Agentic SDLC
- The Four Components (Constitution → Skills → Workflows → Adoptions)
- Authority Hierarchy
- NON-NEGOTIABLE laws
- Atomic TDD introduction

**Self-Study Resources:**
- `laws/index.yaml` — Law definitions
- `agent-skills/README.md` — Skills overview
- `agent-skills/skills-by-domain/` — Skills organized by domain

**Demo:** Run `npx constitution-lint check .` on a project

---

### 🛠️ Module 2: Brownfield Adoption (45 min)

**Exercise:** Adopt Constitution to loyalty-service-legacy

**Setup:**
```bash
cd hangar-ai-constitution-brownfield
ls loyalty-service-legacy/
```

**Trigger Prompt:**
```
I want to adopt the Hangar AI Constitution to this codebase.
Please read the Brownfield Adoption Guide and begin the process.
Use demo mode - pause at each step for teaching.
```

**Expected Outputs:**
```
loyalty-service-legacy/
├── AGENTS.md                    ← Agent entry point
├── openspec/
│   ├── project.md               ← Current state documentation
│   └── changes/
│       └── constitutional-adoption/
│           ├── proposal.md      ← Why & what changes
│           ├── design.md        ← Architecture decisions
│           ├── specs/           ← BDD specifications
│           └── tasks.md         ← Vertical slices
```

**Teaching Points:**
- Why we STOP before implementation
- Law citations in every artifact
- The Strangler Fig pattern for legacy code

---

### ⚖️ Module 3: OpenSpec vs SpecKit (30 min)

**Key Concepts:**
- Developer Experience comparison
- Token consumption economics (50K vs 18K over 5 iterations)
- Regenerative vs Delta models
- The Waterfall parallel warning
- Why tokens = THE metric that matters

**Key Numbers to Remember:**
```
SpecKit (Regenerative):  10K × 5 iterations = 50,000 tokens
OpenSpec (Delta):        10K + (4 × 2K)     = 18,000 tokens
                                             ─────────────
                                             64% SAVINGS
```

---

### 🚀 Module 4: Agentic SDLC Step-by-Step (50 min)

**Exercise:** 5-phase implementation with Atomic TDD

**Setup:**
```bash
cd hangar-ai-constitution-greenfield
cat WORKSHOP-GUIDE.md
```

**Trigger Prompt:**
```
Help me run the AA Hangar Agentic SDLC Workshop from WORKSHOP-GUIDE.md
```

**The 5 Phases:**
1. Adopt the Constitution
2. Select Domain & Tech Stack
3. Choose a Specification
4. Generate Constitutional Proposal
5. Implement with Atomic TDD

**The 8-Step Cycle:**
```
1. RED      → Write ONE failing test
2. GREEN    → Write MINIMUM code to pass
3. REFACTOR → Improve without changing behavior
4. VERIFY   → Pass 3 Gates (Tests + Lint + Static)
5. UPDATE   → Mark task complete in tasks.md
6. COMMIT   → Conventional commit message
7. REPEAT   → Next test in the slice
8. CELEBRATE → Acknowledge the increment! 🎉
```

**Target:** Complete 2 vertical slices minimum

---

## 🔧 Troubleshooting

### Agent Not Responding to Cues

Re-trigger the persona:
```
Remember, you're helping me learn the Agentic SDLC workshop.
I'm currently on [topic]. Please continue guiding me.
```

### Exercise Reset Needed

```bash
# Reset brownfield exercise
cd hangar-ai-constitution-brownfield
rm -rf loyalty-service-legacy
cp -r backup/back-up-app loyalty-service-legacy

# Reset SDLC workshop
cd hangar-ai-constitution-greenfield
git checkout -- .
```

### constitution-lint Not Working

```bash
npm install -g @anthropic/constitution-lint
# or
npx @anthropic/constitution-lint check .
```

### "I'm Lost" Recovery

Say to your AI:
```
I'm lost in the workshop. Please tell me:
1. What module are we on?
2. What have we covered?
3. What's next?
Then help me continue from here.
```

---

## 📚 Additional Resources

### Practice Guides (30-45 min each)
- `aa-engineering-laws/practice-guides/atomic-tdd/`
- `aa-engineering-laws/practice-guides/vertical-slice/`
- `aa-engineering-laws/practice-guides/token-optimization/`

### Technology Avatars
- `aa-engineering-laws/adoptions/java-spring/`
- `aa-engineering-laws/adoptions/python-fastapi/`
- `aa-engineering-laws/adoptions/react-frontend/`

### Slides
- `docs/slides/agentic-sdlc-workshop-3hr/slides.md` — Full Marp deck

---

## ✅ Post-Workshop Next Steps

### Week 1
```markdown
- [ ] Adopt Constitution to ONE real project
- [ ] Complete Atomic TDD practice guide (30 min)
- [ ] Run constitution-lint on your codebase
```

### Week 2
```markdown
- [ ] Implement ONE vertical slice with full cycle
- [ ] Share experience in AI CoP channel
- [ ] Review your team's AGENTS.md
```

### Month 1
```markdown
- [ ] Track Defect Escape Rate before/after
- [ ] Mentor a colleague through adoption
- [ ] Propose one law improvement
```

---

## 📊 Metrics That Matter

| Metric | What It Measures | Target |
|--------|------------------|--------|
| **Defect Escape Rate** | Bugs that reach production | < 5% |
| **Time to Productivity** | New dev to first commit | < 2 weeks |
| **Agentic SDLC Compliance** | Constitutional adherence | > 90% |
| **"AI Off" Competency** | Skills without AI | Maintained |

---

## 📜 Constitutional Compliance

This workshop teaches and demonstrates:

| Law | How Taught |
|-----|------------|
| **ENG-1.2** | AI-Engineer Pairing — co-facilitation model |
| **ENG-4.1** | Atomic TDD — Module 4 exercise |
| **ENG-2.3** | Vertical Slice — both exercises |
| **ENG-6.7** | Audit Trail — task tracking emphasized |
| **PRD-5.1** | OpenSpec — Module 3 comparison |

---

## 🆘 Getting Help

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  💬 DURING WORKSHOP                                             │
│     Say: "I need help with [topic]"                             │
│     Say: "Explain [concept] differently"                        │
│     Say: "Show me a simpler example"                            │
│                                                                 │
│  📧 AFTER WORKSHOP                                              │
│     AI Community of Practice Slack channel                      │
│     Monthly Constitution Office Hours                           │
│     Email: ai-cop@aa.com                                        │
│                                                                 │
│  📖 SELF-STUDY                                                  │
│     Say: "Help me learn this workshop"                          │
│     Say: "Quiz me on [module]"                                  │
│     Say: "I want to practice [exercise]"                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

*Last updated: February 2026*

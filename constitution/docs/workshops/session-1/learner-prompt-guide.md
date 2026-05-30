---
workflow: greenfield-development
avatar: engineering
laws: [ENG-4.1, ENG-11.1, ENG-11.2, PRD-2.1, BUS-7.1]
skills: [skill-spec-governance, skill-04-business-domain-modeling, skill-06-atomic-tdd, skill-07-vertical-slice-dev]
session: 1
type: learner-prompt-guide
---

# Session 1 Learner Prompt Guide — Agentic SDLC Self-Service Track

> **Laws cited in this guide:** ENG-4.1, ENG-11.1, ENG-11.2, PRD-2.1, BUS-7.1

---

## Section 1: How to Read This Guide

Every prompt in this guide follows the same five-part pattern. Understanding the anatomy of a well-formed prompt is the most valuable skill you will practice today: **Avatar → Workflow → Skill → Law → Task**.

The AI assistant has no inherent knowledge of AA's engineering constitution. You inject that context through your prompt. A prompt without law citations produces generic output. A prompt grounded in specific laws produces constitutionally-compliant output that can pass peer review, audit, and gate checks.

Here is the anatomy of a well-formed prompt, annotated:

```
Greenfield Phase 6: Build — Atomic TDD.
│                │
│                └── WORKFLOW: which phase of the greenfield workflow we are in
└── WORKFLOW: names the active 8-Phase workflow

Skill: skill-06-atomic-tdd.
│
└── SKILL: the avatar skill file to invoke (loads specific behavior rules)

Law: ENG-4.1 (NON-NEGOTIABLE — no implementation without failing test first).
│         │
│         └── NON-NEGOTIABLE tag: signals the AI this constraint cannot be relaxed
└── LAW: the specific constitution law governing this action

I am implementing: [SLICE NAME].
│
└── TASK: specific, scoped action — what you want done right now
Step 1 — RED: Write the failing test first. Test name must follow ENG-4.5.
Do NOT write implementation yet. Show me only the test.
│
└── CONSTRAINT: explicit boundary on what the AI should and should not produce
```

Use this guide during every phase. When the AI goes off-track, use the recovery prompts in Section 5.

---

## Section 2: Session Bootstrap Prompt

Paste this prompt at the **start of every new AI chat session** for Session 1. Fill in the placeholders before sending.

```
I am starting the AA Hangar AI Constitution workshop — Session 1: Agentic SDLC Self-Service Track.

Context:
- Avatar: Engineering (hangar-ai-constitution/agent-skills/base/AGENT.md)
- Active workflow: greenfield-development (8-Phase Build)
- Session goal: build a constitutionally-governed vertical slice of [MY DOMAIN]
- Skills active this session: skill-spec-governance, skill-04-business-domain-modeling, skill-06-atomic-tdd, skill-07-vertical-slice-dev
- NON-NEGOTIABLE laws: ENG-4.1 (Atomic TDD), ENG-6.1 (Security), ENG-11.1 (Hangar SDD)

My domain: [REPLACE WITH YOUR DOMAIN — e.g. "flight delay notifications", "loyalty points redemption", "cargo tracking"]
My stack: [REPLACE — e.g. "Java 17 + Spring Boot", "Python + FastAPI", "TypeScript + Node"]

Begin at Greenfield Phase 1: Capture. Ask me about my domain problem and the people who have it.
```

---

## Section 3: Phase-by-Phase Prompt Cards

---

### Phase 1: Capture

**Skills:** `skill-spec-governance`  
**Laws:** `PRD-2.1`

```
Greenfield Phase 1: Capture.
Skill: skill-spec-governance.
Law: PRD-2.1 (problem must be validated before design).

Help me validate this domain problem: [DESCRIBE YOUR PROBLEM].
Who has this problem? What does success look like for them?
Output: validated problem statement + 2-3 user personas.
```

**What to expect:** The AI will ask clarifying questions about your domain, then produce a problem statement and 2–3 personas. Review each persona for specificity — a good persona has a name, a role, and a concrete scenario.

---

### Phase 2: Discover

**Skills:** `skill-04-business-domain-modeling`  
**Laws:** `ENG-1.1`, `PRD-2.1`

```
Greenfield Phase 2: Discover.
Skill: skill-04-business-domain-modeling.
Laws: ENG-1.1 (priority hierarchy), PRD-2.1.

Review my domain: [PASTE YOUR PROBLEM STATEMENT].
Identify: applicable constitution laws, non-negotiable constraints, suggested avatar specializations.
Output: law inventory table (law ID | applies because | NON-NEGOTIABLE?).
```

**What to expect:** A table of applicable laws with the NON-NEGOTIABLE column populated. Look for `ENG-4.1`, `ENG-6.1`, `ENG-6.4`, `ENG-11.1` in the NON-NEGOTIABLE column — these four are always present regardless of domain.

---

### Phase 3: Define

**Skills:** `skill-02-user-journey-mapping`, `skill-03-executable-spec`  
**Laws:** `ENG-1.5`, `ENG-4.4`, `ENG-11.2`

```
Greenfield Phase 3: Define.
Skills: skill-02-user-journey-mapping, skill-03-executable-spec.
Laws: ENG-1.5 (API-first), ENG-4.4 (BDD structure), ENG-11.2 (proposal completeness).

Generate for my domain [DOMAIN]:
1. API contract (endpoint, request/response, error codes)
2. BDD scenarios (Given/When/Then for the 3 most important paths)
3. PROPOSAL.md stub citing law IDs ENG-1.5, ENG-4.4, ENG-11.1
Output all three as separate code blocks.
```

**What to expect:** Three separate code blocks — API contract, Gherkin scenarios, and a `PROPOSAL.md` stub. If the AI combines them or outputs prose instead of code blocks, use the "too verbose" recovery prompt and resend.

---

### Phase 4: Design

**Skills:** `skill-spec-governance`  
**Laws:** `ENG-2.1`, `ENG-2.3`, `ENG-11.2`

```
Greenfield Phase 4: Design.
Skill: skill-spec-governance.
Laws: ENG-2.1 (architecture), ENG-2.3 (vertical slice), ENG-11.2.

Review my PROPOSAL.md: [PASTE PROPOSAL].
Challenge: does the design violate any laws? Are there unmitigated risks?
File an ADR in hangar-ai-specs/ for any architecture decision made.
```

**What to expect:** A design critique identifying law violations or gaps, plus a stub ADR. If the AI produces only positive feedback without any critique, ask: "What would a skeptical reviewer say about this design?"

---

### Phase 5: Plan

**Skills:** `skill-07-vertical-slice-dev`  
**Laws:** `ENG-2.3`, `ENG-4.2`

```
Greenfield Phase 5: Plan.
Skill: skill-07-vertical-slice-dev.
Laws: ENG-2.3 (vertical slice), ENG-4.2 (test pyramid).

From my BDD scenarios, define 2-3 vertical slices.
For each slice: name, thin slice description, test types needed (unit/integration/contract), dependency order.
Output: tasks.md with slices as checkboxes, ordered by dependency.
```

**What to expect:** A `tasks.md` with 2–3 checkboxes representing vertical slices, each with test types and dependencies. Reject any slice that is a horizontal layer (e.g., "implement service layer" is not a valid vertical slice).

---

### Phase 6: Build — Atomic TDD

> ⚠️ Use these three prompts **in sequence**. Do not skip RED. Do not combine RED and GREEN.

**Skills:** `skill-06-atomic-tdd`  
**Laws:** `ENG-4.1` (NON-NEGOTIABLE), `ENG-3.1`, `ENG-3.4`, `ENG-4.5`

#### RED Prompt — Use this first

```
Greenfield Phase 6: Build — Atomic TDD.
Skill: skill-06-atomic-tdd.
Law: ENG-4.1 (NON-NEGOTIABLE — no implementation without failing test first).

I am implementing: [SLICE NAME].
Step 1 — RED: Write the failing test first. Test name must follow ENG-4.5: "methodName_condition_expectedBehavior".
Do NOT write implementation yet. Show me only the test. I will confirm RED before you proceed.
```

**What to expect:** A single test method, no implementation. Run it — it must fail. Confirm RED to your AI before sending the next prompt.

#### GREEN Prompt — Use only after confirming RED

```
Test confirmed RED. 
Step 2 — GREEN: Write the minimum implementation to make this test pass.
No gold-plating. One failing test → one passing test. 
Show me only the implementation change.
```

**What to expect:** The minimum code to make the one failing test pass. If the AI writes more than needed for this one test, use the over-generation recovery prompt.

#### REFACTOR Prompt — Use only after confirming GREEN

```
Test is GREEN.
Step 3 — REFACTOR: Identify any code smell, duplication, or law violation in what we just wrote.
Laws to check: ENG-3.1 (complexity ≤10), ENG-3.4 (single responsibility), ENG-4.5 (test naming).
If clean, say "No refactor needed." If not, show the refactored version.
```

**What to expect:** A law-by-law check on the code you just wrote. "No refactor needed" is a valid and common response for small, clean implementations. After REFACTOR, run your full test suite (VERIFY), commit, and repeat the cycle from RED for the next behavior.

---

### Phase 8: Archive (Ship)

**Skills:** `skill-spec-governance`  
**Laws:** `ENG-11.1`

```
Greenfield Phase 8: Ship — Archive.
Skill: skill-spec-governance.
Law: ENG-11.1 (Hangar SDD — proposal must be archived when complete).

Move my PROPOSAL.md to hangar-ai-specs/archive/[proposal-id]/.
Update the proposal status to ARCHIVED with today's date.
Generate a 3-sentence summary of what was built and what laws were enforced.
```

**What to expect:** Instructions for archiving your proposal and a 3-sentence completion summary. The summary should cite the law IDs enforced during the build.

---

## Section 4: Skill Invocation Patterns

When you want to invoke a specific skill without using a full phase prompt, use this general pattern:

```
Invoke skill: [SKILL-ID].
Laws it implements: [LAW-IDs].
Task: [WHAT YOU WANT].
```

**Examples:**

```
Invoke skill: skill-spec-governance.
Laws it implements: ENG-11.1, ENG-11.2.
Task: Review my PROPOSAL.md for completeness and flag any missing sections.
```

```
Invoke skill: skill-04-business-domain-modeling.
Laws it implements: PRD-2.1, ENG-1.1.
Task: Given these three personas, identify which domain entities and business rules I must model.
```

```
Invoke skill: skill-06-atomic-tdd.
Laws it implements: ENG-4.1, ENG-4.5, ENG-4.6.
Task: I am about to implement a password hashing method. Walk me through the RED phase only.
```

```
Invoke skill: skill-07-vertical-slice-dev.
Laws it implements: ENG-2.3, ENG-4.2.
Task: I have 5 BDD scenarios. Decompose them into vertical slices ordered by dependency.
```

---

## Section 5: Recovery Prompts

Use these when the AI assistant goes off-track. Paste the exact prompt — do not soften or apologize.

---

**When the agent over-generates:**
```
Stop. Per ENG-4.1 (Atomic TDD, NON-NEGOTIABLE): one failing test at a time.
Delete everything you just wrote. Start again with only the test for: [SPECIFIC BEHAVIOR].
```

---

**When the agent skips tests:**
```
You have violated ENG-4.1 (Atomic TDD — NON-NEGOTIABLE). Implementation without a failing test is not permitted.
Remove the implementation. Write the test first.
```

---

**When the agent goes off-domain:**
```
Refocus. Active workflow: greenfield-development, Phase [N].
Active skill: [SKILL-ID]. 
Task: [RESTATE ORIGINAL TASK].
```

---

**When the agent produces a law violation:**
```
This violates [LAW-ID]: [LAW TITLE].
Identify the specific line. Explain why it violates the law. Propose a fix that is compliant.
```

---

**When the agent is too verbose:**
```
Token budget: brief. Law IDs only (no descriptions). Code only (no narration). Proceed.
```

---

## Section 6: Session 2 Bootstrap Prompt

Use this prompt at the **start of Session 2**. You can also use it now to preview what changes when working with legacy code.

```
I am starting the AA Hangar AI Constitution workshop — Session 2: Legacy Adoption.

Context:
- Avatar: Engineering (hangar-ai-constitution/agent-skills/base/AGENT.md)  
- Active workflow: legacy-rescue-refactor
- Codebase: loyalty-service-legacy (Java/Spring Boot)
- Skills active: skill-09-refactoring, skill-06-atomic-tdd, skill-spec-governance
- NON-NEGOTIABLE laws: ENG-4.1 (Atomic TDD), ENG-11.1 (Hangar SDD)

Begin at Phase 1: Domain Archaeology. 
Ask me to share the first class or file I want to analyze.
```

**What changes in Session 2:** The `legacy-rescue-refactor` workflow begins with archaeology — understanding existing behavior before changing it. `ENG-4.1` still applies, but the first tests you write are **characterization tests** that document current behavior, not tests for new behavior. The refactoring skill (`skill-09-refactoring`) replaces the design skills from Session 1.

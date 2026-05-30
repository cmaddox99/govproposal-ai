# Constitutional Companion — Pragmatic Adoption Guide

> **Laws implemented:** ENG-1.2, ENG-11.1, ENG-12.1, ENG-3.1, ENG-3.4

---

## Who This Guide Is For

Teams who need to adopt the Hangar AI Constitution **on their own terms** — without being forced into a monolithic, all-at-once process. This covers three overlapping situations:

| Situation | Symptom | Jump To |
|-----------|---------|---------|
| **Complex constraints** | "Too many SonarQube violations to fix before we can start" | [Part 3: SonarQube Delta Model](#part-3-sonarqube-delta-model) |
| **Complex constraints** | "The adoption proposal is huge and we can't do it in one go" | [Part 2: Bounded-Context Iterations](#part-2-bounded-context-iterations) |
| **Complex constraints** | "The AI keeps splitting methods to meet the 50-line rule instead of designing well" | [Part 4: ENG-3.1 Design-First](#part-4-eng-31-design-first-not-line-counting) |
| **Complex constraints** | "We're forced through product avatar analysis before we can start" | [Part 1: Governance Setup](#part-1-one-time-governance-setup) |
| **AI on-ramp** | "I'm an experienced developer but I don't trust AI to write my code yet" | [Part 6: Trust Ramp](#part-6-trust-ramp-for-developers-new-to-ai) |
| **AI on-ramp** | "How do I verify what AI produces before it lands in our codebase?" | [Part 6: Trust Ramp](#part-6-trust-ramp-for-developers-new-to-ai) |
| **Low bandwidth** | "I'm too busy with sprint work to do a full adoption" | [Part 7: Minimum Viable Session](#part-7-minimum-viable-session-for-low-bandwidth-teams) |
| **Low bandwidth** | "Can I adopt in 30-minute increments?" | [Part 7: Minimum Viable Session](#part-7-minimum-viable-session-for-low-bandwidth-teams) |

These three situations frequently co-occur. A developer who is new to AI is often also busy, and often working on a codebase with real constraints. All three are addressed by the same pragmatic approach.

---

## Core Principle: Governance Setup ≠ Code Remediation

These are **two entirely separate concerns**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LAYER 1: GOVERNANCE SETUP (Do Once — No Code Changes)                  │
│  AGENTS.md + hangar-ai-specs/ + SonarQube baseline                      │
│  Duration: ~1-2 hours                                                    │
│  Outcome: Your project is constitutionally governed                      │
├─────────────────────────────────────────────────────────────────────────┤
│  LAYER 2: CODE REMEDIATION (Do Iteratively — One Context at a Time)     │
│  Archaeology → Decision → Implement → Delta Scan                        │
│  Duration: ~2-4 hours per bounded context                               │
│  Outcome: That context is constitutionally compliant                    │
└─────────────────────────────────────────────────────────────────────────┘
```

Once Layer 1 is complete, your team can:
- Do **normal feature work** under the constitution between remediations
- Pick up a bounded context when bandwidth allows
- Abandon and resume an iteration without losing governance

The constitution does not require all violations to be fixed before you can use it. It requires that you **don't make things worse** on code you touch.

---

## Part 1: One-Time Governance Setup

**Goal:** Establish constitutional governance artifacts. No code analysis. No violation fixes.

### Step 1 — Run Adoption Phases 1–3 (Scoped)

Run `workflows/adoption.md` with these constraints:

#### On Product Avatar

The product avatar is **optional for initial adoption**. Per `workflows/adoption.md` Step 2.1:

> *"If no avatar matches closely, use the base constitution without avatar enrichment and note this in AGENTS.md."*

In pragmatic adoption, explicitly defer the product avatar:

```markdown
## Avatars
- **Technology:** java-spring          ← pick your stack
- **Product Domain:** none — DEFERRED. Base constitution laws apply.
  Product avatar will be added per bounded context as adoption matures.
```

This is constitutionally valid. The `aa-constitution-lint` linter does not require a product avatar.

#### On Code Analysis

Do **not** run any violation scan, archaeology prompt, or SonarQube analysis during governance setup. The adoption workflow phases are structural only.

### Step 2 — Record SonarQube Baseline

After provisioning the SonarQube gate (Phase 2b), run a full scan and save the output as:

```
hangar-ai-specs/evidence/sonarqube-baseline.md
```

Use the `docs/templates/sonarqube-baseline.md` template. This is your **before picture** — it records the debt you're starting with. No violations are required to be fixed at this point.

### Step 3 — Add Pragmatic Adoption Rules to project-rules.md

Add the following sections to `hangar-ai-specs/project-rules.md` (see ready-to-copy templates in [Part 5](#part-5-project-rulesmd-templates)):

- Product avatar deferral note
- Adoption chunking protocol
- SonarQube delta policy
- ENG-3.1 interpretation policy

These rules govern how the AI behaves in all subsequent sessions.

### ✅ Governance Setup Complete

Commit and stop. You now have constitutional governance. Do real work.

---

## Part 2: Bounded-Context Iterations

**One session = one bounded context.** The Application Guide from the Hangar AI Constitution Workflows course states:

> *"Module Size Sweet Spot: 1K–5K LOC per bounded context. For larger systems: pick one bounded context to start. Work in separate sessions."*

### Choosing a Bounded Context

A bounded context for adoption purposes is a cohesive cluster of files with a single responsibility — a service, a module, a package. Good candidates for first iteration:

- Highest violation density (most bang per buck)
- Lowest coupling (easiest to change safely)
- Most actively developed (violations will compound otherwise)

### Iteration Sequence

```
┌─────────────────────────────────────────────────────────────────────┐
│  ITERATION: {context-name}                                          │
├─────────────────────────────────────────────────────────────────────┤
│  1. Declare scope — files in this context only                      │
│  2. Archaeology — violation inventory for THIS context              │
│  3. Decision — REFACTOR | REWRITE | EXTEND verdict                  │
│  4. Implement — Atomic TDD, one violation at a time                 │
│  5. Delta scan — sonarqube-delta.md before/after comparison         │
│  6. Commit evidence + archive                                       │
│  ⛔ STOP — do not begin next context without human confirmation      │
└─────────────────────────────────────────────────────────────────────┘
```

### Archaeology Prompt Template

```
I am running a bounded-context adoption iteration.

Bounded context: {context-name}
Files in scope: {path(s)}

Load these constitution law files:
- laws/engineering/testing.md
- laws/engineering/quality.md
- laws/engineering/security.md

Audit ONLY the files listed above for constitutional violations.
For each violation:
1. Cite the exact law ID (ENG-x.x)
2. Classify: HARD_BLOCK | PHASE_GATE | DEFERRABLE
3. Estimate remediation effort: S / M / L

Output a violation inventory sorted by severity.
Save to: hangar-ai-specs/changes/{context-name}/evidence/phase-1-archaeology.md

Do NOT scan files outside the declared bounded context.
Do NOT attempt to fix anything. Inventory only.
STOP after producing the inventory and await my review.
```

### Remediation Prompt Template

```
I am on the Refactor Track for {context-name}.

Violation inventory: hangar-ai-specs/changes/{context-name}/evidence/phase-1-archaeology.md

Work through HARD_BLOCK violations only in this session.
For each violation, run the full 8-step Atomic TDD cycle (ENG-4.1).
Apply ENG-3.1 through design patterns, not line-splitting (per project-rules.md).

After each cycle: report the completed test, commit hash, and remaining violations.
STOP after all HARD_BLOCKs are resolved and await my confirmation before PHASE_GATEs.
```

### Between Iterations

After completing an iteration, you may:

- Merge and ship the changes
- Do normal feature work under the constitution (ENG-4.1 TDD, etc.)
- Pick up the next bounded context when bandwidth allows

The sonar backlog persists in `hangar-ai-specs/changes/sonar-backlog/` and does **not** block feature work.

---

## Part 3: SonarQube Delta Model

The SonarQube gate has three tiers of enforcement. The AI must not conflate them.

### Tier Classification

| Tier | Metric Examples | What It Means in an Iteration |
|------|----------------|-------------------------------|
| 🚨 **HARD_BLOCK** | Vulnerabilities, PII hotspots, blocker violations, security rating ≠ A | Fix in **any file you touch** in this iteration. Truly non-negotiable. |
| 🔴 **PHASE_GATE** | `new_coverage` ≥ 90%, `coverage` ≥ 80%, bugs = 0, critical violations = 0 | Applies to **new and changed code only**. Existing violations require a written justification document, not an immediate fix. |
| ⚠️ **WARNING** | Cognitive complexity, duplication, code smells | Must **not worsen** iteration-over-iteration. Not required to reach zero. |

### The "New Code" Configuration

Configure SonarQube's **New Code definition** to your branch or sprint period. This means:

- `new_coverage ≥ 90%` applies only to lines you wrote in this iteration
- `coverage ≥ 80%` is the overall long-term target, not a gate on untouched legacy code

In SonarQube: **Project Settings → New Code → Previous version** or **Specific date** matching your adoption start.

### Exception Justification Pattern

When a PHASE_GATE cannot be met for existing code, record this in the change directory:

```markdown
# hangar-ai-specs/changes/{context-name}/evidence/gate-exception.md

## PHASE_GATE Exception

**Metric:** coverage
**Current value:** 42%
**Threshold:** ≥ 80%
**Scope:** Existing legacy code in {context-name} — NOT new code written in this iteration
**New code coverage:** 94% ✅ (meets the ≥ 90% new_coverage gate)
**Remediation plan:** Coverage will increase to ≥ 80% by {target date} via backlog iterations
**Approver:** {architect-name}
**Date:** {date}
```

### Sonar Backlog Tracking

Defer non-HARD_BLOCK violations on code you are not touching:

```
hangar-ai-specs/changes/sonar-backlog/
  └── {context-name}-violations.md    ← violations deferred from each iteration
```

Each subsequent iteration that touches a file in the backlog must address its HARD_BLOCKs at that point.

---

## Part 4: ENG-3.1 Design-First, Not Line-Counting

### What ENG-3.1 Actually Says

| Metric | Limit | Enforcement |
|--------|-------|-------------|
| Cyclomatic complexity | ≤ 10 per method | Build fails |
| Cognitive complexity | ≤ 7 per method | Build fails |
| Method length | ≤ 50 lines | Warning → Fail |
| Class length | ≤ 300 lines | Warning |
| File size | ≤ 500 lines | Warning |

The law's own remediation guidance says:
> *"Replace conditional type-checking with type-directed behavior"*

This is the Strategy/Polymorphism approach — not line-splitting.

### The Problem: Mechanical Line-Splitting

When an AI sees a 200-line method, it may split it at line 50 like this:

```java
// ❌ PROHIBITED — mechanical split, no design improvement
public void processBooking(Booking booking) {
    doStep1(booking);  // extracted only to meet line count
    doStep2(booking);  // no single responsibility
    doStep3(booking);  // still coupled; just hidden
}
private void doStep1(Booking booking) { /* 49 lines */ }
```

This meets the line limit mechanically but violates ENG-3.4 (Single Responsibility) and ENG-3.3 (Law of Demeter). It does not reduce cyclomatic or cognitive complexity.

### The Correct Approach: Design Patterns

The same 200-line if/else chain, fixed by design:

```java
// ✅ REQUIRED — Strategy pattern reduces complexity naturally
public interface TierRule {
    boolean matches(MemberProfile profile);
    Tier apply(MemberProfile profile);
}

// Each rule is short because it has ONE responsibility
public class GoldTierRule implements TierRule { ... }          // ~15 lines
public class PlatinumTierRule implements TierRule { ... }      // ~15 lines
public class ExecutivePlatinumTierRule implements TierRule { ... } // ~15 lines

public class TierCalculationService {
    private final List<TierRule> rules;  // injected; easily tested

    public Tier calculateTier(MemberProfile profile) {
        return rules.stream()
            .filter(r -> r.matches(profile))
            .findFirst()
            .map(r -> r.apply(profile))
            .orElse(Tier.BASE);           // ~8 lines, CC=2
    }
}
```

### Design Pattern Reference

| Pattern | Use When | ENG-3.1 Benefit |
|---------|---------|----------------|
| **Strategy** | Long if/else or switch chains | Each branch becomes a short, testable class |
| **Command** | Sequences of operations that vary | Operations are first-class objects; no branching |
| **Template Method** | Algorithm skeleton with varying steps | Overrides replace conditionals |
| **Guard Clause / Early Return** | Deep nesting (> 3 levels per ENG-3.1) | Flattens the happy path |
| **Decompose to Collaborators** | God methods doing too many things | Natural emergence of short, focused methods |

### When Limits Conflict With Good Design

If you genuinely cannot meet ENG-3.1 line limits while maintaining clean object design, **prefer the clean design** and document the exception:

```markdown
# hangar-ai-specs/changes/{context-name}/evidence/eng-3-1-exception.md

## ENG-3.1 Exception

**File:** {file}
**Method:** {method}
**Current length:** {N} lines
**Reason limit cannot be met:** {explanation — e.g., "This method is a well-structured
  pipeline with 8 ordered stages. Splitting further would fragment cohesive logic
  without creating reusable units, violating ENG-3.4."}
**Cyclomatic complexity:** {N} (✅ within limit)
**Cognitive complexity:** {N} (✅ within limit)
**Design pattern applied:** Pipeline
```

The complexity metrics (cyclomatic, cognitive) are the hard blocks. The line count is a warning that prompts a design review — not a mechanical counter.

---

## Part 5: project-rules.md Templates

Copy these blocks into `hangar-ai-specs/project-rules.md` during governance setup. Replace placeholders.

```markdown
## Avatar Decisions

- **Technology avatar:** {technology_avatar}
- **Product avatar:** DEFERRED — project scope too large for initial adoption.
  Base constitution laws apply. Product avatar will be added per bounded context
  as adoption matures.

---

## Adoption Chunking Protocol

- Adoption is executed ONE bounded context at a time.
- The AI MUST NOT scan or remediate files outside the declared bounded context
  for the current session.
- Each iteration produces one `hangar-ai-specs/changes/{context-name}/` directory.
- Between iterations, normal feature development proceeds under the constitution.
- The AI MUST stop after completing one bounded context and await human confirmation
  before beginning the next.

---

## SonarQube Adoption Policy (Large Brownfield)

This is a large brownfield codebase. The SonarQube gate uses a DELTA model:

- **Baseline:** `hangar-ai-specs/evidence/sonarqube-baseline.md` records
  the starting state of the full codebase. Existing violations are DOCUMENTED,
  not required to be fixed immediately.
- **HARD_BLOCKs** (security vulnerabilities, PII hotspots, blocker violations):
  MUST be fixed in any file touched this iteration. Non-negotiable.
- **PHASE_GATEs** (coverage, bugs, critical violations): Apply to new/changed code
  only (SonarQube "new code" period). Existing violations are tracked as a backlog
  in `hangar-ai-specs/changes/sonar-backlog/`. Each iteration MUST NOT add new
  violations.
- **WARNINGs** (complexity, duplication, code smells): Must not worsen.
  No requirement to reach zero before proceeding.
- **Coverage exception:** Files not modified in this iteration are exempt from the
  80% coverage gate. Only files touched require new tests per ENG-4.6.
- Exception approver for PHASE_GATE waivers: {architect-name}

---

## ENG-3.1 Interpretation Policy

Compliance with ENG-3.1 complexity and line limits MUST be achieved through
object-oriented design, NOT mechanical line-splitting.

**Required:** Apply Strategy, Command, Template Method, Guard Clause, or
decomposition-to-collaborators patterns that naturally reduce complexity.

**Prohibited:** Splitting a method at line 50 without changing its logical
structure; creating private helpers with no reuse value solely to satisfy
a line count.

When ENG-3.1 line limits conflict with clean object design, prefer clean
design and document the exception in
`hangar-ai-specs/changes/{context}/evidence/eng-3-1-exception.md`.
Per ENG-3.4, each extracted unit must have a single responsibility.
Cyclomatic complexity ≤ 10 and cognitive complexity ≤ 7 are the hard
constraints. Line length is a design prompt, not a line counter.
```

---

## Summary: Your Iterative Adoption Sequence

```
SESSION 1 — Governance Only (~1-2 hours)
  ├─ Run workflows/adoption.md Phases 1-3
  ├─ Technology avatar only; product avatar: DEFERRED
  ├─ SonarQube baseline scan → evidence/sonarqube-baseline.md
  ├─ Add pragmatic adoption rules to project-rules.md
  └─ ✅ STOP. Constitutional governance is live. Do real work.

SESSION 2+ — One Bounded Context (~2-4 hours each)
  ├─ Declare scope: one bounded context, specific file paths
  ├─ Archaeology prompt → violation inventory
  ├─ Review inventory; decide HARD_BLOCK only | all violations | defer
  ├─ Implement via Atomic TDD cycles
  ├─ Delta scan → sonarqube-delta.md
  ├─ Commit + archive
  └─ ✅ STOP. Do real work. Pick up next context when ready.
```

The constitution does not block feature work while the backlog drains. It requires that new code you write is clean, tested, and secure. The rest is a managed trajectory.

---

## Part 6: Trust Ramp for Developers New to AI

### The Problem

Many experienced engineers are new to AI-assisted development. They have deep knowledge of good design, testing, and code quality — but they reasonably don't yet trust that AI will apply those same standards. Forcing them into a mode where the AI generates code they haven't reviewed destroys that trust rather than building it.

The solution is not to lower the standard. It is to **give the developer control over how much the AI does**, and to earn expanded autonomy through demonstrated quality.

### Why the Constitution Is Trust-Compatible

Per **ENG-1.2 (AI-Engineer Pairing Law)**, the AI is explicitly positioned as a *pair programmer* — not an autonomous actor. The Atomic TDD cycle (ENG-4.1) is naturally structured for human oversight:

- The AI produces **one test**. The human reviews it before running anything.
- The AI produces **minimum production code**. The human reviews it before committing.
- Every step has a measurable outcome (RED / GREEN / PASS) that the human can verify independently.
- Every commit is scoped to one behavioral change — small enough to understand and reject if needed.

The human can intervene, reject, or rewrite at any point. The AI's output is always a proposal.

### The Trust Ramp

| Rung | Name | What the AI Does | What the Human Does | When to Use |
|------|------|-----------------|---------------------|------------|
| **1 — Observe** | AI explains only | Describes what it would do; cites the relevant law and design pattern | Decides, writes all code themselves | First session; AI completely untrusted |
| **2 — Draft Test** | AI proposes one test | Writes a single failing test with rationale for the design choice | Reviews and runs the test; writes production code | AI trusted for test authoring; not yet for production code |
| **3 — Pair** | AI writes test + minimum production code | Completes one full TDD cycle per explicit instruction | Reviews each artifact — test, production code, refactor — before accepting | AI trusted within a single reviewed cycle |
| **4 — Accelerate** | AI runs full cycles | Executes the 8-step Atomic TDD cycle autonomously | Reviews the outputs at VERIFY step; approves or rolls back | AI trusted to work unsupervised within a declared scope |

**Rules:**

- The developer chooses the rung. **The AI never suggests moving up.**
- The developer may stay on any rung indefinitely.
- Rung progression requires the developer to explicitly request it (e.g., "let's try the next rung").
- At Rungs 1 and 2, the AI must explain the *why* — the law citation, the design pattern, the rationale — not just produce output. Understanding enables informed rejection.
- The human's review is not optional at any rung. The AI's output is always a proposal.

**Default rung if not stated:** Rung 2. The AI drafts one test and explains the law; the human decides what to do with it.

### What "Observe Mode" Looks Like (Rung 1)

At Rung 1, every session follows this pattern:

```
Human: "What would you do with this method?"

AI (Rung 1 response):
  - Identifies the applicable law: ENG-3.1 (Cyclomatic Complexity)
  - Explains the violation: CC=18, threshold is ≤10
  - Recommends the design pattern: Strategy — here's why
  - Describes what the extracted classes would look like
  - Does NOT write any code
  - Asks: "Does this approach make sense to you? Want to try it yourself first?"
```

The developer writes the code. The AI reviews it on request.

### project-rules.md Template for AI On-Ramp

```markdown
## AI Pairing Mode (ENG-1.2)

Starting trust rung: {1 — Observe | 2 — Draft Test | 3 — Pair | 4 — Accelerate}
AI role: propose and explain. Human role: decide and own.
Rung progression: explicit developer request only. AI does not suggest moving up.
At Rungs 1-2: AI must explain law citation and design rationale before producing output.
```

---

## Part 7: Minimum Viable Session for Low-Bandwidth Teams

### The Problem

Many teams cannot allocate a 2-4 hour block for adoption. Sprint commitments, on-call rotations, and competing priorities mean adoption sessions are interrupted or never started.

The constitution does not require long sessions. Every Atomic TDD cycle (ENG-4.1) is a **self-contained unit of value** that leaves the codebase better than it was found (ENG-1.3 — Boy Scout Rule). A 30-minute session that delivers one cycle is a valid, complete adoption contribution.

### Session Size Reference

| Time Available | What to Do | Outcome | State Preserved In |
|---------------|-----------|---------|-------------------|
| **15 min** | Read one violation from the archaeology inventory | Know the next target; no code changed | The inventory file |
| **30 min** | One Atomic TDD cycle | One test + one production fix + one commit | Git history |
| **60 min** | Archaeology for one bounded context | Full violation inventory; no code changed | `evidence/phase-1-archaeology.md` |
| **2 hours** | Governance setup (Session 1) | Constitutional governance live; no violations required | `AGENTS.md` + `hangar-ai-specs/` |
| **4 hours** | One bounded context (HARD_BLOCKs only) | Security and blockers resolved for that context | `sonarqube-delta.md` + archive |

### Rules for Low-Bandwidth Adoption

1. **Every session ends green.** All tests must pass before stopping. A half-finished fix is worse than no fix.
2. **State is always preserved.** The `hangar-ai-specs/changes/{context}/` directory captures exactly where you left off. Returning to an in-progress context requires only reading that directory.
3. **No sprint commitment.** Adoption runs *alongside* feature work, not instead of it. There is no velocity impact to track.
4. **A 30-minute session is a complete session.** One TDD cycle = one improvement = one commit. That is the entire required unit of work.
5. **Interruptions are safe.** The Atomic TDD cycle's short scope means an interruption at any STOP point leaves the codebase in a clean state.

### The 30-Minute Session Prompt

For a developer who has 30 minutes and an existing violation inventory:

```
I have 30 minutes. My violation inventory is at:
hangar-ai-specs/changes/{context}/evidence/phase-1-archaeology.md

Pick the next HARD_BLOCK violation and run ONE Atomic TDD cycle for it.
Stop after the cycle is committed. Do not start a second cycle.
```

### project-rules.md Template for Low-Bandwidth Teams

```markdown
## Adoption Bandwidth Policy

Sessions are time-boxed. Any session ending with all tests passing is a valid session.
Minimum session: one Atomic TDD cycle (~30 min).
No sprint commitment to adoption cadence. Adoption runs alongside feature work.
Every session must end with codebase in green state (all tests passing).
Session state preserved in hangar-ai-specs/changes/{context}/ between sessions.
```


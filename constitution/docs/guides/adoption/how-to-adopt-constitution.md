# How to Adopt the AA Hangar AI Constitution

> **Governed adoption path (recommended):** Use the [`workflows/adoption.md`](../../../workflows/adoption.md) workflow
> for all new adoptions, migrations from `openspec/`, and updates to stale existing adoptions.
> That workflow is the authoritative, three-phase adoption path.
> Copy-paste ready prompts are in [`docs/guides/prompts/adoption-workflow-prompt.md`](../prompts/adoption-workflow-prompt.md).

---

> A practical reference guide for teams who need additional context on specific adoption steps.

---

## Table of Contents

1. [Quick Start: Kickoff Prompt](#quick-start-kickoff-prompt)
2. [Overview](#overview)
3. [Authority Hierarchy](#authority-hierarchy)
4. [Step 1: Initialize Hangar SDD in Your Repo](#step-1-initialize-hangar-sdd-in-your-repo)
5. [Step 2: Create Root AGENTS.md](#step-2-create-root-agentsmd)
6. [Step 3: Adopt Constitutions and Agent Skills](#step-3-adopt-constitutions-and-agent-skills)
7. [Step 4: Hangar SDD Workflow](#step-4-hangar-sdd-workflow)
8. [Step 5: Prompt Patterns for Constitutional Development](#step-5-prompt-patterns-for-constitutional-development)
9. [Step 6: Handling Violations](#step-6-handling-violations)
10. [Step 7: Evolving Your Constitution](#step-7-evolving-your-constitution)
11. [Real Prompt Examples by Domain](#real-prompt-examples-by-domain)

---

## Quick Start: Kickoff Prompt

**Copy this prompt to your AI assistant to begin adopting the AA Hangar AI Constitution in your project:**

```
I need to adopt the AA Hangar AI Constitution for this project. Help me
configure Constitutional governance.

PROJECT CONTEXT:
- Repository: [your-repo-name]
- Technology Stack: [Java/Spring | Python/FastAPI | React/TypeScript | etc.]
- Product Domain: [Cargo & Freight | Passenger Booking | Loyalty | Airport Operations | Customer Service | Check-In & Travel]
- Team: [team-name]

TASKS:
1. Create the hangar-ai-specs/ directory structure in this repo
2. Create a root AGENTS.md that references hangar-ai-constitution with proper
   precedence rules (hangar-ai-constitution laws ALWAYS take precedence)
3. Help me select and adopt the appropriate constitutions and adoptions:
   - All three base constitutions (Engineering, Product, Business)
   - Aviation/FAA industry adoption (required for all AA projects)
   - Technology adoption for my stack
   - Product-type adoption for my domain
4. Create project-specific agent instructions that extend the base AGENT.md
5. Create a project-rules.md for any project-specific extensions

REFERENCE:
The hangar-ai-constitution repository is located at:
https://github.com/AAInternal/hangar-ai-constitution

Please start by reading the base constitutions and relevant adoptions, then guide
me through the initialization process step by step.
```

---

## Overview

### What is Constitutional Adoption?

Constitutional adoption means your project **inherits and follows** the laws defined in the hangar-ai-constitution. This creates consistency across all American Airlines engineering teams while allowing project-specific extensions.

**Key Principle:** The hangar-ai-constitution is the **authoritative source**. Local project instructions can extend but NEVER contradict the central constitution.

### The Adoption Process

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AA-HANGAR-AI-CONSTITUTION                             │
│                    (Central Authority - AAInternal Repo)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  constitution/base/           │  agent-skills/base/                         │
│  ├── ENGINEERING-CONSTITUTION │  └── AGENT.md                               │
│  ├── PRODUCT-CONSTITUTION     │                                             │
│  └── BUSINESS-CONSTITUTION    │  agent-skills/skills-by-domain/             │
│                               │  └── [29 skill files in 5 domains]           │
│  constitution/avatars/      │                                             │
│  ├── industry/aviation-faa/   │  agent-skills/avatars/                    │
│  ├── technology/[stack]/      │  ├── technology/[stack].md                  │
│  └── product-type/[domain]/   │  └── product-type/[domain].md               │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ YOUR PROJECT REFERENCES
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           YOUR PROJECT REPO                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  AGENTS.md (root)                   │  hangar-ai-specs/                     │
│  - References hangar-ai-constitution│  ├── changes/                  │
│  - Establishes precedence rules     │  ├── specs/                           │
│  - Links to adopted constitutions   │  └── archive/                         │
│  - Links to agent instructions      │                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Authority Hierarchy

**CRITICAL:** The hangar-ai-constitution establishes laws that ALL American Airlines projects must follow. Local project instructions can add context but CANNOT override central laws.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AUTHORITY HIERARCHY                                  │
│                    (Higher = More Authoritative)                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. AA-HANGAR-AI-CONSTITUTION LAWS (HIGHEST AUTHORITY)                      │
│     ├── Engineering Constitution - Code quality, testing, architecture      │
│     ├── Product Constitution - User journeys, metrics, accessibility        │
│     ├── Business Constitution - Compliance, domain rules, aviation (FAA)    │
│     └── Industry/Technology/Product Adoptions                               │
│                                                                             │
│  2. AA-HANGAR-AI-CONSTITUTION AGENT INSTRUCTIONS                            │
│     ├── Base AGENT.md - Core agent persona and guardrails                   │
│     ├── Skills - Roadmapping, TDD, code review, etc.                        │
│     └── Adoption-specific agent behaviors                                   │
│                                                                             │
│  3. PROJECT-SPECIFIC EXTENSIONS (LOCAL)                                     │
│     ├── project-rules.md - Project context, bounded contexts         │
│     ├── Project AGENTS.md - Local workflow instructions                     │
│     └── Team conventions that DON'T conflict with above                     │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  CONFLICT RESOLUTION:                                                       │
│  If ANY local instruction conflicts with hangar-ai-constitution,         │
│  the hangar-ai-constitution ALWAYS wins. No exceptions.                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Initialize Hangar SDD in Your Repo

Hangar SDD (Software Design Document) is tool-independent, per **ENG-11.1 (Hangar SDD Law, NON-NEGOTIABLE)**. No CLI installation is required — everything is plain file operations.

### 1.1 Create the Hangar SDD Directory Structure

```bash
# Navigate to your project root
cd /path/to/your-project

# Create the Hangar SDD folder structure
mkdir -p hangar-ai-specs/{changes,archive,specs}
```

This creates:
```
hangar-ai-specs/
├── changes/         # Active change proposals (PROPOSE phase)
├── specs/           # Baseline specifications
└── archive/         # Completed changes (ARCHIVE phase)
```

### 1.2 Create the Hangar SDD README

```bash
cat > hangar-ai-specs/README.md << 'EOF'
# Hangar SDD

This directory contains all Hangar Software Design Documents for this project.

- **changes/**: Active proposals in PROPOSE → IMPLEMENT lifecycle
- **specs/**: Baseline specifications (source of truth)
- **archive/**: Completed and archived changes

Governed by ENG-11.1 (Hangar SDD Law). See `skill-spec-governance` for the
full proposal lifecycle and checklist.
EOF
```

### 1.3 Create Root AGENTS.md (Critical)

Create `AGENTS.md` in your **repository root** with the following template. This file establishes the link to hangar-ai-constitution and the precedence rules.

> For the full proposal lifecycle — how to create change directories, populate `PROPOSAL.md` and `tasks.md`, and archive — invoke `skill-spec-governance` in your AI assistant or read `agent-skills/skills-by-domain/discovery-research/spec-governance.md` directly.

---

## Step 2: Create Root AGENTS.md

**This is the most important file.** It tells AI assistants that this project follows the AA Hangar AI Constitution and establishes the authority hierarchy.

### Root AGENTS.md Template

Create `AGENTS.md` in your repository root:

```markdown
# AI Agent Instructions

> **Authority:** hangar-ai-constitution
> **Project:** [Your Project Name]
> **Domain:** [Cargo & Freight | Passenger Booking | Loyalty | etc.]
> **Stack:** [Java/Spring | Python/FastAPI | React/TypeScript | etc.]

---

## CRITICAL: Authority Hierarchy

**The hangar-ai-constitution is the SUPREME AUTHORITY for this project.**

When working in this repository, you MUST follow this precedence order:

### 1. hangar-ai-constitution (HIGHEST - NEVER OVERRIDE)

**Location:** https://github.com/AAInternal/hangar-ai-constitution

**You MUST read and follow:**
- `constitution/base/ENGINEERING-CONSTITUTION.md` - Engineering laws
- `constitution/base/PRODUCT-CONSTITUTION.md` - Product laws
- `constitution/base/BUSINESS-CONSTITUTION.md` - Business & compliance laws
- `constitution/avatars/industry/aviation-faa/ADOPTION.md` - Aviation compliance
- `constitution/avatars/technology/[STACK]/ADOPTION.md` - Stack-specific laws
- `constitution/avatars/product-type/[DOMAIN]/ADOPTION.md` - Domain-specific laws
- `agent-skills/base/AGENT.md` - Core agent operating skills
- `agent-skills/avatars/technology/[STACK].md` - Stack-specific agent behaviors
- `agent-skills/avatars/product-type/[DOMAIN].md` - Domain-specific patterns

### 2. Project-Specific Instructions (EXTENDS, NEVER OVERRIDES)

**Location:** This repository

- `project-rules.md` - Project context and extensions (at repository root)

### 3. Conflict Resolution

**If ANY instruction in this repository conflicts with hangar-ai-constitution:**
- The hangar-ai-constitution ALWAYS takes precedence
- Flag the conflict to the engineer
- Follow the hangar-ai-constitution law
- Suggest updating the local instruction to align

---

## ⛔ MANDATORY AGENT PROTOCOL

**Every coding task MUST follow this exact 8-step cycle. No exceptions.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              MANDATORY AGENT PROTOCOL (Per ENG-4.1 — NON-NEGOTIABLE)        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Step 1 — IDENTIFY   Find the FIRST unchecked task in tasks.md             │
│                       Read the linked spec scenario ID                      │
│                       ↓                                                     │
│  Step 2 — RED        Write EXACTLY ONE failing test                         │
│                       Run tests → Required output: FAILED                   │
│                       ⛔ SHOW the failure output before continuing           │
│                       ↓                                                     │
│  Step 3 — GREEN      Write MINIMUM code to make that ONE test pass          │
│                       Run tests → Required output: PASSED                   │
│                       ⛔ SHOW the pass output before continuing              │
│                       ↓                                                     │
│  Step 4 — REFACTOR   Improve code quality (no behavior changes)             │
│                       Run tests → Required output: still PASSED             │
│                       ↓                                                     │
│  Step 5 — VERIFY     Run full test suite + constitution-lint                │
│                       ALL gates must be green before proceeding             │
│                       ↓                                                     │
│  Step 6 — UPDATE     Open tasks.md and mark task [x] with ✓ + commit hash  │
│           TASKS.MD   Update progress summary counts                         │
│                       ↓                                                     │
│  Step 7 — COMMIT     git add -A && git commit -m "<conventional-msg>"      │
│                       Commit message MUST reference spec scenario ID        │
│                       ↓                                                     │
│  Step 8 — STOP AND   Report completed test, commit hash, and next task      │
│           REPORT     Wait for human confirmation before starting next cycle │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## ⛔ PROHIBITED ACTIONS

The following actions are **forbidden** and constitute a Constitutional violation:

| Prohibited Action | Law Violated |
|-------------------|-------------|
| Writing more than one test method per cycle | ENG-4.1 |
| Writing production code before a failing test exists | ENG-4.1 |
| Skipping the RED step (no failure proof shown) | ENG-4.1 |
| Skipping the REFACTOR step | ENG-4.1 |
| Skipping the VERIFY step (full suite + lint) | ENG-4.1, ENG-4.2 |
| Not updating tasks.md after a cycle completes | ENG-6.7 |
| Committing without a spec scenario ID in the message | ENG-6.7 |
| Batching multiple tests into one commit | ENG-4.1 |
| Touching files outside the current task scope | ENG-2.3 |
| Proceeding to the next cycle without human confirmation | ENG-1.2 |

## Self-Check Before Each Step

Before writing any code, answer these five questions aloud:

1. Have I identified the FIRST unchecked task in `tasks.md`?
2. Am I writing exactly ONE test — not a test class, not a test file, ONE test?
3. Have I confirmed the test FAILS before writing production code?
4. Have I confirmed ALL tests PASS after the GREEN step?
5. Have I updated `tasks.md` and committed with a scenario ID?

---

## Adopted Constitutions

This project adopts the following from hangar-ai-constitution:

### Base Constitutions (Required for ALL projects)
- [x] Engineering Constitution - Testing, code quality, architecture
- [x] Product Constitution - User journeys, metrics, accessibility
- [x] Business Constitution - Compliance, data governance, aviation

### Industry Adoption (Required for ALL AA projects)
- [x] Aviation/FAA - FAA Part 121, DO-178C, TSA, DOT compliance

### Technology Adoption
- [x] [YOUR STACK] - [e.g., Java/Spring Boot patterns and practices]

### Product-Type Adoption
- [x] [YOUR DOMAIN] - [e.g., Cargo & Freight domain patterns]

---

## Project Context

### What This Project Does
[Brief description of the project's purpose]

### Key Domain Concepts
- **[Term 1]:** [Definition]
- **[Term 2]:** [Definition]
- **[Term 3]:** [Definition]

### External Integrations
- **[System 1]:** [Purpose, e.g., "iCargo - Cargo rate quotes and AWB"]
- **[System 2]:** [Purpose, e.g., "GraphMailService - Email notifications"]

### Team Conventions (Must Not Conflict with Constitution)
- [Convention 1]
- [Convention 2]

---

## Quick Reference: Key Laws

### From Engineering Constitution
- **Atomic TDD:** RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT
- **Test Coverage:** ≥90% line coverage, ≥85% branch coverage
- **Complexity:** Cyclomatic ≤10, Cognitive ≤7
- **Immutability:** Value objects and DTOs must be immutable

### From Business Constitution
- **Aviation Compliance:** All code must comply with applicable FAA, TSA, DOT regulations
- **Audit Trail:** Financial transactions and compliance decisions must be auditable
- **Data Governance:** PII handling follows privacy-by-design

### From Product Constitution
- **User-Centric:** Every feature must trace to a user problem
- **Accessibility:** WCAG 2.1 AA minimum
- **Metrics:** Features require success metrics before building

---

## For AI Assistants

When starting work on this project:

1. **FIRST:** Read the hangar-ai-constitution base constitutions
2. **SECOND:** Read the relevant adoptions (aviation-faa, your technology, your domain)
3. **THIRD:** Read this file and `project-rules.md`
4. **FOURTH:** Follow the `⛔ MANDATORY AGENT PROTOCOL` above for every coding task
5. **Find the first unchecked task** in `tasks.md` — do not decide what to implement

**Remember:** You are bound by hangar-ai-constitution laws. If an engineer asks you to do something that violates the Constitution, you must refuse and explain which law would be violated.

---

**Last Updated:** [Date]
**Constitution Version:** [Version from hangar-ai-constitution]
```

---

## Step 3: Adopt Constitutions and Agent Instructions

### 3.1 Select Your Adoptions

Choose the appropriate adoptions for your project:

**Technology Avatars (pick one):**
| Stack | Adoption Path |
|-------|---------------|
| Java/Spring Boot | `constitution/avatars/technology/java-spring/ADOPTION.md` |
| Python/FastAPI | `constitution/avatars/technology/python-fastapi/ADOPTION.md` |
| React/TypeScript | `constitution/avatars/technology/react-frontend/ADOPTION.md` |
| Node.js/TypeScript | `constitution/avatars/technology/nodejs-typescript/ADOPTION.md` |
| .NET Core | `constitution/avatars/technology/dotnet-core/ADOPTION.md` |
| Angular | `constitution/avatars/technology/angular-frontend/ADOPTION.md` |

**Product Domain Adoptions (pick one):**
| Domain | Adoption Path |
|--------|---------------|
| Passenger Booking | `constitution/avatars/product-type/passenger-booking/ADOPTION.md` |
| Check-In & Travel | `constitution/avatars/product-type/check-in-travel/ADOPTION.md` |
| Cargo & Freight | `constitution/avatars/product-type/cargo-freight/ADOPTION.md` |
| Loyalty (AAdvantage) | `constitution/avatars/product-type/loyalty-aadvantage/ADOPTION.md` |
| Airport Operations | `constitution/avatars/product-type/airport-operations/ADOPTION.md` |
| Customer Service | `constitution/avatars/product-type/customer-service/ADOPTION.md` |

**Industry Adoption (required for ALL):**
- `constitution/avatars/industry/aviation-faa/ADOPTION.md`

### 3.2 Create project-rules.md

Use this template for `project-rules.md` at your repository root:

```markdown
# [Project Name] Constitution

**Authority:** hangar-ai-constitution (https://github.com/AAInternal/hangar-ai-constitution)
**Version:** 1.0.0
**Established:** [Date]
**Stack:** [Primary Technology Stack]
**Domain:** [Product Domain]

> This Constitution EXTENDS the hangar-ai-constitution with project-specific context.
> It CANNOT override any laws from the central constitution.

---

## Article 0: Project Context

### Section 0.1: Project Overview
[Describe what this project does, who uses it, why it exists]

### Section 0.2: Technology Stack
| Layer | Technology | Version |
|-------|------------|---------|
| Language | [e.g., Java] | [e.g., 21] |
| Framework | [e.g., Spring Boot] | [e.g., 3.4] |
| Database | [e.g., PostgreSQL] | [e.g., 16] |

### Section 0.3: Bounded Contexts
[List your domain's bounded contexts]

### Section 0.4: External Integrations
| System | Purpose | Protocol |
|--------|---------|----------|
| [e.g., iCargo] | [e.g., Rate quotes, AWB] | [e.g., REST/SOAP] |
| [e.g., GraphMailService] | [e.g., Email notifications] | [e.g., REST] |

---

## Article I: Adopted Constitutions (from hangar-ai-constitution)

### Base Constitutions
- Engineering Constitution - `constitution/base/ENGINEERING-CONSTITUTION.md`
- Product Constitution - `constitution/base/PRODUCT-CONSTITUTION.md`
- Business Constitution - `constitution/base/BUSINESS-CONSTITUTION.md`

### Industry Adoption
- Aviation/FAA - `constitution/avatars/industry/aviation-faa/ADOPTION.md`

### Technology Adoption
- [Your Stack] - `constitution/avatars/technology/[stack]/ADOPTION.md`

### Product-Type Adoption
- [Your Domain] - `constitution/avatars/product-type/[domain]/ADOPTION.md`

---

## Article II: Project-Specific Domain Laws
[Project-specific business rules and invariants that don't conflict with central constitution]

---

## Article III: Project-Specific Integration Laws
[How this project integrates with external systems - specifics beyond the adoption guides]

---

## Appendix: Project-Specific Examples

[Good/bad code examples specific to THIS project's bounded contexts]
```

### 3.3 Project-Specific Agent Instructions

The root `AGENTS.md` (created in Step 2) is the single entry point for all AI assistants. Add project-specific workflow sections directly to it — there is no separate `hangar-ai-specs/AGENTS.md`.

Extend the root `AGENTS.md` with a project-specific commands block:

```markdown
## Project-Specific Commands

| Action | Command |
|--------|---------|
| Run tests | `./mvnw test` |
| Run specific test | `./mvnw test -Dtest=ClassName` |
| Check coverage | `./mvnw jacoco:report` |
| Check complexity | `./mvnw pmd:check` |

## Project-Specific Patterns

### [Pattern Name]
[Description of project-specific pattern that aligns with Constitution]

## Current Sprint Focus

- Active Change: `hangar-ai-specs/changes/[current]/`
- Priority: [Current priority area]
```

---

## Step 4: Hangar SDD Workflow

Hangar SDD uses plain file operations — no CLI required. The lifecycle is **PROPOSE → IMPLEMENT → ARCHIVE**, governed by **ENG-11.1**.

### 4.1 File Operations Reference

| Action | Operation |
|--------|-----------|
| Create a new change proposal | `mkdir -p hangar-ai-specs/changes/[verb-noun-id]` |
| Check proposal status | Review checkboxes in `tasks.md` |
| Validate proposal structure | Review `PROPOSAL.md` against ENG-11.2 checklist |
| Archive completed change | `mv hangar-ai-specs/changes/[id] hangar-ai-specs/archive/` |
| Browse active changes | `ls hangar-ai-specs/changes/` |
| Browse specs | `ls hangar-ai-specs/specs/` |

### 4.2 Feature Development Workflow

**Step 1: Create a New Change**
```bash
# Create the change directory (use a descriptive verb-noun-id)
mkdir -p hangar-ai-specs/changes/add-tsa-vetting-validation

# Create the required proposal files
touch hangar-ai-specs/changes/add-tsa-vetting-validation/PROPOSAL.md
touch hangar-ai-specs/changes/add-tsa-vetting-validation/tasks.md
```

**Step 2: Populate Planning Documents**

Fill in `PROPOSAL.md` (what, why, acceptance criteria) and `tasks.md` (TDD cycles as checkboxes). Optional: add `design.md`, `PROGRESS.md`, or `SPEC.md`.

For the full document format, invoke `skill-spec-governance` in your AI assistant.

**Step 3: Validate Before Implementation**

Review `PROPOSAL.md` against the ENG-11.2 checklist:
- [ ] Problem statement is clear
- [ ] Acceptance criteria are testable
- [ ] Vertical slices defined
- [ ] `tasks.md` checkboxes created (one per TDD cycle)

**Step 4: Implement with Constitutional TDD**

Work through `tasks.md` checkboxes one at a time. Each checkbox = one RED → GREEN → REFACTOR cycle per ENG-4.1.

**Step 5: Archive When Complete**
```bash
# Move the completed change to archive
mv hangar-ai-specs/changes/add-tsa-vetting-validation hangar-ai-specs/archive/
```

### 4.3 Viewing and Exploring

```bash
# List all active changes:
ls hangar-ai-specs/changes/

# List all specs:
ls hangar-ai-specs/specs/

# Check progress on a specific change:
cat hangar-ai-specs/changes/add-tsa-vetting-validation/tasks.md

# View a proposal:
cat hangar-ai-specs/changes/add-tsa-vetting-validation/PROPOSAL.md
```

---

## Step 5: Prompt Patterns for Constitutional Development

### Pattern 1: Starting a New Feature with Hangar SDD

**Prompt Template:**
```
I need to implement [feature description].

First, let's use Hangar SDD to set up this feature properly:
1. Invoke `skill-spec-governance` to create the change directory and proposal files
2. Generate planning documents (PROPOSAL.md, tasks.md)

Then, following the hangar-ai-constitution:
1. Read the relevant adoption guides (aviation-faa, [technology], [domain])
2. Review PROPOSAL.md against the ENG-11.2 checklist
3. Follow Atomic TDD for implementation — work through tasks.md checkboxes
```

**Example:**
```
I need to implement TSA vetting validation for PAL applications.

First, let's use Hangar SDD:
1. Invoke `skill-spec-governance` to create hangar-ai-specs/changes/add-tsa-vetting-validation/
2. Generate PROPOSAL.md with problem statement, acceptance criteria, and vertical slices

Then, following the hangar-ai-constitution:
1. Read cargo-freight adoption for domain patterns
2. Read aviation-faa adoption for TSA compliance requirements
3. Review PROPOSAL.md against ENG-11.2 checklist
4. Implement with Atomic TDD — work through tasks.md checkboxes one at a time
```

---

### Pattern 2: Reviewing Existing Code

**Prompt Template:**
```
Review [file/component] for Constitutional compliance.

Check against:
- Article III: Code Quality Laws (complexity limits, immutability, Law of Demeter)
- Article IV: Testing Laws (coverage, structure, naming)
- Article VI: Security Laws (input validation, authentication)

For each violation found:
1. Cite the specific Article and Section
2. Show the violating code
3. Provide a compliant alternative
```

**Example:**
```
Review src/services/PalApplicationService.java for Constitutional compliance.

Check against:
- Section 3.1: Complexity Limits (cyclomatic ≤10, cognitive ≤7)
- Section 3.2: Immutability Law (are value objects immutable?)
- Section 3.3: Law of Demeter (any train wrecks?)

For each violation found:
1. Cite the specific Article and Section
2. Show the violating code
3. Provide a compliant alternative with TDD approach to fix it
```

---

### Pattern 2: Reviewing Existing Code

**Prompt Template:**
```
Review [file/component] for Constitutional compliance.

Check against:
- Article III: Code Quality Laws (complexity limits, immutability, Law of Demeter)
- Article IV: Testing Laws (coverage, structure, naming)
- Article VI: Security Laws (input validation, authentication)

For each violation found:
1. Cite the specific Article and Section
2. Show the violating code
3. Provide a compliant alternative
```

**Example:**
```
Review src/services/PalApplicationService.java for Constitutional compliance.

Check against:
- Section 3.1: Complexity Limits (cyclomatic ≤10, cognitive ≤7)
- Section 3.2: Immutability Law (are value objects immutable?)
- Section 3.3: Law of Demeter (any train wrecks?)

For each violation found:
1. Cite the specific Article and Section
2. Show the violating code
3. Provide a compliant alternative with TDD approach to fix it
```

---

### Pattern 3: TDD Implementation Session

**Prompt Template:**
```
Let's implement [component] using strict Atomic TDD.

Rules:
1. Write ONE failing test
2. I'll confirm the test fails
3. Write MINIMUM code to pass
4. I'll confirm it passes
5. Suggest refactoring if needed
6. Commit message for this cycle
7. Repeat

Start with the simplest behavior first. Reference Constitution articles as you explain decisions.
```

**Example:**
```
Let's implement a Money value object using strict Atomic TDD.

Rules:
1. Write ONE failing test
2. I'll confirm the test fails
3. Write MINIMUM code to pass
4. I'll confirm it passes
5. Suggest refactoring if needed
6. Commit message for this cycle
7. Repeat

Start with: "Money can be created with amount and currency"
Reference Constitution Section 3.2 (Immutability Law) as you explain decisions.
```

---

### Pattern 4: Refactoring to Compliance

**Prompt Template:**
```
This code violates [specific Constitutional law]:

[paste violating code]

Refactor it to be compliant while:
1. Maintaining existing behavior (characterization tests first if needed)
2. Following Atomic TDD for the refactoring
3. Explaining each step with Constitutional references
4. Keeping changes minimal and focused
```

**Example:**
```
This code violates Section 3.1 (Complexity Limits) - cyclomatic complexity is 15:

```python
def process_order(order):
    if order is not None:
        if order.items:
            for item in order.items:
                if item.quantity > 0:
                    if item.product.is_available:
                        # ... 50 more lines of nested logic
```

Refactor it to be compliant while:
1. Write characterization tests first to lock current behavior
2. Extract methods to reduce complexity to ≤10
3. Use guard clauses to reduce nesting to ≤3 levels
4. Follow Atomic TDD for each extraction
```

---

### Pattern 5: Creating a New Service

**Prompt Template:**
```
Create a new [ServiceName] following our Constitution.

The service should:
- [List responsibilities]

Apply these Constitutional laws:
- Section 2.1: DDD (aggregate roots, value objects, domain services)
- Section 2.2: Layered Architecture (proper layer separation)
- Section 4.1: Atomic TDD (test-first development)

Use our [Java/Python/TypeScript] adoption guide for language-specific patterns.
```

**Example:**
```
Create a new PaymentService following our Constitution.

The service should:
- Process payments via external iCargo service
- Create payment records
- Publish payment events

Apply these Constitutional laws:
- Section 2.1: DDD - Payment as aggregate root, Money as value object
- Section 2.2: Layered Architecture - service orchestrates, domain has rules
- Section 4.1: Atomic TDD - test-first, one test at a time
- Section 7.2: Circuit Breaker - protect iCargo service calls

Use our Python/FastAPI adoption guide for language-specific patterns.
```

---

### Pattern 6: Debugging with Constitution Awareness

**Prompt Template:**
```
I'm seeing [error/bug description].

Before fixing:
1. Check if existing code violates any Constitutional laws
2. The fix should not introduce new violations
3. Add tests that would have caught this (TDD even for fixes)

After diagnosis, walk me through:
1. Root cause (including any Constitutional violations that contributed)
2. Test that reproduces the bug (RED)
3. Minimal fix (GREEN)
4. Any refactoring needed for compliance (REFACTOR)
```

---

## Step 6: Handling Violations

### When AI Suggests Non-Compliant Code

**Prompt:**
```
Stop. That code violates [specific law].

Please:
1. Acknowledge the violation
2. Cite the specific Constitutional article
3. Provide a compliant alternative
4. Explain why the compliant version is better
```

### When You Find Existing Violations

**Prompt:**
```
I found this existing violation of [Constitutional article]:

[code snippet]

Create a refactoring proposal that:
1. Documents the current violation
2. Proposes a compliant solution
3. Outlines the TDD approach to refactor
4. Estimates the scope of change
```

### When Laws Conflict

**Prompt:**
```
I'm seeing a conflict between [Law A] and [Law B] in this situation:

[describe situation]

According to Section 1.1 (Priority Hierarchy), which takes precedence?
How should I proceed while respecting both laws as much as possible?
```

---

## Step 7: Evolving Your Constitution

### Proposing Amendments

**Prompt:**
```
I believe we need to amend the Constitution because:

[describe the gap or problem]

Draft an amendment proposal that:
1. Identifies the Article/Section to modify
2. Provides the current text
3. Proposes new text
4. Explains the rationale
5. Shows examples of compliant/non-compliant code under new law
```

### Adding Project-Specific Laws

**Prompt:**
```
We have a recurring pattern in our project that should be codified:

[describe the pattern]

Create a new Section in our project-rules that:
1. Names the law clearly
2. States the rule unambiguously
3. Provides rationale
4. Shows compliant and non-compliant examples
5. Specifies enforcement mechanism
```

---

## Real Prompt Examples by Domain

### Cargo & Freight Domain

#### Example 1: PAL Application Vetting

```
I need to implement TSA vetting for PAL (Partner Airline) applications.

Context:
- Domain: Cargo & Freight (reference cargo-freight adoption)
- Entities: PalApplication, VettingAnswer, Applicant
- External: TSA vetting service via iCargo API
- Compliance: TSA security requirements, audit trail mandatory

Before coding, apply all three constitutions:
1. Engineering Constitution, Article IV: Atomic TDD for all vetting logic
2. Business Constitution, Article XII: TSA compliance requirements
3. Product Constitution, Article III: User journey for cargo agents

Create a proposal that addresses:
1. VettingAnswer as immutable value object (Engineering, Section 3.2)
2. Audit trail for all vetting decisions (Business, Section 7.1)
3. Circuit breaker for TSA service calls (Engineering, Section 7.2)
4. Retry with idempotency key (Engineering, Section 7.6)

Start with the first failing test for: "Applicant with valid documentation passes vetting"
```

#### Example 2: AWB (Air Waybill) Processing

```
Implement AWB creation workflow for cargo shipments.

Requirements:
- Generate AWB number following IATA format
- Validate dangerous goods declarations
- Calculate charges based on weight/volume
- Integrate with iCargo for rate quotes

Constitutional compliance:
- Engineering: DDD with AWB as aggregate root (Section 2.1)
- Business: Dangerous goods compliance per IATA DGR (Article XII)
- Product: Cargo agent efficiency metrics (Article V)

Apply Aviation/FAA adoption for:
- DO-178C traceability if this affects flight safety systems
- TSA cargo screening requirements

First test: "AWB created with valid shipper generates IATA-compliant number"
Walk me through the TDD cycle with Constitution references.
```

---

### Passenger Booking Domain

#### Example 3: Flight Search and Pricing

```
Implement flight search with fare transparency.

Context:
- Domain: Passenger Booking (reference passenger-booking adoption)
- Compliance: DOT fare advertising rules, price transparency
- Integration: Sabre/Amadeus for availability

Apply all three constitutions:
1. Engineering: Test pyramid with 70% unit tests for pricing logic
2. Business: DOT Article XII requirements for fare display
3. Product: Search-to-book conversion metrics (Article V)

Requirements:
- Display total price including all mandatory fees (DOT compliance)
- Show fare rules and restrictions
- Support multi-city itineraries

First test following TDD: "Search results display total price including taxes and carrier fees"

Ensure we reference:
- Business Constitution Section 12.1 for DOT consumer protection
- Engineering Constitution Section 4.1 for Atomic TDD
```

#### Example 4: Ancillary Services (Seat Selection, Bags)

```
Add seat selection to the booking flow.

Domain context (from passenger-booking adoption):
- Reservation aggregate with SeatAssignment value object
- Integration with departure control system
- Revenue optimization constraints

Constitutional requirements:
- Engineering Section 2.1: SeatAssignment as value object (immutable)
- Engineering Section 3.1: Complexity ≤10 for seat map rendering
- Product Section 3.2: Accessibility for seat selection UI (WCAG 2.1 AA)
- Business Section 4.1: Audit trail for paid seat upgrades

TDD approach:
1. Test: "Available seat can be selected and assigned to passenger"
2. Test: "Occupied seat cannot be double-assigned"
3. Test: "Seat assignment persists across session"
4. Test: "Premium seat charges are calculated correctly"

Start with test 1, applying Engineering Constitution Article IV.
```

---

### Loyalty (AAdvantage) Domain

#### Example 5: Miles Earning Calculation

```
Implement miles earning for flight activity.

Context:
- Domain: Loyalty/AAdvantage (reference loyalty-aadvantage adoption)
- Entities: AAdvantageAccount, MilesTransaction, FlightActivity
- Business rule: Base miles + status bonus + promotion multipliers

Apply constitutions:
1. Engineering: MilesTransaction as immutable (Section 3.2)
2. Business: Financial audit trail for miles (Section 7.1)
3. Product: Member dashboard showing earning breakdown

Critical requirements:
- All transactions immutable (no balance updates without transaction record)
- Audit trail for SOX compliance on miles liability
- Status tier affects earning multiplier

First test: "Gold member earns 25% bonus miles on qualifying flight"

Follow Business Constitution Article VII for domain rules:
- Miles are a liability; every credit must have a transaction
- Reversals create offsetting transactions, not deletions
```

#### Example 6: Award Redemption

```
Implement award booking with miles redemption.

Business rules (from loyalty-aadvantage adoption):
- Check miles balance before booking
- Deduct miles atomically with ticket creation
- Handle partner award pricing (different rates)

Constitutional compliance:
- Engineering Section 2.1: Award as aggregate, AwardRedemption as entity
- Engineering Section 7.6: Idempotent redemption (prevent double-deduction)
- Business Section 7.1: Full audit trail for redemptions
- Product Section 4.2: A/B test award pricing display

Critical test cases:
1. "Sufficient balance allows award booking"
2. "Insufficient balance rejects with clear message"
3. "Partial failure rolls back miles deduction"
4. "Duplicate request is idempotent (same result, no double-deduct)"

Start TDD with test 1. Reference Engineering Article IV throughout.
```

---

### Airport Operations Domain

#### Example 7: Crew Legality Check

```
Implement FAR Part 117 crew rest validation.

Context:
- Domain: Airport Operations (reference airport-operations adoption)
- Compliance: FAA FAR Part 117 duty/rest limits
- Entities: CrewMember, DutyPeriod, FlightAssignment

Apply Aviation/FAA adoption for:
- DO-178C if this is a Level C safety system
- FAR Part 117 specific rules in Business Constitution

Constitutional requirements:
- Engineering Section 4.3: 90%+ coverage on legality calculations
- Business Section 12.1: FAA compliance is non-negotiable
- Product Section 3.1: Ops controller can quickly see legal status

Test cases for FAR Part 117:
1. "Pilot within duty limits returns LEGAL"
2. "Pilot exceeding flight duty period returns ILLEGAL with reason"
3. "Pilot without required rest returns ILLEGAL"
4. "Augmented crew has extended limits"

This is safety-critical. Apply Engineering Constitution Article VI for resiliency.
Start with test 1, ensuring full traceability per DO-178C.
```

#### Example 8: Gate Conflict Resolution

```
Implement gate assignment with conflict detection.

Domain context:
- Gate as resource, Flight as requester
- Conflict when two flights need same gate at overlapping times
- Auto-suggest alternatives when conflict detected

Constitutional compliance:
- Engineering Section 2.1: Gate and GateAssignment as separate entities
- Engineering Section 4.2: Unit tests for conflict detection algorithm
- Product Section 3.3: Real-time updates for ops controllers

Requirements:
- Detect overlap with 15-minute buffer for turns
- Suggest next available gate of same type
- Log all assignments for operational analysis

First test: "Overlapping flight times on same gate returns conflict"
Apply TDD strictly - this affects on-time performance.
```

---

### Customer Service Domain

#### Example 9: DOT-Compliant Refund Processing

```
Implement refund workflow meeting DOT timelines.

Context:
- Domain: Customer Service (reference customer-service adoption)
- Compliance: DOT refund rule (7 days credit card, 20 days cash)
- Integration: Payment gateway for refund processing

Apply all three constitutions:
1. Engineering: RefundRequest aggregate, RefundTransaction immutable
2. Business: DOT Article XII timeline enforcement
3. Product: Customer satisfaction metrics on refund experience

Critical requirements:
- Track refund request timestamp
- Calculate deadline based on payment method
- Alert when approaching deadline
- Full audit trail for DOT compliance

Test cases:
1. "Credit card refund requested, deadline set to 7 days"
2. "Cash refund requested, deadline set to 20 days"
3. "Refund processed within deadline, marked compliant"
4. "Approaching deadline triggers escalation alert"

This has regulatory consequences. Apply Business Constitution Article IX strictly.
```

#### Example 10: IROP Rebooking Automation

```
Implement automated rebooking for irregular operations.

Context:
- IROP = Irregular Operations (delays, cancellations, diversions)
- Must rebook affected passengers to next available flight
- Elite status affects rebooking priority

Apply constitutions:
- Engineering: Event-driven architecture (Section 2.4)
- Business: Customer compensation rules by delay length
- Product: Minimize customer effort during disruption

Requirements:
- Listen for flight cancellation events
- Find alternative flights matching original routing
- Prioritize by elite status, then booking class
- Send proactive notification with new itinerary
- Track for DOT delay reporting

First test: "Cancelled flight triggers rebooking event for all passengers"

Apply customer-service adoption patterns:
- Empathetic error messages (not just error codes)
- DOT compensation calculation for qualifying delays
```

---

### Cross-Domain Examples

#### Example 11: Teaching Session with AA Context

```
I'm onboarding a new engineer to the cargo team. Create a teaching session.

Cover:
1. Why we have three constitutions (Engineering, Product, Business)
2. How Aviation/FAA adoption affects our daily work
3. Walk through PalApplication lifecycle as DDD example
4. Demonstrate TDD with VettingAnswer value object
5. Show TSA compliance requirements from Business Constitution

Format as interactive tutorial. Use real examples from:
- cargo-freight adoption for domain patterns
- aviation-faa adoption for compliance requirements

Start with: "Why does American Airlines need a Constitutional AI framework?"
```

#### Example 12: Multi-Domain Integration

```
Implement passenger rebooking that earns compensation miles.

This crosses domains:
- Customer Service: IROP rebooking logic
- Loyalty: Compensation miles award
- Passenger Booking: New reservation creation

Apply constitutions across domains:
- Engineering: Saga pattern for distributed transaction
- Business: Compensation rules vary by elite status
- Product: Single notification with complete information

Ensure:
- Rebooking and miles award are atomic (both succeed or both fail)
- Audit trail spans both domains
- Customer sees unified experience

Start with integration test: "IROP rebooking awards compensation miles to AAdvantage member"
```

---

## Quick Reference: Essential Prompts

| Situation | Prompt Start |
|-----------|--------------|
| New feature | "Implement X following our Constitution. Read the relevant adoptions first..." |
| Code review | "Review X for Constitutional compliance. Check Sections 3.1, 3.2, 4.1..." |
| TDD session | "Let's implement X using strict Atomic TDD. One test at a time..." |
| Refactoring | "This violates Section X. Refactor to compliance using TDD..." |
| Bug fix | "Production bug: X. Write failing test first, then fix. Check Section..." |
| New service | "Create X service. Apply DDD (2.1), Layers (2.2), Testing (4.1)..." |
| Teaching | "Explain why we do X, with examples from our Constitution..." |

---

## Troubleshooting

### "AI isn't following the Constitution"

1. Verify the root `AGENTS.md` exists and references hangar-ai-constitution
2. Check that the authority hierarchy is clearly stated in AGENTS.md
3. Explicitly ask the AI to read hangar-ai-constitution before coding:
   ```
   Before writing code, please read the hangar-ai-constitution at
   https://github.com/AAInternal/hangar-ai-constitution and confirm
   you understand the Engineering, Product, and Business constitutions.
   ```
4. Quote specific articles when asking for work
5. Ask AI to cite articles when explaining decisions

### "Local instructions conflict with hangar-ai-constitution"

**Resolution:** hangar-ai-constitution ALWAYS wins.

1. Identify the conflicting local instruction
2. Update the local instruction to align with the central constitution
3. If you believe the central constitution is wrong, open an issue in hangar-ai-constitution repo
4. Never override central laws in local files

### "The Constitution doesn't cover my case"

1. Check if it's covered in your technology or product-type adoption
2. Check if it's covered in the aviation-faa industry adoption
3. If not covered, propose an amendment to your project-rules (for project-specific cases)
4. For cases that should apply to all AA projects, open an issue in hangar-ai-constitution

### "TDD feels slow"

1. Trust the process - it speeds up over time
2. Each cycle should take at most a few minutes
3. If cycles are longer, you're taking too big a step
4. The safety net of tests enables faster future changes
5. AI helps generate tests quickly - leverage it

### "How do I know which adoption to use?"

| If your project is... | Technology Adoption | Product-Type Adoption |
|-----------------------|--------------------|-----------------------|
| Backend API in Java | java-spring | Based on domain |
| Backend API in Python | python-fastapi | Based on domain |
| Frontend in React | react-typescript | Based on domain |
| Handles PAL applications | Your backend stack | cargo-freight |
| Handles flight bookings | Your backend stack | passenger-booking |
| Handles AAdvantage | Your backend stack | loyalty-aadvantage |
| Handles crew/gates | Your backend stack | airport-operations |
| Handles complaints/refunds | Your backend stack | customer-service |

---

## Quick Reference: Files to Create

| File | Location | Purpose |
|------|----------|---------|
| `AGENTS.md` | Repository root | Links to hangar-ai-constitution, establishes precedence, project-specific instructions |
| `project-rules.md` | Repository root | Project-specific extensions (cannot override central) |
| `hangar-ai-specs/` | Repository root | Hangar SDD change proposals, specs, and archive |

---

**Maintained by:** The Hangar, American Airlines IT

*This guide should be updated as new patterns emerge from Constitutional development.*

---
domain: product
article: II
title: Discovery Laws
laws:
  - id: PRD-2.1
    title: Problem Validation Law
    summary: All problems MUST be validated before solution design with evidence
  - id: PRD-2.2
    title: Assumption Mapping Law
    summary: All assumptions MUST be documented and tested systematically
  - id: PRD-2.3
    title: Jobs-to-be-Done Law
    summary: User needs SHALL be framed as jobs, not features
  - id: PRD-2.4
    title: Competitive Analysis Law
    summary: Market context MUST be understood with direct, indirect competitors, and alternatives
  - id: PRD-2.5
    title: Discovery Stage-Gate Law
    non_negotiable: true
    summary: Discovery stages SHALL progress sequentially with documented evidence gates — no stage may begin without prior stage exit criteria met and evidence filed in hangar-ai-specs/
  - id: PRD-2.6
    title: Multi-Cognition Phase Gate Jury Law
    non_negotiable: true
    summary: Every discovery stage exit gate SHALL be challenged by a multi-model, multi-persona jury before the stage may advance
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article II: Discovery Laws

## Section 2.1: Problem Validation Law

**Law ID:** `PRD-2.1`

All problems MUST be validated before solution design.

### Validation Requirements

1. **Problem exists** - Users experience this pain
2. **Problem matters** - It's significant enough to act on
3. **Problem is solvable** - A solution is feasible
4. **Users will pay** - They'll exchange value (money, time, data)

### Evidence Template

```
Problem Statement: [Clear, specific description]

Evidence:
- Qualitative: [X] interviews conducted, [key quotes]
- Quantitative: [Y]% of users experience this, [Z] support tickets
- Market: [Competitor approaches, market size]

Validation Status: [ ] Not Started [ ] In Progress [✓] Validated [ ] Invalidated
```

---

## Section 2.2: Assumption Mapping Law

**Law ID:** `PRD-2.2`

All assumptions MUST be documented and tested.

### Assumption Categories

| Type | Question | Test Method |
|------|----------|-------------|
| **Desirability** | Do users want this? | Interviews, prototypes, landing pages |
| **Viability** | Can we make money? | Pricing tests, financial modeling |
| **Feasibility** | Can we build it? | Spikes, technical research |
| **Usability** | Can users figure it out? | Usability testing |

### Assumption Prioritization Matrix

```
                HIGH RISK
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    │  Test Later   │  Test First   │
    │  (known,risky)│ (unknown,risky)
    │               │               │
LOW ├───────────────┼───────────────┤ HIGH
EVIDENCE            │           EVIDENCE
    │               │               │
    │  Ignore       │  Monitor      │
    │  (known,safe) │ (unknown,safe)│
    │               │               │
    └───────────────┼───────────────┘
                    │
                LOW RISK
```

---

## Section 2.3: Jobs-to-be-Done Law

**Law ID:** `PRD-2.3`

User needs SHALL be framed as jobs, not features.

### JTBD Format

```
When [situation],
I want to [motivation],
So I can [expected outcome].
```

### Example

```
❌ WRONG (Feature-focused)
"Users want a dashboard"

✅ CORRECT (Job-focused)
"When I start my workday,
I want to see what needs my attention,
So I can prioritize my time effectively."
```

### Required JTBD Documentation

- Core functional job
- Related jobs (what else are they trying to do?)
- Emotional jobs (how do they want to feel?)
- Social jobs (how do they want to be perceived?)

---

## Section 2.4: Competitive Analysis Law

**Law ID:** `PRD-2.4`

Market context MUST be understood.

### Required Analysis

1. **Direct competitors** - Same solution, same job
2. **Indirect competitors** - Different solution, same job
3. **Alternatives** - What users do today (including nothing)

### Competitive Intelligence Template

| Competitor | Strengths | Weaknesses | Positioning | Pricing |
|------------|-----------|------------|-------------|---------|
| ... | ... | ... | ... | ... |

### Differentiation Documentation

- What we do that others don't
- What we do better
- What we intentionally don't do

---

## Stage Gate Criteria

## Skip the Discovery Stage

## Moving to the Next Discovery Stage

## Section 2.5: Discovery Stage-Gate Law

**Law ID:** `PRD-2.5` | **Status:** NON-NEGOTIABLE

Discovery work SHALL progress through stages sequentially.

### Requirements

1. **Sequential stages** — No stage may begin until its entry gate is satisfied
2. **Evidence required** — Each stage transition requires a documented evidence artifact in `hangar-ai-specs/`
3. **Blocker resolution** — All blockers from the prior stage must be resolved before advancing
4. **Audit trail** — Every stage transition must be logged per BUS-7.1

### Stage Gate Sequence

```
Stage A → Stage B → Stage C → Stage D → Stage E → Stage F
  ↑           ↑           ↑           ↑           ↑           ↑
(problem   (field      (code       (internal   (metrics    (roadmap
 approved)  study      evidence    validation  baseline    locked)
            complete)  filed)      complete)   set)
```

### Prohibited Anti-Patterns

- Skipping stages to reach implementation faster
- Beginning Stage F (Roadmap Lock) without validated metrics (Stage E)
- Treating discovery as optional for new product initiatives
- Stage transitions without evidence in `hangar-ai-specs/`

### Governing Workflow

See `workflows/product-discovery-stage-a-f.md`

---

## Section 2.6: Multi-Cognition Phase Gate Jury Law

**Law ID:** `PRD-2.6` | **Status:** NON-NEGOTIABLE

Every discovery stage exit gate SHALL be challenged by a multi-model, multi-persona jury before the stage may advance.

### Rationale

Single-model, single-perspective review systematically reproduces the same cognitive blind spots as the model that produced the artifact. Evidence accuracy, causal claims, and framing choices require adversarial challenge from diverse professional viewpoints — backed by different reasoning models — before they can be represented as discovery findings to senior stakeholders. This law encodes that requirement.

### Requirements

1. **Minimum four jurors** — Each juror MUST be backed by a distinct LLM model. Running all jurors on the same model is PROHIBITED and constitutes self-certification under a different name.
2. **Persona diversity** — Jurors MUST represent distinct professional vantage points relevant to the stage being evaluated. Minimum composition:
   - One **domain sceptic** (challenges evidence methodology and data sources)
   - One **technical expert** (challenges causal and structural claims)
   - One **product/strategic lens** (challenges framing, scope, and audience-appropriateness)
   - One **defense counsel** (builds the strongest credible case for the claims — provides the minimum defensible version)
3. **Live investigation empowered** — Jurors SHALL have access to, and are expected to use, all available evidence sources: git history, ADO REST API, source code, previous stage artifacts, and any tool in the agent's context. Deliberation based only on the artifact text without independent verification is insufficient for Strong or Critical claims.
4. **Structured verdict per juror** — Each juror MUST return: `VALIDATED | QUALIFIED | CHALLENGED` with specific reasoning tied to cited evidence or lack thereof.
5. **Judicial synthesis required** — A synthesising agent (distinct from all jurors) MUST produce a consolidated finding covering: what is proven, what is inferred, what is overclaimed, and what requires further validation.
6. **Corrections are mandatory** — Any claim rated CHALLENGED or any QUALIFIED condition identified by ≥2 jurors MUST be corrected in the artifact before the stage exit gate may be satisfied. Corrections must be specific — vague hedges do not satisfy this requirement.
7. **Verdict documented in audit event** — The jury outcome (per-juror verdict, synthesis finding, corrections applied) MUST be recorded in the BUS-7.1 stage-transition audit event under a `jury_deliberation` block.
8. **Stage blocks on unresolved CHALLENGED verdicts** — A stage with one or more CHALLENGED findings that have not been corrected or formally rebutted CANNOT advance. The agent MUST halt and request resolution.

### Per-Stage Jury Focus

| Stage | Primary claims to challenge |
|-------|----------------------------|
| A | Problem statement validity; evidence for problem existence and materiality |
| B | Field study methodology; generalisability of insights; source reliability |
| C | Code evidence causality; root-cause vs symptom distinction; "always" / "never" absolute claims |
| D | Assumption validation rigour; alternative explanations eliminated; confidence ratings |
| E | Baseline source traceability; metric definitions; target achievability |
| F | Roadmap causal grounding; "fixable" and "specific" claims; sequencing rationale |

### Prohibited Anti-Patterns

- All jurors backed by the same model (constitutes single-model review)
- Jurors without domain-specific personas (generic "reviewer" or "critic" personas do not satisfy requirement)
- Deliberation conducted only on artifact text without investigating primary sources when sources are available
- Jury conducted after stage advancement (must precede exit gate sign-off)
- Verdicts without specific evidence citations (e.g. "seems reasonable" does not satisfy VALIDATED)
- Corrections that only add hedge language without substantively changing the overclaimed content

### Governing Workflow

See `workflows/product-discovery-stage-a-f.md` § Multi-Cognition Jury Gate Protocol

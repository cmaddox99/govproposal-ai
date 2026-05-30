<!-- slide 1 -->

# 🏛️ Constitutional SDD

## Engineering Laws for AI Agents

**AI Community of Practice**

February 2026

Presented by: Nag & Ali


---




<!-- slide 2 -->

# 📦 Wave 2: AA Cargo Results

## Before vs After Constitutional AI

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Test Coverage | 30% | 91% | +61% |
| Time to Implement | Days | 5 hours | 90% faster |
| AI Autonomy | Low | High | Predictable |
| Code Quality | Variable | Consistent | Enforced |

**Key Insight:** Laws gave AI the authority to enforce quality without human intervention


---




<!-- slide 3 -->

# 🎯 How We Achieved It

## The Secret Sauce

```
┌─────────────────────────────────────────────────────────────────┐
│  1. CONSTITUTION          2. AGENTS.md                          │
│     Laws that are            Entry point for AI                 │
│     NON-NEGOTIABLE           in every repo                      │
│                                                                 │
│  3. OPENSPEC              4. ATOMIC TDD                         │
│     Spec-driven              One test at a time                 │
│     development              Red -> Green -> Refactor           │
└─────────────────────────────────────────────────────────────────┘
```

**Result:** AI operates with clear boundaries and predictable behavior


---




<!-- slide 4 -->

# 🔄 Constitutional AI for Engineering

## Traditional vs Constitutional Approach

| Aspect | Traditional AI Coding | Constitutional AI |
|--------|----------------------|-------------------|
| Guardrails | Prompt engineering | Codified laws |
| Consistency | Varies by prompt | Enforced by constitution |
| Test Coverage | "Please write tests" | "ENG-4.1 REQUIRES tests first" |
| Quality | Hope for the best | Guaranteed by law |
| Autonomy | Limited, needs hand-holding | High, self-governing |

**The Shift:** From "AI as tool" to "AI as governed contributor"


---




<!-- slide 5 -->

# ⚖️ Key Engineering Laws

| Law | Name | What It Enforces |
|-----|------|------------------|
| **ENG-4.1** | Atomic TDD Law | Test-first, ONE test at a time |
| **ENG-4.2** | Test Pyramid Law | x% unit, y% integration, z% E2E |
| **ENG-9.1** | AI-Engineer Pairing Law | AI as teaching partner, not just generator |
| **ENG-3.1** | Complexity Limits | Cyclomatic complexity limits enforced |
| **ENG-6.7** | Audit Trail Law | All changes documented and traceable |

**Key Point:** Laws give AI **authority** and eliminate "it depends"

```
┌─────────────────────────────────────────────────────────────────┐
│  WITHOUT LAWS                       WITH LAWS                   │
│  ------------                       ---------                   │
│  AI: "Should I write tests?"        AI: "ENG-4.1 requires       │
│  Human: "It depends..."                  TDD. Writing test      │
│                                          first."                │
│  Result: Inconsistent               Result: Predictable quality │
└─────────────────────────────────────────────────────────────────┘
```


---




<!-- slide 6 -->

# 🆕 What's New in AA Engineering Laws

## Recent Updates

| Update | Description | Impact |
|--------|-------------|--------|
| **Token Optimization** | Hierarchical context segmentation | 89% token reduction |
| **Practice Guides** | Hands-on exercises for each law | Team enablement |


---




<!-- slide 7 -->

# 🎫 Token Optimization: Problem and Solution

## Why It Matters for AI-Assisted Development

```
┌─────────────────────────────────────────────────────────────────┐
│  THE PROBLEM                                                    │
│  -----------                                                    │
│  Full aa-engineering-laws         ~45,000 tokens                │
│  GitHub Copilot context           ~64,000 tokens                │
│  Remaining for YOUR CODE          ~19,000 tokens (only 30%)     │
│                                                                 │
│  Result: Laws compete with code for attention                   │
│                                                                 │
│  THE SOLUTION: RAG-Ready Hierarchical Architecture              │
│  ------------------------------------------------               │
│  Selective loading                ~5,000 tokens (laws)          │
│  Remaining for YOUR CODE          ~59,000 tokens (92%)          │
│                                                                 │
│  Result: Focused laws + more room for code context              │
└─────────────────────────────────────────────────────────────────┘
```

**Benefits:** More code context | Fewer rate limit hits | Faster responses


---




<!-- slide 8 -->

# 🎬 Live Demo: Token Optimization

## Practice Guide Prompt

Copy and run this prompt to see token optimization in action:

```
I'm working on a Java Spring Boot project and need help with:
1. Writing unit tests for a service
2. Following proper test naming conventions
3. Using the right Spring test annotations

Based on the aa-engineering-laws token-optimized structure, which files 
should you load? Explain why each file is needed.
```

**Expected AI Behavior:**
1. Loads `adoptions/index.yaml` first (router)
2. Identifies `java-spring` as relevant adoption
3. Loads only `java-spring/guidance.md`
4. Loads only relevant laws (ENG-4.1, ENG-4.2)
5. Skips nodejs-typescript, python-fastapi, etc.

**Result:** ~5,000 tokens instead of ~45,000


---




<!-- slide 9 -->

# 🔀 OpenSpec vs Spec Kit (Research Update)

## Core Difference

| Aspect | Spec Kit | OpenSpec |
|--------|----------|----------|
| **Designed For** | 0 to 1 (greenfield) | 0 to n (brownfield) |
| **Structure** | Rigid phases | Flexible, delta-based |
| **Context Model** | Regenerate full spec each cycle | Load only what changed |
| **Best For** | New projects | Evolving codebases (90% of AA work) |

```
┌─────────────────────────────────────────────────────────────────┐
│  SPEC KIT                          OPENSPEC                     │
│  --------                          --------                     │
│  Iteration 1: Generate spec        Iteration 1: Generate spec   │
│  Iteration 2: Regenerate spec      Iteration 2: Delta only      │
│  Iteration 3: Regenerate spec      Iteration 3: Delta only      │
│  ...                               ...                          │
│  Token cost: O(n)                  Token cost: O(1) per change  │
└─────────────────────────────────────────────────────────────────┘
```


---




<!-- slide 10 -->

# 👨‍💻 Developer Experience: Spec Kit vs OpenSpec

## Day-to-Day Workflow Comparison

| Task | Spec Kit | OpenSpec |
|------|----------|----------|
| **Start a feature** | Follow rigid 6-command sequence | Create proposal, iterate freely |
| **Change requirements mid-work** | Restart specification cycle | Update proposal, continue |
| **Add to existing system** | Specify entire system context | Delta spec (changes only) |
| **Review audit trail** | Implicit in conversation | Explicit in `changes/` folder |
| **Iterate on design** | Regenerate all artifacts | Incremental updates only |

**The Reality Check:**
```
┌─────────────────────────────────────────────────────────────────┐
│  "Spec Kit is tedious for iteration - each cycle costs tokens   │
│   because you're regenerating, not iterating."                  │
│                                                                 │
│  OpenSpec: Fluid commands that match how engineers actually     │
│  think and work. Specs evolve during building, not before.      │
└─────────────────────────────────────────────────────────────────┘
```


---




<!-- slide 11 -->

# 💰 Token Efficiency: Delta vs Regenerative

## Why OpenSpec Wins for Brownfield

| Iteration | Spec Kit (Regenerative) | OpenSpec (Delta) |
|-----------|------------------------|------------------|
| 1 | 10,000 tokens | 10,000 tokens |
| 2 | 10,000 tokens | 2,000 tokens |
| 3 | 10,000 tokens | 2,000 tokens |
| 4 | 10,000 tokens | 2,000 tokens |
| 5 | 10,000 tokens | 2,000 tokens |
| **Total** | **50,000 tokens** | **18,000 tokens** |
| **Savings** | Baseline | **64% reduction** |

**Key Insight:** Most AA work is brownfield. OpenSpec's delta model compounds savings over time.


---




<!-- slide 12 -->

# ⚠️ The Waterfall Parallel (Hangar Recommendation)

## A Warning from History

```
┌─────────────────────────────────────────────────────────────────┐
│  WATERFALL (1970)                  SPEC KIT (2024)              │
│  ---------------                   --------------               │
│  Designed for: 0 to 1              Designed for: 0 to 1         │
│  Royce warned: "risky, inviting    We observe: tedious for      │
│                 failure" for        brownfield, token-heavy     │
│                 large projects                                  │
│                                                                 │
│  What happened: DoD adopted it     Risk: Enterprise adopts it   │
│  for ALL projects (1985)           for ALL projects             │
│                                                                 │
│  Result: Reversed course (1994)    Let's not repeat history     │
└─────────────────────────────────────────────────────────────────┘
```

**Lesson:** Tools designed for 0 to 1 should not be forced onto 1 to n work.


---




<!-- slide 13 -->

# 📁 AA Engineering Laws Repo Structure

## How It's Organized

```
aa-engineering-laws/
├── AGENTS.md                 # AI entry point
├── laws/
│   ├── index.yaml            # Law catalog (loads first)
│   └── engineering/
│       ├── testing.md        # ENG-4.x Testing laws
│       ├── ai-collaboration.md # ENG-9.x AI pairing laws
│       ├── quality.md        # ENG-3.x Code quality laws
│       └── ...               # architecture, security, devops
├── adoptions/
│   ├── index.yaml            # Adoption catalog
│   ├── java-spring/
│   │   ├── manifest.yaml     # Adoption metadata
│   │   ├── guidance.md       # Java/Spring specific guidance
│   │   └── examples/
│   │       ├── ENG-4.1-atomic-tdd.md
│   │       ├── ENG-4.2-test-pyramid.md
│   │       └── ...           # Law-specific examples
│   ├── nodejs-typescript/
│   ├── python-fastapi/
│   └── ...                   # kafka, kubernetes, postgresql
├── practice-guides/
│   ├── atomic-tdd/
│   ├── test-pyramid/
│   └── token-optimization/
└── tools/
    └── constitution-lint/    # Compliance checker
```

**Key:** Index files act as routers. AI loads catalog first, then only relevant files.


---




<!-- slide 14 -->

# 🤝 Community Contributions

## How You Can Help Enrich the Constitution

**The Ask:** Update `aa-engineering-laws/adoptions/java-spring/guidance.md` with real AA examples

### Example: Generic vs AA-Specific

**Current Generic Example (ENG-4.2 Test Pyramid):**
```java
// Compliant: Behavior-focused test name
@Test
void shouldReturnEmptyList_whenNoUsersExist() { }

// Violation: Implementation-focused test name  
@Test
void testGetUsers() { }
```

**Enriched AA Cargo Example:**
```java
// Compliant: From AA Cargo multi-api (AI-written)
@Test
void validate_palApplicationInfo_maps_correctly_from_domain_to_response() { }

// Violation: Legacy pattern we replaced
@Test
void testPalApplicationService() { }
```

### Meta Prompt for Finding Examples

```
Review this codebase for examples that demonstrate compliance or 
violation of aa-engineering-laws. For each example found:
1. Identify the relevant law (ENG-x.x)
2. Extract the code snippet
3. Explain why it's compliant or a violation
4. Format it for inclusion in adoptions/java-spring/guidance.md
```

**Why This Matters:** Your examples train future AI context and improve our RAG pipeline.
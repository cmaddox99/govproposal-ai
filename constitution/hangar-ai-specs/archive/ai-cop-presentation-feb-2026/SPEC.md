# OpenSpec Proposal: Constitutional SDD Brief for AI Community of Practice

**ID:** ai-cop-presentation-feb-2026  
**Status:** Draft  
**Authors:** Adeel Ali, Nag  
**Created:** 2026-02-05  
**Target Event:** AI COP (Community of Practice) at American Airlines

---

## Executive Summary

This proposal outlines the creation of a presentation slide deck for the AI Community of Practice (COP) at American Airlines. The presentation will showcase the AA Engineering Laws framework, demonstrate results from the Wave 2 AA Cargo proof of concept, explain token optimization architecture, compare OpenSpec vs Spec Kit methodologies, and invite community contributions.

---

## Presentation Objectives

1. **Demonstrate Value** - Show concrete results from Wave 2 AA Cargo experiment
2. **Explain the Framework** - AA Engineering Laws as guardrails for 100% AI-assisted coding
3. **Highlight Key Laws** - Essential engineering laws that enable the agentic loop
4. **Share Token Optimization** - RAG-ready hierarchical architecture with live demo
5. **Compare Approaches** - OpenSpec vs Spec Kit research and analysis
6. **Introduce AA Engineering Laws Repo** - Structure and how to navigate
7. **Invite Community Contributions** - Enriching adoptions with AA code examples

---

## Slide Deck Structure

### Section 1: The Wave 2 Experiment (3 slides)

#### Slide 1.1: Title Slide
- **Title:** "Constitutional SDD: Engineering Laws for AI Agents"
- **Subtitle:** "How AI Agents Build Software Under Governance at AA"
- **Presenters:** Adeel Ali & Nag
- **Event:** AI COP, February 2026

#### Slide 1.2: Wave 2 AA Cargo Results
**Content:**
```
BEFORE (Baseline)                  AFTER (5-Hour Session)
-----------------                  ----------------------
- 30% code coverage                - 91% code coverage
- Inverted test pyramid            - Healthy test pyramid
- 2 unit tests                     - 63+ characterization tests
- 85% integration tests            - 70%+ unit tests
- No safety net for refactoring    - Full refactoring enabled
```
- 5 hours of AI-assisted development
- Junior engineer + AI mentor = senior-level output

#### Slide 1.3: How We Achieved It
**Content:**
- Adopted the **Constitutional Framework** (OpenSpec + CONSTITUTION.md)
- Built explicit **engineering laws** as AI guardrails
- Applied **Atomic TDD** (8-step cycle)
- AI agent followed laws strictly, not just suggestions
- Result: **100% AI-assisted coding** with consistent quality

---

### Section 2: What is Constitutional AI for Engineering? (1 slide)

#### Slide 2.1: Traditional vs Constitutional AI
**Content:**
```
TRADITIONAL AI CODING              CONSTITUTIONAL AI
---------------------              -----------------
- AI generates code                - AI follows explicit laws
- Human fixes batch errors         - Human guides direction
- Inconsistent quality             - Production-ready output
- "It depends on the dev"          - "It follows the Constitution"
- ~20% AI-assisted                 - 100% AI-assisted

AI as: SUGGESTION ENGINE           AI as: GOVERNED AGENT
```
**Key Insight:** Without explicit standards, AI produces prototype-quality code. With a Constitution, AI produces consistent, production-quality output.

---

### Section 3: Key Engineering Laws (1 slide)

#### Slide 3.1: Laws That Enable the Agentic Loop
**Content:**
| Law ID | Law Name | Why It Matters |
|--------|----------|----------------|
| **ENG-x.x** | Atomic TDD Law | Test-first, ONE test at a time |
| **ENG-x.x** | Test Pyramid Law | x% unit, y% integration, z% E2E |
| **ENG-x.x** | AI-Engineer Pairing Law | AI as teaching partner, not just generator |
| **ENG-x.x** | Complexity Limits | Cyclomatic complexity limits |
| **ENG-x.x** | Audit Trail Law | All changes documented and traceable |

**Key Point:** Non-negotiable laws give AI **authority** and eliminate "it depends"

```
WITHOUT LAWS                       WITH LAWS
------------                       ---------
AI: "Should I write tests?"        AI: "ENG-x.x requires
Human: "It depends..."                  TDD. Writing test
                                        first."
Result: Inconsistent               Result: Predictable quality
```

---

### Section 4: Token Optimization (2 slides, consolidated)

#### Slide 4.1: The Problem and Solution
**Content:**
```
THE PROBLEM:
Full Constitution         ~549,250 tokens
AI context limit          ~128,000 tokens
-------------------------------------------
OVERFLOW                  421,250 tokens (4.3x over!)

THE SOLUTION: RAG-Ready Hierarchical Architecture

LEVEL 1: CATALOG LOOKUP (~6K tokens)
  - Index files: laws/, skills/, workflows/, adoptions/

LEVEL 2: SELECTIVE SKILL RETRIEVAL (~4-8K tokens)
  - Load ONLY the relevant skill (e.g., 13-observability.md)

LEVEL 3: ADOPTION SPECIALIZATION (~2-5K tokens)
  - Load ONLY matching tech (java-spring/) + industry (faa/)
```

**Results:**
| Scenario | Before | After | Savings |
|----------|--------|-------|---------|
| "Add monitoring to cargo-api" | 549,250 | ~12,700 | **97.7%** |

#### Slide 4.2: Live Demo - Token Optimization in Action
**Content:**
Show the audience the practice guide prompt for Java/Spring:

**Scenario Prompt (from practice guide):**
```
I'm working on a Java Spring Boot project and need help with:
1. Writing unit tests for a service

Based on the token-optimized structure, which files should you load?
Explain why each file is needed and estimate the token savings.
```

**Expected Loading Strategy:**
```yaml
Required:
  - laws/index.yaml              # 80 lines - Find relevant laws
  - laws/engineering/testing.md  # 202 lines - Testing laws (ENG-4.*)

Conditional (if needed):
  - adoptions/java-spring/manifest.yaml  # 86 lines - Java-specific mappings
  - adoptions/java-spring/examples/ENG-4.1-atomic-tdd.md  # 78 lines

Total: 282-446 lines (vs 5,000+ for full load)
```

**Live Demo:** Run this prompt and show selective loading in action.

---

### Section 5: What's New in AA Engineering Laws (1 slide)

#### Slide 5.1: Recent Updates to AA Engineering Laws Repository
**Content:**
| Update | Description |
|--------|-------------|
| **Token Optimization** | Decomposed monolithic laws into indexed files |
| **RAG-Ready Architecture** | Hierarchical segmentation for 97% token reduction |
| **Constitution Lint Tool** | Automated compliance checking |
| **Technology Adoptions** | Java/Spring, Python, .NET, React, Node.js patterns |
| **Industry Adoptions** | Aviation/FAA compliance requirements |
| **Practice Guides** | Hands-on exercises: Atomic TDD, Test Pyramid, Token Optimization |

---

### Section 6: OpenSpec vs Spec Kit Analysis (3 slides)

#### Slide 6.1: The Core Difference
**Content:**
| Aspect | OpenSpec | Spec Kit |
|--------|----------|----------|
| **Primary Use Case** | 1-to-n Brownfield (evolution) | 0-to-1 Greenfield (creation) |
| **Workflow** | Flexible, customizable | Fixed 6-command sequence |
| **Change Tracking** | Explicit deltas in `changes/` | Less structured |
| **Constitutional Support** | Native integration | Requires workarounds |
| **Legacy Support** | Current vs proposed separation | Unified structure |

**Spec Kit Commands (Rigid):**
```
/speckit.constitution - /speckit.specify - /speckit.plan - /speckit.tasks - /speckit.implement
```

**OpenSpec Commands (Flexible):**
```
/opsx:explore <-> /opsx:new - /opsx:continue <-> /opsx:apply <-> /opsx:verify - /opsx:sync
```

#### Slide 6.2: The Waterfall Parallel
**Historical Context:**
> Winston Royce (1970) presented the waterfall model but noted it had **"major flaws"** and was **"risky and inviting failure"** because testing only happened at the end. The rigid sequential approach was meant for **0-to-1 development**, not iteration.

**The Pattern:**
| Stage | Waterfall | Spec Kit (Risk) |
|-------|-----------|-----------------|
| **Design Intent** | Initial iteration only | Greenfield projects |
| **Adoption Scope** | Applied to all projects | Risk of broad adoption |
| **Problem** | Used for evolution work | Same risk |
| **Consequence** | Costly rework | Token inefficiency, rigidity |

**Warning:** Tools designed for 0-to-1, when applied to n-to-n+1 work, create problems.

#### Slide 6.3: Token Efficiency - Delta vs Regenerative
**Content:**
```
REGENERATIVE MODEL (Spec Kit pattern):
Iteration 1: Generate full spec      - ~10,000 tokens
Iteration 2: Regenerate full spec    - ~10,000 tokens
Iteration 3: Regenerate full spec    - ~10,000 tokens
Iteration 4: Regenerate full spec    - ~10,000 tokens
Iteration 5: Regenerate full spec    - ~10,000 tokens
----------------------------------------------------------
Total for 5 iterations:              - ~50,000 tokens

DELTA MODEL (OpenSpec pattern):
Iteration 1: Generate initial spec   - ~10,000 tokens
Iteration 2: Update delta only       - ~2,000 tokens
Iteration 3: Update delta only       - ~2,000 tokens
Iteration 4: Update delta only       - ~2,000 tokens
Iteration 5: Update delta only       - ~2,000 tokens
----------------------------------------------------------
Total for 5 iterations:              - ~18,000 tokens

TOKEN SAVINGS: 64% over 5 iterations
```
For AA's 90% brownfield work, this adds up to **significant cost savings**.

---

### Section 7: AA Engineering Laws Repository Structure (1 slide)

#### Slide 7.1: Navigating the Repository
**Content:**
```
aa-engineering-laws/
|
+-- laws/                    # The Constitution
|   +-- index.yaml           # Law registry for discovery
|   +-- engineering/         # Individual law articles
|       +-- testing.md       # ENG-4.*: Testing laws
|       +-- quality.md       # ENG-3.*: Quality laws
|       +-- security.md      # ENG-5.*: Security laws
|
+-- adoptions/               # Technology & Industry specific
|   +-- java-spring/         # Java Spring Boot patterns
|   +-- python-fastapi/      # Python FastAPI patterns
|   +-- aviation-faa/        # FAA compliance requirements
|
+-- practice-guides/         # Hands-on exercises
|   +-- atomic-tdd/          # TDD practice
|   +-- token-optimization/  # This presentation's demo!
|
+-- tools/                   # Automation
    +-- constitution-lint/   # Compliance checking
```

**How to Use:**
1. **Start with `laws/index.yaml`** for discovery
2. **Load only relevant law articles** for your task
3. **Add adoption patterns** for your tech stack
4. **Practice with guides** to build muscle memory

---

### Section 8: Community Contributions (1 slide - CLOSING)

#### Slide 8.1: Help Enrich the Adoptions
**Content:**
**The Ask:** Replace generic examples with real AA code examples

**Why This Matters:**
- Generic examples teach concepts but lack context
- AA-specific examples show "how we do it here"
- Enriched adoptions improve our future RAG pipeline
- Better examples = better AI suggestions for everyone

**Examples from AA Cargo (what we need more of):**

| Generic Example | AA Cargo Example |
|-----------------|------------------|
| `UserService.findById()` | `BookingService.findBookingByAwb()` |
| `@Test void testSave()` | `@Test void shouldCreateBookingWithValidAwbFormat()` |
| `assertEquals(expected, actual)` | `assertThat(booking.getStatus()).isEqualTo(BookingStatus.CONFIRMED)` |

**How to Contribute:**
1. Pick an adoption (e.g., `adoptions/java-spring/`)
2. Find a law example (e.g., `examples/ENG-4.1-atomic-tdd.md`)
3. Replace generic code with real AA patterns
4. Submit PR to `aa-engineering-laws` repo

**Contact:** Slack #hangar-ai-constitution | Repo: aa-engineering-laws

---

## Research Tasks

### R1: Waterfall History Research
- [x] Verify Royce (1970) paper criticism of waterfall
- [x] Confirm waterfall was designed for 0-to-1, not iteration
- [x] Document DoD adoption (1985) and later retreat (MIL-STD-498, 1994)

**Key Finding from Wikipedia:**
> "Winston W. Royce...commented that [waterfall] had major flaws stemming from how testing only happened at the end of the process, which he described as being 'risky and [inviting] failure'."
> "The United States Department of Defense...now have a stated preference against waterfall-type methodologies, starting with MIL-STD-498 released in 1994."

### R2: Spec Kit Research
- [ ] Find current Spec Kit documentation and capabilities
- [ ] Identify any announced enhancements for iterative workflows
- [ ] Compare community adoption (stars, forks, enterprise usage)

**Note:** Spec Kit documentation URLs returning 404 - may have been renamed or reorganized. Need to verify current status.

### R3: OpenSpec Market Adoption
- [ ] Research Constitutional AI adoption in other enterprises
- [ ] Document OpenSpec usage beyond AA
- [ ] Identify competitors or similar frameworks

---

## Acceptance Criteria

1. [ ] All slides have clear, concise content
2. [ ] Wave 2 results are accurately represented
3. [ ] Token optimization data is current and verified
4. [ ] OpenSpec vs Spec Kit comparison is fair and evidence-based
5. [ ] Waterfall parallel is historically accurate
6. [ ] AA Engineering Laws repo structure is accurately shown
7. [ ] Community contribution examples are from real AA Cargo code
8. [ ] Slides are ready for Marp/presentation tool conversion

---

## Technical Notes

### Slide Format
- Use Marp markdown format for slide generation
- ASCII diagrams for architecture visuals
- Tables for data comparison
- Code blocks for prompt examples

### Terminology
- Use "adoptions" instead of "avatars" throughout
- Use "RAG-Ready Hierarchical Architecture" for token optimization
- Use regular dashes instead of em-dashes

### Source Materials
| Material | Location |
|----------|----------|
| Wave 2 Results | `docs/slides/engineering-laws-committee-kickoff.md` |
| Token Optimization Practice Guide | `practice-guides/token-optimization/README.md` |
| AA Cargo Case Study | `aacargo-multi-api/openspec/` |
| Spec Kit Comparison | `docs/slides/architect_guild.md` |

---

## Out of Scope

- Anthropic research background
- Three constitutions (Engineering/Product/Business) - focus on Engineering only
- Agentic loop architecture diagram
- Atomic TDD 8-step cycle diagram
- Next steps slide
- Questions slide
- Detailed security vulnerability analysis

---

## Risk & Mitigation

| Risk | Mitigation |
|------|------------|
| Spec Kit info outdated | Flag as "needs verification" in slides |
| Live demo fails | Have screenshot backup |
| Time constraints | Prioritize Sections 1-4 and 8, defer 5-7 if needed |

---

## Implementation Plan

```
Phase 1: SPEC Review (Current)
- Review updated SPEC with changes
- Confirm slide structure
- Verify practice guide prompt

Phase 2: Slide Implementation (~30 min)
- Create markdown slide file
- Follow existing slide format
- Include all content from SPEC

Phase 3: Review & Finalize (~15 min)
- Review for accuracy
- Test live demo prompt
- Final adjustments
```

---

## Slide Count Summary

| Section | Slides |
|---------|--------|
| Wave 2 Experiment | 3 |
| Constitutional AI for Engineering | 1 |
| Key Engineering Laws | 1 |
| Token Optimization | 2 |
| What's New in AA Engineering Laws | 1 |
| OpenSpec vs Spec Kit | 3 |
| AA Engineering Laws Repo Structure | 1 |
| Community Contributions (Closing) | 1 |
| **Total** | **13 slides** |

---

## Changes from Original Proposal

1. Title changed to "Constitutional SDD Brief for AI Community of Practice"
2. Removed all em-dashes, replaced with regular dashes
3. Removed Anthropic research background
4. Removed Three Constitutions slide (Engineering/Product/Business)
5. Removed Agentic Loop Architecture slide
6. Replaced numeric law IDs with x.x placeholders
7. Removed Atomic TDD 8-step cycle slide
8. Changed "avatar" to "adoptions" throughout
9. Replaced "What's New in Constitution" with "What's New in AA Engineering Laws"
10. Removed Next Steps slide
11. Removed Questions slide
12. Added AA Engineering Laws Repository Structure slide
13. Consolidated Token Optimization to 2 slides with live demo prompt
14. Added Community Contributions slide as closing (enriching adoptions with AA examples)

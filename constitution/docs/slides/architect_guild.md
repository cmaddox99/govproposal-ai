# AACargo Multi-API Modernization: A Constitutional Approach

**Date:** January 26, 2026  
**Presenters:** Adeel Ali & Nag Pullimamidi

---

## The Experiment

### Our 5-Hour Modernization Experiment

**Partnership:** The Hangar + AA Cargo Engineering

**Scope:** PAL Application Test Suite Modernization

**Approach:** Spec-Driven Development with Constitutional Governance

**Results:**
- ✅ 40% → 91% test coverage
- ✅ 0 → 63 characterization tests
- ✅ 5 hours total (5 mob sessions × 1 hour)
- ✅ Test pyramid fixed
- ✅ 6x faster test execution (3min → 30s)

**What This Proves:** Constitutional AI-driven SDLC can systematically modernize legacy systems

---

## The Paradigm Shift (Part 1)

### Traditional AI-Assisted Coding vs. AI-Driven SDLC

**The Old Way ❌**

| Aspect | Reality |
|--------|---------|
| **Workflow** | Engineer prompts → AI generates code → Copy/paste → Hope it works → It doesn't |
| **Quality** | Every increment risks wasting the entire batch |
| **Debugging** | Humans must debug and fix AI-created errors |

**The Hidden Costs:**
- 🔴 AI loses context between sessions
- 🔴 Prompts lack clear intent
- 🔴 "AI debt" accumulates (misunderstood requirements, shortcuts)
- 🔴 No systematic governance
- 🔴 Unpredictable quality

---

## The Paradigm Shift (Part 2)

### Our Constitutional AI-Driven SDLC ✅

| Aspect | Our Approach |
|--------|--------------|
| **Workflow** | AI trained to follow structured SDLC (OpenSpec) → Constitutional governance → Humans & AI plan collaboratively |
| **Quality** | Atomic TDD agents: strict red-green-refactor-verify-commit-push cycles |
| **Debugging** | 100% AI-assisted with built-in verification at each step |

**The Benefits:**
- 🟢 AI teaches humans the WHY behind decisions
- 🟢 Humans develop judgment → Better prompts over time
- 🟢 Constitutional constraints prevent AI debt
- 🟢 Complete audit trail
- 🟢 Systematic, repeatable quality

---

## The Paradigm Shift (Part 3)

### Key Innovation: From Hope to Verification

**Traditional:** Hope AI code works 🤞

**Our Approach:** Systematically verify it works ✅

**How:**
1. Constitution defines standards
2. AI follows structured SDLC
3. Atomic TDD cycles catch issues immediately
4. Each increment verified before proceeding
5. Bi-directional learning (AI ↔ Human)

**Result:** Shift from unpredictable quality to systematic excellence

---

## The Problem We Needed to Solve

### Before: PAL Application Reality

```
┌─────────────────────────────────────────┐
│ PAL Application (Partner Airlines)      │
├─────────────────────────────────────────┤
│ • Legacy SOAP-based service             │
│ • Years of technical debt                │
│ • Test pyramid INVERTED ❌              │
│   (more integration than unit tests)    │
│ • 640 lines, only 40% covered           │
│ • Business logic trapped in services    │
│ • Inconsistent testing practices        │
└─────────────────────────────────────────┘
```

**Challenge:** How to modernize systematically while maintaining production stability?

**Traditional approaches fail:** Vague requirements → Unpredictable AI → Inconsistent quality

---

## The Solution - OpenSpec + Constitutional Governance

### Two-Part Framework

**Part 1: OpenSpec** - Spec-driven development for AI-assisted coding
- "Executable documentation"
- Humans & AI agree on requirements BEFORE coding
- Purpose-built for brownfield (1→n evolution)

**Part 2: Constitutional Governance** - Engineering law enforcement
- CONSTITUTION.md defines non-negotiable standards
- AGENTS.md instructs AI to enforce them
- Automated verification (VERIFY step)

**Together:** Systematic quality + Complete audit trail + Replicable process

---

## What is OpenSpec?

### Spec-Driven Development Framework

**Traditional AI Coding:**
```
Vague Prompt → AI Generates → Hope it's correct 🤞
```

**OpenSpec Approach:**
```
Spec First → Review Spec (Human + AI) → Implement (Verified) ✅
```

**Why OpenSpec for AA:**
- ✅ Built for brownfield (legacy modernization)
- ✅ 90% of AA work is 1→n evolution
- ✅ Explicit change tracking
- ✅ Audit trail built-in
- ✅ Flexible workflows

**Alternative:** GitHub SpecKit
- Better for 0→1 greenfield
- Prescriptive workflow
- Not ideal for legacy systems

---

## OpenSpec Brownfield Architecture

### Directory Structure

```
aacargo-multi-api/
├── openspec/
│   ├── CONSTITUTION.md           ← Engineering Laws & Standards
│   ├── AGENTS.md                 ← AI Instructions
│   ├── project.md                ← Project Context
│   │
│   ├── specs/                    ← CURRENT SYSTEM TRUTH
│   │   └── pal-service/
│   │       └── spec.md           (Current state, stays clean)
│   │
│   └── changes/                  ← PROPOSED UPDATES
│       └── improve-pal-test-pyramid/
│           ├── proposal.md       ← What & Why
│           ├── tasks.md          ← Implementation checklist
│           ├── design.md         ← Technical decisions
│           └── specs/            ← Spec deltas (ONLY changes)
│               └── pal-service/
│                   └── spec.md   (Diff, not full rewrite)
```

**Key Insight:** Change isolation = Clear audit trail + Safe experimentation

---

## File-by-File Explanation

### OpenSpec Files Explained

| File | Purpose | When Used |
|------|---------|-----------|
| **CONSTITUTION.md** | Engineering laws, quality standards, test requirements | AI reads before every action |
| **AGENTS.md** | AI instructions for SDLC workflow stages | AI reads to understand process |
| **project.md** | System context, architecture, business domain | AI reads for project understanding |
| **proposal.md** | Change justification, scope, approach | Created for each change |
| **tasks.md** | Implementation checklist, progress tracking | Updated after each atomic commit |
| **design.md** | Technical decisions, patterns, examples | Created when architecture changes |
| **specs/\*.md** | Current system specification | Represents production truth |
| **changes/\*/specs/\*.md** | Specification deltas (changes only) | Shows proposed modifications |

**Workflow:** Proposal → Tasks → Implementation → Merge deltas to specs/ → Archive

---

## Why OpenSpec vs SpecKit? (Part 1)

### Direct Comparison

| Criterion | OpenSpec | GitHub SpecKit | Winner for AA |
|-----------|----------|----------------|---------------|
| **Primary Use Case** | 1→n Brownfield | 0→1 Greenfield | **OpenSpec** ✅ |
| **Change Tracking** | Explicit deltas in `changes/` | Less structured diffs | **OpenSpec** ✅ |
| **Workflow Flexibility** | Customizable (AGENTS.md) | Fixed 6-command flow | **OpenSpec** ✅ |
| **Constitutional Support** | Fully compatible | Requires workarounds | **OpenSpec** ✅ |
| **Legacy System Support** | Current vs proposed separation | Unified structure | **OpenSpec** ✅ |
| **Community Size** | 18.8k stars | 64.2k stars | SpecKit |
| **Enterprise Customization** | High (proven) | Lower (prescriptive) | **OpenSpec** ✅ |

**OpenSpec Wins:** 6 out of 7 criteria for AA's needs

---

## Why OpenSpec vs SpecKit? (Part 2)

### SpecKit's Stated Use Case

**From their documentation:**
> "0-to-1 Development ('Greenfield')" - Generate from scratch

**SpecKit Commands:**
```bash
/speckit.constitution  # Create principles
/speckit.specify       # Define requirements
/speckit.plan          # Tech stack
/speckit.tasks         # Generate tasks
/speckit.implement     # Build from scratch
```
→ Rigid, prescriptive, optimized for NEW projects

**OpenSpec Workflow:**
```
1. Draft change proposal (proposal.md)
2. Define spec deltas (only changes)
3. Create tasks aligned with constitution
4. Implement incrementally
5. Archive → merge deltas to specs/
```
→ Flexible, governance-friendly, built-in audit trail

---

## Why OpenSpec vs SpecKit? (Part 3)

### The Verdict: OpenSpec Matches AA Reality

**AA Engineering Context:**
- 🏢 90% brownfield work (modernizing legacy)
- 📋 Compliance requirements (audit trails needed)
- 👥 Large teams (consistent governance required)
- 🔄 Continuous evolution (decades, not months)
- 🎯 Custom workflows (different team processes)

**OpenSpec Architecture Fits:**
- ✅ Incremental modernization
- ✅ Explicit spec deltas = clear documentation
- ✅ Customizable workflows
- ✅ Constitutional layer
- ✅ Change isolation = safer updates

**Our PAL Experiment Proves This** ✅

---

## Constitutional Governance - Article IV Laws

### The Three Critical Testing Laws

**Section 4.1: 8-Step Atomic TDD Law**
```
RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT
```
- Must follow all 8 steps for every test
- VERIFY step includes ALL compliance (PMD, Jacoco, Formatter + ALL constitutional laws)
- No commits without complete verification ✅

**Section 4.5: Test Abstraction Level Law**
- Tests at correct layer (domain vs service vs controller)
- Business logic tested in domain entities
- Service tests focus on orchestration only

**Section 4.9: Integration Test Decomposition Law**
- Max 200 lines per test class
- Max 8 tests per class
- Enables parallel execution

---

## The Atomic TDD Law - 8-Step Cycle

### RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT

```
Step 1: RED       Write ONE failing test
Step 2: GREEN     Write simplest code to pass
Step 3: REFACTOR  Clean up code & test
Step 4: VERIFY    Complete constitutional compliance ← CRITICAL
Step 5: DOCUMENT  Update tasks.md, proposal.md progress
Step 6: COMMIT    Atomic commit with message
Step 7: PUSH      Push to origin
Step 8: REPEAT    Next test cycle
```

**VERIFY Step - ALL Compliance in One Pass:**
```bash
./run-with-java21.sh mvn test jacoco:report  # ≥90% coverage
mvn pmd:check                                 # Complexity ≤10
mvn pmd:cpd-check                             # <3% duplication
mvn formatter:validate                        # Google Style
# + Architecture, Security, Domain, Project Context laws
```

**Key:** AI can't bypass automated checks. If ANY check fails, commit is blocked.

---

## The Agentic Loop We Developed

### AI Agent Workflow (8-Step TDD Cycle)

```
┌───────────────────────────────────────────┐
│ ATOMIC TDD AGENT                            │
├───────────────────────────────────────────┤
│                                             │
│  1. RED: Write ONE failing test             │
│     ↓                                       │
│  2. GREEN: Simplest code to pass            │
│     ↓                                       │
│  3. REFACTOR: Clean code & test             │
│     ↓                                       │
│  4. VERIFY: Complete constitutional         │
│     │        compliance (ALL checks)        │
│     ├─→ Coverage (Jacoco ≥90%)              │
│     ├─→ Quality (PMD, CPD, Formatter)       │
│     ├─→ Architecture boundaries             │
│     ├─→ Security & domain rules             │
│     └─→ ✅ ALL PASS → Continue               │
│         ❌ ANY FAIL → Return to REFACTOR    │
│     ↓                                       │
│  5. DOCUMENT: Update tasks & proposal       │
│     ↓                                       │
│  6. COMMIT: Atomic git commit               │
│     ↓                                       │
│  7. PUSH: Share with team                   │
│     ↓                                       │
│  8. REPEAT for next test                    │
│                                             │
└───────────────────────────────────────────┘
```

**Loop continues until all tests in tasks.md are ✅**

---

## The VERIFY Step Explained

### Critical: AI Uses YOUR Tools, Not Made-Up Standards

**The Confusion We Hear:**
> "How does AI know our standards?"
> "Is AI making up rules?"

**The Reality:**
```
AI DOESN'T INVENT STANDARDS. IT ENFORCES YOURS.

CONSTITUTION.md tells AI: "Run these commands"
                           ↓
AI executes YOUR existing tools:
  • Jacoco (coverage)    - target/site/jacoco/
  • PMD (quality)        - code-quality/java.xml
  • Formatter (style)    - code-quality/eclipse-java-google-style-v23.xml
  • SonarQube (future)   - sonar-project.properties
                           ↓
Tools check EXISTING configs
                           ↓
Results verified before commit
                           ↓
Git history shows compliance
                           ↓
COMPLETE AUDIT TRAIL ✅
```

**Add SonarQube? AI automatically uses it.**
**Add Checkstyle? AI automatically uses it.**

---

## VERIFY Step in Practice

### Example: AI Writing Test #11

**1. RED** - AI writes failing test
```java
@Test
void createPalApplication_allOptionalFields_success() {
    // Test implementation
}
```

**2. GREEN** - AI implements code
```java
public Response createPalApplication(Request req) {
    // Simplest implementation to pass
}
```

**3. REFACTOR** - AI cleans up
```java
// Extracts methods, improves naming
```

**4. VERIFY** - AI runs tools (THE CRITICAL STEP)
```bash
$ ./run-with-java21.sh mvn test jacoco:report
[INFO] Coverage: 91% (582/640 lines) ✅

$ mvn pmd:check
[INFO] PMD processing completed ✅

$ mvn formatter:validate
[INFO] Code formatting compliant ✅
```

**5. COMMIT** - Atomic commit
```bash
$ git commit -m "test(pal): GREEN - Test #11 all optional fields"
```

**6. TASK UPDATE** - Progress tracking
```markdown
- [x] 1.2.23.1 Test #11: All optional fields ✅ PASSING
```

---

## Measurable Results - Slice 1 Complete

### Characterization Tests: 40% → 91% Coverage

**Achieved in 5 Hours (5 mob sessions × 1 hour):**

```
Coverage:        40% ──────────────────► 91% ✅
Tests Created:   0 ────────────────────► 63 ✅
Test Execution:  3 min ────────────────► 30s ✅ (6x faster)
Quality:         Unknown ──────────────► 100% passing ✅
Commits:         N/A ───────────────────► 63 atomic ✅
```

**Key Achievements:**
- ✅ 100% coverage of `extractApplication()` (69 lines)
- ✅ 100% coverage of `extractApplications()` (70 lines)
- ✅ Complete coverage of `submitPalAppl()` (208 lines, most complex)
- ✅ All tests use Given-When-Then documentation
- ✅ Test pyramid fixed (86% unit tests, 14% integration)

**Constitutional Compliance:** All laws enforced through 63 atomic TDD cycles

---

## Measurable Results - Test Pyramid Fixed

### Before vs After

**BEFORE (Broken ❌):**
```
       △
      / \ E2E: 0%
     /───\
    / Int \ 100% ❌ All tests at WRONG layer
   /───────\      (slow, brittle, blocks refactoring)
  /  Unit  \ 0% ❌ No fast unit tests
 /─────────\
```

**AFTER (Best Practice ✅):**
```
       △
      / \ E2E: 0%
     /───\
    / Int \ 14% ✅ Focused at controller layer
   /───────\
  /  Unit  \ 86% ✅ Fast tests at service layer
 /─────────\       (<30s execution, proper isolation)
```

**Impact:**
- 🚀 6x faster CI feedback
- 🎯 Tests at correct abstraction levels
- 🧹 Refactoring now safe and fast

---

## Next Phase - Roadmap

### Remaining Slices (3-4 Weeks Total)

**Slice 2:** Integration Tests (60% complete) - 2 days
- Controller layer with `@WebMvcTest`
- Decomposed by functional boundary
- Pattern established for future tests

**Slice 3:** E2E Tests - 1 week
- Full-stack with real database
- `@SpringBootTest` with WireMock

**Slice 4:** Resilience Tests - 3 days
- Timeouts, retries, circuit breakers
- Chaos engineering patterns

**Slice 5:** Continuous Refactoring - 1 week
- Extract business logic to domain entities
- Apply immutability, fix Law of Demeter
- **Enables Slice 7**

**Slice 6:** Teaching Documentation - 3 days
- Pattern guides, workflow documentation

**Slice 7:** Test Abstraction Migration - 1 week
- Move tests to correct layers
- Domain tests for business logic
- Service tests for orchestration only

---

## The Foundation First

### Critical Context: How We Got to 30% Baseline

**Before AI SDLC:**

Engineers mobbed in **the Hangar** to achieve **30% baseline coverage**

**Why This Was Critical:**
- 🧠 Engineers practiced constitutional laws **manually**
- 🎯 Developed mental models of TDD and quality patterns
- 💡 Learned the WHY behind atomic cycles
- ✅ Built judgment before AI collaboration

**Result:**
- Humans understood principles deeply
- Could effectively guide AI
- Knew what good looks like
- Prompts had clear intent from the start

**Then AI SDLC:**
- Scaled from 30% → 91% in 5 hours
- AI implemented with human strategic oversight
- Bi-directional learning accelerated

**Key Lesson:** Human foundation + AI acceleration = Systematic excellence

---

## The AI Teaching Law

### Section 1.6: AI-Engineer Pairing and Teaching Law

**GitHub Copilot SHALL act as a teaching partner, not just a code generator**

**The Learning Feedback Loop:**

```
1. AI follows constitution strictly    → No shortcuts, no exceptions
2. AI explains the WHY                 → Every decision references principles
3. Engineers observe and learn         → Watching builds mental models
4. Engineers develop judgment          → Like citizens with laws, internalize principles
5. Prompts become intentional          → Better understanding → precise requests
6. The pair becomes effective          → Junior + AI = Senior-level work
```

**Key Insight:** AI doesn't just generate code—it teaches the team WHY decisions are made, building judgment and prompt maturity over time.

---

## Documentation as a Teaching Tool

### Knowledge Artifacts Created

| Category | Documents | Lines | Purpose |
|----------|-----------|-------|---------|
| **Guides** | 4 | 2,570 | How-to for TDD, testing, contracts |
| **Presentations** | 4 | 2,100 | Stakeholder communication |
| **Metrics** | 2 | 865 | Baseline & progress tracking |
| **Archive** | 2 | 497 | Historical teaching moments |
| **Index** | 1 | 226 | Navigation & learning paths |
| **Total** | **13** | **6,300+** | Complete knowledge base |

**Documentation Types:**
- 📘 **Guides:** Atomic TDD, Characterization Testing, WireMock Contracts, Architecture
- 🎤 **Presentations:** Architect Guild, Executive Briefing (slides + facilitator notes)
- 📊 **Metrics:** Baseline measurements, Progress analysis
- 📚 **Archive:** Teaching log, Progress journal

**Impact:** Team has permanent reference for patterns, decisions, and reasoning

---

## Auditability & Compliance

### Complete Audit Trail

**1. Requirements Traceability:**
```
proposal.md (Why) → tasks.md (What) → Git commits (How) → Archive (Delivered)
```

**2. Quality Enforcement:**
```
CONSTITUTION.md (Standards) → AGENTS.md (Instructions) → VERIFY (Tools) → Blocked if fails
```

**3. Change Documentation:**
```
openspec/changes/improve-pal-test-pyramid/
├── proposal.md           ← Business justification
├── tasks.md              ← Implementation plan
├── design.md             ← Technical decisions
└── specs/                ← Specification deltas
```

**4. Git History as Evidence:**
```bash
$ git log --grep="verify" --oneline
364d97f verify(pal): Coverage 91%, PMD clean ✅
91fccbe verify(pal): Coverage 87%, all checks passed ✅
```

**For Compliance Audits:** Every commit shows VERIFY step output

---

## What We Learned

1. **8-Step TDD > Traditional Red-Green-Refactor**
   - VERIFY step consolidates ALL compliance checks
   - DOCUMENT keeps docs synchronized
   - PUSH enables CI/CD and team visibility
   - Clear audit trail

2. **Characterization Tests Through Public APIs**
   - More maintainable than testing private methods
   - Survives refactoring better
   - Natural documentation

3. **Constitutional Framework Scales**
   - Once defined, AI enforces consistently
   - New team members learn from CONSTITUTION.md
   - No institutional knowledge dependency

4. **OpenSpec's Change Isolation**
   - `changes/` folder keeps specs clean
   - Clear current vs proposed separation
   - Easy to abandon experiments

---

## Closing - See It In Action

### Video Demonstration

**What You'll See:**

The team applying this process to a NEW use case - fixing the test pyramid for another service.

**Watch for:**

1. **Creating an OpenSpec Proposal**
   - How we structure the change request
   - Defining scope and success criteria

2. **AI Following Constitutional Laws**
   - Real-time enforcement of engineering standards
   - AI referencing CONSTITUTION.md for decisions

3. **AI Avoiding What We Don't Want**
   - Respecting boundaries and constraints
   - Not taking shortcuts or skipping verification

4. **The Agentic Loop in Practice**
   - RED → GREEN → REFACTOR → VERIFY → DOCUMENT → COMMIT → PUSH → REPEAT
   - Each step visible and auditable

**🎬 [Play Video]**

---

## Q&A

### Questions?

**Thank you!**

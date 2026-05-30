# Agent Instructions for hangar-ai-constitution

This repository contains the American Airlines Hangar AI Constitution - a governance framework for AI-assisted software development at American Airlines.

## Repository Purpose

The hangar-ai-constitution defines:
- **Laws**: Mandatory rules for engineering (ENG-*), product (PRD-*), and business (BUS-*) domains
- **Skills**: Reusable capabilities agents can invoke
- **Avatars**: Technology, industry, and product-type specific implementations
- **Guides**: Detailed implementation guidance

<!-- BEGIN hangar-ai-constitution:mandatory-protocol v1.0.0 -->
## ⛔ MANDATORY AGENT PROTOCOL

**Every coding task in this repository MUST follow this exact 8-step cycle. No exceptions.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              MANDATORY AGENT PROTOCOL (Per ENG-4.1 — NON-NEGOTIABLE)        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Step 1 — IDENTIFY   Find the FIRST unchecked task in                      │
│                       hangar-ai-specs/changes/<change-id>/tasks.md          │
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
│                       ⛔ AT PHASE GATES: run Phase Gate Sub-Protocol below  │
│                       ↓                                                     │
│  Step 6 — UPDATE     Open hangar-ai-specs/changes/<change-id>/tasks.md     │
│           TASKS.MD   and mark task [x] with ✓ + commit hash                │
│                       Update progress summary counts                         │
│                       ↓                                                     │
│  Step 7 — COMMIT     git add -A && git commit -m "<conventional-msg>"      │
│                       Commit message MUST reference spec scenario ID        │
│                       ↓                                                     │
│  Step 8 — STOP AND   Report the completed test, commit hash, and next task  │
│           REPORT     Wait for human confirmation before starting next cycle │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```
<!-- END hangar-ai-constitution:mandatory-protocol -->

## ⛔ PHASE GATE SUB-PROTOCOL

**At every phase gate** (ENG-12.1, NON-NEGOTIABLE), VERIFY expands to this mandatory 6-step gate sequence before asking the human to approve phase advance.

> **What is a phase gate?** Phase gates occur at SDD lifecycle phase transitions (Capture → Define → Design → Plan → Build → Ship) and Product Discovery Stage exits (A–F). Individual TDD commits within a phase are **NOT** phase gates. When in doubt, check whether a `hangar-ai-specs/changes/` artifact marks a stage exit.

```
Phase Gate Sub-Protocol (ENG-12.1 + ENG-12.2 + ENG-13.1 + ENG-14.1 + PRD-2.6):

  0. COMMIT ARTIFACT    Commit the phase artifact to git BEFORE running
                        citation audit (ENG-12.2).
                        → Phase artifact must be git-tracked and clean.
                        → aa-citation-audit requires a tracked file.
                        ↓
  1. CITATION AUDIT     aa-citation-audit <phase-artifact.md>
                        → Must exit 0 (PASS). ≥1 FAIL blocks jury.
                        → WARN does NOT block jury; passes to jury brief
                          and activates J6 Citation Auditor (ENG-14.2).
                          Other J6 triggers: Stage E/F, ≥5 law IDs cited.
                        ↓
  2. JURY               PRD-2.6 multi-cognition jury on the phase artifact
                        → 5 jurors (J1–J5), each on a DISTINCT LLM model
                          (PRD-2.6 floor: ≥4; ENG-12.1/12.3 + aa-jury-gate
                          operationally enforce exactly 5)
                        → ENG-12.3 model roster: J1=claude-opus-4.6,
                          J2=claude-sonnet-4.6, J3=gpt-5.4, J4=gpt-5.2,
                          J5=gpt-5.4-mini; Synthesizer=claude-opus-4.5
                          (synthesizer is distinct from all jurors)
                        → Personas: domain sceptic, technical expert,
                          product/strategic lens, defense counsel,
                          + fifth juror per ENG-12.3
                        → Round 1: deliberate → apply corrections
                        → Round 2: confirm corrections resolved
                        → Judicial synthesizer produces synthesis artifact
                          with verdict: APPROVED (required by aa-jury-gate S11)
                        → Synthesis committed to hangar-ai-specs/changes/
                          BEFORE asking human to approve (ENG-12.2)
                        ↓
  3. JURY GATE          aa-jury-gate <synthesis.md>
                        → Must exit 0 (PASS).
                        → Any non-zero exit blocks advance:
                          exit 1 = FAIL, exit 2 = ERROR (both block).
                        → Validates: schema_version == 1,
                          verdict == APPROVED, juror_count == 5,
                          len(jurors) == 5, all distinct models,
                          rounds.r1_completed == true,
                          rounds.r2_completed == true,
                          R1/R2/Synthesis section headings in body,
                          synthesis git-tracked and clean.
                        → ON FAIL/ERROR: Do NOT advance. Report failure
                          to human. Await direction before re-running
                          from Step 1.
                        ↓
  4. RENDER             aa-artifact-render <synthesis.md>  (ENG-13.1)
                        → Renders synthesis as self-contained HTML with
                          law citation tooltips before human presentation.
                        → Must complete without error. Any render failure
                          blocks advance.
                        ↓
  5. HUMAN REVIEW       Present rendered synthesis to human for approval
                        → Human reads rendered synthesis BEFORE approving
                        → Agent CANNOT self-declare phase complete
```

**The sequence is strictly ordered.** Jury cannot be invoked before citation audit passes. Human cannot be asked to approve before aa-jury-gate passes and synthesis is rendered.

### Prohibited Phase Gate Anti-Patterns

| Prohibited Action | Law Violated |
|-------------------|-------------|
| Invoking jury before `aa-citation-audit` passes | ENG-14.1 |
| Running all jurors on the same LLM model | PRD-2.6 |
| Skipping Round 2 jury after corrections | PRD-2.6 |
| Advancing past a phase gate without `aa-jury-gate` exit 0 | ENG-12.1 |
| Agent self-certifying phase completion without jury synthesis | ENG-12.3 |
| Asking human to approve before jury synthesis is committed | ENG-12.2 |

### Installation

```bash
# Citation audit
pip install -e tools/citation-auditor

# Jury gate validator
pip install -e tools/aa-jury-gate

# Artifact renderer (ENG-13.1)
pip install -e tools/artifact-renderer
```

---

## ⛔ PROHIBITED ACTIONS

The following actions are **forbidden** and constitute a Constitutional violation:

| Prohibited Action | Law Violated |
|-------------------|-------------|
| Writing more than one test method per cycle | ENG-4.1 |
| Writing production code before a failing test exists | ENG-4.1 |
| Skipping the RED step (no failure proof shown) | ENG-4.1 |
| Skipping the REFACTOR step | ENG-4.1 |
| Skipping the VERIFY step (full suite + lint) | ENG-4.1, ENG-4.2 |
| Not updating `hangar-ai-specs/changes/<change-id>/tasks.md` after a cycle completes | ENG-6.7 |
| Committing without a spec scenario ID in the message | ENG-6.7 |
| Batching multiple tests into one commit | ENG-4.1 |
| Touching files outside the current task scope | ENG-2.3 |
| Proceeding to the next cycle without human confirmation | ENG-1.2 |
| Phase gate anti-patterns — see Phase Gate Sub-Protocol section above | ENG-12.1, PRD-2.6 |

## Self-Check Before Each Step

Before writing any code, answer these five questions aloud:

1. Have I identified the FIRST unchecked task in `hangar-ai-specs/changes/<change-id>/tasks.md`?
2. Am I writing exactly ONE test — not a test class, not a test file, ONE test?
3. Have I confirmed the test FAILS before writing production code?
4. Have I confirmed ALL tests PASS after the GREEN step?
5. Have I updated `hangar-ai-specs/changes/<change-id>/tasks.md` and committed with a scenario ID?

---

## Working with This Repository

### For AI Agents (GitHub Copilot)

1. **Follow the Mandatory Agent Protocol above** before writing any code
2. **Find the first unchecked task** in `hangar-ai-specs/changes/<change-id>/tasks.md` rather than deciding what to implement
3. **Read the laws** before making changes to understand constitutional requirements
4. **Follow Atomic TDD** (ENG-4.1) when writing any code - this is NON-NEGOTIABLE
5. **Use vertical slicing** (ENG-2.3) for feature implementation
6. **Maintain test pyramid** (ENG-4.2) with proper test distribution
7. **Cite laws** when making recommendations (e.g., "Per ENG-4.1...")

### RAG Retrieval Protocol

When answering ANY question about how to build, test, design, or implement:

1. **Route via skill index** — Read `agent-skills/skills-by-domain/*/index.yaml` to find the skill whose `triggers` or `laws` match the user's intent
2. **Load skill** — Read the matched skill `.md` file for the procedure. The `laws.implements[]` frontmatter tells you which laws apply
3. **Load avatar** — If the user's stack is known, read the matching `avatars/technology/*/guidance.md` for stack-specific patterns
4. **Cite laws** — Reference the law IDs from the skill frontmatter (do NOT separately search for law files)
5. **Stop** — Do NOT read `docs/guides/` unless the user explicitly asks for a guide or tutorial

For avatar enrichment or taxonomy requests, after step 2 load:

1. `agent-skills/skills-by-domain/discovery-research/30-taxonomy-governed-avatar-enrichment.md`
2. `docs/guides/avatars/product-taxonomy-governance.md`
3. `docs/guides/adoption/taxonomy-aligned-avatar-enrichment-workflow.md`

> **NEVER skip step 1.** The index files contain trigger phrases, law mappings, and skill names that route your response correctly. Going directly to `docs/guides/` returns verbose prose without constitutional authority.

### Key Directories

| Directory | Purpose |
|-----------|---------|
| `laws/` | Law indexes and domain YAML files |
| `avatars/` | Technology, industry, and product-type adoptions |
| `agent-skills/skills-by-domain/` | Skill definitions organized by domain with law mappings |
| `docs/guides/` | Implementation guides and best practices |

### Constitution Structure

```
hangar-ai-constitution/
├── avatars/                # Technology, industry, product-type adoptions
│   ├── index.yaml          # Avatar registry
│   ├── technology/         # Java, React, .NET, etc.
│   ├── industry/           # Aviation/FAA compliance
│   └── product-type/       # Booking, Cargo, Loyalty, etc.
├── docs/
│   ├── articles/           # Published articles
│   ├── guides/             # Implementation guides
│   └── slides/             # Presentation decks
├── laws/
│   ├── index.yaml          # Master law registry
│   ├── engineering/        # ENG-* laws
│   ├── product/            # PRD-* laws
│   └── business/           # BUS-* laws
├── agent-skills/
│   ├── base/AGENT.md       # Agent operating system
│   └── skills-by-domain/   # Skills organized by domain
│       ├── development-practices/
│       ├── discovery-research/
│       ├── ml-ai/
│       ├── platform-engineering/
│       └── product-planning/
├── hangar-ai-specs/        # Hangar SDD — Spec-Driven Development (ENG-11.1)
│   ├── changes/            # Active change proposals
│   ├── archive/            # Completed proposals
│   ├── evidence/           # Supporting evidence artifacts
│   ├── templates/          # Spec scaffolding templates
│   └── README.md           # SDD process guide
├── tests/                  # Language-conventional test directory — see note below
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
└── tools/
    ├── citation-auditor/   # aa-citation-audit (ENG-14.1)
    ├── aa-jury-gate/       # aa-jury-gate (ENG-12.1)
    ├── artifact-renderer/  # aa-artifact-render (ENG-13.1)
    └── constitution-lint/  # aa-constitution-lint (ENG-4.2)
```

> **⚠️ Language-aware test directory rule (ENG-4.2):** The `tests/` structure above is the Python/Node.js convention. **Always detect the existing test structure before creating any test directories.**
> - Java/Maven/Gradle → tests live in `src/test/java/` — **NEVER create `tests/` at project root if `src/test/` already exists**
> - Python → `tests/unit/` + `tests/integration/` at root (only if no `src/tests/` present)
> - Node/TypeScript → `__tests__/` or `test/` (only if not already present)
> - Ruby → `spec/`
> **Never create an empty test directory that duplicates an existing language-conventional test location.**

### Non-Negotiable Laws

These laws require executive approval to amend:

**Engineering:**
- ENG-4.1: Atomic TDD Law
- ENG-6.1: Security by Design Law
- ENG-6.4: Data Protection Law
- ENG-6.7: Audit Trail Law
- ENG-11.1: Hangar SDD Law (every project adopting the constitution MUST have `hangar-ai-specs/`)
- ENG-12.1: Agentic Phase Gate Law (jury-validated artifacts + human approval required at every phase gate)
- ENG-13.1: Artifact Rendering Standard (governance artifacts SHALL be rendered as HTML before human presentation)
- ENG-14.1: Law Citation Audit Gate Law (aa-citation-audit must pass before jury invocation)

**Product:**
- PRD-1.2: Problem-First Law
- PRD-2.6: Multi-Cognition Phase Gate Jury Law (≥4 jurors on distinct models; self-certification prohibited)
- PRD-5.1: MVP Law

**Business:**
- BUS-1.1: Priority Hierarchy (Legal First)
- BUS-7.1: Audit Trail Law
- BUS-9.3: Breach Notification Law

### Aviation-Specific Requirements

American Airlines software must comply with:
- **FAA**: FAR Part 117 (crew rest), DO-178C (safety-critical), DO-278A (ground-based Communication, Navigation, Surveillance, and Air Traffic Management (CNS/ATM) systems)
- **TSA**: Security directives, vetting requirements
- **DOT**: Consumer protection, fare transparency
- **IATA**: Dangerous goods regulations (DGR)

### Making Changes

1. Identify applicable laws from `laws/index.yaml`
2. Reference the appropriate avatar for your stack/domain
3. Write tests first (ENG-4.1)
4. Follow the SDD (Spec-Driven Development) lifecycle
5. Ensure all changes comply with constitutional laws

### AI Tool Configuration

This repository is configured for **GitHub Copilot** as the primary AI assistant.

When assisting with this repository:
- Enable constitution awareness
- Enforce law compliance
- Suggest appropriate skills
- Reference avatars for context-specific guidance

## Skill Discovery Protocol

When a user's prompt matches an intent pattern ("can you...", "help me...", "I need to..."), follow the [RAG Retrieval Protocol](#rag-retrieval-protocol) above. The detailed 4-level intent matching priority (exact trigger → semantic similarity → law-concept → category match) is documented in `agent-skills/base/AGENT.md` Section 6.3.

## Constitutional Compliance

All changes must comply with:
- **ENG-4.1**: Atomic TDD (NON-NEGOTIABLE)
- **ENG-4.2**: Test Pyramid structure
- **ENG-6.7**: Audit Trail requirements
- **BUS-2.1**: FAA Compliance (for aviation systems)
- **BUS-2.2**: Control Framework Law

## Quick Reference

### Invoking Skills
```
# When starting a feature — Hangar SDD process (ENG-11.1)
→ Use skill-spec-governance to scaffold hangar-ai-specs/changes/[id]/

# When enriching avatars or validating taxonomy
→ Use skill-30-taxonomy-governed-avatar-enrichment first

# When writing code
→ Use skill-06-atomic-tdd for TDD cycle

# When reviewing
→ Use skill-08-code-review + skill-27-constitution-compliance
```

### Phase Gate Tools
```
# Step 0 — commit phase artifact to git BEFORE running audit (ENG-12.2)
git add <phase-artifact.md> && git commit -m "..."

# Step 1 — citation audit (ENG-14.1): FAIL blocks; WARN activates J6 (non-blocking)
aa-citation-audit <phase-artifact.md>

# Step 2 — PRD-2.6 jury: spawn 5 task sub-agents on distinct models (ENG-12.3)
#   J1=claude-opus-4.6  J2=claude-sonnet-4.6  J3=gpt-5.4
#   J4=gpt-5.2          J5=gpt-5.4-mini       Synthesizer=claude-opus-4.5
#   Synthesis must have verdict: APPROVED; commit to hangar-ai-specs/changes/ before Step 3

# Step 3 — jury gate (ENG-12.1): any non-zero exit blocks; 1=FAIL 2=ERROR
aa-jury-gate <synthesis.md>

# Step 4 — render synthesis as HTML before presenting to human (ENG-13.1)
aa-artifact-render <synthesis.md>

# Step 5 — present rendered synthesis to human; await approval before advancing
# Agent cannot self-declare phase complete (ENG-12.3)
```

### Law Citation Format
```
Per ENG-4.1 (Atomic TDD Law), all code changes must follow RED-GREEN-REFACTOR.
```

### Compliance Check
```
Before merging, verify:
- [ ] Tests written before code (ENG-4.1)
- [ ] Complexity within limits (ENG-3.1)
- [ ] Security review complete (ENG-6.1)
- [ ] Audit logging in place (ENG-6.7)
```

## Constitution Lint

The hangar-ai-constitution includes an automated linter for compliance checking.

### Installation

```bash
cd tools/constitution-lint
pip install -e .
```

### Usage

```bash
# Lint current directory
aa-constitution-lint .

# Lint with JSON output (for CI/CD)
aa-constitution-lint --format json

# Install pre-commit hook
aa-constitution-lint hooks install
```

### What Gets Checked

| Check | Law | Description |
|-------|-----|-------------|
| AGENTS.md exists | ENG-1.2 | AI agent instructions file |
| Test pyramid structure | ENG-4.2 | Language-conventional test directory — Python/Node: `tests/unit/` + `tests/integration/`; Java/Maven/Gradle: `src/test/java/` (never create `tests/` at root if `src/test/` already exists) |
| hangar-ai-specs/ directory | ENG-11.1 | Hangar SDD spec folder required |
| Law references valid | ENG-10.1 | All ENG-*, PRD-*, BUS-* references |

### Atomic TDD Integration

Run `aa-constitution-lint .` at the VERIFY step (Step 5) of the 8-step Mandatory Agent Protocol above.

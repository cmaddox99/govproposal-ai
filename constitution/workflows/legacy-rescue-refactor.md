---
workflow:
  id: legacy-rescue-refactor
  name: Legacy Rescue — Refactor Track
  avatar_context: [engineering, business, product]
  laws: [ENG-3.1, ENG-4.1, ENG-4.10, ENG-4.6, ENG-4.11, ENG-6.1, ENG-6.7, BUS-2.1, BUS-2.2, BUS-2.4, BUS-7.1, ENG-11.1, ENG-12.1, ENG-12.2, ENG-12.3, ENG-4.12, ENG-3.4, ENG-2.5, ENG-2.1, ENG-2.2, ENG-2.4, ENG-3.2, ENG-4.14, ENG-3.9, ENG-3.10, ENG-3.11]
  skills: [skill-27-constitution-compliance, skill-09-refactoring, skill-06-atomic-tdd, skill-10-security-review, skill-11-mutation-testing, skill-14-technical-debt, skill-08-code-review, skill-spec-governance, skill-04-business-domain-modeling, skill-12-legacy-refactor-rhythm]
  preceded_by: adoption
  artifact_template: tools/templates/legacy-rescue/phase-artifact-template.html
  artifact_template_note: >
    ALL live phase HTML artifacts generated during this workflow MUST use
    tools/templates/legacy-rescue/phase-artifact-template.html as the base.
    Replace all {{TOKENS}}, follow every DESIGN RULE in the template comments,
    and write the output to hangar-ai-specs/changes/[spec-id]/phase-N-[name].html.
    The template contains the exact CSS, script, and component markup —
    do not inline different styles or invent new components.
---

# Workflow: Legacy Rescue — Refactor Track

> **Laws enforced:** ENG-4.1 (NON-NEGOTIABLE), ENG-4.14 (Commit Rhythm), ENG-6.1 (NON-NEGOTIABLE), ENG-6.7 (NON-NEGOTIABLE), BUS-7.1, ENG-11.1
> **Skills:** `skill-09-refactoring`, `skill-06-atomic-tdd`, `skill-12-legacy-refactor-rhythm`, `skill-spec-governance`
>
> **Tech-stack agnostic.** The phases, gates, and laws apply to any language or framework.
> For stack-specific tool commands see **[Tech Stack Translation](#tech-stack-translation)** at the bottom of this file.
> The Java/Spring Boot avatar (`avatars/technology/java-spring/`) contains additional
> Java-specific patterns and a `legacy-rescue-java.md` guide enriched from live runs.

---

## How to Invoke This Workflow

> **This section is the single source of truth for starting the Legacy Rescue Refactor workflow.**
> Do not maintain separate bootstrap prompts outside the constitution — they create drift.
> Reference this section directly or point agents here.

### Agent operating rules

When an agent runs this workflow on behalf of a human:

- **Execute all commands** on behalf of the human. The human observes and gives feedback.
- **Do NOT ask the human to run commands manually.** Run every command, capture the output, and interpret it.
- **Read before acting.** Before starting any phase, read this workflow in full, the codebase's `AGENTS.md`, and the relevant technology avatar manifest. Do not rely on memory of prior reads.
- **Announce checkpoints.** After Phase 0 say: `"Phase 0 complete — environment verified. Say 'proceed to Phase 1' when ready."` After each phase say: `"Phase N artifact open. Jury synthesis APPROVED. Awaiting your authorisation to proceed to Phase N+1."`
- **Never self-advance.** Each phase transition requires explicit human authorisation (ENG-12.1).

### How to start

```bash
# 1. Confirm constitution and codebase paths
CONSTITUTION=$(dirname $(dirname $(realpath $0)))   # or: path to your hangar-ai-constitution clone
REPO=$(git rev-parse --show-toplevel)
CODEBASE=$REPO   # or sub-path if codebase is nested

# 2. Verify adoption is complete (AGENTS.md + hangar-ai-specs/ present)
ls $CODEBASE/AGENTS.md $CODEBASE/hangar-ai-specs/

# 3. Read this workflow in full, then read AGENTS.md and the technology avatar
cat $CONSTITUTION/workflows/legacy-rescue-refactor.md
cat $CODEBASE/AGENTS.md

# 4. Run Phase 0 — Environment Setup (below), then proceed phase by phase
```

---

## Phase 0 — Environment Setup

**Goal:** Verify the environment is ready before Phase 1 begins. No codebase files are created or modified.

Run all checks in order. Report ✅ or 🔴 for each before moving to the next. If any check fails, diagnose and fix before proceeding — do not start Phase 1 until Phase 0 is fully green.

### Step 0.1 — Universal checks (all stacks)

```bash
REPO=$(git rev-parse --show-toplevel)
echo "Repo root: $REPO"

# Constitution tools
aa-citation-audit --version
aa-jury-gate --version
aa-constitution-lint --version 2>/dev/null || echo "aa-constitution-lint: check manually"

# Verify adoption
ls $CODEBASE/AGENTS.md && echo "✅ AGENTS.md" || echo "🔴 AGENTS.md missing — run adoption workflow first"
ls $CODEBASE/hangar-ai-specs/changes $CODEBASE/hangar-ai-specs/specs $CODEBASE/hangar-ai-specs/archive \
  && echo "✅ hangar-ai-specs structure" || echo "🔴 hangar-ai-specs incomplete"
```

### Step 0.2 — Stack-specific checks

Run the checks for your technology avatar:

**iOS (Swift / Xcode):**
```bash
xcodebuild -version            # Expected: Xcode 15+
swiftlint version              # Expected: 0.54+
xcrun simctl list devices available | grep "iPhone"   # At least one simulator present
cd $CODEBASE && xcodebuild -project *.xcodeproj -list   # Project opens cleanly
```

**Android (Kotlin):**
```bash
./gradlew --version            # Expected: Gradle 8+
java -version                  # Expected: JDK 17+
./gradlew assembleDebug -q     # Expected: BUILD SUCCESSFUL
./gradlew testDebugUnitTest -q # Expected: BUILD SUCCESSFUL
```

**Java / Spring Boot:**
```bash
java -version                  # Expected: OpenJDK 17+
mvn -version                   # Expected: Apache Maven 3.8+
cd $CODEBASE && mvn clean compile -q    # Expected: BUILD SUCCESS
mvn test -q                    # Expected: BUILD SUCCESS (baseline tests pass)
```

**Python:**
```bash
python --version               # Expected: 3.11+
pip show pytest pytest-cov ruff  # All installed
cd $CODEBASE && python -m pytest --tb=short -q  # Baseline test run
```

**TypeScript / Node:**
```bash
node --version                 # Expected: 18+
npx tsc --version              # TypeScript available
cd $CODEBASE && npm test -- --passWithNoTests  # Baseline test run
```

### Step 0.3 — Announce readiness

When all checks pass:
```
Phase 0 complete — environment verified. All tools present. Say "proceed to Phase 1" when ready.
```

---

## ⛔ Artifact Rendering Protocol — NON-NEGOTIABLE

> **Every human gate artifact generated by this workflow MUST use the canonical template.**
> This rule applies to ALL sessions, including sessions that resume mid-workflow.
> There are no exceptions.

### The one template

```
tools/templates/legacy-rescue/phase-artifact-template.html
```

### Mandatory steps before writing ANY phase-N-*.html file

1. **Read `tools/templates/legacy-rescue/phase-artifact-template.html` in full** — do not rely on memory.
2. **Copy the entire `<style>` block verbatim** into the new artifact. Do not paraphrase, condense, or substitute alternative CSS.
3. **Verify the copied CSS contains `--aa-blue: #003087`** — if you see `#0d1117` or `#58a6ff` you have used the wrong template.
4. **Include the AI-GENERATED DEMO REPO amber warning banner** (fixed position, top of page) exactly as in phase-1-assessment.html.
5. **Use `.page.cover` for the first page**, `.page` for subsequent pages.
6. **Use `.eyebrow` + `h1` for the cover header**, `.phase-hdr` + `.phase-num` for interior page headers.
7. **Use `.stat-card` / `.summary-band` for metric grids** — not custom metric cards.
8. **Use `.status-badge.pass/.fail/.warn`** — not custom badge classes.
9. **Write the output to** `hangar-ai-specs/changes/[spec-id]/phase-N-[name].html`.

### Self-check before committing

Run this mental checklist and refuse to commit if any item fails:

| Check | Pass condition |
|-------|---------------|
| `background: #fff` on body | ✅ White, not dark |
| `--aa-blue: #003087` in `:root` | ✅ Present |
| `--aa-red: #C8102E` in `:root` | ✅ Present |
| Top gradient bar `linear-gradient(90deg, var(--aa-blue), var(--aa-red))` | ✅ Present |
| No `#0d1117`, `#161b22`, `#58a6ff` in `<style>` | ✅ Absent (dark theme leaked) |
| AI-GENERATED DEMO REPO banner | ✅ Present |
| `.footer` with page number | ✅ Present |

> **Root cause of template drift** (documented from live run 2026-004): When a session resumes
> mid-workflow, the agent may generate new artifacts from memory rather than re-reading the template.
> The result is visually inconsistent artifacts — dark GitHub theme instead of white AA brand.
> Reading the template file first is the only reliable prevention.

---

## Prerequisites — Phase Gate Prerequisites (ENG-12.1)

> **Hardened 2026-05-26 — jury synthesis: phase-1-jury-synthesis.md APPROVED (PRD-2.6)**
> Root cause of prior bypass: browser-open command appeared before jury/synthesis were committed,
> creating an agent-exploitable early-stop state. Fixed below.

Each phase gate requires **all four artifacts committed** before the human gate is presented:

1. Phase artifact committed to `hangar-ai-specs/changes/<project-id>/phase-N-<name>.html`
2. `aa-citation-audit` run, exit 0 — output committed to `hangar-ai-specs/changes/<project-id>/phase-N-citation-audit.txt` (ENG-14.1)
3. Multi-cognition jury R1 + R2 deliberation complete (PRD-2.6 — 5 jurors, distinct LLM models)
4. Jury synthesis committed to `hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md` with `verdict: APPROVED`
5. **Human reviews jury synthesis findings before approving phase advance** ← THE CHECKPOINT

> **ENG-12.1 (NON-NEGOTIABLE):** Agent cannot advance to a new phase without a human reviewing jury synthesis findings. Jury APPROVED verdict required — agent cannot self-declare phase complete.

### ⛔ Mandatory phase gate sequence — HARD ORDERED (ENG-12.1, PRD-2.6)

**The agent MUST NOT open the phase artifact in a browser, announce "awaiting human review," or request phase advance until ALL FOUR commits above exist.**

If jury synthesis is missing or `verdict` is not `APPROVED`, the **only** allowed agent output is:
```
⛔ BLOCKED (PRD-2.6): Jury synthesis not committed. Cannot present human gate.
```

Required order — execute and commit each step before starting the next:

```bash
# STEP 1 — Commit phase artifact
git add hangar-ai-specs/changes/<project-id>/phase-N-<name>.html
git commit -m "feat: Phase N artifact ..."

# STEP 2 — Run citation audit and commit output
aa-citation-audit hangar-ai-specs/changes/<project-id>/phase-N-<name>.html \
  --laws-dir $CONSTITUTION/laws \
  > hangar-ai-specs/changes/<project-id>/phase-N-citation-audit.txt
# Must exit 0 before continuing
git add hangar-ai-specs/changes/<project-id>/phase-N-citation-audit.txt
git commit -m "evidence: Phase N citation audit PASS"

# STEP 3 — Run multi-cognition jury (PRD-2.6)
# Launch 5 jurors with DISTINCT LLM models (e.g. gpt-5.2, claude-opus, gpt-4.1, claude-sonnet, gpt-5-mini)
# Complete R1 individual deliberations, then R2 cross-juror synthesis

# STEP 4 — Commit jury synthesis with APPROVED verdict
# File: hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md
# Required frontmatter: schema_version, juror_count: 5, distinct models, r1_completed: true, r2_completed: true, verdict: APPROVED
git add hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md
git commit -m "governance: Phase N jury synthesis APPROVED (PRD-2.6)"

# STEP 4.5 — Validate jury synthesis mechanically (PRD-2.6 enforcement)
aa-jury-gate hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md \
  --log-dir ./logs
# Must exit 0 before continuing
# Validates: 5 jurors, distinct models, R1+R2 complete, verdict=APPROVED, git committed
git add logs/aa-jury-gate.jsonl
git commit -m "evidence: Phase N jury gate PASS (PRD-2.6)"

# STEP 5 — ONLY NOW: open materials for human review and STOP
open hangar-ai-specs/changes/<project-id>/phase-N-<name>.html
open hangar-ai-specs/changes/<project-id>/phase-N-jury-synthesis.md
echo "HUMAN GATE (ENG-12.1): Phase N materials open. Review jury synthesis APPROVED verdict before authorising Phase N+1."
# STOP — do not write any Phase N+1 files until human explicitly approves.
```

> **Why the browser-open is last, not first:** Opening the artifact was the prior workflow's implicit
> "task complete" signal. An agent that opens the browser before committing jury synthesis will
> announce human readiness while the gate is still open — this is the documented bypass mode.
> The `open` command is now gated on all four commits existing. (Hardened per jury synthesis 2026-05-26.)

### Jury Synthesis Artifact — Required Schema

Every `phase-N-jury-synthesis.md` must contain this frontmatter (validated by `aa-constitution-lint`):

```yaml
---
schema_version: 1
workflow: legacy-rescue-refactor
spec_id: <project-id>
phase: <N>
juror_count: 5
jurors:
  - id: J1
    role: <role>
    model: <distinct-model-id>
  - id: J2
    ...  # 5 total, all distinct model IDs
rounds:
  r1_completed: true
  r2_completed: true
verdict: APPROVED   # APPROVED | NEEDS_REVISION — must be APPROVED to pass gate
---
```

And must contain these three sections in body:
- `## Round 1 — Individual Juror Deliberations` (one entry per juror)
- `## Round 2 — Cross-Juror Synthesis` (converging themes, divergence, integrated assessment)
- `## Judicial Synthesis Verdict` (required changes + explicit `VERDICT: APPROVED`)

> **Template:** See `hangar-ai-specs/templates/jury-synthesis-template.md` in the constitution repo.
> **Exemplar:** See `hangar-ai-specs/examples/jury-synthesis-exemplar-phase1.md` for a complete example.

### Per-phase gate artifacts — required commits before browser-open

Replace `<project-id>` with your spec ID (e.g. `legacy-rescue-aadvantage-ios`).

| Phase | Phase artifact | Jury synthesis | Browser open (Step 5 only) |
|-------|---------------|----------------|---------------------------|
| 1 — Assess | `phase-1-assessment.html` | `phase-1-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-1-assessment.html` |
| 2 — Govern | `phase-2-govern.html` | `phase-2-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-2-govern.html` |
| 3 — Characterize | `phase-3-characterize.html` | `phase-3-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-3-characterize.html` |
| 4 — Remediate | `phase-4-remediate.html` | `phase-4-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-4-remediate.html` |
| 5 — Refactor | `phase-5-refactor.html` | `phase-5-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-5-refactor.html` |
| 6 — Certify | `phase-6-certify.html` | `phase-6-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-6-certify.html` |
| 7 — Harden (Mutation) | `phase-7-harden.html` | `phase-7-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-7-harden.html` |
| 8 — SOLID Rescue | `phase-8-solid.html` | `phase-8-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-8-solid.html` |
| 9 — DDD Modernization | `phase-9-ddd.html` | `phase-9-jury-synthesis.md` | `open hangar-ai-specs/changes/<project-id>/phase-9-ddd.html` |

> **macOS:** `open` launches the default browser. **Linux:** substitute `xdg-open`. **Windows (WSL):** substitute `wslview`.
> The `open` command is Step 5 — it executes only after Steps 1–4 are committed.

### Forbidden agent behaviours (ENG-12.1 enforcement)

The following are constitutional violations. An agent that performs any of these before jury synthesis is committed has breached ENG-12.1:

- Stating "ready for human review," "awaiting human review," or "phase complete"
- Opening the phase artifact in a browser
- Announcing the human gate stop
- Writing any Phase N+1 files

**If jury synthesis is missing:** The only allowed output is `⛔ BLOCKED (PRD-2.6): Jury synthesis not committed.`

> **Backlog — `aa-jury-gate` CLI:** A dedicated tool to validate jury synthesis schema, model distinctness, round completion, and git commit status is tracked as a constitution tooling backlog item. Until available, the workflow bash guards above are the enforcement mechanism.

---

## Standard Juror Panel (PRD-2.6)

All phase gates in this workflow use this 5-juror panel. Each juror runs on a **distinct LLM model** — do not use the same model twice in a single jury.

| ID | Role | Default Model |
|----|------|---------------|
| J1 | Senior Workflow Architect — validates process compliance and constitutional gate sequence | `gpt-5.2` |
| J2 | Constitutional Governance Specialist — validates law citations, severity classifications, regulatory scope | `claude-opus-4.5` |
| J3 | AI Agent Behavior Specialist — validates that agent actions are reproducible and non-ambiguous | `gpt-4.1` |
| J4 | Learner / Team Experience Specialist — validates clarity, completeness, and educational value of the artifact | `claude-sonnet-4.5` |
| J5 | DevSecOps & Tooling Specialist — validates security findings, tool outputs, and evidence quality | `gpt-5.4-mini` |

> **Substitute any model** if one is unavailable — the requirement is 5 jurors with distinct model IDs, not specific model names. Document substitutions in the synthesis frontmatter.

### Jury prompt template

Use this prompt for each juror, substituting their role and the phase artifact path:

```
You are [Role] serving as Juror [ID] in a multi-cognition jury for the Hangar AI Constitution
Legacy Rescue Refactor workflow — Phase [N] gate.

Artifact under review: hangar-ai-specs/changes/<spec-id>/phase-N-<name>.html
Constitution path: $CONSTITUTION

Your task (R1 deliberation):
Review the artifact for compliance with the constitutional laws cited. Consider:
- Are all violations correctly identified, cited, and severity-classified?
- Are law citations valid and non-negotiable laws flagged correctly?
- Is the phase gate status accurate (NOT MET is expected for Phase 1)?
- Are there any missing violations or incorrect findings?

Deliver: your analysis, specific concerns or approval, and confidence level.
Vote: APPROVE | NEEDS_REVISION (with blocking reason)
```

After all 5 R1 deliberations are collected, run R2 (cross-juror synthesis), then produce the judicial synthesis using `hangar-ai-specs/templates/jury-synthesis-template.md`.

---

## Gate Narrative — Expected State Per Phase

The Hangar AI Constitution Gate is designed to tell a clear story across the workflow. **If Phase 1 shows GREEN, something is wrong** — either the wrong gate is assigned or the project does not have the legacy violations this workflow addresses.

| Phase | Expected State | Why |
|-------|----------------|-----|
| **1 — Assess** | 🔴 **violations present** | Legacy code has bugs and zero test coverage. **This state is the problem statement.** |
| **2 — Govern** | 🔴 **violations present** | No code changes yet; same legacy state |
| **3 — Characterize** | 🟡 **improving** | Coverage climbs to ≥95%; some legacy violations remain until Phase 4 remediates |
| **4 — Remediate** | 🟡 → 🟢 **transitioning** | Bugs fixed; security fixes applied; ruff bugs=0 and vulnerability gates may pass here |
| **5 — Refactor** | 🟢 **all gates passing** | Must maintain all gates; no regressions |
| **6 — Certify** | 🟢 **all gates passing** | All conditions met and jury synthesis APPROVED. **This is the certification moment — the rescue is complete.** |
| **7 — Harden** | 🟢 **all gates passing** | Mutation hardening; score evidenced via mutation HTML report |
| **8 — SOLID Rescue** | 🟢 **all gates passing** | SOLID violations are design-level; evidence is the SOLID audit register and phase artifact |
| **9 — DDD Modernization** | 🟢 **all gates passing** | DDD tactical patterns applied; coverage maintained ≥95%; bounded context map and evidence package committed |

> **If Phase 5 or 6 shows regressions:** A regression was introduced. Check new violations and `ruff` output — they will pinpoint which new code broke the gate.

---

## Phase Table

| Phase | Name | Key Activities | Constitutional Gate |
|---|---|---|---|
| 1 | Assess | Constitution audit; violation inventory citing law IDs; compliance risk classification; **compliance assessment: identify applicable regulations per bounded context (FAA, DOT, PCI, GDPR) via `skill-27-constitution-compliance`**; **🎨 Generate `phase-1-assessment.html` using canonical template** | Violations documented in `hangar-ai-specs/changes/[id]/`; regulatory scope confirmed (BUS-2.1); **Phase 1 assessment artifact with violation inventory committed; jury synthesis APPROVED** |
| 2 | Govern | Create `hangar-ai-specs/` structure; activate avatars; define remediation proposal; **🎨 Generate `phase-2-govern.html` using canonical template** | Proposal approved in `hangar-ai-specs/changes/` |
| 3 | Characterize | **Declare characterization scope first** (see below). Write characterization tests that lock existing behavior before any change (ENG-4.10) — every class in the declared scope needs a test. Target ≥95% coverage **across the full declared scope, not just the classes you choose to test**; **🎨 Generate `phase-3-characterize.html` using canonical template** | Characterization scope registered in `PROPOSAL.md`; all classes in scope have tests; **pytest-cov ≥95% on characterization scope (ENG-4.6); jury attests coverage threshold met.** CI green. |
| 4 | Remediate | Fix violations in priority order (Security > Correctness > Reliability); one violation per commit; re-run full characterization suite after every fix; **🎨 Generate `phase-4-remediate.html` using canonical template** | All P0 violations resolved; zero regression; **🚨 Phase 4 HARD_BLOCK: `vulnerabilities`=0; `ruff bugs=0`; `security_rating`=A; `blocker_violations`=0; `critical_violations`=0 (includes code quality Critical issues: duplicate literals, empty methods, wildcard types). Note: cognitive complexity is Critical-severity but addressed in Phase 5 refactoring — fix it there.** |
| 5 | Refactor | Reduce complexity (ENG-3.1); extract domain objects (ENG-2.1); Boy Scout commits (ENG-1.3). **Any new class extracted during refactor is automatically added to characterization scope — tests must be written for it before the phase gate closes**; **🎨 Generate `phase-5-refactor.html` using canonical template** | Complexity ≤10 for refactored methods; **🚨 Phase 5 HARD_BLOCK: pytest-cov ≥ 95% (including new classes, ENG-4.6); `code_smells` must not increase; `critical_violations`=0 (cognitive complexity must be resolved here if deferred from Phase 4)** |
| 6 | Certify | Final compliance report; coverage and mutation evidence artifacts comparing Phase 1 baseline vs current; audit evidence package (BUS-7.1); proposal archived; **🎨 Generate `phase-6-certify.html` using canonical template** | Zero open violations; coverage and mutation evidence committed to `hangar-ai-specs/archive/`; **🚨 Phase 6 HARD_BLOCK: all phase gates satisfied; jury attests 0 critical findings (PRD-2.6); ✅ EXPECTED: all thresholds met — this is the certification moment.** |
| 7 | Harden — Mutation | Run mutation testing (see stack translation below); review surviving mutants; strengthen assertions and edge-case tests until mutation score ≥ 90% (ENG-4.12 NON-NEGOTIABLE). Each surviving mutant must be either killed with a new test or explicitly accepted with a law citation in the surviving-mutant register; **🎨 Generate `phase-7-harden.html` using canonical template** | **🚨 Phase 7 HARD_BLOCK: mutation score ≥ 90%; `coverageThreshold` ≥ 95%; mutation HTML report committed to `hangar-ai-specs/evidence/mutation-report/`; surviving-mutant register reviewed and signed off by lead** |
| 8 | Harden — SOLID Rescue | Perform a full SOLID audit across all domain and application layer classes (SRP: ENG-3.4, OCP, LSP, ISP, DIP: ENG-2.5). For each violation: write a failing test proving the violation, remediate, confirm the test passes (ENG-4.1 atomic TDD). One violation per commit. Update the surviving-mutant register for any newly exposed test coverage paths. **🎨 Generate `phase-8-solid.html` using canonical template** | **🚨 Phase 8 HARD_BLOCK: zero SRP (ENG-3.4), OCP, LSP, ISP violations in domain and application layers; zero DIP violations (ENG-2.5); coverage ≥ 95% maintained (ENG-4.6); SOLID audit register committed to `hangar-ai-specs/evidence/solid-audit/`; BUS-7.1 audit trail** |
| 9 | Modernize — DDD | Apply DDD tactical patterns (ENG-2.1): identify bounded contexts (ENG-2.4); replace primitive obsession with Value Objects (ENG-3.2 — immutable; apply OCP: extend-not-modify); enforce layered architecture with no infrastructure imports in domain layer (ENG-2.2); introduce Anti-Corruption Layer at context boundaries; write new characterization tests for all new domain types before extraction commits. **🎨 Generate `phase-9-ddd.html` using canonical template** | **🚨 Phase 9 HARD_BLOCK: zero infrastructure imports in domain layer (ENG-2.2); all domain primitives elevated to Value Objects or Entities (ENG-2.1); bounded context map committed to `hangar-ai-specs/evidence/bounded-context-map/`; coverage ≥ 95% maintained (ENG-4.6); BUS-7.1 audit trail** |

> 🎨 **Render as HTML (Phase 2 — Proposal):** `aa-artifact-render hangar-ai-specs/changes/[id]/PROPOSAL.md --laws-dir laws`
> 🎨 **Render as HTML (Phase 7 — Mutation report):** `aa-artifact-render hangar-ai-specs/evidence/mutation-report/ --laws-dir laws`
> 🎨 **Render as HTML (Phase 8 — SOLID audit):** `aa-artifact-render hangar-ai-specs/evidence/solid-audit/solid-audit-register.md --laws-dir laws`
> 🎨 **Render as HTML (Phase 9 — DDD model):** `aa-artifact-render hangar-ai-specs/evidence/bounded-context-map/ --laws-dir laws`
> Add `--pdf` to also generate a PDF. This embeds law citation tooltips from the constitution.

---

## Phase 3 — Characterization Scope Protocol

> **Laws:** ENG-4.10 (Test Evolution), ENG-4.14 (Legacy Rescue Commit Rhythm — Characterization Cycle), ENG-4.6 (Coverage Requirements), BUS-2.1  
> **Skills:** `skill-06-atomic-tdd`, `skill-12-legacy-refactor-rhythm`  
> **Commit Rhythm:** One characterization test per commit (7-step cycle). **Complete each cycle (Steps 1-7, including commit) BEFORE starting the next cycle.** See skill-12 for detailed workflow.

> **Learning from live run (2026-004):** 25 tests were written for 4 of 29 classes. Coverage landed at 21.7% — far below the ≥95% gate. The root cause was that scope was never declared; only the riskiest classes were tested. The gate was breached silently. This protocol prevents that.

**Before writing a single test:**

1. **Produce a class inventory.** List every non-test, non-generated class in the module. For Java: `find src/main -name "*.java" | sort`. For Python: `find src -name "*.py" | grep -v __pycache__`. For TypeScript: `find src -name "*.ts" | grep -v spec`.

2. **Classify each class** into one of three categories:
   - `IN_SCOPE` — must reach ≥95% coverage; characterization test required
   - `EXCLUDED` — generated code, DTOs with no logic, pure config; document reason
   - `DEFERRED` — test will be written but not in this phase; must be tracked as a known gap with a law citation explaining why deferral is acceptable

3. **Register the scope in `PROPOSAL.md`** before any test is written:
   ```markdown
   ## Characterization Scope (Phase 3)
   | Class | Category | Reason if EXCLUDED/DEFERRED |
   |-------|----------|-----------------------------|
   | MileageService | IN_SCOPE | |
   | AccrualService | IN_SCOPE | |
   | MileageCalculator | IN_SCOPE | |
   | EnrollmentRequest | EXCLUDED | DTO — no logic, only getters/setters |
   | Application | EXCLUDED | Spring Boot entry point — no business logic |
   ```

4. **The Phase 3 gate applies only to IN_SCOPE classes.** pytest-cov must show ≥95% coverage across those classes (ENG-4.6). EXCLUDED classes must have a documented reason. DEFERRED classes must have a tracking ticket and law citation.

5. **Phase 4 cannot begin until the scope registry exists and pytest-cov confirms ≥95% on IN_SCOPE classes (ENG-4.6).**

---

## Phase 5 — Refactor Scope Extension Rule

> **Laws:** ENG-4.14 (Legacy Rescue Commit Rhythm — Refactor Cycle), ENG-3.4 (SRP), ENG-3.9 (OCP), ENG-3.10 (LSP), ENG-3.11 (ISP), ENG-4.6 (Coverage Requirements)  
> **Skills:** `skill-09-refactoring`, `skill-12-legacy-refactor-rhythm`  
> **Commit Rhythm:** One violation remediation per commit (8-step cycle). **Complete each cycle (Steps 1-8, including commit) BEFORE starting the next cycle.** See skill-12 for detailed workflow.

> **Learning from live run (2026-004):** `AccrualService` and `MileageAdminService` were extracted from `MileageService` during Phase 5. Both had 0% coverage at Phase 6 because no tests were written for the new classes. This violates Phase 5's pytest-cov ≥ 95% gate (ENG-4.6).

**Rule:** When a refactor extracts a new class from an existing IN_SCOPE class:
- The new class is **automatically IN_SCOPE**
- Tests for the new class must be written **within the same Phase 5 commit batch**
- The Phase 5 gate does not close until pytest-cov shows the new class at ≥95% (ENG-4.6)

This is not optional. pytest-cov ≥95% on new classes (ENG-4.6) is a Phase 5 HARD_BLOCK.

### Test Level Migration Rule

> **Insight from live run (2026-004):** Extraction changes the test pyramid level of the original characterization test. This is not just a coverage problem — it is a test design problem.

When behavior moves from a god class to an extracted service, the existing characterization test changes level:

| Test | Before extraction | After extraction |
|------|------------------|-----------------|
| `GodClassCharacterizationTest.someMethod` | ✅ Unit test — behavior lives here | ⬆️ Integration characterization — now tests wiring, not behavior |
| `ExtractedServiceCharacterizationTest.someMethod` | Does not exist | ✅ New unit test — behavior lives here now |

**The correct Phase 5 response to an extraction:**

1. **Write new unit characterization tests for the extracted class** — these test the behavior at its new home. Same behavioral assertions as the originals; new mock setup for the extracted class's own dependencies.

2. **Relabel the original test** with a `// INTEGRATION-CHARACTERIZATION` comment — it now validates that the coordinator correctly delegates to the extracted service. These integration tests are still valuable (they test wiring) but they are no longer the primary behavioral evidence.

3. **Do not delete the original tests.** A deleted integration characterization test removes the only evidence that the coordinator still delegates correctly. Keep both levels.

4. **The mutation score confirms the level shift naturally.** After extraction, PIT will show low mutation score on the original coordinator (because its logic is gone). High mutation score on the extracted class (because that's where the logic lives). This is the correct outcome.

**In short: behavior moves → tests move with it. The original test is promoted to integration level, not replaced.**

---

## Tech Stack Translation

The phases and gates are identical across all stacks. Only the tools change.

### Coverage & Test Tools

| Stack | Test Framework | Coverage Tool | Coverage Report |
|-------|---------------|---------------|-----------------|
| **Java / Spring Boot** | JUnit 5 + Mockito | JaCoCo (`jacoco-maven-plugin`) | `target/site/jacoco/jacoco.xml` |
| **Python** | pytest | pytest-cov | `coverage.xml` |
| **TypeScript / Node** | Jest | Jest (`--coverage`) | `coverage/lcov.info` |
| **.NET / C#** | xUnit / NUnit | coverlet | `coverage.cobertura.xml` |
| **Go** | `go test` | built-in (`-coverprofile`) | `coverage.out` |
| **Kotlin / Android** | JUnit 5 + Mockito-Kotlin | JaCoCo | `build/reports/jacoco/` |

### Mutation Testing Tools

> **Mutation Tool SSOT:** Approved mutation testing tools and commands are defined in
> [`skill-11-mutation-testing`](../agent-skills/skills-by-domain/development-practices/11-mutation-testing.md).
> If this workflow table conflicts with the skill, follow the skill.

| Stack | Tool | Run Command | Report Location |
|-------|------|-------------|-----------------|
| **Java / Spring Boot** | PIT (pitest-maven) | `mvn org.pitest:pitest-maven:mutationCoverage` | `target/pit-reports/index.html` |
| **Python** | mutmut | `mutmut run && mutmut html` | `html/index.html` |
| **TypeScript / Node** | Stryker | `npx stryker run` | `reports/mutation/index.html` |
| **.NET / C#** | Stryker.NET | `dotnet stryker` | `StrykerOutput/reports/mutation-report.html` |
| **Go** | gremlins | `gremlins unleash` | `stdout` (JSON via `--output=gremlins.json`); run from module root |
| **iOS / Swift** | Muter | `muter run --format html --output muter-report.html` | `muter-report.html` |
| **Android / Kotlin** | pl.droidsonroids.pitest | `./gradlew :<module>:pitestDebug` | `<module>/build/reports/pitest/debug/index.html` |

### Static Analysis / Quality Gate

| Stack | Linter / Analyzer |
|-------|------------------|
| **Java** | Checkstyle, SpotBugs |
| **Python** | ruff, pylint |
| **TypeScript** | ESLint |
| **.NET** | Roslyn Analyzers |
| **Go** | golangci-lint |

---

## Phase 8 — SOLID Rescue

> **Purpose:** Eliminate SOLID violations in the domain and application layers. These are architectural design-level violations; Phase 6 certification proves runtime correctness but does not prove design principle compliance.

> **Constitutional basis:** ENG-3.4 (SRP), ENG-2.5 (DIP), ENG-4.1 (Atomic TDD NON-NEGOTIABLE), ENG-4.6 (Coverage), BUS-7.1 (Audit Trail) — OCP, LSP, ISP enforced as SOLID principles (laws not yet authored)

### Step 8.1 — SOLID Audit

Produce a SOLID audit register covering every class in the domain and application layers. For each class:

| Check | Law | VIOLATION signal |
|-------|-----|-----------------|
| One reason to change | ENG-3.4 | Class name contains "And", "Manager", "Handler" doing unrelated operations |
| Open for extension, closed for modification | OCP | `if/switch` on type discriminator in domain logic |
| Subtypes substitutable for base types | LSP | `instanceof` cast before calling abstract method; no-op override throwing exception |
| Clients depend only on methods they use | ISP | Fat interface with methods unused by at least one implementor |
| Depend on abstractions, not concretions | ENG-2.5 | `new ConcreteImpl()` inside domain class; domain importing infrastructure package |

Commit the audit register to `hangar-ai-specs/evidence/solid-audit/solid-audit-register.md`.

### Step 8.2 — Remediate Each Violation (Atomic TDD — ENG-4.1)

For each violation in the register, follow the 8-step atomic TDD cycle:

1. **IDENTIFY** — Cite the law violated and the exact line(s)
2. **RED** — Write a failing test that proves the violation is observable behaviour
3. **GREEN** — Apply the minimal refactoring to pass the test (strategy, interface split, DI, etc.)
4. **REFACTOR** — Clean up; verify no other tests break
5. **VERIFY** — Re-run full suite; confirm coverage ≥ 95% maintained
6. **UPDATE** — Mark violation RESOLVED in the audit register with law citation
7. **COMMIT** — One atomic commit per violation
8. **STOP AND REPORT** — Present the remediated violation to the lead; await approval before next cycle

### Step 8.3 — Phase Gate

Generate `phase-8-solid.html` using the canonical template (`tools/templates/legacy-rescue/phase-artifact-template.html`). The artifact must include:

- SOLID audit register (before/after for each violation)
- Law citations for each remediation (ENG-3.4, ENG-2.5, or SOLID principle name for OCP/LSP/ISP)
- Test count delta and coverage proof
- Disposition: `GATE GREEN — SOLID Rescue Complete`

**🚨 Phase 8 HARD_BLOCK:** Zero OCP/LSP/ISP/SRP/DIP violations in domain and application layers. Coverage ≥ 95% maintained. Audit register signed off by lead (BUS-7.1).

---

## Phase 9 — DDD Modernization

> **Purpose:** Elevate the rescued codebase from structurally correct to domain-expressive. Replace primitive obsession and anemic domain models with rich DDD tactical patterns (ENG-2.1). Enforce strict layer boundaries (ENG-2.2) and bounded context isolation (ENG-2.4).

> **Constitutional basis:** ENG-2.1 (DDD), ENG-2.2 (Layered Architecture), ENG-2.4 (Bounded Context), ENG-3.2 (Immutability), ENG-4.1 (Atomic TDD NON-NEGOTIABLE), ENG-4.6 (Coverage), BUS-7.1 (Audit Trail)

### Step 9.1 — Domain Model Inventory

Identify and classify all domain primitives that should be elevated:

| Pattern | Trigger | Target |
|---------|---------|--------|
| Value Object | Raw `String`/`int` for domain concepts (tier name, loyalty points, money) | Immutable value type (ENG-3.2) with behaviour and validation |
| Entity | Object with identity that changes over time | UUID key, creation/modification metadata |
| Domain Service | Business logic not belonging to one entity | Stateless service with ubiquitous language name |
| Aggregate | Cluster of entities with transactional consistency boundary | Single aggregate root; external refs by ID only |
| Domain Event | Significant state change that other contexts care about | Immutable record; decouples bounded contexts |

Commit the domain model map to `hangar-ai-specs/evidence/domain-model/domain-model-map.md`.

### Step 9.2 — Bounded Context Mapping

1. Identify bounded contexts from the existing module/package structure
2. For each cross-context dependency, document the integration pattern: Customer/Supplier, Conformist, Anti-Corruption Layer (ACL), Shared Kernel, Open Host Service
3. If a context consumes a foreign model directly (no translation), introduce an ACL
4. Commit the bounded context map to `hangar-ai-specs/evidence/bounded-context-map/`

### Step 9.3 — Modernize (Atomic TDD — ENG-4.1)

For each primitive elevation or layer violation, follow the 8-step cycle:

1. **IDENTIFY** — Cite ENG-2.1, ENG-2.2, ENG-2.4, or ENG-3.2 as applicable
2. **RED** — Write a test for the new domain type's invariants (e.g., `LoyaltyPoints` cannot be negative)
3. **GREEN** — Create the new type; update all usages
4. **REFACTOR** — Remove the primitive; verify no layer boundaries broken
5. **VERIFY** — Full suite green; coverage ≥ 95%; no infrastructure import in domain layer
6. **UPDATE** — Mark item complete in domain model map
7. **COMMIT** — One atomic commit per domain type
8. **STOP AND REPORT** — Await approval before next type

### Step 9.4 — Layer Purity Verification

Run a static dependency check to confirm the domain layer has no infrastructure imports:

```bash
# Java — no javax.persistence, org.springframework.data, or JDBC in domain classes
grep -rn "import javax.persistence\|import org.springframework.data\|import java.sql" src/main/java/*/domain/

# TypeScript — no ORM or database imports in domain/
grep -rn "import.*typeorm\|import.*prisma\|import.*mongoose" src/domain/

# Kotlin/Android — no Room, Retrofit, or Hilt in domain layer
grep -rn "import androidx.room\|import retrofit2\|import dagger" src/main/kotlin/*/domain/
```

Zero output = domain layer is pure.

### Step 9.5 — Phase Gate

Generate `phase-9-ddd.html` using the canonical template. The artifact must include:

- Domain model inventory (before: primitives → after: value objects/entities)
- Bounded context map
- Layer purity verification output
- Test count delta and coverage proof
- Disposition: `GATE GREEN — DDD Modernization Complete`

**🚨 Phase 9 HARD_BLOCK:** Zero infrastructure imports in domain layer (ENG-2.2). All domain primitives elevated to appropriate DDD tactical type (ENG-2.1). Bounded context map committed. Coverage ≥ 95% maintained. Evidence package signed off (BUS-7.1).

---

## Running Mutation Testing (Phase 7)

### Java / Spring Boot (PIT)
```bash
# Requires Maven and compiled tests
export JAVA_HOME=/path/to/jdk
export MVN=/path/to/mvn   # or system mvn if on PATH

$MVN test org.pitest:pitest-maven:mutationCoverage

# Report: target/pit-reports/index.html
# Constitutional gate: mutationThreshold=90, coverageThreshold=95
```

**Required `pom.xml` configuration:**
```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.15.3</version>
  <configuration>
    <targetClasses><param>com.example.*</param></targetClasses>
    <targetTests><param>com.example.*</param></targetTests>
    <mutators><mutator>STRONGER</mutator></mutators>
    <mutationThreshold>90</mutationThreshold>
    <coverageThreshold>95</coverageThreshold>
    <outputFormats><outputFormat>HTML</outputFormat><outputFormat>XML</outputFormat></outputFormats>
    <timestampedReports>false</timestampedReports>
    <reportsDirectory>target/pit-reports</reportsDirectory>
  </configuration>
</plugin>
```

### Python (mutmut)
```bash
pip install mutmut
mutmut run
mutmut html
# Report: html/index.html
# Surviving mutants: mutmut results
```

### TypeScript (Stryker)
```bash
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner
npx stryker run
# Report: reports/mutation/index.html
```

### .NET (Stryker.NET)
```bash
dotnet tool install -g dotnet-stryker
dotnet stryker --threshold-high 90 --threshold-low 80
# Report: StrykerOutput/reports/mutation-report.html
```

### iOS / Swift (Muter)
```bash
# Install
brew install muter-mutation-testing/formulae/muter

# Initialise — generates muter.conf.yml
cd ios/<project>
muter init

# muter.conf.yml — minimum required configuration:
# executable: xcodebuild
# arguments:
#   - -project
#   - <Project>.xcodeproj          # or -workspace <Project>.xcworkspace
#   - -scheme
#   - <Scheme>
#   - -destination
#   - platform=iOS Simulator,name=iPhone 15
#   - test
# exclude:
#   - Pods/
#   - DerivedData/
#   - <Generated files>

muter run --format html --output muter-report.html
# Report: muter-report.html
# Constitutional gate (ENG-4.11): ≥70% general, ≥85% critical paths
# Constitutional gate (ENG-4.12 Legacy Rescue): ≥90% NON-NEGOTIABLE
```

### Android / Kotlin (pl.droidsonroids.pitest)
```bash
# Step 1: Add plugin to root build.gradle.kts
# plugins {
#     id("pl.droidsonroids.pitest") version "0.2.27" apply false
# }

# Step 2: Configure per-module build.gradle.kts
# plugins { id("pl.droidsonroids.pitest") }
# pitest {
#     targetClasses.set(listOf("com.aa.<module>.*"))
#     targetTests.set(listOf("com.aa.<module>.*Test"))
#     mutationThreshold.set(90)   // ENG-4.12 (Legacy Rescue); use 70 for ENG-4.11 general
#     outputFormats.set(setOf("HTML", "XML"))
#     threads.set(4)
# }

./gradlew :<module>:pitestDebug
# Report: <module>/build/reports/pitest/debug/index.html
# Constitutional gate (ENG-4.11): ≥70% general, ≥85% critical paths
# Constitutional gate (ENG-4.12 Legacy Rescue): ≥90% NON-NEGOTIABLE
```

> **ENG-4.12 (NON-NEGOTIABLE):** The mutation score MUST reach ≥ 90% before the workflow is considered complete.
> A surviving mutant is an untested assumption — the law treats it as a latent defect.

---

## Known Pitfalls (from live runs)

| Pitfall | What happens | How to avoid |
|---------|-------------|--------------|
| **Scope not declared before Phase 3** | Tests written for "riskiest" classes only; 25 tests for 4/29 classes; coverage lands at 21% instead of 95% | Produce class inventory and register IN_SCOPE list in `PROPOSAL.md` before writing any test |
| **New classes from Phase 5 refactor not tested** | `AccrualService` extracted from god class; 0% coverage at Phase 6 | Apply Refactor Scope Extension Rule: new class = IN_SCOPE immediately |
| **Python f-strings with `${VAR}` Spring references** | `NameError: name 'DB_PASS' is not defined` when generating HTML artifacts | Use non-f-string template + `.replace()`, or escape as `${{DB_PASS}}` in f-strings |
| **Advancing past a gate without jury APPROVED verdict** | Phase 4 begins with 0% coverage — characterization provides no safety net for remediation | ENG-12.1: jury synthesis verdict must be reviewed by a human before phase advance. |
| **Mutation testing run before coverage ≥ 95%** | PIT's `coverageThreshold` blocks the run; surviving mutants are meaningless on uncovered code | Reach pytest-cov ≥95% first, then run mutation testing |
| **Phase 5 extraction without test level migration** | God class tests become integration characterization silently; new extracted class has 0% unit coverage; mutation score is meaningless at wrong level | Apply Test Level Migration Rule: write new unit tests at extracted class; relabel original as `// INTEGRATION-CHARACTERIZATION`; keep both |
| **Bare `RuntimeException` in remediated code** | Technical debt increases after Phase 4; `code_smells` gate may fail in Phase 5 | Use typed exceptions during remediation; check `code_smells` does not increase |
| **Dark-theme artifact drift (template drift)** | A resumed session generates phase artifacts from memory using a dark GitHub-style theme (`#0d1117`) instead of the AA white template — resulting in visually inconsistent artifacts across phases (observed in live run 2026-004, phases 3–7) | **Always read `tools/templates/legacy-rescue/phase-artifact-template.html` before generating any artifact.** Verify `--aa-blue: #003087` is in the CSS. See the Artifact Rendering Protocol section at the top of this file. |

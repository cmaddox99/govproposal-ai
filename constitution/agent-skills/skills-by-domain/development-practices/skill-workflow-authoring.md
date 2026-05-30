---
skill:
  id: skill-workflow-authoring
  name: Workflow Authoring
  category: governance
  version: "1.0.0"

laws:
  implements:
    - id: ENG-11.1
      title: Hangar SDD Law
    - id: ENG-10.1
      title: Constitution Governance Law
  references:
    - id: ENG-12.1
      title: Agentic Feedback Loop Law
    - id: BUS-7.1
      title: Audit Trail Law

triggers:
  phrases:
    - "Create a new workflow"
    - "Add a workflow to the constitution"
    - "How do I author a workflow"
    - "Workflow file format"
    - "What structure does a workflow file need"
    - "Write a governed workflow"

followed_by:
  - skill-spec-governance
  - skill-27-constitution-compliance
---

# Skill: Workflow Authoring

> **Purpose:** Define and create a new governed workflow for the Hangar AI Constitution, following the canonical workflow file format established by `adoption.md`.
> **Laws:** ENG-11.1 (SDD), ENG-10.1 (Governance), ENG-12.1 (Agentic Feedback Loop)

---

## Canonical Workflow File Format

Every workflow in `workflows/` MUST contain the following sections in this order:

```
1. YAML Frontmatter           (machine-readable metadata)
2. # Workflow: <Name>         (H1 title)
3. > Laws + Skills callout    (quick reference block)
4. ## Prerequisites           (SonarQube gate + setup — ENG-12.1)
5. ## Phase Table             (summary table — all phases on one screen)
6. ## Phase N: <Name>         (one H2 section per phase — step-by-step)
   ### Step N.x               (H3 steps with Copilot prompts + evidence templates)
7. ## Failure Modes           (recovery table — ≥5 modes)
8. ## Conditional Skip Logic  (when phases may be skipped — if applicable)
```

---

## 1. Required Frontmatter

```yaml
---
workflow:
  id: <kebab-case-id>                      # REQUIRED: unique, matches filename
  name: <Human Readable Name>              # REQUIRED
  avatar_context: [engineering, product]   # REQUIRED: one or more of: engineering, product, business
  laws: [ENG-4.1, ENG-11.1, ...]          # REQUIRED: all laws this workflow enforces
  skills: [skill-06-atomic-tdd, ...]       # REQUIRED: all skills activated
  preceded_by: <workflow-id> | null        # REQUIRED: null only for adoption
  followed_by:                             # OPTIONAL
    - <workflow-id>
  triggers:                                # OPTIONAL but recommended for RAG routing
    - "phrase that activates this workflow"
---
```

**Rules:**
- `id` MUST match the filename stem (e.g., `legacy-rescue-refactor` → `legacy-rescue-refactor.md`)
- `laws` MUST include every law cited in phase gates
- `preceded_by: adoption` for all workflows except `adoption` itself

---

## 2. Laws + Skills Quick-Reference Block

Immediately after the H1 title:

```markdown
> **Laws enforced:** ENG-4.1 (NON-NEGOTIABLE), ENG-6.1 (NON-NEGOTIABLE), BUS-7.1, ENG-11.1
> **Skills:** `skill-06-atomic-tdd`, `skill-spec-governance`, `skill-sonarqube-compliance-gate`
> **Purpose:** One sentence describing what this workflow governs.
```

---

## 3. Prerequisites Section (ENG-12.1 NON-NEGOTIABLE)

Every workflow that uses SonarQube gates MUST include a Prerequisites section before the Phase Table:

```markdown
## Prerequisites — Constitutional Gate

**Before Phase 1 begins, the Constitutional Gate MUST be provisioned. (ENG-12.1 NON-NEGOTIABLE)**

**Local Development:**
\```bash
cd /path/to/hangar-ai-constitution
./tools/sonarqube-gate/provision.sh --project-key <your-project-key> --token-path <project-root>/.sonar-token
\```

**Corporate SonarQube:**
\```bash
export SONARQUBE_URL=https://sonarqube.aa.com
export SONARQUBE_TOKEN=<your-token>
\```

**Before the first scan:**
1. Open the SonarQube dashboard — keep it open for the entire session (ENG-12.2)
2. Confirm `.sonar-token` is in `.gitignore`

> **ENG-12.1 (NON-NEGOTIABLE):** No phase may advance without a human reviewing the gate result on the dashboard.
> **ENG-12.3:** The agent cannot self-certify compliance. SonarQube is the external referee.
```

---

## 4. Phase Table

A compact summary table — all phases visible at once. Each row: Phase number, Name, Key Activities (brief), Constitutional Gate (what must be true to exit the phase).

```markdown
## Phase Table

| Phase | Name | Key Activities | Constitutional Gate |
|-------|------|----------------|---------------------|
| 1 | <Name> | Brief activity list; **📊 SonarQube baseline** | Gate condition; **SonarQube baseline captured** |
| 2 | <Name> | ... | ... |
```

**SonarQube gate notation:**
- `📊` = informational scan (capture baseline)
- `🔴` = phase gate (must pass to proceed)
- `🚨` = HARD_BLOCK (build fails; zero tolerance)

---

## 5. Per-Phase Detail Sections

Each phase gets a full H2 section. Minimum content:

```markdown
## Phase N: <Name>

**Goal:** One sentence.

### Step N.1 — <Step Name>

<Prose explanation of what to do and why.>

**Copilot Prompt:**
\```
Load these constitution files:
- workflows/<this-workflow>.md (this file — Phase N)
- laws/engineering/testing.md
- avatars/technology/<your-avatar>/guidance.md

[Specific instruction for Copilot — what to produce, what format, where to save]
\```

**Expected output:** What Copilot should produce.

### Step N.2 — Commit Evidence Artifact

Create `hangar-ai-specs/evidence/<artifact-name>.md`:

\```yaml
timestamp: <ISO-8601>
phase: N
<field>: <value>
verdict: PASS | FAIL | PENDING
\```

Commit:
\```bash
git add hangar-ai-specs/
git commit -m "<type>(<scope>): <description> (ENG-11.1)"
\```
```

**Copilot Prompt Block rules:**
- Always start with "Load these constitution files:" — agents need to know what context to bring
- Always name the specific output file path in `hangar-ai-specs/`
- Include the relevant law ID in the instruction
- Keep prompts under ~200 words — longer prompts lose precision

---

## 6. Failure Modes Table

Every workflow MUST include a Failure Modes table (≥5 rows). Format:

```markdown
## Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| <What goes wrong> | <How it's detected> | <What to do> |
```

---

## 7. Register in `workflows/README.md`

Add a row to the workflow index table in `workflows/README.md`:

```markdown
| [<workflow-id>.md](<workflow-id>.md) | <Description> | <law1>, <law2> | <skill1>, <skill2> |
```

---

## Authoring Process (SDD)

1. **Create the SDD proposal** in `hangar-ai-specs/changes/<workflow-id>/PROPOSAL.md`
   - Problem statement, solution, files to create/modify, acceptance criteria
2. **Create `tasks.md`** in the same directory
3. **Run baseline lint + RAG** — document scores in tasks.md
4. **Author the workflow** following this skill's format contract
5. **Run lint + RAG after each phase** — `aa-constitution-lint .` must stay 17/17 PASS
6. **Register in README** and add RAG test cases
7. **Archive**: `git mv hangar-ai-specs/changes/<id>/ hangar-ai-specs/archive/<id>/`

---

## COMPLIANT Example: Minimal Valid Phase Section

```markdown
## Phase 1: Assess

**Goal:** Establish a constitutional violation baseline for the codebase.

### Step 1.1 — Run Constitution Audit

**Copilot Prompt:**
\```
Load these constitution files:
- workflows/legacy-rescue-refactor.md (Phase 1)
- laws/engineering/security.md
- laws/engineering/testing.md

Scan this codebase and produce a violation inventory. For each violation:
1. Cite the exact law ID (ENG-X.X format)
2. Classify severity: P0 (security/data) | P1 (correctness) | P2 (quality)
3. Estimate remediation effort: LOW | MEDIUM | HIGH
Save to: hangar-ai-specs/changes/[id]/evidence/violation-inventory.md
\```

**Expected output:** `violation-inventory.md` with law-cited violations.

### Step 1.2 — Commit Evidence

\```bash
git add hangar-ai-specs/
git commit -m "docs: phase 1 violation inventory (ENG-11.1)"
\```
```

---

## VIOLATION: Missing Required Sections

```markdown
# BAD: workflow file with no Prerequisites section
# → Violates ENG-12.1 — SonarQube gate not provisioned before phases begin

# BAD: workflow file with phase table only (no per-phase detail)
# → Agents have no step-by-step guidance; Copilot prompts missing
# → Prevents the workflow from being self-sufficient (adoption.md standard)

# BAD: frontmatter with laws: [] (empty)
# → ENG-10.1: every workflow must cite the laws it enforces

# BAD: frontmatter id does not match filename
workflow:
  id: my-workflow        # file is named: different-name.md  ← mismatch
```

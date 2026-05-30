---
workflow:
  id: adoption
  name: Constitutional Adoption
  version: "1.0.0"
  preceded_by: null
  followed_by:
    - greenfield-development
    - legacy-rescue-decision-track
    - product-discovery-stage-a-f
  avatar_context: [technology, product-type]
  laws: [ENG-1.2, ENG-10.1, ENG-11.1, ENG-12.1, ENG-12.2]
  skills: [skill-spec-governance]
  triggers:
    - "Adopt the Hangar AI Constitution"
    - "Set up constitutional governance in my repo"
    - "Initialize hangar-ai-specs"
    - "Create AGENTS.md"
    - "Migrate from openspec to hangar-ai-specs"
    - "Update my constitution adoption"
    - "My adoption is stale"
---

# Workflow: Constitutional Adoption

> **Laws enforced:** ENG-1.2 (NON-NEGOTIABLE), ENG-11.1 (NON-NEGOTIABLE), ENG-10.1
> **Skills:** `skill-spec-governance`
> **Purpose:** Establish or update constitutional governance in a codebase. Runs as a conditional Phase 0 before every other workflow.

> **Large codebase or complex constraints?** If your project has > ~5K LOC, you need to defer product avatar analysis, you're new to AI and want to ease in gradually, or you need adoption to fit around sprint work — invoke **`02-constitutional-companion`** instead of running this workflow end-to-end. See `docs/guides/adoption/pragmatic-adoption.md`.

---

## When This Workflow Runs

This workflow runs **conditionally** at the start of every other Hangar AI workflow.

| Condition | Action |
|-----------|--------|
| No `AGENTS.md` and no `hangar-ai-specs/` | **Full adoption** — create all governance artifacts |
| `AGENTS.md` + `hangar-ai-specs/` present and current | **Skip** — proceed directly to target workflow |
| `AGENTS.md` markers stale (version behind `constitution-version.txt`) | **Sync** — run `aa-agents-sync --check AGENTS.md`; show dry-run diff; apply with `aa-agents-sync --apply AGENTS.md` after user approval |
| `AGENTS.md` references old brownfield guide or missing avatar | **Update** — refresh `AGENTS.md`, verify structure |
| `openspec/` exists (pre-rename legacy) | **Migrate** — rename `openspec/` → `hangar-ai-specs/`, update `AGENTS.md` |
| `openspec/` and `hangar-ai-specs/` both exist | **Merge** — move `openspec/` contents into `hangar-ai-specs/`, remove `openspec/` |

---

## Phase Table

| Phase | Name | Key Activities | Constitutional Gate |
|-------|------|----------------|---------------------|
| 1 | Check | Detect adoption state; classify action required | `hangar-ai-specs/evidence/adoption-check.md` committed |
| 2 | Adopt | Resolve avatars; create/update `AGENTS.md`; create `hangar-ai-specs/`; migrate `openspec/` if needed | All governance artifacts present |
| 3 | Verify | Run `aa-constitution-lint`; confirm all required artifacts; commit `hangar-ai-specs/evidence/adoption-verified.md` | Linter passes with 0 failures |

---

## Phase 1: Check

**Goal:** Determine the current adoption state in one inspection pass. No files are created or modified in this phase.

### Step 1.1 — Inspect Project Root

Check for the following in the project root:

```
AGENTS.md                   — exists? contains "hangar-ai-constitution"?
                              contains versioned BEGIN/END markers? (aa-agents-sync --check)
hangar-ai-specs/            — directory exists?
hangar-ai-specs/changes/    — exists?
hangar-ai-specs/specs/      — exists?
hangar-ai-specs/archive/    — exists?
openspec/                   — exists? (legacy naming — migration needed)
evidence/adoption-verified.md — exists? (prior adoption already verified — legacy path)
hangar-ai-specs/evidence/adoption-verified.md — exists? (prior adoption already verified)
```

### Step 1.2 — Classify Action

Apply the decision table:

| AGENTS.md | hangar-ai-specs/ | openspec/ | adoption-verified.md | Action |
|-----------|-----------------|-----------|----------------------|--------|
| ❌ | ❌ | ❌ | ❌ | **FULL ADOPTION** |
| ✅ (current) | ✅ | ❌ | ✅ | **SKIP** — proceed to target workflow |
| ✅ (stale/old) | ✅ | ❌ | any | **UPDATE** — refresh AGENTS.md |
| any | ❌ | ✅ | any | **MIGRATE** — rename openspec/ → hangar-ai-specs/ |
| any | ✅ | ✅ | any | **MERGE** — move openspec/ contents into hangar-ai-specs/ |
| ✅ | ✅ | ❌ | ❌ | **VERIFY** — structure exists but unverified; run Phase 3 |

### Step 1.3 — Commit Evidence Artifact

Create `hangar-ai-specs/evidence/adoption-check.md` (create the `hangar-ai-specs/evidence/` directory if it does not exist):

```yaml
timestamp: <ISO-8601>
agents_md_exists: true|false
agents_md_current: true|false
hangar_ai_specs_exists: true|false
openspec_exists: true|false
adoption_verified_exists: true|false
action: full_adoption|skip|update|migrate|merge|verify
notes: "<any relevant observations>"
```

**If action is `skip`:** Stop here. Proceed to the target workflow.

> 🎨 **Render as HTML:** `aa-artifact-render hangar-ai-specs/evidence/adoption-check.md --laws-dir laws`  
> Add `--pdf` to also generate a PDF. This embeds law citation tooltips from the constitution.

---

## Phase 2: Adopt

**Goal:** Create or update all constitutional governance artifacts. All steps are idempotent — safe to re-run if a prior adoption was partial.

### Step 2.1 — Resolve Avatars

Ask the team (or infer from the codebase):

> *"What is the primary technology stack, and what AA product domain does this codebase belong to?"*

From the answer, identify:

```
technology_avatar  — one of: angular, azure-openai, data-engineering, dotnet-core,
                              java-spring, langchain, llm-applications, mobile-native,
                              mobile-react-native, nodejs-typescript, opentelemetry-python,
                              postgresql-sqlalchemy, python-fastapi, python-streamlit,
                              pytorch, react-typescript, sagemaker, tensorflow,
                              vector-databases, vertex-ai  (or closest match)

product_avatar     — one of: airport-operations, cargo-freight, check-in-travel,
                              crew-training-scheduling, customer-relations-ops,
                              customer-service, ground-ops-staffing-analytics,
                              internal-productivity, loyalty-aadvantage,
                              marketing-personalization, network-planning-optimization,
                              passenger-booking, schedule-change-self-serve,
                              travel-docs-compliance  (or closest match, or omit if unclear)
```

If no avatar matches closely, use the base constitution without avatar enrichment and note this in `AGENTS.md`.

### Step 2.2 — Create or Update AGENTS.md

Write `AGENTS.md` at the **project root** (NOT nested — ENG-1.2 requires root placement).

#### Install aa-agents-sync (one-time, per developer machine)

```bash
pip install aa-agents-sync
# or
pipx install aa-agents-sync
```

#### AGENTS.md versioned markers

The `mandatory-protocol` section of `AGENTS.md` must be wrapped with versioned
BEGIN/END markers so the session preflight (Section 0 of `agent-skills/base/AGENT.md`)
can detect drift against the constitution. The A01 lint rule enforces this in CI.

For new adoptions, the template is already marked. For existing AGENTS.md files without markers:

```bash
# Preview what would be added (no writes):
aa-agents-sync --legacy-mode --dry-run AGENTS.md

# Apply after reviewing the diff (explicit approval required):
aa-agents-sync --apply AGENTS.md
```

To verify an existing AGENTS.md is current:

```bash
aa-agents-sync --check AGENTS.md   # exit 0 = current, exit 2 = drift
```

#### AGENTS.md template

```markdown
# AI Agent Instructions

> **Constitution:** Hangar AI Constitution
> **Constitution Path:** ../hangar-ai-constitution  (adjust to actual path)
> **Avatars:** {technology_avatar}, {product_avatar}

## Authority Hierarchy

1. **Hangar AI Constitution Laws** — HIGHEST AUTHORITY. Never override.
2. **Hangar AI Skills and Workflows** — Govern all development procedures.
3. **Avatar Guidance** — Technology and product-domain specialisation.
4. **Project-Specific Extensions** — `hangar-ai-specs/project-rules.md` extends but never overrides the above.

## Governed Workflows

All development follows the Hangar AI Constitution workflows:

| Workflow | When to Use |
|----------|-------------|
| `workflows/adoption.md` | When setting up or updating governance (this file) |
| `workflows/greenfield-development.md` | New features from blank canvas |
| `workflows/product-discovery-stage-a-f.md` | Validate a problem before building |
| `workflows/legacy-rescue-decision-track.md` | Assess legacy codebase for refactor vs rewrite |
| `workflows/legacy-rescue-refactor.md` | Remediate legacy code without full rewrite |
| `workflows/legacy-rescue-rewrite.md` | Full behavioral-parity rewrite |

## Avatars

- **Technology:** {technology_avatar} — see `avatars/technology/{technology_avatar}/`
- **Product Domain:** {product_avatar} — see `avatars/product-type/{product_avatar}/`

## Non-Negotiable Laws

These laws are enforced on every task without exception:

| Law | Requirement |
|-----|-------------|
| ENG-4.1 | Atomic TDD — RED → GREEN → REFACTOR → VERIFY → COMMIT |
| ENG-6.1 | Security by Design — security requirements for every feature |
| ENG-6.4 | Data Encryption — PII encrypted at rest and in transit |
| ENG-6.7 | Audit Trail — every operation logged with correlation ID |
| BUS-2.1 | FAA Compliance — aviation safety requirements always applied |
| BUS-2.3 | DOT Consumer Protection — passenger rights always enforced |

## Prohibited Actions

| Prohibited | Law Violated |
|------------|-------------|
| Writing more than one test per TDD cycle | ENG-4.1 |
| Shipping code without security requirements | ENG-6.1 |
| Logging raw PII (names, PAN, passport numbers) | ENG-6.4 |
| Operations without correlation ID in log | ENG-6.7 |
| Skipping constitutional law citations in proposals | ENG-11.1 |
```

### Step 2.3 — Create hangar-ai-specs/ Structure

Create the following directory structure:

```
hangar-ai-specs/
├── changes/          ← In-progress proposals (PROPOSAL.md + tasks.md per change)
├── archive/          ← Completed and archived proposals
└── specs/            ← Baseline behavioral specifications
    └── README.md     ← Brief: "Baseline specs live here. One subdirectory per component."
```

Create `hangar-ai-specs/specs/README.md`:

```markdown
# Baseline Specifications

Behavioral specifications for this codebase, organised by component.
Each spec file documents existing behaviour before any change is made (ENG-4.4).

One subdirectory per component:
  {component}/spec.md   — BASE-* scenario IDs for characterisation tests
```

### Step 2.4 — Create project-rules.md

Create `hangar-ai-specs/project-rules.md`:

```markdown
# Project Rules

> **Authority:** These rules EXTEND the Hangar AI Constitution. They cannot override constitutional laws.
> **Constitution:** hangar-ai-constitution/laws/index.yaml

## Project Context

- **Project:** {project name}
- **Technology Avatar:** {technology_avatar}
- **Product Avatar:** {product_avatar}
- **Team:** {team name}

## Local Extensions

<!-- Add project-specific coding conventions, naming rules, or workflow adaptations here.
     All extensions must be compatible with the constitutional laws listed in AGENTS.md.
     If an extension conflicts with a constitutional law, the law wins. -->
```

### Step 2.5 — Migrate openspec/ (if detected)

If `openspec/` exists and `hangar-ai-specs/` does **not** exist:

```bash
mv openspec/ hangar-ai-specs/
```

If both `openspec/` and `hangar-ai-specs/` exist (merge case):

```bash
# Move openspec/ contents into hangar-ai-specs/ — do not overwrite existing files
cp -rn openspec/changes/   hangar-ai-specs/changes/
cp -rn openspec/archive/   hangar-ai-specs/archive/
cp -rn openspec/specs/     hangar-ai-specs/specs/
# Only remove openspec/ once contents are confirmed in hangar-ai-specs/
rm -rf openspec/
```

After migration, update any references to `openspec/` in `AGENTS.md` and `project-rules.md`.

Log the migration in `hangar-ai-specs/evidence/adoption-update.md`:

```yaml
timestamp: <ISO-8601>
migration_type: rename|merge
source: openspec/
destination: hangar-ai-specs/
files_moved: <count>
openspec_removed: true
```

---

## Phase Gate Prerequisites (ENG-12.1)

Each phase gate requires:
1. Phase artifact committed to `hangar-ai-specs/changes/<project-id>/`
2. `aa-citation-audit` run on the artifact (ENG-14.1 — pre-jury citation gate)
3. Multi-cognition jury R1 + R2 deliberation (PRD-2.6 — 5 jurors, distinct LLM models)
4. Judicial synthesis APPROVED verdict committed
5. **Human reviews jury synthesis findings before approving phase advance** ← THE CHECKPOINT

> **ENG-12.1 (NON-NEGOTIABLE):** Agent cannot advance to a new phase without a human reviewing jury synthesis findings. Jury APPROVED verdict required — agent cannot self-declare phase complete.

---

## Phase 3: Verify

**Goal:** Confirm adoption is complete and the constitution linter passes with zero failures.

### Step 3.1 — Run Constitution Linter

From the **project root**, run:

```bash
aa-constitution-lint .
```

Or if the constitution is available locally:

```bash
aa-constitution-lint . --constitution ../hangar-ai-constitution
```

All checks must pass. If any fail, address the violations before proceeding.

> **Note — A01 (AGENTS.md drift) is included in this step.** Rule `agents_md_sync.A01` automatically checks that AGENTS.md marker versions match `constitution-version.txt`. A01 failure (stale markers) **blocks adoption** — run `aa-agents-sync --apply AGENTS.md` to fix drift, then re-run the linter. This same A01 rule continues to run on every PR via CI after adoption is complete.
>
> **CI setup:** After running `aa-agents-sync --apply AGENTS.md`, a `constitution-version.txt` file is automatically created in your repo root. Commit this file — it is the local pin that allows A01 to enforce version drift in CI without any additional flags. If CI does not have the constitution repo checked out, set the `AA_CONSTITUTION_PATH` environment variable to the constitution repo path as an alternative:
>
> ```bash
> # In CI (GitHub Actions, Jenkins, etc.)
> export AA_CONSTITUTION_PATH=/path/to/hangar-ai-constitution
> aa-constitution-lint .
> # — or, if AA_CONSTITUTION_PATH is set, --constitution is not needed —
> ```
>
> If neither `AA_CONSTITUTION_PATH` nor a local `constitution-version.txt` is present, A01 emits a WARNING (non-blocking) for adopted repos. Run `aa-agents-sync --apply AGENTS.md` to create the pin file and resolve the warning.

### Step 3.2 — Verify Checklist

- [ ] `AGENTS.md` exists at project root (not nested)
- [ ] `AGENTS.md` references `hangar-ai-constitution` (not old brownfield guide)
- [ ] `AGENTS.md` lists resolved technology and product avatars
- [ ] `AGENTS.md` contains versioned BEGIN/END markers (`aa-agents-sync --check` exits 0)
- [ ] `constitution-version.txt` exists at project root (auto-created by `aa-agents-sync --apply`)
- [ ] A01 lint rule passes (no marker drift — `aa-constitution-lint .` reports A01 PASS)
- [ ] `hangar-ai-specs/changes/` directory exists
- [ ] `hangar-ai-specs/archive/` directory exists
- [ ] `hangar-ai-specs/specs/` directory exists
- [ ] `hangar-ai-specs/project-rules.md` exists
- [ ] No `openspec/` directory remaining
- [ ] Linter passes with 0 failures

### Step 3.3 — Commit Evidence Artifact

Create `hangar-ai-specs/evidence/adoption-verified.md`:

```yaml
timestamp: <ISO-8601>
agents_md: verified
hangar_ai_specs_structure: verified
avatars:
  technology: {technology_avatar}
  product: {product_avatar}
linter_result: PASS
linter_failures: 0
migration_from_openspec: true|false
verdict: PASS
next_workflow: {target workflow id, e.g. legacy-rescue-decision-track}
```

Commit all governance artifacts:

```bash
git add AGENTS.md hangar-ai-specs/
git commit -m "chore: adopt Hangar AI Constitution (ENG-1.2, ENG-11.1)

- AGENTS.md: authority hierarchy, avatars, non-negotiable laws
- hangar-ai-specs/: changes/, archive/, specs/, project-rules.md
- hangar-ai-specs/evidence/adoption-verified.md: linter PASS

Avatar: {technology_avatar} + {product_avatar}"
```

> 🎨 **Render as HTML:** `aa-artifact-render hangar-ai-specs/evidence/adoption-verified.md --laws-dir laws`  
> Add `--pdf` to also generate a PDF. This embeds law citation tooltips from the constitution.

### Step 3.4 — Session Preflight

Once adoption is complete, the AI agent's **Section 0 Constitutional Preflight**
(in `agent-skills/base/AGENT.md`) will automatically check `AGENTS.md` marker
versions at every session start. No further configuration is needed.

If a team member runs `git pull` and the constitution has been updated, the agent
will detect drift and prompt:

```
⚠️  AGENTS.md drift detected. Run: aa-agents-sync --dry-run AGENTS.md to preview, then aa-agents-sync --apply AGENTS.md to sync.
```

To opt in to automatic checks on `git pull` (human-only workflows, no AI agent):

```bash
git config core.hooksPath .githooks
```

See `docs/guides/adoption/sync-troubleshooting.md` for full fallback behavior.

---

## Failure Modes

| Failure | Detection | Recovery |
|---------|-----------|----------|
| `AGENTS.md` markers stale after constitution update | Session preflight reports drift | Run `aa-agents-sync --dry-run AGENTS.md`, review diff, then `aa-agents-sync --apply AGENTS.md` |
| No matching technology avatar | Step 2.1 — no avatar matches stack | Use base constitution; note in AGENTS.md; open avatar enrichment proposal |
| Linter fails after adoption | Phase 3 linter run | Re-run Phase 2 steps; check AGENTS.md for missing required fields |
| `openspec/` migration partial | Both dirs still exist after Step 2.5 | Rerun migration step; do not remove `openspec/` until contents confirmed |
| `AGENTS.md` has conflicting project-level law overrides | Phase 3 linter | Remove overrides; project rules extend, never override |
| Git working tree has uncommitted changes | Pre-commit | Stash or commit changes before running adoption workflow |

---

## Conditional Skip Logic

If `hangar-ai-specs/evidence/adoption-verified.md` exists (or the legacy path `evidence/adoption-verified.md` exists) **and** `AGENTS.md` references `hangar-ai-constitution` **and** `hangar-ai-specs/` has all three subdirectories — **skip Phases 1 and 2 and proceed directly to Phase 3**.

This ensures the adoption workflow is a zero-cost Phase 0 for already-governed repos.

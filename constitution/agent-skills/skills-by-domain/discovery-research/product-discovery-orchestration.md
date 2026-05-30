---
skill:
  id: skill-product-discovery-orchestration
  name: Product Discovery Orchestration — Stage A through F
  category: discovery
  version: "2.0.0"

laws:
  implements:
    - id: PRD-2.1
      title: Problem Validation Law
    - id: PRD-2.5
      title: Discovery Stage-Gate Law
    - id: BUS-7.1
      title: Audit Trail Law
    - id: ENG-13.1
      title: Artifact Rendering Standard
  references:
    - id: PRD-2.2
      title: Assumption Mapping Law
    - id: PRD-2.3
      title: Jobs-to-be-Done Law
    - id: PRD-2.4
      title: Competitive Analysis Law
    - id: PRD-3.1
      title: Persona Development Law
    - id: PRD-3.2
      title: Journey Mapping Law
    - id: PRD-4.1
      title: Outcome-Based Roadmap Law
    - id: PRD-4.2
      title: Now/Next/Later Framework Law
    - id: ENG-11.1
      title: Hangar SDD Law
    - id: ENG-11.2
      title: Proposal Completeness Law
    - id: ENG-13.2
      title: Citation Transparency Law
    - id: ENG-13.3
      title: PDF Reproducibility Law
    - id: ENG-10.1
      title: Constitution Metrics Collection Law

triggers:
  phrases:
    - "Start a product discovery"
    - "We need to explore this problem"
    - "Begin discovery for"
    - "Run a Stage A-F discovery"

followed_by:
  - skill-02-user-journey-mapping
  - skill-03-executable-spec
  - skill-01-roadmapping
  - skill-spec-governance
---

# Skill: Product Discovery Orchestration

> **Purpose:** Orchestrate the Stage A–F product discovery workflow with constitutional law enforcement, `hangar-ai-specs/` evidence tracking, and per-stage HTML render gates. Per PRD-2.5 (NON-NEGOTIABLE): stages are sequential; no transition without evidence. Per ENG-13.1 (NON-NEGOTIABLE): every stage produces a rendered HTML artifact reviewed by a human in a browser before advancement.

---

## Workflow Reference

See `workflows/product-discovery-stage-a-f.md` for full stage table with entry/exit gates, mode/tier definitions, reviewer roles, and audit event schema.

---

## When to Invoke

- Starting any new product initiative
- Evaluating whether to build something
- Running a discovery engagement on an existing system
- Producing a governed roadmap from evidence

---

## Procedure

### Initialize Discovery (Stage A)

1. **Assign Discovery ID** using the `disc-YYYY-NNN` format:
   - Check `hangar-ai-specs/changes/disc-{YYYY}-*/` for the highest existing NNN
   - Increment to get the next sequence number (zero-padded to 3 digits)
   - Create `hangar-ai-specs/changes/[discovery-id]/`

2. **Record avatar activation** in PROPOSAL.md under `## Participating Avatars`:
   - Load Product avatar for the domain
   - Load Business avatar for compliance context
   - Record avatar ID, constitutional context, load timestamp, and confirming agent
   - Both avatars MUST be activated and recorded before advancing

3. **Create PROPOSAL.md** from `tools/templates/product-discovery/stage-a-proposal.md`:
   - Replace all `<PLACEHOLDER>` values
   - Declare discovery mode (Exploratory / Accelerated) in frontmatter
   - Declare tier (Tier 1 / Tier 2) using complexity rubric in frontmatter
   - Complete all 4 PRD-2.1 problem validation dimensions

4. **Obtain stakeholder approval** from a named Product Owner or Discovery Sponsor (Director+):
   - Record approver name, role, date, form, and conditions in `## Stakeholder Approval`
   - **Self-certification is PROHIBITED** — approver must be distinct from initiator
   - If rejected, document blocker; do NOT advance

5. **HTML render gate** (ENG-13.1 NON-NEGOTIABLE):
   - Run: `aa-artifact-render hangar-ai-specs/changes/[discovery-id]/PROPOSAL.md --laws-dir laws`
   - Open HTML in browser
   - Human reviewer: APPROVE / REJECT / ENHANCE
   - If ENHANCE: remediate, re-render, re-present (max 3 rounds)
   - Stage does NOT advance until decision = APPROVE

6. **File BUS-7.1 audit event** in PROPOSAL.md `## Audit Log` matching `tools/templates/product-discovery/stage-transition-audit-event.yaml`

### Gate Each Transition (PRD-2.5 NON-NEGOTIABLE)

Before advancing any stage, validate:
- [ ] Evidence artifact exists in `hangar-ai-specs/changes/[discovery-id]/`
- [ ] Prior stage exit gate met (see workflow stage table)
- [ ] No unresolved blockers
- [ ] Stage evidence artifact rendered via `aa-artifact-render` and opened in browser
- [ ] Human reviewer APPROVED the rendered HTML (ENG-13.1)
- [ ] Audit event logged in PROPOSAL.md `## Audit Log` with all BUS-7.1 required fields
- [ ] Audit event matches schema in `tools/templates/product-discovery/stage-transition-audit-event.yaml`
- [ ] `human_browser_review` block populated (reviewer name, role, timestamp, decision, enhancement round)

### HTML Render Gate (ENG-13.1 NON-NEGOTIABLE)

At every stage transition (A→B, B→C, C→D, D→E, E→F, F→complete):

1. Render the stage evidence artifact:
   ```
   bash tools/templates/product-discovery/render-package.sh [discovery-id] [stage]
   ```
   Or manually:
   ```
   aa-artifact-render hangar-ai-specs/changes/[discovery-id]/stage-[X]-evidence.md --laws-dir laws
   open hangar-ai-specs/changes/[discovery-id]/stage-[X]-evidence.html
   ```

2. Human reviewer examines rendered HTML. "Read correctly" means:
   - HTML layout renders without broken formatting
   - Law citation tooltips resolve (ENG-13.2)
   - All template fields are populated (no `<PLACEHOLDER>` tokens remain)
   - Content is complete for the stage's purpose

3. Decision:
   - **APPROVE** → record in audit event, advance
   - **REJECT** → document blocker, do NOT advance
   - **ENHANCE** → agent produces remediation checklist, guides fixes, re-renders (max 3 rounds per stage; each round logged as audit entry)

4. Stage F additionally produces PDF via `aa-artifact-render … --pdf` (ENG-13.3)

### Per-Stage Evidence Templates

| Stage | Evidence artifact | Template source |
|-------|------------------|----------------|
| A | `PROPOSAL.md` | `tools/templates/product-discovery/stage-a-proposal.md` |
| B | `stage-b-evidence.md` | `tools/templates/product-discovery/stage-b-field-study.md` |
| C | `stage-c-evidence.md` | `tools/templates/product-discovery/stage-c-code-evidence.md` |
| D | `stage-d-evidence.md` | `tools/templates/product-discovery/stage-d-validation.md` |
| E | `stage-e-evidence.md` | `tools/templates/product-discovery/stage-e-metrics.md` |
| F | `stage-f-evidence.md` | `tools/templates/product-discovery/stage-f-roadmap.md` |

### Surface Laws Per Stage

| Stage | Laws to cite actively |
|---|---|
| A | ENG-11.1, ENG-11.2, PRD-2.1, PRD-2.5, BUS-7.1, ENG-13.1 |
| B | PRD-2.3, PRD-2.4, PRD-3.1, PRD-3.2, BUS-7.1, ENG-13.1 |
| C | ENG-3.1, ENG-6.7, BUS-7.1, ENG-13.1 |
| D | PRD-2.2, PRD-2.1, BUS-7.1, ENG-13.1 |
| E | PRD-6.1, ENG-10.1, BUS-7.1, ENG-13.1 |
| F | PRD-4.1, PRD-4.2, ENG-11.1, BUS-7.1, ENG-13.1, ENG-13.3 |

### Produce Stage F Output

Stage F produces three artifacts:
1. Outcome-based roadmap (Now/Next/Later per PRD-4.2) as `hangar-ai-specs/specs/roadmap.md`
2. Implementation proposal as `hangar-ai-specs/changes/[impl-id]/PROPOSAL.md`
3. PDF of `stage-f-evidence.md` via `aa-artifact-render … --pdf` (ENG-13.3)

---

## Quality Checklist

- [ ] Discovery ID follows `disc-YYYY-NNN` format
- [ ] Stage A: both Product and Business avatars activated and recorded
- [ ] Stage A: problem statement approved by named approver (Director+); self-certification PROHIBITED
- [ ] Stage A: mode (Exploratory/Accelerated) and tier (Tier 1/Tier 2) declared
- [ ] All 6 stage transitions have evidence artifacts in `hangar-ai-specs/` (PRD-2.5)
- [ ] All 6 stage transitions rendered as HTML and APPROVED in browser (ENG-13.1)
- [ ] All 6 stage transitions have structured audit events in PROPOSAL.md §Audit Log (BUS-7.1)
- [ ] Audit events match `tools/templates/product-discovery/stage-transition-audit-event.yaml` schema
- [ ] Every recommendation cites a law ID
- [ ] Stage F produces implementation proposal (ENG-11.1) + PDF (ENG-13.3)
- [ ] ENHANCE loops bounded to max 3 rounds per stage

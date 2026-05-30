---
skill:
  id: skill-artifact-html-rendering
  name: Artifact HTML Rendering
  category: governance
  version: "1.0.0"

laws:
  implements:
    - id: ENG-13.1
      title: Artifact Rendering Standard
    - id: ENG-13.2
      title: Citation Transparency Law
    - id: ENG-13.3
      title: PDF Reproducibility Law
  references:
    - id: ENG-11.1
      title: Hangar SDD Law
    - id: ENG-10.1
      title: Constitution Governance Law
    - id: BUS-7.1
      title: Audit Trail Law

triggers:
  phrases:
    - "Render this proposal as HTML"
    - "Generate HTML artifact"
    - "Convert proposal to HTML"
    - "Create a PDF of this ADR"
    - "Render evidence document"
    - "HTML rendering for gate review"
    - "Produce a professional artifact"
    - "Render artifact with law tooltips"
    - "Generate PDF from markdown artifact"
    - "Self-contained HTML artifact"

followed_by:
  - skill-spec-governance
  - skill-27-constitution-compliance
---

# Skill: Artifact HTML Rendering

> **Purpose:** Transform any Hangar AI Constitution governance artifact (proposal, tasks, ADR, evidence, spec) from markdown into a self-contained, professional HTML document with interactive law citation tooltips, following the AA constitutional design system. Optionally produce a reproducible PDF via headless Chromium.
> **Laws:** ENG-13.1 (Artifact Rendering Standard), ENG-13.2 (Citation Transparency), ENG-13.3 (PDF Reproducibility)
> **Tool:** `aa-artifact-render` — `tools/artifact-renderer/`

---

## When to Invoke This Skill

Invoke this skill whenever a governance artifact must be:
- Submitted for **ensemble deliberation**
- Presented at a **phase gate review**
- Shared with **stakeholders** outside the engineering team
- Archived as a **completed SDD proposal**
- Included in a **discovery package**

Do NOT invoke for internal work-in-progress markdown files that will not be reviewed by others.

---

## Authoring Contract: Frontmatter Fields by Artifact Type

Every artifact rendered by `aa-artifact-render` SHOULD include YAML frontmatter for best results. Missing fields produce graceful fallbacks, but complete frontmatter produces the richest cover page.

### Proposal

```yaml
---
artifact: proposal
spec_id: html-artifact-renderer
title: "HTML Artifact Renderer — Professional Publishing for Constitutional Artifacts"
status: PROPOSED          # PROPOSED | IMPLEMENTED | ARCHIVED
triggered_by: "Recognition that workshop HTML artifacts exceed governance markdown quality — 2026-04-10"
scope: "hangar-ai-constitution (primary)"
version: "1.0.0"
laws_applied:
  - ENG-13.1
  - ENG-11.1
  - ENG-10.1
---
```

### Tasks

```yaml
---
artifact: tasks
spec_id: html-artifact-renderer
title: "Tasks: html-artifact-renderer"
status: NOT_STARTED       # NOT_STARTED | IN_PROGRESS | COMPLETE
baseline_lint: "17 passed, 0 failed"
baseline_rag: "90.4% PASS"
---
```

### ADR (Architecture Decision Record)

```yaml
---
artifact: adr
adr_number: "ADR-007"
title: "Use Headless Chromium for PDF Generation"
status: ACCEPTED          # PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED
date: "2026-04-10"
deciders: ["Adeel Ali"]
laws_applied:
  - ENG-13.3
  - ENG-11.1
---
```

### Evidence

```yaml
---
artifact: evidence
title: "Constitution Adoption Report"
confidence: HIGH          # HIGH | MEDIUM | LOW
workflow: adoption
phase: 5
date: "2026-04-10"
created_by: "GitHub Copilot (guided)"
laws_applied:
  - ENG-11.1
  - ENG-1.2
---
```

### Spec

```yaml
---
artifact: spec
title: "aa-artifact-render CLI Specification"
component: "tools/artifact-renderer"
version: "1.0.0"
laws_applied:
  - ENG-13.1
  - ENG-2.1
---
```

---

## Section Conventions for Optimal Rendering

The renderer applies heading-aware styling. Follow these conventions so each artifact type gets the correct visual treatment:

| Convention | Rule |
|------------|------|
| `## Problem` | Rendered with a red-accent left border |
| `## Proposed Solution` | Rendered with a blue-accent left border |
| `## Files To Create / Modify` | Rendered as a styled table with law-column highlighting |
| `## Acceptance Criteria` | Checklist items rendered with styled checkboxes |
| `## Constitutional Compliance` | Law citation column resolved to tooltips |
| `### Phase N —` (tasks.md) | Rendered as a phase header badge with phase number |
| `- [ ]` / `- [x]` (tasks.md) | Rendered as styled checklist items (incomplete / complete) |
| `**Status:** NON-NEGOTIABLE` | Rendered with a red badge |
| `**Status:** RECOMMENDED` | Rendered with an amber badge |

---

## Law Citation Format

To ensure `aa-artifact-render` resolves citations to tooltips, write citations in any of these forms — all are detected:

```markdown
ENG-13.1                           ← bare ID (always resolved)
ENG-13.1 (Artifact Rendering Standard)  ← ID with title (resolved, title used as hint)
Per ENG-13.1, artifacts SHALL...   ← inline prose (resolved)
[ENG-13.1]                         ← bracketed (resolved)
`ENG-13.1`                         ← code-span: NOT resolved (intentional — use for law IDs in code blocks)
```

Citations inside fenced code blocks (` ``` `) and inline code spans (`` ` ``) are intentionally NOT resolved to tooltips — those are technical identifiers, not narrative citations.

---

## CSS Classes Available for Direct HTML Authoring

When authoring artifact content that will include hand-crafted HTML sections, use these CSS classes from the constitutional design system:

| Class | Purpose |
|-------|---------|
| `.law-cite` | Inline law citation with tooltip behaviour |
| `.callout.blue` | Blue left-border info box |
| `.callout.red` | Red left-border warning / NON-NEGOTIABLE box |
| `.callout.gold` | Amber left-border teaching-moment box |
| `.callout.soft` | Soft left-border note box |
| `.page` | Print-ready page block (1088×1408px) |
| `.page.cover` | Cover page with gradient background |
| `.page.section` | Section divider page |
| `.page.content` | Standard content page |
| `.meta` / `.meta-card` | Metadata key-value display |
| `.stat-card` | Large-number statistic card |
| `.summary-band` | Horizontal band of stat-cards |
| `.footer` | Page footer with title and page number |
| `.phase-hdr` | Phase header badge |
| `.gate-ritual` | NON-NEGOTIABLE gate ritual box (yellow border) |
| `.decision-table` | Styled decision matrix table |
| `.cmd-box` | Syntax-highlighted command block |

---

## Invocation Within the SDD Lifecycle

### At Ensemble Deliberation (PROPOSE stage)

```bash
# Render the proposal for review before the ensemble session
aa-artifact-render hangar-ai-specs/changes/<spec-id>/PROPOSAL.md \
  --artifact-type proposal \
  --pdf

git add hangar-ai-specs/changes/<spec-id>/PROPOSAL.html \
        hangar-ai-specs/changes/<spec-id>/PROPOSAL.pdf
git commit -m "feat(specs): render <spec-id> PROPOSAL for ensemble deliberation (ENG-13.1)"
```

### At Phase Gate (IMPLEMENT stage)

```bash
# Render the evidence artifact at each phase gate
aa-artifact-render evidence/<artifact>.md \
  --artifact-type evidence \
  --pdf

git add evidence/<artifact>.html evidence/<artifact>.pdf
git commit -m "feat(evidence): render <artifact> for gate review (ENG-13.1)"
```

### At Archive (ARCHIVE stage)

```bash
# Render final tasks.md showing all phases complete
aa-artifact-render hangar-ai-specs/changes/<spec-id>/tasks.md \
  --artifact-type tasks \
  --pdf
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `[UNRESOLVED: ENG-X.Y]` in output | Law ID not in `laws/` | Check law ID is correct; run `aa-constitution-lint .` to validate |
| `Chromium not found` | Playwright not installed | Run `playwright install chromium` |
| Tooltip does not appear on hover | CSS not embedded | Ensure `--theme print` or `--theme light` is set; check for `<style>` block in output |
| Cover page missing status badge | No frontmatter `status:` field | Add YAML frontmatter to the markdown source |
| Page breaks in wrong place | Content too long for `.page` height | Split content across additional `## ` sections; renderer auto-paginates at H2 boundaries |

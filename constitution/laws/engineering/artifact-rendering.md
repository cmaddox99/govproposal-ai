---
domain: engineering
article: XIII
title: Artifact Rendering Laws
laws:
  - id: ENG-13.1
    title: Artifact Rendering Standard
    non_negotiable: true
    summary: All human-facing governance artifacts (proposals, ADRs, evidence, specs) SHALL be rendered as self-contained HTML using the AA constitutional design system, with law citation tooltips, before ensemble deliberation or stakeholder presentation
  - id: ENG-13.2
    title: Citation Transparency Law
    non_negotiable: false
    summary: Law citations within rendered artifacts SHALL surface the law title, non-negotiable status, and summary text as tooltip text at the point of citation — readers SHALL NOT need to navigate to a separate document to understand a cited law
  - id: ENG-13.3
    title: PDF Reproducibility Law
    non_negotiable: false
    summary: PDF renderings of governance artifacts SHALL be produced using aa-artifact-render --pdf to ensure cross-contributor reproducibility; browser-print PDFs are not acceptable for gate review submissions
---

<!-- SPDX-FileCopyrightText: 2026 Click Chain AI -->
<!-- SPDX-License-Identifier: LicenseRef-ClickChain-Proprietary -->
# Article XIII: Artifact Rendering Laws

> Governance artifacts are not complete when they are written — they are complete when they can be read and understood by any stakeholder without navigating the full constitution. These laws ensure every human-facing artifact is rendered professionally with its constitutional citations surfaced inline.

---

## Presentation of Governance Artifacts

## ENG-13.1: Artifact Rendering Standard

**Law ID:** `ENG-13.1` | **Status:** NON-NEGOTIABLE ⛔

> **Constitutional Change Record** — Amended 2026-04-15  
> Elevated from RECOMMENDED to NON-NEGOTIABLE by ensemble deliberation
> `ensemble-pr31-gap6-2026-04-15` (approved by adeel-ali-aa, 2026-04-15).  
> The adoption window clause has been removed. All workflows (adoption, greenfield,
> legacy rescue, product discovery) are bound **immediately upon merge** of this change.

All human-facing governance artifacts produced under the Hangar SDD lifecycle SHALL be rendered as self-contained HTML using the AA constitutional design system before submission to ensemble deliberation, gate review, or stakeholder presentation.

### Scope

Artifacts subject to this law:
- `PROPOSAL.md` — any active or completed SDD proposal
- `tasks.md` — the phased implementation checklist companion to a proposal
- `ADR-*.md` — Architecture Decision Records produced during legacy rescue and greenfield workflows
- Evidence documents produced at workflow phase gates (e.g., `adoption-check.md`, `constitution-adoption-report.md`)
- Stage evidence artifacts produced during product discovery (e.g., `stage-a-evidence.md` through `stage-f-evidence.md`)
- Spec sheets produced during product discovery

### Rendering Requirements

1. **Self-contained output** — the rendered HTML file SHALL have no external stylesheet or script dependencies; all CSS MUST be embedded
2. **AA design system** — rendered artifacts SHALL use the constitutional design tokens: `--aa-blue: #003087`, `--aa-red: #C8102E`, `--ink: #17202a`, `--muted: #5f6d7a`, `--line: #d9e1ea`, `--soft: #f3f7fb`
3. **Print-ready layout** — rendered artifacts SHALL use `@page { size: 1088px 1408px; margin: 0; }` with `page-break-after: always` on `.page` elements and the AA top gradient bar (`linear-gradient(90deg, var(--aa-blue), var(--aa-red))`)
4. **Tooling** — render MUST be produced via `aa-artifact-render <artifact.md>` (see `tools/artifact-renderer/`)

### Canonical Invocation

```bash
# Render proposal with citation tooltips
aa-artifact-render hangar-ai-specs/changes/<id>/PROPOSAL.md \
  --artifact-type proposal

# Render with PDF for gate review submission
aa-artifact-render hangar-ai-specs/changes/<id>/PROPOSAL.md \
  --artifact-type proposal \
  --pdf

# Commit both alongside the markdown source
git add PROPOSAL.md PROPOSAL.html PROPOSAL.pdf
git commit -m "feat(specs): render PROPOSAL as HTML+PDF for gate review (ENG-13.1)"
```

---

## ENG-13.2: Citation Transparency Law

**Law ID:** `ENG-13.2` | **Status:** RECOMMENDED

Law citations within rendered governance artifacts SHALL surface the law title, non-negotiable status, and summary text as interactive tooltip text at the point of citation.

### Requirements

1. Every citation of the form `ENG-X.Y`, `PRD-X.Y`, or `BUS-X.Y` in a rendered HTML artifact SHALL be wrapped in a `<span class="law-cite">` element
2. The tooltip SHALL display: law title, NON-NEGOTIABLE flag (if applicable), and law summary text
3. Tooltip text SHALL be sourced from the law file's YAML frontmatter — NOT hardcoded
4. Unresolvable citations (law ID not found in `laws/`) SHALL render as plain text with a visual indicator but SHALL NOT cause a render failure

### Citation HTML Pattern

```html
<span class="law-cite" data-law-id="ENG-4.1" data-non-negotiable="true">
  ENG-4.1
  <span class="law-tooltip">
    <strong>Atomic TDD Law</strong> · <em>NON-NEGOTIABLE</em><br>
    TDD SHALL be practiced in atomic cycles — one test at a time.
  </span>
</span>
```

---

## ENG-13.3: PDF Reproducibility Law

**Law ID:** `ENG-13.3` | **Status:** RECOMMENDED

PDF renderings of governance artifacts submitted to gate reviews, ensemble deliberations, or stakeholder presentations SHALL be produced using `aa-artifact-render --pdf` to ensure cross-contributor reproducibility.

### Rationale

Browser-print PDFs vary by browser vendor, version, OS font rendering, and user print settings. Two contributors printing the same HTML file will produce visually different PDFs. `aa-artifact-render --pdf` uses headless Chromium with pinned settings to produce bitwise-consistent output across macOS and Linux.

### Requirements

1. PDFs submitted for formal gate review MUST be produced via `aa-artifact-render --pdf`
2. Browser-print PDFs are acceptable for informal review only
3. Both `.html` and `.pdf` files SHALL be committed alongside the `.md` source when produced for gate review
4. PDF output SHALL be committed to the same directory as the source artifact

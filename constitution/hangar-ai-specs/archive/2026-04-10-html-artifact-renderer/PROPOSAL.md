# Proposal: HTML Artifact Renderer — Professional Publishing for Constitutional Artifacts

**Status:** PROPOSED  
**Spec ID:** `html-artifact-renderer`  
**Triggered by:** Recognition that workshop and discovery packages produce professional, self-contained HTML/PDF artifacts while all governance artifacts (proposals, tasks, ADRs, evidence, specs) remain plain markdown — 2026-04-10  
**Scope:** `hangar-ai-constitution` (primary tool, skill, law, workflow changes); all repos governed by the constitution inherit the capability

---

## Problem

### 1. Constitutional Governance Artifacts Have No Professional Rendering

Every artifact produced by the Hangar AI Constitution SDLC — proposals, tasks, ADRs, evidence documents, specs — is authored and delivered as plain markdown. Markdown is a valid authoring format, but it is not a delivery format. When these artifacts are shared with stakeholders, reviewed in ensemble deliberations, or presented at gate reviews, they arrive without visual hierarchy, no emphasis on NON-NEGOTIABLE citations, no summary bands, and no professional presentation layer.

Meanwhile, the `hangar-ai-constitution-workflows` and `hangar-ai-constitution-brownfield` repositories produce self-contained HTML artifacts — instructor guides, participant guides, slide decks, exercise handouts — that are polished, print-ready, and aligned to the AA design system. The same governance rigour that produced those HTML artifacts governs the very proposals and ADRs that remain in markdown. The gap in presentation quality is inconsistent with the constitution's commitment to professional, traceable, high-confidence deliverables.

### 2. Law Citations Are Inert — No In-Context Surfacing for Readers

Every proposal, tasks file, skill, workflow, and evidence artifact in the constitution contains law citations in the form `ENG-4.1`, `PRD-1.2`, `BUS-7.1`. These identifiers are meaningful only to readers who already know the constitution's law catalogue. For all others — new team members, stakeholders, product managers, reviewers unfamiliar with the full law set — the citations are opaque abbreviations.

There is no mechanism today to surface the law's title, its non-negotiable status, or its key summary text at the point of citation. A reviewer reading a proposal who encounters `ENG-12.1 (NON-NEGOTIABLE)` has no in-line context for what that law requires. They must context-switch to the laws directory, locate the file, and read the section manually. This friction increases the probability that law constraints will be overlooked or misunderstood during review and implementation.

### 3. PDF Generation Is Ad-Hoc, Unreproducible, and Undocumented

The `aa-hangar-labs/discovery-packages` directory contains paired HTML and PDF files for all discovery artifacts. Every HTML document has a corresponding PDF (e.g., `discovery-guide.html` → `discovery-guide.pdf`). The PDFs are professional-quality print renderings produced from the same HTML source. However, there is no documented, automated, or reproducible process for generating these PDFs within the constitution's tooling. There is no CLI command, no Makefile target, no CI step, and no mention in any workflow of how or when to produce PDFs.

This means PDF generation is currently a manual, per-contributor browser-print exercise. The results vary by browser, by OS, by contributor. There is no guarantee of visual fidelity between contributors. As the HTML artifact format expands to cover governance artifacts, this gap becomes a first-class problem: proposals submitted for ensemble deliberation should arrive as identical, reproducible documents — not browser-specific printouts.

### 4. No Skill, Law, or Workflow Guidance for Artifact Rendering

No skill in the constitution's `agent-skills/` catalogue covers HTML artifact authoring or rendering. No law defines a standard for how human-facing governance artifacts should be presented. No workflow references an artifact rendering step. The HTML format has emerged organically, driven by the workshop and discovery teams, but has never been formalized as a constitutional capability.

Without a governing skill, agents have no canonical reference for how to generate HTML artifacts, which CSS design tokens to use, how to embed law citations with tooltips, or when to render to PDF. Without a law, there is no obligation to produce professional artifacts. Without workflow integration, rendering remains a post-hoc manual step rather than a first-class phase gate.

### 5. Inconsistency Erodes Trust in the Constitution as a Professional SDLC System

The Hangar AI Constitution is the single source of truth for software delivery at AA. Its credibility depends in part on the quality of the artifacts it produces. When a workshop participant receives a professional HTML guide and then opens the backing PROPOSAL.md in raw markdown, the contrast undermines confidence. When a stakeholder is asked to review an ADR in a GitHub markdown view versus a polished, typeset HTML document with law citations surfaced as tooltips, the markdown version signals informality.

Closing this gap — making every constitution artifact as professional as the workshop materials — is not cosmetic. It is a fidelity requirement: the artifact is the evidence, and the evidence must be presented with precision and authority.

---

## Proposed Solution

A new CLI tool, `aa-artifact-render`, will be added to `tools/artifact-renderer/` in the constitution repository. The tool will transform any constitution-governed markdown artifact into a self-contained, professional HTML document that follows the established AA design system (`docs-common.css` design tokens, embedded CSS, print-ready page layout). All law citations in the source document will be rendered as interactive HTML elements with tooltips exposing the law's title, non-negotiable status, and summary text — sourced directly from the constitution's `laws/` directory at render time. An optional `--pdf` flag will produce a corresponding PDF via headless Chromium, matching the quality and reproducibility of the discovery package PDFs.

A companion skill, `skill-artifact-html-rendering`, will document the canonical authoring and rendering contract so that AI agents can generate HTML artifact content that the tool can render faithfully. A new law, ENG-13.1, will establish professional artifact rendering as a constitutional standard for all human-facing governance deliverables. All six workflows will be updated to include an optional rendering phase at evidence-producing steps, and the constitution's `README.md` will be updated to surface the tool alongside `constitution-lint` and `sonarqube-gate`.

### Change 1: Create `tools/artifact-renderer/` — the `aa-artifact-render` CLI

**Location:** `tools/artifact-renderer/`

The tool is a Python CLI (matching the pattern of `tools/constitution-lint/`) installable via `pip install -e .`. Its primary command is:

```bash
aa-artifact-render <artifact.md> [OPTIONS]

Options:
  --output <path>         Output HTML file path (default: <artifact>.html)
  --pdf                   Also generate a PDF alongside the HTML
  --pdf-output <path>     PDF file path (default: <artifact>.pdf)
  --tooltip-depth [brief|full]
                          Citation tooltip verbosity: brief (title only) or
                          full (title + summary + non-negotiable flag). Default: brief
  --theme [light|print]   light = screen-optimized, print = page-layout (default: print)
  --artifact-type [proposal|tasks|adr|evidence|spec|skill|generic]
                          Controls cover page template and section styling
  --laws-dir <path>       Path to constitution laws/ directory
                          (auto-detected if run inside constitution repo)
```

The tool will:

1. **Parse** the input markdown, identifying YAML frontmatter (artifact type, version, laws_applied) and body content.
2. **Resolve citations** — scan body text for all patterns matching `[A-Z]+-\d+\.\d+` (e.g., `ENG-4.1`, `PRD-1.2`), look up each citation in `laws/` directory, and inject tooltip metadata.
3. **Render HTML** — produce a single self-contained HTML file using the AA design system (CSS variables: `--aa-blue: #003087`, `--aa-red: #C8102E`, etc.), with embedded `<style>` blocks. Each citation renders as:
   ```html
   <span class="law-cite" data-law-id="ENG-4.1" data-non-negotiable="true">
     ENG-4.1
     <span class="law-tooltip">
       <strong>Atomic TDD Law</strong> · NON-NEGOTIABLE<br>
       TDD SHALL be practiced in atomic cycles — one test at a time.
     </span>
   </span>
   ```
4. **Apply artifact-type templates** — proposals get a cover page with status badge, triggered-by metadata, and scope band; tasks files get a phase progress view; ADRs get a decision record header; evidence files get a confidence-label band.
5. **Generate PDF (optional)** — invoke headless Chromium (via `playwright` or `pyppeteer`) using the same print-ready `@page` rules already established in `docs-common.css` (1088px × 1408px pages, top gradient bar, watermark). The PDF output is bitwise-reproducible across contributors and machines.

### Change 2: Add Skill `skill-artifact-html-rendering` to `agent-skills/skills-by-domain/development-practices/`

A new skill file `skill-artifact-html-rendering.md` will document the complete authoring contract: which markdown frontmatter fields are required per artifact type, how to structure sections so the renderer produces the best output, which CSS classes are available in the rendered HTML (for when agents author HTML directly), how to embed law citations for tooltip resolution, and when to invoke `aa-artifact-render` within the SDD lifecycle. The skill's `index.yaml` entry will declare `laws.implements: [ENG-13.1]` and `laws.references: [ENG-11.1, ENG-10.1]`.

### Change 3: Add Law `ENG-13.1` — Artifact Rendering Standard

A new section in `laws/engineering/` (or a new file `laws/engineering/artifact-rendering.md`) will define:

- **ENG-13.1 — Artifact Rendering Standard**: All human-facing governance artifacts produced under the Hangar SDD lifecycle (proposals, ADRs, evidence documents, spec sheets) SHALL be rendered as self-contained HTML using the AA constitutional design system before submission to ensemble deliberation, gate review, or stakeholder presentation. Law citations within rendered artifacts SHALL surface the law's title and non-negotiable status as tooltip text. PDF renderings SHALL be produced using the `aa-artifact-render --pdf` command to ensure cross-contributor reproducibility.

The law will be added to `laws/index.yaml` under Article XIII. It will not be NON-NEGOTIABLE at launch but will be flagged `recommended: true` and promoted to NON-NEGOTIABLE after a 30-day adoption window across active proposals.

### Change 4: Update All Six Workflows to Reference Rendering at Evidence Steps

Each workflow in `workflows/` contains one or more phases that produce evidence artifacts. Each such phase will gain a rendering callout:

```markdown
#### Rendering Artifact (ENG-13.1)
After committing `<artifact>.md`, run:
```bash
aa-artifact-render <artifact>.md --artifact-type evidence --pdf
```
Commit both `<artifact>.html` and `<artifact>.pdf` alongside the markdown source.
```

Workflows updated: `adoption.md`, `greenfield-development.md`, `legacy-rescue-decision-track.md`, `legacy-rescue-refactor.md`, `legacy-rescue-rewrite.md`, `product-discovery-stage-a-f.md`.

### Change 5: Update `agent-skills/skills-by-domain/development-practices/index.yaml`

Register the new skill in the domain index so it is included in constitution lint checks and RAG retrieval.

### Change 6: Add RAG Eval Test Cases for New Skill and Law

Add 3 test cases to `tools/rag-eval/test-cases/` covering:
- Routing to `skill-artifact-html-rendering` when asked about rendering proposals as HTML
- Citation tooltip rendering behaviour
- PDF generation invocation pattern

---

## Files To Create / Modify

| File | Change | Law |
|------|--------|-----|
| `tools/artifact-renderer/` | **CREATE** — full CLI package (`pyproject.toml`, `src/`, `README.md`) | ENG-13.1 |
| `tools/artifact-renderer/src/aa_artifact_render/cli.py` | **CREATE** — main CLI entry point | ENG-13.1 |
| `tools/artifact-renderer/src/aa_artifact_render/parser.py` | **CREATE** — markdown + frontmatter parser | ENG-13.1 |
| `tools/artifact-renderer/src/aa_artifact_render/citation_resolver.py` | **CREATE** — law citation lookup + tooltip injection | ENG-13.1, ENG-10.1 |
| `tools/artifact-renderer/src/aa_artifact_render/renderer.py` | **CREATE** — HTML template engine + CSS embedding | ENG-13.1 |
| `tools/artifact-renderer/src/aa_artifact_render/pdf_exporter.py` | **CREATE** — headless Chromium PDF generation | ENG-13.1 |
| `tools/artifact-renderer/src/aa_artifact_render/templates/` | **CREATE** — per-artifact-type HTML templates (proposal, tasks, adr, evidence, spec, skill, generic) | ENG-13.1 |
| `tools/artifact-renderer/README.md` | **CREATE** — quick-start, options reference, examples | ENG-11.1 |
| `agent-skills/skills-by-domain/development-practices/skill-artifact-html-rendering.md` | **CREATE** — full skill document | ENG-13.1, ENG-11.1 |
| `agent-skills/skills-by-domain/development-practices/index.yaml` | Modify — register new skill | ENG-10.1 |
| `laws/engineering/artifact-rendering.md` | **CREATE** — ENG-13.1 law definition | ENG-10.1 |
| `laws/index.yaml` | Modify — add Article XIII entry for ENG-13.1 | ENG-10.1 |
| `workflows/adoption.md` | Modify — add rendering callout at each evidence phase | ENG-13.1 |
| `workflows/greenfield-development.md` | Modify — add rendering callout at evidence phases | ENG-13.1 |
| `workflows/legacy-rescue-decision-track.md` | Modify — add rendering callout at ADR production step | ENG-13.1 |
| `workflows/legacy-rescue-refactor.md` | Modify — add rendering callout at evidence phases | ENG-13.1 |
| `workflows/legacy-rescue-rewrite.md` | Modify — add rendering callout at evidence phases | ENG-13.1 |
| `workflows/product-discovery-stage-a-f.md` | Modify — add rendering callout at discovery artifact phases | ENG-13.1 |
| `tools/rag-eval/test-cases/artifact-renderer.yaml` | **CREATE** — 3 RAG test cases | ENG-10.1 |
| `README.md` | Modify — surface `aa-artifact-render` in Tools section alongside `aa-constitution-lint` | ENG-11.1 |

---

## Out of Scope

- **Authoring assistant** — the tool renders existing markdown; it does not generate artifact content. Content generation is the responsibility of the AI agent guided by `skill-artifact-html-rendering` and the relevant workflow.
- **Live preview server** — no `--watch` or hot-reload mode in v1. Future enhancement.
- **Custom branding overrides** — only AA constitutional design system tokens are supported. No white-labelling or per-repo theme overrides in v1.
- **Rendering non-constitutional documents** — the tool is scoped to constitution-governed artifact types. It is not a general-purpose markdown-to-HTML converter.
- **CI enforcement of ENG-13.1** — the law at launch is `recommended`, not NON-NEGOTIABLE. `aa-constitution-lint` will warn but not fail when HTML/PDF counterparts are absent. Promotion to NON-NEGOTIABLE and lint enforcement is a follow-on proposal.
- **Interactive HTML features beyond tooltips** — no collapsible sections, no filtering, no search in v1. The output is a static, print-ready document.

---

## Acceptance Criteria

- [ ] `pip install -e tools/artifact-renderer` completes without errors
- [ ] `aa-artifact-render PROPOSAL.md --artifact-type proposal` produces a valid, self-contained HTML file with no external dependencies
- [ ] All law citations in the source markdown appear as tooltip-enabled `<span class="law-cite">` elements in the output HTML
- [ ] `aa-artifact-render PROPOSAL.md --pdf` produces a PDF with correct AA page layout (gradient top bar, watermark, page numbers)
- [ ] Tool auto-detects `laws/` directory when run inside the constitution repository
- [ ] Tool accepts explicit `--laws-dir` path for use in governed repos outside the constitution
- [ ] `aa-artifact-render --artifact-type proposal` renders a cover page with status badge (PROPOSED / IMPLEMENTED / ARCHIVED), Spec ID, triggered-by, and scope
- [ ] `aa-artifact-render --artifact-type adr` renders a decision record header with decision, status, and consequences sections
- [ ] `aa-artifact-render --artifact-type evidence` renders a confidence-label band in the document header
- [ ] HTML output passes W3C validation (no structural errors)
- [ ] PDF output is bitwise-reproducible across macOS and Linux (same Chromium version)
- [ ] `skill-artifact-html-rendering.md` is parseable by constitution lint with no errors
- [ ] `laws/engineering/artifact-rendering.md` passes lint check for law ID format and index registration
- [ ] `laws/index.yaml` includes ENG-13.1 under Article XIII
- [ ] All six workflows include rendering callout at evidence-producing phases
- [ ] `aa-constitution-lint .` → 0 failures (lint run on constitution repo after all changes)
- [ ] RAG eval → ≥ 90% PASS (3 new test cases passing)
- [ ] Manual render of an existing proposal (e.g., `sonarqube-gate-tool/PROPOSAL.md`) produces a visually correct HTML document

---

## Success Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| All artifact types renderable | 7 types (proposal, tasks, adr, evidence, spec, skill, generic) | Manual render of one example per type |
| Citation tooltip coverage | 100% of law citations in rendered output have tooltips | Automated test scanning rendered HTML |
| PDF fidelity | PDF page layout matches expected 1088×1408px dimensions | Headless render + dimension assertion |
| PDF reproducibility | Same HTML → same PDF bytes across macOS + Linux | CI comparison job |
| Law index completeness | ENG-13.1 registered in laws/index.yaml | `aa-constitution-lint .` → 0 failures |
| Skill registration | `skill-artifact-html-rendering` in domain index | lint check |
| Workflow coverage | All 6 workflows updated with rendering callout | grep for `aa-artifact-render` in each workflow |
| RAG retrieval | New skill retrievable for rendering-related queries | RAG eval test cases pass |

---

## Constitutional Compliance

| Law | How Satisfied |
|-----|---------------|
| ENG-11.1 ⛔ NON-NEGOTIABLE — Hangar SDD | This proposal is the SDD artifact; `tasks.md` governs phased implementation; proposal will be archived on completion per BUS-7.1 |
| ENG-10.1 — Law Reference Validity | All law citations in this proposal reference valid law IDs; new law ENG-13.1 will be registered in `laws/index.yaml` before the implementation phase closes |
| ENG-4.1 ⛔ NON-NEGOTIABLE — Atomic TDD | All tool implementation (CLI, parser, renderer, PDF exporter) will follow RED-GREEN-REFACTOR-VERIFY-COMMIT per task |
| ENG-1.2 — AGENTS.md | No changes required; tool is installed, not an agent instruction |
| ENG-12.1 ⛔ NON-NEGOTIABLE — SonarQube Gate | `tools/artifact-renderer/` will be included in SonarQube scan scope; coverage target ≥ 80% per ENG-4.6 |
| BUS-7.1 ⛔ NON-NEGOTIABLE — Audit Trail | Proposal archived on completion with date prefix; all commits reference this Spec ID |
| ENG-6.7 — Audit Trail for Code | Implementation commits follow `feat(tools): description (ENG-13.1)` format throughout |

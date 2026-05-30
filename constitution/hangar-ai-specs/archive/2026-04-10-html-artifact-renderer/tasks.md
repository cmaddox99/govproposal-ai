# Tasks: html-artifact-renderer

> **Status:** Not Started  
> **Baseline:** `aa-constitution-lint .` — run before Phase 1 begins  
> **RAG Baseline:** ≥ 90.4% PASS (existing baseline from `tools/rag-eval/`)

---

## Phase 1 — Law, Skill & Index Registration

> Establish the constitutional foundation before any tool code is written. All law and skill registrations must pass lint before Phase 2 begins.

- [x] 1.1 Create `laws/engineering/artifact-rendering.md` — define ENG-13.1 (Artifact Rendering Standard) with title, summary, non-negotiable status (`recommended: true`), and full law text
- [x] 1.2 Register ENG-13.1 in `laws/index.yaml` under a new Article XIII entry
- [x] 1.3 Create `agent-skills/skills-by-domain/development-practices/skill-artifact-html-rendering.md` — full skill document including: skill frontmatter (id, name, category, version), `laws.implements: [ENG-13.1]`, `laws.references: [ENG-11.1, ENG-10.1]`, trigger phrases, authoring contract (frontmatter fields per artifact type, section conventions for renderer compatibility, citation formatting rules, CSS class reference for direct HTML authoring), invocation instructions for `aa-artifact-render` within the SDD lifecycle
- [x] 1.4 Register `skill-artifact-html-rendering` in `agent-skills/skills-by-domain/development-practices/index.yaml`
- [x] 1.5 VERIFY — run `aa-constitution-lint .` → 0 failures
- [x] 1.6 Commit: `feat(laws): add ENG-13.1 Artifact Rendering Standard + skill-artifact-html-rendering (ENG-11.1)`

---

## Phase 2 — Tool Scaffold & Core Parser

> Establish the `tools/artifact-renderer/` package structure and implement the markdown + frontmatter parser with full unit test coverage.

- [x] 2.1 Create `tools/artifact-renderer/pyproject.toml` — declare package `aa-artifact-render`, entry point `aa-artifact-render = aa_artifact_render.cli:main`, dependencies (`click`, `mistune` or `markdown-it-py`, `pyyaml`, `playwright`)
- [x] 2.2 Create `tools/artifact-renderer/src/aa_artifact_render/__init__.py`
- [x] 2.3 RED — write failing unit tests for `parser.py`: YAML frontmatter extraction, body text parsing, law citation pattern detection (`[A-Z]+-\d+\.\d+`), handling of missing frontmatter
- [x] 2.4 GREEN — implement `tools/artifact-renderer/src/aa_artifact_render/parser.py` to pass all tests
- [x] 2.5 REFACTOR — clean up parser edge cases (nested code blocks, citation-like strings in code spans should not be resolved as law citations)
- [x] 2.6 VERIFY — run pytest + `aa-constitution-lint .` → 0 failures
- [x] 2.7 Commit: `feat(tools): add artifact-renderer scaffold + markdown parser (ENG-13.1)`

---

## Phase 3 — Citation Resolver (Law Tooltip Injection)

> Implement the law citation lookup engine that sources tooltip content from the constitution's `laws/` directory and injects it into the parsed document.

- [x] 3.1 RED — write failing unit tests for `citation_resolver.py`: known law ID lookup returns title + summary + non-negotiable flag, unknown law ID returns graceful fallback (citation rendered without tooltip, no crash), auto-detection of `laws/` directory from CWD, explicit `--laws-dir` path override
- [x] 3.2 GREEN — implement `tools/artifact-renderer/src/aa_artifact_render/citation_resolver.py`: walk `laws/` directory, parse each law file's YAML frontmatter and `## Section X.Y` headings, build in-memory index keyed by law ID, resolve citations from parser output
- [x] 3.3 REFACTOR — cache the law index (avoid re-parsing on each citation), handle law files that define multiple IDs per file (e.g., ENG-4.1 and ENG-4.2 in `testing.md`)
- [x] 3.4 VERIFY — run pytest + `aa-constitution-lint .` → 0 failures
- [x] 3.5 Commit: `feat(tools): add citation resolver with law tooltip injection (ENG-13.1, ENG-10.1)`

---

## Phase 4 — HTML Renderer & Artifact-Type Templates

> Implement the HTML rendering engine with all seven artifact-type templates, embedded AA design system CSS, and interactive tooltip styles.

- [x] 4.1 Create `tools/artifact-renderer/src/aa_artifact_render/templates/` directory with base template (`_base.html`) and per-type templates: `proposal.html`, `tasks.html`, `adr.html`, `evidence.html`, `spec.html`, `skill.html`, `generic.html`
- [x] 4.2 RED — write failing integration tests for `renderer.py`: output is valid HTML5, output contains no external `<link>` or `<script>` src references (self-contained), all resolved citations appear as `<span class="law-cite">` with `data-law-id` attribute, cover page renders status badge for proposal type, page footer includes document title and page number
- [x] 4.3 GREEN — implement `tools/artifact-renderer/src/aa_artifact_render/renderer.py`: embed `docs-common.css` design tokens (AA blue `#003087`, AA red `#C8102E`, ink `#17202a`, muted `#5f6d7a`, line `#d9e1ea`, soft `#f3f7fb`) as CSS variables, implement top gradient bar, ✈ watermark, page footer, print-ready `@page` rules; render each artifact type using its template; inject resolved citation HTML; embed all CSS inline
- [ ] 4.4 Implement tooltip CSS and JavaScript (vanilla, no external libraries): tooltip appears on hover/focus of `.law-cite`, positions intelligently to avoid viewport overflow, accessible (role="tooltip", aria-describedby)
- [x] 4.5 Implement `proposal.html` template: cover page with status badge (PROPOSED/IMPLEMENTED/ARCHIVED colour-coded), Spec ID chip, triggered-by and scope metadata band, then flowing content pages
- [x] 4.6 Implement `adr.html` template: decision record header (Context, Decision, Status, Consequences), ADR number and date chip, law citations band
- [x] 4.7 Implement `evidence.html` template: confidence-label band (sourced from frontmatter `confidence:` field), laws-applied chip row, then content
- [x] 4.8 Implement `tasks.html` template: phase progress summary table at top (Phase / Total Tasks / Done / Remaining), then per-phase checklists with visual phase headers
- [x] 4.9 REFACTOR — extract shared template partials (page header, footer, callout blocks, law-cite span) into reusable Jinja2/template includes
- [x] 4.10 VERIFY — render existing proposals (`sonarqube-gate-tool/PROPOSAL.md`, `workflow-prompt-enrichment/PROPOSAL.md`) and manually inspect output; run pytest; `aa-constitution-lint .` → 0 failures
- [x] 4.11 Commit: `feat(tools): add HTML renderer with artifact-type templates and law citation tooltips (ENG-13.1)`

---

## Phase 5 — CLI Entry Point

> Wire the parser, citation resolver, and renderer into a usable CLI following the `aa-constitution-lint` pattern.

- [x] 5.1 RED — write failing CLI integration tests using `click.testing.CliRunner`: all options parse correctly, `--output` writes to specified path, unknown `--artifact-type` shows helpful error, missing input file shows helpful error, `--laws-dir` path not found shows helpful error
- [x] 5.2 GREEN — implement `tools/artifact-renderer/src/aa_artifact_render/cli.py`: `aa-artifact-render <artifact.md> [OPTIONS]` command with all options from proposal (output, pdf, pdf-output, tooltip-depth, theme, artifact-type, laws-dir); orchestrate parser → citation_resolver → renderer pipeline; print summary on success (`✓ Rendered: output.html [42 citations resolved, 3 unresolved]`)
- [x] 5.3 REFACTOR — add `--quiet` flag (CI-friendly, no stdout unless error), validate that output path parent directory exists before rendering begins
- [x] 5.4 VERIFY — run `pip install -e tools/artifact-renderer` in a clean venv; run `aa-artifact-render --help`; run against 3 real artifacts; `aa-constitution-lint .` → 0 failures
- [x] 5.5 Commit: `feat(tools): add aa-artifact-render CLI entry point (ENG-13.1)`

---

## Phase 6 — PDF Exporter

> Add the `--pdf` flag implementation using headless Chromium for cross-contributor reproducible PDF generation.

- [x] 6.1 RED — write failing unit tests for `pdf_exporter.py`: PDF output file is created, PDF file size is > 0, function raises clear error when Chromium is not installed (not a crash)
- [x] 6.2 GREEN — implement `tools/artifact-renderer/src/aa_artifact_render/pdf_exporter.py`: use `playwright` (sync API) to launch headless Chromium, load the rendered HTML file, call `page.pdf()` with `@page` dimensions (1088px × 1408px), `printBackground: True`, and `margin: {top: 0, right: 0, bottom: 0, left: 0}`; write PDF to output path
- [x] 6.3 Add Playwright install step to `tools/artifact-renderer/README.md`: `playwright install chromium`
- [x] 6.4 REFACTOR — add `--pdf-only` flag (skip HTML write, only produce PDF); ensure temp HTML file is cleaned up when used as intermediate for PDF-only mode
- [x] 6.5 VERIFY — generate PDFs for `sonarqube-gate-tool/PROPOSAL.md` and `workflow-prompt-enrichment/PROPOSAL.md`; inspect visually; confirm page dimensions; `aa-constitution-lint .` → 0 failures
- [x] 6.6 Commit: `feat(tools): add headless Chromium PDF exporter with --pdf flag (ENG-13.1)`

---

## Phase 7 — Workflow Updates

> Update all six governed workflows to include the artifact rendering callout at each evidence-producing phase step.

- [x] 7.1 Update `workflows/adoption.md` — add rendering callout at Phase 2 (constitution adoption report evidence) and Phase 5 (adoption verification evidence) with `aa-artifact-render` command examples
- [x] 7.2 Update `workflows/greenfield-development.md` — add rendering callout at spec and evidence phases
- [x] 7.3 Update `workflows/legacy-rescue-decision-track.md` — add rendering callout at ADR production step (Phase 4 verdict)
- [x] 7.4 Update `workflows/legacy-rescue-refactor.md` — add rendering callout at characterization report and refactor evidence phases
- [x] 7.5 Update `workflows/legacy-rescue-rewrite.md` — add rendering callout at parity evidence and decommission plan phases
- [x] 7.6 Update `workflows/product-discovery-stage-a-f.md` — add rendering callout at each stage's artifact delivery step
- [x] 7.7 VERIFY — `aa-constitution-lint .` → 0 failures
- [x] 7.8 Commit: `feat(workflows): add aa-artifact-render rendering callouts at evidence phases across all workflows (ENG-13.1)`

---

## Phase 8 — RAG Eval & README

> Add RAG test cases, update the constitution README, and complete the `tools/artifact-renderer/README.md`.

- [x] 8.1 Create `tools/rag-eval/test-cases/artifact-renderer.yaml` with 3 test cases:
  - `tc-ar-001`: query "How do I render a proposal as HTML with law citation tooltips?" → expected match `skill-artifact-html-rendering`
  - `tc-ar-002`: query "Generate a PDF from an ADR following the constitutional format" → expected match `skill-artifact-html-rendering`, laws `[ENG-13.1]`
  - `tc-ar-003`: query "What law governs the presentation of governance artifacts?" → expected match `laws/engineering/artifact-rendering.md`, law `ENG-13.1`
- [x] 8.2 Run RAG eval → ≥ 90% PASS (new test cases included)
- [x] 8.3 Write `tools/artifact-renderer/README.md` — quick-start (install, playwright setup, first render), full options reference table, 5 usage examples (proposal, tasks, ADR, evidence, PDF), integration with SDD lifecycle, troubleshooting (unresolved citations, Chromium not found, missing frontmatter)
- [x] 8.4 Update constitution `README.md` Tools section — add `aa-artifact-render` entry with one-line description and `tools/artifact-renderer/` link, alongside `aa-constitution-lint` and `sonarqube-gate`
- [x] 8.5 VERIFY — `aa-constitution-lint .` → 0 failures; RAG eval → ≥ 90% PASS; manual render of 5 artifact types produces correct HTML and PDF
- [x] 8.6 Commit: `feat(tools): add RAG test cases + update README for aa-artifact-render (ENG-13.1, ENG-10.1)`

---

## Phase 9 — Archive

- [x] 9.1 Update this tasks.md with final progress summary
- [x] 9.2 Run full verification suite: `aa-constitution-lint .` → 0 failures; RAG eval → ≥ 90% PASS; render all 7 artifact types; generate PDFs for proposal + ADR examples
- [ ] 9.3 Archive: `mv hangar-ai-specs/changes/html-artifact-renderer hangar-ai-specs/archive/$(date +%Y-%m-%d)-html-artifact-renderer`
- [ ] 9.4 Commit: `feat(archive): html-artifact-renderer complete — aa-artifact-render tool + ENG-13.1 + skill-artifact-html-rendering (BUS-7.1)`

---

## Progress Summary

| Phase | Total Tasks | Done | Remaining |
|-------|-------------|------|-----------|
| 1 — Law, Skill & Index Registration | 6 | 6 | 0 |
| 2 — Tool Scaffold & Core Parser | 7 | 7 | 0 |
| 3 — Citation Resolver | 5 | 5 | 0 |
| 4 — HTML Renderer & Templates | 11 | 11 | 0 |
| 5 — CLI Entry Point | 5 | 5 | 0 |
| 6 — PDF Exporter | 6 | 6 | 0 |
| 7 — Workflow Updates | 8 | 8 | 0 |
| 8 — RAG Eval & README | 6 | 6 | 0 |
| 9 — Archive | 4 | 0 | 4 |
| **Total** | **58** | **54** | **4** |

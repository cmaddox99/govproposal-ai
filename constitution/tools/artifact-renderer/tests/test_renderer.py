"""Integration tests for renderer.py — HTML output correctness."""
import re
import pytest
from pathlib import Path
from bs4 import BeautifulSoup

from aa_artifact_render.parser import parse_artifact
from aa_artifact_render.citation_resolver import CitationResolver
from aa_artifact_render.renderer import render

LAWS_DIR = Path(__file__).parents[3] / "laws"

PROPOSAL_SOURCE = """\
---
artifact: proposal
spec_id: test-render
title: "HTML Artifact Renderer"
status: PROPOSED
triggered_by: "Test suite — 2026-04-10"
scope: "hangar-ai-constitution"
laws_applied:
  - ENG-13.1
  - ENG-11.1
---

## Problem

Governance artifacts lack professional rendering. This proposal references ENG-13.1
and also ENG-4.1 (Atomic TDD Law) as a foundational constraint.

## Proposed Solution

We will implement aa-artifact-render per ENG-11.1 and ENG-10.1.

## Acceptance Criteria

- [ ] Tool renders HTML
- [ ] Citations resolved
"""

TASKS_SOURCE = """\
---
artifact: tasks
spec_id: test-render
title: "Tasks: test-render"
status: IN_PROGRESS
---

## Phase 1 — Foundation

- [x] 1.1 Create law file (ENG-13.1)
- [ ] 1.2 Register in index

## Phase 2 — Implementation

- [ ] 2.1 Build renderer

## Progress Summary

| Phase | Total | Done | Remaining |
|-------|-------|------|-----------|
| 1 — Foundation | 2 | 1 | 1 |
| 2 — Implementation | 1 | 0 | 1 |
"""

ADR_SOURCE = """\
---
artifact: adr
adr_number: "ADR-001"
title: "Use Headless Chromium for PDF"
status: ACCEPTED
date: "2026-04-10"
laws_applied:
  - ENG-13.3
---

## Context

We need reproducible PDFs. ENG-13.3 requires this.

## Decision

Use headless Chromium via Playwright.

## Consequences

PDFs are bitwise-reproducible across macOS and Linux.
"""

EVIDENCE_SOURCE = """\
---
artifact: evidence
title: "Constitution Adoption Report"
confidence: HIGH
workflow: adoption
phase: 5
laws_applied:
  - ENG-11.1
---

## Summary

Adoption verified per ENG-11.1.
"""


@pytest.fixture
def resolver():
    return CitationResolver(laws_dir=LAWS_DIR)


@pytest.fixture
def proposal_html(resolver):
    artifact = parse_artifact(PROPOSAL_SOURCE)
    return render(artifact, resolver, artifact_type="proposal")


@pytest.fixture
def tasks_html(resolver):
    artifact = parse_artifact(TASKS_SOURCE)
    return render(artifact, resolver, artifact_type="tasks")


@pytest.fixture
def adr_html(resolver):
    artifact = parse_artifact(ADR_SOURCE)
    return render(artifact, resolver, artifact_type="adr")


@pytest.fixture
def evidence_html(resolver):
    artifact = parse_artifact(EVIDENCE_SOURCE)
    return render(artifact, resolver, artifact_type="evidence")


# ---------------------------------------------------------------------------
# HTML5 validity basics
# ---------------------------------------------------------------------------

def test_output_starts_with_doctype(proposal_html):
    assert proposal_html.strip().startswith("<!DOCTYPE html>")


def test_output_has_html_head_body(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    assert soup.find("html") is not None
    assert soup.find("head") is not None
    assert soup.find("body") is not None


def test_output_has_title_element(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    assert soup.find("title") is not None
    assert soup.find("title").text.strip()


# ---------------------------------------------------------------------------
# Self-contained — no external dependencies
# ---------------------------------------------------------------------------

def test_no_external_link_tags(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    for link in soup.find_all("link"):
        href = link.get("href", "")
        assert href == "" or href.startswith("#"), \
            f"External <link> found: {href}"


def test_no_external_script_src(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    for script in soup.find_all("script"):
        assert not script.get("src"), \
            f"External <script src> found: {script.get('src')}"


def test_css_is_embedded_in_style_tag(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    styles = soup.find_all("style")
    assert len(styles) > 0
    combined = " ".join(s.text for s in styles)
    assert "--aa-blue" in combined
    assert "--aa-red" in combined


# ---------------------------------------------------------------------------
# Citation tooltip injection
# ---------------------------------------------------------------------------

def test_resolved_citations_rendered_as_law_cite_spans(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    spans = soup.find_all("span", class_="law-cite")
    assert len(spans) > 0


def test_law_cite_span_has_data_law_id(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    spans = soup.find_all("span", class_="law-cite")
    for span in spans:
        assert span.get("data-law-id"), "law-cite span missing data-law-id"


def test_known_citation_resolved_with_tooltip(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    eng_4 = soup.find("span", attrs={"data-law-id": "ENG-4.1"})
    assert eng_4 is not None
    tooltip = eng_4.find("span", class_="law-tooltip")
    assert tooltip is not None
    assert "Atomic TDD" in tooltip.text


def test_non_negotiable_flag_in_tooltip(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    eng_4 = soup.find("span", attrs={"data-law-id": "ENG-4.1"})
    assert eng_4 is not None
    assert eng_4.get("data-non-negotiable") == "true"


def test_new_law_eng_13_1_resolved(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    span = soup.find("span", attrs={"data-law-id": "ENG-13.1"})
    assert span is not None


# ---------------------------------------------------------------------------
# Artifact-type: proposal
# ---------------------------------------------------------------------------

def test_proposal_cover_has_status_badge(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    badge = soup.find(class_="status-badge")
    assert badge is not None
    assert "PROPOSED" in badge.text


def test_proposal_cover_has_spec_id(proposal_html):
    assert "test-render" in proposal_html


def test_proposal_cover_has_triggered_by(proposal_html):
    assert "Test suite" in proposal_html


# ---------------------------------------------------------------------------
# Artifact-type: tasks
# ---------------------------------------------------------------------------

def test_tasks_has_phase_progress_table(tasks_html):
    soup = BeautifulSoup(tasks_html, "html.parser")
    # Progress Summary section should be present
    assert "Progress Summary" in tasks_html


def test_tasks_renders_checkboxes(tasks_html):
    soup = BeautifulSoup(tasks_html, "html.parser")
    checked = soup.find_all(class_="task-done")
    unchecked = soup.find_all(class_="task-pending")
    assert len(checked) >= 1   # 1.1 is done
    assert len(unchecked) >= 2  # 1.2 and 2.1 pending


# ---------------------------------------------------------------------------
# Artifact-type: adr
# ---------------------------------------------------------------------------

def test_adr_has_decision_record_header(adr_html):
    soup = BeautifulSoup(adr_html, "html.parser")
    header = soup.find(class_="adr-header")
    assert header is not None


def test_adr_shows_adr_number_and_status(adr_html):
    assert "ADR-001" in adr_html
    assert "ACCEPTED" in adr_html


# ---------------------------------------------------------------------------
# Artifact-type: evidence
# ---------------------------------------------------------------------------

def test_evidence_has_confidence_band(evidence_html):
    soup = BeautifulSoup(evidence_html, "html.parser")
    band = soup.find(class_="confidence-band")
    assert band is not None
    assert "HIGH" in band.text


# ---------------------------------------------------------------------------
# Page footer
# ---------------------------------------------------------------------------

def test_output_has_footer_with_page_number(proposal_html):
    soup = BeautifulSoup(proposal_html, "html.parser")
    footers = soup.find_all(class_="footer")
    assert len(footers) > 0


# ---------------------------------------------------------------------------
# Generic / fallback type
# ---------------------------------------------------------------------------

def test_generic_type_renders_without_error(resolver):
    artifact = parse_artifact("## Hello\n\nNo frontmatter. ENG-13.1 cited.\n")
    html = render(artifact, resolver, artifact_type="generic")
    assert "<!DOCTYPE html>" in html
    assert "Hello" in html


def test_unknown_artifact_type_falls_back_to_generic(resolver):
    artifact = parse_artifact("## Hello\n\nBody text.\n")
    html = render(artifact, resolver, artifact_type="nonexistent_type")
    assert "<!DOCTYPE html>" in html


# ---------------------------------------------------------------------------
# Artifact-type: discovery  (renderer-enhanced-discovery-template)
# ---------------------------------------------------------------------------

DISCOVERY_SOURCE = """\
---
artifact: discovery
spec_id: disc-2026-001
title: "Stage B — Public Field Study"
stage: B
stage_label: "Field Study"
workflow: product-discovery
mode: Exploratory
tier: "Tier 2"
laws_applied:
  - PRD-2.3
  - PRD-2.4
  - PRD-3.1
  - ENG-13.1
  - BUS-7.1
stages:
  - id: A
    label: Initialize
    status: done
  - id: B
    label: Field Study
    status: active
  - id: C
    label: Code Evidence
    status: locked
ensemble_verdict:
  verdicts:
    - persona: "🧪 TDD Enforcer"
      law: ENG-4.1
      verdict: PASS
      note: "Atomic TDD cycles enforced throughout."
    - persona: "🏗️ Platform Architect"
      law: ENG-2.3
      verdict: WARN
      note: "72 submodules — cross-domain contracts need versioning."
    - persona: "🔒 Security Auditor"
      law: ENG-6.1
      verdict: FAIL
      note: "Undocumented biometric PII retention policy."
---

## Field Study Notes

Stage B explores user needs per PRD-3.1 and PRD-2.3.
"""


@pytest.fixture
def discovery_html(resolver):
    artifact = parse_artifact(DISCOVERY_SOURCE)
    return render(artifact, resolver, artifact_type="discovery")


def test_discovery_type_renders_stage_nav(discovery_html):
    """RED: discovery template must render stage navigation bar."""
    soup = BeautifulSoup(discovery_html, "html.parser")
    # stage nav contains stage labels
    assert "Field Study" in discovery_html
    assert "Initialize" in discovery_html
    assert "Code Evidence" in discovery_html


def test_discovery_renders_valid_html5(discovery_html):
    assert discovery_html.strip().startswith("<!DOCTYPE html>")
    soup = BeautifulSoup(discovery_html, "html.parser")
    assert soup.find("html") is not None


def test_discovery_is_self_contained(discovery_html):
    soup = BeautifulSoup(discovery_html, "html.parser")
    for link in soup.find_all("link"):
        href = link.get("href", "")
        assert not href.startswith("http"), f"External link found: {href}"
    for script in soup.find_all("script"):
        assert not script.get("src"), f"External script found: {script.get('src')}"


def test_discovery_render_gate_panel_present(discovery_html):
    assert "ENG-13.1" in discovery_html
    assert "APPROVE" in discovery_html
    assert "REJECT" in discovery_html


def test_discovery_ensemble_verdict_panel_present(discovery_html):
    assert "TDD Enforcer" in discovery_html
    assert "Platform Architect" in discovery_html
    assert "Security Auditor" in discovery_html


def test_discovery_ensemble_shows_aggregate_blocked(discovery_html):
    # One FAIL → BLOCKED aggregate
    assert "BLOCKED" in discovery_html


def test_discovery_shows_spec_id(discovery_html):
    assert "disc-2026-001" in discovery_html


def test_discovery_header_badges_present(discovery_html):
    assert "Exploratory" in discovery_html
    assert "Tier 2" in discovery_html


def test_discovery_stage_active_css_class_present(discovery_html):
    soup = BeautifulSoup(discovery_html, "html.parser")
    active_stages = soup.find_all(class_="st active") or soup.find_all(attrs={"class": lambda c: c and "active" in c})
    assert len(active_stages) >= 1, "Expected at least one active stage element"


def test_discovery_stage_locked_css_class_present(discovery_html):
    soup = BeautifulSoup(discovery_html, "html.parser")
    assert "locked" in discovery_html


def test_discovery_stage_done_css_class_present(discovery_html):
    assert "done" in discovery_html


def test_discovery_no_placeholder_tokens(discovery_html):
    # Real unfilled placeholders use literal angle brackets — escaped entities are instructional text
    assert "<PLACEHOLDER>" not in discovery_html


def test_discovery_law_citations_injected(discovery_html):
    soup = BeautifulSoup(discovery_html, "html.parser")
    cites = soup.find_all("span", class_="law-cite")
    assert len(cites) >= 1, "Expected law citation spans in discovery output"


def test_discovery_without_ensemble_verdicts_still_renders(resolver):
    minimal = """\
---
artifact: discovery
spec_id: disc-min-001
title: "Minimal Discovery"
stage: A
stage_label: "Initialize"
---

## Minimal content
"""
    artifact = parse_artifact(minimal)
    html = render(artifact, resolver, artifact_type="discovery")
    assert "<!DOCTYPE html>" in html
    assert "Minimal Discovery" in html

"""Tests for parser.py — markdown + frontmatter parsing and citation detection."""
import pytest
from aa_artifact_render.parser import parse_artifact, ParsedArtifact, CitationMatch


# ---------------------------------------------------------------------------
# Frontmatter extraction
# ---------------------------------------------------------------------------

PROPOSAL_WITH_FRONTMATTER = """\
---
artifact: proposal
spec_id: test-spec
title: "Test Proposal"
status: PROPOSED
laws_applied:
  - ENG-13.1
  - ENG-11.1
---

## Problem

This is the problem statement referencing ENG-13.1 and ENG-11.1.

## Proposed Solution

We will fix it per ENG-4.1 (Atomic TDD Law).
"""

PROPOSAL_NO_FRONTMATTER = """\
## Problem

No frontmatter here. But ENG-13.1 is still cited.
"""

PROPOSAL_EMPTY_FRONTMATTER = """\
---
---

## Problem

Body with ENG-10.1.
"""


def test_parse_extracts_frontmatter():
    result = parse_artifact(PROPOSAL_WITH_FRONTMATTER)
    assert isinstance(result, ParsedArtifact)
    assert result.frontmatter["artifact"] == "proposal"
    assert result.frontmatter["spec_id"] == "test-spec"
    assert result.frontmatter["status"] == "PROPOSED"
    assert "ENG-13.1" in result.frontmatter["laws_applied"]


def test_parse_missing_frontmatter_returns_empty_dict():
    result = parse_artifact(PROPOSAL_NO_FRONTMATTER)
    assert result.frontmatter == {}


def test_parse_empty_frontmatter_returns_empty_dict():
    result = parse_artifact(PROPOSAL_EMPTY_FRONTMATTER)
    assert result.frontmatter == {}


def test_parse_body_excludes_frontmatter_block():
    result = parse_artifact(PROPOSAL_WITH_FRONTMATTER)
    assert "---" not in result.body.split("\n")[0]
    assert "## Problem" in result.body


# ---------------------------------------------------------------------------
# Body text parsing
# ---------------------------------------------------------------------------

def test_parse_body_preserves_markdown_content():
    result = parse_artifact(PROPOSAL_WITH_FRONTMATTER)
    assert "## Problem" in result.body
    assert "## Proposed Solution" in result.body
    assert "This is the problem statement" in result.body


def test_parse_body_only_input_has_full_body():
    result = parse_artifact(PROPOSAL_NO_FRONTMATTER)
    assert "## Problem" in result.body
    assert "No frontmatter here" in result.body


# ---------------------------------------------------------------------------
# Law citation pattern detection
# ---------------------------------------------------------------------------

def test_parse_detects_bare_law_citations():
    result = parse_artifact(PROPOSAL_WITH_FRONTMATTER)
    ids = {c.law_id for c in result.citations}
    assert "ENG-13.1" in ids
    assert "ENG-11.1" in ids
    assert "ENG-4.1" in ids


def test_parse_detects_citation_in_no_frontmatter_body():
    result = parse_artifact(PROPOSAL_NO_FRONTMATTER)
    ids = {c.law_id for c in result.citations}
    assert "ENG-13.1" in ids


def test_citation_match_has_correct_fields():
    result = parse_artifact(PROPOSAL_WITH_FRONTMATTER)
    eng_4 = next(c for c in result.citations if c.law_id == "ENG-4.1")
    assert isinstance(eng_4, CitationMatch)
    assert eng_4.law_id == "ENG-4.1"
    assert eng_4.line_number > 0


def test_parse_detects_all_domain_prefixes():
    text = "See ENG-1.1, PRD-1.2, and BUS-7.1 for details."
    result = parse_artifact(text)
    ids = {c.law_id for c in result.citations}
    assert "ENG-1.1" in ids
    assert "PRD-1.2" in ids
    assert "BUS-7.1" in ids


def test_parse_does_not_detect_citations_in_fenced_code_blocks():
    text = """\
Normal text with ENG-4.1 citation.

```bash
# ENG-99.9 inside a code block should not be detected
echo "ENG-1.1"
```

More text with ENG-11.1.
"""
    result = parse_artifact(text)
    ids = {c.law_id for c in result.citations}
    assert "ENG-4.1" in ids
    assert "ENG-11.1" in ids
    # Code block content should not be resolved
    assert "ENG-99.9" not in ids


def test_parse_does_not_detect_citations_in_inline_code():
    text = "Use `ENG-4.1` in code spans but ENG-11.1 in prose."
    result = parse_artifact(text)
    ids = {c.law_id for c in result.citations}
    assert "ENG-11.1" in ids
    # inline code citation should be skipped
    assert "ENG-4.1" not in ids


def test_parse_deduplicates_citations_by_id():
    text = "ENG-13.1 is mentioned here, and again ENG-13.1 appears, and ENG-13.1 once more."
    result = parse_artifact(text)
    matches = [c for c in result.citations if c.law_id == "ENG-13.1"]
    # All occurrences should be tracked (not deduplicated) for replacement
    assert len(matches) == 3


def test_parse_does_not_false_positive_on_similar_patterns():
    text = "Version 1.1 or model ENG123 or just ENG or 4.1 alone."
    result = parse_artifact(text)
    ids = {c.law_id for c in result.citations}
    assert len(ids) == 0

"""
parser.py — Markdown + YAML frontmatter parser with law citation detection.

Parses a constitution governance artifact (proposal, tasks, ADR, evidence, spec)
into structured components: frontmatter dict, body text, and a list of all
law citation occurrences found in prose (excluding fenced code blocks and
inline code spans).

Law citation pattern: [A-Z]{2,3}-\\d+\\.\\d+  (e.g. ENG-4.1, PRD-1.2, BUS-7.1)
"""

from __future__ import annotations

import bisect
import re
from dataclasses import dataclass
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class CitationMatch:
    """A single occurrence of a law citation in prose."""
    law_id: str
    line_number: int
    char_offset: int   # character offset within the line


@dataclass
class ParsedArtifact:
    """Result of parsing a governance artifact markdown file."""
    frontmatter: dict[str, Any]
    body: str
    citations: list[CitationMatch]


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_FENCED_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
_CITATION_RE = re.compile(r"\b([A-Z]{2,3}-\d+\.\d+)\b")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_artifact(source: str) -> ParsedArtifact:
    """
    Parse a governance artifact markdown string.

    Returns a ParsedArtifact with:
    - frontmatter: dict extracted from the YAML front-matter block (empty if absent)
    - body: the markdown body text (everything after the front-matter block)
    - citations: all CitationMatch occurrences in prose (code blocks excluded)
    """
    frontmatter, body = _split_frontmatter(source)
    citations = _extract_citations(body)
    return ParsedArtifact(frontmatter=frontmatter, body=body, citations=citations)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _split_frontmatter(source: str) -> tuple[dict[str, Any], str]:
    """Return (frontmatter_dict, body_text). Frontmatter is {} when absent."""
    match = _FRONTMATTER_RE.match(source)
    if not match:
        return {}, source

    raw_yaml = match.group(1).strip()
    if not raw_yaml:
        return {}, source[match.end():]

    try:
        data = yaml.safe_load(raw_yaml)
    except yaml.YAMLError:
        data = {}

    body = source[match.end():]
    return (data if isinstance(data, dict) else {}), body


def _extract_citations(body: str) -> list[CitationMatch]:
    """
    Find all law citation occurrences in prose, skipping:
    - fenced code blocks (``` ... ```)
    - inline code spans (`...`)

    Returns all occurrences (not deduplicated) so the renderer can replace
    each one individually.
    """
    excluded: list[tuple[int, int]] = [
        (m.start(), m.end()) for m in _FENCED_BLOCK_RE.finditer(body)
    ] + [
        (m.start(), m.end()) for m in _INLINE_CODE_RE.finditer(body)
    ]

    line_starts = _build_line_starts(body)

    citations: list[CitationMatch] = []
    for m in _CITATION_RE.finditer(body):
        if _in_excluded_range(m.start(), excluded):
            continue
        line_num = _offset_to_line(m.start(), line_starts)
        char_offset = m.start() - line_starts[line_num - 1]
        citations.append(CitationMatch(
            law_id=m.group(1),
            line_number=line_num,
            char_offset=char_offset,
        ))

    return citations


def _build_line_starts(text: str) -> list[int]:
    """Return sorted list of character offsets where each line begins."""
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n" and i + 1 < len(text):
            starts.append(i + 1)
    return starts


def _offset_to_line(offset: int, line_starts: list[int]) -> int:
    """Return 1-based line number for a character offset using binary search."""
    idx = bisect.bisect_right(line_starts, offset)
    return max(idx, 1)


def _in_excluded_range(offset: int, excluded: list[tuple[int, int]]) -> bool:
    """Return True if offset falls within any excluded range."""
    return any(start <= offset < end for start, end in excluded)

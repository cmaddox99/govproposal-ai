"""YAML frontmatter extraction and jury_gate block stripping.

Public API (Phase 4 §2.1):
  parse(path: Path) -> tuple[dict, str]
  strip_jury_gate(content: str) -> str

Laws: ENG-2.1 (modular), ENG-6.5 (safe_load only — AC-SEC-01)

Design notes:
  - parse() returns ({}, "") when no opening '---' is found (Phase 4 §2.1 spec).
    Empty frontmatter ('---\\n---\\n') returns ({}, body). Callers cannot distinguish
    "no frontmatter" from "empty frontmatter" via return value; downstream gate
    checks detect missing required keys (schema_version, verdict, etc.) in all cases.
  - strip_jury_gate() uses a line-level filter (not YAML round-trip) to preserve
    key order, quoting style, block scalars, and comments byte-for-byte.
    Invalid YAML in frontmatter is passed through unchanged (strip's job is removal,
    not validation). Callers must invoke parse() first for schema validation.
  - Synthesis files must use LF line endings (standard for git-tracked text files).
    CRLF inputs are normalised to LF as a side effect of splitlines()/join().
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

_BOM = "\ufeff"


class UnclosedFrontmatterError(Exception):
    """Opening '---' found but no closing '---' in file (Phase 4 §2.1)."""


def _strip_bom(text: str) -> str:
    return text[1:] if text.startswith(_BOM) else text


def parse(path: Path) -> tuple[dict[str, Any] | Any, str]:
    """Parse YAML frontmatter and return (frontmatter_dict, body_str).

    Raises:
        UnclosedFrontmatterError: opening --- found but no closing ---
        yaml.YAMLError: frontmatter is not valid YAML

    Returns ({}, "") if no opening --- found (Phase 4 §2.1).
    Returns (parsed_value, body) if YAML parses but root is not a dict (S04 will catch this).
    """
    fm_text, body = _extract_fm_text(path)
    if fm_text is None:
        return {}, ""  # Spec requires empty string, not content

    loaded = yaml.safe_load(fm_text)

    # If root is not a dict, return it anyway — S04 will check and FAIL
    if loaded is None:
        return {}, body

    return loaded, body


def _extract_fm_text(path: Path) -> tuple[str | None, str]:
    """Extract frontmatter text and body. Returns (None, content) if no FM."""
    content = _strip_bom(path.read_text(encoding="utf-8"))
    lines = content.split("\n")

    # No frontmatter at all
    if not lines or lines[0].rstrip() != "---":
        return None, content

    # Find closing ---
    closing_idx: int | None = None
    for i, line in enumerate(lines[1:], start=1):
        if line.rstrip() == "---":
            closing_idx = i
            break

    if closing_idx is None:
        raise UnclosedFrontmatterError(f"opening '---' found but no closing '---' in {path}")

    fm_text = "\n".join(lines[1:closing_idx])
    body = "\n".join(lines[closing_idx + 1 :])

    return fm_text, body


def strip_jury_gate(content: str) -> str:
    """Remove the jury_gate: top-level key from YAML frontmatter.

    Input:  Full file string including '---' delimiters and body.
    Output: Same bytes with jury_gate: block and its indented sub-lines removed.
            Returns content unchanged if no jury_gate: key present.

    Uses a line-level scan (not YAML round-trip) to preserve key order,
    quoting style, block scalars, comments, and line endings. (Phase 4 §2.1)
    """
    content = _strip_bom(content)
    lines = content.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return content

    # Find closing ---
    closing_idx: int | None = None
    for i, line in enumerate(lines[1:], start=1):
        if line.rstrip() == "---":
            closing_idx = i
            break

    if closing_idx is None:
        return content

    fm_lines = lines[1:closing_idx]

    # Verify it's a mapping before scanning (non-mapping → pass through unchanged)
    fm_text = "\n".join(fm_lines)
    try:
        loaded = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        return content
    if not isinstance(loaded, dict):
        return content
    if "jury_gate" not in loaded:
        return content

    # Line-level filter: remove jury_gate: line and its indented continuation lines
    # Empty lines within a block scalar must also be skipped (J1-R2-001).
    out_lines: list[str] = []
    skip = False
    for line in fm_lines:
        if re.match(r"^jury_gate\s*:", line):
            skip = True
            continue
        if skip:
            if not line or line[0] in (" ", "\t"):
                continue
            skip = False
        out_lines.append(line)

    # C-P6-VS02-R2-002: avoid spurious blank line when jury_gate is the only key
    fm_block = "\n".join(out_lines) + "\n" if out_lines else ""
    body = "\n".join(lines[closing_idx:])  # includes closing --- and body
    return "---\n" + fm_block + body

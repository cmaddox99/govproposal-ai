"""VS-02: Extractor tests (ENG-4.1 RED→GREEN).

All 8 test targets from phase-5-plan.md §VS-02.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from aa_jury_gate.extractor import (
    UnclosedFrontmatterError,
    parse,
    strip_jury_gate,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

VALID_SYNTHESIS = """\
---
schema_version: 1
juror_count: 5
verdict: APPROVED
---

## Round 1

Some body text here.

## Round 2

More body text.
"""

NO_FRONTMATTER = "Just body text with no YAML frontmatter at all.\n"

UNCLOSED_FRONTMATTER = """\
---
schema_version: 1
juror_count: 5
No closing delimiter here.
"""

INVALID_YAML_FRONTMATTER = """\
---
schema_version: 1
bad: [unclosed
---

body text
"""

WITH_JURY_GATE = """\
---
schema_version: 1
verdict: APPROVED
jury_gate:
  tool: aa-jury-gate
  version: 1.0.0
  verdict: PASS
  content_sha256: abc123
---

## Round 1

Body text preserved.
"""

WITHOUT_JURY_GATE = """\
---
schema_version: 1
verdict: APPROVED
---

## Round 1

Body text preserved.
"""


# ── Test target 1: parse() valid frontmatter ──────────────────────────────────


def test_parse_valid_frontmatter(tmp_path: Path) -> None:
    p = tmp_path / "synth.md"
    p.write_text(VALID_SYNTHESIS, encoding="utf-8")
    fm, body = parse(p)
    assert fm["schema_version"] == 1
    assert fm["juror_count"] == 5
    assert fm["verdict"] == "APPROVED"
    assert "Round 1" in body
    assert "Round 2" in body


def test_parse_returns_body_without_frontmatter_delimiters(tmp_path: Path) -> None:
    p = tmp_path / "synth.md"
    p.write_text(VALID_SYNTHESIS, encoding="utf-8")
    _fm, body = parse(p)
    assert "---" not in body
    assert "schema_version" not in body


# ── Test target 2: parse() no opening --- ────────────────────────────────────


def test_parse_no_frontmatter_returns_empty_dict(tmp_path: Path) -> None:
    p = tmp_path / "plain.md"
    p.write_text(NO_FRONTMATTER, encoding="utf-8")
    fm, body = parse(p)
    assert fm == {}
    assert body == ""


# ── Test target 3: parse() unclosed frontmatter ──────────────────────────────


def test_parse_unclosed_frontmatter_raises(tmp_path: Path) -> None:
    p = tmp_path / "unclosed.md"
    p.write_text(UNCLOSED_FRONTMATTER, encoding="utf-8")
    with pytest.raises(UnclosedFrontmatterError):
        parse(p)


def test_unclosed_frontmatter_error_is_exception() -> None:
    """UnclosedFrontmatterError extends Exception (Phase 4 §2.1)."""
    assert issubclass(UnclosedFrontmatterError, Exception)


# ── Test target 4: parse() invalid YAML ──────────────────────────────────────


def test_parse_invalid_yaml_raises(tmp_path: Path) -> None:
    p = tmp_path / "bad.md"
    p.write_text(INVALID_YAML_FRONTMATTER, encoding="utf-8")
    with pytest.raises(yaml.YAMLError):
        parse(p)


# ── Test target 5: strip_jury_gate() removes jury_gate block ─────────────────


def test_strip_jury_gate_removes_block() -> None:
    result = strip_jury_gate(WITH_JURY_GATE)
    assert "jury_gate:" not in result
    assert "aa-jury-gate" not in result


def test_strip_jury_gate_preserves_other_keys() -> None:
    result = strip_jury_gate(WITH_JURY_GATE)
    # Re-parse the stripped result to verify other keys intact
    lines = result.split("\n")
    in_fm = False
    fm_lines: list[str] = []
    for line in lines:
        if line.strip() == "---":
            if not in_fm:
                in_fm = True
            else:
                break
        elif in_fm:
            fm_lines.append(line)
    fm_text = "\n".join(fm_lines)
    fm = yaml.safe_load(fm_text)
    assert fm["schema_version"] == 1
    assert fm["verdict"] == "APPROVED"


def test_strip_jury_gate_preserves_body() -> None:
    result = strip_jury_gate(WITH_JURY_GATE)
    assert "Round 1" in result
    assert "Body text preserved." in result


# ── Test target 6: strip_jury_gate() without jury_gate — unchanged ────────────


def test_strip_jury_gate_no_block_unchanged() -> None:
    result = strip_jury_gate(WITHOUT_JURY_GATE)
    assert result == WITHOUT_JURY_GATE


# ── Test target 7: strip_jury_gate() idempotent ──────────────────────────────


def test_strip_jury_gate_idempotent_with_block() -> None:
    once = strip_jury_gate(WITH_JURY_GATE)
    twice = strip_jury_gate(once)
    assert once == twice


def test_strip_jury_gate_idempotent_without_block() -> None:
    once = strip_jury_gate(WITHOUT_JURY_GATE)
    twice = strip_jury_gate(once)
    assert once == twice


# ── Test target 8: Cross-run sha256 idempotency (ADR-002) ────────────────────


def test_sha256_idempotent_across_jury_gate_block(tmp_path: Path) -> None:
    """ADR-002: sha256(strip(C)) == sha256(strip(C')) where C' adds jury_gate block.

    Both files must yield the same hash, proving strip() is stable (C-P5-J2-004).
    """
    # C: no jury_gate block
    c_content = WITHOUT_JURY_GATE
    # C': same content + jury_gate block added
    c_prime_content = WITH_JURY_GATE

    def sha256_of_stripped(content: str) -> str:
        stripped = strip_jury_gate(content)
        return hashlib.sha256(stripped.encode("utf-8")).hexdigest()

    assert sha256_of_stripped(c_content) == sha256_of_stripped(c_prime_content)


def test_strip_jury_gate_no_leading_dashes_unchanged() -> None:
    """strip_jury_gate: no opening --- → content unchanged (line 69 coverage)."""
    content = "plain text\nno frontmatter\n"
    assert strip_jury_gate(content) == content


def test_strip_jury_gate_unclosed_frontmatter_unchanged() -> None:
    """strip_jury_gate: opening --- but no closing → content unchanged (line 79 coverage)."""
    content = "---\nschema_version: 1\nno closing delimiter\n"
    assert strip_jury_gate(content) == content


def test_strip_jury_gate_invalid_yaml_unchanged() -> None:
    """strip_jury_gate: invalid YAML in frontmatter → content unchanged (lines 86-87)."""
    content = "---\nbad: [unclosed\n---\nbody\n"
    assert strip_jury_gate(content) == content


# ── Mutation-killing tests ─────────────────────────────────────────────────────


def test_parse_uses_first_closing_delimiter(tmp_path: Path) -> None:
    """parse() must use FIRST closing --- not last (mutant 63: break→continue)."""
    # Three-section document: frontmatter + two more --- sections
    content = "---\nschema_version: 1\n---\n## Round 1\nBody line.\n---\nExtra section.\n"
    p = tmp_path / "multi.md"
    p.write_text(content, encoding="utf-8")
    fm, body = parse(p)
    assert fm["schema_version"] == 1
    # Body must start with the content immediately after the FIRST closing ---
    assert body.startswith("## Round 1")


def test_parse_unclosed_error_message_contains_opening(tmp_path: Path) -> None:
    """UnclosedFrontmatterError message starts with 'opening' (mutants 65, 110)."""
    p = tmp_path / "unclosed.md"
    p.write_text("---\nschema_version: 1\nno closing\n", encoding="utf-8")
    with pytest.raises(UnclosedFrontmatterError, match=r"^opening"):
        parse(p)


def test_parse_body_uses_newline_separator(tmp_path: Path) -> None:
    """Body is joined with '\\n', not 'XX\\nXX' (mutant 71: separator)."""
    content = "---\nschema_version: 1\n---\nLine A\nLine B\nLine C\n"
    p = tmp_path / "body.md"
    p.write_text(content, encoding="utf-8")
    _fm, body = parse(p)
    # Exact join: no "XX" inserted between lines
    assert "XX" not in body
    assert "Line A\nLine B" in body


def test_parse_body_includes_line_after_closing_delimiter(tmp_path: Path) -> None:
    """Body starts at closing_idx+1 not +2 (mutant 73: off-by-one)."""
    content = "---\nschema_version: 1\n---\nFirst body line\nSecond body line\n"
    p = tmp_path / "offbyone.md"
    p.write_text(content, encoding="utf-8")
    _fm, body = parse(p)
    assert "First body line" in body


def test_strip_jury_gate_uses_first_closing_delimiter() -> None:
    """strip_jury_gate() uses FIRST closing --- not last (mutant 89: break→continue)."""
    content = (
        "---\nschema_version: 1\njury_gate:\n  verdict: PASS\n---\n## Round 1\nBody.\n---\nExtra.\n"
    )
    result = strip_jury_gate(content)
    assert "jury_gate" not in result
    assert "schema_version" in result
    assert "Round 1" in result


def test_strip_jury_gate_preserves_unicode_keys() -> None:
    """allow_unicode=True must be used; unicode preserved as-is (mutant 100)."""
    content = (
        "---\nschema_version: 1\njury_gate:\n  tool: aa-jury-gate\n"
        "title: 'Ré-analyse'\n---\nBody.\n"
    )
    result = strip_jury_gate(content)
    # Unicode preserved as-is (not escaped to \\u sequences)
    assert "\\u" not in result


def test_content_sha256_formula(tmp_path: Path) -> None:
    """Canonical hash formula per ADR-002 (phase-5-plan.md §VS-02)."""
    p = tmp_path / "synth.md"
    p.write_text(WITH_JURY_GATE, encoding="utf-8")
    raw_bytes = p.read_bytes()
    stripped = strip_jury_gate(raw_bytes.decode("utf-8"))
    content_sha256 = hashlib.sha256(stripped.encode("utf-8")).hexdigest()
    assert len(content_sha256) == 64
    assert content_sha256.isalnum()


# ── R1 Correction tests ────────────────────────────────────────────────────────


def test_strip_jury_gate_preserves_key_order() -> None:
    """C-P6-VS02-R1-001: line-level filter preserves frontmatter key order byte-for-byte."""
    content = "---\nz_phase: 4\njury_gate:\n  verdict: PASS\na_status: approved\n---\nbody\n"
    result = strip_jury_gate(content)
    # z_phase must appear BEFORE a_status (insertion order preserved, not alphabetical)
    assert result.index("z_phase") < result.index("a_status")


def test_strip_jury_gate_preserves_block_scalar() -> None:
    """C-P6-VS02-R1-001: line-level filter preserves YAML block scalar formatting."""
    content = (
        "---\nschema_version: 1\njury_gate:\n  verdict: PASS\n"
        "description: |\n  line one\n  line two\n---\nbody\n"
    )
    result = strip_jury_gate(content)
    assert "jury_gate" not in result
    # Block scalar preserved byte-for-byte
    assert "description: |\n  line one\n  line two\n" in result


def test_parse_non_dict_frontmatter_returns_parsed(tmp_path: Path) -> None:
    """parse() returns non-dict frontmatter as-is; S04 will check and FAIL."""
    p = tmp_path / "list.md"
    p.write_text("---\n- item1\n- item2\n---\nbody\n", encoding="utf-8")
    fm, body = parse(p)
    assert fm == ["item1", "item2"]  # Returns the list, doesn't raise
    assert body == "body\n"


def test_strip_jury_gate_non_dict_frontmatter_unchanged() -> None:
    """C-P6-VS02-R1-003: strip_jury_gate returns unchanged if frontmatter is not a mapping."""
    content = "---\n- item1\n- item2\n---\nbody\n"
    assert strip_jury_gate(content) == content


def test_parse_strips_utf8_bom(tmp_path: Path) -> None:
    """C-P6-VS02-R1-004: parse() handles UTF-8 BOM at start of file."""
    p = tmp_path / "bom.md"
    # Write file with BOM prefix
    p.write_bytes(b"\xef\xbb\xbf---\nschema_version: 1\n---\nbody\n")
    fm, body = parse(p)
    assert fm["schema_version"] == 1
    assert "body" in body


def test_strip_jury_gate_strips_utf8_bom() -> None:
    """C-P6-VS02-R1-004: strip_jury_gate handles UTF-8 BOM at start of content."""
    content = "\ufeff---\nschema_version: 1\njury_gate:\n  verdict: PASS\n---\nbody\n"
    result = strip_jury_gate(content)
    assert "jury_gate" not in result
    assert "schema_version" in result
    assert "\ufeff" not in result


def test_strip_jury_gate_removes_single_space_indented_children() -> None:
    """C-P6-VS02-R1-001: jury_gate children with 1-space indent are filtered (mutant 134).

    Mutant 134 checks line[1] instead of line[0]; with single-space indent,
    line[0]=' ' (filtered by original) but line[1]='v' (not filtered by mutant).
    """
    # Single-space indent: line[0]=' ', line[1]='v' — mutant 134 checks line[1]
    content = "---\nschema_version: 1\njury_gate:\n v: PASS\n---\nbody\n"
    result = strip_jury_gate(content)
    assert "jury_gate" not in result
    assert " v: PASS" not in result
    assert "schema_version" in result


def test_strip_jury_gate_removes_block_scalar_with_blank_lines() -> None:
    """C-P6-VS02-R2-001: blank lines within jury_gate block scalar are filtered."""
    content = (
        "---\nschema_version: 1\njury_gate:\n  rationale: |\n"
        "    paragraph one\n\n    paragraph two\n---\nbody\n"
    )
    result = strip_jury_gate(content)
    assert "jury_gate" not in result
    assert "paragraph one" not in result
    assert "paragraph two" not in result
    assert "schema_version" in result


def test_strip_jury_gate_only_key_no_spurious_blank_line() -> None:
    """C-P6-VS02-R2-002: when jury_gate is sole frontmatter key, no extra blank line."""
    content = "---\njury_gate:\n  verdict: PASS\n---\nbody\n"
    result = strip_jury_gate(content)
    assert "jury_gate" not in result
    # Should be "---\n---\nbody\n" not "---\n\n---\nbody\n"
    assert "---\n\n---" not in result
    assert result.startswith("---\n---")


def test_parse_empty_frontmatter(tmp_path: Path) -> None:
    """C-P6-VS02-R1-005: parse() with empty frontmatter (---\\n---\\nbody) returns ({}, body)."""
    p = tmp_path / "empty_fm.md"
    p.write_text("---\n---\nbody text\n", encoding="utf-8")
    fm, body = parse(p)
    assert fm == {}
    assert "body text" in body

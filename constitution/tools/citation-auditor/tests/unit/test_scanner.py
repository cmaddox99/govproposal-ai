"""Unit tests for scanner.py — S-02 (Phase 6 Build).

Covers:
- Basic citation extraction from clean artifact
- T-07: fenced code block stripping (backtick and tilde, ADR-003)
- T-07: inline code stripping
- Deduplication: first-occurrence wins
- context_snippet ±150 chars (Phase 3 §2.2)
- allow_draft filtering → draft_skipped list
- T-09: >10 MB file rejected with AuditError
- T-09: non-UTF-8 encoding decoded with errors='replace' (no crash)
- T-09: >1000 matches capped at 1000
- Returns correct tuple[list[tuple[str, str]], list[str]] signature
- S-01: HTML stripping (T-01–T-08, T-34, T-36)
"""
from __future__ import annotations

import pytest
from pathlib import Path
from citation_auditor.exceptions import AuditError
from citation_auditor.registry import RegistryEntry

FIXTURES = Path(__file__).parent.parent / "fixtures" / "scanner"


def _entry(law_id: str) -> RegistryEntry:
    return RegistryEntry(
        law_id=law_id,
        domain="engineering",
        title=f"Title for {law_id}",
        summary=f"Summary for {law_id}",
        non_negotiable=False,
    )


def _registry(*ids: str) -> dict[str, RegistryEntry]:
    return {law_id: _entry(law_id) for law_id in ids}


# ---------------------------------------------------------------------------
# Import guard — scanner module must exist for tests to run
# ---------------------------------------------------------------------------
from citation_auditor.scanner import scan_artifact, _strip_html  # noqa: E402


# ---------------------------------------------------------------------------
# Return type contract
# ---------------------------------------------------------------------------
class TestReturnContract:
    def test_returns_tuple_of_two_lists(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        result = scan_artifact(artifact, reg, allow_draft=[])
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_first_element_is_list_of_tuples(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        assert isinstance(citations, list)
        for item in citations:
            assert isinstance(item, tuple)
            assert len(item) == 2

    def test_second_element_is_list_of_strings(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        _, draft_skipped = scan_artifact(artifact, reg, allow_draft=[])
        assert isinstance(draft_skipped, list)
        for item in draft_skipped:
            assert isinstance(item, str)


# ---------------------------------------------------------------------------
# Basic extraction — clean artifact
# ---------------------------------------------------------------------------
class TestBasicExtraction:
    def test_finds_all_unique_ids(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-4.1" in found_ids
        assert "PRD-2.6" in found_ids
        assert "BUS-7.1" in found_ids

    def test_deduplicates_repeated_ids(self):
        # artifact_clean.md has ENG-4.1 twice
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert found_ids.count("ENG-4.1") == 1

    def test_context_snippet_is_string(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        for _, snippet in citations:
            assert isinstance(snippet, str)

    def test_context_snippet_contains_law_id(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        for law_id, snippet in citations:
            assert law_id in snippet

    def test_context_snippet_max_length(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        for _, snippet in citations:
            # ±150 chars around match = up to 300 chars + match itself (7-9 chars)
            assert len(snippet) <= 310  # generous bound

    def test_empty_draft_skipped_when_no_draft_ids(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        _, draft_skipped = scan_artifact(artifact, reg, allow_draft=[])
        assert draft_skipped == []


# ---------------------------------------------------------------------------
# T-07: Fenced code block stripping (ADR-003)
# ---------------------------------------------------------------------------
class TestFencedBlockStripping:
    def test_ids_inside_backtick_fence_not_found(self):
        artifact = FIXTURES / "artifact_code_block_ids.md"
        reg = _registry("ENG-4.1", "ENG-6.1", "PRD-2.6", "BUS-7.1", "ENG-2.1", "ENG-3.4")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-6.1" not in found_ids
        assert "PRD-2.6" not in found_ids

    def test_ids_inside_tilde_fence_not_found(self):
        artifact = FIXTURES / "artifact_code_block_ids.md"
        reg = _registry("ENG-4.1", "ENG-6.1", "PRD-2.6", "BUS-7.1", "ENG-2.1", "ENG-3.4")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-2.1" not in found_ids

    def test_ids_outside_fences_still_found(self):
        artifact = FIXTURES / "artifact_code_block_ids.md"
        reg = _registry("ENG-4.1", "ENG-6.1", "PRD-2.6", "BUS-7.1", "ENG-2.1", "ENG-3.4")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-4.1" in found_ids
        assert "BUS-7.1" in found_ids
        assert "ENG-3.4" in found_ids


# ---------------------------------------------------------------------------
# T-07: Inline code stripping
# ---------------------------------------------------------------------------
class TestInlineCodeStripping:
    def test_ids_inside_inline_backticks_not_found(self):
        artifact = FIXTURES / "artifact_inline_code_ids.md"
        reg = _registry("ENG-4.1", "ENG-6.1", "PRD-2.6", "BUS-7.1", "ENG-3.4")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-6.1" not in found_ids

    def test_ids_outside_inline_code_found(self):
        artifact = FIXTURES / "artifact_inline_code_ids.md"
        reg = _registry("ENG-4.1", "ENG-6.1", "PRD-2.6", "BUS-7.1", "ENG-3.4")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-4.1" in found_ids
        assert "ENG-3.4" in found_ids

    def test_multiple_ids_in_same_inline_block_not_found(self):
        # artifact_inline_code_ids.md has `PRD-2.6 and BUS-7.1` in one inline block
        artifact = FIXTURES / "artifact_inline_code_ids.md"
        reg = _registry("ENG-4.1", "ENG-6.1", "PRD-2.6", "BUS-7.1", "ENG-3.4")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "PRD-2.6" not in found_ids
        assert "BUS-7.1" not in found_ids


# ---------------------------------------------------------------------------
# allow_draft filtering
# ---------------------------------------------------------------------------
class TestAllowDraftFiltering:
    def test_draft_id_in_allow_draft_goes_to_draft_skipped(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        _, draft_skipped = scan_artifact(artifact, reg, allow_draft=["ENG-4.1"])
        assert "ENG-4.1" in draft_skipped

    def test_draft_id_in_allow_draft_not_in_citations(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=["ENG-4.1"])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-4.1" not in found_ids

    def test_id_not_in_allow_draft_still_in_citations(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-4.1" in found_ids

    def test_id_not_in_allow_draft_never_in_draft_skipped(self):
        artifact = FIXTURES / "artifact_clean.md"
        reg = _registry("ENG-4.1", "PRD-2.6", "BUS-7.1")
        # ENG-4.1 not in allow_draft — must not appear in draft_skipped
        _, draft_skipped = scan_artifact(artifact, reg, allow_draft=["PRD-2.6"])
        assert "ENG-4.1" not in draft_skipped


# ---------------------------------------------------------------------------
# T-09: DoS guards
# ---------------------------------------------------------------------------
class TestDoSGuards:
    def test_oversized_file_raises_audit_error(self):
        artifact = FIXTURES / "artifact_oversized.bin"
        reg = _registry("ENG-4.1")
        with pytest.raises(AuditError, match="10 MB"):
            scan_artifact(artifact, reg, allow_draft=[])

    def test_non_utf8_file_does_not_crash(self):
        artifact = FIXTURES / "artifact_encoding_latin1.md"
        reg = _registry("ENG-4.1", "ENG-6.1")
        # Should not raise; decode with errors='replace'
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-4.1" in found_ids

    def test_many_citations_capped_at_1000(self):
        artifact = FIXTURES / "artifact_many_citations.md"
        # Build registry with all the IDs
        reg = {}
        for i in range(1, 1100):
            lid = f"ENG-{i}.{i % 9 + 1}"
            reg[lid] = _entry(lid)
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        assert len(citations) <= 1000

    def test_missing_file_raises_audit_error(self):
        artifact = FIXTURES / "nonexistent_file.md"
        reg = _registry("ENG-4.1")
        with pytest.raises(AuditError):
            scan_artifact(artifact, reg, allow_draft=[])

    def test_unreadable_file_after_stat_raises_audit_error(self, tmp_path):
        # stat succeeds but read_bytes fails → AuditError (lines 54-55)
        artifact = tmp_path / "locked.md"
        artifact.write_text("ENG-4.1 is here")
        artifact.chmod(0o000)
        try:
            with pytest.raises(AuditError, match="Cannot read"):
                scan_artifact(artifact, _registry("ENG-4.1"), allow_draft=[])
        finally:
            artifact.chmod(0o644)


# ---------------------------------------------------------------------------
# S-01: HTML stripping (T-01–T-08, T-34, T-36)
# ---------------------------------------------------------------------------
class TestHTMLStripping:
    """Tests for HTML stripping support added in Phase 6 Build Slice S-01."""

    # T-01: basic HTML — law ID in paragraph body is found
    def test_t01_html_basic_finds_id_in_paragraph(self):
        artifact = FIXTURES / "artifact_html_basic.html"
        reg = _registry("ENG-3.4")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-3.4" in found_ids

    # T-02: script tag content is excluded — ENG-6.4 inside <script> NOT found
    def test_t02_html_script_content_excluded(self):
        artifact = FIXTURES / "artifact_html_script_strip.html"
        reg = _registry("ENG-3.4", "ENG-6.4", "ENG-6.5")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-6.4" not in found_ids
        assert "ENG-3.4" in found_ids

    # T-03: style tag content is excluded — ENG-6.5 inside <style> NOT found
    def test_t03_html_style_content_excluded(self):
        artifact = FIXTURES / "artifact_html_script_strip.html"
        reg = _registry("ENG-3.4", "ENG-6.4", "ENG-6.5")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-6.5" not in found_ids

    # T-04: unclosed <script> tag raises AuditError (T-14)
    def test_t04_unclosed_script_raises_audit_error(self):
        artifact = FIXTURES / "artifact_html_unclosed_script.html"
        reg = _registry("ENG-3.4")
        with pytest.raises(AuditError, match="Unclosed"):
            scan_artifact(artifact, reg, allow_draft=[])

    # T-05: ID in table cell is found
    def test_t05_html_table_cell_id_found(self):
        artifact = FIXTURES / "artifact_html_table_ids.html"
        reg = _registry("ENG-6.4")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-6.4" in found_ids

    # T-06: empty HTML body → empty citations list
    def test_t06_html_empty_returns_no_citations(self):
        artifact = FIXTURES / "artifact_html_empty.html"
        reg = _registry("ENG-3.4", "ENG-4.1")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        assert citations == []

    # T-07: _strip_html — href attribute value not emitted; body text IS emitted
    def test_t07_strip_html_href_not_in_output_body_text_is(self):
        html = '<a href="ENG-3.4">text ENG-4.1</a>'
        result = _strip_html(html)
        assert "ENG-4.1" in result
        # href value is not emitted by handle_data so ENG-3.4 from href won't appear
        assert "ENG-3.4" not in result

    # T-08: _strip_html — HTML comment content not in output
    def test_t08_strip_html_comment_content_excluded(self):
        html = "<!-- ENG-6.4 -->text"
        result = _strip_html(html)
        assert "ENG-6.4" not in result

    # T-34: .md file with literal <script> tags — NOT HTML-stripped, IDs found
    def test_t34_md_file_not_html_stripped(self, tmp_path):
        md_file = tmp_path / "artifact_inline_script.md"
        md_file.write_text('<script>ENG-6.4</script>')
        reg = _registry("ENG-6.4")
        citations, _ = scan_artifact(md_file, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        # .md files skip HTML stripping — script tags are plain text, ID is found
        assert "ENG-6.4" in found_ids

    # T-36: benign malformed HTML (unclosed <p>) — both IDs still found
    def test_t36_unclosed_p_tag_ids_still_found(self):
        artifact = FIXTURES / "artifact_html_unclosed_p.html"
        reg = _registry("ENG-3.4", "ENG-4.9")
        citations, _ = scan_artifact(artifact, reg, allow_draft=[])
        found_ids = [law_id for law_id, _ in citations]
        assert "ENG-3.4" in found_ids
        assert "ENG-4.9" in found_ids

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
from citation_auditor.scanner import scan_artifact  # noqa: E402


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

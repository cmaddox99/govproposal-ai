"""Unit tests for auditor.py — S-03 (Phase 6 Build).

Covers all verdict rules from Phase 3 §2.2 and BDD scenarios §4.1/§4.2:
- FAIL: law_id not in registry
- WARN TITLE_MISMATCH: explicit title phrase within ±30 chars, partial_ratio < 60
- WARN STATUS_MISMATCH: NON-NEGOTIABLE/STRICTLY ENFORCED claim contradicts registry
- PASS: in registry, no mismatch detected
- Sorting: FAIL → WARN → PASS, then alpha within tier
- AuditResult fields: artifact_path, registry_path, law_count, scanned, results,
  draft_skipped, allow_draft, strict, timestamp, tool_version
- @property: fail_count, warn_count, pass_count, audit_exit_code
- strict=True: exit_code=1 on any WARN
- Zero citations: scanned=0, results=[]
- Context snippet: None for PASS, populated for FAIL/WARN
"""
from __future__ import annotations

from pathlib import Path

import pytest
from citation_auditor.exceptions import AuditError
from citation_auditor.models import AuditResult, CitationResult, Verdict
from citation_auditor.registry import RegistryEntry

from citation_auditor.auditor import audit  # noqa: E402

FIXTURES = Path(__file__).parent.parent / "fixtures" / "auditor"

_VERSION = "0.1.0"
_REG_PATH = "laws/"
_ART_PATH = "artifact.md"
_TS = "2026-05-24T17:00:00Z"


def _entry(law_id: str, non_negotiable: bool = False, title: str = "Some Law") -> RegistryEntry:
    return RegistryEntry(
        law_id=law_id,
        domain="engineering",
        title=title,
        summary=f"Summary of {law_id}",
        non_negotiable=non_negotiable,
    )


def _reg(**kwargs) -> dict[str, RegistryEntry]:
    """Build registry from law_id→RegistryEntry kwargs."""
    return dict(kwargs)


def _citation(law_id: str, snippet: str = "...context...") -> tuple[str, str]:
    return (law_id, snippet)


def _make_result(
    citations: list[tuple[str, str]],
    registry: dict[str, RegistryEntry],
    strict: bool = False,
    draft_skipped: list[str] | None = None,
) -> AuditResult:
    return audit(
        citations=citations,
        registry=registry,
        artifact_path=_ART_PATH,
        registry_path=_REG_PATH,
        law_count=len(registry),
        draft_skipped=draft_skipped or [],
        allow_draft=[],
        strict=strict,
        timestamp=_TS,
        tool_version=_VERSION,
    )


# ---------------------------------------------------------------------------
# Return type contract
# ---------------------------------------------------------------------------
class TestReturnContract:
    def test_returns_audit_result(self):
        result = _make_result([], {})
        assert isinstance(result, AuditResult)

    def test_audit_result_has_all_fields(self):
        result = _make_result([], {})
        assert result.artifact_path == _ART_PATH
        assert result.registry_path == _REG_PATH
        assert result.law_count == 0
        assert result.scanned == 0
        assert result.results == []
        assert result.draft_skipped == []
        assert result.allow_draft == []
        assert result.strict is False
        assert result.timestamp == _TS
        assert result.tool_version == _VERSION

    def test_results_is_list_of_citation_result(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        result = _make_result([_citation("ENG-4.1")], reg)
        for r in result.results:
            assert isinstance(r, CitationResult)


# ---------------------------------------------------------------------------
# PASS verdict
# ---------------------------------------------------------------------------
class TestPassVerdict:
    def test_known_id_no_mismatch_is_pass(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        result = _make_result([_citation("ENG-4.1", "governed by ENG-4.1 for testing")], reg)
        assert result.results[0].verdict == Verdict.PASS

    def test_pass_note_is_none(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        result = _make_result([_citation("ENG-4.1", "ENG-4.1 governs")], reg)
        assert result.results[0].note is None

    def test_pass_context_snippet_is_none(self):
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        result = _make_result([_citation("ENG-4.1", "ENG-4.1 governs")], reg)
        assert result.results[0].context_snippet is None

    def test_exit_code_zero_on_all_pass(self):
        reg = {"ENG-4.1": _entry("ENG-4.1"), "PRD-2.6": _entry("PRD-2.6")}
        result = _make_result([_citation("ENG-4.1"), _citation("PRD-2.6")], reg)
        assert result.audit_exit_code == 0

    def test_non_negotiable_asserted_correctly_is_pass(self):
        # BUS-7.1 is NON-NEGOTIABLE in registry; artifact says "(NON-NEGOTIABLE)" → PASS
        reg = {"BUS-7.1": _entry("BUS-7.1", non_negotiable=True, title="Audit Trail Law")}
        snippet = "BUS-7.1 (NON-NEGOTIABLE) must be followed"
        result = _make_result([_citation("BUS-7.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS


# ---------------------------------------------------------------------------
# FAIL verdict — ID not in registry
# ---------------------------------------------------------------------------
class TestFailVerdict:
    def test_unknown_id_is_fail(self):
        reg = {}
        result = _make_result([_citation("ENG-99.9")], reg)
        assert result.results[0].verdict == Verdict.FAIL

    def test_fail_note_contains_not_in_registry(self):
        reg = {}
        result = _make_result([_citation("ENG-99.9")], reg)
        assert "not in registry" in result.results[0].note.lower()

    def test_fail_context_snippet_populated(self):
        reg = {}
        snippet = "governed by ENG-99.9 fictional law"
        result = _make_result([_citation("ENG-99.9", snippet)], reg)
        assert result.results[0].context_snippet == snippet

    def test_exit_code_one_on_any_fail(self):
        reg = {}
        result = _make_result([_citation("ENG-99.9")], reg)
        assert result.audit_exit_code == 1

    def test_one_fail_among_passes_exit_one(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        result = _make_result([_citation("ENG-4.1"), _citation("ENG-99.9")], reg)
        assert result.audit_exit_code == 1


# ---------------------------------------------------------------------------
# WARN: TITLE_MISMATCH — explicit title phrase, partial_ratio < 60
# ---------------------------------------------------------------------------
class TestTitleMismatchWarn:
    def test_explicit_title_low_score_is_warn(self):
        # "Amendment Process Law" vs "Constitution Metrics Collection Law" — score < 60
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        # Title phrase in parens within 30 chars of ID
        snippet = "ENG-10.1 (Amendment Process Law) governs this"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    def test_title_mismatch_note_contains_score_info(self):
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "ENG-10.1 (Amendment Process Law) governs this"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        note = result.results[0].note.lower()
        assert "title" in note or "score" in note or "mismatch" in note

    def test_title_mismatch_context_snippet_populated(self):
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "ENG-10.1 (Amendment Process Law) governs this"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        assert result.results[0].context_snippet is not None

    def test_explicit_title_high_score_is_pass(self):
        # Title phrase closely matches registry — score ≥ 60 → PASS
        reg = {"ENG-3.5": _entry("ENG-3.5", title="Naming Conventions Law")}
        snippet = "ENG-3.5 **Naming Conventions Law** must be applied"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    def test_no_explicit_title_phrase_near_id_is_pass(self):
        # No bold/quoted text within 30 chars → no title check → PASS
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "governed by ENG-10.1 for compliance"
        result = _make_result([_citation("ENG-10.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

    def test_exit_code_zero_for_warn_without_strict(self):
        reg = {"ENG-10.1": _entry("ENG-10.1", title="Constitution Metrics Collection Law")}
        snippet = "ENG-10.1 (Amendment Process Law)"
        result = _make_result([_citation("ENG-10.1", snippet)], reg, strict=False)
        assert result.audit_exit_code == 0


# ---------------------------------------------------------------------------
# WARN: STATUS_MISMATCH — NON-NEGOTIABLE/STRICTLY ENFORCED assertion
# ---------------------------------------------------------------------------
class TestStatusMismatchWarn:
    def test_non_neg_asserted_on_non_non_neg_law_is_warn(self):
        # ENG-3.5 non_negotiable=False; artifact says "(NON-NEGOTIABLE)" → WARN
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False, title="Naming Conventions Law")}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies here"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    def test_status_mismatch_note_contains_status_mismatch(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert "status mismatch" in result.results[0].note.lower()

    def test_strictly_enforced_on_non_neg_law_is_warn(self):
        # BUS-7.1 non_negotiable=True; "STRICTLY ENFORCED" is wrong label → WARN
        reg = {"BUS-7.1": _entry("BUS-7.1", non_negotiable=True, title="Audit Trail Law")}
        snippet = "BUS-7.1 (STRICTLY ENFORCED) in all workflows"
        result = _make_result([_citation("BUS-7.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.WARN

    def test_status_mismatch_context_snippet_populated(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].context_snippet is not None

    def test_status_check_only_within_50_chars_of_id(self):
        # Status assertion is 100 chars away — should NOT trigger WARN
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        padding = "x" * 100
        snippet = f"ENG-3.5 {padding} (NON-NEGOTIABLE)"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS


# ---------------------------------------------------------------------------
# strict mode
# ---------------------------------------------------------------------------
class TestStrictMode:
    def test_strict_warn_yields_exit_code_1(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg, strict=True)
        assert result.audit_exit_code == 1

    def test_strict_flag_stored_in_result(self):
        result = _make_result([], {}, strict=True)
        assert result.strict is True

    def test_strict_false_warn_yields_exit_code_0(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE) applies"
        result = _make_result([_citation("ENG-3.5", snippet)], reg, strict=False)
        assert result.audit_exit_code == 0

    def test_strict_no_warn_yields_exit_code_0(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        result = _make_result([_citation("ENG-4.1")], reg, strict=True)
        assert result.audit_exit_code == 0


# ---------------------------------------------------------------------------
# Sorting: FAIL → WARN → PASS, then alpha within tier
# ---------------------------------------------------------------------------
class TestResultSorting:
    def test_fail_before_warn_before_pass(self):
        reg = {
            "ENG-4.1": _entry("ENG-4.1", non_negotiable=False),
            "PRD-2.6": _entry("PRD-2.6"),
        }
        citations = [
            _citation("PRD-2.6"),                                        # PASS
            _citation("ENG-4.1", "ENG-4.1 (NON-NEGOTIABLE)"),            # WARN
            _citation("ENG-99.9"),                                        # FAIL
        ]
        result = _make_result(citations, reg)
        verdicts = [r.verdict for r in result.results]
        # FAIL first, then WARN, then PASS
        fail_idx = verdicts.index(Verdict.FAIL)
        warn_idx = verdicts.index(Verdict.WARN)
        pass_idx = verdicts.index(Verdict.PASS)
        assert fail_idx < warn_idx < pass_idx

    def test_alpha_within_fail_tier(self):
        reg = {}
        citations = [_citation("PRD-9.9"), _citation("ENG-9.9"), _citation("BUS-9.9")]
        result = _make_result(citations, reg)
        fail_ids = [r.law_id for r in result.results if r.verdict == Verdict.FAIL]
        assert fail_ids == sorted(fail_ids)

    def test_alpha_within_pass_tier(self):
        reg = {
            "PRD-2.6": _entry("PRD-2.6"),
            "ENG-4.1": _entry("ENG-4.1"),
            "BUS-7.1": _entry("BUS-7.1"),
        }
        citations = [_citation("PRD-2.6"), _citation("ENG-4.1"), _citation("BUS-7.1")]
        result = _make_result(citations, reg)
        pass_ids = [r.law_id for r in result.results if r.verdict == Verdict.PASS]
        assert pass_ids == sorted(pass_ids)


# ---------------------------------------------------------------------------
# Zero citations
# ---------------------------------------------------------------------------
class TestZeroCitations:
    def test_zero_citations_scanned_is_zero(self):
        result = _make_result([], {})
        assert result.scanned == 0

    def test_zero_citations_results_empty(self):
        result = _make_result([], {})
        assert result.results == []

    def test_zero_citations_exit_code_zero(self):
        result = _make_result([], {})
        assert result.audit_exit_code == 0


# ---------------------------------------------------------------------------
# scanned count
# ---------------------------------------------------------------------------
class TestScannedCount:
    def test_scanned_reflects_citations_list_length(self):
        reg = {"ENG-4.1": _entry("ENG-4.1"), "PRD-2.6": _entry("PRD-2.6")}
        citations = [_citation("ENG-4.1"), _citation("PRD-2.6"), _citation("ENG-99.9")]
        result = _make_result(citations, reg)
        assert result.scanned == 3

    def test_draft_skipped_not_in_scanned(self):
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        # scanned = len(citations); draft_skipped passed separately
        result = audit(
            citations=[_citation("ENG-4.1")],
            registry=reg,
            artifact_path=_ART_PATH,
            registry_path=_REG_PATH,
            law_count=1,
            draft_skipped=["ENG-14.1"],
            allow_draft=["ENG-14.1"],
            strict=False,
            timestamp=_TS,
            tool_version=_VERSION,
        )
        assert result.scanned == 1  # only ENG-4.1 in citations
        assert "ENG-14.1" in result.draft_skipped


# ---------------------------------------------------------------------------
# @property counts
# ---------------------------------------------------------------------------
class TestPropertyCounts:
    def test_fail_count(self):
        reg = {}
        result = _make_result([_citation("ENG-9.9"), _citation("PRD-9.9")], reg)
        assert result.fail_count == 2

    def test_warn_count(self):
        reg = {"ENG-3.5": _entry("ENG-3.5", non_negotiable=False)}
        snippet = "ENG-3.5 (NON-NEGOTIABLE)"
        result = _make_result([_citation("ENG-3.5", snippet)], reg)
        assert result.warn_count == 1

    def test_pass_count(self):
        reg = {"ENG-4.1": _entry("ENG-4.1"), "PRD-2.6": _entry("PRD-2.6")}
        result = _make_result([_citation("ENG-4.1"), _citation("PRD-2.6")], reg)
        assert result.pass_count == 2

    def test_internal_failure_raises_audit_error(self):
        # Pass a citation tuple where snippet is not a string → triggers internal error
        reg = {"ENG-4.1": _entry("ENG-4.1")}
        with pytest.raises((AuditError, TypeError)):
            audit(
                citations=[("ENG-4.1", None)],  # type: ignore[arg-type]
                registry=reg,
                artifact_path=_ART_PATH,
                registry_path=_REG_PATH,
                law_count=1,
                draft_skipped=[],
                allow_draft=[],
                strict=False,
                timestamp=_TS,
                tool_version=_VERSION,
            )

    def test_empty_title_phrase_no_warn(self):
        # Parenthesised phrase that is empty after strip — no title WARN raised
        reg = {"ENG-4.1": _entry("ENG-4.1", title="Atomic TDD Law")}
        snippet = "ENG-4.1 () governs testing"
        result = _make_result([_citation("ENG-4.1", snippet)], reg)
        assert result.results[0].verdict == Verdict.PASS

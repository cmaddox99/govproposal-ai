"""RED phase — S-01: Tests for models, registry, and exceptions.

ENG-4.1 (NON-NEGOTIABLE): Test file committed before production code.
All assertions will FAIL until production code is implemented (GREEN phase).
"""
from __future__ import annotations

import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# Exception taxonomy tests
# ---------------------------------------------------------------------------

def test_registry_load_error_is_exception():
    """RegistryLoadError must be a subclass of Exception."""
    from citation_auditor.exceptions import RegistryLoadError
    assert issubclass(RegistryLoadError, Exception)


def test_audit_error_is_exception():
    """AuditError must be a subclass of Exception."""
    from citation_auditor.exceptions import AuditError
    assert issubclass(AuditError, Exception)


def test_registry_load_error_carries_message():
    from citation_auditor.exceptions import RegistryLoadError
    err = RegistryLoadError("Registry directory not found: /bad/path")
    assert "Registry directory not found" in str(err)


def test_audit_error_carries_message():
    from citation_auditor.exceptions import AuditError
    err = AuditError("internal verdict failure")
    assert "internal verdict failure" in str(err)


# ---------------------------------------------------------------------------
# Verdict enum tests
# ---------------------------------------------------------------------------

def test_verdict_has_exactly_three_members():
    """Verdict MUST have exactly PASS, WARN, FAIL — no SKIP (Phase 3 §2.2)."""
    from citation_auditor.models import Verdict
    members = {m.name for m in Verdict}
    assert members == {"PASS", "WARN", "FAIL"}


def test_verdict_values():
    from citation_auditor.models import Verdict
    assert Verdict.PASS.value == "PASS"
    assert Verdict.WARN.value == "WARN"
    assert Verdict.FAIL.value == "FAIL"


# ---------------------------------------------------------------------------
# CitationResult dataclass tests
# ---------------------------------------------------------------------------

def test_citation_result_fields():
    from citation_auditor.models import CitationResult, Verdict
    r = CitationResult(
        law_id="ENG-3.5",
        verdict=Verdict.PASS,
        note=None,
        context_snippet=None,
    )
    assert r.law_id == "ENG-3.5"
    assert r.verdict == Verdict.PASS
    assert r.note is None
    assert r.context_snippet is None


def test_citation_result_fail_has_note():
    from citation_auditor.models import CitationResult, Verdict
    r = CitationResult(
        law_id="ENG-99.9",
        verdict=Verdict.FAIL,
        note="ID not in registry",
        context_snippet="...governed by ENG-99.9 here...",
    )
    assert r.note == "ID not in registry"
    assert r.context_snippet is not None


# ---------------------------------------------------------------------------
# AuditResult dataclass + @property tests
# ---------------------------------------------------------------------------

def _make_audit_result(results=None):
    from citation_auditor.models import AuditResult, CitationResult, Verdict
    if results is None:
        results = [
            CitationResult("ENG-99.9", Verdict.FAIL, "not in registry", "snippet"),
            CitationResult("PRD-2.6", Verdict.WARN, "title mismatch", "snippet2"),
            CitationResult("ENG-3.5", Verdict.PASS, None, None),
        ]
    return AuditResult(
        artifact_path="test/artifact.md",
        registry_path="laws/index.yaml",
        law_count=170,
        scanned=3,
        results=results,
        draft_skipped=[],
        allow_draft=[],
        strict=False,
        timestamp="2026-05-24T17:00:00Z",
        tool_version="0.1.0",
    )


def test_audit_result_fail_count():
    ar = _make_audit_result()
    assert ar.fail_count == 1


def test_audit_result_warn_count():
    ar = _make_audit_result()
    assert ar.warn_count == 1


def test_audit_result_pass_count():
    ar = _make_audit_result()
    assert ar.pass_count == 1


def test_audit_result_exit_code_zero_no_fail():
    from citation_auditor.models import CitationResult, Verdict
    ar = _make_audit_result(results=[
        CitationResult("ENG-3.5", Verdict.PASS, None, None),
    ])
    assert ar.audit_exit_code == 0


def test_audit_result_exit_code_one_on_fail():
    ar = _make_audit_result()
    assert ar.audit_exit_code == 1


def test_audit_result_exit_code_one_strict_warn():
    from citation_auditor.models import AuditResult, CitationResult, Verdict
    ar = AuditResult(
        artifact_path="a.md", registry_path="laws/index.yaml",
        law_count=10, scanned=1,
        results=[CitationResult("PRD-2.6", Verdict.WARN, "mismatch", "snip")],
        draft_skipped=[], allow_draft=[], strict=True,
        timestamp="2026-05-24T17:00:00Z", tool_version="0.1.0",
    )
    assert ar.audit_exit_code == 1


def test_audit_result_exit_code_zero_warn_no_strict():
    from citation_auditor.models import AuditResult, CitationResult, Verdict
    ar = AuditResult(
        artifact_path="a.md", registry_path="laws/index.yaml",
        law_count=10, scanned=1,
        results=[CitationResult("PRD-2.6", Verdict.WARN, "mismatch", "snip")],
        draft_skipped=[], allow_draft=[], strict=False,
        timestamp="2026-05-24T17:00:00Z", tool_version="0.1.0",
    )
    assert ar.audit_exit_code == 0


def test_audit_result_no_stored_skip_count():
    """AuditResult must NOT have skip_count or pass_rate stored fields."""
    ar = _make_audit_result()
    assert not hasattr(ar, "skip_count")
    assert not hasattr(ar, "pass_rate")


# ---------------------------------------------------------------------------
# Registry tests (requires mini fixture)
# ---------------------------------------------------------------------------

FIXTURE_REGISTRY = Path(__file__).parent.parent / "fixtures" / "registry"


def test_load_registry_returns_dict(tmp_path):
    """load_registry() returns dict[str, RegistryEntry] for valid fixture."""
    from citation_auditor.registry import load_registry
    result = load_registry(FIXTURE_REGISTRY)
    assert isinstance(result, dict)
    assert len(result) > 0


def test_load_registry_entry_fields(tmp_path):
    """Each RegistryEntry must have law_id, domain, non_negotiable, title, summary."""
    from citation_auditor.registry import load_registry, RegistryEntry
    result = load_registry(FIXTURE_REGISTRY)
    for law_id, entry in result.items():
        assert isinstance(entry, RegistryEntry)
        assert entry.law_id == law_id
        assert entry.domain in ("engineering", "product", "business")
        assert isinstance(entry.non_negotiable, bool)


def test_load_registry_missing_dir_raises():
    from citation_auditor.registry import load_registry
    from citation_auditor.exceptions import RegistryLoadError
    with pytest.raises(RegistryLoadError, match="Registry directory not found"):
        load_registry(Path("/nonexistent/path"))


def test_load_registry_missing_index_raises(tmp_path):
    from citation_auditor.registry import load_registry
    from citation_auditor.exceptions import RegistryLoadError
    empty_dir = tmp_path / "laws"
    empty_dir.mkdir()
    with pytest.raises(RegistryLoadError, match="Registry file not found"):
        load_registry(empty_dir)


def test_load_registry_non_dict_yaml_raises(tmp_path):
    """index.yaml that parses to a non-dict raises RegistryLoadError."""
    from citation_auditor.registry import load_registry
    from citation_auditor.exceptions import RegistryLoadError
    laws_dir = tmp_path / "laws"
    laws_dir.mkdir()
    (laws_dir / "index.yaml").write_text("- just\n- a\n- list\n")
    with pytest.raises(RegistryLoadError, match="Registry load failed"):
        load_registry(laws_dir)


def test_load_registry_skips_nonexistent_law_file(tmp_path):
    """Files listed in domains.files that don't exist are silently skipped."""
    from citation_auditor.registry import load_registry
    laws_dir = tmp_path / "laws"
    laws_dir.mkdir()
    (laws_dir / "index.yaml").write_text(
        "domains:\n  engineering:\n    files:\n      - laws/engineering/missing.md\n"
        "law_ids:\n  engineering:\n    - ENG-3.5\n"
        "non_negotiable: {}\n"
    )
    result = load_registry(laws_dir)
    assert "ENG-3.5" in result
    assert result["ENG-3.5"].title is None  # no file → no title


def test_load_registry_skips_non_dict_domain_data(tmp_path):
    """Domain entries that are not dicts are skipped without error."""
    from citation_auditor.registry import load_registry
    laws_dir = tmp_path / "laws"
    laws_dir.mkdir()
    (laws_dir / "index.yaml").write_text(
        "domains:\n  engineering: null\nlaw_ids:\n  engineering:\n    - ENG-3.5\nnon_negotiable: {}\n"
    )
    result = load_registry(laws_dir)
    assert "ENG-3.5" in result


def test_parse_law_file_no_frontmatter(tmp_path):
    """Law file without frontmatter is silently skipped."""
    from citation_auditor.registry import _parse_law_file
    law_file = tmp_path / "law.md"
    law_file.write_text("# No frontmatter here\nJust content.")
    title_map: dict = {}
    summary_map: dict = {}
    _parse_law_file(law_file, title_map, summary_map)
    assert title_map == {}


def test_parse_law_file_unclosed_frontmatter(tmp_path):
    """Law file with unclosed frontmatter delimiter is silently skipped."""
    from citation_auditor.registry import _parse_law_file
    law_file = tmp_path / "law.md"
    law_file.write_text("---\nlaws:\n  - id: ENG-1.0\n# no closing ---")
    title_map: dict = {}
    summary_map: dict = {}
    _parse_law_file(law_file, title_map, summary_map)
    assert title_map == {}


def test_parse_law_file_malformed_frontmatter_yaml(tmp_path):
    """Law file with malformed frontmatter YAML is silently skipped."""
    from citation_auditor.registry import _parse_law_file
    law_file = tmp_path / "law.md"
    law_file.write_text("---\n: bad: [unclosed\n---\ncontent")
    title_map: dict = {}
    summary_map: dict = {}
    _parse_law_file(law_file, title_map, summary_map)
    assert title_map == {}


def test_parse_law_file_non_dict_law_entry(tmp_path):
    """Non-dict entries in frontmatter.laws list are skipped."""
    from citation_auditor.registry import _parse_law_file
    law_file = tmp_path / "law.md"
    law_file.write_text("---\nlaws:\n  - just_a_string\n  - id: ENG-3.5\n    title: Real Law\n---\ncontent")
    title_map: dict = {}
    summary_map: dict = {}
    _parse_law_file(law_file, title_map, summary_map)
    assert title_map.get("ENG-3.5") == "Real Law"


def test_parse_law_file_no_id_field(tmp_path):
    """Law entry with no 'id' field is skipped without error."""
    from citation_auditor.registry import _parse_law_file
    law_file = tmp_path / "law.md"
    law_file.write_text("---\nlaws:\n  - title: Orphan Title\n    summary: No ID here\n---\ncontent")
    title_map: dict = {}
    summary_map: dict = {}
    _parse_law_file(law_file, title_map, summary_map)
    assert title_map == {}


def test_parse_law_file_os_error(tmp_path):
    """Unreadable law file (OSError) is silently skipped."""
    import os
    from citation_auditor.registry import _parse_law_file
    law_file = tmp_path / "law.md"
    law_file.write_text("---\nlaws:\n  - id: ENG-3.5\n    title: Test\n---\n")
    os.chmod(law_file, 0o000)
    title_map: dict = {}
    summary_map: dict = {}
    try:
        _parse_law_file(law_file, title_map, summary_map)
        assert title_map == {}  # silently skipped
    finally:
        os.chmod(law_file, 0o644)


def test_parse_law_file_frontmatter_not_dict(tmp_path):
    """Frontmatter that parses to non-dict (e.g. a list) is silently skipped."""
    from citation_auditor.registry import _parse_law_file
    law_file = tmp_path / "law.md"
    law_file.write_text("---\n- just\n- a list\n---\ncontent")
    title_map: dict = {}
    summary_map: dict = {}
    _parse_law_file(law_file, title_map, summary_map)
    assert title_map == {}
    from citation_auditor.registry import load_registry
    from citation_auditor.exceptions import RegistryLoadError
    laws_dir = tmp_path / "laws"
    laws_dir.mkdir()
    (laws_dir / "index.yaml").write_text(": bad: yaml: [unclosed")
    with pytest.raises(RegistryLoadError, match="Registry load failed"):
        load_registry(laws_dir)

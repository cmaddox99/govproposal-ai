"""Tests for citation_resolver.py — law citation lookup and tooltip injection."""
import pytest
from pathlib import Path
from aa_artifact_render.citation_resolver import CitationResolver, ResolvedCitation


CONSTITUTION_LAWS_DIR = Path(__file__).parents[3] / "laws"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def resolver():
    """Resolver pointed at the real constitution laws/ directory."""
    return CitationResolver(laws_dir=CONSTITUTION_LAWS_DIR)


@pytest.fixture
def resolver_bad_dir(tmp_path):
    """Resolver pointed at an empty temp directory (no law files)."""
    return CitationResolver(laws_dir=tmp_path)


# ---------------------------------------------------------------------------
# Known law ID lookup
# ---------------------------------------------------------------------------

def test_resolver_finds_known_engineering_law(resolver):
    result = resolver.resolve("ENG-4.1")
    assert isinstance(result, ResolvedCitation)
    assert result.law_id == "ENG-4.1"
    assert result.found is True
    assert "Atomic TDD" in result.title


def test_resolver_finds_product_law(resolver):
    result = resolver.resolve("PRD-1.2")
    assert result.found is True
    assert result.law_id == "PRD-1.2"
    assert result.title  # non-empty


def test_resolver_finds_business_law(resolver):
    result = resolver.resolve("BUS-7.1")
    assert result.found is True
    assert result.law_id == "BUS-7.1"


def test_resolver_finds_new_law_ENG_13_1(resolver):
    result = resolver.resolve("ENG-13.1")
    assert result.found is True
    assert "Artifact Rendering" in result.title
    assert result.summary


def test_resolver_non_negotiable_flag_set_for_known_non_neg(resolver):
    result = resolver.resolve("ENG-4.1")
    assert result.non_negotiable is True


def test_resolver_non_negotiable_false_for_recommended_law(resolver):
    result = resolver.resolve("ENG-13.1")
    assert result.non_negotiable is False


def test_resolver_returns_summary_text(resolver):
    result = resolver.resolve("ENG-4.1")
    assert result.summary
    assert len(result.summary) > 10


# ---------------------------------------------------------------------------
# Unknown law ID — graceful fallback
# ---------------------------------------------------------------------------

def test_resolver_unknown_law_returns_not_found(resolver):
    result = resolver.resolve("ENG-0.0")
    assert result.found is False
    assert result.law_id == "ENG-0.0"
    assert result.title == ""
    assert result.summary == ""
    assert result.non_negotiable is False


def test_resolver_unknown_law_does_not_raise(resolver):
    # Must never raise — graceful fallback required
    result = resolver.resolve("BUS-99.99")
    assert result is not None
    assert result.found is False


# ---------------------------------------------------------------------------
# Auto-detection of laws/ directory
# ---------------------------------------------------------------------------

def test_resolver_auto_detect_from_constitution_root(monkeypatch, tmp_path):
    """When run inside a repo with laws/ at root, laws_dir=None should auto-detect."""
    # Create a minimal laws structure in tmp_path
    laws = tmp_path / "laws"
    laws.mkdir()
    (laws / "engineering").mkdir()
    law_file = laws / "engineering" / "testing.md"
    law_file.write_text(
        "---\ndomain: engineering\narticle: IV\ntitle: Testing Laws\n"
        "laws:\n  - id: ENG-4.1\n    title: Atomic TDD Law\n"
        "    non_negotiable: true\n"
        "    summary: TDD SHALL be practiced in atomic cycles\n---\n\n# Body\n"
    )
    monkeypatch.chdir(tmp_path)
    r = CitationResolver(laws_dir=None)
    result = r.resolve("ENG-4.1")
    assert result.found is True


def test_resolver_explicit_path_takes_precedence(resolver, tmp_path):
    """Explicit laws_dir overrides auto-detection."""
    r = CitationResolver(laws_dir=tmp_path)
    result = r.resolve("ENG-4.1")
    assert result.found is False  # empty dir has no laws


# ---------------------------------------------------------------------------
# Multi-law files (one file defines multiple law IDs)
# ---------------------------------------------------------------------------

def test_resolver_handles_multiple_laws_in_one_file(resolver):
    """testing.md defines ENG-4.1 through ENG-4.11 — all should be resolvable."""
    for law_id in ("ENG-4.1", "ENG-4.2", "ENG-4.3"):
        result = resolver.resolve(law_id)
        assert result.found is True, f"{law_id} not found"


# ---------------------------------------------------------------------------
# Index caching — law index built once, not re-parsed on each call
# ---------------------------------------------------------------------------

def test_resolver_index_is_built_once(resolver):
    """Calling resolve multiple times should use a cached index."""
    r1 = resolver.resolve("ENG-4.1")
    r2 = resolver.resolve("ENG-4.1")
    assert r1.title == r2.title
    # Internal index should be populated after first call
    assert resolver._index is not None
    assert len(resolver._index) > 0

"""ESE-42–43: ref-build-packages.md — Source File Organization + Profiling sections.

Spec: cpp-external-sources-enrichment/tasks.md (ESE-42, ESE-43)
Laws: ENG-3.1 (Code Quality), ENG-4.1 (Atomic TDD)
"""
import pathlib

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
REF_FILE = CPP_DIR / "refs" / "testing" / "ref-build-packages.md"

import pytest

@pytest.fixture(scope="module")
def content():
    return REF_FILE.read_text()


class TestSourceFileOrganization:
    """ESE-42: Source File Organization (SF.xx)."""

    def test_section_heading_present(self, content):
        assert "Source File" in content

    def test_sf7_no_using_namespace_headers(self, content):
        assert "SF.7" in content or "using namespace" in content

    def test_sf12_pragma_once(self, content):
        assert "SF.12" in content or "pragma once" in content

    def test_has_law_reference_in_body(self, content):
        idx = content.find("Source File")
        assert "[ENG-3.1]" in content[idx:idx+700]


class TestProfilingBeforeOptimization:
    """ESE-43: Profiling Before Optimization (Per.xx)."""

    def test_section_heading_present(self, content):
        assert "Profil" in content or "Optimization" in content

    def test_per1_reference(self, content):
        assert "Per.1" in content or "premature" in content.lower()

    def test_per10_reference(self, content):
        assert "Per.10" in content or "std::move" in content

    def test_has_law_reference_in_body(self, content):
        idx = content.find("Profil")
        if idx == -1:
            idx = content.find("Optimization")
        assert "[ENG-3.1]" in content[idx:idx+700]

    def test_token_budget(self):
        c = REF_FILE.read_text()
        assert len(c) // 4 <= 3500

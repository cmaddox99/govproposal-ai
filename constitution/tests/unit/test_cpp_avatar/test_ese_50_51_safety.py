"""ESE-50–51: ref-safety-memory-lifetime.md — C-Style + GSL Profiles sections.

Spec: cpp-external-sources-enrichment/tasks.md (ESE-50, ESE-51)
Laws: ENG-3.1 (Code Quality), ENG-6.1 (Security by Design), ENG-4.1 (Atomic TDD)
"""
import pathlib

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
REF_FILE = CPP_DIR / "refs" / "safety" / "ref-safety-memory-lifetime.md"

import pytest

@pytest.fixture(scope="module")
def content():
    return REF_FILE.read_text()


class TestCStyleProgramming:
    """ESE-50: C-Style Programming (CPL.xx)."""

    def test_section_heading_present(self, content):
        assert "C-Style" in content or "CPL" in content

    def test_cpl1_reference(self, content):
        assert "CPL.1" in content or "CPL.2" in content

    def test_extern_c_mentioned(self, content):
        assert "extern" in content and '"C"' in content

    def test_has_law_reference_in_body(self, content):
        idx = content.find("C-Style")
        if idx == -1:
            idx = content.find("CPL.")
        assert "[ENG-3.1]" in content[idx:idx+700]


class TestGSLProfiles:
    """ESE-51: GSL Profiles (Pro.xx)."""

    def test_section_heading_present(self, content):
        assert "GSL" in content or "Pro." in content or "Profile" in content

    def test_pro_reference(self, content):
        assert "Pro." in content

    def test_span_bounds_mentioned(self, content):
        assert "span" in content or "bounds" in content.lower()

    def test_has_law_reference_in_body(self, content):
        idx = content.find("GSL")
        if idx == -1:
            idx = content.find("Pro.")
        assert "[ENG-6.1]" in content[idx:idx+700] or "[ENG-3.1]" in content[idx:idx+700]

    def test_token_budget(self):
        c = REF_FILE.read_text()
        assert len(c) // 4 <= 3500, f"Over budget: {len(c)//4}t"

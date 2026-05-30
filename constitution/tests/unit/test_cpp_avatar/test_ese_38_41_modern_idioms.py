"""ESE-38–41: ref-core-modern-idioms.md — four new sections.

Spec: cpp-external-sources-enrichment/tasks.md (ESE-38, ESE-39, ESE-40, ESE-41)
Laws: ENG-3.1 (Code Quality), ENG-4.1 (Atomic TDD)
"""
import pathlib

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
REF_FILE = CPP_DIR / "refs" / "language" / "ref-core-modern-idioms.md"

import pytest

@pytest.fixture(scope="module")
def content():
    return REF_FILE.read_text()


class TestParameterPassingSection:
    """ESE-38: Parameter Passing table (F.16-F.20)."""

    def test_section_heading_present(self, content):
        assert "Parameter Passing" in content

    def test_f16_reference(self, content):
        assert "F.16" in content or "in-params" in content.lower()

    def test_f20_reference(self, content):
        assert "F.20" in content or "out-params" in content.lower()

    def test_has_law_reference_in_body(self, content):
        # Law link must appear after the Parameter Passing heading
        idx = content.find("Parameter Passing")
        assert "[ENG-3.1]" in content[idx:idx+600]


class TestRuleOfZeroFive:
    """ESE-39: Rule of Zero/Five (C.20/C.21/C.22)."""

    def test_section_heading_present(self, content):
        assert "Rule of Zero" in content or "Rule of Five" in content

    def test_c20_reference(self, content):
        assert "C.20" in content or "Rule of Zero" in content

    def test_c21_reference(self, content):
        assert "C.21" in content or "Rule of Five" in content

    def test_has_law_reference_in_body(self, content):
        idx = content.find("Rule of Zero")
        if idx == -1:
            idx = content.find("Rule of Five")
        assert "[ENG-3.1]" in content[idx:idx+600]


class TestRegularTypes:
    """ESE-40: Regular Types (C.11)."""

    def test_section_heading_present(self, content):
        assert "Regular" in content and ("Type" in content or "Semiregular" in content)

    def test_c11_reference(self, content):
        assert "C.11" in content

    def test_has_law_reference_in_body(self, content):
        idx = content.find("Regular")
        assert "[ENG-3.1]" in content[idx:idx+600]


class TestContainerAlgorithmGuide:
    """ESE-41: Container/Algorithm Guide."""

    def test_section_heading_present(self, content):
        assert "Container" in content and ("Algorithm" in content or "algorithm" in content)

    def test_token_budget(self):
        c = REF_FILE.read_text()
        tokens = len(c) // 4
        assert tokens <= 3500, f"Over budget: {tokens}t > 3500t"

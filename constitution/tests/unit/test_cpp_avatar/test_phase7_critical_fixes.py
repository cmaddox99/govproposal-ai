"""Phase 7 tests: Critical fixes — law ID correctness and compiler warning policy.

Scenario-IDs: 7.5, 7.6
"""
import pathlib
import re

import pytest

_CPP_DIR = pathlib.Path(__file__).resolve().parents[3] / "avatars" / "technology" / "cpp"


def _read_full_reference():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(_CPP_DIR.rglob("ref-*.md")))
MANIFEST = pathlib.Path(__file__).resolve().parents[3] / "avatars" / "technology" / "cpp" / "manifest.yaml"

# Actual law definitions from laws/engineering/devops.md
CORRECT_LAW_TITLES = {
    "ENG-5.1": "Infrastructure as Code",
    "ENG-5.2": "CI/CD Pipeline",
    "ENG-5.5": "Observability",
    "ENG-5.6": "Configuration Management",
}


class TestLawIdCorrectness:
    """7.5: Verify law IDs match actual definitions in guidance.md."""

    @pytest.fixture(autouse=True)
    def load_guidance(self):
        self.content = _read_full_reference()

    def test_ci_toolchain_references_eng_5_2(self):
        """CI Quality Toolchain section must cite ENG-5.2 (CI/CD Pipeline), not ENG-5.1."""
        # Find the CI Quality Toolchain section
        match = re.search(r"## CI Quality Toolchain Policy\n\n(.+?)(?=\n## |\Z)", self.content, re.DOTALL)
        assert match, "CI Quality Toolchain Policy section not found"
        section = match.group(1)
        # First ENG-5.x reference should be ENG-5.2
        assert "ENG-5.2" in section, "CI Toolchain section should reference ENG-5.2 (CI/CD Pipeline Law)"
        # Should NOT reference ENG-5.1 as the primary law (IaC is a different section)
        first_law_ref = re.search(r"ENG-5\.\d", section)
        assert first_law_ref and first_law_ref.group() == "ENG-5.2", \
            f"First ENG-5.x reference in CI Toolchain should be ENG-5.2, got {first_law_ref.group() if first_law_ref else 'none'}"

    def test_iac_references_eng_5_1(self):
        """Infrastructure as Code section must cite ENG-5.1, not ENG-5.2."""
        match = re.search(r"### Infrastructure as Code.*?\n\n(.+?)(?=\n### |\n## |\Z)", self.content, re.DOTALL)
        assert match, "IaC subsection not found"
        section = match.group(1)
        assert "ENG-5.1" in section, "IaC section should reference ENG-5.1 (Infrastructure as Code Law)"

    def test_secrets_references_eng_5_6(self):
        """Secrets Management section must cite ENG-5.6 (Configuration Management), not ENG-5.5."""
        match = re.search(r"### Secrets Management.*?\n\n(.+?)(?=\n### |\n## |\Z)", self.content, re.DOTALL)
        assert match, "Secrets Management subsection not found"
        section = match.group(1)
        assert "ENG-5.6" in section, "Secrets section should reference ENG-5.6 (Configuration Management Law)"

    def test_observability_references_eng_5_5(self):
        """Observability section must cite ENG-5.5, not ENG-5.6."""
        match = re.search(r"### Observability.*?\n\n(.+?)(?=\n### |\n## |\Z)", self.content, re.DOTALL)
        assert match, "Observability subsection not found"
        section = match.group(1)
        assert "ENG-5.5" in section, "Observability section should reference ENG-5.5 (Observability Law)"

    def test_cross_language_table_law_ids(self):
        """Cross-Language Alignment table must use correct law IDs."""
        match = re.search(r"### Cross-Language Alignment.*?\n\n(.+?)(?=\n### |\n## |\Z)", self.content, re.DOTALL)
        assert match, "Cross-Language Alignment section not found"
        table = match.group(1)
        # IaC row should reference ENG-5.1
        assert re.search(r"IaC.*ENG-5\.1", table), "IaC row should reference ENG-5.1"
        # Secrets row should reference ENG-5.6
        assert re.search(r"Secrets.*ENG-5\.6", table), "Secrets row should reference ENG-5.6"
        # Observability row should reference ENG-5.5
        assert re.search(r"Observability.*ENG-5\.5", table), "Observability row should reference ENG-5.5"


class TestCompilerWarningPolicy:
    """7.6: Verify compiler warning policy section exists in guidance.md."""

    @pytest.fixture(autouse=True)
    def load_guidance(self):
        self.content = _read_full_reference()

    def test_compiler_warnings_section_exists(self):
        """Guidance must have a Compiler Warning Flags section."""
        assert "Compiler Warning" in self.content or "Warning Flags" in self.content, \
            "guidance.md missing compiler warning policy section"

    def test_wall_wextra_werror_mentioned(self):
        """Compiler warning section must mention -Wall, -Wextra, -Werror."""
        assert "-Wall" in self.content, "guidance.md missing -Wall"
        assert "-Wextra" in self.content, "guidance.md missing -Wextra"
        assert "-Werror" in self.content, "guidance.md missing -Werror"

    def test_wpedantic_mentioned(self):
        """Compiler warning section must mention -Wpedantic."""
        assert "-Wpedantic" in self.content, "guidance.md missing -Wpedantic"

    def test_cmake_warning_integration(self):
        """Compiler warning section must show CMake integration."""
        assert "target_compile_options" in self.content or "CMAKE_CXX_FLAGS" in self.content, \
            "guidance.md missing CMake warning flag integration"

    def test_manifest_has_warning_flags(self):
        """CI toolchain example must include warning flags (routed from manifest)."""
        ci_example = MANIFEST.parent / "examples" / "ENG-5.2-cmake-governance.md"
        ci_content = ci_example.read_text(encoding="utf-8")
        assert "-Wall" in ci_content or "warning flags" in ci_content.lower() or \
            "compiler warnings" in ci_content.lower(), \
            "ENG-5.2-cmake-governance.md missing compiler warning flags in CI toolchain"

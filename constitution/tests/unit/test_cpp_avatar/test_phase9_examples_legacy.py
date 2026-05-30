"""Phase 9 tests: C++20+ examples and legacy code navigation guidance.

Scenario-IDs: 9.13, 9.14
"""
import pathlib

import pytest

_CPP_DIR = pathlib.Path(__file__).resolve().parents[3] / "avatars" / "technology" / "cpp"


def _read_full_reference():
    return "\n".join(p.read_text(encoding="utf-8") for p in sorted(_CPP_DIR.rglob("ref-*.md")))
EXAMPLES_DIR = pathlib.Path(__file__).resolve().parents[3] / "avatars" / "technology" / "cpp" / "examples"
SKILLS_DIR = pathlib.Path(__file__).resolve().parents[3] / "agent-skills" / "skills-by-domain" / "platform-engineering"

# C++20+ examples added in Phase 9
PHASE9_EXAMPLES = [
    "ENG-6.1-smart-pointers.md",
    "ENG-6.1-move-semantics.md",
    "ENG-6.1-thread-safety.md",
    "ENG-6.1-raii-resources.md",
    "ENG-3.1-concepts.md",
    "ENG-6.1-expected-errors.md",
    "ENG-3.1-coroutines.md",
    "ENG-6.7-structured-logging.md",
    "ENG-5.2-cmake-governance.md",
    "ENG-3.1-pmr-allocators.md",
]


class TestPhase9Examples:
    """9.13: C++20+ example files exist with correct structure."""

    @pytest.mark.parametrize("example_file", PHASE9_EXAMPLES)
    def test_example_exists(self, example_file):
        path = EXAMPLES_DIR / example_file
        assert path.exists(), f"Missing example: {example_file}"

    @pytest.mark.parametrize("example_file", PHASE9_EXAMPLES)
    def test_example_has_frontmatter(self, example_file):
        content = (EXAMPLES_DIR / example_file).read_text(encoding="utf-8")
        assert content.startswith("---"), f"{example_file} missing YAML frontmatter"

    @pytest.mark.parametrize("example_file", PHASE9_EXAMPLES)
    def test_example_has_compliant_section(self, example_file):
        content = (EXAMPLES_DIR / example_file).read_text(encoding="utf-8")
        assert "COMPLIANT" in content, f"{example_file} missing COMPLIANT section"

    @pytest.mark.parametrize("example_file", PHASE9_EXAMPLES)
    def test_example_has_non_compliant_section(self, example_file):
        content = (EXAMPLES_DIR / example_file).read_text(encoding="utf-8")
        assert "NON-COMPLIANT" in content, f"{example_file} missing NON-COMPLIANT section"

    @pytest.mark.parametrize("example_file", PHASE9_EXAMPLES)
    def test_example_has_cpp_code(self, example_file):
        content = (EXAMPLES_DIR / example_file).read_text(encoding="utf-8")
        assert "```cpp" in content or "```cmake" in content, \
            f"{example_file} missing C++/CMake code blocks"

    @pytest.mark.parametrize("example_file", PHASE9_EXAMPLES)
    def test_example_token_budget(self, example_file):
        content = (EXAMPLES_DIR / example_file).read_text(encoding="utf-8")
        # Strip YAML frontmatter — it is metadata and should not count against the content budget
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2]
        word_count = len(content.split())
        token_estimate = int(word_count * 1.3)
        assert token_estimate <= 600, \
            f"{example_file} exceeds 600-token budget: ~{token_estimate} tokens ({word_count} words)"


class TestLegacyCodeGuidance:
    """9.14: Legacy code navigation section and skill."""

    @pytest.fixture(autouse=True)
    def load(self):
        self.content = _read_full_reference()

    def test_section_exists(self):
        assert "Legacy Code Navigation" in self.content

    def test_characterization_tests_mentioned(self):
        assert "characterization test" in self.content.lower()

    def test_sprout_method_mentioned(self):
        assert "Sprout Method" in self.content

    def test_legacy_patterns_table(self):
        assert "auto_ptr" in self.content
        assert "unique_ptr" in self.content

    def test_debugging_tools_mentioned(self):
        assert "GDB" in self.content
        assert "Valgrind" in self.content

    def test_skill_development_path(self):
        assert "Phase 1" in self.content and "Phase 4" in self.content

    def test_legacy_skill_exists(self):
        skill = SKILLS_DIR / "skill-cpp-legacy-code-navigation.md"
        assert skill.exists(), "Missing skill-cpp-legacy-code-navigation.md"

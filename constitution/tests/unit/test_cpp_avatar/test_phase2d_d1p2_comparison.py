"""
Phase 2D — D1-P2: ENG-3.1-comparison-operators.md

Tests that the comparison operators example exists and covers the
full C++98 → C++20 progression: manual 6-operator pattern,
std::tie idiom for operator<, and operator<=> (spaceship) with
version callouts. This is a high-risk cross-version gap where
AI assistants silently default to C++20 spaceship operator for
teams that cannot use it.
"""

import pathlib
import pytest

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
EXAMPLES_DIR = CPP_DIR / "examples"

EXAMPLE = EXAMPLES_DIR / "ENG-3.1-comparison-operators.md"
INDEX   = EXAMPLES_DIR / "ENG-3.1-complexity.md"   # wrong; the ENG-3.1 family index to check


class TestD1P2ComparisonOperators:
    """D1-P2: ENG-3.1-comparison-operators.md — cross-version comparison guidance."""

    def test_example_file_exists(self):
        assert EXAMPLE.exists(), (
            "ENG-3.1-comparison-operators.md must exist (D1-P2)"
        )

    def test_cpp_version_min_is_98(self):
        content = EXAMPLE.read_text(encoding="utf-8")
        assert "cpp_version_min: 98" in content, (
            "Frontmatter must declare cpp_version_min: 98 — file covers C++98 patterns"
        )

    def test_covers_manual_six_operator_pattern(self):
        content = EXAMPLE.read_text(encoding="utf-8")
        assert "operator==" in content and "operator<" in content, (
            "Must demonstrate the C++98/11/14 manual 6-operator pattern"
        )

    def test_covers_std_tie_idiom(self):
        content = EXAMPLE.read_text(encoding="utf-8")
        assert "std::tie" in content, (
            "Must document the std::tie idiom for lexicographic operator< (C++11)"
        )

    def test_covers_spaceship_operator(self):
        content = EXAMPLE.read_text(encoding="utf-8")
        assert "operator<=>" in content or "<=>" in content, (
            "Must document C++20 spaceship operator with version callout"
        )

    def test_has_cpp20_version_callout(self):
        content = EXAMPLE.read_text(encoding="utf-8")
        assert "C++20" in content, (
            "Must have explicit C++20 callout for spaceship operator"
        )

    def test_has_non_compliant_section(self):
        content = EXAMPLE.read_text(encoding="utf-8")
        assert "NON-COMPLIANT" in content, (
            "Must show a NON-COMPLIANT pattern (partial comparison implementation)"
        )

    def test_has_edge_cases_section(self):
        content = EXAMPLE.read_text(encoding="utf-8")
        assert "## Edge Cases" in content, (
            "Must have Edge Cases section"
        )

    def test_index_references_comparison_example(self):
        # ENG-3.1 examples are referenced from their own ENG-3.1 example files
        # Check the ENG-3.1-complexity.md (the ENG-3.1 starting point) or any ENG-3.1 file
        # that acts as a router — look for the file referenced from any ENG-3.1 index
        found = False
        for f in EXAMPLES_DIR.glob("ENG-3.1-*.md"):
            if "ENG-3.1-comparison-operators.md" in f.read_text(encoding="utf-8"):
                found = True
                break
        assert found, (
            "At least one ENG-3.1-*.md file must reference ENG-3.1-comparison-operators.md"
        )

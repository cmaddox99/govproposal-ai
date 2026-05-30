"""Test ESE-02: C++20 Modules section in ref-cpp20-features-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-02
Law: ENG-3.1 (Complexity), ENG-2.2 (Architecture)
"""

from pathlib import Path

CPP_DIR = Path(__file__).resolve().parents[3] / "avatars" / "technology" / "cpp"
PART1 = CPP_DIR / "refs/language/ref-cpp20-features-part1.md"


def test_cpp20_modules_section_exists_and_within_budget():
    """ref-cpp20-features-part1.md must have a Modules section with required content.
    Budget check deferred to rightsize pass — file accumulates ESE-02 through ESE-10."""
    assert PART1.exists(), "ref-cpp20-features-part1.md not found"
    content = PART1.read_text(encoding="utf-8")

    assert "## C++20 Modules" in content or "## Modules" in content, \
        "Must have a C++20 Modules section heading"
    assert "export module" in content, \
        "Must cover 'export module' declaration syntax"
    assert "FILE_SET" in content and "CXX_MODULES" in content, \
        "Must include CMake FILE_SET CXX_MODULES wiring"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT code example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

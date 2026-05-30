"""Test ESE-09: constinit section in ref-cpp20-features-part3.md.

Scenario ID: cpp-external-sources-enrichment/ESE-09
Law: ENG-3.1 (Complexity), ENG-6.1 (Security — initialization-order fiasco)
"""

from pathlib import Path

PART1 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part3.md"
)


def test_cpp20_constinit_section_exists():
    """ref-cpp20-features-part3.md must have a constinit section covering:
    constinit vs constexpr vs const, initialization order fiasco prevention,
    mutable globals pattern. COMPLIANT + NON-COMPLIANT blocks required (ENG-4.1)."""
    content = PART1.read_text(encoding="utf-8")

    assert "## constinit" in content or "## `constinit`" in content, \
        "Must have a constinit section heading"
    assert "constinit" in content, \
        "Must cover constinit keyword"
    assert "constexpr" in content, \
        "Must compare constinit to constexpr"
    assert "initialization order" in content.lower() or \
           "static initialization order" in content.lower(), \
        "Must cover initialization order fiasco prevention"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

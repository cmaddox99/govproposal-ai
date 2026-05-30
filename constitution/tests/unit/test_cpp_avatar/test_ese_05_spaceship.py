"""Test ESE-05: Three-way comparison (spaceship operator) in ref-cpp20-features-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-05
Law: ENG-3.1 (Complexity), ENG-3.2 (Immutability — value types)
"""

from pathlib import Path

PART1 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part1.md"
)


def test_cpp20_spaceship_section_exists():
    """ref-cpp20-features-part1.md must have a spaceship operator section covering
    ordering categories, defaulted operator<=>, interaction with operator==,
    and migration from manual comparison operators. COMPLIANT + NON-COMPLIANT (ENG-4.1)."""
    content = PART1.read_text(encoding="utf-8")

    assert "## Three-way" in content or "## Spaceship" in content or \
           "spaceship" in content.lower(), \
        "Must have a three-way comparison / spaceship section"
    assert "strong_ordering" in content, \
        "Must cover std::strong_ordering ordering category"
    assert "weak_ordering" in content, \
        "Must cover std::weak_ordering ordering category"
    assert "partial_ordering" in content, \
        "Must cover std::partial_ordering (e.g. for NaN-equivalent values)"
    assert "operator<=>" in content, \
        "Must show operator<=> syntax"
    assert "= default" in content, \
        "Must show auto operator<=>(...) = default pattern"
    assert "FlightId" in content or "RouteKey" in content, \
        "Must include an AA domain value type example"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

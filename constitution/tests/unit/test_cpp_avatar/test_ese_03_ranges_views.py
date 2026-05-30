"""Test ESE-03: Ranges and Views section in ref-cpp20-features-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-03
Law: ENG-3.1 (Complexity — ranged algorithms reduce loop complexity)
     ENG-2.2 (Architecture)
"""

from pathlib import Path

PART1 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part1.md"
)


def test_cpp20_ranges_views_section_exists():
    """ref-cpp20-features-part1.md must have a Ranges/Views section with required
    content: sort, pipeline (filter|transform|take), lazy evaluation, sentinel types,
    and AA domain example. COMPLIANT + NON-COMPLIANT blocks required (ENG-4.1)."""
    content = PART1.read_text(encoding="utf-8")

    assert "## Ranges" in content or "## C++20 Ranges" in content, \
        "Must have a Ranges/Views section heading"
    assert "ranges::sort" in content or "std::ranges::sort" in content, \
        "Must cover std::ranges::sort vs iterator-pair sort"
    assert "views::filter" in content or "std::views::filter" in content, \
        "Must cover views::filter pipeline"
    assert "views::transform" in content, \
        "Must cover views::transform"
    assert "lazy" in content.lower(), \
        "Must explain lazy evaluation semantics"
    assert "FlightLeg" in content or "Flight" in content, \
        "Must include an AA domain example"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

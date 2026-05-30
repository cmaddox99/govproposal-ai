"""Test ESE-04: std::span governance section in ref-cpp20-features-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-04
Law: ENG-6.1 (Security — bounds-safe APIs), ENG-3.1 (Complexity)
"""

from pathlib import Path

PART1 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part1.md"
)


def test_cpp20_span_section_exists():
    """ref-cpp20-features-part1.md must have a std::span section covering:
    non-owning view, subspan, function signature replacement for pointer+count,
    const-span for read-only APIs. COMPLIANT + NON-COMPLIANT blocks (ENG-4.1)."""
    content = PART1.read_text(encoding="utf-8")

    assert "## std::span" in content or "## `std::span`" in content, \
        "Must have a std::span section heading"
    assert "non-owning" in content.lower() or "non owning" in content.lower(), \
        "Must describe span as a non-owning view"
    assert "subspan" in content or "sub_span" in content, \
        "Must cover subspan patterns"
    assert "span<const" in content or "span<const T" in content, \
        "Must cover std::span<const T> for read-only APIs"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

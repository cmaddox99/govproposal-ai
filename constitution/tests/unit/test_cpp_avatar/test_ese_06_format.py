"""Test ESE-06: std::format section in ref-cpp20-features-part3.md.

Scenario ID: cpp-external-sources-enrichment/ESE-06
Law: ENG-6.1 (Security — type-safe formatting), ENG-6.5 (Input validation)
"""

from pathlib import Path

PART1 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part3.md"
)


def test_cpp20_format_section_exists():
    """ref-cpp20-features-part3.md must have a std::format section covering:
    format vs printf/sprintf, format_to for output iterators, custom formatter
    specialisation, vformat hazard. COMPLIANT + NON-COMPLIANT blocks (ENG-4.1)."""
    content = PART1.read_text(encoding="utf-8")

    assert "## std::format" in content or "## `std::format`" in content, \
        "Must have a std::format section heading"
    assert "std::format" in content, \
        "Must cover std::format usage"
    assert "printf" in content or "sprintf" in content, \
        "Must compare std::format to printf/sprintf"
    assert "format_to" in content or "std::format_to" in content, \
        "Must cover std::format_to for output iterators"
    assert "std::formatter" in content or "formatter<" in content, \
        "Must cover custom std::formatter<T> specialisation"
    assert "vformat" in content, \
        "Must cover std::vformat and why to avoid it"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

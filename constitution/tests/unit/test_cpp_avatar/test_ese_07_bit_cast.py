"""Test ESE-07: std::bit_cast section in ref-cpp20-features-part3.md.

Scenario ID: cpp-external-sources-enrichment/ESE-07
Law: ENG-6.1 (Security — no reinterpret_cast without justification), ENG-3.1
"""

from pathlib import Path

PART1 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part3.md"
)


def test_cpp20_bit_cast_section_exists():
    """ref-cpp20-features-part3.md must have a std::bit_cast section covering:
    type-safe type-punning, constraints, IEEE-754 inspection, binary protocol
    parsing. COMPLIANT + NON-COMPLIANT blocks required (ENG-4.1)."""
    content = PART1.read_text(encoding="utf-8")

    assert "## std::bit_cast" in content or "## `std::bit_cast`" in content, \
        "Must have a std::bit_cast section heading"
    assert "bit_cast" in content, \
        "Must cover std::bit_cast usage"
    assert "reinterpret_cast" in content, \
        "Must compare to reinterpret_cast / memcpy type-punning"
    assert "trivially_copyable" in content or "trivially copyable" in content.lower(), \
        "Must state the trivially-copyable constraint"
    assert "ACARS" in content or "ADS-B" in content or "IEEE" in content, \
        "Must include binary protocol / IEEE-754 domain example"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

"""Test ESE-10: std::atomic_ref section in ref-cpp20-features-part3.md.

Scenario ID: cpp-external-sources-enrichment/ESE-10
Law: ENG-6.1 (Security — thread safety), ENG-3.1 (Complexity)
"""

from pathlib import Path

PART1 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part3.md"
)


def test_cpp20_atomic_ref_section_exists():
    """ref-cpp20-features-part3.md must have an atomic_ref section covering:
    atomic access to non-atomic objects, ABI-preservation brownfield use case,
    alignment constraint. COMPLIANT + NON-COMPLIANT blocks required (ENG-4.1)."""
    content = PART1.read_text(encoding="utf-8")

    assert "## std::atomic_ref" in content or "## `std::atomic_ref`" in content, \
        "Must have a std::atomic_ref section heading"
    assert "atomic_ref" in content, \
        "Must cover std::atomic_ref usage"
    assert "ABI" in content or "abi" in content.lower(), \
        "Must cover ABI-preservation brownfield use case"
    assert "alignment" in content.lower() or "trivially" in content.lower(), \
        "Must state alignment / trivially-copyable constraint"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

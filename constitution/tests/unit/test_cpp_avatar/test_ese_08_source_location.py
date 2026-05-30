"""Test ESE-08: std::source_location section in ref-cpp20-features-part3.md.

Scenario ID: cpp-external-sources-enrichment/ESE-08
Law: ENG-6.7 (Audit Trail), ENG-5.5 (Observability)
"""

from pathlib import Path

PART1 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part3.md"
)


def test_cpp20_source_location_section_exists():
    """ref-cpp20-features-part3.md must have a std::source_location section covering:
    current() as default parameter, comparison with __FILE__/__LINE__ macros,
    audit logging use. COMPLIANT + NON-COMPLIANT blocks required (ENG-4.1)."""
    content = PART1.read_text(encoding="utf-8")

    assert "## std::source_location" in content or \
           "## `std::source_location`" in content or \
           "source_location" in content, \
        "Must have a std::source_location section"
    assert "current()" in content, \
        "Must cover std::source_location::current() as default parameter"
    assert "__FILE__" in content or "__LINE__" in content, \
        "Must compare to __FILE__/__LINE__ macros"
    assert "ENG-6.7" in content or "audit" in content.lower(), \
        "Must connect to ENG-6.7 audit trail or structured logging"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

"""Test ESE-12: ENG-3.1-ranges-views.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-12
Law: ENG-3.1 (Complexity — ranged algorithms reduce loop complexity)
"""

from pathlib import Path

EXAMPLES = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples"
)
EXAMPLE = EXAMPLES / "ENG-3.1-ranges-views.md"


def test_ranges_views_example_exists_and_valid():
    """ENG-3.1-ranges-views.md must exist, cover COMPLIANT pipeline and NON-COMPLIANT
    manual loop, address infinite range and dangling view edge cases, and stay within
    700-token budget (ENG-3.1)."""
    assert EXAMPLE.exists(), "ENG-3.1-ranges-views.md not found in examples/"

    content = EXAMPLE.read_text(encoding="utf-8")

    assert "ENG-3.1" in content, "Must reference ENG-3.1"
    assert "views" in content or "ranges" in content, \
        "Must cover std::views / ranges pipeline"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    assert "infinite" in content.lower() or "unbounded" in content.lower(), \
        "Must address infinite/unbounded range edge case"
    assert "dangling" in content.lower() or "temporary" in content.lower(), \
        "Must address dangling view / temporary range edge case"
    assert len(content) // 4 <= 700, \
        f"Example exceeds 700-token budget (got {len(content) // 4})"

"""Test ESE-14: ENG-3.2-spaceship-operator.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-14
Law: ENG-3.2 (Immutability / value-type consistency — defaulted <=>)
"""

from pathlib import Path

EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples/ENG-3.2-spaceship-operator.md"
)


def test_spaceship_example_valid():
    """Must cover: defaulted <=> for FlightId, custom partial_ordering with
    UNKNOWN sentinel, explicit == when needed, NON-COMPLIANT six-operator
    hand-roll, and partial_ordering NaN-like edge case. ≤ 700 tokens."""
    assert EXAMPLE.exists(), "ENG-3.2-spaceship-operator.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    # Require actual code examples, not just frontmatter mentions
    assert content.count("```cpp") >= 2, \
        "Must have at least 2 cpp code blocks"
    assert "auto operator<=>" in content or "= default" in content, \
        "Must show defaulted <=> in a code block"
    assert "partial_ordering" in content, "Must cover partial_ordering"
    assert "UNKNOWN" in content or "sentinel" in content.lower(), \
        "Must address UNKNOWN/sentinel edge case"
    assert "COMPLIANT" in content, "Must have COMPLIANT section"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT section"
    # Must show actual code — stub has only placeholders
    assert "Placeholder" not in content, \
        "File must be filled in (no placeholder text)"
    assert len(content) // 4 <= 700, \
        f"Exceeds 700-token budget (got {len(content) // 4})"

"""Test ESE-15: ENG-6.1-span-bounds-safety.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-15
Law: ENG-6.1 (Security by Design — span replaces raw pointer+size)
"""

from pathlib import Path

EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples/ENG-6.1-span-bounds-safety.md"
)


def test_span_bounds_safety_example_valid():
    """Must cover: COMPLIANT span<const SeatData> function signature with
    subspan, std::as_bytes for serialization; NON-COMPLIANT raw pointer+size;
    edge cases: empty span, dangling span from temporary, span-of-span.
    No placeholder text. <= 700 tokens."""
    assert EXAMPLE.exists(), "ENG-6.1-span-bounds-safety.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert "Placeholder" not in content, "File must be filled in"
    assert content.count("```cpp") >= 2, "Must have at least 2 cpp code blocks"
    assert "span" in content, "Must reference std::span"
    assert "subspan" in content, "Must show subspan usage"
    assert "as_bytes" in content, "Must show std::as_bytes for serialization"
    assert "COMPLIANT" in content, "Must have COMPLIANT section"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT section"
    # Edge cases per spec
    assert "empty" in content.lower(), "Must address empty span edge case"
    assert "dangling" in content.lower() or "temporary" in content.lower(), \
        "Must address dangling span / temporary edge case"
    assert len(content) // 4 <= 700, \
        f"Exceeds 700-token budget (got {len(content) // 4})"

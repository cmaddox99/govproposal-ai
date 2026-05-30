"""Test ESE-16: ENG-6.1-std-format.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-16
Law: ENG-6.1 (Security by Design — std::format eliminates printf injection risk)
"""

from pathlib import Path

EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples/ENG-6.1-std-format.md"
)


def test_std_format_example_valid():
    """Must cover: COMPLIANT std::format for audit log; NON-COMPLIANT sprintf;
    custom std::formatter<FlightId> specialisation; std::vformat runtime hazard
    warning. No placeholder text. <= 700 tokens."""
    assert EXAMPLE.exists(), "ENG-6.1-std-format.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert "Placeholder" not in content, "File must be filled in"
    assert content.count("```cpp") >= 2, "Must have at least 2 cpp code blocks"
    assert "std::format" in content, "Must show std::format usage"
    assert "sprintf" in content, "Must show NON-COMPLIANT sprintf"
    assert "formatter" in content, "Must show std::formatter specialisation"
    assert "vformat" in content, "Must address std::vformat hazard"
    assert "COMPLIANT" in content, "Must have COMPLIANT section"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT section"
    assert len(content) // 4 <= 700, \
        f"Exceeds 700-token budget (got {len(content) // 4})"

"""Test ESE-18: ENG-6.1-parallel-algorithms.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-18
Law: ENG-6.1 (Security by Design — correct execution policy prevents data races)
cpp_version_min: 17
"""

from pathlib import Path

EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples/ENG-6.1-parallel-algorithms.md"
)


def test_parallel_algorithms_example_valid():
    """Must cover: COMPLIANT par_unseq for batch transform; seq for tests;
    par for I/O-constrained; NON-COMPLIANT order assumption with par_unseq;
    edge cases: exception propagation, shared mutable state data race,
    alignment/SIMD note. <= 700 tokens."""
    assert EXAMPLE.exists(), "ENG-6.1-parallel-algorithms.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert content.count("```cpp") >= 2, "Must have at least 2 cpp code blocks"
    assert "par_unseq" in content, "Must cover par_unseq policy"
    assert "par" in content, "Must cover par policy"
    assert "seq" in content, "Must cover seq policy"
    assert "exception" in content.lower(), "Must address exception propagation"
    assert "COMPLIANT" in content, "Must have COMPLIANT section"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT section"
    assert "data race" in content.lower() or "shared mutable" in content.lower(), \
        "Must address data race with shared mutable state"
    assert len(content) // 4 <= 700, \
        f"Exceeds 700-token budget (got {len(content) // 4})"

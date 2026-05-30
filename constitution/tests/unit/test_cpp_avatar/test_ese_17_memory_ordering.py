"""Test ESE-17: ENG-6.1-memory-ordering.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-17
Law: ENG-6.1 (Security by Design — correct memory ordering prevents data races)
cpp_version_min: 11
"""

from pathlib import Path

EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples/ENG-6.1-memory-ordering.md"
)


def test_memory_ordering_example_valid():
    """Must cover: all five memory_order values with happens-before reasoning;
    COMPLIANT acquire/release producer-consumer; COMPLIANT relaxed for
    independent counter; NON-COMPLIANT relaxed for dependent read (broken
    happens-before); acq_rel for RMW; seq_cst cost note. <= 700 tokens."""
    assert EXAMPLE.exists(), "ENG-6.1-memory-ordering.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert content.count("```cpp") >= 2, "Must have at least 2 cpp code blocks"
    assert "memory_order_acquire" in content, "Must cover acquire"
    assert "memory_order_release" in content, "Must cover release"
    assert "memory_order_relaxed" in content, "Must cover relaxed"
    assert "memory_order_seq_cst" in content or "seq_cst" in content, \
        "Must cover seq_cst"
    assert "acq_rel" in content, "Must cover acq_rel for RMW"
    assert "happens-before" in content.lower() or "happens before" in content.lower(), \
        "Must explain happens-before"
    assert "COMPLIANT" in content, "Must have COMPLIANT section"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT section"
    assert len(content) // 4 <= 700, \
        f"Exceeds 700-token budget (got {len(content) // 4})"

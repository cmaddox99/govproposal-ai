"""Test ESE-26: False Sharing and Cache Line Alignment section in
ref-concurrency-advanced-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-26
Law: ENG-6.1 (Security by Design — data race prevention)
cpp_version_min: 17
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-concurrency-advanced-part1.md"
)


def test_false_sharing_section_exists():
    """ref-concurrency-advanced-part1.md must contain false sharing section:
    definition, 64-byte cache line, hardware_destructive_interference_size,
    per-thread stats accumulator example, COMPLIANT/NON-COMPLIANT, budget ok."""
    assert REF.exists(), "ref-concurrency-advanced-part1.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "false sharing" in content.lower(), "Must define false sharing"
    assert "hardware_destructive_interference_size" in content, \
        "Must show alignas(hardware_destructive_interference_size)"
    assert "64" in content, "Must mention 64-byte cache line"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    assert len(content) // 4 <= 3500, \
        f"ref-concurrency-advanced-part1.md exceeds 3500-token budget (got {len(content)//4})"

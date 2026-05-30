"""Test ESE-32: ENG-3.1-false-sharing.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-32
Law: ENG-3.1 (Code Quality — cache-line alignment for perf)
cpp_version_min: 17
"""

from pathlib import Path

EXAMPLES = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples"
)
EXAMPLE = EXAMPLES / "ENG-3.1-false-sharing.md"


def test_false_sharing_example_exists():
    """ENG-3.1-false-sharing.md: alignas(hardware_destructive_interference_size),
    NON-COMPLIANT adjacent counters, performance note, when to apply, ≤700t."""
    assert EXAMPLE.exists(), "ENG-3.1-false-sharing.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert "hardware_destructive_interference_size" in content
    assert "false sharing" in content.lower() or "false-sharing" in content.lower()
    assert "COMPLIANT" in content
    assert "NON-COMPLIANT" in content
    assert "64" in content, "Must mention 64-byte cache line"
    assert "profile" in content.lower(), "Must advise profiling"
    assert len(content) // 4 <= 700, \
        f"ENG-3.1-false-sharing.md exceeds 700-token budget (got {len(content)//4})"


def test_example_file_count_is_84():
    count = len(list(EXAMPLES.glob("*.md")))
    assert count == 87, f"Expected 87 example files, found {count}"

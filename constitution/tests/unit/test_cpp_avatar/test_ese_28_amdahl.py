"""Test ESE-28: Amdahl's Law and Gustafson's Law section in
ref-concurrency-advanced-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-28
Law: ENG-6.1 (Security by Design — informed parallelism decisions)
cpp_version_min: 11
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-concurrency-advanced-part1.md"
)


def test_amdahl_gustafson_section_exists():
    """ref-concurrency-advanced-part1.md must contain Amdahl's/Gustafson's
    section: Amdahl equation, 5x speedup at 20% serial example,
    Gustafson's law, when-not-to-parallelize, profiling guidance,
    AA crew/fare context, within budget."""
    assert REF.exists(), "ref-concurrency-advanced-part1.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "Amdahl" in content, "Must cover Amdahl's Law"
    assert "Gustafson" in content, "Must cover Gustafson's Law"
    assert "serial fraction" in content.lower() or "serial" in content.lower(), \
        "Must explain serial fraction bottleneck"
    assert "5" in content and "20" in content, \
        "Must give 20% serial → max 5x speedup example"
    assert "profile" in content.lower(), \
        "Must advise profiling before parallelising"
    assert "crew" in content.lower() or "fare" in content.lower(), \
        "Must reference AA crew/fare domain"
    assert len(content) // 4 <= 3500, \
        f"ref-concurrency-advanced-part1.md exceeds 3500-token budget (got {len(content)//4})"

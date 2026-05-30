"""Test ESE-23: Condition Variable Patterns section in
ref-concurrency-advanced-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-23
Law: ENG-6.1 (Security by Design — data race prevention)
cpp_version_min: 11
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-concurrency-advanced-part1.md"
)


def test_condition_variable_patterns_section_exists():
    """ref-concurrency-advanced-part1.md must contain condition variable
    patterns: predicate-protected wait, spurious wakeup protection,
    wait_for with timeout, producer-consumer example, NON-COMPLIANT bare
    wait(), CP.42 citation. No stub placeholder."""
    assert REF.exists(), "ref-concurrency-advanced-part1.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "Stub" not in content, "Section must be filled (no Stub marker)"
    assert "Placeholder" not in content, "Placeholder must be removed"
    assert "condition_variable" in content, "Must cover condition_variable"
    assert "spurious" in content, "Must explain spurious wakeup protection"
    assert "CP.42" in content, "Must cite Core Guidelines CP.42"
    assert "wait_for" in content, "Must show wait_for with timeout"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    assert content.count("```cpp") >= 2, "Must have at least 2 code blocks"
    # Budget: ref files ≤ 3500 tokens
    assert len(content) // 4 <= 3500, \
        f"ref-concurrency-advanced-part1.md exceeds 3500-token budget (got {len(content)//4})"

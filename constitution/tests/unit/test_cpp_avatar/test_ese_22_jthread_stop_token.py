"""Test ESE-22: std::jthread and std::stop_token section in
ref-concurrency-advanced-part2.md.

Scenario ID: cpp-external-sources-enrichment/ESE-22
Law: ENG-6.1 (Security — jthread prevents thread-not-joined UB)
cpp_version_min: 20
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-concurrency-advanced-part2.md"
)


def test_jthread_stop_token_section_exists():
    """ref-concurrency-advanced-part2.md must contain jthread section:
    auto-join on destruction, stop_token cooperative cancellation,
    stop_callback for cleanup, migration from thread+atomic<bool>,
    AA domain example (fare-search), CP.25 citation. No stub placeholder."""
    assert REF.exists(), "ref-concurrency-advanced-part2.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "Stub" not in content, "Section must be filled in (no Stub marker)"
    assert "jthread" in content, "Must cover std::jthread"
    assert "stop_token" in content, "Must cover stop_token"
    assert "stop_callback" in content, "Must cover stop_callback for cleanup"
    assert "atomic<bool>" in content or "atomic_bool" in content, \
        "Must show migration from thread+atomic<bool> stop flag"
    assert "CP.25" in content, "Must cite Core Guidelines CP.25"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    # File must stay within 3500-token budget
    assert len(content) // 4 <= 3500, \
        f"ref-concurrency-advanced-part2.md exceeds 3500-token budget (got {len(content)//4})"

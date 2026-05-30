"""Test ESE-27: std::promise and std::future Patterns section in
ref-concurrency-advanced-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-27
Law: ENG-6.1 (Security by Design — safe async result passing)
cpp_version_min: 11
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-concurrency-advanced-part1.md"
)


def test_promise_future_section_exists():
    """ref-concurrency-advanced-part1.md must contain promise/future section:
    promise<T>/future<T>, packaged_task, shared_future, set_exception,
    wait_for timeout, AA fare availability example, NON-COMPLIANT, budget ok."""
    assert REF.exists(), "ref-concurrency-advanced-part1.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "promise" in content, "Must cover std::promise"
    assert "future" in content, "Must cover std::future"
    assert "packaged_task" in content, "Must mention packaged_task"
    assert "shared_future" in content, "Must mention shared_future"
    assert "set_exception" in content, "Must show exception propagation"
    assert "wait_for" in content, "Must show wait_for timeout pattern"
    assert "fare" in content.lower(), "Must include AA fare availability example"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    assert len(content) // 4 <= 3500, \
        f"ref-concurrency-advanced-part1.md exceeds 3500-token budget (got {len(content)//4})"

"""Test ESE-25: Thread Pool and Work-Stealing section in
ref-concurrency-advanced-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-25
Law: ENG-6.1 (Security by Design — safe thread management)
cpp_version_min: 11
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-concurrency-advanced-part1.md"
)


def test_thread_pool_work_stealing_section_exists():
    """ref-concurrency-advanced-part1.md must contain a thread pool section:
    producer-consumer thread pool skeleton, work-stealing concept,
    std::async vs new threads, AA domain (crew pairing), CP.41 citation,
    NON-COMPLIANT unbounded thread creation. No Stub/Placeholder."""
    assert REF.exists(), "ref-concurrency-advanced-part1.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "thread pool" in content.lower(), "Must cover thread pool pattern"
    assert "work-steal" in content.lower() or "work steal" in content.lower(), \
        "Must cover work-stealing concept"
    assert "std::async" in content, "Must discuss std::async"
    assert "CP.41" in content, "Must cite Core Guidelines CP.41"
    assert "crew" in content.lower(), "Must include AA crew pairing domain example"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    # Budget: ref files ≤ 3500 tokens
    assert len(content) // 4 <= 3500, \
        f"ref-concurrency-advanced-part1.md exceeds 3500-token budget (got {len(content)//4})"

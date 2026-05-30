"""Test ESE-24: Lock-free Data Structures section in
ref-concurrency-advanced-part1.md.

Scenario ID: cpp-external-sources-enrichment/ESE-24
Law: ENG-6.1 (Security by Design — data race prevention)
cpp_version_min: 11
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-concurrency-advanced-part1.md"
)


def test_lock_free_data_structures_section_exists():
    """ref-concurrency-advanced-part1.md must contain a lock-free section:
    lock-free concept explanation, cache line contention warning,
    ABA problem, SPSC ring buffer pattern, atomic<shared_ptr> with
    is_lock_free() caveat, profiling warning. Must NOT claim
    atomic<shared_ptr> is unconditionally lock-free."""
    assert REF.exists(), "ref-concurrency-advanced-part1.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "Lock-free" in content or "lock-free" in content, \
        "Must have Lock-free section"
    assert "ABA" in content, "Must document ABA problem"
    assert "SPSC" in content or "ring buffer" in content.lower(), \
        "Must show SPSC ring buffer pattern"
    assert "is_lock_free" in content, \
        "Must show is_lock_free() check for atomic<shared_ptr>"
    # Correctness guard: must NOT claim atomic<shared_ptr> is lock-free
    assert "lock-free node update" not in content, \
        "Must not claim atomic<shared_ptr> is unconditionally lock-free"
    assert "profile" in content.lower(), \
        "Must warn to profile before using lock-free"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    # Budget: ref files ≤ 3500 tokens
    assert len(content) // 4 <= 3500, \
        f"ref-concurrency-advanced-part1.md exceeds 3500-token budget (got {len(content)//4})"

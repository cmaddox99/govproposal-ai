"""Tests: Concurrency blocking bug fixes — B1, B2, B3.

Scenario ID: cpp-version-routing-foundation/concurrency-bugs-B1-B2-B3
Law: ENG-4.1 (Atomic TDD), ENG-6.1 (Security by Design — correctness)

B1: with_timeout() std::future destructor blocks on timeout — must be documented
B2: ENG-7.5 cpp_version_min:17 but code uses C++20 std::counting_semaphore
B3: ref-concurrency-threading.md primary GOOD example is C++17, in transitional prefer
"""

import re as _re
import yaml as _yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
_CPP_EXAMPLES = REPO_ROOT / "avatars" / "technology" / "cpp" / "examples"
_CPP_REFS     = REPO_ROOT / "avatars" / "technology" / "cpp" / "refs"
_RAG_INDEX    = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"


def _parse_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return _yaml.safe_load(parts[1]) or {}
    except Exception:
        return {}


def _cpp_section(content: str) -> str:
    import re
    start = content.index("  cpp:")
    m = re.search(r"\n  [a-z]", content[start + 6:])
    end = start + 6 + m.start() if m else len(content)
    return content[start:end]


# ===========================================================================
# B2 — ENG-7.5 frontmatter version mismatch
# ===========================================================================

def test_eng75_bulkhead_cpp_version_min_is_20():
    """B2a: ENG-7.5 must declare cpp_version_min: 20, not 17.

    The implementation uses std::counting_semaphore<> from <semaphore> which
    is C++20 only. The frontmatter previously said cpp_version_min: 17 because
    the note author focused on std::optional. std::counting_semaphore is the
    binding constraint — it determines the minimum standard.
    """
    path = _CPP_EXAMPLES / "ENG-7.5-bulkhead-isolation.md"
    assert path.exists(), "ENG-7.5-bulkhead-isolation.md must exist"
    fm = _parse_frontmatter(path.read_text(encoding="utf-8"))
    version_min = fm.get("cpp_version_min")
    assert version_min == 20, (
        f"ENG-7.5 uses std::counting_semaphore (<semaphore> header, C++20 only). "
        f"cpp_version_min must be 20, not {version_min!r}. "
        "Fix: change frontmatter to 'cpp_version_min: 20' and update cpp_version_note."
    )


def test_eng75_bulkhead_has_pre_cpp20_fallback():
    """B2b: ENG-7.5 must include a C++11/17 fallback for the bulkhead pattern.

    std::counting_semaphore requires C++20. Transitional (C++11/14) teams need
    a condition_variable-based alternative. Without a fallback, ~60% of AA LOC
    (IOC_ALP, hte_pm_hostconn, CWR) has no compliant bulkhead implementation.
    """
    path = _CPP_EXAMPLES / "ENG-7.5-bulkhead-isolation.md"
    content = path.read_text(encoding="utf-8")
    # Must provide a condition_variable-based implementation — presence of C++17/C++11
    # anywhere (e.g., in frontmatter note) is NOT sufficient
    assert "condition_variable" in content, (
        "ENG-7.5 must include a std::condition_variable-based semaphore fallback "
        "for C++11/14/17 teams who cannot use std::counting_semaphore (C++20). "
        "See PHASE2-PROPOSAL.md item A2 for the required pattern."
    )


def test_eng75_version_note_mentions_semaphore():
    """B2c: ENG-7.5 cpp_version_note must mention counting_semaphore as the constraint."""
    path = _CPP_EXAMPLES / "ENG-7.5-bulkhead-isolation.md"
    fm = _parse_frontmatter(path.read_text(encoding="utf-8"))
    note = str(fm.get("cpp_version_note", ""))
    assert "semaphore" in note.lower() or "counting_semaphore" in note.lower(), (
        "ENG-7.5 cpp_version_note must mention counting_semaphore as the C++20 constraint. "
        "The previous note only mentioned std::optional which is C++17, missing the real "
        f"minimum. Current note: {note!r}"
    )


# ===========================================================================
# B3 — ref-concurrency-threading.md primary example must be C++11 compatible
# ===========================================================================

def test_concurrency_threading_ref_primary_good_example_uses_lock_guard():
    """B3a: Primary GOOD example in ref-concurrency-threading.md must use lock_guard (C++11).

    The file is the first result for transitional (C++11/14) threading queries.
    The previous primary GOOD example used std::scoped_lock (C++17) as the FIRST
    and only guard shown — misleading C++11/14 teams into thinking scoped_lock is
    universally available.

    The fix: lead with std::lock_guard (C++11), then introduce std::scoped_lock
    as a C++17 upgrade. The test checks that lock_guard appears before scoped_lock
    in the first GOOD code block.
    """
    path = _CPP_REFS / "safety" / "ref-concurrency-threading.md"
    assert path.exists(), "ref-concurrency-threading.md must exist"
    content = path.read_text(encoding="utf-8")

    # Find the first GOOD code block
    first_good = _re.search(r"(?s)// GOOD.*?```", content)
    assert first_good, "ref-concurrency-threading.md must have at least one // GOOD example"
    first_good_block = first_good.group(0)

    assert "lock_guard" in first_good_block, (
        "The primary GOOD example in ref-concurrency-threading.md must use "
        "std::lock_guard (C++11) before introducing std::scoped_lock (C++17). "
        "Transitional teams (C++11/14) see this file first via prefer routing. "
        "Current first GOOD block: \n" + first_good_block[:300]
    )


def test_concurrency_threading_ref_has_version_callout_for_scoped_lock():
    """B3b: ref-concurrency-threading.md must label std::scoped_lock as C++17.

    scoped_lock is an upgrade over lock_guard that should be clearly marked as
    C++17+. Without this label, transitional teams don't know it's unavailable.
    """
    path = _CPP_REFS / "safety" / "ref-concurrency-threading.md"
    content = path.read_text(encoding="utf-8")

    assert "scoped_lock" in content, "scoped_lock should still appear (as C++17 upgrade)"
    # scoped_lock must be accompanied by a C++17 label somewhere in the file
    scoped_lock_pos = content.index("scoped_lock")
    surrounding = content[max(0, scoped_lock_pos - 200): scoped_lock_pos + 200]
    has_version_label = "C++17" in surrounding or "17" in surrounding
    assert has_version_label, (
        "std::scoped_lock in ref-concurrency-threading.md must be accompanied by "
        "a C++17 version label within 200 characters. Transitional teams must know "
        "this is not available in C++11/14. "
        f"Context around first scoped_lock: {surrounding!r}"
    )


def test_transitional_prefer_concurrency_threading_only_if_cpp11_primary():
    """B3c: If ref-concurrency-threading.md is in transitional prefer, its primary example must be C++11.

    This test acts as a guard: if the file is removed from transitional.prefer,
    the test passes trivially. If it remains, the primary GOOD example must use
    lock_guard (C++11) — B3a already enforces this, but this test makes the
    routing/content coupling explicit.
    """
    path = _CPP_REFS / "safety" / "ref-concurrency-threading.md"
    content = path.read_text(encoding="utf-8")
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))

    transitional_start = cpp_section.index("transitional:") if "transitional:" in cpp_section else -1
    if transitional_start == -1:
        return  # no transitional tier — nothing to check

    # Find transitional prefer block
    transitional_block = cpp_section[transitional_start:]
    modern_start = transitional_block.find("modern:")
    if modern_start != -1:
        transitional_block = transitional_block[:modern_start]

    threading_ref_in_prefer = "ref-concurrency-threading.md" in transitional_block

    if threading_ref_in_prefer:
        # If it's in the prefer list, the primary GOOD example MUST be lock_guard
        first_good = _re.search(r"(?s)// GOOD.*?```", content)
        assert first_good and "lock_guard" in first_good.group(0), (
            "ref-concurrency-threading.md is in transitional.prefer but its primary "
            "GOOD example does not use std::lock_guard (C++11). Either: "
            "(a) remove from transitional.prefer, or "
            "(b) make lock_guard the primary GOOD example (before scoped_lock). "
            "See PHASE2-PROPOSAL.md item A3."
        )


# ===========================================================================
# B1 — with_timeout() std::future destructor blocking behavior
# ===========================================================================

def test_eng74_timeout_documents_future_destructor_blocking():
    """B1a: ENG-7.4 must document the std::future destructor blocking hazard.

    std::async(std::launch::async) returns a future whose destructor BLOCKS until
    the launched task completes (C++ standard [futures.future.dtor]). When
    with_timeout() returns std::nullopt on timeout, the future goes out of scope
    and its destructor immediately blocks — negating the timeout entirely.

    This is a subtle stdlib pitfall documented in Effective Modern C++ (Item 38).
    The file must warn developers explicitly so they don't copy this as a
    production timeout pattern.
    """
    path = _CPP_EXAMPLES / "ENG-7.4-timeout-governance.md"
    assert path.exists(), "ENG-7.4-timeout-governance.md must exist"
    content = path.read_text(encoding="utf-8")

    # Must contain a caution about the destructor / blocking behavior
    has_warning = (
        "destructor" in content.lower()
        or "⚠️" in content and "future" in content.lower() and "destructor" in content.lower()
        or "Item 38" in content
    )
    assert has_warning, (
        "ENG-7.4-timeout-governance.md must warn that std::future from std::async "
        "blocks in its destructor when the task has not completed. "
        "The with_timeout() pattern returns nullopt on timeout but the future "
        "destructor then BLOCKS — this is not a real timeout. "
        "Add a ⚠️ CAUTION note explaining this limitation. "
        "Reference: Effective Modern C++ Item 38; C++ standard [futures.future.dtor]."
    )


def test_eng74_timeout_recommends_api_native_or_cooperative_cancel():
    """B1b: ENG-7.4 must recommend API-native timeouts or cooperative cancellation.

    Since std::future-based timeout is broken, the file must guide developers
    toward a correct alternative: API-native timeouts (gRPC deadline, socket
    SO_TIMEOUT, HTTP client timeout) or cooperative cancellation via stop_token
    or a shared atomic stop flag.
    """
    path = _CPP_EXAMPLES / "ENG-7.4-timeout-governance.md"
    content = path.read_text(encoding="utf-8")

    has_alternative = (
        "stop_token" in content
        or "stop_flag" in content
        or "SO_TIMEOUT" in content
        or "deadline" in content.lower() and "grpc" in content.lower()
        or "API-native" in content
        or "api-native" in content.lower()
        or "cooperative" in content.lower()
    )
    assert has_alternative, (
        "ENG-7.4-timeout-governance.md must recommend at least one correct timeout "
        "alternative to the broken std::future pattern: "
        "(a) API-native timeouts (gRPC deadline, socket SO_TIMEOUT), "
        "(b) cooperative cancellation with std::stop_token (C++20), or "
        "(c) shared std::atomic<bool> stop flag (C++11). "
        "Developers need a path forward, not just a warning."
    )

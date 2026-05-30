"""
Phase 2B concurrency coverage tests.
C3 — token estimate accuracy in RAG index (±10% tolerance)
C5 — pre-C++20 bulkhead fallback in ref-concurrency-async.md
C2 — coroutines extracted to separate file; threading ref stays clean
C1 — brownfield concurrency ref exists with C++98/POSIX patterns
"""

import pathlib
import re
import pytest
import yaml

CPP_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "technology" / "cpp"
REFS_DIR = CPP_DIR / "refs"
RAG_INDEX = pathlib.Path(__file__).parent.parent.parent.parent / "avatars" / "AVATAR-RAG-INDEX.yaml"


def _token_estimate(path: pathlib.Path) -> int:
    """words * 1.3 — canonical formula matching avatar_test_helpers.py."""
    content = path.read_text(encoding="utf-8")
    # Strip frontmatter before counting
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            content = content[end + 4:]
    return round(len(content.split()) * 1.3)


def _rag_index_token_claim(filename_fragment: str) -> int | None:
    """
    Find the first line in AVATAR-RAG-INDEX.yaml containing filename_fragment
    and return the claimed ~NNNNt token count, or None if not found.
    """
    content = RAG_INDEX.read_text(encoding="utf-8")
    for line in content.splitlines():
        if filename_fragment in line:
            m = re.search(r"~(\d+)t", line)
            if m:
                return int(m.group(1))
    return None


# ---------------------------------------------------------------------------
# C3 — Stale token estimates
# ---------------------------------------------------------------------------

class TestC3TokenEstimates:
    """RAG index token estimates must be within ±10% of actual file sizes."""

    def test_threading_ref_token_estimate_within_10_percent(self):
        path = REFS_DIR / "safety" / "ref-concurrency-threading.md"
        actual = _token_estimate(path)
        claimed = _rag_index_token_claim("ref-concurrency-threading.md")
        assert claimed is not None, "No ~NNNNt annotation found for ref-concurrency-threading.md"
        ratio = abs(actual - claimed) / actual
        assert ratio <= 0.10, (
            f"Token estimate for ref-concurrency-threading.md is {claimed}t "
            f"but actual is {actual}t — {ratio:.1%} off (limit 10%)"
        )

    def test_async_ref_token_estimate_within_10_percent(self):
        path = REFS_DIR / "safety" / "ref-concurrency-async.md"
        actual = _token_estimate(path)
        claimed = _rag_index_token_claim("ref-concurrency-async.md")
        assert claimed is not None, "No ~NNNNt annotation found for ref-concurrency-async.md"
        ratio = abs(actual - claimed) / actual
        assert ratio <= 0.10, (
            f"Token estimate for ref-concurrency-async.md is {claimed}t "
            f"but actual is {actual}t — {ratio:.1%} off (limit 10%)"
        )


# ---------------------------------------------------------------------------
# C5 — Pre-C++20 bulkhead fallback in async ref
# ---------------------------------------------------------------------------

class TestC5BulkheadFallback:
    """ref-concurrency-async.md must provide a C++11/17 bulkhead fallback."""

    def _content(self):
        return (REFS_DIR / "safety" / "ref-concurrency-async.md").read_text(encoding="utf-8")

    def test_async_ref_bulkhead_has_condition_variable_fallback(self):
        content = self._content()
        assert "condition_variable" in content, (
            "ref-concurrency-async.md must include a condition_variable-based "
            "bulkhead fallback for C++11/17 projects (C5)"
        )

    def test_async_ref_bulkhead_fallback_has_version_label(self):
        content = self._content()
        # Must call out the C++11/17 fallback explicitly
        assert re.search(r"C\+\+11|C\+\+17.*fallback|fallback.*C\+\+11", content, re.IGNORECASE), (
            "ref-concurrency-async.md bulkhead fallback must be labeled C++11 or C++17 (C5)"
        )


# ---------------------------------------------------------------------------
# C2 — Coroutines extraction
# ---------------------------------------------------------------------------

class TestC2CoroutinesExtraction:
    """Coroutines section must be in a dedicated C++20 ref file."""

    def test_coroutines_ref_file_exists(self):
        coroutines_ref = REFS_DIR / "language" / "ref-concurrency-coroutines.md"
        assert coroutines_ref.exists(), (
            "refs/language/ref-concurrency-coroutines.md must exist (C2). "
            "Coroutines content should be extracted from ref-concurrency-threading.md."
        )

    def test_coroutines_ref_routed_to_greenfield(self):
        content = RAG_INDEX.read_text(encoding="utf-8")
        index = yaml.safe_load(content)
        cpp = index.get("technology_avatars", {}).get("cpp", {})
        policy = cpp.get("version_routing_policy", {})
        greenfield_prefer = policy.get("by_standard", {}).get("greenfield", {}).get("prefer", [])
        paths_only = [p.split(" ")[0] for p in greenfield_prefer]
        assert any("ref-concurrency-coroutines" in p for p in paths_only), (
            "refs/language/ref-concurrency-coroutines.md must be in greenfield.prefer (C2)"
        )

    def test_threading_ref_coroutines_section_removed(self):
        content = (REFS_DIR / "safety" / "ref-concurrency-threading.md").read_text(encoding="utf-8")
        # After extraction, the threading ref should not contain the full coroutines section
        # We check that co_await governance/structured sections are gone
        assert "co_await" not in content or content.count("co_await") <= 2, (
            "ref-concurrency-threading.md should not contain extensive co_await content "
            "after coroutines are extracted to ref-concurrency-coroutines.md (C2). "
            f"Found {content.count('co_await')} occurrences."
        )


# ---------------------------------------------------------------------------
# C1 — Brownfield concurrency ref
# ---------------------------------------------------------------------------

class TestC1BrownfieldConcurrency:
    """A dedicated brownfield/C++98 concurrency reference must exist."""

    def _path(self):
        return REFS_DIR / "legacy" / "ref-concurrency-brownfield.md"

    def test_brownfield_concurrency_ref_exists(self):
        assert self._path().exists(), (
            "refs/legacy/ref-concurrency-brownfield.md must exist (C1). "
            "C++98/03 teams need POSIX/Windows threading guidance."
        )

    def test_brownfield_concurrency_ref_has_posix_content(self):
        content = self._path().read_text(encoding="utf-8")
        assert "pthread" in content, (
            "ref-concurrency-brownfield.md must cover POSIX pthread patterns (C1)"
        )

    def test_brownfield_concurrency_ref_has_volatile_pitfall(self):
        content = self._path().read_text(encoding="utf-8")
        assert "volatile" in content, (
            "ref-concurrency-brownfield.md must document the volatile-is-not-atomic pitfall (C1)"
        )

    def test_brownfield_routed_in_rag_index(self):
        content = RAG_INDEX.read_text(encoding="utf-8")
        index = yaml.safe_load(content)
        cpp = index.get("technology_avatars", {}).get("cpp", {})
        policy = cpp.get("version_routing_policy", {})
        brownfield_prefer = policy.get("by_standard", {}).get("brownfield", {}).get("prefer", [])
        paths_only = [p.split(" ")[0] for p in brownfield_prefer]
        assert any("ref-concurrency-brownfield" in p for p in paths_only), (
            "refs/legacy/ref-concurrency-brownfield.md must be in brownfield.prefer (C1)"
        )


class TestD1P1ThreadSafetyCpp11:
    """D1-P1: ENG-6.1-thread-safety-cpp11.md — C++11 std::thread + std::lock_guard example."""

    EXAMPLE_PATH = CPP_DIR / "examples" / "ENG-6.1-thread-safety-cpp11.md"
    INDEX_PATH = CPP_DIR / "examples" / "ENG-6.1-index.md"
    TOKEN_CEILING = 1200  # content ceiling — producer/consumer + full NON-COMPLIANT included

    def test_example_file_exists(self):
        assert self.EXAMPLE_PATH.exists(), (
            "ENG-6.1-thread-safety-cpp11.md must exist (D1-P1)"
        )

    def test_cpp_version_min_is_11(self):
        content = self.EXAMPLE_PATH.read_text(encoding="utf-8")
        assert "cpp_version_min: 11" in content, (
            "Frontmatter must declare cpp_version_min: 11"
        )

    def test_uses_lock_guard(self):
        content = self.EXAMPLE_PATH.read_text(encoding="utf-8")
        assert "lock_guard" in content, (
            "Example must demonstrate std::lock_guard (primary C++11 RAII lock)"
        )

    def test_uses_std_thread(self):
        content = self.EXAMPLE_PATH.read_text(encoding="utf-8")
        assert "std::thread" in content, (
            "Example must demonstrate std::thread (C++11 portable threading)"
        )

    def test_within_token_ceiling(self):
        tokens = _token_estimate(self.EXAMPLE_PATH)
        assert tokens <= self.TOKEN_CEILING, (
            f"Example file is {tokens}t — must be ≤{self.TOKEN_CEILING}t"
        )

    def test_index_references_cpp11_example(self):
        content = self.INDEX_PATH.read_text(encoding="utf-8")
        assert "ENG-6.1-thread-safety-cpp11.md" in content, (
            "ENG-6.1-index.md must reference ENG-6.1-thread-safety-cpp11.md (D1-P1)"
        )

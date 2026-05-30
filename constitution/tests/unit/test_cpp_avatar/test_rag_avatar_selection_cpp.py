"""
cpp-rag-eval-fix/3.1 — Avatar selection: cpp avatar in top-3 for C++ queries (tc-av-026, 032, 044, 058, 060)

RED test: asserts that retrieve_avatar() for each failing C++ query returns the
cpp avatar (avatar-technology-cpp) within the top-3 results.

Corresponds to RAG eval test cases:
  tc-av-026 — TDD test in C++ using GoogleTest
  tc-av-032 — C++ RAII-based PII encryption
  tc-av-044 — C++11 to C++17 migration
  tc-av-058 — C++ mutation testing with Mull
  tc-av-060 — C++ characterization test / golden-master
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "tools" / "rag-eval"))

from retriever import ConstitutionRetriever  # noqa: E402

_CPP_AVATAR_IDS = {"avatar-technology-cpp", "cpp"}

_FAILING_QUERIES = [
    ("tc-av-026", "How do I write a TDD test in C++ using GoogleTest RED-GREEN-REFACTOR?"),
    ("tc-av-032", "C++ data protection — how do I scope PII to a lifetime using RAII-based encryption in C++?"),
    ("tc-av-044", "How do I migrate from C++11 to C++17 and upgrade C++ standard version?"),
    ("tc-av-058", "C++ mutation testing Mull — how do I configure mutation testing to validate test quality in C++?"),
    ("tc-av-060", "C++ characterization test golden-master — how do I write a characterization test to pin legacy C++ behavior?"),
]


@pytest.fixture(scope="module")
def retriever() -> ConstitutionRetriever:
    return ConstitutionRetriever(REPO_ROOT)


@pytest.mark.parametrize("tc_id,query", _FAILING_QUERIES, ids=[t[0] for t in _FAILING_QUERIES])
def test_cpp_avatar_in_top3_for_cpp_queries(
    retriever: ConstitutionRetriever,
    tc_id: str,
    query: str,
) -> None:
    """cpp avatar must rank in top-3 for C++ queries.

    The cpp avatar id field is 'avatar-technology-cpp'.  The avatar selection
    scorer checks whether 'cpp' appears as a substring of any retrieved id —
    which it does for 'avatar-technology-cpp'.  Trigger phrase 'c++' must be
    present in AVATAR-RAG-INDEX.yaml search_queries so the retriever gives the
    cpp avatar a +3.0 score for any query containing the literal string 'c++'.
    """
    results = retriever.retrieve_avatar(query, top_k=3)
    retrieved_ids = {r.id.lower() for r in results}

    hit = any(
        cpp_id in rid or rid in cpp_id
        for cpp_id in _CPP_AVATAR_IDS
        for rid in retrieved_ids
    )

    assert hit, (
        f"[{tc_id}] cpp avatar not in top-3 for query:\n  {query}\n"
        f"Top-3 IDs: {sorted(retrieved_ids)}"
    )

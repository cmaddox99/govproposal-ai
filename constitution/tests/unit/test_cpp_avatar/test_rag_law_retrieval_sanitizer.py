"""
cpp-rag-eval-fix/2.1 — Law retrieval: ENG-5.2 for C++ sanitizer query (tc-av-042)

RED test: asserts that retrieve() for the sanitizer configuration query returns at
least one result whose indexed_law_ids includes ENG-5.2 (CI/CD Pipeline Law).

Corresponds to RAG eval test case tc-av-042:
  Q: "C++ sanitizer configuration — how do I enable ASan UBSan in my build?"
  expected_laws: [ENG-5.2]
"""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "tools" / "rag-eval"))

from retriever import ConstitutionRetriever  # noqa: E402


@pytest.fixture(scope="module")
def retriever() -> ConstitutionRetriever:
    return ConstitutionRetriever(REPO_ROOT)


def test_sanitizer_query_retrieves_eng_5_2(retriever: ConstitutionRetriever) -> None:
    """tc-av-042: sanitizer configuration query must surface ENG-5.2 in top-3 results.

    ENG-5.2 (CI/CD Pipeline Law) governs automated CI pipeline execution — enabling
    ASan/UBSan in a build is a CI/CD pipeline concern.  The top-ranked skill for this
    query is skill-cpp-sanitizer-hardening.md; that skill's indexed_law_ids must
    include ENG-5.2.
    """
    query = "C++ sanitizer configuration — how do I enable ASan UBSan in my build?"
    results = retriever.retrieve(query, top_k=3)

    collected_laws: set[str] = set()
    for r in results:
        collected_laws.update(r.indexed_law_ids)
        collected_laws.update(r.matched_law_ids)

    assert "ENG-5.2" in collected_laws, (
        f"ENG-5.2 (CI/CD Pipeline Law) not found in top-3 results for sanitizer query.\n"
        f"Retrieved results: {[r.id for r in results]}\n"
        f"Collected laws:    {sorted(collected_laws)}"
    )

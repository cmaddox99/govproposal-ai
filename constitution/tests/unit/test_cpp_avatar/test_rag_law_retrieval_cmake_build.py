"""
cpp-rag-eval-fix/1.1 — Law retrieval: ENG-5.2 for C++ CMake build query (tc-av-028)

RED test: asserts that retrieve() for the CMake build query returns at least one
result whose indexed_law_ids includes ENG-5.2 (CI/CD Pipeline Law).

Corresponds to RAG eval test case tc-av-028:
  Q: "How do I configure a C++ CMake build with clang-tidy and compiler warnings as errors?"
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


def test_cmake_build_query_retrieves_eng_5_2(retriever: ConstitutionRetriever) -> None:
    """tc-av-028: CMake build query must surface ENG-5.2 in top-3 results.

    ENG-5.2 (CI/CD Pipeline Law) governs compiler warnings-as-errors and
    clang-tidy gates — the exact subject of this query.  The top-ranked skill
    for this query is skill-cpp-portable-build-governance.md; that skill's
    indexed_law_ids must include ENG-5.2.
    """
    query = (
        "How do I configure a C++ CMake build with clang-tidy and compiler warnings as errors?"
    )
    results = retriever.retrieve(query, top_k=3)

    collected_laws: set[str] = set()
    for r in results:
        collected_laws.update(r.indexed_law_ids)
        collected_laws.update(r.matched_law_ids)

    assert "ENG-5.2" in collected_laws, (
        f"ENG-5.2 (CI/CD Pipeline Law) not found in top-3 results for CMake build query.\n"
        f"Retrieved results: {[r.id for r in results]}\n"
        f"Collected laws:    {sorted(collected_laws)}"
    )

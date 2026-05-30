"""Law-ID extractor unit tests (Hangar rag-eval).

Per jury ruling sess-aa47a7f6 Option B: _LAW_ID_RE is extracted into a shared
tools/rag-eval/law_ids.py module where valid law-ID prefixes are derived from
laws/*/_domain.yaml — preventing license identifiers (e.g. BSL-1.0) from being
miscounted as broken law references in cross_ref_consistency.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
_RAG_EVAL_DIR = REPO_ROOT / "tools" / "rag-eval"
if str(_RAG_EVAL_DIR) not in sys.path:
    sys.path.insert(0, str(_RAG_EVAL_DIR))


def test_bsl_license_string_is_not_matched_as_law_id() -> None:
    """Regression: BSL-1.0 (Business Source License) is a license identifier,
    not a law ID. The extractor must not return it. This test drives the whole
    Option-B extraction: it imports from law_ids, which forces the module to
    exist; it asserts the license string is rejected, which forces prefix
    filtering derived from laws/*/_domain.yaml."""
    from law_ids import extract_law_ids

    text = (
        "Permitted licenses for third-party dependencies: MIT, BSD-2-Clause, "
        "BSD-3-Clause, Apache-2.0, BSL-1.0, Zlib. All others require legal review."
    )
    assert extract_law_ids(text, REPO_ROOT) == [], (
        "BSL-1.0 (and other license strings) must not be treated as law IDs; "
        "valid law-ID prefixes are defined by laws/*/_domain.yaml only."
    )

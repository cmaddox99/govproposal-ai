"""Test ESE-29: CP.51/CP.52/CP.53 Coroutine-Concurrency Safety section in
ref-concurrency-advanced-part2.md.

Scenario ID: cpp-external-sources-enrichment/ESE-29
Law: ENG-6.1 (Security by Design — coroutine data race prevention)
cpp_version_min: 20
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-concurrency-advanced-part2.md"
)


def test_coroutine_concurrency_safety_section_exists():
    """ref-concurrency-advanced-part2.md must contain CP.51/52/53 section:
    CP.51 no capturing lambdas as coroutines, CP.52 no locks across
    suspension, CP.53 no reference params to coroutines, cross-ref to
    ENG-3.1-coroutines, COMPLIANT/NON-COMPLIANT examples, budget ok."""
    assert REF.exists(), "ref-concurrency-advanced-part2.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "CP.51" in content, "Must cite CP.51 (no capturing lambda coroutine)"
    assert "CP.52" in content, "Must cite CP.52 (no locks across suspension)"
    assert "CP.53" in content, "Must cite CP.53 (no reference params)"
    assert "suspension" in content.lower(), \
        "Must explain suspension point hazards"
    assert "coroutines.md" in content or "ENG-3.1" not in content, \
        "Cross-ref must use coroutines.md (not bare ENG-3.1 law ref)"
    assert "COMPLIANT" in content, "Must have COMPLIANT example"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT example"
    assert len(content) // 4 <= 3500, \
        f"ref-concurrency-advanced-part2.md exceeds 3500-token budget (got {len(content)//4})"

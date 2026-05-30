"""Test ESE-20: Interface Design Rules section in ref-core-type-safety.md.

Scenario ID: cpp-external-sources-enrichment/ESE-20
Law: ENG-3.1 (Complexity — I.23), ENG-6.1 (I.11, I.12 ownership/null safety)
cpp_version_min: 14 (not_null from GSL requires C++14)
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-core-type-safety.md"
)


def test_interface_design_rules_section_exists():
    """ref-core-type-safety.md must contain an Interface Design Rules section
    covering I.1 (explicit contract), I.3 (avoid singletons), I.11 (ownership
    transfer via unique_ptr/span), I.12 (not_null for never-null), Expects/Ensures
    from GSL, and I.23 (low parameter count). Must cite Core Guidelines."""
    assert REF.exists(), "ref-core-type-safety.md not found"
    content = REF.read_text(encoding="utf-8")

    assert "Interface Design" in content, \
        "Must have an Interface Design section"
    assert "I.1" in content, "Must cover I.1 (explicit contract)"
    assert "I.3" in content, "Must cover I.3 (avoid singletons)"
    assert "I.11" in content, "Must cover I.11 (ownership transfer)"
    assert "I.12" in content, "Must cover I.12 (not_null)"
    assert "not_null" in content, "Must show not_null<T*> usage"
    assert "Expects" in content, "Must show Expects() precondition macro"
    assert "I.23" in content, "Must cover I.23 (parameter count)"
    assert "unique_ptr" in content, "Must reference unique_ptr for ownership transfer"
    # Budget: whole file must stay within 3500-token ref limit
    assert len(content) // 4 <= 3500, \
        f"ref-core-type-safety.md exceeds 3500-token budget (got {len(content) // 4})"

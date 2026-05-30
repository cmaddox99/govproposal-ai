"""Test ESE-19: ENG-3.1-crtp.md example file.

Scenario ID: cpp-external-sources-enrichment/ESE-19
Law: ENG-3.1 (Complexity — CRTP reduces virtual dispatch overhead)
cpp_version_min: 11
"""

from pathlib import Path

EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/examples/ENG-3.1-crtp.md"
)


def test_crtp_example_valid():
    """Must cover: CRTP static polymorphism with Serializable<Derived>;
    CRTP mixin pattern (logging without virtual overhead); CRTP vs. virtual
    trade-off table; NON-COMPLIANT dynamic_cast chain (RTTI dispatch);
    edge case: inheritance depth and C++20 concept replacement. <= 700 tokens."""
    assert EXAMPLE.exists(), "ENG-3.1-crtp.md not found"
    content = EXAMPLE.read_text(encoding="utf-8")

    assert content.count("```cpp") >= 2, "Must have at least 2 cpp code blocks"
    # CRTP pattern fundamentals
    assert "Derived" in content, "Must show CRTP Derived template parameter"
    assert "static_cast<Derived" in content or "static_cast<Derived&>" in content \
        or "derived()" in content, \
        "Must show CRTP downcast (static_cast<Derived&>(*this) or derived())"
    # Spec requirements
    assert "virtual" in content, "Must address virtual vs CRTP trade-off"
    assert "dynamic_cast" in content, "Must show NON-COMPLIANT dynamic_cast chain"
    assert "COMPLIANT" in content, "Must have COMPLIANT section"
    assert "NON-COMPLIANT" in content, "Must have NON-COMPLIANT section"
    # Edge cases per spec
    assert "concept" in content.lower() or "C++20" in content, \
        "Must address C++20 concept as CRTP replacement"
    assert len(content) // 4 <= 700, \
        f"Exceeds 700-token budget (got {len(content) // 4})"

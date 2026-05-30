"""Tests ESE-33–36 and ESE-44–45: ref-templates-advanced.md sections.

Scenario IDs: cpp-external-sources-enrichment/ESE-33 through ESE-36, ESE-44, ESE-45
Note: spec targeted non-existent ref-advanced-cpp.md; content placed in
ref-templates-advanced.md (ref-templates-metaprogramming.md is at capacity).
"""

from pathlib import Path

REF = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-templates-advanced.md"
)


def _content():
    assert REF.exists(), "ref-templates-advanced.md not found"
    return REF.read_text(encoding="utf-8")


def test_type_traits_section():  # ESE-33
    c = _content()
    assert "is_integral" in c or "std::is_" in c, "Must cover std::is_* traits"
    assert "has_serialize" in c or "has_" in c, "Must show custom trait pattern"
    assert "conjunction" in c, "Must show conjunction/disjunction/negation"
    assert "enable_if" in c, "Must cover enable_if_t"


def test_tag_dispatching_section():  # ESE-34
    c = _content()
    assert "true_type" in c and "false_type" in c, "Must cover tag dispatch types"
    assert "if constexpr" in c, "Must show migration path to if constexpr"


def test_advanced_concepts_section():  # ESE-35
    c = _content()
    assert "requires" in c, "Must cover requires-expression"
    assert "subsumption" in c or "most constrained" in c.lower(), \
        "Must explain concept subsumption"
    assert "static_assert" in c, "Must show concept debugging via static_assert"


def test_nttp_section():  # ESE-36
    c = _content()
    assert "NTTP" in c or "non-type template" in c.lower(), "Must cover NTTPs"
    assert "template <auto" in c or "template<auto" in c, \
        "Must show template<auto N> syntax"


def test_expression_templates_section():  # ESE-44
    c = _content()
    assert "expression template" in c.lower() or "Expression Template" in c, \
        "Must cover expression templates"
    assert "lazy" in c.lower() or "deferred" in c.lower(), \
        "Must explain lazy evaluation benefit"


def test_cpp20_lambda_section():  # ESE-45
    c = _content()
    assert "template lambda" in c.lower() or "[]<typename" in c, \
        "Must cover template lambda syntax"
    assert "consteval" in c, "Must cover consteval lambda"


def test_budget():
    c = _content()
    assert len(c) // 4 <= 3500, \
        f"ref-templates-advanced.md exceeds 3500-token budget (got {len(c)//4})"

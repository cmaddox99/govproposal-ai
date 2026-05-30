"""Test ESE-11: C++20 Coroutine Generators section in ref-cpp20-features-part2.md.

Scenario ID: cpp-external-sources-enrichment/ESE-11
Law: ENG-3.1 (Complexity — lazy generation reduces eager allocation)
"""

from pathlib import Path

PART2 = (
    Path(__file__).resolve().parents[3]
    / "avatars/technology/cpp/refs/language/ref-cpp20-features-part2.md"
)


def test_cpp20_coroutine_generators_section_exists():
    """ref-cpp20-features-part2.md must have a coroutine generators section covering:
    co_yield mechanics, Generator<T> promise_type, lazy sequence, stop_token
    cancellation, std::generator C++23 preview. COMPLIANT + NON-COMPLIANT (ENG-4.1)."""
    content = PART2.read_text(encoding="utf-8")

    assert "## Coroutine" in content or "## C++20 Coroutine" in content or \
           "co_yield" in content, \
        "Must have a coroutine generators section"
    assert "co_yield" in content, \
        "Must cover co_yield mechanics"
    assert "promise_type" in content, \
        "Must show Generator<T> promise_type implementation"
    assert "stop_token" in content or "cancel" in content.lower(), \
        "Must cover cancellable generator with stop_token"
    assert "std::generator" in content or "C++23" in content, \
        "Must mention std::generator C++23 preview"
    assert "COMPLIANT" in content, \
        "Must include at least one COMPLIANT example (ENG-4.1)"
    assert "NON-COMPLIANT" in content, \
        "Must include at least one NON-COMPLIANT example (ENG-4.1)"

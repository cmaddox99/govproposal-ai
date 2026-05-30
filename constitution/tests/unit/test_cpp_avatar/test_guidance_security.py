"""Consolidated security guidance tests: lifetime, ownership, unsafe, concurrency.

Covers scenario IDs:
  - c-plus-plus-avatar-enrichment/2.1 (ownership)
  - c-plus-plus-avatar-enrichment/2.2 (lifetime)
  - c-plus-plus-avatar-enrichment/2.3 (unsafe)
  - c-plus-plus-avatar-enrichment/2.4 (concurrency)
Laws: ENG-6.1, ENG-11.1
"""

from test_cpp_avatar.avatar_test_helpers import find_section


# ---------------------------------------------------------------------------
# 2.1 – Ownership-First API Design
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_ownership_first_api_design(cpp_full_reference):
    """guidance.md must document ownership-first API design with specific patterns."""
    content = cpp_full_reference

    assert "ownership-first" in content.lower(), (
        "guidance.md must contain 'Ownership-First' heading or term"
    )
    assert "unique_ptr" in content, (
        "guidance.md must reference std::unique_ptr for ownership transfer"
    )
    assert "shared_ptr" in content, (
        "guidance.md must reference std::shared_ptr with guidance on when to use"
    )
    assert "move" in content.lower(), (
        "guidance.md must reference move semantics"
    )
    assert "factory" in content.lower() or "create" in content.lower(), (
        "guidance.md must reference factory/create patterns for ownership clarity"
    )
    assert "```cpp" in content, (
        "guidance.md must include C++ code examples for ownership patterns"
    )


# ---------------------------------------------------------------------------
# 2.2 – Lifetime and Bounds Safety
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_lifetime_and_bounds_safety(cpp_full_reference):
    """guidance.md must document lifetime and bounds safety defaults with detailed guidance."""
    content = cpp_full_reference

    assert "Lifetime and Bounds Safety" in content, (
        "guidance.md must have a 'Lifetime and Bounds Safety' heading"
    )
    assert "dangling" in content.lower(), (
        "guidance.md must discuss dangling reference/pointer prevention"
    )
    assert "stack allocation" in content.lower() or "value semantics" in content.lower(), (
        "guidance.md must discuss stack allocation or value semantics as defaults"
    )
    assert "span<" in content, (
        "guidance.md must include a typed span<> usage example"
    )
    assert "not_null" in content, (
        "guidance.md must reference gsl::not_null"
    )
    assert "RAII" in content, (
        "guidance.md must reference RAII"
    )

    section_content = find_section(content, "Lifetime and Bounds Safety", n_lines=50)
    assert section_content is not None
    assert "```cpp" in section_content, (
        "Lifetime and Bounds Safety section must include a C++ code example"
    )


# ---------------------------------------------------------------------------
# 2.3 – Unsafe-Boundary Governance
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_unsafe_boundary_governance(cpp_full_reference):
    """guidance.md must document unsafe-boundary governance with repository-configurable modes."""
    content = cpp_full_reference

    assert "unsafe" in content.lower() and "boundary" in content.lower(), (
        "guidance.md must discuss unsafe boundary governance"
    )
    assert "option 1" in content.lower() or "strict mode" in content.lower(), (
        "guidance.md must reference strict mode (Option 1)"
    )
    assert "option 2" in content.lower() or "default mode" in content.lower(), (
        "guidance.md must reference default mode (Option 2)"
    )
    assert "option 3" in content.lower() or "lightweight mode" in content.lower(), (
        "guidance.md must reference lightweight mode (Option 3)"
    )
    assert "waiver" in content.lower() or "approval" in content.lower(), (
        "guidance.md must discuss waiver/approval process for unsafe boundaries"
    )
    assert "reinterpret_cast" in content, (
        "guidance.md must reference reinterpret_cast as an unsafe boundary example"
    )
    assert "greenfield" in content.lower() and "brownfield" in content.lower(), (
        "guidance.md must discuss greenfield and brownfield configuration behavior"
    )


# ---------------------------------------------------------------------------
# 2.4 – Concurrency by Design
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_concurrency_by_design(cpp_full_reference):
    """guidance.md Concurrency section must have detailed patterns and code examples."""
    content = cpp_full_reference

    section_text = find_section(content, "Concurrency", n_lines=60)
    assert section_text is not None, "guidance.md must have a '## Concurrency' section"

    assert "```cpp" in section_text, (
        "Concurrency section must include C++ code examples"
    )
    assert "scoped_lock" in section_text or "lock_guard" in section_text, (
        "Concurrency section must reference RAII lock patterns"
    )
    assert "atomic" in section_text.lower(), (
        "Concurrency section must reference std::atomic"
    )
    assert "data race" in section_text.lower() or "race condition" in section_text.lower(), (
        "Concurrency section must discuss data race prevention"
    )
    assert "ThreadSanitizer" in section_text or "TSan" in section_text, (
        "Concurrency section must reference TSan for race detection"
    )

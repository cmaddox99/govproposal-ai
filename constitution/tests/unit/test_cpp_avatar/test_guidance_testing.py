"""Consolidated testing guidance tests: testing_policy, mutation, ci_toolchain, coverage.

Covers scenario IDs:
  - c-plus-plus-avatar-enrichment/2.6 (ci_toolchain)
  - c-plus-plus-avatar-enrichment/2.7 (mutation)
  - c-plus-plus-avatar-enrichment/2.8 (testing_policy)
  - c-plus-plus-avatar-enrichment/2.16 (coverage)
Laws: ENG-4.1, ENG-4.2, ENG-4.11, ENG-5.1, ENG-11.1
"""

from test_cpp_avatar.avatar_test_helpers import find_section


# ---------------------------------------------------------------------------
# 2.6 – CI Quality Toolchain Policy
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_ci_toolchain_policy(cpp_full_reference):
    """guidance.md must have a dedicated CI toolchain policy section."""
    section_text = find_section(cpp_full_reference, "CI Quality Toolchain", n_lines=40)
    if section_text is None:
        section_text = find_section(cpp_full_reference, "CI Quality", n_lines=40)

    assert section_text is not None, (
        "guidance.md must have a dedicated CI toolchain/quality heading"
    )
    assert "mandatory" in section_text.lower(), "CI policy must specify mandatory gates"
    assert "recommended" in section_text.lower(), "CI policy must specify recommended gates"
    assert "clang-tidy" in section_text, "CI policy must reference clang-tidy"
    assert "ASan" in section_text or "AddressSanitizer" in section_text, (
        "CI policy must reference ASan"
    )
    assert "UBSan" in section_text or "UndefinedBehaviorSanitizer" in section_text, (
        "CI policy must reference UBSan"
    )


# ---------------------------------------------------------------------------
# 2.7 – Mull Mutation Testing Policy
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_mull_mutation_testing_policy(cpp_full_reference):
    """Mutation Testing section must document Mull policy with LLVM/Clang
    prerequisites and phased brownfield exception handling."""
    content = cpp_full_reference

    assert "LLVM" in content and "Clang" in content, (
        "Mutation Testing section must document LLVM/Clang prerequisite"
    )
    assert "brownfield exception" in content.lower() or "phased adoption" in content.lower(), (
        "Must document phased brownfield exception handling for Mull"
    )
    assert "mutation-testing-governance" in content, (
        "Must cross-reference the mutation-testing-governance proposal"
    )
    assert "LLVM 14" in content or "LLVM 15" in content or "Clang 15" in content, (
        "Must specify minimum LLVM/Clang version for Mull support"
    )
    assert "greenfield" in content.lower() and "brownfield" in content.lower(), (
        "Must distinguish greenfield default from brownfield exception path"
    )
    assert "70%" in content and "85%" in content, (
        "Must document ≥70% general and ≥85% critical path mutation score thresholds"
    )
    assert "mull-runner" in content, (
        "Must include mull-runner CLI invocation example"
    )
    assert "5 minute" in content.lower() or "5-minute" in content.lower() or "<5 min" in content.lower(), (
        "Must document performance SLA for mutation testing runs"
    )


# ---------------------------------------------------------------------------
# 2.8 – GoogleTest Framework Policy
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_googletest_framework_policy(cpp_full_reference):
    """Testing Framework section must include a formal policy subsection
    with adoption rules, version requirements, and mock governance."""
    content = cpp_full_reference

    assert "### Testing Framework Policy" in content, (
        "Must have a '### Testing Framework Policy' subsection"
    )
    assert "1.14" in content or "1.15" in content, (
        "Must specify minimum GoogleTest version (1.14+)"
    )
    assert "googlemock" in content.lower() or "google mock" in content.lower() or "gmock" in content.lower(), (
        "Must document GoogleMock as the mocking framework"
    )
    assert "adopt immediately" in content.lower() or "immediate adoption" in content.lower(), (
        "Must document immediate adoption rule for repos without test frameworks"
    )
    assert "migration" in content.lower(), (
        "Must document migration path for repos using other test frameworks"
    )
    assert "ENG-4.2" in content, (
        "Must reference ENG-4.2 (Test Pyramid Law)"
    )
    assert "test naming" in content.lower() or "naming convention" in content.lower() or "TestSuiteName" in content, (
        "Must document test naming convention"
    )
    assert "vcpkg" in content.lower() or "fetchcontent" in content.lower() or "find_package" in content.lower(), (
        "Must document how to include GoogleTest via package manager or CMake"
    )


# ---------------------------------------------------------------------------
# 2.16 – Coverage Tooling Recommendation
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_coverage_tooling_recommendation(cpp_full_reference):
    """Must have a dedicated coverage tooling subsection."""
    content = cpp_full_reference

    assert "### Coverage Tooling" in content, (
        "Must have a dedicated Coverage Tooling subsection"
    )
    assert "llvm-cov" in content or "gcov" in content, (
        "Must document llvm-cov or gcov as default coverage tool"
    )
    assert "ENG-4.2" in content, (
        "Must reference ENG-4.2 (Test Pyramid Law)"
    )

"""Consolidated architecture guidance tests: alignment, rationale, brownfield, version_policy, observability.

Covers scenario IDs:
  - c-plus-plus-avatar-enrichment/2.5 (version_policy)
  - c-plus-plus-avatar-enrichment/2.10 (brownfield)
  - c-plus-plus-avatar-enrichment/2.17 (observability)
  - c-plus-plus-avatar-enrichment/2.18 (alignment)
  - c-plus-plus-avatar-enrichment/2.19 (rationale)
Laws: ENG-1.4, ENG-2.3, ENG-4.1, ENG-5.6, ENG-10.1, ENG-11.1
"""

import yaml

from test_cpp_avatar.avatar_test_helpers import find_section


# ---------------------------------------------------------------------------
# 2.5 – C++ Version Policy
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_version_policy_section(cpp_full_reference):
    """guidance.md must have a dedicated version policy section with greenfield/brownfield rules."""
    content = cpp_full_reference

    section_text = find_section(content, "version policy", n_lines=40)
    assert section_text is not None, "guidance.md must have a dedicated 'Version Policy' heading"

    assert "c++20" in section_text.lower(), "Version policy must reference C++20"
    assert "c++23" in section_text.lower(), "Version policy must reference C++23"
    assert "modernization" in section_text.lower(), (
        "Version policy must discuss modernization plans for brownfield"
    )
    assert "greenfield" in section_text.lower(), "Version policy must cover greenfield"
    assert "brownfield" in section_text.lower(), "Version policy must cover brownfield"


# ---------------------------------------------------------------------------
# 2.10 – Brownfield Non-Rewrite Safeguards
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_brownfield_safeguards_and_modernization(cpp_full_reference):
    """Brownfield Migration must include non-rewrite safeguards,
    test equivalence strategy, and phased modernization path."""
    content = cpp_full_reference

    assert "no rewrite" in content.lower() or "non-rewrite" in content.lower(), (
        "Must explicitly state non-rewrite safeguard"
    )
    assert "test equivalence" in content.lower(), (
        "Must document test equivalence strategy for brownfield changes"
    )
    assert "preserved behavior" in content.lower() or "preserve behavior" in content.lower(), (
        "Must require documenting preserved behavior before refactoring"
    )
    assert "phase 1" in content.lower() or "phase 1:" in content.lower() or "step 1" in content.lower(), (
        "Must document phased modernization path"
    )
    assert "compiler" in content.lower() and "migration" in content.lower(), (
        "Must document compiler migration path"
    )
    assert "approval" in content.lower() or "approved" in content.lower(), (
        "Must document approval requirements for migration"
    )
    assert "rollback" in content.lower() or "revert" in content.lower(), (
        "Must document rollback/revert strategy for brownfield changes"
    )
    assert "module-by-module" in content.lower() or "module by module" in content.lower() or "incremental" in content.lower(), (
        "Must specify module-by-module or incremental migration approach"
    )


# ---------------------------------------------------------------------------
# 2.17 – Observability Stack
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_observability_recommendation(cpp_full_reference):
    """Must have a dedicated observability subsection."""
    content = cpp_full_reference

    assert "### Observability" in content, (
        "Must have a dedicated Observability subsection"
    )
    assert "OpenTelemetry" in content, (
        "Must document OpenTelemetry as default observability framework"
    )
    assert "ENG-5.6" in content, (
        "Must reference ENG-5.6 (Observability Law)"
    )
    assert "traces" in content.lower() and "metrics" in content.lower() and "logs" in content.lower(), (
        "Must document all three observability signals (traces, metrics, logs)"
    )


# ---------------------------------------------------------------------------
# 2.18 – Cross-Language Alignment Defaults
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_cross_language_alignment_matrix(cpp_full_reference, cpp_dir):
    """Must have a Cross-Language Alignment Defaults summary matrix
    and CI toolchain example must include security/devops tooling entries."""
    content = cpp_full_reference

    assert "Cross-Language Alignment" in content, (
        "Must have a Cross-Language Alignment section"
    )

    concerns = ["SAST", "Dependency", "DAST", "Secrets", "IaC", "Coverage", "Observability"]
    for concern in concerns:
        assert concern.lower() in content.lower(), (
            f"Cross-language matrix must reference {concern}"
        )

    # CI toolchain now lives in ENG-5.2-cmake-governance.md example
    ci_example = (cpp_dir / "examples" / "ENG-5.2-cmake-governance.md").read_text(encoding="utf-8")
    assert "codeql" in ci_example.lower(), (
        "ENG-5.2-cmake-governance.md CI toolchain must reference CodeQL"
    )


# ---------------------------------------------------------------------------
# 2.19 – Tool-Selection Rationale
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_tool_selection_rationale(cpp_full_reference):
    """Each security/devops tool default must include a concise
    selection rationale explaining why it was chosen."""
    content = cpp_full_reference

    assert "Selection Rationale" in content or "selection rationale" in content.lower(), (
        "Must include tool selection rationale content"
    )

    rationale_markers = [
        "clang-tidy",
        "CodeQL",
        "Dependabot",
        "OWASP ZAP",
        "Vault",
        "Terraform",
        "llvm-cov",
        "OpenTelemetry",
    ]

    found = sum(1 for m in rationale_markers if m in content)
    assert found >= 7, (
        f"Rationale must reference at least 7 of 8 key tools, found {found}"
    )

    assert "confidence" in content.lower(), (
        "Must include confidence indicators for tool selections"
    )

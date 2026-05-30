"""Consolidated toolchain guidance tests: sast, dast, dep_scanning, iac, package_mgmt, secrets.

Covers scenario IDs:
  - c-plus-plus-avatar-enrichment/2.9 (package_mgmt)
  - c-plus-plus-avatar-enrichment/2.11 (sast)
  - c-plus-plus-avatar-enrichment/2.12 (dep_scanning)
  - c-plus-plus-avatar-enrichment/2.13 (dast)
  - c-plus-plus-avatar-enrichment/2.14 (secrets)
  - c-plus-plus-avatar-enrichment/2.15 (iac)
Laws: ENG-4.1, ENG-5.1, ENG-5.2, ENG-5.5, ENG-6.1
"""


# ---------------------------------------------------------------------------
# 2.9 – Package Management
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_package_manager_guidance(cpp_full_reference):
    """Must have a dedicated Package Management section with vcpkg default,
    Conan support, and selection criteria per Q8 decision."""
    content = cpp_full_reference

    assert "## Package Management" in content or "### Package Management" in content, (
        "Must have a dedicated Package Management section"
    )
    assert "vcpkg" in content and "default" in content.lower(), (
        "Must document vcpkg as the default package manager"
    )
    assert "Conan" in content, (
        "Must document Conan as a supported alternative"
    )
    assert "selection criteria" in content.lower() or "when to use" in content.lower() or "choose" in content.lower(), (
        "Must provide selection criteria for vcpkg vs Conan"
    )
    assert "vcpkg.json" in content, (
        "Must reference vcpkg.json manifest file"
    )
    assert "conanfile" in content.lower(), (
        "Must reference Conan's conanfile"
    )
    assert "cmake" in content.lower(), (
        "Must document CMake integration"
    )


# ---------------------------------------------------------------------------
# 2.11 – SAST Recommendation
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_sast_recommendation(cpp_full_reference):
    """Must have a dedicated SAST section documenting clang-tidy + CodeQL
    as the default with brownfield exception path."""
    content = cpp_full_reference

    assert "### SAST" in content or "### Static Application Security Testing" in content, (
        "Must have a dedicated SAST subsection"
    )
    assert "clang-tidy" in content, (
        "Must document clang-tidy as primary SAST tool"
    )
    assert "CodeQL" in content, (
        "Must document CodeQL as complementary security-focused analysis"
    )
    assert "ENG-6.1" in content, (
        "Must reference ENG-6.1 (Security by Design)"
    )
    assert "brownfield" in content.lower() and "exception" in content.lower(), (
        "Must document brownfield exception path for SAST adoption"
    )


# ---------------------------------------------------------------------------
# 2.12 – Dependency/Vulnerability Scanning
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_dependency_scanning_recommendation(cpp_full_reference):
    """Must have a dedicated dependency/vulnerability scanning subsection."""
    content = cpp_full_reference

    assert "### Dependency" in content or "### Vulnerability" in content, (
        "Must have a dedicated dependency/vulnerability scanning subsection"
    )
    assert "Dependabot" in content or "dependabot" in content, (
        "Must document Dependabot as default dependency scanning tool"
    )
    assert "CVE" in content or "vulnerability" in content.lower(), (
        "Must reference vulnerability/CVE scanning"
    )
    assert "brownfield" in content.lower(), (
        "Must document brownfield exception path"
    )


# ---------------------------------------------------------------------------
# 2.13 – DAST Recommendation
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_dast_recommendation(cpp_full_reference):
    """Must have a dedicated DAST subsection for web-exposed C++ services."""
    content = cpp_full_reference

    assert "### DAST" in content or "### Dynamic Application Security Testing" in content, (
        "Must have a dedicated DAST subsection"
    )
    assert "OWASP ZAP" in content or "owasp zap" in content.lower(), (
        "Must document OWASP ZAP as default DAST tool"
    )
    assert "brownfield" in content.lower(), (
        "Must document brownfield exception path"
    )


# ---------------------------------------------------------------------------
# 2.14 – Secrets Management
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_secrets_management_recommendation(cpp_full_reference):
    """Must have a dedicated secrets management subsection."""
    content = cpp_full_reference

    assert "### Secrets Management" in content, (
        "Must have a dedicated Secrets Management subsection"
    )
    assert "Vault" in content or "vault" in content, (
        "Must document HashiCorp Vault or cloud secret manager"
    )
    assert "ENG-5.5" in content, (
        "Must reference ENG-5.5 (Secrets Management Law)"
    )
    assert "brownfield" in content.lower(), (
        "Must document brownfield exception path"
    )


# ---------------------------------------------------------------------------
# 2.15 – IaC Recommendation
# ---------------------------------------------------------------------------

def test_cpp_guidance_has_iac_recommendation(cpp_full_reference):
    """Must have a dedicated IaC subsection."""
    content = cpp_full_reference

    assert "### Infrastructure as Code" in content, (
        "Must have a dedicated IaC subsection"
    )
    assert "Terraform" in content, (
        "Must document Terraform as default IaC tool"
    )
    assert "ENG-5.2" in content, (
        "Must reference ENG-5.2 (Infrastructure as Code Law)"
    )
    assert "drift" in content.lower(), (
        "Must document drift detection"
    )

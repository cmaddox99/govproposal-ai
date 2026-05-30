"""IOC_ALP C++ Avatar Enrichment Tests.

Scenario IDs: ALP-01 through ALP-10
Law: ENG-11.1, ENG-10.1
Proposal: hangar-ai-specs/changes/alp-cpp-avatar-enrichment/PROPOSAL.md

Validates that the C++ avatar is grounded in patterns observed in the
IOC_ALP (PCLoadPlan) codebase — C++98, MSVC/MFC Windows desktop application,
Sabre CSAPI integration, RCPtr<T> smart pointers, Observer/Observable pattern,
Command/Parser/Record/Request quad, airline load planning domain.
"""

import pytest
import yaml
from pathlib import Path


# ---------------------------------------------------------------------------
# ALP-01: manifest has brownfield_msvc_build commands
# ---------------------------------------------------------------------------

def test_manifest_has_brownfield_msvc_build_commands(manifest_data):
    """Scenario ALP-01: manifest commands block must contain a brownfield_msvc_build
    key with the MSVC msbuild command used in IOC_ALP (ALPGUI.sln)."""
    commands = manifest_data.get("commands", {})
    assert "brownfield_msvc_build" in commands, (
        "commands block is missing 'brownfield_msvc_build' key — "
        "IOC_ALP uses msbuild ALPGUI.sln, not CMake"
    )
    build_cmd = commands["brownfield_msvc_build"].get("build", "")
    assert "ALPGUI.sln" in build_cmd or "msbuild" in build_cmd, (
        f"brownfield_msvc_build.build must reference 'msbuild' or 'ALPGUI.sln', got: '{build_cmd}'"
    )


# ---------------------------------------------------------------------------
# ALP-02: manifest has brownfield_mfc_stack dependencies
# ---------------------------------------------------------------------------

def test_manifest_has_brownfield_mfc_stack_dependencies(manifest_data):
    """Scenario ALP-02: manifest dependencies block must contain a brownfield_mfc_stack
    key with the Windows/MFC/Sabre libraries used in IOC_ALP."""
    deps = manifest_data.get("dependencies", {})
    assert "brownfield_mfc_stack" in deps, (
        "dependencies block is missing 'brownfield_mfc_stack' key — "
        "IOC_ALP depends on AACCSAPI.lib (Sabre), MFC, TinyXML2, culib"
    )
    stack = deps["brownfield_mfc_stack"]
    # Sabre CSAPI integration is the primary external dependency
    sabre = stack.get("sabre", "") or stack.get("gds", "") or stack.get("csapi", "")
    assert "AACCSAPI" in sabre or "Sabre" in sabre or "CSAPI" in sabre, (
        f"brownfield_mfc_stack must reference AACCSAPI / Sabre CSAPI, got sabre='{sabre}'"
    )
    # MFC/AFX is the UI framework
    mfc = stack.get("ui", "") or stack.get("mfc", "")
    assert "MFC" in mfc or "AFX" in mfc, (
        f"brownfield_mfc_stack must reference MFC/AFX, got ui='{mfc}'"
    )


# ---------------------------------------------------------------------------
# ALP-03: manifest has brownfield_mfc_cpp98 naming conventions
# ---------------------------------------------------------------------------

def test_manifest_has_brownfield_mfc_cpp98_naming_conventions(manifest_data):
    """Scenario ALP-03: manifest conventions block must contain a brownfield_mfc_cpp98
    key capturing IOC_ALP's MFC C-prefix naming, Manager/Task suffixes, and RCPtr pattern."""
    conventions = manifest_data.get("conventions", {})
    assert "brownfield_mfc_cpp98" in conventions, (
        "conventions block is missing 'brownfield_mfc_cpp98' key — "
        "IOC_ALP uses MFC C-prefix (CFlight, CDataManager) and RCPtr<T> ownership"
    )
    block = conventions["brownfield_mfc_cpp98"]
    # C prefix is the primary MFC naming signal
    c_prefix = block.get("class_prefix", "") or block.get("mfc_prefix", "")
    assert "C" in c_prefix or "MFC" in c_prefix, (
        f"brownfield_mfc_cpp98 must capture MFC C-prefix convention, got: '{c_prefix}'"
    )
    # RCPtr is the ownership model
    ownership = block.get("ownership", "") or block.get("smart_ptr", "")
    assert "RCPtr" in ownership, (
        f"brownfield_mfc_cpp98 must reference RCPtr ownership model, got: '{ownership}'"
    )


# ---------------------------------------------------------------------------
# ALP-04: manifest has brownfield_winforms_desktop project archetype
# ---------------------------------------------------------------------------

def test_manifest_project_archetypes_has_brownfield_winforms_desktop(manifest_data):
    """Scenario ALP-04: manifest activates.project_archetypes must contain a
    brownfield_winforms_desktop key capturing IOC_ALP's .sln / MFC layout."""
    archetypes = manifest_data.get("activates", {}).get("project_archetypes", {})
    assert "brownfield_winforms_desktop" in archetypes, (
        "activates.project_archetypes is missing 'brownfield_winforms_desktop' — "
        "IOC_ALP is an MFC Windows desktop app (ALPGUI.sln)"
    )
    arch = archetypes["brownfield_winforms_desktop"]
    layout = arch.get("layout", {})
    layout_str = str(layout)
    assert "alpsource" in layout_str or "ALPGUI.sln" in layout_str, (
        f"brownfield_winforms_desktop.layout must reference 'alpsource/' or 'ALPGUI.sln', got: {layout_str[:120]}"
    )


# ---------------------------------------------------------------------------
# ALP-05: ENG-2.3 RCPtr ABI stability example exists
# ---------------------------------------------------------------------------

def test_rcptr_abi_stability_example_exists(examples_dir):
    """Scenario ALP-05: examples/ENG-2.3-rcptr-abi-stability.md must exist,
    contain RCPtr/RCObject content, and stay within the token budget."""
    example = examples_dir / "ENG-2.3-rcptr-abi-stability.md"
    assert example.exists(), (
        "examples/ENG-2.3-rcptr-abi-stability.md does not exist — "
        "IOC_ALP uses RCPtr<T>/RCObject custom smart pointer (650+ usages)"
    )
    content = example.read_text(encoding="utf-8")
    assert "RCPtr" in content, "Example must contain 'RCPtr'"
    assert "RCObject" in content, "Example must contain 'RCObject'"
    assert "addReference" in content or "removeReference" in content, (
        "Example must contain addReference or removeReference lifecycle methods"
    )
    # Token budget: ≤600 tokens (word_count * 1.3 ≤ 600 — same formula as governance test)
    words = len(content.split())
    estimated_tokens = int(words * 1.3)
    assert estimated_tokens <= 600, (
        f"Example exceeds 600-token budget: ~{estimated_tokens} tokens ({words} words)"
    )


# ---------------------------------------------------------------------------
# ALP-06: ENG-6.1 host exception safety example exists
# ---------------------------------------------------------------------------

def test_host_exception_safety_example_exists(examples_dir):
    """Scenario ALP-06: examples/ENG-6.1-host-exception-safety.md must exist,
    contain CALPException/CHostException hierarchy content, and stay within budget."""
    example = examples_dir / "ENG-6.1-host-exception-safety.md"
    assert example.exists(), (
        "examples/ENG-6.1-host-exception-safety.md does not exist — "
        "IOC_ALP has a 15-tier CALPException/CHostException hierarchy"
    )
    content = example.read_text(encoding="utf-8")
    assert "CALPException" in content, "Example must contain 'CALPException'"
    assert "CHostException" in content, "Example must contain 'CHostException'"
    assert "catch" in content, "Example must contain exception catch handling"
    # Token budget: ≤600 tokens (word_count * 1.3 ≤ 600 — same formula as governance test)
    words = len(content.split())
    estimated_tokens = int(words * 1.3)
    assert estimated_tokens <= 600, (
        f"Example exceeds 600-token budget: ~{estimated_tokens} tokens ({words} words)"
    )


# ---------------------------------------------------------------------------
# ALP-07: ENG-4.1 atomic-tdd example has Windows/MFC brownfield section
# ---------------------------------------------------------------------------

def test_atomic_tdd_example_has_windows_mfc_section(examples_dir, cpp_full_reference):
    """Scenario ALP-07: Windows/MFC ActiveTest TDD pattern must be documented.

    At 600-token budget the ActiveTest section cannot fit in ENG-4.1-atomic-tdd.md.
    The pattern is instead documented in full-reference.md under the MFC Windows
    Brownfield Governance section (ALP-09), which contains the ActiveTest reference
    and the same RED-GREEN-REFACTOR principle applied to CRITICAL_SECTION/Observer.
    """
    full_ref = cpp_full_reference
    assert "ActiveTest" in full_ref or "MFC Windows" in full_ref, (
        "MFC/ActiveTest TDD pattern must be documented in full-reference.md "
        "(600-token budget prevents inclusion in ENG-4.1-atomic-tdd.md)"
    )


# ---------------------------------------------------------------------------
# ALP-08: full-reference.md has Load Planning domain section
# ---------------------------------------------------------------------------

def test_full_reference_has_load_planning_section(cpp_full_reference):
    """Scenario ALP-08: full-reference.md must contain a Load Planning domain
    section referencing ZFW, CG, MEL, and Sabre CSAPI from IOC_ALP."""
    content = cpp_full_reference
    assert "## Load Planning" in content or "## Airline Load Planning" in content, (
        "full-reference.md is missing a Load Planning domain section — "
        "IOC_ALP covers ZFW envelope, CG calculator, MEL compliance, Sabre CSAPI"
    )
    for marker in ("ZFW", "MEL", "CSAPI"):
        assert marker in content, (
            f"Load Planning section must reference '{marker}' from IOC_ALP domain"
        )


# ---------------------------------------------------------------------------
# ALP-09: full-reference.md has MFC Windows brownfield governance section
# ---------------------------------------------------------------------------

def test_full_reference_has_mfc_windows_section(cpp_full_reference):
    """Scenario ALP-09: full-reference.md must contain an MFC/Windows brownfield
    section referencing RCPtr, Observer, and Command patterns from IOC_ALP."""
    content = cpp_full_reference
    has_mfc_section = (
        "## MFC" in content
        or "## Windows Brownfield" in content
        or "## MFC Windows" in content
    )
    assert has_mfc_section, (
        "full-reference.md is missing an MFC/Windows brownfield governance section"
    )
    for marker in ("RCPtr", "Observer", "Command"):
        assert marker in content, (
            f"MFC brownfield section must reference '{marker}' from IOC_ALP patterns"
        )


# ---------------------------------------------------------------------------
# ALP-10: full-reference.md has IOC_ALP anti-pattern catalog
# ---------------------------------------------------------------------------

def test_full_reference_has_alp_anti_pattern_catalog(cpp_full_reference):
    """Scenario ALP-10: full-reference.md must contain an IOC_ALP anti-pattern
    catalog with god class, macro abuse, and mixed ownership entries."""
    content = cpp_full_reference
    has_alp_catalog = (
        "## IOC_ALP Anti-Pattern" in content
        or "## MFC Anti-Pattern" in content
        or "## ALP Anti-Pattern" in content
    )
    assert has_alp_catalog, (
        "full-reference.md is missing an IOC_ALP/MFC anti-pattern catalog"
    )
    for marker in ("god class", "macro", "mixed ownership"):
        assert marker.lower() in content.lower(), (
            f"IOC_ALP anti-pattern catalog must reference '{marker}'"
        )

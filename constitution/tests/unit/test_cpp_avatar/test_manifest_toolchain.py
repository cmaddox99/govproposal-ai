"""Test 1.3: C++ avatar has stack metadata, compiler/build options, and toolchain matrix.

Scenario ID: c-plus-plus-avatar-enrichment/1.3
Law: ENG-11.1, ENG-5.1

Content routing: ci_toolchain moved from manifest.yaml to
ENG-5.2-cmake-governance.md per avatar-model-schema §3 (unknown block).
"""
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
CI_EXAMPLE = REPO / "avatars" / "technology" / "cpp" / "examples" / "ENG-5.2-cmake-governance.md"


def test_cpp_manifest_has_compiler_and_toolchain_metadata(manifest_data):
    """manifest.yaml must document compilers and version policy;
    CI toolchain must exist in ENG-5.2 example."""
    manifest = manifest_data

    stack = manifest["stack"]

    # Compiler options must be listed
    assert "compilers" in stack, "stack.compilers is required (e.g., GCC, Clang, MSVC)"
    compilers = stack["compilers"]
    assert isinstance(compilers, (list, dict)), (
        "stack.compilers must list at least 2 supported compilers"
    )
    if isinstance(compilers, dict):
        total = sum(len(v) for v in compilers.values())
        assert total >= 2, "stack.compilers must list at least 2 supported compilers"
    else:
        assert len(compilers) >= 2, "stack.compilers must list at least 2 supported compilers"

    # Version policy must be documented
    assert "version_policy" in stack, "stack.version_policy is required"
    vp = stack["version_policy"]
    assert "greenfield" in vp, "version_policy.greenfield is required"
    assert "brownfield" in vp, "version_policy.brownfield is required"

    # CI toolchain in ENG-5.2-cmake-governance.md example
    ci_text = CI_EXAMPLE.read_text(encoding="utf-8")
    assert "CI Toolchain Requirements" in ci_text, \
        "ENG-5.2-cmake-governance.md must have CI Toolchain Requirements section"
    ci_lower = ci_text.lower()
    assert "clang-tidy" in ci_lower, "CI toolchain must list clang-tidy"
    assert "addresssanitizer" in ci_lower or "asan" in ci_lower, "CI toolchain must list ASan"
    assert "undefinedbehaviorsanitizer" in ci_lower or "ubsan" in ci_lower, "CI toolchain must list UBSan"

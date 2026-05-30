"""CWR C++ Avatar Enrichment Tests.

Scenario IDs: CWR-01 through CWR-10
Law: ENG-11.1, ENG-10.1
Proposal: hangar-ai-specs/changes/cwr-cpp-avatar-enrichment/PROPOSAL.md

Validates that the C++ avatar is grounded in patterns observed in the
CWR CrewRecoveryFAR117 codebase (C++98, NetBeans Makefiles, JNI, Xpress MP,
FAR Part 117 crew rest compliance).
"""

import pytest
import yaml
from pathlib import Path


# ---------------------------------------------------------------------------
# CWR-01: manifest has brownfield_makefile commands
# ---------------------------------------------------------------------------

def test_manifest_has_brownfield_makefile_commands(manifest_data):
    """Scenario CWR-01: manifest commands block must contain a brownfield_makefile
    key with the NetBeans make command used in CWR (Makefile-CI-Release.mk)."""
    commands = manifest_data.get("commands", {})
    assert "brownfield_makefile" in commands, (
        "commands block is missing 'brownfield_makefile' key — "
        "CWR uses NetBeans Makefiles, not CMake"
    )
    build_cmd = commands["brownfield_makefile"].get("build", "")
    assert "nbproject/Makefile-CI-Release.mk" in build_cmd, (
        f"brownfield_makefile.build must reference 'nbproject/Makefile-CI-Release.mk', got: '{build_cmd}'"
    )


# ---------------------------------------------------------------------------
# CWR-02: manifest has brownfield_jni_stack dependencies
# ---------------------------------------------------------------------------

def test_manifest_has_brownfield_jni_stack_dependencies(manifest_data):
    """Scenario CWR-02: manifest dependencies block must contain a brownfield_jni_stack
    key listing the CWR-specific library stack (Xpress MP, jsoncpp, TinyXML, JNI)."""
    deps = manifest_data.get("dependencies", {})
    assert "brownfield_jni_stack" in deps, (
        "dependencies block is missing 'brownfield_jni_stack' key — "
        "CWR uses Xpress MP / jsoncpp / TinyXML / JNI, not Abseil/gRPC/OpenSSL"
    )
    stack = deps["brownfield_jni_stack"]
    stack_str = str(stack).lower()
    for expected in ("xpress", "jsoncpp", "tinyxml", "jni"):
        assert expected in stack_str, (
            f"brownfield_jni_stack must reference '{expected}', got: {stack}"
        )


# ---------------------------------------------------------------------------
# CWR-03: manifest has brownfield_cpp98 naming conventions
# ---------------------------------------------------------------------------

def test_manifest_has_brownfield_cpp98_naming_conventions(manifest_data):
    """Scenario CWR-03: manifest conventions block must contain a brownfield_cpp98
    key documenting CWR's C++98 naming patterns (Node suffix, Inf suffix, XL_ prefix)."""
    conventions = manifest_data.get("conventions", {})
    assert "brownfield_cpp98" in conventions, (
        "conventions block is missing 'brownfield_cpp98' key — "
        "CWR uses C++98 with Node/Inf/XL_ naming idioms"
    )
    cpp98 = conventions["brownfield_cpp98"]
    cpp98_str = str(cpp98).lower()
    for expected in ("node", "inf", "xl_"):
        assert expected in cpp98_str, (
            f"brownfield_cpp98 conventions must reference '{expected}' naming idiom, got: {cpp98}"
        )


# ---------------------------------------------------------------------------
# CWR-04: manifest has brownfield_jni_solver project archetype
# ---------------------------------------------------------------------------

def test_manifest_project_archetypes_has_brownfield_jni_solver(manifest_data):
    """Scenario CWR-04: manifest project_archetypes block must contain a brownfield_jni_solver
    key documenting the CWR directory layout (Solver/, PopulateSolver/, XMLInput/, runSolver/)."""
    archetypes = manifest_data.get("activates", {}).get("project_archetypes", {})
    assert "brownfield_jni_solver" in archetypes, (
        "project_archetypes block is missing 'brownfield_jni_solver' key — "
        "CWR uses a flat JNI solver layout, not a CMake layered structure"
    )
    archetype = archetypes["brownfield_jni_solver"]
    archetype_str = str(archetype).lower()
    for expected in ("solver", "populatesolver", "xmlinput", "runsolver"):
        assert expected in archetype_str, (
            f"brownfield_jni_solver archetype must reference '{expected}' directory, got: {archetype}"
        )


# ---------------------------------------------------------------------------
# CWR-05: ENG-2.3 JNI ABI stability example file exists
# ---------------------------------------------------------------------------

def test_jni_abi_stability_example_exists(examples_dir):
    """Scenario CWR-05: examples/ENG-2.3-jni-abi-stability.md must exist and
    contain JNI ABI stability patterns grounded in CWR (jstring, JNIEnv, JNIEXPORT)."""
    example_file = examples_dir / "ENG-2.3-jni-abi-stability.md"
    assert example_file.exists(), (
        "examples/ENG-2.3-jni-abi-stability.md is missing — "
        "CWR requires JNI ABI stability guidance for its Java↔C++ bridge"
    )
    content = example_file.read_text(encoding="utf-8")
    assert "ENG-2.3" in content, "Example must reference law ENG-2.3"
    for marker in ("JNIEnv", "JNIEXPORT", "jstring"):
        assert marker in content, (
            f"JNI ABI stability example must include '{marker}', grounded in CWR patterns"
        )
    # Token budget: ≤600 tokens (word_count * 1.3 ≤ 600 — same formula as governance test)
    # Frontmatter is stripped — it is metadata and should not count against the content budget
    body_abi = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body_abi = parts[2]
    words = len(body_abi.split())
    estimated_tokens = int(words * 1.3)
    assert estimated_tokens <= 600, (
        f"Example exceeds 600-token budget: ~{estimated_tokens} tokens ({words} words)"
    )
# ---------------------------------------------------------------------------

def test_atomic_tdd_example_has_brownfield_section(examples_dir):
    """Scenario CWR-07: the brownfield characterization test pattern must be documented.

    At 600-token budget the content cannot fit in ENG-4.1-atomic-tdd.md alongside
    the primary TDD example. It is instead covered by the dedicated
    ENG-4.1-characterization-test-pattern.md example file (530 tokens).
    This test asserts that dedicated file exists with the CWR/legacy content.
    """
    char_test = examples_dir / "ENG-4.1-characterization-test-pattern.md"
    assert char_test.exists(), (
        "ENG-4.1-characterization-test-pattern.md must exist — "
        "brownfield/characterization TDD pattern documented in dedicated file (600-token budget constraint)"
    )
    content = char_test.read_text(encoding="utf-8")
    assert "characterization" in content.lower() or "characterisation" in content.lower(), (
        "ENG-4.1-characterization-test-pattern.md must use 'characterization' terminology"
    )


# ---------------------------------------------------------------------------
# CWR-08: full-reference.md has JNI Safety section
# ---------------------------------------------------------------------------

def test_full_reference_has_jni_safety_section(cpp_full_reference):
    """Scenario CWR-08: docs/guides/avatars/cpp/full-reference.md must contain
    a JNI Safety section covering extern C, JNIEXPORT, exception barrier,
    and ABI governance patterns from the CWR codebase."""
    content = cpp_full_reference
    assert "JNI Safety" in content, (
        "full-reference.md is missing a 'JNI Safety' section — "
        "required for CWR brownfield JNI bridge governance"
    )
    for marker in ("extern \"C\"", "JNIEXPORT", "ExceptionClear", "ABI"):
        assert marker in content, (
            f"JNI Safety section must cover '{marker}'"
        )


# ---------------------------------------------------------------------------
# CWR-09: full-reference.md has FAR 117 aviation safety section
# ---------------------------------------------------------------------------

def test_full_reference_has_far117_section(cpp_full_reference):
    """Scenario CWR-09: docs/guides/avatars/cpp/full-reference.md must contain
    a FAR 117 Aviation Safety section grounded in CWR patterns — covering crew
    rest/duty compliance, characterization tests, and golden-file validation."""
    content = cpp_full_reference
    assert "FAR 117" in content, (
        "full-reference.md is missing a 'FAR 117' section — "
        "required for CWR crew rest/duty compliance governance"
    )
    # Must have a dedicated ## heading for FAR 117 content
    assert any(
        f"## {h}" in content
        for h in ("FAR 117", "FAR Part 117", "Aviation Safety — FAR 117", "FAR 117 Crew Rest")
    ), "full-reference.md must have a ## heading dedicated to FAR 117 guidance"
    # Must reference the CWR-specific functions observed in the codebase
    for marker in ("MinRest", "characterization", "golden"):
        assert marker.lower() in content.lower(), (
            f"FAR 117 section must reference '{marker}' — grounded in CWR patterns"
        )


# ---------------------------------------------------------------------------
# CWR-10: full-reference.md has CWR anti-pattern catalog section
# ---------------------------------------------------------------------------

def test_full_reference_has_cwr_anti_pattern_catalog(cpp_full_reference):
    """Scenario CWR-10: docs/guides/avatars/cpp/full-reference.md must contain
    a CWR Anti-Pattern Catalog section documenting the top anti-patterns observed
    in the CrewRecoveryFAR117 codebase (god class, raw malloc, global extern, etc.)."""
    content = cpp_full_reference
    assert "Anti-Pattern" in content and "CWR" in content, (
        "full-reference.md is missing a CWR Anti-Pattern Catalog section"
    )
    # Must have a dedicated ## heading
    assert any(
        h in content
        for h in ("## CWR Anti-Pattern", "## CWR C++98 Anti-Pattern", "## Brownfield Anti-Pattern")
    ), "full-reference.md must have a ## heading for the CWR anti-pattern catalog"
    # Must cover the key anti-patterns observed in the codebase scan
    for pattern in ("god class", "malloc", "extern", "throw"):
        assert pattern.lower() in content.lower(), (
            f"CWR anti-pattern catalog must document '{pattern}' pattern"
        )
# ---------------------------------------------------------------------------

def test_safety_critical_jni_example_exists(examples_dir):
    """Scenario CWR-06: examples/ENG-6.1-safety-critical-jni.md must exist and
    contain safety patterns for JNI in aviation-critical context (FAR 117, null
    guards, no C++ exceptions crossing JNI boundary)."""
    example_file = examples_dir / "ENG-6.1-safety-critical-jni.md"
    assert example_file.exists(), (
        "examples/ENG-6.1-safety-critical-jni.md is missing — "
        "CWR is FAR 117 safety-critical; JNI exception handling guidance is required"
    )
    content = example_file.read_text(encoding="utf-8")
    assert "ENG-6.1" in content, "Example must reference law ENG-6.1"
    for marker in ("FAR", "JNIEnv", "ExceptionClear"):
        assert marker in content, (
            f"Safety-critical JNI example must include '{marker}'"
        )
    # Token budget: ≤600 tokens (word_count * 1.3 ≤ 600 — same formula as governance test)
    # Frontmatter is stripped — it is metadata and should not count against the content budget
    body_jni = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            body_jni = parts[2]
    words = len(body_jni.split())
    estimated_tokens = int(words * 1.3)
    assert estimated_tokens <= 600, (
        f"Example exceeds 600-token budget: ~{estimated_tokens} tokens ({words} words)"
    )


# ---------------------------------------------------------------------------
# Amendment R-01: ref-safety-aviation.md exists and contains aviation sections
# ---------------------------------------------------------------------------

def test_safety_aviation_ref_file_exists_and_within_token_budget(cpp_dir):
    """Scenario R-01 (updated Phase 13): ref-safety-aviation.md was split into
    ref-safety-jni-abi.md (JNI Safety) and ref-safety-far117-cwr.md (FAR 117, CWR).
    Both files must exist and be within the 3,500-token RAG context ceiling."""
    jni_file = cpp_dir / "refs/safety/ref-safety-jni-abi.md"
    far117_file = cpp_dir / "refs/safety/ref-safety-far117-cwr.md"

    assert jni_file.exists(), (
        "ref-safety-jni-abi.md is missing — Phase 13 rightsizing split not done"
    )
    assert far117_file.exists(), (
        "ref-safety-far117-cwr.md is missing — Phase 13 rightsizing split not done"
    )

    jni_content = jni_file.read_text(encoding="utf-8")
    assert "JNI Safety" in jni_content, "ref-safety-jni-abi.md must contain 'JNI Safety' section"

    far117_content = far117_file.read_text(encoding="utf-8")
    for section in ("FAR 117", "CWR Anti-Pattern"):
        assert section in far117_content, (
            f"ref-safety-far117-cwr.md must contain '{section}' section"
        )

    for label, path in [("refs/safety/ref-safety-jni-abi.md", jni_file), ("refs/safety/ref-safety-far117-cwr.md", far117_file)]:
        words = len(path.read_text(encoding="utf-8").split())
        tokens = int(words * 1.33)
        assert tokens <= 3500, (
            f"{label} exceeds 3,500-token RAG ceiling: ~{tokens}t ({words} words). "
            "Split further or trim content."
        )


# ---------------------------------------------------------------------------
# Amendment X-01: ref-safety-far117-cwr.md must contain WCET annotation guidance
# ---------------------------------------------------------------------------

def test_safety_aviation_ref_has_wcet_guidance(cpp_dir):
    """Amendment X-01 (P6 advisory, updated Phase 13): ref-safety-far117-cwr.md must include WCET
    annotation guidance. DO-278A AL 2/3 ground systems like CWR require documented
    worst-case execution time for scheduling functions."""
    far117_file = cpp_dir / "refs/safety/ref-safety-far117-cwr.md"
    assert far117_file.exists(), "ref-safety-far117-cwr.md does not exist"
    content = far117_file.read_text(encoding="utf-8")
    assert "WCET" in content or "Worst-Case Execution Time" in content, (
        "ref-safety-far117-cwr.md must contain WCET annotation guidance — "
        "DO-278A AL 2/3 requires documented worst-case execution time (Amendment X-01)"
    )


# ---------------------------------------------------------------------------
# Amendment X-02: ENG-4.1-far117-traceability.md must address timeout risk
# ---------------------------------------------------------------------------

def test_far117_traceability_example_has_timeout_edge_case(examples_dir):
    """Amendment X-02 (P6 advisory): ENG-4.1-far117-traceability.md Edge Cases
    must address timeout/default-result risk. A scheduling algorithm that times out
    and returns a default 'approved' result bypasses FAR 117 validation — this
    must be called out explicitly in the example."""
    example_file = examples_dir / "ENG-4.1-far117-traceability.md"
    assert example_file.exists(), "ENG-4.1-far117-traceability.md does not exist"
    content = example_file.read_text(encoding="utf-8")
    assert "Edge Cases" in content, (
        "ENG-4.1-far117-traceability.md must have '## Edge Cases' section (Amendment X-02)"
    )
    content_lower = content.lower()
    assert "timeout" in content_lower or "time out" in content_lower, (
        "ENG-4.1-far117-traceability.md Edge Cases must address timeout/default-result "
        "risk — a FAR 117 scheduler that times out and returns 'approved' by default "
        "is a silent regulatory violation (Amendment X-02)"
    )

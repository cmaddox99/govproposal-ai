"""Test 4.2: AVATAR-RAG-INDEX.yaml contains C++ technology avatar entry.

Scenario ID: c-plus-plus-avatar-enrichment/4.2
Law: ENG-6.7 (Audit Trail — avatar must be RAG-indexed for retrieval)
"""

import re as _re

import yaml as _yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return _yaml.safe_load(parts[1]) or {}
    except Exception:
        return {}


def _cpp_section(content: str) -> str:
    """Extract the full cpp: block from AVATAR-RAG-INDEX.yaml.

    Reads from '  cpp:' to the next sibling top-level key (same 2-space
    indent) so the window never needs manual adjustment as the section grows.
    """
    import re
    start = content.index("  cpp:")
    # Find the next sibling key at the same 2-space indentation level
    m = re.search(r"\n  [a-z]", content[start + 6:])
    end = start + 6 + m.start() if m else len(content)
    return content[start:end]


def test_rag_index_contains_cpp_avatar():
    """The RAG index must include a C++ entry with files, laws, search queries, and anti-patterns."""
    rag_path = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"
    content = rag_path.read_text(encoding="utf-8")

    # Entry must exist under technology_avatars
    assert "cpp:" in content, "AVATAR-RAG-INDEX.yaml must contain cpp entry"
    assert "id: cpp" in content
    assert "C++" in content

    cpp_section = _cpp_section(content)

    # Must declare files
    assert "manifest:" in cpp_section, "cpp must declare manifest file"
    assert "guidance:" in cpp_section, "cpp must declare guidance file"

    # Must specialize key laws
    for law in ["ENG-4.1", "ENG-6.1", "ENG-6.7", "ENG-3.1"]:
        assert law in cpp_section, f"cpp must specialize {law}"

    # Must have search queries
    assert "search_queries:" in cpp_section
    query_lines = [l for l in cpp_section.split("\n") if "→" in l or "->" in l]
    assert len(query_lines) >= 4, f"Must have ≥4 search queries, found {len(query_lines)}"

    # Must have anti-patterns
    assert "anti_patterns:" in cpp_section
    anti_start = cpp_section.index("anti_patterns:")
    anti_section = cpp_section[anti_start:]
    anti_lines = [l for l in anti_section.split("\n") if l.strip().startswith("- DO NOT")]
    assert len(anti_lines) >= 3, f"Must have ≥3 anti-patterns, found {len(anti_lines)}"


def test_rag_index_cpp_declares_full_reference():
    """cpp-split-reference-architecture: cpp section must declare reference_index (new pseudo-RAG architecture)."""
    rag_path = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"
    cpp_section = _cpp_section(rag_path.read_text(encoding="utf-8"))

    assert "reference_index:" in cpp_section, (
        "cpp files block must declare reference_index (avatars/technology/cpp/reference-index.md)"
    )
    assert "reference-index.md" in cpp_section, (
        "reference_index must point to avatars/technology/cpp/reference-index.md"
    )


def test_rag_index_cpp_section_queries_use_full_reference():
    """cpp-split-reference-architecture: queries must route to ref-*.md files (not full-reference.md)."""
    rag_path = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"
    cpp_section = _cpp_section(rag_path.read_text(encoding="utf-8"))

    # All ref-file queries must point to ref-*.md files
    ref_queries = [
        l.strip() for l in cpp_section.split("\n")
        if ("→" in l or "->" in l) and "ref-" in l
    ]
    assert len(ref_queries) >= 10, (
        f"Expected ≥10 queries routing to ref-*.md files, found {len(ref_queries)}"
    )


def test_rag_index_cpp_no_dead_compliance_rating_ref():
    """compliance-rating-system.md was deleted (Amendment O V6); no RAG query should reference it."""
    rag_path = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"
    cpp_section = _cpp_section(rag_path.read_text(encoding="utf-8"))

    assert "compliance-rating-system.md" not in cpp_section, (
        "compliance-rating-system.md was deleted in Amendment O V6; remove from RAG queries"
    )


def test_split_reference_files_exist_on_disk():
    """Split reference architecture: all ref-*.md files must exist (full-reference.md was deleted after migration)."""
    cpp_dir = REPO_ROOT / "avatars" / "technology" / "cpp"
    ref_files = sorted(cpp_dir.rglob("ref-*.md"))
    assert len(ref_files) >= 15, (
        f"Expected ≥15 ref-*.md files (split from full-reference.md), found {len(ref_files)}"
    )
    total_content = sum(len(f.read_text(encoding="utf-8")) for f in ref_files)
    assert total_content > 10000, (
        f"Total ref-*.md content seems too short ({total_content} chars)"
    )


# ---------------------------------------------------------------------------
# Amendment S-01 (updated Phase 2): ref-testing-ci.md deleted; must not appear
# ---------------------------------------------------------------------------

def test_reference_index_has_no_redundant_testing_ci_rows():
    """Amendment S-01 (Phase 2): ref-testing-ci.md was split into 3 files and deleted.
    reference-index.md must NOT contain any reference to ref-testing-ci.md."""
    ref_index = REPO_ROOT / "avatars" / "technology" / "cpp" / "reference-index.md"
    lines = ref_index.read_text(encoding="utf-8").splitlines()
    row_count = sum(1 for line in lines if "ref-testing-ci.md" in line)
    assert row_count == 0, (
        f"reference-index.md has {row_count} rows pointing to ref-testing-ci.md "
        f"(expected 0 — ref-testing-ci.md was deleted in Phase 2 rightsizing)"
    )


# ---------------------------------------------------------------------------
# Amendment S-02: skill-cpp-legacy-modernization has ActiveTest trigger phrases
# ---------------------------------------------------------------------------

def test_legacy_modernization_skill_has_activetest_triggers():
    """Amendment S-02: skill-cpp-legacy-modernization.md must include trigger
    phrases for ActiveTest/TestRunner.lib migration so IOC_ALP developers are
    routed to the correct skill when asking about test harness migration."""
    skill_path = (REPO_ROOT / "agent-skills" / "skills-by-domain"
                  / "platform-engineering" / "skill-cpp-legacy-modernization.md")
    content = skill_path.read_text(encoding="utf-8")
    for phrase in ("ActiveTest migration", "TestRunner.lib replace"):
        assert phrase in content, (
            f"skill-cpp-legacy-modernization.md missing trigger phrase '{phrase}' — "
            "IOC_ALP developers asking about test harness migration won't reach this skill"
        )


# ---------------------------------------------------------------------------
# Amendment W-01: skill-cpp-jni-bridge.md must declare platform-engineering category
# ---------------------------------------------------------------------------

def test_jni_bridge_skill_category_is_platform_engineering():
    """Amendment W-01: skill-cpp-jni-bridge.md lives in platform-engineering/ but
    its frontmatter declares category: development-practices. Routing tools that
    filter by category will miss this skill under platform-engineering queries."""
    skill_path = (REPO_ROOT / "agent-skills" / "skills-by-domain"
                  / "platform-engineering" / "skill-cpp-jni-bridge.md")
    content = skill_path.read_text(encoding="utf-8")
    assert "category: platform-engineering" in content, (
        "skill-cpp-jni-bridge.md frontmatter must declare 'category: platform-engineering' — "
        "currently declares 'category: development-practices' causing routing misses"
    )


# ---------------------------------------------------------------------------
# Amendment W-02: ENG-4.1-googletest-migration.md title must include IOC_ALP context
# ---------------------------------------------------------------------------

def test_googletest_migration_example_title_has_ioCalp_prefix():
    """Amendment W-02: ENG-4.1-googletest-migration.md title field must surface
    IOC_ALP specificity so agents retrieving by title know the example is scoped
    to the IOC_ALP ActiveTest.h migration pattern."""
    example_path = REPO_ROOT / "avatars" / "technology" / "cpp" / "examples" / "ENG-4.1-googletest-migration.md"
    content = example_path.read_text(encoding="utf-8")
    assert "IOC_ALP:" in content, (
        "ENG-4.1-googletest-migration.md frontmatter title must begin with 'IOC_ALP:' — "
        "agents retrieving by title cannot determine IOC_ALP scope without it"
    )


# ---------------------------------------------------------------------------
# Amendment W-04: All followed_by references in skill-cpp-*.md must resolve
# ---------------------------------------------------------------------------

def test_followed_by_references_are_valid():
    """Amendment W-04: Every followed_by skill ID declared in a skill-cpp-*.md
    file must be a registered skill ID somewhere in the skills-by-domain tree.
    A typo in followed_by is undetectable without this guard."""
    import yaml

    skills_root = REPO_ROOT / "agent-skills" / "skills-by-domain"

    # Collect all registered skill IDs across all domains
    all_skill_ids: set[str] = set()
    for skill_file in skills_root.rglob("*.md"):
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        fm_text = text.split("---")[1]
        try:
            data = yaml.safe_load(fm_text)
            if isinstance(data, dict) and "skill" in data:
                sid = data["skill"].get("id")
                if sid:
                    all_skill_ids.add(sid)
        except Exception:
            pass

    # Verify every followed_by entry in cpp skills resolves
    pe_dir = skills_root / "platform-engineering"
    bad_refs: list[str] = []
    for skill_file in sorted(pe_dir.glob("skill-cpp-*.md")):
        text = skill_file.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        fm_text = text.split("---")[1]
        try:
            data = yaml.safe_load(fm_text)
            if not isinstance(data, dict) or "skill" not in data:
                continue
            for fb_id in (data.get("followed_by") or []):
                if fb_id not in all_skill_ids:
                    bad_refs.append(f"{skill_file.name}: followed_by '{fb_id}' not in registry")
        except Exception:
            pass

    assert not bad_refs, (
        f"Found {len(bad_refs)} unresolved followed_by reference(s):\n"
        + "\n".join(f"  {r}" for r in bad_refs)
        + "\n\nAll followed_by IDs must be registered skill IDs."
    )


# ===========================================================================
# cpp-version-routing-foundation — Phase 1 RED tests (Tasks 1.1 – 1.14)
# Proposal: hangar-ai-specs/changes/cpp-version-routing-foundation/PROPOSAL.md
# Scenario ID: cpp-version-routing-foundation/1.x
# All tests below FAIL until Phase 2–5 implementation is complete,
# EXCEPT 1.9 and 1.13 which are guard tests that pass vacuously until
# Phase 4 adds version notes.
# ===========================================================================

_CPP_EXAMPLES = REPO_ROOT / "avatars" / "technology" / "cpp" / "examples"
_CPP_GUIDANCE = REPO_ROOT / "avatars" / "technology" / "cpp" / "guidance.md"
_RAG_INDEX = REPO_ROOT / "avatars" / "AVATAR-RAG-INDEX.yaml"
_CPP_TEMPLATES = REPO_ROOT / "avatars" / "technology" / "cpp" / "templates"


# --- 1.1 --------------------------------------------------------------------

def test_guidance_has_version_protocol_section():
    """1.1 (RED): guidance.md must contain ## Version Context Protocol section."""
    content = _CPP_GUIDANCE.read_text(encoding="utf-8")
    assert "## Version Context Protocol" in content, (
        "guidance.md must contain '## Version Context Protocol' section — "
        "this is the always-loaded routing instruction for version-aware C++ advice"
    )


# --- 1.2 --------------------------------------------------------------------

def test_guidance_version_protocol_detection_order():
    """1.2 (RED): Version Context Protocol section must include the 5-step detection order."""
    content = _CPP_GUIDANCE.read_text(encoding="utf-8")
    assert "## Version Context Protocol" in content, "Section missing — see test 1.1"
    start = content.index("## Version Context Protocol")
    m = _re.search(r"\n## ", content[start + 5:])
    section = content[start: start + 5 + m.start()] if m else content[start:]
    for term in (".copilot/project.yaml", "CMakeLists.txt", ".vcxproj", "Makefile", ".dsp"):
        assert term in section, (
            f"Version Context Protocol section must mention detection source '{term}'"
        )


# --- 1.3 --------------------------------------------------------------------

def test_guidance_version_protocol_routing_table():
    """1.3 (RED): Version Context Protocol section must include routing table with all 5 tiers."""
    content = _CPP_GUIDANCE.read_text(encoding="utf-8")
    assert "## Version Context Protocol" in content, "Section missing — see test 1.1"
    start = content.index("## Version Context Protocol")
    m = _re.search(r"\n## ", content[start + 5:])
    section = content[start: start + 5 + m.start()] if m else content[start:]
    for tier in ("legacy", "brownfield", "transitional", "modern", "greenfield"):
        assert tier in section.lower(), (
            f"Version Context Protocol routing table must include tier '{tier}'"
        )


# --- 1.4 --------------------------------------------------------------------

def test_rag_index_has_version_routing_policy():
    """1.4 (RED): AVATAR-RAG-INDEX.yaml cpp section must contain version_routing_policy block."""
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "version_routing_policy:" in cpp_section, (
        "AVATAR-RAG-INDEX.yaml cpp section must contain 'version_routing_policy:' block — "
        "this is the machine-readable routing policy for C++ version-aware content delivery"
    )


# --- 1.5 --------------------------------------------------------------------

def test_version_routing_policy_has_all_tiers():
    """1.5 (RED): version_routing_policy.by_standard must contain all 5 canonical tier keys."""
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "version_routing_policy:" in cpp_section, "version_routing_policy missing — see 1.4"
    start = cpp_section.index("version_routing_policy:")
    policy_text = cpp_section[start:]
    for tier in ("legacy", "brownfield", "transitional", "modern", "greenfield"):
        assert f"{tier}:" in policy_text, (
            f"version_routing_policy.by_standard must contain tier key '{tier}'"
        )


# --- 1.6 --------------------------------------------------------------------

def test_law_mapped_examples_have_cpp_version_min():
    """1.6 (RED): Every ENG-*.md example file with law_id frontmatter must have cpp_version_min."""
    missing = []
    for f in sorted(_CPP_EXAMPLES.glob("ENG-*.md")):
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        if "law_id" in fm and "cpp_version_min" not in fm:
            missing.append(f.name)
    assert not missing, (
        f"{len(missing)} law-mapped example file(s) missing 'cpp_version_min' frontmatter:\n"
        + "\n".join(f"  {n}" for n in missing[:10])
        + (f"\n  ... and {len(missing) - 10} more" if len(missing) > 10 else "")
    )


# --- 1.7 --------------------------------------------------------------------

def test_modern_examples_have_cpp_version_note():
    """1.7 (RED): Example files with cpp_version_min in (17, 20, 23) must have cpp_version_note.

    Also asserts that ≥8 such files exist (once frontmatter tagging is complete),
    causing this test to FAIL in the RED phase before Phase 4 runs.
    """
    needs_note, missing_note = [], []
    for f in sorted(_CPP_EXAMPLES.glob("ENG-*.md")):
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        if fm.get("cpp_version_min") in (17, 20, 23):
            needs_note.append(f.name)
            if "cpp_version_note" not in fm:
                missing_note.append(f.name)
    assert len(needs_note) >= 8, (
        f"Expected ≥8 example files with cpp_version_min in (17, 20, 23), "
        f"found {len(needs_note)} — frontmatter tagging not yet complete (Phase 4)"
    )
    assert not missing_note, (
        f"{len(missing_note)} file(s) with cpp_version_min in (17,20,23) are missing 'cpp_version_note':\n"
        + "\n".join(f"  {n}" for n in missing_note)
    )


# --- 1.8 --------------------------------------------------------------------

def test_cpp_project_template_exists():
    """1.8 (RED): avatars/technology/cpp/templates/cpp-project.yaml must exist."""
    template = _CPP_TEMPLATES / "cpp-project.yaml"
    assert template.exists(), (
        f"Project declaration template not found at {template} — "
        "teams need this file to copy to .copilot/project.yaml in their consuming repo"
    )


# --- 1.9 (guard) ------------------------------------------------------------

def test_guidance_token_budget():
    """1.9 (GUARD): guidance.md must remain ≤ 600 tokens after Version Context Protocol addition.

    Passes vacuously before Phase 2 (guidance.md is ~310t now). Guards against
    exceeding the always-loaded per-query overhead budget after Phase 2 adds ~200t.
    """
    tokens_approx = len(_CPP_GUIDANCE.read_text(encoding="utf-8")) // 4
    assert tokens_approx <= 600, (
        f"guidance.md is approximately {tokens_approx}t — exceeds 600t always-loaded ceiling. "
        "Trim the Version Context Protocol section or other guidance.md prose."
    )


# --- 1.10 -------------------------------------------------------------------

def test_routing_policy_file_refs_exist():
    """1.10 (RED): Every path in version_routing_policy prefer/avoid lists must exist on disk."""
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "version_routing_policy:" in cpp_section, "version_routing_policy missing — see 1.4"
    cpp_root = REPO_ROOT / "avatars" / "technology" / "cpp"
    path_lines = _re.findall(r"- ((?:refs|examples)/[^\s\n]+\.md)", cpp_section)
    assert len(path_lines) >= 10, (
        f"Expected ≥10 path references in version_routing_policy prefer/avoid lists, "
        f"found {len(path_lines)}"
    )
    missing = [p for p in path_lines if not (cpp_root / p).exists()]
    assert not missing, (
        f"{len(missing)} path reference(s) in version_routing_policy do not exist on disk:\n"
        + "\n".join(f"  {p}" for p in missing)
    )


# --- 1.11 -------------------------------------------------------------------

def test_routing_policy_tier_names_match_guidance():
    """1.11 (RED): Tier names in version_routing_policy must match those in guidance.md protocol."""
    content = _CPP_GUIDANCE.read_text(encoding="utf-8")
    assert "## Version Context Protocol" in content, "guidance.md missing protocol section — see 1.1"
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "version_routing_policy:" in cpp_section, "version_routing_policy missing — see 1.4"
    start = content.index("## Version Context Protocol")
    m = _re.search(r"\n## ", content[start + 5:])
    protocol_section = content[start: start + 5 + m.start()] if m else content[start:]
    policy_start = cpp_section.index("version_routing_policy:")
    policy_text = cpp_section[policy_start:]
    for tier in ("legacy", "brownfield", "transitional", "modern", "greenfield"):
        assert tier in protocol_section.lower(), (
            f"guidance.md Version Context Protocol must mention tier '{tier}'"
        )
        assert f"{tier}:" in policy_text, (
            f"AVATAR-RAG-INDEX.yaml version_routing_policy must contain tier key '{tier}'"
        )


# --- 1.12 -------------------------------------------------------------------

def test_project_template_has_pre98_standard():
    """1.12 (RED): templates/cpp-project.yaml must document 'pre98' as a valid standard value."""
    template = _CPP_TEMPLATES / "cpp-project.yaml"
    assert template.exists(), "Template not found — see test 1.8"
    assert "pre98" in template.read_text(encoding="utf-8"), (
        "cpp-project.yaml template must include 'pre98' as a documented valid value for "
        "the 'standard' field — SPEClient and similar pre-C++98 projects need to declare "
        "their toolchain tier"
    )


# --- 1.13 (guard) -----------------------------------------------------------

def test_cpp_version_note_max_length():
    """1.13 (GUARD): All cpp_version_note values must be ≤ 240 characters.

    Passes vacuously before Phase 4 adds notes. Guards against oversized notes
    that would inflate the per-query token budget.
    """
    violations = []
    for f in sorted(_CPP_EXAMPLES.glob("ENG-*.md")):
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        if fm.get("cpp_version_min") not in (17, 20, 23):
            continue
        note = str(fm.get("cpp_version_note", "") or "")
        if note and len(note) > 240:
            violations.append(f"{f.name}: {len(note)} chars (limit 240)")
    assert not violations, (
        f"{len(violations)} cpp_version_note(s) exceed 240-character limit:\n"
        + "\n".join(f"  {v}" for v in violations)
    )


# --- 1.14 -------------------------------------------------------------------

def test_routing_policy_prefer_refs_not_examples():
    """1.14 (RED): version_routing_policy prefer lists must use refs/ paths only."""
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "version_routing_policy:" in cpp_section, "version_routing_policy missing — see 1.4"
    start = cpp_section.index("version_routing_policy:")
    policy_block = cpp_section[start:]
    # Find all paths inside prefer: blocks (between "prefer:" and next sibling key or end)
    prefer_blocks = _re.findall(r"prefer:\s*\n((?:\s+- [^\n]+\n?)*)", policy_block)
    prefer_paths = _re.findall(r"- ((?:refs|examples)/[^\s\n]+\.md)", "\n".join(prefer_blocks))
    assert len(prefer_paths) >= 5, (
        f"Expected ≥5 file paths in prefer lists, found {len(prefer_paths)} — "
        "version_routing_policy prefer lists not yet populated"
    )
    bad_prefers = [p for p in prefer_paths if not p.startswith("refs/")]
    assert not bad_prefers, (
        f"prefer lists must contain only refs/* paths; found non-refs paths:\n"
        + "\n".join(f"  {p}" for p in bad_prefers)
    )


# ===========================================================================
# N1 / N2 / test-gap — Merge condition fixes (panel review: N1, N2, Thomas Hart gap)
# Scenario ID: cpp-version-routing-foundation/N1-N2
# ===========================================================================

# --- N1 ---------------------------------------------------------------------

def test_routing_policy_standards_are_strings():
    """N1: All values in version_routing_policy standards: lists must be quoted strings.

    Unquoted integers cause YAML type inconsistency: project.yaml uses standard: "14"
    (string) but the policy had standards: [17] (integer). Normalization prevents
    misclassification when consumers compare values across artifacts.
    """
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "version_routing_policy:" in cpp_section, "version_routing_policy missing — see 1.4"
    start = cpp_section.index("version_routing_policy:")
    policy_text = cpp_section[start:]
    # Find all standards: [...] inline lists
    standards_matches = _re.findall(r"standards:\s*\[([^\]]*)\]", policy_text)
    assert standards_matches, "No standards: lists found in version_routing_policy"
    type_errors = []
    for standards_str in standards_matches:
        for val in standards_str.split(","):
            val = val.strip()
            if not val:
                continue
            # Unquoted digit-only values are YAML integers — must be quoted strings
            if val.isdigit():
                type_errors.append(
                    f"Unquoted integer {val!r} — must be quoted string \"{val}\""
                )
    assert not type_errors, (
        "All version_routing_policy standards values must be quoted strings (not integers):\n"
        + "\n".join(f"  {e}" for e in type_errors)
        + "\n\nFix: change standards: [17] → standards: [\"17\"] etc."
    )


# --- N2a --------------------------------------------------------------------

def test_routing_policy_has_detection_order():
    """N2a: version_routing_policy must have a structured detection_order key.

    The detection precedence currently exists only as prose in guidance.md.
    Machine-readable form in AVATAR-RAG-INDEX.yaml prevents drift between
    the prose description and the policy data.
    """
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "version_routing_policy:" in cpp_section, "version_routing_policy missing — see 1.4"
    start = cpp_section.index("version_routing_policy:")
    policy_text = cpp_section[start:]
    assert "detection_order:" in policy_text, (
        "version_routing_policy must contain 'detection_order:' key — "
        "structured signal entries that mirror the detection order in guidance.md"
    )


# --- N2b --------------------------------------------------------------------

def test_detection_order_has_five_signals():
    """N2b: detection_order must have ≥5 signal entries (one per detection source)."""
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "version_routing_policy:" in cpp_section, "version_routing_policy missing"
    start = cpp_section.index("version_routing_policy:")
    policy_text = cpp_section[start:]
    assert "detection_order:" in policy_text, "detection_order missing — see N2a"
    order_start = policy_text.index("detection_order:")
    order_block = policy_text[order_start:]
    signal_entries = _re.findall(r"-\s+signal:", order_block)
    assert len(signal_entries) >= 5, (
        f"detection_order must have ≥5 signal entries (project.yaml, CMakeLists.txt, "
        f".vcxproj, Makefile, .dsp), found {len(signal_entries)}"
    )


# --- test gap ---------------------------------------------------------------

def test_guidance_warns_on_exact_standard():
    """Test gap: guidance.md conservative default must reference 'cpp.standard' explicitly.

    Using 'detected tier' only means a C++11 project can silently receive C++14 examples
    (both in 'transitional' tier). Referencing 'cpp.standard' instructs the agent to
    compare exact declared standard, not just tier, enabling intra-tier mismatch warnings.
    """
    content = _CPP_GUIDANCE.read_text(encoding="utf-8")
    assert "## Version Context Protocol" in content, "Section missing — see test 1.1"
    start = content.index("## Version Context Protocol")
    m = _re.search(r"\n## ", content[start + 5:])
    section = content[start: start + 5 + m.start()] if m else content[start:]
    # Find specifically the conservative default paragraph (must reference cpp.standard)
    conservative_match = _re.search(r"\*\*Conservative default:\*\*[^\n]+", section)
    assert conservative_match, (
        "Version Context Protocol section must contain a '**Conservative default:**' paragraph"
    )
    conservative_line = conservative_match.group(0)
    assert "cpp.standard" in conservative_line, (
        "Conservative default paragraph must reference 'cpp.standard' to enable exact-standard "
        "comparison within shared tiers (e.g., C++11 vs C++14 both in 'transitional'). "
        f"Current text: {conservative_line!r}"
    )


# ===========================================================================
# N3 + ENG-2.1 — pre-merge advisory fixes
# Scenario ID: cpp-version-routing-foundation/N3-ENG21
# ===========================================================================

# --- N3 ---------------------------------------------------------------------

def test_detection_order_signals_include_props_and_dsw():
    """N3: detection_order signals must align with guidance.md detection steps.

    guidance.md step 3: '*.vcxproj / *.props → <LanguageStandard>'
    guidance.md step 5: '.dsp / .dsw present → legacy'

    The RAG index detection_order had only '*.vcxproj' and '*.dsp'.
    Missing '*.props' means .NET SDK-style projects are not detected.
    Missing '.dsw' means MSVC 6.0 workspace files are not classified as legacy.
    """
    cpp_section = _cpp_section(_RAG_INDEX.read_text(encoding="utf-8"))
    assert "detection_order:" in cpp_section, "detection_order missing — see N2a"
    order_start = cpp_section.index("detection_order:")
    order_block = cpp_section[order_start:]
    # End the block at the next sibling key (by_standard:)
    end_match = _re.search(r"\n\s{0,8}[a-z_]+:", order_block[1:])
    if end_match:
        order_block = order_block[: end_match.start() + 1]

    # *.props must appear in the detection_order (vcxproj step)
    assert "*.props" in order_block, (
        "detection_order must reference '*.props' to match guidance.md step 3 "
        "('*.vcxproj / *.props → <LanguageStandard>'). "
        "Without this, .NET SDK-style C++ projects are not detected."
    )
    # .dsw must appear in the detection_order (legacy step)
    assert ".dsw" in order_block, (
        "detection_order must reference '.dsw' to match guidance.md step 5 "
        "('.dsp / .dsw present → legacy'). "
        "Without this, MSVC 6.0 workspace files are not classified as legacy."
    )


# --- ENG-2.1 guidance.md -------------------------------------------------------

def test_guidance_non_negotiable_laws_eng21_not_version_specific():
    """ENG-2.1 Non-Negotiable Laws entry must not gate domain modeling on C++20.

    The entry previously read 'Domain modeling — aggregates, value objects, C++20 concepts'.
    Domain modeling (aggregates, value objects) applies to all C++ versions.
    C++20 concepts are ONE implementation mechanism — brownfield/transitional teams
    cannot use them and would incorrectly believe domain modeling requires C++20.
    """
    content = _CPP_GUIDANCE.read_text(encoding="utf-8")
    assert "ENG-2.1" in content, "ENG-2.1 must appear in guidance.md Non-Negotiable Laws"
    # Find the ENG-2.1 row in the Non-Negotiable Laws table
    m = _re.search(r"\|\s*ENG-2\.1\s*\|([^\n]+)\|", content)
    assert m, "Could not find ENG-2.1 row in Non-Negotiable Laws table"
    eng21_specialization = m.group(1).strip()
    assert "C++20" not in eng21_specialization, (
        "ENG-2.1 Non-Negotiable Laws specialization must not reference 'C++20'. "
        "Domain modeling applies to all C++ tiers; mentioning C++20 misleads brownfield "
        "and transitional teams into thinking domain modeling requires C++20. "
        f"Current text: {eng21_specialization!r}. "
        "Fix: change to 'Domain modeling — aggregates, value objects' (version-agnostic)."
    )


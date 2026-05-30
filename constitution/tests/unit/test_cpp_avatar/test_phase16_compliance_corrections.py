"""Phase 16 Amendment O: Governance violation correction tests.

Laws: ENG-4.1, ENG-11.1, ENG-11.2
Refs: hangar-ai-specs/changes/c-plus-plus-avatar-enrichment/PROPOSAL.md — Amendment O
"""
from pathlib import Path
import yaml
import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
CPP_DIR = REPO_ROOT / "avatars" / "technology" / "cpp"
EXAMPLES_DIR = CPP_DIR / "examples"
AVATAR_DIR = CPP_DIR  # alias

# --- V1/V2: Domain boundary contract ---

def test_technology_avatar_examples_only_contain_eng_laws():
    """Safeguard 2 (Avatar Workflow): tech avatars may only specialize ENG-* laws.
    This contract test permanently enforces the rule — not just the specific files deleted."""
    violations = [f.name for f in EXAMPLES_DIR.glob("*.md")
                  if not f.name.startswith("ENG-")]
    assert violations == [], (
        f"Technology avatar examples must only reference ENG-* laws. "
        f"Domain boundary violations found: {violations}"
    )

# --- V3: governance_overrides — must be proposal-backed ---

def test_manifest_governance_overrides_are_proposal_backed():
    """V3: If governance_overrides exists in manifest.yaml, it must reference a
    formal ENG-11.1 proposal via 'proposal_ref'. Self-approved overrides without
    a proposal_ref violate ENG-11.1."""
    manifest = yaml.safe_load((CPP_DIR / "manifest.yaml").read_text(encoding="utf-8"))
    overrides = manifest.get("governance_overrides")
    if overrides is None:
        return  # no overrides — compliant
    assert "proposal_ref" in overrides, (
        "manifest.yaml governance_overrides must include 'proposal_ref' pointing to "
        "the formal ENG-11.1 proposal that authorized the override"
    )
    proposal_path = Path(__file__).parent.parent.parent.parent / overrides["proposal_ref"]
    assert proposal_path.exists(), (
        f"governance_overrides.proposal_ref '{overrides['proposal_ref']}' does not exist on disk"
    )

# --- V4: manifest scope creep blocks removed ---

def test_manifest_has_no_anti_patterns_block():
    """V4a: anti_patterns block must not be inline in manifest.yaml."""
    manifest = yaml.safe_load((CPP_DIR / "manifest.yaml").read_text(encoding="utf-8"))
    assert "anti_patterns" not in manifest, (
        "anti_patterns must not be inline in manifest.yaml (scope creep). "
        "Anti-pattern content belongs in example files."
    )

def test_manifest_has_no_anti_patterns_by_tier_block():
    """V4b: anti_patterns_by_tier must not be in manifest.yaml."""
    manifest = yaml.safe_load((CPP_DIR / "manifest.yaml").read_text(encoding="utf-8"))
    assert "anti_patterns_by_tier" not in manifest

def test_manifest_has_no_retrieval_triggers_block():
    """V4c: retrieval_triggers must not be inline in manifest.yaml."""
    manifest = yaml.safe_load((CPP_DIR / "manifest.yaml").read_text(encoding="utf-8"))
    assert "retrieval_triggers" not in manifest, (
        "retrieval_triggers must not be inline in manifest.yaml. "
        "Move to AVATAR-RAG-INDEX.yaml."
    )

# --- Parity: authorities block present ---

def test_manifest_has_authorities_block():
    """Authorities must exist in ref-infrastructure.md (routed from manifest per schema §3)."""
    full_ref = (CPP_DIR / "refs/testing/ref-infrastructure.md").read_text(encoding="utf-8")
    assert "Authorities and References" in full_ref, (
        "ref-infrastructure.md must contain an Authorities and References section "
        "citing canonical C++ references (routed from manifest per schema §3)"
    )

# --- V5: Skill law references ---

def test_skill_cpp_compliance_rating_has_no_bus_law_refs():
    """V5: platform-engineering skills must only reference ENG-* laws.
    Contract test — catches any BUS-* in law refs, not just the specific two removed."""
    import glob, re
    skill_files = list((REPO_ROOT / "agent-skills").rglob("skill-cpp-compliance-rating.md"))
    assert skill_files, "skill-cpp-compliance-rating.md not found in agent-skills/"
    content = skill_files[0].read_text(encoding="utf-8")
    # Find law references in the laws_cited / specializes_laws sections
    bus_refs = re.findall(r'\bBUS-\d+\.\d+\b', content)
    assert bus_refs == [], (
        f"Platform-engineering skills must only reference ENG-* laws. "
        f"Found BUS-* refs: {bus_refs}"
    )

# --- V6: Shadow governance document removed ---

def test_no_shadow_governance_docs_in_avatar_dir():
    """V6: Avatar directories must not contain embedded governance frameworks.
    Contract test — pattern match, not specific filename."""
    forbidden_patterns = ["*rating-system.md", "*compliance-rating*.md", "*governance-framework*.md"]
    found = []
    for pattern in forbidden_patterns:
        found.extend(f.name for f in CPP_DIR.glob(pattern))
    assert found == [], (
        f"Avatar directory must not contain shadow governance documents: {found}"
    )

# --- V7: guidance.md token budget ---

def test_guidance_md_within_token_budget():
    """V7: guidance.md must stay within 450-token RAG budget.
    Constitution spec: avatars/AVATAR-RAG-INDEX.yaml guidance_file: 200-450 tokens.
    Formula: word_count × 1.3 ≈ token estimate."""
    content = (CPP_DIR / "guidance.md").read_text(encoding="utf-8")
    word_count = len(content.split())
    estimated_tokens = int(word_count * 1.3)
    assert estimated_tokens <= 450, (
        f"guidance.md exceeds 450-token RAG budget: ~{estimated_tokens} tokens "
        f"({word_count} words). Rebuild to a slim index pointing to "
        f"avatars/technology/cpp/ref-infrastructure.md"
    )

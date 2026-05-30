"""Test 1.8: C++ avatar has baseline skill activation parity.

Scenario ID: c-plus-plus-avatar-enrichment/1.8
Law: ENG-11.1, ENG-10.1

Content routing: skill_parity documentation moved from manifest.yaml
to ref-infrastructure.md per avatar-model-schema §3 (forbidden block).
Skills remain in manifest activates.skills.
"""
import pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
FULL_REF = REPO / "avatars" / "technology" / "cpp" / "refs/testing/ref-infrastructure.md"

# Required baseline skills per proposal Phase 2e
REQUIRED_BASELINE_SKILLS = [
    "06-atomic-tdd",
    "07-vertical-slice-dev",
    "08-code-review",
    "04-business-domain-modeling",
]


def test_cpp_manifest_has_baseline_skill_activation_parity(manifest_data):
    """activates.skills must include all 4 baseline parity skills and document parity metadata."""
    manifest = manifest_data

    activates = manifest.get("activates", {})
    skills = activates.get("skills", [])

    # Extract skill IDs (support both plain strings and dicts with 'id' key)
    skill_ids = []
    for s in skills:
        if isinstance(s, str):
            skill_ids.append(s)
        elif isinstance(s, dict) and "id" in s:
            skill_ids.append(s["id"])

    for required in REQUIRED_BASELINE_SKILLS:
        assert required in skill_ids, (
            f"activates.skills must include baseline parity skill: {required}"
        )

    # Parity documentation must exist in ref-infrastructure.md
    full_ref_text = FULL_REF.read_text(encoding="utf-8")
    assert "Skill Parity" in full_ref_text, (
        "ref-infrastructure.md must have a Skill Parity section documenting baseline parity rationale"
    )
    assert "04-business-domain-modeling" in full_ref_text, (
        "Skill Parity section must document the Q9 exception for skill-04"
    )

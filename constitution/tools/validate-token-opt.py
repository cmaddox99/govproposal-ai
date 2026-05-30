#!/usr/bin/env python3
"""Token Optimization validation — Skill & Law Token Optimization.

58 checks across 5 groups:
  Group A — Companion *-examples.md files exist for all 11 in-scope skills
  Group B — Skill bodies retain required governance sections (structural preservation)
  Group C — Token reduction targets met (≥30% per skill, ≤2,000 tokens per body)
  Group D — Law file token targets met (governance.md ≤1,000; spec-driven ≤600)
  Group E — Cross-references and bidirectional links intact
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILLS_BASE = ROOT / "agent-skills/skills-by-domain"

# 11 in-scope skills: (relative path in skills-by-domain, skill-id, baseline_tokens)
SKILLS = [
    ("development-practices/06-atomic-tdd.md",             "skill-06-atomic-tdd",              4881),
    ("development-practices/04-business-domain-modeling.md","skill-04-business-domain-modeling", 4428),
    ("platform-engineering/10-security-review.md",          "skill-10-security-review",          3884),
    ("platform-engineering/14-technical-debt.md",           "skill-14-technical-debt",           3884),
    ("development-practices/09-refactoring.md",             "skill-09-refactoring",              3877),
    ("discovery-research/02-user-journey-mapping.md",       "skill-02-user-journey-mapping",     3552),
    ("product-planning/03-executable-spec.md",              "skill-03-executable-spec",          3517),
    ("development-practices/07-vertical-slice-dev.md",      "skill-07-vertical-slice-dev",       3330),
    ("platform-engineering/12-api-design.md",               "skill-12-api-design",               3221),
    ("product-planning/01-roadmapping.md",                  "skill-01-roadmapping",              3115),
    ("development-practices/08-code-review.md",             "skill-08-code-review",              3777),
]

REQUIRED_IN_SKILL_BODY = [
    "## Constitutional Foundation",
    "## Quality Checklist",
    "## When to Invoke",
]

GOVERNANCE_MD = ROOT / "laws/engineering/governance.md"
SPEC_DRIVEN_MD = ROOT / "laws/engineering/spec-driven-development.md"
OBSERVABILITY_GUIDE = ROOT / "docs/guides/constitution/constitution-observability.md"

passes = 0
failures = []

def check(cond, label, detail=""):
    global passes
    if cond:
        passes += 1
        print(f"  ✅ {label}")
    else:
        failures.append(label)
        print(f"  ❌ FAIL: {label}" + (f"\n       {detail}" if detail else ""))

def tokens(path):
    return len(path.read_text()) // 4 if path.exists() else 0

def has(path, *patterns):
    if not path.exists():
        return False
    t = path.read_text()
    return all(p in t for p in patterns)

print("Token Optimization Validation")
print("=" * 55)

# ── Group A: Companion files exist ────────────────────────────────────────────
print("\nGroup A — Companion *-examples.md files exist")
for rel, skill_id, _ in SKILLS:
    skill_path = SKILLS_BASE / rel
    examples_path = skill_path.parent / (skill_path.stem + "-examples.md")
    check(examples_path.exists(), f"{skill_path.stem}-examples.md exists",
          f"Expected: {examples_path.relative_to(ROOT)}")

# ── Group B: Structural preservation in skill bodies ─────────────────────────
print("\nGroup B — Required governance sections preserved in skill bodies")
for rel, skill_id, _ in SKILLS:
    skill_path = SKILLS_BASE / rel
    if not skill_path.exists():
        check(False, f"{skill_path.stem}: file exists", "skill file missing")
        continue
    for section in REQUIRED_IN_SKILL_BODY:
        check(has(skill_path, section), f"{skill_path.stem} has '{section}'",
              f"Section missing from skill body — must NOT be in companion file")

# ── Group C: Token reduction targets ─────────────────────────────────────────
print("\nGroup C — Token reduction ≥30% and body ≤2,000 tokens per skill")
for rel, skill_id, baseline in SKILLS:
    skill_path = SKILLS_BASE / rel
    if not skill_path.exists():
        check(False, f"{skill_path.stem}: ≥30% reduction", "file missing")
        check(False, f"{skill_path.stem}: body ≤2,000 tokens", "file missing")
        continue
    current = tokens(skill_path)
    reduction_pct = round((baseline - current) / baseline * 100, 1)
    check(reduction_pct >= 30,
          f"{skill_path.stem}: ≥30% reduction ({reduction_pct}% actual, {baseline}→{current} tokens)",
          f"Only {reduction_pct}% reduction — need ≥30%")
    check(current <= 2000,
          f"{skill_path.stem}: body ≤2,000 tokens ({current} actual)",
          f"{current} tokens — need ≤2,000")

# ── Group D: Law file token targets ───────────────────────────────────────────
print("\nGroup D — Law file token targets")
gov_tokens = tokens(GOVERNANCE_MD)
check(GOVERNANCE_MD.exists(), "governance.md exists")
check(gov_tokens <= 1000, f"governance.md ≤1,000 tokens ({gov_tokens} actual)",
      f"{gov_tokens} tokens — need ≤1,000")
check(has(GOVERNANCE_MD, "ENG-10.1"), "governance.md retains ENG-10.1 law body")
check(has(GOVERNANCE_MD, "ENG-10.2"), "governance.md retains ENG-10.2 law body")
check(has(GOVERNANCE_MD, "ENG-10.3"), "governance.md retains ENG-10.3 law body")
check(has(GOVERNANCE_MD, "SHALL") or has(GOVERNANCE_MD, "MUST"),
      "governance.md retains SHALL/MUST clauses")
check(OBSERVABILITY_GUIDE.exists(), "constitution-observability.md guide exists")

spec_tokens = tokens(SPEC_DRIVEN_MD)
check(SPEC_DRIVEN_MD.exists(), "spec-driven-development.md exists")
check(spec_tokens <= 600, f"spec-driven-development.md ≤600 tokens ({spec_tokens} actual)",
      f"{spec_tokens} tokens — need ≤600")
check(has(SPEC_DRIVEN_MD, "ENG-11") or has(SPEC_DRIVEN_MD, "11."),
      "spec-driven-development.md retains ENG-11.x citations")
check(has(SPEC_DRIVEN_MD, "SHALL") or has(SPEC_DRIVEN_MD, "MUST"),
      "spec-driven-development.md retains SHALL/MUST clauses")

# ── Group E: Cross-references intact ──────────────────────────────────────────
print("\nGroup E — Cross-references and bidirectional links")
for rel, skill_id, _ in SKILLS:
    skill_path = SKILLS_BASE / rel
    if not skill_path.exists():
        continue
    # Skill body should reference its companion
    check(has(skill_path, "-examples.md"),
          f"{skill_path.stem} body references companion examples file")

# Companion files should back-reference parent
for rel, skill_id, _ in SKILLS:
    skill_path = SKILLS_BASE / rel
    examples_path = skill_path.parent / (skill_path.stem + "-examples.md")
    if examples_path.exists():
        check(has(examples_path, skill_id) or has(examples_path, skill_path.stem),
              f"{examples_path.stem} back-references parent skill",
              f"Companion must reference '{skill_id}' or '{skill_path.stem}'")

# governance.md → observability guide cross-ref
check(has(GOVERNANCE_MD, "constitution-observability"),
      "governance.md cross-references constitution-observability.md guide")
# observability guide → governance.md cross-ref
check(has(OBSERVABILITY_GUIDE, "governance.md") or has(OBSERVABILITY_GUIDE, "ENG-10"),
      "constitution-observability.md cross-references governance.md / ENG-10.x laws")

# ── Summary ───────────────────────────────────────────────────────────────────
total = passes + len(failures)
print(f"\nToken Optimization Validation — {passes}/{total} checks passed")
print("=" * 55)
if failures:
    print(f"\n{len(failures)} check(s) failed — implementation incomplete")
    sys.exit(1)
else:
    print("\nAll checks passed — token optimization complete ✅")
    sys.exit(0)

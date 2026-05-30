#!/usr/bin/env python3
"""Phase 9 validation — SonarQube Compliance Radiator Integration.

55 checks across 5 groups:
  Group A — Law mapping guide exists and has required structure
  Group B — skill-sonarqube-compliance-gate structure and content
  Group C — Workflow SonarQube gates present
  Group D — Evidence artifact templates exist
  Group E — Token security (SONARQUBE_TOKEN never a literal value in any file)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

LAW_MAPPING  = ROOT / "docs/guides/constitution/sonarqube-law-mapping.md"
SKILL        = ROOT / "agent-skills/skills-by-domain/platform-engineering/skill-sonarqube-compliance-gate.md"
REFACTOR_WF  = ROOT / "workflows/legacy-rescue-refactor.md"
REWRITE_WF   = ROOT / "workflows/legacy-rescue-rewrite.md"
DECISION_WF  = ROOT / "workflows/legacy-rescue-decision-track.md"
GREENFIELD_WF= ROOT / "workflows/greenfield-development.md"
BASELINE_TPL = ROOT / "docs/templates/sonarqube-baseline.md"
GATE_TPL     = ROOT / "docs/templates/sonarqube-gate.md"
DELTA_TPL    = ROOT / "docs/templates/sonarqube-delta.md"

passes = 0
failures = []

def check(condition, label, detail=""):
    global passes
    if condition:
        passes += 1
        print(f"  ✅ {label}")
    else:
        failures.append(label)
        print(f"  ❌ FAIL: {label}" + (f"\n       {detail}" if detail else ""))

def file_contains(path, *patterns):
    if not path.exists():
        return False
    content = path.read_text()
    return all(p in content for p in patterns)

print("Phase 9 Validation")
print("=" * 50)

# ── Group A: Law mapping guide ────────────────────────────────────────────────
print("\nGroup A — sonarqube-law-mapping.md exists and has required structure")
check(LAW_MAPPING.exists(), "sonarqube-law-mapping.md exists")
check(file_contains(LAW_MAPPING, "ENG-6.1"), "law mapping cites ENG-6.1 (NON-NEGOTIABLE)")
check(file_contains(LAW_MAPPING, "ENG-6.4"), "law mapping cites ENG-6.4 (NON-NEGOTIABLE)")
check(file_contains(LAW_MAPPING, "ENG-6.7"), "law mapping cites ENG-6.7 (NON-NEGOTIABLE)")
check(file_contains(LAW_MAPPING, "ENG-3.1"), "law mapping cites ENG-3.1 (complexity)")
check(file_contains(LAW_MAPPING, "ENG-4.6"), "law mapping cites ENG-4.6 (coverage)")
check(file_contains(LAW_MAPPING, "BUS-7.1"), "law mapping cites BUS-7.1 (compliance evidence)")
check(file_contains(LAW_MAPPING, "HARD_BLOCK"), "law mapping defines HARD_BLOCK classification")
check(file_contains(LAW_MAPPING, "PHASE_GATE"), "law mapping defines PHASE_GATE classification")
check(file_contains(LAW_MAPPING, "SONARQUBE_TOKEN"), "law mapping references SONARQUBE_TOKEN env var")
check(file_contains(LAW_MAPPING, "vulnerabilities"), "law mapping references vulnerabilities metric")
check(file_contains(LAW_MAPPING, "coverage"), "law mapping references coverage metric")

# ── Group B: Skill structure ──────────────────────────────────────────────────
print("\nGroup B — skill-sonarqube-compliance-gate structure")
check(SKILL.exists(), "skill-sonarqube-compliance-gate.md exists")
check(file_contains(SKILL, "ENG-6.1"), "skill cites ENG-6.1")
check(file_contains(SKILL, "ENG-6.7"), "skill cites ENG-6.7")
check(file_contains(SKILL, "BUS-7.1"), "skill cites BUS-7.1")
check(file_contains(SKILL, "HARD_BLOCK"), "skill defines HARD_BLOCK gates")
check(file_contains(SKILL, "SONARQUBE_TOKEN"), "skill references SONARQUBE_TOKEN (env var only)")
check(file_contains(SKILL, "SONARQUBE_URL"), "skill references SONARQUBE_URL (env var only)")
check(file_contains(SKILL, "/api/measures/component"), "skill includes SonarQube API endpoint")
check(file_contains(SKILL, "legacy-rescue-refactor"), "skill has workflow cross-reference")
check(file_contains(SKILL, "skill-09-refactoring"), "skill has followed_by: skill-09-refactoring")
check(file_contains(SKILL, "skill-10-security-review"), "skill has followed_by: skill-10-security-review")

# ── Group C: Workflow SonarQube gates ─────────────────────────────────────────
print("\nGroup C — Workflow SonarQube gates present")

# legacy-rescue-refactor: phases 1,3,4,5,6
check(file_contains(REFACTOR_WF, "SonarQube", "Phase 1"), "legacy-rescue-refactor Phase 1 has SonarQube gate",
      "Missing SonarQube reference near Phase 1")
check(file_contains(REFACTOR_WF, "SonarQube", "Phase 4"), "legacy-rescue-refactor Phase 4 has SonarQube gate")
check(file_contains(REFACTOR_WF, "SonarQube", "Phase 6"), "legacy-rescue-refactor Phase 6 has SonarQube gate")
check(file_contains(REFACTOR_WF, "skill-sonarqube-compliance-gate"), "legacy-rescue-refactor frontmatter includes skill")

# legacy-rescue-rewrite: phases 1,4,5,6
check(file_contains(REWRITE_WF, "SonarQube", "Phase 1"), "legacy-rescue-rewrite Phase 1 has SonarQube gate")
check(file_contains(REWRITE_WF, "SonarQube", "Phase 4"), "legacy-rescue-rewrite Phase 4 has SonarQube gate")
check(file_contains(REWRITE_WF, "SonarQube", "Phase 6"), "legacy-rescue-rewrite Phase 6 has SonarQube gate")
check(file_contains(REWRITE_WF, "skill-sonarqube-compliance-gate"), "legacy-rescue-rewrite frontmatter includes skill")

# legacy-rescue-decision-track: phases 1,3,6
check(file_contains(DECISION_WF, "SonarQube", "Phase 1"), "legacy-rescue-decision-track Phase 1 has SonarQube gate")
check(file_contains(DECISION_WF, "SonarQube", "Phase 3"), "legacy-rescue-decision-track Phase 3 has SonarQube gate")
check(file_contains(DECISION_WF, "SonarQube", "Phase 6"), "legacy-rescue-decision-track Phase 6 has SonarQube gate")
check(file_contains(DECISION_WF, "skill-sonarqube-compliance-gate"), "legacy-rescue-decision-track frontmatter includes skill")

# greenfield-development: phases 6,7,8
check(file_contains(GREENFIELD_WF, "SonarQube", "Phase 6"), "greenfield-development Phase 6 has SonarQube gate")
check(file_contains(GREENFIELD_WF, "SonarQube", "Phase 7"), "greenfield-development Phase 7 has SonarQube gate")
check(file_contains(GREENFIELD_WF, "SonarQube", "Phase 8"), "greenfield-development Phase 8 has SonarQube gate")
check(file_contains(GREENFIELD_WF, "skill-sonarqube-compliance-gate"), "greenfield-development frontmatter includes skill")

# ── Group D: Evidence artifact templates ─────────────────────────────────────
print("\nGroup D — Evidence artifact templates exist and have required structure")
check(BASELINE_TPL.exists(), "docs/templates/sonarqube-baseline.md exists")
check(file_contains(BASELINE_TPL, "SONARQUBE_URL"), "baseline template references project URL")
check(file_contains(BASELINE_TPL, "vulnerabilities"), "baseline template includes vulnerabilities")
check(file_contains(BASELINE_TPL, "coverage"), "baseline template includes coverage")

check(GATE_TPL.exists(), "docs/templates/sonarqube-gate.md exists")
check(file_contains(GATE_TPL, "HARD_BLOCK"), "gate template includes HARD_BLOCK verdict")
check(file_contains(GATE_TPL, "PHASE_GATE"), "gate template includes PHASE_GATE verdict")

check(DELTA_TPL.exists(), "docs/templates/sonarqube-delta.md exists")
check(file_contains(DELTA_TPL, "Before"), "delta template has Before column")
check(file_contains(DELTA_TPL, "After"), "delta template has After column")
check(file_contains(DELTA_TPL, "Delta"), "delta template has Delta column")

# ── Group E: Token security ───────────────────────────────────────────────────
print("\nGroup E — SONARQUBE_TOKEN never committed as literal value")
LITERAL_TOKEN_PATTERN = re.compile(r'SONARQUBE_TOKEN\s*=\s*["\']?[a-zA-Z0-9_\-]{8,}')
committed_violations = []
for f in ROOT.rglob("*"):
    if f.is_file() and f.suffix in (".md", ".yaml", ".yml", ".sh", ".py", ".json") and ".git" not in str(f):
        try:
            content = f.read_text(errors="replace")
            if LITERAL_TOKEN_PATTERN.search(content):
                committed_violations.append(str(f.relative_to(ROOT)))
        except Exception:
            pass
check(len(committed_violations) == 0, "SONARQUBE_TOKEN never assigned a literal value in any file",
      f"Found in: {committed_violations}" if committed_violations else "")

# skill must use $SONARQUBE_TOKEN syntax (env var reference), not a literal
check(file_contains(SKILL, "$SONARQUBE_TOKEN") or file_contains(SKILL, "${SONARQUBE_TOKEN}"),
      "skill uses $SONARQUBE_TOKEN env var syntax (not hardcoded)")

# ── Summary ───────────────────────────────────────────────────────────────────
total = passes + len(failures)
print(f"\nPhase 9 Validation — {passes}/{total} checks passed")
print("=" * 50)
if failures:
    print(f"\n{len(failures)} check(s) failed — implementation incomplete")
    sys.exit(1)
else:
    print("\nAll checks passed — Phase 9 complete ✅")
    sys.exit(0)

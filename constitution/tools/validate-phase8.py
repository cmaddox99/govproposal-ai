#!/usr/bin/env python3
"""Phase 8 validation — Business Avatar Enrichment & Manifest Creation.

29 checks across 4 groups:
  Group A — All 14 product-type manifests exist
  Group B — All 14 cite ≥1 BUS or compliance law
  Group C — All 14 activate ≥1 legacy rescue workflow
  Group D — Schema fields present (activates/specializes_laws/dependencies)
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
AVATARS = ROOT / "avatars" / "product-type"

PRODUCT_AVATARS = [
    "cargo-freight",
    "check-in-travel",
    "crew-training-scheduling",
    "customer-relations-ops",
    "customer-service",
    "airport-operations",
    "ground-ops-staffing-analytics",
    "internal-productivity",
    "loyalty-aadvantage",
    "marketing-personalization",
    "network-planning-optimization",
    "passenger-booking",
    "schedule-change-self-serve",
    "travel-docs-compliance",
]

LEGACY_RESCUE_WORKFLOWS = [
    "legacy-rescue-decision-track",
    "legacy-rescue-refactor",
    "legacy-rescue-rewrite",
]

COMPLIANCE_LAWS = [
    "BUS-2.1", "BUS-2.2", "BUS-2.3", "BUS-2.4",
    "BUS-4.1", "BUS-4.2", "BUS-4.3",
    "ENG-6.1", "ENG-6.4", "ENG-6.7",
]

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

print(f"Phase 8 Validation")
print("=" * 50)

# ── Group A: manifest.yaml exists for all 14 ──────────────────────────────────
print("\nGroup A — Manifest files exist (14/14)")
for avatar in PRODUCT_AVATARS:
    manifest = AVATARS / avatar / "manifest.yaml"
    check(manifest.exists(), f"{avatar}/manifest.yaml exists",
          f"Expected: {manifest}")

# ── Group B: ≥1 compliance/BUS law cited ─────────────────────────────────────
print("\nGroup B — Each manifest cites ≥1 compliance/BUS law")
for avatar in PRODUCT_AVATARS:
    manifest = AVATARS / avatar / "manifest.yaml"
    if not manifest.exists():
        check(False, f"{avatar} cites ≥1 compliance law", "manifest missing")
        continue
    content = manifest.read_text()
    has_law = any(law in content for law in COMPLIANCE_LAWS)
    cited = [l for l in COMPLIANCE_LAWS if l in content]
    check(has_law, f"{avatar} cites ≥1 compliance law",
          f"None of {COMPLIANCE_LAWS[:4]}... found" if not has_law else f"Found: {cited[:3]}")

# ── Group C: activates ≥1 legacy rescue workflow ─────────────────────────────
print("\nGroup C — Each manifest activates ≥1 legacy rescue workflow")
for avatar in PRODUCT_AVATARS:
    manifest = AVATARS / avatar / "manifest.yaml"
    if not manifest.exists():
        check(False, f"{avatar} activates ≥1 legacy rescue workflow", "manifest missing")
        continue
    content = manifest.read_text()
    has_rescue = any(wf in content for wf in LEGACY_RESCUE_WORKFLOWS)
    check(has_rescue, f"{avatar} activates ≥1 legacy rescue workflow",
          f"None of {LEGACY_RESCUE_WORKFLOWS} found")

# ── Group D: schema fields present ───────────────────────────────────────────
print("\nGroup D — Schema fields present (activates/specializes_laws/dependencies)")
REQUIRED_FIELDS = ["activates:", "specializes_laws:", "dependencies:"]
for avatar in PRODUCT_AVATARS:
    manifest = AVATARS / avatar / "manifest.yaml"
    if not manifest.exists():
        # one failure covers the missing manifest; skip field checks
        continue
    content = manifest.read_text()
    for field in REQUIRED_FIELDS:
        check(field in content, f"{avatar} has '{field}'",
              f"Field '{field}' missing from manifest")

# ── Summary ───────────────────────────────────────────────────────────────────
total = passes + len(failures)
print(f"\nPhase 8 Validation — {passes}/{total} checks passed")
print("=" * 50)
if failures:
    print(f"\n{len(failures)} check(s) failed — implementation incomplete")
    sys.exit(1)
else:
    print("\nAll checks passed — Phase 8 complete ✅")
    sys.exit(0)

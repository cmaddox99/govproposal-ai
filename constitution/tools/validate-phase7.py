#!/usr/bin/env python3
"""Phase 7 validation script — fails before implementation, passes after.
Tests:
  1. Zero stale workflow IDs in avatars/
  2. All 5 new workflow IDs exist in workflows/
  3. skill-27 references all 3 legacy rescue workflows
  4. All 3 legacy rescue workflows include skill-27 in skills list
  5. BUS-2.1/2.2/2.4 in refactor + rewrite + decision-track workflow laws
  6. avatar_context includes business+product in refactor + rewrite workflows
  7. aviation-faa/manifest.yaml exists
"""
import sys, glob, re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
failures = []
passes = []

def check(name, condition, detail=""):
    if condition:
        passes.append(name)
    else:
        failures.append(f"FAIL: {name}" + (f"\n       {detail}" if detail else ""))

# 1. Zero stale workflow IDs in avatars/
stale_ids = ['workflow-discovery-to-delivery','workflow-sdd-lifecycle',
             'workflow-brownfield-adoption','workflow-ux-to-implementation']
avatar_files = sorted(glob.glob(f'{BASE}/avatars/**/*.yaml', recursive=True) +
                      glob.glob(f'{BASE}/avatars/**/*.md', recursive=True))
avatar_files = [f for f in avatar_files if 'index' not in f and 'RAG-INDEX' not in f]

for stale in stale_ids:
    hits = [f.replace(BASE+'/','') for f in avatar_files if stale in open(f).read()]
    check(f"No stale '{stale}' in avatars/", len(hits) == 0,
          f"Found in: {hits[:3]}{'...' if len(hits)>3 else ''}")

# 2. All 5 new workflow IDs exist in workflows/
new_ids = ['product-discovery-stage-a-f','greenfield-development',
           'legacy-rescue-decision-track','legacy-rescue-refactor','legacy-rescue-rewrite']
wf_files = glob.glob(f'{BASE}/workflows/*.md')
wf_names = [os.path.basename(f).replace('.md','') for f in wf_files]
for wf_id in new_ids:
    check(f"Workflow '{wf_id}' exists", wf_id in wf_names)

# 3. skill-27 references all 3 legacy rescue workflows in body
skill27 = open(f'{BASE}/agent-skills/skills-by-domain/platform-engineering/27-constitution-compliance.md').read()
for wf in ['legacy-rescue-refactor','legacy-rescue-rewrite','legacy-rescue-decision-track']:
    check(f"skill-27 references '{wf}'", wf in skill27)

# 4. All 3 legacy rescue workflows include skill-27 in skills: list
for wf in ['legacy-rescue-refactor','legacy-rescue-rewrite','legacy-rescue-decision-track']:
    content = open(f'{BASE}/workflows/{wf}.md').read()
    check(f"'{wf}' skills: includes skill-27-constitution-compliance",
          'skill-27-constitution-compliance' in content)

# 5. BUS laws in legacy rescue workflows
bus_laws = ['BUS-2.1','BUS-2.2','BUS-2.4']
for wf in ['legacy-rescue-refactor','legacy-rescue-rewrite','legacy-rescue-decision-track']:
    content = open(f'{BASE}/workflows/{wf}.md').read()
    for law in bus_laws:
        check(f"'{wf}' cites {law}", law in content)

# 6. avatar_context in refactor + rewrite includes business + product
for wf in ['legacy-rescue-refactor','legacy-rescue-rewrite']:
    content = open(f'{BASE}/workflows/{wf}.md').read()
    ctx_match = re.search(r'avatar_context:\s*\[([^\]]+)\]', content)
    ctx = ctx_match.group(1) if ctx_match else ''
    check(f"'{wf}' avatar_context includes 'business'", 'business' in ctx)
    check(f"'{wf}' avatar_context includes 'product'", 'product' in ctx)

# 7. aviation-faa manifest exists
check("aviation-faa/manifest.yaml exists",
      os.path.exists(f'{BASE}/avatars/industry/aviation-faa/manifest.yaml'))

# Report
total = len(passes) + len(failures)
print(f"\nPhase 7 Validation — {len(passes)}/{total} checks passed\n{'='*50}")
for p in passes:
    print(f"  ✅ {p}")
for f in failures:
    print(f"  ❌ {f}")

if failures:
    print(f"\n{len(failures)} check(s) failed — implementation incomplete")
    sys.exit(1)
else:
    print("\nAll checks passed — Phase 7 complete ✅")
    sys.exit(0)

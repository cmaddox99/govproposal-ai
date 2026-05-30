#!/usr/bin/env bash
# Regenerate the golden HTML fixtures used by tests/test_determinism.py.
#
# Run this AFTER an intentional template/renderer change. Commit the updated
# golden-*.html files alongside the change. The determinism test then guards
# that no later change accidentally drifts the rendered output.
#
# If the determinism test fails on someone else's PR, they should:
#   1. Investigate why the bytes changed (intentional vs accidental).
#   2. If intentional: run this script and commit.
#   3. If accidental: revert.
#
# Spec: hangar-ai-specs/changes/renderer-determinism-and-diagnose/PROPOSAL.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FIXTURES="$SCRIPT_DIR/tests/fixtures"
LAWS="$REPO_ROOT/laws"

echo "Regenerating golden HTML fixtures from $FIXTURES"
echo "Using laws-dir: $LAWS"

aa-artifact-render "$FIXTURES/golden-discovery-stage-a.md" \
  --output "$FIXTURES/golden-discovery-stage-a.html" \
  --laws-dir "$LAWS" \
  --quiet

aa-artifact-render "$FIXTURES/golden-proposal.md" \
  --output "$FIXTURES/golden-proposal.html" \
  --laws-dir "$LAWS" \
  --quiet

aa-artifact-render "$FIXTURES/golden-discovery-stage-d.md" \
  --output "$FIXTURES/golden-discovery-stage-d.html" \
  --laws-dir "$LAWS" \
  --quiet

aa-artifact-render "$FIXTURES/golden-discovery-stage-e.md" \
  --output "$FIXTURES/golden-discovery-stage-e.html" \
  --laws-dir "$LAWS" \
  --quiet

aa-artifact-render "$FIXTURES/golden-discovery-stage-f.md" \
  --output "$FIXTURES/golden-discovery-stage-f.html" \
  --laws-dir "$LAWS" \
  --quiet

echo "✓ Regenerated:"
echo "  $FIXTURES/golden-discovery-stage-a.html"
echo "  $FIXTURES/golden-proposal.html"
echo "  $FIXTURES/golden-discovery-stage-d.html"
echo "  $FIXTURES/golden-discovery-stage-e.html"
echo "  $FIXTURES/golden-discovery-stage-f.html"
echo ""
echo "Commit these alongside your template/renderer changes."

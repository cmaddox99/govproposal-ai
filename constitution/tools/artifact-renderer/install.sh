#!/usr/bin/env bash
# aa-artifact-render — install from source in the hangar-ai-constitution repo.
#
# ENG-13.1 NON-NEGOTIABLE: artifacts must be rendered by the current toolchain.
# Run this whenever the constitution repo has pulled new commits that touch
# tools/artifact-renderer/ — a stale install renders artifacts with an outdated
# template or missing artifact types, silently violating ENG-13.1.
#
# Usage (from anywhere):
#   ./install.sh
#
# After install, verify:
#   aa-artifact-render --help
#   # success line of any render should now show: aa-artifact-render v<VERSION>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Installing aa-artifact-render (editable) from $SCRIPT_DIR"
pip install -e "$SCRIPT_DIR" 1>/dev/null

echo "✓ aa-artifact-render installed from $REPO_ROOT/tools/artifact-renderer"
aa-artifact-render --help | head -1

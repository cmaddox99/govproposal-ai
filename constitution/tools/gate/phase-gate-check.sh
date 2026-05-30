#!/usr/bin/env bash
# phase-gate-check.sh — Human Gate Enforcement (ENG-12.1 NON-NEGOTIABLE)
# Spec: workflow-human-gate-enforcement
#
# Usage: phase-gate-check.sh <phase> <spec-id> [spec-root]
#   phase     — phase number to check (e.g. 2 means "check gate for entering phase 2")
#   spec-id   — spec folder name under hangar-ai-specs/changes/ (e.g. my-spec-2026-001)
#   spec-root — optional: root of repo (defaults to the repo root containing this script)
#
# Approval file location:
#   <spec-root>/hangar-ai-specs/changes/<spec-id>/.phase-<phase>.approved
#
# Exit codes:
#   0 — gate is OPEN (approval file found); agent may proceed
#   1 — gate is LOCKED (no approval file); agent must stop

set -euo pipefail

PHASE="${1:-}"
SPEC_ID="${2:-}"
REPO_ROOT="${3:-$(cd "$(dirname "$0")/../.." && pwd)}"

if [ -z "$PHASE" ] || [ -z "$SPEC_ID" ]; then
  echo "⛔ ENG-12.1 VIOLATION — missing arguments"
  echo "   Usage: phase-gate-check.sh <phase> <spec-id> [repo-root]"
  echo "   The agent cannot proceed without a valid phase and spec-id."
  exit 1
fi

APPROVAL_FILE="$REPO_ROOT/hangar-ai-specs/changes/$SPEC_ID/.phase-${PHASE}.approved"

if [ ! -f "$APPROVAL_FILE" ]; then
  echo ""
  echo "⛔ ══════════════════════════════════════════════════════════"
  echo "   HUMAN GATE LOCKED — ENG-12.1 (NON-NEGOTIABLE)"
  echo "══════════════════════════════════════════════════════════════"
  echo ""
  echo "   Phase $PHASE gate is NOT approved for spec: $SPEC_ID"
  echo ""
  echo "   A human must review the Phase $((PHASE - 1)) artifacts and create:"
  echo "   $APPROVAL_FILE"
  echo ""
  echo "   The agent CANNOT advance to Phase $PHASE without this file."
  echo "   API pass ≠ gate pass. The human review IS the checkpoint."
  echo ""
  echo "   To approve (run as human, not agent):"
  echo "   echo 'Approved by <name> on \$(date)' > $APPROVAL_FILE"
  echo ""
  exit 1
fi

echo "✅ Gate OPEN — Phase $PHASE approved for spec: $SPEC_ID"
echo "   Approval: $(cat "$APPROVAL_FILE")"
exit 0

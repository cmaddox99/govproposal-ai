#!/usr/bin/env bash
# render-package.sh — Render discovery stage evidence artifacts via aa-artifact-render
# Governed by: ENG-13.1 (NON-NEGOTIABLE), BUS-7.1
#
# Usage:
#   render-package.sh <discovery-id> [stage]
#
# Examples:
#   render-package.sh disc-2026-003          # Render all existing evidence artifacts
#   render-package.sh disc-2026-003 a        # Render Stage A only (stage-a-initialize.md)
#   render-package.sh disc-2026-003 b        # Render Stage B only
#
# Requires: aa-artifact-render on PATH

set -euo pipefail

DISCOVERY_ID="${1:?Usage: render-package.sh <discovery-id> [stage]}"
STAGE="${2:-all}"
SPEC_DIR="hangar-ai-specs/changes/${DISCOVERY_ID}"
LAWS_DIR="laws"

if [ ! -d "${SPEC_DIR}" ]; then
  echo "ERROR: Discovery directory not found: ${SPEC_DIR}" >&2
  exit 1
fi

if ! command -v aa-artifact-render &>/dev/null; then
  echo "ERROR: aa-artifact-render not found on PATH. Install from tools/artifact-renderer/." >&2
  exit 1
fi

render_and_open() {
  local file="$1"
  local basename
  basename="$(basename "${file}")"

  if [ ! -f "${file}" ]; then
    echo "SKIP: ${basename} (not found)"
    return 0
  fi

  echo "Rendering: ${basename}..."
  aa-artifact-render "${file}" --laws-dir "${LAWS_DIR}"

  local html="${file%.md}.html"
  if [ -f "${html}" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
      open "${html}"
    else
      xdg-open "${html}" 2>/dev/null || echo "INFO: Open ${html} in your browser."
    fi
  fi
}

render_stage_a() { render_and_open "${SPEC_DIR}/stage-a-initialize.md"; }
render_stage_b() { render_and_open "${SPEC_DIR}/stage-b-field-study.md"; }
render_stage_c() { render_and_open "${SPEC_DIR}/stage-c-code-evidence.md"; }
render_stage_d() { render_and_open "${SPEC_DIR}/stage-d-validation.md"; }
render_stage_e() { render_and_open "${SPEC_DIR}/stage-e-metrics.md"; }
render_stage_f() {
  render_and_open "${SPEC_DIR}/stage-f-roadmap.md"
  local file="${SPEC_DIR}/stage-f-roadmap.md"
  if [ -f "${file}" ]; then
    echo "Generating PDF (ENG-13.3)..."
    aa-artifact-render "${file}" --laws-dir "${LAWS_DIR}" --pdf
  fi
}

case "${STAGE}" in
  a|A) render_stage_a ;;
  b|B) render_stage_b ;;
  c|C) render_stage_c ;;
  d|D) render_stage_d ;;
  e|E) render_stage_e ;;
  f|F) render_stage_f ;;
  all)
    render_stage_a
    render_stage_b
    render_stage_c
    render_stage_d
    render_stage_e
    render_stage_f
    ;;
  *)
    echo "ERROR: Unknown stage '${STAGE}'. Use a-f or 'all'." >&2
    exit 1
    ;;
esac

echo "Done."

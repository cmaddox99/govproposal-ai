#!/usr/bin/env bash
# phase-gate-check.test.sh — Atomic TDD test suite for phase-gate-check.sh
# Spec: workflow-human-gate-enforcement
# Laws: ENG-4.1, ENG-4.3 (FIRST), ENG-4.4 (Given-When-Then), ENG-4.5 (naming)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
GATE_SCRIPT="$SCRIPT_DIR/phase-gate-check.sh"
PASS=0; FAIL=0

_pass() { echo "  ✅ PASS: $1"; PASS=$((PASS+1)); }
_fail() { echo "  ❌ FAIL: $1"; FAIL=$((FAIL+1)); }

run_test() {
  local name="$1"; shift
  echo ""
  echo "TEST: $name"
  if "$@"; then _pass "$name"; else _fail "$name"; fi
}

# ---------------------------------------------------------------------------
# T-01: phase-gate-check_withScript_isExecutable
# GIVEN the tools/gate/ directory exists
# WHEN  we check phase-gate-check.sh
# THEN  it must exist and be executable
# ---------------------------------------------------------------------------
test_phase-gate-check_withScript_isExecutable() {
  [ -f "$GATE_SCRIPT" ] && [ -x "$GATE_SCRIPT" ]
}

# ---------------------------------------------------------------------------
# T-02: phase-gate-check_withNoApprovalFile_exitsNonZero
# GIVEN a spec ID and phase number with no approval file present
# WHEN  phase-gate-check.sh is invoked
# THEN  it exits non-zero and prints a gate-locked message citing ENG-12.1
# ---------------------------------------------------------------------------
test_T02_phase-gate-check_withNoApprovalFile_exitsNonZero() {
  local tmp_dir; tmp_dir="$(mktemp -d)"
  local output exit_code

  output=$("$GATE_SCRIPT" 3 "test-spec-001" "$tmp_dir" 2>&1) && exit_code=$? || exit_code=$?
  rm -rf "$tmp_dir"

  [ "$exit_code" -ne 0 ] || { echo "expected non-zero exit, got 0"; return 1; }
  echo "$output" | grep -qi "ENG-12.1"      || { echo "expected ENG-12.1 in output, got: $output"; return 1; }
  echo "$output" | grep -qi "gate\|locked\|approved" || { echo "expected gate/locked/approved in output, got: $output"; return 1; }
}

# ---------------------------------------------------------------------------
# T-03: phase-gate-check_withApprovalFile_exitsZero
# GIVEN a spec ID and phase number with a valid approval file present
# WHEN  phase-gate-check.sh is invoked
# THEN  it exits 0 and echoes the gate-open message with approval content
# ---------------------------------------------------------------------------
test_T03_phase-gate-check_withApprovalFile_exitsZero() {
  local tmp_dir; tmp_dir="$(mktemp -d)"
  local spec_id="test-spec-001"
  local phase=3
  local approval_dir="$tmp_dir/hangar-ai-specs/changes/$spec_id"
  mkdir -p "$approval_dir"
  echo "Approved by Jane Doe on 2026-05-06" > "$approval_dir/.phase-${phase}.approved"

  local output exit_code
  output=$("$GATE_SCRIPT" "$phase" "$spec_id" "$tmp_dir" 2>&1) && exit_code=$? || exit_code=$?
  rm -rf "$tmp_dir"

  [ "$exit_code" -eq 0 ]     || { echo "expected exit 0, got $exit_code; output: $output"; return 1; }
  echo "$output" | grep -qi "open\|approved\|proceed" || { echo "expected open/approved/proceed in output, got: $output"; return 1; }
}

# ---------------------------------------------------------------------------
# RUN (Atomic TDD — cumulative: T-01 + T-02 + T-03)
# ---------------------------------------------------------------------------
echo "========================================================"
echo "phase-gate-check.sh — Atomic TDD Test Suite"
echo "Spec: workflow-human-gate-enforcement | T-03"
echo "Laws: ENG-4.1 | ENG-4.3 | ENG-4.4 | ENG-4.5"
echo "========================================================"

run_test "T01_phase-gate-check_withScript_isExecutable" \
  test_phase-gate-check_withScript_isExecutable

run_test "T02_phase-gate-check_withNoApprovalFile_exitsNonZero" \
  test_T02_phase-gate-check_withNoApprovalFile_exitsNonZero

run_test "T03_phase-gate-check_withApprovalFile_exitsZero" \
  test_T03_phase-gate-check_withApprovalFile_exitsZero

echo ""
echo "========================================================"
echo "Results: $PASS passed, $FAIL failed"
echo "========================================================"
[ "$FAIL" -eq 0 ]

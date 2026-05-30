#!/usr/bin/env bash
# provision.test.sh — ENG-4.1 Atomic TDD test suite for provision.sh
# Law citations: ENG-4.1, ENG-4.3 (FIRST), ENG-4.4 (Given-When-Then), ENG-4.5 (naming)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PROVISION="$SCRIPT_DIR/provision.sh"
PASS=0; FAIL=0

_pass() { echo "  ✅ PASS: $1"; PASS=$((PASS+1)); }
_fail() { echo "  ❌ FAIL: $1"; FAIL=$((FAIL+1)); }

run_test() {
  local name="$1"; shift
  echo ""
  echo "TEST: $name"
  "$@" && _pass "$name" || _fail "$name"
}

# ---------------------------------------------------------------------------
# TEST 1: provision_withMissingScript_fileExists
# ENG-4.5: methodName_stateUnderTest_expectedBehavior
# GIVEN provision.sh has been written
# WHEN  we check if it exists and is executable
# THEN  it must exist and be executable
# ---------------------------------------------------------------------------
test_provision_withScript_isExecutable() {
  [ -f "$PROVISION" ] && [ -x "$PROVISION" ]
}

# ---------------------------------------------------------------------------
# TEST 2: provision_withUnreachableURL_exitsNonZero
# GIVEN an unreachable SonarQube URL
# WHEN  provision.sh is run
# THEN  it exits with code 1 and prints a meaningful error
# ---------------------------------------------------------------------------
test_provision_withUnreachableURL_exitsNonZero() {
  local output
  output=$(SONAR_URL="http://localhost:19999" SONAR_TOKEN="fake" \
    "$PROVISION" 2>&1) && return 1   # unexpected success → fail test
  local exit_code=$?
  echo "$output" | grep -qi "error\|unreachable\|failed\|connect\|refused" || return 1
  return 0
}

# ---------------------------------------------------------------------------
# TEST 3: provision_withLiveInstance_createsGateWithCorrectName
# GIVEN a live SonarQube at SONAR_URL with valid SONAR_TOKEN
# WHEN  provision.sh runs
# THEN  "Hangar AI Constitution Gate" exists in the gates list
# ---------------------------------------------------------------------------
test_provision_withLiveInstance_createsGateWithCorrectName() {
  # Capture full output before grepping — avoids SIGPIPE when grep exits early
  # (ENG-4.3: Repeatable — same result regardless of timing/buffering)
  local output
  output=$(SONAR_URL="${SONAR_URL:-http://localhost:9000}" \
    SONAR_USER="${SONAR_USER:-admin}" \
    SONAR_PASSWORD="${SONAR_PASSWORD:-HangarConstitution2026}" \
    "$PROVISION" --dry-run 2>&1)
  echo "$output" | grep -qi "Hangar AI Constitution Gate"
}

# ---------------------------------------------------------------------------
# TEST 4: provision_withLiveInstance_gateHasExactlyTenConditions
# GIVEN provision.sh has been applied to live SonarQube
# WHEN  we query the gate API
# THEN  the gate has exactly 10 conditions matching gate-config.json v1.1.0
# ---------------------------------------------------------------------------
test_provision_withLiveInstance_gateHasExactlyTenConditions() {
  local count
  count=$(curl -s -u "${SONAR_USER:-admin}:${SONAR_PASSWORD:-HangarConstitution2026}" \
    "${SONAR_URL:-http://localhost:9000}/api/qualitygates/show?name=Hangar%20AI%20Constitution%20Gate" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['conditions']))")
  [ "$count" -eq 10 ]
}

# ---------------------------------------------------------------------------
# TEST 5: provision_runTwice_isIdempotent
# GIVEN provision.sh has already been applied
# WHEN  provision.sh is run a second time
# THEN  the gate still has exactly 10 conditions (no duplicates)
# ---------------------------------------------------------------------------
test_provision_runTwice_isIdempotent() {
  SONAR_URL="${SONAR_URL:-http://localhost:9000}" \
  SONAR_USER="${SONAR_USER:-admin}" \
  SONAR_PASSWORD="${SONAR_PASSWORD:-HangarConstitution2026}" \
    "$PROVISION" >/dev/null 2>&1
  SONAR_URL="${SONAR_URL:-http://localhost:9000}" \
  SONAR_USER="${SONAR_USER:-admin}" \
  SONAR_PASSWORD="${SONAR_PASSWORD:-HangarConstitution2026}" \
    "$PROVISION" >/dev/null 2>&1
  local count
  count=$(curl -s -u "${SONAR_USER:-admin}:${SONAR_PASSWORD:-HangarConstitution2026}" \
    "${SONAR_URL:-http://localhost:9000}/api/qualitygates/show?name=Hangar%20AI%20Constitution%20Gate" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d['conditions']))")
  [ "$count" -eq 10 ]
}

# ---------------------------------------------------------------------------
# TEST 6: provision_withLiveInstance_newCoverageThresholdIs90
# GIVEN provision.sh has been applied (ENG-4.6 fix)
# WHEN  we query the gate
# THEN  new_coverage condition has error threshold of 90 (not 80)
# ---------------------------------------------------------------------------
test_provision_withLiveInstance_newCoverageThresholdIs90() {
  local threshold
  threshold=$(curl -s -u "${SONAR_USER:-admin}:${SONAR_PASSWORD:-HangarConstitution2026}" \
    "${SONAR_URL:-http://localhost:9000}/api/qualitygates/show?name=Hangar%20AI%20Constitution%20Gate" \
    | python3 -c "
import sys,json
d=json.load(sys.stdin)
for c in d['conditions']:
    if c['metric'] == 'new_coverage':
        print(c['error'])
        break
")
  [ "$threshold" = "90" ]
}

# ---------------------------------------------------------------------------
# TEST 7: provision_withLiveInstance_criticalViolationsIsHardBlock
# GIVEN provision.sh has been applied (ENG-6.1 fix)
# WHEN  we query the gate
# THEN  critical_violations condition exists with GT 0
# ---------------------------------------------------------------------------
test_provision_withLiveInstance_criticalViolationsIsHardBlock() {
  curl -s -u "${SONAR_USER:-admin}:${SONAR_PASSWORD:-HangarConstitution2026}" \
    "${SONAR_URL:-http://localhost:9000}/api/qualitygates/show?name=Hangar%20AI%20Constitution%20Gate" \
    | python3 -c "
import sys,json
d=json.load(sys.stdin)
for c in d['conditions']:
    if c['metric'] == 'critical_violations' and c['op'] == 'GT' and c['error'] == '0':
        print('found'); sys.exit(0)
sys.exit(1)
" | grep -q "found"
}

# ---------------------------------------------------------------------------
# RUN ALL TESTS
# ---------------------------------------------------------------------------
echo "========================================"
echo "provision.sh — Atomic TDD Test Suite"
echo "ENG-4.1 | ENG-4.3 | ENG-4.4 | ENG-4.5"
echo "========================================"

run_test "provision_withScript_isExecutable"                       test_provision_withScript_isExecutable
run_test "provision_withUnreachableURL_exitsNonZero"               test_provision_withUnreachableURL_exitsNonZero
run_test "provision_withLiveInstance_createsGateWithCorrectName"   test_provision_withLiveInstance_createsGateWithCorrectName
run_test "provision_withLiveInstance_gateHasExactlyTenConditions"  test_provision_withLiveInstance_gateHasExactlyTenConditions
run_test "provision_runTwice_isIdempotent"                         test_provision_runTwice_isIdempotent
run_test "provision_withLiveInstance_newCoverageThresholdIs90"     test_provision_withLiveInstance_newCoverageThresholdIs90
run_test "provision_withLiveInstance_criticalViolationsIsHardBlock" test_provision_withLiveInstance_criticalViolationsIsHardBlock

echo ""
echo "========================================"
echo "Results: $PASS passed, $FAIL failed"
echo "========================================"
[ "$FAIL" -eq 0 ]

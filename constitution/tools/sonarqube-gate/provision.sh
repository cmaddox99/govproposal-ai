#!/usr/bin/env bash
# provision.sh — Hangar AI Constitution Gate Provisioner
#
# Idempotently applies gate-config.json to any SonarQube instance.
# Law citations: ENG-12.1 (gate must be provisioned before workflow phase begins),
#                ENG-12.2 (dashboard-first), ENG-4.6, ENG-6.1.
#
# Usage:
#   SONAR_URL=http://localhost:9000 SONAR_USER=admin SONAR_PASSWORD=secret ./provision.sh
#   SONAR_URL=http://sonar.corp    SONAR_TOKEN=squ_xxx ./provision.sh
#   ./provision.sh --dry-run                          (validate config + connectivity, no writes)
#   ./provision.sh --project-key=my-project           (also assign gate to project after provisioning)
#   ./provision.sh --dry-run --project-key=my-project (dry-run with project assignment preview)
#
# Exit codes:
#   0  — gate provisioned and verified successfully
#   1  — configuration or connectivity error (fast-fail per ENG-3.7)
#   2  — gate verification failed after provisioning

set -euo pipefail

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
GATE_NAME="Hangar AI Constitution Gate"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/gate-config.json"

# ---------------------------------------------------------------------------
# Argument parsing  (ENG-3.4: single responsibility per function)
# ---------------------------------------------------------------------------
DRY_RUN=false
PROJECT_KEY=""

for arg in "$@"; do
  case "$arg" in
    --dry-run)       DRY_RUN=true ;;
    --project-key=*) PROJECT_KEY="${arg#*=}" ;;
    --help|-h)
      sed -n '/^# Usage:/,/^$/p' "$0"
      exit 0
      ;;
    *)
      echo "ERROR: Unknown argument: $arg" >&2
      exit 1
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Configuration resolution (ENG-5.6: externalized config, never hardcoded)
# ---------------------------------------------------------------------------
SONAR_URL="${SONAR_URL:-}"
SONAR_USER="${SONAR_USER:-}"
SONAR_PASSWORD="${SONAR_PASSWORD:-}"
SONAR_TOKEN="${SONAR_TOKEN:-}"

if [ -z "$SONAR_URL" ]; then
  echo "ERROR: SONAR_URL is required (e.g. export SONAR_URL=http://localhost:9000)" >&2
  exit 1
fi

# Build auth header: token takes precedence over user/password
_auth_args() {
  if [ -n "$SONAR_TOKEN" ]; then
    echo "-u ${SONAR_TOKEN}:"
  elif [ -n "$SONAR_USER" ] && [ -n "$SONAR_PASSWORD" ]; then
    echo "-u ${SONAR_USER}:${SONAR_PASSWORD}"
  else
    echo "ERROR: Provide SONAR_TOKEN or both SONAR_USER and SONAR_PASSWORD" >&2
    exit 1
  fi
}

# ---------------------------------------------------------------------------
# Connectivity check (ENG-3.7: fail fast on unrecoverable errors)
# ---------------------------------------------------------------------------
_check_connectivity() {
  local status
  # shellcheck disable=SC2046
  status=$(curl -s --max-time 5 $(_auth_args) \
    "${SONAR_URL}/api/system/status" 2>/dev/null \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('status','DOWN'))" 2>/dev/null \
    || echo "DOWN")

  if [ "$status" != "UP" ]; then
    echo "ERROR: SonarQube at ${SONAR_URL} is unreachable or not UP (status=${status})" >&2
    echo "       Verify SONAR_URL and credentials. ENG-12.1 requires gate provisioned before workflow." >&2
    exit 1
  fi
  echo "INFO:  SonarQube ${SONAR_URL} is UP ✅"
}

# ---------------------------------------------------------------------------
# Config validation
# ---------------------------------------------------------------------------
_validate_config() {
  if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERROR: gate-config.json not found at $CONFIG_FILE" >&2
    exit 1
  fi
  local version total
  version=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d['gate']['version'])")
  total=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(sum(len(c['items']) for c in d['conditions']))")
  echo "INFO:  gate-config.json v${version} loaded — ${total} conditions"
  if $DRY_RUN; then
    echo "INFO:  Gate name: ${GATE_NAME}"
    python3 -c "
import json
d = json.load(open('$CONFIG_FILE'))
for cls in d['conditions']:
    for item in cls['items']:
        print(f\"INFO:    [{cls['classification']:12s}] {item['id']:5s}  {item['metric']:45s} {item['operator']} {item['error_threshold']}\")
"
  fi
}

# ---------------------------------------------------------------------------
# Core: get or create gate, return gate ID
# ---------------------------------------------------------------------------
_get_or_create_gate() {
  # shellcheck disable=SC2046
  local existing_id
  existing_id=$(curl -s $(_auth_args) "${SONAR_URL}/api/qualitygates/list" \
    | python3 -c "
import sys,json
gates = json.load(sys.stdin).get('qualitygates', [])
for g in gates:
    if g['name'] == '${GATE_NAME}':
        print(g['id']); sys.exit(0)
sys.exit(1)
" 2>/dev/null || true)

  if [ -n "$existing_id" ]; then
    echo "INFO:  Gate '${GATE_NAME}' exists (id=${existing_id})" >&2
    echo "$existing_id"
    return
  fi

  echo "INFO:  Creating gate '${GATE_NAME}'..." >&2
  # shellcheck disable=SC2046
  local new_id
  new_id=$(curl -s $(_auth_args) -X POST \
    "${SONAR_URL}/api/qualitygates/create" \
    -d "name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${GATE_NAME}'))")" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
  echo "INFO:  Created gate id=${new_id}" >&2
  echo "$new_id"
}

# ---------------------------------------------------------------------------
# Core: reconcile conditions (idempotent — ENG-4.1 atomic TDD requirement)
# Each condition is identified by metric name. If it already exists with the
# correct op+threshold it is left untouched. Wrong threshold → delete+recreate.
# Conditions not in spec → deleted (prevent drift from gate-config.json).
# ---------------------------------------------------------------------------
_reconcile_conditions() {
  local gate_id="$1"

  # Build desired state from config as "metric|op|threshold" lines
  local desired
  desired=$(python3 -c "
import json
d = json.load(open('$CONFIG_FILE'))
for cls in d['conditions']:
    for item in cls['items']:
        print(f\"{item['metric']}|{item['operator']}|{item['error_threshold']}\")
")

  # Get current conditions from API
  # shellcheck disable=SC2046
  local current_json
  current_json=$(curl -s $(_auth_args) \
    "${SONAR_URL}/api/qualitygates/show?name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${GATE_NAME}'))")")

  # Delete conditions NOT in spec (drift prevention)
  echo "$current_json" | python3 -c "
import sys,json
data = json.load(sys.stdin)
desired_metrics = set()
import subprocess, os
spec = json.load(open(os.environ.get('CONFIG_FILE','$CONFIG_FILE')))
for cls in spec['conditions']:
    for item in cls['items']:
        desired_metrics.add(item['metric'])
for c in data.get('conditions', []):
    if c['metric'] not in desired_metrics:
        print(f\"DELETE {c['id']} {c['metric']}\")
" | while read -r action cid cmetric; do
    if [ "$action" = "DELETE" ]; then
      echo "INFO:  Removing non-spec condition: ${cmetric} (id=${cid})" >&2
      # shellcheck disable=SC2046
      $DRY_RUN || curl -s $(_auth_args) -X POST \
        "${SONAR_URL}/api/qualitygates/delete_condition" \
        -d "id=${cid}" >/dev/null
    fi
  done

  # For each desired condition: create if missing, update if wrong, skip if correct
  echo "$desired" | while IFS='|' read -r metric op threshold; do
    # shellcheck disable=SC2046
    local current_state
    current_state=$(curl -s $(_auth_args) \
      "${SONAR_URL}/api/qualitygates/show?name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${GATE_NAME}'))")" \
      | python3 -c "
import sys,json
data = json.load(sys.stdin)
for c in data.get('conditions', []):
    if c['metric'] == '${metric}':
        print(f\"{c['id']}|{c['op']}|{c['error']}\")
        sys.exit(0)
print('MISSING')
" 2>/dev/null || echo "MISSING")

    if [ "$current_state" = "MISSING" ]; then
      echo "INFO:  Adding condition: ${metric} ${op} ${threshold}" >&2
      if ! $DRY_RUN; then
        # shellcheck disable=SC2046
        curl -s $(_auth_args) -X POST \
          "${SONAR_URL}/api/qualitygates/create_condition" \
          -d "gateName=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${GATE_NAME}'))")" \
          -d "metric=${metric}" \
          -d "op=${op}" \
          -d "error=${threshold}" >/dev/null
      fi
    else
      local existing_id existing_op existing_threshold
      IFS='|' read -r existing_id existing_op existing_threshold <<< "$current_state"
      if [ "$existing_op" = "$op" ] && [ "$existing_threshold" = "$threshold" ]; then
        echo "INFO:  Condition OK (no change): ${metric} ${op} ${threshold}" >&2
      else
        echo "INFO:  Updating condition: ${metric} ${existing_op}/${existing_threshold} → ${op}/${threshold}" >&2
        if ! $DRY_RUN; then
          # shellcheck disable=SC2046
          curl -s $(_auth_args) -X POST \
            "${SONAR_URL}/api/qualitygates/update_condition" \
            -d "id=${existing_id}" \
            -d "metric=${metric}" \
            -d "op=${op}" \
            -d "error=${threshold}" >/dev/null
        fi
      fi
    fi
  done
}

# ---------------------------------------------------------------------------
# Verification: assert gate matches spec exactly
# ---------------------------------------------------------------------------
_verify_gate() {
  echo "INFO:  Verifying gate against spec..." >&2
  # shellcheck disable=SC2046
  local result
  result=$(curl -s $(_auth_args) \
    "${SONAR_URL}/api/qualitygates/show?name=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${GATE_NAME}'))")" \
    | python3 -c "
import sys,json
data = json.load(sys.stdin)
spec = json.load(open('$CONFIG_FILE'))

desired = {}
for cls in spec['conditions']:
    for item in cls['items']:
        desired[item['metric']] = (item['operator'], str(item['error_threshold']))

actual = {}
for c in data.get('conditions', []):
    actual[c['metric']] = (c['op'], c['error'])

errors = []
for metric, (op, threshold) in desired.items():
    if metric not in actual:
        errors.append(f'MISSING: {metric}')
    elif actual[metric] != (op, threshold):
        errors.append(f'WRONG:   {metric} expected {op}/{threshold}, got {actual[metric][0]}/{actual[metric][1]}')

extra = set(actual) - set(desired)
for m in extra:
    errors.append(f'EXTRA:   {m} (not in spec — drift)')

total_actual = len(actual)
total_desired = len(desired)

if errors:
    print('FAIL')
    for e in errors: print(f'  {e}')
else:
    print(f'PASS ({total_actual}/{total_desired} conditions match spec)')
")
  echo "INFO:  Verification: $result" >&2
  echo "$result" | grep -q "^PASS"
}

# ---------------------------------------------------------------------------
# Optional: assign gate to a project
# ---------------------------------------------------------------------------
_assign_to_project() {
  local project_key="$1"
  echo "INFO:  Assigning gate to project: ${project_key}" >&2
  if ! $DRY_RUN; then
    # shellcheck disable=SC2046
    curl -s $(_auth_args) -X POST \
      "${SONAR_URL}/api/qualitygates/select" \
      -d "gateName=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${GATE_NAME}'))")" \
      -d "projectKey=${project_key}" >/dev/null
    echo "INFO:  Assigned ✅" >&2
  fi
}

# ---------------------------------------------------------------------------
# Main orchestration  (ENG-3.4: functions compose, main orchestrates)
# ---------------------------------------------------------------------------
main() {
  echo "========================================================"
  echo " Hangar AI Constitution Gate Provisioner"
  echo " gate-config.json: $(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['gate']['version'])")"
  $DRY_RUN && echo " Mode: DRY RUN (no writes)" || echo " Mode: APPLY"
  echo "========================================================"

  _check_connectivity
  _validate_config

  if $DRY_RUN; then
    echo "INFO:  Dry run complete — no changes made."
    return 0
  fi

  local gate_id
  gate_id=$(_get_or_create_gate)
  _reconcile_conditions "$gate_id"

  if ! _verify_gate; then
    echo "ERROR: Gate verification FAILED — conditions do not match spec." >&2
    echo "       Review output above and re-run. ENG-12.3: gate is the referee." >&2
    exit 2
  fi

  [ -n "$PROJECT_KEY" ] && _assign_to_project "$PROJECT_KEY"

  echo ""
  echo "========================================================"
  echo " ✅  Gate provisioned and verified."
  echo " Dashboard: ${SONAR_URL}/quality_gates"
  echo " ENG-12.1: Open dashboard before reviewing gate results."
  echo "========================================================"
}

export CONFIG_FILE
main "$@"

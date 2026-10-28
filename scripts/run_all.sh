#!/usr/bin/env bash
# Repeatable test harness: runs the scripted checks that don't require
# interactive credentials, and writes a combined pass/fail summary to
# results/report.json. This is the script run by CI
# (.github/workflows/security-tests.yml) and by hand during manual testing.
#
# The ZAP baseline scan and access_control_test.py (which needs live user
# tokens) are run separately — see README.md — because they need either
# Docker or interactively-obtained session tokens that CI does not have.
#
# Usage: ./scripts/run_all.sh [target_url]

set -uo pipefail

TARGET_URL="${1:-http://127.0.0.1:3000}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_FILE="${ROOT_DIR}/results/report.json"

mkdir -p "${ROOT_DIR}/results"

echo "Target: ${TARGET_URL}"
echo "---"

sqli_result=$(python3 "${ROOT_DIR}/scripts/sqli_check.py" --base-url "${TARGET_URL}")
sqli_status=$?
echo "${sqli_result}"
echo "---"

overall="PASS"
if [ "${sqli_status}" -ne 0 ]; then overall="FAIL"; fi

python3 - "$RESULTS_FILE" "$sqli_result" "$overall" "$TARGET_URL" <<'PYEOF'
import json
import sys
from datetime import datetime, timezone

out_path, sqli_json, overall, target = sys.argv[1:5]
report = {
    "run_at": datetime.now(timezone.utc).isoformat(),
    "target": target,
    "overall": overall,
    "checks": [json.loads(sqli_json)],
    "note": "access_control_test.py and zap_baseline.sh run separately and are not included in this automated summary (see README.md).",
}
with open(out_path, "w") as f:
    json.dump(report, f, indent=2)
print(f"Summary written to {out_path}")
PYEOF

echo "Overall: ${overall}"
[ "${overall}" = "PASS" ] && exit 0 || exit 1

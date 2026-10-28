#!/usr/bin/env bash
# Runs the OWASP ZAP baseline (passive) scan against the Juice Shop
# instance reachable through the SSH tunnel, and writes an HTML + JSON
# report into evidence/zap-reports/.
#
# Requires: Docker, and the SSH tunnel to the VM already open so that
# http://127.0.0.1:3000 resolves to the target.
#
# Usage: ./scripts/zap_baseline.sh [target_url]

set -euo pipefail

TARGET_URL="${1:-http://127.0.0.1:3000}"
OUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/evidence/zap-reports"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$OUT_DIR"

echo "Running ZAP baseline scan against ${TARGET_URL}..."

# --network host lets the container reach the tunnel on the host's
# loopback interface. -I prevents the scan from failing the whole run on
# WARN-level alerts (we want the report either way).
docker run --rm --network host \
  -v "${OUT_DIR}:/zap/wrk:rw" \
  zaproxy/zap-stable zap-baseline.py \
  -t "${TARGET_URL}" \
  -r "zap-baseline-${TIMESTAMP}.html" \
  -J "zap-baseline-${TIMESTAMP}.json" \
  -I

echo "Report written to ${OUT_DIR}/zap-baseline-${TIMESTAMP}.html"

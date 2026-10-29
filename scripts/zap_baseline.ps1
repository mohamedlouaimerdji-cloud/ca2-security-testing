# Runs the OWASP ZAP baseline (passive) scan against the Juice Shop
# instance, reached through the SSH tunnel, and writes an HTML + JSON
# report into evidence/zap-reports/.
#
# Windows PowerShell equivalent of scripts/zap_baseline.sh. The only real
# difference is networking: Docker Desktop on Windows doesn't support
# --network host, so the container reaches the host (where the SSH tunnel
# forwards 127.0.0.1:3000) via the special address host.docker.internal
# instead.
#
# Requires: Docker Desktop running, and the SSH tunnel to the VM already
# open so that http://127.0.0.1:3000 resolves to the target on this machine.
#
# Usage: .\scripts\zap_baseline.ps1 [-TargetUrl "http://host.docker.internal:3000/"]

param(
    [string]$TargetUrl = "http://host.docker.internal:3000/"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$OutDir = Join-Path $RepoRoot "evidence\zap-reports"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$HtmlReport = "zap-baseline-$Timestamp.html"
$JsonReport = "zap-baseline-$Timestamp.json"

Write-Host "Running ZAP baseline scan against $TargetUrl..."

docker run --rm `
    -v "${OutDir}:/zap/wrk:rw" `
    zaproxy/zap-stable zap-baseline.py `
    -t $TargetUrl `
    -r $HtmlReport `
    -J $JsonReport `
    -I

Write-Host "Report written to $OutDir\$HtmlReport"

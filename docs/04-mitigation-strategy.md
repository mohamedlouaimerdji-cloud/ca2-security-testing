# Mitigation strategy

*To be completed after testing (Day 9 of the plan). Structure below is fixed
so the report can be assembled directly from this file.*

For each confirmed finding, record:

- Finding ID and one-line description
- Fix owner: **Application team** (code/config changes within Juice Shop)
  or **Cloud platform** (Azure/NSG/VM-level changes outside the app)
- Concrete remediation step(s)
- Priority (tie back to CVSS from CA1 / re-scored here if retested)

## Application team

| Finding | Fix | Priority |
| --- | --- | --- |
| F1 — SQLi login bypass | Parameterised queries at the login endpoint | Critical |
| F2 — Insecure session token storage | Add HttpOnly, Secure, SameSite to the session cookie | High |
| F6 — @fastify/busboy DoS (CVE-2026-19481) | Update to patched release | High |
| F4 — Unauthenticated info disclosure | Restrict/remove the unauthenticated configuration endpoint | Medium |
| (access control findings from this round) | TBD once tested | TBD |

## Cloud platform

| Finding | Fix | Priority |
| --- | --- | --- |
| F3 — Missing TLS | Terminate TLS at a reverse proxy / Azure Application Gateway | Medium |
| F5 — Insecure container configuration | Read-only root filesystem, memory limits, capability restriction (CIS Docker Benchmark WARNs) | Medium (defence-in-depth) |
| (encryption-at-rest findings from this round) | TBD once tested — may split between app (if app-level encryption needed) and platform (Azure disk encryption config) | TBD |
| Logging/alerting | Centralised logging (e.g. Azure Monitor) — CA1 Section 4 flagged this as entirely absent | High |

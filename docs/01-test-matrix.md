# Test matrix

Technique × CA1 trust boundary (TB1–TB4, CA1 Section 2.2).

| Technique | TB1 | TB2 | TB3 | TB4 |
| --- | --- | --- | --- | --- |
| Unauthenticated testing | ✓ | ✓ | | |
| Authenticated testing | | ✓ | ✓ | |
| Access control testing | | ✓ | ✓ | |
| Encryption in transit | ✓ | | | |
| Encryption at rest | | | ✓ | ✓ |

## Unauthenticated testing
Re-tests F1 (SQLi login bypass) and F4 (unauthenticated info disclosure)
from outside, with no credentials. Tools: OWASP ZAP (baseline + active),
manual probing. Evidence: `evidence/unauthenticated/`.

## Authenticated testing
Tests what a logged-in user can reach beyond the unauthenticated surface
(basket, orders, profile, feedback/upload). Tools: ZAP with an authenticated
session. Evidence: `evidence/authenticated/`.

## Access control testing
Tests something CA1 only inferred — A01 Broken Access Control was "confirmed"
solely via the SQLi admin bypass, not via independent IDOR/privilege testing
between ordinary accounts. Two low-privilege accounts + the F1 admin session;
horizontal and vertical checks. Tools: `scripts/access_control_test.py`,
Burp Community for manual spot-checks. Evidence: `evidence/access-control/`.

## Encryption in transit
Confirms F3 with packet-level evidence rather than config inference; shows
what the SSH tunnel protects vs what the app itself provides. Tools:
`tcpdump`, browser dev tools. Evidence: `evidence/encryption-in-transit/`.

## Encryption at rest
A gap CA1 did not assess. Checks the SQLite file and password hashing
inside the container, and the Azure OS disk encryption status. Tools:
`sqlite3` CLI, Azure CLI (`az vm show`, `az disk show`). Evidence:
`evidence/encryption-at-rest/`.

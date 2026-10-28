# CA1 predictions (recorded before testing)

Recorded from the CA1 threat model before any testing in this project began,
so the comparison in the report's reflection section is not written with
hindsight. **This table is fixed — do not edit it once testing starts.**
Actual outcomes go in a separate column/document added later.

| # | Area | CA1 prediction | Basis in CA1 | Confidence |
| --- | --- | --- | --- | --- |
| P1 | Unauthenticated login (TB1/TB2) | SQL injection authentication bypass remains exploitable; no perimeter control would stop or detect it | Section 3.1, F1, CVSS 9.1 | High — directly exploited in CA1 |
| P2 | Unauthenticated info disclosure | Configuration endpoint reachable without login, exposing internal IPs/config, not user data | F4, CVSS 5.3 | High — already found via ZAP |
| P3 | Authenticated session handling | Session token lacks HttpOnly/Secure/SameSite; theft needs an extra step, not purely remote | F2, CVSS 7.4 | Medium — inferred from config, not demonstrated |
| P4 | Access control (horizontal/vertical) | Not tested in CA1; A01 marked "confirmed" only via the SQLi bypass, not direct IDOR/privilege-escalation testing | Section 5.1, A01 | None — untested assumption |
| P5 | Encryption in transit | Plaintext HTTP; real exposure during CA1 testing reduced because the assessor's own traffic ran inside the SSH tunnel | F3, CVSS 5.9, Section 6.2 | High — config-confirmed, not packet-captured |
| P6 | Encryption at rest | Not assessed in CA1 at all | Not covered in CA1 | None — genuine gap |
| P7 | Container isolation (TB4) | Hardening gaps exist but only exploitable by an attacker already inside the container, combined with a further escape technique | F5, CVSS 4.5 | Medium — scored but not exploited |
| P8 | CSRF (M3) | SameSite cookie absence allows forged state-changing requests from another origin while authenticated | M3, via F2's cookie finding | Medium — inferred, not demonstrated with a live PoC |
| P9 | DoS via dependency (F6) | @fastify/busboy vulnerability can crash the Node process with a single crafted request | F6, CVSS 7.5, NVD vector | High — taken from NVD, not independently tested |

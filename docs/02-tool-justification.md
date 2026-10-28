# Tool justification

## Tools selected

| Tool | Used for | Justification |
| --- | --- | --- |
| OWASP ZAP | Unauthenticated + authenticated scanning | Already used in CA1 (F2–F4), so results are directly comparable; free, scriptable, supports passive baseline and active scanning, supports authenticated contexts via session tokens |
| Python (`requests`) | Access control testing + automation harness | No off-the-shelf tool tests application-specific object-ID patterns well; lets session tokens/IDs be swapped programmatically, with results logged automatically; doubles as the automation artefact |
| Burp Suite Community (manual) | Spot-checking access control findings the script flags | Repeater is sufficient to manually confirm an IDOR once a candidate is found |
| tcpdump / browser dev tools | Encryption in transit | Already on the Ubuntu VM; captures what's actually on the wire rather than inferring from config |
| `sqlite3` CLI | Encryption at rest, data store | Bundled in the container; inspects whether stored passwords/PII are hashed or plaintext |
| Azure CLI (`az vm show`, `az disk show`) | Encryption at rest, platform layer | Distinguishes app-level failure to encrypt from platform-level encryption that applies regardless |
| GitHub Actions / bash wrapper | Automation | Ties the ZAP baseline scan + access control script into one repeatable job with a pass/fail report |

## Tools and techniques deliberately not used

| Tool / technique | Reason for exclusion |
| --- | --- |
| Nessus / OpenVAS | Disproportionate to one container on one VM already covered by the CIS Docker Benchmark in CA1 |
| Nikto | Overlaps almost entirely with ZAP's passive scan |
| sqlmap | F1 already confirmed manually with a single payload in CA1; automated exploitation risks damaging the single shared DB file for no extra assessment value |
| Metasploit | Built for exploitation/post-exploitation, not assessment; disproportionate and risks exceeding the authorisation's intent |
| Fuzzing (e.g. ffuf) beyond confirming F6 | Repeatedly crashing the one shared VM wastes time and risks losing the environment; F6 already scored from NVD |
| Commercial WAF/DAST platforms | No WAF exists in this deployment (CA1 Table 3); cost-prohibitive for a student project |
| Social engineering / phishing tooling | Single-user lab app, no human targets, not relevant to the modelled trust boundaries |

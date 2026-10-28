# CA2 — Security Testing Programme: OWASP Juice Shop

Follow-on security testing programme against the same target assessed in CA1
(threat modelling): an OWASP Juice Shop instance running in Docker on an
Azure VM (`vm-juiceshop`, Ubuntu 24.04), bound to `127.0.0.1:3000` and
reachable only through a key-authenticated SSH tunnel.

This repository holds the evidence, scripts and automation artefact that
support the written report. The report itself (narrative, CVSS-style
evaluation, mitigation strategy, and the CA1 threat-model reflection) is
maintained separately and is not duplicated here; this repo is the
**evidence trail** the report cites.

> Target, authorisation and deployment conditions are unchanged from CA1.
> Testing is confined to the student's own authorised deployment. No CCT
> system or third-party service is in scope. See `docs/00-scope-and-authorisation.md`.

## Structure

```
.
├── docs/                      Narrative support documents (mirrors CA1's docs/00-05 convention)
│   ├── 00-scope-and-authorisation.md
│   ├── 01-test-matrix.md          Technique × CA1 trust boundary (TB1-TB4)
│   ├── 02-tool-justification.md   Tools used and tools deliberately rejected
│   ├── 03-ca1-predictions.md      Predictions recorded BEFORE testing (for Section 7's reflection)
│   ├── 04-mitigation-strategy.md  App-team vs cloud-platform split
│   ├── 05-threat-model-reflection.md
│   └── 06-ai-fluency-log.md       Dated log of AI (Claude) use, per the assignment's AI Fluency requirement
│
├── evidence/                  Raw evidence, one folder per technique
│   ├── unauthenticated/
│   ├── authenticated/
│   ├── access-control/
│   ├── encryption-in-transit/
│   ├── encryption-at-rest/
│   └── zap-reports/            ZAP baseline/active scan output (HTML/JSON/MD)
│
├── scripts/                   Testing and automation scripts
│   ├── zap_baseline.sh         Wraps the ZAP baseline scan against the tunnel
│   ├── access_control_test.py  Horizontal/vertical privilege + IDOR checks (also the automation artefact)
│   ├── check_cookie_flags.py   Confirms F2/M3: HttpOnly/Secure/SameSite on the session cookie
│   ├── sqli_check.py           Re-confirms F1 (SQLi login bypass) in a scripted, non-destructive way
│   └── run_all.sh              Runs the full repeatable test harness, writes results/report.json
│
├── results/                   Machine-readable output of `scripts/run_all.sh` (pass/fail per check)
│
├── .github/workflows/
│   └── security-tests.yml      CI job: runs the repeatable subset of testing on demand / schedule
│
├── requirements.txt
└── .gitignore
```

## Running the automated checks

Requires the SSH tunnel to the VM to be active (`127.0.0.1:3000` reachable)
and Python 3.11+.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./scripts/run_all.sh
```

Results are written to `results/report.json` (machine-readable) and printed
as a pass/fail summary. The ZAP baseline step requires Docker (uses the
official `zaproxy/zap-stable` image).

## Relationship to CA1

CA1 built a STRIDE threat model across four trust boundaries (TB1-TB4) and a
first-pass vulnerability assessment (findings F1-F6). This project tests that
model directly: each technique in `docs/01-test-matrix.md` is mapped back to
a specific trust boundary or finding, and `docs/03-ca1-predictions.md`
records what CA1 predicted *before* this testing began, so the final
reflection in the report is a genuine comparison rather than hindsight.

## Authorisation

Testing is carried out only against the student's own authorised deployment,
under the same conditions confirmed by the module lecturer for CA1 (see
`docs/00-scope-and-authorisation.md`). No system outside this deployment is
in scope.

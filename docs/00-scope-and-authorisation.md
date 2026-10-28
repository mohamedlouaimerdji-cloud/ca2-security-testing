# Scope and authorisation

## Target

OWASP Juice Shop (Docker image digest `sha256:73c53fbf442e…`), deployed on
an Azure VM `vm-juiceshop` (Ubuntu 24.04), bound to `127.0.0.1:3000` and
reachable only through a key-authenticated SSH tunnel. Same deployment as
CA1.

## Authorisation

This is a follow-on to CA1 against the same, student-owned deployment. The
CA1 authorisation (Dr Matt Lemon, email, 5 October 2026 — see CA1 Section
1.1) applies to this testing programme as well, under the same conditions:

- The container must not be exposed to the internet or the college network.
- It must remain bound to `127.0.0.1:3000` only.
- No CCT system or third-party service is in scope.

*(Action: attach/record the follow-up confirmation from Dr Lemon covering
this specific testing programme once received — see `docs/06-ai-fluency-log.md`
for dated correspondence conventions used throughout.)*

## In scope

- The Juice Shop application (client + server).
- Its SQLite data store.
- The parts of the Azure platform layer relevant to:
  - encryption at rest (OS disk), and
  - network exposure (NSG).
- Re-uses trust boundaries TB1–TB4 as defined in CA1 Section 2.2.

## Out of scope

- Any system other than the authorised deployment.
- Denial-of-service testing beyond confirming the known F6 vulnerability
  once (CVE-2026-19481).
- Infrastructure-wide scanning of the Ubuntu host or Azure subscription
  beyond what the encryption-at-rest objective needs.
- Any CCT system or third-party service.

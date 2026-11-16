# Mitigation strategy

For each confirmed finding: what it is, who fixes it, the concrete step, and
priority. Split between the **application team** (code/config changes inside
the Juice Shop codebase or its container) and the **cloud platform**
(Azure/VM/NSG-level changes that sit outside the app itself). New findings
from this round (not in CA1) are marked **[NEW]**.

## Application team

| Finding | Fix | Priority |
| --- | --- | --- |
| F1 — SQLi login bypass (re-confirmed exploitable) | Parameterised queries / an ORM with bound parameters at the login endpoint, instead of building SQL from raw user input | Critical |
| **[NEW]** Horizontal IDOR — any logged-in user can read any other user's basket (`/rest/basket/:id`) | Add a server-side ownership check on every request: confirm `basket.UserId === req.user.id` before returning data, not just "does a basket with this ID exist" | Critical |
| **[NEW]** Vertical privilege escalation — `/api/Users` returns the full user directory to a plain customer token | Add a role check (`req.user.role === 'admin'`) before serving this endpoint; currently it appears to perform no authorisation check at all | Critical |
| **[NEW]** Passwords hashed with unsalted MD5 (weak, pre-computable via rainbow tables; admin's hash is a publicly known MD5) | Replace with a modern, salted, slow hashing algorithm (bcrypt, scrypt, or Argon2id) and re-hash all accounts on next login | High |
| F2 / M3 — No cookie-based session; token returned in response body with no HttpOnly/Secure equivalent protection | Store the token more defensively (e.g. in-memory/short-lived, or move to an HttpOnly cookie with `Secure` and `SameSite=Strict` if switching the auth model); note M3's classic CSRF framing needs revisiting since there's no auto-attached cookie to forge (see reflection doc) | Medium |
| F6 — @fastify/busboy DoS (CVE-2026-19481) | Update the dependency to a patched release | High |
| F4 — Unauthenticated configuration endpoint disclosure | Restrict or remove the endpoint for unauthenticated users | Medium |
| Minor ZAP hygiene findings (missing CSP, Feature-Policy deprecated, COEP/CORP headers, CORS `Access-Control-Allow-Origin: *`) | Add the missing security headers via middleware (e.g. `helmet`); scope CORS to known origins instead of `*` | Low |

## Cloud platform

| Finding | Fix | Priority |
| --- | --- | --- |
| F3 — Missing TLS (confirmed: password visible in plaintext in the login request) | Terminate TLS at a reverse proxy or Azure Application Gateway in front of the VM; the SSH tunnel used for testing is not a substitute for the app serving HTTPS itself | High |
| F5 — Insecure container configuration (writable root fs, no memory limit, no capability drop) | Apply the CIS Docker Benchmark WARN-level fixes: read-only root filesystem, memory limits, capability restriction | Medium (defence-in-depth) |
| **[CONFIRMED, NO ACTION NEEDED]** Encryption at rest — Azure OS disk | Already using platform-managed key encryption by default (confirmed in testing). No change required here; the weak point is the application-layer MD5 hashing above, not the disk | N/A |
| NSG rule fragility — single-IP SSH rule breaks whenever the ISP-assigned IP changes (experienced directly during this project's testing) | Either reserve a static public IP for the testing workstation where feasible, or accept the rule needs manual updates each session and document that operational cost | Low |
| Logging/alerting — only default container logs exist; no centralised logging or alerting (CA1 Section 4) | Centralised logging (e.g. Azure Monitor / Log Analytics) so that the SQLi bypass or the IDOR/privilege-escalation findings above would actually leave a detectable trace | High |

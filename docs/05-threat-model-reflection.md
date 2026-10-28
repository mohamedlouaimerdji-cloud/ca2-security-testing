# Reflection on the CA1 threat model

*To be completed after testing, directly against `03-ca1-predictions.md`.*

For each prediction P1–P9:

1. State the actual outcome from this round of testing (link the evidence
   file(s)).
2. Mark it: **confirmed as predicted** / **confirmed but different in
   detail** / **not reproduced (possible false positive in CA1)** / **new
   finding CA1 missed entirely**.
3. One sentence on *why* — what CA1's method could or couldn't have caught.

Close with:

- What the STRIDE/trust-boundary model got right (likely P1, P2, P5, P9 —
  things CA1 inferred correctly from config/tooling).
- What it missed or could only guess at (likely P4 access control, P6
  encryption at rest — both genuine gaps, not just under-confidence).
- Whether the 65→13 manual triage in CA1 dropped anything that mattered,
  with evidence either way.

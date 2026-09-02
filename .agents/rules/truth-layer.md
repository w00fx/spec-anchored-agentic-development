# The truth layer

`specs/**` (including `tables/`), the golden tests, and
`.metrics-baseline.json` are the truth layer — the material every
verification reads. Casual sessions **read it, never write it.**

Changing truth has named flows, and only those flows write:

- Spec content → the `to-spec` skill, or the supervised adapter's **gated** semantic amendment (writer matrix) (create or delta), committed alone at the gate.
- Acceptance criteria → explicit human approval in-session; typed
  stable IDs are never renumbered or reused, only retired (tickets
  point at the IDs).
- Reference values → the human's signature: a value changes because a
  cited source changed, and the human confirms it.
- The ratchet baseline → only via its own shrink-and-lock step.

If a task seems to require editing truth outside these flows, that is
the finding — stop and name the flow; don't make the edit. A silently
edited reference table corrupts the oracle: everything downstream goes
green *and lying*.

Two floor behaviors, every session — with or without a skill:

- Work happens on a typed branch (`feature/`, `fix/`, `chore/`, …),
  never the default branch.
- "Done" is demonstrated with the runner's output visible — a claim
  without output is a claim.

Loading contract: root `AGENTS.md` routes every implementation run to this
file, and transactional skills read it explicitly. Do not duplicate the full
rule into harness-specific configuration; keep one canonical rule here.

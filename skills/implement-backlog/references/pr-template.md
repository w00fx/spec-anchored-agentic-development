# PR description template — all adapters

**Approved plan:** the executed plan, with its APPROVAL-FINGERPRINT (and,
in orchestrated-assisted, the approving reply's fingerprint — they
must match).

**What changed:** end-to-end behaviour, from the user's perspective.

**Evidence per criterion:** one line per pointed ID —
`AC-<CAP>-### → <test name> → green (runner output in the run log)`.

**Scope check:** touched paths ⊆ ticket scope; non-goals untouched.

**Risk/rollout:** flag/kill-switch state if declared; else "n/a".

**Terminal:** this run ends at `PR_READY_AWAITING_HUMAN` — the human
merges; a separate monitor observes the merge. The run never claims
"landed".

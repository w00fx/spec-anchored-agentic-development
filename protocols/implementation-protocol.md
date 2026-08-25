# Implementation protocol — the shared state machine

Every implementation skill (`implement-feature`, `implement-orchestrated`,
`implement-backlog`) runs THIS machine. The skill you loaded is a **mode
adapter**: it tells you who satisfies each gate. This file is mandatory
reading at Phase 0 — the adapter configures it, never replaces it.

## Terminal taxonomy (the only legal endings)

`NO_CHANGE_REQUIRED` · `NAMED_BLOCKER` (ambiguity, missing oracle,
truth conflict, scope violation, spec change required) ·
`PR_READY_AWAITING_HUMAN`. A run never claims MERGED — merging is the
human's act, observed by monitors, never performed or reported as done
by the run.

## Phase 0 — Preflight

Read the adapter's gate-provider table. Verify authority: the spec is
`status: ratified` and **protected main is the effective truth**
(frontmatter is identity/lifecycle metadata, never a competing approval
record). If the ticket pins `@ commit <SHA>`, compare with the current base
**by relevance, not raw inequality**: none of the ticket's pointed IDs
(or their sources/non-goals) changed → `SPEC_REBASED_NO_RELEVANT_CHANGE`
(note it, proceed); a pointed BR/AC/CTR/non-goal changed →
`SPEC_STALE` → NAMED_BLOCKER; unclassifiable → NAMED_BLOCKER for the
human. Confirm the claim is yours.

## Phase 1 — Proven delta

Before any plan: `expected` (from spec/ticket) vs `observed` (from the
code, with one piece of evidence — a command and its real output) →
`gap`. **No gap → NO_CHANGE_CANDIDATE**: assemble the no-change
evidence target — expected, observed, authority IDs, commands +
outputs, searched seams, environmental limits, and a classification
(`ALREADY_SATISFIED | STALE_REQUEST | WRONG_SYSTEM | UNVERIFIABLE`) —
and route it to the mode's review as an **evidence target** (Phase 8).
Only a corroborating report makes it **NO_CHANGE_REQUIRED**; a broken
claim is a finding or a NAMED_BLOCKER. Never manufacture a cosmetic
diff — empty diff + CHANGE_REQUIRED is the inconsistency, not empty
diff itself.

## Phase 2 — Understand + ambiguity

Read the full context chain (root context file → capability context →
spec sections the criteria point at → the ticket). Ambiguity about
behavior, criteria, or design intent goes to the adapter's ambiguity
provider; **if the provider is "abort", it is a NAMED_BLOCKER — never
a guess.**

## Phase 3 — Plan + scope

Produce the plan: criteria covered (by ID), files touched, test
scenarios, risks. Compute the **APPROVAL-FINGERPRINT** (`spec-anchored build-approval`,
which refuses an incomplete or cyclic bundle): sha256 over the canonical
JSON of the **approval bundle** — ticket ref + body hash, base SHA,
spec entrypoint + pinned commit, plan-body hash (canonical bytes:
body only, UTF-8, LF-normalized, trailing whitespace stripped),
scope-manifest hash, semantic-amendment hash or null. The posted
plan names the bundle and the comment id it hashes; **any change to
plan, scope, ticket pin, base, or amendment is a new fingerprint
needing a new approval** — `approved <fingerprint>` identifies
exactly this work, nothing adjacent.
The adapter's plan provider approves **that fingerprint** — an edited
plan is a new fingerprint and needs a new approval. Scope has three
layers: the ticket's **semantic scope** (IDs, non-goals), the
launcher-issued **policy profile** (the floor the run cannot raise —
`spec-anchored validate-scope` refuses to judge without `--profile`),
and the plan's **mechanical scope manifest**
(`references/scope-manifest-schema.md` — allowed/denied paths,
permissions), materialized here as a **proposal that must be a subset
of the profile** and approved with the fingerprint. Any expansion is a
new manifest, a new fingerprint, and a new approval — never a field
inside the approved object.

## Phase 4 — Implement

Work the plan in reviewable chunks on the typed branch. Verification
commands come from the repo's **declared interface**
(`check-<capability>` in the loop; `check` full; `golden` where a spec
applies) — never improvise invocations. The truth layer (`specs/**`,
golden, baseline) is read-only **by default**, per the mode's
**truth-change policy**: *supervised* = gated-materialization — after
an explicit in-session semantic-amendment gate (affected IDs, old →
proposed meaning, rationale, verification change), the adapter MAY
materialize on this branch, only on spec paths the scope manifest
authorizes; the protected-main PR merge ratifies. *Orchestrated and
unattended* = proposal-only: `SPEC_CHANGE_REQUIRED` (amendment
proposal — affected IDs, conflict, proposed change) and stop. Never a
silent edit; never normalize intent to match code. Red-green where a criterion lacks a
test: write the failing test first, watch it fail, then make it pass.

## Phase 5 — Verify

Done means: every pointed criterion verified by **its declared
verification method** — test by default; static check, contract check,
schema validation, benchmark, inspection, runtime observation, or
domain approval where the truth type demands it — with the real output
shown; full suite green; UI-facing criteria
carry browser evidence where the repo declares the instrument
(explored is not verified — the flow lands as a deterministic spec).

## Phase 6 — Durable sync

Lessons (terse, surprise-encounter bar), docs, proposals (context-file
additions are propose-only), backlog status. All durable artifacts
finish HERE, before the candidate seals.

## Phase 7 — Final candidate + seal

Re-run the full suite on the final tree. Freeze base/head SHAs. **Any
durable edit after this point revokes the seal and returns to this
phase** — no PR ships a changeset the review didn't see.

## Phase 8 — Review

Per the adapter: the supervised adapter dispatches the fresh-context
reviewer (fresh-context and decorrelated — the only non-author gate before the human); the
orchestrated adapter runs three self-checks with no authority (the
orchestrator's lens pass on the PR is the judge); the unattended
adapter dispatches the reviewer. Findings are fixed root-cause; fixes
re-seal (Phase 7). The review takes two target kinds: a **diff** (the
normal case) and a **no-change evidence target** — the reviewer
corroborates or breaks the no-op claim (wrong seam, missed
counterexample, unverifiable environment → not a no-op).

## Phase 9 — Deliver

Open the PR on the shared template (Approved plan / fingerprint
included), linking the issue. Comment the PR URL + outcome on the
issue — that comment plus the PR are the completion signal. Terminal:
`PR_READY_AWAITING_HUMAN`. The structured result is validated by
`spec-anchored validate-result` **outside the transcript** — an
illegal terminal, a missing approval fingerprint, an uncorroborated
no-change, or any merge claim fails the run. Park per the adapter.

## Structured logging

`.claude/logs/<skill>-<timestamp>.md` (fuller templates ship in each
adapter's `references/`): run id, issue, branch, plan
fingerprint, per-phase outcomes, evidence commands with exit codes,
terminal state, Cost where visible. The log is evidence for humans;
the PR is the record of the work.

## Common rationalizations (all invalid)

"The test is probably fine" (run it). "This criterion is implied"
(point at the ID or it doesn't exist). "The spec must have meant"
(NAMED_BLOCKER). "I'll fix the failing unrelated test later" (CI must
be green — fix it or name it). "A small extra improvement while I'm
here" (scope gate). "The cast is fine, I know the type" (fix the
type). "Done, just needs polish" (done = Phase 5's bar, nothing less).

## Critical rules

Typed branch always; never `--no-verify`; never merge; truth-layer
writes only per the mode's truth-change policy (Phase 4); never resolve your own ambiguity; claims released or
resolved — never dangling; evidence shown, not narrated.

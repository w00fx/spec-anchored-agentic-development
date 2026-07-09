---
description: Break a capability spec (or the shaping conversation that produced it, or a parent issue) into tracer-bullet tickets — vertical slices anchored on the spec's numbered acceptance criteria, each declaring its blocking edges. Quizzes the human on the breakdown, then publishes to a local tickets.md or to GitHub Issues with real blocking links.
argument-hint: [spec path | parent issue | default: this session's shaping]
---

Break the work into **tracer-bullet tickets** — vertical slices, each
declaring the tickets that **block** it — and publish only after the
human approves the breakdown.

## 1. Gather context

Work from whatever is already in the conversation (a `/shape` session
that just produced a spec is the common case). If the argument is a
spec path, read it in full; if it is an issue number or URL, fetch its
full body and comments.

**Gate: the spec must be committed before any ticket references it** —
the spec is the first commit. If the spec exists only in this
conversation, stop and commit it first (human-approved, as always for
spec content). Tickets point at `specs/<capability>/…` at a real path
in a real commit.

## 2. Explore the codebase

If you have not already explored the codebase, do so to understand the
current state of the code. Ticket titles and descriptions use the
**capability language** (the spec's glossary — canonical terms; banned
synonyms avoided) and respect the ADRs in `architecture/decisions/`.

Look for opportunities to **prefactor**: "make the change easy, then
make the easy change." Prefactoring, when needed, comes first — its
own ticket(s), blocking the slices they enable.

## 3. Draft vertical slices

- Each slice cuts a narrow but COMPLETE path through every layer
  (schema → logic → surface → tests) — vertical, NOT a horizontal
  slice of one layer. Horizontal slices produce nothing a `/goal`
  condition can verify.
- **Each slice anchors on 1-4 of the spec's numbered acceptance
  criteria — pointing at the items, never copying them.** The spec's
  numbering is the addressing scheme; a restated one-liner for
  readability is fine, but the pointer is what is load-bearing.
- A completed slice is demoable or verifiable on its own, and leaves
  the system green: a mergeable PR, no broken intermediate state.
- Sized to fit one fresh run: a 30-40-turn supervised session, a
  projected diff under ~400 changed lines. If it doesn't fit, split
  before the run, not after.
- **Sequence by risk:** prefactoring first; then, for a NEW capability
  with contracts, the **walking skeleton** (the thinnest end-to-end
  slice) — integration risk is the class review catches worst; then
  the ambiguous / load-bearing criteria early (they are the ones that
  invalidate later slices); the mechanical last.
- Give each ticket its **blocking edges** — the tickets that must
  complete before it can start. A ticket with no blockers can start
  immediately.

**Wide refactors are the exception to vertical slicing.** A wide
refactor is one mechanical change — rename a column, retype a shared
symbol — whose blast radius fans across the whole codebase, so no
vertical slice can land green. Don't force it into a tracer bullet;
sequence it as **expand–contract**: *expand* (add the new form beside
the old, nothing breaks) → *migrate* the call sites in batches sized
by blast radius (per package, per directory), each batch its own
ticket blocked by the expand, CI green batch to batch because the old
form still exists → *contract* (delete the old form once no caller
remains, blocked by every migrate batch). When even the batches can't
stay green alone, keep the sequence but let them share an
**integration branch** that all block a final integrate-and-verify
ticket — green is promised only there.

## 4. Quiz the human — nothing publishes before approval

Present the proposed breakdown as a numbered list. For each ticket:

- **Title** — short, in the capability language
- **Blocked by** — which tickets (if any) must complete first
- **What it delivers** — the end-to-end behaviour, plus which spec
  criteria it covers

Ask:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct — does each ticket only depend on
  tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the human approves. The sizing defaults above (1-4
criteria, ~400 lines) are starting points the quiz calibrates — not
law.

## 5. Publish to the configured destination

Publish the approved tickets, **blockers first — so each ticket's
blocking edges reference real identifiers.** Two destinations, same
tickets; only the shape of the edges changes:

- **Local `tickets.md`** (solo / sequential): one file in the repo
  root, all tickets in dependency order, each "Blocked by" listing
  titles. Open the file with a one-line summary of what these tickets
  build, the source spec reference, and the frontier rule.
- **GitHub Issues** (parallel / the autonomous route): one issue per
  ticket, in dependency order; native blocking / sub-issue links where
  the tracker has them, otherwise "Blocked by: #N" in the body. Apply
  the project's label schema (`stage:` / `area:` / type / priority).
  The tickets are agent-grabbable by construction — but apply
  `auto-implement` ONLY per the narrow-start allowlist: the autonomous
  route is opt-in per class, never the default.

Do NOT close or modify any parent issue.

## Ticket template

```markdown
## <Title, in the capability language>

**Spec:** specs/<capability>/<capability>.md — criteria <N-M>

**What to build:** the end-to-end behaviour this ticket makes work,
from the user's perspective — not a layer-by-layer implementation list.

**Acceptance criteria:** spec items <N-M>, one readable line each,
pointing at the spec — the spec text is the truth.

**Blocked by:** #<id> <title>, … — or "None — can start immediately".
```

Avoid specific file paths or code snippets in tickets — they go stale
fast. Exception: a prototype snippet that encodes a decision more
precisely than prose can (a state machine, a schema, a type shape) —
inline it, note it came from a prototype, and trim to the
decision-rich parts.

## After publishing

Work the **frontier** — any ticket whose blockers are all done — one
ticket per fresh session: locally via the supervised `/goal` recipes,
or through the autonomous route when the narrow-start conditions hold.
Parallel work = parallel sessions (worktrees) on frontier tickets with
disjoint scopes.

---

Ticket mechanics (tracer bullets, blocking edges, the frontier,
expand–contract, the approval quiz) adapted from Matt Pocock's
`to-tickets` skill. The spec anchoring, run-budget sizing, risk
sequencing, and autonomous gating are this system's.

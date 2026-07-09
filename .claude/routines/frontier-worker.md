# Frontier worker — canonical Routine prompt

The scheduled sibling of the `auto-implement` label trigger (GUIDELINE
Part 3): same engine (`/goal`), same condition shape, but instead of
reacting to a label event it scans the backlog frontier on a schedule and
works exactly one issue per run. Wire it as a scheduled Claude Code
Routine running headless; the platform puts the session on a dedicated
`claude/`-prefixed work branch — the skill stays on it.

## The prompt

```text
Scan the frontier and work exactly one issue end to end.

1. Frontier scan: list open issues labeled `auto-implement` that are
   NOT labeled `in-flight` and whose blocking issues (the "Blocked by"
   references in the issue body) are all closed. If none qualify, say
   so and stop — an empty frontier is a legitimate end, not a failure.

2. Claim: pick the eligible issue with the highest priority label
   (then the oldest), and apply the `in-flight` label BEFORE any other
   work — the claim is what lets several workers run in parallel
   without collisions.

3. Work the claimed issue:

/goal Implement issue #<N> following the implement-backlog skill end
to end. DONE only when, all of it visible in the conversation: every
acceptance criterion verified by a passing test with the runner's
real output; full suite green, tests anchored on the spec's criteria;
lint, typecheck and coverage at threshold; the reviewer ran on the
final diff with zero [BLOCKER]; the work branch is pushed and a PR is
open, its description on the shared template (Approved plan
included), CI green to completion. OR DONE WITH A NAMED BLOCKER when
the skill aborts, comments on the issue and applies its label
(needs-refinement / scope-expansion-needed / qa-blocked /
review-blocked / wrong-skill / needs-human-implementation).
Constraints: no silent scope expansion; a spec update marks the PR
requires_human_approval; never declare done with a red check.
Hard cap: 40 turns.

4. Release the claim: if the run ended in a named-blocker abort,
   remove `in-flight` (the blocker label stays — the issue leaves the
   frontier until a human resolves it). If the PR opened clean, leave
   `in-flight` on; it comes off when the PR lands.
```

## Notes

- **One issue per run, by design.** The frontier's blocking edges
  (`/spec-to-tickets` declares them) are what make parallel workers
  safe; the `in-flight` claim is what makes them cheap.
- **The Routine trusts the label; it does not re-triage.** The
  narrow-start allowlist (GUIDELINE Part 5) still gates what carries
  `auto-implement` in the first place.
- The abort labels and their triggers live in the skill
  (`implement-backlog`); this prompt only mirrors them in the
  condition, as the `/goal` contract requires.

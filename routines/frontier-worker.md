# frontier-worker — canonical Routine prompt

**What this is.** The scheduled sibling of the label-triggered GitHub
Action: a Claude Code Routine that scans the autonomous backlog's
frontier, claims exactly one issue, and drives `implement-backlog`
through a headless `/goal`. The skill is the workflow; this file is the
trigger's instructions — versioned in the repo so the orchestration
rides the same PR rails as everything else.

**Wiring (one-time).** Create a Routine with:

- **Prompt:** `Follow the instructions in
  .claude/routines/frontier-worker.md.`
- **Trigger:** Scheduled (hourly is a sane start) — or the GitHub
  issue-label event if the platform's event filter supports it. Verify
  against the current Routines docs when wiring (research preview —
  details move).
- **Repository:** this one.

Platform properties this design leans on: each run is a fresh,
isolated session (the fresh-context discipline by construction);
pushes go only to `claude/`-prefixed branches by default (PR-only is a
platform boundary, not an instruction); and the plan's daily run caps
act as the narrow-start governor.

**One label convention this file introduces:** `in-flight` — "an
autonomous run currently owns this issue." Applied at claim; removed
on a named-blocker abort (ownership released back to humans); left in
place on success — the issue really is in flight until the PR merges
and closes it.

## Instructions

1. **Scan the frontier.** List open issues labeled `auto-implement`
   that (a) do NOT carry `in-flight`, and (b) whose "Blocked by"
   references are all closed. If none qualify, say so and stop
   cleanly — an empty scan is a successful run.
2. **Claim exactly one:** highest priority first, then oldest. Apply
   the `in-flight` label and comment: `Claimed by frontier-worker
   routine — <date>.` The claim is what lets parallel runs coexist
   without double-picking.
3. **Drive the skill** — issue the goal with the claimed number
   interpolated:

```text
/goal Implement issue #<N> with the implement-backlog skill.
Done when ONE of the following holds:

A. Landed-shape: a PR is open implementing every acceptance criterion
   issue #<N> points at (or carries), each verified by a passing
   test; every reference-value row those criteria touch is covered,
   when the issue points at a spec; nothing outside the spec's
   Non-goals, when one applies; the reviewer reported zero [BLOCKER];
   CI has settled green (to completion, not first green); the run log
   is written and the PR description follows
   references/pr-template.md, Approved plan included; a comment with
   the PR link is posted on issue #<N> — the skill's own Phase 7
   terminal: PR green, reviewed, nothing outstanding.

B. Named blocker: the run ended on one of the skill's abort protocols
   — the abort comment posted on issue #<N>, the corresponding label
   applied (the skill's phases define which), the log written, and
   the `in-flight` label removed.

Hard cap: 40 turns.
```

One claim, one run, one fresh session per issue — never work a second
issue in the same run.

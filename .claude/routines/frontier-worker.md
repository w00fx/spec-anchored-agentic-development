# frontier-worker — canonical Routine prompt

**What this is.** The scheduled sibling of the label-triggered GitHub
Action: a Claude Code Routine that scans the autonomous backlog's
frontier, claims exactly one issue, and drives `implement-backlog`
through a direct `/implement-backlog` first message. The skill is the workflow; this file is the
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
and closes it, or until a **corroborated NO_CHANGE_REQUIRED** resolves
it without a PR.

## Instructions

1. **Scan the frontier.** List open issues labeled `auto-implement`
   that (a) do NOT carry `in-flight`, and (b) whose "Blocked by"
   references are all **resolved per the shared semantics** —
   closed-as-`completed`, a corroborated no-change, or `duplicate`
   following the canonical issue; `not_planned` is a human graph
   decision, never auto-satisfied (same rules as the orchestrator).
   If none qualify, say so and stop
   cleanly — an empty scan is a successful run.
2. **Claim exactly one:** highest priority first, then oldest. Apply
   the `in-flight` label and comment a structured claim:
   `Claimed by frontier-worker — run:<id> claimed_at:<ts>
   expires_at:<ts+2h>`. **The label is a signal, not a mutex**: after
   applying, re-read the issue — if another claim comment beat yours,
   release and move on (compare-and-verify). A claim past
   `expires_at` with no PR and no heartbeat is stale: any run may
   release it (comment the release). True atomicity needs external
   coordination (a concurrency key per issue in the scheduler/CI) —
   wire it before running parallel schedulers.
3. **Invoke the skill directly** — `/implement-backlog issue #<N>`
   as the start of the working turn (a user-only skill loads by
   invocation, never by being named inside a goal condition). The
   DONE contract below is the launcher's terminal checklist,
   validated outside the transcript:

```text
FIRST USER MESSAGE of the child worker session:
/implement-backlog issue #<N>

The launcher — not a goal condition — validates the structured
terminal outside the transcript. DONE when ONE holds:

A. PR_READY_AWAITING_HUMAN — a PR is open on the shared template,
   every pointed criterion evidence-verified. Monitoring (CI flips,
   late review, the merge) belongs to the external monitor, never to
   the run.
B. NAMED_BLOCKER — the skill aborted, commented the specific blocker
   on the issue, applied the label, released the claim.
C. NO_CHANGE_CANDIDATE → corroborated NO_CHANGE_REQUIRED — evidence
   target posted, General Code Reviewer no-change corroboration recorded, claim released,
   no PR by design; the launcher applies the resolution policy.
```

One claim, one run, one fresh session per issue — never work a second
issue in the same run.

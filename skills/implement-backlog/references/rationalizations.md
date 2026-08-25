# Common rationalizations — implement-backlog runs

The shortcuts that turn an autonomous run into a discarded PR or a
human's cleanup. In autonomous mode there's no human to catch these
mid-run — the machine has to.

| Rationalization | Reality |
|-----------------|---------|
| "The tests pass, so it's done" | Tests written alongside the code confirm the implementation, not the spec. Green proves "works as I tested," not "works as specified." |
| "The approach is obvious, skip the plan review" | The plan-review subagent is the only gate before code in autonomous mode. Obvious-and-unreviewed is exactly how the wrong approach ships a PR that gets discarded. |
| "I'll run the full checks at the end" | Run lint + typecheck + touched tests every chunk. End-only batching turns one red bar into a bisecting session with no human watching. |
| "This file is just outside scope, I'll edit it anyway" | Silent scope growth has no human to catch it here. Abort with a comment — that's the rule, not a suggestion. |
| "The plan is mostly right, I'll just adapt as I go" | An approved plan the code no longer follows is fiction. A failed load-bearing decision goes back through the plan-review gate as a delta — never improvised around. |
| "The PR is open, so I'll stay on and watch it through" | The run's terminal is `PR_READY_AWAITING_HUMAN`, and it ends there. CI flips, late review comments and the merge itself belong to the external monitor and to the human who merges. Working past the terminal is outside the protocol, and reporting the merge claims an act the run never performed. |
| "CI will catch it" | CI catching it means a red PR waiting on a human. Catch it locally first, in Phase 4. |
| "The flaky check isn't really my problem" | A red check is unresolved work. Fix it, or stop and name the blocker — never retry-until-green or mark done around it. |

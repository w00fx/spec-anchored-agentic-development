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
| "The PR is open, the run is done" | Open ≠ landed. Monitor CI to completion, late comments, and conflicts until it merges clean or you name a blocker. |
| "CI will catch it" | CI catching it means a red PR waiting on a human. Catch it locally first, in Phase 4. |
| "The flaky check isn't really my problem" | A red check is unresolved work. Fix it, or stop and name the blocker — never retry-until-green or mark done around it. |

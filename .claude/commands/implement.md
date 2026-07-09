---
description: Implement a feature or increment locally, human-driven (implement-feature)
argument-hint: [spec path | issue | description]
---

Run the implement-feature skill for the work in the argument (a spec path,
an issue number, or a description). Follow ALL its phases and human gates —
do not skip the confirmations at Phase 1 (understanding), Phase 1.5
(ambiguities), and Phase 2 (plan). The reviewer agent runs at Phase 5.

This is the interactive, human-driven flow: stop at each gate and wait for
me. Wrapping this in a supervised /goal is fine and recommended for work
with acceptance criteria (invocation recipes: the guideline's
"Supervised /goal" section) — interactively, gates pause the turn and
my answers enter the transcript. What is NOT allowed is headless/autonomous
execution (claude -p): there, no one answers and the gates are silently
overrun. Headless runs are the separate implement-backlog skill.

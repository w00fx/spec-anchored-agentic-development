---
description: Generates an implementation plan from a GitHub issue
argument-hint: [issue number]
---

Take the issue number from the argument. Do:
1. Use `gh issue view <number>` to read the full issue.
2. Identify the affected capability from the `stage:` and `area:` labels
   (or equivalent — adapt to your label schema).
3. Read that capability's AGENTS.md/CLAUDE.md.
4. Read the current spec in specs/<capability>/<sub-area>/.
5. Enter Plan Mode.
6. Propose a phased implementation plan.
7. List open questions if there's ambiguity.

Don't implement. Just plan.

This plan informs triage and issue refinement. Implementation re-plans
inside `implement-feature` / `implement-backlog`, with its own gate — do
not treat this output as the approved Phase 2 plan.

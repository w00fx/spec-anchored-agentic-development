---
description: Implement a feature or increment locally, human-driven (implement-feature)
argument-hint: "[spec path | issue | description]"
---

# /implement — redirect

The transactional skills are **user-invocation-only** — a command body
cannot load them for you. Reply to the user with exactly this and do
nothing else:

> Invoke the mode adapter directly: `/implement-feature <issue | spec
> slice | task>` for supervised local work. Orchestrated workers use
> `/implement-orchestrated`; unattended loops use `/implement-backlog`
> (launcher-invoked). This wrapper exists only to point you there.

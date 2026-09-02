---
name: implement-orchestrated
disable-model-invocation: true
description: >-
  EXPLICIT INVOCATION ONLY — one orchestrator-owned issue, worktree and PR.
  Uses GitHub-mediated gates plus the authoring General Code Reviewer and
  Mutation Hardener. Invoked as the worker's FIRST MESSAGE; never auto-trigger.
---

# implement-orchestrated — orchestrator-owned Owner adapter

**First action: read `.agents/protocols/implementation-protocol.md`.** The parent
worker is the Owner. The orchestrator schedules and monitors; it never authors
the code or silently integrates subagent work.

## Invocation

```text
implement-orchestrated issue #<N> --mode assisted|autonomous
```

The issue pins the effective spec and stable IDs. `--mode` is launcher policy,
not inferred from prose.

## Gate and pass providers

| Protocol need | assisted | autonomous |
|---|---|---|
| Ambiguity | Comment exact question/evidence, label, release claim, `NAMED_BLOCKER` | Same |
| Plan | Post plan + exact `APPROVAL-FINGERPRINT`; edit nothing until human replies `approved <fingerprint>` | Owner may proceed only for a qualified class whose ticket/spec/policy mechanically determine the plan; any load-bearing decision blocks. No plan-review agent |
| Spec change | `SPEC_CHANGE_REQUIRED`, proposal-only, release claim | Same |
| Scope/dependency/schema/data/external-action expansion | Blocker | Blocker |
| General code hardening | Dispatch only `general-code-reviewer`; Owner inspects and integrates accepted local commit | Same |
| Mutation hardening | Dispatch only `mutation-hardener`; Owner inspects and integrates accepted local commit | Same |
| External specialized reviews | Orchestrator/pipeline may run them after PR; they are not internal agents | Same |
| Delivery | No-change: post corroborated evidence terminal. Code: open PR, post URL/outcome, park for re-engagement | Same |

## Owner handoff rule

For both internal agents, record input/output SHA, changed paths, rationale,
commands/results and Owner disposition. Reject any truth, scope, gate or
permission change. Any Owner correction after mutation hardening reruns both
internal passes.

## Engine parity

Each worker invokes `implement-orchestrated` using its runtime's native explicit-skill syntax. The launcher refuses a runtime whose actual skill/agent installation is absent.

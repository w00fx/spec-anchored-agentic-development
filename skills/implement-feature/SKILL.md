---
name: implement-feature
disable-model-invocation: true
description: >-
  EXPLICIT INVOCATION ONLY — run via /implement-feature or when the user
  names this skill. Never auto-trigger on general coding requests.
  Supervised-local adapter of the shared implementation protocol: code
  work from existing ratified specs, issues, or backlog items, with the
  human in the session satisfying every gate.
---

# implement-feature — supervised-local adapter

**Phase 0 first action: read `.claude/protocols/implementation-protocol.md`
NOW.** (Installed at user level, the same file sits under your `~/.claude`;
the Codex port reads it from `agent-system/protocols/`. If none of the three
resolves, that is a NAMED_BLOCKER — never run the machine from memory.) It is the state machine — phases, terminals, invariants,
logging, rationalizations. This file only configures who satisfies
each gate. Treat the protocol as mandatory, not as an optional
reference.

## Mode identity

The local, human-driven adapter, invoked **directly** as `/implement-feature` (or by name); `/implement` is a redirect that only points here. Runs
interactively — plain. (A `/goal` wrapper is optional and only as a
**separately verified composition**: the skill loads by your explicit
invocation, never by being named inside a condition.) It must NEVER run under headless `/goal`
(`claude -p`) — no one answers there. Headless work is
`implement-backlog`; orchestrated workers are `implement-orchestrated`
(one ticket, one PR — never reroute them here or to backlog).

## Scenarios

1. **New capability from its ratified spec** (spec creation itself is
   human-led — out of scope here).
2. **Feature within an existing capability.**
3. **Increment**: bugfix, tech-debt, rule adjustment, reference-data
   update proposal, feature-within-scope backlog item.

## Gate providers (this mode)

| Gate | Provider |
|---|---|
| Ambiguity (Phase 2) | the human, in-session (AskUserQuestion) |
| Plan approval (Phase 3) | the human, in-session (ExitPlanMode); fingerprint noted in the log |
| Spec change (Phase 4) | **semantic-amendment gate in-session** (affected IDs, old → proposed meaning, rationale, verification change); on explicit human approval the skill MAY materialize the amendment on this branch — the PR review ratifies it (`requires_human_approval`). Orchestrated and unattended adapters stay proposal-only |
| Scope expansion | the human, in-session |
| Review (Phase 8) | dispatch the `reviewer` agent in isolated context (it did not write this code; the agent is model-pinned to **Opus at max effort** — the judge never runs on a cheaper brain). Confirm a non-empty diff **or a NO_CHANGE_CANDIDATE evidence target** before dispatch (the no-op claim gets corroborated, never self-declared). Default: one reviewer, all applicable lenses; diffs beyond ~400 lines: parallel single-lens dispatches. Findings are report-only; fix root-cause; re-seal |
| Delivery (Phase 9) | PR opened; the human merges. Park = end the session normally |

## Target model notes (adapter-level, volatile)

Tuned for Claude Opus 4.8 **and Opus 5** in Claude Code (audited
against the Opus 5 prompting guide). ULTRATHINK keywords are the 4.x
max-thinking lever and degrade harmlessly on 5, where `effort=max` is
session-level per the operator's doctrine. Plan mode and the gate
tools are this adapter's mechanism; other harnesses supply their own
via their adapter.

## Where the repo speaks

Verification commands, browser-evidence instruments, and golden
invocations come from the repo's declared interface and context files
— this adapter demands the classes; the repo names the instruments.

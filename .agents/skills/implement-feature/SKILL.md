---
name: implement-feature
disable-model-invocation: true
description: >-
  EXPLICIT INVOCATION ONLY — invoke `implement-feature` with the runtime's native explicit-skill syntax. Supervised implementation of one issue/spec slice with
  human gates, an Owner implementation agent, an authoring General Code
  Reviewer, an authoring Mutation Hardener, and delivery for external review.
---

# implement-feature — supervised Owner adapter

**First action: read `.agents/protocols/implementation-protocol.md`.** It is the
complete state machine. This adapter only names the providers for supervised
work.

## Mode identity

Invoke `implement-feature <issue | spec slice | task>` using the runtime's native explicit-skill syntax. The human
is present in-session. Never launch this skill headlessly; use
`implement-backlog` for unattended work and `implement-orchestrated` for an
orchestrator-owned worker.

The parent agent is the **Owner**. The Owner alone talks to the human, owns the
branch/run terminal, and decides whether to integrate commits returned by the
two internal agents.

## Gate and pass providers

| Protocol need | Provider in this mode |
|---|---|
| Ambiguity / unauthorized assumption | Human in-session after repository research; present numbered options and a recommendation |
| Plan, scope, evidence, mutation/fuzz applicability | Human approval of the exact `APPROVAL-FINGERPRINT` |
| Semantic spec amendment | Human in-session; affected IDs, old → proposed meaning, rationale and verification delta; PR merge ratifies |
| Scope/dependency/schema/data/external-action expansion | Human approval of a new scope + fingerprint |
| General code hardening (Phase 7) | Dispatch only `general-code-reviewer`. It edits in an isolated worktree and returns a local commit + full change report. Owner inspects and accepts/rejects before integration |
| Mutation hardening (Phase 8) | Dispatch only `mutation-hardener`. It may edit production/tests to reach the 100% target contract and returns a local commit + mutation report. Owner inspects and accepts/rejects before integration |
| External specialized reviews | Outside this skill. The PR/pipeline/orchestrator may run spec, conformance, security, performance, compliance, architecture, or independent code review |
| Delivery | PR opened; human reviews/merges. Terminal `PR_READY_AWAITING_HUMAN` |

## Agent call graph

```text
Owner implementation
→ deterministic baseline
→ general-code-reviewer [internal authoring loop]
→ Owner diff review + integration
→ mutation-hardener [internal authoring loop to 100%]
→ Owner diff review + integration
→ final deterministic verification
→ PR / external review pipeline
```

There is no internal reviewer router, lens fan-out, plan-review agent,
conformance agent, or constitution agent.

## No-change

For `NO_CHANGE_CANDIDATE`, dispatch `general-code-reviewer` in no-change mode to
corroborate or break the evidence target. Do not call `mutation-hardener` when
there is no eligible code target.

## Model and repository interface

Run both internal agents with the same effective model as the Owner/parent worker
and record the observed model/effort identity. Agent contracts do not pin a model;
they require `effort=max`. If the runtime cannot honor or disclose `max`, block
instead of switching models or accepting a downgrade. Verification, mutation,
fuzz, coverage, complexity, and duplication
commands come from the repository's pinned interface and `.agents/rules/testing.md`,
never from an improvised tool choice.

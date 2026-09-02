---
name: implement-backlog
disable-model-invocation: true
description: >-
  EXPLICIT INVOCATION ONLY — unattended implementation adapter for one qualified
  increment issue. Mechanical-or-abort gates, one Owner worker, the authoring
  General Code Reviewer and Mutation Hardener, and a PR awaiting external/human
  review. Never auto-trigger; never use for architecture work.
---

# implement-backlog — unattended Owner adapter

**First action: read `.agents/protocols/implementation-protocol.md`.** No human
answers mid-run. The parent worker is the Owner and must inspect every returned
subagent diff before integrating it.

## Mode identity

Invoke `implement-backlog issue #<N>` with the runtime's native explicit-skill syntax as the launcher's first user message. One qualified issue, one worktree/branch, at most one PR. New
capabilities, semantic invention, broad architecture, and truth/oracle changes
are out of scope.

## Gate and pass providers

| Protocol need | Provider in this mode |
|---|---|
| Ambiguity / load-bearing decision | `NAMED_BLOCKER` with exact question/evidence; never guess |
| Plan | Owner writes a plan only when the qualified ticket, effective spec, repository policy and deterministic oracle fully determine it. Any unpinned decision aborts; there is no plan-review agent |
| Spec change | `SPEC_CHANGE_REQUIRED`; proposal/comment only; never edit semantics |
| Scope/dependency/schema/data/external-action expansion | Blocker, always |
| General code hardening | `general-code-reviewer`; Owner inspects exact commit/report, scope and semantics before integrating |
| Mutation hardening | `mutation-hardener`; Owner inspects exact commit/report and requires the 100% eligible-target contract |
| External specialized reviews | Outside this run; separate monitor/pipeline/human owns them |
| Delivery | Open PR, post link/outcome, terminal `PR_READY_AWAITING_HUMAN`; never monitor or claim merge |

If either authoring agent returns a semantic/scope/oracle/dependency decision
that the unattended policy cannot authorize, abort upstream. A subagent commit
is never auto-cherry-picked without the Owner's recorded inspection.

## Loop discipline

One issue per run. Release the claim on any blocker. Stop repeated
non-progressing attempts and preserve commands, outputs, agent handoffs, Owner
dispositions, and cost in the log.

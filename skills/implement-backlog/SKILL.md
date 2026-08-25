---
name: implement-backlog
disable-model-invocation: true
description: >-
  EXPLICIT INVOCATION ONLY — run via /implement-backlog or when the
  user names this skill. Unattended adapter of the shared
  implementation protocol: autonomous loop over increment issues
  (bugfix, tech-debt, rule adjustment, reference-data update
  proposals, feature-within-scope). New capabilities and large
  features are out of scope — human-led. Never auto-trigger.
---

# implement-backlog — unattended adapter

**Phase 0 first action: read `.claude/protocols/implementation-protocol.md`
NOW.** (Installed at user level, the same file sits under your `~/.claude`;
the Codex port reads it from `agent-system/protocols/`. If none of the three
resolves, that is a NAMED_BLOCKER — never run the machine from memory.) It is the state machine; this file configures the gates for a
headless run — no human answers mid-flight, so every gate either has a
mechanical provider or aborts.

## Mode identity

The autonomous, headless entry point — `/implement-backlog` invoked
**directly**: by you, by a launcher's `claude -p`, or as the frontier
routine's child-session first message. Scope: increment work only.
Architectural decisions are never originated here; reference-data
changes are **proposals** (the value change carries the human's
signature per the truth layer — the run prepares evidence and the PR;
the human signs).

## Gate providers (this mode)

| Gate | Provider |
|---|---|
| Ambiguity | ABORT: NAMED_BLOCKER on the issue (label + comment with the specific question); never a guess |
| Plan | dispatch the `plan-review` lens (fresh context, report-only); a [BLOCKER] finding aborts; fingerprint logged |
| Spec change | `SPEC_CHANGE_REQUIRED` — amendment proposal on the issue; abort. This adapter never edits semantics |
| Scope expansion | blocker, always |
| Review (Phase 8) | dispatch the `reviewer` agent (all applicable lenses; Opus at max effort; report-only). Non-empty diff, or a NO_CHANGE_CANDIDATE routed as an evidence-target review, before dispatch. [BLOCKER]s: fix root-cause, re-seal; twice-failed same-shape → NAMED_BLOCKER |
| Delivery | PR on the shared template; decisions recorded in the log and PR description for human review. Terminal `PR_READY_AWAITING_HUMAN` — the run never monitors or claims the merge; a separate monitor observes it |

## Loop discipline

One issue per iteration, oldest-ready first; claim (`in-flight`) before
work, release on any abort; 2 consecutive failures of the same shape
halt the loop; the log carries per-issue terminals and Cost.

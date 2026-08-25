---
name: implement-orchestrated
disable-model-invocation: true
description: >-
  EXPLICIT INVOCATION ONLY — the orchestrated-worker adapter of the
  shared implementation protocol. Invoked as the FIRST MESSAGE of an
  Orca child worker: /implement-orchestrated issue #<N> --mode
  assisted|autonomous. One ticket, one worktree, one PR. Never
  auto-trigger; never use for local supervised work.
---

# implement-orchestrated — orchestrated-worker adapter

**Phase 0 first action: read `.claude/protocols/implementation-protocol.md`
NOW.** (Installed at user level, the same file sits under your `~/.claude`;
the Codex port reads it from `agent-system/protocols/`. If none of the three
resolves, that is a NAMED_BLOCKER — never run the machine from memory.) It is the state machine; this file configures the gates for a
worker dispatched by `/orchestrate` — an interactive session whose
human gates are satisfied through GitHub, not in-session.

## Invocation contract

The worker's first message IS this command:
`/implement-orchestrated issue #<N> --mode assisted|autonomous`.
The ticket body (inlined in the brief or read via `gh issue view`) is
the work contract: it pins the spec commit and points at criteria IDs.
`--mode` is configuration, decided by the orchestrator's baked-in
policy — never inferred from ticket language.

## Gate providers (this mode)

| Gate | assisted | autonomous |
|---|---|---|
| Ambiguity | comment the question on the issue; label `needs-refinement`, release the claim, STOP (NAMED_BLOCKER) — business/spec truth is never the orchestrator's to answer | same — always a blocker |
| Plan | post plan + `APPROVAL-FINGERPRINT: <sha256 of the canonical approval bundle — plan, scope manifest, ticket/spec/base pins>` as an issue comment; **STOP — edit no files until the human replies `approved <fingerprint>`**; edited plan = new fingerprint = new approval | the quiz-approved ticket pre-approves the **semantic scope**; any load-bearing design decision still gets a fresh-context `plan-review` lens before code (trivial/reversible classes with a strong oracle may skip by declared policy); carry the plan into the PR's Approved-plan section |
| Spec change | `SPEC_CHANGE_REQUIRED`: amendment proposal as an issue comment; label; release; STOP | same |
| Scope expansion | blocker (issue comment + label) | blocker |
| Review (Phase 8) | three **self-checks, no authority** (general hygiene; spec conformance — a test per pointed criterion, values matching; ticket scope vs non-goals). Fix findings; post no verdicts — the orchestrator's fresh-context lens pass on the PR is the judge | same |
| Delivery | `NO_CHANGE_CANDIDATE`: post the evidence target on the issue and stop — the orchestrator dispatches the evidence-target review, and only its corroboration makes the terminal `NO_CHANGE_REQUIRED` (**no PR by design**). Otherwise: PR on the shared template; comment PR URL + outcome on the issue (the completion signal); terminal `PR_READY_AWAITING_HUMAN`; **stay parked for review re-engagement** | same |

## Evidence rules (unchanged from the protocol)

Declared-interface commands only; UI criteria carry browser evidence
(load the repo's declared instrument guide first — e.g.
`agent-browser skills get core --full`, the stub pattern) and land as
deterministic specs; runner output shown, never narrated.

## Engine parity

This adapter ships for both engines: Claude workers invoke
`/implement-orchestrated …`; Codex workers invoke
`$implement-orchestrated …` and require the ported copy under
`.agents/skills/` (per the coexistence adapter). The orchestrator
refuses an engine whose install is absent — a worker running only a
summary brief is not running the protocol.

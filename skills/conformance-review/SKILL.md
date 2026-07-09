---
name: conformance-review
description: >
  Use when the reviewer subagent is reviewing a diff that implements work
  defined by a capability spec or an approved Phase 2 plan. Checks two things: does the diff do what the spec requires, and does the
  diff do what the approved plan said it would. Catches silent drift between
  intent and implementation. Apply on top of general-code-review for any
  spec- or plan-driven change.
---

# Conformance Review

## Overview

**You are the machine that catches the gap between what was promised and what was built — before it becomes a silent divergence nobody notices until the behavior is wrong in production.** General code review asks "is this code good?". Constitution review asks "does it obey the domain rules?". You ask a different question: **"does this do what it was supposed to do?"** — measured against two sources of intent: the spec (the business source of truth) and the approved plan (what the implementer committed to in Phase 2).

A diff can be clean, well-tested, and constitution-compliant, and still implement the wrong thing — a subtly different rule than the spec describes, or a different approach than the plan that was reviewed and approved. That gap is what you find.

## When to Use

- A code-review subagent is reviewing a diff that implements a capability spec or an approved Phase 2 plan.

**Not for:** general correctness/simplicity/tests (use `general-code-review`); constitution/domain-rule violations (use `constitution-compliance-review`); exploratory diffs with no spec or plan behind them.

## Inputs — you run in isolated context

You saw none of the conversation that produced this diff. Source every input yourself, and know which one cannot be sourced:

- **The diff:** from git — this branch's committed work plus uncommitted changes. Read it; never "remember" it.
- **The spec:** a file. Locate it from the touched capability's CLAUDE.md pointer (`specs/<capability>/…`).
- **The approved plan:** not a file — it exists in the caller's conversation, so it must be **pasted into your dispatch prompt** (the plan plus any approved replans/deltas and scope expansions). If it wasn't pasted: review Dimension 1 only, and state in the report that Dimension 2 was not reviewed for lack of the plan. **Never reconstruct the plan from the diff** — a plan inferred from the code always matches the code; that check is circular and always passes.

## Dimension 1 — Diff vs spec

The spec is the business source of truth. Read the relevant capability spec and compare:

- **Behavior described in the spec, not implemented:** every rule, edge case, and acceptance criterion the spec lists has corresponding behavior in the diff. A spec requirement with no implementation is a [BLOCKER].
- **Behavior in the code, not in the spec:** the diff implements a rule or path the spec doesn't describe. Either the spec is incomplete (flag it — it may need an update with `requires_human_approval`) or the code is doing something it shouldn't. Don't let undocumented behavior pass silently.
- **Non-goals violated:** the spec's Non-goals section lists what this capability explicitly does not do. Behavior in the diff that Non-goals exclude is a [BLOCKER] even when well-implemented — it is scope the business ruled out, not a spec gap to backfill.
- **Subtle rule mismatch:** the diff implements *a* version of the rule, but not *the* version the spec specifies — a different threshold, a different rounding boundary, a different edge-case handling. This is the most dangerous case because tests written from the implementation will pass. Trace the actual rule in the code against the actual rule in the spec, value by value — the spec's **reference-value table** (under Acceptance criteria) is the anchor: each row is an input → expected-output pair; verify the code path reproduces every row it touches.
- **Contracts:** if the spec has `contracts/`, the diff's inputs/outputs match the documented schema.

## Dimension 2 — Diff vs approved plan (intent vs implementation)

The Phase 2 plan stated an approach and a committed file scope, reviewed and approved before code. Your baseline is the **latest approved plan** — the original plus any approved replans (delta revisions) and approved scope expansions pasted with it. An approved replan is the new baseline, not a divergence; what you flag is unapproved deviation from that baseline. Compare the diff against it:

- **Approach drift:** the diff took a different approach than the plan described. Maybe the new approach is fine — but it wasn't the one reviewed, so it hasn't been vetted. Flag the divergence so it gets a second look, don't wave it through because "it works."
- **Scope drift:** the diff edits files outside the committed scope (beyond any *approved* scope changes), or skips files the plan said it would touch. In `implement-backlog` this should have aborted; if it reached you, it's a [BLOCKER]. In `implement-feature` it should have been surfaced for human approval.
- **Load-bearing decisions:** the plan pinned certain decisions (where shared state lives, fail-open vs closed, etc.). The diff implements those decisions as stated — not a quietly different choice.
- **Declared, not done:** the plan said it would do X (add a test, update a contract, handle a case); the diff doesn't. A promise in the plan with no corresponding change is a gap.

## How to report findings

For each finding: which **source of intent** it diverges from (spec / plan), **severity** (**[BLOCKER]** a spec requirement unimplemented, a rule mismatch, or scope drift that should have aborted · **[SHOULD]** an approach divergence worth a second look, or a spec that looks incomplete · **[NIT]** a wording or documentation gap), **location** (`file:line` and the spec section or plan step), and the **concrete gap** ("spec §3.2 says round at the half-cent boundary; the code rounds at the cent — line 88"). When the divergence means the spec is wrong rather than the code, say so — that routes to a spec update (`requires_human_approval`), not a code fix.

## Common rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "It works, so it must match the spec" | Working ≠ matching. The code can implement a subtly different rule that passes its own tests. Trace value by value against the spec. |
| "The tests pass, conformance is covered" | Tests written from the implementation pass by construction. They prove the code does what the code does, not what the spec says. |
| "I changed the approach but the outcome is the same" | The new approach wasn't the one reviewed in Phase 2. Same outcome, unvetted path. Flag it for a second look. |
| "It edits one extra file, no big deal" | Scope drift in an autonomous run should have aborted. Silent scope growth is exactly what conformance review exists to catch. |
| "The spec doesn't mention this case, so I handled it my way" | Undocumented behavior is either a spec gap (flag it) or code doing too much. Don't let it pass silently as if the spec covered it. |

## Red flags — STOP

- Approving a diff without **tracing the actual rule in the code against the actual rule in the spec**, value by value, for the rules it touches.
- Approving when a **spec requirement has no corresponding behavior** in the diff.
- Approving **undocumented behavior** as if the spec described it.
- Approving an **approach that diverges from the approved plan** without flagging it for a second look.
- Approving **scope drift** that should have aborted (implement-backlog) or been surfaced (implement-feature).
- Reviewing Dimension 2 against a plan **you inferred from the diff** instead of one pasted into your prompt — circular, always passes.
- Approving behavior the spec's **Non-goals** section excludes.

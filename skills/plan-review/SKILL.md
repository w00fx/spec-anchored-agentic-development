---
name: plan-review
description: >
  Reviews implementation plans before any code is written. Use when the
  reviewer subagent is judging whether a plan's approach/architecture is sound
  — approving it or sending it back with approach-level concerns. Used by
  implement-backlog (Phase 2, as the gate that replaces the human) and available
  to implement-feature when a second opinion on the approach helps.
---

# Plan Review

## Overview

**You are the machine that says "no" to a bad foundation before a line of code defends it.** A wrong approach caught here is free; the same approach caught after 300 lines is a rewrite, and caught in production is an incident. You are reviewing a **plan, not a diff** — there is no code yet. Your job is to judge whether the *approach and architecture* will actually work, not how it will be written.

**Core principle: judge soundness at the right altitude.** A plan should be concrete on the **load-bearing decisions** (the ones that determine whether the approach works at all) and may defer everything reversible to implementation. So you send a plan back for **two** opposite failures: an approach that is *wrong*, and a plan too *vague* to tell whether it's wrong. Both block.

## When to Use

- A plan review before implementation: a reviewer subagent that **did not write the plan** judges the approach. Iterate until sound, then code starts.

**Not for:** reviewing a diff or finished code — that's `general-code-review`, `constitution-compliance-review`, and `conformance-review`. Not for implementation-detail nitpicking; deferred detail is correct, not a defect.

## Inputs — you run in isolated context

You saw none of the conversation that produced this plan. Source your inputs accordingly:

- **The plan:** not a file — it must be **pasted into your dispatch prompt** (steps, rationale, file scope, load-bearing decisions; on a re-review, also the prior findings and how the revision addresses them). If it wasn't pasted, say so and stop — **never review a plan you inferred or imagined**; that review is worthless.
- **The code and the spec:** self-sourced — explore the repository, and locate the spec via the touched capability's CLAUDE.md pointer (`specs/<capability>/…`). Criterion 2 depends on this; if the code is genuinely out of reach, review on the stated context and flag the assumption explicitly.

## What "sound" means — the criteria

Walk these, roughly in order:

1. **Does it meet the goal — including the unhappy paths?** Trace the plan against the acceptance criteria AND the failure modes, not just the happy path. Concurrency, multiple replicas, restarts, partial failure, a dependency being down, retries re-entering an intermediate state — does the approach still hold? An approach that only works on the happy path is unsound.
2. **Does it fit the existing architecture?** Reuse over reinvent. If the codebase already has the infrastructure the plan proposes to build (a parser, a client, a helper, a contract), that's almost always the answer — **check the actual code and the capability spec, don't assume**. Reinventing available infra is the most common avoidable flaw. If the code is genuinely out of reach, review on the stated context and **flag the assumption explicitly** rather than silently approving as if you'd checked.
3. **Does it respect capability boundaries?** Does the plan keep the change inside the right capability, or does it leak responsibility across a boundary the architecture draws (e.g. applying a business rule in a stage that's only supposed to validate structure)? Crossing a boundary the constitution defines is a [BLOCKER] — it's an architecture decision, not an increment.
4. **Is it the simplest approach that works?** Flag over-engineering (a new abstraction/service/config nobody asked for), gold-plating, *and* missing pieces. Right-sized.
5. **Are the load-bearing decisions pinned down?** Identify the irreversible / expensive / architecture-determining choices and require they be made now. Reversible, local choices should be deferred.
6. **Are risks and unknowns named?** The hard parts, integration points between capabilities, data flow, and the one or two things most likely to be wrong should be called out, not glossed.
7. **If the plan creates a new top-level folder/module: is it a capability, not an entity or a layer?** Apply the three tests — the name is a business verb/outcome, not a data noun (`payments/`, not `customer/`); it's a vertical slice (that capability's rules, use cases, persistence), not a horizontal layer (`controllers/`, `utils/`); imports point inward. A plan that introduces package-by-entity or package-by-layer structure is making a boundary decision disguised as a filing choice — [BLOCKER] until the boundary is redrawn around the business outcome.

## The decisive test: deferred detail vs. unspecified decision

When something is missing from the plan, ask: **"does the answer change whether the approach works, or which architecture we commit to?"**

- **Yes → it must be in the plan now.** (Where shared state lives given concurrency; fail-open vs fail-closed when the store is down; which entity is the key; which existing context owns this.) Leaving these implicit is a [BLOCKER] — that's the core of the problem, not a detail.
- **No → defer it.** (Exact config schema, variable names, which file, error-message wording.) Demanding these at plan stage is premature and is itself a review error.

This line is the whole skill. A plausible-sounding plan that hand-waves a load-bearing decision is **not** approvable just because it reads well.

## How to respond

**APPROVE** only when the approach is sound *and* every load-bearing decision is pinned. Otherwise **SEND BACK** with specific, approach-level concerns — and, when there is one, the simpler/correct alternative named concretely (not "rethink this" but "the parser context already exposes a validated Decimal; reuse it instead of re-parsing the string here"). Tag each: **[BLOCKER]** makes the approach wrong, crosses a context boundary, or leaves a load-bearing decision unspecified · **[SHOULD]** a clearly better approach · **[NIT]** optional. The implementer iterates and you re-review until sound. Do not approve a plan with an open [BLOCKER] because "they'll figure it out in implementation."

## Common rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "The plan reads well, approve it" | Reading well ≠ working. Trace it against the failure modes and the real codebase. |
| "It's vague but they'll sort the details out while coding" | Some "details" are load-bearing decisions. If the answer changes the architecture, pin it now. |
| "I shouldn't demand specifics at plan stage" | True for reversible detail, false for the decision the whole approach hinges on. Use the deferred-detail-vs-decision test. |
| "It touches two capabilities but that's fine" | Crossing a boundary the constitution defines is an architecture change, not an increment. Flag it. |
| "Looks like the standard approach, ship it" | The standard approach can still be wrong for this topology (multi-replica, existing infra, this domain's rules). Check fit. |

## Red flags — STOP

- Approving a plan you haven't traced against its **failure modes**, only the happy path.
- Approving a plan that **reinvents infrastructure** the codebase already has — without checking the code or spec.
- Approving while a **load-bearing decision** is still "somewhere appropriate" / unspecified.
- Approving a plan that **leaks responsibility across a capability boundary**.
- Sending a plan back over **implementation detail** that should be deferred.

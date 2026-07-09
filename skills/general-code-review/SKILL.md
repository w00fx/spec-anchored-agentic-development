---
name: general-code-review
description: >
  Use when the reviewer subagent is reviewing a diff for correctness/logic,
  simplicity/reuse, test quality, or type design — the default reviewer
  dimension for the implement-feature and implement-backlog loops. Domain-rule,
  audit-trail, and spec-conformance concerns are NOT here — route those to
  constitution-compliance-review and conformance-review.
---

# General Code Review

## Overview

**You are a machine the producer ran so a human wouldn't have to be the one to catch this.** Find the defects, the needless complexity, the missing coverage, and the type-level holes that would otherwise survive until a human reviewer — or production. Report what is *actually* wrong, with evidence, not stylistic opinions.

This is the default reviewer covering four dimensions. Domain/regulatory concerns (correct numeric type for a sensitive value, source citation, audit trail, responsibility separation) belong to `constitution-compliance-review`. Whether the diff matches the spec or the approved plan belongs to `conformance-review`. Apply those alongside this skill when they fit.

## When to Use

- A code-review subagent is reviewing a diff (per-iteration or whole-changeset) and needs correctness, simplicity, test-quality, and type-design coverage.
- This is the **default** dimension — almost every diff warrants it.

**Not for:** domain-rule/constitution findings; spec or plan divergence; pure formatting a linter already enforces; bikeshedding naming with no correctness or clarity impact.

## Inputs — you run in isolated context

Source everything yourself: the **diff** from git (this branch's committed work plus uncommitted changes — and the commits themselves via `git log` for Dimension 5); the **spec**, when Dimension 3 needs its acceptance criteria, via the touched capability's CLAUDE.md pointer. If no spec covers the touched area, anchor Dimension 3 on the issue's acceptance criteria instead.

## Dimension 1 — Correctness & logic

Does it do the right thing, on the unhappy paths too?

- **Edge & boundary cases:** empty/single/huge inputs, zero, negative, off-by-one, first/last iteration, overflow.
- **Error handling:** are errors caught, propagated, or swallowed? Is a rejected promise / non-zero exit / partial failure handled? Are resources released on the error path (no leaked handles, locks, transactions)?
- **Null/undefined/absent:** is "missing" handled distinctly from "empty" or "zero"?
- **Concurrency:** shared mutable state, races, await-in-loop ordering, non-atomic read-modify-write, unguarded caches.
- **Logic:** inverted conditionals, wrong boolean operator, equality pitfalls, mutating a collection while iterating, incorrect early return, assumptions that data was already validated upstream (was it?).
- **Contract drift:** does the change match its callers and the tests? Did a signature change leave a caller behind?

## Dimension 2 — Simplicity & reuse

Could this be smaller, clearer, or stop repeating itself?

- **Reuse:** an existing helper/util/type this duplicates? Prefer calling it.
- **Duplication:** the same logic in 2–3 places that should be one function.
- **Dead code:** unused vars, unreachable branches, commented-out blocks, params nobody passes.
- **Over-engineering:** abstraction with one caller, configurability nobody asked for, a class where a function would do.
- **New top-level folders are capabilities, not entities or layers:** if the diff creates a top-level folder/module, apply the three tests — business verb/outcome, not data noun (`payments/`, not `customer/`); vertical slice, not a horizontal layer (`controllers/`, `utils/`); imports point inward. Package-by-entity smuggled in as package-by-feature is a boundary problem, not a filing choice — [BLOCKER] if the folder will anchor future code, [SHOULD] otherwise.
- **Altitude:** a function doing too many things; deeply nested conditionals that flatten with early returns; a long parameter list that wants an object.
- **Naming & clarity:** names that mislead or under-describe; a comment that exists only because the code is unclear (fix the code). Comments explain *why*, not *what*.

The named vocabulary for structural findings — twelve Fowler smells with fixes, under the binding rules (the repo's documented standard overrides; always a judgement call, capped at [SHOULD]; skip what tooling enforces) — lives in `references/smell-baseline.md`; read it when structural quality is in question.

## Dimension 3 — Test quality

Tests are the machine that says "no" on the next change — judge whether they actually will.

- **New behavior is covered:** the diff's new logic and edge cases have tests that would fail if the behavior regressed.
- **Tests assert behavior, not implementation:** they check outcomes, not internal call sequences or private state. A test that breaks on a harmless refactor is testing the wrong thing.
- **Tests anchor on the spec:** for a regulated domain, the strongest tests trace to the spec's acceptance criteria, not to what the code happens to do. A test derived from the implementation confirms the implementation.
- **Over-mocking:** mocking the thing under test, or so much that the test only proves the mocks were called. Prefer real collaborators; mock only at genuine boundaries (network, clock, fs).
- **Edge & negative cases:** error inputs, empty inputs, the boundary values from Dimension 1.
- **Determinism:** no reliance on real time, random, network, or ordering; no leaked state between tests.

Worked GOOD/BAD examples and the mocking boundary rule live in `references/test-standards.md` — read it whenever the diff touches tests.

## Dimension 4 — Type design

Make illegal states unrepresentable instead of catching them at runtime.

- **Illegal states representable:** a pair of booleans or optionals encoding a state that should be one union; a struct where some field combinations are invalid.
- **Stringly-typed domain values:** a raw `string`/`number` id where a branded/distinct type would prevent mixing two id kinds. (Sensitive numeric values — money, quantities — are covered more strictly by `constitution-compliance-review`; route the numeric-type question there.)
- **Casts and escape hatches:** `as` / `!` / equivalent forced casts that paper over a real mismatch instead of fixing the type.
- **Exhaustiveness:** a `switch`/match over a union that silently falls through instead of being exhaustive.
- **Parse, don't trust:** if the right fix for a "validated upstream" assumption is to parse into a type that carries the guarantee, say so — that's stronger than a runtime check.

## Dimension 5 — Commit quality

The commits are part of the deliverable — the producer was told so, and you are the reviewer that promise names. Read them via `git log` on the branch:

- **Coherent, reviewable units:** each commit stands alone as one logical change; the sequence tells the story of the implementation.
- **No mixed concerns:** a refactor and a behavior change in the same commit hide the behavior change from review. Flag the mix.
- **Messages say what and why**, referencing the spec section or issue when relevant — not "fix", "wip", "updates".

Severity here is typically **[SHOULD]** (a mixed-concerns commit, a misleading message) or **[NIT]** (wording); a commit problem is rarely a [BLOCKER] unless it hides a behavior change.

## How to report findings

For each finding: **dimension** (correctness / simplicity / test / type / commits), **severity** (**[BLOCKER]** real defect or missing coverage of new behavior · **[SHOULD]** clear improvement · **[NIT]** minor/optional), **location** (`file:line` or symbol), and a **concrete fix** — not "this is complex" but the specific simplification. A finding with no demonstrable wrong behavior, duplication, or coverage gap is a NIT at most; say so honestly rather than inflating it.

## Common rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "It works on the happy path, ship it" | The happy path is the one case you already know works. Review is for the others. |
| "There's no test but the code is obviously correct" | Obvious-and-untested is how regressions enter. New behavior needs a test that would catch its breaking. |
| "The test passes, so it's a good test" | A passing test that asserts implementation details fails on the next refactor and proves nothing about behavior. |
| "It's a bit duplicated but extracting is overkill" | Two copies drift. If the logic is identical and load-bearing, name it once. |
| "I mocked everything so the test is isolated" | Isolation via heavy mocking often tests the mocks. Test through real collaborators; mock only true boundaries. |
| "The cast is fine, I know the type" | A cast that papers over a mismatch is a runtime crash waiting for the input you didn't picture. Fix the type. |

## Red flags — STOP

- Approving a diff whose new behavior has **no test that would fail if it broke**.
- Calling something "complex" or "unclear" without naming the concrete simplification.
- Flagging a domain-rule, numeric-type, audit-trail, or spec-conformance issue here instead of routing it to `constitution-compliance-review` / `conformance-review`.
- Inflating a NIT to a BLOCKER, or burying a real BLOCKER among nits.

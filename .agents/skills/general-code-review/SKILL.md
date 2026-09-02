---
name: general-code-review
description: >
  Criteria for the internal authoring General Code Reviewer. Use on one exact
  Owner candidate to find and fix concrete correctness, simplicity, local
  architecture, test-quality, type, and commit defects before mutation
  hardening. This is cleanup/hardening, not external approval.
---

# General code-review and cleanup criteria

Apply this skill inside the `general-code-reviewer` agent. Review the exact
candidate, fix concrete defects inside the approved scope, verify the result,
and inspect it again. The resulting commit is still a proposal that the Owner
must inspect; this skill never supplies independent approval.

Specialized spec/conformance, security, performance, compliance, and systemic
architecture reviews run outside the implementation harness. Surface a concrete
indicator when found, but do not claim those external reviews happened.

## Required inputs

Require the exact input SHA, complete diff, task/outcome, approved plan and
scope, repository context/rules, verification commands, and baseline failures.
Do not operate on a moving or unidentified candidate.

## Dimension 1 — Correctness and regression surface

Trace the happy path and material failures:

- empty, single, large, zero, negative, first/last, overflow, and absent values;
- error propagation, partial failure, cleanup, retries, cancellation and timeout;
- duplicates, ordering, idempotency, races and non-atomic state transitions;
- caller/consumer compatibility, signatures, serialization and contract drift;
- behavior outside the touched lines that the change can regress.

Fix reproducible defects. Add or strengthen permanent regression coverage at
the boundary where the defect actually occurs.

## Dimension 2 — Simplicity, cohesion and local architecture

Remove needless complexity without expanding the task:

- duplicated logic or mechanisms already supplied by the repository;
- dead code, unreachable branches and obsolete compatibility shims;
- speculative abstractions, unused configurability and one-caller frameworks;
- functions with mixed responsibilities, deep nesting or misleading names;
- framework/IO concerns leaking into business logic;
- local dependency-direction, ownership or resource-lifecycle mistakes;
- new technical-layer/entity folders that violate the capability layout.

Read `references/smell-baseline.md` when structural quality is material. A smell
alone does not justify unrelated cleanup; fix it when it creates a concrete
correctness, testability, coupling or maintenance problem in the approved
change.

## Dimension 3 — Test quality

Follow `.agents/rules/testing.md` and read
`references/test-standards.md` whenever tests change.

Require tests that:

- prove observable behavior and relevant failure/boundary cases;
- use the lowest faithful boundary instead of mocking the behavior under test;
- remain deterministic and isolated from uncontrolled time, randomness,
  ordering or network state;
- would fail if the intended behavior regressed;
- preserve fuzz-found seeds/minimized reproducers where applicable;
- do not weaken golden/reference oracles or merely mirror implementation.

Do not perform language mutation here; that belongs to the subsequent
`mutation-hardener` pass.

## Dimension 4 — Types and contracts

Prefer representations that make invalid states difficult or impossible:

- parse untrusted values into types that carry guarantees;
- model state alternatives explicitly rather than as unrelated booleans;
- keep nullability, precision, ownership, lifecycle and error semantics clear;
- remove casts and untyped escape hatches that hide a real mismatch;
- make matches/switches exhaustive where the language permits it.

## Dimension 5 — Commit and handoff quality

The agent produces one local handoff commit. Ensure that commit:

- contains only accepted in-scope hardening work;
- separates no unrelated refactor or generated noise;
- has a message explaining what and why;
- leaves the tracked tree clean after verification;
- can be inspected as one exact `input_candidate_sha..output_commit_sha` diff.

## Internal loop

```text
inspect exact candidate
→ identify evidence-backed findings
→ fix in scope
→ run affected checks
→ inspect the resulting candidate again
→ repeat while progress is measurable
```

Stop instead of guessing when a fix needs semantic, scope, dependency, oracle,
privilege or external-action authority the agent does not possess.

## Finding and change standard

A `BLOCKER`-class defect needs a reproducible counterexample, failing required
command, unambiguous contract/rule violation, concrete data/security risk, or
missing required evidence. Unsupported preference does not justify a change.

Every applied change must appear in the agent handoff with path, summary,
reason, behavioral impact and verification. The Owner decides whether it lands.

---
name: ticket-readiness-review
description: Review a proposed issue or issue batch before publication or dispatch. Use to verify that each issue is a coherent one-issue/one-task delivery contract, detect both over-splitting and umbrella outcomes that combine independent boundaries, and validate spec references, scope, evidence, risk, and dependencies. Report-only; never edit tickets.
---

# Ticket readiness review

Review the ticket contracts and, when available, the complete proposed set. Do not review
the implementation plan or code. Do not edit the tickets.

Classify every finding as `[BLOCKER]`, `[SHOULD]`, or `[NIT]`. Include the evidence and a
concrete correction.

Use these tests:

> Could a fresh worker execute this task without inventing semantics, scope,
> dependencies, evidence, or permissions?

> Is this issue a coherent delivery task, rather than a requirement, component, test,
> specialist pass, or implementation step promoted into the tracker?

> Does the complete set minimize coordination cost without combining independently
> acceptable outcomes?

> Does a broad outcome label hide capabilities that can be reviewed, accepted,
> recovered, reverted, or verified independently?

## Per-ticket checks

1. **Effective spec and stable IDs** — the ticket points to the effective spec revision
   and uses complete stable IDs. Missing, unknown, positional, or recreated normative
   references are `[BLOCKER]`.

2. **Problem is a claim** — the current problem is stated without presuming an unproven
   diagnosis, and the worker may establish `NO_CHANGE_REQUIRED`. A demanded patch
   regardless of current behavior is `[BLOCKER]`.

3. **One primary outcome** — assess size by the number of independently demonstrable
   outcomes, not by files, steps, requirements, or estimated diff size:

   - no independently useful outcome means the task is too small and should normally be
     merged with the task that completes it;
   - one primary outcome is the intended size;
   - multiple independently acceptable outcomes mean the task is too large and should be
     split at those boundaries.

   Supporting behaviors, failure cases, evidence, and hardening for the same primary
   outcome do not count as separate outcomes.

   Apply the **umbrella-outcome test**: expand broad labels such as `safe lifecycle`,
   `platform foundation`, or `evidence system` into the concrete capabilities delivered.
   If a reviewer could accept one capability and reject another without contradicting
   the stated outcome, the task is too large and must be split at those independent
   boundaries. A broad noun phrase does not create cohesion.

4. **Coherent delivery** — several requirements, components, layers, and test types may
   belong together when they produce the same outcome. Do not request a split solely
   because the diff, file count, criterion count, or internal plan appears large.

5. **Included work is complete** — schemas, adapters, tests, mutation hardening,
   observability, cleanup, and review required for the outcome remain internal work
   unless they possess a genuinely independent delivery boundary.

6. **Scope and non-goals** — the capability area and exclusions are explicit enough to
   prevent silent expansion. Missing high-risk exclusions are `[BLOCKER]`; ordinary
   clarification may be `[SHOULD]`.

7. **Expected evidence** — every verified ID has a credible method and scenario. Tests
   must remain with the behavior they verify. Missing evidence for autonomous work is
   `[BLOCKER]`; for supervised work, classify according to material risk.

8. **Risk and delivery** — rollout, rollback or recovery, external effects, migration,
   and approval requirements are stated when applicable.

9. **Dependencies** — blockers are explicit, real, acyclic, and use the repository's
   canonical representation. Do not infer hidden edges.

## Independent-boundary test

A retained split is justified only when at least one condition is true:

- both parts are meaningful and acceptable independently;
- they have independent rollback or recovery paths;
- different semantic owners or approval authorities govern them;
- a migration, deployment, external-effect, or experiment lifecycle must complete
  independently;
- their scopes are operationally disjoint and safe to execute separately;
- reviewers must make genuinely independent judgments;
- one part is a reusable enabler for multiple downstream outcomes and has its own
  verification.

If none applies, the split is probably a coordination artifact rather than a delivery
boundary.

## Granularity blockers

Report `[BLOCKER]` for these smells unless an independent boundary is demonstrated:

- **Requirement-per-ticket** — one issue for each `BR-*`, `AC-*`, or criterion cluster.
- **Layer/component ticket** — schema, repository, service, adapter, queue, or metric
  separated from the outcome it enables.
- **Separate-test-ticket** — unit, integration, contract, regression, or golden tests
  separated from the implementation they verify.
- **Specialist-pass ticket** — mutation testing, QA, cleanup, hardening, or review made
  into its own issue.
- **Foundation-for-later** — helpers or infrastructure with no independently useful
  result and only one immediate consumer.
- **Serial shards** — consecutive issues reopen the same context to finish one outcome.
- **Temporary plumbing** — one issue creates a structure immediately replaced or
  completed by the next.
- **Same-review-story split** — the issues would be clearer and safer as one PR.
- **Wave/container issue** — an issue exists only to group, phase, or order other issues.
- **Duplicate outcome** — multiple issues claim substantially the same result.
- **Umbrella outcome** — one broad title combines capabilities with independent
  acceptance, rollback, recovery, authority, lifecycle, failure-containment,
  verification, or operational-ownership boundaries. Require a split at those
  boundaries.

## Mandatory batch review

When reviewing a generated set:

1. Confirm that explicit milestones and checkpoints were considered as initial
   candidates, not copied mechanically one-to-one.
2. Inspect every immediate dependency `A -> B`.
3. If A has no useful demonstrable result without B, and both continue the same outcome
   and lifecycle, report `[BLOCKER] Merge A and B`.
4. Merge siblings separated only by requirement group, layer, component, test type, or
   specialist pass.
5. Expand every broad outcome label and confirm that it does not hide independently
   reviewable, reversible, recoverable, or verifiable capabilities.
6. When multiple decompositions remain defensible, prefer the one with fewer cross-ticket
   handoffs while preserving independent delivery boundaries; require a brief rationale
   for rejecting the coarser or more fragmented alternative.
7. Confirm that every stable ID is covered or explicitly deferred.
8. Confirm that no grouping-only or wave artifact exists.

Do not judge the batch by a numeric task count. There is no minimum, maximum, or ratio
between tasks and milestones/checkpoints. A large batch may be correct when every split
has a genuine independent boundary; a small batch may still be fragmented or may combine
unrelated outcomes. Judge only the semantic delivery boundaries and the merge/split tests
above.

## Output

For each issue, return:

```text
#<id or candidate> — READY
```

or classified findings with evidence and the exact merge, split, or rewrite required.

End with:

```markdown
| Task | Ready? | Blockers | Primary outcome | Merge/split action |
|---|---|---|---|---|
```

Then return exactly one batch verdict:

```text
READY
NOT_READY
```

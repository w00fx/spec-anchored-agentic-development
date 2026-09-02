---
name: spec-to-tickets
disable-model-invocation: true
description: >-
  Decompose a ratified capability spec into coherent one-issue/one-task delivery units without splitting by requirement, layer, component, test type, or implementation step.
argument-hint: "[spec path | parent issue]"
---
Convert one effective capability spec into a reviewed set of implementation issues.
You may inspect the repository and publish or update issues. Do not modify production
code or the capability spec.

# Core law

One issue is one **delivery task**:

> the smallest coherent unit that produces one meaningful, independently demonstrable
> outcome and justifies one owner, one branch, at most one PR, and one complete
> implementation-to-review lifecycle.

Optimize for cohesion and coordination cost, not for the smallest technically separable
change.

Do not equate these units:

```text
requirement ID       durable truth in the spec
issue / task         coherent delivery outcome
implementation step work inside the task's plan
verification case    evidence proving the task
specialist pass      mutation, QA, hardening, or review inside the task
```

One task may implement and verify many stable IDs, cross several layers, contain several
test types, and use multiple fresh specialist agents.

# 1. Pin truth and inspect the seam

Read the complete capability spec and its canonical companion files. Resolve the exact
committed revision that makes it effective on the protected/default branch.

Every task records:

```text
capability ID
spec path
spec commit
stable IDs implemented and verified
```

If the spec is not effective, stop with `SPEC_NOT_EFFECTIVE`.

Inspect the relevant code, contracts, tests, ADRs, and repository conventions. Identify:

- what already exists;
- the missing delivery outcomes;
- explicit milestones and checkpoints;
- shared implementation contexts;
- independent approval, rollout, rollback, migration, experiment, or operational
  boundaries.

Use capability language in titles and descriptions.

# 2. Draft outcome-oriented candidates

Use the spec's milestones, checkpoints, vertical validations, independently demonstrable
experiments, and lifecycle boundaries as the first candidates. They are candidates, not
automatic one-to-one tickets.

Build a milestone/checkpoint reconciliation before finalizing the candidates:

```markdown
| Milestone/checkpoint | Proposed task(s) | Treatment | Boundary rationale |
|---|---|---|---|
| <M0-A> | <Task 1> | kept | <why this is one delivery boundary> |
| <M0-C> | <Tasks 3-5> | split | <independent lifecycle boundaries> |
| <M2, M3> | <Task 8> | merged | <why they form one primary outcome> |
```

This reconciliation is diagnostic, not a sizing formula. There is no minimum, maximum,
or expected ratio between tasks and milestones/checkpoints. A checkpoint may become one
task, several tasks, part of another task, or no separate task at all. Every split still
requires an independent boundary; every merge must preserve one coherent primary outcome.

For each candidate, complete this sentence:

```text
After this task, the system can <one meaningful observable capability>.
```

A valid candidate has:

- exactly one primary outcome;
- a useful state when completed;
- one coherent review story;
- mapped stable IDs and credible evidence;
- explicit non-goals;
- an appropriate rollback or recovery boundary;
- no broad label that hides several independently reviewable capabilities.

# 3. Split only at an independent boundary

Keep work together when it serves the same outcome, even when it spans schemas, domain
logic, persistence, infrastructure, tests, mutation hardening, cleanup, or review.

Split only when at least one strong boundary exists:

- each part is meaningful and acceptable independently;
- each part has an independent rollback or recovery path;
- different semantic owners or approval authorities govern the parts;
- a migration, deployment, external-effect, or experiment lifecycle must complete
  independently;
- the scopes are operationally disjoint and safe to execute in parallel;
- reviewers must make genuinely independent judgments;
- one part is a reusable enabler required by multiple downstream outcomes and has its
  own verification.

Record the exact boundary justifying every retained split.

Never split merely because:

- there are many `BR-*`, `AC-*`, files, components, or layers;
- unit, integration, contract, regression, mutation, QA, or review work is needed;
- a fresh agent context is useful;
- the predicted diff or plan has many steps;
- smaller issues appear easier to estimate.

Agent boundary is not ticket boundary.

## Choose between defensible decompositions

More than one decomposition may satisfy the rules. Do not optimize for the fewest or
the greatest number of tasks.

Prefer the decomposition that minimizes cross-ticket coordination while preserving
independently reviewable delivery boundaries. Fewer handoffs are good only when they do
not combine work that can be accepted, rejected, recovered, or reverted independently.

A broad label does not make several independent capabilities one coherent outcome. For
any candidate such as `establish the safe lifecycle`, `build the platform foundation`,
or `implement the evidence system`, expand the label into the concrete capabilities the
system gains and ask whether those parts have materially independent:

- acceptance or review decisions;
- rollback or recovery paths;
- semantic authority or approval boundaries;
- lifecycle states or failure containment;
- verification seams;
- operational ownership.

If they do, split at those boundaries. If splitting would create preparation-only
issues, temporary plumbing, repeated context loading, or multiple PRs needed only to
demonstrate one final result, keep the work together.

When two decompositions remain defensible, present the recommended one and briefly
explain why the alternative is too coarse or too fragmented.

# 4. Reject microtask issues

These are normally internal plan steps, not issues:

```text
create a schema, enum, table, queue, repository, adapter, service, or metric
add unit, integration, contract, or regression tests
run mutation testing or fix surviving mutants
perform QA, cleanup, hardening, or review
```

They become issues only when the independent-boundary rule above is satisfied.

Treat these patterns as granularity blockers:

- one requirement or acceptance criterion per ticket;
- serial layer/component tickets for one outcome;
- tests separated from the behavior they verify;
- mutation-, QA-, cleanup-, or review-only tickets;
- “foundation for the next issue” with no independent value;
- consecutive shards reopening the same context to finish one story;
- temporary plumbing immediately replaced by the next issue;
- milestone, phase, or wave containers with no implementation outcome;
- umbrella outcomes whose broad title masks independently reviewable, reversible,
  recoverable, or verifiable capabilities.

# 5. Run a mandatory merge pass

After drafting candidates, reduce them before showing them to the human.

For every immediate dependency `A -> B`, ask:

1. Does A produce a useful demonstrable result without B?
2. Do A and B have different approval, rollout, rollback, migration, or experiment
   boundaries?
3. Will B immediately reopen the same context to finish the same outcome?
4. Is A merely a schema, adapter, test, infrastructure element, or foundation for B?
5. Would one PR tell a clearer and safer review story?

Merge A and B when A has no independent delivery value and the same outcome and
lifecycle continue in B.

Also merge siblings separated only by component, layer, requirement cluster, test type,
or specialist pass.

Report before approval:

```yaml
candidate_tasks_before_merge: <N>
published_tasks_after_merge: <M>
merged_candidates:
  - candidates: [<A>, <B>]
    reason: <why they are one delivery>
retained_splits:
  - candidates: [<A>, <B>]
    boundary: <independent boundary>
```

# 6. Validate the complete graph

Verify that:

- every required stable ID is covered or explicitly deferred with a reason;
- each task has one primary outcome and one coherent review story;
- no task exists only for a component, layer, test type, or specialist pass;
- no immediate dependency pair should have been one task;
- no two tasks have the same primary outcome;
- no task uses an umbrella outcome to combine independent acceptance, rollback,
  recovery, authority, lifecycle, verification, or ownership boundaries;
- dependencies are explicit, real, and acyclic;
- no grouping-only, milestone-container, or wave issue exists;
- every explicit milestone/checkpoint is reconciled as kept, merged, split, deferred, or
  intentionally non-ticket work;
- each split from one milestone/checkpoint into multiple tasks names an independent
  boundary rather than merely a smaller implementation step;
- each merge of multiple milestones/checkpoints preserves one coherent primary outcome;
- rerunning can identify the same logical tasks instead of duplicating them.

Do not accept or reject the graph by task count. Counts may be reported to make the
shape visible, but they never create a terminal state, override the boundary tests, or
require a human exception.

# 7. Write each issue

Use the repository's stricter issue template when one exists; otherwise use:

```markdown
## <Outcome-oriented title in capability language>

**Capability:** `<CAP-ID>`
**Spec:** `<spec path>` @ `<commit SHA>`
**Implements:** `<one or more stable IDs>`
**Verifies:** `<one or more stable IDs>`

### Problem claim / current state
<What appears missing or incorrect. Do not presume an unproven diagnosis.>

### Outcome
<One meaningful, independently demonstrable result.>

### Included work
<High-level responsibilities that belong inside this task. Do not turn them into
separate issues or prescribe a speculative file-by-file plan.>

### Expected evidence
- `<requirement ID>` — `<verification method and scenario>`

### Scope and non-goals
- In scope: `<coherent capability area>`
- Out of scope: `<explicit exclusions>`

### Risk and delivery
- Risk: `<low | medium | high | critical | normative | security-sensitive>`
- Rollout: `<strategy or not applicable>`
- Rollback/recovery: `<strategy>`
- Autonomy: `<eligible only under an already qualified policy; otherwise ineligible>`

### Blocked by
- `<issue reference>` or `None`
```

`Included work` may contain schemas, adapters, tests, mutation hardening, observability,
cleanup, or other internal responsibilities. Their presence does not create more issues.

# 8. Run ticket readiness review

Before asking for human approval or publishing anything, explicitly invoke the existing
`ticket-readiness-review` skill on the **complete proposed set**, including the dependency
graph and the merge-pass report.

The readiness review must evaluate both:

- whether each issue is an executable task contract;
- whether the set is over-split or improperly combined.

Resolve every `[BLOCKER]`. If the review returns `NOT_READY`, revise the decomposition
and rerun the mandatory merge pass and readiness review.

Do not replace this review with self-review inside the same generation pass.

# 9. Human review and publication

Before publishing, present:

- task titles and primary outcomes;
- stable-ID coverage;
- dependency graph;
- milestone/checkpoint reconciliation;
- counts of milestones/checkpoints, candidates, and final tasks as descriptive context
  only;
- count before and after the merge pass;
- merges performed;
- retained splits and their independent boundaries;
- any materially plausible alternative decomposition and why it was rejected as too
  coarse or too fragmented;
- readiness-review findings and resolutions;
- deferred requirements;
- risk, rollout, and rollback/recovery notes.

Ask the human to approve the task boundaries and graph. If rejected, revise, rerun the
merge pass, and rerun `ticket-readiness-review`. Do not publish a partial or unapproved
set.

After approval:

- create or update one issue per delivery task;
- publish blockers before dependents when identifiers are required;
- use the repository's canonical dependency representation;
- recognize existing logical tasks on rerun instead of duplicating them;
- never create wave, container, test-only, mutation-only, QA-only, or review-only issues;
- do not close or rewrite unrelated issues.

# Terminal states

Finish as exactly one:

```text
PUBLISHED
READY_TO_PUBLISH
SPEC_NOT_EFFECTIVE
NAMED_BLOCKER
```

For any non-success terminal, state the blocker, evidence gathered, and exact human or
repository action required.

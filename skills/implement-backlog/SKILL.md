---
name: implement-backlog
description: >
  Autonomous implementation workflow for increment work triggered by new
  GitHub issues. Runs end-to-end without human confirmation between phases:
  reads the issue and relevant context (CLAUDE.md → capability CLAUDE.md
  → spec, applicable rules, past lessons), aborts if ambiguities are detected
  (commenting on the issue), plans with maximum reasoning, implements with
  scope discipline and meaningful commits, runs local QA gates (tests → code
  review), and opens a PR. Limited to increment scenarios (bugfix, tech-debt,
  rule adjustment, reference data update, feature-within-scope from
  backlog). New capabilities and large features are OUT of scope —
  those are human-led through the `implement-feature` skill. Decisions are
  recorded in the log and PR description for human review at PR approval.
  Every run produces a structured log.

  Trigger: a thin GitHub Action runs `claude -p "/goal ..."` in headless
  mode when an issue gets the `auto-implement` label. Claude Code's native
  /goal command is the persistence engine; this skill is the workflow it
  drives. There is no custom orchestrator service.
---

You are an autonomous senior engineer implementing increment work in this
codebase, triggered by a new GitHub issue.

This skill is **autonomous**: it runs end-to-end without human confirmation
between phases. Decisions are recorded in the log and the PR description
for human review at the PR approval step.

**Scope:** increment work only — bugfix, tech-debt, rule adjustment,
reference data update, or feature-within-scope items from backlog.

**Out of scope:** new capabilities and large features. Those involve
architectural decisions that are not safe to make autonomously, and are
handled by the `implement-feature` skill (local, human-driven). If the
issue describes work that is clearly architectural (new capability,
new sub-area, major new feature spanning multiple capabilities), abort with
a comment on the issue routing the work appropriately.

**How this skill is driven.** This skill is the *workflow*; it does not
provide its own persistence. Persistence comes from Claude Code's native
`/goal` command — a session-scoped Stop hook that, after every turn, has a
fresh model re-check a completion condition and forces another turn until
it holds. A thin GitHub Action runs `claude -p "/goal <condition>"` in
headless mode when an issue gets the `auto-implement` label. The condition
names this skill as the workflow and mirrors the completion criteria and
the abort cases below — including a "done with a named blocker" clause, so
a legitimate abort ends the goal instead of looping forever. The Action is
the trigger, the native `/goal` is the engine, this skill is the workflow,
and the `reviewer` agent carries the criteria — there is no custom
orchestrator service.

**Target model:** this skill is tuned for Claude Opus 4.8 running in
Claude Code headless mode (`claude -p`). The thinking-depth lever here
is the ULTRATHINK keyword (Phase 2) — there is no plan mode in this
skill: "do not edit any file" is the instructional substitute, because
an interactive plan gate would be silently overrun with no one to
answer it. On a model change, re-audit the skill: thinking defaults
and instruction-following behavior shift between model families.

You follow a phased workflow analogous to `implement-feature`, with these
differences:
- No human confirmation between phases (decisions are logged and surfaced
  in the PR).
- Ambiguity → abort with comment on the issue (do NOT guess).
- Scope expansion mid-implementation → abort (do NOT silently grow).
- Repeated QA failure (3+ iterations on the same issue) → abort with
  comment on the issue.

Every run appends a structured log under `.claude/logs/`.

## Phase 1: Understand

1. Read the triggering issue in full: title, body, labels, comments,
   attachments.
2. Read the CLAUDE.md at the repository root.
3. Identify the target capability from the issue. Read its
   CLAUDE.md, which should point to its spec — follow that pointer and
   read the capability spec.
4. Read `.claude/rules/` for any rules that may apply.
5. Read `lessons.md` for past pitfalls relevant to this area.
6. Map the current state of the code that will be changed, using the
   exploration tools and discipline in the root CLAUDE.md (structural
   queries before reading whole files).

**Scope routing check:** if the issue describes new capability
creation, new sub-area, or a major new feature, abort with a comment on
the issue:
- Explain why this is out of scope for `implement-backlog`.
- Route to `implement-feature` (local, human-led).
- Apply a label like `wrong-skill` or `needs-human-implementation`.
- STOP. Do NOT proceed.

Record in the log:
- Issue reference, summary
- Target capability
- Spec sections, rules, lessons identified as relevant
- Files and capabilities that will be affected
- Risks or edge cases observed

Proceed to Phase 1.5 (no confirmation gate).

## Phase 1.5: Resolve ambiguities

Check explicitly for:
- Issue body silent on edge cases (missing input, invalid source,
  out-of-range values, retries).
- Numeric handling unspecified (rounding mode, precision, scale, units).
- A referenced rule or table has multiple versions, or conflicting
  versions — which one applies?
- The target capability is unclear.
- Acceptance criteria not specific enough to verify ("should work", "must
  be correct" are not criteria).
- Source attribution: required normative source not provided.

As you scan, label every point where you would otherwise fill an
unspecified behavior with a plausible default: write it as `ASSUMPTION:
<behavior you'd assume> — <what the issue leaves undefined>`. Forcing the
guess to be named turns an invisible default into a visible question — an
unlabeled assumption is the gap that ships looking done.

**If any ambiguity is detected:**

1. Post a comment on the issue with:
   - Numbered list of detected ambiguities.
   - Proposed interpretation for each (so the human refining the issue
     has a starting point).
   - Explicit request: "Please refine the issue and re-trigger
     implementation when ready."
2. Apply a label like `needs-refinement` (or the repo convention).
3. Record the abort in the log.
4. STOP. Do NOT proceed to Phase 2.

**If no ambiguity is detected:**

Record this in the log and proceed to Phase 2.

The reason to abort rather than guess: an autonomous run that guesses
wrong on intent produces a PR that may have to be discarded entirely.
Forcing the issue back to the reporter for clarification is cheaper than
re-doing the implementation.

## Phase 2: Plan

Use maximum reasoning depth (ULTRATHINK) for this phase. Do not edit any
file.

1. Think through the implementation step by step.
2. For each step, identify:
   - Which spec sections, rules, or constitution items apply.
   - What existing code will be affected.
   - What could break, especially cross-capability concerns.
   - What edge cases the issue makes explicit.
3. Break the work into small, sequential changes.
4. Identify which tests need to be written or updated.
5. Map dependencies between steps.
6. Explicitly list the files you expect to edit. This is your committed
   scope for Phase 3.
7. Separate **load-bearing decisions** from **deferred details**. A
   load-bearing decision determines whether the approach works at all or
   which architecture you commit to (where shared state lives given
   concurrency, fail-open vs fail-closed when a dependency is down, which
   entity is the key, which existing infra you reuse). These MUST be
   resolved in the plan. Deferred details are reversible and local — leave
   them to implementation. The test: "does the answer change whether the
   approach works, or which architecture we commit to?" If yes, it's
   load-bearing; pin it now.

Record the plan in the log as a numbered list with rationale per step, the
file list as a separate block, and the load-bearing decisions called out
explicitly. The plan also goes into the PR description (Phase 7).

**Plan review gate (replaces the human gate of `implement-feature`).**

In `implement-feature` a human reviews the plan before code is written.
Here there's no human — so a fresh subagent is the gate. Before proceeding
to Phase 3, dispatch a plan-review subagent via the Agent tool, in isolated
context (it must NOT be the context that wrote the plan — a fresh context
doesn't share the author's blind spots):

- task: Run reviewer
- prompt: "Review the implementation plan pasted below (no code yet)
  for approach soundness. Load the plan-review skill and apply its
  criteria in full — the skill is the single source of the soundness
  bar; do not substitute a shorter checklist. Report
  [BLOCKER]/[SHOULD]/[NIT] with a concrete alternative for each
  blocker. Do not approve a plan with an open BLOCKER.

  PLAN:
  [paste the full plan here — steps, rationale, file scope,
  load-bearing decisions]"

The plan is pasted because the reviewer runs in isolated context — it
cannot see this conversation, and "this plan" means nothing to a fresh
context. The criteria are deliberately NOT repeated in the prompt: the
skill is the single source of truth, and an inlined copy silently
drifts as the skill evolves.

If the reviewer returns a BLOCKER, revise the plan and re-dispatch —
same prompt, plus a section the fresh instance needs in order to
inherit the thread instead of re-litigating it:

  PRIOR REVIEW FINDINGS (iteration N-1) AND HOW THIS REVISION
  ADDRESSES EACH:
  [paste each finding → what changed in the plan]

Iterate until the approach is sound, then proceed to Phase 3 — capped
at 3 review iterations, the same cap Phases 4 and 5 use. A plan that
can't converge in three rounds almost always means the issue
under-specifies the work:

1. STOP. Post a comment on the issue with the unresolved BLOCKERs and
   why they resisted revision.
2. Apply the `needs-refinement` label.
3. Record the abort in the log.

A wrong approach caught here is free; caught after implementation it's
a discarded PR.

This is the same `reviewer` agent used for code review in Phase 5 — one
reviewer agent, multiple criteria skills; here it loads plan-review.

## Phase 3: Implement

1. Implement the changes following the plan.
2. Write or update tests for every piece of business logic. Tests must
   anchor on the behavior described in the spec's acceptance criteria
   (or the issue's) — NOT on what the code happens to
   do. A test derived from the implementation confirms the implementation;
   it doesn't prove the behavior is correct.
3. Follow all rules in `.claude/rules/`.
4. After each logical chunk — before writing the next one — run lint AND
   the tests covering the code you just touched. Do not write the next
   chunk until both are green. Checks every chunk (not batched at the end)
   catch a break while it's cheap to locate. Run the full suite in Phase 4
   regardless.

**Commits during implementation:**

Make commits as the implementation progresses. The number of commits is
a judgment call based on what aids review — NOT a mechanical 1:1
mapping with plan steps.

Guidelines:
- Each commit should be a coherent, reviewable unit.
- Commit messages map to what changed and why, referencing the issue.
- Avoid commits that mix unrelated changes.
- A small change may be a single commit; a multi-faceted change may
  produce several.

**Examples:**
- Change: implemented the rounding fix from issue #142 plus its tests →
  commit: `payments: round at half-cent boundary per spec (#142)`
- Change: updated the reference table to the 2026-07 version, no logic
  change → commit: `rates: update reference table to 2026-07 (#155,
  data only)`

**Scope discipline — abort on expansion:**

If you find yourself needing to edit a file that was NOT in the
committed scope from Phase 2:

1. STOP. Do not edit it.
2. Post a comment on the issue with:
   - Which file you wanted to touch.
   - What change was needed.
   - Why the original plan missed this.
   - Recommendation: split into another issue, or refine the current
     issue and re-trigger.
3. Apply a label like `scope-expansion-needed`.
4. Record the abort in the log.
5. STOP. Do NOT silently grow the scope.

Unlike `implement-feature` (which can ask a human to approve expansion
in-flight), this skill aborts. A clean abort with explanation is cheaper
than a PR that grew unrecognizably during implementation.

**Minimal solution — the Opus guard:**

Opus-family models tend to overdeliver, and in autonomous mode no human
trims the excess mid-run — the guard is you. Keep the change the
minimum the issue needs:
- No features, refactors, or "improvements" beyond what the issue asks
  — a bugfix doesn't need the surrounding code cleaned up.
- No docstrings, comments, or type annotations on code you didn't
  change.
- No defensive handling for scenarios that can't happen — validate at
  system boundaries, trust internal code.
- No helpers or abstractions for one-time operations, and no design
  for hypothetical future requirements.

Everything past the minimum is review surface without value — and here
it lands on the human at PR review, undiluted.

## Phase 4: Test

Run the full local test suite.

**If tests fail:**
1. Read the failure output carefully.
2. Fix the issue.
3. Run tests again.
4. Repeat — but cap iterations.

If the project has an eval regression suite (see `EVALS.md` if present),
and this change touches code covered by it, run the relevant subset.

**If the same failure occurs 3+ times:**

1. STOP. Do not keep retrying.
2. Post a comment on the issue with:
   - Description of the failure.
   - What was tried.
   - Why it keeps failing (best hypothesis).
3. Apply a label like `qa-blocked`.
4. Record the abort in the log.
5. STOP.

Do NOT proceed to Phase 5 until tests are green.

## Phase 5: Code Review

Use the Agent tool to dispatch the `reviewer` agent in isolated context
(it did not write this code).

**Default — one reviewer, all applicable lenses:**

- task: Run reviewer
- prompt: "Review this change set — obtain the diff yourself via git
  (this branch's committed work plus uncommitted changes). Load the
  applicable review-criteria skills per your routing table — the
  conditions are not restated here on purpose (an inlined copy
  drifts); conformance-review applies, and the approved plan it needs
  (from Phase 2, plus any approved deltas) is pasted below. Report
  [BLOCKER]/[SHOULD]/[NIT]; do not edit.

  APPROVED PLAN:
  [paste the plan here]"

**Large or critical diff — three parallel single-lens reviewers.** If the
diff exceeds roughly 400 changed lines or 10 files, or conformance will
trace multiple spec sections, dispatch three `reviewer` tasks in ONE
message (they run in parallel), each pinned to a single lens (general /
constitution-compliance against architecture/constitution.md / conformance
against the spec and the approved plan **pasted into its prompt**). Each
prompt tells the reviewer to obtain the diff via git — isolated context
sees no "session". Merge the reports: de-duplicate, keep
the highest severity for duplicates. The plan gate (Phase 2) is never
parallelized.

Wait for the review report(s).

**If issues found:**
1. Fix the issues.
2. Go back to Phase 4 (tests) → Phase 5 (Code Review).
3. Repeat until the review passes — but apply the same 3-iteration
   cap. If the review keeps surfacing the same kind of issue 3+ times,
   abort with a comment on the issue (label `review-blocked`).

Tests and review are sequential gates: any fix during review forces
re-running tests, because the fix may have broken something else.

## Phase 6: Close the loop

Only proceed once tests are green AND review is clean.

1. **Lessons** (`lessons.md`): append a terse, concrete entry if this
   run revealed a new pattern, pitfall, or recurring mistake.

2. **Spec**: never edit the spec in this skill — spec changes are
   business-rule decisions, and an autonomous run has no human at the
   gate to approve one (note the CLAUDE.md rule below: if the *context
   file* is propose-only here, the business source of truth is too).
   If the implementation revealed the spec is wrong, incomplete, or
   out of sync with reality: propose the correction in the PR
   description and in a comment on the issue, and mark the run
   `requires_human_approval = true` — the proposal needs an explicit
   human decision at PR review, not a routine skim. If the spec error
   blocks implementing the issue correctly, the issue's foundation is
   wrong: abort with the `needs-refinement` label instead of building
   on it.

3. **CLAUDE.md** (root or capability): if you found yourself
   repeating instructions or context that should be persistent, propose
   an addition in the PR description (do NOT edit CLAUDE.md directly in
   this skill).

4. **Issue**: prepare the closure comment with PR link. Close on merge
   if applicable (the merge action itself happens outside this skill).

## Phase 7: Open PR and monitor until landed

Opening the PR is NOT the finish line. Done = the change merged clean, or
you're blocked on something only a human can resolve. Open the PR
following the description template in `references/pr-template.md`: read
it when you open the PR and mirror its sections. Two of them are
load-bearing beyond the human review — the **Approved plan** section is
the plan's public home (Phase 2 records the plan in the log *and*
here; `/explain` and any future reviewer without this conversation
pull intent from it), and **Spec correction proposed** pairs with the
`requires_human_approval` flag.

If `requires_human_approval = true`, apply a label like
`human-approval-required` on the PR (or the repo convention).

Post a comment on the originating issue with the PR link.

**Monitor until landed.** After opening, watch the PR until it merges
clean — do not abandon it at open:

- **CI to completion**, not just to the first green. A check can go green
  then flip red as the full pipeline runs (the green-minute rule) — wait
  for the pipeline to settle.
- **Late comments.** From an *external review tool*: advisory. They inform
  the human who approves the merge; the loop does not wait on them or abort
  on them, and they are NOT part of the completion condition (what gates is
  Phase 5 + CI — deterministic checks and the contextual reviewer, reliable
  enough to block; an external reviewer's precision is not). From a *human*:
  address them if in scope, or if they need a decision only a human can
  make, leave the PR for human resolution and stop.
- **Merge conflicts** — if the base branch moved, rebase/resolve and
  re-run the QA gates (Phase 4 → Phase 5) on the result, since resolving a
  conflict is a code change.

If monitoring surfaces an issue the skill can fix within scope, fix it and
re-run the affected gates. If it surfaces something out of scope or needing
human judgment, comment on the PR/issue naming exactly what's blocking and
stop — don't mark done around an unresolved check.

(Operational note: monitoring runs against the GitHub API. The watch window
and whether merge is automatic or human-gated follow repo policy — until
auto-merge by class exists (`AUTONOMY-PLAYBOOK.md`, Milestone 4), a human merges, and
the skill's job ends at "PR green, reviewed, and nothing outstanding.")

## Structured logging

Append a structured log to
`.claude/logs/implement-backlog-{ISO timestamp}.md`. The full schema —
trigger, one section per phase, and the per-phase abort outcomes —
lives in `references/log-template.md`: read it when you open the log
at the start of the run, and mirror its structure phase by phase.

The log is the audit trail. Since there are no human confirmations
during the run, the log is the only record of the decisions taken.

## Common rationalizations

The shortcuts that turn an autonomous run into a discarded PR or a human's
cleanup. In autonomous mode there's no human to catch these mid-run — the
machine has to.

| Rationalization | Reality |
|-----------------|---------|
| "The tests pass, so it's done" | Tests written alongside the code confirm the implementation, not the spec. Green proves "works as I tested," not "works as specified." |
| "The approach is obvious, skip the plan review" | The plan-review subagent is the only gate before code in autonomous mode. Obvious-and-unreviewed is exactly how the wrong approach ships a PR that gets discarded. |
| "I'll run the full checks at the end" | Run lint + touched tests every chunk. End-only batching turns one red bar into a bisecting session with no human watching. |
| "This file is just outside scope, I'll edit it anyway" | Silent scope growth has no human to catch it here. Abort with a comment — that's the rule, not a suggestion. |
| "The PR is open, the run is done" | Open ≠ landed. Monitor CI to completion, late comments, and conflicts until it merges clean or you name a blocker. |
| "CI will catch it" | CI catching it means a red PR waiting on a human. Catch it locally first, in Phase 4. |
| "The flaky check isn't really my problem" | A red check is unresolved work. Fix it, or stop and name the blocker — never retry-until-green or mark done around it. |

## Critical rules

The phases above carry their own protocols and reasons; these five are
the cross-cutting invariants worth restating:

- **No human mid-run — abort instead.** Every would-be question is an
  abort with issue comment + label + log entry. The four labels are
  the vocabulary: `needs-refinement`, `scope-expansion-needed`,
  `qa-blocked`, `review-blocked` (each phase defines its trigger — the
  labels are stable; the conditions live where they're enforced).
- **The plan-review gate always runs before code**, in a fresh
  context. It replaces the human gate of `implement-feature`; skipping
  it means no gate at all.
- **Dispatch the reviewer via the Agent tool, in isolated context** — a
  reviewer that didn't write the work is the point, for the plan and
  for the code.
- **Never edit the spec or CLAUDE.md in this skill** — propose in the
  PR description instead. Both are human-decision artifacts, and this
  run has no human at the gate.
- **Cap every loop at 3** — plan review, tests, code review. The
  fourth attempt at the same failure is a signal, not a retry: abort
  and name the blocker.

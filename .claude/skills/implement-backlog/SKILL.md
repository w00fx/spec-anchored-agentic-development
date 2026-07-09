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
  mode when an issue gets the `auto-implement` label — or a scheduled
  Routine works the frontier (canonical prompt:
  `.claude/routines/frontier-worker.md`). Claude Code's native
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
orchestrator service. A scheduled Claude Code **Routine** is the sibling
wiring — same engine, same condition shape; it scans the frontier,
claims one issue, and issues the `/goal` (canonical prompt:
`.claude/routines/frontier-worker.md`).

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
- **New-rule check:** the issue's expected behavior encodes a business
  rule the capability spec does not cover — that is a spec change, not
  an increment. Rule merges are human-gated (this skill never edits
  the spec): abort, and the comment names the rule and routes the work
  to the human-led path.

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
4. Identify which tests need to be written or updated — and the
   **seam** they attach to: prefer an existing seam over a new one, the
   highest seam that still isolates the behavior, ideally one for the
   whole change. A good seam gives tests something durable to target,
   so the code underneath can change without the tests moving.
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
   it doesn't prove the behavior is correct. Write to the shared
   standard the reviewer will hold this work to:
   `.claude/skills/general-code-review/references/test-standards.md`
   (worked GOOD/BAD examples + the mocking boundary rule).
3. Follow all rules in `.claude/rules/`.
4. After each logical chunk — before writing the next one — run lint, typecheck, AND
   the tests covering the code you just touched. Do not write the next
   chunk until all three are green. Checks every chunk (not batched at the end)
   catch a break while it's cheap to locate. Run the full suite in Phase 4
   regardless.

**Work branch — before the first edit or commit:**

If the harness already put the session on a dedicated work branch
(Routines does: `claude/`-prefixed — stay on it; the platform only
allows pushes there), use it. Otherwise create one named by type,
with the issue number: `fix/142-<slug>`, `feature/<slug>`,
`refactor/<slug>`, `chore/<slug>`. Never commit to the default
branch.

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

**Plan invalidation — when the approach itself fails:**

Scope discipline covers "I need one more file." This covers the bigger
break: implementation reveals that a load-bearing decision from the
approved plan is wrong, or the approach doesn't work. Do not improvise
a new approach inside the old plan — an approved plan the code no
longer follows is fiction, and conformance review will flag the
divergence anyway. Instead:

1. STOP editing.
2. Produce a revised plan as a **delta** over the approved one: what
   changes, why, and what the implementation revealed that planning
   didn't foresee.
3. Re-dispatch the plan-review gate — Phase 2's prompt, plus the prior
   findings section AND the delta's rationale. The gate that approved
   the original plan is the gate for its revision; no human is needed,
   because the plan gate here was never a human.
4. The revision counts against the **same 3-iteration plan-review
   cap** as Phase 2. Cap exhausted → the existing abort: comment with
   what failed, label `needs-refinement`, log, STOP.
5. On approval: record the replan in the log (`Replans`), revert the
   work the new plan invalidates (never leave it half-aligned), and
   continue under the revised plan.

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

Before any dispatch, confirm the diff is non-empty — an empty diff
should fail here, not inside the reviewer.

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
1. Fix the issues — and each fix ships with a **regression test that
   failed before the fix and passes after it**, when the finding is
   test-shaped. A finding fixed without red-then-green is fixed by
   claim, not by proof — and the class of bug the reviewer caught once
   should be caught by the machine forever after. When a finding isn't
   test-shaped (naming, structure, a comment), say so and note how it
   was verified instead. Never invent a hollow test just to satisfy
   this step.
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

**Monitor until landed** — the full protocol (CI to completion, the
late-comments policy, merge conflicts re-running the gates) lives in
`references/pr-template.md`: read it when the PR opens.

## Structured logging

Append a structured log to
`.claude/logs/implement-backlog-{ISO timestamp}.md`. The full schema —
trigger, one section per phase, and the per-phase abort outcomes —
lives in `references/log-template.md`: read it when you open the log
at the start of the run, and mirror its structure phase by phase.

The log is the audit trail. Since there are no human confirmations
during the run, the log is the only record of the decisions taken.

## Common rationalizations

The shortcuts that turn an autonomous run into a discarded PR or a
human's cleanup — and in autonomous mode there's no human to catch
them mid-run, so the machine has to. The full table lives in
`references/rationalizations.md`: read it alongside the log template
when the run starts.

## Critical rules

The phases above carry their own protocols and reasons; these five are
the cross-cutting invariants worth restating:

- **No human mid-run — abort instead.** Every would-be question is an
  abort with issue comment + label + log entry. The labels are the
  vocabulary: `needs-refinement`, `scope-expansion-needed`,
  `qa-blocked`, `review-blocked`, plus Phase 1's scope-routing pair
  (`wrong-skill` / `needs-human-implementation`). Each phase defines
  its trigger — the labels are stable; the conditions live where
  they're enforced.
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

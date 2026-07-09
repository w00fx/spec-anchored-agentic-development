---
name: implement-feature
description: >
  Local implementation workflow for code work based on existing specs, issues,
  or backlog items, with human confirmation gates between phases. Covers three
  scenarios: implementing a new capability from its spec, implementing a
  large feature in an existing capability, and applying increments (bugfix,
  tech-debt, rule adjustment) from backlog. Reads relevant context (CLAUDE.md
  → capability CLAUDE.md → spec, applicable rules, past lessons), surfaces
  ambiguities before planning, plans with maximum reasoning, implements with
  scope discipline and meaningful commits, runs local QA gates (tests → code
  review), and closes the loop (lessons, spec, CLAUDE.md, backlog). Spec
  creation and refinement are OUT of scope — that work is human-led, outside
  this skill. Every run produces a structured log. Use this skill whenever the
  user asks to implement, build, code, fix, or apply a change from a
  spec, issue, or backlog item — even without typing /implement. Invoke
  with /implement followed by what to do.

  Examples:

  - /implement read [spec path] and implement [capability]
  - /implement implement [feature described in issue ref] in [capability]
  - /implement apply pending items from issue [issue reference]
  - /implement fix the [behavior] in [path] — should be [X] not [Y]
---

You are a senior engineer implementing code work in this codebase, based on
an existing spec, issue, or backlog item.

This skill covers three scenarios, all starting from existing
specification/backlog input:

1. **New capability**: implementing the code structure for a capability
   whose spec already exists (created human-led, outside this skill).
2. **Large feature**: implementing a large feature within an existing
   capability. There is no separate feature-spec — the capability spec is
   the source of truth and the issue defines the scope; the work is carried
   by a larger Phase 2 plan, and if the feature introduces a new business
   rule, that rule is merged into the capability spec at the gate (human
   approval) before implementation.
3. **Increment**: bugfix, tech-debt, rule adjustment, reference data update,
   or feature-within-scope item from backlog.

**Out of scope:** spec creation and spec refinement. If the user asks to
create a new spec or refactor an existing spec, STOP and clarify — that
work is human-led, not skill work.

This skill is the **local, human-driven** entry point, invoked via the
`/implement` command. It runs interactively — plain, or wrapped in a
**supervised `/goal`** (the recommended pattern for work with acceptance
criteria): interactively, the gate tools (`AskUserQuestion` /
`ExitPlanMode`) pause the turn, the human answers, and the answers enter
the transcript — so the gates and the loop coexist, while the fresh
evaluator keeps the worker from declaring completion before the condition
holds. What this skill must NEVER run under is **headless `/goal`**
(`claude -p`): there, no one answers, and the gates are silently overrun
rather than honored. Autonomous, headless implementation is the separate
`implement-backlog` skill.

**Target model:** this skill is tuned for Claude Opus 4.8 running in
Claude Code — plan mode plus the ULTRATHINK keyword are its
thinking-depth levers. On a model change, re-audit the skill: thinking
defaults and instruction-following behavior shift between model
families, and a capability jump is the right moment to re-evaluate
which instructions are still needed.

You follow a strict phased workflow that ensures every change is tested,
spec-compliant, code-reviewed, and that the work loop is closed. Every run
appends a structured log under `.claude/logs/`.

One rule governs every gate in this workflow: **a "no" from the human
means revise and re-present that same phase** — it never means "proceed
with adjustments." A corrected understanding re-presents Phase 1; a
rejected plan re-enters Phase 2; a rejected rule-merge (Phase 1.5)
means the feature as understood is blocked — rescope it or stop.
Silence about what "no" means is how gates get skipped in practice.

## Phase 1: Understand

1. Read the user's instructions carefully.
2. Identify the input: spec path, issue/backlog
   reference, or direct prompt.
3. Read the relevant input in full.
4. Read the CLAUDE.md at the repository root for general context and
   navigation pointers.
5. Identify the target capability. Read its CLAUDE.md, which should
   point to its spec — follow the pointer and read the capability spec.
6. Read `.claude/rules/` for any rules that may apply to the area being
   changed.
7. Read `lessons.md` for past pitfalls relevant to this area.
8. Map the current state of the code that will be changed, using the
   exploration tools and discipline in the root CLAUDE.md (structural
   queries before reading whole files).

Summarize to the user:
- What you understood needs to be done
- Which input you read (spec / issue)
- Target capability and which spec sections, rules, or constitution
  items apply
- Files and capabilities that will be affected
- Any risks or edge cases you see

Wait for explicit user confirmation before proceeding to Phase 1.5.

## Phase 1.5: Resolve ambiguities

Before planning, surface any ambiguity that would force you to guess. Do
NOT proceed to Phase 2 with unresolved ambiguity — guessing here propagates
through every subsequent phase and produces correct code for a wrong
interpretation.

Check explicitly for:
- Spec or item description silent on edge cases (missing input, invalid
  source, out-of-range values, retries).
- Numeric handling unspecified (rounding mode, precision, scale, units).
- A referenced rule or table has multiple versions in the repository, or
  conflicting versions — which one applies?
- The target capability is unclear, or the change could plausibly
  belong to one of several.
- Acceptance criteria not specific enough to verify ("should work", "must
  be correct" are not criteria).
- Source attribution: if the domain requires citing normative sources, is
  the source available for every rule being touched?
- **Large feature (scenario 2) — new-rule check:** does any behavior you
  are about to implement encode a business rule the capability spec does
  not yet cover? If yes, this gate is where it stops: propose the spec
  merge (rule text, target section, `requires_human_approval = true`) and
  proceed to Phase 2 only after the human approves and the spec is
  updated. The spec is the source of truth — a rule that ships only in
  code is a rule nobody can audit.

As you scan, label every point where you would otherwise fill an
unspecified behavior with a plausible default: write it as `ASSUMPTION:
<behavior you'd assume> — <what the spec leaves undefined>`. Forcing the
guess to be named turns an invisible default into a visible question — an
unlabeled assumption is the gap that ships looking done.

Present a numbered list of ambiguities to the user with your proposed
interpretation for each. Use AskUserQuestion to confirm or correct.

If no ambiguities exist, state that explicitly and ask for confirmation to
proceed to Phase 2.

## Phase 2: Plan

This is the most critical phase. The quality of the plan determines the
quality of everything that follows.

**Tell the user: "Entering plan mode with maximum reasoning."**

Enter plan mode. Use ULTRATHINK to activate maximum reasoning depth.

In plan mode (read-only, no edits allowed):

1. Think through the implementation step by step.
2. For each step, identify:
   - Which spec sections, rules, or constitution items apply.
   - What existing code will be affected.
   - What could break, especially cross-capability concerns.
   - What edge cases the resolved ambiguities now make explicit.
3. Break the work into small, sequential changes.
4. Identify which tests need to be written or updated — and the
   **seam** they attach to: prefer an existing seam over a new one, the
   highest seam that still isolates the behavior, ideally one for the
   whole change. A good seam gives tests something durable to target,
   so the code underneath can change without the tests moving.
5. Map dependencies between steps — what must happen before what.
6. Explicitly list the files you expect to edit. This is your committed
   scope for Phase 3.
7. Separate **load-bearing decisions** from **deferred details**. A
   load-bearing decision determines whether the approach works at all or
   which architecture you commit to (where shared state lives given
   concurrency, fail-open vs fail-closed when a dependency is down, which
   entity is the key, which existing infra you reuse). These MUST be
   resolved in the plan. Deferred details are reversible and local (exact
   config schema, variable names, error-message wording) — leave them to
   implementation. The test: "does the answer change whether the approach
   works, or which architecture we commit to?" If yes, it's load-bearing;
   pin it now. Don't hide a load-bearing decision as a detail.

Present the plan to the user as a numbered list with rationale per step,
the file list as a separate block, and the load-bearing decisions called
out explicitly. Wait for explicit approval before proceeding to Phase 3.

## Phase 3: Implement

1. Implement the changes following the approved plan.
2. Write or update tests for every piece of business logic. Tests must
   anchor on the behavior described in the spec's acceptance criteria
   (or the issue's) — NOT on what the code happens to
   do. A test derived from the implementation confirms the implementation;
   it doesn't prove the behavior is correct. Cover the edge cases the
   resolved ambiguities made explicit, not just the happy path. Write
   to the shared standard the reviewer will hold this work to:
   `.claude/skills/general-code-review/references/test-standards.md`
   (worked GOOD/BAD examples + the mocking boundary rule).
3. Follow all rules in `.claude/rules/`.
4. After each logical chunk — before writing the next one — run lint, typecheck, AND
   the tests covering the code you just touched. Do not write the next
   chunk until all three are green. Running checks every chunk (not batched at
   the end) catches a break while it's still cheap to locate; batching
   turns one red bar into a bisecting session. Run the full suite in
   Phase 4 regardless.

**Work branch — before the first edit or commit:**

Create a work branch named by type — `feature/<slug>`, `fix/<slug>`,
`refactor/<slug>`, `chore/<slug>`, `docs/<slug>` (or the repo's own
convention), with the issue number when one exists
(`fix/142-round-half-cent`). If the session is already on a dedicated
work branch, stay on it. Never commit to the default branch.

**Commits during implementation:**

Make commits as the implementation progresses. The number of commits is a
judgment call based on what aids review — NOT a mechanical 1:1 mapping
with plan steps.

Guidelines:
- Each commit should be a coherent, reviewable unit.
- Commit messages map to what changed and why, referencing the spec
  section or issue when relevant.
- Avoid commits that mix unrelated changes (e.g., refactor + new
  behavior in the same commit).
- A small change may be a single commit; a multi-faceted change may
  produce several.

**Examples:**
- Change: implemented the PENDING-duplicate rejection rule plus its
  tests → commit: `payments: reject duplicate charge while PENDING
  (spec: Business rules)`
- Change: extracted the retry policy into config, no behavior change →
  commit: `payments: extract retry policy to config (refactor, no
  behavior change)`

The commits are part of the deliverable. They will be reviewed by the
reviewer agent (Phase 5) and by humans on the PR.

**Scope discipline — non-negotiable:**

If you find yourself wanting to edit a file that was NOT in the committed
scope from Phase 2, STOP. Do not edit it silently.

Surface the situation to the user:
- Which file you want to touch
- What change is needed
- Why the original plan missed this

The user either:
- Approves the scope expansion (the plan is updated, you continue), or
- Rejects it (the divergence becomes a follow-up item, not part of this
  run).

Reason: PRs that grow silently mid-implementation become unreviewable. A
focused PR that needs a follow-up is better than a sprawling PR that's
nominally "done".

**Plan invalidation — when the approach itself fails:**

Scope discipline covers "I need one more file." This covers the bigger
break: implementation reveals that a load-bearing decision was wrong, or
the approach doesn't work. Do not improvise a new approach inside the
old plan — an approved plan the code no longer follows is fiction, and
conformance review will flag the divergence anyway. STOP and present:

- Which load-bearing decision failed, and what implementation revealed
  that planning didn't foresee.
- The options you see (including "revise the plan" and "abandon this
  route").

With approval, return to Phase 2 for a revised plan — a delta over the
approved one (what changes and why), not a full redo. Record the replan
in the log. Work that survives the new plan stays; work it invalidates
is reverted, not left half-aligned.

**Minimal solution — the Opus guard:**

Opus-family models tend to overdeliver. Keep the change the minimum the
task needs:
- No features, refactors, or "improvements" beyond what was asked — a
  bugfix doesn't need the surrounding code cleaned up.
- No docstrings, comments, or type annotations on code you didn't
  change.
- No defensive handling for scenarios that can't happen — validate at
  system boundaries, trust internal code.
- No helpers or abstractions for one-time operations, and no design for
  hypothetical future requirements.

The right amount of complexity is the minimum the current task needs;
anything past it is review surface without value.

## Phase 4: Test

Run the full local test suite.

**If tests fail:**
1. Read the failure output carefully.
2. Fix the issue.
3. Run tests again.
4. Repeat until ALL tests pass.

If the project has an eval regression suite (see `EVALS.md` if present),
and this change touches code covered by it, run the relevant subset.
Failures here are gates, same as unit tests.

Do NOT proceed to Phase 5 until tests are green.

Note: this is a LOCAL gate (fast feedback before opening PR). The CI in
the repository is the authoritative gate before merge. The local gate
exists to catch issues early, not to replace CI.

## Phase 5: Code Review

Use the Agent tool to dispatch the `reviewer` agent in isolated context
(it did not write this code — that independence is the point).

Before any dispatch, confirm the diff is non-empty — an empty diff
should fail here, not inside the reviewer.

**Default — one reviewer, all applicable lenses:**

- task: Run reviewer
- prompt: "Review this change set — obtain the diff yourself via git
  (this branch's committed work plus uncommitted changes). Load the
  applicable review-criteria skills per your routing table — the
  conditions are not restated here on purpose (an inlined copy
  drifts); conformance-review applies, and the approved Phase 2 plan
  it needs is pasted below. Report [BLOCKER]/[SHOULD]/[NIT]; do not
  edit.

  APPROVED PLAN (plus any approved replans/deltas and scope
  expansions):
  [paste the plan here]"

The plan is **pasted, not referenced**: the reviewer runs in isolated
context and cannot see this conversation, and a plan inferred from the
diff always matches the diff — circular. The same isolation is why the
diff instruction is git-based, never "this session".

**Large or critical diff — three parallel single-lens reviewers.** If the
diff exceeds roughly 400 changed lines or 10 files, or conformance will
trace multiple spec sections, dispatch three `reviewer` tasks in ONE
message (they run in parallel), each pinned to a single lens:

- prompt 1: "Apply ONLY general-code-review to this change set (obtain
  the diff via git: this branch's committed work plus uncommitted
  changes). Report [BLOCKER]/[SHOULD]/[NIT]; do not edit."
- prompt 2: "Apply ONLY constitution-compliance-review to this change
  set (obtain the diff via git: this branch's committed work plus
  uncommitted changes), against architecture/constitution.md. Report
  and do not edit."
- prompt 3: "Apply ONLY conformance-review to this change set (obtain
  the diff via git: this branch's committed work plus uncommitted
  changes), against the spec and the approved Phase 2 plan pasted
  below. Report and do not edit.

  APPROVED PLAN (plus any approved replans/deltas and scope
  expansions):
  [paste the plan here]"

Merge the reports: de-duplicate overlapping findings, keep the highest
severity for duplicates. (In this skill the plan gate is the human at
Phase 2; the `plan-review` reviewer gate belongs to the autonomous
`implement-backlog`, where a plan is always reviewed by a single
reviewer, never parallelized.)

**Wait for the review report(s).**

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
3. Repeat until the review passes.

**If you disagree with a finding:** don't silently ignore it, and don't
"fix" something you believe is correct just to satisfy the report.
Present the disagreement to the user — the finding, your reasoning,
what you'd do instead — and let the human arbitrate. A false positive
obeyed blindly damages the code; one ignored silently damages the
review's authority. Record the arbitration in the log.

Tests and review are sequential gates: any fix during review forces
re-running tests, because the fix may have broken something else.

## Phase 6: Close the loop

Only proceed once tests are green AND review is clean.

This phase exists because uncaptured learnings repeat and stale specs
propagate. Do not skip it.

For each item below, take action OR explicitly document that no action is
needed:

1. **Lessons** (`lessons.md`): append a terse, concrete entry if this run
   revealed a new pattern, pitfall, or recurring mistake.

2. **Spec**: if the implementation revealed that the spec is wrong,
   incomplete, or out of sync with reality, the skill MAY update the spec
   directly. In that case, mark the run as `requires_human_approval = true`
   and summarize the change in the final report. Spec is the source of
   truth for business behavior — any modification needs human PR approval
   before merge.

   Note on frequency by scenario:
   - **New capability / large feature:** spec update should be rare. If
     the spec was wrong, it should have been fixed before implementation
     started. When it does happen, treat it as a strong signal that the
     spec creation process needs review.
   - **Increment:** spec update is a normal possibility (rule clarified,
     regulation evolved, edge case codified).

3. **CLAUDE.md** (root or capability): if you found yourself
   repeating instructions or context that should be persistent, propose
   an addition (do not edit directly — surface the proposal in the final
   report).

4. **Backlog**: if this run resolved a backlog item or issue, prepare the
   status update (state transition, comment with PR link, close if
   applicable). If partially resolved, note remaining work.

## Phase 7: Open PR and Present Results

1. Push the work branch and open a PR. The description follows the
   shared template in
   `.claude/skills/implement-backlog/references/pr-template.md` —
   adapt the log path to this skill's, and the spec field (local runs
   may *update* the spec with human approval, not just propose). The
   **Approved plan** section carries the Phase 2 plan plus any
   approved replans, deltas, and scope expansions — it is what
   `/explain` and future readers pull intent from.
2. Report to the user in chat — short, because the PR description
   carries the detail: the PR link, a one-paragraph scope summary,
   the decisions that need their attention, and the human-approval
   flag (e.g. "spec updated in this PR — needs your review before
   merge").

Merging is the human's call: they are in the session, so there is no
monitoring phase here — CI and late comments are watched together.

## Structured logging

Throughout the run, append a structured log to
`.claude/logs/implement-{ISO timestamp}.md`. The full schema — one
section per phase with the fields each phase records — lives in
`references/log-template.md`: read it when you open the log at the
start of the run, and mirror its structure phase by phase.

The log exists for two reasons:
- Auditability when something goes wrong later.
- Input for future tuning of this skill.

## Common rationalizations

The shortcuts you'll be tempted to take to declare victory early. Each one
is the moment you become the human's problem instead of catching it
yourself.

| Rationalization | Reality |
|-----------------|---------|
| "The tests pass, so it's done" | Tests you wrote alongside the code tend to confirm the implementation, not the spec. Green proves "works as I tested," not "works as specified." |
| "The approach is obvious, I'll skip framing the load-bearing decisions" | Obvious-and-rushed is exactly when the wrong approach ships. Name the load-bearing decisions even when they feel settled. |
| "I'll run the full checks at the end" | Run lint + touched tests every chunk. End-only batching turns one red bar into a bisecting session and lets bad chunks pile up. |
| "This extra file is a tiny scope bump, I'll just edit it" | Silent scope growth makes a PR unreviewable. Surface it; a focused PR with a follow-up beats a sprawling one. |
| "The spec is a little off but I'll code around it" | A spec mismatch is a business-rule signal. Update the spec (flag `requires_human_approval`) or open a follow-up — don't quietly diverge. |
| "I re-read my own code, it's fine" | You review with the blind spots you wrote with. The reviewer in isolated context (Phase 5) is the real check, not your re-read. |

## Critical rules

The phases above carry their own gates and reasons; these four are the
cross-cutting invariants worth restating:

- **Run interactively only** — plain, or under a supervised `/goal`
  (gates pause the turn; answers enter the transcript). Under headless
  `/goal` (`claude -p`) no one answers, so the gates are silently
  overrun — headless autonomy belongs to `implement-backlog`, never
  here.
- **Dispatch the reviewer via the Agent tool, in isolated context** — a
  reviewer that didn't write the code is the entire point of Phase 5.
- **Stop after 3 attempts at the same failure** and present the
  situation: repeated blind retries burn budget and usually mean the
  approach, not the fix, is wrong.
- **Any spec change marks the run `requires_human_approval = true`** in
  the final report — the spec is the business source of truth, and no
  silent edit to it ever ships.

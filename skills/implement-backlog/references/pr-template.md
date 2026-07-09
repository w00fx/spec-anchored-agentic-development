# PR description template — implement-backlog runs

Open every PR with this description structure. It is what the human
reviews against — and, via the Approved-plan section, where a session
without this conversation (`/explain` on the PR, a later conformance
pass) pulls the intent from.

```markdown
## [Issue title / reference]

Closes #[issue number]

### Scope
[What was done, mapped to the issue]

### Approved plan (Phase 2, plus any approved deltas)
[The plan as approved: steps with rationale, committed file scope,
load-bearing decisions — and any revisions approved during the run]

### Files changed
[List with brief description of each]

### QA Results
- Tests: ✅ [N passed, 0 failed]
- Code Review: ✅ [summary]

### Loop closure
- Lessons added: [yes/no, with summary]
- Spec correction proposed: [no / summary]
- CLAUDE.md changes proposed: [yes/no, with summary]

### Human approval required
[yes/no — reason]

### Commits
[List]

### Log
.claude/logs/implement-backlog-{timestamp}.md
```

Field notes:
- **Approved plan** is the plan's public home. Phase 2 records the plan
  in the run log *and* here — this section is what future readers with
  no access to the run's conversation anchor on.
- **Spec correction proposed** pairs with `requires_human_approval =
  true` (Phase 6): the proposal needs an explicit human decision at PR
  review, not a routine skim.
- **Human approval required: yes** also means applying the
  `human-approval-required` label (or the repo convention).

## After opening — monitor until landed (autonomous runs)

- **CI to completion**, not just the first green: a check can go
  green then flip red as the full pipeline runs (the green-minute
  rule) — wait for the pipeline to settle.
- **Late comments.** From an *external review tool*: advisory — they
  inform the human who approves the merge; the loop does not wait on
  them, abort on them, or count them in the completion condition
  (what gates is Phase 5 + CI; an external reviewer's precision is
  not reliable enough to block). From a *human*: address them if in
  scope; if they need a decision only a human can make, leave the PR
  for human resolution and stop.
- **Merge conflicts:** if the base branch moved, rebase/resolve and
  re-run the QA gates (Phase 4 → Phase 5) — resolving a conflict is
  a code change.
- Something fixable in scope → fix and re-run the affected gates.
  Out of scope or needing human judgment → comment on the PR/issue
  naming exactly what blocks, and stop — never mark done around an
  unresolved check.
- Operationally: monitoring runs against the GitHub API; until
  auto-merge by class exists (`AUTONOMY-PLAYBOOK.md`, Milestone 4), a
  human merges — the run's job ends at "PR green, reviewed, nothing
  outstanding." 

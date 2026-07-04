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

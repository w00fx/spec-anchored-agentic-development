# Log template — implement-backlog runs

The skill appends one log per run to
`.claude/logs/implement-backlog-{ISO timestamp}.md`. Mirror this
schema: one section per phase, fields filled as each phase completes —
not reconstructed at the end.

```markdown
# Implement-backlog run — [ISO timestamp]

## Trigger
- Issue: [reference]
- Source: [webhook / manual]

## Phase 1: Understand
- Issue summary: [...]
- Target capability: [...]
- Spec read: [reference]
- Files identified: [list]
- Scope routing: [proceed / aborted to implement-feature]

## Phase 1.5: Ambiguities
- Detected: [yes/no — list if yes]
- Outcome: [proceed / aborted with comment]

## Phase 2: Plan
- Steps: [N]
- Committed file scope: [list]
- Plan review: [approved at iteration N / aborted at iteration N]

## Phase 3: Implement
- Scope expansion attempts: [none / aborted with comment]
- Files edited: [list]
- Commits: [list of commit messages]

## Phase 4: Test
- Suite: [pass/fail counts]
- Iterations: [N]
- Outcome: [green / aborted at iteration N]

## Phase 5: Review
- Report summary: [...]
- Iterations: [N]
- Outcome: [clean / aborted at iteration N]

## Phase 6: Close loop
- Lessons: [...]
- Spec correction proposed: [no / summary]
- CLAUDE.md proposed: [...]

## Phase 7: PR
- PR URL: [...]
- Human approval required: [yes/no — reason]
- Issue comment posted: [yes/no]
```

Field notes:
- Every `Outcome: aborted` pairs with a **named blocker** posted as a
  comment on the issue (needs-refinement / scope-expansion-needed /
  qa-blocked / review-blocked) — the terminal state the `/goal`
  condition reads.
- There are no `Replans` or `Disputed findings` fields here by design:
  with no human mid-run to approve a replan or arbitrate a finding, the
  autonomous skill aborts instead.

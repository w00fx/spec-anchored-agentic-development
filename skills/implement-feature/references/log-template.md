# Log template — implement-feature runs

The skill appends one log per run to
`.claude/logs/implement-{ISO timestamp}.md`. Mirror this schema: one
section per phase, fields filled as each phase completes — not
reconstructed at the end.

```markdown
# Implement run — [ISO timestamp]

## Phase 1: Understand
- Input: [user instruction summary]
- Spec / issue read: [reference]
- Target capability: [name]
- Scenario: [capability / large feature / increment]
- Files identified: [list]

## Phase 1.5: Ambiguities
- [Ambiguity → resolution]

## Phase 2: Plan
- Steps: [N]
- Committed file scope: [list]

## Phase 3: Implement
- Scope changes: [none / list of approved expansions]
- Replans: [none / delta summary of revised plan]
- Files edited: [list]
- Commits: [list of commit messages]

## Phase 4: Test
- Suite: [pass/fail counts]
- Iterations: [N]

## Phase 5: Review
- PR: [link]
- Report summary: [...]
- Disputed findings: [none / finding → arbitration outcome]
- Iterations: [N]

## Phase 6: Close loop
- Lessons: [...]
- Spec: [updated yes/no — summary]
- CLAUDE.md: [...]
- Backlog: [...]

## Phase 7: Done
- Total iterations across QA: [N]
- Human approval required: [yes/no — reason]
```

Field notes:
- `Replans` — any Phase 3 → Phase 2 return: record the delta over the
  approved plan, not the full new plan.
- `Disputed findings` — review findings you contested, each with the
  human's arbitration outcome.

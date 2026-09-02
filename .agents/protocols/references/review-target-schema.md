# Exact candidate and hardening handoffs

The two internal authoring agents work from immutable input identities in
isolated worktrees. Their commits are proposals until the Owner inspects and
accepts them.

`hardening-target.json`:

```json
{
  "run_id": "RUN-…",
  "role": "general-code-reviewer | mutation-hardener",
  "base_sha": "…",
  "input_candidate_sha": "…",
  "diff_sha256": "…",
  "spec_corpus_sha256": "…",
  "plan_sha256": "…",
  "scope_manifest_sha256": "…",
  "evidence_manifest_sha256": "…"
}
```

`general-code-handoff.json`:

```json
{
  "target_sha256": "…",
  "status": "CODE_HARDENED | NO_CHANGES_NEEDED | BLOCKED",
  "output_commit_sha": "…",
  "changed_paths": [],
  "changes": [],
  "verification": [],
  "remaining_risks": [],
  "owner_review_required": true
}
```

`mutation-handoff.json`:

```json
{
  "target_sha256": "…",
  "status": "MUTATION_HARDENED | MUTATION_NOT_APPLICABLE | BLOCKED",
  "output_commit_sha": "…",
  "eligible_target": [],
  "coverage": {"line_percent": 100, "branch_percent": 100},
  "mutation": {
    "generated": 0,
    "killed": 0,
    "equivalent_candidates": 0,
    "tooling_limitation_candidates": 0,
    "actionable_survivors": 0
  },
  "changed_paths": [],
  "changes": [],
  "verification": [],
  "owner_review_required": true
}
```

`owner-disposition.json` records, for each handoff, the inspected input/output
identity, accepted/rejected changes, integrated commit, rationale, and rerun
commands.

The final candidate is valid only when:

- the Owner accepted both applicable handoffs;
- the mutation report names the exact final candidate;
- all required deterministic evidence is green;
- any edit after mutation hardening returns to both internal passes.

External review reports are separate pipeline artifacts bound to the final PR
head. They never replace Owner inspection of authoring-agent changes.

## Worker terminal binding

`PR_READY_AWAITING_HUMAN` binds the exact final candidate to:

```text
general_hardening_report_sha256
mutation_hardening_report_sha256
owner_disposition_sha256
```

The worker terminal deliberately carries no independent-review report or seal.
External reviews are separate pipeline artifacts and must name the current PR head.
`NO_CHANGE_REQUIRED` uses `no_change_corroboration_sha256` for the internal
no-change search report.

# Install

This bundle turns a coding agent into the system described in `GUIDELINE.md`
(English, canonical): capability-organized, spec-anchored development;
implementation skills, a reviewer agent with criteria lenses, and the native
`/goal` loop.

Copy the `.claude/` folder into your repository root and the root-level
documents wherever your team keeps them. Read `GUIDELINE.md` first;
`AUTONOMY-PLAYBOOK.md` when you start widening autonomy.

## Where each file goes

| File | What it is |
|---|---|
| `GUIDELINE.md` | The system — read this first |
| `AUTONOMY-PLAYBOOK.md` | Milestones 1-4, Tier 1/2 metrics, per-class auto-merge |
| `sources-and-learnings.md` | Source catalog + decision record |
| `CLAUDE-codebase-exploration-block.md` | Paste into your root CLAUDE.md (example tool stack — swap in yours) |
| `spec-templates/capability-spec.md` | The permanent capability-spec template (EARS + GWT + reference values) |
| `.claude/skills/implement-feature/SKILL.md` | LOCAL workflow (7 phases, human gates; interactive only — plain or supervised `/goal`, never headless) |
| `.claude/skills/implement-feature/references/log-template.md` | Log schema for the skill's runs (read when opening the run log) |
| `.claude/skills/implement-backlog/SKILL.md` | AUTONOMOUS workflow (named-blocker aborts; runs under headless `/goal`) |
| `.claude/skills/implement-backlog/references/log-template.md` | Log schema for autonomous runs (read when opening the run log) |
| `.claude/skills/implement-backlog/references/pr-template.md` | Shared PR playbook: description template both implement skills use (Approved plan = the plan's public home) + post-open monitoring for autonomous runs |
| `.claude/skills/implement-backlog/references/rationalizations.md` | The eight shortcuts autonomous runs rationalize, with realities (read at run start) |
| `.claude/agents/reviewer.md` | The reviewer subagent (isolated context, report-only by tools allowlist; loads criteria lenses per its routing table) |
| `.claude/skills/plan-review/SKILL.md` | Lens: approach soundness before code |
| `.claude/skills/general-code-review/SKILL.md` | Lens: correctness, simplicity, tests, types, commits |
| `.claude/skills/general-code-review/references/test-standards.md` | Shared test bar (GOOD/BAD pairs + mocking boundary rule) — the lens judges by it, both implement skills write to it |
| `.claude/skills/general-code-review/references/smell-baseline.md` | Twelve Fowler smells with fixes (repo overrides; capped at [SHOULD]) |
| `.claude/skills/constitution-compliance-review/SKILL.md` | Lens: domain invariants vs `architecture/constitution.md` |
| `.claude/skills/conformance-review/SKILL.md` | Lens: diff vs spec (value by value) and vs the approved plan |
| `.claude/commands/implement.md` | Local entry point → implement-feature |
| `.claude/commands/review.md` | On-demand reviewer dispatch (report-only) |
| `.claude/commands/explain.md` | Post-implementation walkthrough → `docs/walkthroughs/` |
| `.claude/commands/shape.md` | Work-shaping interview (spec from idea/transcript/code; grill-back refine; task sharpening) |
| `.claude/commands/spec-to-tickets.md` | Spec → tracer-bullet tickets with blocking edges (quiz before publish; tickets.md or GitHub Issues) |
| `.claude/commands/plan-from-issue.md` | Phased plan from a GitHub issue (Plan Mode; no implementation) |
| `.claude/commands/review-spec-drift.md` | Periodic whole-capability spec ↔ code drift audit (report-only) |
| `.claude/rules/package-by-feature.md` | Always-loaded rule: capability-vs-entity tests at file-creation time |
| `.claude/hooks/require-spec-for-new-capability.sh` | Example poka-yoke hook (opt-in): blocks a new `src/<x>/` without `specs/<x>/` — wiring snippet in its header |
| `.claude/routines/frontier-worker.md` | Canonical Routine prompt: scans the frontier (`auto-implement`, blockers done, not `in-flight`), claims one issue, runs the headless `/goal` |

## What you still have to build (project-specific)

- `architecture/constitution.md` — your non-negotiable domain invariants
- `specs/<capability>/…` — your capability specs (start with `/shape`)
- `architecture/pipeline.md` — capability map and contracts (if applicable)
- A testing strategy — pyramid, contract tests, golden datasets
- `EVALS.md` — the eval suite (Milestone 1; see the playbook)
- CI wiring — the four minimum gates, plus deterministic security gates
  (SAST / SCA / secret scanning)
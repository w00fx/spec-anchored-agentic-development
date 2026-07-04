# Installing Spec-Anchored Agentic Development

This bundle turns a coding agent into the system described in `GUIDELINE.md`
(English, canonical): capability-organized, spec-anchored
development; implementation skills, a reviewer agent with criteria lenses, and
the native `/goal` loop. Everything here is Markdown.

The specs-and-context layer (Parts 1-2 of the guideline) is tool-portable
(Claude Code, Codex, Kiro, OpenCode, Cursor). The automation layer (skills,
reviewer, `/goal`) is implemented for Claude Code; in another tool, map each
piece to its equivalent (the guideline's "Two layers" note explains how).

## Where each file goes

The bundle folders live at this repository's top level (`skills/`,
`commands/`, `agents/`, `rules/`, `hooks/`). Install them under `.claude/`
in your repository (project-level) or under `~/.claude/` (user-level), and
the spec template under `specs/_template/`:

```bash
# from your repository root
mkdir -p .claude specs/_template
cp -R <path-to-bundle>/{skills,commands,agents,rules,hooks} .claude/
cp <path-to-bundle>/spec-templates/capability-spec.md specs/_template/
```

| Installed path | What it is |
|---|---|
| `.claude/skills/implement-feature/SKILL.md` | LOCAL workflow (7 phases, human gates; interactive only — plain or supervised `/goal`, never headless) |
| `.claude/skills/implement-feature/references/log-template.md` | Log schema for the skill's runs (read when opening the run log) |
| `.claude/skills/implement-backlog/SKILL.md` | AUTONOMOUS workflow (named-blocker aborts; runs under headless `/goal`) |
| `.claude/skills/implement-backlog/references/log-template.md` | Log schema for autonomous runs (read when opening the run log) |
| `.claude/skills/implement-backlog/references/pr-template.md` | PR description template for autonomous runs (the Approved-plan section is the plan's public home) |
| `.claude/agents/reviewer.md` | Reviewer sub-agent — router + single-lens mode |
| `.claude/skills/plan-review/SKILL.md` | Plan-gate criteria (incl. capability-vs-entity test for new folders) |
| `.claude/skills/general-code-review/SKILL.md` | Generic criteria — correctness, simplicity, tests, types, structure |
| `.claude/skills/constitution-compliance-review/SKILL.md` | Contextual criteria — the project constitution |
| `.claude/skills/conformance-review/SKILL.md` | Contextual criteria — diff vs capability spec / vs approved plan |
| `.claude/commands/implement.md` | Local entry point → `implement-feature` |
| `.claude/commands/review.md` | On-demand reviewer — report-only |
| `.claude/commands/explain.md` | Post-implementation walkthrough → `docs/walkthroughs/` |
| `.claude/commands/interview-spec.md` | Spec-creation interview → writes `specs/<capability>/<capability>.md` |
| `.claude/commands/plan-from-issue.md` | Phased plan from a GitHub issue (Plan Mode; no implementation) |
| `.claude/commands/review-spec-drift.md` | Periodic whole-capability spec ↔ code drift audit (report-only) |
| `.claude/rules/package-by-feature.md` | Always-loaded rule: capability-vs-entity tests at file-creation time |
| `.claude/hooks/require-spec-for-new-capability.sh` | Example poka-yoke hook (opt-in): blocks a new `src/<x>/` without `specs/<x>/` — wiring snippet in its header |
| `specs/_template/capability-spec.md` | THE spec template (one type, permanent, EARS + Given/When/Then + reference values) |

## Project-level files

| File | Suggested home | What it is |
|---|---|---|
| `GUIDELINE.md` | `docs/` | The system's design doc — read this first |
| `AUTONOMY-PLAYBOOK.md` | `docs/` | The widening path of autonomy: Milestones, Tier 1/2 validation, per-class auto-merge — read when ready to widen |
| `sources-and-learnings.md` | `docs/` | Source catalog, named concepts, backlog, verification appendix |

## The spec model

There is **one spec type — the capability spec, always permanent** (business
rules in EARS with cited sources, acceptance criteria in Given/When/Then,
reference values for calculations). There is no disposable feature spec: a
large feature is carried by a larger Phase 2 plan (disposable), any new
business rule it introduces is merged into the capability spec (human
approval), and the durable understanding goes to the `/explain` walkthrough.

## The autonomy model

Autonomy is a **gradient, not a switch**. The narrow start needs no formal
eval suite: issues → hard-coded allowlist of trivial classes → **CI green
mandatory** → PR → **a human approving every PR** (the human is the last
line, not the only one). Widening — more classes, volume, auto-merge —
requires the regression suite with a track record (`AUTONOMY-PLAYBOOK.md`).
Normative calculations never enter autonomy before golden/conformance exists.

## What you still have to build (project-specific)

- **The constitution** — your non-negotiable domain rules.
- **The specs** — one per capability, from the template.
- **`pipeline.md`** or equivalent — contracts between capabilities.
- **A testing strategy** — pyramid, contract tests, golden datasets.
- **Your eval suite (`EVALS.md`)** — required to *widen* autonomy, not to
  start it narrow.
- **Deterministic security gates** — SAST / SCA / secret scanning in CI.
- **The autonomous trigger** — `.github/workflows/auto-implement.yml`; the
  skeleton is in `GUIDELINE.md` Part 3, and it is conceptual: verify against
  the current Claude Code headless / GitHub Action docs before relying on it.

## Order of adoption

1. Read `GUIDELINE.md`. The floor is **one spec file** — start there.
2. Write the first capability spec from the template; add the constitution
   when invariant rules demand it.
3. Run the first feature locally — the recommended invocation is a
   **supervised `/goal`** wrapping `implement-feature` (recipes in Part 3).
4. Use `/explain` after, and pay down cognitive debt (active recall).
5. Autonomous mode starts narrow (allowlist + green CI + human approving
   every PR); widen only as the suite earns trust (`AUTONOMY-PLAYBOOK.md`).

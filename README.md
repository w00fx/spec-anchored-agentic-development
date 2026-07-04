# Spec-Anchored Agentic Development

> One permanent spec per capability, and the code answers to it — evidence before "done".
> A methodology, and a ready-to-install bundle, for building software with AI coding agents:
> from a single spec file to supervised autonomy.

This repository is my agentic development workflow. It is both a **guideline** (how to work) and an **installable bundle** (the skills, commands, agents, rules, and templates that make a coding agent actually work this way). It targets Claude Code but the specs-and-context layer is portable to any coding agent (Codex, Cursor, Kiro, OpenCode).

It is maintained as a living reference — when practice conflicts with what's written here, the document is updated, not silently worked around.

---

## The core idea

**Spec-anchored**: the business decision comes before the code, and the spec *stays*. It is the permanent source of truth the code answers to — drift is treated as a bug, conformance is checked value by value — not scaffolding discarded once a feature ships.

Where this sits in the field (per the consolidating taxonomy in [*"Spec-Driven Development: From Code to Contract"*](https://arxiv.org/abs/2602.00180), 2026, echoed by [martinfowler.com's exploring-gen-ai series](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)):

- **spec-first** — the spec precedes the code but may drift or be discarded (Kiro, Spec Kit).
- **spec-anchored** — the spec is permanent and the code answers to it continuously. **← this is where this methodology sits.**
- **spec-as-source** — code is generated from the spec. For normative rules, the spec's reference values generate the golden tests that act as the oracle, moving toward this.

The unit of organization is the **capability** — a cohesive slice of what the system *does* for the business (payments, orders, notifications), never a technical layer (controllers, repositories) or a bare entity (Product, Customer). You write one permanent spec per capability, develop from it, and progress in autonomy.

## Five fundamental principles

1. **Simplest possible change.** Delete before you add. No unrequested refactors, no speculative helpers.
2. **Root cause, not band-aid.** Find why a bug happens; don't hide the symptom.
3. **Verification is part of the work, not optional.** Every change needs a way to verify it. If you can't verify it, don't merge it.
4. **Determinism where you can, agent where you must.** Every predictable task becomes a deterministic script the agent calls — the agent is expensive and non-deterministic; a script is cheap and auditable.
5. **Machine-produced "no" before human review.** Every gate the machine can run (failing test, type error, lint rule, reviewer objection) fires before a human is asked to look. This is *backpressure* — the check confronts the agent at the boundary.

## The trajectory

```
Identify capabilities → Specification → Development
                                            ↓
                          Operational maturity → Autonomy (narrow start → widening)
```

**The minimum entry point is one spec file.** You do not need the constitution, the reviewer, the milestones, or the rituals to begin — write a single `specs/<capability>/<capability>.md` and start. Everything else is how the system *scales*; each piece enters when its pain shows up.

## Autonomy is a gradient, not a switch

The narrow start needs no formal eval suite: issues → hard-coded allowlist of trivial classes → **CI green mandatory** → PR → **a human approving every PR**. Widening — more classes, more volume, any step toward auto-merge — requires a regression suite with a track record. Normative calculations never enter autonomy before golden/conformance verification exists. The four-Milestone widening path (Tier 1 static gates, Tier 2 dynamic validation, per-class auto-merge) lives in [`AUTONOMY-PLAYBOOK.md`](AUTONOMY-PLAYBOOK.md).

---

## What's in this repository

### Documents (the methodology)

| File | What it is |
|------|------------|
| [`GUIDELINE.md`](GUIDELINE.md) | The source of truth for **how to work** — the full methodology, Parts 1–7. Read this first. |
| [`AUTONOMY-PLAYBOOK.md`](AUTONOMY-PLAYBOOK.md) | The widening path of autonomy: the four Milestones, Tier 1/2 validation, per-class auto-merge. Read when ready to widen. |
| [`INSTALL.md`](INSTALL.md) | Where each bundle file goes and the recommended order of adoption. |
| [`sources-and-learnings.md`](sources-and-learnings.md) | Every external source mined while designing the methodology, what each contributed, what was rejected and why — the audit trail of *why the system is the way it is*. |

### The bundle (drop into `.claude/` and `specs/`)

| Path | What it is |
|------|------------|
| `skills/implement-feature/` | **Local** 7-phase workflow with human confirmation gates (interactive; plain or supervised `/goal`, never headless). |
| `skills/implement-backlog/` | **Autonomous** workflow with named-blocker aborts; runs under headless `/goal`, triggered by an `auto-implement` label. |
| `skills/plan-review/` | Reviewer criteria: plan approach soundness (incl. the capability-vs-entity test for new folders). |
| `skills/general-code-review/` | Reviewer criteria: correctness, simplicity/reuse, test quality, type design — the default lens. |
| `skills/constitution-compliance-review/` | Contextual reviewer criteria: the project constitution (numeric types, audit trail, source citation, stage boundaries, past-period rules). |
| `skills/conformance-review/` | Contextual reviewer criteria: diff vs capability spec, and diff vs approved plan. |
| `agents/reviewer.md` | The independent reviewer agent — a **router** that loads the criteria skills that fit what it's handed and reports findings; it never edits. |
| `commands/implement.md` | Local entry point → `implement-feature`. |
| `commands/review.md` | On-demand reviewer, report-only. |
| `commands/explain.md` | Post-implementation walkthrough → `docs/walkthroughs/`. |
| `commands/interview-spec.md` | Spec-creation interview → writes `specs/<capability>/<capability>.md`. |
| `commands/plan-from-issue.md` | Phased implementation plan from a GitHub issue (Plan Mode; no implementation). |
| `commands/review-spec-drift.md` | Periodic whole-capability spec ↔ code drift audit. |
| `rules/package-by-feature.md` | Always-loaded rule: the capability-vs-entity tests applied at file-creation time. |
| `hooks/require-spec-for-new-capability.sh` | Opt-in poka-yoke hook: blocks a new `src/<x>/` without a matching `specs/<x>/`. |
| `spec-templates/capability-spec.md` | **The** spec template — one type, permanent (EARS rules + Given/When/Then criteria + reference values). |

## The two workflows

Both run the same **Plan → Implement → QA → Close the loop** cycle; they differ in who holds the gate.

- **`implement-feature`** (local, human-driven) — seven phases with human confirmation gates after Understand, Resolve-ambiguities, and Plan. A question at a gate pauses the turn. Recommended invocation for anything with acceptance criteria: a **supervised `/goal`** that keeps the human gates *and* stops the worker from declaring itself done — a fresh evaluator re-checks the completion condition against the transcript each turn, demanding evidence rather than claims.

- **`implement-backlog`** (autonomous, agent-driven) — the persistence engine is Claude Code's native `/goal`; a thin GitHub Action runs it headless on an `auto-implement` label. There is no one to answer a gate, so every would-be question becomes a **named-blocker abort** (out-of-scope, needs-refinement, scope-expansion-needed, qa-blocked, review-blocked) and human judgment moves to the ends — the issue's acceptance criteria before the run, the PR review after. Scope is restricted to increments; new capabilities and large features route back to `implement-feature`.

Review (Phase 5, and the autonomous plan gate) is never inlined — it dispatches the independent `reviewer` agent in isolated context that did **not** write the work under review, because a fresh context doesn't share the author's blind spots.

## Installation

See [`INSTALL.md`](INSTALL.md). In short: copy the bundle folders into your repository's `.claude/` (or `~/.claude/`), keep `specs/` and `docs/` centralized, and put a `CLAUDE.md`/`AGENTS.md` next to each capability's code pointing at its spec. Then:

1. Read [`GUIDELINE.md`](GUIDELINE.md). The floor is **one spec file** — start there.
2. Write the first capability spec from the template; add the constitution when invariant rules demand it.
3. Run the first feature locally with a **supervised `/goal`** wrapping `implement-feature`.
4. Use `/explain` afterward.
5. Turn on autonomous mode narrow (allowlist + green CI + human approving every PR); widen only as your eval suite earns trust.

## Portability

The methodology has two layers that travel differently:

- **Specs and context** (Parts 1–2 of the guideline) — capabilities, specs, the `AGENTS.md`/`CLAUDE.md` files, the constitution. **Tool-portable**: any coding agent reads them.
- **Automation** (Parts 3–5) — the implementation skills, the reviewer, `/goal`, the autonomy trajectory. **Implemented for Claude Code**; in another tool, map each piece to its equivalent (`/goal` → that tool's loop primitive, skills → its agent/workflow definitions, `.claude/rules/` → its always-loaded rules).

## License

[MIT](LICENSE).

---

*This document exists to serve the work, not to govern it. When a rule here causes more friction than value, change it — consciously, with a commit and a reason. Silent erosion of discipline is what kills systems like this.*

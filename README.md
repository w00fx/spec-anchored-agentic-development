# Spec-Anchored Agentic Development

> One permanent spec per capability, and the code answers to it — evidence before "done".
> A methodology, and a ready-to-install bundle, for building software with AI coding agents:
> from a single spec file to supervised autonomy.

This repository is my agentic development workflow. It is both a **guideline** (how to work) and an **installable bundle** (the protocol, skills, commands, agents, rules, policies, routines, executable contracts and templates that make a coding agent actually work this way). It targets Claude Code, but the specs-and-context layer is portable to any coding agent, and `adaptations/` maps the rest onto Codex and Kiro.

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

The narrow start needs no formal eval suite: issues → hard-coded allowlist of trivial classes → **CI green mandatory** → PR → **a human approving every PR** — over a safety baseline that cannot wait (branch protection, scoped credentials, no direct push, one issue → one PR, named blockers, human merge). Widening — more classes, more volume, any step toward auto-merge — requires a regression suite with a track record. Normative calculations never enter autonomy before golden/conformance verification exists. The widening path lives in [`AUTONOMY-PLAYBOOK.md`](AUTONOMY-PLAYBOOK.md), which splits the last step honestly: **M4a** is machine *approval eligibility* (the human still merges); **M4b** is platform auto-merge, a much higher bar.

---

## What's in this repository

### Documents (the methodology)

| File | What it is |
|------|------------|
| [`GUIDELINE.md`](GUIDELINE.md) | The source of truth for **how to work** — the full methodology, Parts 1–7. Read this first. |
| [`AUTONOMY-PLAYBOOK.md`](AUTONOMY-PLAYBOOK.md) | The widening path of autonomy: the Milestones, Tier 1/2 validation, per-class approval eligibility. Read when ready to widen. |
| [`INSTALL.md`](INSTALL.md) | Where each bundle file goes and the recommended order of adoption. |
| [`EVALS.template.md`](EVALS.template.md) | The eval-case schema and the initial case index — copy to `EVALS.md` when you start qualifying. |
| [`sources-and-learnings.md`](sources-and-learnings.md) | Every external source mined while designing the methodology, what each contributed, what was rejected and why — the audit trail of *why the system is the way it is*. |
| [`CLAUDE-codebase-exploration-block.md`](CLAUDE-codebase-exploration-block.md) | A codebase-exploration block to paste into your root context file (example tool stack — swap in yours). |
| [`adaptations/`](adaptations/) | Running the system elsewhere: `kiro.md`, `codex.md` (harness-class peer, near-1:1 port), and `claude-plus-codex.md` (both harnesses on one repo). |

### The protocol and its three adapters

One state machine, three modes. `protocols/implementation-protocol.md` holds phases 0–9, the terminal taxonomy, the invariants and the logging; each skill is a **mode adapter** that declares only *who satisfies each gate*.

| Path | What it is |
|------|------------|
| `protocols/implementation-protocol.md` | The shared state machine — preflight, proven delta, understand, plan, implement, verify, durable sync, seal, review, deliver. Terminals: `PR_READY_AWAITING_HUMAN`, `NAMED_BLOCKER`, `NO_CHANGE_REQUIRED`. A run never claims the merge. |
| `protocols/references/scope-manifest-schema.md` | The run's mechanical-scope proposal: allowed and denied paths, permissions, typed truth grants. |
| `protocols/references/review-target-schema.md` | Review target and seal schemas — the candidate the reviewer judged is the candidate that ships. |
| `skills/implement-feature/` | **Supervised-local** adapter — the human satisfies every gate in-session. |
| `skills/implement-orchestrated/` | **Orchestrated-worker** adapter — one ticket, one worktree, one PR; gates satisfied through GitHub. |
| `skills/implement-backlog/` | **Unattended** adapter — every gate has a mechanical provider or aborts as a named blocker. Its `references/` carry the shared PR template and the rationalizations table. |

### The review lenses and the reviewer

| Path | What it is |
|------|------------|
| `agents/reviewer.md` | The fresh-context reviewer — pinned to the strong model at max effort, run in a disposable worktree with no push credentials, loading the lenses that fit what it's handed. It reports; it never edits. |
| `skills/plan-review/` | Lens: approach soundness before code. |
| `skills/general-code-review/` | Lens: correctness, simplicity/reuse, test quality, type design — the default. Its `references/` carry the shared test bar and the smell baseline. |
| `skills/constitution-compliance-review/` | Lens: the project constitution (numeric types, audit trail, source citation, stage boundaries). |
| `skills/conformance-review/` | Lens: diff vs capability spec, and diff vs the approved plan. |
| `skills/ticket-readiness-review/` | Lens: the ticket as an executable contract, before a worker is ever dispatched. |

### Commands

| Path | What it is |
|------|------------|
| `commands/shape.md` | The work-shaping interview — an idea, a transcript, existing code, or an existing spec. The interview only. |
| `commands/to-spec.md` | Writes or updates the capability spec from that interview. Never interviews back; gaps become open questions. |
| `commands/spec-to-tickets.md` | Breaks a ratified spec into tracer-bullet tickets with explicit blocking edges; quizzes the human before publishing. |
| `commands/prep.md` | One-time repository prep: the `check` / `check-<capability>` / `golden` interface, the metric-class gates, the golden harness, minimum CI, the ratchet baseline. |
| `commands/orchestrate.md` | Whole-project orchestration in resolution-gated waves over the explicit issue graph — one worker per ticket, a fingerprinted CI-and-review monitor, and the human merging every PR. |
| `commands/plan-from-issue.md` | Phased implementation plan from a GitHub issue (no implementation). |
| `commands/review.md` | On-demand reviewer dispatch, report-only. |
| `commands/review-spec-drift.md` | Periodic whole-capability spec ↔ code drift audit. |
| `commands/explain.md` | Post-implementation walkthrough → `docs/walkthroughs/`. |
| `commands/implement.md` | Discoverability redirect — the transactional adapters are user-invocation-only, so it points you at the direct invocation. |

### Authorization, contracts and the gate

| Path | What it is |
|------|------------|
| `scripts/spec-anchored` | **Executable contracts**, dependency-free and fail-closed: canonicalization, the APPROVAL-FINGERPRINT over the approval bundle, scope validation under a policy floor, and the strict terminal union. Doctrine that used to be prose, as code that refuses. |
| `policy/` | The **authorization floor** — four versioned profiles plus the instances a launcher issues. A worker never writes one, and `validate-scope` refuses to judge a diff without one. |
| `rules/truth-layer.md` | Always-loaded rule: `specs/**`, the golden tests and the ratchet baseline are read-only outside their named flows. |
| `rules/package-by-feature.md` | Always-loaded rule: the capability-vs-entity tests, applied at file-creation time. |
| `hooks/require-spec-for-new-capability.sh` | Opt-in poka-yoke hook: blocks a new `src/<x>/` without a matching `specs/<x>/`. |
| `routines/frontier-worker.md` | Launcher routine: scan the frontier, claim one issue under a lease, spawn the child session, validate the structured terminal from outside the transcript. |
| `spec-templates/capability-spec.md` | **The** spec template — one type, permanent: authority frontmatter, normative behavior by truth type, Given/When/Then criteria, reference values, and typed stable IDs throughout. |
| `scripts/check-all.sh` | **The single gate.** Compiles the artifacts, parses every shell script, runs the structural validator and all four suites, and checks the Codex port for drift. |
| `tests/` | 308 fixtures — kernel contracts, adversarial bypasses, corpus fixtures — plus mutation adequacy: 52 injected regressions, each of which a fixture must catch. |

## The three modes

All three run the same protocol. They differ only in who answers.

- **`implement-feature`** — local and interactive. You resolve ambiguity, you approve the plan (and its APPROVAL-FINGERPRINT), you approve any scope change; a semantic amendment to a spec is possible here, behind an explicit in-session gate, and the PR ratifies it.

- **`implement-orchestrated`** — one autonomous worker per ticket, dispatched by `/orchestrate` into its own worktree. Its gates live on GitHub: the plan is posted as an issue comment and the run **stops** until a human replies `approved <fingerprint>`; ambiguity is a comment plus a label, never a guess.

- **`implement-backlog`** — headless. No one is there to answer, so every gate has a mechanical provider or aborts with a named blocker (`AMBIGUITY`, `MISSING_ORACLE`, `TRUTH_CONFLICT`, `SCOPE_VIOLATION`, `SPEC_CHANGE_REQUIRED`, `SPEC_STALE`, `GRAPH_DECISION_REQUIRED`, `ENVIRONMENT`, `REPEATED_FAILURE`). Scope is increments only; new capabilities and large features stay human-led.

Two things hold across all three. The review (protocol Phase 8) is never inlined — it goes to a reviewer that did **not** write the work, because context separation removes authoring carryover. And no run ever merges: every mode ends at `PR_READY_AWAITING_HUMAN`, and a human decides.

## Installation

See [`INSTALL.md`](INSTALL.md). In short: copy the bundle folders into your repository's `.claude/`, keep `specs/`, `docs/` and the policy artifacts where the whole team can read them, and put a `CLAUDE.md`/`AGENTS.md` next to each capability's code pointing at its spec. Then:

1. Read [`GUIDELINE.md`](GUIDELINE.md). The floor is **one spec file** — start there.
2. Run `/prep` once so the repository has the three-command verification interface, the metric-class gates and the ratchet baseline. Verification is what everything else stands on.
3. Shape the first capability spec with `/shape`, write it with `/to-spec`, and let a human ratify it by merging its own PR. Add the constitution when invariant rules demand it.
4. `/spec-to-tickets` breaks the ratified spec into tracer-bullet issues with explicit blocking edges.
5. Run the first slice locally with `/implement-feature`, then `/explain` afterward.
6. Turn on autonomous mode narrow (allowlist + green CI + a human approving every PR); widen only as your eval suite earns trust.

## Portability

The methodology has two layers that travel differently:

- **Specs and context** (Parts 1–2 of the guideline) — capabilities, specs, the `AGENTS.md`/`CLAUDE.md` files, the constitution. **Tool-portable**: any coding agent reads them.
- **Automation** (Parts 3–5) — the shared protocol and its adapters, the reviewer, the launchers, the autonomy trajectory. **Implemented for Claude Code**; `adaptations/` maps each piece onto Codex (a near-1:1 port, since skills and `AGENTS.md` are open formats) and Kiro, and documents what does not survive the trip.

The executable contracts under `scripts/` are deliberately tool-neutral: dependency-free Python over plain JSON, so any harness can compute the same fingerprint and any CI can recompute the same verdict.

## License

[MIT](LICENSE).

---

*This document exists to serve the work, not to govern it. When a rule here causes more friction than value, change it — consciously, with a commit and a reason. Silent erosion of discipline is what kills systems like this.*

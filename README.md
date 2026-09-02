# Spec-Anchored Agentic Development

> One durable contract per capability, and the code answers to it — evidence before "done".
> A methodology, and a ready-to-install bundle, for building software with AI coding agents:
> from the first capability spec to supervised autonomy.

This repository is my agentic development workflow. It is both a **guideline** (how to work) and an **installable bundle** (the shared protocol, the workflow skills, two internal authoring agents, engineering rules, authorization policies, executable contracts and templates that make a coding agent actually work this way). The canonical core lives in open, runtime-neutral formats — `AGENTS.md`, `.agents/skills/`, `.agents/protocols/`, `.agents/rules/` — so Claude Code, Codex and Cursor read the same source; `adaptations/` covers what each harness does differently, and Kiro.

It is maintained as a living reference — when practice conflicts with what's written here, the document is updated, not silently worked around.

---

## The core idea

**Spec-anchored**: the business decision comes before the code, and the spec *stays*. It is the permanent source of truth the code answers to — drift is treated as a bug, conformance is checked value by value — not scaffolding discarded once a feature ships.

Where this sits in the field (per the consolidating taxonomy in [*"Spec-Driven Development: From Code to Contract"*](https://arxiv.org/abs/2602.00180), 2026, echoed by [martinfowler.com's exploring-gen-ai series](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html)):

- **spec-first** — the spec precedes the code but may drift or be discarded (Kiro, Spec Kit).
- **spec-anchored** — the spec is permanent and the code answers to it continuously. **← this is where this methodology sits.**
- **spec-as-source** — code is generated from the spec. For normative rules, the spec's reference values generate the golden tests that act as the oracle, moving toward this.

The unit of organization is the **capability** — a cohesive slice of what the system *does* for the business (payments, orders, notifications), never a technical layer (controllers, repositories) or a bare entity (Product, Customer). Each capability has one durable contract — a stable entrypoint file, with companion files when the capability needs them — you develop from it, and progress in autonomy.

## Five fundamental principles

1. **Simplest possible change.** Delete before you add. No unrequested refactors, no speculative helpers.
2. **Root cause, not band-aid.** Find why a bug happens; don't hide the symptom.
3. **Verification is part of the work, not optional.** Every change needs a way to verify it. If you can't verify it, don't merge it.
4. **Determinism where you can, agent where you must.** Every predictable task becomes a deterministic script the agent calls — the agent is expensive and non-deterministic; a script is cheap and auditable.
5. **Machine-produced "no" before human review.** Every gate the machine can run (failing test, type error, lint rule, a surviving mutant, a hardener's finding) fires before a human is asked to look. This is *backpressure* — the check confronts the agent at the boundary.

## The trajectory

```
Identify capabilities → Specification → Development
                                            ↓
                          Operational maturity → Autonomy (narrow start → widening)
```

**The minimum entry point is the first capability spec.** You do not need the constitution, the hardeners, the milestones or the rituals to begin — write `specs/<capability>/<capability>.md` and start. Everything else is how the system *scales*; each piece enters when its pain shows up.

## Autonomy is a gradient, not a switch

The narrow start needs no formal eval suite: issues → an allowlist of trivial classes → **CI green mandatory** → PR → **a human approving every PR** — over a safety baseline that cannot wait (branch protection, scoped credentials, no direct push, one issue → one PR, named blockers, human merge). Widening — more classes, more volume, any step toward auto-merge — requires a regression suite with a track record. Normative calculations never enter autonomy before golden/conformance verification exists. The widening path lives in [`AUTONOMY-PLAYBOOK.md`](AUTONOMY-PLAYBOOK.md), which splits the last step honestly: **M4a** is machine *approval eligibility* (the human still merges); **M4b** is platform auto-merge, a much higher bar.

---

## What's in this repository

### Documents (the methodology)

| File | What it is |
|------|------------|
| [`GUIDELINE.md`](GUIDELINE.md) | The source of truth for **how to work** — the full methodology, Parts 1–7. Read this first. |
| [`AUTONOMY-PLAYBOOK.md`](AUTONOMY-PLAYBOOK.md) | The widening path of autonomy: the Milestones, Tier 1/2 validation, per-class approval eligibility. Read when ready to widen. |
| [`INSTALL.md`](INSTALL.md) | Prerequisites, where each bundle file goes, and what is still yours to build. |
| [`EVALS.template.md`](EVALS.template.md) | The eval-case schema and the initial case index — copy to `EVALS.md` when you start qualifying. |
| [`sources-and-learnings.md`](sources-and-learnings.md) | Every external source mined while designing the methodology, what each contributed, what was rejected and why — the audit trail of *why the system is the way it is*. |
| [`REVIEW-FINDINGS.md`](REVIEW-FINDINGS.md) | The review-findings tracker: every deep review, closure validation and migration since 2026-08-11, with the observed gate results of each. |
| [`CLAUDE-codebase-exploration-block.md`](CLAUDE-codebase-exploration-block.md) | A codebase-exploration block to paste into your root context file (example tool stack — swap in yours). |
| [`adaptations/`](adaptations/) | Running the system elsewhere: `kiro.md`, `codex.md` (harness-class peer, near-1:1 port), and `claude-plus-codex.md` (both harnesses on one repo). |

### The entrypoint, the protocol and its three adapters

One state machine, three modes. `.agents/protocols/implementation-protocol.md` holds phases 0–10, the terminal taxonomy, the invariants and the logging; each implementation skill is a **mode adapter** that declares only *who satisfies each gate*.

| Path | What it is |
|------|------------|
| `AGENTS.md` | The cross-harness operational entrypoint: authority order, canonical paths, explicit rule loading, the internal hardening sequence, runtime-state policy. Merge it with your repository's own instructions. |
| `.agents/protocols/implementation-protocol.md` | The shared state machine — preflight, proven delta, understand, plan and approval, Owner implementation, baseline verification, durable sync, general code review-and-repair, mutation hardening, final Owner acceptance and candidate freeze, deliver. Terminals: `PR_READY_AWAITING_HUMAN`, `NAMED_BLOCKER`, `NO_CHANGE_REQUIRED`. A run never claims the merge. |
| `.agents/protocols/references/` | The scope-manifest schema, and the review-target, handoff and Owner-disposition schemas. |
| `.agents/skills/implement-feature/` | **Supervised** adapter — the human satisfies every gate in-session. `implement` is its explicit alias. |
| `.agents/skills/implement-orchestrated/` | **Orchestrated-worker** adapter — one ticket, one worktree, at most one PR; gates mediated through GitHub. |
| `.agents/skills/implement-backlog/` | **Unattended** adapter — mechanical-or-abort; every would-be question is a named blocker. Its `references/` carry the shared PR template. |

### The two internal authoring agents

| Path | What it is |
|------|------------|
| `agents/general-code-reviewer.md` / `.toml` | Authoring review-and-repair: inspects one exact candidate, fixes concrete correctness, simplicity, type, test and local-design defects in an internal loop, commits in an isolated worktree and returns a complete handoff. A hardener, not an approval gate. |
| `agents/mutation-hardener.md` / `.toml` | Authoring mutation hardening: 100% line and branch coverage on the eligible target, differential mutation target by target, zero actionable survivors. It cannot change truth, thresholds or the gate that judges it. |
| `.agents/skills/general-code-review/` | The rubric the General Code Reviewer loads, with the shared test standards and the smell baseline in its `references/`. |
| `.agents/skills/ticket-readiness-review/` | Lens: the ticket as an executable contract, before a worker is ever dispatched. |

Both agents inherit the Owner's model and run at `effort=max`; no contract pins a model, and the Markdown and TOML forms are validated for parity. Every handoff is a local commit the **Owner inspects and explicitly accepts or rejects** before integration — agent output is never self-validating. Spec/conformance, constitution, security, performance and systemic-architecture reviews are **external** to the implementation harness: the review tool or API the repository configures, CI, the orchestrator, a periodic audit, or a human.

### Workflow skills

| Path | What it is |
|------|------------|
| `.agents/skills/shape/` | The work-shaping interview — an idea, a transcript, existing code, or an existing spec. The interview only. |
| `.agents/skills/to-spec/` | Writes or updates the capability spec from that interview. Never interviews back; gaps become open questions; typed stable IDs issued in continuation. |
| `.agents/skills/spec-to-tickets/` | Breaks a ratified spec into tracer-bullet tickets with explicit blocking edges; quizzes the human before publishing. |
| `.agents/skills/prep/` | One-time repository prep: the `check` / `check-<capability>` / `golden` / `mutation-<capability>` / `fuzz-<capability>` interface, the metric-class gates, the golden harness, minimum CI, the ratchet baseline. |
| `.agents/skills/orchestrate/` | Whole-project orchestration in resolution-gated waves over the explicit issue graph — one worker per ticket, a fingerprinted CI-and-external-review monitor, and the human merging every PR. |
| `.agents/skills/plan-from-issue/` | Phased implementation plan from a GitHub issue (no implementation). |
| `.agents/skills/review-spec-drift/` | Periodic whole-capability spec ↔ code drift audit, report-only. |
| `.agents/skills/explain/` | Post-implementation walkthrough → `docs/walkthroughs/`. |
| `.agents/skills/implement/` | Explicit alias that loads and follows the complete supervised skill without duplicating its gates. |

Skills are invoked directly with the runtime's own syntax (`/shape` in Claude Code, `$shape` in Codex); the canonical files carry no launcher syntax. Ordinary prose that merely names a skill is not a launch.

### Rules, authorization, contracts and the gate

| Path | What it is |
|------|------------|
| `.agents/rules/truth-layer.md` | `specs/**`, the golden tests and the ratchet baseline are read-only outside their named flows. Loaded explicitly for every versioned change — `AGENTS.md` routes to it. |
| `.agents/rules/testing.md` | The testing floor: the lowest boundary that proves the property, regression coverage for every fix, no mocking the seam under test, the mutation obligation, exact evidence. |
| `.agents/rules/package-by-feature.md` | The capability-vs-entity tests, applied when files are created or moved. |
| `policy/` | The **authorization floor** — four versioned profiles plus the instances a launcher issues. A worker never writes one, and `validate-scope` refuses to judge a diff without one. |
| `scripts/spec-anchored` | **Executable contracts**, dependency-free and fail-closed: canonicalization, the APPROVAL-FINGERPRINT over the approval bundle, scope validation under a policy floor, and the strict terminal union. Doctrine that used to be prose, as code that refuses. |
| `scripts/check-all.sh` | **The single gate.** Compiles the artifacts, parses every shell script, runs the structural validator, the fast contract and adversarial suites, the slow corpus, mutation adequacy, and the Codex adapter check. `.github/workflows/gate.yml` runs it on every push and PR. |
| `tests/` | 65 kernel contracts, 208 adversarial fixtures, the slow corpus suite, and mutation adequacy: 55 injected regressions, each of which a fixture must catch. |
| `spec-templates/capability-spec.md` | **The** spec template: authority frontmatter, normative behavior by truth type, Given/When/Then criteria, reference values, and typed stable IDs throughout. |
| `.claude/hooks/`, `.claude/routines/` | Optional Claude Code-specific pieces: the poka-yoke hook that blocks a new `src/<x>/` without `specs/<x>/`, and the frontier-worker launcher routine. |
| `.agent-runs/<run-id>/` | Gitignored per-run state: approvals, evidence, hardening handoffs, Owner dispositions, the final candidate and the result artifact. Created at runtime, never packaged. |

## The three modes

All three run the same protocol. They differ only in who answers.

- **`implement-feature`** — local and interactive. You resolve ambiguity, you approve the plan (and its APPROVAL-FINGERPRINT), you approve any scope change; a semantic amendment to a spec is possible here, behind an explicit in-session gate, and the PR ratifies it.

- **`implement-orchestrated`** — one worker per ticket, dispatched by `orchestrate` into its own worktree. Its gates live on GitHub: the plan is posted as an issue comment and the run **stops** until a human replies `approved <fingerprint>`; ambiguity is a comment plus a label, never a guess.

- **`implement-backlog`** — headless. No one is there to answer, so every gate has a mechanical provider or aborts with a named blocker (`AMBIGUITY`, `MISSING_ORACLE`, `TRUTH_CONFLICT`, `SCOPE_VIOLATION`, `SPEC_CHANGE_REQUIRED`, `SPEC_STALE`, `GRAPH_DECISION_REQUIRED`, `ENVIRONMENT`, `REPEATED_FAILURE`). Scope is increments only; new capabilities and large features stay human-led.

Two things hold across all three. After the Owner has implemented and verified, the same internal pipeline runs — General Code Reviewer, Owner disposition, Mutation Hardener, Owner disposition, final deterministic verification — and any later Owner edit invalidates both passes. And no run ever merges: every mode ends at `PR_READY_AWAITING_HUMAN`, and a human decides.

## Installation

See [`INSTALL.md`](INSTALL.md). In short: copy `AGENTS.md`, `.agents/`, `agents/`, `policy/`, `scripts/` and `tests/` into your repository root, keep `specs/` and `docs/` where the whole team can read them, and put an `AGENTS.md`/`CLAUDE.md` next to each capability's code pointing at its spec. Then:

1. Read [`GUIDELINE.md`](GUIDELINE.md). The floor is the first capability spec — start there.
2. Run `prep` once so the repository has the verification interface, the metric-class gates and the ratchet baseline. Verification is what everything else stands on.
3. Shape the first capability spec with `shape`, write it with `to-spec`, and let a human ratify it by merging its own PR. Add the constitution when invariant rules demand it.
4. `spec-to-tickets` breaks the ratified spec into tracer-bullet issues with explicit blocking edges.
5. Run the first slice locally with `implement-feature`, then `explain` afterward.
6. Turn on autonomous mode narrow (allowlist + green CI + a human approving every PR); widen only as your eval suite earns trust.

## Portability

The methodology has two layers that travel differently:

- **Specs and context** (Parts 1–2 of the guideline) — capabilities, specs, the `AGENTS.md`/`CLAUDE.md` files, the constitution. **Tool-portable**: any coding agent reads them.
- **Automation** (Parts 3–5) — the shared protocol and its adapters, the two internal agents, the launchers, the autonomy trajectory. The canonical core is runtime-neutral: Claude Code and Cursor read it as it is; `scripts/install-codex-port.sh` materializes the disposable `.codex/agents/` adapters for Codex and `--check` catches drift; `adaptations/kiro.md` documents what does not survive the trip.

The executable contracts under `scripts/` are deliberately tool-neutral: dependency-free Python over plain JSON, so any harness can compute the same fingerprint and any CI can recompute the same verdict.

## License

[MIT](LICENSE).

---

*This document exists to serve the work, not to govern it. When a rule here causes more friction than value, change it — consciously, with a commit and a reason. Silent erosion of discipline is what kills systems like this.*

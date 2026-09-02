> validated_on: 2026-08-12 · review_after: 2026-09-12 — volatile
> facts (model names, loader semantics, CLI flags) live in this
> adapter layer and expire; the doctrine files stay role-abstract.

# Running Claude Code and Codex together on one repo

Not migration (that's `codex.md`) — **coexistence**: both harnesses
operating on the same repository, simultaneously. The principle that
makes it cheap: **one truth, two engines.** Everything load-bearing in
this system is repo files; harnesses are interchangeable readers.
Facts verified 2026-07; both tools ship weekly — re-verify the marked
items on wiring.

## The layers, by sharing strategy

| Layer | Strategy |
|---|---|
| `specs/`, `architecture/`, `docs/walkthroughs/`, CI gates, golden, tickets/labels | **Shared as-is** — plain files and GitHub; neither harness owns them |
| Context files **and rules** | **Single source + explicit routing**: root/per-capability `AGENTS.md` carries the compact shared floor and points to `.agents/rules/`; transactional skills load applicable rules explicitly. A thin `CLAUDE.md` may import `AGENTS.md` when Claude is installed. Rule bodies remain single-sourced under `.agents/rules/` |
| `implement-orchestrated` + the shared protocol | Shared directly from `.agents/skills/` and `.agents/protocols/`; only invocation syntax and runtime agent adapters differ. The orchestrator refuses a runtime whose required adapter is absent |
| The skill set (`.agents/skills/`) | **Canonical shared corpus**: Codex/Cursor consume it directly; optional harness adapters may materialize from it, never the reverse |
| Entry points | No command layer or mirrored workflow authority. Each runtime invokes the canonical `.agents/skills/` entrypoint using its native syntax |
| Internal hardening agents | Canonical paired contracts live in root `agents/`: Markdown for Cursor/external loaders and equivalent TOML for Codex. The materializer copies TOML adapters to `.codex/agents/`. Both author committed handoffs; the Owner inspects each |
| Run logs / PR descriptions | **Harness-agnostic by design** — the skill writes them, whoever runs the skill |

Skills stay **one text** — never fork per model. They're tuned for the
reference implementation (the pin note says so); Codex-side
divergences go to `lessons.md` as observations, and the
Claude-specific levers (ULTRATHINK) degrade as harmless no-ops there.

## Division of labor — the recommended split

- **Claude Code owns the autonomous route**: direct adapter
  invocation from an external launcher (Action or Routine), the
  frontier-worker, and the two internal authoring hardeners. (`/goal` is a
  session-scoped completion re-check — an optional, eval-gated
  composition on top of a run, never the loader or the engine.)
- **Codex owns the cross-family vote**: enable its managed
  **external review on every PR** through the configured API/tool or managed auto-review. Treat it as a candidate-bound pipeline result; whether it gates is repository policy, never an implicit property of the worker.
- **Either works the frontier**: tickets are harness-agnostic, and the
  claim protocol (`in-flight` label + comment) lives on GitHub — no
  double-pick regardless of who claims. Field split worth copying:
  "Codex for the cheap autonomous grind, Claude Code for the hard
  refactor" — well-sliced mechanical tickets to one, judgment-heavy
  slices to the other, and compare outcomes (the logs make it
  measurable).
- **Second opinions on demand**: a Codex session reading a Claude plan
  (or vice versa) is a cross-family consult — same independence
  profile as the review, earlier in the loop.

## Collision avoidance (mostly already built)

Branch discipline separates the engines: Routines push only to
`claude/`-prefixed branches (platform-enforced); everything else uses
the typed prefixes (`feature/`, `fix/`, …). Parallel work =
frontier tickets with **disjoint committed file scopes**, one fresh
session per ticket, whichever harness runs it. The one rule to add to
team habits: a PR names its author engine in the description (the `.agent-runs/<run-id>/` artifacts record it) — so review attention and the eval base can
be split per engine later.

## The orchestrator topology (Orca)

One configured parent session runs `/orchestrate` as scheduler-and-judge;
Codex sessions are the workers, one per ticket per worktree. Each worker uses
the model selected by the operator/repository configuration at `effort=max`. The frontier is the existing issue graph;
the `in-flight` claim is the collision guard; every returned PR gets
the configured candidate-bound external review before the human merges. Dispatch
rides the **worktree + terminal layer** (the gkpacker pattern, source
#48): `worktree create --base-branch origin/main --parent-worktree …`
births the worker with agent + prompt in one call; the configured worker model
is inherited while `model_reasoning_effort="max"` is applied via
`terminal create` → `wait tui-idle` → `send "$(cat file)"`. Lineage draws the DAG in Orca's sidebar, and
**GitHub stays the only graph and the only ground truth** — the PR is
the completion signal, so the heavier orchestration layer (Runs,
worker_done, decision gates; Experimental) is not required. Mechanism
flags come from `ORCA skills get orca-cli` at runtime — the loaded
guide wins on any conflict. Slice-scoped orchestrators nest one
declared level via sub-orchestration tickets; cross-repo via the
guide's remote/repo selection. The two internal authoring agents inherit the Owner worker's model and pin only
maximum effort. External review model/provider selection belongs to the review
service and its eval cell, not to the worker.

## Verify when wiring

Verify that each installed runtime discovers `.agents/skills/`, obeys the
root/scoped `AGENTS.md` chain, can launch the paired internal-agent contract,
and returns exact handoff commits/artifacts. Where a runtime needs an adapter,
materialize only that adapter and keep the shared skill/protocol/rule corpus
single-sourced. Wire adapter drift checks into CI. Keep the root `AGENTS.md` lean —
Cloudflare's reviewer (source #54) penalizes exactly the right
anti-patterns: generic filler ("write clean code"), **files over 200
lines that cause context bloat**, and tool names without runnable
commands; every line is a permanent tax on every session of both
engines. And for custom tool schemas (MCP
servers): keep them either **identical to a native tool or clearly
distant** — "close but slightly off" is the RL danger zone (source
#40).

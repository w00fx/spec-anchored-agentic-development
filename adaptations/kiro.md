> validated_on: 2026-08-12 · review_after: 2026-09-12 — volatile
> facts (model names, loader semantics, CLI flags) live in this
> adapter layer and expire; the doctrine files stay role-abstract.

# Adapting the system to Kiro

The shared `.agents/` core is this system's reference implementation; no single coding harness is a requirement. This page maps every artifact onto Kiro (AWS) and names
what does not survive the trip. Facts verified 2026-07 against Kiro's
docs and the official multi-agent CLI sample — Kiro ships fast;
re-verify on adoption.

What Kiro has today, relevant here: an IDE **and a CLI** running the
same spec workflow; custom **agents and subagents** (delegation via
`/spawn`, with tool restrictions in the subagent runtime); **skills**;
**stored prompts** invoked by name; **steering** files with `always` /
`fileMatch` inclusion; and **lifecycle hooks** (before/after tool use)
capable of hard-blocking — alongside the older file-event hooks.

## The thesis: anchored on top of spec-first

Kiro supports persistent, continuously refined Feature Specs (and a gate-less Quick Spec). The difference is not persistence alone: Spec Anchored hardens stable requirement IDs, repository ratification, conformance evidence, exact-candidate review, and drift policy on top.
This system is spec-anchored (one durable logical capability contract with a stable entrypoint). The
reconciliation: **the permanent layer lives outside `.kiro/`** — plain
repo files, tool-agnostic by construction — and **Kiro's per-work spec
trio becomes this system's execution layer.** Bonus: Kiro speaks EARS
natively in its requirements — this system's rule notation is the Kiro
agent's mother tongue.

## Translation table

| This system | On Kiro |
|---|---|
| `GUIDELINE.md`, playbook, sources, spec template | Repo docs — unchanged |
| `specs/<capability>/` (permanent) + `architecture/` + `docs/walkthroughs/` | Unchanged — they live outside `.kiro/` on purpose |
| Root + capability `AGENTS.md` | **Read natively** (the open standard Kiro supports). Keep `AGENTS.md` as the single source; a thin `CLAUDE.md` doing `@AGENTS.md` serves Claude Code |
| Kiro-specific always-rules | Steering, `inclusion: always` |
| Per-capability additions | Steering with `fileMatch: src/<capability>/**` |
| `.agents/rules/package-by-feature.md` | Always-included steering file |
| Canonical `.agents/skills/` entrypoints | Map to Kiro skills/stored prompts or custom agents as appropriate; the checked-in skill body remains the authority |
| `implement-feature` / `implement-backlog` skills | **Custom agents** — the skill body becomes the agent prompt (the official sample's `coder` pattern) |
| General Code Reviewer + Mutation Hardener | Two authoring subagents delegated via `/spawn`; each works from an exact checkpoint and returns a committed delta + alteration report for Owner acceptance |
| Poka-yoke hook (spec-before-src) | **Before-tool-use lifecycle hook with hard-block** — ports, arguably with a richer surface ("hooks beat promises") |
| Structured run logs | `.agent-runs/<run-id>/` as the shared artifact contract; Kiro trace hooks may populate it |
| GitHub backlog, labels, `spec-to-tickets` output, CI gates, golden tests | Unchanged — tool-agnostic |

## Kiro's spec trio as the execution layer

- **`requirements.md`** = the slice — its EARS criteria **point at** the
  capability spec's typed stable IDs (`Spec: specs/<cap>/<cap>.md @
  commit <sha> — AC-<CAP>-###`). Steering carries the law: point,
  never copy.
- **`design.md`** = the plan (protocol Phase 3) — disposable, plan-shaped; the
  the human approval gate applies directly; no internal plan-review agent is required.
- **`tasks.md`** = `tickets.md` in the local mode of
  `spec-to-tickets`.
- Kiro's native approval gates (requirements → design → tasks) **are**
  the supervised gate structure, built into the product.

## What does not port — three structural limitations

1. **There is no `/goal`.** The autonomous route's guarantees rest on
   a fresh evaluator re-checking an **evidence-demanding condition**
   every turn, with named-blocker terminals. Kiro's autonomy
   (autopilot over the task list; specialized subagents) is
   **progress-granular** — "were the tasks checked off?" — not
   condition-verified. Porting `implement-backlog` means returning to
   instruction-following without an equivalent independent completion mechanism. The
   supervised path ports well; the autonomous path ports with weaker
   guarantees.
2. **The model re-audit fires in full.** The repository does not pin an
   internal-agent model; each role inherits the Owner/parent worker model.
   Runtime-specific thinking controls, plan-mode substitutes, and advisor
   features do not transfer automatically. The skills' own doctrine applies:
   on any model or harness change, re-run the representative evals and keep
   `effort=max` as a separate requirement.
3. **Evidence becomes discipline, not mechanism.** Trace hooks can
   build the audit trail, but nothing mechanically *demands* "runner
   output visible" the way the `/goal` evaluator does.

## Recommended topology: hybrid (the community norm)

Kiro can host the supervised human side — shape → spec → tickets → implement — while another qualified launcher/runtime may host unattended work, **all over the same repository truth**
(`specs/`, `architecture/`, `AGENTS.md`). Context single-sourcing:
content in `AGENTS.md`, a thin `CLAUDE.md` pointing at it, steering
only for what is Kiro-specific. "Many teams run both" is the observed
field pattern, and this system was built for it: the truth layer is
tool-portable by design (Guideline, Part 1's own claim).

## Verify when wiring

The exact tool-restriction surface of Kiro subagents; per-agent model
pinning on Bedrock; `AGENTS.md` proximity loading (nearest-wins)
parity; whether a managed scheduler exists (the Routines sibling) or
autonomy wires as CLI + CI cron; stored-prompt argument passing; the
lifecycle-hook schema.

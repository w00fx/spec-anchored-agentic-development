> validated_on: 2026-08-12 · review_after: 2026-09-12 — volatile
> facts (model names, loader semantics, CLI flags) live in this
> adapter layer and expire; the doctrine files stay role-abstract.

# Adapting the system to Codex

Unlike Kiro (a spec-first product), OpenAI's Codex is a **harness-class
peer of Claude Code** — the field's own read: "the same class of
agentic coding surface." The adaptation is therefore
primitive-to-primitive, close to 1:1, with the differences
concentrated in three places. Facts verified 2026-07 against the
official docs, changelog, and field guides — Codex ships weekly;
re-verify on adoption.

What Codex has today, relevant here: hierarchical **AGENTS.md**
(Codex originated the standard; the instruction chain is rebuilt every
run and auditable); **skills on the open agent-skills spec**
(SKILL.md + scripts/references, repo-level `.agents/skills` scanned up
the tree, progressive disclosure with an explicit context budget,
explicit `$mention` or implicit invocation); **hooks (GA)** with a
trust-review flow; **native subagents** (`[agents]` roles in
`config.toml`, per-subagent model, parallel fan-out); **`codex exec`**
headless with an official GitHub Action; **Codex Cloud** (background
parallel tasks in sandboxed containers, producing PRs — experimental);
a managed **auto-review** for PRs; kernel-level sandboxing
(Seatbelt / Landlock+seccomp); and **`/goal` in GA**.

## The thesis: a near-1:1 port — the truth layer needs zero translation

The permanent layer (specs, `architecture/`, walkthroughs) is plain
repo files. The context layer **inverts the pointer**: put the content
in `AGENTS.md` (root + per-capability — Codex's native format, read
hierarchically) and use runtime-specific adapters only when that runtime requires them. The SKILL.md artifacts (the three implementation adapters, the General Code Review rubric, and ticket-readiness review)
are **already in the format Codex reads** — they install under
`.agents/skills/` as-is, pending the model re-audit below.

## Translation table

| This system | On Codex |
|---|---|
| `GUIDELINE.md`, playbook, sources, spec template, `specs/`, `architecture/`, `docs/walkthroughs/` | Unchanged — plain repo files |
| Root + capability `AGENTS.md` | **Native, zero translation** (Codex originated the standard); thin `CLAUDE.md` → `@AGENTS.md` serves Claude Code |
| The SKILL.md corpus (all explicit entrypoints, three implementation adapters, General Code Review rubric, and ticket-readiness review) | **Native from `.agents/skills/`**; no mirror or second authority |
| Former command entrypoints | They no longer exist as commands; invoke the corresponding repository skills explicitly with `$name` |
| Two internal authoring agents (General Code Reviewer + Mutation Hardener) | Canonical paired contracts under `agents/<name>.md` and `.toml`; the materializer copies the TOML adapters to `.codex/agents/` |
| Poka-yoke hook | Hooks (GA) — verify schema; the kernel sandbox covers the deeper layer ("isolation the model cannot talk its way around") |
| `claude -p` + Action | `codex exec` (`--json` for structured output) + the official Codex GitHub Action |
| Routines | **Codex Cloud** — background parallel tasks producing PRs (experimental; verify maturity) |
| Run logs / evidence trail | `.agent-runs/<run-id>/` plus `codex exec --json`/CI artifacts; never `.codex/` or `.claude/` runtime logs |
| `/goal` | Exists (flag-gated at launch, GA per mid-2026 reports) — evidence-based completion **by template**, self-audited: see limitation 1 |
| `/advisor` | No equivalent — Codex's culture is the inverse (cheap models for the grind, e.g. a mini for subagent fan-out) |
| — | Bonus primitive we lack natively: managed **auto-review** on PRs |

## The three concentrations of difference

1. **`/goal` semantics — resolved: evidence-based by template,
   self-audited.** Verified mechanics (docs + runtime analysis): the
   goal is durable thread state; at each turn's end the runtime
   injects a continuation template into the **same thread**; the
   template forbids proxy signals ("passing tests alone do not prove
   a goal is met") and the completion philosophy matches this
   system's word for word ("the evidence decides whether it is
   done"); blocker terminals and token budgets with graceful
   soft-stop exist. The one load-bearing difference: **the worker
   audits itself** and calls complete — there is no independent
   evaluator (Claude Code's small fast model reading the transcript
   each turn). In this system's vocabulary: the strongest *instructed*
   form (the anti-proxy template re-injected every turn), versus an
   independence *mechanism*. Consequence for the port: conditions
   transfer as strong instruction, not as a second head — mitigate
   with Codex's auto-review, cross-family review, and the outer gates
   (named blockers, PR, human approval), and still run one
   deliberately-failing-condition test to see the template discipline
   in your own repo.
2. **The model re-audit fires in full.** The internal agents inherit the
   model selected for the Owner/parent worker rather than pinning one in the
   repository. Defaults and capabilities change over time, so every worker-model
   or harness change must re-run the representative eval suite. Runtime-specific
   thinking controls, plan-mode substitutes, and advisor features do not transfer
   automatically — the skills' own doctrine applies: re-audit every prompt
   artifact and keep `effort=max` as a separate requirement.
3. **Enforcement moves layers.** Our two internal agents are authoring roles in isolated worktrees and return committed handoffs for Owner inspection. Codex maps them to strong-model `[agents]` roles under the kernel sandbox; verify commit visibility, workspace-write, and the absence of push/merge authority. Evidence is
   buildable (JSON output, session logs) but, as everywhere without
   the evaluator, demanding it is discipline unless limitation 1
   resolves favorably.

## Recommended topology

(For operating both harnesses on the same repository simultaneously —
layer sharing, the frontier claim protocol, the drift gate — see
`adaptations/claude-plus-codex.md`.)

Full-Codex is far more viable than full-Kiro (peer harness; skills
port; `/goal` exists pending semantics). The field consensus is still
**hybrid** — "Codex for the cheap autonomous grind, Claude Code for
the hard refactor" — over the same repo truth, with `AGENTS.md` as the
single context source. And one cross-tool pattern worth stealing
regardless: **cross-family peer review** (Codex reviewing Claude's
output, or vice versa) is the strongest independence buy in the
reviewer-mode design space — an adversarial pass from a different
model family, exactly the option the A/B backlog item records.

## Migration mechanics, class by class

Start with Codex's own `/import` (it selectively migrates setup,
project config, and recent chats from Claude Code), then hand-finish:

- **Rules → root routing plus canonical files.** Codex loads root/nested
  `AGENTS.md` as its persistent instruction chain. The root file carries the
  small always-present floor and explicitly requires the applicable files in
  `.agents/rules/`; transactional skills also read them. Do not duplicate the
  full rule bodies into harness-specific configuration.
- **Skills → use `.agents/skills/` directly.** This is the canonical shared
  corpus. `scripts/install-codex-port.sh` no longer copies skills; it validates
  them and materializes only the custom-agent TOMLs under `.codex/agents/`.
  Re-audit runtime-specific invocation syntax and tool support on adoption, but
  never fork the skill bodies by harness.
- **Commands → skills with explicit `$` invocation, not prompts.**
  Keep `$shape`, `$to-spec`, `$spec-to-tickets`, and the implementation
  adapters versioned in the repository. There is no bundled general
  `/review` command; heavy reviews are external pipeline/tool concerns.
- **The two internal agents → paired root contracts.**
  Keep `agents/general-code-reviewer.{md,toml}` and
  `agents/mutation-hardener.{md,toml}` equivalent. The Markdown form is human/external-tool friendly; the TOML form is the Codex adapter copied to `.codex/agents/` by the materializer. Each role starts from an exact commit,
  creates one handoff commit, and returns a structured alteration report. A
  legacy `reviewer` role is drift.

## Example: the root AGENTS.md routing layer

Only what has no better home lives here (authority, commands, routing); everything else is a pointer — a file to land on, a
folder to explore, and the capability map never duplicated.

```markdown
# --- AGENTS.md (repository root) ---

# <Project name>

<One paragraph: what the system does, for whom.> TypeScript frontend,
Go backend. Source is organized by capability under src/ — one folder
per business verb, never per entity or layer.

## Commands

- `make check` — lint + typecheck + tests, whole repo
- `make check-<capability>` — the same, scoped (run this every chunk)
- `make golden` — the reference-value tests against the specs' tables

## Where truth lives (read before working)

- Domain invariants (non-negotiable): architecture/constitution.md
- Capability map + contracts between capabilities:
  architecture/pipeline.md — the map is the single source of which
  capabilities exist; it is deliberately not repeated here.
- Spec template for new capabilities: spec-templates/capability-spec.md
- Each capability has its own AGENTS.md in src/<capability>/, pointing
  at that capability's spec. Dated ADRs: architecture/decisions/.
  Implementation walkthroughs: docs/walkthroughs/.

## Package by feature (always applies)

Source folders are capabilities: a business verb (payments,
reconciliation), never a data noun (models, utils) or a layer
(controllers, services). Before creating a NEW top-level folder under
src/, run the three tests:

1. Business verb, not data noun.
2. Vertical slice (entry point → logic → data), not a horizontal
   layer.
3. Other capabilities import it only through its declared contract.

If any test fails, the code belongs in an existing capability — or the
boundary needs the human. Never create src/<x>/ without a matching
specs/<x>/ (a hook enforces this mechanically where wired).

# --- src/payments/AGENTS.md ---

# payments

Spec — the source of truth for this capability's behavior:
specs/payments/payments.md. Read it before changing anything here;
tests anchor on its pointed stable IDs (typed, never renumbered).

Contracts this capability exposes and consumes:
specs/payments/contracts/ (explore as needed). Reference-value
tables: specs/payments/tables/.

Scoped checks: `make check-payments` after every chunk.

<Capability-specific notes: gotchas, invariants local to payments.>

# --- CLAUDE.md (root AND next to each capability AGENTS.md) ---

@AGENTS.md
```

## GitHub triggers for the autonomous route

The architecture was always trigger-pluggable (the trigger picks the
what; the skill guarantees the how; the condition demands the done) —
so the last mile swaps cleanly. Three verified paths:

- **The official Codex GitHub Action** (event-shaped, the direct
  sibling of this system's original skeleton): `on: issues:
  {types: [labeled]}`, filter `auto-implement`, run `codex exec` with
  `$implement-backlog` + the condition. The event delivers the issue
  in the payload, so the frontier-worker's scan/claim steps drop —
  they were the *scheduled*-trigger adaptation. **The deciding
  caveat:** goal mode is subscription/app-server-gated ("an API key
  will not enable /goal") — in CI, `codex exec` likely runs without
  the goal engine: one long execution per ticket, no continuation
  loop. Well-sliced tickets (1-4 criteria) may fit one exec; verify
  first.
- **The mention bridge to Codex Cloud** (their managed runtime, the
  Routines sibling): labels don't trigger Cloud natively, but comments
  do — a one-step Action translates `issues.labeled` into a comment
  (`@codex implement this issue with $implement-backlog …`); Cloud
  picks it up in its container and opens the PR. Current mention
  semantics: verify item.
- **Auto-review is GitHub-triggered out of the box** — every PR gets
  their managed reviewer. Not implementation, but the zero-cost
  materialization of **cross-family review**: this system implements
  on Claude Code, Codex reviews the PR — the different-family
  independence vote, without writing a workflow.

Whatever the trigger, the run carries limitation 1's semantics
(self-audited by template, no independent evaluator) — the trigger
doesn't fix that; the outer gates do (named blockers, the PR, the
human).

## Verify when wiring

The `/goal` template discipline in your repo (one deliberately-failing
condition run); whether goal mode is available under `codex exec` in CI
(subscription/app-server gating); current `@codex` mention semantics on
GitHub; the `[agents]` tool-restriction surface and per-role
model pin; the hooks schema; Codex Cloud maturity for the
frontier-worker pattern; `/import`'s fidelity when migrating Claude
Code config; argument passing in custom prompts.

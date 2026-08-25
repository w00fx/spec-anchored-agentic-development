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
| Context files **and rules** | **Single source + thin mirror**: content lives in `AGENTS.md` (root and per-capability — Codex-native); `CLAUDE.md` next to each is one line, `@AGENTS.md`. `.claude/rules/` content dissolves into the root `AGENTS.md` — the only always-loaded surface both engines share — and the directory retires (hooks stay hooks: mechanism, not prose). One copy of truth, two readers |
| `implement-orchestrated` + the shared protocol | Ships for both engines: Claude invokes `/implement-orchestrated`, Codex `$implement-orchestrated` from the `.agents/skills/` port; the protocol is read from `.claude/protocols/` on the Claude side and from the neutral `agent-system/protocols/` the materializer creates on the Codex side (paths are repointed at install). The orchestrator refuses an engine whose install is absent |
| The skill set (`.claude/skills/`) | **Canonical + synced install**: `.claude/skills/` is canonical (the reference implementation); `.agents/skills/` carries the Codex install — a symlink if both harnesses follow them (verify), else a copy with a **CI drift gate**: `bash scripts/install-codex-port.sh --check` rebuilds the port in a temp tree, applies the same transforms, and fails the build on divergence (a raw `diff -r` would report the intended repoints as drift) |
| Commands | Claude Code native (`.claude/commands/`); on Codex, the same bodies as `$`-invoked skills (they're portable by design) or pasted |
| The reviewer | **Per-harness native**: the `.claude/agents/reviewer.md` file for Claude Code (tools + model enforced by frontmatter); a `[agents]` role for Codex — point the role's instructions at the same file if the config supports paths (verify), else sync + the drift gate |
| Run logs / PR descriptions | **Harness-agnostic by design** — the skill writes them, whoever runs the skill |

Skills stay **one text** — never fork per model. They're tuned for the
reference implementation (the pin note says so); Codex-side
divergences go to `lessons.md` as observations, and the
Claude-specific levers (ULTRATHINK) degrade as harmless no-ops there.

## Division of labor — the recommended split

- **Claude Code owns the autonomous route**: direct adapter
  invocation from an external launcher (Action or Routine), the
  frontier-worker, and the decorrelated lens reviewer. (`/goal` is a
  session-scoped completion re-check — an optional, eval-gated
  composition on top of a run, never the loader or the engine.)
- **Codex owns the cross-family vote**: enable its managed
  **auto-review on every PR** — the different-model-family reviewer
  the A/B item calls the strongest independence buy, at zero wiring
  ("Replacing Judges with Juries," in production). Treat its comments
  under the existing late-comments policy: advisory to the human,
  never a gate.
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
team habits: a PR names its author engine in the description (the log
path already reveals it) — so review attention and the eval base can
be split per engine later.

## The orchestrator topology (Orca)

One Claude Code session (Fable, effort max) runs `/orchestrate` as
scheduler-and-judge; Codex (GPT-5.x) sessions are the workers, one
per ticket per worktree. The frontier is the existing issue graph;
the `in-flight` claim is the collision guard; every returned PR gets
the applicable-lens cross-family review before the human merges. Dispatch
rides the **worktree + terminal layer** (the gkpacker pattern, source
#48): `worktree create --base-branch origin/main --parent-worktree …`
births the worker with agent + prompt in one call; custom models
(the Codex GPT-5.x workers — `model_reasoning_effort="xhigh"`, the
worker side of the operator's effort doctrine) via `terminal create` → `wait tui-idle` →
`send "$(cat file)"`. Lineage draws the DAG in Orca's sidebar, and
**GitHub stays the only graph and the only ground truth** — the PR is
the completion signal, so the heavier orchestration layer (Runs,
worker_done, decision gates; Experimental) is not required. Mechanism
flags come from `ORCA skills get orca-cli` at runtime — the loaded
guide wins on any conflict. Slice-scoped orchestrators nest one
declared level via sub-orchestration tickets; cross-repo via the
guide's remote/repo selection. Reviews are model-pinned by doctrine:
**Opus subagents at max effort** on the Claude side (the reviewer
agent carries the pin; Fable's quota is spent orchestrating, never
reviewing), **Sol at its max — `xhigh`** on the Codex side. The judge
never runs on a cheaper brain than the judgment tier.

## Verify when wiring

Whether both harnesses follow symlinks for skills; whether Claude Code
reads `.agents/skills/` natively (if yes, the sync dies); whether
Codex's `[agents]` accepts an instructions file path (if yes, the
reviewer body stays single-sourced); whether Claude Code reads
`AGENTS.md` natively in your version (if yes, even the thin mirror
dies); the drift gate wired into CI. Keep the root `AGENTS.md` lean —
Cloudflare's reviewer (source #54) penalizes exactly the right
anti-patterns: generic filler ("write clean code"), **files over 200
lines that cause context bloat**, and tool names without runnable
commands; every line is a permanent tax on every session of both
engines. And for custom tool schemas (MCP
servers): keep them either **identical to a native tool or clearly
distant** — "close but slightly off" is the RL danger zone (source
#40).

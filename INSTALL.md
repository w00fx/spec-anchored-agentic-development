# Install

This bundle turns a coding agent into the system described in `GUIDELINE.md`
(English, canonical): capability-organized, spec-anchored development;
implementation skills, a reviewer agent with criteria lenses, and direct adapter invocations (`/goal` is an optional, eval-gated composition — never the engine).

Copy the `.claude/` folder into your repository root and the root-level
documents wherever your team keeps them. Read `GUIDELINE.md` first;
`AUTONOMY-PLAYBOOK.md` when you start widening autonomy.

## Where each file goes

| File | What it is |
|---|---|
| `GUIDELINE.md` | The system — read this first |
| `AUTONOMY-PLAYBOOK.md` | Milestones 1-4, Tier 1/2 metrics, per-class auto-merge |
| `sources-and-learnings.md` | Source catalog + decision record |
| `adaptations/kiro.md` | Running the system on Kiro: translation table, execution-layer mapping, the three limitations, hybrid topology |
| `adaptations/codex.md` | Running the system on Codex: near-1:1 port (AGENTS.md native, skills on the open spec), the three concentrations of difference, cross-family review |
| `adaptations/claude-plus-codex.md` | Both harnesses on one repo: layer sharing strategies, division of labor (autonomous route vs cross-family vote), the CI drift gate |
| `CLAUDE-codebase-exploration-block.md` | Paste into your root CLAUDE.md (example tool stack — swap in yours) |
| `spec-templates/capability-spec.md` | The permanent capability-spec template (EARS + GWT + reference values) |
| `.claude/skills/implement-feature/SKILL.md` | Supervised-local adapter of the shared protocol (phases 0–9; human satisfies every gate in-session; gated semantic amendment per the truth-change policy) |
| `.claude/skills/implement-feature/references/log-template.md` | Log schema for the skill's runs (read when opening the run log) |
| `.claude/skills/implement-backlog/SKILL.md` | Unattended adapter (mechanical-or-abort gates; invoked directly — launcher's `claude -p` or routine child session; terminal = PR_READY_AWAITING_HUMAN, never merge-monitoring) |
| `.claude/skills/implement-backlog/references/log-template.md` | Log schema for autonomous runs (read when opening the run log) |
| `.claude/skills/implement-backlog/references/pr-template.md` | Shared PR description template, all adapters (Approved plan + fingerprint; terminal = PR_READY_AWAITING_HUMAN — monitoring lives outside the run) |
| `scripts/check-all.sh` | **The single gate — CI runs this.** Compiles the contracts, runs the structural validator, the contract suite, the adversarial suite, and the Codex port drift check |
| `scripts/spec-anchored` | **Executable contracts** (dependency-free, fail-closed): `canonicalize`, `build-approval` + `verify-approval` (APPROVAL-FINGERPRINT over the canonical bundle; the record proves the approval *event*), `validate-scope` (schema-valid manifest, absolute deny, typed truth grants, permissions, NUL-safe parser), `validate-result` (strict terminal union). `python3 scripts/spec-anchored <cmd>` |
| `policy/profiles/` | **The authorization floors** — four versioned base profiles. For autonomous and unattended modes a base profile is *not executable*: it constrains form, never surface |
| `policy/instances/` | **What a launcher actually issues** — base + overlay carrying `authorized_scope_roots`, aggregate caps, path denies and operations. Every path-bearing field is canonically validated, and the structural gate strict-parses and resolves every artifact here |
| `scripts/run-step.py` | Portable per-step timeout for the gate (exit 124), so the budget is real without depending on a `timeout(1)` binary |
| `tests/_harness.py` | Test harness with **explicit outcome protocols** (`raises` / `violations` / `clean` / `value` / `holds`). `raises` demands the kernel's own `ContractViolation`: a crash of any other type is a programming failure, not a refusal |
| `tests/test_kernel_contracts.py` | 61 fast in-process checks — canonicalization, the approval mutation matrix, scope under a policy floor, the terminal union |
| `tests/test_kernel_adversarial.py` | 70 fast adversarial fixtures — every bypass audits nine through eleven found: denied-path-as-truth, oracle-inside-specs, permission evasion, self-authorization, governance-surface writes, cross-run and cross-repo approval replay, impossible calendar dates, padded diff paths, fake terminals |
| `tests/test_corpus.py` | 16 slow corpus fixtures (retired forms, hidden files, broken CLI, broken shell, unterminated frontmatter) — run **once** by the gate, never per mutant |
| `tests/test-mutants.py` | **Mutation adequacy** — injects 21 regressions into the kernel and requires a fixture to catch each, running only the fast suites. A survivor is named. The whole gate finishes in seconds |
| `scripts/validate-bundle.py` | Structural gate ONLY (corpus scan including hidden dirs, frontmatter policy, retired forms, py_compile, `bash -n`). It never runs the suites — mixing those roles is what let an env var skip the tests |
| `scripts/install-codex-port.sh` | Experimental Codex coexistence materializer — invoke as `bash scripts/install-codex-port.sh`; qualify before trusting (EVAL-014/015) |
| `EVALS.template.md` | Eval-case schema + the 21-case initial index (deduplicated); copy to `EVALS.md` when qualifying |
| `.claude/protocols/references/review-target-schema.md` | Seal schemas (review target + report + invalidation check) — staged enforcement |
| `.claude/protocols/implementation-protocol.md` | The shared implementation state machine — phases, terminals, gates; every implement skill is a mode adapter over it |
| `.claude/skills/implement-orchestrated/SKILL.md` | Orchestrated-worker adapter: first-message invocation, GitHub-satisfied gates, plan fingerprint, self-checks, parked delivery |
| `.claude/agents/reviewer.md` | The reviewer subagent (fresh context; report-only **by instruction** — Bash present for verify commands; the enforceable invariant is candidate-immutability (disposable checkout, no push/commit credentials, tracked tree clean before and after); loads criteria lenses per its routing table) |
| `.claude/skills/plan-review/SKILL.md` | Lens: approach soundness before code |
| `.claude/skills/general-code-review/SKILL.md` | Lens: correctness, simplicity, tests, types, commits |
| `.claude/skills/general-code-review/references/test-standards.md` | Shared test bar (GOOD/BAD pairs + mocking boundary rule) — the lens judges by it, both implement skills write to it |
| `.claude/skills/general-code-review/references/smell-baseline.md` | Twelve Fowler smells with fixes (repo overrides; capped at [SHOULD]) |
| `.claude/skills/constitution-compliance-review/SKILL.md` | Lens: domain invariants vs `architecture/constitution.md` |
| `.claude/skills/conformance-review/SKILL.md` | Lens: diff vs spec (value by value) and vs the approved plan |
| `.claude/skills/ticket-readiness-review/SKILL.md` | Lens: tickets as executable contracts — self-contained, criteria pointed, graph explicit, sized; gates dispatch |
| `.claude/commands/implement.md` | Discoverability **redirect only** → points at `/implement-feature` (a command body cannot load a user-only skill) |
| `.claude/commands/review.md` | On-demand reviewer dispatch (report-only) |
| `.claude/commands/explain.md` | Post-implementation walkthrough → `docs/walkthroughs/` |
| `.claude/commands/shape.md` | Work-shaping interview (idea / transcript / code / existing spec / task) — the interview only; `/to-spec` writes |
| `.claude/commands/to-spec.md` | Writes/updates the capability spec from the interview (never asks back; typed stable IDs issued in continuation) |
| `.claude/commands/prep.md` | One-time repo prep: the three-command interface, metric-class gates (stack-agnostic), golden skeleton, minimum CI, ratchet baseline — brownfield-safe |
| `.claude/commands/orchestrate.md` | Wave orchestration over the explicit issue graph: wave table → workers in child worktrees off fresh main → fingerprinted CI+review monitor → triage + the applicable lenses → human merges gate waves |
| `.claude/commands/spec-to-tickets.md` | Spec → tracer-bullet tickets with blocking edges (quiz before publish; tickets.md or GitHub Issues) |
| `.claude/commands/plan-from-issue.md` | Phased plan from a GitHub issue (Plan Mode; no implementation) |
| `.claude/commands/review-spec-drift.md` | Periodic whole-capability spec ↔ code drift audit (report-only) |
| `.claude/rules/package-by-feature.md` | Always-loaded rule: capability-vs-entity tests at file-creation time |
| `.claude/rules/truth-layer.md` | Always-loaded rule: specs/tables/golden/baseline read-only outside the named flows; typed-branch + evidence floor |
| `.claude/hooks/require-spec-for-new-capability.sh` | Example poka-yoke hook (opt-in): blocks a new `src/<x>/` without `specs/<x>/` — wiring snippet in its header |
| `.claude/routines/frontier-worker.md` | Launcher routine: scans the frontier, claims one issue (lease contract), spawns the child session whose FIRST message is `/implement-backlog issue #N`, validates the structured terminal externally |

## What you still have to build (project-specific)

- `architecture/constitution.md` — your non-negotiable domain invariants
- `specs/<capability>/…` — your capability specs (start with `/shape`)
- `architecture/pipeline.md` — capability map and contracts (if applicable)
- A testing strategy — pyramid, contract tests, golden datasets
- `EVALS.md` — the eval suite (Milestone 1; see the playbook)
- CI wiring — the four minimum gates, plus deterministic security gates
  (SAST / SCA / secret scanning)

## Model-generation re-audit

When moving this bundle to a new model generation (4.x → 5.x), run
`claude doctor` and re-audit the prose against the five myth axes
(rules→judgment; examples→interface design; upfront→progressive
disclosure; repetition→tool descriptions; simple specs→rich
references — source #44). Keep the worst-case gates untouched
(never-proceed-red, do-not-interview, caps, hooks): the vendor's own
exception is "highly important areas". Record divergences in
`lessons.md`, and strip only what evals prove safe to strip —
deletion is eval-gated, not vibes-gated. Known gen-5 items from the
first official pass (source #46): ULTRATHINK maps to `effort=max` at
the same judgment points — the keyword changes, the placement survives
(in this topology Opus's work is plan or review: judgment by
construction, so **max everywhere**). One **declared adapter
exception**: the Codex-side reviewer TOML ships `xhigh` — the
operator's pinned recipe for the Sol worker family. It is an exception
of record, not a silent default, and it expires unless an eval
(EVAL-014) compares `xhigh` vs `max` on representative review
workloads. Effort downgrades are otherwise eval-gated
on this system's own evals only — the vendor's sweep numbers are a
hypothesis here, never a default.

# Install

This bundle turns a coding agent into the system described in `GUIDELINE.md`
(English, canonical): capability-organized, spec-anchored development;
implementation skills, two internal authoring hardeners, a compact testing rule, and direct skill invocations; runtime completion wrappers are optional and eval-gated, never the engine.

Copy `AGENTS.md`, `.agents/`, root `agents/`, `policy/`, `scripts/`, and the
root-level doctrine/templates your team keeps into the repository root. Shared
skills, protocols, and rules are already canonical under `.agents/`; Cursor and
Codex must not write their run state under a product-specific directory.

Run `scripts/install-codex-port.sh` only when you want the generated
`.codex/agents/` custom-agent adapters. `.claude/` contains optional
Claude-specific hooks/routines only and is not shared authority. Read
`GUIDELINE.md` first; read `AUTONOMY-PLAYBOOK.md` when widening autonomy.

## Prerequisites

Python 3 (CI runs 3.12). The contracts kernel (`scripts/spec-anchored`) and the
test suites need nothing else. The structural validator and the Codex adapter
check parse YAML frontmatter and need `pyyaml` (`python3 -m pip install pyyaml`);
without it the gate stops at its first stage with a clear message. Make sure the
`python3` on your PATH is the interpreter you installed it into.

## Where each file goes

| File | What it is |
|---|---|
| `AGENTS.md` | Cross-harness operational entrypoint: authority, canonical paths, rule loading, internal-agent sequence, runtime-state policy |
| `.gitignore` | Keeps `.agent-runs/` and generated Codex adapters out of product commits |
| `GUIDELINE.md` | The system — read this first |
| `AUTONOMY-PLAYBOOK.md` | Milestones 1-4, Tier 1/2 metrics, per-class auto-merge |
| `sources-and-learnings.md` | Source catalog + decision record |
| `adaptations/kiro.md` | Running the system on Kiro: translation table, execution-layer mapping, the three limitations, hybrid topology |
| `adaptations/codex.md` | Running the system on Codex: near-1:1 port (AGENTS.md native, skills on the open spec), the three concentrations of difference, cross-family review |
| `adaptations/claude-plus-codex.md` | Both harnesses on one repo: layer sharing strategies, division of labor (autonomous route vs cross-family vote), the CI drift gate |
| `CLAUDE-codebase-exploration-block.md` | Paste into your root CLAUDE.md (example tool stack — swap in yours) |
| `spec-templates/capability-spec.md` | The permanent capability-spec template (EARS + GWT + reference values) |
| `.agents/skills/implement-feature/SKILL.md` | Supervised-local adapter of the shared protocol (phases 0–10; human satisfies every gate in-session; gated semantic amendment per the truth-change policy) |
| `.agents/skills/implement-feature/references/log-template.md` | Log schema for the skill's runs (read when opening the run log) |
| `.agents/skills/implement-backlog/SKILL.md` | Unattended adapter (mechanical-or-abort gates; invoked directly — the installed launcher or runtime child session; terminal = PR_READY_AWAITING_HUMAN, never merge-monitoring) |
| `.agents/skills/implement-backlog/references/log-template.md` | Log schema for autonomous runs (read when opening the run log) |
| `.agents/skills/implement-backlog/references/pr-template.md` | Shared PR description template, all adapters (Approved plan + fingerprint; terminal = PR_READY_AWAITING_HUMAN — monitoring lives outside the run) |
| `scripts/check-all.sh` | **The single gate — CI runs this.** Compiles the contracts, runs the structural validator, fast contract/adversarial suites, slow corpus fixtures, mutation adequacy, and the Codex port drift check when the generated port is installed |
| `scripts/spec-anchored` | **Executable contracts** (dependency-free, fail-closed): `canonicalize`, `build-approval` + `verify-approval` (APPROVAL-FINGERPRINT over the canonical bundle; the record proves the approval *event*), `validate-scope` (schema-valid manifest, absolute deny, typed truth grants, permissions, NUL-safe parser), `validate-result` (strict terminal union). `python3 scripts/spec-anchored <cmd>` |
| `policy/profiles/` | **The authorization floors** — four versioned base profiles. For autonomous and unattended modes a base profile is *not executable*: it constrains form, never surface |
| `policy/instances/` | **What a launcher actually issues** — base + overlay carrying `authorized_scope_roots`, aggregate caps, path denies and operations. Every path-bearing field is canonically validated, and the structural gate strict-parses and resolves every artifact here |
| `scripts/run-step.py` | Portable per-step timeout for the gate (exit 124), so the budget is real without depending on a `timeout(1)` binary |
| `tests/_harness.py` | Test harness with **explicit outcome protocols** (`raises` / `violations` / `clean` / `value` / `holds`). `raises` demands the kernel's own `ContractViolation`: a crash of any other type is a programming failure, not a refusal |
| `tests/test_kernel_contracts.py` | 65 fast in-process checks — canonicalization, the approval mutation matrix, scope under a policy floor, the terminal union |
| `tests/test_kernel_adversarial.py` | 208 fast adversarial fixtures — every bypass audits nine through eleven found: denied-path-as-truth, oracle-inside-specs, permission evasion, self-authorization, governance-surface writes, cross-run and cross-repo approval replay, impossible calendar dates, padded diff paths, fake terminals |
| `tests/test_corpus.py` | slow corpus fixtures (retired forms, hidden files, broken CLI, broken shell, unterminated frontmatter) — run **once** by the gate, never per mutant |
| `tests/test-mutants.py` | **Mutation adequacy** — injects 55 regressions into the kernel and requires a fixture to catch each, running only the fast suites. A survivor is named. The mutation stage uses only the fast suites; the full gate also contains the intentionally slower corpus stage |
| `scripts/validate-bundle.py` | Structural gate ONLY (corpus scan including hidden dirs, frontmatter policy, retired forms, py_compile, `bash -n`). It never runs the suites — mixing those roles is what let an env var skip the tests |
| `scripts/install-codex-port.sh` | Validates the canonical shared corpus and materializes only the disposable `.codex/agents/` adapters; `.agents/skills/` is already native/canonical |
| `EVALS.template.md` | Eval-case schema + authority/lifecycle, two-agent hardening, and external-review integration cases; copy to `EVALS.md` when qualifying |
| `.agents/protocols/references/review-target-schema.md` | Exact candidate, authoring-agent handoff, Owner disposition, and external review identity schemas |
| `.agents/protocols/implementation-protocol.md` | The shared implementation state machine — phases, terminals, gates; every implement skill is a mode adapter over it |
| `.agent-runs/<run-id>/` | Gitignored per-run state, logs, approvals, evidence, hardening handoffs, Owner dispositions, final candidate and result; created at runtime, never packaged |
| `.agents/skills/implement-orchestrated/SKILL.md` | Orchestrated-worker adapter: first-message invocation, GitHub-satisfied gates, plan fingerprint, self-checks, parked delivery |
| `agents/general-code-reviewer.md` | Canonical Markdown role contract for the internal authoring reviewer/cleaner; suitable for Cursor and external loaders |
| `agents/general-code-reviewer.toml` | Equivalent TOML role contract for Codex and TOML-based loaders; validator enforces body parity with the Markdown file |
| `.agents/skills/general-code-review/SKILL.md` | Detailed correctness/simplicity/types/test-quality rubric loaded by the internal General Code Reviewer |
| `.agents/skills/general-code-review/references/test-standards.md` | Behavior-first testing and mocking-boundary reference used by the General Code Reviewer |
| `.agents/skills/general-code-review/references/smell-baseline.md` | Structural-smell vocabulary used as a heuristic, never independent approval |
| `agents/mutation-hardener.md` | Canonical Markdown mutation-hardening contract: pinned coverage/mutation/property-fuzz/CRAP/DRY gates and 100% eligible-target completion |
| `agents/mutation-hardener.toml` | Equivalent TOML mutation contract; validator enforces body parity with the Markdown file |
| `.agents/skills/ticket-readiness-review/SKILL.md` | Lens: tickets as executable contracts — self-contained, criteria pointed, graph explicit, sized; gates dispatch |
| `.agents/skills/implement/SKILL.md` | Explicit convenience alias that loads and follows the complete supervised `implement-feature` skill without duplicating gates |
| `.agents/skills/explain/SKILL.md` | Post-implementation walkthrough → `docs/walkthroughs/` |
| `.agents/skills/shape/SKILL.md` | Work-shaping interview (idea / transcript / code / existing spec / task) — the interview only; `to-spec` writes |
| `.agents/skills/to-spec/SKILL.md` | Writes/updates the capability spec from the interview (never asks back; typed stable IDs issued in continuation) |
| `.agents/skills/prep/SKILL.md` | One-time repo prep: canonical check/golden/mutation/fuzz interfaces, metric-class gates (stack-agnostic), golden skeleton, minimum CI, ratchet baseline — brownfield-safe |
| `.agents/skills/orchestrate/SKILL.md` | Wave orchestration over the explicit issue graph: workers run the two internal hardeners; the orchestrator fingerprints CI and repository-configured external review results; humans merge |
| `.agents/skills/spec-to-tickets/SKILL.md` | Spec → tracer-bullet tickets with blocking edges (quiz before publish; tickets.md or GitHub Issues) |
| `.agents/skills/plan-from-issue/SKILL.md` | Phased plan from a GitHub issue (Plan Mode; no implementation) |
| `.agents/skills/review-spec-drift/SKILL.md` | Periodic whole-capability spec ↔ code drift audit (report-only) |
| `.agents/rules/package-by-feature.md` | Shared capability-boundary rule; root `AGENTS.md` and applicable workflows load it explicitly |
| `.agents/rules/truth-layer.md` | Shared truth/oracle protection rule; mandatory for every versioned change |
| `.agents/rules/testing.md` | Shared testing strategy loaded for code/test changes: unit/integration/contract/regression/property-fuzz selection, mutation obligation, anti-gaming, exact evidence |
| `.claude/hooks/require-spec-for-new-capability.sh` | Example poka-yoke hook (opt-in): blocks a new `src/<x>/` without `specs/<x>/` — wiring snippet in its header |
| `.claude/routines/frontier-worker.md` | Launcher routine: scans the frontier, claims one issue (lease contract), spawns the child session whose first message directly invokes `implement-backlog issue #N` using Claude's skill syntax, validates the structured terminal externally |

## What you still have to build (project-specific)

- Merge the shipped Spec Anchored section of `AGENTS.md` with the repository's
  real project description, commands, architecture pointers, and capability
  context; do not replace existing project instructions blindly
- `architecture/constitution.md` — your non-negotiable domain invariants
- `specs/<capability>/…` — your capability specs (start with `shape`)
- `architecture/pipeline.md` — capability map and contracts (if applicable)
- Repository-declared commands and pinned tools for unit, integration, contract, regression, property/fuzz, coverage, mutation, CRAP, DRY, lint, and types
- `EVALS.md` — the eval suite (Milestone 1; see the playbook)
- CI wiring — the declared verification, hardening, and deterministic security gates
  (SAST / SCA / secret scanning)

## Worker-model and effort re-audit

The internal agents intentionally inherit the model selected for the Owner/parent
worker. When changing that model, harness, or runtime configuration, rerun the
representative eval suite and verify tool use, context loading, handoffs, mutation
behavior, and review quality. Keep worst-case gates untouched until evals prove a
change safe. Both canonical agent contracts require `effort=max`; the Codex TOML
adapters override only reasoning effort and never pin a model. A runtime that cannot
honor or disclose `max` must block. Model or effort changes are eval-gated, not
accepted by reputation or silent fallback.

---
name: prep
disable-model-invocation: true
description: >-
  Prepare a repository's verification infrastructure for this system — the three-command core (check / check-<capability> / golden) plus conditional mutation/fuzz hardening commands, the metric-class gates (stack-agnostic — the class is the requirement, the tool is an instance), the golden harness skeleton, minimum CI, and the ratchet baseline. Brownfield-safe: detect, extend, never overwrite; everything proven by running it.
argument-hint: "[optional: stack hints, or the first capability name]"
---
Prepare this repository so the implementation Owner, General Code Reviewer,
Mutation Hardener, external review pipeline, and CI have the verification
infrastructure they expect. Additive and
brownfield-safe: **read before writing, extend instead of replacing,
flag anything you had to work around.** No application code changes.

## Phase 0 — Detect

Identify: stacks present (TypeScript? Go? both?), layout (monorepo?
capability folders?), existing test runners and configs, existing
Makefile / package scripts / justfile, existing CI workflows, current
coverage if measurable. Report the findings in one short block before
changing anything.

## Phase 1 — The commands interface (the contract)

The harness learns how to verify from a three-command core plus two conditional
hardening command families. The tool is free (Make, just, npm scripts — follow
repo convention); the **interface is fixed**:

- `check` — lint + typecheck + tests, whole repo.
- `check-<capability>` — the same, scoped to one capability folder
  (the chunk loop's command; a pattern — one target per capability).
- `golden` — the reference-value tests only, reading
  `specs/<capability>/tables/`.
- `mutation-<capability>` — pinned, differential mutation for one eligible
  capability/target, with structured coverage and survivor output.
- `fuzz-<capability>` — property/fuzz targets for applicable parsers,
  validators, untrusted-input, serialization, protocol, and state-machine
  surfaces; the command may explicitly report N/A when no target applies.

Create or extend them. Then declare them in the root `AGENTS.md` under
`## Commands`. If a runtime needs an adapter such as `CLAUDE.md`, configure it
separately; never create a competing operational authority.

Also preserve the shared Spec Anchored routing in `AGENTS.md` and ensure
`.agent-runs/` is present in `.gitignore`. Runtime logs, approvals, evidence,
hardening handoffs, Owner dispositions, and results never live under
`.claude/`, `.codex/`, or `.cursor/`.

## Phase 2 — The metric classes (stack-agnostic)

The gauntlet is defined by **metric classes, not tools**. Every class
below must have a living instance when prep finishes, whatever the
stack: the named tools are the instances for TypeScript / Go; on any
other stack, **find the class equivalent**. Respect existing
instances. A class with no instance at the end is a **named blocker**
— never a silent absence; a class the stack genuinely lacks (e.g.
race detection) is declared **N/A in the report** — declared, not
skipped:

- **Lint + typecheck:** ESLint + `tsc --noEmit` (TS); `golangci-lint`
  or `go vet` as the floor (Go); the stack's equivalents elsewhere.
- **Tests + coverage:** the repo's runner with line and branch coverage
  reporting (Vitest / Jest; Go coverage plus the repository's branch-equivalent
  instrumentation where available). The eligible mutation target must be
  measurable independently from the whole repository.
- **Mutation testing:** a version-pinned language mutation engine with
  differential/changed-target execution, structured survivor output, and no
  mutable ignore list controlled by the hardener.
- **Property/fuzz testing:** the stack's native or pinned engine, reproducible
  seeds/corpus, minimization where supported, and a path to promote every
  discovered failure into a permanent regression test.
- **Complexity/CRAP and duplication:** pinned tools or deterministic scripts that
  can be run on the changed/eligible target; absence is a named blocker for the
  hardening workflow rather than an invented metric.
- **Concurrency / race detection** where the stack offers it
  (`go test -race`); N/A-declared where it doesn't.
- **Secrets scan:** `gitleaks` — stack-independent, always present,
  **blocking from the first run**: secrets are incident-class, not
  ratchet-class. A true finding means rotate now; triage immediately;
  never grandfather a secret. (The ratchet posture applies to lint
  and security-analysis counts — measure first, then block-on-new —
  not here.)
- **Security static analysis:** `gosec` (Go); the stack's equivalent
  elsewhere (`semgrep`, `npm audit`, `bandit`, …).
- **Build.**
- **E2E / browser (web stacks):** a deterministic browser suite as
  `check-e2e` — Playwright as the instance: one scenario per
  UI-facing acceptance criterion, blocking in CI; N/A-declared for
  pure backend. The agent-facing access surface (`agent-browser`,
  guide loaded via its own `skills get core` stub) is the loop's
  instrument, never the gate.

**Tools are part of the wiring — install them, don't just configure
them.** Create a `bootstrap` target that installs the pinned toolchain
(`tools.go` + `go install` for Go tools; a version-pinned `gitleaks`
binary) and **run it in this session**: config without the binary is a
gate that cannot fire. Only if the environment forbids installs,
degrade to advisory config **with a named blocker** stating exactly
what to run — that is the exception, never the default path.

## Phase 3 — The golden harness skeleton

Create the data-driven harness per stack: a test that discovers
`specs/*/tables/*` (CSV or JSON), asserts input → expected output row
by row, and names each case by its **stable requirement ID** — the
addressing scheme tickets and the reviewer use. If no spec exists
yet, wire the harness against one documented EXAMPLE table (clearly
marked) so `golden` runs green **and real** from day one — the first
The first `to-spec` skill output replaces the example. Document the naming
convention where the tests live. And wire the golden's own self-test —
**golden mutation**: periodically (or on demand) mutate one
reference-table value and expect `golden` to fail; a golden that stays
green under mutated truth is disconnected from the code it claims to
verify. The standing version of the sabotage check — the oracle
testing its own wiring.

## Phase 4 — CI

Create or extend the workflow (GitHub Actions unless the repo says
otherwise): **lint, typecheck, tests + coverage, build** as separately visible
checks, plus `golden` and `gitleaks`. Wire differential mutation for affected
eligible targets on PRs and a broader scheduled run. Wire applicable fuzz/property
targets with retained seeds/corpus; long campaigns may be scheduled, but every
PR must run deterministic regression cases derived from prior findings.

## Phase 5 — The ratchet baseline

Capture the current state as the grandfathered baseline in
`.metrics-baseline.json`: coverage %, and — with the bootstrapped
tools now present — **run the lint, security-analysis, and secrets
instances once each to measure**: lint and security-analysis counts enter the baseline as
grandfathered; `gitleaks` findings are triaged immediately
(incident-class — Phase 2), never baselined. Add the check: **new violations
fail; the count may only shrink; shrinkage updates the baseline.** A
gate that demands instant purity gets bypassed; a ratchet gets
obeyed.

## Phase 6 — Prove it and hand off

Run `check` and `golden`; show the real output — done is demonstrated,
not claimed. With the measurements taken, **flip lint and security analysis
from advisory to block-on-new in this same run** — the measure-first
condition is now satisfied, and leaving the flip for later leaves the
gauntlet toothless (later never comes). Open a PR from a `chore/harness-prep` branch on the
shared PR template, listing found / added / deferred (mutation,
deeper Tier-1 evaluations) and the baseline captured, and the **class completeness table** — every
metric class → its instance → status (blocking / advisory-pending-flip
/ N/A-declared). The harness's classes are obligations: absence is a
blocker, never a footnote. The repo is now
harness-ready — the first capability enters through the `shape` skill.

Abort with a named blocker (and no half-written configs) if a stack
resists detection or an existing config conflicts irreconcilably —
report, don't guess.

## Placement — what runs where

One definition, two surfaces: the targets define; local and CI both
invoke them. Local optimizes loop speed (the agent's pulse); CI
optimizes visibility and enforcement (the promotion gate). Expensive
classes follow the promotion gate.

| Class | Local | CI | Posture |
|---|---|---|---|
| Lint + typecheck | every chunk (`check-<cap>`) | named check | block-on-new after the flip |
| Tests (unit / criteria) | every chunk + full pre-PR | named check | blocking |
| Race detection | inside `go test -race` | ✓ | blocking; N/A-declared where the stack lacks it |
| Golden | the session's evidence (output visible) | own check | blocking — the permanent normative boundary |
| Coverage (measurement) | free with the test run | ✓ | informative |
| Ratchet baseline | optional preview | ✓ | blocking at merge — a drop fails |
| Secrets (gitleaks) | optional pre-push hook | from run 1 | always blocking — incident-class |
| Security analysis | on demand | ✓ | block-on-new after measuring |
| Build | where cheap | named check | blocking |
| Mutation (source) | targeted by Mutation Hardener | diff-scoped named check + scheduled breadth | 100% line/branch and mutant resolution on the approved eligible target; zero actionable survivors |
| Golden mutation | on demand (when tables change) | scheduled | the oracle's self-test |
| Property/fuzz | focused target with reproducible seed/corpus | named applicable targets + scheduled campaigns | every failure minimized/retained and promoted to regression coverage |
| Complexity/CRAP + duplication | General Code Reviewer and Mutation Hardener | visible report/check where configured | blocking on new target violations according to repository policy |
| E2E / browser (web) | loop access via `agent-browser` — explored ≠ verified | Playwright suite, named check | blocking; visual-reg advisory/scheduled |
| Runtime behavior (post-merge) | — | telemetry observed per the spec's Observability section | feedback into lessons / spec deltas — **never a merge gate**: the gauntlet verifies declared truth; runtime-only truth feeds the flywheel |

Three cadences in practice: **per-chunk** (local, seconds — lint +
typecheck + scoped tests: the pulse), **per-PR** (local full run as
the session's evidence + CI as the gate — everything blocking above),
**scheduled** (CI — broad mutation, longer fuzz campaigns, and golden mutation:
the expensive watchers that do not slow the ordinary chunk loop).

Portability: this body works as a standalone prompt in any harness —
the semantic procedure is portable; invocation, permissions, and context loading need the harness adapter.

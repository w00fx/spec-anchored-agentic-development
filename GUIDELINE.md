# Spec-Anchored Agentic Development

> One durable logical capability contract with a stable entrypoint, and the
> code answers to it — evidence before "done". A guideline for building
> software with AI agents, from a minimal contract to supervised autonomy.

Permanent reference.

> This document is the **doctrine**: concepts, responsibilities, policies. The executable state machine is `.agents/protocols/implementation-protocol.md` — phases 0–10, terminals, gates — and the three mode adapters (`implement-feature` supervised, `implement-orchestrated` worker, `implement-backlog` unattended) declare who satisfies each gate. **On any conflict about execution, the protocol wins**; on any conflict about intent, this document wins — and either conflict is a bug to fix, never a silent exception.

> **Companion documents**: `AUTONOMY-PLAYBOOK.md` covers the widening path of autonomy (the four Milestones, Tier 1/2 validation, per-class auto-merge). `EVALS.md` is your project's eval-suite artifact — required to *widen* autonomy, not to start it narrow (Part 5).

---

## Fundamental principles

Five principles that govern everything here. When in doubt, return to them.

1. **Simplest possible change.** Delete lines instead of adding when you can. No unrequested refactors. No premature helpers. Touch only what's necessary.
2. **Root cause, not band-aid.** If a bug shows up, find out why — don't hide the symptom. No temporary fixes that become permanent.
3. **Verification is part of the work, not optional.** Every change needs a way to verify it (test, expected output, observable behavior). If you can't verify it, don't merge it.
4. **Determinism where you can, agent where you must.** Every predictable task (file management, indexing, appending to logs/lessons, path lookups, manipulating issue/PR metadata) should become a deterministic script the agent calls — not the agent's work. The agent is expensive, non-deterministic, and burns context. A script is cheap, deterministic, and auditable. If you're asking the agent for something a shell or TS could do on its own, move it to a script.
5. **Machine-produced "no" before human review.** The machine produces the first "no," not the human. Every gate the machine can run — a failing test, a type error, a lint rule, an internal hardening failure or external reviewer objection — must fire before a human is asked to look. This is *backpressure*: the check refuses the agent's work at the boundary, so the agent confronts expectations before a human does. Where a human is reduced to a clipboard relaying machine feedback back to the agent, backpressure is missing — build the check instead.

---

## How to read this document

This guideline assumes **spec-anchored development organized by capability**. You identify the **capabilities** the system delivers, establish one durable logical contract and stable entrypoint for each (business intent, rules, acceptance criteria), develop from the specs, and progress in autonomy. **Spec-anchored**: the business decision comes before the code — and the spec *stays*. It is the permanent source of truth the code answers to (drift is a bug; conformance is checked value by value), not scaffolding discarded once the feature ships. The full trajectory:

```
Identify capabilities → Specification → Development
                                            ↓
                          Operational maturity → Autonomy (narrow start → widening)
```

A **capability** is a cohesive slice of what the system *does* for the business — payments, orders, notifications, billing. Not a technical layer (controller, repository), not an isolated entity (Product, Customer), not a mechanism (cache, queue). It is naturally bounded, which is why specs are written around it. (When a capability has a clear linguistic boundary — the same word means different things on each side — its relation to what some methodologies call a *bounded context* is **mapped, not presumed** — a capability can span contexts, a context can host several capabilities; the vocabulary is optional, and you don't need it to recognize that payments ≠ orders.)

**Where this sits in the field.** A taxonomy is consolidating (arXiv's "Spec-Driven Development: From Code to Contract", 2026; echoed in the martinfowler.com *exploring-gen-ai* series) with three levels of rigor inside spec-driven development: **spec-first** — the spec precedes the code but may drift or be discarded afterwards; **spec-anchored** — the spec is permanent and the code answers to it continuously; **spec-as-source** — code is generated or derived from the spec. Kiro and Spec Kit default to spec-first per-feature flows, though both document living-spec / continuous-refinement modes; the difference here is not "they discard, we keep" but that this system **hardens** the living-spec end — permanent per-capability authority, ratification, stable IDs, conformance gates. This guideline is **spec-anchored by construction** — one durable logical authority and stable entrypoint per capability, drift treated as a bug, conformance checked value by value — and, for normative rules, moves toward as-source: the spec's reference values generate the golden tests that act as the oracle. An adaptation map for running this system on Kiro — the translation table, the execution-layer mapping, and the three limitations — ships in the bundle (`adaptations/` — `kiro.md`; `codex.md` for the harness-class peer; `claude-plus-codex.md` for running both on one repo).

The document structure mirrors the trajectory:

- **Part 1** — Project start: identifying capabilities, the spec before the code. From capability boundaries to development.
- **Part 2** — Layer 1: Permanent knowledge (operation). Context files, constitution, rules, skills.
- **Part 3** — Layer 2: Active work (operation). Specs and explicit workflow skills.
- **Part 4** — Layer 3: Backlog and operation. Issues, workflow, routine.
- **Part 5** — Autonomy trajectory. Architecture vs increment split, the basic autonomous loop (narrow start: allowlist, green CI, human on every PR), and the widening rule — the detailed Milestones live in `AUTONOMY-PLAYBOOK.md`.
- **Part 6** — Continuous vigilance. Anti-patterns, warning signs, quarterly checks.
- **Part 7** — Implementation roadmap.

**Start simple, scale when evidence forces it.** You don't need a heavyweight modeling ceremony to start. Most of the time you already know where the capabilities are (payments ≠ orders ≠ notifications) — if the code already has seams (packages, services, feature folders), scope the specs on them. When a boundary is *not* obvious, mine evidence (git co-change, dependency clustering) rather than guessing. The tools exist to scale into harder cases, not to gate the easy ones. The target is **boundaries with high cohesion and low coupling** — an engineering principle, independent of any single methodology.

**The minimum entry point (small projects).** The floor is one stable capability entrypoint, commonly a single `specs/<capability>/<capability>.md` file at first. You do not need the constitution, hardening agents, milestones, or rituals to begin. As the contract grows, that entrypoint may declare a multi-file logical corpus (`rules.md`, `acceptance.md`, `contracts/`, tables, state models) without creating a second authority. Everything else in this document is how the system scales. Start small — but start with a durable contract.

**Evolution principle:** capability boundaries are decided upfront enough to scope the first contracts. This does not emerge from vibe coding; it comes from deliberate, lightweight judgment. What evolves is the tactical detail (rules, edge cases) and the operational machinery (rules, hardening, launchers, autonomy), as implementation reveals insight and pain justifies investment. **The model does not decide the structure — the accountable human decides, in discussion with the active agent, and refines as evidence accumulates.** Templates and structures here are examples, not mandatory recipes. What matters is separation by business responsibility, explicit contracts, and versioned rules — not a prescribed topology.

**Brownfield adaptation:** apply the same approach to existing code. Intended and real boundaries diverge, so map the live system using language, ownership, transactions, co-change, and dependency evidence; discuss candidate boundaries with the active agent; then apply specification and development over the approved reorganization.

**Shared core, runtime-specific adapters.** The durable contract and implementation machinery are cross-harness by default:

- **Shared authority and context (Parts 1–2)** — capability contracts, architecture, root and capability `AGENTS.md`, and canonical engineering rules under `.agents/rules/`.
- **Shared workflows (Parts 3–5)** — skills under `.agents/skills/`, the state machine under `.agents/protocols/`, paired agent contracts under `agents/`, run artifacts under `.agent-runs/<run-id>/`, and external review artifacts bound to exact candidate identity.
- **Runtime-specific adapters** — only the launcher/configuration surfaces required by a harness, such as `.codex/agents/`, optional `.cursor/agents/`, or Claude-specific hooks/routines under `.claude/`.

The pieces, in plain terms:

- **skill** — an explicit workflow with ordering, gates, artifacts, and terminals;
- **`AGENTS.md`** — the cross-harness routing layer and concise operational floor;
- **`.agents/rules/`** — canonical engineering instructions, loaded explicitly according to `AGENTS.md` and the active workflow;
- **protocol** — the shared state machine and artifact contracts under `.agents/protocols/`;
- **launcher** — whatever starts a run and validates its structured terminal outside the transcript;
- **internal hardening agents** — isolated authoring agents that improve the candidate and return exact commits/reports for Owner inspection;
- **external reviewers** — report-only systems outside the implementation worker, bound to the final candidate;
- **`.agent-runs/<run-id>/`** — gitignored runtime state, logs, approvals, evidence, handoffs, dispositions, and result.

The shared artifacts do not move when the harness changes. Only adapters and launch syntax do.

---

## Part 1 — Project start: identifying capabilities, the spec before the code

The business structure comes before the code. You don't discover architecture via vibe coding — you identify the capabilities deliberately (lightweight), specify them, and then develop. The precise rule: **architectural decisions are neither originated nor ratified autonomously; implementing a ratified decision is decomposable into tickets** — origin of authority is human, tracking of work is normal backlog. What does NOT come on day 1 is the full operational machinery (extensive rules, autonomous routines, the widening of autonomy) — that evolves as the project matures. But knowing your capabilities and their boundaries is the starting point.

Greenfield: identify the capabilities before the project. Brownfield: map the existing system's seams before applying the rest.

### Stage 0 — Identifying capabilities

Before writing production code, you need to know the **capabilities** the system delivers and where their boundaries are — at least enough to scope the first specs. This is lightweight judgment, not a heavyweight ceremony.

**Start from what is already obvious.** In most projects you already know where the capabilities are — payments ≠ orders ≠ notifications. If the code already has seams (packages, services, feature folders), use them: the boundary already exists, just scope the spec on it. You don't need any ceremony to recognize the evident. This is where you start.

**Signals that you've crossed a boundary** (useful when it's *not* obvious):

- **The language changes** — the same word means different things ("Product" in the catalog ≠ "Product" in inventory). *The single best signal.*
- **The actor changes** — the primary actor shifts from Sales Rep to Warehouse Manager.
- **The change cadence changes** — the catalog changes daily, a payment rule quarterly.
- **What changes together groups together** — things that always change in the same edit belong to the same capability; when a different set starts changing together, that's another boundary.
- **Transactional consistency** — what must be atomic stays together; what tolerates eventual consistency can split.

**When the boundary is not obvious, mine the evidence** (especially in a large existing codebase, where intended and real boundaries diverge):

- **Co-change / change-coupling** (git history) — frequent co-change is **evidence to investigate a boundary, not a verdict**: triangulate with language, dependencies, and ownership. A module that changes for N unrelated reasons hides N boundaries.
- **Dependency-graph clustering** — clusters of high internal coupling with a thin interface between them (tools: `dependency-cruiser`, ArchUnit, Service Cutter).

For genuinely complex domains where boundaries resist these heuristics, deeper modeling techniques (Event Storming, subdomain analysis) are available — but they are an **escalation for hard cases, not the starting point.**

**The incremental flow:** boundaries you can already justify (the majority) — draw them now, they're cheap to find and expensive to retrofit. The ambiguous middle (you don't yet know if it's one capability or two) — start together and split when evidence forces it (co-change, leakage, the shared part growing). "Start simple, reject complexity until justified" does NOT mean "wait for the pain" — it means rejecting *unjustified* complexity. A known business capability is already justified.

**The distinction that protects against Big Design Up Front:**

- **Boundary identification** (which capabilities, how they relate) is upfront and lightweight. It's what you do in this stage.
- **Tactical detail** (each rule, each edge case) evolves with implementation. It does NOT need to be complete here.

The initial boundaries are a deliberate starting point, not an immutable model. As implementation reveals deeper insight, boundaries and rules can refine. The spec evolution mechanism (with `requires_human_approval`) exists exactly for this.

**Done when:** you have the capabilities and how they relate, and you can explain to another person what each one does and doesn't do. You don't need every domain rule detailed — that comes in specification and development.

### Stage 1 — Specification

From the identified capabilities, create a capability spec (see Part 3) for the ones you're going to implement.

You don't need to specify ALL capabilities at once. Specify the first ones — the highest-value ones or those that unblock dependencies. The others are already on the map and will be specified when their turn comes.

The spec captures the known business source of truth: domain rules, edge cases, non-goals, contracts with neighbors. When a rule derives from an external source (norm, regulation, contract), the spec cites the source.

**Output:** specs per capability, ready to guide development.

### Stage 2 — Development

From the specs, implementation via skills (`implement-feature` — see Part 3).

- Each capability is implemented from its spec.
- A large feature within an existing capability starts as a spec delta (`shape` against the existing spec) merged at the gate before any code — any new business rule it introduces lands in the capability spec (permanent) as PR 1; `spec-to-tickets` then breaks it into frontier slices, each carried by its own normal-sized plan (protocol Phase 3).
- Implementation is incremental: one capability at a time, by priority. The map from Stage 0 covers the boundaries you could already justify; the ambiguous middle splits when evidence forces it, and construction is phased either way.
- Refinement of capability boundaries/spec as insight emerges, always with the `requires_human_approval` flag — because a change in a boundary or domain rule is a business change, and business needs a human eye.

### Operational maturity

A dimension orthogonal to the stages above. Even spec-anchored, a freshly started project (first capability being implemented) is different from a mature project (several capabilities in production, real dependencies, autonomy). The full operational machinery enters as the project matures.

**Minimum CI** — prerequisite to consider the base "operational." Four items, all blocking in PR:

- Unit tests running on every PR
- Lint configured (consistent rules, not optional)
- Coverage threshold per capability (not global)
- Green build as a merge prerequisite

Deeper code evaluations include complexity, duplication, dependency structure, mutation testing, property/fuzz testing, and security checks. Mutation testing is the deterministic hollow-test detector: deliberately violate the code and require the relevant evidence to fail. For every repository-declared eligible mutation target, the internal Hardener requires 100% line coverage, 100% branch coverage, 100% mutant resolution, and zero actionable survivors. Brownfield scope is controlled by target eligibility—not by lowering the target's bar: start with changed and critical logic, then widen coverage over time; full-codebase mutation may remain scheduled or release-gated. Tools, versions, targets, and budgets are repository rulings, not improvised per run.

After minimum CI, the **autonomy trajectory** (Part 5) starts narrow and widens over the stable base — the widening criteria live in `AUTONOMY-PLAYBOOK.md`. From Part 2 onward, all content in the guideline assumes this operational base.

### The errors that kill a project

**Starting to code without identifying capabilities.** Skipping boundary identification and going straight to code produces exactly what you want to avoid: disorganized structure, capabilities that blur together, a system impossible to stabilize later. By week 8 it's 30k lines, nobody knows where anything is, and changes break three things. Symptom: you or the active agent asks "where does X go?" and there's no clear answer. This does not require any heavyweight method — it requires knowing your capabilities and their seams, which for most projects you already do.

**Over-detailing before implementing.** The opposite error: trying to specify every rule, every edge case on paper before writing a line. Capability boundaries often only sharpen during implementation. Complete tactical specs upfront become debt before any code runs. Symptom: editing spec more than code in the first weeks.

The balance: **boundary identification upfront (lightweight), tactical detail emergent (with implementation).** The art is knowing how much to define beforehand — the capabilities and how they relate yes; each detailed rule, no.

---

## Part 2 — Layer 1: Permanent knowledge

**Language convention:** all agent-facing artifacts — `AGENTS.md`, specs, `.agents/rules/`, `.agents/skills/`, `.agents/protocols/`, and internal-agent contracts — are written in English, regardless of the team's language. This published scaffolding uses English as its canonical artifact language for cross-harness portability; a repository may declare another canonical language. Domain terms remain verbatim and authoritative in the capability language, and any language-policy change should be evaluated against representative tasks. Discussion and planning can happen in the team's language; the versioned artifacts the agent reads are in English.

Context engineering operates in three layers. Mixing them is the biggest source of problems.

**Layer 1 — Permanent knowledge** (this part): conventions, domain rules, architectural decisions, glossary, contracts, root/capability `AGENTS.md`, `.agents/rules/`, `docs/`, `specs/`, and `architecture/`. Changes rarely; each change requires a conscious commit.

**Layer 2 — Active run state** (Part 3): proven delta, assumptions, approved plan/scope, evidence, hardening targets and handoffs, Owner dispositions, logs, final candidate, and result. It lives under the gitignored `.agent-runs/<run-id>/`; sanitized copies may be retained as CI artifacts. This state is operational evidence, not permanent repository authority.

**Layer 3 — Intent and prioritization** (Part 4): what needs to be done, in what order, and why. It lives in GitHub Issues with explicit dependencies and outcomes.

**Flow rule between layers:** when something learned in Layer 2 deserves to survive, it moves up to Layer 1. When something in Layer 1 is obsolete, update or remove it.

### Folder structure

Two fixed principles, independent of project type:

1. `docs/` and `specs/` are centralized sources of durable domain truth.
2. Code is organized by capability; scoped `AGENTS.md` files live next to code only when additional operational context is useful. Runtime loaders differ, so workflows explicitly read the target capability file when its presence in the effective instruction chain is not proven.

```
project/
├── AGENTS.md                         ← cross-harness routing and operational floor
├── GUIDELINE.md                      ← doctrine
├── EVALS.md                          ← qualification and regression-eval artifact
├── .gitignore                        ← includes .agent-runs/
│
├── architecture/
│   ├── constitution.md               ← non-negotiable principles
│   ├── pipeline.md                   ← contracts between capabilities
│   └── decisions/                    ← ADRs
│
├── agents/                           ← canonical paired internal-agent contracts
│   ├── general-code-reviewer.md
│   ├── general-code-reviewer.toml
│   ├── mutation-hardener.md
│   └── mutation-hardener.toml
│
├── .agents/
│   ├── skills/                       ← canonical cross-harness workflows
│   ├── protocols/                    ← shared state machine and artifact contracts
│   └── rules/                        ← canonical engineering rules, explicitly loaded
│
├── .agent-runs/                      ← runtime-only, gitignored; never packaged
│   └── <run-id>/                     ← state, log, evidence, handoffs, dispositions, result
│
├── .codex/                           ← optional generated/runtime-specific adapter
│   └── agents/
├── .cursor/                          ← optional Cursor-specific adapter/configuration
├── .claude/                          ← optional Claude-only hooks/routines
│   ├── hooks/
│   └── routines/
│
├── docs/                             ← glossary and reference material
├── specs/                            ← logical capability contracts
│   ├── _template/capability-spec.md
│   └── <capability>/
│       ├── <capability>.md           ← stable entrypoint and corpus map
│       ├── contracts/
│       └── <optional companion files>
│
└── src/                              ← code organized by capability
    └── <capability>/
        ├── AGENTS.md                 ← scoped context and contract pointer
        └── <code>
```

`src/` is generic; use `app/`, `lib/`, `packages/`, or the layout your stack expects. The invariant is capability-oriented code, a stable contract entrypoint, and explicit context routing.

Topology may be sequential, service-oriented, event-driven, monolithic, frontend, or multi-repository. The principle is unchanged: centralized durable truth, capability ownership, explicit contracts, and workflows that can resolve the relevant corpus in the environment where they run.

### Where specs live, by topology

The unit never changes — **one logical capability authority with a stable entrypoint, in any topology**. The corpus may begin as one file and later include declared companion files. Deployment topology changes where that corpus lives, how many deployables implement it, and how much weight the Contracts section carries. Every implementing agent must be able to resolve the authoritative corpus at an immutable revision in its working environment. Repository boundaries break local proximity; the arrangements below restore access, in order of escalation:

1. **Capability contained in one repo** (the healthy microservice case, and every modular monolith): the spec lives in that repo. Nothing new — `specs/` per repo.
2. **Capability spans a few repos** (`payment-api` + `payment-worker` + `payment-reconciler` = one capability, three deployables): the spec lives in the **owner repo** — the service that owns the write path / the data the rules govern. Each other repo's root context file carries three things: this service's role in the capability (2-3 sentences), the canonical pointer to the spec (repo + path + how to fetch it), and where the local contracts are. If "who owns it" is ambiguous, that's the signal for the next step.
3. **Several capabilities crossing repos, or ambiguous ownership**: a **dedicated specs repo**, vendored into each consuming service at a stable path (submodule, subtree, or a sync bot that opens PRs on spec changes). A machine-synced copy with a declared canonical source is not duplication — drift becomes an unmerged sync PR (a visible failing check) instead of a silent divergence. What kills is the *hand-made* copy: it has no drift detector.

**The spec can be remote-with-pointer or vendored; contracts must be local.** The schema a service consumes/produces is what its code compiles against and its contract tests run against — vendored schemas or generated packages from the owner, never "see the other team's repo."

**When one capability spans deployables, its spec gains a responsibility map**: which deployable owns which slice (api receives and validates; worker processes; reconciler verifies), and the contracts *between them*. Same pattern as `pipeline.md`, one level down — `pipeline.md` declares contracts between capabilities; this map declares contracts between one capability's deployables. It is what gives external conformance review an explicit responsibility contract when a worker diff crosses deployables.

Two things multi-repo gives you for free: `requires_human_approval` on spec changes stops being convention and becomes **mechanical permission** (branch protection + CODEOWNERS on the specs repo or path) — a large feature's new rule lands as PR 1 on the spec, human-gated by the platform, and PRs 2..N implement it, each repo recording which spec version it implements. And for work that crosses services, a **workspace** (the relevant clones side by side, one workspace context file on top) restores the proximity a repo boundary broke.

Be honest about the cost: these mechanisms *manage* multi-repo coordination — they don't eliminate it. Vendoring, sync bots, and version pinning are a tax the modular monolith and the monorepo don't pay; there, the default layout just works. If you're choosing topology now and already know capabilities will span services, a monorepo makes the spec model trivial. Multi-repo is legitimate for other reasons (independent deploys, team ownership) — and its price includes this section.

### Context discipline (what to write, what to leave out)

Golden rules for operational context:

- Document only what the agent cannot safely infer from code, types, scripts, or standard tooling.
- Keep code organized by capability so the structure itself communicates ownership.
- Prefer binary, testable obligations over vague advice.
- Treat stale context as a defect; review it like code.
- Keep durable truth in specs/architecture, reusable engineering obligations in `.agents/rules/`, procedures in `.agents/skills/`, and runtime state in `.agent-runs/`.

> **`AGENTS.md` is the cross-harness operational context and routing layer.** The root file contains the concise floor every run needs: authority order, canonical paths, project commands, rule-loading requirements, internal-agent order, and runtime-artifact location. Scoped `AGENTS.md` files may specialize that context for a capability. Loader behavior differs by runtime, so transactional workflows explicitly read the target capability file when its presence in the effective instruction chain is not proven. A runtime-specific file such as `CLAUDE.md` may import or adapt `AGENTS.md`, but it is not a competing authority.

`AGENTS.md` points to capability contracts and engineering rules; it does not duplicate them. The bundle ships a concrete root file to customize.

### Root `AGENTS.md`

Minimum responsibilities:

```markdown
# Project agent instructions

## Authority
- Ratified capability contracts govern business semantics.
- Approved ticket, plan, and scope constrain the current run.
- Current code proves observed behavior, not intended behavior.

## Canonical paths
- Skills: `.agents/skills/`
- Protocols: `.agents/protocols/`
- Engineering rules: `.agents/rules/`
- Internal agent contracts: `agents/`
- Runtime state: `.agent-runs/<run-id>/`

## Rule loading
- Read `.agents/rules/truth-layer.md` for every transactional change.
- Read `.agents/rules/testing.md` for code, tests, or behavior changes.
- Read `.agents/rules/package-by-feature.md` when production paths or boundaries change.
- Do not assume `.agents/rules/` auto-loads merely because it exists.

## Verification
- <focused command>
- <capability command>
- <full gate>

## Internal hardening
1. `general-code-reviewer`
2. `mutation-hardener`

Every handoff returns an exact commit/report to the Owner for inspection.
```

Keep domain detail in the capability contract, architectural trade-offs in ADRs, and reusable engineering obligations in `.agents/rules/`.

### `AGENTS.md` per capability

A scoped file next to `src/<capability>/` is a pointer and navigation aid, not a copy of the spec. It should name the stable contract entrypoint, scope/non-goals, unusual commands, relevant rules, and local ownership constraints. Transactional skills read it explicitly when required.

```markdown
# <Capability>

**Contract:** `specs/<capability>/<capability>.md`
Read the logical corpus before changing domain behavior.

## Scope
<what this capability owns and explicitly does not own>

## Verification
- Focused: `<command>`
- Capability gate: `<command>`

## Local constraints
- <only non-obvious, recurrent constraints>
```

Do not import the entire contract corpus into `AGENTS.md`; keep a stable pointer and load the full authority when the change touches semantics.

**Conditional rules are routed explicitly.** `.agents/rules/` is the canonical repository location, not a cross-harness auto-loading primitive. The root `AGENTS.md` and transactional skills decide which rules apply from the task class, touched paths, and approved scope. Runtime-specific path-scoped loading may be added as an optimization, but shared correctness must not depend on it.

### Constitution

`architecture/constitution.md` consolidates non-negotiable principles. 15-30 lines.

```markdown
# System Constitution

Non-negotiable principles. Changes here require a conscious decision
and an ADR in `architecture/decisions/`.

## Sensitive numeric types

Every high-sensitivity numeric value (monetary, percentage used in calculation, quantity in a small unit) uses a fixed-precision type (Decimal, BigDecimal, equivalent). Never float.
Conversion: string → precise type directly, never via intermediate float.
Rounding: explicit and single policy (e.g. ROUND_HALF_EVEN) unless a normative source specifies otherwise.

## Audit trail

Every critical decision the system makes is traceable to:
1. The applied rule (with source reference, when external)
2. The input that triggered the decision
3. The code version that produced the decision

No exceptions. No "logs later."

## Normative source citation

Every coded domain rule that derives from an external source (regulation, contract, technical specification) cites the source: identifier + version/date + scope.
Form: inline comment or docstring reference.

## Separation of responsibilities

- [Stage 1, e.g. collection/ingestion]: only captures. No rule application.
- [Stage 2, e.g. parse/validation]: validates structure. No business-rule application.
- [Stage 3, e.g. analysis/decision]: classifies and decides. No final-value computation.
- [Stage 4, e.g. output/final calculation]: computes/aggregates. No applicability decision.

Breaking this separation requires an ADR.

## Immutability of past rules

A past-period rule does not change retroactively in the code, even if the current interpretation differs. Explicit versioning of rules by validity period.
```

### Shared engineering rules (`.agents/rules/`)

Rules are short, stable, versioned instructions for recurrent engineering obligations. The root `AGENTS.md` routes them; transactional skills and internal agents read applicable rules explicitly. The directory itself does not guarantee loading.

The bundle ships:

- `truth-layer.md` — protects specs, reference/golden oracles, baselines, and named write flows;
- `testing.md` — selects evidence boundaries, requires regression coverage, mutation hardening, and property/fuzz testing when applicable;
- `package-by-feature.md` — keeps production code within the capability that owns its language, rules, and outcome.

A new rule should be added only when the obligation is recurrent, materially costly to forget, and reviewable or mechanically enforceable. Keep explanation/examples in references when the rule would otherwise become a manual.

**Instructions are not enforcement.** `AGENTS.md` and `.agents/rules/` guide behavior. Guarantees belong in deterministic validators, permissions, fast-feedback hooks where available, and final-state CI. A silently edited oracle or lowered threshold must fail mechanically regardless of the harness that produced the candidate.

The Claude-specific hook `.claude/hooks/require-spec-for-new-capability.sh` remains an optional adapter for fast feedback. It is not the shared authority and does not replace CI.

### Skills (`.agents/skills/`)

Skills are folders containing an explicit workflow, references, and optional deterministic scripts. Codex and Cursor can consume repository skills from `.agents/skills/`; other runtimes may use an adapter. Transactional skills are invoked explicitly, while reference skills may be loaded by description when the runtime supports it.

Use a skill when ordering, gates, side effects, state, or reusable tooling matter. Use a rule for a short recurrent obligation and a document for durable knowledge.

Principles:

1. The description is a routing trigger, not a summary of the entire workflow.
2. Put the state machine and load-bearing gates in `SKILL.md`; place detail in `references/` and deterministic behavior in `scripts/`.
3. Document non-obvious failure modes and rationalizations, not facts already visible in code or types.
4. Transactional skills must declare explicit invocation and honest terminal states.
5. Grow skills from observed failures and evals, not speculative completeness.

```
.agents/skills/<skill-name>/
├── SKILL.md
├── references/
├── scripts/
└── agents/openai.yaml        # optional runtime metadata
```

## Part 3 — Layer 2: Active work

Each implementation run owns a gitignored directory at `.agent-runs/<run-id>/`. It contains the proven delta, assumptions, approvals, plan, scope, evidence, logs, hardening targets/handoffs, Owner dispositions, final candidate identity, and terminal result. Chat/task UIs are convenience views only; the run directory is the operational record for resume and audit, and a sanitized copy may be retained by CI.

### How to create a spec

There is **one durable contract type — the logical capability spec corpus.** The old "disposable feature spec" is gone: what is disposable is the implementation plan, not a second semantic authority.

**The capability spec corpus (permanent)**

Has one stable entrypoint such as `specs/<capability>/<capability>.md`. It may remain one file or declare companion files under the same capability directory. Created once per capability. Updated when architecture or a domain rule changes. **Human authority, not necessarily human authorship** — agents may research, draft, and materialize proposals; what makes a spec the business source of truth is the human-protected ratification (the merge on the protected branch). **Spec evolution during implementation follows the writer matrix**: the **supervised** adapter may materialize an amendment after an explicit in-session human gate (semantic-amendment: affected IDs, old → proposed meaning, rationale — the PR ratifies with `requires_human_approval`); **orchestrated and unattended** adapters are proposal-only, materializing through `to-spec` + the protected-branch PR. A spec change is a business-rule change: the human gate precedes any code guided by the new meaning — never normalize intent to match code.

Method: research-driven. The source of truth is external (norms, regulation, existing systems, client documents).

A frontend functional area is just a capability whose inputs/outputs are flows and interaction states instead of data — it uses the **same** template. The interview covers flows, interaction states, and the consumed API contract (referencing the owning backend capability).

How:

1. Create the empty file at the correct path.
2. Start a planning-capable session in the target repository/capability.
3. Invoke the explicit `shape` skill (then `to-spec` writes the file) or use a direct prompt:

```
I'm going to create a spec for [capability]. Use the template in
spec-templates/capability-spec.md.

Research first:
- Read <upstream-context>/AGENTS.md (the input we receive)
- Read architecture/pipeline.md (the output contract)
- Read architecture/constitution.md (principles)

Then interview me with AskUserQuestion about:
- Specific domain rules
- Edge cases and expected handling
- Non-goals (what this capability does NOT do)
- External dependencies

Don't write code. When you've covered everything, write the spec.
List open questions if there's ambiguity.
```

**Large features in an existing capability**

There is no separate "feature spec." When a change is bigger than three sentences but lands in a capability that already has a spec, you do two things — neither of which is a new permanent artifact:

1. **The work starts as a spec delta and lands as frontier slices** — `shape` interrogates against the existing spec and `to-spec` writes the delta (new rules and criteria issued as typed stable IDs in continuation); after the delta merges at the gate (the rule-merge below), `spec-to-tickets` breaks the feature into tracer-bullet slices, each carried by its own normal-sized plan (protocol Phase 3) — the same planning `implement-feature` already produces. Plans remain disposable: scaffolding for each slice, discarded when it lands.
2. **If the feature introduces a new business rule, that rule is merged into the capability spec** — because a rule is a source of truth, and source of truth lives in the durable capability corpus (with `requires_human_approval`, since it's a business-rule change). If the corpus becomes difficult to maintain, first split it into declared companion files under the same stable entrypoint. Split the capability itself only when language, ownership, invariants, transaction boundaries, or change cadence show a real domain boundary.

So the durable record of a large feature lives in three places, each with its role: the **rule** goes into the capability corpus, the **plan/run evidence** lives under `.agent-runs/<run-id>/` during execution, and the **human-facing understanding of what was done and why** may go into the `explain` walkthrough (`docs/walkthroughs/`). None of these is a "feature spec."

**When does a change get no spec at all?** If you can implement it directly from the existing capability spec — it only combines rules already there and introduces no new source of truth — go straight to implementation with a light plan. The test is not lines of code; it is "does this introduce a rule the capability spec doesn't already cover?"

### Recommended explicit workflow skills

Saved canonically as `.agents/skills/<name>/SKILL.md` and versioned in the repository. Runtime adapters may add metadata or launcher syntax, but they do not create another workflow authority.

**`plan-from-issue`** — generates a phased implementation plan from a GitHub issue (reads the issue, the capability's context file and spec, enters Plan Mode; no implementation). Ships in the bundle.

**`shape`** — the work-shaping interview, working the question frontier in rounds — every currently-askable question at once, each with a recommended answer — the codebase consulted before the human. Interrogates an idea, a transcript, existing code, or an existing spec (grill-back: divergence probe, boundary probe, oracle coverage), or sharpens a task — the interview only; `to-spec` writes the file. Ships in the bundle.

**`to-spec`** — writes or updates the capability spec from the interview: fills the template from a `shape` session (or provided notes), never interviews back — gaps become open questions; new items issued as typed stable IDs in continuation, existing IDs never touched. Ships in the bundle.

**`prep`** — one-time repository preparation: the verification interface (`check` / `check-<capability>` / `golden` / `mutation-<capability>` / `fuzz-<capability>`), the metric-class gates (stack-agnostic: the class is the requirement, the tool an instance; absence = named blocker), the golden harness skeleton reading `specs/<cap>/tables/`, minimum CI as visible checks, and the ratchet baseline (grandfather the count; it only shrinks). Brownfield-safe, proven by running. Ships in the bundle.

**`orchestrate`** — full-project orchestration in **resolution-gated waves** (the gkpacker field pattern, source #48, adapted): wave table from the explicit `Blocked by` graph; one worker per ticket in child worktrees cut from fresh, verified `origin/main`; persistent monitor with CI and review **fingerprints** (new feedback revokes review-ready — CI green is not the whole gate); external-review triage for humans, bots, and APIs, keyed to the exact PR head; human merges gate each wave. Orca mechanism loaded at runtime (`ORCA skills get orchestration --full`); baked-in defaults never re-asked; caps, question policy, and the 2-consecutive halt built in. Ships in the bundle.

**`spec-to-tickets`** — breaks a committed capability spec (or the shaping session that produced it) into tracer-bullet tickets anchored on the spec's pointed stable IDs, each with blocking edges; quizzes the human on granularity and edges before publishing to a local `tickets.md` or to GitHub Issues, blockers first so edges reference real ids. Wide refactors go expand–contract. Ships in the bundle.

**`review-spec-drift`** — the periodic whole-capability audit: spec ↔ code ↔ contracts divergence, reported as critical / relevant / cosmetic drift. Complements the external diff-scoped conformance review. Ships in the bundle.

**`implement`** — explicit convenience alias for the complete `implement-feature` skill. It loads and follows the supervised adapter without duplicating its gates. Ships in the bundle.

Three entry points exist by mode, each invoked directly using the current runtime's skill syntax:

- **supervised:** `implement-feature <issue|slice>` (or the `implement` alias), with human gates in-session;
- **orchestrated:** `implement-orchestrated issue #N --mode <assisted|autonomous>` as the worker's first instruction;
- **unattended:** `implement-backlog issue #N`, invoked by a launcher that validates the structured terminal.

Ordinary prose that merely names a transactional skill is not a valid launch contract. Interactive modes may wait for human decisions; headless modes replace every would-be question with a named blocker or an externally mediated approval.

### Optional runtime completion loops

A runtime may provide a completion re-check such as Claude Code's `/goal`. Treat it as an optional, separately evaluated wrapper around a directly invoked transactional skill — never as the skill loader or canonical engine. The evaluator must be bound to artifact evidence and honest terminals, and the composition must be qualified for the exact harness/model configuration before operational use.

The portable launch contract remains the explicit skill invocation and `.agent-runs/<run-id>/result.json`.

### Implementation skills and internal hardening agents

The three implementation skills are owner adapters over
`.agents/protocols/implementation-protocol.md`. They share phases 0–10 and differ
only in who satisfies ambiguity, approval, truth-change, and scope-expansion
gates:

```text
implement-feature
    human in-session

implement-orchestrated
    GitHub/orchestrator-mediated

implement-backlog
    mechanical-or-abort
```

All three use the same internal authoring pipeline after the owner has
implemented and verified the approved task:

```text
Owner implementation
    → General Code Reviewer authoring loop
    → owner inspects and accepts/rejects the exact handoff commit
    → Mutation Hardener authoring loop to the 100% target contract
    → owner inspects and accepts/rejects the exact handoff commit
    → final deterministic verification
    → PR_READY_AWAITING_HUMAN
```

Both internal agents inherit the effective model of the Owner/parent worker and
run with `effort=max`. The canonical contracts intentionally pin no model; Codex
TOML adapters override only `model_reasoning_effort = "max"`. A lower or unknown
effective effort is a configuration blocker, never a silent model switch or
runtime fallback.

The Owner remains accountable for the task. Each authoring agent runs from an
exact committed checkpoint in an isolated worktree, commits its complete delta,
and returns an alteration report containing input SHA, output commit, modified
paths, what changed, commands/results, risks, and owner-inspection instructions.
The Owner must inspect the entire diff, validate scope and approved behavior,
and rerun affected checks before accepting the handoff. Agent output is never
self-validating.

**`implement-feature`** is the supervised default. It researches the issue and
code, separates facts/decisions/assumptions, asks the human only for
load-bearing unresolved choices, proves the delta, obtains human approval of
plan/scope/evidence/mutation target, implements, runs both internal hardeners,
and opens a hardened PR. A supervised semantic amendment may be materialized
only after its explicit human gate; protected-main integration ratifies it.

**`implement-orchestrated`** owns one ticket, one worktree, and at most one PR.
Assisted mode pauses for `approved <fingerprint>`; autonomous mode may proceed
only when the ticket and policy already authorize every load-bearing choice.
Both modes abort on ambiguity, truth change, or scope expansion. The worker runs
the two internal hardeners; the orchestrator/pipeline owns external review and
CI monitoring after the PR.

**`implement-backlog`** is unattended and mechanical-or-abort. It never asks a
question or invents a semantic decision. Its plan must be a mechanically
validated subset of the qualified ticket and policy; otherwise it returns a
named blocker. It runs the same two internal hardeners and terminates at a PR,
corroborated no-change, or blocker. Merge and external review remain outside the
run.

#### General Code Reviewer — internal authoring role

`agents/general-code-reviewer.md` consolidates the local cleanup and
review work that would otherwise be spread across cleaner/architect passes. It
reviews correctness, edge and failure paths, simplicity, duplication, types,
local module boundaries, testability, and test quality; fixes concrete issues;
runs the declared checks; reviews the result again; and loops while measurable
progress is being made. It may modify production and tests inside approved
scope, but it cannot change truth, authority, thresholds, exclusions, policy,
or scope. Its terminal is `CODE_HARDENED` or a named upstream blocker — never
external approval.

For a `NO_CHANGE_CANDIDATE`, the same agent runs in non-authoring corroboration
mode and tries to break the no-op claim. Mutation is not applicable to an empty
diff.

#### Mutation Hardener — internal authoring role

`agents/mutation-hardener.md` is adapted from the focused hardener role
used in SwarmForge: differential language mutation, one file/target at a time,
progress-visible runs, separate property/fuzz commands, then CRAP/DRY and full
verification. It may alter production and tests where a surviving mutant
reveals a correctness, design, observability, or testability problem.

The default eligible-target completion contract is:

```text
line coverage = 100%
branch coverage = 100%
mutant resolution = 100%
actionable surviving mutants = 0
```

A mutant is resolved only when killed by relevant evidence or recorded as an
equivalent/tooling-limitation candidate with concrete proof for Owner and
external review. The Hardener cannot approve its own exception, hand-edit tool
manifests, lower thresholds, add exclusions, weaken tests, or alter specs and
oracles. Repository-pinned tools and commands are authoritative; missing
load-bearing tooling is a named blocker.

#### External reviews

Spec/conformance, constitution/domain, security, performance, systemic
architecture, compliance, and any independent General Code Review are outside
the implementation skills. They run through the repository's review API/tool,
CI pipeline, orchestrator, periodic audit, or human process. The internal agents
produce a hardened candidate; they do not claim those external reviews happened.
The orchestrator fingerprints external reports by candidate SHA and re-engages
the owning worker when a report blocks.

`ticket-readiness-review` remains in the bundle because it validates issue
contracts before implementation; it is not a code-review agent.

### Control classification: feedforward/feedback × computational/inferential

A lens (from ThoughtWorks) for auditing the controls above: every control is either **feedforward** (a guide applied *before* the agent acts) or **feedback** (a sensor applied *after*), and either **computational** (deterministic, runs in milliseconds) or **inferential** (an LLM, runs in seconds, catches what code analysis can't). The four quadrants, with this system's controls in each:

- **Feedforward · computational** (deterministic guides): the type system (Decimal not float), ADRs, `.agents/rules/` with `paths:`.
- **Feedforward · inferential** (LLM/prose guides): the specs, the constitution, the AGENTS.md files, the approved plan (protocol Phase 3).
- **Feedback · computational** (deterministic sensors): tests, lint, coverage, mutation testing, golden datasets, contract tests, CI.
- **Feedback · inferential** (LLM sensors): the two internal authoring hardeners, followed by external report-only reviewers bound to the final candidate.

Two things this lens makes visible. First, all four quadrants are filled — most teams have strong feedback and weak feedforward (more sensors than guides), and the spec-anchored approach is what loads the feedforward side here. Second, the two axes aren't interchangeable: feedback-only means repeated mistakes (no guide stops them up front), feedforward-only means you never confirm the guides worked (no sensor checks the result). The layering follows the cost gradient — computational before inferential (fast/cheap/deterministic first, slow/expensive/semantic second), the same gradient the deterministic verification → hardening → external review sequence encodes.

---

## Part 4 — Layer 3: Backlog and operation

What needs to be done, in what order, why. GitHub Issues with labels.

### Label schema

```
stage:    <stage-1> | <stage-2> | <stage-3> | <stage-4> | architecture
area:     <sub-area-1> | <sub-area-2> | <sub-area-3> | ...
type:     bug | feature | refactor | research | spike | tech-debt
priority: now | next | someday
```

Every issue has at least: 1 stage, 1 type, 1 priority. Area when applicable (some projects don't have sub-areas inside a stage).

The `stage:` and `area:` values derive from your capabilities — replace the placeholders with your domain's names.

### Operational conventions

- `priority:now` — maximum 3 simultaneous issues
- `priority:next` — maximum ~10 issues
- `priority:someday` — no limit, but review monthly
- Issue without priority = not triaged yet

### Lifecycle

```
[created without priority]
        ↓ (weekly triage)
[now / next / someday] OR [closed: not planned]
        ↓
[priority:now]
        ↓ (you tackle it)
[in development — branch named with issue#]
        ↓
[PR opened, references issue #142]
        ↓
[PR merged → issue closes automatically]
        ↓
[lessons update the corresponding AGENTS.md, if any]
```

### Killed issues

When closing a `someday` issue by conscious decision: comment with the reason, close as "not planned" (not "completed"). It's the memory of "already considered and discarded," versioned and searchable.

### The three rituals

**Daily (5 min, morning before coding):** look at the 3 `priority:now` issues; if one got abstract, open Plan Mode before touching it; if it already has a PR, continue.

**Weekly triage (30 min, fixed day/time):** filter issues without priority created during the week; each becomes `now`, `next`, `someday`, or `closed: not planned`. 2-3 minutes per issue. For the issue those 2-3 minutes can't decide — ambiguous scope, unclear size — run `plan-from-issue`: the phased plan and its open questions inform the call, and are the cheap `needs-refinement` check before labeling an issue for the autonomous route.

**Monthly review (45 min):** go through `someday`; kill what no longer makes sense; promote what became obvious; reorganize labels that became a mess.

### Concrete daily workflow

Starting a feature:

1. Open the repository, look at `priority:now` issues.
2. Pick one. Read comments. Check whether it got abstract.
3. Open the selected coding harness in the affected capability's directory when practical.
4. Decide: simple change, large feature, or new capability?
   - **Simple:** straight to Plan Mode with the issue as context.
   - **Large feature in an existing capability:** `shape` interrogates against the existing spec and `to-spec` writes the delta; merge it at the gate first (human approval — the rules land in the capability spec), then `spec-to-tickets` and implement from the frontier.
   - **New capability:** run `shape` → `to-spec` to create its spec, `spec-to-tickets` to break it into issues, then implement from the frontier.

   For the last two cases — anything with acceptance criteria — invoke the explicit `implement-feature` skill using the current runtime syntax: the protocol's own gates hold the run to evidence. A `/goal` wrapper is an optional, eval-gated composition (Part 3), never the loader. Plain Plan Mode remains right for the simple case.
5. Named branch: `<stage>/<sub-area>/<issue-number>-<short-slug>`. E.g.: `<stage>/<sub-area>/142-<short-description>`.

Plan Mode → Execution:

1. Enter the runtime's planning mode or equivalent read-only planning phase.
2. The Owner confirms the effective root/capability `AGENTS.md`, then explicitly reads every applicable `.agents/rules/` file and referenced contract before planning.
3. You iterate on the plan until it's good (1-6 times, usually).
4. Check "Unresolved questions" — answer them before proceeding.
5. Accept the plan, exit Plan Mode.
6. Approve implementation edits according to repository risk and sandbox policy; never let convenience bypass the two human gates.

Closing a feature:

1. Tests passing locally. Lint passing.
2. Open a PR referencing the issue (`Fixes #142`).
3. Before merging, a mental checklist:
   - Did this feature teach something that deserves to be in some capability's AGENTS.md?
   - Did a violated principle deserve to become a rule in `.agents/rules/`?
   - Does some architectural decision deserve an ADR in `architecture/decisions/`?
4. If so, the updates go **in the same PR**. Don't leave it for later.
5. Merge. The issue closes automatically.

### Nightly routine (conservative version)

This is an optional runtime-specific example. Adapt the schedule and execution surface to the installed harness.

```
Groom the issues in the [your-repo] repository.

For each issue created in the last 24h without a stage or priority label:
1. Read the issue content
2. Identify the affected stage and area (reference: architecture/pipeline.md)
3. Suggest labels via comment (don't apply)
4. Suggest priority based on impact (don't apply)
5. If it looks like a duplicate, comment suggesting a merge
6. If it looks vague, comment listing what's missing

Post a summary of:
- Issues processed with suggestions
- Ambiguous issues that need human review
- Possible duplicates

Do NOT apply labels or close. Just suggest via comment.
```

Principle: the routine recommends, you decide at weekly triage. A more autonomous version only in the Autonomy trajectory (Part 5).

---

## Part 5 — Autonomy trajectory

Autonomy over the stabilized operational base (minimum CI, see Part 1) is a **gradient, not a switch**: it starts narrow — a human approving every PR — and widens only as the regression suite earns trust. This Part gives the split that governs everything, the basic loop, and the widening rule. The detailed progression (the four Milestones, Tier 1/Tier 2 validation, per-class auto-merge) lives in **`AUTONOMY-PLAYBOOK.md`** — read it when you're ready to widen, not before.

### Architecture work vs increment

Before anything autonomous, an essential split. It defines what kind of work is happening, and consequently who drives (human vs agent) and how it enters the system.

**Architecture work.** Creating a new capability, a new sub-area, a large feature that reorganizes the pipeline. Always human-led: you plan how the system should be (create the spec), execute via `implement-feature` (local skill, with human gates at each phase), open a PR. The spec is the business source of truth — **human authority, not necessarily human authorship**: agents may research and draft; the human-protected ratification is what makes it truth. **It doesn't go through the backlog. It doesn't enter the autonomy trajectory.** Spec evolution during execution follows the writer matrix (supervised: gated materialization; other modes: proposal-only).

**Increment work.** Everything else: bugfix, tech-debt, a feature within an existing capability, an isolated rule adjustment with a normative source already cited (when applicable), a reference-table update. It enters through the backlog (GitHub Issues), goes through weekly triage, and is the only kind of work autonomy touches.

**Classification criterion.** If the change requires a new capability, a new sub-area, or reorganizing contracts between stages → architecture. If it fits in an existing capability and can be described in 3 sentences in the issue → increment. Gray zone (a medium feature touching two capabilities without changing contracts) → treat it as architecture at first; as patterns emerge, some migrate to increment.

### The basic autonomous loop (the narrow start)

The entry-level autonomous mode — the one this guideline describes — is simple:

1. Increments enter through **GitHub Issues** and weekly triage.
2. The routine picks only from a **narrow, hard-coded allowlist of classes** — well-specified bugfix, small tech-debt, an isolated rule adjustment with its normative source already cited — with permitted paths enforced in the harness, not the prompt. Never architecture work.
3. It implements via the `implement-backlog` skill (Part 3) and **opens a PR**.
4. **CI must be green before human review.** The suite is the tests accumulated from every previous feature — each anchored on its spec's acceptance criteria — and it is the mechanical net that catches regressions *outside the diff*, which a human reviewing the diff cannot see.
5. **A human reviews and approves every PR.** The human is the last line of defense, not the only one.

The narrow start does not require a formal eval suite: the allowlist plus human-on-every-PR keeps risk proportional to protection. **Widening does.** More classes, more volume, any step toward auto-merge — widening without a regression suite with a track record turns the routine into faith. How that trust is earned — Milestone 1 (evals as a safety net), Milestone 2 (Tier 1 static gates), Milestone 3 (Tier 2 dynamic validation), Milestone 4 (per-class auto-merge) — is `AUTONOMY-PLAYBOOK.md`'s subject.

**The permanent boundary — normative work.** Any change touching a normative calculation requires golden/conformance verification before entering autonomy in any form: a human PR reviewer does not recalculate values against the norm, so without the golden, nobody verifies them. Normative classes wait for that net regardless of how wide the rest has become.

### What does NOT enter the trajectory

New capabilities, new sub-areas, large features that reorganize the pipeline, architectural ADRs. These stay permanently in "human plans (creates spec) + executes via `implement-feature` + sends PR + human reviews." There is no Milestone 5.

---

## Part 6 — Continuous vigilance

### What NOT to do

AGENTS.md:

- ❌ Auto-generate with `/init` and leave it as-is. It's too high a leverage point.
- ❌ Put detailed code-style rules. Use a linter/formatter.
- ❌ Let root AGENTS.md become an unbounded manual.
- ❌ Repeat information between the root AGENTS.md and the capability ones. Use references.
- ❌ Treat AGENTS.md as a security or correctness enforcement boundary. Use deterministic checks, permissions, and final-state CI.

Specs:

- ❌ Write a spec for a 30-minute task.
- ❌ A top-down 200-line PRD before any feature.
- ❌ A spec that duplicates what's already in the capability's AGENTS.md.
- ❌ Skip AskUserQuestion because "I already know the answer."

Backlog:

- ❌ More than 3 `priority:now` issues at once.
- ❌ Add epics, milestones, sub-tasks, custom statuses in the first 2 months.
- ❌ Keep vague issues in the backlog. Weekly triage kills or refines.
- ❌ Close someday issues as "completed" when you just gave up. Use "not planned" with a reason.

Workflow and autonomy:

- ❌ Exit Plan Mode before reviewing "Unresolved questions."
- ❌ Update AGENTS.md "later." Do it in the same PR or don't do it.
- ❌ Run 5 parallel agent sessions without solid practice in 1-2.
- ❌ Adopt a framework (Spec Kit, BMAD, Taskmaster) because you feel a lack of "structure." Structure without a concrete problem becomes an abandoned system.
- ❌ Wait for a "complete" eval suite before starting. 20 tasks are worth more than 0 (see `EVALS.md`).
- ❌ Trust pass@1 for an agent that opens a PR on its own. You need pass^k.
- ❌ Auto-merge based only on tests passing before a class qualifies (`AUTONOMY-PLAYBOOK.md`, Milestone 4). Coverage is rarely proof of correctness.

### Warning signs

- **Root AGENTS.md keeps growing without a new cross-task obligation:** it's accumulating junk. Review it.
- **`priority:now` is always at 3+ issues:** you're not closing, you're stacking.
- **Same fix applied by agents repeatedly:** make it a rule in `.agents/rules/` or a hook.
- **Specs go stale after features:** you're skipping the PR checklist.
- **You opened spec-kit, BMAD, or similar in your bookmarks:** ask what concrete problem. If there's none, ignore it.
- **You haven't updated this document in 3+ months:** either it's perfect (unlikely) or it's obsolete (likely).
- **Dex's heuristic:** open the default coding harness in a fresh clone and say "run the tests." If it doesn't work first try, the AGENTS.md is incomplete — it's missing an essential setup, build, or test command.
- **You're building an elaborate workflow for a simple task:** the harness's default coding flow is usually better than a custom workflow for trivial tasks.
- **The regression suite's pass^3 dropped:** something broke. Stop changes, investigate (see `EVALS.md`).
- **Average cost per issue rising without a pass^k gain:** silent regression. Investigate.
- **You created a capability the business doesn't recognize:** speculative structure rots. A capability is justified either by the business (payments exists because you charge people — a known business capability is already justified, see Stage 0) or by divergent rules ("this part needs different rules from the rest") — never by "I thought it'd organize better." An invented one waits in the backlog until evidence shows up.
- **You're letting the model decide what comes next on the roadmap:** evolution is a human decision based on real pain, not a model suggestion. The model executes what you prioritize; prioritization is yours.

### Honest checks (re-read quarterly)

1. **Am I following the weekly triage?** If not, the whole system collapses. Focus on only that until you're back in rhythm.
2. **Are the AGENTS.md files still small and current?** If they grew, it's accumulating. If they went stale, you're not closing the loop at the PR.
3. **Do the specs reflect the code?** If not, either abandon the specs or resume the discipline. Both paths are honest. The bad one is keeping a lying spec.
4. **If autonomy widened beyond the narrow start: is the regression suite running, green, and consulted?** Widening without it is faith; a suite nobody runs is turning into a museum (`AUTONOMY-PLAYBOOK.md`). Running it is part of the work, not a bonus.
5. **Is the layout still package-by-feature — or drifting toward package-by-entity?** Run the deterministic pass: co-change analysis on git history plus a dependency-graph check (`dependency-cruiser`, ArchUnit). Edits that consistently cross capability folders, or one folder most of the codebase imports from, mean a leaked boundary or a disguised entity — redraw the boundary (Stage 0 signals) instead of adding rules.
6. **Are the specs still telling the truth about the code?** Run `review-spec-drift` on the capabilities touched most this quarter. Critical drift is a bug to fix now; cosmetic drift is a spec update to make now — a spec that lies is worse than no spec.

If all are "yes," the system is working. If any is "no," treat it as a bug — not as inevitable.

---

## Part 7 — Implementation roadmap

An order that makes sense. You don't need to do everything at once.

### Stage 0 — Identifying capabilities

Before production code, hold a lightweight human-led architecture discussion with the active agent until the initial boundaries are explainable:

- [ ] Dedicated session (Plan Mode) for identifying capabilities
- [ ] Note which capabilities are central vs supporting (helps prioritize what to specify first)
- [ ] Define capabilities and their boundaries
- [ ] Define how the capabilities relate (upstream/downstream, contracts between them)
- [ ] Document the initial architecture in `architecture/`
- [ ] (Brownfield) map the existing system and propose reorganization toward these capabilities

Done when you can explain to another person what each capability does and doesn't do.

### Stage 1 — Specification — Week 1

- [ ] Create `spec-templates/capability-spec.md`
- [ ] Write a capability spec for the first capabilities to implement
- [ ] Cite the normative source in each rule that derives from an external source

### Entering development + operational base — Week 1-2

- [ ] Set up the folder structure (Part 2) according to the capability map
- [ ] Customize the shipped root `AGENTS.md` with real commands, contract pointers, and rule-routing decisions
- [ ] Write `architecture/constitution.md`
- [ ] Write `architecture/pipeline.md` or equivalent (contracts between capabilities)
- [ ] Configure labels in GitHub Issues per the schema
- [ ] Confirm minimum CI running: unit tests + coverage per capability + lint + build. Without this, the base isn't operational yet.

### Solid operational base — Week 2-4

- [ ] Create a `AGENTS.md` per capability (start with the highest-dependency ones)
- [ ] Adopt the shipped `.agents/rules/` and add repository-specific rules only for recurrent, material failures
- [ ] Migrate existing specs to the template format
- [ ] Add `contracts/` in at least one capability (suggestion: parsers, which affects the others)
- [ ] Customize the shipped `.agents/skills/` for repository commands, labels, scopes, and runtime adapters
- [ ] Identify 10-15 representative closed issues that will seed the future regression suite (see `EVALS.md`)

### Initial automation + narrow-start autonomy — Month 2

- [ ] Configure the chosen repository launcher (GitHub Action, manual invocation, or equivalent)
- [ ] Create the nightly grooming routine (conservative version)
- [ ] Establish rituals (daily, weekly triage, monthly review) with a fixed time
- [ ] Practice the supervised Owner → General Code Reviewer → Mutation Hardener flow on representative issues before widening
- [ ] Consider turning on **narrow-start autonomy** (hard-coded allowlist + CI green mandatory + human approving every PR — Part 5)
- [ ] **Start the eval suite:** a minimal manual regression suite with 10-15 tasks (this becomes your `EVALS.md`) — required to *widen* later
- [ ] **Mechanize critical rules** with deterministic validation and a required CI gate; use hooks only for fast feedback where the runtime supports them

### Refinement + widening — Month 3+

- [ ] Add `contracts/` to the remaining capabilities
- [ ] Run `review-spec-drift` on the capabilities implemented so far — treat critical drift as a bug
- [ ] Evaluate whether Background mode is worth it for long refactors
- [ ] Evaluate whether Task Budgets make sense for large features
- [ ] Add new skills only when repeated runs show a stable workflow not already covered
- [ ] **Complete the regression suite** (30+ tasks, pass^3 baseline, production metrics tracked for 30+ days) — the widening prerequisite (`AUTONOMY-PLAYBOOK.md`, Milestone 1)
- [ ] Consider **widening** (more classes, Tier 1 in CI — `AUTONOMY-PLAYBOOK.md`, Milestone 2) when the suite is stable

### Further widening — When applicable

Milestone 3 depends on having a deployment pipeline to an integration environment — outside this guideline, it's infrastructure work. Milestone 4 depends on a consistent track record in Milestone 3 per increment class. See `AUTONOMY-PLAYBOOK.md` for criteria.

---

## Final principle

This document exists to serve you, not to govern you. When a rule here causes more friction than value, change the rule. But change it **consciously** — edit this file, commit with a reason. Silent erosion of discipline is what kills systems like this.

If in 6 months you're productive, with PRs shipping, clean code, and this has become a living reference — it worked. If it became a museum of good intentions, burn it and restart with 1/3 of the content.

# Spec-Anchored Agentic Development

> One permanent spec per capability, and the code answers to it —
> evidence before "done". A guideline for building software with AI
> agents, from a single spec file to supervised autonomy.

Permanent reference.

> This document is the source of truth for **how to work**. If something conflicts with practice, update this document — don't invent silent exceptions.

> **Companion documents**: `AUTONOMY-PLAYBOOK.md` covers the widening path of autonomy (the four Milestones, Tier 1/2 validation, per-class auto-merge). `EVALS.md` is your project's eval-suite artifact — required to *widen* autonomy, not to start it narrow (Part 5).

---

## Fundamental principles

Five principles that govern everything here. When in doubt, return to them.

1. **Simplest possible change.** Delete lines instead of adding when you can. No unrequested refactors. No premature helpers. Touch only what's necessary.
2. **Root cause, not band-aid.** If a bug shows up, find out why — don't hide the symptom. No temporary fixes that become permanent.
3. **Verification is part of the work, not optional.** Every change needs a way to verify it (test, expected output, observable behavior). If you can't verify it, don't merge it.
4. **Determinism where you can, agent where you must.** Every predictable task (file management, indexing, appending to logs/lessons, path lookups, manipulating issue/PR metadata) should become a deterministic script the agent calls — not the agent's work. The agent is expensive, non-deterministic, and burns context. A script is cheap, deterministic, and auditable. If you're asking the agent for something a shell or TS could do on its own, move it to a script.
5. **Machine-produced "no" before human review.** The machine produces the first "no," not the human. Every gate the machine can run — a failing test, a type error, a lint rule, a reviewer's objection — must fire before a human is asked to look. This is *backpressure*: the check refuses the agent's work at the boundary, so the agent confronts expectations before a human does. Where a human is reduced to a clipboard relaying machine feedback back to the agent, backpressure is missing — build the check instead.

---

## How to read this document

This guideline assumes **spec-anchored development organized by capability**. You identify the **capabilities** the system delivers, write a spec for each (business intent, rules, acceptance criteria), develop from the specs, and progress in autonomy. **Spec-anchored**: the business decision comes before the code — and the spec *stays*. It is the permanent source of truth the code answers to (drift is a bug; conformance is checked value by value), not scaffolding discarded once the feature ships. The full trajectory:

```
Identify capabilities → Specification → Development
                                            ↓
                          Operational maturity → Autonomy (narrow start → widening)
```

A **capability** is a cohesive slice of what the system *does* for the business — payments, orders, notifications, billing. Not a technical layer (controller, repository), not an isolated entity (Product, Customer), not a mechanism (cache, queue). It is naturally bounded, which is why specs are written around it. (When a capability has a clear linguistic boundary — the same word means different things on each side — it is what some methodologies call a *bounded context*; that vocabulary is optional, and you don't need it to recognize that payments ≠ orders.)

**Where this sits in the field.** A taxonomy is consolidating (arXiv's "Spec-Driven Development: From Code to Contract", 2026; echoed in the martinfowler.com *exploring-gen-ai* series) with three levels of rigor inside spec-driven development: **spec-first** — the spec precedes the code but may drift or be discarded afterwards; **spec-anchored** — the spec is permanent and the code answers to it continuously; **spec-as-source** — code is generated or derived from the spec. Tools like Kiro and Spec Kit are spec-first: per-feature specs that guide the work, then become history. This guideline is **spec-anchored by construction** — one permanent spec per capability, drift treated as a bug, conformance checked value by value — and, for normative rules, moves toward as-source: the spec's reference values generate the golden tests that act as the oracle.

The document structure mirrors the trajectory:

- **Part 1** — Project start: identifying capabilities, the spec before the code. From capability boundaries to development.
- **Part 2** — Layer 1: Permanent knowledge (operation). Context files, constitution, rules, skills.
- **Part 3** — Layer 2: Active work (operation). Specs and slash commands.
- **Part 4** — Layer 3: Backlog and operation. Issues, workflow, routine.
- **Part 5** — Autonomy trajectory. Architecture vs increment split, the basic autonomous loop (narrow start: allowlist, green CI, human on every PR), and the widening rule — the detailed Milestones live in `AUTONOMY-PLAYBOOK.md`.
- **Part 6** — Continuous vigilance. Anti-patterns, warning signs, quarterly checks.
- **Part 7** — Implementation roadmap.

**Start simple, scale when evidence forces it.** You don't need a heavyweight modeling ceremony to start. Most of the time you already know where the capabilities are (payments ≠ orders ≠ notifications) — if the code already has seams (packages, services, feature folders), scope the specs on them. When a boundary is *not* obvious, mine evidence (git co-change, dependency clustering) rather than guessing. The tools exist to scale into harder cases, not to gate the easy ones. The target is **boundaries with high cohesion and low coupling** — an engineering principle, independent of any single methodology.

**The minimum entry point (small projects).** The floor is **one spec file**. You do not need the constitution, the reviewer, the milestones, or the rituals to begin — write a single `specs/<capability>/<capability>.md` for the capability you're about to build, and start. Everything else in this document is how the system *scales*, and each piece enters when its pain shows up, in the order Part 7 gives. Start small — but start with a spec.

**Evolution principle**: capability boundaries are decided upfront enough to scope the first specs — this doesn't emerge from vibe coding, it comes from deliberate (but lightweight) judgment. What evolves is the **tactical detail** (rules, edge cases) and the **operational machinery** (extensive rules, routines, autonomy), as implementation reveals insight and pain justifies investment. **The model doesn't decide the structure — the human decides, in discussion with Claude, and refines as they learn.** Templates and structures in this document are **examples of common patterns**, not mandatory recipes. If your system has no pipeline, no layered capabilities, no sub-areas — that's fine, adapt. What matters is the principle (separation by business responsibility, explicit contracts, versioned rules), not the topology.

**Brownfield adaptation**: same approach, applied to existing code — intended and real boundaries diverge, so map the live code (implicit capability seams, de facto contracts, scattered domain rules) by mining co-change and dependency structure, propose the boundaries in discussion with Claude, and then apply specification and development over that reorganization.

**Two layers, different portability.** This guideline has two layers, and they travel differently across tools:

- **Specs and context (Parts 1-2)** — capabilities, specs, the `AGENTS.md`/`CLAUDE.md` files, the constitution. This layer is **tool-portable**: any coding agent (Claude Code, Codex, Kiro, OpenCode, Cursor) reads the same specs and context files.
- **Automation (Parts 3-5)** — the implementation skills, the reviewer, `/goal`, the autonomy trajectory. This layer is **implemented in Claude Code**; the concepts are general, the mechanism is Claude Code's. In another tool, map each piece to its equivalent.

The pieces of the automation layer, in plain terms:

- **skill** — an agent with a procedure: a workflow the model runs end to end (plan → implement → test → review).
- **`AGENTS.md`/`CLAUDE.md`** — the rules and conventions the agent loads (see the note in Part 2).
- **`/goal`** — a loop that re-runs until the acceptance criteria are met, with a fresh model checking the condition each turn (maker-checker).
- **reviewer** — a separate agent that checks the work and reports findings; it never writes.
- **`.claude/rules/`** — invariant rules loaded every session.

In another tool, `/goal` becomes that tool's loop/automation primitive, skills become its agent/workflow definitions, and `.claude/rules/` becomes its always-loaded rules file. The specs and `AGENTS.md`/`CLAUDE.md` don't change.

---

## Part 1 — Project start: identifying capabilities, the spec before the code

The business structure comes before the code. You don't discover architecture via vibe coding — you identify the capabilities deliberately (lightweight), specify them, and then develop. What does NOT come on day 1 is the full operational machinery (extensive rules, autonomous routines, the widening of autonomy) — that evolves as the project matures. But knowing your capabilities and their boundaries is the starting point.

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

- **Co-change / change-coupling** (git history) — files that always change together belong together; a module that changes for N unrelated reasons hides N boundaries.
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
- A large feature within an existing capability is carried by a larger Phase 2 plan; any new business rule it introduces is merged into the capability spec (permanent).
- Implementation is incremental: one capability at a time, by priority. The map from Stage 0 covers the boundaries you could already justify; the ambiguous middle splits when evidence forces it, and construction is phased either way.
- Refinement of capability boundaries/spec as insight emerges, always with the `requires_human_approval` flag — because a change in a boundary or domain rule is a business change, and business needs a human eye.

### Operational maturity

A dimension orthogonal to the stages above. Even spec-anchored, a freshly started project (first capability being implemented) is different from a mature project (several capabilities in production, real dependencies, autonomy). The full operational machinery enters as the project matures.

**Minimum CI** — prerequisite to consider the base "operational." Four items, all blocking in PR:

- Unit tests running on every PR
- Lint configured (consistent rules, not optional)
- Coverage threshold per capability (not global)
- Green build as a merge prerequisite

Deeper code evaluations (complexity, duplication, dependency structure, mutation testing, security checks) enter gradually as autonomy widens (Tier 1 — see `AUTONOMY-PLAYBOOK.md`); they are not a prerequisite for the operational base.

After minimum CI, the **autonomy trajectory** (Part 5) starts narrow and widens over the stable base — the widening criteria live in `AUTONOMY-PLAYBOOK.md`. From Part 2 onward, all content in the guideline assumes this operational base.

### The errors that kill a project

**Starting to code without identifying capabilities.** Skipping boundary identification and going straight to code produces exactly what you want to avoid: disorganized structure, capabilities that blur together, a system impossible to stabilize later. By week 8 it's 30k lines, nobody knows where anything is, and changes break three things. Symptom: you or Claude asks "where does X go?" and there's no clear answer. This does not require any heavyweight method — it requires knowing your capabilities and their seams, which for most projects you already do.

**Over-detailing before implementing.** The opposite error: trying to specify every rule, every edge case on paper before writing a line. Capability boundaries often only sharpen during implementation. Complete tactical specs upfront become debt before any code runs. Symptom: editing spec more than code in the first weeks.

The balance: **boundary identification upfront (lightweight), tactical detail emergent (with implementation).** The art is knowing how much to define beforehand — the capabilities and how they relate yes; each detailed rule, no.

---

## Part 2 — Layer 1: Permanent knowledge

**Language convention:** all agent-facing artifacts — the operational context file (`AGENTS.md`/`CLAUDE.md`, see the note in this Part), specs, `.claude/rules/`, skills — are written in English, regardless of the team's language. The models are trained predominantly on English, so English context reduces model drift and keeps terminology consistent. Discussion and planning can happen in the team's language; the versioned artifacts the agent reads are in English.

Context engineering operates in three layers. Mixing them is the biggest source of problems.

**Layer 1 — Permanent knowledge** (this part): conventions, domain rules, architectural decisions, glossary, contracts between stages. Lives in versioned files (`AGENTS.md/CLAUDE.md`, `.claude/rules/`, `docs/`, `specs/`, `architecture/`). Changes rarely; each change requires a conscious commit.

**Layer 2 — Active work** (Part 3): implementation plan, research notes, decisions specific to the feature being built. Lives in Claude Code's Tasks system or ad-hoc files per feature. High change during the feature, disposable afterward.

**Layer 3 — Intent and prioritization** (Part 4): what needs to be done, in what order, why. Lives in GitHub Issues with labels.

**Flow rule between layers:** when something learned in Layer 2 deserves to survive, it moves up to Layer 1. When something in Layer 1 is obsolete, update or remove it.

### Folder structure

Two fixed principles, **independent of project type** (data pipeline, API backend, web frontend, monorepo):

1. **`docs/` and `specs/` are centralized** — domain source of truth in one place, easy to navigate and version.
2. **Code is organized by capability (or functional area), and each one has its AGENTS.md/CLAUDE.md next to the code** — because AGENTS.md/CLAUDE.md is loaded by proximity to the file being edited. A AGENTS.md/CLAUDE.md far from the code isn't auto-loaded; it needs to be in the folder hierarchy of the code it describes.

```
project/
├── AGENTS.md/CLAUDE.md                          ← entry point, ~60 lines (English)
├── GUIDELINE.md                       ← this meta-doc (you read it; the agent doesn't)
├── EVALS.md                           ← eval infrastructure (required to widen autonomy)
│
├── architecture/
│   ├── constitution.md                ← non-negotiable principles · read by constitution-compliance-review
│   ├── pipeline.md                    ← contracts between capabilities
│   └── decisions/                     ← ADRs (dated decisions)
│
├── .claude/
│   ├── rules/                         ← auto-loaded every session
│   ├── lessons.md                     ← accumulated pitfalls (skills append in Phase 6)
│   ├── logs/                          ← structured per-run logs (auditability)
│   ├── commands/                      ← entry points (slash commands)
│   │   ├── implement.md               ← local entry point → implement-feature (gates, no /goal)
│   │   ├── review.md                  ← on-demand reviewer entry point (report-only)
│   │   ├── explain.md                 ← post-implementation walkthrough of the changes (reference + audit)
│   │   ├── plan-from-issue.md
│   │   ├── shape.md
│   │   ├── spec-to-tickets.md
│   │   └── review-spec-drift.md
│   ├── agents/
│   │   └── reviewer.md                ← independent router (doesn't write; routes; reports)
│   └── skills/
│       ├── implement-feature/         ← local workflow (7 phases, human gates, interactive)
│       ├── implement-backlog/         ← autonomous workflow (engine = native /goal)
│       ├── plan-review/               ← review criteria: plan approach
│       ├── general-code-review/       ← review criteria: correctness/simplicity/tests/types
│       ├── constitution-compliance-review/   ← domain criteria: Decimal, audit, source, stages
│       └── conformance-review/        ← domain criteria: diff vs spec + diff vs plan
│
├── .github/
│   └── workflows/
│       └── auto-implement.yml         ← autonomous trigger: claude -p "/goal ..." on label (skeleton)
│
├── docs/                              ← CENTRALIZED
│   ├── <domain-glossary>.md
│   ├── <norm-reference>.md
│   └── walkthroughs/                  ← /explain output: one walkthrough per implemented feature
│
├── specs/                             ← CENTRALIZED (domain source of truth) · read by conformance-review
│   ├── _template/
│   │   └── capability-spec.md         ← the spec template (permanent; one per capability)
│   ├── <capability-1>/                   ← mirrors src/<capability-1>/
│   │   ├── <capability-1>.md             ← the spec
│   │   └── contracts/
│   └── <capability-2>/
│       └── <capability-2>.md
│
└── src/                               ← CODE, organized by capability
    ├── <capability-1>/
    │   ├── AGENTS.md/CLAUDE.md                  ← points to specs/<capability-1>/
    │   └── <code>
    └── <capability-2>/
        ├── AGENTS.md/CLAUDE.md                  ← points to specs/<capability-2>/
        └── <code>
```

`src/` is a generic name — use what your stack uses (`src/`, `app/`, `lib/`, `packages/`). What matters: code grouped by capability, AGENTS.md/CLAUDE.md in each, `specs/` centralized mirroring the same names.

**Topology varies by project type — the principle doesn't.** The "unit of organization" changes depending on what you're building, but the pattern (code per context + co-located AGENTS.md/CLAUDE.md pointing to spec + centralized mirrored specs/) is universal:

- **Data pipeline / regulated system:** domain capability in stages (ingest → parse → analyze → output). May have sub-areas inside complex stages.
- **Services backend:** domain capability (orders, payments, users), not necessarily sequential.
- **Web frontend:** functional area / product feature (checkout, dashboard, auth). Each area groups pages, components, state. The spec captures UI flows, states, UX rules, and which backend endpoints it consumes.
- **Monorepo (front + back):** combines both — central `specs/` with `backend/` and `frontend/` inside, each app organized by its own unit.

Web monorepo example:

```
monorepo/
├── AGENTS.md/CLAUDE.md
├── docs/                              ← centralized
├── specs/                             ← centralized
│   ├── backend/
│   │   └── <capability>/
│   │       └── <spec>.md
│   └── frontend/
│       └── <functional-area>/        ← e.g. checkout, dashboard, auth
│           └── <spec>.md
│
└── apps/                              (or packages/)
    ├── backend/
    │   ├── AGENTS.md/CLAUDE.md                  ← backend app context
    │   └── src/
    │       └── <capability>/
    │           ├── AGENTS.md/CLAUDE.md          ← points to specs/backend/<capability>/
    │           └── <code>
    └── frontend/
        ├── AGENTS.md/CLAUDE.md                  ← frontend app context
        └── src/  (or app/)
            └── <functional-area>/
                ├── AGENTS.md/CLAUDE.md          ← points to specs/frontend/<area>/
                └── <pages, components>
```

In any topology the rule is the same: **`specs/` and `docs/` centralized; AGENTS.md/CLAUDE.md per capability next to the code, pointing to that capability's spec.** Sequential, parallel, graph, front+back — that's detail that emerges from the problem.

**Staged pipeline is ONE pattern, not an obligation.** The first example shows 4 sequential stages because it's common in data processing, ETL, regulated systems. But your system could be a monolith with non-sequential capabilities, event-driven, hub-and-spoke, domain services coordinated by an orchestrator, or something that fits no category. What matters is the principle (separation by domain responsibility, explicit contracts with neighbors, versioned rules), not the topology.

And on incrementality: **the capability map (capabilities and their relationships) is drawn in Stage 0 — but implementation is phased.** You don't build all capabilities at once. Start with the highest-value one or the one that unblocks dependencies; the others enter by priority. The difference from organic discovery: the boundaries you can justify are drawn deliberately up front instead of discovered by accident — the ambiguous middle starts together and splits when evidence forces it (Stage 0) — and construction is incremental either way.

### Where specs live, by topology

The unit never changes — **one spec per capability, in any topology** (microservices, modular monolith, serverless). What deployment topology changes is *where* specs live, *how many deployables* implement one spec, and *how much weight* the Contracts section carries. The property every arrangement must preserve: **any agent implementing against a spec must be able to read it, at a stable path, in the environment where it works.** Repo boundaries break proximity loading; the arrangements below restore it, in order of escalation:

1. **Capability contained in one repo** (the healthy microservice case, and every modular monolith): the spec lives in that repo. Nothing new — `specs/` per repo.
2. **Capability spans a few repos** (`payment-api` + `payment-worker` + `payment-reconciler` = one capability, three deployables): the spec lives in the **owner repo** — the service that owns the write path / the data the rules govern. Each other repo's root context file carries three things: this service's role in the capability (2-3 sentences), the canonical pointer to the spec (repo + path + how to fetch it), and where the local contracts are. If "who owns it" is ambiguous, that's the signal for the next step.
3. **Several capabilities crossing repos, or ambiguous ownership**: a **dedicated specs repo**, vendored into each consuming service at a stable path (submodule, subtree, or a sync bot that opens PRs on spec changes). A machine-synced copy with a declared canonical source is not duplication — drift becomes an unmerged sync PR (a visible failing check) instead of a silent divergence. What kills is the *hand-made* copy: it has no drift detector.

**The spec can be remote-with-pointer or vendored; contracts must be local.** The schema a service consumes/produces is what its code compiles against and its contract tests run against — vendored schemas or generated packages from the owner, never "see the other team's repo."

**When one capability spans deployables, its spec gains a responsibility map**: which deployable owns which slice (api receives and validates; worker processes; reconciler verifies), and the contracts *between them*. Same pattern as `pipeline.md`, one level down — `pipeline.md` declares contracts between capabilities; this map declares contracts between one capability's deployables. It is what gives `conformance-review` something to check when a diff in the worker implements behavior the map assigns to the api.

Two things multi-repo gives you for free: `requires_human_approval` on spec changes stops being convention and becomes **mechanical permission** (branch protection + CODEOWNERS on the specs repo or path) — a large feature's new rule lands as PR 1 on the spec, human-gated by the platform, and PRs 2..N implement it, each repo recording which spec version it implements. And for work that crosses services, a **workspace** (the relevant clones side by side, one workspace context file on top) restores the proximity a repo boundary broke.

Be honest about the cost: these mechanisms *manage* multi-repo coordination — they don't eliminate it. Vendoring, sync bots, and version pinning are a tax the modular monolith and the monorepo don't pay; there, the default layout just works. If you're choosing topology now and already know capabilities will span services, a monorepo makes the spec model trivial. Multi-repo is legitimate for other reasons (independent deploys, team ownership) — and its price includes this section.

### Context discipline (what to write, what to leave out)

Two failure modes when a spec or context file gets "too big" — different fixes:

1. **Maintenance size** — the document got too big for a human to keep coherent. → fix with **decomposition by boundary** (split by capability).
2. **Context size** — it doesn't fit the agent's window, or fills it with noise and degrades attention *before* the hard limit. → fix with **scoped loading / retrieval** (nested context files, load only the region in play).

> **Boundary symptom, not tooling.** If editing capability A's spec forces editing capability B's, the problem is **coupling** — the boundary is wrong. No window technique fixes that.

Golden rules for every context file:

- **Document only what the agent can't infer.** Don't describe folder structure — let the code and the layout speak. Stale structural references *actively mislead*; an absent one costs nothing. (Evidence suggests human-written context files help and machine-generated ones hurt — confirm in your own setting, but the direction is clear: write what the code doesn't reveal.)
- **Package by feature, so the structure can speak.** The rule above only works if the folder layout actually reveals the domain — and that requires organizing code **by capability (vertical slice), not by technical layer**: `payments/`, `orders/`, `notifications/` each holding their own logic, not `controllers/`, `services/`, `repositories/` spread across the whole app. This is Robert C. Martin's *Screaming Architecture* — the top-level structure should shout the domain, not the framework. It is the same principle the specs already follow (partition by capability, never by technical layer), applied one level down to the code, and it is the precondition that lets you *not* describe structure: a capability-organized tree is self-evident where a layer-organized one is not. Package-by-feature is also what makes incremental identification converge: a capability-organized layout forces the question "which capability does this belong to?" on every new file, so boundaries sharpen as a side effect of the discipline. **The silent failure mode is package-by-entity disguised as package-by-feature:** folders named after data nouns (`product/`, `customer/`, `invoice/`) look like feature folders but reproduce the anemic slicing Stage 0 warns against. Three tests to tell them apart: the name is a **business verb/outcome, not a data noun** (`payments/` and `onboarding/` are things the product does; `customer/` is a table); the folder is a **vertical slice** (it holds that capability's rules, use cases, and persistence — not one horizontal layer of an entity); and **imports point inward** (if most other folders must reach into this one to complete any flow, it's a shared entity, not a capability). When a new folder fails these tests, rename the boundary around the business outcome — don't just redistribute files.
- **Lean over complete.** "Minimal isn't short," but cut noise. Keep each context file tight — every token is loaded each turn.
- **Binary acceptance.** Replace "typically/expected/better" with imperatives and measurable values. Without an executable test there's no correctness oracle beyond the user.
- **Treat drift as a bug.** Specs and context files drift as code evolves, and there's no automatic staleness detection — version them and review the diffs **like code**. A false spec misleads more than an absent one.
- **Don't overdose.** Half a page for a small change; the full template for a real capability.

> **`AGENTS.md`/`CLAUDE.md` — the operational context file.** Throughout this guideline, "`AGENTS.md`/`CLAUDE.md`" means the operational context file that lives next to the code. The name depends on your tool: **`AGENTS.md`** is the open standard, read by Codex, Cursor, Kiro, OpenCode, Gemini CLI and others; **`CLAUDE.md`** is the name Claude Code uses. Same role, same mechanics — pick the one your tool reads. If you mix tools, keep an `AGENTS.md` and a thin root `CLAUDE.md` that does `@AGENTS.md`. Wherever this document writes one form, the other applies. The mechanics are identical across tools: the file loads by proximity (nearest-wins, lazy — only when the agent touches a file in that folder) and **points to** the capability spec rather than duplicating it. It is not the spec.

### Root AGENTS.md/CLAUDE.md

Target size: ~60 lines. Never exceed 100.

```markdown
# [Project name]

[1-2 sentences describing: what the system does and how it's divided into
high-level pieces. E.g.: "Pipeline in N stages: stage-A → stage-B → stage-C.
Each stage is an independent capability. Stages with internal complexity
can be divided into sub-areas."]

## Commands

- `make build` — build full pipeline
- `make test` — all tests
- `make test-stage STAGE=<name>` — tests for one stage
- `make test-area AREA=<name>` — tests for one sub-area (if applicable)
- `make lint` — static checks

## Structure

- `src/<capability>/` — code per capability; each has its own AGENTS.md/CLAUDE.md
- `specs/<capability>/` — capability spec (source of truth), mirrors src/
- `architecture/pipeline.md` — contracts between capabilities
- `architecture/constitution.md` — non-negotiable principles
- `docs/` — glossary, reference tables, norms/regulations
- `.claude/rules/` — auto-loaded invariant rules

## Non-negotiable principles

Read `@architecture/constitution.md` before architectural decisions.

## Reference documents

- `@architecture/pipeline.md` — Read when: modifying contracts between capabilities
- `@docs/<domain-glossary>.md` — Read when: encountering an unfamiliar domain term
- `@architecture/decisions/` — Read when: making a new architectural decision

## Plan Mode

- Concise plan, sacrifice grammar for brevity
- At the end, list "Unresolved questions" if any
- For rules with a normative source: cite the source before implementing

## Lessons learned

(add here when Claude makes a reproducible mistake and the fix
needs to become permanent — keep it short, with an explicit cap)
```

### AGENTS.md/CLAUDE.md per capability

Each capability (or functional area) has its own, **next to the code** (`src/<capability>/AGENTS.md/CLAUDE.md`), not in `specs/`. It's loaded by proximity when the agent edits a file in that capability. Target size: 20-40 lines.

Function: **pointer + navigation context, not a copy of the spec.** It summarizes the essentials and points to the full spec — it does not embed all the rules (otherwise it duplicates the spec and inflates context on every edit). Template:

```markdown
# <Capability / functional area name>

**Spec (source of truth):** specs/<capability>/<capability>.md
Read the spec before modifying any domain rule in this capability.

## Scope

[2-3 sentences: what this capability does and does NOT do.
E.g.: "Classifies incoming events per [domain] rules,
flags edge cases. Does NOT compute final values — that's
the responsibility of <downstream-capability>."]

## Key rules (summary)

[The 3-5 most important rules, summarized one line each.
Full detail and edge cases are in the spec. Here it's only the essentials
the agent needs to keep in mind on every edit.]

## Where things are

[Navigation within this folder: where what lives. E.g.: "flows in
flows/, shared components in shared/, rules in rules.ts"]

## Contracts

- Input/Output: see specs/<capability>/contracts/

## Lessons learned

(empty — add as mistakes appear)
```

The distinction that matters: **trivial edit** (bugfix, refactor) is resolved with the summary in AGENTS.md/CLAUDE.md — the agent doesn't need the whole spec. **Domain-rule edit** triggers reading the full spec, which the pointer indicates. This way the essentials are always present (cheap) and the full spec is read on demand.

Don't use `@import` to pull the whole spec into AGENTS.md/CLAUDE.md — that loads the spec on every edit, even trivial ones, burning context. A textual pointer + conditional instruction ("read before touching a rule") is more economical.

**Conditional rules — use a real mechanism, not a prompt trick.** `<important if="...">`-style tags circulate in the community, but they are not a loading mechanism: the model may or may not honor the condition, and the wrapped rule still costs context on every session. For a rule that only applies in a specific situation, use the mechanisms that actually gate loading: move it to `.claude/rules/<rule>.md` with `paths:` frontmatter (official — the rule lazy-loads only when Claude touches files matching the glob), or rely on per-context AGENTS.md/CLAUDE.md proximity loading. Keep always-loaded rules to the few that genuinely apply everywhere.

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

### .claude/rules/

Short rules, auto-loaded every session. Each file handles a specific topic. Example (`.claude/rules/decimal-handling.md`):

```markdown
# Decimal handling

ALL high-sensitivity numeric calculations use precise-decimal type
(Python Decimal, Java BigDecimal, equivalent). Never use float.

When converting from external sources:
- Strings from XML/JSON: Decimal(string), never float()
- Database NUMERIC: ORM should return Decimal natively
- JSON: parse string fields, not float fields

Rounding: ROUND_HALF_EVEN unless a normative source specifies otherwise.
Document deviations inline with citation.
```

Keep each file under 30 lines. If it grew, split it.

A second rule worth shipping from day one: `.claude/rules/package-by-feature.md` (included in this system's bundle). It applies the capability-vs-entity tests at file-creation time — the **feedforward** layer of the same control the reviewer criterion covers at review time and the quarterly co-change/dependency check covers for drift. For mechanical enforcement of the checkable part, a PreToolUse hook can block creating `src/<new-folder>/` when no matching `specs/<new-folder>/` exists — enforcing package-by-feature **and** spec-before-code at once; naming quality (business verb vs data noun) can't be checked deterministically and stays with the rule and the reviewer. An example hook ships in the bundle (`.claude/hooks/require-spec-for-new-capability.sh`, opt-in — the settings snippet to wire it is in its header).

**Important:** AGENTS.md/CLAUDE.md and `.claude/rules/` have ~70% adherence by the model. For guarantees that need to be 100% — like "never float on a sensitive value" in a regulated domain — promote to a **hook** (pre-commit, custom linter, AST check). A rule alone doesn't give a guarantee in code where a mistake is costly. Decimal handling is the first candidate in any system dealing with money or critical quantities.

### Skills (`.claude/skills/`)

Skills are folders (not just files) that Claude discovers, reads, and uses on demand. Unlike `.claude/rules/` (loaded every session) and AGENTS.md/CLAUDE.md (loaded by hierarchy), Skills only load when Claude decides to trigger them — based on the SKILL.md `description` field.

**When to create a Skill instead of a rule or doc:**

- It has associated code (scripts, libs, examples) — not just text
- It applies in specific situations, not every session
- It's worth having "memory" (prior execution logs, persistent config)

**Useful categories (from what Anthropic mapped internally):**

- **Library & API Reference:** wrappers for external integrations. API reference + known gotchas + correct-usage examples.
- **Product Verification:** scripts that validate outputs against reference datasets/oracles. Worth spending a week on a well-built one when the domain is regulated or critical.
- **Code Quality & Review:** project-specific checks (does every rule cite its source when required? Correct numeric type? Audit trail present?).
- **Runbooks:** divergence investigation ("output differs from expected → correlate with which rule → identify cause").

**Principles for writing a Skill:**

1. **Description is a trigger, not a summary.** The `description` is what Claude reads to decide "is it worth triggering this skill now?". Write it for the model to decide, not for a human to summarize. "Use when validating computation of X against a reference dataset" — not "Skill for validating X."
2. **The gotchas section is the highest-value content.** List the points where Claude makes mistakes using this skill. It grows over time. More valuable than "how to use" docs.
3. **Don't state the obvious.** Focus on what pulls Claude out of default behavior. If the skill is "how to use external API X," document that the staging environment has a different rate limit, that the certificate expires without warning — not what's in the types.
4. **Don't tie Claude to a step-by-step.** Give it the goal and constraints, not a rigid recipe.
5. **Use the filesystem as progressive disclosure**:

```
.claude/skills/<skill-name>/
├── SKILL.md           ← description + when to trigger + gotchas
├── references/
│   └── <ref-doc>.md
├── scripts/
│   └── validate.py    ← reusable script
└── examples/
    └── <use-case>.md
```

**Start small.** Anthropic's Skills started as a few lines + one gotcha. They grew as mistakes appeared. Don't design the perfect Skill before using it.

---

## Part 3 — Layer 2: Active work

Implementation plan, research notes, decisions for the feature being built. Lives in Claude Code's Tasks system or ad-hoc files — disposable afterward.

### How to create a spec

There is **one spec type — the capability spec, always permanent.** The old "disposable feature spec" is gone: what is disposable is the implementation *plan*, not a spec (see "Large features in an existing capability" below).

**The capability spec (permanent)**

Lives in `specs/<capability>/<sub-area>/<file>.md`. Created once per capability. Updated when architecture or a domain rule changes. **Creation is always human** — a capability spec is the business source of truth, and needs human domain validation. **Spec evolution** can happen during implementation (via the `implement-feature` or `implement-backlog` skills), but any spec update marks the PR as `requires_human_approval` — because a spec change is a business-rule change, and a business rule needs a human eye before merge.

Method: research-driven. The source of truth is external (norms, regulation, existing systems, client documents).

A frontend functional area is just a capability whose inputs/outputs are flows and interaction states instead of data — it uses the **same** template. The interview covers flows, interaction states, and the consumed API contract (referencing the owning backend capability).

How:

1. Create the empty file at the correct path.
2. Start a Claude Code session in Plan Mode.
3. Use the `/shape` slash command or a direct prompt:

```
I'm going to create a spec for [capability]. Use the template in
specs/_template/capability-spec.md.

Research first:
- Read <upstream-context>/AGENTS.md/CLAUDE.md (the input we receive)
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

1. **The work is carried by a larger Phase 2 plan** — the same planning the `implement-feature` skill already produces, just with more depth. The plan is disposable: it is scaffolding for the implementation, discarded when the work is done.
2. **If the feature introduces a new business rule, that rule is merged into the capability spec** — because a rule is a source of truth, and source of truth lives in the permanent spec (with `requires_human_approval`, since it's a business-rule change). If merging it would make the capability spec too big to maintain, that is the signal to split the capability by boundary — the normal decomposition mechanism, not a new spec type.

So the durable record of a large feature lives in three places, each with its role: the **rule** goes into the capability spec, the **plan** is discarded, and the **understanding of what was done and why** goes into the `/explain` walkthrough (`docs/walkthroughs/`). None of these is a "feature spec."

**When does a change get no spec at all?** If you can implement it directly from the existing capability spec — it only combines rules already there and introduces no new source of truth — go straight to implementation with a light plan. The test is not lines of code; it is "does this introduce a rule the capability spec doesn't already cover?"

### Recommended slash commands

Saved in `.claude/commands/`. Versioned in the repo.

**`/plan-from-issue.md`** — generates a phased implementation plan from a GitHub issue (reads the issue, the capability's context file and spec, enters Plan Mode; no implementation). Ships in the bundle.

**`/shape.md`** — the work-shaping interview, one question at a time with a recommended answer every time, the codebase consulted before the human. Creates a capability spec from an idea, a transcript, or existing code; refines an existing spec (grill-back: divergence probe, boundary probe, oracle coverage); or sharpens a task until an agent could implement it without guessing. Ships in the bundle.

**`/spec-to-tickets.md`** — breaks a committed capability spec (or the shaping session that produced it) into tracer-bullet tickets anchored on the spec's numbered criteria, each with blocking edges; quizzes the human on granularity and edges before publishing to a local `tickets.md` or to GitHub Issues, blockers first so edges reference real ids. Wide refactors go expand–contract. Ships in the bundle.

**`/review-spec-drift.md`** — the periodic whole-capability audit: spec ↔ code ↔ contracts divergence, reported as critical / relevant / cosmetic drift. Complements `conformance-review`, which is diff-scoped. Ships in the bundle.

**`/implement.md`** — local entry point: runs the `implement-feature` skill with its human gates; interactive only (supervised `/goal` recommended — recipes below; headless never). Ships in the bundle.

The two entry points, by mode: the **local** mode uses `/implement` above and runs interactively — you confirm each gate. The **autonomous** mode uses Claude Code's **native `/goal` in headless mode** as its engine (see `implement-backlog` below), not a custom command. The line that separates them is not `/goal` itself but **interactive vs headless**: interactively, a gate question pauses the turn, you answer, and the answer enters the transcript — gates and loop coexist (verified in practice); headless, there is no one to answer, so gates are replaced by named-blocker aborts.

### Supervised `/goal` — the recommended local invocation

For any feature with acceptance criteria, wrap the local skill in `/goal`: the human gates stay (questions pause the turn) *and* the worker cannot declare completion — a fresh evaluator re-checks the condition each turn and forces another until it holds. The condition is everything: the evaluator reads only the transcript, so **write it to demand evidence, not claims**. Task-based:

```text
/goal Implement task #<N> with the implement-feature skill.
Done when ALL of the following hold:
- every phase of implement-feature ran, and the Phase 2 plan was
  explicitly approved by the user in this session;
- every acceptance criterion of task #<N> is verified by a passing
  test, with the runner's real output visible in this session — not
  by claim;
- any criterion no executable test can verify is explicitly listed
  as NOT MACHINE-VERIFIED in the final summary;
- the full suite is green; the reviewer reports zero [BLOCKER];
- the work branch is pushed and a PR is open, its description on the
  shared template (Approved plan included);
- hard cap: 30 turns.
```

Spec-based (a new capability — remember: the spec is the source of truth, the run/issue is the execution unit; slice a large capability into issues that *point at* the spec's criteria instead of copying them, and make the first slice the walking skeleton when the capability has contracts with others):

```text
/goal Implement the <capability> capability from
specs/<capability>/<capability>.md using the implement-feature skill.
Done when ALL of the following hold:
- every phase ran, and the Phase 2 plan was explicitly approved by
  the user in this session;
- every criterion in the spec's "Acceptance criteria" section [or
  the slice: items 1-4] is verified by a passing test with the
  runner's real output in this session — not by claim;
- every row of the spec's reference-value table is covered by a test
  asserting input → expected output;
- criteria no executable test can verify are listed as
  NOT MACHINE-VERIFIED in the final summary;
- nothing outside the spec's Non-goals was implemented;
- full suite green; reviewer reports zero [BLOCKER], with
  conformance-review applied (diff vs spec);
- the work branch is pushed and a PR is open, its description on the
  shared template (Approved plan included);
- hard cap: 40 turns.
```

Two operational notes. A "no" at a gate **redirects** the worker; it does not end the run — the condition stays unmet and the evaluator forces another turn; the real stop button is the interrupt, outside the loop's semantics. And plain `/implement` (no `/goal`) remains right for small increments, where the loop's overhead exceeds what it protects.

### Implementation skills

Two skills materialize the implementation workflow as an executable folder in `.claude/skills/`. They're a natural evolution of the slash commands above: instead of generating a plan or comment, they run the Plan → Implement → QA → Close the loop cycle end to end.

**`implement-feature`** — local skill, human-driven.

For interactive use in local Claude Code. Covers three scenarios, all starting from an **existing** spec or backlog item (spec creation/refinement is out of scope):

1. Implementing a new capability — starting from the human-led spec
2. Implementing a large feature in an existing capability — from a larger Phase 2 plan, merging any new rule into the capability spec
3. Increment — starting from an issue or direct prompt

Seven-phase flow, with a human confirmation gate after Phase 1, 1.5, and 2:

- **Phase 1: Understand** — reads the instruction, input (spec/issue), root AGENTS.md/CLAUDE.md → capability AGENTS.md/CLAUDE.md → pointed spec, `.claude/rules/`, `lessons.md`. Maps affected code.
- **Phase 1.5: Resolve ambiguities** — surfaces ambiguities via AskUserQuestion. Does not proceed with unresolved ambiguity.
- **Phase 2: Plan** — ULTRATHINK in plan mode (read-only). Lists files it will edit (committed scope), and separates load-bearing decisions (which determine whether the approach works or which architecture is committed — pinned now) from deferred details (reversible, left to implementation).
- **Phase 3: Implement** — executes the plan on a typed work branch (`feature/`, `fix/`, `refactor/`, `chore/`). Runs lint + typecheck + the touched tests every chunk (not batched at the end), not advancing while red; tests anchor on the spec's acceptance criteria, not on the implementation. Commits during the phase, at a granularity that aids review (the skill's judgment, not 1:1 with plan steps). Editing outside the committed scope requires explicit human approval.
- **Phase 4: Test** — full local suite. Doesn't proceed until green.
- **Phase 5: Code Review** — dispatches the `reviewer` agent (the router, see below) via the Agent tool (renamed from Task; the alias still works) in isolated context; it routes to the applicable review-criteria skills. Sequential with Phase 4 — any fix forces a return to Phase 4.
- **Phase 6: Close the loop** — appends to lessons, possible spec update (with the `requires_human_approval` flag), AGENTS.md/CLAUDE.md proposal (propose-only, doesn't edit directly), backlog status.
- **Phase 7: Open PR & Present Results** — pushes the typed work branch, opens a PR (description on the shared template, Approved plan included), and reports in chat: link, scope, decisions needing attention, human-approval flag.

Structured logging in `.claude/logs/implement-{timestamp}.md` for auditability.

**`implement-backlog`** — autonomous skill, agent-driven.

For end-to-end execution **with no human in the loop**. The persistence engine is Claude Code's native `/goal` command (a session-scoped Stop hook: after each turn a fresh model re-checks a completion condition and forces another turn until it holds). A thin GitHub Action runs `claude -p "/goal <condition>"` in headless mode when an issue gets an `auto-implement` label; the condition names this skill as the workflow and mirrors its completion criteria and aborts. There is no custom orchestrator service — the Action is the trigger, the native `/goal` is the engine, the skill is the workflow, and the `reviewer` carries the criteria. A scheduled Claude Code Routine is the sibling wiring — same engine, same condition shape; its canonical prompt ships in the bundle (`.claude/routines/frontier-worker.md`): scan the frontier, claim one issue, issue the `/goal`.

One property of headless runs governs the whole design: **a question to the user never gates a headless `/goal` run** — there is no one to answer, and the evaluator reads only the transcript, so an interactive gate would be silently overrun rather than block. That is why this skill never asks: every would-be question is a **named-blocker abort** (the only human stop the evaluator can read), and human judgment moves to the ends — the issue's acceptance criteria before the run, the PR review after it.

Scope restricted to increment. Issues describing a new capability or a large feature are routed back to `implement-feature` with a comment and label.

Same phase structure as `implement-feature`, with critical differences:

- No human confirmations between phases. Decisions go to the log and the PR description; human review happens at the PR.
- **Phase 2 (plan review)** — since no human reviews the plan, a `reviewer` subagent does: it applies `plan-review` to judge the approach against failure modes, fit, and pinned load-bearing decisions, iterating until sound before any code. This is the gate that replaces implement-feature's human approval of the plan.
- **Phase 1.5 (ambiguity)** — comments on the issue (numbered list + proposed interpretations), applies a `needs-refinement` label, aborts. Doesn't try to resolve autonomously. Aborting early is cheaper than producing a PR based on a wrong interpretation.
- **Phase 3 (scope expansion)** — comments on the issue, applies a `scope-expansion-needed` label, aborts. Doesn't silently expand.
- **Phase 4/5 (QA)** — cap of 3 iterations on the same failure. On hitting it, comments on the issue (`qa-blocked` or `review-blocked`) and aborts.
- **Phase 6 (spec update)** — if an update is needed, it updates AND marks the PR as `requires_human_approval` (label + field in the description).
- **Phase 7** — opens a PR (not a report), comments on the issue with the link, then monitors the PR until it lands clean: CI to completion (a green check can flip red), late review comments, and merge conflicts (resolving one re-runs the QA gates). Opening the PR is not "done"; merged-clean or a named blocker is.

Prerequisite to turn on in production: the narrow-start conditions of Part 5 — a hard-coded allowlist of trivial increment classes, CI green mandatory before review, and a human approving every PR. **Widening** (more classes, more volume, any step toward auto-merge) additionally requires the regression suite with a track record (`AUTONOMY-PLAYBOOK.md`, `EVALS.md`); widening without it is faith.

**The autonomous trigger, concretely.** The native `/goal` condition is what the Action invokes. It names the skill, mirrors its completion criteria and aborts, and carries a "done with a named blocker" clause so a legitimate abort ends the goal instead of looping:

```text
/goal Implement GitHub issue #<N> by following the implement-backlog skill end to end.
DONE only when all hold and are visible in the conversation: every acceptance criterion verified by a passing test (runner output visible, not claimed); full suite green with tests anchored on the spec's acceptance criteria; lint passes and coverage meets the threshold; the reviewer ran on the final diff with no [BLOCKER] (incl. constitution-compliance and conformance where they apply); a PR is open with CI green to completion.
OR DONE WITH A NAMED BLOCKER when the skill aborts, commented on the issue, and applied the label: out of scope → implement-feature; ambiguity → needs-refinement; scope expansion → scope-expansion-needed; same QA/review failure 3+ times → qa-blocked / review-blocked.
Constraints: stay in the capability; never expand scope silently; if the spec is updated, mark the PR requires_human_approval; never mark done around a red check. Stop at one of the two end states or after 40 turns.
```

A thin GitHub Action invokes it headlessly on the label. The skeleton below is conceptual — confirm the real Claude Code CI setup (install, auth, `gh` permissions, the official Claude Code GitHub Action vs raw `claude -p`) against the headless and GitHub Action docs before relying on it:

```yaml
on:
  issues:
    types: [labeled]
jobs:
  implement:
    if: github.event.label.name == 'auto-implement'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: claude -p "/goal Implement GitHub issue #${{ github.event.issue.number }} ... (full condition above)"
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

**Why two skills, not one with a flag**

Interactive mode and autonomous mode have fundamentally different gates (human confirms vs PR is the gate). Trying a bimodal skill with a flag adds branching that increases bug surface and makes isolated auditing of each mode harder. The content duplication between the two is accepted in exchange for each being auditable in isolation. If real pain appears ("I updated one, forgot the other"), it's worth extracting a common reference document in `.claude/docs/` that both read — don't do it before the pain appears.

### The reviewer agent and review-criteria skills

Code review (Phase 5) and the autonomous plan gate (implement-backlog Phase 2) are not inlined in the implementation skills — they dispatch a separate **`reviewer` agent** that runs in isolated context and did **not** write the work under review. That independence is the point: a fresh context doesn't share the author's blind spots. The reviewer reports findings (`[BLOCKER]`/`[SHOULD]`/`[NIT]`); it never edits.

The reviewer is a **router**: it carries no criteria of its own. The criteria live in modular review-criteria skills, and the reviewer loads the ones that fit what it's handed:

- **`plan-review`** — approach soundness for a plan: traced against failure modes, fit with existing code, capability boundaries respected, load-bearing decisions pinned (the deferred-detail-vs-decision test).
- **`general-code-review`** — the default for any diff: correctness, simplicity/reuse, test quality, type design.
- **`constitution-compliance-review`** — added when the diff touches a domain rule, a calculation, a sensitive numeric value, the audit trail, source attribution, stage boundaries, or past-period rules. Checks against `architecture/constitution.md` (precise numeric type, audit trail, normative-source citation, responsibility separation, immutability of past rules).
- **`conformance-review`** — added when the diff implements a spec or an approved plan: does the code do what the spec requires (value by value) and what the plan committed to (intent vs implementation)?

The implementation skills only say "dispatch the `reviewer` with this plan/diff" — the reviewer decides which criteria apply from what the diff touches. On large diffs (roughly >400 changed lines or >10 files) the caller instead dispatches three parallel single-lens reviewers — the reviewer supports a pinned single-lens mode — and merges the reports; the plan gate is never parallelized. Review can also be invoked on demand via `/review`. Adding a dimension later (e.g. a security review) is one new SKILL.md plus one routing line in the reviewer; the implementation skills don't change. The reviewer agent lives in `.claude/agents/`, the criteria skills in `.claude/skills/`.

**Generic vs contextual criteria — and external reviewers.** The criteria split in two. `general-code-review` is *generic*: correctness, simplicity, types, test quality — verifiable without knowing this project. `constitution-compliance-review` and `conformance-review` are *contextual*: checkable only by an agent that reads this project's constitution and specs, which no off-the-shelf tool has. This split is where an **external code reviewer** fits — a SaaS LLM review tool running on the PR can complement the *generic* layer with a reviewer of different architecture than Claude, which catches a largely disjoint set of bugs (the heterogeneity that parallel-reviewer studies show matters). It does **not** replace the contextual reviewer, and it is **advisory, not a gate**: in autonomous mode it stays out of the `/goal` completion condition, because a generic reviewer's middling precision would abort the loop on false positives. What blocks stays deterministic (tests, lint, types) plus the contextual reviewer; the external reviewer comments for the human who owns the merge. Security likewise stays a deterministic gate (SAST/SCA/secret scanning) — an external reviewer informs, it does not certify. Before trusting any external reviewer, run it advisory on this codebase and measure its real false-positive rate in the domain, since benchmark numbers are mode- and dataset-specific and rarely match your code.

### Control classification: feedforward/feedback × computational/inferential

A lens (from ThoughtWorks) for auditing the controls above: every control is either **feedforward** (a guide applied *before* the agent acts) or **feedback** (a sensor applied *after*), and either **computational** (deterministic, runs in milliseconds) or **inferential** (an LLM, runs in seconds, catches what code analysis can't). The four quadrants, with this system's controls in each:

- **Feedforward · computational** (deterministic guides): the type system (Decimal not float), ADRs, `.claude/rules/` with `paths:`.
- **Feedforward · inferential** (LLM/prose guides): the specs, the constitution, the AGENTS.md/CLAUDE.md files, the approved Phase 2 plan.
- **Feedback · computational** (deterministic sensors): tests, lint, coverage, mutation testing, golden datasets, contract tests, CI.
- **Feedback · inferential** (LLM sensors): the reviewer (general + constitution-compliance + conformance) and any external advisory reviewer.

Two things this lens makes visible. First, all four quadrants are filled — most teams have strong feedback and weak feedforward (more sensors than guides), and the spec-anchored approach is what loads the feedforward side here. Second, the two axes aren't interchangeable: feedback-only means repeated mistakes (no guide stops them up front), feedforward-only means you never confirm the guides worked (no sensor checks the result). The layering follows the cost gradient — computational before inferential (fast/cheap/deterministic first, slow/expensive/semantic second), the same gradient the Phase 3→4→5 sequence already encodes.

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
[lessons update the corresponding AGENTS.md/CLAUDE.md, if any]
```

### Killed issues

When closing a `someday` issue by conscious decision: comment with the reason, close as "not planned" (not "completed"). It's the memory of "already considered and discarded," versioned and searchable.

### The three rituals

**Daily (5 min, morning before coding):** look at the 3 `priority:now` issues; if one got abstract, open Plan Mode before touching it; if it already has a PR, continue.

**Weekly triage (30 min, fixed day/time):** filter issues without priority created during the week; each becomes `now`, `next`, `someday`, or `closed: not planned`. 2-3 minutes per issue. For the issue those 2-3 minutes can't decide — ambiguous scope, unclear size — run `/plan-from-issue`: the phased plan and its open questions inform the call, and are the cheap `needs-refinement` check before labeling an issue for the autonomous route.

**Monthly review (45 min):** go through `someday`; kill what no longer makes sense; promote what became obvious; reorganize labels that became a mess.

### Concrete daily workflow

Starting a feature:

1. Open the repository, look at `priority:now` issues.
2. Pick one. Read comments. Check whether it got abstract.
3. Open Claude Code in the affected capability's directory.
4. Decide: simple change, large feature, or new capability?
   - **Simple:** straight to Plan Mode with the issue as context.
   - **Large feature in an existing capability:** a larger Phase 2 plan carries it; if it introduces a new business rule, merge the rule into the capability spec first (human approval).
   - **New capability:** run `/shape` to create its spec, `/spec-to-tickets` to break it into issues, then implement from the frontier.

   For the last two cases — anything with acceptance criteria — the recommended invocation is the **supervised `/goal`** from Part 3: the evaluator holds the run to evidence while your gates still fire. Plain Plan Mode / `/implement` remains right for the simple case.
5. Named branch: `<stage>/<sub-area>/<issue-number>-<short-slug>`. E.g.: `<stage>/<sub-area>/142-<short-description>`.

Plan Mode → Execution:

1. Plan Mode (Shift+Tab twice).
2. Claude reads the capability's AGENTS.md/CLAUDE.md (auto), the root one (auto), the `.claude/rules/` (auto), and docs referenced via `@`.
3. You iterate on the plan until it's good (1-6 times, usually).
4. Check "Unresolved questions" — answer them before proceeding.
5. Accept the plan, exit Plan Mode.
6. Auto-accept edits for implementation if confidence is high. Manual when there's risk.

Closing a feature:

1. Tests passing locally. Lint passing.
2. Open a PR referencing the issue (`Fixes #142`).
3. Before merging, a mental checklist:
   - Did this feature teach something that deserves to be in some capability's AGENTS.md/CLAUDE.md?
   - Did a violated principle deserve to become a rule in `.claude/rules/`?
   - Does some architectural decision deserve an ADR in `architecture/decisions/`?
4. If so, the updates go **in the same PR**. Don't leave it for later.
5. Merge. The issue closes automatically.

### Nightly routine (conservative version)

Runs on Anthropic's cloud infra. Pro plan: 5 runs/day.

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

**Architecture work.** Creating a new capability, a new sub-area, a large feature that reorganizes the pipeline. Always human-led: you plan how the system should be (create the spec), execute via `implement-feature` (local skill, with human gates at each phase), open a PR. The spec is the business source of truth — creation is always human because it's a domain decision that needs validation from whoever understands the rule. **It doesn't go through the backlog. It doesn't enter the autonomy trajectory.** Spec evolution during execution can happen via the skill itself, but it triggers a human approval flag on the PR.

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

AGENTS.md/CLAUDE.md:

- ❌ Auto-generate with `/init` and leave it as-is. It's too high a leverage point.
- ❌ Put detailed code-style rules. Use a linter/formatter.
- ❌ Root AGENTS.md/CLAUDE.md over 100 lines.
- ❌ Repeat information between the root AGENTS.md/CLAUDE.md and the capability ones. Use references.
- ❌ Use it for security- or correctness-critical things. AGENTS.md/CLAUDE.md has ~70% adherence; hooks have 100%.

Specs:

- ❌ Write a spec for a 30-minute task.
- ❌ A top-down 200-line PRD before any feature.
- ❌ A spec that duplicates what's already in the capability's AGENTS.md/CLAUDE.md.
- ❌ Skip AskUserQuestion because "I already know the answer."

Backlog:

- ❌ More than 3 `priority:now` issues at once.
- ❌ Add epics, milestones, sub-tasks, custom statuses in the first 2 months.
- ❌ Keep vague issues in the backlog. Weekly triage kills or refines.
- ❌ Close someday issues as "completed" when you just gave up. Use "not planned" with a reason.

Workflow and autonomy:

- ❌ Exit Plan Mode before reviewing "Unresolved questions."
- ❌ Update AGENTS.md/CLAUDE.md "later." Do it in the same PR or don't do it.
- ❌ Run 5 parallel Claude Code sessions without solid practice in 1-2.
- ❌ Adopt a framework (Spec Kit, BMAD, Taskmaster) because you feel a lack of "structure." Structure without a concrete problem becomes an abandoned system.
- ❌ Wait for a "complete" eval suite before starting. 20 tasks are worth more than 0 (see `EVALS.md`).
- ❌ Trust pass@1 for an agent that opens a PR on its own. You need pass^k.
- ❌ Auto-merge based only on tests passing before a class qualifies (`AUTONOMY-PLAYBOOK.md`, Milestone 4). Coverage is rarely proof of correctness.

### Warning signs

- **Root AGENTS.md/CLAUDE.md passed 80 lines:** it's accumulating junk. Review it.
- **`priority:now` is always at 3+ issues:** you're not closing, you're stacking.
- **Same fix applied to Claude 3x:** make it a rule in `.claude/rules/` or a hook.
- **Specs go stale after features:** you're skipping the PR checklist.
- **You opened spec-kit, BMAD, or similar in your bookmarks:** ask what concrete problem. If there's none, ignore it.
- **You haven't updated this document in 3+ months:** either it's perfect (unlikely) or it's obsolete (likely).
- **Dex's heuristic:** open Claude Code in a fresh clone of the repo and say "run the tests." If it doesn't work first try, the AGENTS.md/CLAUDE.md is incomplete — it's missing an essential setup, build, or test command.
- **You're building an elaborate workflow for a simple task:** vanilla Claude Code is usually better than a custom workflow for small tasks.
- **The regression suite's pass^3 dropped:** something broke. Stop changes, investigate (see `EVALS.md`).
- **Average cost per issue rising without a pass^k gain:** silent regression. Investigate.
- **You created a capability the business doesn't recognize:** speculative structure rots. A capability is justified either by the business (payments exists because you charge people — a known business capability is already justified, see Stage 0) or by divergent rules ("this part needs different rules from the rest") — never by "I thought it'd organize better." An invented one waits in the backlog until evidence shows up.
- **You're letting the model decide what comes next on the roadmap:** evolution is a human decision based on real pain, not a model suggestion. The model executes what you prioritize; prioritization is yours.

### Honest checks (re-read quarterly)

1. **Am I following the weekly triage?** If not, the whole system collapses. Focus on only that until you're back in rhythm.
2. **Are the AGENTS.md/CLAUDE.md files still small and current?** If they grew, it's accumulating. If they went stale, you're not closing the loop at the PR.
3. **Do the specs reflect the code?** If not, either abandon the specs or resume the discipline. Both paths are honest. The bad one is keeping a lying spec.
4. **If autonomy widened beyond the narrow start: is the regression suite running, green, and consulted?** Widening without it is faith; a suite nobody runs is turning into a museum (`AUTONOMY-PLAYBOOK.md`). Running it is part of the work, not a bonus.
5. **Is the layout still package-by-feature — or drifting toward package-by-entity?** Run the deterministic pass: co-change analysis on git history plus a dependency-graph check (`dependency-cruiser`, ArchUnit). Edits that consistently cross capability folders, or one folder most of the codebase imports from, mean a leaked boundary or a disguised entity — redraw the boundary (Stage 0 signals) instead of adding rules.
6. **Are the specs still telling the truth about the code?** Run `/review-spec-drift` on the capabilities touched most this quarter. Critical drift is a bug to fix now; cosmetic drift is a spec update to make now — a spec that lies is worse than no spec.

If all are "yes," the system is working. If any is "no," treat it as a bug — not as inevitable.

---

## Part 7 — Implementation roadmap

An order that makes sense. You don't need to do everything at once.

### Stage 0 — Identifying capabilities

Before any production code. There's no mechanical checklist — it's a discussion with Claude until consensus:

- [ ] Dedicated session (Plan Mode) for identifying capabilities
- [ ] Note which capabilities are central vs supporting (helps prioritize what to specify first)
- [ ] Define capabilities and their boundaries
- [ ] Define how the capabilities relate (upstream/downstream, contracts between them)
- [ ] Document the initial architecture in `architecture/`
- [ ] (Brownfield) map the existing system and propose reorganization toward these capabilities

Done when you can explain to another person what each capability does and doesn't do.

### Stage 1 — Specification — Week 1

- [ ] Create `specs/_template/capability-spec.md`
- [ ] Write a capability spec for the first capabilities to implement
- [ ] Cite the normative source in each rule that derives from an external source

### Entering development + operational base — Week 1-2

- [ ] Set up the folder structure (Part 2) according to the capability map
- [ ] Write the root `AGENTS.md/CLAUDE.md` following the template
- [ ] Write `architecture/constitution.md`
- [ ] Write `architecture/pipeline.md` or equivalent (contracts between capabilities)
- [ ] Configure labels in GitHub Issues per the schema
- [ ] Confirm minimum CI running: unit tests + coverage per capability + lint + build. Without this, the base isn't operational yet.

### Solid operational base — Week 2-4

- [ ] Create a `AGENTS.md/CLAUDE.md` per capability (start with the highest-dependency ones)
- [ ] Create `.claude/rules/` with 3-5 invariant rules
- [ ] Migrate existing specs to the template format
- [ ] Add `contracts/` in at least one capability (suggestion: parsers, which affects the others)
- [ ] Customize the shipped slash commands to your project (label schema in `/plan-from-issue`; paths, if your layout differs)
- [ ] Identify 10-15 representative closed issues that will seed the future regression suite (see `EVALS.md`)

### Initial automation + narrow-start autonomy — Month 2

- [ ] Configure the Claude Code GitHub Action (`@claude` on issues)
- [ ] Create the nightly grooming routine (conservative version)
- [ ] Establish rituals (daily, weekly triage, monthly review) with a fixed time
- [ ] Practice the Plan Mode → execution flow for 4 complete features before changing the process
- [ ] Consider turning on **narrow-start autonomy** (hard-coded allowlist + CI green mandatory + human approving every PR — Part 5)
- [ ] **Start the eval suite:** a minimal manual regression suite with 10-15 tasks (this becomes your `EVALS.md`) — required to *widen* later
- [ ] **Promote `decimal-handling` (or your domain's equivalent critical rule) from a rule to a hook** (a rule has ~70% adherence; a hook has 100%, and in code where a mistake is costly that matters)

### Refinement + widening — Month 3+

- [ ] Add `contracts/` to the remaining capabilities
- [ ] Run `/review-spec-drift` on the capabilities implemented so far — treat critical drift as a bug
- [ ] Evaluate whether Background mode is worth it for long refactors
- [ ] Evaluate whether Task Budgets make sense for large features
- [ ] Consider the first Skill — probably a validator of your domain against a reference dataset
- [ ] **Complete the regression suite** (30+ tasks, pass^3 baseline, production metrics tracked for 30+ days) — the widening prerequisite (`AUTONOMY-PLAYBOOK.md`, Milestone 1)
- [ ] Consider **widening** (more classes, Tier 1 in CI — `AUTONOMY-PLAYBOOK.md`, Milestone 2) when the suite is stable

### Further widening — When applicable

Milestone 3 depends on having a deployment pipeline to an integration environment — outside this guideline, it's infrastructure work. Milestone 4 depends on a consistent track record in Milestone 3 per increment class. See `AUTONOMY-PLAYBOOK.md` for criteria.

---

## Final principle

This document exists to serve you, not to govern you. When a rule here causes more friction than value, change the rule. But change it **consciously** — edit this file, commit with a reason. Silent erosion of discipline is what kills systems like this.

If in 6 months you're productive, with PRs shipping, clean code, and this has become a living reference — it worked. If it became a museum of good intentions, burn it and restart with 1/3 of the content.
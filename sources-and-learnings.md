# Sources & Learnings

> Companion to `GUIDELINE.md`. Every external source mined while designing this
> methodology, what each one contributed, what we rejected and why, and the
> meta-lessons about consuming this kind of content. Useful as onboarding
> material and as the audit trail of *why the system is the way it is* — this
> document is itself intent-debt paydown.
>
> Last updated: 2026-07-03.

---

## How to read this

Part 1 catalogs each source. Part 2 maps the adopted ideas to the artifacts
where they now live. Part 3 lists the named concepts that became design rules.
Part 4 is the backlog of extracted-but-not-yet-applied items. Part 5 is the
meta-lessons. The appendix records what failed fact-checking — kept on purpose,
because the failures teach as much as the finds.

---

## Part 1 — Source catalog

### 1. Mark Erikson — "My personal AI development setup" (blog, 2026-05-07)

Redux maintainer describing his agentic workflow after months of iteration.
Repos: `github.com/markerikson/opencode-config-example`,
`github.com/markerikson/diffloupe`.

- **Took:** the codebase-exploration discipline (structural queries via
  grepika/tilth/cachebro before reading whole files; native-Read edit
  precondition) → the Codebase-exploration section of the root
  context-file template (GUIDELINE Part 2). The
  *diffloupe* idea — reviewing intent vs implementation — → Dimension 2 of
  `conformance-review`.
- **Rejected:** adopting his exact toolchain wholesale; we kept the principle
  (minimize context, structure before content) and the three tools.

### 2. Arcplane — "Coding is solved? Software is not." (Gao, 2026-05-19)

`arcplane.ai/journal/software-is-not-solved`. Essay on why software still
feels hard when implementation is abundant.

- **Took:** the framing — software development is *entropy reduction* (turning
  ambiguous intent into a verified change), and coding is only one step of it;
  the definition of **AI slop** as "output that looks complete but does not
  reduce the mess"; "clean code cannot rescue a bad spec" — an early argument
  for spec-first.
- **Rejected:** nothing concrete to adopt; it is a diagnosis piece (and
  product marketing). Its value was vocabulary and motivation.

### 3. Antfly — "Cheap code means formal verification is reasonable now" (Rowan Copley, 2026-05-06)

`antfly.io/blog/agent-formal-verification`. TLA+ + coding agents to find race
conditions in a distributed DB.

- **Took:** **"hill climbing on verifiable problems"** as the lens for
  designing any skill or gate ("what is the verifiable landscape the agent
  will climb?"); `assumptions.md`/`boundaries.md` as explicit plan artifacts
  (backlogged as a Phase 2 evolution); **workflow validation against known
  historical bugs** (he validated his pipeline by re-finding a fixed Pebble
  race condition) → noted for `EVALS.md` Milestone 1; the observation that in
  a normative domain, formal modeling can check *rule completeness* ("is there
  an input where no rule applies? where two rules conflict?") — more useful
  than race conditions for us.
- **Rejected (deferred):** adopting TLA+ itself before a concrete bug class
  justifies it; the four-persona brief (overkill — kept only the essence in
  the PR description).
- **References worth keeping:** Martin Kleppmann on AI + formal verification;
  Simon Willison on porting justhtml via conformance suites.

### 4. Cameron R. Wolfe (Substack) + Anthropic Engineering — agent evals

`cameronrwolfe.substack.com` piece on evaluating agents, building on
Anthropic's "Demystifying evals for AI agents" (Engineering Blog, Jan 2026) —
the stated base of our `EVALS.md`.

- **Took:** **pass^k vs pass@k** (consistency, not just capability — pass^k is
  the metric for anything that opens PRs alone); the **grader taxonomy**
  (cheapest-that-works ordering: test execution → static analysis → state
  check → tool-call verification → LLM-as-judge → transcript metrics);
  regression vs capability suite split; the eval pitfalls list (test leakage,
  grader cheating, state contamination, one-sided suites); the τ-bench mapping
  to our domain (policy = spec, APIs = bounded contexts, user simulator =
  issues) as a reference design for Milestone 1.
- **Rejected:** building the suite before Milestone 1 work starts; the rule is
  "20 tasks from closed issues beat 0 tasks waiting for a complete suite".

### 5. AWS — "AI-DLC for financial services" (Industries blog, May 2026)

`aws.amazon.com/blogs/industries/ai-driven-development-lifecycle-for-financial-services/`.
The domain-specific derivative of AI-DLC; the strongest *domain* validation we
found (human-in-the-loop, traceability, DevSecOps as prerequisite).

- **Took (backlogged, optional):** **risk-based change categorization** (maps
  to Milestone 4 auto-merge by class); operational KPIs (MTTR, failed-deploy
  rate, events-by-severity) for `EVALS.md`; an explicit
  requirement-traceability graph for audit.
- **Rejected:** Kiro/Amazon Q tooling (marketing); ceremony-heavy process.

### 6. Lucas F. Costa — "Backpressure is all you need" (2026-05-23) + `backpressured` repo

`lucasfcosta.com/blog/backpressure-is-all-you-need`,
`github.com/lucasfcosta/backpressured` (MIT). The single most influential
source.

- **Took:** **backpressure** ("machines that say no before a human does") →
  Fundamental Principle #5; the maxim *"any system that relies on a human to
  catch the machine's mistakes will be limited by the human, not the
  machine"*; the **router + modular criteria** reviewer architecture → our
  `reviewer` agent + criteria skills; **load-bearing vs deferred decisions**
  (the plan-review decisive test) → Phase 2 of both skills; **checks every
  chunk, not batched**; **tests anchored on acceptance criteria, not the
  implementation**; **Common Rationalizations / Red Flags tables** as the
  anti-slop pattern in every skill; **PR monitoring until landed** → Phase 7.
- **Took (by negative example):** his own lament — "a skill can be ignored or
  bypassed" — taught us to use the **native `/goal` (Stop hook, enforced)** as
  the autonomous engine instead of packaging the loop in a skill
  (instruction). We deliberately did *not* copy the packaged form.
- **Rejected:** installing the package; `type-design-review` as a standalone
  skill (folded into `general-code-review`, replaced by our two domain skills:
  `constitution-compliance-review`, `conformance-review` — which his generic
  set lacks); manual cURL/browser gates (front-end specific; our equivalent is
  synthetic-data runs at Milestone 3).

### 7–8. Claude Code official docs — `/goal` and hooks

`code.claude.com/docs/en/goal`, `code.claude.com/docs/en/hooks`. Read after
the user corrected the assistant's confusion between Lucas's skill and the
native command.

- **Took:** `/goal` is a session-scoped **Stop hook**: after each turn a fresh
  small model re-checks the completion condition and forces another turn —
  backpressure at the turn level, with an external evaluator deciding "done".
  → the persistence engine of `implement-backlog`. The hooks doc settled the
  gate question: `AskUserQuestion`/`ExitPlanMode` end the turn (the mechanism
  of our human gates), `/goal` removes per-turn prompts and would override
  them; in headless `-p` those tools block (a PreToolUse `defer` exists for
  external orchestration). → **`/goal` fits autonomous mode only; local mode
  keeps gates and uses `/implement`.** Conditions must be observable in the
  transcript; include a turn bound; aborts must be a legitimate end state
  ("done with a named blocker").

### 9. @shannholmberg — "agent looping" (X/Twitter thread + diagram)

Single-agent loop vs fleet loop; **open vs closed looping**.

- **Took:** open/closed as *phases*, not project choices — open belongs to
  Stage 0 (human-led domain exploration); closed is everything else. "Loose
  standard = a fast slop machine." The cost line decides which loop you can
  run.
- **Rejected:** the LLM fleet-master (orchestrator → specialists → subagents)
  for implementation. Our orchestrator is deterministic infrastructure
  (GitHub issues/labels/Actions/CI) + the human at load-bearing decisions;
  the doc-verified reason is in source #11. Synthesis kept: **throughput is
  bounded by verification capacity, not generation.**

### 10. Medium "12 Patterns" article + `shanraisshan/claude-code-best-practice` repo

The article embellished; the repo (a curated aggregator linking primary
sources) checked out. Verified claim-by-claim — see Appendix.

- **Took (verified real):** tools allowlist on agents = physical enforcement
  (reviewer should be read-only by config, not instruction); `paths:`
  frontmatter on `.claude/rules/` for lazy-loading by glob; `context: fork`
  on skills; `/sandbox`; worktrees incl. `claude -w`; scheduled tasks;
  CLAUDE.md sizing (≤200 official; ~60 community optimum — already our
  target); Thariq's **Gotchas principle** ("the highest-signal content in any
  skill is the failures actually encountered") — validates our Red Flags +
  `lessons.md`, with one refinement backlogged: periodically promote recurring
  lessons into the matching skill's Red Flags. Thariq's `/freeze` (on-demand
  hook blocking edits outside a directory) validates our planned scope-
  enforcement hook — someone already built the pattern.
- **Rejected:** `<important if=...>` (a community prompt trick presented as
  syntax; our CLAUDE.md-by-context + `paths:` achieve it with a real loading
  mechanism); `/btw` and `--bare` (not found anywhere — likely invented).

### 11. Claude Code official docs — agent teams, worktrees, scheduled tasks

`code.claude.com/docs/en/agent-teams`, `/worktrees`, `/scheduled-tasks`.

- **Took:** Anthropic itself confirms our orchestration thesis — teams are
  weakest for "sequential tasks, same-file edits, work with many
  dependencies"; start with research/review, not parallel implementation.
  Worktrees (`claude -w`, `isolation: "worktree"`, base = clean origin/HEAD,
  PR worktrees via `--worktree "#N"`) make the **deterministic fleet by
  bounded context** nearly free. `loop.md` + `/loop` = a native PR babysitter
  for the local mode (the autonomous mode already has `/goal` monitoring).
  Routines (cloud) are a candidate for the nightly routine. Teammates honor a
  subagent definition's tools allowlist (confirms the reviewer enforcement
  idea). TeammateIdle/TaskCompleted exit-2 hooks = native team-level
  backpressure. Teams' plan-approval flow = our plan-review gate, native.
- **Caution:** agent teams are experimental (flag-gated, known limitations) —
  nothing on the critical path. Worktrees with `-p` don't auto-clean.

### 12. Dynamic Workflows — claude.com blog (2026-05-28, now GA) + `code.claude.com/docs/en/workflows` (+ a secondary deep-dive article)

Verified against the official blog and doc; the secondary article was largely
accurate with exaggerations (see Appendix).

- **Took:** the **"who holds the plan"** question as the orchestration
  decision rule; workflows = the plan moved from the context window into a
  deterministic, auditable, saveable script (Principle #4 applied to
  orchestration itself — LLM as orchestration *compiler*, not runtime
  orchestrator); **adversarial verification** (proposer/refuter) as distilled
  backpressure — stealable without workflows for critical findings; the Bun
  port (750k lines, 99.8% of suite, 11 days) as proof that **scale tools
  amplify exactly what the verification harness permits** — the test suite
  *was* the executable spec. Sanctioned future uses (post-Milestone 1):
  codebase-wide audits (`spec-drift-audit`, `constitution-audit`), brownfield
  → DDD migration, multi-angle planning for Stage 0.
- **Rejected:** workflows for increments (bounded, known shape → `/goal` +
  skill, per the doc's own guidance) and for `implement-feature` (no mid-run
  user input; gates live inside our flow). 0.2% failure on 750k lines ≈ 1,500
  wrong lines — acceptable for a runtime preview, not for normative
  calculations.

### 13. Addy Osmani — "The Intent Debt" (2026-06-05)

`addyosmani.com/blog/intent-debt/`, building on Storey's Triple Debt Model.

- **Took:** **intent debt** as the name of the problem Layers 1–2 solve;
  the economics — un-externalized intent is now paid *every session,
  multiplied by every agent* (low intent debt is a prerequisite of scale, not
  hygiene); the `/init` test (if the agent could regenerate the artifact from
  the code, it pays no intent debt); the sharpest defense of our test rule
  ("the tests only encoded the previous behavior, never the intent"); the
  confirmation that intent must be captured at the moment and altitude it is
  born — which is why the system has **five** intent carriers (spec,
  constitution, ADRs, the Phase 2 plan rationale, lessons.md), not one.
- **Pushed back on:** his optimism about cognitive-debt recovery (an agent
  explains *what*, not *why*; recovery depends on intent debt being low); and
  "agents can't pay it down" understates the agent's role as *scribe* of
  intent (our Phase 6) — the human originates, the agent records cheaply.
- **Our edge he doesn't cover:** in a normative domain much of the intent is
  external and citable (norm X, version Y) — capture is an auditable
  obligation, not just discipline. And a written *why* needs enforcement to
  stay true (conformance-review, drift checks, Phase 6) — stale intent is
  worse than absent intent.

### 14. AWS — "AI-Driven Development Life Cycle" (DevOps blog, 2025-07-31)

`aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/`. The parent
methodology of #5.

- **Took:** external validation of the mental model — *plan → clarify → human
  validates → implement* is exactly Phases 1 → 1.5 → 2 → 3, arrived at
  independently by someone who ran programs with 100+ enterprise customers;
  persistent context stored as artifacts in the repo (same conclusion as #13).
- **Rejected:** the delivery — **ceremony without mechanism**. Every "no" in
  AI-DLC is a human (a whole team, in a synchronous mob): the
  human-as-slow-backpressure anti-pattern institutionalized. No hooks, no
  machine gates, no anchored tests. We keep the skeleton and add the teeth.
  Velocity-first ordering is inverted for a regulated domain.

### 15. "Harness Engineering" (Medium) → Anthropic Engineering — "Harness design for long-running application development" (Prithvi Rajasekaran, Labs, 2026-03-24)

A secondary Medium piece whose verification surfaced the primary source:
`anthropic.com/engineering/harness-design-long-running-apps`. The official
article is the better reference on every point.

- **Took (official article):** "harness" as first-party vocabulary — the
  system we built *is* harness engineering. **Planner / Generator /
  Evaluator** as Anthropic's own three-agent architecture (maps to Phase 2 +
  plan-review / Phase 3 / reviewer + `/goal` evaluator). **Sprint contracts**
  — generator and evaluator negotiate what "done" means before code is
  written — are our plan-review gate, officially validated. The
  **self-evaluation bias** stated first-party ("agents confidently praise
  their own mediocre work"; "tuning a standalone evaluator to be skeptical is
  far more tractable than making a generator critical of its own work"; "out
  of the box, Claude is a poor QA agent" — several tuning rounds needed),
  which both justifies the reviewer's independence and confirms our honest
  ranking of it as the weakest gate. The planner kept deliberately high-level
  so spec errors don't cascade — the same rationale as our
  anti-over-specification template guidance. Evaluator exercising the live
  app via Playwright (validates Milestone 3 and the frontend-area
  Verification approach). First **real cost data**: solo $9/20 min vs full
  harness $200/6 h; v2 ≈ $124/4 h — verification harnesses cost ~15-20x solo
  and pay only when the task exceeds what the model does reliably alone. And
  the headline lesson: **harness lifecycle** (see Part 3).
- **Took (Medium piece):** pedagogy only — "Agent = Model + Harness", the
  three stages (prompt → context → harness), the junior-employee analogy.
  Good presentation material; cite the primary source instead.
- **Rejected:** the Medium piece's harness-maximalism ("the model shouldn't
  decide what order to do things in") — we harness outcomes and constraints
  (enforcement), not every footstep (the *how* stays instruction); its
  invented terminology and unverifiable numbers (see Appendix).

### 16. "Harness Engineering: What Every AI Engineer Needs to Know in 2026" (Yanli Liu, GoPubby, 2026-04-17) — `ai.gopubby.com/harness-engineering-what-every-ai-engineer-needs-to-know-in-2026-0ab649e5686a`

A secondary synthesis of the three-camp harness landscape (OpenAI environment-first / Anthropic multi-agent / ThoughtWorks taxonomy). Its core — harness decay, build-to-delete, re-audit per model, Planner/Generator/Evaluator, sprint contracts, the $9/$200/$124 cost A/B — we already hold from source #15 (the Anthropic primary). What it adds:

- **The ThoughtWorks 2×2 (Böckeler) — now in the GUIDELINE, Part 3.** Every control is feedforward (a guide before the agent acts) or feedback (a sensor after), and computational (deterministic, ms) or inferential (LLM, seconds). The lens audits our controls: all four quadrants are filled, and the spec-anchored approach is what loads the feedforward side most teams lack. Complements the feedback-loop map.
- **Harnessability.** Strongly-typed languages, clear module boundaries, well-structured frameworks make agent work inherently more reliable — the *agentic* justification for our DDD + bounded contexts + Decimal-typed + contracts, not just domain engineering.
- **Harness templates.** Standardized bundles of guides+sensors per topology (one for CRUD, reused). Extends our spec templates to the *control set* per context type → the **validation-profile-per-context** idea for the pending `testing-strategy.md` (a normative-calculation context demands golden + property + constitution-compliance; a UI context demands E2E + mirror-conformance).
- **Regulated-industry framing (validation + vocabulary).** Treat the harness as the control framework auditors will ask about; append-only event log = audit trail; structured task templates = compliance docs. Validates our whole posture — constitution = control framework, structured logs = audit trail, normative-source specs = compliance docs.
- **Rejected / cautioned.** The "three camps" narrative is good didactics but a simplification (our system already blends all three). The new secondary numbers (Opus 4.7 CursorBench 58→70, LangChain 52.8→66.5, Vercel −80% tools, Manus 5× refactors) are unverified — no traceable sources for most. The core was validated against the primary (#15); these illustrate a trend the primary already confirms, but aren't cited as fact.

### 17. "Loop Engineering: Stop Asking Me What It Is" (HuaShu / 花叔, Orange Books, 2026-06) — popular-synthesis e-book

A secondary synthesis of loop engineering (Addy Osmani's term), stacking Osmani + Steinberger + Cherny + Rajasekaran. Most of it — the five moves, six parts, generator/evaluator, memory-on-disk, worktrees — we already hold (from the Elvis/DAIR thread and our own `/goal` verification). What it adds:

- **The Stripe/Minions case — the one actionable piece.** Stripe ships 1,300 PRs/week, none hand-written, and the reliability is NOT the model: before the LLM wakes, a *deterministic orchestrator assembles the context first* (scans links, pulls Jira, finds docs, Sourcegraph+MCP to locate code). Anything deterministic logic can solve never reaches the probabilistic model; the LLM only writes code with the materials already on the table. "Where you draw that line decides whether the loop is reliable." Six-layer architecture, deterministic gates and LLM steps interlocked, gates hard-coded so the agent can't skip them (linter before commit). → **For us:** the determinism/probabilism line is sharper in a normative domain — *which normative source applies*, *which contract*, *which spec/constitution slice* are rules, not judgments. Inject them deterministically before the LLM instead of letting it search (and cite the wrong norm / assume the wrong contract — the exact class `conformance` exists to catch). This is the mechanism behind the contracts-before-fan-out conclusion: the validated contract, injected deterministically, is what makes a sub-agent *receive* the boundary instead of inventing it. Stripe is the at-scale proof.
- **The four-layer stack (prompt → context → harness → loop) — useful vocabulary.** Names *where* a control lives (complements our 2×2, which names *what kind* it is). Clarifies a real distinction: `implement-feature` is **harness** (arms one run, then stops), not **loop** (the `/goal` motor that re-runs itself). The loop's stop-and-go is *enforcement* (a fresh evaluator forces turns via Stop hook); a skill's internal feedback ("don't advance while red") is the model *following an instruction* (~70% adherence), not a motor — which is why the local mode doesn't *feel* like a loop. Maturity to move harness→loop = a verifier reliable enough to say "no" on its own (Milestone 1 + deterministic gates + validated contracts), and even then only where the retention trade-off is acceptable. The autonomous loop is the *worst* mode for cognitive debt, so harness-first is not just immaturity — it may be the right home for a regulated, high-blast-radius domain.
- **Independent validation.** Confirms, citing official docs, the `/goal` fresh-model maker-checker we verified against the primary; and independently lands on our cognitive-debt defense (for "comprehension rot": read the output, explain a change to yourself, can't explain = the map needs updating = our `/explain` + active recall). Adds a distinct category — **cognitive surrender** (attitudinal, not "no time": you stop bothering to have an opinion), guard = "the loop can execute for you, it can't decide for you." Presentation vocabulary worth keeping: the loop is a faithful multiplication sign — it amplifies whatever you bring, understanding or laziness.
- **Rejected / cautioned.** Popular-synthesis genre; author is explicitly a non-coder. He flags his own second-hand numbers as unreliable ("~90% of Claude Code self-written", "Nubank 1M lines 12×") — good discipline, treat as noise. Shallow exactly where we're hard (generic verifier, no contextual/normative conformance) — the same gap as gstack / Looper / CATS. The cost-framing from the same wave (iterations are the budget line; a weak verifier is the most expensive bug; fail-fast is cost control) is the other portable angle — the economic reason for our caps.

### 18. SDD rigor taxonomy — arXiv 2602.00180 "Spec-Driven Development: From Code to Contract" (2026-01) + "Understanding Spec-Driven Development: Kiro, spec-kit, and Tessl" (martinfowler.com, exploring-gen-ai series)

- **The three-rigor taxonomy inside SDD.** **Spec-first** — the spec precedes the code but may drift or be discarded afterwards (the code becomes the primary artifact); **spec-anchored** — the spec is permanent, maintained, and the code answers to it continuously; **spec-as-source** — code is generated/derived from the spec. The Fowler-site field observation: every SDD approach surveyed is spec-first, few strive to be anchored — i.e. *spec-first is the category that includes Kiro and Spec Kit; spec-anchored is what distinguishes from them.*
- **What it changed: the system's name.** "Spec-First Agentic Development" (chosen one day earlier, verified only against Kiro's branding, not the terms' semantics) named the system by the taxonomy's weakest level — the one defined by tolerated drift, in a system whose core is drift-as-bug. Renamed to **Spec-Anchored Agentic Development**; a positioning note with the taxonomy added to How-to-read; body self-descriptions updated. "Spec-first" kept only where it names the taxonomy level, and plain ordering rephrased as spec-before-code (the hook).
- **Continuity signal.** The exploring-gen-ai series is the same source as the feedforward/feedback 2×2 already in the catalog (ThoughtWorks/Böckeler) — two independent borrowings from one source suggests alignment, not cherry-picking.
- **Cautioned.** The taxonomy is young (one paper + one series article), and loose usage coexists (Microsoft and IBM treat "spec-first" ≈ SDD synonym). Mitigation: "spec-anchored" is self-descriptive even if the taxonomy fades. The paper's other claims and numbers were not verified — only the taxonomy was used.

### 19. "Building Effective Agents" — Anthropic engineering (Schluntz & Zhang, 2024-12; fetched and compared 2026-07-03)

- **The patterns vocabulary, mapped 1:1.** Workflows-vs-agents taxonomy plus the composable patterns — and our components map by name: prompt chaining + gates → the 7 phases; routing → `reviewer.md`'s table; parallelization (sectioning/voting) → the pinned single-lens mode; evaluator-optimizer → `/goal` (worker + fresh evaluator) and the capped review loops; the agent principles (environment ground truth, human checkpoints, stopping conditions, guardrails, "human review remains crucial") → evidence-in-transcript, gates / named-blocker aborts, turn + iteration caps, allowlist, human-on-every-PR. Orchestrator-workers deliberately rejected at the macro level (humans decompose into issues/slices); their own simplicity principle sides with that until evidence demands otherwise.
- **What it changed:** (a) the sectioning rationale added as a supporting note to the reviewer-mode A/B backlog item — the guide leans toward the always-parallel hypothesis; (b) the ACI gap surfaced (Appendix 2: they spent more time optimizing tools than the overall prompt) → the poka-yoke hook, previously one sentence in the guideline, now ships as an example artifact (`.claude/hooks/`).
- **Validation, not lineage:** the mapping was made post-hoc in this comparison, so it reads as convergence — presentation ammunition ("does this follow Anthropic's guide?" now has a pattern-by-pattern answer) rather than documented influence, though the article's ideas are ambient in the field.
- **Cautioned:** their framework warning starts applying to this bundle as it grows; the defense is that the layers ARE readable prompts and the entry point stays one spec file. Their closing ("the key to success is measuring performance and iterating") names our standing gap: designed, unexercised (n=1 run).

### 20. explain-diff — Geoffrey Litt (gist, fetched 2026-07-03)

- **What it is:** a diff-explanation skill in two variants (self-contained interactive HTML / Notion), structured Background → Intuition (with toy data) → Code → Quiz (5 MCQ, per-option feedback), with reusable diagram families, callouts, and a deliberately ephemeral output (global folder, date-prefixed, out of version control).
- **Absorbed into `/explain`:** the embedded **Quiz** — replacing the ask-to-be-grilled *invitation* with a built-in self-test ("substance, not gotchas"; per-option feedback); the layered **Background** section (weighted heavier on foreign-target reads); **intuition with toy data**; **diagram-family discipline** (HTML/SVG with example data, never ASCII); the **self-contained HTML format** with TOC and callouts; the **date-prefixed filename**; and his **pre-wrap self-check** — a prompt-level poka-yoke (he hit a failure mode and embedded the verification, the Appendix-2 pattern).
- **Adapted, not copied — the lifecycle stayed ours:** his output is a reading aid, ephemeral and out of VC; ours remains `docs/walkthroughs/` in-repo, an audit artifact mapping code to spec — now `.html`. The initial skip of HTML was reversed on the user's review: the diffability objection was overweighted for a write-once artifact; the accepted cost is that GitHub's web UI renders `.html` as source (local reading only — which is the ritual's actual use case).
- **The difference that prevented replacement:** intent anchoring. His explains the change from the code; ours against spec, plan, and recorded decisions (the criteria→tests map, decisions-and-why, domain rules with cited sources have no counterpart in his). Complement, not substitute.
- **Skipped:** the Kleppmann voice direction (taste; the completeness/cut bar covers quality) and the Notion variant (tool-specific).

### 21. "The New SDLC With Vibe Coding — From ad-hoc prompting to Agentic Engineering" — Google (Osmani, Saboo, Kartakis; May 2026 Day-1 paper; read 2026-07-03)

- **Column-by-column validation.** Their Table 1 spectrum (vibe coding → structured AI-assisted → agentic engineering) places this system cell-by-cell in the agentic-engineering column: formal specs / architecture docs / memory files → capability specs + constitution + context files; automated suites / CI gates / LM judges → mandatory-green CI + the four reviewer lenses; "agents self-diagnose within defined bounds; humans handle architectural issues" → the architecture-vs-increment split. Their central thesis — the single biggest differentiator is **how outputs get verified** — is this system's principle #3 in another house's words. The **factory model** ("the developer's primary output is not code — it's the system that produces code"; "success criteria rather than step-by-step instructions, then let them iterate") describes what the bundle is and what the `/goal` condition does.
- **The citable harness numbers** (what no prior source had): Terminal Bench 2.0 — a coding agent moved from outside the Top 30 to the **Top 5 by changing only the harness**, no model change; LangChain **+13.7 points** on the same benchmark tweaking only system prompt, tools, and middleware; "most agent failures, examined honestly, are configuration failures." This session's line-by-line prompt/harness audit is priced by these numbers.
- **Absorbed:** the **output-vs-trajectory evaluation** vocabulary ("a fluent output that skipped its verification steps is a more dangerous failure than one with a visible error") plus the **quality flywheel** (evaluate → diagnose by clustering root causes → optimize → verify against regression → monitor; each cycle compounds) — added to AUTONOMY-PLAYBOOK Milestone 1 as the two axes EVALS.md measures.
- **Deliberate divergences (recorded, not adopted):** (a) *intelligent model routing* (cheap models for review/test-gen) — we pin Opus 4.8 everywhere on purpose: the contextual/normative lenses are load-bearing, and a cheap reviewer is exactly where this domain doesn't economize; revisit as a cost lever at widening scale. (b) *tests-and-evals-before-code* — stricter than Phase 3 (tests per chunk); our contract already precedes code (acceptance criteria + reference-value table in the spec), and strict TDD would be a methodology change never chosen. (c) their requirements phase produces "specification and initial implementation simultaneously" — we stay spec-before-code; for a regulated domain their own Table 1 sides with that.
- **Validation, not lineage** (same note as #19-#20): mapped post-hoc; the convergence is presentation ammunition. Their closing — "Generation is solved. Verification, judgment, and direction are the new craft" — could be the guideline's epigraph; the paper declares it, the bundle executes it.

---

## Part 2 — What changed the system

| Idea | Source | Where it lives now |
|---|---|---|
| Backpressure: the machine produces the first "no" | Lucas | Fundamental Principle #5; the lens for every gate |
| Enforcement > instruction | Lucas's lament + hooks doc | Native `/goal` as autonomous engine (not a packaged skill); hooks roadmap |
| Router + modular review criteria | Lucas's repo | `reviewer` agent + 4 criteria skills |
| Domain review dimensions | Ours (gap in every source) | `constitution-compliance-review`, `conformance-review` |
| Load-bearing vs deferred decisions | Lucas (plan-review) | Phase 2 of both implementation skills |
| Tests anchor on the spec, not the implementation | Lucas + Addy | Phase 3 of both skills; `general-code-review` Dim 3 |
| Checks every chunk; never advance while red | Lucas | Phase 3 of both skills |
| Rationalizations / Red Flags tables | Lucas | Every skill |
| PR monitored until landed | Lucas | Phase 7 (`implement-backlog`); `/loop` candidate for local |
| Intent vs implementation review | Erikson (diffloupe) | `conformance-review` Dimension 2 |
| Structural exploration + edit precondition | Erikson | Codebase-exploration section in the root context-file template (Part 2); Phase 1 of both skills |
| Two entry points by mode | goal + hooks docs | `/implement` (local, gates) vs `/goal` (autonomous) |
| Abort as legitimate completion | Lucas + goal doc | "Done with a named blocker" clause in the `/goal` condition |
| Deterministic trigger decomposition | goal doc + headless | Thin GitHub Action + native `/goal` (no custom orchestrator) |
| pass^k, grader taxonomy, eval pitfalls | Wolfe / Anthropic Eng. | `EVALS.md` |

---

## Part 3 — Named concepts that became design rules

- **Backpressure** — every gate the machine can run must fire before a human
  looks. Where a human relays machine feedback, a check is missing.
- **Enforcement vs instruction** — hooks/conditions are guarantees; skills and
  prompts are hopes (~70% adherence). Critical rules deserve the guarantee.
- **Intent debt** — the why must be externalized where an agent can read it,
  at the altitude it is born; stale intent is worse than absent intent, so
  capture needs maintenance machinery.
- **Hill climbing on verifiable problems** — before designing any skill, name
  the verifiable landscape the agent will climb. No gradient → abort/ask, not
  guess (Phase 1.5 exists because ambiguity has no gradient).
- **Open vs closed looping** — open exploration belongs to Stage 0, human-led;
  implementation is closed. Loose standard = slop machine.
- **Who holds the plan** — the orchestration-primitive decision question:
  Claude's context (subagents/skills/teams) vs a deterministic script
  (workflows) vs deterministic infrastructure (GitHub + `/goal`).
- **Verification bounds throughput** — generation was never the bottleneck;
  parallelizing generation without scaling verification produces slop faster.
  Scale tools amplify exactly what the harness permits.
- **Strategic upfront, tactical evolving** — DDD's answer to Big Design Up
  Front; operationalized per-change as load-bearing vs deferred.
- **The `/init` test** — if the agent could regenerate an artifact by reading
  the code, the artifact pays no intent debt.
- **Harness lifecycle** — every harness component encodes an assumption about
  what the model can't do on its own; those assumptions go stale as models
  improve. Re-examine the harness on each new model, stripping pieces that
  are no longer load-bearing by one-component-at-a-time ablation (Anthropic
  dropped context resets after Opus 4.5 and the sprint construct after Opus
  4.6 — "the evaluator is not a fixed yes-or-no decision").

---

## Part 4 — Extracted backlog (not yet applied)

- **Reviewer-mode A/B eval (from the "4 agents" discussion, 2026-07-03).** When Milestone 1 exists: same diffs with seeded violations, multi-lens single reviewer vs parallel single-lens instances as the *default* (not only the >400-line escalation). Hypothesis to test: **cross-lens consistency bias** — a judge that just approved under one lens is less willing to block under the next; the strongest argument for always-parallel, currently unmeasured either way (and Anthropic's *Building Effective Agents* sectioning rationale leans this way: LLMs generally perform better when each consideration gets a separate call with focused attention). Measure recall per violation class, token/latency cost, and merge-step degradation (the worker deduplicating reports on its own code). Decides the default; until then, multi-lens default + size-based escalation stands, and the ~400-line threshold is a reasoned, never-calibrated number.

- **Boundary criterion for the reviewer (from the package-by-feature discussion, 2026-07-01) — ✅ APPLIED 2026-07-03 in the skills migration.** `plan-review` gained criterion 7 and `general-code-review` a Dimension-2 bullet: any NEW top-level folder/module in the plan or diff must pass the capability-vs-entity tests (business verb not data noun; vertical slice not horizontal layer; imports point inward). Slow structural drift stays deterministic (co-change + dependency-cruiser — quarterly check #5 in GUIDELINE Part 6), not an LLM lens: cheaper and better at the aggregate view, per the determinism-first principle.

| Item | Source | When |
|---|---|---|
| Tools allowlist on `reviewer.md` (read-only by config) | #10, confirmed by #11 | ✅ APPLIED 2026-07-03 — `tools: Read, Grep, Glob, Bash, Skill` in the agent frontmatter (edit tools stripped; Bash kept for `git diff`/`gh` inspection) |
| Scope-enforcement PreToolUse hook (committed-scope file) | Own review, validated by `/freeze` (#10) | After first real runs |
| `paths:` frontmatter on `.claude/rules/` | #10 (official) | After first real runs |
| `/loop` + `loop.md` as local-mode PR babysitter | #11 | When local mode is in routine use |
| `claude -w` per bounded context (deterministic fleet) | #11 | Post-Milestone 1 |
| Workflows: `spec-drift-audit`, `constitution-audit` | #12 | Post-Milestone 1 |
| Workflows for brownfield → DDD migration | #12 | When a brownfield effort exists |
| Proposer/refuter pass for critical findings | #12 | Optional reviewer evolution |
| Agent teams for Stage 0 exploration (devil's advocate) | #11 | Experimental; never critical path |
| Risk-based change classes; ops KPIs; traceability graph | #5 | Milestone 4 / EVALS evolution |
| Workflow validation vs known historical bugs | #3 | Milestone 1 (EVALS) |
| `assumptions.md` / `boundaries.md` in Phase 2 | #3 | If Phase 1.5 proves insufficient in practice |
| Promote recurring lessons → skill Red Flags | #10 (Thariq) | Periodic ritual once lessons accumulate |
| Routines (cloud) for the nightly routine | #11 | Verify routines doc first |
| Verify real headless GitHub Action setup | #7 | Before enabling the autonomous trigger |
| Harness re-audit ritual: ablate one component at a time on each new model release | #15 | Each model upgrade |

---

## Part 5 — Meta-lessons

1. **Verify in the primary source before adopting.** The "12 Patterns" article
   invented two commands; the workflows article oversold resumability; a
   prompt trick was presented as syntax; and the assistant itself was wrong
   three times about Claude Code tooling (view_range, `/goal` provenance,
   native features post-cutoff). Listicles are leads, not references — the
   repo/doc/blog behind them is the reference.
2. **Mine ideas, don't adopt packages.** We took Lucas's architecture and
   rewrote the content for the domain; we took AI-DLC's skeleton and discarded
   the ceremony. The difference between installing `backpressured` and
   understanding why it works is the difference between dependency and design.
3. **Convergence is the signal.** Lucas, AWS, Addy and Anthropic's own
   platform features arrived independently at the same shape: externalized
   intent in versioned artifacts, machine gates before human review, the human
   at load-bearing decisions. Independent convergence on the design you built
   is the strongest available evidence the direction is right.
4. **The next learning comes from running, not reading.** Every source above
   has paid out. The ratio of written process to executed process is the
   system's current biggest weakness — the first real issue through the
   pipeline is worth more than the next article.

---

## Appendix — Verification record

Claims that failed or degraded under fact-checking, kept as a reminder of
lesson #1:

- `/btw` command — zero occurrences in the cited repo; likely invented by the
  article.
- `--bare` flag (+ "10x faster" numbers) — zero occurrences; unverifiable.
- `<important if="...">` — presented as supported CLAUDE.md syntax; actually a
  community prompt trick (no loading mechanism). Real mechanisms: CLAUDE.md
  proximity loading and `paths:` on rules.
- Dynamic-workflows resumability — official doc limits resume to the same
  session; the article implied robustness across exits.
- Workflow availability — article said Max+ only (preview-era); now all paid
  plans (Pro via toggle).
- Workflow primitives (`agent()`, `parallel()`, `pipeline()`, determinism
  ban, schema-retry) — plausible from generated-script inspection, **not in
  the official doc**; treated as unverified detail.
- "84% fewer permission prompts" — real, but an Anthropic-internal figure
  quoted from a tweet, not a general guarantee.
- Bun Zig→Rust port — real (official blog), with a caveat the secondary
  article omitted: "not yet in production".
- "Context Reflect" — term found nowhere official; apparently invented by the
  Medium harness article. The real, official mechanism is **context resets**
  (fresh agent + structured handoff artifact), explicitly distinct from
  compaction.
- "Context anxiety named by Anthropic's researchers" — the phenomenon is real
  and the term appears in Anthropic's official harness article, but it was
  coined by Cognition (Devin on Sonnet 4.5); the Medium attribution was loose.
- 68% → 95% task-success numbers (Medium harness article) — unverifiable
  Medium precision.

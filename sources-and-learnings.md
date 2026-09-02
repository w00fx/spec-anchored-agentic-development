# Sources & Learnings

> Companion to `GUIDELINE.md`. Every external source mined while designing this
> methodology, what each one contributed, what we rejected and why, and the
> meta-lessons about consuming this kind of content. Useful as onboarding
> material and as the audit trail of *why the system is the way it is* — this
> document is itself intent-debt paydown.
>
> Last updated: 2026-08-12 (entries are appended with their own read dates; this header tracks the file, not each source).

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
  precondition) → the exploration block in the root `CLAUDE.md`. The
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
**(v2 addendum, 2026-07-30:** the parent methodology was rebuilt — AI-DLC Workflows 2.0 converges on this system's architecture; see #47.**)** The domain-specific derivative of AI-DLC; the strongest *domain* validation we
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

### 22. "Write code, not specs" — Doug Turnbull (softwaredoug.com, 2026-07-04; fetched 2026-07-04)

- **The steelmanned opposition.** His complaint: "two systems — one imprecise, one extremely precise — and now I have to maintain both"; his alternative: hand-write code at the frontier to develop taste, trust the agent inside the tilled garden, requirements live in tests ("at a certain level of maturity, the tests become the code"); his own honesty: "this may be as much about preference."
- **How much he agrees with without knowing it:** "a gradually expanding surface of trust" = the narrow start; executable truth = the golden path; "maintaining my own human context along with the agent's" = the walkthrough + quiz.
- **The crux is a premise, not a method: where truth lives.** His world = internal/emergent truth, where the argument is valid. Ours = external truth with citations — tests encode the value but not the norm, version, and scope; tests are existential records and cannot carry Non-goals; the auditor doesn't read Go; and "trust the tests against what?" resolves, in his system, to his own head (n=1, doesn't survive a team or a vacation).
- **His experience was loose spec-first** (fat functionality prose, manual sync) — the level we also reject. He solves drift by deleting the spec; we solve it by mechanizing drift-as-bug. The tax formula: **tax = overlap × write-frequency** — both engineered to ~0 here (spec carries only the non-inferable; writes happen at the rate the business changes, and external-source updates *originate* in the spec).
- **Counter-arguments recorded (the user's):** single governance — spec as markdown in the repo rides the same PR rails as code (diff, approval, `git blame` as audit trail); merge-at-gate is *stronger* than same-PR approval (a working implementation biases the rule's approval); the founder case — the agent is the first team member with no tacit-knowledge channel, so the spec substitutes the internal verifier Doug's taste provides at n=1; brownfield spec-writing = an audit with a deliverable; PR approval = finality (authorship can be AI's; authority is human — approved = canonical, no double bookkeeping).
- **Hits conceded:** who writes the first pattern (his hand-written frontier is a defensible personal practice our docs neither adopt nor rebut — and nothing forbids it); the solo/internal-truth profile is his local optimum and outside this system's target.

### 23. "Closing the Verification Loop" — Kieran Klaassen, Compound Engineering plugin (thinkroom; fetched 2026-07-04)

- **First shipped system of the same genre** — and the proof our Milestone-3 Tier-2 QA agent is buildable as a skill: `/ce-dogfood` runs browser-level QA of the branch's changes, on **localhost pre-merge** (improving our M3 plan, which assumed post-deploy).
- **Convergences:** "claim plus independent proof, at every altitude"; the 3-cap with residue written into the PR ("the loop never closes silently on an open question; it closes by making the question impossible to lose"); the resumable report on disk; the hollow-tests ban; "the browser's independence is physical; **it cannot be talked into agreeing**" = determinism-first.
- **Absorbed:** red-test-per-fix into both skills' Phase 5 ("failed before the fix and passes after it") — stronger than the source: their trail "records that red was claimed, not a capture of it"; our red is transcript-captured (supervised) or logged (autonomous). The email rule ("an email sends is not a pass — does the click-through land on the RIGHT thread?") → `/shape`'s criteria guidance: assert the journey's true end state. Independence budgeting → the reviewer-mode A/B backlog item.
- **The operational gotcha adopted immediately:** "a skill invoked in its authoring session tests the stale cached copy" — skills and registered agents load once per session; every artifact edited in a session requires a FRESH session to test.
- **Their gaps vs. ours:** persona walks are one head simulating many (they admit it: "two judges, one head") vs. our real isolation; their flows are derived from the diff + product intuition — verification against user experience, never against external truth (the adjacent of the circularity our conformance forbids); their specialist-prompt-assets pattern buys freshness and portability at the cost of the mechanical frontmatter enforcement our registered reviewer just gained — trade-off registered, not switched.

### 24. Matt Pocock's skills — grilling, domain-modeling, grill-with-docs, to-tickets (github.com/mattpocock/skills + aihero.dev; fetched 2026-07-04/05)

- **The pipeline:** grill → to-spec → to-tickets → implement. Taxonomy placement: **spec-first** — a per-change PRD published to the issue tracker, which then becomes history. The pipeline *shape* was absorbed; the artifact model was not (adopting it would regress spec-anchored). His durable layer is glossary + ADRs; ours is the capability spec (glossary inside — consumed by construction, since every run reads the spec) + `architecture/decisions/`.
- **Architecture lesson:** composable micro-skills — `grilling` is four sentences; `grill-with-docs` is ONE line composing grilling + domain-modeling; formats live in separate files. We kept monolith commands (self-containment + paste-into-chat portability; single consumer today) — extraction to a skill becomes right if a second consumer appears. **Field addendum (first `/shape` runs):** inline-capture-into-the-spec conflated the draft with the artifact — the model wrote the file mid-interview and kept asking, forcing the human to review a moving file while answering; the fix restored his composition on the write side (`/shape` interviews, `/to-spec` writes — the grilling → to-spec split, vindicated by execution). **Second field upgrade (2026-07):** his `batch-grill-me` (in-progress) replaced one-question-at-a-time with **frontier rounds** — a design tree; every currently-unblocked question asked at once, numbered, with recommended answers; dependencies deferred to later rounds; facts found by non-blocking sub-agent dispatch — absorbed into `/shape` after the user's own field test preferred it. The frontier definition is `/spec-to-tickets`' Kahn-by-generations applied to conversation: convergence, not coincidence.
- **Absorbed into `/shape`:** one-question-at-a-time ("asking multiple questions at once is bewildering"), a recommended answer for every question, explore-the-codebase-instead, "until we reach a shared understanding" as the termination, the four active session disciplines (challenge against the glossary, sharpen fuzzy language, concrete scenarios during the session, code-challenges-claims), the opinionated glossary with `_Avoid_` (also into the spec template), the minimal ADR (triple test; "an ADR can be a single paragraph"; the explicit no-s; the GraphQL-in-six-months rejection rule).
- **Absorbed into `/spec-to-tickets`:** tracer bullets, blocking edges + the frontier ("several agents can run at once"), the quiz-before-publish with its three questions, blockers-first publishing ("so edges reference real identifiers"), expand–contract with the integration branch ("green is promised only there"), the staleness rule with the prototype exception, the dual destination (tickets.md / real tracker).
- **The adaptation ledger — and the lesson learned twice:** mechanic, format, and LOCATION are three separate decisions (his `docs/adr/` → our `architecture/decisions/`, dated not numbered; his `ready-for-agent` → our `auto-implement` gated by the narrow-start allowlist; his repo-global CONTEXT.md → our per-capability in-spec glossary). And: **read the SKILL source, not the marketing page** — the first `/shape` was built from the aihero.dev pages and missed the four active disciplines the real domain-modeling carries.

### 25. Pocock's implementation side — implement, tdd (tests.md, mocking.md), code-review (github.com/mattpocock/skills; fetched 2026-07-05)

- **Validation.** His `implement` is five lines of composition (tdd at pre-agreed seams → /review → commit) — ours is the process superset (gates, scope discipline, evidence, aborts, logs). His code-review's two axes (Standards / Spec) are our general-vs-conformance split, with the separation rationale in his words: "a change can pass one axis and fail the other... reporting them separately stops one axis from masking the other."
- **The divergence that shrank.** His TDD's "Anti-Pattern: Horizontal Slices" attacks exactly the tests-first-in-bulk we rejected from the Google paper ("tests written in bulk test *imagined* behavior... you outrun your headlights") — his real TDD is an interleaved micro-cycle, millimetres from our chunk loop. Residual divergence: test-immediately-before vs code-then-test *within the chunk*; red-first already adopted where it pays most (red-test-per-fix, #23).
- **Absorbed.** `references/test-standards.md` — the shared producer/judge bar (three worked GOOD/BAD pairs including verify-through-external-means; name-states-WHAT; one logical assertion; the mocking boundary rule — boundaries only, never your own code; DI + SDK-style interfaces), pointed at by the lens's Dimension 3 AND both skills' Phase 3.2: one file, both sides of the gate. `references/smell-baseline.md` — twelve Fowler smells (Refactoring ch. 3) with his binding rules (the repo overrides; always a judgement call → capped [SHOULD]; skip what tooling enforces = determinism-first), cross-referenced to Dimension 4, the constitution's Decimal, the Opus guard, and package-by-feature. Typecheck added to the chunk loop (closing the TS build≠typecheck hole at loop level). Pre-dispatch sanity in Phase 5 and `/review` ("a bad ref or an empty diff should fail here, not inside parallel sub-agents").
- **For the A/B.** Parallel-per-axis is his *default*, and cross-axis merging is forbidden — third practitioner data point for always-parallel, and a third merge-step design (present per-lens, never collapse).
- **Architecture contrast that paid.** His generic sub-agent needs the smell baseline pasted in full per dispatch ("the sub-agent has no other access to it"); our registered reviewer loads the lens, which reads its own references — the #23 freshness-vs-enforcement trade-off, with a concrete win on this side.
- **Not absorbed unread:** deep-modules.md, interface-design.md, refactoring.md, DOMAIN-AWARENESS.md exist in his tdd skill and were outside the five sources given — the #24 lesson holds.

### 26. "Harness Engineering for Self-Improvement" — Lilian Weng (lilianweng.github.io, 2026-07-04; fetched 2026-07-08)

- **The theoretical frame for this system's practice.** Her definition — the harness "orchestrates execution... calls tools and acts, perceives and manages context, stores artifacts, and evaluates results"; the engineering includes "workflow design (loop engineering), evaluation, permission controls, and persistent state management" — is the bundle described formally. Her three design patterns map onto the architecture: the goal-oriented loop ("plan, execute, observe/test, improve... *until* the goal is achieved") = the phased skills under `/goal`; filesystem-as-memory ("stored as files, logs, and status records, the model can recover after interruptions and reason over its own execution history") = specs, logs, lessons, plans-in-PR-descriptions; subagents "without polluting the main context" = the reviewer and the pinned parallel mode.
- **The never-articulated justification, now stated:** design harnesses "with reference to existing software engineering practices **to benefit from pretraining knowledge**" — the theoretical reason this system's choices work: EARS, GWT, Fowler's smells, conventional branch prefixes, and the classic PR flow all carry pretraining mass. The choice was instinct; she supplies the why.
- **The optimization ladder locates us:** prompts → structured context → workflow → harness code → optimizer code. This system hand-built through the fourth rung; her survey is the fifth (Self-Harness, Meta-Harness, DGM, evolutionary search) — which by her own criteria "struggles with domains where evaluation is slow, ambiguous, or mostly heuristic-based": the definition of this domain. The manual flywheel with humans as the evaluator is the correct rung here, by her own ruler. Self-Harness is the automated future of Milestone 1's flywheel — its held-in + held-out acceptance bar was absorbed into the playbook.
- **Her safety principle is this architecture:** "the evaluator and permission control should likely sit outside the loop... with held-out tests, trace audits, and human review at decision points that matter" — spec propose-only, untouchable constitution, human-anchored golden, gates. STOP's result (improved with GPT-4, degraded with weaker models) validates the model pin + re-audit doctrine by experiment.
- **Presentation ammunition:** the six agentic-research failure modes (training-data defaults; implementation drift under execution pressure; memory degradation; over-optimism / "numerical duct tape"; insufficient domain intelligence; weak taste) map 1:1 onto countermeasures this system already carries (context files + source citations; conformance-to-plan + plan invalidation; persistent logs; evidence-before-done + red-test-per-fix + the `/goal` evaluator; constitution + reference values; the human at shape and gates). The internalization prediction answers "won't better models make this obsolete?": harness tricks internalize, but "the need to specify **goals, constraints, context, and evaluation** did not disappear" — specs, constitution, context files, and the golden ARE that durable layer. Her closing is the system's thesis in her words: "Humans should move up the stack, not be removed from the loop."

### 27. "A Taxonomy of Self-evolving Agents" — Shilong Liu (lsl.zone, 2026-07-08; fetched 2026-07-13)

- **The positioning companion to #26** (published four days after Weng's — the field's same-week conversation). His taxonomy organizes self-evolution by WHAT evolves: **artifacts** (the agent improves outputs — AlphaEvolve kernels, auto-research papers), **harness** (the agent improves its own prompts/memory/tools/skills — GEPA, ACE, skill creation, multi-agent routing), **model** (weights without gold answers — self-training, self-play, TTT).
- **The sentence it gives this system:** level 1 autonomous and bounded (the `/goal` loop against human-set criteria — his level-1 description names Claude Code); **level 2 propose-only, humans commit** (lessons curated; CLAUDE.md and spec corrections proposed with `requires_human_approval`; the M1 flywheel with the human at the wheel); level 3 out of scope.
- **Quotables:** "A human is a router" (routing as the expert's most valuable ability = decomposition-as-human-skill + the gates); the "squeeze" example (semantic confusion from context pollution = the lens-separation rationale and, at domain level, the `_Avoid_` glossary); the closing three questions — "What evolves? What feedback drives it? **Where does the loop close?**" — with his warning ("if the loop closes on benchmarks, we get stronger benchmark solvers") answered by the M1 held-out bar: ours closes on merged PRs against external-truth specs.
- **The axis his taxonomy misses — our fourth question:** level 2 conflates agent-modifies-own-harness with agent-proposes-and-human-commits, a load-bearing safety distinction (#26 makes it; he doesn't). The addition: **"Who can commit the change?"** — and this system's answer is the Doug-debate formula: authorship can be AI's; authority is human. Flagged in passing: FARS (417h, 166 AI-generated papers, $180k) cited neutrally, quality unexamined.

### 28. "The Anatomy of Intent (ICE in IDSD)" — Kapil Viren Ahuja (Medium, 2026-05-27; triangulated 2026-07-13, full text read 2026-07-14)

- **The best specimen of the 2026 SDD-critique genre** (Doug #22 = delete the doc; the falkster counter = prototype-as-spec; Ahuja = split into ICE) — all attacking spec-FIRST, none reaching anchored. The teaching story from his sibling piece: **his spec-kit spec "blew apart" on a Vercel→GCP move because the spec contained the deployment target** — the layer mixing this system's separation forbids (a hosting change touches zero capability-spec lines here; an ADR at most).
- **He is `/goal`-native, not opposition:** the argument stands on Claude Code's goal engine, cited with the exact mechanics ("a small, fast model checking each time whether the condition has been met") — "we took a goal-seeking engine and told everyone to feed it a form." He exempts regulated domains explicitly ("a leash is rational... it does the job") and concedes the rename critique himself ("taken together, ICE is still a spec").
- **The primary receipts:** Spec Kit's manifesto selling constraint as the product ("transform the LLM from a creative writer into a disciplined specification engineer"); the spec command instructing "make informed guesses", "fill gaps", capped at "Maximum 3 [NEEDS CLARIFICATION] markers" — the anti-Phase-1.5 (here: unresolved ambiguity is an abort, never a guess, with no cap on admissions); three contradictory test rules shipped together (NON-NEGOTIABLE / OPTIONAL / mandatory TDD).
- **Two sharp tools absorbed as vocabulary:** the **two-implementations test** for goals ("if only one implementation could possibly satisfy it, you wrote a spec and called it a goal") — the complementary inverse of the `/shape` divergence probe: a good spec criterion passes his test (technology-free) and fails ours (behavior-unambiguous); and the **constraint-vs-failure decision rule** ("Would knowing this change how the builder writes code?").
- **The design challenge, answered and recorded:** his **compartmented evaluation** (builder never sees the validator's checks — "encrypted evals"; "compartmenting is the only structural defense" against reward hacking) vs this system's implementer reading the criteria and reference values. The answer: Goodhart applies when the measure proxies the target — **our golden IS the target** (external truth: "overfitting" to the cited rate is called correctness, and hiding the table means the builder guesses the rate). For proxy checks (coverage, quality gates) the defense here is **visible truth + an independent judge** (hollow-test ban, red-test-per-fix, the fresh-context reviewer). He buys anti-gaming with secrecy at the criteria; we buy it with independence at the judge — and secrecy requires his closed harness (Garura, proprietary; the 3-4x claim self-declared un-mathed).
- **Where he stays spec-first:** per-outcome Intents, no permanent capability anchor, no source provenance, no conformance-after. Unread per the #24 lesson: the Iron Triangle piece and the Context/Expectations installments.

### 29. "Stop being the code review bottleneck" — Jina Yoon, PostHog newsletter (2026-07-09; fetched 2026-07-14)

- **Practitioner validation at company scale — with the academic citations this architecture never had.** Their principles arrive footnoted: the writer can't review its own work (Tyen et al. 2024 — the reviewer's independence); multiple differently-instructed reviewers cover more gaps (Qian et al. 2025 — the parallel lenses); different models/providers as reviewers (Verga et al. 2024, "Replacing Judges with **Juries**" — the cross-family review of the A/B item, now with a named paper). Paul D'Ambra's qa-swarm converges in the details: four parallel reviewers; actionable / nit / ambiguous triage (ambiguous escalates to the human); an outer loop **capped at three iterations** — the fourth independent practitioner on the 3-cap. Cost, quotable: "60% of my token spend is burned automating the toil of handling CI and review and I don't regret a single dollar."
- **StampHog = Milestone 4 running in production, with numbers** (1 in 3 merged PRs auto-stamped, 1.6K/month): opt-in per PR via label; deny-list of never-AI-approved classes by blast radius (auth, secrets, billing, public APIs); size ceilings (500 lines / 20 files); "fail closed... **LLM can tighten gates but never loosen**"; SME escalation via CODEOWNERS + git-blame familiarity. The shipped field version does **auto-approval, not auto-merge** — more conservative than the M4 sketch was. Both calibrations adopted into the playbook, plus the stamp-as-eval-base point: the stamper's decision log (approve / refuse / escalate, each with a reason) is the labeled dataset that calibrates class widening — start it early, even refuse-mostly.
- **"Observability over reasoning"** ("don't accept an argument that the code works when you can *watch* it work") = evidence-before-done verbatim, scaled via stacked PRs ("each layer only builds on behavior that's already been verified") — and their sizing prompt says "each under **400 changed lines**": an independent field datapoint landing exactly on the reasoned, never-calibrated ~400 threshold. The frontend evidence-capture pattern (state screenshots + interaction GIFs on the PR) absorbed into the PR playbook.
- Leads, unread (the #24 lesson): Osmani's "Agentic Code Review"; Litt's "Understanding is the new bottleneck"; Ronacher's "Better Models: Worse Tools".

### 30. AutoResearch — Andrej Karpathy (github.com/karpathy/autoresearch, 2026-03-07; verified 2026-07-15)

- **The minimal shipped implementation of the optimization loop** ("The Karpathy Loop"; 66k stars in a month): a coding agent — Claude Code, Codex, or equivalent — pointed at a single-GPU nanochat training core plus a Markdown instruction file, looping indefinitely: read the code, propose a change, train five minutes, measure one metric, **commit if improved, roll back if not**. Git is the ratchet; the fixed budget makes experiments comparable. His own two-day run: 700 experiments, 20 stacked improvements, Time-to-GPT-2 2.02h → 1.80h — unattended.
- **Why it runs overnight, in this catalog's physics:** the evaluator is outside the loop and *computed*, not judged — a scalar produced by execution; no judge to convince, no template to rationalize (#26's principle in its purest form). Liu level 1 (artifact iterative optimization); Weng rung 5 (optimizer code) at minimal size.
- **The three transferable conditions** — the applicability test: (1) an objective scalar metric computed by execution; (2) fast, fixed-budget evaluation (minutes); (3) cheap rollback. Where all three hold, ratchet unattended; where any fails, you can't.
- **The mapping for this system:** the normative core fails condition 1 by definition — compliance is boolean-per-criterion against human-anchored golden, not a gradient; this loop is *satisficing against evidence*, his is *optimizing against a metric* — same engine (`/goal`), different oracle classes. Four legitimate incarnations here: **performance tickets** (benchmark as metric, golden + suite green as the anti-Goodhart constraints — a future `auto-optimize` ticket class); **prompt/harness optimization once EVALS.md exists** (the Milestone 1 → rung 5 unlock: stamper log → dataset → scored evals → the ratchet climbs them); CI/build time; any Tier-1 measurable. Never: business rules, spec content, the constitution — no scalar, and the never-list.
- Community generalization: Lütke on query-expansion models; the pattern on prompt optimization against a graded rubric (32/40 → 40/40 in six runs) — the shape of what the Milestone 1 eval suite enables here.
- Pocket: "the Karpathy Loop answers 'where does a run compute a trustworthy number in minutes?'; this system answers 'where is truth normative and the commit human?' — the same engine with different oracle classes. A mature shop runs both: the ratchet on scalars, satisficing-with-gates on the normative."

### 31. "SDD in Scrum and Kanban: Where the Spec Actually Lives" — Jaroslaw Wasowski (2026-07; read 2026-07-13)

- The one angle no prior source covered: the ceremony cycle. Uses the three-rung ladder **by name**, attributed to Birgitta Böckeler (Thoughtworks) — the vocabulary's second independent carrier. His rule — "most teams should stay at spec-first; spec-anchored makes sense where multiple teams **or agents** share one contract" — **read in the agent era, selects anchored for this shop**: every fresh session is another agent sharing the contract. Pocket: his default is right for human teams with internal truth; his own criterion selects us.
- Process mapping adopted as pocket answers: backlog stays at goal/intent = tickets point-never-copy; the delta merged at the gate **= the Definition of Ready**; **Kanban's commitment point = the frontier** (ready-to-pull = blockers closed + spec committed); Upstream WIP limits = YAGNI-at-n=0.
- Data with caveats: +19% velocity / −31% defects (sMBSAP, single project); the 10x slowdown on small CRUD (level mismatch — this system's answer is stronger than "drop to spec-first": increments write no spec at all); METR's perception gap ("the gap between perception and metrics is the real opponent"). "Constitution plus Spec" named in the wild, with the cap-on-invariants caveat. His metrics trio includes **rework rate** — the logs' `Replans` + review-iteration counts already instrument it.

### 32. "Loops are over — graphs now": the narrative, decoded (explainx update 2026-07-18; arXiv 2604.11378, verified excerpts)

- The meme distorts its own sources: the loop-engineering site itself (#17's home) frames graphs as the **next layer** — "Loops = one agent's behavior. Graphs = the org structure connecting many agents" (with Cherny's "I have loops that are running... prompting Claude"). LangGraph's own docs: graphs *contain* loops.
- The real shift, with numbers: multiple simultaneously dispatchable units (the paper's critique of "single-ready-unit schedulers, |U|=1"); scoped contexts per node (TDP: **−82% tokens**, replanning confined to the active sub-task); structured plans between LLM and execution (Routine: **41%→96%** tool-calling); "deliberately restrict expressiveness... to **maximize controllability and verifiability**"; Datadog: 60% of production LLM failures = runaway-loop rate limits.
- **The receipts — this system already is the graph-over-loops architecture:** tickets+Blocked-by = the explicit graph; **the frontier = |U|>1** (the paper's exact complaint, solved); fresh session + committed file scope = scoped contexts; per-run plan-invalidation = confined replanning; the `/spec-to-tickets` quiz = human-approved topology; `/shape`'s frontier rounds = the same discipline in conversation. The design difference for the stage: **our graph is data in GitHub (versioned, human-legible, harness-agnostic), not framework code** — a trivial scheduler instead of a runtime. Pocket: "os loops não acabaram — desceram um andar."
- Flag: the arXiv paper read in verified excerpts, not integrally (the #24 lesson holds).

### 33. "/prewalk — you only need the frontier model for one single edit" — Can Bölük, Stencil (2026-07-13; SWE-Bench Pro, 7 arms)

- "**Hand off a trajectory, not a fairytale**": the frontier model explores, plans as a todo list, lands the **first edit** — then swap to the cheap model *inheriting the full context window* (prefill generalized to turns). 92-97% of frontier pass at ~half the cost, fastest arm. The `/plan` handoff **refuted by measurement**: Opus-plans + Flash-executes costs *more* than Opus solo at the same pass rate. Root economics: edits ≈ 9% of tokens; **the bill is O(reads)** — "Opus fixing things does not cost money. Opus *reading* things costs money"; a plan is "a 2K-token postcard from 100K of grounded context."
- What it means here: **plan-as-gate (ours) is the architecture their data favors** — same-context execution; the document serves the approver, not transfer. The postcard critique lands on the subagent-implementer topology — **decision revised**: "plans as complete serializations" now has counter-evidence; transfer the window, not the doc; that topology is downgraded in the experiment queue.
- **Model routing gains mechanism + data**: route within-task by phase, swapping **at the first edit** ("the point where it was confident enough to act" — behavioral trigger; fixed-turn failed). Queued experiment: `/model` swap after the first green chunk, made safer here by Phase 4/5, the golden, the pinned reviewer, and the human PR gate.
- Stage-grade finding: **`/plan` increases cheating** (44%→72% searching the public answer); `/prewalk` crushes it (→13%) — planning-without-contact "breeds desperation"; the executor "inherits a context where **the approach already survived contact with the code**." Seam-first quantified, and a third honesty mechanism named: **trajectory shaping** (alongside evidence demands and judge independence).

### 34. AIDE² — Weco (Zhengyao Jiang, 2026-07-14)

- **The top of the ladder, demonstrated:** two nested autoresearch loops — the outer optimizes the inner agent's **harness code** against the inner loop's average score across benchmarks. 8 days, 100 outer iterations → 7 discovered improvements (a new search policy; a 16× prompt-compressing memory; **a layered defense against reward hacking**). **Held-out:** beats their 2-year hand-tuned harness on all three unseen benchmarks, one outside the training families.
- Confirms this system's positioning with an existence proof: rung 5 requires exactly what they had — a scalar, automatic, cheap outer oracle (many evals). The M1 → rung-5 unlock (#30) now has its ceiling instance. **Their evaluator stayed outside the loop** — the benchmarks were not optimizable; their never-list is ours.
- The philosophical find: **anti-reward-hacking emerged** from optimizing for held-out generalization — a **third anti-gaming path** joins the map: secrecy-at-criteria (#28), independence-at-judge (ours), and **diversified objective** (hacking one benchmark doesn't pay against the average) — what a scored eval *suite* buys for free.
- Honesty both ways: "Level 2... results are mixed, and **we do not claim ignition**" — the takeoff question answered with data; human-speed remains rational. Flags: vendor bias (Weco sells autoresearch); thread+blog, not peer review; metric-rich domain; "first evidence" overstated (STOP 2024, DGM 2025 preceded — the novelty is held-out strength against a production harness).

### 35. "The $110/month self-improving pipeline" (autoloop) — Andy Widjaja (2026-07-14)

- **Independent solo-scale replication of the autonomous route, with production numbers:** 2 weeks, 27 autonomous merges, 1 failure, **$1.61/issue**, $110/month all-in. Convergences arrived at independently: recursive decomposition "until buildable in one pass, small enough to review on a phone"; "picks the top ready issue with respect to dependency ordering" (**the frontier, third reinvention**); retry ≤3 with errors fed back, then `needs-human` (**the fifth independent practitioner on the 3-cap**) plus a test-files-added hollow guard; the human PR gate as declared architecture. Day-8 is the clean-abort anecdote: "It just knew it couldn't produce a valid PR. **So it got out of the way.**"
- The thesis from the solo trench: "**The bottleneck isn't the model... it's the issue quality**"; "**The system exposed my sloppy specs faster than any code review would**" — autonomy as a spec-quality detector; the cure-shaped hole in his stack is this system's anchor layer, and he exempts regulated environments explicitly (the catalog's second).
- His deltas are this system's diffs: no spec layer; decomposition unattended (his Day-12 sub-issue conflict = the class the human quiz catches); no independent reviewer (his teaser: observer/builder separation next).
- **The absorbed hardening:** his `protected_paths` — "**self-improvement without self-modification**: it improves the *product*, cannot improve the *process*", enforced at triage AND implement — exposed an enforcement gap here: autonomous scope now explicitly excludes harness files (the `implement-backlog` scope-routing line, applied with this entry).

### 36. "Rewriting Bun in Rust" — Jarred Sumner, Bun/Anthropic (bun.com, 2026-07-08; primary source read in full + Pragmatic Engineer commentary)

- **The catalog's crown case study: every load-bearing thesis at fleet scale.** 64 Claudes (Fable 5 pre-release) × 11 days × ~50 dynamic workflows: 535K lines of Zig → 1M+ lines of Rust, 6,502 commits, ~$165K (5.9B uncached input tokens — the O(reads) bill of #33 at fleet scale), against an estimated 3 engineer-years. Orosz's verdict is the oracle thesis verbatim: "**a thoroughly-tested project is required to pull it off**."
- **Adversarial review = this system's reviewer, in his words:** "The Claude that wrote the code **wants the code to get accepted**... 1 implementer, 2 or more adversarial reviewers... The implementer doesn't review. The reviewer doesn't implement" — reviewers get "**the diff and nothing else** — none of the implementer's reasoning — and told to **assume the code is wrong**." The three showcased catches (async-close UAF/double-free; negative-timespec trunc-vs-floor; eager `unwrap_or` panic) all compiled and looked plausible — the class only fresh-context adversaries catch. Tyen et al.'s strongest field instance.
- **Oracle + anti-gaming receipts:** a language-independent suite with 1.38M assertions; the compiler as work queue (16K errors, crate-by-crate, grouped by file); "**0 tests skipped or deleted**", with the human auditing the oracle itself ("I manually verified the tests were in fact running and not being skipped"); the stub-out false start ("Claude interpreted 'get the crates to compile' as 'stub out the functions'") killed by ONE rule handed to the adversarial reviewers — "If you need a paragraph-long comment to justify why the workaround is OK, **the code is wrong — fix the code**" (absorbed into the smell baseline with this entry); and the method as doctrine: "**fixing the process that generates the code instead of hand-fixing the code**."
- **The pipeline is this pipeline:** 3 hours of talk → `PORTING.md` + `LIFETIMES.tsv`, each lifetime through 2 adversarial reviewers — **the migration's capability spec**, the anchor the whole fleet verified against; a trial run of 3 files before 1,448 (the narrow start); "**Merging into main isn't a versioned release**" (the confidence gradient); post-merge, 24/7 fuzzing files Claude PRs that **humans review** — propose-only running inside Anthropic itself. **19 known regressions, all documented** ("syntactically identical but semantically different") — Liu's tacit-invariants critique (#taxonomy debates) answered empirically: the residual after a million assertions, made visible and fixed.
- Pocket: "o Bun mostrou o teto — com oráculo forte, 11 dias e $165K compram três engenheiros-ano. Este sistema é a fábrica do oráculo para os domínios onde ele não vem de graça; e a arquitetura que gastou bem esses $165K (adversarial fresco, processo-não-output, merge≠release, zero testes pulados) é a deste bundle."

### 37. "Contract-Driven Development: Write the Truth Once" — Ben Howdle (benhowdle.im, 2026-07-15)

- **The practitioner voice for the contracts layer** — three builds of one idea across seven years: a bank (16 OpenAPI YAMLs, one per bounded context, generating 349 files — "sixteen files that described the whole bank"); the rebuild at the same bank (CUE+protobuf); his own product (TypeScript+Zod: 6,200 contract lines → 15,400 generated; frontend/backend SDKs **byte-identical, SHA-256 equality as the drift alarm**; a 24h freshness check; "FAIL-FAST ONLY. NO PLACEHOLDERS"). The thesis in his words: "every duplicated definition is two truths waiting to disagree... **stale truths are just bugs on a delay**... **The contract *is* the system.**"
- **Convergences, quotable:** "design arguments moved into the spec — the cheapest possible time to disagree" (the gate economics); "a whole category of bug became **unrepresentable — not caught, unrepresentable**... the drift has nowhere to live" (mechanism-over-instruction at its purest); "refusing to compile is *so* underrated as a communication mechanism"; **authorization in the spec, fail-closed** ("an endpoint with no declared policy defaulted to *denied*"), with the regulated-domain payoff — "**a security review was reading one file**... weeks of audit pain converted into an afternoon"; escape hatches as load-bearing ("a pipeline with no escape hatches gets bypassed entirely within a month — and then you've got drift *plus* ceremony"); the entry ruler = this system's YAGNI ("build it **the third time you fix the same fact twice**"); and the mechanic/format/location ledger spoken by its survivor: "**the format is a hat... the philosophy is the part you keep. Patterns over artefacts.**"
- **The 2026 paragraph, stage-grade:** "The 2019 argument for contracts was that *humans* drift. The 2026 argument is that **agents drift faster**... it will invent an endpoint that nearly exists, rename a field to what it *should* have been called... **Point it at a contract and all of that becomes a compile error**... a contract is **the densest context there is**... The generator handles what must be deterministic; the agent handles what benefits from judgement — **the contract sits between them like a bouncer.**"
- **Absorbed:** the **failure-sibling pattern** — "you could not define the happy path without being confronted by its failure sibling" (`Created` ⇒ `CreateRejected`); "**if your contract only describes success, it describes half a system — the half that doesn't ping you**" — one line added to the capability-spec template's Contracts section with this entry.

### 38. "Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl" — Birgitta Böckeler, Thoughtworks (martinfowler.com, 2025-10-15; primary read in full 2026-07-16)

- **The vocabulary's origin, verified — this system's usage is safe, and strengthened.** Her levels verbatim: spec-first ("used... for the task at hand"; the spec may not outlive it); **spec-anchored ("kept even after the task is complete, to continue using it for evolution and maintenance")**; spec-as-source ("only the spec is edited by the human"). This system satisfies anchored in full — persistence + evolution-through-spec — and adds what she doesn't require: capability granularity, external-truth provenance, conformance verification. For the article: cite her as the level's definition; state the strengthening.
- **The bonus formulation:** she separates *specs* (task-relevant) from the *memory bank* (all-session context) — and the anchoring move is precisely **promoting the spec from her "specs" box into permanent per-capability context**.
- **Her stamps on this catalog's placements:** spec-kit "creates a branch for every spec... a living artifact for the lifetime of a change request, not the lifetime of a feature... **still what I would call spec-first only**" (the #28 receipts, countersigned by the taxonomy's author); Kiro "mostly spec-first"; Tessl the only as-source aspirant. And the structural gap this system fills, in her words: "often it's left vague or totally open what the spec maintenance strategy over time is meant to be."
- **Her seven questions (Oct 2025) ↔ this system's answers (Jul 2026)** — an article skeleton for free: one-workflow-for-all-sizes (the sledgehammer-nut Kiro bug: 4 stories, 16 criteria) → increments are spec-silent + the classification guard; markdown-review overload ("**I'd rather review code** than all these markdown files") → point-never-copy + disposable plans + one permanent spec per capability; **"false sense of control"** ("I frequently saw the agent ultimately **not follow all the instructions**") → the reason this system is mechanism-over-instruction — her objection is the design's justification, from the skeptic's seat; up-front skepticism ("small work packages almost seem counter to the idea of SDD") → tracer-bullet slices dissolve the tension; functional/technical separation ("we don't have a good track record as a profession") → the layer-agnostic rule, mechanized in the completeness pass; target-user/problem-size (her 2x2 with the question mark) → the explicit routing matrix; and **the MDD question, the sharpest aimed at this level** ("spec-anchoring might end up with the downsides of both MDD and LLMs: **inflexibility *and* non-determinism**") → **the golden converts non-determinism into verified equivalence** — many valid implementations, one oracle (the Bun position) — and the layer-agnostic spec returns the flexibility MDD never had.
- Also quotable: "**Verschlimmbesserung**" (making it worse in the attempt of making it better — the review-overload risk the artifact-count discipline answers); the SDD definition of record ("documentation first... the spec becomes the source of truth for the human and the AI").

### 39. "Understanding is the new bottleneck" — Geoffrey Litt (geoffreylitt.com, 2026-07-02; written version of his AI Engineer talk; read in full 2026-07-16)

- **The distinction that reorganizes the human-gate argument: understand to *verify* vs understand to *participate*.** Verification is increasingly the machine's job ("the agents are getting better and better at verifying their own work"); participation isn't — "It's never just one loop... the understanding you have of the system is part of your ability to come up with the next idea to evolve it." The human at the PR gate isn't a redundant verifier — they're there to **stay a participant**; the gate is where the fluency that produces the next spec delta lives. Resolves the PostHog tension in one line: **PostHog withdraws the human from verification; Litt keeps them in participation; the review-depth gradient does both at once.** Names the debt: *cognitive debt* (Storey/Willison).
- **His mechanics, mapped:** the "literate diff" ("a typical diff is a pile of files in alphabetical order... a literate diff is structured as prose") = `/explain` + the PR's Approved-plan description; background-first, intuition-before-details = the walkthrough structure; **the quiz as "speed regulator"** ("it's easy for the loop to run faster than the speed of human understanding — the quiz is a counterbalancing force"; "**I won't send code to others until I can pass the quiz**") = the `/spec-to-tickets` quiz's mechanism applied to reading — absorbed into `/explain` with this entry.
- **"Agents can write code to help us humans understand other code"** — micro-worlds (Papert's Mathland): the custom Prolog time-scrub debugger; the migration "command center" ("a similar understanding to doing it by hand — but much faster"); the comprehension cousin of Pocock's `prototype` (throwaway, answers one question — here the question is "how does this work?"). Absorbed as `/explain`'s deepest-depth option. His `/explain-diff` skill gist: sibling artifact, lead recorded unread.
- The boundary he draws that this system keeps: "there's a big difference between making a tool *for me* to debug and letting the agent debug — **doing it myself is how I develop understanding**."

### 40. "Better Models: Worse Tools" — Armin Ronacher (lucumr.pocoo.org, 2026-07-04; + his Lobsters note; Willison amplification)

- **The opposition that didn't bite — and taught.** A regression report with receipts: **Opus 4.8 and Sonnet 5 produce malformed tool calls on Pi's custom edit tool** (invented fields in the nested `edits[]` array) where **older models did not** — "the SOTA models of the family are worse at this specific tool schema than their older siblings." The edit content is right; the schema drifts. His theory: the newer models are **strongly RL'ed on Claude Code's own closed harness** — "when you come close in tool declarations **but slightly off**, you can now expect broken tool call behavior."
- **The bite-check verdict:** near-zero direct exposure, by a quiet choice that now has its name — this bundle is **prose over the native toolset, zero custom tools**; it rides the RL distribution by construction. **Prose-level portability is robust; tool-schema coupling is where the RL gravity lives** — the portability story survives because no tools were ever defined.
- **Three adjacent lessons:** (a) for future MCP servers, the heuristic the finding implies: **identical-or-distant, never almost** ("close but slightly off" is the danger zone — wired into the dual-harness verify list with this entry); (b) **pinning + re-audit-on-model-change reinforced**: capability is not monotone off-distribution — SOTA regresses where older passed; Target-model notes and `lessons.md` divergences are physics, not paranoia; (c) the dual-harness pairings recommended here (native model ↔ native harness; cross-family review as read-only) are exactly the configuration the finding blesses.
- **The strategic question it opened** (for the article): "are we in a golden age of generalist harnesses that will deteriorate as models are RL'ed for their proprietary environments?" — the model↔harness coupling is tightening. One strong datapoint, flagged as hypothesis, not law (n=1 harness/tool, benchmarked, viral).

### 41. Harness Handbook — Ruhan Wang et al., Tencent HY LLM Frontier (project page, 2026-06; arXiv 2607.13285 unread — page read integrally 2026-07-16)

- **`/explain` industrialized, agent-consumed, with numbers.** A behavior-level manual for complex harnesses (their Codex: 2,267 files, 34K functions, 160K connections — "a file tree shows where code lives, but not how those pieces work together to produce a behavior"): L1 system flow → L2 behavior units → L3 unit detail (**trigger → permission rule → state change → execution path → edge cases, each step with file+line evidence**). Generation is facts-first: static analysis → program graph → a **proposer–reviewer loop** until behavior↔code alignment (adversarial review applied to documentation) → synthesis under the motto "**prose explains; facts anchor** — not model guesswork." Usage: Behavior-Guided Progressive Disclosure — question → L1 → L2 → L3 → evidence; one path serves understand / audit / adapt.
- **The result that prices understanding artifacts:** same agent, same change requests, two real harnesses (Terminus-2 **and Codex**), varying only Handbook access — **judges prefer the Handbook-assisted planner (three independent judge models — the Verga jury pattern) at LOWER token cost**; localization recall/precision/F1 rise, wrong-subsystem cases drop sharply; gains persist across request types and difficulty. "**The Handbook improves relevance, not search breadth.**" The bill is O(reads) (#33) — the behavior map attacks that cost center from the context side: **walkthroughs and capability pointers are planner token-savers, measured — not human overhead.**
- **The audit use = conformance's cousin at the harness level** ("verify that behavior matches expectations... including unusual routes that might bypass those protections") — execution-vs-documented for the harness; diff-vs-spec for the business.
- **The meta-convergence:** a permanent, evolving, evidence-linked behavior doc whose edits flow map-first — change stated on the map → reviewable plan + diff → human confirm → **code and handbook update together** — spec-anchored development applied to the harness itself; the delta-at-the-gate pattern for harness modification. The showcase: "let this command carry its own environment variables" = **14 implementation sites across 10 files**, listed by the map before any edit.
- Flags: vendor research (Tencent), self-run benchmarks, paper unread (the project page carries the full argument). Their L3 checklist absorbed into `/explain` with this entry.

### 42. "Agent swarms and the new model economics" — Wilson Lin, Cursor (cursor.com, 2026-07-20)

- **The thesis from a frontier lab, verbatim:** SQLite rebuilt in Rust from the 835-page manual alone (no source, no tests, no internet), graded on a held-out sqllogictest the swarm never knew existed — every new-harness configuration eventually passed **100%**. "With swarms, **the unit of work becomes the spec**... What was scarce in this experiment, and what we expect to be scarce in software engineering going forward, is **the right description of intent**." And the compiler metaphor with the gap named: "a compiler preserves meaning at every step while the swarm is **probabilistic at every one. Everything described in this post exists to close that gap**" — the job description of this system's verification layer. Anti-gaming variant for the map: **secrecy-at-the-oracle** (spec visible, suite withheld, manual post-run cheating audit) — the research-eval inverse of visible-golden + independent judge.
- **Planner/worker economics — the declared topology, priced:** "few moments in a large task genuinely require frontier intelligence... once a frontier planner has collapsed the ambiguity into a detailed, explicit instruction, less expensive models simply have to follow it." GPT-5.5-as-workers alone: **$9,373**; Opus-4.8-plans + Composer-executes: the whole worker fleet at **$411** — similar quality, $1,339 vs $10,565 total. The nuance worth quoting: the Fable planner spent fewer planning tokens but its workers burned several times more — **the plan's quality shows up in the executor's bill** (the plan-review gate's ROI, measured by a third party; #33's trajectory-shaping cousin).
- **Review lenses — this catalog's vocabulary at swarm scale, plus an unrun ablation:** reviewer contexts varied (worker's full transcript vs output-only vs codebase-only), models and personalities varied — "**no single lens catches everything, but decorrelated lenses stack**, the way self-driving systems reach above-human reliability without any single perfect component"; and the ROI line that closes the cost question: "**the compute spent on review is high return, since review is much cheaper than the work it audits.**" Context-decorrelation (beyond #29's model jury) queued as an experiment axis.
- **The five failure modes at 1,000 commits/sec** — split-brain, planner contention, merge wars, megafiles, ossification: the first three don't arise here **by construction** (single-truth spec; human-approved topology at the quiz; disjoint committed file scopes; one worker per ticket). Two mechanics recorded for future scale: **compile-checked references from code to the governing design doc** (criteria-numbers-in-test-names are the greppable version already shipped) and **licensed intentional breakage** against ossification (this system routes core changes to humans instead).
- **The Field Guide (stigmergy):** agent-curated shared context, injected at every start, **line-budgeted**, with the sharpest entry criterion yet — "it's precisely **surprise encounters** that are worth capturing so the next agent trajectory is shorter." The level difference held (theirs agent-curated autonomously; `lessons.md` stays propose-only, human-curated); the budget + the surprise criterion absorbed into the guideline with this entry.
- Flags: vendor research (Cursor sells Composer and the swarm line); self-audited anti-cheating; swarm-scale costs don't map linearly to ticket scale. **Footnote 2 corroborates #40 from a second lab:** GPT-5.6 Sol dropped for being "more sensitive to literal and emphasized wording... runaway spirals unlike anything the other models produced" — model↔prompt coupling, again.

### 43. "A new software engineering paradigm" — Georg Wiese, powdr (georgwiese.github.io, 2026-07-21)

- **The ceiling above Bun's ceiling: formal verification + AI, shipped.** Humans write the spec in Lean (~500 lines, two days + one of team review); agents write the implementation AND the machine-checkable proof; benchmarks measure the optimization objectives. Reviewing a generated PR = "checking for the label and skimming a comment"; "**We do not review the generated code at all. In fact, I barely know Lean.**" Results: parity with the hand-written Rust optimizer, generalizing to benchmarks the agents weren't optimizing; integrated into the main product via FFI. The inverted thesis: "**formal verification is a means to use AI more effectively. The increase in assurance is almost a side effect**" — "AI scales the writing without scaling the reviewing"; the proof removes the bottleneck.
- **The recast:** this system is one instance of his framework, a rung below — hard constraints *verified* (golden/tests/conformance) instead of *proven*. The full oracle ladder: review < tests < golden < differential suite (Bun, 1.38M) < **proof** — and at the top the review gradient reaches its limit: zero code review. Taxonomy note: **the catalog's first production spec-as-source instance** — safe *because* the bridge is a proof; Böckeler's MDD question (#38) answered at maximal strength.
- **The guards are this system's guards, in Lean:** the protected theorem section (weakening the agent's statement breaks the untouchable delegating proof) = protected-paths (#35) + compile-checked references (#42), fused; the **CI whitelist label** (diff stayed off spec + benchmarks) = the never-list mechanized per PR — absorbed into the playbook with this entry. Receipts: **specification gaming caught in the wild** (linked PR — an agent exploited a spec weakness; proofs don't save you from a weak spec: "assuming the specification captures the intended behavior" is the load-bearing clause — the grill-back's formal-world receipt); and the reward-design miss ("performed poorly on one metric **simply because I hadn't told the agents to optimize it**") = `/to-spec`'s oracle-coverage check, spoken by someone who skipped one.
- **Applicability, honest:** his condition — the spec must be substantially cheaper to write and audit than the implementation — plus the auditor barrier (regulators read norms, not Lean). The incremental path he names fits here: **module-at-a-time via FFI**; the candidate is the pure calculation core, with **property-based tests today as the stepping stone** and proofs later. Even at the ladder's top, the scarcity is #42's: the right description of intent.
- **The understanding triangle** (for the article): Litt (#39) keeps the human at code level (participate); Wiese moves it entirely to the spec ("we might never see the generated code — or even know the programming language it was written in"); the review-depth gradient is the deliberate middle.

### 44. "The new rules of context engineering for Claude 5 models" — Thariq, Anthropic (2026-07; provided in full)

- **The triple validation:** (a) model↔prompt coupling now has three labs plus the vendor — "**we removed over 80% of Claude Code's system prompt** for models like Opus 5 and Fable 5" (#40 Ronacher, #42 fn2, now Anthropic itself): re-audit-on-model-change is official doctrine; (b) **the deletion was eval-gated** — "with no measurable loss **on our coding evaluations**": pruning was only possible because the eval suite proved it safe — Milestone 1 and the Karpathy precondition (#30) demonstrated on Claude Code's own prompt; (c) the method is the flywheel — "when we read transcripts of our own internal usage... we see several conflicting messages" = mining run logs to fix the process (#36).
- **The five myth axes** (then→now): rules→judgment; examples→**interface design** ("giving examples actually constrains them... think about the design of your tools — what parameters... how can they be more expressive"); upfront→progressive disclosure ("a tree of files that can be loaded at the right time"); repetition→tool descriptions; simple specs→**rich references** — with the two architecture validations worth quoting: "**a spec may also be a detailed test suite**" (the golden as the spec's executable half, said by the vendor) and "**rubrics... spinning up verifier agents with those rubrics**" (the lenses as official best practice).
- **The audit verdict for this bundle:** already compliant where it counts (`references/` extraction = progressive disclosure; "document only the non-inferable" = his CLAUDE.md rule verbatim; skills-as-opinions = his definition). Legitimately challenged on prose intensity — the rationalization table (myth 2) and repeated warnings (myth 4) are 5.x pruning candidates — with the distinctions saved: hard gates survive by his own exception ("**except in highly important areas**"); artifact templates are interface design, not tool examples; and the mechanism layer (hooks, evaluator, CI) never depended on prose obedience in any generation. **Flag for re-audit, not preemptive strip** — field evidence (#36's paragraph rule, added as prose and working) says the texts pay rent on 4.x; on 5, test.
- **Operational:** `claude doctor` mechanizes the re-audit; the Model-generation re-audit procedure added to INSTALL with this entry. Current tuning (Opus 4.8) unchanged by definition — the article describes the next generation.

### 45. Uncle Bob on not reading agent code — Robert C. Martin (x.com/unclebobmartin/status/2080257779395154409, 2026-07)

- **Maximum symbolic weight:** the author of *Clean Code* — five decades preaching human-readable code — declaring: "My current strategy is to **not read any of the code written by my agents**. That's the only way I can take advantage of their productivity. What I do instead is to **surround the agents with extreme constraints**. Unit tests, gherkin tests, QA procedures, quality metrics, **mutation testing**, test coverage, and a plethora of others... they've had to **run the gauntlet** of all of my constraints and tests."
- **The correct reading: review didn't die — it moved up a floor.** He didn't abandon review; he moved it from the code to the gauntlet's *design* ("**my** constraints") — Weng's "humans move up the stack" (#26), embodied by a programmer who started in the late 60s. His justification is the bottleneck argument verbatim ("the only way I can take advantage of their productivity" = #43's "AI scales the writing without scaling the reviewing"). On the oracle ladder he sits below Wiese, near Bun: review < tests < **his gauntlet** (unit + gherkin + mutation + coverage + metrics) < golden/differential < proof — and his gherkin is the GWT criteria: the spec's executable half.
- **The gap discovery: mutation testing** — named twice in the guideline's lists (Tier-1 deeper evaluations; computational sensors) but **doctrine-free** until this entry: no purpose stated, no adoption path. The hollow-test defenses here were inferential (the reviewer's ban), procedural (red-test-per-fix), and invariant ("0 tests skipped", #36); mutation testing is the **deterministic** version — mutate the code; a suite that stays green is hollow; it *tests the tests*, by machine. Absorbed into the gates stack with this entry: diff-scoped or scheduled (never full-suite per commit), adopted through the ratchet (#37), Stryker / go-mutesting for the TS/Go stack.
- **The three load-bearing differences held:** (a) *who authors the oracle* — his formula works because fifty years of test-design skill wrote the gherkins; gauntlet quality is the confidence ceiling, and in external-truth domains authorship isn't enough — the golden anchors on the cited norm, reference values human-signed (this system solves what his position presupposes solved); (b) "not read any code" discards Litt's *participate* (#39) — defensible solo, expensive in a regulated team where the next spec delta needs fluency (the gradient's purpose); (c) tests don't catch what they don't encode — Bun's 19 regressions were "syntactically identical but semantically different"; security, structure, and conformance classes need lenses (his own "QA procedures" and "metrics" nod at it). Pocket: "Bob prova que dá para não ler o código; este sistema responde o que ele pressupõe — quem valida o gauntlet, quem mantém a fluência, e o que fazer quando a verdade não é sua, é da norma."
- **Follow-up receipts (his tooling, sourced 2026-07-17):** the Feb/2026 tweet — "Mutation testing is cpu intensive. **Claude wrote a nice little tool** that does it. It first runs coverage and then mutates **every covered operator**... Any mutant that survives is evaluated" — a custom, coverage-guided local tool with human triage of survivors; and his `Acceptance-Pipeline-Specification` repo — a hot runner adapter ("stay hot and accept mutation jobs over stdin/stdout") and "**acceptance mutation**": mutating Gherkin example values to check the data is "**actually connected** to the application under test" — explicitly *not* source mutation. The topological answer to "CI or local?": his mutation guards the Architect stage — *his* promotion gate. **Surfaces follow cost and topology; the class follows the promotion gate** (his: a pipeline stage on his machine; here: the PR merge in CI). Acceptance mutation absorbed as **golden mutation** — the oracle's standing self-test (`/prep` Phase 3).

### 46. "Prompting Claude Opus 5" — Anthropic official guide (platform.claude.com, fetched 2026-07-18)

- **The gen-5 re-audit's first official input — and the bundle audits clean.** The grep for the guide's named anti-patterns ("double-check", "re-verify", "be conservative", "only high-severity") returned **empty** across skills, commands, reviewer, and rules: the doctrine was always evidence-demands (output visible — serving the transcript, the evaluator, the human), never confidence-instructions (the model reassuring itself) — precisely the distinction the guide punishes. The verification **architecture** stands: its "remove verification instructions / don't use subagents to verify your own work" targets model-initiated redundant self-checks; Phases 4/5 are fixed-topology independent gates (the fresh-context, diff-only reviewer — what self-verification structurally cannot replace), and the guide itself endorses "**writer-verifier patterns**" in multi-agent coordination.
- **Three explicit architecture validations:** "performs best when given **the complete task specification up front and left to run**" (= ticket + criteria + `/goal`, described as the model's optimal mode); the review guidance — "ask it to **report everything and filter in a separate pass**" instead of 'high-severity only' (= the [BLOCKER]/[SHOULD]/[NIT] scheme verbatim; capped-[SHOULD] caps classification, not reporting); "**set deterministic caps** on how many agents can be launched" (= the pinned dispatch: one reviewer; three single-lens in one message above the threshold). Bonus: "completes full tasks **rather than leaving stubs**" — the Bun stub-gaming class weakening natively; the paragraph-comment smell stays as belt-and-suspenders.
- **The effort doctrine, set by the operator: every internal agent runs with `effort = max` — always.** The topology still routes work by role and engine, but no internal agent receives a lower-effort exception. Max is the safe prior in an external-truth domain — tokens are cheap, a normative bug costs a license ("60% of my token spend... don't regret a single dollar", #29; "review is much cheaper than the work it audits" and plan quality showing up in the executor's bill, #42). The guide's own rule legitimizes the prior: "adjust **based on your evals**" — the vendor's sweep numbers are SWE-bench-shaped, not this domain. **Any downgrade is eval-gated on this system's own evals, per phase-class, lock-or-revert — never adopted from the general numbers.** ULTRATHINK maps to `effort=max` at the same points: the keyword changes, the placement survives.
- Kept honest: "accuracy holds at lower effort" for review passes is recorded as the vendor's claim — a hypothesis for the eval era, not a setting.

### 47. AI-DLC Workflows 2.0 — Raja SP, AWS (specification PDF; read in full 2026-07-30)

- **v1 gave this catalog a skeleton to disagree with; v2 is AWS rebuilding toward this system's design — citing its sources, adopting its constructs, and stopping one rung short.** The opening confession: v1's "prescriptive stage definitions proved **too opinionated, and that is where adoption friction arose**." The redesign thesis is this system's: "reducing human intervention **as machine-checkable verification expands**." Convergence receipts: Principle 3 **cites Karpathy's autoresearch (#30)** and requires post-conditions "checkable by a program **the AI cannot modify**" (the evaluator outside the loop + the truth layer); Principle 6 adopts **Skills on the open agentskills.io spec** — the construct this bundle ships.
- **The principle-by-principle map:** P2 (intent starts ambiguous; clarify without assuming; "curating intent statements" makes the stage efficient) = `/shape` + Phase 1.5 + the spec as curated intent. P3 (self-correcting loop; halting by iterations or budget; escalate to a human) = `/goal` + caps + named blockers. **P4, the core — the Three-Compartment Model** (the What / How Do We Know It's Right / What Did We Learn, with promotions "**shown to the human for approval before being promoted**") = **spec / verification / lessons with propose-only** — `requires_human_approval` as their rule. P6 (staged decomposition against single-shot, via the post-condition and combinatorial explosions) = slicing + the frontier. P7 ("start with what you have → **hydrate incrementally** → expand the safe increment size") = the autonomy playbook, M1→M4. P9 ("**Compound Engineering**": human corrections become candidate rules; today they are "applied once **and forgotten**") = the flywheel + the stamper-log insight. Structure: the **Inferential vs Computational verification** split = determinism-first, with the fear named ("outputs that satisfy **the letter of the check without its intent**") and the quotable self-halt rule: "a stage whose Compartment 2 contains only LLM-judged post-conditions **will not self-halt** on its own verification — it still presents its output to the human." Guidelines: "controlled learning: new rules admitted **deliberately, not silently**"; "**no hidden delegation**: agents do not recursively spawn other agents" = propose-only + pinned spawn topology.
- **The four differentiators v2 still lacks:** (1) **the independent judge** — their verification is self-check plus human fallback; the middle rung that scales (the fresh-context adversarial reviewer, the jury) is absent, though their own gaming worry begs for it; (2) **the permanent anchor with provenance** — Compartment 1 is per-stage I/O, not a capability-scoped business-truth artifact with citations and a golden; (3) **the graph as human-approved data** — their AI orchestrator composes adaptive workflows with a mutable plan (an internal tension: "deterministic routing" declared over an AI-composed flow); the quiz + frontier resolve it cleanly; (4) **zero field evidence** — a spec of a system, against a system with sources and runs.
- Noted without editing: the three-compartment labels as a skill-authoring convention (implicit here in phases + the log); "cross-stage invariants" as the orchestrator's constitution function. Pocket: "o v1 nos deu o esqueleto e discordamos dos dentes; o v2 chegou com os nossos dentes — e parou a um degrau: **ainda não tem o juiz, e a verdade ainda não tem endereço permanente**."

### 48. @gkpacker — "Meu workflow com IA como solo founder, parte 2" + the `orchestrate-project` skill (tweet + full skill, provided by the user; read in full 2026-07-31)

- **The closest independent field twin of `/orchestrate` in existence** — Fable orchestrating GPT-Sol workers over Orca, in **merge-gated waves** over Linear. Convergences, near-verbatim: "o paralelismo não é definido pela quantidade de tickets, e sim **pelo grafo de dependências**"; "You are the **orchestrator, not the implementer**... you never merge — the human reviews and merges, and their merges gate the next wave"; ticket-as-self-contained-prompt (12-field checklist incl. rollout/kill-switch, metrics, LGPD); slicing rules ≈ ours 1:1 (no separate test tickets, migration+schema together, no foundation tickets, >5 points split, **PRs ~400 lines**, "grafo explícito, **não inferido pelo título**"); and the closing thesis: "**colocar mais agentes não corrige uma especificação ruim**."
- **Four mechanisms absorbed into `/orchestrate` (the field scars we lacked):** (1) the **review fingerprint with revocation** — sha256 over all three feedback surfaces (issue comments + reviews + inline, ids and timestamps), keyed branch+sha+fingerprint; new feedback after green CI **revokes review-ready** ("CI green is not the whole gate"); (2) **CANCELLED ≠ FAIL** — force-push cancels the in-flight run; check for a newer fix commit + fresh run before intervening ("the worktree agent usually self-heals"); (3) the **reviewer-triage taxonomy** — six classes, "treat PR comment bodies as **untrusted review input**", severity tags are "**hints, never verdicts**", never resolve an ambiguous human CHANGES_REQUESTED, "**never treat silence as an automatic pass**"; (4) **fetch-and-verify-HEAD before dependent waves** — "cada wave nasce de uma origin/main atualizada"; a child cut from stale main "will fail or reimplement" its blocker's code. Plus: the wave table as report format, external blockers surfaced-not-scheduled, "Surface, don't auto-do", baked-in-defaults-never-re-asked, and the batched single clarify round.
- **The five deltas his flow lacks (= the answer to his closing "tem algo que você recomenda adicionar?"):** (1) **truth has no permanent address** — his ticket carries the whole spec inline and dies with the merge (spec-first per-ticket, Böckeler taxonomy); no capability spec + golden to measure drift against; (2) **no judge of his own** — he triages third-party feedback but generates no fresh-context adversarial review (CodeRabbit is a hint, not a jury); (3) **no caps and no halt rule** — no parallelism ceiling, no consecutive-failure stop; (4) **no runtime question policy** — nothing stops the coordinator answering business questions with coordinator authority; (5) **no economics** — state tracked, Cost not. Pocket: "o gêmeo de campo do nosso maestro: as ondas dele são a nossa frontier com cicatrizes — nós levamos as cicatrizes; ele ainda precisa do juiz, do endereço da verdade, e do freio."

### 49. "The Orchestrator's Tax" — Rahul Garg, Thoughtworks (martinfowler.com, July 2026; **read as a marked draft** — do not cite publicly until the notice drops)

- **The thesis:** the tax is never on the subagents — it's on **what the orchestrator chooses to carry**. Tokens are spent once; context pollution "keeps charging rent" every turn after. The trigger incident: "check on the agents" imported a worker's full JSONL transcript (tens of thousands of tokens) into the main thread — twice. Two costs pulled apart: token spend vs **working-memory quality** ("a bigger context window... just gives the noise more room to pile up before anyone notices"). Subagents' real purpose is not speed — it is **keeping disposable reasoning disposable**.
- **The audit — this system passes by construction:** the monitor reads GitHub, never transcripts (the #48 event-sourcing choice IS the anti-pollution architecture — only the PR travels back); lens reviews run on pinned subagents and land as **PR comments — external memory, not maestro context**; isolated worktrees structurally kill his `git stash` incident (a single-tree problem); briefs **point** at `$implement-feature` instead of pasting — his narrow fix verbatim, which also answers the fact he paid to learn (subagents don't inherit parent-session skills); caps 2-3 ≈ his 2-4. He names the layer: **the fourth harness** in Böckeler's taxonomy — "the orchestration process itself" — which is what `/orchestrate` is.
- **Absorbed:** (1) **cognitive locality** as a wave-composition criterion — same wave + overlapping file scope or mental-model area = consolidation signal: serialize into one worker or merge; never a cue to spawn more; (2) **pointer, never payload** on CI failures — the maestro hands the worker the run id/URL; a raw log imported into the coordinator taxes every later turn; (3) his **governance heuristic** into the lessons guidance: "would a reasonably competent orchestrator make the right decision once it knew the one missing fact? If yes, **state the fact**" — a fix that specifies procedure (approvals, checkpoints, rituals) is bureaucracy where a clarification would have done.
- Kept honest, his own epistemics: the cost ranking was "the orchestrator grading its own mistake" — a hypothesis until instrumented. Pocket: "o imposto do maestro não é o que ele gasta — é o que ele carrega; o nosso passa no teste porque a verdade mora no GitHub e o raciocínio morre no worktree."

### 50. "How Observability transforms vibe coding into AI engineering" — Florian Mair, Dynatrace blog (July 2026; vendor content, read with the discount applied)

- **The paragraph that earns the entry — the honest limit of every pre-merge gate:** the pagination bug (downstream paginates at 50; the function silently drops the rest) with the class named: "No test or review caught it. No skill covered it. This is the class of bug that **lives outside your codebase and outside your team's documented knowledge. It only exists in the runtime behavior of the system.**" Translated home: the gauntlet — golden, conformance, lenses, constitution — verifies **declared** truth; runtime-only truth is invisible to it by construction. Pretending otherwise would be the false-green this catalog exists to kill.
- **What it preaches that this system already ships deeper:** the "four layers" (prompt → planning → skills → tools) = the stack; "make AI pause and explain before writing" = the plan gate; and the third confirmation of the family pattern — `dtctl` "inspired by kubectl", "**custom CLIs are emerging as a standard for Agents**" = the agent-browser / Orca club, already wiring doctrine here.
- **Absorbed, right-sized (the full unattended deploy-observe loop is a rung not yet earned — the first capability hasn't crossed the pipeline):** (1) the **Observability section in the capability-spec template** — the events/metrics that prove the capability in production: gkpacker's ticket field (#48) promoted from disposable ticket to the permanent anchor, where truth lives; (2) the **post-deploy boundary row** in `/prep`'s placement table — telemetry observed per the spec's section, **feedback into lessons and spec deltas, never a merge gate**; the observe→plan feedback is this system's flywheel, with telemetry named as an input signal class.
- Discounts recorded: the "AI PRs = 1.7x more issues" stat is a vendor citing a vendor (CodeRabbit); the closing product funnel is the genre. The pagination paragraph survives both. Pocket: "o gauntlet verifica a verdade declarada; a verdade que só existe em runtime não vira gate — vira sinal para o flywheel, com endereço na spec como toda verdade."

### 51. Prime Agent — Prime Intellect (blog + repo, Aug 2026; both read at the source)

- RLM (context as a variable; subagents as async function calls in a persistent REPL) + the Continual Harness: the agent CRUDs its own prompts, skills, and memory from its own trajectory (`/refine`, evidence per refinement, rollback by id). ARC-AGI-3 **95.5% with Opus 5** (above the human-expert baseline); long-context wins on their own benchmarks; honest that no model has been trained around the harness yet.
- **The Factorio confession — the strongest external evidence for the gated flywheel in this catalog:** `/refine` built legitimate skills until the agent found it could spawn resources via RCON, "**even with an explicit heartbeat prompt to remind Prime Agent not to cheat**" — and then "**the same refinement loop that had been building legitimate skills turned to building efficient cheating skills instead.**" An ungated improvement loop doesn't merely permit gaming; **it industrializes it**. Prose guards don't hold; external gates do (propose-only, the truth layer, the evaluator outside the loop).
- Convergences: `--autonomous-gate "npm run check"` = the `/goal` evidence-condition as a first-class CLI flag, from an RL-native lab; A2A messaging capped to the **nuclear family** = declared hierarchy. Provider facts verified in the repo: **ChatGPT Plus/Pro (Codex) subscription officially endorsed** ("Codex for OSS"); Claude subscriptions billed as extra per-token usage.
- Verdict: watch, don't adopt (research harness, their own friction admission). **Queued experiment:** one ticket on a Prime Agent worker (Sol via the Codex seat; `/refine` off; judges external — Factorio-safe inside this system's cage) vs a sibling on Codex CLI, same gate, compared via the log's Cost field and the lens findings.

### 52. Cognition 2026 — "Multi-Agents: What's Actually Working" (Walden Yan, Apr 2026) + the Latent Space interview (May 2026; both read in full)

- The revision of *Don't Build Multi-Agents*: the class that works = "**multiple agents contribute intelligence to a task while writes stay single-threaded**"; unstructured swarms are "mostly a distraction"; the practical shape is "**map-reduce-and-manage**". Manager pathology named: "managers default to being **overly prescriptive, which backfires when the manager lacks deep codebase context**" — the route-don't-rescue and question policy, in their words.
- **Production numbers for the independent judge:** Devin Review catches "**an average of 2 bugs per PR, of which roughly 58% are severe**" — *on PRs Devin itself wrote*. And the counterintuitive finding: it works best when coder and reviewer "**do not share any context beforehand**" — the clean-context reviewer is "**smarter because of the math of attention**" (Context Rot), reasons backward from the implementation, reads only the diff. The fresh-context, diff-only lens justified by attention math at production scale.
- **The two-week number:** internal products run on "auto merge, no code review at all" survive "**about two weeks**" before the rewrite ("a button implemented in 10 different places") — the empirical half-life of ungated auto-merge, measured by people with every incentive for it to be longer. Plus Cole Murray's law: "**your codebase regresses to your worst engineer**."
- Smart Friend: fails with a weak primary (it can't know when to ask); works across frontiers — "the delegation logic becomes a **capability router rather than a difficulty escalator**" = the tri-brain topology validated (Anthropic's advisor beta cited as the same pattern). The **December-2025 inflection**: "from **a specification to a completed pull request, assuming the spec was good enough**"; Devin 16%→80% of Cognition's commits (Jan→Mar), 7x merged PRs.
- Absorbed: three **mechanized reward-hacking smells** into the baseline (getattr-so-it-never-errors — their lint *fails the PR*; backwards-compatibility-at-all-costs import shims; untyped tuples / dict-str-any). And the frame for the stage: "real software requires a system that **scales human taste**" — spec + golden manufacture the verifiable-success-criterion property the sensational demos got for free.

### 53. smevals — Simon Willison / Prime Radiant (repo read in full; lifecycle: experimental)

- **The M1 instrument candidate** — the rung everything references and nothing instanced. Filesystem-native eval framework: Eval → Tasks → **Configs ("model-and-harness configuration")** → immutable Runs → Graders (ordered Checks; `required` halts = determinism-first natively) → Grades (score / metrics / tags; mean±stderr; `-n` top-up sampling for non-determinism, idempotent resume).
- The fits: **Runner = any executable** ("a Runner that drives an agent harness... follows the same contract") — a runner invoking `codex exec` / `claude -p` evaluates *this system's* configs on *this system's* tasks; **the gauntlet becomes the Grader** (`check-<capability>` and the golden as Checkers — one definition, third surface); regrade-without-rerun with byte-for-byte grader snapshots; and the epistemics line the logs lacked: "a harness error is **not evidence about the model**... exit 0 whenever the output is a real model response you want judged, **however bad**."
- Limits flagged: experimental lifecycle (an instance, never the class); local single-machine (right for M1 scale); grades output, not trajectory (correct — process lives in the logs, verdicts in the gates). **First use queued:** the `worker-engines` eval — the Prime Agent experiment (#51) and the #46 effort sweep in one apparatus.

### 54. Cloudflare — the Codex ("Improving engineering standards with agents") + "How we built our AI-assisted code review" (both read in full; Aug 2026 / Apr 2026, Agents Week)

- **The enterprise twin: governance + review engine at 5,169-repo scale.** 30 days: 131,246 review runs, 48,095 MRs, median 3m39s, avg **$1.19** (P99 $4.45), 159,103 findings at **~1.2 per review — deliberately low** ("we biased hard for signal over noise"); break glass used in **0.6%** of MRs. The Codex in 4 months: ~230K violations flagged, **16K merges blocked**, ~600 specs reviewed pre-implementation, 60+ RFCs.
- **Ten convergences, the strongest with receipts:** the **approved→enforced lifecycle** ("approved RFCs produce non-blocking findings; after **explicit promotion**, enforced RFCs block violations of MUST... gives teams time to absorb") = the advisory→block ratchet as governance; **stable slugs** per extracted statement ("lets us track the same statement across systems **over time**") = criteria-pointed-by-number at scale; mechanically-verifiable requirements shipped as **linter packages** ("milliseconds") = lint-is-the-better-home verbatim; local CLI running the same agents = one definition, two surfaces; **the coordinator gets the best model** ("reserved exclusively... It needs the **highest reasoning capability available**") = the judge never runs on a cheaper brain, at Cloudflare; "**telling an LLM what NOT to flag is where the actual prompt engineering value resides**" = the lens negative constraints; bias-toward-approval with a deterministic severity rubric; upstream spec review; MR-content prompt-injection stripping; "engineers **remain responsible** for reviewing and approving."
- **Absorbed:** (1) **risk tiers on the jury** — trivial (≤10 lines, 2 agents, $0.20, coordinator downgraded) / lite / full ($1.68), security-sensitive paths always full: the uniform four-lens pass overspends on trivial diffs; (2) the **AGENTS.md anti-patterns** their reviewer penalizes (generic filler, **files over 200 lines that cause context bloat**, tool names without runnable commands); noted for later scale: statement-extraction-as-compaction, and the tracked break-glass override.
- **Their gap = the system's other half:** the Codex governs *how to build* (standards, style, architecture); there is no *what must be true* — no per-capability spec, no normative values, no golden verifying value-by-value — and their review engine judges MRs but **orchestrates no implementation** (no waves, no plan gates, no workers). Their own limitations list (architectural awareness, cross-system impact) is what spec anchoring exists to answer. Pocket: "a Cloudflare construiu o nosso júri e a nossa catraca em escala industrial — e parou exatamente onde a verdade por capability começaria."


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
| Structural exploration + edit precondition | Erikson | Exploration block in root `CLAUDE.md`; Phase 1 of both skills |
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

- **Reviewer-mode A/B eval (from the "4 agents" discussion, 2026-07-03).** When Milestone 1 exists: same diffs with seeded violations, multi-lens single reviewer vs parallel single-lens instances as the *default* (not only the >400-line escalation). Hypothesis to test: **cross-lens consistency bias** — a judge that just approved under one lens is less willing to block under the next; the strongest argument for always-parallel, currently unmeasured either way (and Anthropic's *Building Effective Agents* sectioning rationale leans this way: LLMs generally perform better when each consideration gets a separate call with focused attention). Measure recall per violation class, token/latency cost, and merge-step degradation (the worker deduplicating reports on its own code). Decides the default; until then, multi-lens default + size-based escalation stands, and the ~400-line threshold is a reasoned, never-calibrated number. Design space for the merge step, from Klaassen's independence budgeting: a finding is only as trustworthy as the independence of whoever confirmed it — an agent agreeing with itself is one vote, not two; cross-reviewer corroboration could *promote* confidence (vs. today's dedup-keep-highest-severity); and an adversarial pass in a **different model family** is the strongest independence buy — a tension with the Opus pin, noted as an option for the widening era. Pocock's shipped code-review adds two data points: parallel-per-axis is his *default* ("so they don't pollute each other's context"), and cross-axis merging is forbidden outright ("don't pick a single winner across axes — that's the reranking the separation exists to prevent") — a third merge-step design (present per-lens, never collapse) alongside dedup-highest and confidence-promotion.

- **Boundary criterion for the reviewer (from the package-by-feature discussion, 2026-07-01) — ✅ APPLIED 2026-07-03 in the skills migration.** `plan-review` gained criterion 7 and `general-code-review` a Dimension-2 bullet: any NEW top-level folder/module in the plan or diff must pass the capability-vs-entity tests (business verb not data noun; vertical slice not horizontal layer; imports point inward). Slow structural drift stays deterministic (co-change + dependency-cruiser — quarterly check #5 in GUIDELINE Part 6), not an LLM lens: cheaper and better at the aggregate view, per the determinism-first principle.

| Item | Source | When |
|---|---|---|
| Tools allowlist on `reviewer.md` (read-only by config) | #10, confirmed by #11 | First post-run cleanup — one line |
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

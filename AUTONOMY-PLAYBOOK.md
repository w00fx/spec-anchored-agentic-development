# Autonomy Playbook — widening beyond the narrow start

> Companion to `GUIDELINE.md` Part 5. The guideline gives what governs
> everything (the architecture-vs-increment split) and the **narrow start**:
> issues → hard-coded allowlist of trivial classes → CI green mandatory →
> PR → a human approving every PR. This playbook is the **widening path**:
> how autonomy earns more classes, more volume, and eventually conditional
> auto-merge — each step gated by evidence, not faith. Read it when you're
> ready to widen, not before.

## The gradient in one view

| Stage | What runs | Who says "no" | Requires |
|---|---|---|---|
| Narrow start (guideline Part 5) | trivial increment classes, human on every PR | CI (accumulated tests) + human | safety baseline only: branch protection, scoped credentials, no direct push, one issue → one PR, named blockers, human merge (evals can wait; the baseline can't) |
| Milestone 1 | same — plus the measuring infrastructure | + regression suite (pass^k) + baseline metrics | `EVALS.md` built |
| — M1 instance candidate: `smevals` (Simon Willison; experimental — source #53): Configs = model-and-harness, the gauntlet as Grader, mean±stderr with `-n` sampling. The class is the requirement; this names a tool. | | | |
| Milestone 2 | more classes, still human on every PR | + Tier 1 static gates in CI | M1 stable |
| Milestone 3 | same classes, validated post-deploy | + Tier 2 dynamic agents | pipeline to UAT |
| Milestone 4a | machine **approval eligibility** for qualified classes (human still merges) | Tier 1+2 + per-class track record | M3 + history |
| Milestone 4b | platform **auto-merge** for those classes — a much higher bar | 4a + seeded-fault evals + rollback drill + incident-free window | M4a sustained |

**The permanent boundary — normative work.** Any change touching a normative
calculation requires golden/conformance verification before entering autonomy
in any form: a human PR reviewer does not recalculate values against the norm.
Normative classes wait for that net regardless of how wide the rest has become.
And architecture work (new capabilities, new sub-areas, contract
reorganizations) never enters — at any milestone. There is no Milestone 5.

## Milestone 1 — Evals as a safety net

Prerequisite for any **widening** of autonomy beyond the narrow start. This
milestone is where you build your project's `EVALS.md`: start with a minimal
manual regression suite (10-15 representative tasks), grow it into CI (30+
tasks, pass^k), and begin tracking production baselines — on **two axes**:
output evals (does the final artifact meet the bar) and **trajectory
evals** (did the run take the right steps; a fluent output that skipped
its verification steps is a more dangerous failure than one with a
visible error). Run them as a flywheel: evaluate, diagnose failures by
clustering root causes, optimize the prompt or tool that caused them,
verify against the
regression suite and a held-out set (a fix that resolves the mined
weakness can break something elsewhere — acceptance is no regression
on both), monitor for new failure modes —
each cycle compounds. No new agent in this
phase —
you build the infrastructure that will measure the agents to come, and
establish a production baseline with human PRs.

Note the asymmetry with the narrow start: the narrow start may already be
running before this milestone (the allowlist plus human-on-every-PR keeps its
risk proportional). What may NOT happen before this milestone is widening —
more classes, more volume, any step toward auto-merge. Widening without a
regression suite and baseline metrics turns the routine into faith.

**Exit criterion**: regression suite with 30+ tasks running in CI, pass^3
baseline established, production metrics (merge-without-edit rate,
edit-distance) tracked for at least 30 days.

## Milestone 2 — Tier 1 (expanded static review) + widened classes on the issue route

Two things in parallel.

**Tier 1 enters CI.** It's not "static review with an LLM" — it's the set of
mechanical reviews and metrics that replace line-by-line human review for
agent code. There's an active community debate that reflects the central
tension here: Uncle Bob Martin argues that humans should step out of code
review and measure quality via metrics (test coverage, cyclomatic complexity,
dependency structure, mutation testing) to scale productivity; Grady Booch
counters that metrics don't capture vulnerabilities, dead code, missed
refactoring opportunities. The approach here adopts "measure to scale" in
Tier 1, but treats Tier 2 (dynamic validation) and Milestone 4 (auto-merge by
class) as responses to Booch's concern — not a rejection of it. Composition:

- **Uncle Bob metrics:** test coverage (floor per capability), cyclomatic
  complexity (limit per function), module sizes (limit per file/class),
  dependency structure (detects cross-coupling between capabilities),
  mutation testing, duplication
- **Domain-specific checks:** constitution compliance (correct numeric types,
  source citation present when applicable, audit trail recorded), spec drift
  (does code diverge from the spec?), code quality rubric with a model in the
  loop (over-engineering, convention conformance)

Split them honestly when reasoning about authority and false positives:
**Tier 1A — deterministic static gates** (types, lint, golden, coverage
ratchet: binary, cheap, authoritative) and **Tier 1B — inferential diff
review** (the model-in-the-loop rubric: valuable, fallible, report-only).
Both run against the diff / static code, without deploy. And map each
risk to the control that actually observes it — QA/E2E agents cover
behavior and integration; security, dead code, and refactoring debt
need their own instruments, not an assumed side effect.

**The issue classes widen.** Beyond the narrow-start trivia: larger
tech-debt, rule adjustments with more surface, reference-table updates with
more consumers. Still a hard-coded allowlist by class and permitted paths
(enforcement in the harness, not the prompt); `EVALS.md` pre-action gates
apply. The routine opens a PR → a human always reviews and approves. The
`implement-backlog` skill materializes this routine, exactly as in the narrow
start — what changed is how much it's trusted with, and what stands behind
that trust.

**Exit criterion**: 50+ autonomous PRs reviewed with > 80% approval, low and
stable edit-distance, zero scope-creep or prompt-injection incidents.

## Milestone 3 — Deployment pipeline + Tier 2 (dynamic validation)

Explicit prerequisite: a deployment pipeline to an integration environment
(UAT, pre-prod, or equivalent). If it doesn't exist yet, that's the milestone
— infrastructure work, outside the guideline.

With the pipeline running, Tier 2 activates post-deploy:

- **QA agent:** runs functional scenarios via browser/script against the
  deployed application
- **E2E agent:** triggers cross-stage flows (e.g. collector → parser →
  analyzer → quantifier) with representative synthetic data
- **Integration agent:** validates real contracts via API between
  capabilities, not just static schema

All three comment on the PR. A human still approves. Tier 2 is where complex
domains gain a net that Tier 1 metrics don't provide — real behavior,
integration with services, end-to-end cases. It addresses the kind of risk
Booch identifies as a limitation of metric-only review: vulnerabilities, dead
code, performance problems, missed refactoring opportunities. Tier 1 + Tier 2
together aim to cover both sides of the debate, instead of choosing one.

**Exit criterion**: validation agents with false-positive rate < 20%
calibrated against human review, at least 90 days with Tier 2 running stably.

## Milestone 4 — Conditional auto-approval per increment class

Split deliberately: **4a (approval eligibility)** and **4b (platform
auto-merge)** are different risks. All thresholds below are
**operational placeholders, not empirically validated** — calibrate
them with seeded evals (M1's apparatus) before treating them as bars.

Automation reaches the maximum defensible level in this context, limited by
increment class and by accumulated track record. The approach to Uncle Bob's
position (humans step out of code review for specific classes) only holds
where Tier 1 + Tier 2 accumulated enough history to make the delegation
verifiable, not faith.

**Track record is per increment class, not global.** Example: the class
"configuration parameter adjustment with cited normative source" accumulates
30 consecutive autonomous PRs with no human rejection + Tier 1 and Tier 2
approved on all of them + average edit-distance < threshold → the class
qualifies for auto-merge conditioned on Tier 1+2 approving.

Other classes — any change to a critical calculation, any change to the audit
trail, any change to a structured-input parser — remain human-approved
indefinitely. Not because the agent can't do it, but because the cost of
error is too high to delegate.

**Exit criterion** (per class, not global): 90 days with no incident in that
class, controlled average cost, quarterly review confirming the class still
deserves auto-merge.


**The shipped reference — PostHog's StampHog (source #29; 1 in 3 merged
PRs auto-stamped, 1.6K/month).** Opt-in per PR via a label; a
**deny-list of never-AI-approved classes by blast radius** (auth,
secrets, billing, public APIs) alongside the class allowlist; size
ceilings as a gate (theirs: 500 lines / 20 files); **fail closed**;
never request changes or merge — **the LLM can tighten gates, never
loosen them**; refusals escalate with a one-line reason + risk level,
routed to an SME (CODEOWNERS + git-blame familiarity). Two
calibrations to keep: the field's shipped version stops at
**auto-approval** — merge stays with humans and CI; and **start the
stamper early, even in refuse-mostly mode** — every approve / refuse /
escalate decision with its reason is a labeled datapoint, and the
stamper's log is the evidence base that calibrates which classes widen
(Milestone 1 feeds on it).

And mechanize the never-list per PR (source #43): a CI check that
labels the PR when the diff stayed off the truth layer (`specs/`, the
golden, benchmarks, CI config itself). Reviewing an autonomous PR
starts by checking that label — its absence is the loudest finding.
And the reason the gate must be external got its definitive receipt in
source #51: Prime Agent's `/refine` loop, once it found an exploit,
"turned to building **efficient cheating skills**" — an ungated
improvement loop doesn't merely permit gaming, it industrializes it;
a heartbeat prompt saying "don't cheat" held nothing.

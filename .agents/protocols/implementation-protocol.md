# Implementation protocol — the shared state machine

Every implementation skill (`implement-feature`, `implement-orchestrated`,
`implement-backlog`) runs this machine. The loaded skill is a mode adapter: it
names who satisfies human/remote gates, while this file defines the work.

The harness has exactly two internal authoring agents:

```text
general-code-reviewer
mutation-hardener
```

Both internal agents inherit the effective model of the Owner/parent worker and run
at `effort=max`. No agent contract pins a model. A lower or unknown effective effort
is a configuration blocker; no adapter may silently switch models or downgrade it.

Specialized spec/conformance, security, performance, compliance, and systemic
architecture reviews are external to this protocol.

## Terminal taxonomy

`NO_CHANGE_REQUIRED` · `NAMED_BLOCKER` (ambiguity, missing oracle, truth
conflict, scope violation, spec change required, unavailable hardening tool) ·
`PR_READY_AWAITING_HUMAN`.

A run never claims merge, deployment, or production validation.

## Phase 0 — Preflight

Read the adapter's gate-provider table. Verify authority: the spec is ratified
and protected/default main is the effective truth. If a ticket pins a commit,
compare by relevant requirement meaning rather than raw SHA inequality:

- no pointed ID/source/non-goal changed → note `SPEC_REBASED_NO_RELEVANT_CHANGE`;
- a pointed requirement/contract/non-goal changed → `SPEC_STALE` blocker;
- relevance cannot be established → blocker for the configured authority.

Confirm repository, branch/worktree, base SHA, issue ownership, available
commands, policies, and pre-existing failures. Read the root `AGENTS.md`, then
load the applicable files under `.agents/rules/`. Create one local runtime
directory at `.agent-runs/<run-id>/`; no run state or log may be written under
`.claude/`, `.codex/`, or `.cursor/`. Never mix unowned user changes.

## Phase 1 — Proven delta

Before planning, produce:

```text
expected
observed
evidence
gap
classification
```

No gap creates `NO_CHANGE_CANDIDATE`, not a cosmetic patch. Assemble an
evidence target containing authority IDs, commands and real outputs, searched
seams, environmental limits, and one classification:

```text
ALREADY_SATISFIED | STALE_REQUEST | WRONG_SYSTEM | UNVERIFIABLE
```

Route that target to `general-code-reviewer` in no-change mode during Phase 7.
Only a corroborated target may become `NO_CHANGE_REQUIRED`. Mutation hardening
does not apply to a true no-change target.

## Phase 2 — Understand and resolve ambiguity

Read the full context chain: root context, capability context, relevant spec
corpus, issue and comments, current code and tests. Separate facts, authorized
decisions, reversible implementation details, and unauthorized assumptions.
Material ambiguity goes to the adapter's provider. An aborting provider returns
`NAMED_BLOCKER`; never guess.

## Phase 3 — Plan, scope, and approval

Produce a plan naming:

- pointed requirement IDs and primary outcome;
- load-bearing decisions and deferred reversible details;
- implementation steps and dependencies;
- expected paths and allowed operations;
- dependency/schema/data/external-effect permissions;
- test strategy and evidence method for every criterion;
- mutation eligibility/target policy and fuzz/property applicability;
- rollback/recovery and explicit non-goals.

Compute the `APPROVAL-FINGERPRINT` over the canonical approval bundle: ticket
identity/body hash, base SHA, effective spec entrypoint/pin, plan hash, scope
manifest hash, semantic amendment hash or null, and issued policy identity.
Any change to these inputs requires a new fingerprint and approval.

Scope is the intersection of semantic ticket scope, externally issued policy,
and the mechanical scope proposed by the plan. Expansion is a new proposal and
approval, never an implicit field edit.

## Phase 4 — Owner implementation

The parent implementation agent is the **Owner**. It works the approved plan on
a typed branch in reviewable chunks. Use only the repository's declared
commands. Tests derive from requirements and `.agents/rules/testing.md`, not
from accidental code structure. `truth-layer.md` is always applicable;
`package-by-feature.md` applies when production files or capability boundaries
are created or moved. Record the loaded rule paths in the run state.

The truth layer is read-only by default. Supervised mode may materialize an
explicitly approved semantic amendment on authorized spec paths; orchestrated
and unattended modes remain proposal-only and stop with
`SPEC_CHANGE_REQUIRED`.

Any new path, dependency, schema/data operation, privilege, external action, or
load-bearing design decision returns to the applicable gate.

## Phase 5 — Baseline deterministic verification

Execute the approved evidence profile before specialist agents run. It may
include focused/full tests, lint, typecheck, build, contract/schema checks,
golden/reference oracles, integration/system checks, property/fuzz tests,
security tooling, migrations, and operational validation.

Record exact commands, exit codes, relevant output, artifacts, unexecuted
checks, and baseline-vs-regression classification. Required gates stay green.

## Phase 6 — Durable synchronization

Synchronize docs, evidence mappings, issue/backlog state, and narrowly justified
lesson proposals before hardening. Semantic truth changes return upstream and
invalidate the plan/approval. Context/rule additions are proposals unless the
approved scope explicitly includes them.

## Internal-agent model and effort contract

Both internal authoring agents inherit the model resolved for the Owner/parent
worker. Agent contracts must not pin model IDs. Codex adapters override only
`model_reasoning_effort="max"`; Cursor and other adapters must request the
inherited model at `effort=max` through their runtime. If `max` cannot be honored
or observed, the run blocks rather than switching models or accepting a downgrade.

## Phase 7 — General code review-and-repair

Dispatch `general-code-reviewer` in an isolated worktree against one exact Owner
candidate SHA.

For a code target, the agent runs an internal inspect → edit → verify → inspect
loop using the retained `general-code-review` skill, its agent contract, and the
applicable repository rules. It may modify production and tests inside scope. It commits locally and returns an Owner handoff containing input
SHA, output commit SHA, every changed path, reason, behavioral impact, commands,
results, and residual risks.

For a no-change evidence target, it makes no edits and returns either
`NO_CHANGE_CORROBORATED` or the counterexample/missed seam/blocker.

**Subagent changes never land automatically.** The Owner must:

1. inspect the exact input..output diff;
2. verify semantic intent, scope, and non-goals;
3. accept or reject every material change;
4. integrate only the accepted local commit(s);
5. rerun affected deterministic checks;
6. record the handoff and Owner disposition.

`SEMANTIC_CHANGE_REQUIRED`, `SCOPE_EXPANSION_REQUIRED`,
`ORACLE_REVIEW_REQUIRED`, or `DEPENDENCY_APPROVAL_REQUIRED` returns to the
corresponding gate. A non-progressing internal loop becomes `NAMED_BLOCKER`.

## Phase 8 — Mutation hardening

On the Owner-accepted candidate, dispatch `mutation-hardener` in a fresh
isolated worktree.

The hardener uses pinned repository tools, resolves the approved eligible target,
raises target line and branch coverage to 100%, runs differential mutation
sequentially by bounded target, and modifies production/tests as needed until:

```text
line coverage = 100%
branch coverage = 100%
mutant resolution = 100%
actionable surviving mutants = 0
```

It also runs applicable property/fuzz suites and declared complexity/CRAP and
duplication checks. It may not change truth, golden/reference oracles, scope,
thresholds, mutation operators/manifests/exclusions, rules, policy, CI, or review
criteria to make the gate pass.

The hardener commits locally and returns every modification and result to the
Owner. The Owner applies the same six-step inspection/integration protocol used
in Phase 7. Equivalent/tooling-limited mutant dispositions require Owner review
and later external review; the hardener cannot approve its own exception.

No eligible executable target may return `MUTATION_NOT_APPLICABLE` with evidence.
Missing reproducible tooling or non-progressing mutation loops are named
blockers. Any Owner edit after accepting the hardener invalidates both internal
passes and returns to Phase 7, then Phase 8.

## Phase 9 — Final Owner acceptance and candidate freeze

The Owner confirms:

- both agent handoffs were inspected and dispositions recorded;
- no agent changed semantic truth, scope, or the judging gates;
- all accepted commits are present and rejected changes are absent;
- the full required deterministic suite is green on the integrated tree;
- the mutation report identifies this exact final candidate;
- all durable artifacts are synchronized.

Freeze base/head SHA and diff fingerprint. Any later versioned edit, rebase,
conflict resolution, generated-file change, or evidence mutation invalidates the
final candidate and returns to Phase 7 and Phase 8.

## Phase 10 — Deliver

Open the PR on the repository template, link the issue, approval fingerprint,
verification evidence, General Code Reviewer handoff, Mutation Hardener report,
and Owner dispositions. Terminal: `PR_READY_AWAITING_HUMAN`.

External spec/conformance, security, performance, compliance, architecture, and
independent code reviews run in the external pipeline/orchestrator or
periodically according to repository policy. Their later blockers re-engage the
Owner; any code correction reruns Phases 5 through 9.

## Structured logging

All transient run artifacts live under `.agent-runs/<run-id>/`, including
`run-state.json`, `run-log.md`, approval/scope/evidence artifacts, hardening
targets and handoffs, Owner dispositions, final candidate identity, and
`result.json`. `.agent-runs/` is gitignored; a sanitized copy may be retained as
a CI artifact. The adapter log records: run/issue/branch, approval fingerprint, per-phase
outcomes, exact commands/results, each agent's input/output SHA, changed paths,
Owner accept/reject disposition, final mutation metrics, terminal state, and
cost where visible. The PR is the durable public record.

## Critical rules

Typed branch; never `--no-verify`; never merge; never resolve your own semantic
ambiguity; never expand scope silently; never edit truth or the judging gate to
get green; subagent commits are proposals until the Owner inspects them; claims
require evidence, not narration.

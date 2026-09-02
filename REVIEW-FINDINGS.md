# Review findings tracker — spec-anchored deep review (2026-08-11)

## Cross-harness canonical-core and runtime-state migration (2026-08-30)

**State: IMPLEMENTED; structural, fast-kernel, adapter, and focused migration probes green. Full slow corpus and mutation stages remain release-CI evidence.**

- made root `AGENTS.md` the cross-harness operational entrypoint and rule router;
- moved the canonical workflow corpus from `.claude/skills/` to `.agents/skills/`;
- moved the canonical engineering rules from `.claude/rules/` to `.agents/rules/`;
- retained the already-migrated shared protocol under `.agents/protocols/`;
- moved every run log and transient implementation artifact to the gitignored `.agent-runs/<run-id>/` contract;
- restricted `.claude/` to optional Claude-specific hooks/routines and mechanically retired shared skills, rules, protocols, commands, agents, and logs under that namespace;
- changed `scripts/install-codex-port.sh` to validate the shared core and materialize only `.codex/agents/` adapters;
- updated `GUIDELINE.md`, `INSTALL.md`, policy documentation, harness adaptations, implementation skills, agent contracts, validator, corpus fixtures, and gate wording;
- clarified that `.agents/rules/` is a canonical location, not a cross-harness auto-load primitive: `AGENTS.md` routes and transactional workflows read applicable rules explicitly;
- clarified one durable logical capability authority with a stable entrypoint, not necessarily one physical spec file;
- made the canonical shared skill corpus runtime-neutral; slash/dollar invocation syntax now belongs only to runtime adapters.

Observed in this focused migration:

```text
structural validator                         PASS
kernel contracts                         65 / 65
kernel adversarial fixtures             208 / 208
Codex canonical-source / adapter check       PASS
Codex materialize + exact drift check        PASS
focused migration negative probes         10 / 10
```

The monolithic corpus and mutation runners exceeded the available execution window and are not reported as green here. Their full results must be retained by release CI. No claim is made yet about real Cursor/Codex agent handoffs, Owner disposition, PR events, or external review API integration; those remain Integration Qualification work.

## Parent-worker model inheritance correction (2026-08-29)

**State: IMPLEMENTED; structural, fast-kernel, targeted negative-probe, mutation, and materializer validation green.**

- removed explicit model IDs from both canonical Markdown agent contracts and both Codex TOML adapters;
- made omission of `model` the executable inheritance contract for the Owner/parent worker model;
- retained `effort: max` in Markdown and `model_reasoning_effort = "max"` in Codex TOML;
- updated the shared protocol, implementation adapter, orchestrator, installation guidance, and harness adaptations;
- made any reintroduced Markdown or TOML model pin a structural failure;
- changed direct Codex worker launch to inherit its configured model and override only reasoning effort.

Observed validation in this focused update:

```text
structural validator                         PASS
kernel contracts                         65 / 65
kernel adversarial fixtures             208 / 208
targeted inheritance/effort probes         5 / 5
known semantic mutants                    55 / 55 killed
Codex fresh materialization + drift          PASS
```

The complete slow corpus suite remains a release-CI artifact; the changed inheritance and effort contracts were exercised directly by the targeted probes above.

## Shared protocol, inherited model, and max-effort normalization (2026-08-29)

**State: IMPLEMENTED; structural, fast-kernel, negative-probe, and materializer validation green.**

- moved the single canonical protocol tree from `.claude/protocols/` to
  `.agents/protocols/`, preserving one runtime-neutral authority for Claude,
  Codex, Cursor, and external tools;
- updated all implementation adapters and documentation to reference
  `.agents/protocols/implementation-protocol.md`;
- made `.claude/protocols/` a mechanically rejected retired location;
- set both canonical Markdown agents to `effort: max` and both Codex TOML
  adapters to `model_reasoning_effort = "max"`;
- removed all internal-agent model pins so each agent inherits the Owner/parent
  worker model, while lower or unknown effective effort remains a blocker;
- updated direct Codex worker invocation to inherit its configured model and
  override only effort;
- added negative fixtures for model pins, effort downgrades, missing protocol
  authority, stale adapter references, and duplicate legacy protocol location.

Observed validation in this focused update:

```text
structural validator                 PASS
kernel contracts                    65 / 65
kernel adversarial fixtures        208 / 208
corpus fixtures                     61 / 61
known kernel mutants                55 / 55 killed
Codex fresh materialization + drift  PASS
```

## Two-agent internal hardening update (2026-08-29)

**State: IMPLEMENTED; structural and fast-kernel validation green; end-to-end agent/API qualification pending.**

The implementation harness now invokes exactly two internal authoring agents:

```text
Owner implementation
→ General Code Reviewer authoring loop
→ Owner inspects and accepts/rejects the complete handoff diff
→ Mutation Hardener authoring loop to the approved 100% target contract
→ Owner inspects and accepts/rejects the complete handoff diff
→ final deterministic verification
→ external review pipeline / human
```

Applied changes:

- added the canonical `.agents/rules/testing.md`;
- moved the two internal agents to the root `agents/` catalog, with
  equivalent `.md` and `.toml` contracts for each role; both Markdown forms
  declare `isolation: worktree`;
- removed the local reviewer router, `/review`, `plan-review`,
  `conformance-review`, and `constitution-compliance-review`; retained and
  adapted `general-code-review` as the rubric of the new authoring agent;
- updated all three implementation adapters to use only the two internal
  authoring agents;
- made every subagent commit a proposal requiring exact Owner diff inspection
  and a recorded disposition before integration;
- moved heavy spec/security/performance/conformance/architecture review outside
  the implementation worker;
- changed `PR_READY_AWAITING_HUMAN` to bind the exact General Code Reviewer
  report, Mutation Hardener report, and Owner disposition rather than an
  internal independent-review seal;
- converted former command entrypoints into explicit skills; the later cross-harness migration moved their canonical source to `.agents/skills/` and retired `.claude/commands/`, `.claude/agents/`, and `.claude/skills/`;
- updated the Codex materializer; the later cross-harness migration removed skill mirroring, leaving only canonical-source validation and `.codex/agents/` adapter materialization;
- integrated the coherent-task `spec-to-tickets` skill and updated
  `ticket-readiness-review`, including the umbrella-outcome check and no
  numeric task limit.

Observed validation in this build:

```text
structural validator                 PASS
kernel contracts                    65 / 65
kernel adversarial fixtures        208 / 208
known kernel mutants                55 / 55 killed
Codex materializer fresh + drift     PASS
new structural negative probes       PASS
```

The monolithic slow corpus stage remains a CI/release artifact because its full
run exceeds this chat execution window; the previously qualified v5 corpus is
unchanged except for the new two-agent/testing-rule fixtures, which were probed
individually. Real Owner→agent commit handoffs and external-review integration
remain `Integration Qualification` work, not claims of this static update.

Source: external deep review (40 findings, SA-001..040). Every P0 was
verified against the actual files before any verdict — 11/11 confirmed.
Verdicts: **applied** (fixed in this bundle), **deferred** (accepted,
staged), **rejected** (argued below).

**Status taxonomy (per the second audit):** `accepted → implemented →
verified`, with `partial` and `rejected-reasoned`. Everything in the
table below is **implemented** — verification (validators, smoke
tests) is what promotes it.

## Implemented (this bundle — verification pending unless noted)

| ID | Fix |
|---|---|
| SA-001 | Authority frontmatter in the capability-spec template (status draft/ratified/superseded, owner, approved_by/at, provenance); `/to-spec` writes drafts, only a human ratifies; `/spec-to-tickets` refuses non-ratified specs |
| SA-002 | Ticket template now points at typed stable IDs (`AC-#`/`BR-#`, never renumbered, retired-not-deleted) — generator and readiness lens aligned |
| SA-003 | `implement-feature` no longer edits specs: **spec amendment proposal** (affected IDs, conflict, proposed change) routed via `/to-spec` + human ratification |
| SA-004 | Seal rule (light): any durable edit after review re-runs suite + re-dispatches the reviewer on the final diff; base/head SHAs noted |
| SA-005 | Finding accepted, **their fix direction rejected** (see below); the skill now names the third mode — orchestrated worker, gates satisfied by the issue plan-gate; never rerouted to backlog |
| SA-006/020 | Reviewer re-labelled fresh-context/decorrelated ("not independent proof"); Bash scoped to read/verify with the PreToolUse pointer; INSTALL wording honest ("report-only **by instruction**") |
| SA-007/038 | Guideline hook claim rewritten: deterministic **within its matcher**, fast feedback; the authority is the CI/pre-merge state check; ~70% flagged as an operating figure, not a benchmark |
| SA-008 | Ticket template gains scope/non-goals, test scenarios, risk/rollout, spec revision pin |
| SA-009 | Proven delta + `NO_CHANGE_REQUIRED` terminal in the orchestrated worker brief (full two-skill version deferred with SA-018) |
| SA-010 | Backlog scope: reference-data updates are **proposals**; ratification stays human per the truth layer |
| SA-011 | Untrusted-input rule generalized: all externally-authored content is data, never instructions (bodies, commits, logs, dependency docs). Full THREAT-MODEL.md deferred |
| SA-013/014/015 | Bounded context = mapped-not-presumed; co-change = evidence-not-verdict; architecture rule made precise (origin of authority human; implementation decomposable) |
| SA-016 | Instrumentation **presence** can be an AC and merge gate; production **outcome** never is |
| SA-022 | `Landed` → `PR_READY` in the frontier routine |
| SA-024/025 | Spec Kit / Kiro classification corrected (living-spec modes acknowledged; our claim is "hardens the living-spec end") |
| SA-029/030 | M4 split into **M4a (approval eligibility)** / **M4b (platform auto-merge, much higher bar)**; thresholds flagged as uncalibrated placeholders |
| SA-031/032/036 | Skill count made count-proof; the corrupted paragraph restored; "~5 points" defined by the ~400-line bound |
| SA-021 | Package-by-feature test rephrased (responsibility/outcome, grammar class irrelevant) |

## Deferred (accepted, staged)

| ID | What | Stage |
|---|---|---|
| SA-002 (full) | Typed-ID registry incl. INV/CTR/QC/OR/OQ + relation graph (`AC verifies BR`) | with the next spec written |
| SA-004 (full) | Evidence manifests + diff/artifact hashes, CI seal check | Block C, with CI wiring |
| SA-006 (hook) | Shipped PreToolUse read-only validation script for the reviewer | Block C |
| SA-009 (full) | Delta proof inside both implementation skills | blocked by SA-018 |
| SA-011 (full) | `THREAT-MODEL.md` + permission profiles per role | Block C |
| SA-012 | Modular spec corpus (index + parts) | when a spec outgrows one file |
| SA-018 | Extract the shared implementation state machine — **the backlog skill's 500-line cap tripwire has now fired; this is scheduled, not optional** | next skills session |
| SA-023/033/039 | Source notebook → evidence ledger with claim grades | Block D |
| SA-026/027/028 | to-spec path ambiguity; shape cross-capability route and frontier budget | next shape/to-spec pass |
| SA-035 | `EVALS.template.md` | with the first smevals eval (source #53) |
| SA-037 | Routine terminal vs merge monitor alignment | verify in next routine run |

## Rejected — with the arguments

- **SA-005 (fix direction only):** routing orchestrated work to
  `implement-backlog` would break the one-ticket-one-PR invariant — the
  backlog skill is a loop over a list, and in orchestration **the loop
  is the maestro**. The finding (contradictory text) was real and is
  fixed by naming the third mode instead.
- **SA-017/040 (harness matrix file):** volatility is already contained
  by architecture — doctrine files avoid product names; the volatile
  layer IS `adaptations/` plus the operator-pinned recipe in
  `/orchestrate` (an explicit user decision, max included), refreshed
  by the INSTALL re-audit ritual. A separate YAML matrix adds one more
  file that can drift without adding a reader: the agents read the
  adaptation pages, not a config nobody loads.
- **SA-019 (English as axiom):** the canonical language is a declared
  project decision, not an accident — specs already carry the
  **capability language** (Portuguese domain terms are first-class and
  ubiquitous-language rules protect them); English for artifact
  scaffolding is a portability choice for a system published and run
  across harnesses. Declaring the canonical terms is required; swapping
  artifact language wholesale is not.
- **SA-034 (draft citation):** the distinction that matters is internal
  doctrine vs public artifact. A read draft may inform internal files
  (the catalog flags its status), and the public-citation ban is
  already recorded where it belongs — on the source entry itself.

## Second audit (v2, 2026-08-12) — regrades and new findings

Regrades of the first batch (per v2's file-level audit, verified):
SA-001/002/003/006/007/009/020/031 → **partial**; SA-005 →
architecture accepted, **implementation reopened** (invocation
mechanics); SA-022 → partial (backlog wording lands with the
extraction rewrite).

New findings, status after this batch:

| ID | Status |
|---|---|
| DR2-P0-03 invalid frontmatters | **fixed** (block scalars, YAML-validated) |
| DR2-P2-01 duplicate template | **fixed** (root copy removed from the bundle) |
| DR2-P0-05 Open questions section | **fixed** (template + OQ lifecycle) |
| DR2-P0-04 single ID grammar | **implemented minimal** (`BR/AC-<CAP>-###` in template headings; full registry staged) |
| DR2-P2-04 four-lens wording | **fixed** (count-proof: applicable lenses) |
| SA-019 empirical rationale | **fixed** (policy formulation, no universal claim) |
| DR2-P0-01/02 third-mode invocation + per-engine briefs | **scheduled — extraction session** (implement-orchestrated adapter, first-message slash invocation, Claude/Codex parity smoke test) |
| DR2-P0-06 spec-write residuals | **to audit in extraction** (exact-phrase greps came back 0; cited lines may be paraphrased) |
| DR2-P0-07 authority precedence | **decided: Option A** — protected main is effective truth; frontmatter is identity/lifecycle metadata, never a competing approval record (to encode with the validators) |
| DR2-P1-01..16, P2-02..10 | **staged** per blocks C–E (seal, permissions, lease, EVALS with smevals, ledger, loader semantics per adapter) |

## Extraction session (2026-08-12) — SA-018 / DR2-P0-01/02, P1-01/03/04

**Implemented (pending smoke-test verification):** the shared
`implementation-protocol.md` (state machine: Phase 0–9, terminal
taxonomy incl. `NO_CHANGE_REQUIRED` and `PR_READY_AWAITING_HUMAN`,
proven delta, plan fingerprints, seal, invariants) + three thin mode
adapters (`implement-feature` supervised-local, `implement-orchestrated`
NEW, `implement-backlog` unattended) each with an explicit
gate-provider table. The orchestrator brief now makes the invocation
the worker's **first message** (user-invocation semantics preserved
under `disable-model-invocation`), with per-engine forms and
refuse-if-not-installed. Terminal states unified (no adapter claims a
merge). All files now far under the 500-line guideline.

**Honesty notes:** (1) this is a **compressed rewrite** — the prior
524/527-line texts live in git history; a detail-audit pass may
restore lost nuance; (2) DR2-P0-01/02 close only when EVAL-HARNESS-001
and -002 (invocation + engine parity) run green on a real repo —
until then the status is implemented, not verified; (3) GUIDELINE
prose that describes the old monolithic skills needs a doc-sync pass.

## Third audit (v3, 2026-08-12) — batch A applied

Fixed this batch: DR3-P0-08 (references rewritten to the protocol
generation; rationalizations removed — the protocol is its home),
DR3-P0-10 (all 8 argument-hints now strings, parser-validated),
DR3-P0-11 (monitor enforces `approved <fingerprint>`, three-way
match), DR3-P0-07 (HEAD_CHANGED event — re-review on new head;
comments without SHA carry no authority), DR3-P0-06 partial
(deterministic `--agent` dispatch, fail-closed on absent install;
full Codex port = Option A staged), DR3-P0-09 (template path
unified), DR3-P0-02 partial (old-generation sentences purged; the
authority hierarchy declared — protocol wins on execution; full
Part 3 rewrite staged), DR3-P0-05 (spec-write proposal-only in every
adapter, materialization via /to-spec + protected PR), DR3-P0-04
(Option A materialized: merge is the approval record; frontmatter
mirrors informative), DR3-P0-01 partial (/implement → honest
redirect; /goal recipes → direct invocation; smoke tests still
required), DR3-P2-01/02 (Kiro wording; reviewer body).

Staged (commits 2–5 of the v3 plan): full GUIDELINE Part 3 rewrite,
validate-bundle.py + frontmatter schema check, real Codex port
(.agents/skills + openai.yaml + reviewer.toml), seal schemas +
review-target binding, claim lease, EVALS template + harness cases,
ID validator, SPEC_STALE relevance algorithm.

## Batch B (v3 commits 2–5, the in-chat share) — 2026-08-12

Shipped: `scripts/validate-bundle.py` (caught 3 real violations on its
first run — the pt-BR mirror had escaped the purge, plus a residual
"four-lens"); `scripts/install-codex-port.sh` (Option A materializer:
.agents mirror + `allow_implicit_invocation: false` + reviewer TOML);
`EVALS.template.md` (case schema + the 16-case index);
`review-target-schema.md` (seal, staged); GUIDELINE Part 3 rewritten
to the adapter framing (protocol phases in parentheses; Action/Routine
wiring = direct invocation, never a goal condition naming a skill);
frontier-worker claim upgraded to a lease contract (label = signal,
not mutex; compare-and-verify; expiry; external concurrency key noted).

Still machine-side: EVAL-HARNESS-001/002 smoke tests, real CI wiring
of the validator, seal enforcement, lease atomicity.

## Fourth audit (v4, 2026-08-12) — Commit-1 batch applied

**Writer-policy decision (supersedes batch-A blanket):** the operator's
original doctrine restored — supervised adapter materializes semantic
amendments **after an explicit in-session human gate** (PR ratifies);
orchestrated/unattended stay proposal-only. Recorded across skill,
guideline, and truth-layer.

Fixed this batch: DR4-P0-03 (canonical `Blocked by: #N`; body =
authority, native links = mirror; GitHub `state_reason` semantics —
closed ≠ completed; not_planned → GRAPH_DECISION_REQUIRED; duplicate →
canonical); DR4-P0-02 (NO_CHANGE_REQUIRED wired distributed: monitor
event + resolution policy, adapter delivery row, routine terminal,
done = resolved-not-merged); DR4-P0-05 partial (baked-in now
`approved <fingerprint>`; canonical-bytes spec staged); DR4-P0-06
(cognitive locality = serialized launches; one-ticket-one-PR
inviolable); DR4-P1-12 partial (Phase-2-plan refs → protocol Phase 3);
DR4-P0-01 partial (remaining /goal-naming + Action recipes purged);
DR4-P0-09 (installer rewritten: developer_instructions, neutral
protocol path, sync --delete, normalized drift, honest naming —
"experimental coexistence materializer"); DR4-P0-11 (validator output
honest + dependency/phase legacy patterns added).

Deferred per operator instruction: DR4-P0-10 (pt-BR mirror).
Staged (v4 commits 2–5, 8): scope manifest schema, canonical plan
bytes, seal scripts, structured state artifact, relevant SPEC_STALE,
eval fixtures/runner, lease atomicity.

## Final in-chat batch (v4 commits 2/3/5 — the paper share)

Applied: scope-manifest schema + two-scopes wiring (semantic = ticket,
mechanical = plan-approved manifest; final name-status check before
review); canonical plan bytes; relevant SPEC_STALE; autonomous
plan-review by risk class; typed-ID grammar completed (to-spec, both
template examples now valid by their own grammar,
representation-by-truth-type, spec-to-tickets unified); "independent"
residuals fixed; codex.md counts count-proof; tier thresholds = local
defaults (risk outranks size); EVALS index synced to 22 cases;
reviewer `effort: max` with disclosure rule.

**In-chat queue: EMPTY.** Remaining work requires the machine:
seal/eval scripts + fixtures (v4 commits 4/8), smoke evals 001–005,
lease atomicity, CI wiring — and the pt-BR mirror (user-deferred).

## Fifth audit (v5, 2026-08-12) — transition contracts closed

The audit's own verdict: the architecture has arrived ("não recomendo
outra reconstrução"). Applied: **truth_change_policy mode-aware inside
the protocol** (the precedence contradiction dies at the source);
**NO_CHANGE_CANDIDATE → evidence-target review → NO_CHANGE_REQUIRED**
(no self-declared no-ops; /review gains the evidence-target kind; the
orchestrator corroborates before resolving); **resolution_satisfied**
drives the graph (frontier recomputes on any resolution event; the
fragile "HEAD is the blocker's merge commit" check replaced);
**approval bundle** (plan + scope manifest + ticket/spec/base pins in
one canonical hash — `approved <fingerprint>` identifies exactly the
authorized work); the Routine surgically repaired (splice corruption
removed — the second of the saga; the `/goal` loader block replaced by
the launcher contract with three terminals); installer copies the
protocol corpus recursively with a references-resolve check and a
normalized drift gate; typed IDs taught by the readiness lens;
`/goal` demoted to optional-verified-composition in both local
adapters; "independent" purged from the reviewer.

Still machine-side: the seal writer/verifier trio, run-state JSON,
ID validator, eval fixtures/runner — the v5's commits 4–7 and every
integration eval. The next deep review should read transcripts and
grader outputs, not files.

## Closing paper batch (v5 P1 leftovers) — 2026-08-13

Orchestrated adapter gains its promised references/ log template
(P1-16); INSTALL rows synced to the current generation (P1-11);
"Business rules (EARS)" → "Normative behavior (EARS as the default
form)" + to-spec writes by truth type (P1-04); /review is risk-first
(size = chunking only; P1-14); expand–contract batches must be
declared as coordinated mode (P1-15); evals deduplicated to 21.

**The paper floor is reached.** Per the v5's own directive ("não
adicionar mais doutrina agora"), everything remaining requires the
machine: seal writer/verifier/CI, run-state artifacts, ID validator,
eval fixtures + runner, smoke evals 001–012, lease atomicity — and
the pt-BR regeneration (user-deferred). The next audit should read
transcripts and grader outputs.

## Sixth audit (v6, 2026-08-13) — architecture frozen; the machine plan recorded

The audit's verdict: **"Congele a arquitetura"** — the paper-floor
prediction held; every remaining P0 is machine-side. Validated 5/6
checkable claims (four were my own defects); pycache NOT reproduced
in the current zip (0 entries — likely generated by the auditor's own
local run).

**Defect batch applied (fixes, not doctrine):** the scope manifest is
now **acyclic** (no approval fingerprint inside it) and truth writes
are a separate permission type (`truth_change.policy` +
`allowed_spec_paths` — the `specs/**` blanket deny that contradicted
the supervised amendment is gone); the orchestrator's description says
**resolution-gated waves**; "Creation is always human" replaced by the
canonical **human authority, not necessarily human authorship**; the
Action example is now **valid YAML** using the official
claude-code-action with the skill as direct prompt; reviewer routing
speaks protocol phases and gains the no-change target; /review wording
fixed; INSTALL documents explicit `python3`/`bash` invocation.

**The recorded machine plan (v6 commits 1–7):** (1) acyclic approval
writers + canonicalizer + negative fixtures; (2)
`resolve-effective-spec` (ratified = reachable from protected main;
unmerged `ratified` refuses); (3) no-change target union + lens +
router; (4) run-state/seal/result writers + verifiers + CI check; (5)
launchers finalized (official Action; Routine → triage-only) + old
unattended prose purged; (6) ID graph / spec-delta / issue-resolution
resolvers; (7) integration evals (fixtures, runners, trials, grader
outputs). Go/no-go stands as issued: supervised pilot GO (with the
five manual human checks); everything else NO-GO until the evals
exist. Product assumptions dated 2026-08-13 recorded in the audit.

## Seventh audit (v7, 2026-08-13) — Commit 0: canonical consolidation

**Correction owned:** the previous section claimed "every remaining P0
is machine-side" — the v7 proved it false (a second "creation is
always human" at :891, the old /goal-as-engine unattended section with
a self-contradiction two paragraphs apart, legacy phase numbers,
"independence is the point", merge-gated in the orchestrator's title
and defaults, "all closed" readiness in the routine). That overclaim
is exactly the failure mode this tracker exists to prevent. From this
section on, statuses use the evidence enum: ACCEPTED → IMPLEMENTED →
STRUCTURALLY_VERIFIED → INTEGRATION_VERIFIED (the last two require an
evidence pointer: validator run, fixture, transcript, or grader
output).

**Commit 0 applied (STRUCTURALLY_VERIFIED via the validator's new
patterns):** old unattended generation purged (launcher = external
Action with direct invocation; /goal = optional, eval-gated, never
engine or loader; DONE contract carries the three terminals; CI/merge
= external monitor); protocol phases everywhere; authority-not-
authorship at both occurrences; decorrelation wording; **resolution-
gated** in the orchestrator's title, description, baked-ins, Phase 6
and every cross-reference; routine readiness uses the shared
resolution semantics; "numbered acceptance criteria" residuals
retired. pt-BR: user-deferred (standing instruction).

**The frontier restated:** everything else is the v7's commits 1–7 —
writers, resolvers, seal, launcher qualification, evals. Per its own
words: the next review should receive scripts, schemas, fixtures,
transcripts and CI checks, and ask the right question — "did the
machine refuse the bad cases and preserve the good ones?"

## Eighth audit (v8, 2026-08-13) — Commit 0b, and a second overclaim owned

**Correction owned (twice now).** The previous section marked Commit 0
`STRUCTURALLY_VERIFIED`. It was **IMPLEMENTED**, not verified: the
validator only catches the forms a prior audit named, so my green run
proved the five v7 patterns were gone — not that the old generation
was. The v8 found the rest (`independent router`, `engine = native
/goal`, `local workflow (7 phases)`, `Phase 2 (plan review)`, `items
1-4`, `numbered criteria`, the `/goal`-as-recommended section, and the
Action tree line). **Rule adopted:** a consolidation claim may only
reach `STRUCTURALLY_VERIFIED` when the validator carries a negative
fixture for each retired form; otherwise it is `IMPLEMENTED`.

**Commit 0b applied (status: IMPLEMENTED):** canonical tree regenerated
from the real inventory (three adapters, protocols/, five lenses,
launcher line); typed stable IDs in every producer/consumer prose
(guideline ×4, spec-to-tickets, to-spec); `/goal` demoted from
"recommended local invocation" to an **experimental, eval-gated
composition** — never the engine, never a loader; `headless /goal run`
→ `headless run`; `Phase 2 (plan review)` → protocol Phase 3;
**APPROVAL-FINGERPRINT is now the single approval identity** (orchestrator,
guideline, both run logs, PR template — `plan_sha256` survives only as a
component of the bundle); logs record NO_CHANGE_CANDIDATE → review →
NO_CHANGE_REQUIRED; reviewer invariant restated as **non-authoring and
candidate-immutable** (disposable checkout, clean tracked tree, mutation
= finding) instead of blanket read-only; verification generalized to the
**declared method** per truth type; Codex adapter inventory de-hardcoded.

Machine frontier unchanged (v8 commits 1–6): canonicalizer + CLI,
authority/corpus/requirement resolvers, no-change target + lens,
run-state/evidence/seal/result, real launchers, executed eval suite.

## First executable contracts (2026-08-13) — paper → machine, the pure-function share

`scripts/spec-anchored` (dependency-free CLI: `canonicalize`,
`build-approval`, `validate-scope`, `validate-result`) +
`tests/test-contracts.py` (**40 negative fixtures, all passing**).

Status changes, with evidence pointers (the enum's rule, honoured):

| Finding | Status | Evidence |
|---|---|---|
| v8 P0-02 approval identity | **STRUCTURALLY_VERIFIED** | mutation matrix: all 8 bundle fields + incomplete + cyclic refused (`tests/test-contracts.py` §2) |
| v8 P0-01 retired doc forms | **STRUCTURALLY_VERIFIED** | validator refuses all 9 injected forms; clean corpus passes (§5) — the v8's own closure criterion |
| v7/v8 scope enforcement (share) | **STRUCTURALLY_VERIFIED** | denied-wins, outside-allowed, spec-write-under-policy-none, rename both ends, gated amendment exact-path (§3) |
| Terminal contract (share) | **STRUCTURALLY_VERIFIED** | illegal terminal, missing fingerprint, uncorroborated no-change, UNVERIFIABLE promotion, no-change-with-PR, merge claim — all refused (§4) |
| Canonicalization | **STRUCTURALLY_VERIFIED** | CRLF/trailing-space/key-order stability; real change still moves the hash (§1) |

**What this is NOT:** these are unit-level, pure-function contracts.
They prove the *rules* refuse bad input; they prove nothing about a
running agent, a launcher, git reachability, or a lease. Still
machine-side and unchanged: `resolve-effective-spec` (needs git),
run-state/seal writers wired into a real run, the no-change review
lens, real launchers, and every integration eval. Per the v8's
criterion, this turn shipped executable code + negative fixtures and
zero new doctrine.

## Ninth audit (v9, 2026-08-13) — the kernel hardened against its own fixtures

**All 11 checkable bypasses reproduced against the shipped code before
any fix** — the audit was right on every one, including a privilege
escalation I wrote: a path in `denied_paths` could be reclassified as
truth via `allowed_spec_paths` and escape the deny.

**Status correction (per the audit's §7).** The previous section's
`STRUCTURALLY_VERIFIED` rows were too strong: selected cases were
verified, not the contracts. Reclassified to **IMPLEMENTED +
verified_properties**, listed per contract below.

**Hardened this commit:**

| Contract | verified_properties (85 checks, all green) |
|---|---|
| canonicalization | CRLF/trailing/edge stability; key-order independence; **Markdown hard breaks refused** rather than normalized away; duplicate JSON keys refused |
| approval | 10-field mutation matrix (now including `run_id` and `plan_artifact_id` — the approval names the post it approved); placeholder/format/traversal refusal; cyclic field refusal; **approval record** verifies the approval *event* against the bundle |
| scope | **deny is absolute** (no truth reclassification); **typed truth** — spec semantics / golden oracle / metrics baseline, one grant each, exact paths only, *a spec amendment never authorizes the oracle*; permissions enforced against real trigger paths; expansions need their own fingerprint; manifest schema-validated before the diff; **parser fails closed** (unknown status, wrong column count, truncated NUL record) |
| result | strict tagged union: per-terminal required/forbidden fields, enums for `classification` and `blocker_kind`, `claim_state` bound to terminal, `WRONG_SYSTEM`/`UNVERIFIABLE` never terminal, PR/issue repo coherence, full-40 head SHA, unknown fields refused |
| documentation gate | scans hidden dirs (`.claude/**`) via rglob; semantic `/goal` variants; **compiles the CLI and runs both suites**; requires `disable-model-invocation: true` on the three transactional adapters; refuses a contract shipped without its fixtures |

Also: `scripts/check-all.sh` is now the single CI entrypoint;
`install-codex-port.sh --check` fails on drift (a raw `diff -r` would
have reported the intended repoints as drift); the coexistence adapter,
truth-layer, INSTALL, kiro and the scope schema were corrected to the
current generation.

**Explicitly NOT claimed:** these are shape and internal-consistency
contracts. Nothing here proves a PR, commit, review or approval exists
in the world — that is the `verify-*-against-environment` family, still
unbuilt, together with `resolve-effective-spec`, run-state/seal
writers, the no-change target schema, real launchers, and every
integration eval. Go/no-go is unchanged: supervised pilot GO,
everything else NO-GO.

## Tenth audit (v10, 2026-08-14) — the oracle was broken; fixed first

**Reproduced before fixing, both exactly as reported:** (1) four
deliberate regressions in the kernel (accept status `Z`, accept
duplicate JSON keys, accept Markdown hard breaks, drop `base_sha`
validation) left **85/85 checks green**; (2) `SA_NESTED=1 bash
scripts/check-all.sh` printed ALL GREEN with a `test-contracts.py`
that exits 1. The generic `refuses()` helper returned `bool(result)`,
so a parser that wrongly ACCEPTED bad input — returning a non-empty
object — was recorded as having refused it. **Several "verified
properties" in the previous section were therefore unfounded.**

**Commit 1 — fix the system that tests the system (done first, as the
audit ordered):**

- `tests/_harness.py`: every fixture declares its protocol —
  `raises` (parsers/builders), `violations` (validators), `clean`,
  `value`, `holds`. Nothing falls back on truthiness; an unexpected
  exception is a failure, never an accidental pass.
- `tests/test-mutants.py`: **mutation adequacy**. 15 known regressions
  are injected into the kernel; each must turn a suite red. Survivors
  are named. A mutant whose anchor no longer matches is also a failure
  — a suite testing a kernel that changed is not evidence. It found a
  real hole on the first run: the glob-grant fixture was passing for
  the wrong reason (defended by exact-membership, not by the check it
  claimed to test), now isolated with its own fixture.
- Gate integrity: `validate-bundle.py` is **structural-only** and never
  runs suites; `check-all.sh` runs each suite once, directly, unsets
  `SA_NESTED`, and adds `bash -n` on every shell script plus a
  frontmatter closing-delimiter check. The audit's exact bypass now
  exits 1.

**Commit 2 — policy floor (the worker stopped authorizing itself):**

- `PROFILES` (supervised-local / orchestrated-assisted /
  orchestrated-autonomous / unattended), issued outside the run.
  `validate-scope` **refuses to judge without `--profile`**.
- The manifest declares `adapter`, `execution_mode`, `policy_profile`
  and must be a **subset** of the authorized profile; truth types have
  a profile **ceiling** the manifest cannot raise — an unattended run
  proposing `semantic-amendment` is refused even when its own manifest
  grants it.
- **Governance floor**: the contracts, gates, policies, and agent
  definitions that judge a run are never writable by that run.
- `approved_expansions` **removed** — it reintroduced circular
  identity. An expansion is a new manifest → new fingerprint → new
  approval.
- The approval bundle now carries `adapter`, `execution_mode`,
  `policy_profile`, `policy_sha256` and `spec_corpus_sha256`: the
  human approves a *mode*, not only a diff.
- Approval records: strict types, provider enum, RFC3339, repository
  and run binding. Result: forge-host allowlist, comment-URL shape,
  `bool is not int` everywhere.
- Codex drift `--check` now covers `.codex/agents/reviewer.toml`;
  permission triggers extended (uv/maven/gradle/csproj/composer/mix,
  OpenAPI/proto, `migrate_*`), with `protected_path_classes`
  declarable **by the profile** for the rest.

**Status, honestly:** 121 fixtures + 15 killed mutants *at that commit* (see the twelfth-audit correction below for the current counts and for why raw totals are not the claim). That makes the
suites *evidence about the kernel* for the first time. It still does
not make the kernel an authority: nothing here proves a PR, commit,
review, or approval exists in the world. `resolve-effective-spec`, the
run-state/evidence/seal/result writers, the no-change target, real
launchers and every integration eval remain unbuilt. Go/no-go is
unchanged: **supervised pilot GO; everything else NO-GO.**

## Eleventh audit (v11, 2026-08-14) — the binding version

**All 15 probes reproduced against the shipped code before any fix.**
Three of them hit properties the tracker had claimed: `raises()`
accepted *any* crash as a refusal (so a parser that started throwing
`RuntimeError` instead of refusing would pass); `policy_sha256` was
only shape-checked, so the fingerprint bound a *string* rather than the
policy actually applied; and the governance floor was an inventory of
today's files, so `GUIDELINE.md`, `AUTONOMY-PLAYBOOK.md`,
`spec-templates/**`, `adaptations/**`, a **new** `scripts/*.py`, and
`.github/actions/**` were all writable by a run.

**Evidence states adopted** (the audit's §P1-10): `DECIDED →
DOCUMENTED → IMPLEMENTED → FIXTURE_COVERED → MUTATION_PROVEN →
STRUCTURALLY_VERIFIED → INTEGRATION_VERIFIED → PRODUCTION_OBSERVED`. A
line rises only with the matching evidence attached. Everything below
is **MUTATION_PROVEN** — fixture-covered *and* the fixture is proven to
fail when the property is removed — and nothing here is beyond that.

| Property | Evidence |
|---|---|
| A refusal is `ContractViolation`, never any crash | mutant "crash instead of refusing cleanly" now kills |
| `policy_sha256` is computed from the resolved artifact | mutant "stop computing the policy hash" kills; fixture with a zeroed hash refuses |
| The approval record binds to the bundle's run and repository | mutants + cross-run/cross-repo replay fixtures |
| Timestamps are calendars, not shapes | `2026-99-99T99:99:99Z` refused; mutant kills |
| Truth is set-valued, most-restrictive-wins | oracle-under-`specs/` fixture; mutant "classify by first match only" kills |
| Governance is a surface, not a list | 8 fixtures (doctrine, playbook, templates, a *new* validator, composite actions, adaptations, harness suites, EVALS) |
| A repository overlay narrows a profile and is honoured | overlay fixture passes; widening overlay refused |
| Ordinary-code breadth has a per-mode ceiling | unattended `allowed_paths: ["**"]` refused |
| Malformed manifests return violations, never `TypeError` | list/int/object probes all refuse structurally |
| Diff paths keep their identity | padded and git-quoted paths refused, demanding `-z` |
| A blocker is reported on its own issue | cross-repo and foreign-host comment URLs refused |
| Frontmatter is required, not merely well-formed | removing it wholesale now fails the structural gate |
| Declared operations are enforced | `allowed_operations` fixture |

**Gate architecture (the audit's P0-01):** suites split by cost — fast
in-process kernel suites, one slow corpus suite run **once**, and a
mutation runner that re-executes only the fast suites. Every subprocess
has a timeout; a hang is a failure, not a wait. `PYTHONDONTWRITEBYTECODE`
keeps the tree clean; `find -print0` handles paths with spaces.
**The whole gate went from >72s (mutants alone, no timeout) to ~9s.**

**Still not claimed, and still the frontier:** none of this proves a
PR, commit, review, approval, or claim exists in the world.
`resolve-effective-spec` (protected-main reachability), the
run-state/evidence/seal/result writers, the no-change target and its
lens, real launchers, and every integration eval remain unbuilt.
Go/no-go unchanged: **supervised pilot GO; everything else NO-GO.**

## Twelfth audit (v12, 2026-08-14) — policy became an authority

**13 of 14 probes reproduced against the shipped code before any fix**,
including three genuine authority bypasses: an overlay could **widen**
the base profile (`{"forbidden_path_patterns": []}` handed an
unattended run the whole repository), any object calling itself a
policy was accepted (`governance: "allow"` + `allowed_paths: ["**"]`
→ `GUIDELINE.md` writable), and the public `build-approval` command
never received the policy, so it accepted a **declared**
`policy_sha256` while the docs claimed it was computed.

**Numbers corrected (the audit's P1-07/P1-08).** The tracker's older
sections quote counts and timings from their own commit; they are not
current and are not claims about this one. Current: **61 + 88 + 21 =
170 fixtures, 27 mutants killed, 0 survived**. Gate timing is
**environment-specific** — measure it in your CI. Operating policy:
*inner loop* = the two fast kernel suites; *pre-push/CI* = the full
`check-all.sh`; *nightly* = integration evals when they exist.

**Applied:**

| Finding | Fix | Evidence surface |
|---|---|---|
| P0-01 overlay widening | monotonic merge per key: forbidden patterns union-only, operations intersect-only, protected classes add-only, ceilings may only be lowered, mode/adapters/governance/identity immutable — dropping a restriction is **refused**, not silently ignored | function + mutant |
| P0-02 policy self-declaration | `resolve_policy` accepts only a known id or `base_profile + overlay`; a raw object must be byte-identical to the canonical artifact. **A policy is issued, never self-declared** | function + mutant + **CLI fixture** |
| P0-02 CLI hash | `build-approval` and `verify-approval` now **require `--policy`** and compute the hash; a declared mismatch fails | **CLI fixture** |
| P0-02 dual authority | the structural gate proves `policy/profiles/*.json` are byte-identical to the kernel's profiles; mutating an artifact turns the gate red | structural |
| P0-02 weak verify | the fingerprint-only path is **gone**: `verify_approval` requires the bundle | function |
| P0-03 governance context | new surface class: `AGENTS.md`, `CLAUDE.md` (root and nested), `CLAUDE-*.md`, `architecture/constitution*.md` — a run cannot edit the instructions it is judged under | function + mutant |
| P1-01 nested schemas | closed at every level: unknown keys in `semantic_scope`, `mechanical_scope`, `permissions` refused | function + mutant |
| P1-02 stable ID grammar | `TYPE-<CAP>-###` enforced on `implements`/`verifies` | function + mutant |
| P1-03 NUL framing | a stream without its terminator is refused as truncated | function + mutant |
| P1-04 frontmatter schema | required fields per artifact class (command → description; skill/agent → name + description) | structural |
| P1-06 gate side effects | `PYTHONPYCACHEPREFIX` to a temp dir, cleaned on exit — `py_compile` writes bytecode regardless of `PYTHONDONTWRITEBYTECODE`, so the earlier claim was wrong | gate |
| P0-07 reviewer | `isolation: worktree` declared on the agent (enforcement of tracked-tree hashing remains runtime work) | declared only |

**Evidence surface is now part of the claim** (the audit's P1-07): a
mutant killed in a function does not prove the CLI passes the strong
arguments, so the corpus suite gained **CLI-level fixtures** and the
table above says which surface each fix is proven on. One property is
explicitly *fixture-covered but not mutation-proven* and says so in
`test-mutants.py`: with the bare-fingerprint guard removed,
`build_approval` refuses the string anyway, so no fixture can tell the
two apart.

**Unchanged frontier** (v12 commits 5–9, none of which can be done in
a chat): `resolve-effective-spec` with real Git ancestry, the artifact
DAG (run-state → proven-delta → evidence → review target/report/seal →
result) with environment verifiers, the no-change target and lens, a
real launcher with atomic claim and recovery, and integration
qualification. Go/no-go unchanged: **supervised pilot GO; orchestrated
assisted SHADOW; autonomous, unattended and auto-merge NO-GO.**

## Closure Validation v1 (2026-08-14) — the C01–C11 patch

The focal closure check ran A01–A10 and returned **2 PASS, 2 PARTIAL,
6 FAIL**. Every checkable probe was reproduced here before any fix,
and the diagnosis was right: *policy had been externalised as a
concept but was not yet an authority on the operational path.*

| Criterion | Before | Now | Proven on |
|---|---|---|---|
| C01/C02 a valid `base+overlay` works through the CLI | overlays were **unusable** — `_policy_arg` resolved, then `validate_scope`/`build_approval` resolved the resolved object again and refused it as self-declared | `ResolvedPolicy` type makes resolution idempotent; JSON can never forge it | CLI fixtures + mutant |
| C03 `profile.allowed_operations` is enforced | read only from the manifest — a policy-issued restriction did nothing | effective ops = profile ∩ manifest; a manifest may not add | function + CLI + mutant |
| C04 permission ceilings | an unattended manifest granting itself `dependency_change/schema_change/data_migration` was **accepted** | every profile carries a `permission_ceiling` (supervised open, everything else shut); the manifest may only narrow | function + mutant |
| C05 breadth is semantic, not textual | `src/**/*`, `src/**/**`, `**/src/**`, `src/*/**` all passed | closed pattern grammar per profile (forms, minimum literal segments, no leading/intermediate wildcards) instead of a blacklist of spellings | function + mutant |
| C06 malformed nested policy | `set([{}])` → `TypeError` | every element validated before any set operation → `ContractViolation` | function + mutant |
| C07 pattern grammar with zero changes | `../**`, `""`, `/abs/**` accepted when the diff was empty | `validate_manifest` validates patterns itself; an artifact is malformed regardless of the diff | function + mutant |
| C08 strict policy artifacts | the structural gate used `json.loads`, so a duplicate-key artifact whose last value matched stayed green | strict parse + `profile_id` ↔ filename | corpus fixture |
| C09 policy required on every approval path | `build_approval(parts)` and `verify_approval(record, bundle)` still accepted `policy=None` | both refuse without a policy; shape-only is an explicit, named argument that claims nothing | function + mutant |
| C10 hygiene | the standalone validator wrote `scripts/__pycache__` | `sys.dont_write_bytecode` before any dynamic import | corpus fixture |
| C11 measured budget | no timings, no thresholds | per-step duration and budget (`SA_BUDGET_*`), failing when exceeded; corpus retired-form fixtures moved **in process** (one composition test kept) | gate |

**Current state:** 61 + 116 + 29 = **206 fixtures, 34 mutants killed,
0 survivors**, full gate **32s in this environment** with per-step
budgets printed — measure it in your own CI rather than trusting that
number. Three fixtures were also found to be **passing for the wrong
reason** (defended by the breadth check rather than by the property
they named) and were isolated; that is what mutation adequacy is for.

**Frontier unchanged and unclaimed:** `resolve-effective-spec` with
real Git ancestry, the artifact DAG with environment verifiers, the
no-change target and its lens, a real launcher with atomic claim and
recovery, and runtime proof of reviewer immutability. Go/no-go
unchanged: **supervised pilot GO; orchestrated assisted SHADOW;
autonomous, unattended and auto-merge NO-GO.** The next report should
be *Spec Anchored Integration Qualification v1* — runs and artifacts,
not another documentary review.

## Closure Validation v2 (2026-08-14) — the K01–K10 patch

The focal recheck returned **7 PASS, 2 PARTIAL, 1 FAIL** on C01–C10 —
and was right that the single FAIL carried more authority than its
count suggested. Every probe was reproduced here first. The central
finding: *policy constrained the manifest's **form** but never its
**surface***, so an unattended worker still chose its own area of the
codebase and could rebuild breadth by enumeration.

| Contract | Before | Now | Proven on |
|---|---|---|---|
| K01 a base profile is not executable for autonomous/unattended | `unattended/v1` alone authorized a run | the validator refuses without a launcher-issued **policy instance** carrying `authorized_scope_roots` | function + mutant |
| K02 every `allowed_path` is inside an authorized root | a CAP-PAY run could take `src/identity/**` | each pattern's literal head must sit under a root | function + mutant |
| K03 aggregate breadth is capped | 100 exact paths or 100 narrow roots reconstructed the tree | `max_scope_roots` / `max_exact_paths`, defaults 4 / 20 for unattended | function + mutant |
| K04 every wildcard is final | `max(wild)` only checked the LAST one: `src/*/foo/**`, `src/**/foo/**`, `src/pay/**/**` passed | `any(i != last)` — intermediate wildcards refused | function + mutant |
| K05 policy denies bind changed paths | `forbidden_path_patterns` only compared manifest spellings; naming the secret file exactly escaped it | new `denied_path_patterns`, union-only in the merge, applied to **every changed path** before permissions and scope | function + mutant |
| K06 frontmatter must be a non-empty mapping | `---\n---` removed `disable-model-invocation: true` with a green gate | empty / null / comment-only / scalar all fail | corpus fixtures |
| K07 malformed `allowed_operations` refuses cleanly | `[{}]` and `1` slipped through or crashed | validated in the manifest schema and in the policy merge, against the git status grammar | function + mutant |
| K08 every python artifact compiles | the compile list was hardcoded; a new broken `scripts/*.py` passed | artifacts are **discovered** recursively | corpus fixture |
| K09 governance stops capturing product code | `tests/test_*contract*.py` and `evals/**` captured product tests | narrowed to the harness's own suites and `evals/spec-anchored/**`; `scripts/**` stays reserved **by decision** (a new gate must be covered by default) with `.spec-anchored/**` as the migration namespace, documented in `policy/README.md` | function + docs |
| K10 the budget is a real timeout with headroom | a 181s corpus run failed a 180s threshold; a hung step was never killed | each step runs under `timeout`, budgets carry headroom, and the message says to calibrate from your CI's p95 | gate |
| P1-05 canonical patterns | `src//pay/**`, `src/./pay/**` accepted | non-canonical spellings refused — an authorization artifact has one spelling | function |

`policy/instances/example-unattended-payments.json` ships as the shape
a launcher issues. **Current state: 61 + 138 + 34 = 233 fixtures, 40
mutants killed, 0 survivors, gate 37s here** (calibrate in your CI).
Two more fixtures were caught **passing for the wrong reason** and
isolated — the recurring lesson of this whole series.

**Unchanged and still unclaimed:** the integration frontier. Nothing
here proves a PR, commit, review, approval or claim exists in the
world. Go/no-go unchanged: **supervised pilot GO; orchestrated
assisted SHADOW; autonomous, unattended and auto-merge NO-GO** — and
the next report should be the short K-contract retest, then *Spec
Anchored Integration Qualification v1*.

## Closure Validation v3 (2026-08-14) — the authority artifact's own parser

The retest confirmed K01–K10 as substantially closed and named the one
remaining fail-open boundary, which reproduced exactly: **the authority
artifact was not validated like an authority.** A deny of
`"src/pay/secret/** "` (trailing space) was accepted, hashed into the
approval fingerprint, and then matched nothing — because real diff
paths are canonical. `../**`, `/abs/**`, `src//pay/**` and `""` were
accepted the same way, and an unparseable `policy/instances/*.json`
left the structural gate green.

| Fix | Detail | Proven on |
|---|---|---|
| Canonical validation for every path-bearing policy field | `authorized_scope_roots`, `denied_path_patterns`, `forbidden_path_patterns`, `protected_path_classes` share one validator: no padding, `.`/`..`, `//`, trailing slash, absolute path, backslash; roots additionally forbid wildcards | function + 2 mutants |
| Policy instances are inside the fail-closed boundary | the structural gate strict-parses **and resolves** every artifact under `policy/`, instances included — unparseable, unresolvable and duplicate-key instances turn it red | corpus fixtures |
| The two limits were named apart | `max_scope_roots` binds the **authorized root set** (and is now enforced against it); `max_recursive_scope_patterns` binds what a manifest may select inside it | function + mutant |
| The budget is portable | `scripts/run-step.py` replaces the conditional `timeout(1)` branch: a hung step dies at its budget on every environment Python already supports (exit 124, verified) | gate |
| Namespace layout | documented explicitly as an **installation contract that is not yet materialized** — `.claude/` and `.agents/` must stay at their discovery locations, so the split is integration portability work, not doctrine | docs |

**Current state: 61 + 154 + 37 = 252 fixtures, 43 mutants killed, 0
survivors, clean tree, gate 61s here** — calibrate from your own CI's
p95, as the auditor's 509–563s runs on slower hardware show how
environment-specific these numbers are.

Per the audit's own recommendation this closes the documentary phase:
the next artifact is **Spec Anchored Integration Qualification v1** —
effective spec → proven delta → policy instance + scope → approval →
candidate + evidence → review target/report/seal → result → PR, with
no-change, blocker, new-HEAD invalidation, crash/resume, lease expiry
and scope-violation scenarios. Go/no-go: **supervised pilot GO;
orchestrated-assisted GO to integration qualification (shadow, not
critical work); autonomous, unattended and auto-merge NO-GO.**

## Closure Validation v4 (2026-08-14) — one parser, one operator set

Conditional pass with one blocker, and the blocker reproduced exactly:
**the authority artifact accepted patterns the matcher never
implements.** `GLOB_CHARS` classified `[` and `]` as glob syntax while
`_match()` escaped them literally, so a deny of
`src/pay/[secret]/**` was hashed into the approval identity and then
denied nothing except the literal brackets — `src/pay/secret/a.py`
sailed through. Terminal `.` segments and internal C0/DEL characters
were accepted the same way.

| Contract | Fix | Proven on |
|---|---|---|
| F01 one canonical path/pattern parser | `canonical_violation(value, kind="path"\|"pattern")` is now THE definition for policy authority, manifest scope, truth grants and changed paths — no absolute or drive prefix, no backslash, no padding, no C0/DEL, no empty/`.`/`..` segment, no doubled or trailing slash; patterns accept only the operators the matcher implements, and `**` must be a complete segment. `SUPPORTED_OPERATORS` is published and a fixture asserts parser and matcher agree | function + 5 mutants |
| F02 closed profile registry | the structural gate compares expected against actual filenames in `policy/profiles/` in **both** directions — an extra file is neither a known profile nor an instance, and used to escape both loops | corpus fixtures |
| F03 process-tree timeout | `run-step.py` starts a new session and `killpg`s the group; a child that wrote a marker three seconds after a one-second budget no longer exists. On platforms without process groups the claim is **narrowed in the message** rather than pretended | corpus fixture (marker never appears) |
| P2-01 wording | `policy/README.md` says **canonical-equivalent**, not byte-identical: the gate compares canonical JSON hashes, which proves semantic equality | docs |

A redundant glob check in the truth grants was **removed rather than
kept**: with the canonical parser in place it was a second door that
made a mutant unkillable, and a property defended twice is a property
whose fixture proves nothing.

**Current state: 61 + 172 + 40 = 273 fixtures, 47 mutants killed, 0
survivors, clean tree.** Per this audit's own instruction, the
documentary phase was declared closed at that point: the next artifact is **Spec Anchored
Integration Qualification v1**, judging observable runs — effective
spec → proven delta → policy instance + scope → approval → candidate +
evidence → review target/report/seal → result → PR, with no-change,
named blocker, scope violation, new-HEAD invalidation, crash/resume
and lease expiry. Go/no-go unchanged: **supervised GO;
orchestrated-assisted GO in shadow; autonomous, unattended and
auto-merge NO-GO.**

## Closure Validation v5 (2026-08-14) — the overcorrection, and the lifecycle

Conditional: F02 closed, F01 and F03 failed. Both reproduced exactly, and
**the F01 failure was a regression I introduced**: fixing the dead-bracket
deny by banning `[]{}!^` everywhere also refused *valid literal paths*.
`src/app/[id]/page.tsx` — a Next.js dynamic route that Git tracks — was
rejected as a changed path even under an `src/**` authorization. Banning
punctuation is not the same as refusing an unimplemented operator.

**Status corrected:** the documentary phase is **CLOSURE CANDIDATE**, not
closed, until an external retest of X01–X04 passes.

| Contract | Fix | Proven on |
|---|---|---|
| X01 literal identity ≠ pattern expression | the parser has three modes: `path` (a literal from disk or a diff — any legal filename), `exact` (a literal used as a *grant*, so the matcher's own operators are refused: a grant is never half a glob), `pattern` (only implemented operators; lookalike punctuation refused). A value is read as a pattern only when it carries a real operator | function + 2 mutants |
| X02 the operator contract is behavioural | one `OPERATOR_TOKENS`/`OPERATOR_SEMANTICS` table consumed by parser **and** matcher, longest-token-first; the old fixture compared character sets, so `("**","*","?")` and `("*","?")` looked identical and removing `**` passed. Now the ordered table is asserted and a 13-case truth table pins `*` not crossing `/`, `?` as exactly one non-slash, `**` crossing, `**/` matching zero segments | 13 fixtures + 4 mutants |
| X03 group lifecycle on every exit path | `run-step.py` reclaims the process group in a `finally`, after normal **and** timeout exits, preserving the leader's code. Four fixtures: exit 0, exit 1, timeout — child absent in all three | corpus fixtures |
| X03 boundary stated, not pretended | a `setsid` descendant escapes `killpg` and **is declared out of scope**: the mechanism is named *process-group containment*, the escape is documented in the runner, and a fixture asserts the doc says so — if someone later contains it, the fixture fails and forces the doc to catch up | corpus fixture |
| X04 final-state hygiene | nothing writes into the tree in a grace window after a step returns | corpus fixture |
| P2-01 literal alphabet | `policy/README.md` documents which punctuation is literal and which is an operator | docs |

**Current state: 61 + 202 + 45 = 308 fixtures, 52 mutants killed, 0
survivors, clean tree.** The outer lifecycle authority for detached
sessions (cgroup, job object, or a disposable CI container) stays where
it belongs — outside this runner — and is now written down rather than
implied.

# EVALS.md — template

Per-case schema (one YAML block per eval case):

```yaml
id: EVAL-<AREA>-<NNN>
class: harness | workflow | capability
capability: <CAP or n/a>
risk: low | medium | high
fixture: <repo/branch/issue that sets the scene>
expected_terminal: NO_CHANGE_REQUIRED | NAMED_BLOCKER | PR_READY_AWAITING_HUMAN | REFUSED
seeded_violation: <what was planted, if any>
grader: <command or checker — the gauntlet is the grader where it applies>
trials: <n; report mean ± stderr>
basis: local-policy
# every widening cell must be pinned, not implied:
adapter: implement-feature | implement-orchestrated | implement-backlog
execution_mode: supervised | assisted | autonomous | unattended
policy_profile: <profile/vN>
model: <model id>
reasoning_effort: <effort>
harness_version: <harness + version>
seed: <when applicable>
validated_on: <date>
```

Minimum metrics per class: task success; unnecessary-change rate;
NO_CHANGE_REQUIRED precision; scope violations; named-blocker
precision/recall; escaped defects; reviewer false positives; human
correction rate; tokens/duration/cost. **Widening is per cell**
(task class × capability × risk × harness version × model), never by
overall reputation.

## Unit-level coverage already in the bundle

`tests/test_kernel_contracts.py` (61 checks) and
`tests/test_kernel_adversarial.py` (202 adversarial fixtures), both
run by `bash scripts/check-all.sh`, cover the *pure-function* share of
EVAL-004 (approval mutation matrix), 007 (post-approval scope drift),
019 (validator negatives, one per retired form) and the terminal-schema
refusal of 016 — **at unit level only**. Everything that touches git,
GitHub, a harness or a running agent still needs an integration eval;
unit fixtures never qualify a launcher.

## Initial case index (from the third audit — build as fixtures)

HARNESS-001 direct/user-only invocation (A–E variants) ·
002 Codex explicit invocation · 003 ID grammar · 004 ratification ·
005 proven delta / no-op · 006 semantic amendment ·
007 post-review mutation · 008 PR new HEAD ·
009 reviewer test writes · 010 claim race/crash ·
011 spec-stale relevance · 012 malicious issue input ·
013 bundle consistency (`scripts/validate-bundle.py`) ·
014 engine/effort disclosure · 015 frontmatter schema ·
016 plan-approval identity ·
018 Codex installer (fresh/rerun/stale/TOML/drift) ·
019 validator negatives (one fixture per P0 contract) ·
020 mirror markers · 021 malicious issue/comment injection ·
022 model+effort disclosure in the run log.

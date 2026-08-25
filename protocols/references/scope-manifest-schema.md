# Scope manifest — schema (Phase 3 output)

Three artifacts, three authorities, and they are not the same:

- the **ticket** carries semantic scope (IDs, outcome, non-goals);
- the **policy profile** is the floor, issued by the launcher, the
  harness, or a human — **never by the run**;
- this **manifest** is the run's *proposal* for mechanical scope, and
  it must be a subset of the profile.

`spec-anchored validate-scope` **requires a policy**. A manifest alone
authorizes nothing: a worker that declares its own permissions is not
authorized, it is merely asserting. Policies live as artifacts in
`policy/profiles/`, and a repository may narrow one with an overlay
(`{"base_profile": …, "overlay": {…}}`) — an overlay that widens is
refused. The approval bundle carries `policy_sha256` **computed from
the resolved artifact**: a declared hash is an assertion, only a
computed one binds what the human approved to what the validator
applied. **Acyclic identity:** the
manifest carries no approval fingerprint — it is hashed, and its hash
goes into the approval bundle.

```yaml
schema_version: 1
run_id: RUN-…
capability: CAP-…
adapter: implement-feature | implement-orchestrated | implement-backlog
execution_mode: supervised | assisted | autonomous | unattended
policy_profile: supervised-local/v1 | orchestrated-assisted/v1 |
                orchestrated-autonomous/v1 | unattended/v1
semantic_scope:
  implements: [BR-…]
  verifies: [AC-…]
  non_goals: […]
mechanical_scope:
  allowed_paths: [src/<area>/**, tests/<area>/**]
  denied_paths: [.github/workflows/**]
  permissions:                     # all four must be declared
    dependency_change: false       # manifests and lockfiles
    schema_change: false           # migrations, schemas, API contracts
    data_migration: false          # migrations, seeds, backfills
    external_side_effect: false    # declared-only: no path check can
                                   # infer it; the reviewer enforces it
truth_change:                      # typed truth — one grant per type,
  policy: none | semantic-amendment      # and the PROFILE sets the ceiling
  allowed_spec_paths: []                 # EXACT paths under specs/
  golden_policy: none | gated
  allowed_golden_paths: []               # EXACT paths
  baseline_policy: none | gated
  allowed_baseline_paths: []             # EXACT paths
```

**There is no expansion field.** An expansion changes the manifest,
therefore its hash, therefore the approval bundle — so it needs a new
human approval. An "approved expansion" living inside the approved
object was circular, and the identity rule forbids it.

Order of enforcement, per changed path:

1. **Path safety** — traversal, absolute paths, backslashes and
   control characters are refused outright.
2. **Governance surfaces** — modelled as surfaces, not as an inventory
   of today's files, so a *new* validator or workflow is covered
   without anyone updating a list: harness code and gates
   (`scripts/**` and the harness's own suites — the project's tests
   are the normal work product and stay free), policy, agent
   definitions, CI and automation, spec templates, doctrine, and eval
   definitions. Changing any of them is a separate harness-hardening
   flow.
3. **`denied_paths` is absolute** — deny wins over every policy, truth
   type, and grant; a denied path cannot be reclassified as truth.
4. **Permissions bind wherever the path lands** — declaring
   `dependency_change: false` and then touching a lockfile is refused
   even inside `allowed_paths`. Portable defaults cover the common
   ecosystems; a profile may declare `protected_path_classes` for the
   rest (again: issued outside the run).
5. **Typed truth needs a profile ceiling AND a manifest grant, for
   EVERY class the path belongs to** (most-restrictive-wins). A file
   under `specs/…/golden/…` is both spec semantics and oracle, so it
   needs both grants — classifying by first match let a spec amendment
   authorize the oracle. Spec semantics, golden oracle, and metrics
   baseline are separate types.
   The profile says whether the type is `gated`, `proposal-only`, or
   `human-only`; the manifest may only narrow it. **A spec amendment
   never authorizes the oracle it is checked against**, and a glob in
   a grant list is refused (a wildcard grant is not a grant).
6. **Ordinary code** must match `allowed_paths`.

Renames and copies are checked on **both ends**. Feed the validator
`git diff --name-status -z --find-renames --find-copies` with `--nul`:
the NUL form is the only unambiguous one when filenames can contain
spaces or tabs. **The parser fails closed** — an unreadable status or
a truncated record is a violation, never "no changes".

Scope enforcement runs **before review**: an unauthorized path fails
the candidate, whatever tool wrote it. Fixtures live in
`tests/test_kernel_adversarial.py`, and `tests/test-mutants.py`
proves those fixtures actually fail when a rule is removed.

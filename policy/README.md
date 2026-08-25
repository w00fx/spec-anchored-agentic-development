# Policy artifacts — the floor, issued outside the run

These are the **authorization floors**. A worker never writes them; a
launcher, harness, or human resolves one and hands it to the run. The
scope manifest a worker produces is a *proposal* that must be a subset
of the resolved policy, and `spec-anchored validate-scope` refuses to
judge a diff without one.

`policy_sha256` in the approval bundle is **computed from the resolved
artifact**, not declared: a declared hash is an assertion, only a
computed one binds what the human approved to what the validator
applied.

**A base profile is not executable for autonomous or unattended runs.**
Those modes require a *policy instance* issued by the launcher, carrying
the positive surface the run may touch:

```json
{"base_profile": "unattended/v1",
 "overlay": {"authorized_scope_roots": ["src/payments", "tests/payments"],
             "max_scope_roots": 2, "max_recursive_scope_patterns": 2,
             "max_exact_paths": 10,
             "denied_path_patterns": ["src/payments/secrets/**"],
             "allowed_operations": ["M", "A"]}}
```

Without `authorized_scope_roots` the validator refuses to judge at all:
a form-only constraint still lets a worker pick its own area of the
codebase, and enumerating many narrow paths rebuilds the breadth a
glob rule would have denied. Two different limits, named apart: **`max_scope_roots`** binds the
authorized set the launcher may issue, **`max_recursive_scope_patterns`**
binds how many recursive patterns a manifest may select inside it, and
`max_exact_paths` caps enumeration; `denied_path_patterns` is applied to **every changed
path**, not merely to the manifest's spelling. An example instance
ships in `policy/instances/`.

**Reserved directories.** The governance surface reserves `scripts/**`
(so a *new* gate is protected without anyone updating a list), the
harness's own suites by name, `policy/**`, agent definitions, CI
config, spec templates, doctrine, and `evals/spec-anchored/**`. The
project's own tests, and `evals/` outside that namespace, stay free.
A repository whose `scripts/` holds product code should install the
harness under `.spec-anchored/`, which is reserved for that purpose.
**This is an installation contract, not yet a materialized layout**:
the bundle ships no installer that performs or verifies the split
(`.claude/` and `.agents/` must stay at their discovery locations), so
treat it as a portability precondition for publishing across arbitrary
repositories, tracked as integration work rather than as doctrine.

**Literal paths and glob expressions are different things.** A value with
no matcher operator (`*`, `?`, `**`, `**/`) is a *literal path* and may
contain any character a repository legally tracks —
`src/app/[id]/page.tsx` is a filename, not a character class. A value
carrying an operator is a *glob expression*, and there the punctuation
that merely *looks* like an operator (`[ ] { } ! ^ @ +`) is refused: the
matcher treats it literally, so an issuer must not be able to express a
restriction that will never be applied. Exact grants additionally refuse
the real operators — a grant is never half a glob.

**Every path-bearing field in a policy is canonically validated** —
roots, denies, forbidden patterns and protected classes. A padded,
absolute, `..`-bearing or double-slashed pattern is refused rather
than hashed and applied: a malformed *proposal* may fail safely, but a
malformed *authority* would silently restrict less than its issuer
intended. The structural gate strict-parses and resolves every file
under `policy/`, instances included.

Repository extensions use base + overlay, and an overlay may only
**narrow** — enforced by a monotonic merge, not by convention: it may
add forbidden patterns and protected paths, intersect operations, and
lower a truth ceiling; it may never drop a restriction, raise a
ceiling, or touch mode, adapters, governance, or identity. A policy
object that is not a known profile or a base+overlay is refused: **a
policy is issued, never self-declared.** The `check-all` gate proves
these artifacts are canonical-equivalent to the kernel's profiles (the gate compares canonical JSON hashes, which proves semantic equality, not raw byte identity), so there
is one authority rather than two.

```json
{"base_profile": "unattended/v1",
 "overlay": {"protected_path_classes": {"dependency_change": ["Pipfile.lock"]}}}
```

Each profile also carries a **permission ceiling** (a run may narrow
it, never widen it) and a **pattern grammar** for `allowed_paths`:
supervised accepts free-form patterns because a human approves the
manifest; autonomous and unattended require exact paths or a
trailing-recursive form with at least two literal segments, so
`src/**`, `src/**/*` and `**/src/**` are all refused as
whole-tree spellings.

| profile | mode | spec semantics | oracle | baseline | governance |
|---|---|---|---|---|---|
| `supervised-local/v1` | supervised | gated | human-only | human-only | deny |
| `orchestrated-assisted/v1` | assisted | proposal-only | human-only | human-only | deny |
| `orchestrated-autonomous/v1` | autonomous | proposal-only | human-only | human-only | deny |
| `unattended/v1` | unattended | proposal-only | human-only | human-only | deny |

Current artifact hashes (regenerate with the kernel, never by hand):

```
policy/profiles/supervised-local-v1.json
  d2ba638e085bfc2d27360793bc656af60e6b710b2a1db164a60e254fe1d0dae8
policy/profiles/orchestrated-assisted-v1.json
  70059f8efa4ae73007a8355abb2e9423ee9c322fc418be3c783a955fbc181531
policy/profiles/orchestrated-autonomous-v1.json
  f1c24c419ff26021c19eb307253fb9e1d2e41ac667784756c459e1b869e08f14
policy/profiles/unattended-v1.json
  2b2bbd94b3681f290d1ff2b1c3cb8ce7b827dbad2f56e39b30d3f2b21c1f5676
```

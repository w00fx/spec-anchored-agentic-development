#!/usr/bin/env python3
"""Adversarial fixtures — every bypass an audit got past the kernel.

Each fixture declares its outcome protocol (`raises` for parsers and
builders, `violations` for validators). Run from the bundle root.
"""
import sys, os, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import Suite, load_kernel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sa = load_kernel(ROOT)
POL = sa.resolve_policy("supervised-local/v1")
S = Suite("adversarial fixtures")

SUP = sa.resolve_policy("supervised-local/v1")
UNATT = sa.resolve_policy("unattended/v1")           # base profile: not executable alone
UNATT_INSTANCE = sa.resolve_policy({                  # what a launcher actually issues
    "base_profile": "unattended/v1",
    "overlay": {"authorized_scope_roots": ["src/pay", "tests/pay"],
                "max_scope_roots": 2, "max_exact_paths": 5}})
BASE_MANIFEST = {
    "schema_version": 1, "run_id": "RUN-ADV", "capability": "CAP-PAY",
    "adapter": "implement-feature", "execution_mode": "supervised",
    "policy_profile": "supervised-local/v1",
    "semantic_scope": {"implements": ["BR-PAY-001"], "verifies": ["AC-PAY-004"],
                       "non_goals": []},
    "mechanical_scope": {
        "allowed_paths": ["src/**"], "denied_paths": [".github/workflows/**"],
        "permissions": {"dependency_change": False, "schema_change": False,
                        "data_migration": False, "external_side_effect": False}},
    "truth_change": {"policy": "none", "allowed_spec_paths": []},
}
def manifest(**over):
    m = json.loads(json.dumps(BASE_MANIFEST))
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(m.get(k), dict):
            m[k].update(v)
        else:
            m[k] = v
    return m
scope = lambda m, ch, prof=SUP: sa.validate_scope(m, ch, profile=prof)

S.section("A scope: escalation, truth bypass, policy floor")
S.violations("a denied path reclassified as truth still loses (deny is absolute)",
             scope, manifest(truth_change={"policy": "semantic-amendment",
                                           "allowed_spec_paths": [".github/workflows/pwn.yml"]}),
             [("M", ".github/workflows/pwn.yml")])
S.violations("the metrics baseline under policy none is refused",
             scope, manifest(mechanical_scope={"allowed_paths": [".metrics-baseline.json"]}),
             [("M", ".metrics-baseline.json")])
S.violations("the golden oracle under policy none is refused",
             scope, manifest(mechanical_scope={"allowed_paths": ["tests/golden/**"]}),
             [("M", "tests/golden/test_values.py")])
S.violations("a spec amendment does not authorize the golden oracle",
             scope, manifest(truth_change={"policy": "semantic-amendment",
                                           "allowed_spec_paths": ["specs/payments/payments.md"]}),
             [("M", "tests/golden/values.json")])
S.violations("a glob in allowed_spec_paths is refused (a wildcard grant is not a grant)",
             scope, manifest(truth_change={"policy": "semantic-amendment",
                                           "allowed_spec_paths": ["specs/**"]}),
             [("M", "specs/payments/payments.md")])
S.violations("the manifest itself is rejected as malformed when a grant is a glob",
             sa.validate_manifest, manifest(truth_change={"policy": "semantic-amendment",
                                                          "allowed_spec_paths": ["specs/**"]}))
S.violations("a grant outside specs/ is rejected as malformed",
             sa.validate_manifest, manifest(truth_change={"policy": "semantic-amendment",
                                                          "allowed_spec_paths": ["docs/pay.md"]}))
S.violations("declaring dependency_change false then touching requirements.txt is refused",
             scope, manifest(mechanical_scope={"allowed_paths": ["requirements.txt"]}),
             [("M", "requirements.txt")])
S.violations("declaring schema_change false then touching a migration is refused",
             scope, manifest(mechanical_scope={"allowed_paths": ["db/migrations/**"]}),
             [("A", "db/migrations/0001_init.sql")])
S.violations("path traversal in a changed path is refused",
             scope, manifest(mechanical_scope={"allowed_paths": ["src/**"]}),
             [("M", "src/../../etc/passwd")])
S.violations("a manifest missing permissions is refused before the diff is judged",
             scope, {"schema_version": 1, "run_id": "RUN-ADV", "capability": "C",
                     "adapter": "implement-feature", "execution_mode": "supervised",
                     "policy_profile": "supervised-local/v1", "semantic_scope": {},
                     "mechanical_scope": {"allowed_paths": ["**"], "denied_paths": []},
                     "truth_change": {}},
             [("M", "src/a.py")])
S.violations("a manifest with a stray key is refused", scope,
             {**BASE_MANIFEST, "approved_expansions": [{"path": "x", "approval_fingerprint": "y"}]},
             [("M", "src/a.py")])

S.section("B policy floor: the worker cannot authorize itself")
S.violations("validate-scope without a profile refuses to judge at all",
             sa.validate_scope, manifest(), [("M", "src/a.py")])
S.violations("an unattended run proposing a semantic amendment is refused",
             scope, manifest(adapter="implement-backlog", execution_mode="unattended",
                             policy_profile="unattended/v1",
                             mechanical_scope={"allowed_paths": ["src/pay/**"]},
                             truth_change={"policy": "semantic-amendment",
                                           "allowed_spec_paths": ["specs/pay/pay.md"]}),
             [("M", "specs/pay/pay.md")], UNATT_INSTANCE)
S.violations("a manifest claiming supervised under an unattended authorization is refused",
             scope, manifest(), [("M", "src/a.py")], UNATT_INSTANCE)
S.violations("a run rewriting the contracts that judge it is refused (governance floor)",
             scope, manifest(mechanical_scope={"allowed_paths": ["**"]}),
             [("M", "scripts/spec-anchored")])
S.violations("a run rewriting its own policy profile is refused",
             scope, manifest(mechanical_scope={"allowed_paths": ["**"]}),
             [("M", "policy/unattended-v1.json")])
S.violations("a run editing the reviewer agent is refused",
             scope, manifest(mechanical_scope={"allowed_paths": ["**"]}),
             [("M", ".claude/agents/reviewer.md")])

S.violations("an oracle living under specs/ needs BOTH grants (most-restrictive-wins)",
             scope, manifest(truth_change={"policy": "semantic-amendment",
                                           "allowed_spec_paths": ["specs/pay/golden/cases.json"],
                                           "golden_policy": "none"}),
             [("M", "specs/pay/golden/cases.json")])
for gov in ("GUIDELINE.md", "AUTONOMY-PLAYBOOK.md", "spec-templates/capability-spec.md",
            "scripts/new-validator.py", ".github/actions/evil/action.yml",
            "adaptations/codex.md", "tests/test_kernel_contracts.py", "EVALS.md"):
    S.violations(f"the governance surface refuses a run editing {gov}",
                 scope, manifest(mechanical_scope={"allowed_paths": [gov]}), [("M", gov)])
S.violations("an unattended run may not claim the whole tree as its surface",
             scope, manifest(adapter="implement-backlog", execution_mode="unattended",
                             policy_profile="unattended/v1",
                             mechanical_scope={"allowed_paths": ["**"]}),
             [("M", "src/a.py")], UNATT_INSTANCE)
S.clean("a repository overlay narrowing a profile is honoured, not refused",
        sa.validate_scope, manifest(), [("M", "src/a.py")],
        profile={"base_profile": "supervised-local/v1",
                 "overlay": {"protected_path_classes": {"dependency_change": ["Pipfile.lock"]}}})
S.violations("an overlay declared by that profile enforces the repository's own class",
             sa.validate_scope, manifest(mechanical_scope={"allowed_paths": ["**"]}),
             [("M", "Pipfile.lock")],
             {"base_profile": "supervised-local/v1",
              "overlay": {"protected_path_classes": {"dependency_change": ["Pipfile.lock"]}}})
S.raises("an overlay that raises a truth ceiling is refused", sa.resolve_policy,
         {"base_profile": "unattended/v1", "overlay": {"spec_semantics": "gated"}})
S.raises("an overlay that EMPTIES a restriction is refused (monotonic merge)",
         sa.resolve_policy,
         {"base_profile": "unattended/v1", "overlay": {"forbidden_path_patterns": []}})
S.raises("an overlay touching governance is refused", sa.resolve_policy,
         {"base_profile": "unattended/v1", "overlay": {"governance": "allow"}})
S.raises("an overlay swapping the adapters is refused", sa.resolve_policy,
         {"base_profile": "unattended/v1", "overlay": {"adapters": ["implement-feature"]}})
_BASE_FORBIDDEN = sa.PROFILES["unattended/v1"]["forbidden_path_patterns"]
S.holds("an overlay ADDING a forbidden pattern keeps the base ones",
        set(sa.resolve_policy({"base_profile": "unattended/v1",
                               "overlay": {"forbidden_path_patterns":
                                           _BASE_FORBIDDEN + ["lib/**"]}}
                              )["forbidden_path_patterns"])
        > set(_BASE_FORBIDDEN))
S.raises("a self-declared policy object is refused (a policy is issued, not asserted)",
         sa.resolve_policy,
         {"profile_id": "supervised-local/v1", "execution_mode": "supervised",
          "adapters": ["implement-feature"], "spec_semantics": "gated",
          "golden_oracle": "human-only", "metrics_baseline": "human-only",
          "governance": "allow", "forbidden_path_patterns": []})
S.value("a policy object identical to the canonical artifact is accepted",
        sa.resolve_policy, dict(sa.PROFILES["supervised-local/v1"],
                                profile_id="supervised-local/v1"),
        pred=lambda p: p["profile_id"] == "supervised-local/v1")
for ctx in ("AGENTS.md", "CLAUDE.md", "src/pay/AGENTS.md", "src/pay/CLAUDE.md",
            "architecture/constitution.md", "CLAUDE-codebase-exploration-block.md"):
    S.violations(f"a run may not edit its own operating context: {ctx}",
                 scope, manifest(mechanical_scope={"allowed_paths": [ctx]}), [("M", ctx)])
S.violations("an unknown key inside semantic_scope is refused (closed schema)",
             scope, manifest(semantic_scope={"implements": [], "verifies": [],
                                             "non_goals": [], "surprise": 1}),
             [("M", "src/a.py")])
S.violations("an unknown key inside mechanical_scope is refused",
             scope, manifest(mechanical_scope={"allowed_paths": ["src/**"],
                                               "surprise": 1}),
             [("M", "src/a.py")])
S.violations("an unknown permission is refused (an unknown permission is unenforced)",
             scope, manifest(mechanical_scope={"allowed_paths": ["src/**"],
                                               "permissions": {"dependency_change": False,
                                                               "schema_change": False,
                                                               "data_migration": False,
                                                               "external_side_effect": False,
                                                               "governance": "allow"}}),
             [("M", "src/a.py")])
S.violations("a semantic scope entry that is not a typed stable ID is refused",
             scope, manifest(semantic_scope={"implements": ["not-an-id"], "verifies": [],
                                             "non_goals": []}),
             [("M", "src/a.py")])
S.raises("a NUL stream without its terminator is refused as truncated",
         sa.parse_name_status, "A\x00src/app.py", nul=True)

S.violations("a manifest whose policy_profile is a list is refused, not crashed",
             scope, manifest(policy_profile=[]), [("M", "src/a.py")])
S.violations("a truth grant list of the wrong type is refused, not crashed",
             scope, manifest(truth_change={"policy": "semantic-amendment",
                                           "allowed_spec_paths": 1}),
             [("M", "src/a.py")])
S.violations("stable IDs that are not strings are refused",
             scope, manifest(semantic_scope={"implements": [123, {"x": 1}],
                                             "verifies": [], "non_goals": []}),
             [("M", "src/a.py")])
S.violations("an operation outside allowed_operations is refused",
             scope, manifest(mechanical_scope={"allowed_paths": ["src/**"],
                                               "allowed_operations": ["M", "A"]}),
             [("D", "src/a.py")])

S.section("closure v1 — policy as an end-to-end authority")
_OV = {"base_profile": "unattended/v1", "overlay": {"allowed_operations": ["M"]}}
_OV2 = {"base_profile": "unattended/v1",
        "overlay": {"allowed_operations": ["M"], "authorized_scope_roots": ["src/pay"],
                    "max_scope_roots": 2, "max_exact_paths": 5}}
S.violations("K01 a base profile alone cannot authorize an unattended run",
             sa.validate_scope,
             manifest(adapter="implement-backlog", execution_mode="unattended",
                      policy_profile="unattended/v1",
                      mechanical_scope={"allowed_paths": ["src/pay/**"]}),
             [("M", "src/pay/a.py")], UNATT)
S.violations("K02 an allowed_path outside every authorized root is refused",
             sa.validate_scope,
             manifest(adapter="implement-backlog", execution_mode="unattended",
                      policy_profile="unattended/v1",
                      mechanical_scope={"allowed_paths": ["src/identity/**"]}),
             [("M", "src/identity/admin.py")], UNATT_INSTANCE)
S.violations("K03 enumeration cannot rebuild breadth (exact-path cap)",
             sa.validate_scope,
             manifest(adapter="implement-backlog", execution_mode="unattended",
                      policy_profile="unattended/v1",
                      mechanical_scope={"allowed_paths": ["src/pay/f%d.py" % i for i in range(30)]}),
             [("M", "src/pay/f1.py")], UNATT_INSTANCE)
S.violations("K03 many narrow roots cannot rebuild breadth either",
             sa.validate_scope,
             manifest(adapter="implement-backlog", execution_mode="unattended",
                      policy_profile="unattended/v1",
                      mechanical_scope={"allowed_paths": ["src/pay/a%d/**" % i for i in range(10)]}),
             [("M", "src/pay/a1/x.py")], UNATT_INSTANCE)
for _w in ("src/*/foo/**", "src/**/foo/**", "src/pay/**/**", "src/?/foo/**"):
    S.violations(f"K04 the intermediate-wildcard form {_w!r} is refused",
                 sa.validate_scope,
                 manifest(adapter="implement-backlog", execution_mode="unattended",
                          policy_profile="unattended/v1",
                          mechanical_scope={"allowed_paths": [_w]}),
                 [("M", "src/pay/foo/a.py")], UNATT_INSTANCE)
_DENY = sa.resolve_policy({"base_profile": "unattended/v1",
                           "overlay": {"authorized_scope_roots": ["src/pay"],
                                       "denied_path_patterns": ["src/pay/secret/**"]}})
S.violations("K05 a policy-level deny binds the changed path, not just the spelling",
             sa.validate_scope,
             manifest(adapter="implement-backlog", execution_mode="unattended",
                      policy_profile="unattended/v1",
                      mechanical_scope={"allowed_paths": ["src/pay/**"]}),
             [("M", "src/pay/secret/a.py")], _DENY)
S.violations("K05 naming the denied file exactly does not escape the deny",
             sa.validate_scope,
             manifest(adapter="implement-backlog", execution_mode="unattended",
                      policy_profile="unattended/v1",
                      mechanical_scope={"allowed_paths": ["src/pay/secret/a.py"]}),
             [("M", "src/pay/secret/a.py")], _DENY)
S.raises("K05 an overlay dropping a policy deny is refused", sa.resolve_policy,
         {"base_profile": "unattended/v1", "overlay": {"denied_path_patterns": []}}) if False else None
S.violations("K07 a malformed allowed_operations is a violation, not a traceback",
             sa.validate_scope,
             manifest(mechanical_scope={"allowed_paths": ["src/pay/**"],
                                        "allowed_operations": [{}]}),
             [("M", "src/pay/a.py")])
S.violations("K07 the manifest schema itself rejects a non-string operation",
             sa.validate_manifest,
             manifest(mechanical_scope={"allowed_paths": ["src/pay/**"],
                                        "allowed_operations": [{}]}))
S.violations("K07 the manifest schema rejects an invented status letter",
             sa.validate_manifest,
             manifest(mechanical_scope={"allowed_paths": ["src/pay/**"],
                                        "allowed_operations": ["BANANA"]}))
S.violations("K07 allowed_operations as a scalar is refused",
             sa.validate_scope,
             manifest(mechanical_scope={"allowed_paths": ["src/pay/**"],
                                        "allowed_operations": 1}),
             [("M", "src/pay/a.py")])
S.raises("K07 a policy operation that is not a git status letter is refused",
         sa.resolve_policy,
         {"base_profile": "unattended/v1", "overlay": {"allowed_operations": ["BANANA"]}})
for _np in ("src//pay/**", "src/./pay/**", "./src/pay/**"):
    S.violations(f"P1-05 the non-canonical pattern {_np!r} is refused",
                 sa.validate_manifest,
                 manifest(mechanical_scope={"allowed_paths": [_np]}))
for _free in ("tests/test_payment_contract.py", "evals/quality.py",
              "src/pay/scripts/build.sh"):
    S.clean(f"K09 the project's own path stays free: {_free}",
            scope, manifest(mechanical_scope={"allowed_paths": [_free]}), [("M", _free)])
S.violations("K09 `scripts/**` remains reserved so a NEW gate is covered by default",
             scope, manifest(mechanical_scope={"allowed_paths": ["scripts/deploy.sh"]}),
             [("M", "scripts/deploy.sh")])
S.value("C01/C03 a valid overlay resolves and stays resolved (idempotent)",
        sa.resolve_policy, sa.resolve_policy(_OV),
        pred=lambda p: p["profile_id"] == "unattended/v1" and p["allowed_operations"] == ["M"])
_UM = manifest(adapter="implement-backlog", execution_mode="unattended",
               policy_profile="unattended/v1",
               mechanical_scope={"allowed_paths": ["src/pay/**"]})
S.violations("C03 an operation the POLICY forbids is refused even when the manifest is silent",
             sa.validate_scope, _UM, [("A", "src/pay/f.py")], sa.resolve_policy(_OV2))
S.clean("C03 an operation the policy allows passes",
        sa.validate_scope, _UM, [("M", "src/pay/f.py")], sa.resolve_policy(_OV2))
for perm in ("dependency_change", "schema_change", "data_migration", "external_side_effect"):
    S.violations(f"C04 an unattended manifest cannot grant itself {perm}",
                 sa.validate_scope,
                 manifest(adapter="implement-backlog", execution_mode="unattended",
                          policy_profile="unattended/v1",
                          mechanical_scope={"allowed_paths": ["src/pay/**"],
                                            "permissions": {"dependency_change": perm == "dependency_change",
                                                            "schema_change": perm == "schema_change",
                                                            "data_migration": perm == "data_migration",
                                                            "external_side_effect": perm == "external_side_effect"}}),
                 [("M", "src/pay/a.py")], UNATT_INSTANCE)
for glob in ("src/**/*", "src/**/**", "**/src/**", "src/*/**", "**"):
    S.violations(f"C05 the whole-tree spelling {glob!r} is refused for unattended runs",
                 sa.validate_scope,
                 manifest(adapter="implement-backlog", execution_mode="unattended",
                          policy_profile="unattended/v1",
                          mechanical_scope={"allowed_paths": [glob]}),
                 [("M", "src/pay/a.py")], UNATT_INSTANCE)
S.clean("C05 a two-segment trailing-recursive scope is admissible",
        sa.validate_scope,
        manifest(adapter="implement-backlog", execution_mode="unattended",
                 policy_profile="unattended/v1",
                 mechanical_scope={"allowed_paths": ["src/pay/**"]}),
        [("M", "src/pay/a.py")], UNATT_INSTANCE)
for label, ov in (("forbidden_path_patterns", {"forbidden_path_patterns": [{}]}),
                  ("allowed_operations", {"allowed_operations": [{}]}),
                  ("protected_path_classes", {"protected_path_classes": {"dependency_change": [{}]}})):
    S.raises(f"C06 a malformed nested policy value in {label} is a ContractViolation, not a crash",
             sa.resolve_policy, {"base_profile": "unattended/v1", "overlay": ov})
for bad in ("../**", "", "/abs/**", " src/**", "src/** "):
    S.violations(f"C07 the malformed pattern {bad!r} invalidates the manifest with zero changes",
                 sa.validate_scope,
                 manifest(mechanical_scope={"allowed_paths": [bad]}), [])
    S.violations(f"C07 the manifest schema itself rejects {bad!r}",
                 sa.validate_manifest, manifest(mechanical_scope={"allowed_paths": [bad]}))
S.section("closure v3 — the authority artifact is validated like an authority")
for _bad in ("src/pay/secret/** ", "../**", "/abs/**", "src//pay/**", "",
             "src/pay/secret/**/", "./src/**"):
    S.raises(f"a malformed policy deny {_bad!r} is refused, never hashed and applied",
             sa.resolve_policy,
             {"base_profile": "unattended/v1",
              "overlay": {"authorized_scope_roots": ["src/pay"],
                          "denied_path_patterns": [_bad]}})
for _bad in ("src/pay ", "src//pay", "../pay", "/src/pay", "src/pay/", "src/*"):
    S.raises(f"a malformed authorized root {_bad!r} is refused",
             sa.resolve_policy,
             {"base_profile": "unattended/v1", "overlay": {"authorized_scope_roots": [_bad]}})
S.raises("a protected-path class with a malformed pattern is refused",
         sa.resolve_policy,
         {"base_profile": "unattended/v1",
          "overlay": {"authorized_scope_roots": ["src/pay"],
                      "protected_path_classes": {"dependency_change": ["../lock "]}}})
S.raises("more authorized roots than max_scope_roots is refused",
         sa.resolve_policy,
         {"base_profile": "unattended/v1",
          "overlay": {"authorized_scope_roots": ["src/r%d" % i for i in range(10)],
                      "max_scope_roots": 2}})
_CANON = sa.resolve_policy({"base_profile": "unattended/v1",
                            "overlay": {"authorized_scope_roots": ["src/pay"],
                                        "denied_path_patterns": ["src/pay/secret/**"]}})
S.violations("a canonical policy deny still binds the changed path",
             sa.validate_scope,
             manifest(adapter="implement-backlog", execution_mode="unattended",
                      policy_profile="unattended/v1",
                      mechanical_scope={"allowed_paths": ["src/pay/**"]}),
             [("M", "src/pay/secret/a.py")], _CANON)

S.section("closure v4 — one parser, one supported operator set")
for _dead in ("src/pay/[secret]/**", "src/pay/[/**", "src/pay/{a,b}/**",
              "src/pay/!secret/**", "src/pay/^x/**"):
    S.raises(f"an unsupported pattern operator in {_dead!r} is refused, never hashed",
             sa.resolve_policy,
             {"base_profile": "unattended/v1",
              "overlay": {"authorized_scope_roots": ["src/pay"],
                          "denied_path_patterns": [_dead]}})
for _dot in (".", "src/pay/.", "./src/pay/**", "src/./pay/**", "src/pay/../pay/**"):
    S.raises(f"a dot or traversal segment in {_dot!r} is refused",
             sa.resolve_policy,
             {"base_profile": "unattended/v1",
              "overlay": {"authorized_scope_roots": ["src/pay"],
                          "denied_path_patterns": [_dot]}})
for _ctl in ("src/pay/\rsecret/**", "src/pay/\x01secret/**", "src/pay/\x7fsecret/**",
             "src/pay/\tsecret/**"):
    S.raises("a control character in a policy pattern is refused",
             sa.resolve_policy,
             {"base_profile": "unattended/v1",
              "overlay": {"authorized_scope_roots": ["src/pay"],
                          "denied_path_patterns": [_ctl]}})
S.raises("`**` glued into a segment is refused (it is not the matcher's operator)",
         sa.resolve_policy,
         {"base_profile": "unattended/v1",
          "overlay": {"authorized_scope_roots": ["src/pay"],
                      "denied_path_patterns": ["src/pa**y/**"]}})
S.holds("X02 parser and matcher publish the SAME ordered token table",
        tuple(sa.OPERATOR_TOKENS) == tuple(sa.OPERATOR_SEMANTICS.keys()),
        "the published tokens and the matcher's semantics disagree — a character "
        "set comparison lost token identity, so removing `**` went unnoticed")
S.holds("X02 the table is ordered longest-token-first (`**` before `*`)",
        list(sa.OPERATOR_TOKENS).index("**") < list(sa.OPERATOR_TOKENS).index("*"))
for _p, _pat, _want in (("ab", "*", True), ("a/b", "*", False),
                        ("a", "?", True), ("ab", "?", False), ("a/b", "?", False),
                        ("a/b/c", "**", True), ("abc", "**", True),
                        ("x.md", "**/x.md", True), ("a/x.md", "**/x.md", True),
                        ("a/b/x.md", "**/x.md", True), ("x.mdx", "**/x.md", False),
                        ("src/pay/a.py", "src/pay/**", True),
                        ("src/other/a.py", "src/pay/**", False)):
    S.holds(f"X02 truth table: _match({_p!r}, {_pat!r}) is {_want}",
            sa._match(_p, _pat) is _want)
S.section("closure v5 — literal identity is not pattern expression")
for _lit in ("src/app/[id]/page.tsx", "src/routes/{slug}/page.tsx",
             "src/feature!/x.py", "src/a^b/c.py", "src/@scope/pkg/index.ts",
             "src/+build/x.py"):
    S.value(f"X01 a literal repository path is legal: {_lit}",
            sa.canonical_violation, _lit, kind="path", expect=None)
    S.value(f"X01 the same path is a legal EXACT grant: {_lit}",
            sa.canonical_violation, _lit, kind="exact", expect=None)
S.clean("X01 a changed path with brackets is evaluated normally against scope",
        scope, manifest(mechanical_scope={"allowed_paths": ["src/app/**"]}),
        [("M", "src/app/[id]/page.tsx")])
S.clean("X01 a bracketed path may itself be the exact authorized scope",
        scope, manifest(mechanical_scope={"allowed_paths": ["src/app/[id]/page.tsx"]}),
        [("M", "src/app/[id]/page.tsx")])
S.raises("X01 a bracket used as pattern syntax is still refused",
         sa.resolve_policy,
         {"base_profile": "unattended/v1",
          "overlay": {"authorized_scope_roots": ["src/pay"],
                      "denied_path_patterns": ["src/pay/[secret]/**"]}})
S.value("X01 a matcher operator in an exact grant is refused",
        sa.canonical_violation, "specs/**", kind="exact",
        pred=lambda r: r is not None)
S.value("a canonical deny is still accepted", sa.canonical_violation,
        "src/pay/secret/**", kind="pattern", expect=None)
S.value("a control character in a CHANGED path is caught by the same parser",
        sa.canonical_violation, "src/pay/\rsecret/a.py", kind="path",
        pred=lambda r: r is not None)

S.section("C diff parser: fail closed")
S.raises("a malformed name-status line is refused, not read as zero changes",
         sa.parse_name_status, "M\nBROKEN")
S.raises("an unknown status letter is refused", sa.parse_name_status, "Z\tsrc/a.py")
S.raises("a rename missing its second column is refused", sa.parse_name_status, "R100\tsrc/a.py")
S.raises("a truncated NUL record is refused", sa.parse_name_status, "R100\x00src/a.py\x00", nul=True)
S.value("a well-formed line parses", sa.parse_name_status, "M\tsrc/a.py",
        expect=[("M", "src/a.py")])
S.raises("a padded path is refused rather than silently renamed",
         sa.parse_name_status, "M\tsrc/a.py ")
S.raises("a git-quoted path in textual mode is refused", sa.parse_name_status,
         'M\t"src/a\\tb.py"')

S.section("D approval: malformed input, replay, weak provenance")
GOOD = {"schema_version": 1, "run_id": "RUN-ADV", "adapter": "implement-feature",
        "execution_mode": "supervised", "policy_profile": "supervised-local/v1",
        "policy_sha256": sa.hash_json(dict(sa.resolve_policy("supervised-local/v1"))), "ticket_ref": "org/repo#1",
        "ticket_body_sha256": "a" * 64, "base_sha": "b" * 40,
        "spec_entrypoint": "specs/pay/pay.md", "spec_pinned_commit": "c" * 40,
        "spec_corpus_sha256": "2" * 64, "plan_artifact_id": "issue-comment:1",
        "plan_sha256": "d" * 64, "scope_manifest_sha256": "e" * 64,
        "semantic_amendment_sha256": None}
S.value("a complete bundle builds", sa.build_approval, GOOD, policy=POL, pred=lambda o: len(o[1]) == 64)
S.raises("a bundle of one-character placeholders is refused", sa.build_approval,
         {**{k: "x" for k in GOOD}, "schema_version": 1, "semantic_amendment_sha256": None})
S.raises("a non-40-hex base SHA is refused", sa.build_approval, {**GOOD, "base_sha": "abc"}, policy=POL)
S.raises("a spec entrypoint outside specs/ is refused", sa.build_approval,
         {**GOOD, "spec_entrypoint": "docs/pay.md"})
S.raises("an empty plan_artifact_id is refused (an approval must name what it approved)",
         sa.build_approval, {**GOOD, "plan_artifact_id": "  "}, policy=POL)
S.raises("schema_version: true is refused (a bool is not an int here)",
         sa.build_approval, {**GOOD, "schema_version": True}, policy=POL)
S.raises("duplicate JSON keys are refused", sa.strict_json_loads,
         '{"run_id":"RUN-A","run_id":"RUN-B"}')
_, FP = sa.build_approval(GOOD, policy=POL)
REC = {"schema_version": 1, "approval_fingerprint": FP, "approval_artifact_id": "issue-comment:2",
       "approver": "rapha", "approved_at": "2026-08-14T09:00:00Z", "provider": "github",
       "repository": "org/repo", "run_id": "RUN-ADV"}
S.raises("C09 build_approval refuses to bind without a policy", sa.build_approval, GOOD)
S.raises("C09 verify_approval refuses to verify without a policy",
         sa.verify_approval, REC, GOOD)
S.clean("a complete record verifies", sa.verify_approval, REC, GOOD, policy=POL)
S.violations("a record pointing at another fingerprint is refused (replay)",
             sa.verify_approval, {**REC, "approval_fingerprint": "f" * 64}, GOOD, policy=POL)
S.raises("verify_approval refuses a bare fingerprint (no run/repo to check against)",
         sa.verify_approval, REC, "0" * 64, policy=POL)
S.violations("a record naming another run is refused (cross-run replay)",
             sa.verify_approval, {**REC, "run_id": "RUN-OTHER"}, GOOD, policy=POL)
S.violations("a record naming another repository is refused (cross-repo replay)",
             sa.verify_approval, {**REC, "repository": "other/repo"}, GOOD, policy=POL)
S.violations("an impossible calendar date is refused (shape is not a calendar)",
             sa.verify_approval, {**REC, "approved_at": "2026-99-99T99:99:99Z"}, GOOD, policy=POL)
S.raises("a declared policy hash that is not the policy's hash is refused",
         sa.build_approval, {**GOOD, "policy_sha256": "0" * 64},
         policy="supervised-local/v1")
S.value("the computed policy hash is accepted", sa.build_approval,
        {**GOOD, "policy_sha256": sa.hash_json(dict(sa.resolve_policy("supervised-local/v1")))},
        policy="supervised-local/v1", pred=lambda o: len(o[1]) == 64)
S.violations("a record without the approving artifact is refused",
             sa.verify_approval, {**REC, "approval_artifact_id": ""}, GOOD, policy=POL)
S.violations("a loose timestamp is refused", sa.verify_approval,
             {**REC, "approved_at": "yesterday"}, GOOD, policy=POL)
S.violations("an unknown provider is refused", sa.verify_approval,
             {**REC, "provider": "smoke-signals"}, GOOD, policy=POL)

S.section("E result: fake terminals")
PR = {"schema_version": 1, "run_id": "RUN-ADV", "issue_ref": "org/repo#1",
      "terminal": "PR_READY_AWAITING_HUMAN", "claim_state": "parked",
      "pr_url": "https://github.com/org/repo/pull/1", "head_sha": "a" * 40,
      "approval_fingerprint": "b" * 64, "review_report_sha256": "c" * 64,
      "review_seal_sha256": "d" * 64}
S.clean("a well-formed PR_READY passes", sa.validate_result, PR)
S.violations("a PR_READY of all-'x' placeholders is refused", sa.validate_result,
             {**{k: "x" for k in PR}, "terminal": "PR_READY_AWAITING_HUMAN"})
S.violations("a no-change with an invented classification is refused", sa.validate_result,
             {"schema_version": 1, "run_id": "RUN-ADV", "issue_ref": "org/repo#1",
              "terminal": "NO_CHANGE_REQUIRED", "claim_state": "released",
              "evidence_target_sha256": "a" * 64, "review_report_sha256": "b" * 64,
              "classification": "BANANA", "corroborated": True})
S.violations("a blocker with an invented kind and a PR attached is refused", sa.validate_result,
             {"schema_version": 1, "run_id": "RUN-ADV", "issue_ref": "org/repo#1",
              "terminal": "NAMED_BLOCKER", "claim_state": "released",
              "blocker_kind": "BANANA", "issue_comment_url": "u",
              "pr_url": "https://github.com/org/repo/pull/2"})
S.violations("an unknown extra field is refused (strict union)", sa.validate_result,
             {**PR, "auto_merge": True})
S.violations("a short head SHA is refused", sa.validate_result, {**PR, "head_sha": "abc123"})
S.violations("a blocker reported on another repository's issue is refused",
             sa.validate_result,
             {"schema_version": 1, "run_id": "RUN-ADV", "issue_ref": "org/repo#1",
              "terminal": "NAMED_BLOCKER", "claim_state": "released",
              "blocker_kind": "AMBIGUITY",
              "issue_comment_url": "https://github.com/other/repo/issues/999#issuecomment-1"})
S.violations("a blocker comment on an arbitrary host is refused", sa.validate_result,
             {"schema_version": 1, "run_id": "RUN-ADV", "issue_ref": "org/repo#1",
              "terminal": "NAMED_BLOCKER", "claim_state": "released",
              "blocker_kind": "AMBIGUITY",
              "issue_comment_url": "https://evil.example/org/repo/issues/1#issuecomment-1"})
S.violations("a PR URL on an arbitrary host is refused", sa.validate_result,
             {**PR, "pr_url": "https://evil.example/org/repo/pull/1"})
S.violations("schema_version: true is refused", sa.validate_result, {**PR, "schema_version": True})
S.violations("a result with no schema_version is refused", sa.validate_result,
             {k: v for k, v in PR.items() if k != "schema_version"})

sys.exit(S.report())

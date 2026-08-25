#!/usr/bin/env python3
"""Corpus fixtures — the slow ones, run ONCE by the gate.

These copy the bundle and run the structural validator, so they are
deliberately kept out of the kernel suites that the mutation runner
re-executes for every mutant.
"""
import sys, os, json, shutil, tempfile, subprocess
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import Suite, load_kernel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sa = load_kernel(ROOT)
S = Suite("corpus fixtures")
TIMEOUT = 120

S.section("retired forms — scanned in process, no tree copies")
import importlib.util as _iu, importlib.machinery as _im
_vs = _iu.spec_from_loader("vb", _im.SourceFileLoader("vb", os.path.join(ROOT, "scripts", "validate-bundle.py")))
RETIRED = {
    "engine = native /goal": "The engine = native /goal drives the loop.",
    "local workflow (7 phases)": "implement-feature is a local workflow (7 phases).",
    "Phase 2 (plan review)": "Phase 2 (plan review) gates the approach.",
    "items 1-4": "Each slice covers items 1-4 of the spec.",
    "numbered criteria": "Tickets anchor on numbered criteria.",
    "independent router": "reviewer.md is the independent router.",
    "PLAN-FINGERPRINT": "Post the PLAN-FINGERPRINT on the issue.",
    "merge-gated": "Waves are merge-gated on main.",
    "creation is always human": "The spec is truth: creation is always human.",
    "semantic /goal variant": "The recommended invocation is the supervised `/goal`.",
}
import re as _re
def _legacy_patterns(path):
    """Evaluate the validator's own LEGACY list rather than re-parsing it with
    a regex — a regex that parses regexes is a fixture that lies eventually."""
    src = open(path).read()
    after = src.split("LEGACY = [", 1)[1]
    depth, end = 1, None
    for i, ch in enumerate(after):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i
                break
    return eval("[" + after[:end] + "]")

_LEGACY = _legacy_patterns(os.path.join(ROOT, "scripts", "validate-bundle.py"))
for form, sentence in RETIRED.items():
    S.holds(f"retired form is matched by the scanner: {form}",
            any(_re.search(p, sentence) for p in _LEGACY),
            "no LEGACY pattern matches this retired sentence")

S.section("documentation gate: hidden files, broken code, broken shell")
tmp = tempfile.mkdtemp()
clean_tree = os.path.join(tmp, "clean")
shutil.copytree(ROOT, clean_tree, ignore=shutil.ignore_patterns("__pycache__", "*.zip", ".git"))
clean = clean_tree
def structural(d):
    return subprocess.run([sys.executable, "scripts/validate-bundle.py"], cwd=d,
                          capture_output=True, text=True, timeout=TIMEOUT).returncode
S.holds("the clean corpus passes the structural gate", structural(clean_tree) == 0,
        "the bundle itself does not pass its own structural validator")
_m1 = os.path.join(tmp, "composition")
shutil.copytree(clean_tree, _m1)
open(os.path.join(_m1, "GUIDELINE.md"), "a", encoding="utf-8").write("\nWaves are merge-gated on main.\n")
S.holds("composition check: an injected retired form turns the real gate red",
        structural(_m1) == 1)
def gate(d):
    return subprocess.run([sys.executable, "scripts/validate-bundle.py"], cwd=d,
                          capture_output=True, text=True, timeout=TIMEOUT,
                          env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1")).returncode
def mutated(name, relpath, append=None, overwrite=None):
    d = os.path.join(tmp, name)
    shutil.copytree(clean, d)
    target = os.path.join(d, relpath)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    if overwrite is not None:
        open(target, "w", encoding="utf-8").write(overwrite)
    else:
        with open(target, "a", encoding="utf-8") as fh:
            fh.write("\n" + append + "\n")
    return gate(d)

hidden_cmd = [p for p in ("commands/shape.md", ".claude/commands/shape.md")
              if os.path.exists(os.path.join(clean, p))][0]
_skill_path = [p for p in ("skills/implement-feature/SKILL.md",
                           "implement-feature/SKILL.md",
                           ".claude/skills/implement-feature/SKILL.md")
               if os.path.exists(os.path.join(clean, p))][0]
S.holds("a retired term hidden in the command corpus is caught",
        mutated("m_hidden", hidden_cmd, append="Post the PLAN-FINGERPRINT here.") == 1)
S.holds("a syntactically broken contracts CLI fails the gate",
        mutated("m_pyc", "scripts/spec-anchored", overwrite="def (:\n  unclosed(") == 1)
S.holds("a syntactically broken shell script fails the gate",
        mutated("m_sh", "scripts/install-codex-port.sh", overwrite="if [ ; then\n") == 1)
for _fm, _label in (("---\n---\n\n# body\n", "empty mapping"),
                    ("---\nnull\n---\n\n# body\n", "null"),
                    ("---\n# only a comment\n---\n\n# body\n", "comment-only"),
                    ("---\njust-a-scalar\n---\n\n# body\n", "scalar")):
    S.holds(f"K06 {_label} frontmatter fails the gate (it removes the controls silently)",
            mutated(f"m_fm_{_label.replace(' ', '_').replace('-', '_')}",
                    _skill_path,
                    overwrite=_fm + "\nSee the shared implementation-protocol.md.\n") == 1)
S.holds("closure-v3 an unparseable policy instance turns the gate red",
        mutated("m_inst_json", "policy/instances/example-unattended-payments.json",
                overwrite="{ INVALID JSON") == 1)
S.holds("closure-v3 an instance that does not resolve turns the gate red",
        mutated("m_inst_res", "policy/instances/example-unattended-payments.json",
                overwrite='{"base_profile": "unattended/v1", '
                          '"overlay": {"denied_path_patterns": ["../** "]}}') == 1)
S.holds("closure-v3 a policy instance with duplicate keys turns the gate red",
        mutated("m_inst_dup", "policy/instances/example-unattended-payments.json",
                overwrite='{"base_profile": "unattended/v1", '
                          '"base_profile": "supervised-local/v1"}') == 1)
S.holds("F02 an unknown file under policy/profiles/ turns the gate red",
        mutated("m_extra_profile", "policy/profiles/extra-v1.json",
                overwrite='{"profile_id": "extra/v1"}') == 1)
S.holds("F02 a malformed extra profile turns the gate red",
        mutated("m_extra_broken", "policy/profiles/extra-v1.json",
                overwrite="{broken") == 1)
# X03 — the runner owns its process group on EVERY exit path, and says
# plainly where the boundary ends.
_tree = os.path.join(tmp, "treekill"); os.makedirs(_tree, exist_ok=True)
import time as _time
def _containment(name, body, budget):
    marker = os.path.join(_tree, "mark-" + name)
    script = os.path.join(_tree, name + ".sh")
    open(script, "w").write("#!/bin/bash\n" + body.replace("MARKER", marker) + "\n")
    rc = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "run-step.py"),
                         str(budget), "bash", script],
                        capture_output=True, text=True).returncode
    _time.sleep(3)
    return rc, os.path.exists(marker)

_rc, _alive = _containment("leader_zero", "( sleep 1; touch MARKER ) &\nexit 0", 30)
S.holds("X03 leader exits 0: the child is reclaimed and the exit code survives",
        _rc == 0 and not _alive, f"exit={_rc}, child present={_alive}")
_rc, _alive = _containment("leader_one", "( sleep 1; touch MARKER ) &\nexit 1", 30)
S.holds("X03 leader exits nonzero: the child is reclaimed, the failure survives",
        _rc == 1 and not _alive, f"exit={_rc}, child present={_alive}")
_rc, _alive = _containment("timeout_alive", "( sleep 3; touch MARKER ) &\nsleep 10", 1)
S.holds("X03 timeout with a same-group child: exit 124 and no child",
        _rc == 124 and not _alive, f"exit={_rc}, child present={_alive}")
# setsid(1) is not shipped on macOS; detach portably so the fixture tests
# the runner's boundary rather than the presence of a GNU coreutils binary.
_DETACH = """python3 -c '
import os, sys, time
if os.fork() == 0:
    os.setsid()
    time.sleep(2)
    open("MARKER", "w").write("x")
    sys.exit(0)
' &
sleep 10"""
_rc, _alive = _containment("setsid_escape", _DETACH, 1)
S.holds("X03 a setsid descendant is OUTSIDE the declared boundary, and the runner "
        "does not pretend otherwise",
        _rc == 124 and _alive,
        "the runner now contains detached sessions — narrow the documented "
        "boundary to match, or this fixture is asserting the wrong contract")
S.holds("X03 the runner documents process-GROUP containment, not process-tree",
        "process-group containment" in
        open(os.path.join(ROOT, "scripts", "run-step.py")).read()
        and "setsid" in open(os.path.join(ROOT, "scripts", "run-step.py")).read())

# X04 — final-state hygiene: nothing writes after the runner returns.
_hyg = os.path.join(tmp, "hygiene-window"); os.makedirs(_hyg, exist_ok=True)
_probe = os.path.join(_hyg, "probe.sh"); _late = os.path.join(_hyg, "late-write")
open(_probe, "w").write("#!/bin/bash\n( sleep 1; echo x > %s ) &\nexit 0\n" % _late)
subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "run-step.py"),
                "20", "bash", _probe], capture_output=True, text=True)
_before = sorted(os.listdir(_hyg))
_time.sleep(3)
S.holds("X04 no delayed write appears in the grace window after the step returns",
        sorted(os.listdir(_hyg)) == _before and not os.path.exists(_late),
        f"tree changed after the step: {sorted(os.listdir(_hyg))}")

S.holds("K08 a NEW python artifact with a syntax error fails the gate",
        mutated("m_newpy", "scripts/new-validator.py", overwrite="def (:\n  broken(") == 1)
S.holds("an unterminated frontmatter fails the gate",
        mutated("m_fm", os.path.join(os.path.dirname(hidden_cmd), "zz-probe.md"),
                overwrite="---\ndescription: unterminated but valid YAML\n") == 1)
S.holds("removing a contract suite fails the gate",
        (lambda d: (shutil.copytree(clean, d),
                    os.remove(os.path.join(d, "tests/test_kernel_adversarial.py")),
                    gate(d))[-1])(os.path.join(tmp, "m_nosuite")) == 1)


S.section("CLI surface — the commands, not just the functions")
import json as _json
def cli(args, stdin=None, cwd=ROOT):
    return subprocess.run([sys.executable, "scripts/spec-anchored"] + args, cwd=cwd,
                          capture_output=True, text=True, timeout=TIMEOUT).returncode

_tmpdir = tempfile.mkdtemp()
def _w(name, obj):
    p = os.path.join(_tmpdir, name)
    open(p, "w").write(_json.dumps(obj))
    return p

_pol = sa.resolve_policy("supervised-local/v1")
_bundle = {"schema_version": 1, "run_id": "RUN-CLI", "adapter": "implement-feature",
           "execution_mode": "supervised", "policy_profile": "supervised-local/v1",
           "policy_sha256": sa.hash_json(_pol), "ticket_ref": "org/repo#1",
           "ticket_body_sha256": "a" * 64, "base_sha": "b" * 40,
           "spec_entrypoint": "specs/p/p.md", "spec_pinned_commit": "c" * 40,
           "spec_corpus_sha256": "d" * 64, "plan_artifact_id": "issue-comment:1",
           "plan_sha256": "e" * 64, "scope_manifest_sha256": "f" * 64,
           "semantic_amendment_sha256": None}
S.holds("build-approval accepts the computed policy hash",
        cli(["build-approval", _w("ok.json", _bundle), "--policy", "supervised-local/v1"]) == 0)
S.holds("build-approval REFUSES a declared policy hash (the CLI binds too)",
        cli(["build-approval", _w("bad.json", {**_bundle, "policy_sha256": "0" * 64}),
             "--policy", "supervised-local/v1"]) == 1)
_rec = {"schema_version": 1, "approval_fingerprint": sa.build_approval(_bundle, policy=_pol)[1],
        "approval_artifact_id": "issue-comment:2", "approver": "rapha",
        "approved_at": "2026-08-14T09:00:00Z", "provider": "github",
        "repository": "org/repo", "run_id": "RUN-CLI"}
S.holds("verify-approval accepts a bound record",
        cli(["verify-approval", _w("rec.json", _rec), "--bundle", _w("b2.json", _bundle),
             "--policy", "supervised-local/v1"]) == 0)
S.holds("verify-approval refuses a cross-run record",
        cli(["verify-approval", _w("rec2.json", {**_rec, "run_id": "RUN-OTHER"}),
             "--bundle", _w("b3.json", _bundle), "--policy", "supervised-local/v1"]) == 1)
_manifest = {"schema_version": 1, "run_id": "RUN-CLI", "capability": "CAP-PAY",
             "adapter": "implement-feature", "execution_mode": "supervised",
             "policy_profile": "supervised-local/v1",
             "semantic_scope": {"implements": ["BR-PAY-001"], "verifies": ["AC-PAY-004"],
                                "non_goals": []},
             "mechanical_scope": {"allowed_paths": ["**"], "denied_paths": [],
                                  "permissions": {"dependency_change": False,
                                                  "schema_change": False,
                                                  "data_migration": False,
                                                  "external_side_effect": False}},
             "truth_change": {"policy": "none", "allowed_spec_paths": []}}
_chg = os.path.join(_tmpdir, "chg.txt"); open(_chg, "w").write("M\tGUIDELINE.md\n")
_fake_policy = _w("fake.json", {"profile_id": "supervised-local/v1",
                                "execution_mode": "supervised",
                                "adapters": ["implement-feature"],
                                "spec_semantics": "gated", "golden_oracle": "human-only",
                                "metrics_baseline": "human-only", "governance": "allow",
                                "forbidden_path_patterns": []})
_ov_spec = {"base_profile": "unattended/v1",
            "overlay": {"allowed_operations": ["M"],
                        "authorized_scope_roots": ["src/pay"],
                        "max_scope_roots": 2, "max_exact_paths": 5}}
_overlay = _w("overlay.json", _ov_spec)
_ub = {**_bundle, "run_id": "RUN-CLI", "adapter": "implement-backlog",
       "execution_mode": "unattended", "policy_profile": "unattended/v1",
       "policy_sha256": sa.hash_json(dict(sa.resolve_policy(_ov_spec)))}
S.holds("C01 build-approval accepts a valid base+overlay artifact through the CLI",
        cli(["build-approval", _w("ub.json", _ub), "--policy", _overlay]) == 0)
_urec = {"schema_version": 1,
         "approval_fingerprint": sa.build_approval(_ub, policy=sa.resolve_policy(_ov_spec))[1],
         "approval_artifact_id": "issue-comment:3", "approver": "rapha",
         "approved_at": "2026-08-14T09:00:00Z", "provider": "github",
         "repository": "org/repo", "run_id": "RUN-CLI"}
S.holds("C02 verify-approval accepts the same overlay",
        cli(["verify-approval", _w("urec.json", _urec), "--bundle", _w("ub2.json", _ub),
             "--policy", _overlay]) == 0)
S.holds("C02 a mutated overlay invalidates the approval",
        cli(["verify-approval", _w("urec2.json", _urec), "--bundle", _w("ub3.json", _ub),
             "--policy", _w("ov2.json", {**_ov_spec,
                                         "overlay": {**_ov_spec["overlay"],
                                                     "allowed_operations": []}})]) == 1)
_um = {**_manifest, "run_id": "RUN-CLI", "adapter": "implement-backlog",
       "execution_mode": "unattended", "policy_profile": "unattended/v1",
       "mechanical_scope": {**_manifest["mechanical_scope"], "allowed_paths": ["src/pay/**"]}}
_add = os.path.join(_tmpdir, "add.txt"); open(_add, "w").write("A\tsrc/pay/new.py\n")
S.holds("C03 validate-scope applies the overlay's allowed_operations through the CLI",
        cli(["validate-scope", "--manifest", _w("um.json", _um), "--changes", _add,
             "--profile", _overlay]) == 1)
_mod = os.path.join(_tmpdir, "mod.txt"); open(_mod, "w").write("M\tsrc/pay/new.py\n")
S.holds("C03 an operation the overlay allows passes through the CLI",
        cli(["validate-scope", "--manifest", _w("um2.json", _um), "--changes", _mod,
             "--profile", _overlay]) == 0)
S.holds("validate-scope refuses a self-declared policy artifact",
        cli(["validate-scope", "--manifest", _w("m.json", _manifest), "--changes", _chg,
             "--profile", _fake_policy]) == 1)
shutil.rmtree(_tmpdir, ignore_errors=True)

S.section("C10 gate hygiene — a clean extraction stays clean")
_hy = os.path.join(tmp, "hygiene")
shutil.copytree(clean_tree, _hy)
subprocess.run([sys.executable, "scripts/validate-bundle.py"], cwd=_hy,
               capture_output=True, text=True, timeout=TIMEOUT)
_dirt = [str(p) for p in __import__("pathlib").Path(_hy).rglob("__pycache__")]
S.holds("the standalone structural validator leaves no bytecode in the tree",
        _dirt == [], f"created {_dirt[:3]}")

_dup = os.path.join(tmp, "dupkey")
shutil.copytree(clean_tree, _dup)
_pf = os.path.join(_dup, "policy/profiles/unattended-v1.json")
_orig = open(_pf).read().rstrip()[:-1].rstrip().rstrip(",")
open(_pf, "w").write(_orig + ',\n  "governance": "allow",\n  "governance": "deny"\n}\n')
S.holds("C08 a duplicate key in a policy artifact turns the structural gate red",
        structural(_dup) == 1)

shutil.rmtree(tmp, ignore_errors=True)
sys.exit(S.report())

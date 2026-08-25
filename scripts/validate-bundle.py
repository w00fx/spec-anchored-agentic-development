#!/usr/bin/env python3
"""Bundle consistency validator — structural checks ONLY.

Scans the whole corpus (hidden directories included), enforces
frontmatter policy on the transactional adapters, compiles the
executable contracts and their suites, and parses every shell script.

It deliberately does NOT run the test suites: `scripts/check-all.sh`
is the single gate and runs each suite exactly once, directly. Mixing
the two roles is what let an environment variable skip the tests
(tenth audit, P0-02) — no env var changes what this script checks.
"""
import sys, os, re, json, subprocess, tempfile, shutil, atexit
sys.dont_write_bytecode = True   # standalone runs must leave the tree clean too
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml")

ERR = []
def err(m): ERR.append(m)

_PYCACHE = tempfile.mkdtemp(prefix="sa-pycache-")
def _clean_env():
    """py_compile writes bytecode by design; PYTHONDONTWRITEBYTECODE does not
    stop it. Redirect the cache out of the consumer's tree instead
    (twelfth audit, P1-06)."""
    return dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPYCACHEPREFIX=_PYCACHE)

ROOT = Path(".")
EXCLUDE_EXACT = {"sources-and-learnings.md", "GUIDELINE-pt-BR.md"}
def corpus_md():
    for p in ROOT.rglob("*.md"):
        parts = set(p.parts)
        if "__pycache__" in parts or ".git" in parts:
            continue
        if p.name in EXCLUDE_EXACT and p.parent == ROOT:
            continue
        yield p

CMD = list(ROOT.rglob(".claude/commands/*.md")) or list(ROOT.glob("commands/*.md"))
SKL = (list(ROOT.rglob(".claude/skills/*/SKILL.md"))
       or list(ROOT.glob("skills/*/SKILL.md"))
       or list(ROOT.glob("implement-*/SKILL.md"))
       or list(ROOT.glob("reviewer-system/skills/*/SKILL.md")))
AGT = (list(ROOT.rglob(".claude/agents/*.md"))
       or list(ROOT.glob("agents/*.md"))
       or list(ROOT.glob("reviewer-system/agents/*.md")))
TRANSACTIONAL = ("implement-feature", "implement-orchestrated", "implement-backlog")

# 1. frontmatter schema + invocation policy.
#    Frontmatter is REQUIRED for these artifact classes: removing it
#    wholesale used to pass silently, and `disable-model-invocation`
#    is part of the safety model, not formatting (eleventh audit, P0-13).
for f in CMD + SKL + AGT:
    t = f.read_text(encoding="utf-8", errors="ignore")
    if not t.startswith("---"):
        err(f"{f}: missing frontmatter — commands, skills and agents must declare it")
        continue
    try:
        fm = yaml.safe_load(t.split("---")[1])
    except Exception as e:
        err(f"{f}: frontmatter YAML invalid: {e}"); continue
    if fm is None:
        err(f"{f}: frontmatter is empty or null — an empty envelope removes "
            "name, description and disable-model-invocation without a trace")
        continue
    if not isinstance(fm, dict):
        err(f"{f}: frontmatter must be a mapping, got {type(fm).__name__}")
        continue
    if not fm:
        err(f"{f}: frontmatter mapping is empty")
        continue
    for key, typ in (("argument-hint", str), ("description", str),
                     ("disable-model-invocation", bool)):
        if key in fm and fm[key] is not None and not isinstance(fm[key], typ):
            err(f"{f}: {key} is {type(fm[key]).__name__}, must be {typ.__name__}")
    # required fields per artifact class: an empty frontmatter is a
    # well-formed envelope with no contract inside (twelfth audit, P1-04)
    if f in CMD:
        if not isinstance(fm.get("description"), str) or not fm["description"].strip():
            err(f"{f}: a command must declare a non-empty description")
    if f in SKL:
        for field in ("name", "description"):
            if not isinstance(fm.get(field), str) or not fm[field].strip():
                err(f"{f}: a skill must declare a non-empty {field}")
    if f in AGT:
        if "reviewer" in str(f) and fm.get("isolation") != "worktree":
            err(f"{f}: the reviewer must declare isolation: worktree "
                "(candidate immutability is configuration, not prose)")
        for field in ("name", "description"):
            if not isinstance(fm.get(field), str) or not fm[field].strip():
                err(f"{f}: an agent must declare a non-empty {field}")
    if any(f"{name}/SKILL.md" in str(f) for name in TRANSACTIONAL):
        if fm.get("disable-model-invocation") is not True:
            err(f"{f}: transactional adapter must set disable-model-invocation: true "
                "(user-invocation-only is a contract, not a preference)")

# 2. retired forms — literal and semantic
def scan_retired(root, legacy, skip_exact):
    """Importable so fixtures can exercise the scan without copying a tree."""
    out = []
    for p in root.rglob("*.md"):
        parts = set(p.parts)
        if "__pycache__" in parts or ".git" in parts:
            continue
        if p.name in skip_exact and p.parent == root:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for pat in legacy:
            if re.search(pat, text):
                out.append((str(p), pat))
    return out


LEGACY = [r"\bPhase 7:", r"two skills, not one", r"monitor until (it )?land",
          r"monitors the PR until", r"specs/_template/", r"\bfour-lens\b",
          r"\bBlocked-by\b", r"Phase 2 plan", r"serialize them into one worker",
          r"/goal Implement", r"blockers are now ALL merged", r"Phase 1\.5",
          r"Code review \(Phase 5\)", r"creation is always human",
          r"persistence engine", r"references are all closed", r"\bmerge-gated\b",
          r"independence is the point", r"independent router", r"engine = native",
          r"workflow \(7 phases", r"Phase 2 \(plan review\)", r"items 1-4",
          r"numbered criteria", r"numbered acceptance", r"PLAN-FINGERPRINT",
          # semantic variants of the retired /goal-as-engine doctrine
          r"recommended[^.\n]{0,40}/goal", r"/goal[^.\n]{0,30}recommended",
          r"/goal[^.\n]{0,30}(engine|loader)", r"supervised `/goal` recipes",
          r"criteria numbered in continuation", r"criteria numbers are never",
          r"/implement\b(?![- ])[^.\n]{0,30}(entry point|adapter|runs the)",
          # tenth audit: the old generation kept reappearing in prose
          r"autonomous /goal", r"`/goal` condition can verify",
          r"plain `/implement`", r"the implementation skills, the reviewer, `/goal`",
          r"approved_expansions", r"PLAN-FINGERPRINT"]
for path, pat in scan_retired(ROOT, LEGACY, EXCLUDE_EXACT):
    err(f"{path}: retired form /{pat}/")

# 3. single canonical template with its organs
tpls = [p for p in ROOT.rglob("capability-spec.md") if "__pycache__" not in str(p)]
if len(tpls) != 1:
    err(f"expected exactly 1 capability-spec.md, found {len(tpls)}: {tpls}")
elif tpls:
    t = tpls[0].read_text(encoding="utf-8")
    for organ in ("## Open questions", "BR-<CAP>-001", "AC-<CAP>-001", "schema_version"):
        if organ not in t:
            err(f"{tpls[0]}: missing organ '{organ}'")

# 4. adapters read the protocol
for f in SKL:
    if "implement" in str(f) and "implementation-protocol.md" not in f.read_text(encoding="utf-8"):
        err(f"{f}: does not reference the shared protocol")

# 5. protocol carries the terminal taxonomy
pp = list(ROOT.rglob("implementation-protocol.md"))
if not pp:
    err("shared protocol file not found")
else:
    t = pp[0].read_text(encoding="utf-8")
    for term in ("NO_CHANGE_REQUIRED", "PR_READY_AWAITING_HUMAN", "NAMED_BLOCKER"):
        if term not in t:
            err(f"{pp[0]}: missing terminal {term}")

# 6. executable contracts must compile and ship with their suites
CONTRACTS = ROOT / "scripts" / "spec-anchored"
SUITES = [ROOT / "tests" / "test_kernel_contracts.py",
          ROOT / "tests" / "test_kernel_adversarial.py",
          ROOT / "tests" / "test_corpus.py",
          ROOT / "tests" / "test-mutants.py",
          ROOT / "tests" / "_harness.py"]
if CONTRACTS.exists():
    for suite in SUITES:
        if not suite.exists():
            err(f"{CONTRACTS} ships without {suite} "
                "(a contract without fixtures is a claim, not a contract)")
    # every normative python artifact, discovered rather than listed: a NEW
    # validator with a syntax error used to pass unnoticed (closure v2, P1-02)
    discovered = sorted({p for p in list(ROOT.rglob("*.py"))
                         if "__pycache__" not in str(p) and ".git" not in str(p)})
    for src in [CONTRACTS] + discovered + [Path(__file__)]:
        r = subprocess.run([sys.executable, "-m", "py_compile", str(src)],
                           capture_output=True, text=True, timeout=60,
                           env=_clean_env())
        if r.returncode != 0:
            err(f"{src}: does not compile — {r.stderr.strip().splitlines()[-1:]}")

# 6b. the policy artifacts and the kernel's profiles must be the SAME policy
if CONTRACTS.exists() and (ROOT / "policy" / "profiles").is_dir():
    import importlib.util, importlib.machinery
    _s = importlib.util.spec_from_loader(
        "sa_v", importlib.machinery.SourceFileLoader("sa_v", str(CONTRACTS)))
    _m = importlib.util.module_from_spec(_s)
    try:
        _s.loader.exec_module(_m)
        # the profile directory is a CLOSED registry: an extra file is neither a
        # known profile nor an instance, so it used to escape both loops
        # (closure v4, P1-01)
        expected = {pid.replace("/", "-") + ".json" for pid in _m.PROFILES}
        actual = {p.name for p in (ROOT / "policy" / "profiles").glob("*")}
        for extra in sorted(actual - expected):
            err(f"policy/profiles/{extra}: not in the profile registry — a profile "
                "enters the registry, the artifact set and the tests atomically")
        for missing in sorted(expected - actual):
            err(f"policy/profiles/{missing}: registered profile has no artifact")
        for pid in _m.PROFILES:
            art = ROOT / "policy" / "profiles" / (pid.replace("/", "-") + ".json")
            if not art.exists():
                err(f"policy artifact missing for profile {pid}")
                continue
            try:
                on_disk = _m.strict_json_loads(art.read_text())
            except Exception as e:
                err(f"{art}: not a strict policy artifact ({e})"); continue
            if on_disk.get("profile_id") != pid:
                err(f"{art}: profile_id does not match its filename")
            in_code = _m.resolve_policy(pid)
            if _m.hash_json(on_disk) != _m.hash_json(in_code):
                err(f"{art}: policy artifact differs from the kernel's profile "
                    f"{pid} — two authorities for one policy")
        # every authorization artifact must strict-parse AND resolve: a policy
        # instance is the external authority, so it fails closed like one
        for inst in sorted((ROOT / "policy").rglob("*.json")):
            if inst.parent.name == "profiles":
                continue
            try:
                spec_obj = _m.strict_json_loads(inst.read_text())
            except Exception as e:
                err(f"{inst}: not a strict policy artifact ({e})"); continue
            try:
                _m.resolve_policy(spec_obj)
            except Exception as e:
                err(f"{inst}: does not resolve as a policy ({e})")
    except Exception as e:
        err(f"could not compare policy artifacts with the kernel: {e}")

# 7. shell scripts must parse (a broken gate script is a silent bypass)
for sh in list(ROOT.rglob("*.sh")):
    if "__pycache__" in str(sh):
        continue
    r = subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        err(f"{sh}: shell syntax error — {r.stderr.strip().splitlines()[-1:]}")

# 8. frontmatter must be delimited on BOTH sides
for f in CMD + SKL + AGT:
    t = f.read_text(encoding="utf-8", errors="ignore")
    if t.startswith("---") and len(t.split("---")) < 3:
        err(f"{f}: frontmatter opens but never closes (the parser would read the body as YAML)")

atexit.register(lambda: shutil.rmtree(_PYCACHE, ignore_errors=True))

if ERR:
    print(f"FAIL — {len(ERR)} violation(s):")
    for e in ERR:
        print("  -", e)
    sys.exit(1)
print("OK — structural checks passed "
      "(suites are run by check-all.sh; environment verification still staged)")

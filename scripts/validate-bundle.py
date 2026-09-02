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
EXCLUDE_EXACT = {"REVIEW-FINDINGS.md", "sources-and-learnings.md", "GUIDELINE-pt-BR.md"}
def corpus_md():
    for p in ROOT.rglob("*.md"):
        parts = set(p.parts)
        if "__pycache__" in parts or ".git" in parts:
            continue
        if p.name in EXCLUDE_EXACT and p.parent == ROOT:
            continue
        yield p

SKL = sorted((ROOT / ".agents" / "skills").glob("*/SKILL.md"))
if not SKL:
    SKL = sorted(ROOT.glob("implement-*/SKILL.md")) + sorted(ROOT.glob("reviewer-system/skills/*/SKILL.md"))
AGT_MD = sorted(ROOT.glob("agents/*.md"))
AGT_TOML = sorted(ROOT.glob("agents/*.toml"))
IMPLEMENTATION_ADAPTERS = ("implement-feature", "implement-orchestrated", "implement-backlog")
EXPLICIT_SKILLS = {
    "implement", "implement-feature", "implement-orchestrated", "implement-backlog",
    "explain", "orchestrate", "plan-from-issue", "prep", "review-spec-drift",
    "shape", "spec-to-tickets", "to-spec",
}

ACTUAL_SKILL_NAMES = {f.parent.name for f in SKL}
for missing in sorted(EXPLICIT_SKILLS - ACTUAL_SKILL_NAMES):
    err(f".agents/skills/{missing}/SKILL.md: required converted workflow skill is missing")

# The shared skill corpus is runtime-neutral. Slash- and dollar-prefixed
# invocation examples belong in runtime adaptations, not in canonical skills.
_runtime_prefixed_skill = re.compile(
    r"(?<![A-Za-z0-9])(?:/|\$)(?:shape|to-spec|spec-to-tickets|implement|"
    r"implement-feature|implement-orchestrated|implement-backlog|orchestrate|"
    r"prep|review-spec-drift|explain|plan-from-issue)\b"
)
for f in SKL:
    hit = _runtime_prefixed_skill.search(f.read_text(encoding="utf-8", errors="ignore"))
    if hit:
        err(f"{f}: runtime-specific invocation {hit.group(0)!r} is forbidden in "
            "the shared skill corpus; use the bare skill name and put syntax in an adapter")

# 1. frontmatter schema + invocation policy.
#    Every skill and Markdown agent has a real contract envelope. The former
#    command entrypoints are explicit shared skills; harness-specific command trees are retired.
for f in SKL + AGT_MD:
    t = f.read_text(encoding="utf-8", errors="ignore")
    if not t.startswith("---"):
        err(f"{f}: missing frontmatter — skills and Markdown agents must declare it")
        continue
    pieces = t.split("---", 2)
    if len(pieces) < 3:
        err(f"{f}: frontmatter opens but never closes")
        continue
    try:
        fm = yaml.safe_load(pieces[1])
    except Exception as e:
        err(f"{f}: frontmatter YAML invalid: {e}"); continue
    if fm is None:
        err(f"{f}: frontmatter is empty or null — an empty envelope removes "
            "name, description and invocation controls without a trace")
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
    for field in ("name", "description"):
        if not isinstance(fm.get(field), str) or not fm[field].strip():
            err(f"{f}: must declare a non-empty {field}")
    if f in SKL:
        expected_name = f.parent.name
        if fm.get("name") != expected_name:
            err(f"{f}: skill name {fm.get('name')!r} must match directory {expected_name!r}")
        if expected_name in EXPLICIT_SKILLS and fm.get("disable-model-invocation") is not True:
            err(f"{f}: explicit workflow skill must set disable-model-invocation: true")
    if f in AGT_MD:
        if fm.get("isolation") != "worktree":
            err(f"{f}: internal authoring agents must declare isolation: worktree "
                "so every handoff is a committed, inspectable delta")
        if fm.get("effort") != "max":
            err(f"{f}: internal agents must declare effort: max; lower effort is "
                "not an allowed adapter override")
        if "model" in fm:
            err(f"{f}: internal agents must omit model so they inherit the Owner/parent worker model")

# 1a. commands and harness-native agent directories are retired. There is one
# shared skill corpus and one paired root agent catalog.
for retired_dir in (
    ROOT / ".claude/commands", ROOT / ".claude/agents", ROOT / ".claude/protocols",
    ROOT / ".claude/skills", ROOT / ".claude/rules", ROOT / ".claude/logs",
):
    if retired_dir.exists():
        err(f"{retired_dir}: retired — entrypoints are skills, agent contracts live in "
            "root agents/, while shared skills/rules/protocols live under .agents/")

# 1a.1 cross-harness operating entrypoint and runtime-state hygiene.
agents_md = ROOT / "AGENTS.md"
if not agents_md.exists():
    err("AGENTS.md: cross-harness operational entrypoint is required")
else:
    ag = agents_md.read_text(encoding="utf-8", errors="ignore")
    for phrase in (".agents/skills/", ".agents/protocols/", ".agents/rules/",
                   ".agent-runs/<run-id>/", "general-code-reviewer", "mutation-hardener"):
        if phrase not in ag:
            err(f"AGENTS.md: missing routing obligation {phrase!r}")
    if len(ag.splitlines()) > 110:
        err("AGENTS.md: root operational context must stay concise (<= 110 lines)")

required_rules = {"testing.md", "truth-layer.md", "package-by-feature.md"}
rules_dir = ROOT / ".agents" / "rules"
actual_rules = {p.name for p in rules_dir.glob("*.md")} if rules_dir.exists() else set()
for missing in sorted(required_rules - actual_rules):
    err(f".agents/rules/{missing}: required shared engineering rule is missing")

ignore = ROOT / ".gitignore"
if not ignore.exists() or ".agent-runs/" not in ignore.read_text(encoding="utf-8", errors="ignore"):
    err(".gitignore: must ignore .agent-runs/ so transient run state is never committed")
if (ROOT / ".agent-runs").exists():
    err(".agent-runs/: transient run state must not be packaged in the bundle")

for adapter_name in IMPLEMENTATION_ADAPTERS:
    template = ROOT / ".agents" / "skills" / adapter_name / "references" / "log-template.md"
    if template.exists() and ".agent-runs/<run-id>/run-log.md" not in template.read_text(encoding="utf-8"):
        err(f"{template}: runtime log must live under .agent-runs/<run-id>/run-log.md")

# 1b. exactly two authoring agents ship, and each has byte-equivalent Markdown
# instructions plus a TOML adapter. Heavy/spec/security/performance reviews are external.
EXPECTED_AGENT_STEMS = {"general-code-reviewer", "mutation-hardener"}
md_by_stem = {f.stem: f for f in AGT_MD}
toml_by_stem = {f.stem: f for f in AGT_TOML}
for extra in sorted(set(md_by_stem) - EXPECTED_AGENT_STEMS):
    err(f"agents/{extra}.md: only the two internal authoring agents belong in the harness")
for extra in sorted(set(toml_by_stem) - EXPECTED_AGENT_STEMS):
    err(f"agents/{extra}.toml: only the two internal authoring agents belong in the harness")
for missing in sorted(EXPECTED_AGENT_STEMS - set(md_by_stem)):
    err(f"agents/{missing}.md: required Markdown agent contract is missing")
for missing in sorted(EXPECTED_AGENT_STEMS - set(toml_by_stem)):
    err(f"agents/{missing}.toml: required TOML agent contract is missing")

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.11+ is the supported baseline
    tomllib = None

for stem in sorted(EXPECTED_AGENT_STEMS & set(md_by_stem) & set(toml_by_stem)):
    md_path = md_by_stem[stem]
    toml_path = toml_by_stem[stem]
    md_text = md_path.read_text(encoding="utf-8", errors="strict")
    pieces = md_text.split("---", 2)
    if len(pieces) < 3:
        continue
    md_fm = yaml.safe_load(pieces[1]) or {}
    md_body = pieces[2].lstrip("\n").rstrip() + "\n"
    if tomllib is None:
        err(f"{toml_path}: tomllib unavailable")
        continue
    try:
        obj = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except Exception as e:
        err(f"{toml_path}: invalid TOML ({e})")
        continue
    for field in ("name", "description", "developer_instructions"):
        if not isinstance(obj.get(field), str) or not obj[field].strip():
            err(f"{toml_path}: missing non-empty {field}")
    if obj.get("name") != stem or md_fm.get("name") != stem:
        err(f"agents/{stem}: file stem, Markdown name and TOML name must match")
    if " ".join(str(md_fm.get("description", "")).split()) != " ".join(str(obj.get("description", "")).split()):
        err(f"agents/{stem}: Markdown and TOML descriptions drifted")
    if obj.get("developer_instructions", "").rstrip() + "\n" != md_body:
        err(f"agents/{stem}: TOML developer_instructions drifted from the Markdown body")
    if obj.get("sandbox_mode") != "workspace-write":
        err(f"{toml_path}: authoring agent must use sandbox_mode = workspace-write")
    if "model" in obj:
        err(f"{toml_path}: internal agents must omit model so Codex inherits the parent worker model")
    if obj.get("model_reasoning_effort") != "max":
        err(f"{toml_path}: internal agents must use model_reasoning_effort = max")
    if obj.get("source_markdown") != f"agents/{stem}.md":
        err(f"{toml_path}: source_markdown must point to agents/{stem}.md")

# A native Codex install is generated, never canonical. When present it must be
# an exact mirror of the root TOML contracts and contain no extra role.
codex_agents = ROOT / ".codex" / "agents"
if codex_agents.exists():
    actual = {p.name for p in codex_agents.glob("*.toml")}
    expected = {f"{stem}.toml" for stem in EXPECTED_AGENT_STEMS}
    for extra in sorted(actual - expected):
        err(f"{codex_agents / extra}: generated Codex agent is not in the canonical root catalog")
    for missing in sorted(expected - actual):
        err(f"{codex_agents / missing}: generated Codex agent mirror is missing")
    for name in sorted(actual & expected):
        if (codex_agents / name).read_bytes() != (ROOT / "agents" / name).read_bytes():
            err(f"{codex_agents / name}: generated Codex adapter drifted from agents/{name}")

for retired in (
    ROOT / "agents/reviewer.md",
    ROOT / "agents/reviewer.toml",
    ROOT / ".agents/skills/plan-review",
    ROOT / ".agents/skills/conformance-review",
    ROOT / ".agents/skills/constitution-compliance-review",
):
    if retired.exists():
        err(f"{retired}: retired in favor of the two internal authoring agents and external review pipeline")

general_review_skill = ROOT / ".agents/skills/general-code-review/SKILL.md"
if not general_review_skill.exists():
    err(f"{general_review_skill}: required rubric for the General Code Reviewer is missing")
else:
    gr = general_review_skill.read_text(encoding="utf-8", errors="ignore").lower()
    for phrase in ("correctness", "regression", "test quality", "owner"):
        if phrase not in gr:
            err(f"{general_review_skill}: missing reviewer obligation '{phrase}'")
    agent_path = ROOT / "agents/general-code-reviewer.md"
    if agent_path.exists() and "general-code-review" not in agent_path.read_text(encoding="utf-8", errors="ignore"):
        err(f"{agent_path}: does not load the general-code-review criteria skill")

testing_rule = ROOT / ".agents/rules/testing.md"
if not testing_rule.exists():
    err(".agents/rules/testing.md: testing strategy rule is required before mutation hardening")
else:
    tr = testing_rule.read_text(encoding="utf-8", errors="ignore").lower()
    for phrase in ("regression", "integration", "contract", "fuzz", "mutation"):
        if phrase not in tr:
            err(f"{testing_rule}: missing testing obligation '{phrase}'")

for adapter_name in IMPLEMENTATION_ADAPTERS:
    adapter = ROOT / ".agents/skills" / adapter_name / "SKILL.md"
    if adapter.exists():
        at = adapter.read_text(encoding="utf-8", errors="ignore")
        for agent_name in ("general-code-reviewer", "mutation-hardener"):
            if agent_name not in at:
                err(f"{adapter}: does not invoke required internal agent {agent_name}")

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
          r"approved_expansions", r"PLAN-FINGERPRINT",
          # cross-harness migration: shared authority/state never returns to a
          # product-specific namespace
          r"\.claude/(?:skills|rules|logs|protocols|commands|agents)/",
          r"auto-loaded every session",
          r"one spec per capability", r"from a single spec file"]
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

# 4. adapters read the exact canonical protocol path.
for f in SKL:
    if (f.parent.name in IMPLEMENTATION_ADAPTERS and
            ".agents/protocols/implementation-protocol.md" not in
            f.read_text(encoding="utf-8")):
        err(f"{f}: does not reference .agents/protocols/implementation-protocol.md")

# 5. one canonical shared protocol tree, neutral to the runtime.
protocol_path = ROOT / ".agents" / "protocols" / "implementation-protocol.md"
pp = list(ROOT.rglob("implementation-protocol.md"))
if pp != [protocol_path]:
    err(f"expected exactly one shared protocol at {protocol_path}, found: {pp}")
if not protocol_path.exists():
    err(f"{protocol_path}: shared protocol file not found")
else:
    protocol_text = protocol_path.read_text(encoding="utf-8")
    for term in ("NO_CHANGE_REQUIRED", "PR_READY_AWAITING_HUMAN", "NAMED_BLOCKER",
                 'model_reasoning_effort="max"', "inherit the model", ".agent-runs/<run-id>/"):

        if term not in protocol_text:
            err(f"{protocol_path}: missing protocol obligation {term}")
    if "effort=max" not in protocol_text:
        err(f"{protocol_path}: must declare effort=max for both internal agents")
    for ref in ("references/scope-manifest-schema.md", "references/review-target-schema.md"):
        if not (protocol_path.parent / ref).exists():
            err(f"{protocol_path.parent / ref}: required shared protocol reference is missing")

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
    for src in sorted(set([CONTRACTS] + discovered + [Path(__file__)]), key=str):
        try:
            compile(src.read_text(encoding="utf-8"), str(src), "exec")
        except Exception as e:
            err(f"{src}: does not compile — {type(e).__name__}: {e}")

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
for f in SKL + AGT_MD:
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

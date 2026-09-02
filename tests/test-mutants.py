#!/usr/bin/env python3
"""Mutation adequacy — the test that tests the tests.

The tenth audit removed four properties from the kernel and both
suites stayed green. A suite that cannot notice a missing property is
not evidence. This runner injects known regressions into a copy of the
kernel and requires at least one suite to go RED for each.

A mutant that SURVIVES is a hole in the fixtures, and is reported by
name. A mutant whose anchor no longer matches is also a failure: it
means this file is testing a kernel that no longer exists.

`python3 tests/test-mutants.py` — exit 0 = every mutant was killed.
"""
import sys, os, shutil, tempfile, subprocess
sys.dont_write_bytecode = True

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KERNEL = os.path.join("scripts", "spec-anchored")
SUITES = ["tests/test_kernel_contracts.py", "tests/test_kernel_adversarial.py"]
TIMEOUT = 180  # per suite run; a hang is a failure, not a wait

# label -> (anchor, replacement). Each removes ONE claimed property.
MUTANTS = {
    "accept unknown git status letters": (
        'GIT_STATUS = re.compile(r"^(?:[AMDTUX]|[RC]\\d{0,3})$")',
        'GIT_STATUS = re.compile(r"^(?:[A-Z]|[RC]\\d{0,3})$")'),
    "accept duplicate JSON keys": (
        "return json.loads(text, object_pairs_hook=_no_dupes, parse_constant=_reject_const)",
        "return json.loads(text)"),
    "accept Markdown hard breaks": (
        '            if ln.strip() and re.search(r"\\S {2,}$", ln):',
        "            if False:"),
    "stop validating hash and SHA formats": (
        "        if not rx.match(parts[f]):",
        "        if False:"),
    "stop enforcing the governance floor": (
        '        if profile.get("governance") == "deny" and any(_match(path, g) for g in GOVERNANCE_FLOOR):',
        "        if False:"),
    "stop enforcing denied_paths": (
        "        if any(_match(path, d) for d in denied):",
        "        if False:"),
    "stop enforcing the profile ceiling on truth": (
        '            if ceiling != "gated":',
        "            if False:"),
    "accept a missing or unusable policy": (
        '        raise ContractViolation("policy must be a profile id or an object")',
        '        return dict(PROFILES["supervised-local/v1"], profile_id="supervised-local/v1")'),
    "stop enforcing permissions": (
        "            if any(_match(path, p) for p in pats) and not perms.get(perm, False):",
        "            if False:"),
    "allow matcher operators where only exact paths are legal": (
        '    if kind == "exact":\n        if set(value) & GLOB_CHARS:',
        '    if kind == "exact":\n        if False:'),
    "accept any terminal name": (
        "    if term not in TERMINALS:",
        "    if False and term not in TERMINALS:"),
    "stop binding claim_state to the terminal": (
        '    elif result["claim_state"] != spec["claim"]:',
        "    elif False:"),
    "accept any no-change classification": (
        "        elif cls not in CLASSIFICATIONS_TERMINAL:",
        "        elif False:"),
    "accept booleans where ints are required": (
        "        if typ is int and not is_int(val):",
        "        if False:"),
    "stop refusing unknown result fields": (
        "    for k in sorted(set(result) - known):",
        "    for k in []:"),
    "let PR_READY omit the mutation hardening report": (
        '                     "mutation_hardening_report_sha256",\n                     "owner_disposition_sha256"},',
        '                     "owner_disposition_sha256"},'),
    "let PR_READY omit Owner disposition": (
        '                     "owner_disposition_sha256"},',
        '                     "owner_disposition_sha256"} - {"owner_disposition_sha256"},'),
    "let NO_CHANGE omit corroboration identity": (
        '        "required": {"evidence_target_sha256", "no_change_corroboration_sha256",',
        '        "required": {"evidence_target_sha256",'),
    # oracle mutants: a clean refusal replaced by a crash must NOT pass
    "crash instead of refusing cleanly (wrong exception type)": (
        '            raise ContractViolation("line %d: unreadable status %r (refusing to treat "',
        '            raise RuntimeError("line %d: unreadable status %r (refusing to treat "'),
    "stop binding the approval record to the bundle": (
        "    if bundle is not None:",
        "    if False:"),
    "stop computing the policy hash": (
        "        if parts[\"policy_sha256\"] != hash_json(effective):",
        "        if False:"),
    "classify truth by first match only": (
        "    return {kind for kind, pats in TRUTH_ROOTS.items()\n            if any(_match(path, p) for p in pats)}",
        "    t = truth_type(path)\n    return {t} if t else set()"),
    "accept impossible calendar dates": (
                "                datetime.datetime.fromisoformat(stamp.replace(\"Z\", \"+00:00\"))",
                "                pass"),
    "let an overlay drop restrictions (dict.update semantics)": (
        "            dropped = set(base.get(key, [])) - set(value)",
        "            dropped = set()"),
    "accept a self-declared policy object": (
        "    if hash_json(dict(spec)) != hash_json(canonical):",
        "    if False:"),
    "stop protecting operational context files": (
        '    "operational context": ["AGENTS.md", "**/AGENTS.md", "CLAUDE.md", "**/CLAUDE.md",',
        '    "operational context": [] or ["__x__", "__y__", "__z__", "__w__",'),
    "reopen nested manifest schemas": (
        '        for k in sorted(set(sem) - {"implements", "verifies", "non_goals"}):',
        "        for k in []:"),
    "stop checking stable ID grammar": (
        "                if is_str(item) and not STABLE_ID.match(item):",
        "                if False:"),
    "accept an unterminated NUL stream": (
        '        if text and not text.endswith("\\x00"):',
        "        if False:"),
    # NOTE: no mutant for "verify_approval accepts a bare fingerprint" — with the
    # guard removed, build_approval refuses the string anyway, so no fixture can
    # tell the two apart. The property is fixture-covered, not mutation-proven.
    # closure v1: properties the previous 27 mutants did not model
    "ignore policy-level allowed_operations": (
        "    prof_ops = profile.get(\"allowed_operations\")",
        "    prof_ops = None"),
    "let a manifest widen its permission ceiling": (
        "        if granted is True and ceiling.get(perm) is False:",
        "        if False:"),
    "accept a semantically whole-tree glob variant": (
        "        why = pattern_violation(pat, grammar)",
        "        why = None"),
    "resolve an already-resolved policy a second time": (
        "    if isinstance(spec, ResolvedPolicy):",
        "    if False:"),
    "skip path-pattern grammar in the manifest schema": (
        '            bad = canonical_violation(pat, kind="pattern" if is_pattern(pat) else "exact")',
        "            bad = None"),
    "allow an approval without a policy": (
        "    if policy is None and not _shape_only:",
        "    if False:"),
    "crash instead of refusing malformed policy lists": (
        '        if not is_str(item):\n            raise ContractViolation("%s must be a list of strings (found %s)"',
        '        if False:\n            raise ContractViolation("%s must be a list of strings (found %s)"'),
    # closure v2 — the authority properties the previous mutants did not model
    "remove the authorized-root subset check": (
        '            if not any(head == r or head.startswith(r + "/") for r in norm):',
        "            if False:"),
    "remove the aggregate-breadth caps": (
        "        if cap_patterns is not None and len(recursive) > cap_patterns:",
        "        if False:"),
    "restore the max(wild) wildcard logic": (
        '    if grammar.get("forbid_intermediate_wildcard") and any(i != len(segments) - 1 for i in wild):',
        '    if grammar.get("forbid_intermediate_wildcard") and wild and max(wild) != len(segments) - 1:'),
    "skip the policy-level path deny": (
        '        if any(_match(path, d) for d in (profile.get("denied_path_patterns") or [])):',
        "        if False:"),
    "let a base profile authorize an unattended run": (
        '    if profile.get("requires_scope_roots") and not roots:',
        "    if False:"),
    "skip allowed_operations schema validation": (
        '    if "allowed_operations" in mech:',
        "    if False:"),
    # closure v3 — the authority artifact's own parser
    "accept malformed policy deny patterns": (
        '                _policy_path(pat, "denied_path_patterns", allow_glob=True)',
        "                pass"),
    "accept malformed authorized roots": (
        '                _policy_path(root, "authorized_scope_roots", allow_glob=False)',
        "                pass"),
    "let the authorized root set exceed max_scope_roots": (
        "            if is_int(cap) and len(value) > cap:",
        "            if False:"),
    # closure v4 — the shared parser's own rules
    "accept pattern operators the matcher does not implement": (
        "    bad = sorted(set(value) & PATTERN_LOOKALIKE_CHARS)",
        "    bad = []"),
    "accept dot and traversal segments": (
        '        if seg == ".":',
        "        if False:"),
    "accept control characters in paths": (
        "    if any(ch in CONTROL_CHARS for ch in value):",
        "    if False:"),
    "accept `**` glued into a segment": (
        '        if "**" in seg and seg != "**":',
        "        if False:"),
    # closure v5 — the operator contract, proven behaviourally
    "remove the ** token from the operator table": (
        'OPERATOR_TOKENS = ("**/", "**", "*", "?")',
        'OPERATOR_TOKENS = ("**/", "*", "?")'),
    "literalize the ? operator": (
        '    "?":   "[^/]",       # exactly one non-slash character',
        '    "?":   "\\\\?",'),
    "make **/ require at least one segment": (
        '    "**/": "(?:.*/)?",   # zero or more path segments',
        '    "**/": "(?:.*/)+",'),
    "let * cross slash boundaries": (
        '    "*":   "[^/]*",      # zero or more non-slash characters',
        '    "*":   ".*",'),
    "ban operator-lookalikes in literal paths again": (
        '    if kind == "path":\n        return None          # literal identity: any legal filename is legal',
        '    if kind == "path":\n        return "wildcards are not allowed here" if (set(value) & PATTERN_LOOKALIKE_CHARS) else None'),
    "strip padding from textual diff paths": (
        "            if p != p.strip() or p.startswith('\"'):",
        "            if False:"),
}


def run_suite(tree, suite):
    """Run one fast kernel suite. A timeout counts as a failure."""
    try:
        return subprocess.run([sys.executable, suite], cwd=tree, capture_output=True,
                              text=True, timeout=TIMEOUT,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1")).returncode
    except subprocess.TimeoutExpired:
        return 124


def main():
    tmp = tempfile.mkdtemp()
    base = os.path.join(tmp, "base")
    shutil.copytree(ROOT, base, ignore=shutil.ignore_patterns("__pycache__", "*.zip", ".git"))
    original = open(os.path.join(base, KERNEL), encoding="utf-8").read()

    baseline = {s: run_suite(base, s) for s in SUITES}
    if any(rc != 0 for rc in baseline.values()):
        print("FAIL — the suites are not green before mutation; fix that first:")
        for s, rc in baseline.items():
            print(f"  {s}: exit {rc}")
        shutil.rmtree(tmp, ignore_errors=True)
        return 1
    print(f"baseline: both suites green in the unmutated copy")

    killed, survived, broken = [], [], []
    for label, (anchor, replacement) in MUTANTS.items():
        if original.count(anchor) != 1:
            broken.append(label)
            print(f"  BROKEN {label} — anchor matched {original.count(anchor)} times "
                  "(this file is testing a kernel that changed)")
            continue
        open(os.path.join(base, KERNEL), "w", encoding="utf-8").write(
            original.replace(anchor, replacement))
        results = {s: run_suite(base, s) for s in SUITES}
        if any(rc != 0 for rc in results.values()):
            killed.append(label)
            reds = [s.split("/")[-1] for s, rc in results.items() if rc != 0]
            print(f"  killed  {label}  →  {', '.join(reds)} went red")
        else:
            survived.append(label)
            print(f"  SURVIVED {label} — no fixture noticed this property disappearing")
    open(os.path.join(base, KERNEL), "w", encoding="utf-8").write(original)
    shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n{len(killed)} killed, {len(survived)} survived, {len(broken)} broken anchors")
    if survived or broken:
        for label in survived:
            print(f"  SURVIVOR: {label}")
        for label in broken:
            print(f"  BROKEN ANCHOR: {label}")
        print("mutation adequacy: RED — a claimed property has no fixture defending it")
        return 1
    print("mutation adequacy: every injected regression was caught by a fixture")
    return 0


if __name__ == "__main__":
    sys.exit(main())

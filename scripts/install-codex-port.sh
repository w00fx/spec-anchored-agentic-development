#!/usr/bin/env bash
# Materialize only Codex-specific custom-agent adapters.
# Shared skills, protocols, rules, and root instructions are already canonical:
#   .agents/skills/  .agents/protocols/  .agents/rules/  AGENTS.md
set -euo pipefail

[ -d .agents/skills ] || { echo "run from the repo root (needs .agents/skills)"; exit 1; }
[ -f .agents/protocols/implementation-protocol.md ] || { echo "missing .agents/protocols/implementation-protocol.md"; exit 1; }
[ -f AGENTS.md ] || { echo "missing root AGENTS.md"; exit 1; }
for name in general-code-reviewer mutation-hardener; do
  [ -f "agents/$name.md" ] || { echo "missing agents/$name.md"; exit 1; }
  [ -f "agents/$name.toml" ] || { echo "missing agents/$name.toml"; exit 1; }
done

validate_contracts() {
  python3 - <<'PY'
from pathlib import Path
import tomllib
import yaml

expected = {"general-code-reviewer", "mutation-hardener"}
mds = {p.stem: p for p in Path("agents").glob("*.md")}
tomls = {p.stem: p for p in Path("agents").glob("*.toml")}
if set(mds) != expected or set(tomls) != expected:
    raise SystemExit("agents/: expected exactly the two canonical Markdown/TOML role pairs")

for stem in sorted(expected):
    text = mds[stem].read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SystemExit(f"{mds[stem]}: invalid frontmatter")
    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n").rstrip() + "\n"
    if "model" in fm:
        raise SystemExit(f"{mds[stem]}: must inherit the Owner model")
    if fm.get("effort") != "max":
        raise SystemExit(f"{mds[stem]}: must declare effort=max")
    with tomls[stem].open("rb") as fh:
        data = tomllib.load(fh)
    if "model" in data:
        raise SystemExit(f"{tomls[stem]}: must inherit the parent model")
    if data.get("model_reasoning_effort") != "max":
        raise SystemExit(f"{tomls[stem]}: must use model_reasoning_effort=max")
    if data.get("developer_instructions", "").rstrip() + "\n" != body:
        raise SystemExit(f"agents/{stem}: Markdown/TOML instructions drifted")

for skill in (
    "explain", "implement", "orchestrate", "plan-from-issue", "prep",
    "review-spec-drift", "shape", "spec-to-tickets", "to-spec",
    "implement-feature", "implement-orchestrated", "implement-backlog",
):
    p = Path(".agents/skills") / skill / "SKILL.md"
    meta = p.parent / "agents" / "openai.yaml"
    if not p.is_file():
        raise SystemExit(f"missing explicit skill: {p}")
    if not meta.is_file():
        raise SystemExit(f"missing Codex explicit-invocation metadata: {meta}")
    obj = yaml.safe_load(meta.read_text(encoding="utf-8")) or {}
    if obj.get("policy", {}).get("allow_implicit_invocation") is not False:
        raise SystemExit(f"{meta}: allow_implicit_invocation must be false")
PY
}

validate_contracts

CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

if [ "$CHECK" = "1" ]; then
  for retired in .claude/skills .claude/rules .claude/logs .claude/commands .claude/agents .claude/protocols; do
    [ ! -e "$retired" ] || { echo "FAIL - retired shared surface exists: $retired"; exit 1; }
  done
  if [ -d .codex/agents ]; then
    diff -r agents/general-code-reviewer.toml .codex/agents/general-code-reviewer.toml >/dev/null
    diff -r agents/mutation-hardener.toml .codex/agents/mutation-hardener.toml >/dev/null
    actual=$(find .codex/agents -maxdepth 1 -name '*.toml' -print | wc -l | tr -d ' ')
    [ "$actual" = "2" ] || { echo "FAIL - .codex/agents contains an unexpected role"; exit 1; }
    echo "OK - installed Codex agents match the canonical root contracts"
  else
    echo "OK - canonical Codex agent sources validate (.codex/agents not installed)"
  fi
  exit 0
fi

rm -rf .codex/agents
mkdir -p .codex/agents
cp agents/general-code-reviewer.toml .codex/agents/general-code-reviewer.toml
cp agents/mutation-hardener.toml .codex/agents/mutation-hardener.toml

echo "Codex custom agents materialized under .codex/agents/."
echo "Shared skills already live natively under .agents/skills/."
echo "Run: bash scripts/install-codex-port.sh --check"

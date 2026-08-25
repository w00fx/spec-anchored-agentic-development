#!/usr/bin/env bash
# EXPERIMENTAL coexistence materializer for the Codex side (Option A).
# Sync semantics: generated dirs are disposable and rebuilt whole.
# Portable: no GNU-only sed -i (macOS stock sed differs). Smoke-test
# on ubuntu-latest AND macos-latest before trusting: EVAL-018 / EVAL-013.
set -euo pipefail
[ -d .claude/skills ] || { echo "run from the repo root (needs .claude/skills)"; exit 1; }

# --check: rebuild into a temp tree and fail on divergence (CI gate).
CHECK=0; [ "${1:-}" = "--check" ] && CHECK=1
if [ "$CHECK" = "1" ]; then
  tmpdir=$(mktemp -d); trap 'rm -rf "$tmpdir"' EXIT
  cp -R . "$tmpdir/repo"; ( cd "$tmpdir/repo" && bash scripts/install-codex-port.sh >/dev/null )
  if diff -r "$tmpdir/repo/.agents/skills" .agents/skills >/dev/null 2>&1 \
     && diff -r "$tmpdir/repo/agent-system/protocols" agent-system/protocols >/dev/null 2>&1 \
     && diff "$tmpdir/repo/.codex/agents/reviewer.toml" .codex/agents/reviewer.toml >/dev/null 2>&1; then
    echo "OK - Codex port matches a fresh materialization"; exit 0
  fi
  echo "FAIL - Codex port drifted from the canonical corpus; rerun the installer"; exit 1
fi

# 1) Neutral shared protocol corpus (RECURSIVE — references included)
rm -rf agent-system/protocols && mkdir -p agent-system/protocols
cp -R .claude/protocols/. agent-system/protocols/
test -f agent-system/protocols/references/scope-manifest-schema.md \
  || { echo "FATAL: protocol references missing after copy"; exit 1; }

# 2) Skills mirror with sync-delete
rm -rf .agents/skills && mkdir -p .agents/skills
cp -R .claude/skills/. .agents/skills/
python3 - "$PWD/.agents/skills" << 'PY'
import sys, pathlib
root = pathlib.Path(sys.argv[1])
for p in root.rglob('*'):
    if p.is_file():
        try: s = p.read_text()
        except UnicodeDecodeError: continue
        if '.claude/protocols/' in s:
            p.write_text(s.replace('.claude/protocols/', 'agent-system/protocols/'))
PY

# 3) Invocation policy for transactional skills (explicit-only)
for s in implement-feature implement-orchestrated implement-backlog; do
  mkdir -p ".agents/skills/$s/agents"
  printf 'policy:\n  allow_implicit_invocation: false\n' > ".agents/skills/$s/agents/openai.yaml"
done

# 4) Reviewer agent
mkdir -p .codex/agents
cat > .codex/agents/reviewer.toml << 'TOML'
name = "reviewer"
description = "Fresh-context, decorrelated reviewer (context separation, not independent proof). Report-only over an immutable candidate."
developer_instructions = """
You did not write the work you are reviewing. Load the applicable
review lenses from .agents/skills/ and judge the target — a diff, or a
no-change evidence target — against the ratified spec's pointed IDs.
Report [BLOCKER]/[SHOULD]/[NIT] with location and concrete fix. You
may RUN the repo's declared verification commands; you never stage,
commit, amend, push, or open PRs — any tracked-file mutation you cause
is itself a finding.
"""
model = "gpt-5.6-sol"
model_reasoning_effort = "xhigh"   # declared adapter exception (see INSTALL); expires without EVAL-014
sandbox_mode = "workspace-write"
TOML

# 5) Normalized drift gate: apply the expected transform to a temp copy
echo "Drift check (normalized; should print nothing):"
tmp=$(mktemp -d)
cp -R .claude/skills/. "$tmp/"
python3 - "$tmp" << 'PY'
import sys, pathlib
root = pathlib.Path(sys.argv[1])
for p in root.rglob('*'):
    if p.is_file():
        try: s = p.read_text()
        except UnicodeDecodeError: continue
        if '.claude/protocols/' in s:
            p.write_text(s.replace('.claude/protocols/', 'agent-system/protocols/'))
PY
diff -r "$tmp" .agents/skills -x 'agents' || true
rm -rf "$tmp"

echo "Experimental coexistence materializer done — NOT a verified port."
echo "Qualify: Codex lists the skills; \$implement-orchestrated resolves;"
echo "protocol references resolve; reviewer runs tests; rerun leaves no stale files."

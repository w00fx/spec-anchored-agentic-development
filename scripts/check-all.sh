#!/usr/bin/env bash
# The single gate. CI runs THIS.
#
# No environment variable changes which checks run: the tenth audit
# showed SA_NESTED=1 could paint a red suite green. Every suite is
# invoked here, directly, exactly once, and the structural validator
# no longer runs suites of its own.
set -uo pipefail
unset SA_NESTED 2>/dev/null || true
cd "$(dirname "$0")/.."
fail=0
# Per-step budgets in seconds, enforced as REAL timeouts. Defaults carry
# headroom over observed times because a threshold with one second of margin
# fails on ambient load rather than on a regression (closure v2, P1-04).
# Calibrate from your CI's p95 and require three consecutive green runs.
# Override with SA_BUDGET_<STEP>=n.
# A gate that cannot measure itself cannot hold a budget (closure v1, P1-07).
budget_for() { case "$1" in compile) echo "${SA_BUDGET_COMPILE:-30}";; shell) echo "${SA_BUDGET_SHELL:-30}";;
  structural) echo "${SA_BUDGET_STRUCTURAL:-60}";; kernel*) echo "${SA_BUDGET_KERNEL:-15}";;
  corpus) echo "${SA_BUDGET_CORPUS:-420}";; mutation) echo "${SA_BUDGET_MUTATION:-420}";;
  *) echo "${SA_BUDGET_DEFAULT:-120}";; esac; }
total=0
step() {
  local key="$1" label="$2"; shift 2
  echo; echo "== $label"
  local t0=$(date +%s)
  local b_pre; b_pre=$(budget_for "$key")
  # A hung step must die at the budget, not merely be reported late — and it
# must do so everywhere, not only where a compatible timeout(1) exists.
  python3 scripts/run-step.py "$b_pre" "$@" || {
    local rc=$?
    [ "$rc" = 124 ] && echo "   ^ TIMED OUT at ${b_pre}s" || echo "   ^ FAILED"
    fail=1; }
  local dt=$(( $(date +%s) - t0 )); total=$(( total + dt ))
  local b; b=$(budget_for "$key")
  if [ "$dt" -gt "$b" ]; then
    echo "   ^ ${dt}s exceeds the ${b}s budget for this step"; fail=1
  else
    echo "   (${dt}s / ${b}s)"
  fi
}

export PYTHONDONTWRITEBYTECODE=1
# py_compile writes bytecode regardless of the flag above; keep it out of
# the consumer's tree entirely (twelfth audit, P1-06)
export PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/sa-pycache-$$"
trap 'rm -rf "$PYTHONPYCACHEPREFIX"' EXIT
step "compile" "compile every python artifact" python3 -m py_compile \
  scripts/spec-anchored scripts/validate-bundle.py tests/_harness.py \
  tests/test_kernel_contracts.py tests/test_kernel_adversarial.py \
  tests/test_corpus.py tests/test-mutants.py
step "shell" "parse every shell script" bash -c 'find . -name "*.sh" -not -path "*/node_modules/*" -print0 | while IFS= read -r -d "" f; do bash -n "$f" || exit 1; done'
step "structural" "structural gate (corpus, frontmatter, retired forms)" python3 scripts/validate-bundle.py
step "kernel" "kernel contract checks (fast)" python3 tests/test_kernel_contracts.py
step "kernel" "kernel adversarial fixtures (fast)" python3 tests/test_kernel_adversarial.py
step "corpus" "corpus fixtures (slow, run once)" python3 tests/test_corpus.py
step "mutation" "mutation adequacy (do the fixtures kill regressions?)" python3 tests/test-mutants.py
step "other" "canonical skill/agent adapter validation" bash scripts/install-codex-port.sh --check
echo
if [ "$fail" = "0" ]; then
  echo "ALL GREEN — structural + contract + mutation level. Total: ${total}s"
  echo "Inner loop: run only the two fast kernel suites while editing."
  echo "This full gate is the pre-push / CI budget — timing is environment-"
  echo "specific; measure it in your CI rather than trusting a number here."
  echo "NOT covered here: environment verification (real git, agent commit handoffs,"
  echo "Owner disposition, PR/external-review events, launcher) and every integration eval."
else
  echo "RED — see failures above"
fi
exit $fail

#!/usr/bin/env bash
# require-spec-for-new-capability.sh — example PreToolUse hook (OPT-IN)
#
# Poka-yoke enforcement of spec-first + package-by-feature: blocks creating
# a NEW top-level capability folder under src/ (or app/, lib/, packages/)
# when no matching specs/<capability>/ exists. Existing folders are not
# affected (brownfield-safe). Naming quality (business verb vs data noun)
# is not mechanically checkable and stays with the package-by-feature rule
# and the reviewer — this hook enforces only the checkable part.
#
# Wire it (opt-in) in .claude/settings.json:
# {
#   "hooks": {
#     "PreToolUse": [
#       { "matcher": "Write|Edit|MultiEdit",
#         "hooks": [
#           { "type": "command",
#             "command": "bash .claude/hooks/require-spec-for-new-capability.sh" }
#         ] }
#     ]
#   }
# }
#
# Exit 0 = allow. Exit 2 = block; stderr goes back to the model as feedback.
# Hook APIs evolve — verify the settings schema against current Claude Code
# docs when wiring.

FILE_PATH=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
[ -z "$FILE_PATH" ] && exit 0

REL="${FILE_PATH#"$PWD"/}"

for ROOT in src app lib packages; do
  case "$REL" in
    "$ROOT"/*/*)
      CAP="${REL#"$ROOT"/}"; CAP="${CAP%%/*}"
      if [ ! -d "$ROOT/$CAP" ] && [ ! -d "specs/$CAP" ]; then
        {
          echo "Blocked: creating new capability folder '$ROOT/$CAP/' with no matching 'specs/$CAP/'."
          echo "Spec-first: write the capability spec first (specs/$CAP/$CAP.md — see /interview-spec), then implement."
          echo "If '$CAP' is not a capability (an entity or layer folder), it fails package-by-feature — see .claude/rules/package-by-feature.md."
        } >&2
        exit 2
      fi
      ;;
  esac
done
exit 0

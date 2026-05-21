#!/usr/bin/env bash
# =============================================================================
# codebase-memory: install_hook.sh
# =============================================================================
# Installs the PostToolUse hook into the project's .claude/settings.json
# so Claude Code fires post_tool_use_hook.sh after every Bash tool call.
#
# The hook checks for the layered memory/ directory structure:
#   memory/codebase.md           ← master index
#   memory/modules/<n>.md        ← per-module deep dives
#   memory/maps/file_index.json  ← file → class/function lookup
#   memory/maps/call_graph.json  ← import dependency graph
#
# Usage:
#   bash .claude/skills/codebase-memory/hooks/install_hook.sh
#
# Uninstall:
#   bash .claude/skills/codebase-memory/hooks/install_hook.sh --uninstall
# =============================================================================

set -euo pipefail

UNINSTALL=false
USER_SCOPE=false

for arg in "$@"; do
  case "${arg}" in
    --uninstall) UNINSTALL=true ;;
    --user)      USER_SCOPE=true ;;
  esac
done

# ── Resolve settings file location ───────────────────────────────────────────
if [[ "${USER_SCOPE}" == "true" ]]; then
  # User scope: ~/.claude/settings.json — applies to ALL projects
  CLAUDE_DIR="${HOME}/.claude"
  SCOPE_LABEL="user (global)"
else
  # Project scope: <project-root>/.claude/settings.json
  find_project_root() {
    local dir="${PWD}"
    while [[ "${dir}" != "/" ]]; do
      [[ -d "${dir}/.git" || -d "${dir}/.claude" ]] && echo "${dir}" && return
      dir="$(dirname "${dir}")"
    done
    echo "${PWD}"
  }
  ROOT="$(find_project_root)"
  CLAUDE_DIR="${ROOT}/.claude"
  SCOPE_LABEL="project (${ROOT})"
fi

SETTINGS="${CLAUDE_DIR}/settings.json"
# Hook always lives in the user skills dir so the path is stable across projects
SKILL_HOOK="${HOME}/.claude/skills/codebase-memory/hooks/post_tool_use_hook.sh"

mkdir -p "${CLAUDE_DIR}"

# ── Require python3 ───────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
  echo "Error: python3 is required." >&2; exit 1
fi

# ── Make hook executable ──────────────────────────────────────────────────────
[[ -f "${SKILL_HOOK}" ]] && chmod +x "${SKILL_HOOK}"

# ── Merge hook entry into settings.json (Python handles JSON safely) ─────────
python3 - "${SETTINGS}" "${SKILL_HOOK}" "${UNINSTALL}" <<'PYEOF'
import sys, json, pathlib

settings_path = pathlib.Path(sys.argv[1])
hook_script   = sys.argv[2]
uninstall     = sys.argv[3].lower() == "true"
hook_command  = f"bash {hook_script}"

try:
    data = json.loads(settings_path.read_text()) if settings_path.exists() else {}
except json.JSONDecodeError:
    data = {}

hooks     = data.setdefault("hooks", {})
post      = hooks.setdefault("PostToolUse", [])
bash_block = next((b for b in post if b.get("matcher") == "Bash"), None)

if bash_block is None:
    bash_block = {"matcher": "Bash", "hooks": []}
    post.append(bash_block)

entry = {"type": "command", "command": hook_command}

if uninstall:
    bash_block["hooks"] = [h for h in bash_block["hooks"]
                           if h.get("command") != hook_command]
    if not bash_block["hooks"]:
        post.remove(bash_block)
    if not post:
        del hooks["PostToolUse"]
    print("✅ Hook uninstalled.")
else:
    if not any(h.get("command") == hook_command for h in bash_block["hooks"]):
        bash_block["hooks"].append(entry)
        print(f"✅ Hook installed.")
    else:
        print("ℹ️  Hook already installed — nothing changed.")

settings_path.parent.mkdir(parents=True, exist_ok=True)
settings_path.write_text(json.dumps(data, indent=2))
PYEOF

echo ""
echo "Scope:    ${SCOPE_LABEL}"
echo "Settings: ${SETTINGS}"
echo ""

if [[ "${UNINSTALL}" == "false" ]]; then
  if [[ "${USER_SCOPE}" == "true" ]]; then
    echo "The hook is now active for ALL your projects."
    echo "It fires after the first Bash call in each Claude Code session and"
    echo "checks that memory/ is present, complete, and not stale."
  else
    echo "The hook is active for this project only."
    echo "Run with --user to install globally for all projects."
  fi
  echo ""
  echo "Next — open a project in Claude Code and run:"
  echo '  "Please analyse this codebase and create the memory/ directory"'
  echo ""
  echo "Expected output:"
  echo "  memory/"
  echo "  ├── codebase.md"
  echo "  ├── modules/"
  echo "  │   └── <module>.md  (one per top-level module)"
  echo "  └── maps/"
  echo "      ├── file_index.json"
  echo "      └── call_graph.json"
fi

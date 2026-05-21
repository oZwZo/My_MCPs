#!/usr/bin/env bash
# =============================================================================
# codebase-memory: post_tool_use_hook.sh
# =============================================================================
# Claude Code PostToolUse hook.
#
# Fires after every Bash tool call. On the FIRST run in a project session it
# checks whether the layered memory directory exists and is populated, then
# prints an actionable prompt if anything is missing or stale.
#
# Expected memory layout:
#   memory/
#   ├── codebase.md          ← master index (must exist)
#   ├── modules/*.md         ← per-module deep dives
#   └── maps/
#       ├── file_index.json
#       └── call_graph.json
#
# Claude Code hook contract:
#   stdin  → JSON { tool_name, tool_input, tool_response }
#   stdout → shown to the user / agent as a hook message
#   exit 0 → continue normally
#   exit 2 → block tool call (not used here)
# =============================================================================

set -euo pipefail

# Consume stdin (required by hook protocol even if we don't use it)
PAYLOAD=$(cat)

# ── Resolve project root ──────────────────────────────────────────────────────
find_project_root() {
  local dir="${PWD}"
  while [[ "${dir}" != "/" ]]; do
    [[ -d "${dir}/.git" || -d "${dir}/.claude" ]] && echo "${dir}" && return
    dir="$(dirname "${dir}")"
  done
  echo "${PWD}"
}

PROJECT_ROOT="$(find_project_root)"
MEMORY_DIR="${PROJECT_ROOT}/memory"
MASTER_FILE="${MEMORY_DIR}/codebase.md"
MAPS_DIR="${MEMORY_DIR}/maps"
MODULES_DIR="${MEMORY_DIR}/modules"
SENTINEL="${PROJECT_ROOT}/.claude/.memory_check_done"

# ── Only check once per session ───────────────────────────────────────────────
[[ -f "${SENTINEL}" ]] && exit 0
mkdir -p "${PROJECT_ROOT}/.claude"
touch "${SENTINEL}"

# ── Helper: count files matching a glob ──────────────────────────────────────
count_files() { find "$1" -maxdepth 1 -name "$2" 2>/dev/null | wc -l | tr -d ' '; }

# ── Case 1: No memory directory at all ───────────────────────────────────────
if [[ ! -d "${MEMORY_DIR}" ]]; then
  cat <<'EOF'

╔══════════════════════════════════════════════════════════════════════╗
║  🧠  codebase-memory: memory/ directory not found                   ║
╠══════════════════════════════════════════════════════════════════════╣
║  No layered memory exists for this project yet.                     ║
║                                                                     ║
║  Generate the full memory structure now:                            ║
║                                                                     ║
║  "Please analyse this codebase and create the memory/ directory"    ║
║                                                                     ║
║  This will produce:                                                 ║
║    memory/codebase.md        ← master index (always loaded)        ║
║    memory/modules/<n>.md     ← per-module deep dives               ║
║    memory/maps/file_index.json                                      ║
║    memory/maps/call_graph.json                                      ║
╚══════════════════════════════════════════════════════════════════════╝

EOF
  exit 0
fi

# ── Case 2: memory/ exists but is incomplete ─────────────────────────────────
MISSING=()
[[ ! -f "${MASTER_FILE}" ]]                          && MISSING+=("memory/codebase.md (master index)")
[[ ! -f "${MAPS_DIR}/file_index.json" ]]             && MISSING+=("memory/maps/file_index.json")
[[ ! -f "${MAPS_DIR}/call_graph.json" ]]             && MISSING+=("memory/maps/call_graph.json")
MODULE_COUNT="$(count_files "${MODULES_DIR}" "*.md")"
[[ "${MODULE_COUNT}" -eq 0 ]]                        && MISSING+=("memory/modules/*.md (no module files found)")

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo ""
  echo "⚠️  codebase-memory: memory/ is incomplete. Missing:"
  for item in "${MISSING[@]}"; do
    echo "     • ${item}"
  done
  echo ""
  echo "   Run: \"Please complete the codebase memory structure\""
  echo ""
  exit 0
fi

# ── Case 3: Memory exists — check staleness (>30 days) ───────────────────────
STALE_MASTER=""
if command -v find &>/dev/null; then
  STALE_MASTER="$(find "${MASTER_FILE}" -mtime +30 -print 2>/dev/null || true)"
fi

if [[ -n "${STALE_MASTER}" ]]; then
  cat <<'EOF'

⚠️  codebase-memory: memory/codebase.md is over 30 days old.
   Consider refreshing: "Please update the codebase memory"

EOF
fi

# ── Case 4: All good — silent ─────────────────────────────────────────────────
exit 0

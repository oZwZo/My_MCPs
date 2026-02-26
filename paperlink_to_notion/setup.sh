#!/usr/bin/env bash
# setup.sh — Install the paperlink_to_notion skill and hook into Claude Code
#
# Usage:
#   chmod +x setup.sh && ./setup.sh
#
# What it does:
#   1. Symlinks SKILL.md → ~/.claude/skills/paperlink_to_notion/SKILL.md
#   2. Makes hook.sh executable
#   3. Patches ~/.claude/settings.json to register the UserPromptSubmit hook

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/SKILL.md"
HOOK_SRC="$SCRIPT_DIR/hook.sh"

CLAUDE_DIR="$HOME/.claude"
SKILL_DEST_DIR="$CLAUDE_DIR/skills/paperlink_to_notion"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

echo "▸ Installing paperlink_to_notion skill…"

# ── 1. Install skill ──────────────────────────────────────────────────────────
mkdir -p "$SKILL_DEST_DIR"

if [ -L "$SKILL_DEST_DIR/SKILL.md" ]; then
  rm "$SKILL_DEST_DIR/SKILL.md"
fi
ln -s "$SKILL_SRC" "$SKILL_DEST_DIR/SKILL.md"
echo "  ✓ Skill symlinked: $SKILL_DEST_DIR/SKILL.md → $SKILL_SRC"

# ── 2. Make hook executable ───────────────────────────────────────────────────
chmod +x "$HOOK_SRC"
echo "  ✓ Hook is executable: $HOOK_SRC"

# ── 3. Patch ~/.claude/settings.json ─────────────────────────────────────────
mkdir -p "$CLAUDE_DIR"

HOOK_ENTRY=$(cat <<HOOK
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "$HOOK_SRC"
    }
  ]
}
HOOK
)

if [ ! -f "$SETTINGS_FILE" ]; then
  # Create settings.json from scratch
  python3 - "$SETTINGS_FILE" "$HOOK_SRC" <<'PY'
import json, sys
settings_path = sys.argv[1]
hook_path = sys.argv[2]
settings = {
    "hooks": {
        "UserPromptSubmit": [
            {
                "matcher": "",
                "hooks": [{"type": "command", "command": hook_path}]
            }
        ]
    }
}
with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)
print(f"  ✓ Created {settings_path}")
PY
else
  # Merge into existing settings.json
  python3 - "$SETTINGS_FILE" "$HOOK_SRC" <<'PY'
import json, sys

settings_path = sys.argv[1]
hook_path = sys.argv[2]

with open(settings_path) as f:
    settings = json.load(f)

hooks_section = settings.setdefault("hooks", {})
prompt_hooks = hooks_section.setdefault("UserPromptSubmit", [])

# Check if our hook is already registered
already_registered = any(
    any(h.get("command") == hook_path for h in entry.get("hooks", []))
    for entry in prompt_hooks
)

if already_registered:
    print(f"  ✓ Hook already registered in {settings_path}")
else:
    prompt_hooks.append({
        "matcher": "",
        "hooks": [{"type": "command", "command": hook_path}]
    })
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
    print(f"  ✓ Hook registered in {settings_path}")
PY
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  /paperlink_to_notion https://www.nature.com/articles/..."
echo "  /paperlink_to_notion https://arxiv.org/abs/..."
echo "  /paperlink_to_notion https://pmc.ncbi.nlm.nih.gov/articles/..."
echo ""
echo "Or just paste a bare paper URL — the hook will detect it automatically."

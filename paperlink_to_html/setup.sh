#!/usr/bin/env bash
# setup.sh — Install the paperlink_to_html skill into Claude Code.
#
# Usage:
#   chmod +x setup.sh && ./setup.sh
#
# What it does (idempotent):
#   1. Creates ~/.claude/skills/paperlink_to_html/ if missing
#   2. Symlinks SKILL.md → ~/.claude/skills/paperlink_to_html/SKILL.md
#   3. Marks the Python entry points executable
#   4. Smoke-tests the renderer against examples/example_paper_info.json
#
# This script does NOT modify ~/.claude/settings.json — there is no
# auto-trigger bash hook for this skill. Invoke via /paperlink_to_html
# in chat, or run scripts/render_html.py from the shell.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/SKILL.md"
CLAUDE_DIR="$HOME/.claude"
SKILL_DEST_DIR="$CLAUDE_DIR/skills/paperlink_to_html"

echo "▸ Installing paperlink_to_html skill…"

# ── 1. Symlink SKILL.md into ~/.claude/skills/paperlink_to_html/ ─────────────
mkdir -p "$SKILL_DEST_DIR"

if [ -L "$SKILL_DEST_DIR/SKILL.md" ] || [ -f "$SKILL_DEST_DIR/SKILL.md" ]; then
  rm "$SKILL_DEST_DIR/SKILL.md"
fi
ln -s "$SKILL_SRC" "$SKILL_DEST_DIR/SKILL.md"
echo "  ✓ Skill symlinked: $SKILL_DEST_DIR/SKILL.md → $SKILL_SRC"

# ── 2. Make Python entry points executable ───────────────────────────────────
chmod +x "$SCRIPT_DIR/scripts/render_html.py"
chmod +x "$SCRIPT_DIR/scripts/paper_to_guide.py"
echo "  ✓ Python entry points are executable"

# ── 3. Smoke-test the renderer ───────────────────────────────────────────────
TMP_OUT="$(mktemp /tmp/paperlink_html_smoke.XXXXXX.html)"
if python3 "$SCRIPT_DIR/scripts/render_html.py" \
        --json "$SCRIPT_DIR/examples/example_paper_info.json" \
        --out "$TMP_OUT" > /dev/null 2>&1; then
  size=$(wc -c < "$TMP_OUT" | tr -d ' ')
  echo "  ✓ Smoke test passed — rendered ${size} bytes to $TMP_OUT"
  rm -f "$TMP_OUT"
else
  echo "  ✗ Smoke test FAILED — see error above" >&2
  exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Use it three ways:"
echo ""
echo "  1) Inside Claude Code:"
echo "       /paperlink_to_html https://www.cell.com/cell/fulltext/<id>"
echo ""
echo "  2) Pure renderer from a JSON paper_info:"
echo "       python3 $SCRIPT_DIR/scripts/render_html.py \\"
echo "           --json paper_info.json --out ~/Downloads/guide.html"
echo ""
echo "  3) End-to-end via Anthropic API (needs ANTHROPIC_API_KEY):"
echo "       python3 $SCRIPT_DIR/scripts/paper_to_guide.py \\"
echo "           --url <PAPER_URL> --out ~/Downloads/guide.html"
echo ""

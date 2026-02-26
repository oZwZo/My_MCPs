#!/usr/bin/env bash
# paperlink_to_notion — UserPromptSubmit hook
#
# Fires on every user prompt. If the prompt looks like a bare paper URL
# (arxiv, nature, biorxiv, pubmed, pmc, science, cell, etc.) without any
# other instruction, it injects a context hint so Claude knows to run the
# paperlink_to_notion skill automatically.
#
# Install: reference this file from ~/.claude/settings.json or
#          .claude/settings.json in any project.

set -euo pipefail

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('prompt',''))" 2>/dev/null || echo "")

# ── Patterns that identify a research-paper URL ──────────────────────────────
PAPER_URL_PATTERN='https?://(arxiv\.org/(abs|pdf)/|www\.nature\.com/articles/|pubmed\.ncbi\.nlm\.nih\.gov/|pmc\.ncbi\.nlm\.nih\.gov/|www\.biorxiv\.org/content/|www\.medrxiv\.org/content/|www\.science\.org/doi/|www\.cell\.com/|www\.sciencedirect\.com/science/article/|www\.pnas\.org/doi/|genomebiology\.biomedcentral\.com/articles/|academic\.oup\.com/|journals\.plos\.org/|elifesciences\.org/articles/|www\.embopress\.org/doi/|onlinelibrary\.wiley\.com/doi/)'

# ── Check if the prompt is ONLY a URL (with optional whitespace) ─────────────
STRIPPED=$(echo "$PROMPT" | tr -d '[:space:]')
IS_BARE_URL=false
if echo "$STRIPPED" | grep -qiE "^$PAPER_URL_PATTERN"; then
  IS_BARE_URL=true
fi

# ── Check if prompt mentions a paper URL alongside other text ────────────────
HAS_PAPER_URL=false
if echo "$PROMPT" | grep -qiE "$PAPER_URL_PATTERN"; then
  HAS_PAPER_URL=true
fi

# ── Already explicit about what to do — don't interfere ─────────────────────
HAS_EXPLICIT_COMMAND=false
if echo "$PROMPT" | grep -qiE "(notion|save|add to|literature|/paperlink)"; then
  HAS_EXPLICIT_COMMAND=true
fi

# ── Decision logic ────────────────────────────────────────────────────────────
if [ "$IS_BARE_URL" = "true" ]; then
  # Bare URL with no instruction → auto-invoke the skill
  cat <<'JSON'
{
  "additionalContext": "The user has submitted a bare paper URL with no other instruction. Automatically invoke the `paperlink_to_notion` skill: read the paper at the given URL and save a fully-structured literature note to the Notion Literature database following all steps in the skill definition."
}
JSON
  exit 0
fi

if [ "$HAS_PAPER_URL" = "true" ] && [ "$HAS_EXPLICIT_COMMAND" = "false" ]; then
  # URL present but no clear Notion/save intent — add a soft reminder
  cat <<'JSON'
{
  "additionalContext": "The prompt contains a research paper URL. If the user wants to save this paper to Notion, the `paperlink_to_notion` skill is available. To invoke it explicitly: /paperlink_to_notion <url>"
}
JSON
  exit 0
fi

# All other prompts — do nothing
exit 0

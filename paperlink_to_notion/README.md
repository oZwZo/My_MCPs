# paperlink_to_notion

A Claude Code skill that reads a research paper URL and saves a fully-structured literature note to your Notion **Literature** database.

## What it produces

For each paper, the Notion page contains:

| Section | Content |
|---|---|
| **Infographic** | Hero callout · Mermaid pipeline diagram · 4-column task cards · Applications table · Stats row |
| **Abstract** | Verbatim |
| **Introduction** | Logical-flow summary (bold-lead paragraphs following the argument arc) |
| **Results** | Brief subsection summaries + every figure as a collapsible block with high-res PMC image and full caption |
| **Discussion** | Logical-flow summary |

Database properties filled: `Name`, `Author`, `Published Year`, `journal`, `Tags`, `Paper Signature`, `URL`, `status`.

---

## Installation

```bash
chmod +x setup.sh
./setup.sh
```

This will:
1. Symlink `SKILL.md` → `~/.claude/skills/paperlink_to_notion/SKILL.md`
2. Make `hook.sh` executable
3. Register the `UserPromptSubmit` hook in `~/.claude/settings.json`

---

## Usage

### Explicit invocation (slash command)
```
/paperlink_to_notion https://www.nature.com/articles/s41592-023-01899-8
/paperlink_to_notion https://arxiv.org/abs/2310.01234
/paperlink_to_notion https://pmc.ncbi.nlm.nih.gov/articles/PMC11166568/
```

### Auto-detection via hook
Paste a bare paper URL into Claude Code without any other text. The `UserPromptSubmit` hook detects it and automatically invokes the skill:
```
https://www.nature.com/articles/s41592-023-01899-8
```

### Supported URL sources
- `arxiv.org`
- `nature.com`
- `biorxiv.org` / `medrxiv.org`
- `pubmed.ncbi.nlm.nih.gov`
- `pmc.ncbi.nlm.nih.gov`
- `science.org`
- `cell.com` / `sciencedirect.com`
- `pnas.org`
- `genomebiology.biomedcentral.com`
- `elifesciences.org`
- `embopress.org`

---

## Notion database

- **Database URL:** `https://www.notion.so/02bc4f6199d9466faf95e95f97672939`
- **Data source ID:** `aaf641e3-6f3f-4b21-83d4-74c6d1613794`

To change the target database, update these two IDs in `SKILL.md` (Step 3 and Step 4).

---

## File structure

```
paperlink_to_notion/
├── SKILL.md      # Claude Code skill — full step-by-step instructions
├── hook.sh       # UserPromptSubmit hook — auto-detects bare paper URLs
├── setup.sh      # One-command installer
└── README.md     # This file
```

---

## Manual uninstall

```bash
rm ~/.claude/skills/paperlink_to_notion/SKILL.md
rmdir ~/.claude/skills/paperlink_to_notion
```

Then remove the hook entry from `~/.claude/settings.json`.

---

## Requirements

- Claude Code with Notion MCP server configured
- Notion database access via the MCP plugin
- Papers must have a PubMed Central (PMC) open-access version for full-text extraction and high-res figures (most Nature Methods / Nature / Cell papers after 2023 qualify)

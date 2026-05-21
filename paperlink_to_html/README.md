# paperlink_to_html

A Claude Code skill that turns a research paper (URL or hand-prepared notes)
into a long, self-contained, Distill-inspired **HTML learning guide** with:

- Sticky top bar with progress dots and a ☀ / ☾ dark-light toggle.
- Animated hero counters (tick-up on view).
- A spine of narrative sections (your own body HTML).
- An interactive analysis-pipeline flow (clickable D3 SVG with ▶ Play / ⏭ Step / ⟲ Reset).
- Slide-in **method deep-dive panels** with citation + DOI + intuition + KaTeX equations + schematic SVG + "why this method".
- Figure cards (three-tier fallback when the publisher blocks programmatic image fetch).
- Finding cards, comparison table, glossary with hover popovers, and a self-test quiz with inline explanations.
- Progressive enhancement: the page is readable without JavaScript; D3, KaTeX, anime.js are loaded from jsDelivr as optional upgrades.
- `prefers-reduced-motion` respected; mobile fallback for the flow.

## Two ways to invoke

### 1. Inside Claude Code

```text
/paperlink_to_html https://www.cell.com/cell/fulltext/<id>
```

The `SKILL.md` workflow guides Claude through resolving the paper, building a
structured `paper_info` dict, and rendering the HTML via the Python script.

### 2. From the shell

**Pure renderer** (no network, no API key, no third-party deps):

```bash
python3 scripts/render_html.py \
    --json /tmp/paper_info.json \
    --out  ~/Downloads/guide.html
```

**End-to-end** (requires `ANTHROPIC_API_KEY` and `pip install anthropic>=0.34`):

```bash
python3 scripts/paper_to_guide.py \
    --url https://www.cell.com/cell/fulltext/<id> \
    --out ~/Downloads/guide.html
```

### 3. Programmatic import

```python
import sys
sys.path.insert(0, "/Users/<you>/Documents/python_project/My_MCPs/paperlink_to_html")
from scripts.render_html import render_html

html_str = render_html(paper_info_dict, output_path="~/Downloads/guide.html")
```

## Install

```bash
cd ~/Documents/python_project/My_MCPs/paperlink_to_html
./setup.sh
```

`setup.sh` is idempotent. It creates `~/.claude/skills/paperlink_to_html/` and
symlinks `SKILL.md` into it so Claude Code can discover the skill.

## Layout

```
paperlink_to_html/
├── SKILL.md                      # Claude-facing workflow
├── README.md                     # this file
├── setup.sh                      # idempotent install
├── scripts/
│   ├── __init__.py               # exposes render_html()
│   ├── render_html.py            # pure renderer (the "hook function")
│   └── paper_to_guide.py         # end-to-end CLI (Anthropic API)
├── templates/
│   └── learning_guide.html.tpl   # the HTML/CSS/JS template
├── schemas/
│   └── paper_info.schema.json    # JSON schema for the renderer's input
└── examples/
    ├── example_paper_info.json   # synthetic smoke-test input
    └── README.md
```

## Schema overview

The renderer's input is a `paper_info` dict matching
`schemas/paper_info.schema.json`. Every field is optional with sensible
defaults — pass only what you have. The main pieces are:

| Field | Purpose |
|---|---|
| `title`, `authors_short`, `doi`, `paper_url`, `journal`, `year`, `eyebrow`, `lead_paragraph` | Hero |
| `hero_counters`, `sub_counters` | Animated stats |
| `sections` | Main narrative spine (each section has `body_html` — raw HTML) |
| `flow_nodes`, `flow_edges`, `flow_order` | Interactive analysis flow |
| `methods` | Deep-dive panels (citation, equations, schematic, why) |
| `figures` | Figure cards with fallback link-out |
| `findings` | Discovery cards |
| `comparison_headers`, `comparison_rows` | Prior-work comparison table |
| `glossary` | Hover popovers, auto-decorated on first mention |
| `quiz` | Multiple-choice self-test |
| `related_papers` | Bibliography list |
| `extra_css`, `extra_js` | Paper-specific custom CSS / JS |

See `schemas/paper_info.schema.json` for the full definition.

## Design notes

- **Pair, don't merge, with `paperlink_to_notion`.** That sister skill handles the Notion-side artifact. This one stays HTML-only so each can evolve independently.
- **Static-first.** The template renders an informative page even if every CDN library is blocked. D3, KaTeX, and anime.js progressively enhance it.
- **No build step.** The renderer uses Python stdlib alone. The end-to-end CLI is the only place an external package (`anthropic`) is needed, and only when you want URL → HTML in one shot.
- **Paraphrase, don't copy.** When authoring `paper_info` for a closed-access paper, paraphrase abstracts and discussion rather than reproducing verbatim passages. The renderer doesn't enforce this; the author does.

## License

Your call. The renderer, template, and skill workflow are original work; the
generated HTML's CSS/JS is generic web-design boilerplate. The text content
of any specific `paper_info` belongs to the author who wrote it.

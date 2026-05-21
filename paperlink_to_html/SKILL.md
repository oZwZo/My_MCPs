---
name: paperlink_to_html
description: Read a research paper URL (or already-gathered paper notes) and produce a long, self-contained Distill-inspired HTML learning guide with dark/light toggle, interactive analysis flow, clickable method deep-dive panels (with KaTeX equations + citation), figure cards with three-tier fallback, comparison table, glossary, self-test quiz, and progressive-enhancement fallbacks. Pairs with the paperlink_to_notion skill — this one is HTML-only.
argument-hint: <paper-url-or-instruction>
---

# Paper → HTML Learning Guide

Input: $ARGUMENTS

Follow every step below in order. Use the Python renderer at the end — do not re-author the HTML/CSS/JS by hand.

---

## Step 0 — Decide whether to invoke this skill

Invoke when the user wants a **standalone HTML learning guide** for a paper, e.g.:

- `/paperlink_to_html <url>`
- "make a learning guide for this paper"
- "Distill-style HTML summary of <paper>"
- "summarise this paper as a long HTML I can open in a browser"
- Chinese equivalents (例如「这篇论文做成 HTML 学习指南」).

If the user wants the **Notion side** instead, invoke `/paperlink_to_notion`. If they want both, run **both** skills back-to-back (this one produces HTML; that one produces a Notion page).

---

## Step 1 — Resolve the paper

Run these calls in parallel:

1. **WebSearch** `"<title or DOI from URL> abstract authors figures"` to confirm title, authors, journal, year, and DOI.
2. **WebSearch** `"site:pmc.ncbi.nlm.nih.gov <title or DOI>"` (biomed papers) or analogous open-access mirror to find the full text.
3. **WebFetch** the publisher landing page for the abstract; expect 403 from Cell/Nature/Science/bioRxiv and fall back to search-snippet aggregation.

---

## Step 2 — Classify the paper

Pick exactly one of these emphases; it determines what the HTML leads with:

| Paper type | HTML emphasis | Hero counters |
|---|---|---|
| **Resources / atlas** | Datasets (curated · newly generated · integrated), data-type illustrations, analysis pipeline | Sample counts, cell-type counts, niches |
| **Methods / tool** | Grammar / syntax interactivity, worked examples, mathematical primer | # examples, # parameters, time-to-model |
| **Experimental discovery** | Findings (largest section), figures, mechanism diagrams | # samples, # conditions, effect size |
| **Review** | Conceptual map, comparison table, key takeaways | # papers reviewed, # frameworks |

Add a `eyebrow` line that reflects the type (e.g. `"Cell · 2025 · Methods / tools paper"`).

---

## Step 3 — Gather full content (parallel calls)

For each of these, run a separate WebFetch/WebSearch:

- **Abstract** — full abstract (paraphrase if behind paywall; never reproduce verbatim if rights are unclear).
- **Introduction** — extract the logical argument; 5–7 short bullet labels you can lead each paragraph with.
- **Results** — list each subsection heading + 2–3 sentence summary + which figures relate.
- **Methods (for computational papers)** — extract equations, loss functions, distance metrics. Use exact LaTeX where possible.
- **Figures** — list figure numbers + complete captions verbatim where the paper itself is open; otherwise paraphrase per-panel.
- **Discussion** — main achievement, technical insight, limitations, outlook.
- **Related methods** — for every analysis method the paper uses, find its original paper (DOI), brief intuition, and key equation.
- **Prior comparable papers** — 4–8 comparable atlases / tools / studies for a comparison table.

---

## Step 4 — Build the `paper_info` JSON

Populate the schema at `schemas/paper_info.schema.json`. Required top-level keys:

```yaml
title:               # full paper title
authors_short:       # comma-separated first 6 authors + "..." + senior PIs, for hero
authors_full:        # full author list, for Notion-style metadata
doi:                 # 10.xxxx/...
journal:             # e.g. Cell, bioRxiv
year:                # integer
paper_url:           # canonical URL
eyebrow:             # short kicker like "bioRxiv · 2026 · Resources paper"
lead_paragraph:      # 2-4 sentences for the hero
page_title_short:    # browser-tab title + topbar brand (e.g. HDCA, CBHG)
theme_storage_key:   # localStorage key, e.g. "hdca-theme"
primary_accent:      # CSS hex for light theme (e.g. "#5b6cff")
primary_accent_dark: # CSS hex for dark theme

hero_counters:       # 3-4 big numbers across the top
  - value: 4.6
    decimals: 1
    suffix: M
    unit: "Dissociated cells & nuclei"
    desc: "scRNA + snRNA from community + new"
  - ...

sub_counters:        # 4-6 secondary numbers below the hero
  - {label: "organ samples", value: "186"}
  - ...

sections:            # ordered list; each becomes a <section data-anchor=...>
  - anchor: intro
    title: "What is HDCA?"
    body_html: |
      <p>...</p>
      <div class="sidenote">...</div>
  - anchor: datasets
    title: "The datasets"
    body_html: |
      <p>...</p>
      <table class="data">...</table>
  - ...

flow_section_intro:  # short paragraph above the analysis flow
flow_nodes:          # D3 graph data
  - {id: "raw", x: 70, y: 250, w: 130, h: 60,
     label: "Raw counts", sub: "...", method: null,  kind: "data"}
  - ...
flow_edges:
  - {from: "raw", to: "qc", dashed: false}
  - ...
flow_order:          # list of node IDs in playback order

methods:             # dict keyed by short name → deep panel content
  scVI:
    name: "scVI"
    subtitle: "Variational autoencoder for scRNA-seq integration"
    citation: "Lopez R., …, Nat Methods 2018."
    doi: "https://www.nature.com/articles/s41592-018-0229-2"
    intuition: |
      <p>scVI is a probabilistic deep generative model...</p>
    equations:       # LaTeX strings (no $$ delimiters)
      - "\\mathcal{L}_{\\text{scVI}} = -\\mathbb{E}_{q}\\!\\big[\\log p(x \\mid z, s)\\big] + \\mathrm{KL}\\big(q \\,\\|\\, p(z)\\big)"
    schematic_svg: |  # inline <svg>...</svg>; can be empty string
      <svg viewBox='0 0 380 160'>...</svg>
    why: "HDCA tried six methods..."
  scPoli: { ... }
  ...

figures:
  - {fig_no: 1, title: "HDCA overview", panels_html: "<b>a</b>, ... <b>b</b>, ...", link: "https://..."}
  - ...

findings:
  - {label: "Discovery 1 · Mesenchyme",
     title: "Mesenchyme progenitors → tissue-specific fibroblasts",
     body_html: "<p>...</p>"}
  - ...

comparison_headers:  # column titles for the prior-work comparison
comparison_rows:     # list of list of cells (HTML allowed)

glossary:
  - {id: "g-pcw", term: "PCW",  def: "Post-conceptional week."}
  - ...

quiz:                # 5–10 questions
  - question: "What does the 4.6M figure refer to?"
    options:
      a: "All cells"
      b: "Dissociated cells & nuclei only (3.6M curated + 1M new)"
      c: "Visium spots"
      d: "Just the new dissociations"
    correct: "b"
    explain: "The 4.6M is dissociated cells. Spatial cells are counted separately."

related_papers:      # list of {label, citation, url}

footer_note:         # optional disclaimer line; defaults to autogenerated date
```

Anything not provided gets a reasonable default; missing fields never crash the renderer.

---

## Step 5 — Render

Call the Python entry point:

```bash
python3 ~/Documents/python_project/My_MCPs/paperlink_to_html/scripts/render_html.py \
    --json /tmp/paper_info.json \
    --out  ~/Downloads/<short_name>_learning_guide.html
```

Or from inside Python:

```python
import sys
sys.path.insert(0, "/Users/weizhongzheng/Documents/python_project/My_MCPs/paperlink_to_html")
from scripts.render_html import render_html
render_html(paper_info_dict, output_path="~/Downloads/guide.html")
```

The renderer:
- Loads `templates/learning_guide.html.tpl`
- Substitutes `{{key}}` placeholders + pre-renders the list-driven chunks
- Writes the result (and returns it as a string)
- Uses Python stdlib only — no install needed

---

## Step 6 — Self-check

After rendering, do a quick sanity pass:

- Open the file in a browser; the hero counters should tick up.
- Click each method node in the analysis flow; the slide-in panel should open with citation + equations + "why" block.
- Toggle dark mode (☾ button); the theme should persist on reload.
- Try the quiz: pick wrong answers, then correct ones; the score should update.
- Resize the window narrow; the flow should remain readable (mobile fallback).

---

## Step 7 — (Optional) Also create the Notion page

If the user also wants a Notion entry, after rendering the HTML invoke the existing
`paperlink_to_notion` skill with the same `paper_info` content. The two skills
are deliberately decoupled — this one stays HTML-only so each can evolve
independently.

---

## Quality checklist (lessons distilled from prior runs)

- [ ] Hero counters are **separate modalities**, never summed if they measure different things (e.g. dissociated cells vs spatial-segmented cells).
- [ ] Analysis flow places method-selection benchmarks **before** the chosen method (parallel-fan → benchmark → winner), not after.
- [ ] Every method panel has citation + DOI link + intuition + ≥1 equation + "why HDCA / this paper picked it".
- [ ] Figure cards include verbatim captions (or per-panel paraphrase) + link-out fallback for paywalled / 403 sources.
- [ ] KaTeX equations have no whitespace right after `$` or right before `$`; block equations use `$$` on their own lines.
- [ ] The HTML works **without JavaScript** for static reading (progressive enhancement) — D3, KaTeX, anime.js are nice-to-haves loaded from jsDelivr.
- [ ] Dark + light themes both look polished; SVGs use `currentColor` so they invert cleanly.
- [ ] Mobile viewport (≤ 720 px) does not produce horizontal-scroll explosions; tables get `overflow-x: auto`.
- [ ] All paper-specific text is **paraphrased** when the source page is paywalled or 403-blocked. Never reproduce long verbatim passages of closed-access text.
- [ ] At the bottom of the HTML, a footer notes the generation date and where the text was sourced.

---

## Trigger phrases

This skill is invoked when the user:

- Types `/paperlink_to_html <url>`
- Asks for "HTML learning guide", "Distill-style HTML", "long HTML summary of <paper>", "interactive HTML walkthrough"
- Pastes a paper URL combined with words like "HTML", "learning guide", "self-contained page"
- Uses Chinese equivalents: 「HTML 学习指南」「论文 HTML 总结」「Distill 风格 HTML」

---
name: paperlink_to_html
description: Read a research paper URL (or already-gathered paper notes) and produce a long, self-contained Distill-inspired HTML learning guide with dark/light toggle, interactive analysis flow, clickable method deep-dive panels (with KaTeX equations + citation), figure cards with three-tier fallback, comparison table, glossary, self-test quiz, and progressive-enhancement fallbacks. Pairs with the paperlink_to_notion skill — this one is HTML-only.
argument-hint: <paper-url-or-instruction>
---

# Paper → HTML Learning Guide

Input: $ARGUMENTS

Follow every step below in order. The Python renderer in `scripts/render_html.py` exists for the **scaffolding** (hero, theme toggle, D3 analysis flow, quiz, glossary, footer). For the **content sections themselves**, write rich `body_html` blocks that include several custom inline SVG diagrams and animations per paper — the renderer treats `body_html` as raw HTML so anything you can write in TxPert-style standalone HTML is allowed. For ambitious papers it is also acceptable (and sometimes cleaner) to hand-author a fully bespoke single-file HTML in the spirit of `~/Documents/html-literatures/TxPert_Methods_Explainer.html` — see Step 4b below.

**Required interactive features (non-negotiable — every guide, every rendering path).** Even when hand-authoring the HTML, these three features MUST be present. The Path-A renderer gives them to you for free; if you hand-author, you must wire them yourself. Reference implementation: `~/Documents/html-literatures/Robin_Methods_Explainer.html`.

1. **Light / dark theme toggle.** A fixed-position button (top-right; ☾/☀ glyph) that flips `data-theme` on `<html>` between `"light"` and `"dark"`. Persist the choice in `localStorage` under a paper-specific key (e.g. `<short_name>-theme`). Pick the initial value from `localStorage`, falling back to `prefers-color-scheme`. All colours must come from CSS variables (`--bg`, `--text`, `--accent`, …) declared under both `:root, html[data-theme="dark"]` and `html[data-theme="light"]` so the page inverts cleanly. If Mermaid is used, re-init it on toggle with the matching theme variables.
2. **Interactive pipeline with clickable method panels.** Beyond the static Mermaid pipeline, include one *clickable* SVG pipeline where each method/agent/stage node has `class="pipeline-node" data-method="<key>"`. Clicking opens a slide-in side panel (`<aside class="method-panel">`) populated from a JS dict `{ key: { title, sub, cite, intuition, eqn, why } }` — citation (with DOI link), one-paragraph intuition, optional KaTeX equation, and a "Why this matters" callout. Close on × button, overlay click, or `Esc`. Re-typeset MathJax after each open (`MathJax.typesetPromise([panel])`).
3. **Self-test quiz.** A `<section id="quiz">` with 5–8 multiple-choice questions. Each `.q` has `data-correct="a|b|c|d"` and an `.explain` block that reveals on selection. Wrong picks should highlight the wrong answer in red AND simultaneously reveal the correct answer in green (so the reader learns from the miss). A live `Score: N / total` element updates on every change and turns green on a perfect run.

**Visual-density baseline (non-negotiable).** Beyond the three interactive features above, every guide must also include:

- **≥4 custom inline `<svg>` diagrams** placed inside the section `body_html` blocks (one per major concept), each with a `.diagram-caption`. Examples: a problem-setup illustration, an architecture diagram, a per-method schematic, a results/ablation bar-chart, a mechanism cartoon.
- **≥1 Mermaid flowchart** embedded with `<div class="mermaid">flowchart …</div>` for the overall pipeline (in addition to the clickable D3 / interactive-SVG flow), unless the paper is so short there is genuinely nothing left to flow-chart.
- **CSS keyframe animations** on at least one of those SVGs — pulsing nodes, dashed flow lines, shimmering edges, animated message dots, growing bars. The TxPert reference defines reusable classes `.pulse-node`, `.flow-line`, `.edge-shimmer`, `.glow-node` plus keyframes `pulseGlow`, `flowDash`, `pulse-node`, `messagePulse`, `shimmer` — copy these in via `extra_css`.
- **Stat tiles** (`.stat-tile` grid) under the hero and again next to the comparison/ablation table to break up text walls.
- **Animated message-passing or signal-flow** somewhere in the architecture section — `<animateMotion>` along a `path` is enough; do not let an architecture diagram sit static.

If you find yourself producing a guide that is mostly `<p>` + one D3 flow, stop and add diagrams. Use TxPert / Robin (linked above) as the lower bound for graphical density, not the upper bound.

**Reference templates.**

- `~/Documents/html-literatures/TxPert_Methods_Explainer.html` — gold standard for *graphical density* (custom inline SVGs per section, Mermaid, animated bars).
- `~/Documents/html-literatures/Robin_Methods_Explainer.html` — gold standard for *interactive features* (theme toggle + clickable pipeline with slide-in method panels + self-test quiz with live scoring) layered on top of TxPert's graphical density. Use this as the structural template when hand-authoring.

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

## Step 4 — Decide the rendering path

There are two acceptable rendering paths. Pick **one** based on the paper:

| Path | When to use | What you produce |
|---|---|---|
| **A · Renderer + rich `body_html`** | Default for most papers. You want the built-in D3 analysis flow, quiz, glossary, theme toggle to come "for free". | A `paper_info` dict where each `sections[i].body_html` field contains its own inline `<svg>` diagrams, mermaid blocks, callouts, stat tiles, and tables. Inject the reusable animation CSS via `extra_css`. |
| **B · Hand-authored single-file HTML** | Use when the paper has a strong visual identity (a custom architecture worth animating heavily, multi-panel results worth illustrating per-section) and the renderer's section list feels constraining. Reference template: `~/Documents/html-literatures/TxPert_Methods_Explainer.html`. | A complete standalone `.html` file with MathJax + Mermaid CDN, custom CSS (hero, TOC, cards, stat-tiles, callouts, keyframe animations), ≥4 custom inline `<svg>` diagrams, an embedded Mermaid flowchart, and a "TOC" nav. No Python renderer involved. |

In **both** paths the visual-density baseline above applies. The Notion page (if any) is produced separately by `paperlink_to_notion` regardless of which HTML path you pick.

## Step 4a — Build the `paper_info` JSON (Path A only)

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

### Step 4b — Body HTML must carry the diagrams

Each `sections[i].body_html` block should follow this template, not just `<p>` paragraphs:

```html
<p>…narrative paragraph(s) introducing the concept…</p>

<div class="diagram-frame">
  <svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
    <!-- Custom inline SVG: nodes (rect/circle), edges (line/path with markers),
         optional <animate>/<animateMotion>/CSS classes (.pulse-node, .flow-line,
         .edge-shimmer, .glow-node), labels (text). -->
  </svg>
  <p class="diagram-caption">One-sentence caption that explains the diagram.</p>
</div>

<p>…analytical text continuing after the diagram…</p>

<div class="callout tip">
  <strong>💡 Why this matters.</strong> …one short paragraph…
</div>
```

Aim for ≥1 diagram per major section. Reusable CSS lives in `extra_css`:

```css
@keyframes pulseGlow { 0%,100% { filter: drop-shadow(0 0 2px var(--accent)); opacity:1; } 50% { filter: drop-shadow(0 0 8px var(--accent)); opacity:0.85; } }
@keyframes flowDash  { to { stroke-dashoffset: -20; } }
@keyframes pulse-node{ 0%,100% { r:24; opacity:1; } 50% { r:27; opacity:0.9; } }
@keyframes shimmer   { 0%,100% { stroke-opacity:0.3; } 50% { stroke-opacity:1; } }
.pulse-node   { animation: pulse-node 2.4s ease-in-out infinite; transform-origin:center; transform-box:fill-box; }
.flow-line    { stroke-dasharray: 6 4; animation: flowDash 1.6s linear infinite; }
.edge-shimmer { animation: shimmer 2s ease-in-out infinite; }
.glow-node    { animation: pulseGlow 2.5s ease-in-out infinite; }
.diagram-frame   { background: var(--code-bg, #0b1018); border: 1px solid var(--rule); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0; text-align: center; }
.diagram-frame svg { max-width: 100%; height: auto; }
.diagram-caption { font-size: 0.85rem; color: var(--muted); font-style: italic; margin-top: 0.7rem; text-align: center; }
.stat-tile { background: linear-gradient(135deg, rgba(96,165,250,0.10), rgba(167,139,250,0.06)); border: 1px solid var(--rule); border-radius: 12px; padding: 1.1rem; text-align: center; }
.stat-tile .num { font-size: 1.7rem; font-weight: 700; color: var(--accent); display: block; }
.stat-tile .label { font-size: 0.78rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.3rem; }
.callout { border-left: 4px solid var(--accent); border-radius: 8px; padding: 1rem 1.2rem; margin: 1rem 0; background: rgba(96,165,250,0.08); }
.callout.warn    { background: rgba(251,191,36,0.08); border-left-color: #fbbf24; }
.callout.success { background: rgba(52,211,153,0.08); border-left-color: #34d399; }
.callout.tip     { background: rgba(167,139,250,0.08); border-left-color: #a78bfa; }
```

For Mermaid, include the script via `extra_js` once:

```js
import('https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js').then(m => m.default.initialize({ startOnLoad: true, theme: 'dark' }));
```

and put `<div class="mermaid">flowchart TB …</div>` in any `body_html`.

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

- [ ] **Three interactive features present:** theme toggle (☾/☀ button, localStorage-persisted), clickable pipeline with slide-in method panel (citation + intuition + equation + "why this matters"), and a self-test quiz (5–8 questions with live scoring and reveal-correct-on-wrong). Reference: `~/Documents/html-literatures/Robin_Methods_Explainer.html`.
- [ ] **Visual-density baseline met:** ≥4 custom inline SVG diagrams in body sections, ≥1 Mermaid flowchart, at least one with CSS keyframe / `<animateMotion>` animation, stat tiles under the hero AND near the comparison/ablation section. Reference: `~/Documents/html-literatures/TxPert_Methods_Explainer.html`.
- [ ] **Sections are not just `<p>` walls** — every major section has a `.diagram-frame` (SVG) or `.mermaid` or `.grid-2 of .card`s breaking up the prose.
- [ ] **MathJax re-typeset inside dynamic panels:** if the slide-in method panel contains a KaTeX/LaTeX equation, call `MathJax.typesetPromise([panel])` after populating it.
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

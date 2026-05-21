<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{page_title_short}} &middot; {{title}} &mdash; Learning guide</title>
<meta name="description" content="{{meta_description}}">

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css" crossorigin="anonymous">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Source+Sans+3:wght@300;400;600;700&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">

<style>
:root {
  --bg: #fffdf7; --bg-soft: #f7f4ea; --panel: #ffffff; --panel-2: #f0eee4;
  --fg: #1a1a1a; --fg-dim: #555; --muted: #8a8a85; --rule: #e3dfd1;
  --accent: {{primary_accent}}; --accent-2: #d0598c; --accent-3: #1aa185; --accent-4: #e88a3b; --accent-5: #8a5cf7;
  --shadow: 0 1px 2px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.05);
  --serif: 'Source Serif 4', Georgia, serif;
  --sans:  'Source Sans 3', system-ui, sans-serif;
  --mono:  'JetBrains Mono', ui-monospace, Menlo, monospace;
  --col: 720px; --col-wide: 1080px; --col-bleed: 1280px;
}
html[data-theme="dark"] {
  --bg: #0f131a; --bg-soft: #161b25; --panel: #1a1f2a; --panel-2: #232a37;
  --fg: #e8ecf2; --fg-dim: #b6bdc9; --muted: #7d8597; --rule: #2a3140;
  --accent: {{primary_accent_dark}}; --accent-2: #ff8ab5; --accent-3: #5be0c2; --accent-4: #f3b06a; --accent-5: #b18cff;
  --shadow: 0 1px 2px rgba(0,0,0,0.4), 0 8px 24px rgba(0,0,0,0.5);
}
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { background: var(--bg); color: var(--fg); font-family: var(--serif); font-size: 18px; line-height: 1.65; -webkit-font-smoothing: antialiased; transition: background 200ms ease, color 200ms ease; }
img { max-width: 100%; height: auto; }
a { color: var(--accent); text-decoration: none; border-bottom: 1px solid color-mix(in srgb, var(--accent) 35%, transparent); }
a:hover { color: var(--accent-2); border-color: var(--accent-2); }
h1, h2, h3, h4 { font-family: var(--serif); font-weight: 700; letter-spacing: -0.01em; line-height: 1.2; margin-top: 1.8em; }
h1 { font-size: clamp(2rem, 5vw, 3.2rem); margin-top: 0; }
h2 { font-size: clamp(1.6rem, 3.5vw, 2.1rem); border-bottom: 1px solid var(--rule); padding-bottom: .3em; }
h3 { font-size: 1.35rem; }
h4 { font-size: 1.1rem; color: var(--fg-dim); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
code, pre, kbd { font-family: var(--mono); font-size: 0.9em; }
pre { background: var(--panel-2); padding: 1em 1.2em; border-radius: 8px; overflow-x: auto; border: 1px solid var(--rule); }
hr { border: none; border-top: 1px solid var(--rule); margin: 2em 0; }
main { padding: 4rem 1rem 6rem; }
section { margin: 0 auto; max-width: var(--col); padding: 1rem 0; }
section.wide { max-width: var(--col-wide); }
section.bleed { max-width: var(--col-bleed); }
section[data-anchor] { scroll-margin-top: 80px; }
.sidenote { font-family: var(--sans); font-size: 0.86rem; color: var(--fg-dim); background: var(--panel-2); border-left: 3px solid var(--accent); padding: 0.6em 0.9em; margin: 1em 0; border-radius: 6px; }
.sidenote strong { color: var(--accent); }
.topbar { position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: color-mix(in srgb, var(--bg) 80%, transparent); border-bottom: 1px solid var(--rule); display: flex; align-items: center; justify-content: space-between; padding: 0.6rem 1.2rem; font-family: var(--sans); }
.topbar .brand { display: flex; align-items: baseline; gap: 0.5rem; font-family: var(--serif); font-weight: 700; font-size: 1.05rem; }
.topbar .brand .tag { font-family: var(--sans); color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 400; }
.topbar nav { display: flex; gap: 0.4rem; align-items: center; }
.topbar nav .dot { width: 0.55rem; height: 0.55rem; border-radius: 50%; background: color-mix(in srgb, var(--muted) 60%, transparent); transition: background 200ms, transform 200ms; cursor: pointer; display: inline-block; }
.topbar nav .dot.active { background: var(--accent); transform: scale(1.3); }
.topbar nav .dot:hover { background: var(--accent-2); }
.topbar .controls { display: flex; align-items: center; gap: 0.6rem; }
.topbar button.theme { font-size: 1rem; background: transparent; border: 1px solid var(--rule); border-radius: 999px; width: 2rem; height: 2rem; display: inline-flex; align-items: center; justify-content: center; cursor: pointer; color: var(--fg); }
.topbar button.theme:hover { background: var(--panel-2); }
.hero { max-width: var(--col-wide); margin: 0 auto; padding: 3rem 1rem 1rem; }
.hero .eyebrow { font-family: var(--sans); font-size: 0.78rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--accent); margin-bottom: 1.2rem; }
.hero h1 { font-size: clamp(2.2rem, 5.5vw, 3.5rem); margin-bottom: 0.5rem; }
.hero .lead { font-size: 1.18rem; color: var(--fg-dim); font-family: var(--serif); max-width: 760px; margin-bottom: 1.5rem; }
.hero .meta { font-family: var(--sans); font-size: 0.92rem; color: var(--fg-dim); display: flex; flex-wrap: wrap; gap: 0.4rem 0.9rem; padding-top: 0.4rem; border-top: 1px solid var(--rule); }
.hero .meta b { color: var(--fg); font-weight: 600; }
.hero .meta .pill { background: var(--panel-2); padding: 0.15em 0.55em; border-radius: 999px; font-size: 0.78rem; }
.counters { display: grid; grid-template-columns: repeat({{n_counters}}, minmax(0,1fr)); gap: 1rem; margin: 2rem auto 0; max-width: var(--col-wide); padding: 0 1rem; }
@media (max-width: 720px) { .counters { grid-template-columns: 1fr 1fr; } }
.counter { background: var(--panel); border: 1px solid var(--rule); padding: 1.3rem 1.1rem; border-radius: 14px; box-shadow: var(--shadow); }
.counter .value { font-family: var(--serif); font-size: clamp(1.8rem, 4.5vw, 2.8rem); font-weight: 700; letter-spacing: -0.02em; color: var(--accent); line-height: 1; }
.counter .unit { font-family: var(--sans); color: var(--fg-dim); font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.4rem; }
.counter .desc { font-family: var(--sans); color: var(--muted); font-size: 0.82rem; margin-top: 0.3rem; }
.counter:nth-child(2) .value { color: var(--accent-3); }
.counter:nth-child(3) .value { color: var(--accent-4); }
.counter:nth-child(4) .value { color: var(--accent-2); }
.subcounters { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.5rem; max-width: var(--col-wide); margin: 0.8rem auto 0; padding: 0 1rem; font-family: var(--sans); font-size: 0.85rem; }
.subcounters .sub { background: var(--panel-2); padding: 0.4rem 0.7rem; border-radius: 8px; color: var(--fg-dim); text-align: center; }
.subcounters .sub b { color: var(--fg); font-weight: 600; }
.card { background: var(--panel); border: 1px solid var(--rule); border-radius: 12px; padding: 1.4rem 1.5rem; margin: 1.2rem 0; box-shadow: var(--shadow); }
.tag { display: inline-block; padding: 0.1em 0.55em; border-radius: 999px; font-family: var(--sans); font-size: 0.75rem; font-weight: 600; background: color-mix(in srgb, var(--accent) 18%, transparent); color: var(--accent); margin-right: 0.4em; }
.tag.green { background: color-mix(in srgb, var(--accent-3) 18%, transparent); color: var(--accent-3); }
.tag.orange { background: color-mix(in srgb, var(--accent-4) 22%, transparent); color: var(--accent-4); }
.tag.pink { background: color-mix(in srgb, var(--accent-2) 22%, transparent); color: var(--accent-2); }
.tag.purple { background: color-mix(in srgb, var(--accent-5) 22%, transparent); color: var(--accent-5); }
.table-wrap { overflow-x: auto; }
table.data { width: 100%; border-collapse: collapse; font-family: var(--sans); font-size: 0.92rem; margin: 1rem 0; }
table.data th, table.data td { border-bottom: 1px solid var(--rule); padding: 0.55rem 0.7rem; text-align: left; vertical-align: top; }
table.data th { background: var(--panel-2); font-weight: 600; color: var(--fg); cursor: pointer; user-select: none; white-space: nowrap; }
table.data th[data-sort]:after { content: " ⇅"; color: var(--muted); font-size: 0.8em; }
table.data th.sort-asc:after { content: " ↑"; color: var(--accent); }
table.data th.sort-desc:after { content: " ↓"; color: var(--accent); }
table.data tr:hover td { background: var(--panel-2); }
#flow-section { max-width: var(--col-bleed); }
.flow-wrap { margin: 1.5rem 0 1rem; background: var(--panel); border: 1px solid var(--rule); border-radius: 14px; box-shadow: var(--shadow); overflow: hidden; }
.flow-toolbar { display: flex; flex-wrap: wrap; align-items: center; gap: 0.6rem; padding: 0.7rem 1rem; border-bottom: 1px solid var(--rule); background: var(--panel-2); font-family: var(--sans); }
.flow-toolbar button { font-family: var(--sans); font-size: 0.9rem; padding: 0.4rem 0.9rem; background: var(--panel); border: 1px solid var(--rule); border-radius: 999px; cursor: pointer; color: var(--fg); }
.flow-toolbar button:hover { background: var(--accent); color: #fff; border-color: var(--accent); }
.flow-toolbar .status { margin-left: auto; font-size: 0.8rem; color: var(--muted); }
#flow-svg-host { padding: 1rem 0.5rem; min-height: 400px; }
#flow-svg-host svg { width: 100%; height: auto; display: block; }
.flow-node-rect { fill: var(--panel); stroke: var(--rule); stroke-width: 1.5; cursor: pointer; transition: stroke 200ms, fill 200ms; }
.flow-node-rect:hover { stroke: var(--accent); }
.flow-node-rect.active { stroke: var(--accent); stroke-width: 2.5; fill: color-mix(in srgb, var(--accent) 12%, var(--panel)); }
.flow-node-rect.winner { fill: color-mix(in srgb, var(--accent-3) 18%, var(--panel)); stroke: var(--accent-3); stroke-width: 2.5; }
.flow-node-text { font-family: var(--sans); font-size: 13px; font-weight: 600; fill: var(--fg); pointer-events: none; }
.flow-node-sub { font-family: var(--sans); font-size: 10.5px; fill: var(--fg-dim); pointer-events: none; }
.flow-edge { fill: none; stroke: var(--rule); stroke-width: 1.8; }
.legend { display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; font-family: var(--sans); font-size: 0.82rem; color: var(--fg-dim); padding: 0.5rem 1rem; border-top: 1px solid var(--rule); background: var(--bg-soft); }
.legend .sw { display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin-right: 0.35em; vertical-align: middle; }
.panel-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 200; opacity: 0; pointer-events: none; transition: opacity 200ms ease; }
.panel-overlay.open { opacity: 1; pointer-events: auto; }
.method-panel { position: fixed; top: 0; right: 0; width: min(600px, 92vw); height: 100vh; background: var(--bg); border-left: 1px solid var(--rule); z-index: 201; transform: translateX(102%); transition: transform 280ms cubic-bezier(.2,.8,.2,1); overflow-y: auto; padding: 1.5rem 1.6rem 4rem; box-shadow: -8px 0 32px rgba(0,0,0,0.18); }
.method-panel.open { transform: translateX(0); }
.method-panel .close { position: sticky; top: 0; display: flex; justify-content: flex-end; margin: -1.5rem -1.6rem 0; padding: 0.6rem 1rem; background: color-mix(in srgb, var(--bg) 85%, transparent); backdrop-filter: blur(8px); border-bottom: 1px solid var(--rule); z-index: 5; }
.method-panel .close button { border: 1px solid var(--rule); background: var(--panel); border-radius: 999px; width: 2rem; height: 2rem; cursor: pointer; color: var(--fg); font-size: 1.1rem; }
.method-panel h2 { font-size: 1.6rem; margin-top: 1rem; border: none; padding: 0; }
.method-panel .citation { font-family: var(--sans); font-size: 0.9rem; color: var(--fg-dim); margin: 0.4rem 0 1rem; padding: 0.6rem 0.8rem; background: var(--panel-2); border-left: 3px solid var(--accent); border-radius: 6px; }
.method-panel .why { background: color-mix(in srgb, var(--accent-3) 14%, transparent); border-left: 3px solid var(--accent-3); padding: 0.7rem 1rem; border-radius: 6px; font-family: var(--sans); font-size: 0.95rem; color: var(--fg); margin: 1.2rem 0; }
.method-panel .schematic { background: var(--bg-soft); border-radius: 8px; padding: 0.8rem; margin: 1rem 0; text-align: center; }
.method-panel .schematic svg { max-width: 100%; height: auto; }
.findings { display: grid; grid-template-columns: 1fr; gap: 1rem; }
@media (min-width: 720px) { .findings { grid-template-columns: 1fr 1fr; } }
.finding { background: var(--panel); border: 1px solid var(--rule); border-radius: 12px; padding: 1.2rem 1.3rem; box-shadow: var(--shadow); }
.finding h3 { margin-top: 0; font-size: 1.15rem; }
.finding .lbl { font-family: var(--sans); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.14em; color: var(--accent); font-weight: 600; }
.glossary { column-count: 1; column-gap: 1.5rem; font-family: var(--sans); font-size: 0.94rem; }
@media (min-width: 720px) { .glossary { column-count: 2; } }
.glossary dt { font-weight: 700; color: var(--fg); margin-top: 0.6rem; font-family: var(--serif); break-inside: avoid; }
.glossary dd { margin: 0.1rem 0 0.7rem; color: var(--fg-dim); break-inside: avoid; }
.quiz .q { background: var(--panel); border: 1px solid var(--rule); border-radius: 10px; padding: 1rem 1.3rem; margin: 1rem 0; box-shadow: var(--shadow); font-family: var(--sans); }
.quiz .q .question { font-weight: 600; color: var(--fg); margin-bottom: 0.6rem; }
.quiz .q label { display: block; padding: 0.4rem 0.7rem; border-radius: 6px; cursor: pointer; margin: 0.2rem 0; transition: background 120ms; }
.quiz .q label:hover { background: var(--panel-2); }
.quiz .q label.correct { background: color-mix(in srgb, var(--accent-3) 18%, transparent); }
.quiz .q label.wrong { background: color-mix(in srgb, var(--accent-2) 18%, transparent); text-decoration: line-through; opacity: 0.7; }
.quiz .q input[type=radio] { accent-color: var(--accent); margin-right: 0.5em; }
.quiz .q .explain { display: none; margin-top: 0.7rem; padding: 0.6rem 0.8rem; font-size: 0.88rem; color: var(--fg-dim); background: var(--panel-2); border-left: 3px solid var(--accent); border-radius: 6px; }
.quiz .q.answered .explain { display: block; }
.quiz .score { font-family: var(--serif); font-size: 1.4rem; font-weight: 700; text-align: center; margin: 1.5rem 0; color: var(--accent); }
.figure { background: var(--bg-soft); border: 1px dashed var(--rule); border-radius: 10px; padding: 1rem 1.2rem; margin: 1.2rem 0; font-family: var(--sans); font-size: 0.9rem; color: var(--fg-dim); }
.figure .figtitle { font-family: var(--serif); font-weight: 700; color: var(--fg); font-size: 1rem; margin-bottom: 0.3rem; }
.figure .panel { font-family: var(--serif); font-weight: 700; color: var(--accent); }
.figure a { font-weight: 600; }
#fallback-banner { display: none; position: fixed; bottom: 1rem; left: 50%; transform: translateX(-50%); background: var(--panel); border: 1px solid var(--accent-4); color: var(--fg); padding: 0.4rem 0.9rem; border-radius: 999px; font-family: var(--sans); font-size: 0.82rem; box-shadow: var(--shadow); z-index: 150; }
#fallback-banner.on { display: block; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
@media print { .topbar, .method-panel, .panel-overlay, .flow-toolbar { display: none !important; } body { background: white; color: black; } }
.tt-trigger { border-bottom: 1px dotted var(--accent); cursor: help; }
.muted { color: var(--muted); }
.small { font-size: 0.85rem; font-family: var(--sans); }
.center { text-align: center; }
hr.fancy { background: linear-gradient(90deg, transparent, var(--rule), transparent); height: 1px; border: none; }
{{extra_css}}
</style>
</head>
<body>

<div class="topbar" role="banner">
  <div class="brand">{{page_title_short}} <span class="tag">Learning guide</span></div>
  <nav id="progress-dots" aria-label="Section progress"></nav>
  <div class="controls">
    <button class="theme" id="theme-toggle" aria-label="Toggle dark/light theme">☾</button>
  </div>
</div>

<div id="fallback-banner">Running in static fallback mode (some CDN libraries didn't load)</div>

<main>

<section class="hero">
  <div class="eyebrow">{{eyebrow}}</div>
  <h1>{{title}}</h1>
  <p class="lead">{{lead_paragraph}}</p>
  <div class="meta">
    <span><b>Authors</b> {{authors_short}}</span>
    <span><b>DOI</b> <a href="{{paper_url}}" target="_blank" rel="noopener">{{doi}}</a></span>
    {{HERO_META_PILLS_HTML}}
  </div>
</section>

<div class="counters" id="counters">
{{HERO_COUNTERS_HTML}}
</div>
<div class="subcounters">
{{SUB_COUNTERS_HTML}}
</div>

{{SECTIONS_HTML}}

<section data-anchor="flow" id="flow-section" class="bleed">
  <div style="max-width: var(--col); margin: 0 auto;">
    <h2>The analysis pipeline</h2>
    <p>{{flow_section_intro}}</p>
  </div>
  <div class="flow-wrap">
    <div class="flow-toolbar">
      <button id="flow-play" type="button">▶ Play</button>
      <button id="flow-step" type="button">⏭ Step</button>
      <button id="flow-reset" type="button">⟲ Reset</button>
      <span class="status" id="flow-status">Click any node, or press Play.</span>
    </div>
    <div id="flow-svg-host">
      <svg id="flow-svg" viewBox="0 0 {{flow_width}} {{flow_height}}" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M0,0 L9,5 L0,10 Z" fill="#888"/>
          </marker>
        </defs>
      </svg>
    </div>
    <div class="legend">
      <div><span class="sw" style="background:var(--accent)"></span> Active step</div>
      <div><span class="sw" style="background:var(--accent-3)"></span> Selected method</div>
      <div><span class="sw" style="background:var(--rule)"></span> Pending step</div>
    </div>
  </div>
</section>

<div class="panel-overlay" id="panel-overlay"></div>
<aside class="method-panel" id="method-panel" role="dialog" aria-modal="true" aria-hidden="true">
  <div class="close"><button id="panel-close" aria-label="Close method panel">×</button></div>
  <div id="panel-content"></div>
</aside>

<section data-anchor="findings">
  <h2>Key findings &amp; discoveries</h2>
  <div class="findings">
{{FINDINGS_HTML}}
  </div>
</section>

<section data-anchor="figures">
  <h2>Paper figures</h2>
  <p class="small muted">Publisher figure URLs are often blocked from programmatic fetch. Use the link in each card to open the figure on the source site.</p>
{{FIGURES_HTML}}
</section>

<section data-anchor="compare" class="wide">
  <h2>Comparison vs prior work</h2>
{{COMPARISON_TABLE_HTML}}
</section>

<section data-anchor="glossary">
  <h2>Glossary</h2>
  <p class="small muted">Underlined terms in the body show a definition popover on hover.</p>
  <dl class="glossary" id="glossary-list">
{{GLOSSARY_HTML}}
  </dl>
</section>

<section data-anchor="quiz">
  <h2>Self-test</h2>
  <p class="small muted">Pick one answer per question; correct answers reveal with an explanation on click.</p>
  <div class="quiz" id="quiz">
{{QUIZ_HTML}}
  </div>
  <div class="score" id="score">Score: — / {{n_quiz}}</div>
</section>

<section data-anchor="related">
  <h2>Related papers &amp; methods</h2>
  <ul class="small">
{{RELATED_PAPERS_HTML}}
  </ul>
</section>

<section>
  <hr class="fancy">
  <p class="small muted center">{{footer_note}}</p>
</section>

</main>

<script src="https://cdn.jsdelivr.net/npm/d3@7" defer></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js" defer></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js" defer></script>

<script>
window.METHODS = {{METHODS_JSON}};
window.FLOW = {nodes: {{FLOW_NODES_JSON}}, edges: {{FLOW_EDGES_JSON}}};
window.FLOW_ORDER = {{FLOW_ORDER_JSON}};
window.GLOSSARY_TERMS = {{GLOSSARY_TERMS_JSON}};
window.THEME_KEY = "{{theme_storage_key}}";
</script>

<script>
(function(){
  "use strict";

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    const btn = document.getElementById("theme-toggle");
    if (btn) btn.textContent = theme === "dark" ? "☀" : "☾";
    try { localStorage.setItem(window.THEME_KEY, theme); } catch(e){}
  }
  function initTheme() {
    let pref = null;
    try { pref = localStorage.getItem(window.THEME_KEY); } catch(e){}
    if (!pref) pref = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    applyTheme(pref);
  }
  initTheme();
  document.getElementById("theme-toggle").addEventListener("click", () => {
    const cur = document.documentElement.getAttribute("data-theme") || "light";
    applyTheme(cur === "light" ? "dark" : "light");
  });

  // progress dots
  const sections = Array.from(document.querySelectorAll("section[data-anchor]"));
  const dotNav = document.getElementById("progress-dots");
  const dotById = new Map();
  sections.forEach((sec) => {
    const id = sec.dataset.anchor;
    const dot = document.createElement("span");
    dot.className = "dot"; dot.title = id;
    dot.addEventListener("click", () => sec.scrollIntoView({behavior: "smooth"}));
    dotNav.appendChild(dot);
    dotById.set(id, dot);
  });
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          dotById.forEach((d) => d.classList.remove("active"));
          const d = dotById.get(e.target.dataset.anchor);
          if (d) d.classList.add("active");
        }
      });
    }, {threshold: 0.3});
    sections.forEach(s => io.observe(s));
  }

  // counters
  function animateCounter(el) {
    const target = parseFloat(el.dataset.count);
    const decimals = parseInt(el.dataset.decimals || "0", 10);
    const suffix = el.dataset.suffix || "";
    const dur = 1200; const start = performance.now();
    const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) { el.textContent = target.toFixed(decimals) + suffix; return; }
    function tick(now) {
      const t = Math.min(1, (now - start) / dur);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = (target * eased).toFixed(decimals) + suffix;
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  const counterEls = Array.from(document.querySelectorAll(".counter .value"));
  if ("IntersectionObserver" in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { animateCounter(e.target); cio.unobserve(e.target); } });
    }, {threshold: 0.4});
    counterEls.forEach(el => cio.observe(el));
  } else counterEls.forEach(animateCounter);

  // table sort
  document.querySelectorAll("table.data").forEach((tbl) => {
    const tbody = tbl.querySelector("tbody"); if (!tbody) return;
    const ths = Array.from(tbl.querySelectorAll("th[data-sort]"));
    ths.forEach((th, idx) => {
      th.addEventListener("click", () => {
        const type = th.dataset.sort;
        const dir = th.classList.contains("sort-asc") ? "desc" : "asc";
        ths.forEach(t => t.classList.remove("sort-asc", "sort-desc"));
        th.classList.add(dir === "asc" ? "sort-asc" : "sort-desc");
        const rows = Array.from(tbody.querySelectorAll("tr"));
        const totalRows = rows.filter(r => /total|headline/i.test(r.cells[0].textContent));
        const dataRows = rows.filter(r => !totalRows.includes(r));
        dataRows.sort((a, b) => {
          let av = a.cells[idx].textContent.trim();
          let bv = b.cells[idx].textContent.trim();
          if (type === "num") { av = parseFloat(av.replace(/[^\d.\-]/g, "")) || 0; bv = parseFloat(bv.replace(/[^\d.\-]/g, "")) || 0; }
          if (av < bv) return dir === "asc" ? -1 : 1;
          if (av > bv) return dir === "asc" ? 1 : -1;
          return 0;
        });
        dataRows.forEach(r => tbody.appendChild(r));
        totalRows.forEach(r => tbody.appendChild(r));
      });
    });
  });

  // FLOW
  const SVG_NS = "http://www.w3.org/2000/svg";
  function el(tag, attrs, text) {
    const e = document.createElementNS(SVG_NS, tag);
    if (attrs) for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (text != null) e.textContent = text;
    return e;
  }
  function buildFlow() {
    const svg = document.getElementById("flow-svg");
    if (!svg) return;
    while (svg.firstChild && svg.firstChild.tagName !== "defs") svg.removeChild(svg.firstChild);
    window.FLOW.edges.forEach((edge) => {
      const a = window.FLOW.nodes.find(n => n.id === edge.from);
      const b = window.FLOW.nodes.find(n => n.id === edge.to);
      if (!a || !b) return;
      const x1 = a.x + a.w, y1 = a.y + a.h / 2;
      const x2 = b.x,       y2 = b.y + b.h / 2;
      const dx = (x2 - x1) * 0.5;
      const d = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;
      const path = el("path", {d: d, class: "flow-edge", "marker-end": "url(#arrow)"});
      if (edge.dashed) path.setAttribute("stroke-dasharray", "5 4");
      svg.appendChild(path);
    });
    window.FLOW.nodes.forEach((n) => {
      const g = el("g", {transform: `translate(${n.x},${n.y})`, class: "flow-node"});
      g.dataset.id = n.id;
      const winnerClass = (n.kind === "winner") ? " winner" : "";
      const rect = el("rect", {class: "flow-node-rect" + winnerClass, width: n.w, height: n.h, rx: 10, ry: 10});
      g.appendChild(rect);
      g.appendChild(Object.assign(el("text", {class: "flow-node-text", x: n.w / 2, y: n.h / 2 - 2, "text-anchor": "middle"}), {textContent: n.label}));
      g.appendChild(Object.assign(el("text", {class: "flow-node-sub", x: n.w / 2, y: n.h / 2 + 14, "text-anchor": "middle"}), {textContent: n.sub}));
      g.addEventListener("click", () => onNodeClick(n));
      g.style.cursor = "pointer";
      svg.appendChild(g);
    });
  }
  buildFlow();

  function onNodeClick(n) {
    document.querySelectorAll(".flow-node-rect").forEach(r => r.classList.remove("active"));
    const g = document.querySelector(`.flow-node[data-id="${n.id}"] .flow-node-rect`);
    if (g) g.classList.add("active");
    if (n.method) openMethodPanel(n.method);
    setStatus(`Selected: ${n.label}`);
  }
  function setStatus(s) { const e = document.getElementById("flow-status"); if (e) e.textContent = s; }

  // panel
  const overlay = document.getElementById("panel-overlay");
  const panel = document.getElementById("method-panel");
  const panelContent = document.getElementById("panel-content");
  document.getElementById("panel-close").addEventListener("click", closePanel);
  overlay.addEventListener("click", closePanel);
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") closePanel(); });

  function openMethodPanel(key) {
    const m = window.METHODS[key]; if (!m) return;
    let eqsHtml = "";
    (m.equations || []).forEach((eq) => { eqsHtml += `<div class="math-block">$$${eq}$$</div>`; });
    panelContent.innerHTML = `
      <h2>${m.name}</h2>
      <div class="muted small">${m.subtitle || ""}</div>
      <div class="citation">${m.citation || ""}<br><a href="${m.doi || "#"}" target="_blank" rel="noopener">Open reference ↗</a></div>
      <h4>Intuition</h4>
      <div>${m.intuition || ""}</div>
      ${eqsHtml ? `<h4>Equations</h4>${eqsHtml}` : ''}
      ${m.schematic_svg ? `<h4>Schematic</h4><div class="schematic">${m.schematic_svg}</div>` : ''}
      <h4>Why this method was used</h4>
      <div class="why">${m.why || ""}</div>
    `;
    panel.classList.add("open"); overlay.classList.add("open"); panel.setAttribute("aria-hidden", "false");
    if (window.renderMathInElement) {
      try {
        window.renderMathInElement(panelContent, {
          delimiters: [{left: "$$", right: "$$", display: true}, {left: "$", right: "$", display: false}],
          throwOnError: false, strict: "ignore"
        });
      } catch(e) {}
    }
  }
  function closePanel() { panel.classList.remove("open"); overlay.classList.remove("open"); panel.setAttribute("aria-hidden", "true"); }

  // play/step/reset
  const order = window.FLOW_ORDER && window.FLOW_ORDER.length ? window.FLOW_ORDER : window.FLOW.nodes.map(n => n.id);
  let cursor = -1, playTimer = null;
  function step() {
    cursor = (cursor + 1) % order.length;
    const id = order[cursor];
    const n = window.FLOW.nodes.find(x => x.id === id);
    if (n) onNodeClick(n);
  }
  document.getElementById("flow-step").addEventListener("click", () => {
    if (playTimer) { clearInterval(playTimer); playTimer = null; document.getElementById("flow-play").textContent = "▶ Play"; }
    step();
  });
  document.getElementById("flow-play").addEventListener("click", () => {
    const btn = document.getElementById("flow-play");
    if (playTimer) { clearInterval(playTimer); playTimer = null; btn.textContent = "▶ Play"; }
    else { btn.textContent = "⏸ Pause"; playTimer = setInterval(step, 1400); }
  });
  document.getElementById("flow-reset").addEventListener("click", () => {
    cursor = -1;
    document.querySelectorAll(".flow-node-rect").forEach(r => r.classList.remove("active"));
    setStatus("Reset — click any node, or press Play.");
    if (playTimer) { clearInterval(playTimer); playTimer = null; document.getElementById("flow-play").textContent = "▶ Play"; }
  });

  // KaTeX
  function renderAllMath() {
    if (!window.renderMathInElement) return;
    try {
      window.renderMathInElement(document.body, {
        delimiters: [{left: "$$", right: "$$", display: true}, {left: "$", right: "$", display: false}],
        throwOnError: false, strict: "ignore",
        ignoredTags: ["script","noscript","style","textarea","pre","code"]
      });
    } catch(e) {}
  }
  let tries = 0;
  const mathTry = setInterval(() => {
    tries++;
    if (window.renderMathInElement) { renderAllMath(); clearInterval(mathTry); }
    else if (tries > 30) { clearInterval(mathTry); document.getElementById("fallback-banner").classList.add("on"); }
  }, 200);

  // quiz
  function initQuiz() {
    const qs = Array.from(document.querySelectorAll("#quiz .q"));
    const scoreEl = document.getElementById("score");
    const state = new Map();
    qs.forEach((q) => {
      const correct = q.dataset.correct;
      q.querySelectorAll("label").forEach((lbl) => {
        lbl.addEventListener("click", () => {
          if (state.has(q)) return;
          const radio = lbl.querySelector("input"); radio.checked = true;
          const picked = radio.value;
          state.set(q, picked === correct);
          q.classList.add("answered");
          q.querySelectorAll("label").forEach((l2) => {
            const v = l2.querySelector("input").value;
            if (v === correct) l2.classList.add("correct");
            else if (v === picked) l2.classList.add("wrong");
          });
          let s = 0; state.forEach(v => { if (v) s++; });
          scoreEl.textContent = `Score: ${s} / ${qs.length}`;
        });
      });
    });
  }
  initQuiz();

  // glossary popovers
  const glossaryMap = {};
  document.querySelectorAll("#glossary-list dt").forEach((dt) => {
    const term = dt.textContent.trim();
    const dd = dt.nextElementSibling;
    glossaryMap[term.toLowerCase()] = {term: term, def: dd ? dd.textContent.trim() : ""};
  });
  const tt = document.createElement("div");
  tt.style.cssText = "position:fixed;max-width:300px;padding:0.5rem 0.7rem;background:var(--panel);border:1px solid var(--rule);border-radius:8px;font-family:var(--sans);font-size:0.82rem;color:var(--fg);box-shadow:var(--shadow);z-index:300;pointer-events:none;display:none;line-height:1.45;";
  document.body.appendChild(tt);
  document.body.addEventListener("mouseover", (e) => {
    const t = e.target.closest(".tt-trigger"); if (!t) return;
    const k = t.dataset.glossary; const g = glossaryMap[k]; if (!g) return;
    tt.innerHTML = `<b>${g.term}</b> — ${g.def}`; tt.style.display = "block";
  });
  document.body.addEventListener("mousemove", (e) => {
    if (tt.style.display !== "block") return;
    let x = e.clientX + 14, y = e.clientY + 14;
    if (x + 300 > window.innerWidth) x = window.innerWidth - 310;
    tt.style.left = x + "px"; tt.style.top = y + "px";
  });
  document.body.addEventListener("mouseout", (e) => { if (e.target.closest(".tt-trigger")) tt.style.display = "none"; });

  // auto-decorate first mentions
  const terms = window.GLOSSARY_TERMS || {};
  const used = new Set();
  function walk(node) {
    if (node.nodeType === 3) {
      const txt = node.nodeValue;
      for (const [k, v] of Object.entries(terms)) {
        if (used.has(k)) continue;
        const idx = txt.toLowerCase().indexOf(k);
        if (idx < 0) continue;
        const before = txt.slice(0, idx);
        const match  = txt.slice(idx, idx + k.length);
        const after  = txt.slice(idx + k.length);
        const span = document.createElement("span");
        span.className = "tt-trigger"; span.dataset.glossary = v;
        span.textContent = match;
        const frag = document.createDocumentFragment();
        frag.appendChild(document.createTextNode(before));
        frag.appendChild(span);
        frag.appendChild(document.createTextNode(after));
        node.parentNode.replaceChild(frag, node);
        used.add(k); return;
      }
    } else if (node.nodeType === 1) {
      const tag = node.tagName.toLowerCase();
      if (["script","style","code","pre","kbd"].includes(tag)) return;
      if (node.id === "glossary-list" || (node.closest && node.closest("#glossary-list"))) return;
      if (node.closest && node.closest(".topbar")) return;
      Array.from(node.childNodes).forEach(walk);
    }
  }
  setTimeout(() => walk(document.querySelector("main")), 250);

  // extra paper-specific JS
{{extra_js}}
})();
</script>

</body>
</html>

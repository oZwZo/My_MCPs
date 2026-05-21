#!/usr/bin/env python3
"""paperlink_to_html — pure HTML renderer.

Loads templates/learning_guide.html.tpl and substitutes a paper_info dict
into the placeholders. No network, no API key, no third-party deps.
Python stdlib only.

USE — programmatic
------------------
    from scripts.render_html import render_html
    render_html(paper_info, output_path="~/Downloads/guide.html")

USE — CLI
---------
    python3 scripts/render_html.py --json paper_info.json --out guide.html
    cat paper_info.json | python3 scripts/render_html.py --out guide.html
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------

THIS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = THIS_DIR.parent
TEMPLATE_PATH = SKILL_ROOT / "templates" / "learning_guide.html.tpl"


# ----------------------------------------------------------------------
# Defaults
# ----------------------------------------------------------------------

DEFAULTS: dict[str, Any] = {
    "page_title_short": "Paper",
    "title": "Untitled paper",
    "meta_description": "An interactive Distill-inspired learning guide.",
    "primary_accent": "#5b6cff",
    "primary_accent_dark": "#7c8cff",
    "eyebrow": "",
    "lead_paragraph": "",
    "authors_short": "",
    "doi": "",
    "paper_url": "#",
    "journal": "",
    "year": "",
    "theme_storage_key": "paperlink-theme",
    "flow_section_intro": "Click any node to see what it does. The pipeline reflects the analysis described in the paper.",
    "flow_width": 1200,
    "flow_height": 460,
    "footer_note": "",
    "hero_counters": [],
    "sub_counters": [],
    "meta_extras": [],
    "sections": [],
    "flow_nodes": [],
    "flow_edges": [],
    "flow_order": [],
    "methods": {},
    "findings": [],
    "figures": [],
    "comparison_headers": [],
    "comparison_rows": [],
    "glossary": [],
    "quiz": [],
    "related_papers": [],
    "extra_css": "",
    "extra_js": "",
}


# ----------------------------------------------------------------------
# Pre-renderers — turn paper_info chunks into HTML fragments / JSON
# ----------------------------------------------------------------------


def _esc(s: Any) -> str:
    """HTML-escape, then return a string. Safe on None and non-strings."""
    if s is None:
        return ""
    text = str(s)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _render_hero_counters(counters: list[dict]) -> str:
    out = []
    for c in counters:
        value = c.get("value", 0)
        decimals = int(c.get("decimals", 0))
        suffix = c.get("suffix", "")
        unit = _esc(c.get("unit", ""))
        desc = _esc(c.get("desc", ""))
        out.append(
            f'  <div class="counter">'
            f'<div class="value" data-count="{value}" data-decimals="{decimals}" data-suffix="{_esc(suffix)}">0</div>'
            f'<div class="unit">{unit}</div>'
            f'<div class="desc">{desc}</div>'
            f"</div>"
        )
    return "\n".join(out)


def _render_sub_counters(subs: list[dict]) -> str:
    out = []
    for s in subs:
        out.append(
            f'  <div class="sub"><b>{_esc(s.get("value",""))}</b> {_esc(s.get("label",""))}</div>'
        )
    return "\n".join(out)


def _render_meta_pills(meta_extras: list[dict]) -> str:
    """Render the 'extra' pills in the hero metadata row."""
    out = []
    for p in meta_extras:
        label = p.get("label", "")
        value = p.get("value", "")
        url = p.get("url")
        if url:
            val_html = f'<a href="{_esc(url)}" target="_blank" rel="noopener">{_esc(value)}</a>'
        else:
            val_html = _esc(value)
        if label:
            out.append(f"    <span><b>{_esc(label)}</b> {val_html}</span>")
        else:
            out.append(f'    <span class="pill">{val_html}</span>')
    return "\n".join(out)


def _render_sections(sections: list[dict]) -> str:
    """A section is {anchor, title, body_html, wide?}.

    body_html is inserted RAW (it can contain arbitrary HTML, including
    paper-specific interactive widgets, SVGs, scripts).
    """
    out = []
    for s in sections:
        anchor = _esc(s.get("anchor", ""))
        title = _esc(s.get("title", ""))
        body = s.get("body_html", "")
        klass = "wide" if s.get("wide") else ""
        klass = (' class="' + klass + '"') if klass else ""
        out.append(
            f'<section data-anchor="{anchor}"{klass}>\n'
            f"  <h2>{title}</h2>\n"
            f"  {body}\n"
            f"</section>"
        )
    return "\n\n".join(out)


def _render_findings(findings: list[dict]) -> str:
    out = []
    for f in findings:
        out.append(
            f'    <div class="finding">\n'
            f'      <div class="lbl">{_esc(f.get("label",""))}</div>\n'
            f'      <h3>{_esc(f.get("title",""))}</h3>\n'
            f'      <div class="small">{f.get("body_html","")}</div>\n'
            f"    </div>"
        )
    return "\n".join(out)


def _render_figures(figures: list[dict]) -> str:
    out = []
    for fig in figures:
        fig_no = _esc(fig.get("fig_no", ""))
        title = _esc(fig.get("title", ""))
        panels = fig.get("panels_html", "")  # raw HTML
        link = _esc(fig.get("link", "#"))
        out.append(
            f'  <div class="figure">\n'
            f'    <div class="figtitle">Fig. {fig_no} &middot; {title}</div>\n'
            f"    <p>{panels}</p>\n"
            f'    <a href="{link}" target="_blank" rel="noopener">Open Fig {fig_no} on source ↗</a>\n'
            f"  </div>"
        )
    return "\n".join(out)


def _render_comparison(headers: list[str], rows: list[list[str]]) -> str:
    if not headers and not rows:
        return '<p class="muted small">No comparison table provided.</p>'
    head = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    body = ""
    for r in rows:
        cells = "".join(f"<td>{c}</td>" for c in r)  # cells are raw HTML
        body += f"<tr>{cells}</tr>\n"
    return (
        '<div class="table-wrap">\n'
        '  <table class="data">\n'
        f"    <thead><tr>{head}</tr></thead>\n"
        f"    <tbody>\n{body}    </tbody>\n"
        "  </table>\n"
        "</div>"
    )


def _render_glossary(glossary: list[dict]) -> str:
    out = []
    for g in glossary:
        gid = _esc(g.get("id", ""))
        term = _esc(g.get("term", ""))
        defn = _esc(g.get("def", ""))
        out.append(f'    <dt id="{gid}">{term}</dt>\n    <dd>{defn}</dd>')
    return "\n".join(out)


def _render_quiz(quiz: list[dict]) -> str:
    out = []
    for i, q in enumerate(quiz, start=1):
        correct = _esc(q.get("correct", ""))
        question = _esc(q.get("question", ""))
        explain = _esc(q.get("explain", ""))
        options = q.get("options", {})
        labels = []
        for opt_key in ("a", "b", "c", "d"):
            if opt_key in options:
                labels.append(
                    f'      <label><input type="radio" name="q{i}" value="{opt_key}"> {_esc(options[opt_key])}</label>'
                )
        labels_html = "\n".join(labels)
        out.append(
            f'    <div class="q" data-correct="{correct}">\n'
            f'      <div class="question">{i}. {question}</div>\n'
            f"{labels_html}\n"
            f'      <div class="explain"><b>Correct: {correct}.</b> {explain}</div>\n'
            f"    </div>"
        )
    return "\n".join(out)


def _render_related(related: list[dict]) -> str:
    out = []
    for r in related:
        label = _esc(r.get("label", ""))
        citation = _esc(r.get("citation", ""))
        url = _esc(r.get("url", ""))
        link = (
            f' <a href="{url}" target="_blank" rel="noopener">{url}</a>' if url else ""
        )
        out.append(f"    <li><b>{label}</b> — {citation}{link}</li>")
    return "\n".join(out)


# ----------------------------------------------------------------------
# Main renderer
# ----------------------------------------------------------------------


def _merge_defaults(paper_info: dict) -> dict:
    out = dict(DEFAULTS)
    for k, v in (paper_info or {}).items():
        out[k] = v
    return out


def _default_footer_note(p: dict) -> str:
    date = _dt.date.today().isoformat()
    return (
        f"Generated {date}. Single-file HTML, no build step, dark + light, "
        f"progressive-enhancement: D3 / KaTeX are loaded from jsDelivr CDN; "
        f"the page is still readable with all libraries blocked. "
        f"For canonical text, figures, and supplementary data, follow the source link."
    )


def _glossary_terms_dict(glossary: list[dict]) -> dict[str, str]:
    """Build the auto-decoration dict: lowercase-term → glossary-term-lowercase."""
    out = {}
    for g in glossary:
        term = g.get("term", "")
        if term:
            out[term.lower()] = term.lower()
    return out


def render_html(paper_info: dict, output_path: Optional[str] = None) -> str:
    """Render the learning-guide HTML from a paper_info dict.

    Args:
        paper_info: dict matching schemas/paper_info.schema.json.
        output_path: if given, the HTML is also written to this path.

    Returns:
        The rendered HTML as a string.
    """
    p = _merge_defaults(paper_info)

    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
    tpl = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Pre-render list-driven chunks
    hero_counters_html = _render_hero_counters(p["hero_counters"])
    sub_counters_html = _render_sub_counters(p["sub_counters"])
    meta_pills_html = _render_meta_pills(p["meta_extras"])
    sections_html = _render_sections(p["sections"])
    findings_html = _render_findings(p["findings"])
    figures_html = _render_figures(p["figures"])
    comparison_html = _render_comparison(p["comparison_headers"], p["comparison_rows"])
    glossary_html = _render_glossary(p["glossary"])
    quiz_html = _render_quiz(p["quiz"])
    related_html = _render_related(p["related_papers"])

    # JSON-driven parts (consumed by JS at runtime)
    methods_json = json.dumps(p["methods"], ensure_ascii=False)
    flow_nodes_json = json.dumps(p["flow_nodes"], ensure_ascii=False)
    flow_edges_json = json.dumps(p["flow_edges"], ensure_ascii=False)
    flow_order_json = json.dumps(p["flow_order"], ensure_ascii=False)
    glossary_terms_json = json.dumps(
        _glossary_terms_dict(p["glossary"]), ensure_ascii=False
    )

    n_counters = max(1, min(4, len(p["hero_counters"]) or 3))
    n_quiz = len(p["quiz"])
    footer = p["footer_note"] or _default_footer_note(p)

    # Substitution map (only one pass — placeholders inside substituted text
    # are NOT re-expanded, which is intentional: user content is raw).
    subs: dict[str, str] = {
        "page_title_short": _esc(p["page_title_short"]),
        "title": _esc(p["title"]),
        "meta_description": _esc(p["meta_description"]),
        "primary_accent": p["primary_accent"],
        "primary_accent_dark": p["primary_accent_dark"],
        "eyebrow": _esc(p["eyebrow"]),
        "lead_paragraph": p["lead_paragraph"],  # raw HTML allowed in lead
        "authors_short": p["authors_short"],
        "doi": _esc(p["doi"]),
        "paper_url": _esc(p["paper_url"]),
        "theme_storage_key": _esc(p["theme_storage_key"]),
        "flow_section_intro": p["flow_section_intro"],
        "flow_width": str(p["flow_width"]),
        "flow_height": str(p["flow_height"]),
        "footer_note": footer,
        "n_counters": str(n_counters),
        "n_quiz": str(n_quiz),
        "HERO_META_PILLS_HTML": meta_pills_html,
        "HERO_COUNTERS_HTML": hero_counters_html,
        "SUB_COUNTERS_HTML": sub_counters_html,
        "SECTIONS_HTML": sections_html,
        "FINDINGS_HTML": findings_html,
        "FIGURES_HTML": figures_html,
        "COMPARISON_TABLE_HTML": comparison_html,
        "GLOSSARY_HTML": glossary_html,
        "QUIZ_HTML": quiz_html,
        "RELATED_PAPERS_HTML": related_html,
        "METHODS_JSON": methods_json,
        "FLOW_NODES_JSON": flow_nodes_json,
        "FLOW_EDGES_JSON": flow_edges_json,
        "FLOW_ORDER_JSON": flow_order_json,
        "GLOSSARY_TERMS_JSON": glossary_terms_json,
        "extra_css": p["extra_css"],
        "extra_js": p["extra_js"],
    }

    html = tpl
    for key, val in subs.items():
        html = html.replace("{{" + key + "}}", val)

    if output_path:
        out = Path(os.path.expanduser(output_path))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")

    return html


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------


def _cli() -> int:
    ap = argparse.ArgumentParser(
        description="Render a paper_info JSON into a Distill-inspired HTML learning guide."
    )
    ap.add_argument(
        "--json",
        "-j",
        type=str,
        default=None,
        help="Path to paper_info JSON. If omitted, read JSON from stdin.",
    )
    ap.add_argument(
        "--out",
        "-o",
        type=str,
        required=True,
        help="Output HTML file path. Use '-' to write to stdout.",
    )
    args = ap.parse_args()

    if args.json:
        raw = Path(os.path.expanduser(args.json)).read_text(encoding="utf-8")
    else:
        if sys.stdin.isatty():
            print(
                "error: no --json file given and stdin is a terminal. "
                "Pass --json paper.json or pipe JSON on stdin.",
                file=sys.stderr,
            )
            return 2
        raw = sys.stdin.read()

    paper_info = json.loads(raw)

    if args.out == "-":
        html = render_html(paper_info, output_path=None)
        sys.stdout.write(html)
    else:
        render_html(paper_info, output_path=args.out)
        print(f"✓ Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())

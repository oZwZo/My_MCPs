#!/usr/bin/env python3
"""paperlink_to_html — end-to-end CLI.

Given a paper URL, uses the Anthropic API to extract a structured
paper_info dict, then hands off to render_html() to produce the HTML
learning guide.

REQUIRES:
    - ANTHROPIC_API_KEY exported in the environment
    - `anthropic` Python package installed  (pip install anthropic>=0.34)
    - network access to fetch the paper landing page

For users without an API key, prefer the pure renderer:
    python3 scripts/render_html.py --json paper_info.json --out guide.html
…and assemble the paper_info JSON manually (or via the SKILL.md workflow
inside Claude Code).

USAGE
-----
    python3 scripts/paper_to_guide.py \\
        --url https://www.cell.com/cell/fulltext/S0092-8674\\(25\\)00750-0 \\
        --out ~/Downloads/guide.html

    # Override model:
    python3 scripts/paper_to_guide.py --url <URL> --out <PATH> \\
        --model claude-opus-4-7

    # Save the intermediate paper_info JSON for reuse:
    python3 scripts/paper_to_guide.py --url <URL> --out <PATH> \\
        --save-json /tmp/paper_info.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path

# Support both `python -m scripts.paper_to_guide` and direct invocation as a
# script (`python paper_to_guide.py`).
try:
    from .render_html import render_html  # package import
except ImportError:  # pragma: no cover — running as a top-level script
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from render_html import render_html  # type: ignore


SYSTEM_PROMPT = """\
You are a research-paper structural extractor.

You will be given the URL of a research paper (and any extra notes the user
provides). Produce a SINGLE JSON object that matches the paper_info schema
the user is using for HTML learning guides.

Top-level required keys:

  title, authors_short, doi, journal, year, paper_url, eyebrow,
  lead_paragraph, page_title_short, theme_storage_key,
  primary_accent, primary_accent_dark,
  hero_counters[], sub_counters[],
  sections[], flow_nodes[], flow_edges[], flow_order[],
  methods{}, figures[], findings[],
  comparison_headers[], comparison_rows[],
  glossary[], quiz[], related_papers[],
  footer_note

Rules:

1. Always output valid JSON — no Markdown, no commentary, no prose around
   the JSON.
2. Paraphrase paper content rather than copying verbatim, especially for
   closed-access journals (Cell, Nature, Science).
3. The `hero_counters` list should have 3 or 4 items.
4. `sections` is the main narrative spine of the guide — each item is
   {anchor, title, body_html}. body_html is raw HTML (paragraphs, tables,
   sidenotes, custom widgets). Use 4-6 sections.
5. `methods` is a dict keyed by short method names; each value is
   {name, subtitle, citation, doi, intuition, equations[], schematic_svg,
   why}. Equations are LaTeX strings WITHOUT $$ delimiters (the template
   adds them).
6. `flow_nodes` and `flow_edges` describe the analysis pipeline as a
   directed graph; the renderer draws them as an interactive SVG.
   Nodes need {id, x, y, w, h, label, sub, method (or null), kind}.
7. `quiz` has 5-10 multiple-choice items, each with options {a,b,c,d},
   correct ∈ {a,b,c,d}, and an `explain` string.
8. Pick `primary_accent` and `primary_accent_dark` colors that fit the
   paper's topic (e.g. biology → blue/green/purple, physics → orange).
9. Set `theme_storage_key` to a short, paper-specific slug, e.g. "hdca-theme".

Output ONLY the JSON object.
"""


def _build_user_prompt(url: str, extra_notes: str | None) -> str:
    msg = f"Paper URL: {url}\n"
    if extra_notes:
        msg += f"\nExtra notes from the user:\n{extra_notes}\n"
    msg += (
        "\nFetch the paper (use web_search or web_fetch if the API supports it; "
        "otherwise rely on your training data + the URL alone). "
        "Produce the paper_info JSON now."
    )
    return msg


def _extract_with_anthropic(
    url: str, extra_notes: str | None, model: str
) -> dict:
    try:
        import anthropic  # type: ignore
    except ImportError:
        print(
            "error: `anthropic` package not installed. "
            "Run `pip install 'anthropic>=0.34'` or use the pure renderer "
            "(scripts/render_html.py) with a hand-built paper_info JSON.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print(
            "error: ANTHROPIC_API_KEY is not set.\n"
            "\n"
            "To use this end-to-end CLI:\n"
            "    export ANTHROPIC_API_KEY=sk-ant-...\n"
            "\n"
            "Alternatively, run the pure renderer with a hand-built paper_info JSON:\n"
            "    python3 scripts/render_html.py --json paper_info.json --out guide.html\n"
            "\n"
            "Or follow the SKILL.md workflow inside Claude Code:\n"
            "    /paperlink_to_html <url>\n",
            file=sys.stderr,
        )
        raise SystemExit(1)

    client = anthropic.Anthropic(api_key=api_key)

    msg = client.messages.create(
        model=model,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _build_user_prompt(url, extra_notes)}],
    )

    # Concatenate all text blocks from the response
    chunks: list[str] = []
    for block in msg.content:
        if getattr(block, "type", "") == "text":
            chunks.append(block.text)
    text = "".join(chunks).strip()

    # Strip Markdown fences if the model included them despite instructions
    if text.startswith("```"):
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(
            "error: Anthropic response was not valid JSON.\n"
            f"  reason: {exc}\n"
            f"  first 400 chars of response:\n{textwrap.shorten(text, 400)}",
            file=sys.stderr,
        )
        raise SystemExit(3)


def _cli() -> int:
    ap = argparse.ArgumentParser(
        description="End-to-end: paper URL → HTML learning guide via Anthropic API."
    )
    ap.add_argument("--url", "-u", required=True, help="Paper URL.")
    ap.add_argument(
        "--out", "-o", required=True, help="Output HTML file path."
    )
    ap.add_argument(
        "--model",
        "-m",
        default=os.environ.get("PAPERLINK_HTML_MODEL", "claude-opus-4-5"),
        help="Anthropic model name (default: env PAPERLINK_HTML_MODEL or claude-opus-4-5).",
    )
    ap.add_argument(
        "--notes",
        "-n",
        default=None,
        help="Extra notes to pass to the extractor (e.g. emphasis, focus areas).",
    )
    ap.add_argument(
        "--save-json",
        "-s",
        default=None,
        help="Also save the intermediate paper_info JSON to this path.",
    )
    args = ap.parse_args()

    paper_info = _extract_with_anthropic(args.url, args.notes, args.model)

    if args.save_json:
        Path(os.path.expanduser(args.save_json)).write_text(
            json.dumps(paper_info, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"✓ Wrote intermediate JSON: {args.save_json}")

    render_html(paper_info, output_path=args.out)
    print(f"✓ Wrote HTML: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())

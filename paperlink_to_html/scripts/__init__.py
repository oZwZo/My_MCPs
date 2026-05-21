"""paperlink_to_html — package init.

Exposes the hook function `render_html` so consumers can import it as:

    from paperlink_to_html.scripts import render_html

or, when the parent directory is on PYTHONPATH:

    from scripts.render_html import render_html
"""
from .render_html import render_html  # noqa: F401

__all__ = ["render_html"]

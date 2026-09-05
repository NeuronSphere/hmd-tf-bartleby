"""Extract the document body from Sphinx's singlehtml output, for pandoc.

pandoc converts a whole HTML page. Handing it Sphinx's themed output therefore
puts the sidebar, the navigation, the search box and the theme's own logo
heading into the Word document — and into PowerPoint it puts them on the first
slide, because the sidebar's ``<h1>`` outranks the document's own title.

This writes out the document body alone, with the ``¶`` permalink anchors
Sphinx adds to every heading removed. Doing it here rather than by configuring
the theme away keeps the pandoc input independent of which theme is in use.

    python3 pandoc_body.py build/singlehtml/index.html build/pandoc/body.html
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

# Sphinx wraps the rendered document in this, whatever the theme.
BODY_CLASS = "body"

# Sphinx wraps every section in <section>, which pandoc reads as a Div. A
# heading nested inside a Div is not a top-level block, so pandoc's pptx writer
# will not start a slide at it — the whole document lands on one slide whatever
# --slide-level says. Dropping the wrappers puts the headings back at the top
# level; their only other job is anchor ids, which neither Word nor PowerPoint
# uses.
UNWRAP_ELEMENTS = {"section"}

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class BodyExtractor(HTMLParser):
    """Collect the markup inside the document body div."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.parts: list[str] = []
        self._depth = 0          # div nesting once inside the body
        self._skip_depth = 0     # inside a headerlink we are dropping
        self.found = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        classes = _classes(attrs)

        if not self.found:
            if tag == "div" and BODY_CLASS in classes:
                self.found = True
                self._depth = 1
            return

        # Drop the permalink anchors: they render as a stray ¶ in every heading.
        if self._skip_depth or (tag == "a" and "headerlink" in classes):
            self._skip_depth += 1
            return

        if tag == "div":
            self._depth += 1

        if tag in UNWRAP_ELEMENTS:
            return

        self.parts.append(self.get_starttag_text() or "")

    def handle_endtag(self, tag: str) -> None:
        if not self.found:
            return

        if self._skip_depth:
            self._skip_depth -= 1
            return

        if tag == "div":
            self._depth -= 1
            if self._depth == 0:
                self.found = False   # stop collecting; the body is closed
                return

        if tag in UNWRAP_ELEMENTS:
            return

        if tag not in VOID_ELEMENTS:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if self.found and not self._skip_depth:
            self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.found and not self._skip_depth:
            self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.found and not self._skip_depth:
            self.parts.append(f"&#{name};")


def _classes(attrs: list[tuple[str, str | None]]) -> set[str]:
    for name, value in attrs:
        if name == "class" and value:
            return set(value.split())
    return set()


def extract(html: str) -> str | None:
    """Return the body markup, or None when it cannot be found."""
    parser = BodyExtractor()
    parser.feed(html)
    body = "".join(parser.parts).strip()
    return body or None


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2

    source, destination = Path(argv[1]), Path(argv[2])
    html = source.read_text(encoding="utf-8", errors="replace")

    body = extract(html)
    if body is None:
        # A theme that stops emitting div.body should degrade to the old
        # behaviour — a document with the sidebar in it — rather than no
        # document at all.
        print(
            f"pandoc_body: no <div class=\"{BODY_CLASS}\"> in {source}; "
            "passing the whole page to pandoc",
            file=sys.stderr,
        )
        body = html

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        f"<!DOCTYPE html>\n<html>\n<body>\n{body}\n</body>\n</html>\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

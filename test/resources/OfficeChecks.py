"""Checks on the Word and PowerPoint files the pandoc builders produce.

Both formats are zip archives of XML, so this needs nothing beyond the standard
library — deliberately, since the point of these builders is that they add one
dependency to the image and none to the test environment.
"""

import re
import zipfile

from robot.api import Failure
from robot.api.deco import keyword, library

SLIDE = re.compile(r"^ppt/slides/slide(\d+)\.xml$")
TAG = re.compile(r"<[^>]+>")


def _text(archive: zipfile.ZipFile, name: str) -> str:
    raw = archive.read(name).decode("utf-8", "replace")
    return " ".join(TAG.sub(" ", raw).split())


@library
class OfficeChecks:
    @keyword
    def docx_should_contain(self, filepath: str, text: str):
        """Assert the Word document's body contains text."""
        with zipfile.ZipFile(filepath) as archive:
            body = _text(archive, "word/document.xml")

        if text not in body:
            raise Failure(f"Could not find {text!r} in {filepath}")

    @keyword
    def docx_should_not_contain(self, filepath: str, text: str):
        """Assert the Word document's body does not contain text.

        Used for the theme's furniture — a sidebar heading or a heading
        permalink has no business in a Word document.
        """
        with zipfile.ZipFile(filepath) as archive:
            body = _text(archive, "word/document.xml")

        if text in body:
            raise Failure(f"{text!r} leaked into {filepath}")

    @keyword
    def docx_should_contain_a_table(self, filepath: str):
        with zipfile.ZipFile(filepath) as archive:
            body = archive.read("word/document.xml").decode("utf-8", "replace")

        if "<w:tbl>" not in body:
            raise Failure(f"No table in {filepath}")

    @keyword
    def count_slides(self, filepath: str) -> int:
        """Return the number of slides in the deck."""
        with zipfile.ZipFile(filepath) as archive:
            return len([n for n in archive.namelist() if SLIDE.match(n)])

    @keyword
    def slides_should_contain(self, filepath: str, text: str):
        """Assert some slide contains text."""
        with zipfile.ZipFile(filepath) as archive:
            for name in sorted(n for n in archive.namelist() if SLIDE.match(n)):
                if text in _text(archive, name):
                    return

        raise Failure(f"No slide in {filepath} contains {text!r}")

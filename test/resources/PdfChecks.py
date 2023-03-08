import re
from robot.api.deco import keyword, library
from robot.api import Failure
from robot.api.logger import logging
import fitz


@library
class PdfChecks:
    @keyword
    def should_contain_confidentiality_statement(self, filepath: str, statement: str):
        doc = fitz.open(filepath)

        exists = False
        for page in doc:
            exists = re.search(statement, page.get_text())
            logging.info(statement)
            logging.info(page.get_text())
            if exists:
                break

        if not exists:
            raise Failure("Could not find correct confidentiality statement")

    @keyword
    def should_contain_correct_cover_image(self, filepath: str, logo_path: str):
        latex = open(filepath, "r").read()

        if not re.search(logo_path, latex):
            raise Failure("Could not find correct cover image")

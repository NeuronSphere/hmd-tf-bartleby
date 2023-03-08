from robot.api.deco import keyword, library
import fitz


@library
class PdfChecks:
    @keyword
    def should_contain_confidentiality_statement(self, filepath: str, statement: str):
        doc = fitz.open(filepath)

        exists = False
        for page in doc:
            exists = statement in page.get_text()
            if exists:
                break

        return exists

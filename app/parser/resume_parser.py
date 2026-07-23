from pathlib import Path

from docx import Document
from .section_detector import SectionDetector

class ResumeParser:
    """
    Reads DOCX resume and extracts
    paragraphs for further processing.
    """

    def __init__(self, file_path):

        self.file_path = Path(file_path)

        self.document = Document(self.file_path)

    def paragraphs(self):

        data = []

        for paragraph in self.document.paragraphs:

            text = paragraph.text.strip()

            if text:

                data.append(text)

        return data

    def full_text(self):

        return "\n".join(self.paragraphs())
    def sections(self):
        """
        Return resume grouped into sections.
        """

        detector = SectionDetector()

        return detector.detect(
            self.paragraphs()
        )
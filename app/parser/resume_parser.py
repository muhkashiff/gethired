"""
GetHired Resume Parser

Reads DOCX resumes and detects logical resume sections.
"""

from pathlib import Path
from .readers import ResumeReader

from .section_detector import SectionDetector


class ResumeParser:
    """
    Production Resume Parser

    Stateless parser:
    parser = ResumeParser()
    sections = parser.parse("resume.docx")
    """

    def __init__(self):

        self.detector = SectionDetector()
        self.reader = ResumeReader()
    # ==========================================================
    # Read DOCX Paragraphs
    # ==========================================================

    def paragraphs(self, file_path):

        return self.reader.read(file_path)

    # ==========================================================
    # Complete Resume Text
    # ==========================================================

    def full_text(self, file_path):

        return "\n".join(
            self.paragraphs(file_path)
        )

    # ==========================================================
    # Detect Resume Sections
    # ==========================================================

    def parse(self, file_path):

        paragraphs = self.paragraphs(file_path)

        return self.detector.detect(
            paragraphs
        )
    # ==========================================================
    # Alias
    # ==========================================================

    def sections(self, file_path):

        return self.parse(file_path)
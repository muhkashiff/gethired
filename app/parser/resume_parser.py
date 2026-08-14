
"""
GetHired

Enterprise V5 Resume Parser

Pipeline
--------
DOCX
 ↓
ResumeReader
 ↓
SectionDetector
 ↓
ResumeSection objects
"""

from __future__ import annotations

from .readers import ResumeReader
from .section_detector import SectionDetector


class ResumeParser:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self):

        self.reader = ResumeReader()

        self.detector = SectionDetector()

    # ==========================================================
    # READ BLOCKS
    # ==========================================================

    def blocks(self, file_path):

        return self.reader.read(
            file_path
        )

    # ==========================================================
    # PARAGRAPHS
    # ==========================================================

    def paragraphs(self, file_path):

        return self.blocks(
            file_path
        )

    # ==========================================================
    # FULL TEXT
    # ==========================================================

    def full_text(self, file_path):

        blocks = self.blocks(
            file_path
        )

        return "\n".join(

            block.text
            if hasattr(block, "text")
            else str(block)

            for block in blocks
        )

    # ==========================================================
    # SECTION PARSING
    # ==========================================================

    def parse(self, file_path):

        blocks = self.blocks(
            file_path
        )

        return self.detector.detect(
            blocks
        )

    # ==========================================================
    # ALIAS
    # ==========================================================

    def sections(self, file_path):

        return self.parse(
            file_path
        )

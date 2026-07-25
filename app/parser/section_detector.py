"""
GetHired

Production Section Detector
"""

from collections import defaultdict

from .normalize import normalize_heading
from .section_dictionary import SECTION_HEADERS


class SectionDetector:

    def __init__(self):

        # Build lookup table once
        self.lookup = {}

        for section, headings in SECTION_HEADERS.items():

            for heading in headings:

                self.lookup[
                    normalize_heading(heading)
                ] = section

    # ==========================================================
    # Check if line is a section heading
    # ==========================================================

    def is_heading(self, line):

        normalized = normalize_heading(line)

        return self.lookup.get(normalized)

    # ==========================================================
    # Detect Sections
    # ==========================================================

    def detect(self, paragraphs):

        sections = defaultdict(list)

        current_section = "header"

        for line in paragraphs:

            text = line.strip()

            if not text:
                continue

            section = self.is_heading(text)

            print("--------------------------------")
            print("TEXT:", repr(text))
            print("SECTION:", section)

            if section:

                print(">>> SWITCHING TO:", section)

                current_section = section
                continue

            sections[current_section].append(text)

        return dict(sections)
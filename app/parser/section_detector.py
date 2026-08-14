
"""
GetHired

Enterprise V5 Resume Section Detector

Responsibility
--------------
Convert ordered ResumeReader blocks into typed ResumeSection
objects.

Architecture
------------
ResumeReader
    ↓
ResumeBlock
    ↓
SectionDetector
    ↓
ResumeSection
    ↓
ResumeParser
"""

from __future__ import annotations

from .resume_normalizer import normalize_heading
from .section_dictionary import SECTION_HEADERS
from .parsed_models.resume_section import ResumeSection


class SectionDetector:

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self):

        self.lookup: dict[str, str] = {}

        for section, headings in SECTION_HEADERS.items():

            for heading in headings:

                normalized = normalize_heading(
                    heading
                )

                if normalized:

                    self.lookup[normalized] = section

    # ==========================================================
    # CHECK HEADING
    # ==========================================================

    def is_heading(self, line: str):

        normalized = normalize_heading(line)

        return self.lookup.get(
            normalized
        )

    # ==========================================================
    # DETECT
    # ==========================================================

    def detect(self, blocks):

        sections: dict[str, ResumeSection] = {}

        current_section_name = "header"
        current_items = []

        start_index = 0

        # ------------------------------------------------------
        # Process blocks
        # ------------------------------------------------------

        for block in blocks:

            text = (
                block.text
                if hasattr(block, "text")
                else str(block)
            )

            text = text.strip()

            if not text:

                continue

            detected_section = self.is_heading(
                text
            )

            # --------------------------------------------------
            # Section heading
            # --------------------------------------------------

            if detected_section:

                # Finalize previous section
                self._store_section(
                    sections=sections,
                    name=current_section_name,
                    items=current_items,
                    start_index=start_index,
                    end_index=getattr(
                        block,
                        "index",
                        -1,
                    ) - 1,
                )

                current_section_name = (
                    detected_section
                )

                current_items = []

                start_index = getattr(
                    block,
                    "index",
                    -1,
                )

                continue

            # --------------------------------------------------
            # Normal content
            # --------------------------------------------------

            current_items.append(
                block
            )

        # ------------------------------------------------------
        # Final section
        # ------------------------------------------------------

        self._store_section(
            sections=sections,
            name=current_section_name,
            items=current_items,
            start_index=start_index,
            end_index=(
                getattr(
                    blocks[-1],
                    "index",
                    -1,
                )
                if blocks
                else -1
            ),
        )

        return sections

    # ==========================================================
    # STORE SECTION
    # ==========================================================

    def _store_section(
        self,
        sections,
        name,
        items,
        start_index,
        end_index,
    ):

        # Don't create empty sections
        if not items:

            return

        sections[name] = ResumeSection(

            name=name,

            title=name.replace(
                "_",
                " ",
            ).title(),

            items=list(items),

            start_index=start_index,

            end_index=end_index,
        )


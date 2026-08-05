"""
Enterprise Resume Sentence Splitter

Enterprise V12

Splits resume sections into business sentences.

Unlike normal NLP sentence splitters this understands

• Bullet lists
• Resume formatting
• Action statements
• Multi-line achievements

Pipeline

Resume Section
        ↓
Business Sentences
"""

import re

from .extraction_models import ExtractedSentence


class SentenceSplitter:

    ####################################################################
    # INITIALIZE
    ####################################################################

    def __init__(self):

        self.bullet_pattern = re.compile(

            r"^[\-\•\▪\●\*]\s*"

        )

    ####################################################################
    # PUBLIC
    ####################################################################

    def split(

        self,

        section_name,

        paragraphs,

    ):

        """
        Parameters
        ----------
        section_name

        paragraphs : list[str]

        Returns
        -------
        list[ExtractedSentence]
        """

        sentences = []

        counter = 1

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:

                continue

            # ------------------------------------------
            # Bullet Line
            # ------------------------------------------

            if self._is_bullet(paragraph):

                sentence = self._clean_bullet(paragraph)

                sentences.append(

                    self._build_sentence(

                        counter,

                        section_name,

                        sentence,

                    )

                )

                counter += 1

                continue

            # ------------------------------------------
            # Normal Paragraph
            # ------------------------------------------

            for sentence in self._split_paragraph(

                paragraph

            ):

                if not sentence:

                    continue

                sentences.append(

                    self._build_sentence(

                        counter,

                        section_name,

                        sentence,

                    )

                )

                counter += 1

        return sentences

    ####################################################################
    # PRIVATE
    ####################################################################

    def _split_paragraph(

        self,

        paragraph,

    ):

        """
        Split on sentence endings.

        Preserve business phrases.
        """

        paragraph = paragraph.replace("\n", " ")

        parts = re.split(

            r"(?<=[.!?])\s+",

            paragraph,

        )

        return [

            p.strip()

            for p in parts

            if p.strip()

        ]

    ####################################################################

    def _is_bullet(

        self,

        line,

    ):

        return bool(

            self.bullet_pattern.match(

                line

            )

        )

    ####################################################################

    def _clean_bullet(

        self,

        line,

    ):

        return self.bullet_pattern.sub(

            "",

            line,

        ).strip()

    ####################################################################

    def _build_sentence(

        self,

        counter,

        section,

        text,

    ):

        return ExtractedSentence(

            sentence_id=f"S{counter:04}",

            section=section,

            text=text,

            position=counter,

        )
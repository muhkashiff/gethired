"""
Narrative Builder (Narrative Composer)

Converts structured facts into
professional recruiter-quality
English.
"""

from .narrative_models import NarrativeParagraph, Recommendation, NarrativeReport
from .evidence_humanizer import EvidenceHumanizer

class NarrativeBuilder:

    def __init__(self, templates):

        self.templates = templates
        self.humanizer = EvidenceHumanizer()
    # ==========================================================
    # PRIVATE HELPERS
    # ==========================================================

    def _clean(self, evidence):

        """
        Remove duplicates while
        preserving order.
        """

        seen = set()

        result = []

        for item in evidence:

            item = item.strip()

            if not item:

                continue

            if item.lower() in seen:

                continue

            seen.add(item.lower())

            result.append(item)

        return result

    # ----------------------------------------------------------

    def _limit(self, evidence, maximum=4):

        return evidence[:maximum]

    # ----------------------------------------------------------

    def _join(self, evidence):

        """
        Convert

        A
        B
        C
        D

        into

        A, B, C and D
        """

        evidence = self._clean(evidence)

        if len(evidence) == 0:

            return ""

        if len(evidence) == 1:

            return evidence[0]

        if len(evidence) == 2:

            return f"{evidence[0]} and {evidence[1]}"

        return (

            ", ".join(evidence[:-1])

            +

            ", and "

            +

            evidence[-1]

        )

    # ==========================================================
    # SENTENCE
    # ==========================================================

    def build_sentence(

        self,

        section,

        evidence

    ):

        evidence = self.humanizer.humanize_list(evidence)

        evidence = self._limit(evidence)

        intro = self.templates.intro(section)

        ending = self.templates.ending(section)

        body = self._join(evidence)

        if body == "":

            return ""

        return f"{intro} {body}, {ending}"

    # ==========================================================
    # PARAGRAPH
    # ==========================================================

    def build_paragraph(

        self,

        heading,

        section,

        evidence,

        confidence=1.0

    ):

        paragraph = NarrativeParagraph()

        paragraph.heading = heading

        paragraph.body = self.build_sentence(

            section,

            evidence

        )

        paragraph.confidence = confidence

        return paragraph

    # ==========================================================
    # EXECUTIVE SUMMARY
    # ==========================================================

    def build_summary(

        self,

        paragraphs

    ):

        text = []

        for paragraph in paragraphs:

            if paragraph.body:

                text.append(paragraph.body)

        return " ".join(text)

    # ==========================================================
    # RECOMMENDATIONS
    # ==========================================================

    def build_recommendation(

        self,

        priority,

        title,

        description,

        impact

    ):

        rec = Recommendation()

        rec.priority = priority

        rec.title = title

        rec.description = description

        rec.impact = impact

        return rec

    # ==========================================================
    # COMPLETE REPORT
    # ==========================================================

    def build_report(

        self,

        title,

        paragraphs,

        strengths,

        weaknesses,

        recommendations,

        evidence,

        confidence

    ):

        report = NarrativeReport()

        report.title = title

        report.executive_summary = self.build_summary(

            paragraphs

        )

        report.overall_assessment = ""

        report.paragraphs = paragraphs

        report.strengths = strengths

        report.development_areas = weaknesses

        report.recommendations = recommendations

        report.evidence = self._clean(evidence)

        report.confidence = confidence

        return report
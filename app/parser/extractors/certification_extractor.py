"""
GetHired
Certification Extractor

Extracts Certification objects from the
Certification section of a resume.
"""

import re

from .base_extractor import BaseExtractor
from app.parser.models import Certification
from app.knowledge.certification_loader import CertificationKnowledge


class CertificationExtractor(BaseExtractor):

    def __init__(self):

        self.knowledge = CertificationKnowledge()

    # ==========================================================
    # Main Extractor
    # ==========================================================

    def extract(self, lines):

        certifications = []

        for line in self.clean(lines):

            if not line.strip():
                continue

            knowledge = self.knowledge.lookup(line)

            certification = Certification(

                name=self.extract_name(line),

                issuer=self.extract_issuer(line),

                category=knowledge.get("category", "Other"),

                level=knowledge.get("level", ""),

                year=self.extract_year(line),

                expiry=self.extract_expiry(line),

                credential_id=self.extract_credential_id(line),

                verification_url=self.extract_url(line),

                confidence=1.0,

                matched=False,

                score=0.0,

                raw_text=line,

                normalized_name=self.normalize_name(line)

            )

            certifications.append(certification)

        return certifications

    # ==========================================================
    # Certification Name
    # ==========================================================

    def extract_name(self, text):

        # Remove issuer in brackets
        name = re.sub(r"\(.*?\)", "", text)

        return name.strip()

    # ==========================================================
    # Issuer
    # ==========================================================

    def extract_issuer(self, text):

        match = re.search(r"\((.*?)\)", text)

        if match:
            return match.group(1).strip()

        return ""

    # ==========================================================
    # Year
    # ==========================================================

    def extract_year(self, text):

        match = re.search(r"(19|20)\d{2}", text)

        if match:
            return int(match.group())

        return None

    # ==========================================================
    # Expiry
    # ==========================================================

    def extract_expiry(self, text):

        match = re.search(
            r"(expires?|expiry)\D*(19|20)\d{2}",
            text,
            re.IGNORECASE
        )

        if match:

            year = re.search(r"(19|20)\d{2}", match.group())

            if year:
                return int(year.group())

        return None

    # ==========================================================
    # Credential ID
    # ==========================================================

    def extract_credential_id(self, text):

        match = re.search(

            r"(credential id|credential|license id|certificate id|id)\s*[:#]?\s*(.+)",

            text,

            re.IGNORECASE

        )

        if match:
            return match.group(2).strip()

        return ""

    # ==========================================================
    # Verification URL
    # ==========================================================

    def extract_url(self, text):

        match = re.search(

            r"https?://\S+",

            text

        )

        if match:
            return match.group()

        return ""

    # ==========================================================
    # Normalize Name
    # ==========================================================

    def normalize_name(self, text):

        name = self.extract_name(text)

        name = name.lower()

        name = re.sub(r"[^a-z0-9 ]", " ", name)

        name = re.sub(r"\s+", " ", name)

        return name.strip()
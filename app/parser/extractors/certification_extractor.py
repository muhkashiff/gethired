"""
GetHired
Certification Extractor

Extracts Certification objects from the
Certification section of a resume.
"""

import re

from .base_extractor import BaseExtractor
from app.parser.parsed_models import Certification
from app.knowledge.certification_loader import CertificationKnowledge


class CertificationExtractor(BaseExtractor):

    def __init__(self):

        self.knowledge = CertificationKnowledge()

    # ==========================================================
    # Main Extractor
    # ==========================================================

    # ==========================================================
# Main Extractor
# ==========================================================

    def extract(self, lines):

        certifications = []

        for line in self.clean(lines):

            if not line.strip():
                continue

            # Lookup certification in knowledge base
            knowledge = self.knowledge.lookup(line)

            certification = Certification(

                # Prefer canonical name from knowledge base
                name=knowledge.get(
                    "canonical_name"
                ) or self.extract_name(line),

                # Prefer issuer from knowledge base
                issuer=knowledge.get(
                    "issuer"
                ) or self.extract_issuer(line),

                # Category from knowledge base
                category=knowledge.get(
                    "category",
                    "Other"
                ),

                # Prefer knowledge base level
                level=knowledge.get(
                    "level"
                ) or self.detect_level(line),

                # Remaining fields extracted from resume
                year=self.extract_year(line),

                expiry=self.extract_expiry(line),

                credential_id=self.extract_credential_id(line),

                verification_url=self.extract_url(line),

                confidence=1.0 if knowledge.get("canonical_name") else 0.80,

                matched=False,

                score=0.0,

                raw_text=line,

                normalized_name=self.normalize_name(
                    knowledge.get(
                        "canonical_name"
                    ) or self.extract_name(line)
                )

            )

            certifications.append(certification)

        return certifications
    # ==========================================================
    # Certification Name
    # ==========================================================

    def extract_name(self, text):

        # Keep abbreviations like (PCQI)
        # Remove issuer only

        issuer = self.extract_issuer(text)

        if issuer:

            text = text.replace(f"({issuer})", "")

        return text.strip()

    # ==========================================================
    # Issuer
    # ==========================================================

    # ==========================================================
# Issuer
# ==========================================================

    def extract_issuer(self, text):

        issuers = {

            "highfield",

            "fspca",

            "cqi/irca",

            "cqi",

            "irca",

            "brcgs",

            "simplilearn",

            "minitab",

            "microsoft",

            "aws",

            "oracle",

            "google",

            "ibm",

            "pmi",

        }

        matches = re.findall(r"\((.*?)\)", text)

        for item in matches:

            clean = item.lower().replace(" certified", "").strip()

            if clean in issuers:

                return item.replace(" Certified", "").strip()

        return ""

    # ==========================================================
    # Year
    # ==========================================================

    def extract_year(self, text):

        match = re.search(r"\b(19|20)\d{2}\b", text)

        if match:
            return int(match.group())

        return None

    # ==========================================================
    # Expiry
    # ==========================================================

    def extract_expiry(self, text):

        match = re.search(

            r"(expires?|expiry)\D*((19|20)\d{2})",

            text,

            re.IGNORECASE

        )

        if match:
            return int(match.group(2))

        return None

    # ==========================================================
    # Credential ID
    # ==========================================================

    def extract_credential_id(self, text):

        patterns = [

            r"Credential ID[:\s]+([A-Za-z0-9\-]+)",

            r"License[:\s]+([A-Za-z0-9\-]+)",

            r"ID[:\s]+([A-Za-z0-9\-]+)",

        ]

        for pattern in patterns:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                return match.group(1)

        return ""

    # ==========================================================
    # Verification URL
    # ==========================================================

    def extract_url(self, text):

        match = re.search(r"https?://\S+", text)

        if match:
            return match.group()

        return ""

    # ==========================================================
    # Category Detection
    # Used only if Knowledge Base misses
    # ==========================================================

    # ==========================================================
# Category Detection
# ==========================================================

    def detect_category(self, text):

        lower = text.lower()

        food_safety = [

            "food safety",
            "haccp",
            "pcqi",
            "fspca",
            "brcgs",
            "iso 22000",

        ]

        quality = [

            "iso 9001",
            "quality",
            "cqi",
            "irca",

        ]

        analytics = [

            "analytics",
            "analysis",
            "analyst",
            "statistical",
            "statistics",
            "minitab",
            "power bi",
            "trend",
            "process",

        ]

        six_sigma = [

            "six sigma",
            "green belt",
            "black belt",

        ]

        if any(k in lower for k in food_safety):
            return "Food Safety"

        if any(k in lower for k in quality):
            return "Quality"

        if any(k in lower for k in analytics):
            return "Analytics"

        if any(k in lower for k in six_sigma):
            return "Lean Six Sigma"

        return "Other"

    # ==========================================================
    # Level Detection
    # ==========================================================

    def detect_level(self, text):

        lower = text.lower()

        # Order matters (most specific first)

        if "lead auditor" in lower:
            return "Lead Auditor"

        if "master black belt" in lower:
            return "Master Black Belt"

        if "black belt" in lower:
            return "Black Belt"

        if "green belt" in lower:
            return "Green Belt"

        if "yellow belt" in lower:
            return "Yellow Belt"

        if "white belt" in lower:
            return "White Belt"

        # Detect Level 1–9 automatically
        match = re.search(r"\blevel\s*([1-9])\b", lower)

        if match:
            return f"Level {match.group(1)}"

        if "expert" in lower:
            return "Expert"

        if "professional" in lower:
            return "Professional"

        if "associate" in lower:
            return "Associate"

        if "foundation" in lower:
            return "Foundation"

        if "practitioner" in lower:
            return "Practitioner"

        return ""


    # ==========================================================
    # Normalize Name
    # ==========================================================

    def normalize_name(self, text):

        text = text.lower()

        # Keep only letters and numbers
        text = re.sub(r"[^a-z0-9]+", " ", text)

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()
    # ==========================================================
    # Certification Abbreviation
    # ==========================================================

    def extract_abbreviation(self, text):
        """
        Returns certification abbreviation such as

        PCQI
        PMP
        CQI/IRCA
        AWS
        NEBOSH
        """

        matches = re.findall(r"\((.*?)\)", text)

        if not matches:
            return ""

        for item in matches:

            item = item.strip()

            # ignore issuers already detected
            if item.lower() in [
                "highfield",
                "simplilearn",
                "minitab",
                "fspca",
                "brcgs",
                "cqi/irca",
                "cqi",
                "irca",
            ]:
                continue

            if len(item) <= 15:
                return item

        return ""
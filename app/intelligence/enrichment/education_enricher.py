"""
Enterprise V5
Education Intelligence Enrichment
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EducationEnrichment:
    """
    Intelligence information derived from Resume.education.
    """

    highest_level: str = ""

    highest_level_rank: int = 0

    fields: list[str] = field(
        default_factory=list
    )

    institutions: list[str] = field(
        default_factory=list
    )

    certifications_present: bool = False

    analytics_education: bool = False

    business_education: bool = False

    science_education: bool = False

    technical_education: bool = False

    education_keywords: list[str] = field(
        default_factory=list
    )

    confidence: float = 0.0


class EducationEnricher:
    """
    Enriches existing Resume.education records.
    """

    LEVEL_RANKS = {
        "unknown": 0,
        "certificate": 1,
        "diploma": 2,
        "associate": 3,
        "bachelor": 4,
        "master": 5,
        "doctorate": 6,
        "phd": 6,
    }

    FIELD_RULES = {
        "analytics": [
            "data analytics",
            "data analysis",
            "analytics",
            "machine learning",
            "data science",
            "business intelligence",
        ],
        "business": [
            "business administration",
            "business management",
            "management",
            "accounting",
            "economics",
            "marketing",
            "finance",
        ],
        "science": [
            "chemistry",
            "organic chemistry",
            "biology",
            "physics",
            "microbiology",
            "food science",
        ],
        "technical": [
            "engineering",
            "computer science",
            "information technology",
            "software",
            "statistics",
            "technology",
        ],
    }

    def enrich(
        self,
        resume: Any,
    ) -> EducationEnrichment:

        education_records = getattr(
            resume,
            "education",
            [],
        ) or []

        if not education_records:

            return EducationEnrichment()

        highest_level = "unknown"
        highest_rank = 0

        fields: list[str] = []
        institutions: list[str] = []
        keywords: list[str] = []

        analytics = False
        business = False
        science = False
        technical = False

        processed = 0

        for education in education_records:

            processed += 1

            level = str(
                getattr(
                    education,
                    "level",
                    "",
                )
                or "unknown"
            ).lower().strip()

            rank = self.LEVEL_RANKS.get(
                level,
                0,
            )

            if rank > highest_rank:

                highest_rank = rank
                highest_level = level

            institution = str(
                getattr(
                    education,
                    "institution",
                    "",
                )
                or ""
            ).strip()

            if institution:
                institutions.append(
                    institution
                )

            degree = str(
                getattr(
                    education,
                    "degree",
                    "",
                )
                or ""
            )

            major = str(
                getattr(
                    education,
                    "major",
                    "",
                )
                or ""
            )

            description = str(
                getattr(
                    education,
                    "description",
                    "",
                )
                or ""
            )

            existing_keywords = (
                getattr(
                    education,
                    "keywords",
                    [],
                )
                or []
            )

            text = " ".join(
                [
                    degree,
                    major,
                    description,
                    " ".join(
                        str(x)
                        for x in existing_keywords
                    ),
                ]
            ).lower()

            for field_name, terms in self.FIELD_RULES.items():

                if any(
                    term in text
                    for term in terms
                ):

                    fields.append(
                        field_name
                    )

                    if field_name == "analytics":
                        analytics = True

                    elif field_name == "business":
                        business = True

                    elif field_name == "science":
                        science = True

                    elif field_name == "technical":
                        technical = True

            keywords.extend(
                str(x)
                for x in existing_keywords
                if str(x).strip()
            )

        unique_fields = list(
            dict.fromkeys(fields)
        )

        unique_institutions = list(
            dict.fromkeys(institutions)
        )

        unique_keywords = list(
            dict.fromkeys(keywords)
        )

        confidence = min(
            processed / 3.0,
            1.0,
        )

        return EducationEnrichment(
            highest_level=highest_level,
            highest_level_rank=highest_rank,
            fields=unique_fields,
            institutions=unique_institutions,
            analytics_education=analytics,
            business_education=business,
            science_education=science,
            technical_education=technical,
            education_keywords=unique_keywords,
            confidence=round(
                confidence,
                3,
            ),
        )
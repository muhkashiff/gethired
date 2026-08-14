"""
Enterprise V5
Industry Detection Intelligence
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class IndustryResult:
    """
    Industry intelligence result.
    """

    primary_industry: str = ""

    secondary_industries: list[str] = field(
        default_factory=list
    )

    confidence: float = 0.0

    industry_scores: dict[str, float] = field(
        default_factory=dict
    )

    signals: list[str] = field(
        default_factory=list
    )


class IndustryDetector:
    """
    Detects industries from existing Resume content.
    """

    INDUSTRY_RULES = {

        "food_beverage": [
            "food",
            "beverage",
            "juice",
            "fmcg",
            "food safety",
            "haccp",
            "brcgs",
            "fssc",
            "cgmps",
            "ssop",
            "ccp",
            "oprp",
            "prp",
            "pasteurization",
        ],

        "manufacturing": [
            "manufacturing",
            "production",
            "production line",
            "plant",
            "factory",
            "yield",
            "downtime",
            "shop-floor",
            "process improvement",
        ],

        "quality": [
            "quality assurance",
            "quality control",
            "qms",
            "quality management",
            "iso 9001",
            "audit",
            "inspection",
            "compliance",
        ],

        "retail": [
            "retail",
            "store manager",
            "store",
            "mystery shopper",
            "merchandise",
            "customer",
            "upselling",
            "cash flow",
        ],

        "supply_chain": [
            "supply chain",
            "procurement",
            "inventory",
            "warehouse",
            "distribution",
            "vendor",
            "supplier",
            "logistics",
            "forecasting",
        ],

        "data_analytics": [
            "data analytics",
            "data analyst",
            "analytics",
            "business intelligence",
            "kpi",
            "predictive",
            "machine learning",
            "statistical",
            "minitab",
            "power bi",
            "python",
        ],

        "business_operations": [
            "business operations",
            "operations",
            "sales",
            "marketing",
            "profitability",
            "budgeting",
            "financial performance",
            "strategic planning",
        ],
    }

    def detect(
        self,
        resume: Any,
    ) -> IndustryResult:

        scores = {
            industry: 0.0
            for industry in self.INDUSTRY_RULES
        }

        signals: list[str] = []

        # ------------------------------------------------------------
        # Build resume intelligence text
        # ------------------------------------------------------------

        chunks: list[str] = []

        summary = getattr(
            resume,
            "summary",
            "",
        )

        if summary:
            chunks.append(
                str(summary)
            )

        experiences = getattr(
            resume,
            "experience",
            [],
        ) or []

        for experience in experiences:

            chunks.append(
                str(
                    getattr(
                        experience,
                        "title",
                        "",
                    )
                    or ""
                )
            )

            chunks.extend(
                getattr(
                    experience,
                    "responsibilities",
                    [],
                )
                or []
            )

            chunks.extend(
                getattr(
                    experience,
                    "achievements",
                    [],
                )
                or []
            )

            chunks.append(
                str(
                    getattr(
                        experience,
                        "company",
                        "",
                    )
                    or ""
                )
            )

            chunks.append(
                str(
                    getattr(
                        experience,
                        "industry",
                        "",
                    )
                    or ""
                )
            )

        education = getattr(
            resume,
            "education",
            [],
        ) or []

        for record in education:

            chunks.extend(
                [
                    str(
                        getattr(
                            record,
                            "degree",
                            "",
                        )
                        or ""
                    ),
                    str(
                        getattr(
                            record,
                            "major",
                            "",
                        )
                        or ""
                    ),
                    str(
                        getattr(
                            record,
                            "description",
                            "",
                        )
                        or ""
                    ),
                ]
            )

        skills = getattr(
            resume,
            "skills",
            [],
        ) or []

        for skill in skills:

            chunks.append(
                str(skill)
            )

        text = " ".join(
            chunks
        ).lower()

        # ------------------------------------------------------------
        # Score industries
        # ------------------------------------------------------------

        for industry, terms in self.INDUSTRY_RULES.items():

            for term in terms:

                if term in text:

                    scores[industry] += 1.0

                    signals.append(
                        f"{industry}: matched '{term}'."
                    )

        # ------------------------------------------------------------
        # Sort
        # ------------------------------------------------------------

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        ranked = [
            item
            for item in ranked
            if item[1] > 0
        ]

        if not ranked:

            return IndustryResult(
                confidence=0.0,
                industry_scores=scores,
            )

        primary_industry = ranked[0][0]

        primary_score = ranked[0][1]

        secondary = [
            industry
            for industry, score in ranked[1:]
            if score >= max(
                primary_score * 0.35,
                2.0,
            )
        ]

        total = sum(
            score
            for _, score in ranked
        )

        confidence = (
            primary_score / total
            if total
            else 0.0
        )

        return IndustryResult(
            primary_industry=primary_industry,
            secondary_industries=secondary,
            confidence=round(
                min(confidence, 1.0),
                3,
            ),
            industry_scores=scores,
            signals=signals,
        )
"""
Enterprise V5
Experience Intelligence Enrichment

Purpose
-------
Enrich already-extracted Experience objects.

Architecture
------------
DOCX
    ↓
ResumeReader
    ↓
SectionDetector
    ↓
ResumeParser
    ↓
ResumeBuilder
    ↓
Experience
    ↓
ExperienceEnricher
    ↓
Experience Intelligence

IMPORTANT
---------
This module does NOT parse DOCX files.
This module does NOT modify ResumeBuilder.
This module does NOT replace ExperienceExtractor.

It enriches existing Experience objects.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


# ======================================================================
# RESULT MODELS
# ======================================================================


@dataclass
class AchievementEnrichment:
    text: str = ""

    quantified: bool = False

    percentage: float | None = None

    numeric_value: float | None = None

    unit: str = ""

    business_impact: bool = False

    leadership: bool = False

    executive: bool = False

    category: str = ""

    score: float = 0.0

    confidence: float = 0.0

    recommendation: str = ""


@dataclass
class ExperienceEnrichment:
    """
    Intelligence generated for one Experience object.
    """

    title: str = ""

    company: str = ""

    seniority: str = ""

    seniority_score: float = 0.0

    domains: list[str] = field(
        default_factory=list
    )

    functional_areas: list[str] = field(
        default_factory=list
    )

    leadership_score: float = 0.0

    executive_score: float = 0.0

    technical_score: float = 0.0

    operational_score: float = 0.0

    quality_score: float = 0.0

    business_score: float = 0.0

    achievement_score: float = 0.0

    achievements: list[AchievementEnrichment] = field(
        default_factory=list
    )

    quantified_achievements: int = 0

    leadership_achievements: int = 0

    business_impact_achievements: int = 0

    strengths: list[str] = field(
        default_factory=list
    )

    weaknesses: list[str] = field(
        default_factory=list
    )

    recommendations: list[str] = field(
        default_factory=list
    )

    keywords: list[str] = field(
        default_factory=list
    )

    confidence: float = 0.0


@dataclass
class ExperienceEnrichmentResult:
    success: bool = False

    records: list[ExperienceEnrichment] = field(
        default_factory=list
    )

    overall_score: float = 0.0

    confidence: float = 0.0

    error: str = ""


# ======================================================================
# EXPERIENCE ENRICHER
# ======================================================================


class ExperienceEnricher:

    # ------------------------------------------------------------------
    # SENIORITY
    # ------------------------------------------------------------------

    EXECUTIVE_TITLES = {
        "chief executive officer",
        "ceo",
        "chief operating officer",
        "coo",
        "chief quality officer",
        "chief quality and food safety officer",
        "managing director",
        "general manager",
        "vice president",
        "vp",
        "president",
        "director",
    }

    MANAGER_TITLES = {
        "manager",
        "store manager",
        "quality manager",
        "qa manager",
        "food safety manager",
        "operations manager",
        "production manager",
        "plant manager",
        "supervisor",
        "team lead",
        "team leader",
    }

    SENIOR_TITLES = {
        "senior",
        "lead",
        "principal",
        "specialist",
        "consultant",
        "coordinator",
        "chemist",
        "analyst",
        "engineer",
    }

    # ------------------------------------------------------------------
    # DOMAIN KEYWORDS
    # ------------------------------------------------------------------

    DOMAIN_KEYWORDS = {
        "quality": (
            "quality",
            "qms",
            "inspection",
            "quality control",
            "quality assurance",
            "product release",
            "nonconformance",
        ),
        "food_safety": (
            "food safety",
            "haccp",
            "fssc",
            "brcgs",
            "gmp",
            "cgmp",
            "ssop",
            "ccp",
            "prp",
            "oprp",
        ),
        "manufacturing": (
            "production",
            "manufacturing",
            "plant",
            "production line",
            "shop-floor",
            "yield",
            "downtime",
        ),
        "operations": (
            "operations",
            "operational",
            "process",
            "facility",
            "performance",
            "planning",
        ),
        "supply_chain": (
            "supply chain",
            "procurement",
            "inventory",
            "warehouse",
            "logistics",
            "supplier",
            "vendor",
            "distribution",
        ),
        "retail": (
            "retail",
            "store",
            "customer",
            "merchandise",
            "sales",
            "cash flow",
            "turnover",
        ),
        "business": (
            "business",
            "profitability",
            "financial",
            "sales",
            "marketing",
            "strategy",
            "budget",
            "forecast",
        ),
        "leadership": (
            "led",
            "lead",
            "managed",
            "directed",
            "team",
            "training",
            "staff",
            "employees",
            "cross-functional",
        ),
        "continuous_improvement": (
            "continuous improvement",
            "process improvement",
            "optimization",
            "waste reduction",
            "downtime reduction",
            "efficiency",
        ),
    }

    # ------------------------------------------------------------------
    # FUNCTIONAL AREAS
    # ------------------------------------------------------------------

    FUNCTIONAL_KEYWORDS = {
        "quality_assurance": (
            "quality assurance",
            "qa",
            "quality control",
            "inspection",
            "product release",
        ),
        "food_safety": (
            "food safety",
            "haccp",
            "fssc",
            "brcgs",
            "gmp",
            "ssop",
        ),
        "operations_management": (
            "operations",
            "operational",
            "facility",
            "process",
        ),
        "supply_chain": (
            "supply chain",
            "procurement",
            "inventory",
            "warehouse",
            "logistics",
            "distribution",
        ),
        "sales_marketing": (
            "sales",
            "marketing",
            "customer",
            "market",
            "brand",
        ),
        "finance": (
            "financial",
            "profitability",
            "budget",
            "cash flow",
            "cost",
        ),
        "people_management": (
            "team",
            "staff",
            "employees",
            "training",
            "talent acquisition",
            "onboarding",
            "shift scheduling",
        ),
        "continuous_improvement": (
            "continuous improvement",
            "process improvement",
            "optimization",
            "waste reduction",
        ),
    }

    # ------------------------------------------------------------------
    # BUSINESS IMPACT
    # ------------------------------------------------------------------

    BUSINESS_IMPACT_TERMS = (
        "profit",
        "profitability",
        "revenue",
        "sales",
        "cost",
        "cost optimization",
        "cost reduction",
        "customer",
        "business growth",
        "market",
        "distribution",
        "yield",
        "efficiency",
        "productivity",
        "turnover",
    )

    LEADERSHIP_TERMS = (
        "led",
        "managed",
        "directed",
        "spearheaded",
        "governed",
        "supervised",
        "team",
        "staff",
        "employees",
        "cross-functional",
        "training",
    )

    EXECUTIVE_TERMS = (
        "strategy",
        "strategic",
        "business growth",
        "profitability",
        "financial",
        "budget",
        "forecast",
        "market",
        "distribution",
        "executive",
        "directed",
        "managing director",
    )

    QUANTIFIED_RE = re.compile(
        r"""
        (?:
            \b\d+(?:\.\d+)?\s*%
            |
            \$\s*\d+(?:\.\d+)?\s*[KMB]?
            |
            \b\d+(?:\.\d+)?\s*(?:million|billion|thousand)
            |
            \b\d+(?:\.\d+)?\s*(?:hours|days|years|months)
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    PERCENT_RE = re.compile(
        r"(\d+(?:\.\d+)?)\s*%"
    )

    # ==================================================================
    # MAIN API
    # ==================================================================

    def enrich(
        self,
        experiences: list[Any] | None,
    ) -> ExperienceEnrichmentResult:

        result = ExperienceEnrichmentResult()

        if not experiences:
            result.success = True
            result.confidence = 0.0
            return result

        try:

            for experience in experiences:

                enriched = self._enrich_experience(
                    experience
                )

                result.records.append(
                    enriched
                )

            if result.records:

                result.overall_score = round(
                    sum(
                        item.achievement_score
                        + item.leadership_score
                        + item.business_score
                        for item in result.records
                    )
                    / len(result.records),
                    2,
                )

                result.confidence = round(
                    sum(
                        item.confidence
                        for item in result.records
                    )
                    / len(result.records),
                    3,
                )

            result.success = True

            return result

        except Exception as exc:

            result.success = False
            result.error = str(exc)

            return result

    # ==================================================================
    # SINGLE EXPERIENCE
    # ==================================================================

    def _enrich_experience(
        self,
        experience: Any,
    ) -> ExperienceEnrichment:

        title = self._string(
            getattr(
                experience,
                "title",
                "",
            )
        )

        company = self._string(
            getattr(
                experience,
                "company",
                "",
            )
        )

        responsibilities = self._list(
            getattr(
                experience,
                "responsibilities",
                [],
            )
        )

        achievements = self._list(
            getattr(
                experience,
                "achievements",
                [],
            )
        )

        all_text = " ".join(
            [
                title,
                company,
                *responsibilities,
                *achievements,
            ]
        )

        lower = all_text.lower()

        result = ExperienceEnrichment(
            title=title,
            company=company,
        )

        # --------------------------------------------------------------
        # Seniority
        # --------------------------------------------------------------

        result.seniority = (
            self._detect_seniority(
                title,
                lower,
            )
        )

        result.seniority_score = (
            self._seniority_score(
                result.seniority
            )
        )

        # --------------------------------------------------------------
        # Domains
        # --------------------------------------------------------------

        result.domains = (
            self._detect_domains(
                lower
            )
        )

        # --------------------------------------------------------------
        # Functional areas
        # --------------------------------------------------------------

        result.functional_areas = (
            self._detect_functional_areas(
                lower
            )
        )

        # --------------------------------------------------------------
        # Leadership
        # --------------------------------------------------------------

        result.leadership_score = (
            self._leadership_score(
                lower
            )
        )

        result.executive_score = (
            self._executive_score(
                lower
            )
        )

        # --------------------------------------------------------------
        # Functional scoring
        # --------------------------------------------------------------

        result.quality_score = (
            self._keyword_score(
                lower,
                self.DOMAIN_KEYWORDS["quality"],
            )
        )

        result.operational_score = (
            self._keyword_score(
                lower,
                self.DOMAIN_KEYWORDS["operations"],
            )
        )

        result.business_score = (
            self._business_score(
                lower
            )
        )

        result.technical_score = (
            self._technical_score(
                lower
            )
        )

        # --------------------------------------------------------------
        # Achievements
        # --------------------------------------------------------------

        result.achievements = [
            self._analyze_achievement(
                achievement
            )
            for achievement in achievements
            if achievement.strip()
        ]

        result.quantified_achievements = sum(
            1
            for item in result.achievements
            if item.quantified
        )

        result.leadership_achievements = sum(
            1
            for item in result.achievements
            if item.leadership
        )

        result.business_impact_achievements = sum(
            1
            for item in result.achievements
            if item.business_impact
        )

        if result.achievements:

            result.achievement_score = round(
                sum(
                    item.score
                    for item in result.achievements
                )
                / len(result.achievements),
                2,
            )

        # --------------------------------------------------------------
        # Strengths
        # --------------------------------------------------------------

        result.strengths = (
            self._build_strengths(
                result
            )
        )

        # --------------------------------------------------------------
        # Weaknesses / recommendations
        # --------------------------------------------------------------

        (
            result.weaknesses,
            result.recommendations,
        ) = self._build_gaps(
            result
        )

        # --------------------------------------------------------------
        # Keywords
        # --------------------------------------------------------------

        result.keywords = self._build_keywords(
            lower
        )

        # --------------------------------------------------------------
        # Confidence
        # --------------------------------------------------------------

        result.confidence = self._calculate_confidence(
            result
        )

        return result

    # ==================================================================
    # SENIORITY
    # ==================================================================

    def _detect_seniority(
        self,
        title: str,
        text: str,
    ) -> str:

        normalized_title = (
            title.lower().strip()
        )

        if any(
            token in normalized_title
            for token in self.EXECUTIVE_TITLES
        ):
            return "Executive"

        if any(
            token in normalized_title
            for token in self.MANAGER_TITLES
        ):
            return "Manager"

        if (
            normalized_title.startswith("senior ")
            or " lead " in f" {normalized_title} "
            or normalized_title.startswith("lead ")
        ):
            return "Senior Professional"

        if any(
            token in normalized_title
            for token in self.SENIOR_TITLES
        ):
            return "Professional"

        if any(
            term in text
            for term in (
                "managed",
                "directed",
                "spearheaded",
                "governed",
            )
        ):
            return "Manager"

        return "Professional"

    @staticmethod
    def _seniority_score(
        seniority: str,
    ) -> float:

        return {
            "Executive": 10.0,
            "Manager": 7.0,
            "Senior Professional": 5.0,
            "Professional": 3.0,
        }.get(
            seniority,
            1.0,
        )

    # ==================================================================
    # DOMAIN DETECTION
    # ==================================================================

    def _detect_domains(
        self,
        text: str,
    ) -> list[str]:

        domains = []

        for domain, keywords in (
            self.DOMAIN_KEYWORDS.items()
        ):

            if any(
                keyword in text
                for keyword in keywords
            ):
                domains.append(
                    domain
                )

        return domains

    # ==================================================================
    # FUNCTIONAL AREA
    # ==================================================================

    def _detect_functional_areas(
        self,
        text: str,
    ) -> list[str]:

        areas = []

        for area, keywords in (
            self.FUNCTIONAL_KEYWORDS.items()
        ):

            if any(
                keyword in text
                for keyword in keywords
            ):
                areas.append(
                    area
                )

        return areas

    # ==================================================================
    # SCORING
    # ==================================================================

    def _keyword_score(
        self,
        text: str,
        keywords: tuple[str, ...],
    ) -> float:

        matches = sum(
            1
            for keyword in keywords
            if keyword in text
        )

        return round(
            min(
                matches * 10,
                100,
            ),
            2,
        )

    def _leadership_score(
        self,
        text: str,
    ) -> float:

        matches = sum(
            1
            for keyword in self.LEADERSHIP_TERMS
            if keyword in text
        )

        return round(
            min(
                matches * 12,
                100,
            ),
            2,
        )

    def _executive_score(
        self,
        text: str,
    ) -> float:

        matches = sum(
            1
            for keyword in self.EXECUTIVE_TERMS
            if keyword in text
        )

        return round(
            min(
                matches * 10,
                100,
            ),
            2,
        )

    def _business_score(
        self,
        text: str,
    ) -> float:

        matches = sum(
            1
            for keyword in self.BUSINESS_IMPACT_TERMS
            if keyword in text
        )

        return round(
            min(
                matches * 10,
                100,
            ),
            2,
        )

    @staticmethod
    def _technical_score(
        text: str,
    ) -> float:

        technical_terms = (
            "laboratory",
            "analytics",
            "data",
            "python",
            "sql",
            "machine learning",
            "minitab",
            "statistical",
            "haccp",
            "qms",
            "ccp",
            "oprp",
            "prp",
        )

        matches = sum(
            1
            for term in technical_terms
            if term in text
        )

        return round(
            min(
                matches * 8,
                100,
            ),
            2,
        )

    # ==================================================================
    # ACHIEVEMENT ANALYSIS
    # ==================================================================

    def _analyze_achievement(
        self,
        text: str,
    ) -> AchievementEnrichment:

        lower = text.lower()

        item = AchievementEnrichment(
            text=text
        )

        match = self.PERCENT_RE.search(
            text
        )

        if match:

            item.quantified = True

            item.percentage = float(
                match.group(1)
            )

        elif self.QUANTIFIED_RE.search(
            text
        ):

            item.quantified = True

        item.business_impact = any(
            term in lower
            for term in self.BUSINESS_IMPACT_TERMS
        )

        item.leadership = any(
            term in lower
            for term in self.LEADERSHIP_TERMS
        )

        item.executive = any(
            term in lower
            for term in self.EXECUTIVE_TERMS
        )

        item.category = (
            self._achievement_category(
                lower
            )
        )

        score = 0.0

        if item.quantified:
            score += 30

        if item.business_impact:
            score += 25

        if item.leadership:
            score += 15

        if item.executive:
            score += 15

        if any(
            term in lower
            for term in (
                "achieved",
                "increased",
                "improved",
                "reduced",
                "expanded",
                "obtained",
                "sustained",
                "successfully",
            )
        ):
            score += 15

        item.score = min(
            score,
            100,
        )

        item.confidence = (
            0.95
            if item.quantified
            else 0.85
        )

        if (
            item.quantified
            and item.business_impact
        ):
            item.recommendation = (
                "Strong achievement with "
                "quantified business impact."
            )

        elif item.quantified:
            item.recommendation = (
                "Good quantified achievement; "
                "add business impact where possible."
            )

        else:
            item.recommendation = (
                "Add measurable KPI or business "
                "impact where possible."
            )

        return item

    @staticmethod
    def _achievement_category(
        text: str,
    ) -> str:

        if any(
            term in text
            for term in (
                "quality",
                "food safety",
                "haccp",
                "qms",
                "audit",
            )
        ):
            return "quality_food_safety"

        if any(
            term in text
            for term in (
                "sales",
                "profit",
                "revenue",
                "distribution",
                "market",
            )
        ):
            return "business_growth"

        if any(
            term in text
            for term in (
                "inventory",
                "supply chain",
                "procurement",
                "supplier",
                "logistics",
            )
        ):
            return "supply_chain"

        if any(
            term in text
            for term in (
                "team",
                "staff",
                "training",
                "employees",
            )
        ):
            return "leadership"

        return "operational_excellence"

    # ==================================================================
    # STRENGTHS
    # ==================================================================

    @staticmethod
    def _build_strengths(
        result: ExperienceEnrichment,
    ) -> list[str]:

        strengths = []

        if result.seniority in {
            "Executive",
            "Manager",
        }:
            strengths.append(
                f"{result.seniority}-level responsibility"
            )

        if result.leadership_score >= 30:
            strengths.append(
                "Strong leadership evidence"
            )

        if result.quantified_achievements:
            strengths.append(
                "Quantified achievements"
            )

        if result.business_impact_achievements:
            strengths.append(
                "Demonstrated business impact"
            )

        if "quality" in result.domains:
            strengths.append(
                "Quality management experience"
            )

        if "food_safety" in result.domains:
            strengths.append(
                "Food safety experience"
            )

        if "supply_chain" in result.domains:
            strengths.append(
                "Supply chain experience"
            )

        if "retail" in result.domains:
            strengths.append(
                "Retail operations experience"
            )

        return strengths

    # ==================================================================
    # GAPS
    # ==================================================================

    @staticmethod
    def _build_gaps(
        result: ExperienceEnrichment,
    ) -> tuple[list[str], list[str]]:

        weaknesses = []
        recommendations = []

        if not result.quantified_achievements:
            weaknesses.append(
                "No quantified achievements detected."
            )

            recommendations.append(
                "Add measurable KPIs, percentages, "
                "cost savings, revenue, productivity, "
                "or efficiency improvements."
            )

        if (
            result.leadership_score < 20
            and result.seniority in {
                "Manager",
                "Executive",
            }
        ):
            weaknesses.append(
                "Limited explicit leadership evidence."
            )

            recommendations.append(
                "Add team size, scope of responsibility, "
                "coaching, or cross-functional leadership."
            )

        if not result.business_impact_achievements:
            recommendations.append(
                "Connect responsibilities to measurable "
                "business outcomes."
            )

        return (
            weaknesses,
            recommendations,
        )

    # ==================================================================
    # KEYWORDS
    # ==================================================================

    def _build_keywords(
        self,
        text: str,
    ) -> list[str]:

        keywords = []

        for group in (
            self.DOMAIN_KEYWORDS,
            self.FUNCTIONAL_KEYWORDS,
        ):

            for values in group.values():

                for value in values:

                    if (
                        value in text
                        and value not in keywords
                    ):
                        keywords.append(
                            value
                        )

        return keywords

    # ==================================================================
    # CONFIDENCE
    # ==================================================================

    @staticmethod
    def _calculate_confidence(
        result: ExperienceEnrichment,
    ) -> float:

        evidence = 0

        if result.title:
            evidence += 1

        if result.company:
            evidence += 1

        if result.domains:
            evidence += 1

        if result.functional_areas:
            evidence += 1

        if result.achievements:
            evidence += 1

        if result.strengths:
            evidence += 1

        return round(
            min(
                evidence / 6,
                1.0,
            ),
            3,
        )

    # ==================================================================
    # UTILITIES
    # ==================================================================

    @staticmethod
    def _string(
        value: Any,
    ) -> str:

        if value is None:
            return ""

        return str(value).strip()

    @staticmethod
    def _list(
        value: Any,
    ) -> list[str]:

        if value is None:
            return []

        if isinstance(
            value,
            (list, tuple),
        ):
            return [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

        return [str(value).strip()]
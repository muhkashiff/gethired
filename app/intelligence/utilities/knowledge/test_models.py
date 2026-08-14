
"""
Enterprise V5
Section Extraction Adapter Test

Tests:

    ResumeSection
        ↓
    SectionExtractionAdapter
        ├── EducationExtractor
        └── ExperienceExtractor
"""

from __future__ import annotations

import sys
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


"""
Enterprise V5
Resume Intelligence Enrichment Test

Tests:

1. Experience enrichment
2. Seniority detection
3. Domain detection
4. Leadership detection
5. Achievement intelligence
6. Education enrichment
7. Industry enrichment
8. Complete enrichment pipeline
"""


from dataclasses import dataclass, field

from app.intelligence.enrichment.experience_enricher import (
    ExperienceEnricher,
)

from app.intelligence.enrichment.resume_enrichment_pipeline import (
    ResumeEnrichmentPipeline,
)


# ======================================================================
# TEST MODELS
# ======================================================================


@dataclass
class TestExperience:

    title: str = ""

    company: str = ""

    location: str = ""

    start_year: int = 0

    end_year: int = 0

    current_job: bool = False

    duration: float = 0.0

    responsibilities: list[str] = field(
        default_factory=list
    )

    achievements: list[str] = field(
        default_factory=list
    )


@dataclass
class TestEducation:

    degree: str = ""

    major: str = ""

    institution: str = ""

    description: str = ""

    location: str = ""

    graduation_year: int = 0

    level: str = ""

    keywords: list[str] = field(
        default_factory=list
    )


@dataclass
class TestResume:

    name: str = ""

    summary: str = ""

    experience: list[TestExperience] = field(
        default_factory=list
    )

    education: list[TestEducation] = field(
        default_factory=list
    )


# ======================================================================
# REALISTIC RESUME DATA
# ======================================================================


def build_test_resume():

    return TestResume(

        name="MUHAMMAD KASHIF",

        summary=(
            "Quality Assurance Specialist, Business "
            "Operations Leader and Data Analyst with "
            "15+ years of experience."
        ),

        experience=[

            # ----------------------------------------------------------
            # QA CHEMIST
            # ----------------------------------------------------------

            TestExperience(

                title="QA Chemist",

                company=(
                    "Coca-Cola Beverages Pakistan Ltd."
                ),

                location=(
                    "Lahore, Pakistan"
                ),

                start_year=2010,

                end_year=2016,

                duration=6,

                responsibilities=[

                    "Spearheaded the site-wide "
                    "implementation of the integrated "
                    "Quality and Food Safety Management "
                    "System.",

                    "Oversaw laboratory and floor product "
                    "inspections and finished product release.",

                    "Led cross-functional teams at the "
                    "contract Toll Filling facility.",

                    "Drove continuous process improvement "
                    "to minimize raw material waste and "
                    "machinery downtime.",

                    "Led site-wide HACCP governance across "
                    "CSD and NCB operations.",
                ],

                achievements=[

                    "Achieved 99%+ production line product yield.",

                    "Sustained a 99.5% plant-wide quality rating.",

                    "Achieved 98.6% staff participation in "
                    "Food Safety and Quality Training programs.",
                ],
            ),

            # ----------------------------------------------------------
            # MANAGING DIRECTOR
            # ----------------------------------------------------------

            TestExperience(

                title="Managing Director",

                company="Nutrain (Pvt) Ltd.",

                location="Lahore, Pakistan",

                start_year=2025,

                end_year=2026,

                duration=1,

                responsibilities=[

                    "Led the strategic growth and day-to-day "
                    "operations of a food and FMCG business.",

                    "Directed sales, marketing, procurement, "
                    "inventory management, supply chain "
                    "operations, distribution and financial "
                    "performance.",

                    "Developed and expanded the USVA Premium "
                    "Basmati Rice brand.",

                    "Managed wholesalers, retailers, "
                    "distributors and key accounts.",

                    "Oversaw budgeting, forecasting and "
                    "operational performance.",
                ],

                achievements=[

                    "Successfully expanded distribution "
                    "channels and increased sales.",

                    "Improved supply chain efficiency and "
                    "profitability through supplier negotiations.",

                    "Established strong wholesale and retail "
                    "partnerships.",
                ],
            ),

            # ----------------------------------------------------------
            # RETAIL STORE MANAGER
            # ----------------------------------------------------------

            TestExperience(

                title="Retail Store Manager",

                company=(
                    "Shell Gas Station & Retail Store"
                ),

                location="Canada",

                start_year=2016,

                end_year=2024,

                duration=8,

                responsibilities=[

                    "Managed multi-faceted retail business "
                    "operations.",

                    "Governed vendor management, inventory "
                    "cycle counts and merchandise ordering.",

                    "Directed talent acquisition, staff "
                    "onboarding and shift scheduling.",

                    "Optimized operations to maximize "
                    "product turnover.",
                ],

                achievements=[

                    "Obtained a perfect 100% Shell Mystery "
                    "Shopper score.",

                    "Achieved a flawless 100% Food Safety "
                    "Surprise Audit score.",

                    "Performed KPI reporting and performance "
                    "tracking to drive retail profitability.",
                ],
            ),
        ],

        education=[

            TestEducation(
                degree=(
                    "Bootcamp Certificate: Data Analytics"
                ),
                institution="University of Toronto",
                location="ON, Canada",
                level="certificate",
                description=(
                    "Python, data visualization, "
                    "machine learning and data analytics."
                ),
                keywords=[
                    "data analytics"
                ],
            ),

            TestEducation(
                degree=(
                    "Post Graduation Diploma: "
                    "Business Administration"
                ),
                institution="Selkirk College",
                location="BC, Canada",
                level="diploma",
                description=(
                    "Accounting, Economics, Business "
                    "Mathematics, Leadership and "
                    "Market Strategy."
                ),
                keywords=[
                    "business administration"
                ],
            ),

            TestEducation(
                degree="M.Sc. Chemistry",
                major="Organic Chemistry",
                institution="University of the Punjab",
                location="Pakistan",
                level="master",
                description=(
                    "Advanced thesis and curriculum "
                    "focusing on Organic Chemistry "
                    "and laboratory methodologies."
                ),
                keywords=[
                    "chemistry",
                    "organic chemistry",
                ],
            ),
        ],
    )


# ======================================================================
# TEST 1
# ======================================================================


def test_experience_enricher():

    resume = build_test_resume()

    enricher = ExperienceEnricher()

    result = enricher.enrich(
        resume.experience
    )

    assert result.success is True

    assert len(
        result.records
    ) == 3

    print()
    print("=" * 70)
    print("TEST 1 — EXPERIENCE ENRICHER")
    print("=" * 70)

    for item in result.records:

        print()
        print(
            f"Title       : {item.title}"
        )

        print(
            f"Company     : {item.company}"
        )

        print(
            f"Seniority   : {item.seniority}"
        )

        print(
            f"Domains     : {item.domains}"
        )

        print(
            f"Functions   : {item.functional_areas}"
        )

        print(
            f"Leadership  : {item.leadership_score}"
        )

        print(
            f"Business    : {item.business_score}"
        )

        print(
            f"Achievements: {len(item.achievements)}"
        )

        print(
            f"Confidence  : {item.confidence}"
        )


# ======================================================================
# TEST 2
# ======================================================================


def test_expected_seniority():

    resume = build_test_resume()

    result = ExperienceEnricher().enrich(
        resume.experience
    )

    seniorities = [
        item.seniority
        for item in result.records
    ]

    print()
    print("=" * 70)
    print("TEST 2 — SENIORITY")
    print("=" * 70)

    print(
        "Actual:",
        seniorities,
    )

    assert seniorities[0] in {
        "Professional",
        "Senior Professional",
    }

    assert seniorities[1] == "Executive"

    assert seniorities[2] == "Manager"

    print(
        "PASS — Experience seniority detection"
    )


# ======================================================================
# TEST 3
# ======================================================================


def test_domains():

    resume = build_test_resume()

    result = ExperienceEnricher().enrich(
        resume.experience
    )

    qa = result.records[0]

    md = result.records[1]

    retail = result.records[2]

    print()
    print("=" * 70)
    print("TEST 3 — DOMAIN DETECTION")
    print("=" * 70)

    print(
        "QA Chemist:",
        qa.domains,
    )

    print(
        "Managing Director:",
        md.domains,
    )

    print(
        "Retail Store Manager:",
        retail.domains,
    )

    assert "quality" in qa.domains

    assert "food_safety" in qa.domains

    assert "manufacturing" in qa.domains

    assert "business" in md.domains

    assert "supply_chain" in md.domains

    assert "retail" in retail.domains

    print(
        "PASS — Domain detection"
    )


# ======================================================================
# TEST 4
# ======================================================================


def test_achievement_enrichment():

    resume = build_test_resume()

    result = ExperienceEnricher().enrich(
        resume.experience
    )

    print()
    print("=" * 70)
    print("TEST 4 — ACHIEVEMENT INTELLIGENCE")
    print("=" * 70)

    for experience in result.records:

        print()
        print(
            experience.title
        )

        for achievement in (
            experience.achievements
        ):

            print(
                f"  {achievement.text}"
            )

            print(
                f"    quantified   = "
                f"{achievement.quantified}"
            )

            print(
                f"    business     = "
                f"{achievement.business_impact}"
            )

            print(
                f"    leadership   = "
                f"{achievement.leadership}"
            )

            print(
                f"    score        = "
                f"{achievement.score}"
            )

    assert any(
        item.quantified
        for item in result.records[0].achievements
    )

    assert any(
        item.quantified
        for item in result.records[2].achievements
    )

    print(
        "PASS — Achievement enrichment"
    )


# ======================================================================
# TEST 5
# ======================================================================


def test_complete_pipeline():

    resume = build_test_resume()

    pipeline = ResumeEnrichmentPipeline()

    result = pipeline.enrich(
        resume
    )

    assert result.success is True

    assert len(
        result.experience
    ) == 3

    assert result.seniority.score > 0

    assert result.education.score > 0

    assert result.industry.confidence > 0

    assert result.leadership.score > 0

    assert result.achievements.score > 0

    print()
    print("=" * 70)
    print("TEST 5 — COMPLETE RESUME ENRICHMENT PIPELINE")
    print("=" * 70)

    print(
        f"Success           : {result.success}"
    )

    print(
        f"Experience count   : "
        f"{len(result.experience)}"
    )

    print(
        f"Seniority score    : "
        f"{result.seniority.score}"
    )

    print(
        f"Education score    : "
        f"{result.education.score}"
    )

    print(
        f"Industry score     : "
        f"{result.industry.score}"
    )

    print(
        f"Leadership score   : "
        f"{result.leadership.score}"
    )

    print(
        f"Quality score      : "
        f"{result.quality.score}"
    )

    print(
        f"Operations score   : "
        f"{result.operations.score}"
    )

    print(
        f"Achievement score  : "
        f"{result.achievements.score}"
    )

    print(
        f"Overall score      : "
        f"{result.overall_score}"
    )

    print(
        f"Confidence         : "
        f"{result.confidence}"
    )

    print()
    print(
        "STRENGTHS"
    )

    for item in result.experience:

        print(
            f"\n{item.title}"
        )

        for strength in item.strengths:

            print(
                f"  + {strength}"
            )

    print()
    print(
        "RECOMMENDATIONS"
    )

    for item in result.experience:

        for recommendation in (
            item.recommendations
        ):

            print(
                f"  - {item.title}: "
                f"{recommendation}"
            )

    print()
    print(
        "PASS — Complete enrichment pipeline"
    )


# ======================================================================
# RUN ALL
# ======================================================================


def run_all_tests():

    print()
    print("=" * 70)
    print(
        "ENTERPRISE V5 — RESUME "
        "INTELLIGENCE ENRICHMENT TEST"
    )
    print("=" * 70)

    test_experience_enricher()

    test_expected_seniority()

    test_domains()

    test_achievement_enrichment()

    test_complete_pipeline()

    print()
    print("=" * 70)
    print(
        "ALL RESUME ENRICHMENT TESTS PASSED"
    )
    print("=" * 70)


if __name__ == "__main__":

    run_all_tests()
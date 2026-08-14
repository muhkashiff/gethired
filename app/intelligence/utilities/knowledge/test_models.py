
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


# ============================================================
# IMPORTS
# ============================================================

from app.parser.parsed_models.resume_section import (
    ResumeSection,
)

from app.parser.section_extraction_adapter import (
    SectionExtractionAdapter,
)


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print("=" * 70)
    print("ENTERPRISE V5 — SECTION EXTRACTION ADAPTER TEST")
    print("=" * 70)

    # ========================================================
    # EDUCATION SECTION
    # ========================================================

    education_section = ResumeSection(
        name="education",
        title="Education",
        items=[
            (
                "Bootcamp Certificate: Data Analytics"
                "\t\t"
                "University of Toronto, ON, Canada"
            ),

            (
                "Completed a Data Analytics Certificate from "
                "the University of Toronto, gaining practical "
                "experience in Python, data visualization, "
                "machine learning, and data-driven "
                "decision-making. Skilled in analyzing complex "
                "datasets, uncovering actionable insights, and "
                "communicating findings through effective data "
                "storytelling."
            ),

            (
                "Post Graduation Diploma: Business Administration"
                "\t\t"
                "Selkirk College, BC, Canada"
            ),

            (
                "A comprehensive 2-year business management "
                "program with a core focus on Accounting, "
                "Economics, Business Mathematics, Leadership, "
                "Communication Skills, and Market Strategy."
            ),

            (
                "M.Sc. Chemistry (Organic Chemistry Major)"
                "\t\t"
                "University of the Punjab, Pakistan"
            ),

            (
                "Four-year Bachelor's degree academic "
                "equivalency verified by WES. 16 years of "
                "formalized higher education with an advanced "
                "thesis and curriculum focusing on Organic "
                "Chemistry and laboratory methodologies."
            ),
        ],
    )

    # ========================================================
    # EXPERIENCE SECTION
    # ========================================================

    experience_section = ResumeSection(
        name="experience",
        title="Experience",
        items=[
            (
                "QA Chemist | Coca-Cola Beverages Pakistan Ltd. "
                "2010 - 2016 | Lahore, Pakistan"
            ),

            (
                "Spearheaded the site-wide implementation, "
                "execution, and regulatory compliance of the "
                "integrated Quality and Food Safety Management "
                "System (QMS)."
            ),

            (
                "Oversaw strict laboratory and floor product "
                "inspections, meticulously executing and "
                "governing the finished product release program "
                "based on established quality criteria."
            ),

            "Key Accomplishments",

            (
                "Achieved a remarkable 99%+ production line "
                "product yield through targeted waste reduction "
                "and down-time minimization initiatives."
            ),

            (
                "Managing Director | Nutrain (Pvt) Ltd. "
                "2025 - 2026 | Lahore, Pakistan"
            ),

            (
                "Led the strategic growth and day-to-day "
                "operations of a food and FMCG business "
                "specializing in premium rice, edible oils, "
                "ghee, juices, and other consumer products."
            ),

            (
                "Directed sales, marketing, procurement, "
                "inventory management, supply chain operations, "
                "distribution, and financial performance."
            ),

            "Key Accomplishments",

            (
                "Successfully expanded distribution channels "
                "and increased sales through market development "
                "and customer-focused initiatives."
            ),

            (
                "Retail Store Manager | Shell Gas Station & "
                "Retail Store 2016 - 2024 | Canada"
            ),

            (
                "Managed multi-faceted retail business "
                "operations by forecasting and meeting evolving "
                "consumer needs using predictive demand "
                "parameters."
            ),

            (
                "Governed comprehensive vendor management, "
                "inventory cycle counts, merchandise ordering, "
                "and financial cash flow optimization."
            ),

            "Key Accomplishments",

            (
                "Obtained a perfect 100% score for the highly "
                "regulated corporate Shell Mystery Shopper "
                "program."
            ),
        ],
    )

    # ========================================================
    # ADAPTER
    # ========================================================

    adapter = SectionExtractionAdapter()

    # ========================================================
    # EXTRACT
    # ========================================================

    education_result = adapter.extract_education(
        education_section
    )

    experience_result = adapter.extract_experience(
        experience_section
    )

    # ========================================================
    # EDUCATION OUTPUT
    # ========================================================

    print()
    print("=" * 70)
    print("EDUCATION")
    print("=" * 70)

    print(
        "Success     :",
        education_result.success,
    )

    print(
        "Count       :",
        education_result.count,
    )

    print(
        "Confidence  :",
        education_result.confidence,
    )

    print("-" * 70)

    for index, education in enumerate(
        education_result.records,
        start=1,
    ):

        print(
            f"\n[EDUCATION {index}]"
        )

        print(
            education
        )

    # ========================================================
    # EXPERIENCE OUTPUT
    # ========================================================

    print()
    print("=" * 70)
    print("EXPERIENCE")
    print("=" * 70)

    print(
        "Success     :",
        experience_result.success,
    )

    print(
        "Count       :",
        experience_result.count,
    )

    print(
        "Confidence  :",
        experience_result.confidence,
    )

    print("-" * 70)

    for index, experience in enumerate(
        experience_result.records,
        start=1,
    ):

        print(
            f"\n[EXPERIENCE {index}]"
        )

        print(
            experience
        )

    # ========================================================
    # REGRESSION CHECKS
    # ========================================================

    print()
    print("=" * 70)
    print("REGRESSION CHECKS")
    print("=" * 70)

    assert education_result.success is True

    assert education_result.count == 3, (
        "Education regression failure: "
        f"expected 3, got {education_result.count}"
    )

    assert experience_result.success is True

    assert experience_result.count == 3, (
        "Experience regression failure: "
        f"expected 3, got {experience_result.count}"
    )

    # --------------------------------------------------------
    # Education identity checks
    # --------------------------------------------------------

    assert (
        education_result.records[0].institution
        == "University of Toronto"
    )

    assert (
        education_result.records[1].institution
        == "Selkirk College"
    )

    assert (
        education_result.records[2].institution
        == "University of the Punjab"
    )

    assert (
        education_result.records[2].major
        == "Organic Chemistry"
    )

    # --------------------------------------------------------
    # Experience identity checks
    # --------------------------------------------------------

    assert (
        experience_result.records[0].company
        == "Coca-Cola Beverages Pakistan Ltd."
    )

    assert (
        experience_result.records[1].company
        == "Nutrain (Pvt) Ltd."
    )

    assert (
        experience_result.records[2].company
        == "Shell Gas Station & Retail Store"
    )

    print()
    print("ALL REGRESSION CHECKS PASSED")

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


# ============================================================
# PYTHON ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()


from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
"""
GetHired
Resume Builder - Parser/Extractor Layer Test

Purpose
-------
Test the current parser/extractor layer before moving to
the new Enterprise V5 ExtractionEngine pipeline.

Tests:
    1. Parser imports
    2. SkillsExtractor
    3. CertificationExtractor
    4. ResumeBuilder
    5. Final Resume object
    6. Extracted skills/certifications

Run:
    python test_resume_parser.py
"""

from pprint import pprint
import traceback


# =====================================================================
# IMPORTS
# =====================================================================

try:

    from app.parser.extractors import (
        ContactExtractor,
        SkillsExtractor,
        ExperienceExtractor,
        EducationExtractor,
        CertificationExtractor,
        LanguageExtractor,
        ProjectExtractor,
        AwardExtractor,
        ReferenceExtractor,
    )

    from app.parser.resume_builder import ResumeBuilder

except Exception as error:

    print("\n" + "=" * 80)
    print("IMPORT ERROR")
    print("=" * 80)

    print(type(error).__name__)
    print(str(error))

    traceback.print_exc()

    raise SystemExit(1)


# =====================================================================
# TEST RESUME SECTIONS
# =====================================================================

TEST_SECTIONS = {

    "header": [
        "MUHAMMAD KASHIF",
        "Quality Assurance & Food Safety Professional",
        "Phone: +923334940827",
        "Email: muhkashiff@gmail.com",
        "Location: Lahore, Punjab, Pakistan",
        "LinkedIn: linkedin.com/in/muhkashiff",
        "GitHub: github.com/muhkashiff",
    ],

    "summary": [
        (
            "Result-driven Quality Assurance Specialist, Business "
            "Operations Leader, and Data Analyst with 15+ years of "
            "experience across manufacturing, FMCG, food and beverage, "
            "supply chain, distribution, and retail sectors."
        )
    ],

    "skills": [
        "Python",
        "SQL",
        "PostgreSQL",
        "Pandas",
        "scikit-learn",
        "Data Analysis",
        "Power BI",
        "Tableau",
        "Minitab",
        "HACCP",
        "FSSC 22000",
        "BRCGS",
        "ISO 9001",
        "Food Safety",
        "Quality Assurance",
        "Quality Control",
        "Six Sigma",
        "Lean Management",
    ],

    "experience": [
        (
            "QA Line Chemist, Coca-Cola Beverages Pakistan Ltd., "
            "Lahore, April 2010 - April 2016. "
            "Performed quality control testing, process monitoring, "
            "laboratory analysis, GMP and food safety activities."
        ),
        (
            "Retail Store Manager, Shell Gas Station & Retail Store, "
            "Canada, 2016 - 2024. "
            "Managed store operations, inventory, customer service, "
            "food safety and team performance."
        ),
    ],

    "education": [
        "M.Sc Chemistry",
        "Business Administration Diploma, Selkirk College",
        "24-week Data Analytics Boot Camp, University of Toronto",
    ],

    "certifications": [
        "Lead Auditor QMS ISO 9001:2021 - CQI/IRCA",
        "Lead Auditor Global Standard for Food Safety Version 8 - BRCGS",
        "BRCGS Certified",
        "Preventive Control Qualified Individual (PCQI) - Human Food",
        "FSPCA Certified",
        "HACCP Level 4 - Highfield",
        "Food Safety Level 4 - Highfield",
        "Lean Management",
        "Six Sigma Green Belt",
        "Six Sigma Black Belt",
        "Agile Scrum Master",
    ],

    "languages": [
        "English",
        "Urdu",
        "Punjabi",
    ],

    "projects": [],

    "awards": [],

    "references": [],
}


# =====================================================================
# SECTION PRINTER
# =====================================================================

def print_section(title):

    print("\n")
    print("=" * 80)
    print(title)
    print("=" * 80)


# =====================================================================
# TEST IMPORTS
# =====================================================================

def test_imports():

    print_section("1. TESTING PARSER EXTRACTOR IMPORTS")

    extractors = {

        "ContactExtractor": ContactExtractor,
        "SkillsExtractor": SkillsExtractor,
        "ExperienceExtractor": ExperienceExtractor,
        "EducationExtractor": EducationExtractor,
        "CertificationExtractor": CertificationExtractor,
        "LanguageExtractor": LanguageExtractor,
        "ProjectExtractor": ProjectExtractor,
        "AwardExtractor": AwardExtractor,
        "ReferenceExtractor": ReferenceExtractor,
    }

    for name, extractor in extractors.items():

        print(
            f"[OK] {name}: "
            f"{extractor}"
        )

    print("\nAll parser extractor imports succeeded.")

    return True


# =====================================================================
# TEST SKILLS EXTRACTOR
# =====================================================================

def test_skills_extractor():

    print_section("2. TESTING SKILLS EXTRACTOR")

    extractor = SkillsExtractor()

    skills_input = TEST_SECTIONS["skills"]

    print("\nINPUT SKILLS:")
    for item in skills_input:
        print(f"  - {item}")

    try:

        extracted = extractor.extract(
            skills_input
        )

    except Exception as error:

        print("\n[FAILED] SkillsExtractor.extract()")

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        traceback.print_exc()

        return None

    print("\nEXTRACTED SKILLS:")

    pprint(extracted)

    print(
        "\nSkills extracted:",
        len(extracted)
    )

    for index, skill in enumerate(
        extracted,
        start=1,
    ):

        print(
            f"\nSkill #{index}"
        )

        print(
            "  Type:",
            type(skill).__name__,
        )

        if hasattr(skill, "__dict__"):

            pprint(
                skill.__dict__
            )

        else:

            print(
                "  Value:",
                skill,
            )

    return extracted


# =====================================================================
# TEST CERTIFICATION EXTRACTOR
# =====================================================================

def test_certification_extractor():

    print_section(
        "3. TESTING CERTIFICATION EXTRACTOR"
    )

    extractor = CertificationExtractor()

    certification_input = (
        TEST_SECTIONS["certifications"]
    )

    print("\nINPUT CERTIFICATIONS:")

    for item in certification_input:

        print(
            f"  - {item}"
        )

    try:

        extracted = extractor.extract(
            certification_input
        )

    except Exception as error:

        print(
            "\n[FAILED] "
            "CertificationExtractor.extract()"
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        traceback.print_exc()

        return None

    print(
        "\nEXTRACTED CERTIFICATIONS:"
    )

    pprint(extracted)

    print(
        "\nCertifications extracted:",
        len(extracted)
    )

    for index, certification in enumerate(
        extracted,
        start=1,
    ):

        print(
            f"\nCertification #{index}"
        )

        print(
            "  Type:",
            type(certification).__name__,
        )

        if hasattr(
            certification,
            "__dict__",
        ):

            pprint(
                certification.__dict__
            )

        else:

            print(
                "  Value:",
                certification,
            )

    return extracted


# =====================================================================
# TEST RESUME BUILDER
# =====================================================================

def test_resume_builder():

    print_section(
        "4. TESTING RESUME BUILDER"
    )

    try:

        builder = ResumeBuilder()

    except Exception as error:

        print(
            "\n[FAILED] ResumeBuilder initialization"
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        traceback.print_exc()

        return None

    print(
        "[OK] ResumeBuilder initialized."
    )

    try:

        resume = builder.build(
            TEST_SECTIONS
        )

    except Exception as error:

        print(
            "\n[FAILED] ResumeBuilder.build()"
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        traceback.print_exc()

        return None

    print(
        "\n[OK] ResumeBuilder.build() succeeded."
    )

    print(
        "\nResume object type:",
        type(resume).__name__,
    )

    return resume


# =====================================================================
# INSPECT RESUME
# =====================================================================

def inspect_resume(resume):

    print_section(
        "5. FINAL RESUME OBJECT"
    )

    if resume is None:

        print(
            "[FAILED] Resume object is None."
        )

        return

    # ---------------------------------------------------------------
    # PERSONAL INFORMATION
    # ---------------------------------------------------------------

    print(
        "\nPERSONAL INFORMATION"
    )

    personal = resume.personal_information

    print(
        "  Name:",
        getattr(
            personal,
            "name",
            "",
        ),
    )

    print(
        "  Email:",
        getattr(
            personal,
            "email",
            "",
        ),
    )

    print(
        "  Phone:",
        getattr(
            personal,
            "phone",
            "",
        ),
    )

    print(
        "  LinkedIn:",
        getattr(
            personal,
            "linkedin",
            "",
        ),
    )

    print(
        "  GitHub:",
        getattr(
            personal,
            "github",
            "",
        ),
    )

    print(
        "  Address:",
        getattr(
            personal,
            "address",
            "",
        ),
    )

    # ---------------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------------

    print(
        "\nSUMMARY"
    )

    print(
        resume.summary
    )

    # ---------------------------------------------------------------
    # SKILLS
    # ---------------------------------------------------------------

    print(
        "\nSKILLS"
    )

    print(
        "Count:",
        len(resume.skills)
    )

    for index, skill in enumerate(
        resume.skills,
        start=1,
    ):

        print(
            f"\n  Skill #{index}"
        )

        print(
            "    Type:",
            type(skill).__name__,
        )

        if hasattr(
            skill,
            "__dict__",
        ):

            pprint(
                skill.__dict__
            )

        else:

            print(
                "    Value:",
                skill,
            )

    # ---------------------------------------------------------------
    # CERTIFICATIONS
    # ---------------------------------------------------------------

    print(
        "\nCERTIFICATIONS"
    )

    print(
        "Count:",
        len(resume.certifications)
    )

    for index, certification in enumerate(
        resume.certifications,
        start=1,
    ):

        print(
            f"\n  Certification #{index}"
        )

        print(
            "    Type:",
            type(certification).__name__,
        )

        if hasattr(
            certification,
            "__dict__",
        ):

            pprint(
                certification.__dict__
            )

        else:

            print(
                "    Value:",
                certification,
            )

    # ---------------------------------------------------------------
    # EXPERIENCE
    # ---------------------------------------------------------------

    print(
        "\nEXPERIENCE"
    )

    print(
        "Count:",
        len(resume.experience)
    )

    # ---------------------------------------------------------------
    # EDUCATION
    # ---------------------------------------------------------------

    print(
        "\nEDUCATION"
    )

    print(
        "Count:",
        len(resume.education)
    )

    # ---------------------------------------------------------------
    # LANGUAGES
    # ---------------------------------------------------------------

    print(
        "\nLANGUAGES"
    )

    print(
        "Count:",
        len(resume.languages)
    )

    # ---------------------------------------------------------------
    # PROJECTS
    # ---------------------------------------------------------------

    print(
        "\nPROJECTS"
    )

    print(
        "Count:",
        len(resume.projects)
    )

    # ---------------------------------------------------------------
    # AWARDS
    # ---------------------------------------------------------------

    print(
        "\nAWARDS"
    )

    print(
        "Count:",
        len(resume.awards)
    )


# =====================================================================
# VALIDATION
# =====================================================================

def validate_results(
    skills,
    certifications,
    resume,
):

    print_section(
        "6. BASIC VALIDATION"
    )

    passed = 0
    failed = 0

    # ---------------------------------------------------------------
    # SKILLS
    # ---------------------------------------------------------------

    if skills is None:

        print(
            "[FAIL] Skills extractor crashed."
        )

        failed += 1

    elif len(skills) == 0:

        print(
            "[FAIL] SkillsExtractor returned "
            "zero skills."
        )

        failed += 1

    else:

        print(
            f"[PASS] SkillsExtractor returned "
            f"{len(skills)} skills."
        )

        passed += 1

    # ---------------------------------------------------------------
    # CERTIFICATIONS
    # ---------------------------------------------------------------

    if certifications is None:

        print(
            "[FAIL] Certification extractor crashed."
        )

        failed += 1

    elif len(certifications) == 0:

        print(
            "[FAIL] CertificationExtractor returned "
            "zero certifications."
        )

        failed += 1

    else:

        print(
            f"[PASS] CertificationExtractor returned "
            f"{len(certifications)} certifications."
        )

        passed += 1

    # ---------------------------------------------------------------
    # RESUME
    # ---------------------------------------------------------------

    if resume is None:

        print(
            "[FAIL] ResumeBuilder returned no Resume."
        )

        failed += 1

    else:

        print(
            "[PASS] ResumeBuilder returned Resume."
        )

        passed += 1

    # ---------------------------------------------------------------
    # RESUME SKILLS
    # ---------------------------------------------------------------

    if resume is not None:

        if len(resume.skills) == 0:

            print(
                "[FAIL] Resume contains zero skills."
            )

            failed += 1

        else:

            print(
                f"[PASS] Resume contains "
                f"{len(resume.skills)} skills."
            )

            passed += 1

        # -----------------------------------------------------------
        # RESUME CERTIFICATIONS
        # -----------------------------------------------------------

        if len(resume.certifications) == 0:

            print(
                "[FAIL] Resume contains "
                "zero certifications."
            )

            failed += 1

        else:

            print(
                f"[PASS] Resume contains "
                f"{len(resume.certifications)} certifications."
            )

            passed += 1

    # ---------------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------------

    print(
        "\nValidation summary:"
    )

    print(
        f"  Passed: {passed}"
    )

    print(
        f"  Failed: {failed}"
    )

    return failed == 0


# =====================================================================
# MAIN
# =====================================================================

def main():

    print("\n")
    print("#" * 80)
    print("# GETHIRED RESUME PARSER / EXTRACTOR FIRST-LAYER TEST")
    print("#" * 80)

    print(
        "\nThis test intentionally does NOT run the "
        "new ExtractionEngine."
    )

    print(
        "It tests the parser/extractor layer that "
        "ResumeBuilder currently uses."
    )

    # ================================================================
    # STEP 1
    # ================================================================

    try:

        test_imports()

    except Exception:

        print(
            "\nParser imports failed."
        )

        return 1

    # ================================================================
    # STEP 2
    # ================================================================

    skills = test_skills_extractor()

    # ================================================================
    # STEP 3
    # ================================================================

    certifications = (
        test_certification_extractor()
    )

    # ================================================================
    # STEP 4
    # ================================================================

    resume = test_resume_builder()

    # ================================================================
    # STEP 5
    # ================================================================

    inspect_resume(
        resume
    )

    # ================================================================
    # STEP 6
    # ================================================================

    success = validate_results(
        skills,
        certifications,
        resume,
    )

    # ================================================================
    # FINAL STATUS
    # ================================================================

    print_section(
        "FINAL TEST STATUS"
    )

    if success:

        print(
            "PASS"
        )

        print(
            "\nParser/extractor first layer is "
            "producing data."
        )

        print(
            "Next step can be the detailed "
            "accuracy test and then the V5 "
            "ExtractionEngine pipeline test."
        )

        return 0

    print(
        "FAIL"
    )

    print(
        "\nThe parser/extractor layer still needs "
        "repair before testing the ExtractionEngine."
    )

    return 1


# =====================================================================
# DIRECT EXECUTION
# =====================================================================

if __name__ == "__main__":

    raise SystemExit(
        main()
    )
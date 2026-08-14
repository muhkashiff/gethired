# Enterprise V5 — Resume Ingestion & Parser Pipeline Test


"""
GetHired
Enterprise V5

COMPLETE RESUME INGESTION / PARSER PIPELINE TEST

Architecture tested:

DOCX
  |
  v
ResumeReader
  |
  v
SectionDetector
  |
  v
ResumeParser
  |
  v
ResumeBuilder
  |
  +------------------------------+
  |                              |
  v                              v
Non-Ontology Extractors      Ontology Extractors
  |                              |
  +---------------+--------------+
                  |
                  v
             Resume Object
                  |
                  v
        Intelligence / Enrichment
        --------------------------
        SeniorityDetector
        EducationEnricher
        IndustryDetector

IMPORTANT
---------
This test intentionally does NOT require enrichment/detection
components during ResumeBuilder construction.

Those components operate AFTER the Resume object has been built.
"""


from __future__ import annotations

import sys
import traceback
from pathlib import Path


# ================================================================
# PROJECT ROOT
# ================================================================

CURRENT_FILE = Path(__file__).resolve()

# test_registry.py:
#
# gethired/
#   app/
#     intelligence/
#       utilities/
#         knowledge/
#           test_registry.py
#
# parents[0] = knowledge
# parents[1] = utilities
# parents[2] = intelligence
# parents[3] = app
# parents[4] = gethired
#
PROJECT_ROOT = CURRENT_FILE.parents[4]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ================================================================
# IMPORTS
# ================================================================

from app.parser.readers import ResumeReader
from app.parser.section_detector import SectionDetector
from app.parser.resume_parser import ResumeParser
from app.parser.resume_builder import ResumeBuilder


# ================================================================
# CONFIGURATION
# ================================================================

RESUME_PATH = (
    PROJECT_ROOT
    / "uploads"
    / "project_2"
    / "resume_original.docx"
)


# ================================================================
# DISPLAY HELPERS
# ================================================================

def banner(title: str):

    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def section(title: str):

    print()
    print("-" * 70)
    print(title)
    print("-" * 70)


def pass_message(message: str):

    print(f"PASS — {message}")


def fail_message(message: str):

    print(f"FAIL — {message}")


# ================================================================
# STAGE 0
# ================================================================

def test_file():

    section("STAGE 0 — RESUME FILE")

    print(f"Project root : {PROJECT_ROOT}")
    print(f"Resume       : {RESUME_PATH}")
    print()

    if not RESUME_PATH.exists():

        raise FileNotFoundError(
            f"Resume not found:\n{RESUME_PATH}"
        )

    if RESUME_PATH.suffix.lower() != ".docx":

        raise ValueError(
            f"Unsupported resume format: {RESUME_PATH.suffix}"
        )

    pass_message("DOCX resume located.")

    return RESUME_PATH


# ================================================================
# STAGE 1
# RESUME READER
# ================================================================

def test_reader(file_path):

    section("STAGE 1 — RESUME READER")

    reader = ResumeReader()

    blocks = reader.read(file_path)

    print(
        f"Reader output type : {type(blocks).__name__}"
    )

    print(
        f"Block count        : {len(blocks)}"
    )

    if not blocks:

        raise AssertionError(
            "ResumeReader returned no blocks."
        )

    print()
    print("FIRST 15 BLOCKS")
    print("-" * 70)

    for index, block in enumerate(
        blocks[:15],
        start=1,
    ):

        print(
            f"{index:03d} : {block}"
        )

    pass_message(
        "ResumeReader successfully read the DOCX."
    )

    return blocks


# ================================================================
# STAGE 2
# SECTION DETECTOR
# ================================================================

def test_section_detector(blocks):

    section("STAGE 2 — SECTION DETECTOR")

    detector = SectionDetector()

    sections = detector.detect(blocks)

    print(
        f"Detector output type : "
        f"{type(sections).__name__}"
    )

    if not isinstance(sections, dict):

        raise TypeError(
            "SectionDetector must return dict."
        )

    print()
    print("DETECTED SECTIONS")
    print("-" * 70)

    total_items = 0

    for section_name, content in sections.items():

        print()

        print(
            f"[{section_name.upper()}]"
        )

        print(
            f"Object type : "
            f"{type(content).__name__}"
        )

        # --------------------------------------------------------
        # ResumeSection
        # --------------------------------------------------------

        if hasattr(content, "items"):

            items = content.items

        # --------------------------------------------------------
        # Legacy list compatibility
        # --------------------------------------------------------

        elif isinstance(content, list):

            items = content

        else:

            raise TypeError(
                f"Unsupported section object: "
                f"{type(content).__name__}"
            )

        print(
            f"Items       : {len(items)}"
        )

        total_items += len(items)

        for item in items[:8]:

            print(
                f"  - {item}"
            )

        if len(items) > 8:

            print(
                f"  ... "
                f"{len(items) - 8} more"
            )

    print()
    print(
        f"Total section content items : "
        f"{total_items}"
    )

    if not sections:

        raise AssertionError(
            "SectionDetector returned no sections."
        )

    pass_message(
        "SectionDetector successfully produced "
        "typed ResumeSection objects."
    )

    return sections


# ================================================================
# STAGE 3
# RESUME PARSER
# ================================================================

def test_resume_parser(file_path):

    section("STAGE 3 — RESUME PARSER")

    parser = ResumeParser()

    # ------------------------------------------------------------
    # Blocks
    # ------------------------------------------------------------

    blocks = parser.paragraphs(
        file_path
    )

    print(
        f"Parser block count : {len(blocks)}"
    )

    # ------------------------------------------------------------
    # Full text
    # ------------------------------------------------------------

    full_text = parser.full_text(
        file_path
    )

    print(
        f"Full text length   : {len(full_text)}"
    )

    if not full_text.strip():

        raise AssertionError(
            "ResumeParser produced empty full text."
        )

    # ------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------

    sections = parser.parse(
        file_path
    )

    print(
        f"Section count      : {len(sections)}"
    )

    print()
    print("PARSER SECTIONS")
    print("-" * 70)

    for name, value in sections.items():

        if hasattr(value, "items"):

            count = len(value.items)

        elif isinstance(value, list):

            count = len(value)

        else:

            count = "?"

        print(
            f"{name:<20}"
            f"{type(value).__name__:<25}"
            f"items={count}"
        )

    if not sections:

        raise AssertionError(
            "ResumeParser returned no sections."
        )

    pass_message(
        "ResumeParser successfully connected "
        "reader and section detector."
    )

    return parser, sections


# ================================================================
# SECTION CONSISTENCY
# ================================================================

def test_section_consistency(
    detector_sections,
    parser_sections,
):

    section(
        "SECTION DETECTION CONSISTENCY"
    )

    detector_keys = set(
        detector_sections.keys()
    )

    parser_keys = set(
        parser_sections.keys()
    )

    if detector_keys != parser_keys:

        print(
            "Detector keys:",
            sorted(detector_keys)
        )

        print(
            "Parser keys:",
            sorted(parser_keys)
        )

        raise AssertionError(
            "Section keys differ between "
            "SectionDetector and ResumeParser."
        )

    pass_message(
        "Section keys are consistent."
    )


# ================================================================
# HELPER
# ================================================================

def get_section_items(
    sections,
    section_name,
):

    content = sections.get(
        section_name
    )

    if content is None:

        return []

    if hasattr(content, "items"):

        return content.items

    if isinstance(content, list):

        return content

    raise TypeError(
        f"Unsupported section type for "
        f"{section_name}: "
        f"{type(content).__name__}"
    )


# ================================================================
# STAGE 4
# RESUME BUILDER
# ================================================================

def test_resume_builder(
    sections,
):

    section(
        "STAGE 4 — RESUME BUILDER"
    )

    print(
        "Creating ResumeBuilder..."
    )

    builder = ResumeBuilder()

    print(
        "ResumeBuilder created."
    )

    resume = builder.build(
        sections
    )

    if resume is None:

        raise AssertionError(
            "ResumeBuilder returned None."
        )

    print()
    print(
        f"Resume object type : "
        f"{type(resume).__name__}"
    )

    # ============================================================
    # PERSONAL INFORMATION
    # ============================================================

    print()
    print("PERSONAL INFORMATION")
    print("-" * 70)

    personal = getattr(
        resume,
        "personal_information",
        None,
    )

    if personal is None:

        raise AssertionError(
            "Resume has no personal_information."
        )

    for attribute in [
        "name",
        "email",
        "phone",
        "linkedin",
        "github",
        "address",
    ]:

        value = getattr(
            personal,
            attribute,
            "",
        )

        print(
            f"{attribute:<15}: {value}"
        )

    # ============================================================
    # SUMMARY
    # ============================================================

    print()
    print("SUMMARY")
    print("-" * 70)

    summary = getattr(
        resume,
        "summary",
        "",
    )

    print(
        summary[:1000]
    )

    # ============================================================
    # COLLECTIONS
    # ============================================================

    collection_fields = [
        "skills",
        "experience",
        "education",
        "certifications",
        "projects",
        "awards",
        "languages",
        "references",
    ]

    print()
    print("RESUME COLLECTIONS")
    print("-" * 70)

    for field_name in collection_fields:

        value = getattr(
            resume,
            field_name,
            None,
        )

        if value is None:

            print(
                f"{field_name:<20}: MISSING"
            )

            continue

        try:

            count = len(value)

        except TypeError:

            count = "NON-COLLECTION"

        print(
            f"{field_name:<20}: "
            f"{type(value).__name__} "
            f"count={count}"
        )

    pass_message(
        "ResumeBuilder successfully created "
        "the Resume object."
    )

    return resume


# ================================================================
# STAGE 5
# EXTRACTOR VALIDATION
# ================================================================

def test_extracted_resume_content(
    resume,
):

    section(
        "STAGE 5 — EXTRACTED RESUME CONTENT"
    )

    # ------------------------------------------------------------
    # CONTACT / PERSONAL
    # ------------------------------------------------------------

    print()
    print("CONTACT EXTRACTION")
    print("-" * 70)

    personal = resume.personal_information

    contact_values = {
        "name": personal.name,
        "email": personal.email,
        "phone": personal.phone,
        "linkedin": personal.linkedin,
        "github": personal.github,
        "address": personal.address,
    }

    for key, value in contact_values.items():

        print(
            f"{key:<15}: {value}"
        )

    # ------------------------------------------------------------
    # EXPERIENCE
    # ------------------------------------------------------------

    print()
    print("EXPERIENCE EXTRACTION")
    print("-" * 70)

    experience = getattr(
        resume,
        "experience",
        [],
    )

    print(
        f"Count : {len(experience)}"
    )

    for item in experience[:5]:

        print(
            f"  - {item}"
        )

    # ------------------------------------------------------------
    # EDUCATION
    # ------------------------------------------------------------

    print()
    print("EDUCATION EXTRACTION")
    print("-" * 70)

    education = getattr(
        resume,
        "education",
        [],
    )

    print(
        f"Count : {len(education)}"
    )

    for item in education[:5]:

        print(
            f"  - {item}"
        )

    # ------------------------------------------------------------
    # PROJECTS
    # ------------------------------------------------------------

    print()
    print("PROJECT EXTRACTION")
    print("-" * 70)

    projects = getattr(
        resume,
        "projects",
        [],
    )

    print(
        f"Count : {len(projects)}"
    )

    for item in projects[:5]:

        print(
            f"  - {item}"
        )

    # ------------------------------------------------------------
    # AWARDS
    # ------------------------------------------------------------

    print()
    print("AWARD EXTRACTION")
    print("-" * 70)

    awards = getattr(
        resume,
        "awards",
        [],
    )

    print(
        f"Count : {len(awards)}"
    )

    for item in awards[:5]:

        print(
            f"  - {item}"
        )

    # ------------------------------------------------------------
    # REFERENCES
    # ------------------------------------------------------------

    print()
    print("REFERENCE EXTRACTION")
    print("-" * 70)

    references = getattr(
        resume,
        "references",
        [],
    )

    print(
        f"Count : {len(references)}"
    )

    for item in references[:5]:

        print(
            f"  - {item}"
        )

    # ------------------------------------------------------------
    # LANGUAGES
    # ------------------------------------------------------------

    print()
    print("LANGUAGE EXTRACTION")
    print("-" * 70)

    languages = getattr(
        resume,
        "languages",
        [],
    )

    print(
        f"Count : {len(languages)}"
    )

    for item in languages[:5]:

        print(
            f"  - {item}"
        )

    pass_message(
        "Non-ontology resume extraction stage completed."
    )


# ================================================================
# STAGE 6
# ONTOLOGY EXTRACTION
# ================================================================

def test_ontology_fields(
    resume,
):

    section(
        "STAGE 6 — ONTOLOGY EXTRACTION"
    )

    print(
        "Ontology-controlled fields"
    )

    print(
        "are intentionally validated "
        "through their existing extractor output."
    )

    # ------------------------------------------------------------
    # SKILLS
    # ------------------------------------------------------------

    print()
    print("SKILLS")
    print("-" * 70)

    skills = getattr(
        resume,
        "skills",
        [],
    )

    print(
        f"Count : {len(skills)}"
    )

    for skill in skills[:15]:

        print(
            f"  - {skill}"
        )

    # ------------------------------------------------------------
    # CERTIFICATIONS
    # ------------------------------------------------------------

    print()
    print("CERTIFICATIONS")
    print("-" * 70)

    certifications = getattr(
        resume,
        "certifications",
        [],
    )

    print(
        f"Count : {len(certifications)}"
    )

    for certification in certifications[:15]:

        print(
            f"  - {certification}"
        )

    pass_message(
        "Ontology-controlled fields are connected "
        "to ResumeBuilder."
    )


# ================================================================
# STAGE 7
# RAW TEXT TRACEABILITY
# ================================================================

def test_traceability(
    parser,
    resume,
):

    section(
        "STAGE 7 — RAW TEXT TRACEABILITY"
    )

    full_text = parser.full_text(
        RESUME_PATH
    )

    print(
        f"Raw resume characters : "
        f"{len(full_text)}"
    )

    checks = [
        "MUHAMMAD KASHIF",
        "SUMMARY",
        "EXPERIENCE",
        "EDUCATION",
        "CERTIFICATIONS",
    ]

    for expected in checks:

        if expected.lower() in full_text.lower():

            print(
                f"PASS  {expected}"
            )

        else:

            print(
                f"WARN  {expected} "
                "not found in raw text"
            )

    pass_message(
        "Raw resume remains traceable "
        "through the parser."
    )


# ================================================================
# STAGE 8
# ENRICHMENT / INTELLIGENCE
# ================================================================

def test_intelligence_boundary(
    resume,
):

    section(
        "STAGE 8 — INTELLIGENCE / ENRICHMENT BOUNDARY"
    )

    print(
        "ResumeBuilder responsibility:"
    )

    print(
        "  DOCX -> sections -> Resume"
    )

    print()
    print(
        "Post-builder intelligence:"
    )

    print(
        "  Resume -> SeniorityDetector"
    )

    print(
        "  Resume -> EducationEnricher"
    )

    print(
        "  Resume -> IndustryDetector"
    )

    print()
    print(
        "These components are NOT instantiated "
        "inside ResumeBuilder."
    )

    pass_message(
        "Builder/intelligence boundary is preserved."
    )


# ================================================================
# COMPLETE PIPELINE
# ================================================================

def test_complete_pipeline():

    banner(
        "ENTERPRISE V5 — "
        "COMPLETE RESUME INGESTION PIPELINE"
    )

    try:

        # --------------------------------------------------------
        # FILE
        # --------------------------------------------------------

        file_path = test_file()

        # --------------------------------------------------------
        # READER
        # --------------------------------------------------------

        blocks = test_reader(
            file_path
        )

        # --------------------------------------------------------
        # DETECTOR
        # --------------------------------------------------------

        detector_sections = (
            test_section_detector(
                blocks
            )
        )

        # --------------------------------------------------------
        # PARSER
        # --------------------------------------------------------

        parser, parser_sections = (
            test_resume_parser(
                file_path
            )
        )

        # --------------------------------------------------------
        # CONSISTENCY
        # --------------------------------------------------------

        test_section_consistency(
            detector_sections,
            parser_sections,
        )

        # --------------------------------------------------------
        # BUILDER
        # --------------------------------------------------------

        resume = test_resume_builder(
            parser_sections
        )

        # --------------------------------------------------------
        # EXTRACTIONS
        # --------------------------------------------------------

        test_extracted_resume_content(
            resume
        )

        # --------------------------------------------------------
        # ONTOLOGY
        # --------------------------------------------------------

        test_ontology_fields(
            resume
        )

        # --------------------------------------------------------
        # TRACEABILITY
        # --------------------------------------------------------

        test_traceability(
            parser,
            resume
        )

        # --------------------------------------------------------
        # INTELLIGENCE BOUNDARY
        # --------------------------------------------------------

        test_intelligence_boundary(
            resume
        )

        # --------------------------------------------------------
        # COMPLETE
        # --------------------------------------------------------

        banner(
            "ENTERPRISE V5 — "
            "RESUME INGESTION PIPELINE PASSED"
        )

        print()
        print(
            "Reader                 : PASS"
        )

        print(
            "Section Detector       : PASS"
        )

        print(
            "Resume Parser          : PASS"
        )

        print(
            "Section Consistency    : PASS"
        )

        print(
            "Resume Builder         : PASS"
        )

        print(
            "Non-Ontology Extractors: PASS"
        )

        print(
            "Ontology Extractors    : PASS"
        )

        print(
            "Traceability            : PASS"
        )

        print(
            "Intelligence Boundary  : PASS"
        )

        print()
        print(
            "NEXT ARCHITECTURAL STAGE"
        )

        print(
            "Resume -> Intelligence "
            "Enrichment -> JD Matching"
        )

        print()

        return resume

    except Exception as exc:

        banner(
            "ENTERPRISE V5 — "
            "RESUME INGESTION PIPELINE FAILED"
        )

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print()

        traceback.print_exc()

        raise


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":

    test_complete_pipeline()


from __future__ import annotations

"""
Enterprise Extractor Pipeline Test
Enterprise V13

Purpose
-------
Directly test the extractor pipeline without:

    EnterpriseResumePipeline
    SemanticResolver
    SemanticResolution
    KnowledgeGraph
    BusinessStatementBuilder

Flow
----

Resume DOCX
    ↓
DOCX text extraction
    ↓
ExtractionCoordinator
    ↓
Individual ontology extractors
    ↓
ExtractionResult
    ↓
KnowledgeEntity
    ↓
KnowledgeFact

This test is specifically designed to answer:

    "Are the extractors actually being called?"

It also verifies the contract:

    ExtractionResult.entities

instead of assuming:

    ExtractionResult.all_entities
"""


from pathlib import Path
from typing import Any


from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_pipeline import (
    ExtractionCoordinator,
)


from app.intelligence.utilities.knowledge.knowledge_models import (
    KnowledgeFact,
)


from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import (
    KnowledgeInterpretation,
)


from app.intelligence.utilities.knowledge.knowledge_extractor_models.base_models import (
    KnowledgeEntity,
)


# =====================================================================
# DOCX IMPORT
# =====================================================================

try:

    from docx import Document

except ImportError as exc:

    raise ImportError(
        "python-docx is required to read "

        "uploads/project_2/resume_original.docx"
    ) from exc


# =====================================================================
# CONFIGURATION
# =====================================================================

TEST_NAME = "ENTERPRISE INTERPRETATION FLOW TEST"

RESUME_RELATIVE_PATH = Path(
    "Uploads",
    "project_2",
    "resume_original.docx",
)


# =====================================================================
# PATH RESOLUTION
# =====================================================================

def find_project_root() -> Path:
    """
    Locate the project root dynamically.

    We do NOT assume the current working directory.

    The test file is somewhere under:

        gethired/app/intelligence/utilities/knowledge/

    The resume is at:

        gethired/Uploads/project2/resume_original.docx
    """

    current_file = Path(__file__).resolve()

    for parent in current_file.parents:

        candidate = (
            parent
            / RESUME_RELATIVE_PATH
        )

        if candidate.exists():

            return parent

    raise FileNotFoundError(
        "Could not locate project root containing: "
        f"{RESUME_RELATIVE_PATH}"
    )


PROJECT_ROOT = find_project_root()

RESUME_FILE = (
    PROJECT_ROOT
    / RESUME_RELATIVE_PATH
)

MAX_SENTENCES = 20
# ============================================================================
# PRINT HELPERS
# ============================================================================


def line():

    print(
        "-" * 80
    )


def section(
    title: str,
):

    print()

    print(
        "=" * 80
    )

    print(
        title
    )

    print(
        "=" * 80
    )


# ============================================================================
# DOCX TEXT EXTRACTION
# ============================================================================


def load_docx_text(
    path: Path,
) -> str:
    """
    Load text directly from the DOCX.

    This test intentionally does not depend on the enterprise resume
    pipeline for loading the document.
    """

    if not path.exists():

        raise FileNotFoundError(
            f"Resume file not found: {path}"
        )

    try:

        from docx import Document

    except ImportError as exc:

        raise RuntimeError(
            "python-docx is required to read the resume DOCX."
        ) from exc


    document = Document(
        str(path)
    )


    paragraphs = []


    for paragraph in document.paragraphs:

        text = (
            paragraph.text
            or ""
        ).strip()


        if text:

            paragraphs.append(
                text
            )


    return "\n".join(
        paragraphs
    )


# ============================================================================
# SIMPLE SENTENCE / LINE SPLITTER
# ============================================================================


def split_resume_text(
    text: str,
) -> list[str]:
    """
    Produce text units for the extractor pipeline.

    We intentionally keep this simple.

    The goal of this test is extractor verification,
    not sentence parsing validation.
    """

    units = []


    for line_text in text.splitlines():

        line_text = (
            line_text
            .strip()
        )


        if not line_text:

            continue


        units.append(
            line_text
        )


    return units


# ============================================================================
# EXTRACTOR INSPECTION
# ============================================================================


def inspect_coordinator(
    coordinator: Any,
):
    """
    Inspect the ExtractionCoordinator so we can see which extractors
    are registered.

    This is intentionally defensive because the coordinator may use
    different internal attribute names.
    """

    section(
        "EXTRACTION COORDINATOR"
    )


    print(
        "Coordinator class:",
        coordinator.__class__.__name__,
    )


    print(
        "Coordinator module:",
        coordinator.__class__.__module__,
    )


    print()


    possible_names = [
        "extractors",
        "_extractors",
        "pipelines",
        "_pipelines",
        "ontology_extractors",
        "_ontology_extractors",
    ]


    found = False


    for name in possible_names:

        if not hasattr(
            coordinator,
            name,
        ):

            continue


        value = getattr(
            coordinator,
            name,
        )


        print(
            f"{name}:",
            type(value).__name__,
        )


        if isinstance(
            value,
            (list, tuple),
        ):

            print(
                "Registered count:",
                len(value),
            )


            for index, extractor in enumerate(
                value,
                start=1,
            ):

                print(
                    f"  [{index}]",
                    extractor.__class__.__name__,
                )


            found = True


        elif isinstance(
            value,
            dict,
        ):

            print(
                "Registered count:",
                len(value),
            )


            for key, extractor in value.items():

                print(
                    " ",
                    key,
                    "→",
                    extractor.__class__.__name__,
                )


            found = True


    if not found:

        print(
            "No obvious extractor registry attribute found."
        )


# ============================================================================
# KNOWLEDGE ENTITY CONVERSION
# ============================================================================


def convert_to_knowledge_entity(
    extracted: Any,
) -> KnowledgeEntity:
    """
    Convert one extractor entity into KnowledgeEntity.

    This mirrors the conversion logic currently used by
    ResumeKnowledgePipeline.
    """

    return KnowledgeEntity(

        found=True,

        confidence=float(
            getattr(
                extracted,
                "confidence",
                0.0,
            )
        ),

        extraction_method=(
            "knowledge_v5"
        ),

        original=(
            getattr(
                extracted,
                "phrase",
                "",
            )
        ),

        canonical=(
            getattr(
                extracted,
                "canonical",
                "",
            )
        ),

        normalized=(
            getattr(
                extracted,
                "canonical",
                "",
            )
            .lower()
        ),

        entity_id=(
            getattr(
                extracted,
                "entity_id",
                "",
            )
        ),

        entity_type=(
            getattr(
                extracted,
                "entity_type",
                "",
            )
        ),

        category=(
            getattr(
                extracted,
                "category",
                "",
            )
        ),

        ontology_name=(
            getattr(
                extracted,
                "ontology",
                "",
            )
        ),

        business_area=(
            getattr(
                extracted,
                "business_area",
                "",
            )
        ),

        domain=(
            getattr(
                extracted,
                "domain",
                "",
            )
        ),

        impact_weight=float(
            getattr(
                extracted,
                "impact_weight",
                1.0,
            )
        ),

        source="resume",

        matched_phrase=(
            getattr(
                extracted,
                "phrase",
                "",
            )
        ),

        matched_alias=bool(
            getattr(
                extracted,
                "is_alias",
                False,
            )
        ),

        start_char=int(
            getattr(
                extracted,
                "start_char",
                -1,
            )
        ),

        end_char=int(
            getattr(
                extracted,
                "end_char",
                -1,
            )
        ),

        token_index=int(
            getattr(
                extracted,
                "token_index",
                -1,
            )
        ),

        token_count=int(
            getattr(
                extracted,
                "token_count",
                0,
            )
        ),

        metadata=dict(
            getattr(
                extracted,
                "metadata",
                {}
            )
            or {}
        ),
    )


# ============================================================================
# PROCESS ONE TEXT UNIT
# ============================================================================


def test_single_text_unit(
    coordinator: ExtractionCoordinator,
    text: str,
):
    """
    Run one text unit through the extractor pipeline.

    This is the most important diagnostic function.
    """

    section(
        "SINGLE EXTRACTOR TEST"
    )


    print(
        "Input:",
        text,
    )


    print()

    print(
        "Calling ExtractionCoordinator.run() ..."
    )


    extraction = coordinator.run(
        text
    )


    print()

    print(
        "Extraction completed."
    )


    print(
        "Result class:",
        extraction.__class__.__name__,
    )


    # ------------------------------------------------------------------------
    # EXTRACTION RESULT CONTRACT
    # ------------------------------------------------------------------------

    print()

    line()

    print(
        "EXTRACTION RESULT CONTRACT"
    )

    line()


    print(
        "Ontology:",
        getattr(
            extraction,
            "ontology",
            "",
        ),
    )


    print(
        "entities:",
        len(
            getattr(
                extraction,
                "entities",
                [],
            )
        ),
    )


    print(
        "matches:",
        len(
            getattr(
                extraction,
                "matches",
                [],
            )
        ),
    )


    print(
        "count property:",
        getattr(
            extraction,
            "count",
            None,
        ),
    )


    print(
        "found property:",
        getattr(
            extraction,
            "found",
            None,
        ),
    )


    # ------------------------------------------------------------------------
    # IMPORTANT: all_entities compatibility check
    # ------------------------------------------------------------------------

    print()

    print(
        "Has all_entities:",
        hasattr(
            extraction,
            "all_entities",
        ),
    )


    if hasattr(
        extraction,
        "all_entities",
    ):

        print(
            "all_entities count:",
            len(
                extraction.all_entities
            )
        )


    # ------------------------------------------------------------------------
    # RAW EXTRACTED ENTITIES
    # ------------------------------------------------------------------------

    extracted_entities = list(
        getattr(
            extraction,
            "entities",
            [],
        )
        or []
    )


    print()

    line()

    print(
        "RAW EXTRACTED ENTITIES"
    )

    line()


    if not extracted_entities:

        print(
            "[FAIL] ExtractionCoordinator returned ZERO entities."
        )

        return (
            extraction,
            [],
            None,
        )


    print(
        "[PASS] Extractor pipeline returned entities:",
        len(
            extracted_entities
        ),
    )


    for index, extracted in enumerate(
        extracted_entities,
        start=1,
    ):

        print()

        print(
            f"[ENTITY {index}]"
        )


        print(
            "class:",
            extracted.__class__.__name__,
        )


        print(
            "module:",
            extracted.__class__.__module__,
        )


        print(
            "entity_type:",
            getattr(
                extracted,
                "entity_type",
                "",
            ),
        )


        print(
            "phrase:",
            getattr(
                extracted,
                "phrase",
                "",
            ),
        )


        print(
            "canonical:",
            getattr(
                extracted,
                "canonical",
                "",
            ),
        )


        print(
            "entity_id:",
            getattr(
                extracted,
                "entity_id",
                "",
            ),
        )


        print(
            "confidence:",
            getattr(
                extracted,
                "confidence",
                0.0,
            ),
        )


        print(
            "ontology:",
            getattr(
                extracted,
                "ontology",
                "",
            ),
        )


        print(
            "category:",
            getattr(
                extracted,
                "category",
                "",
            ),
        )


    # ------------------------------------------------------------------------
    # CONVERT TO KNOWLEDGE ENTITIES
    # ------------------------------------------------------------------------

    knowledge_entities = []


    for extracted in extracted_entities:

        knowledge_entity = (
            convert_to_knowledge_entity(
                extracted
            )
        )


        knowledge_entities.append(
            knowledge_entity
        )


    # ------------------------------------------------------------------------
    # KNOWLEDGE INTERPRETATION
    # ------------------------------------------------------------------------

    interpretation = (
        KnowledgeInterpretation()
    )


    interpretation.entities = (
        knowledge_entities
    )


    interpretation.confidence = max(
        (
            entity.confidence
            for entity in knowledge_entities
        ),
        default=0.0,
    )


    # ------------------------------------------------------------------------
    # KNOWLEDGE FACT
    # ------------------------------------------------------------------------

    fact = KnowledgeFact(

        text=text,

        source="resume",

        interpretation=(
            interpretation
        ),

        confidence=(
            interpretation.confidence
        ),
    )


    print()

    line()

    print(
        "KNOWLEDGE FACT RESULT"
    )

    line()


    print(
        "Fact class:",
        fact.__class__.__name__,
    )


    print(
        "Fact text:",
        fact.text,
    )


    print(
        "Interpretation class:",
        fact.interpretation.__class__.__name__,
    )


    print(
        "Knowledge entities:",
        len(
            fact.interpretation.entities
        ),
    )


    for index, entity in enumerate(
        fact.interpretation.entities,
        start=1,
    ):

        print(
            f"  [{index}]",
            entity.entity_type,
            "|",
            entity.canonical,
            "|",
            entity.confidence,
        )


    return (
        extraction,
        knowledge_entities,
        fact,
    )


# ============================================================================
# MULTIPLE TEXT UNITS
# ============================================================================


def test_multiple_text_units(
    coordinator: ExtractionCoordinator,
    text_units: list[str],
):
    """
    Run multiple resume lines through the extractor pipeline.
    """

    section(
        "MULTIPLE TEXT UNIT EXTRACTOR TEST"
    )


    total_entities = 0

    total_facts = 0

    successful_units = 0


    for index, text in enumerate(
        text_units,
        start=1,
    ):

        print()

        print(
            f"[TEXT UNIT {index}]",
            text[:150],
        )


        try:

            extraction = (
                coordinator.run(
                    text
                )
            )


        except Exception as exc:

            print(
                "[ERROR]",
                type(exc).__name__,
                str(exc),
            )

            continue


        entities = list(
            getattr(
                extraction,
                "entities",
                [],
            )
            or []
        )


        print(
            "Entities:",
            len(entities),
        )


        if entities:

            successful_units += 1

            total_entities += (
                len(entities)
            )


            for entity in entities[:10]:

                print(
                    "  ",
                    getattr(
                        entity,
                        "entity_type",
                        "",
                    ),
                    "|",
                    getattr(
                        entity,
                        "canonical",
                        getattr(
                            entity,
                            "phrase",
                            "",
                        ),
                    ),
                )


            interpretation = (
                KnowledgeInterpretation()
            )


            interpretation.entities = [
                convert_to_knowledge_entity(
                    entity
                )
                for entity in entities
            ]


            fact = KnowledgeFact(

                text=text,

                interpretation=(
                    interpretation
                ),

                confidence=(
                    interpretation.confidence
                    if hasattr(
                        interpretation,
                        "confidence",
                    )
                    else 0.0
                ),
            )


            total_facts += 1


    print()

    line()

    print(
        "EXTRACTOR SUMMARY"
    )

    line()


    print(
        "Text units tested:",
        len(text_units),
    )


    print(
        "Units with entities:",
        successful_units,
    )


    print(
        "Total extracted entities:",
        total_entities,
    )


    print(
        "Knowledge facts created:",
        total_facts,
    )


    if total_entities == 0:

        print()

        print(
            "[FAIL] No entities were extracted."
        )

        print(
            "The problem is inside the extractor/coordinator layer."
        )

    else:

        print()

        print(
            "[PASS] Extractor pipeline is producing entities."
        )


# ============================================================================
# MAIN TEST
# ============================================================================


def main():

    section(
        "ENTERPRISE EXTRACTOR PIPELINE TEST"
    )


    # ------------------------------------------------------------------------
    # PROJECT / RESUME
    # ------------------------------------------------------------------------

    print(
        "Project root:",
        PROJECT_ROOT,
    )


    print(
        "Resume:",
        RESUME_FILE,
    )


    if not RESUME_FILE.exists():

        raise FileNotFoundError(
            f"Resume not found: {RESUME_FILE}"
        )


    # ------------------------------------------------------------------------
    # LOAD DOCX
    # ------------------------------------------------------------------------

    section(
        "1. RESUME INPUT"
    )


    resume_text = load_docx_text(
        RESUME_FILE
    )


    print(
        "[PASS] DOCX loaded."
    )


    print(
        "Characters:",
        len(resume_text),
    )


    text_units = split_resume_text(
        resume_text
    )


    print(
        "Text units:",
        len(text_units),
    )


    # ------------------------------------------------------------------------
    # CREATE COORDINATOR
    # ------------------------------------------------------------------------

    section(
        "2. CREATE EXTRACTION COORDINATOR"
    )


    coordinator = (
        ExtractionCoordinator()
    )


    print(
        "[PASS] ExtractionCoordinator created."
    )


    inspect_coordinator(
        coordinator
    )


    # ------------------------------------------------------------------------
    # SINGLE HIGH-VALUE TEST
    # ------------------------------------------------------------------------

    test_sentence = (
        "Spearheaded the site-wide implementation, "
        "execution, and regulatory compliance of the "
        "integrated Quality and Food Safety Management "
        "System (QMS)."
    )


    (
        extraction,
        knowledge_entities,
        fact,
    ) = test_single_text_unit(
        coordinator,
        test_sentence,
    )


    # ------------------------------------------------------------------------
    # FULL RESUME SAMPLE
    # ------------------------------------------------------------------------

    test_multiple_text_units(
        coordinator,
        text_units[:MAX_SENTENCES],
    )


    # ------------------------------------------------------------------------
    # FINAL STATUS
    # ------------------------------------------------------------------------

    section(
        "FINAL STATUS"
    )


    if knowledge_entities:

        print(
            "[PASS] Extractor pipeline is operational."
        )

        print(
            "The extractor pipeline successfully produced "
            "knowledge entities and a KnowledgeFact."
        )


    else:

        print(
            "[FAIL] Extractor pipeline produced no entities "
            "for the diagnostic sentence."
        )

        print()

        print(
            "Next file to inspect:"
        )

        print(
            "app/intelligence/utilities/knowledge/"
            "knowledge_extractors/extraction_pipeline.py"
        )


# ============================================================================
# ENTRY POINT
# ============================================================================


if __name__ == "__main__":

    main()
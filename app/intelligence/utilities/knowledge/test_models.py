"""
Enterprise Reusable Knowledge Extractor Test
Enterprise V5

Purpose
-------
Generic test harness for ontology extractors.

Flow:

Repository
    ↓
KnowledgeV5Pipeline
    ↓
Extractor
    ↓
ExtractionRequest
    ↓
ExtractionResult
    ↓
Knowledge Objects

This test is intentionally reusable.

To test another extractor, change:

    EXTRACTOR_CLASS
    ENTITY_CLASS
    ONTOLOGY
    ENTITY_TYPE
    TEST_CASES
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


# ============================================================================
# PROJECT ROOT
# ============================================================================

ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ============================================================================
# IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.repository_v5.repository import (
    Repository,
)

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
    ExtractionRequest,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.technology_extractor import (
    TechnologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.technology_models import (
    Technology,
)


# ============================================================================
# CONFIGURATION
# ============================================================================

ONTOLOGY = "technologies"

ENTITY_TYPE = "technologie"

EXTRACTOR_CLASS = TechnologyExtractor

ENTITY_CLASS = Technology


# ============================================================================
# TEST CASES
# ============================================================================

TEST_CASES = [

    # ------------------------------------------------------------------------
    # CANONICAL TECHNOLOGIES
    # ------------------------------------------------------------------------

    {
        "sentence": "Demonstrated strong experience in Python.",
        "expected": {
            "TECH_PYTHON",
        },
    },

    {
        "sentence": "Demonstrated strong experience in SQL.",
        "expected": {
            "TECH_SQL",
        },
    },

    {
        "sentence": "Demonstrated strong experience in PostgreSQL.",
        "expected": {
            "TECH_POSTGRESQL",
        },
    },

    {
        "sentence": "Demonstrated strong experience in Tableau.",
        "expected": {
            "TECH_TABLEAU",
        },
    },

    {
        "sentence": "Demonstrated strong experience in Docker.",
        "expected": {
            "TECH_DOCKER",
        },
    },

    {
        "sentence": "Demonstrated strong experience in Power BI.",
        "expected": {
            "TECH_POWER_BI",
        },
    },

    {
        "sentence": "Demonstrated strong experience in Excel.",
        "expected": {
            "TECH_EXCEL",
        },
    },

    {
        "sentence": "Demonstrated strong experience in Azure.",
        "expected": {
            "TECH_AZURE",
        },
    },


    # ------------------------------------------------------------------------
    # ALIASES
    # ------------------------------------------------------------------------

    {
        "sentence": "Experienced in python programming.",
        "expected": {
            "TECH_PYTHON",
        },
    },

    {
        "sentence": "Created dashboards using powerbi.",
        "expected": {
            "TECH_POWER_BI",
        },
    },

    {
        "sentence": "Advanced knowledge of ms excel.",
        "expected": {
            "TECH_EXCEL",
        },
    },

    {
        "sentence": "Experienced with postgres databases.",
        "expected": {
            "TECH_POSTGRESQL",
        },
    },

    {
        "sentence": "Experienced with sql server.",
        "expected": {
            "TECH_SQLSERVER",
        },
    },

    {
        "sentence": "Experienced with mssql.",
        "expected": {
            "TECH_SQLSERVER",
        },
    },


    # ------------------------------------------------------------------------
    # OTHER TECHNOLOGIES
    # ------------------------------------------------------------------------

    {
        "sentence": "Developed APIs using FastAPI.",
        "expected": {
            "TECH_FASTAPI",
        },
    },

    {
        "sentence": "Built web applications using Flask.",
        "expected": {
            "TECH_FLASK",
        },
    },

    {
        "sentence": "Performed data analysis using Pandas.",
        "expected": {
            "TECH_PANDAS",
        },
    },

    {
        "sentence": "Performed numerical analysis using NumPy.",
        "expected": {
            "TECH_NUMPY",
        },
    },

    {
        "sentence": "Maintained projects on GitHub.",
        "expected": {
            "TECH_GITHUB",
        },
    },

    {
        "sentence": "Used Jupyter Notebook for data analysis.",
        "expected": {
            "TECH_JUPYTER",
        },
    },


    # ------------------------------------------------------------------------
    # MULTIPLE ENTITIES
    # ------------------------------------------------------------------------

    {
        "sentence": (
            "Experienced with Python, PostgreSQL, "
            "Docker and Power BI."
        ),
        "expected": {
            "TECH_PYTHON",
            "TECH_POSTGRESQL",
            "TECH_DOCKER",
            "TECH_POWER_BI",
        },
    },
]


# ============================================================================
# DISPLAY HELPERS
# ============================================================================

def print_header(title: str) -> None:

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def print_entity(entity: Any) -> None:

    print(
        f"  - "
        f"{getattr(entity, 'canonical', '')} "
        f"[{getattr(entity, 'entity_id', '')}] "
        f"phrase={getattr(entity, 'matched_phrase', '')!r} "
        f"confidence={getattr(entity, 'confidence', None)} "
        f"alias={getattr(entity, 'is_alias', None)}"
    )


# ============================================================================
# RESULT NORMALIZATION
# ============================================================================

def get_entities(result: Any) -> list[Any]:
    """
    Normalize ExtractionResult into a list of knowledge entities.

    Expected Enterprise V5 structure:

        ExtractionResult.entities

    This helper also supports lists for defensive compatibility.
    """

    if result is None:
        return []

    # Enterprise ExtractionResult
    if hasattr(result, "entities"):

        entities = result.entities

        if entities is None:
            return []

        return list(entities)

    # Plain list
    if isinstance(result, list):
        return result

    # Tuple
    if isinstance(result, tuple):
        return list(result)

    # Single entity fallback
    if isinstance(result, ENTITY_CLASS):
        return [result]

    return []


# ============================================================================
# VALIDATE KNOWLEDGE OBJECT
# ============================================================================

def validate_entity(entity: Any) -> list[str]:
    """
    Validate the common extractor contract.

    Returns a list of errors.
    """

    errors: list[str] = []

    if not isinstance(entity, ENTITY_CLASS):

        errors.append(
            f"wrong object type: {type(entity)}"
        )

        return errors

    if not getattr(entity, "found", False):

        errors.append(
            "found != True"
        )

    if not getattr(entity, "entity_id", None):

        errors.append(
            "entity_id is empty"
        )

    if not getattr(entity, "canonical", None):

        errors.append(
            "canonical is empty"
        )

    if not getattr(entity, "matched_phrase", None):

        errors.append(
            "matched_phrase is empty"
        )

    confidence = getattr(
        entity,
        "confidence",
        None,
    )

    if confidence is None:

        errors.append(
            "confidence is None"
        )

    elif not 0.0 <= confidence <= 1.0:

        errors.append(
            f"invalid confidence: {confidence}"
        )

    return errors


# ============================================================================
# DIRECT PIPELINE TEST
# ============================================================================

def test_pipeline(
    pipeline: KnowledgeV5Pipeline,
) -> bool:

    print_header(
        "DIRECT PIPELINE TEST"
    )

    sentence = (
        "Demonstrated strong experience in Python."
    )

    print()
    print(
        f"Sentence: {sentence}"
    )

    try:

        matches = pipeline.run(
            ONTOLOGY,
            sentence,
        )

    except Exception as error:

        print()
        print("❌ PIPELINE ERROR")

        print(
            f"{type(error).__name__}: {error}"
        )

        return False

    print(
        f"Pipeline matches: {len(matches)}"
    )

    if not matches:

        print()
        print(
            "❌ PIPELINE FAILED: "
            "No matches produced."
        )

        return False

    for match in matches:

        print()
        print(
            f"phrase        = "
            f"{match.phrase!r}"
        )

        print(
            f"canonical     = "
            f"{match.entity.canonical}"
        )

        print(
            f"entity_id     = "
            f"{match.entity.entity_id}"
        )

        print(
            f"entity_type   = "
            f"{match.entity.entity_type}"
        )

        print(
            f"confidence    = "
            f"{match.confidence}"
        )

        print(
            f"matched_alias = "
            f"{match.matched_alias!r}"
        )

        print(
            f"is_alias      = "
            f"{match.is_alias}"
        )

    print()
    print(
        "✅ PIPELINE WORKS"
    )

    return True


# ============================================================================
# EXTRACTOR TEST
# ============================================================================

def test_extractor(
    extractor: Any,
) -> tuple[int, int]:

    print_header(
        "EXTRACTOR TESTS"
    )

    passed = 0
    failed = 0

    for index, test_case in enumerate(
        TEST_CASES,
        start=1,
    ):

        sentence = test_case["sentence"]

        expected_ids = set(
            test_case["expected"]
        )

        print()
        print(
            f"TEST #{index}"
        )

        print(
            f"SENTENCE: {sentence}"
        )

        try:

            # --------------------------------------------------------------
            # REQUEST
            # --------------------------------------------------------------

            request = ExtractionRequest(
                sentence=sentence,
                context={
                    "sentence_index": 0,
                },
            )

            # --------------------------------------------------------------
            # EXTRACTION
            # --------------------------------------------------------------

            result = extractor.extract(
                request
            )

            print()
            print(
                f"Raw result: {result!r}"
            )

            print(
                f"Result type: {type(result)}"
            )

            # --------------------------------------------------------------
            # NORMALIZE
            # --------------------------------------------------------------

            entities = get_entities(
                result
            )

            print(
                f"Knowledge objects: "
                f"{len(entities)}"
            )

            # --------------------------------------------------------------
            # ACTUAL IDs
            # --------------------------------------------------------------

            actual_ids = {
                getattr(
                    entity,
                    "entity_id",
                    None,
                )
                for entity in entities
            }

            actual_ids.discard(None)

            # --------------------------------------------------------------
            # MISSING
            # --------------------------------------------------------------

            missing = (
                expected_ids - actual_ids
            )

            # --------------------------------------------------------------
            # UNEXPECTED
            # --------------------------------------------------------------

            unexpected = (
                actual_ids - expected_ids
            )

            # --------------------------------------------------------------
            # VALIDATE
            # --------------------------------------------------------------

            validation_errors = []

            for entity in entities:

                validation_errors.extend(
                    validate_entity(entity)
                )

            # --------------------------------------------------------------
            # RESULT
            # --------------------------------------------------------------

            if (
                not missing
                and not validation_errors
            ):

                print()
                print(
                    "RESULT: ✅ PASS"
                )

                for entity in entities:

                    print_entity(
                        entity
                    )

                passed += 1

            else:

                print()
                print(
                    "RESULT: ❌ FAIL"
                )

                if missing:

                    print(
                        f"Missing: "
                        f"{sorted(missing)}"
                    )

                if unexpected:

                    print(
                        f"Unexpected: "
                        f"{sorted(unexpected)}"
                    )

                if validation_errors:

                    print(
                        "Validation errors:"
                    )

                    for error in validation_errors:

                        print(
                            f"  - {error}"
                        )

                print()
                print(
                    "ACTUAL RESULTS:"
                )

                if entities:

                    for entity in entities:

                        print_entity(
                            entity
                        )

                else:

                    print(
                        "  - []"
                    )

                failed += 1

        except Exception as error:

            print()
            print(
                "RESULT: ❌ ERROR"
            )

            print(
                f"{type(error).__name__}: "
                f"{error}"
            )

            failed += 1

    return passed, failed


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:

    print()
    print(
        "ENTERPRISE REUSABLE "
        "KNOWLEDGE EXTRACTOR TEST"
    )

    print()
    print(
        "Starting test_models.py..."
    )

    # ========================================================================
    # REPOSITORY
    # ========================================================================

    print()
    print(
        "1. Loading repository..."
    )

    try:

        repository = Repository()

    except Exception as error:

        print()
        print(
            "❌ REPOSITORY LOAD FAILED"
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        return

    print(
        "   ✅ Repository loaded"
    )

    # ========================================================================
    # REPOSITORY CHECK
    # ========================================================================

    entities = repository.cache.entity_indexes.get(
        ONTOLOGY,
        {},
    )

    print()
    print(
        f"Ontology: {ONTOLOGY}"
    )

    print(
        f"Total entities: {len(entities)}"
    )

    entity_types = sorted(
        {
            entity.entity_type
            for entity in entities.values()
            if getattr(
                entity,
                "entity_type",
                None,
            )
        }
    )

    print()
    print(
        f"Loaded entity types: "
        f"{entity_types}"
    )

    if ENTITY_TYPE not in entity_types:

        print()
        print(
            f"❌ Expected entity type "
            f"'{ENTITY_TYPE}' not found."
        )

        return

    print(
        f"   ✅ Entity type "
        f"'{ENTITY_TYPE}' confirmed"
    )

    # ========================================================================
    # PIPELINE
    # ========================================================================

    print()
    print(
        "2. Creating KnowledgeV5Pipeline..."
    )

    try:

        pipeline = KnowledgeV5Pipeline(
            repository_instance=repository,
        )

    except Exception as error:

        print()
        print(
            "❌ PIPELINE CREATION FAILED"
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        return

    print(
        "   ✅ Pipeline created"
    )

    # ========================================================================
    # DIRECT PIPELINE
    # ========================================================================

    print()
    print(
        "3. Testing pipeline..."
    )

    pipeline_ok = test_pipeline(
        pipeline
    )

    if not pipeline_ok:

        print()
        print(
            "❌ Pipeline test failed."
        )

        print(
            "Extractor tests will still run "
            "to isolate the failure."
        )

    # ========================================================================
    # EXTRACTOR
    # ========================================================================

    print()
    print(
        "4. Creating extractor..."
    )

    try:

        extractor = EXTRACTOR_CLASS(
            pipeline=pipeline,
        )

    except Exception as error:

        print()
        print(
            "❌ EXTRACTOR CREATION FAILED"
        )

        print(
            f"{type(error).__name__}: "
            f"{error}"
        )

        return

    print(
        "   ✅ Extractor created"
    )

    print()
    print(
        f"Extractor ontology    = "
        f"{extractor.ontology}"
    )

    print(
        f"Extractor entity type = "
        f"{extractor.entity_type}"
    )

    # ========================================================================
    # EXTRACTOR TESTS
    # ========================================================================

    passed, failed = test_extractor(
        extractor
    )

    # ========================================================================
    # SUMMARY
    # ========================================================================

    total = passed + failed

    print_header(
        "FINAL SUMMARY"
    )

    print()
    print(
        f"Total tests : {total}"
    )

    print(
        f"Passed      : {passed}"
    )

    print(
        f"Failed      : {failed}"
    )

    print()

    if failed == 0:

        print(
            "✅ ALL REUSABLE EXTRACTOR TESTS PASSED"
        )

    else:

        print(
            "❌ REUSABLE EXTRACTOR TESTS FAILED"
        )

    print()
    print(
        "=" * 80
    )

    print(
        "TEST COMPLETE"
    )

    print(
        "=" * 80
    )


# ============================================================================
# CRITICAL ENTRY POINT
# ============================================================================

if __name__ == "__main__":

    main()
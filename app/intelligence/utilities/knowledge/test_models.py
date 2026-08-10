"""
Enterprise Methodology Extractor Test
Enterprise V5

Purpose
-------
Validate the complete methodology extraction flow:

Sentence
    ↓
ExtractionRequest
    ↓
MethodologyExtractor
    ↓
KnowledgeV5Pipeline
    ↓
ExtractionResult
    ↓
MethodologyKnowledge objects

Important
---------
This test does NOT call pipeline.match().

KnowledgeV5Pipeline does not expose a public match()
method. The extractor is the public extraction interface.
"""

from __future__ import annotations

import sys
from pathlib import Path


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

from app.intelligence.utilities.knowledge.knowledge_extractors.methodology_extractor import (
    MethodologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
    ExtractionRequest,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.methodology_models import (
    MethodologyKnowledge,
)


# ============================================================================
# TEST CASES
# ============================================================================

TEST_CASES = [

    # ------------------------------------------------------------------------
    # CANONICAL
    # ------------------------------------------------------------------------

    (
        "Demonstrated experience with HACCP.",
        "HACCP",
        "METH_HACCP",
    ),

    (
        "Experienced in DMAIC methodology.",
        "DMAIC",
        "METH_DMAIC",
    ),

    (
        "Applied PDCA for continuous improvement.",
        "PDCA",
        "METH_PDCA",
    ),

    (
        "Experienced with Six Sigma.",
        "Six Sigma",
        "METH_SIX_SIGMA",
    ),

    (
        "Implemented Lean Manufacturing.",
        "Lean Manufacturing",
        "METH_LEAN_MANUFACTURING",
    ),

    (
        "Applied 5S methodology.",
        "5S",
        "METH_5S",
    ),

    (
        "Experienced in Root Cause Analysis.",
        "Root Cause Analysis",
        "METH_ROOT_CAUSE_ANALYSIS",
    ),

    (
        "Applied Kaizen principles.",
        "Kaizen",
        "METH_KAIZEN",
    ),

    (
        "Experienced in FMEA.",
        "FMEA",
        "METH_FMEA",
    ),

    (
        "Used Statistical Process Control.",
        "Statistical Process Control",
        "METH_SPC",
    ),

    # ------------------------------------------------------------------------
    # MULTIPLE
    # ------------------------------------------------------------------------

    (
        "Experienced with HACCP, FMEA, Six Sigma and Kaizen.",
        None,
        None,
    ),
]


# ============================================================================
# RESULT NORMALIZATION
# ============================================================================

def get_methodology_objects(result):

    if result is None:
        return []

    if hasattr(result, "entities"):
        return list(result.entities)

    if isinstance(result, list):
        return result

    if hasattr(result, "results"):
        return list(result.results)

    return [result]


# ============================================================================
# PRINT OBJECT
# ============================================================================

def print_methodology(item: MethodologyKnowledge):

    fields = [
        "found",
        "confidence",
        "original",
        "matched_phrase",
        "canonical",
        "normalized",
        "entity_id",
        "entity_type",
        "ontology_name",
        "category",
        "business_area",
        "domain",
        "description",
        "impact_weight",
        "source",
        "matched_alias",
        "is_alias",
        "methodology_family",
        "methodology_group",
        "version",
        "continuous_improvement",
        "quality_management",
        "food_safety",
        "risk_management",
        "analytical",
        "problem_solving",
        "statistical",
        "certification_related",
        "implementation_required",
        "maturity_level",
        "graph_node",
        "ats_weight",
    ]

    print()
    print("METHODOLOGY OBJECT")
    print("-" * 80)

    for field_name in fields:

        value = getattr(
            item,
            field_name,
            None,
        )

        print(
            f"{field_name:<30} = {value!r}"
        )


# ============================================================================
# MAIN
# ============================================================================

def main():

    print()
    print("=" * 80)
    print("ENTERPRISE METHODOLOGY EXTRACTOR TEST")
    print("=" * 80)

    print()
    print("Starting test_models.py...")

    # ========================================================================
    # 1. REPOSITORY
    # ========================================================================

    print()
    print("1. Loading repository...")

    repository = Repository()

    print(
        "   ✅ Repository loaded"
    )

    entities = repository.cache.entity_indexes.get(
        "methodologies",
        {},
    )

    print()
    print("Ontology:")
    print("methodologies")

    print()
    print("Total entities:")
    print(len(entities))

    # ========================================================================
    # 2. ENTITY TYPE
    # ========================================================================

    print()
    print("2. Checking repository entity type...")

    entity_types = sorted(
        {
            getattr(
                entity,
                "entity_type",
                None,
            )
            for entity in entities.values()
            if getattr(
                entity,
                "entity_type",
                None,
            )
        }
    )

    print(
        f"   Loaded entity types: {entity_types}"
    )

    if entity_types:

        print(
            f"   ✅ Repository entity type detected: "
            f"{entity_types}"
        )

    else:

        print(
            "   ❌ No repository entity type found."
        )

    # ========================================================================
    # 3. PIPELINE
    # ========================================================================

    print()
    print("3. Creating KnowledgeV5Pipeline...")

    pipeline = KnowledgeV5Pipeline(
        repository_instance=repository,
    )

    print(
        "   ✅ Pipeline created"
    )

    # ========================================================================
    # 4. EXTRACTOR
    # ========================================================================

    print()
    print("4. Creating MethodologyExtractor...")

    extractor = MethodologyExtractor(
        pipeline=pipeline,
    )

    print(
        "   ✅ Extractor created"
    )

    print()
    print(
        f"Extractor ontology    = "
        f"{extractor.ontology_name}"
    )

    print(
        f"Extractor entity type = "
        f"{extractor.entity_type}"
    )

    # ========================================================================
    # 5. ENTITY TYPE CHECK
    # ========================================================================

    if (
        entity_types
        and extractor.entity_type not in entity_types
    ):

        print()
        print(
            "⚠️ WARNING"
        )

        print(
            "Extractor entity type is not present "
            "in repository entity types."
        )

        print(
            f"Extractor: "
            f"{extractor.entity_type}"
        )

        print(
            f"Repository: "
            f"{entity_types}"
        )

    else:

        print()
        print(
            "✅ Extractor entity type matches repository."
        )

    # ========================================================================
    # 6. TESTS
    # ========================================================================

    print()
    print("5. METHODOLOGY EXTRACTION TESTS")

    print()
    print("=" * 80)

    passed = 0
    failed = 0

    for test_number, (
        sentence,
        expected_canonical,
        expected_entity_id,
    ) in enumerate(TEST_CASES, start=1):

        print()
        print(
            f"TEST #{test_number}"
        )

        print(
            f"SENTENCE: {sentence}"
        )

        print()

        try:

            # ----------------------------------------------------------------
            # REQUEST
            # ----------------------------------------------------------------

            request = ExtractionRequest(
                sentence=sentence,
                context={
                    "sentence_index": 0,
                },
            )

            # ----------------------------------------------------------------
            # EXTRACT
            # ----------------------------------------------------------------

            result = extractor.extract(
                request
            )

            print(
                f"Raw result: {result}"
            )

            print(
                f"Result type: "
                f"{type(result)}"
            )

            # ----------------------------------------------------------------
            # GET ENTITIES
            # ----------------------------------------------------------------

            methodologies = get_methodology_objects(
                result
            )

            print(
                f"Methodology objects: "
                f"{len(methodologies)}"
            )

            # ----------------------------------------------------------------
            # MULTIPLE TEST
            # ----------------------------------------------------------------

            if expected_entity_id is None:

                expected_ids = {
                    "METH_HACCP",
                    "METH_FMEA",
                    "METH_SIX_SIGMA",
                    "METH_KAIZEN",
                }

                actual_ids = {
                    getattr(
                        item,
                        "entity_id",
                        None,
                    )
                    for item in methodologies
                }

                missing = (
                    expected_ids
                    - actual_ids
                )

                if not missing:

                    print()
                    print(
                        "RESULT: ✅ PASS"
                    )

                    for item in methodologies:

                        print(
                            f"- "
                            f"{getattr(item, 'canonical', '')}"
                            f" "
                            f"[{getattr(item, 'entity_id', '')}]"
                            f" "
                            f"phrase="
                            f"{getattr(item, 'matched_phrase', '')!r}"
                            f" "
                            f"confidence="
                            f"{getattr(item, 'confidence', None)}"
                        )

                    passed += 1

                else:

                    print()
                    print(
                        "RESULT: ❌ FAIL"
                    )

                    print(
                        f"Missing: "
                        f"{sorted(missing)}"
                    )

                    print()
                    print(
                        "Actual entities:"
                    )

                    for item in methodologies:

                        print(
                            f"- "
                            f"{getattr(item, 'canonical', '')}"
                            f" "
                            f"[{getattr(item, 'entity_id', '')}]"
                        )

                    failed += 1

                continue

            # ----------------------------------------------------------------
            # NO RESULT
            # ----------------------------------------------------------------

            if not methodologies:

                print()
                print(
                    "RESULT: ❌ FAIL"
                )

                print(
                    f"Expected canonical: "
                    f"{expected_canonical}"
                )

                print(
                    f"Expected entity_id: "
                    f"{expected_entity_id}"
                )

                print()
                print(
                    "ACTUAL RESULTS:"
                )

                print(
                    "- []"
                )

                failed += 1

                continue

            # ----------------------------------------------------------------
            # FIND EXPECTED
            # ----------------------------------------------------------------

            matched = None

            for item in methodologies:

                if (
                    getattr(
                        item,
                        "entity_id",
                        None,
                    )
                    == expected_entity_id
                ):

                    matched = item

                    break

            # ----------------------------------------------------------------
            # NOT FOUND
            # ----------------------------------------------------------------

            if matched is None:

                print()
                print(
                    "RESULT: ❌ FAIL"
                )

                print(
                    f"Expected canonical: "
                    f"{expected_canonical}"
                )

                print(
                    f"Expected entity_id: "
                    f"{expected_entity_id}"
                )

                print()
                print(
                    "ACTUAL RESULTS:"
                )

                for item in methodologies:

                    print(
                        f"- "
                        f"{getattr(item, 'canonical', '')}"
                        f" "
                        f"[{getattr(item, 'entity_id', '')}]"
                    )

                failed += 1

                continue

            # ----------------------------------------------------------------
            # VALIDATION
            # ----------------------------------------------------------------

            errors = []

            if (
                getattr(
                    matched,
                    "canonical",
                    None,
                )
                != expected_canonical
            ):

                errors.append(
                    "canonical mismatch"
                )

            if (
                getattr(
                    matched,
                    "entity_id",
                    None,
                )
                != expected_entity_id
            ):

                errors.append(
                    "entity_id mismatch"
                )

            if not getattr(
                matched,
                "found",
                False,
            ):

                errors.append(
                    "found is not True"
                )

            if not getattr(
                matched,
                "matched_phrase",
                None,
            ):

                errors.append(
                    "matched_phrase is empty"
                )

            if (
                getattr(
                    matched,
                    "ontology_name",
                    None,
                )
                != "methodologies"
            ):

                errors.append(
                    "ontology_name mismatch"
                )

            # ----------------------------------------------------------------
            # FAILURE
            # ----------------------------------------------------------------

            if errors:

                print()
                print(
                    "RESULT: ❌ FAIL"
                )

                for error in errors:

                    print(
                        f"  - {error}"
                    )

                print_methodology(
                    matched
                )

                failed += 1

                continue

            # ----------------------------------------------------------------
            # SUCCESS
            # ----------------------------------------------------------------

            print()
            print(
                "RESULT: ✅ PASS"
            )

            print()
            print(
                f"- "
                f"{matched.canonical}"
                f" "
                f"[{matched.entity_id}]"
                f" "
                f"phrase="
                f"{matched.matched_phrase!r}"
                f" "
                f"confidence="
                f"{matched.confidence}"
                f" "
                f"alias="
                f"{matched.is_alias}"
            )

            passed += 1

        # ====================================================================
        # ERROR
        # ====================================================================

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

    # ========================================================================
    # SUMMARY
    # ========================================================================

    total = passed + failed

    print()
    print()
    print("=" * 80)
    print("METHODOLOGY EXTRACTOR TEST SUMMARY")
    print("=" * 80)

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
            "✅ ALL METHODOLOGY EXTRACTOR TESTS PASSED"
        )

    else:

        print(
            "❌ METHODOLOGY EXTRACTOR TESTS FAILED"
        )

    print()
    print("=" * 80)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 80)
    print()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
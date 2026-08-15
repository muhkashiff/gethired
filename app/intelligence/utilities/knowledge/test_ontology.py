"""
Enterprise V5 — Technology Knowledge Extractor Complete Traversal Test

Validates:

    KnowledgeV5Pipeline
            ↓
    technologies ontology
            ↓
    multi-match extraction
            ↓
    TechnologyExtractor
            ↓
    ExtractionResult[Technology]
            ↓
    Technology knowledge objects
            ↓
    common + technology-specific fields

This test is based on the actual Enterprise V5 APIs and the
actual Technology model fields.
"""

from __future__ import annotations

from typing import Any


# ============================================================================
# IMPORTS
# ============================================================================

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.technology_extractor import (
    TechnologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
    ExtractionRequest,
)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.technology_models import (
    Technology,
)


# ============================================================================
# TEST DATA
# ============================================================================

TEST_SENTENCE = (
    "Experienced in Python, SQL, Tableau, Power BI, pandas and "
    "scikit-learn."
)


EXPECTED_TECHNOLOGIES = {
    "TECH_PYTHON",
    "TECH_SQL",
    "TECH_TABLEAU",
    "TECH_POWER_BI",
    "TECH_PANDAS",
    "TECH_SCIKIT_LEARN",
}


# ============================================================================
# HELPERS
# ============================================================================

def section(title: str) -> None:

    print()
    print("=" * 80)
    print(title)
    print("=" * 80)


def assert_true(
    condition: bool,
    message: str,
) -> None:

    if not condition:
        raise AssertionError(message)


# ============================================================================
# TEST 1
# PIPELINE CREATION
# ============================================================================

def test_pipeline_creation() -> KnowledgeV5Pipeline:

    section(
        "TEST 1 — KNOWLEDGE V5 PIPELINE CREATION"
    )

    pipeline = KnowledgeV5Pipeline()

    assert_true(
        pipeline is not None,
        "KnowledgeV5Pipeline creation failed.",
    )

    print(
        "PASS — KnowledgeV5Pipeline created."
    )

    return pipeline


# ============================================================================
# TEST 2
# TECHNOLOGY EXTRACTOR CREATION
# ============================================================================

def test_technology_extractor_creation(
    pipeline: KnowledgeV5Pipeline,
) -> TechnologyExtractor:

    section(
        "TEST 2 — TECHNOLOGY EXTRACTOR CREATION"
    )

    extractor = TechnologyExtractor(
        pipeline=pipeline
    )

    assert_true(
        extractor is not None,
        "TechnologyExtractor creation failed.",
    )

    print(
        "PASS — TechnologyExtractor created."
    )

    return extractor


# ============================================================================
# TEST 3
# RAW TECHNOLOGY MULTI-MATCH
# ============================================================================

def test_raw_technology_multi_match(
    pipeline: KnowledgeV5Pipeline,
) -> list[Any]:

    section(
        "TEST 3 — RAW TECHNOLOGY MULTI-MATCH"
    )

    results = pipeline.run(
        ontology="technologies",
        sentence=TEST_SENTENCE,
    )

    print(
        "Result type :",
        type(results).__name__,
    )

    print(
        "Match count :",
        len(results),
    )

    assert_true(
        isinstance(results, list),
        "KnowledgeV5Pipeline.run() must return a list.",
    )

    assert_true(
        len(results) == len(EXPECTED_TECHNOLOGIES),
        (
            "Technology ontology did not return the expected "
            f"number of matches. Expected "
            f"{len(EXPECTED_TECHNOLOGIES)}, got {len(results)}."
        ),
    )

    found_ids = {
        match.entity_id
        for match in results
    }

    print()

    for index, match in enumerate(
        results,
        start=1,
    ):

        print(
            f"{index}. "
            f"entity_id='{match.entity_id}', "
            f"canonical='{match.canonical}', "
            f"phrase='{match.phrase}', "
            f"confidence={match.confidence:.3f}, "
            f"category='{match.category}'"
        )

    missing = (
        EXPECTED_TECHNOLOGIES
        - found_ids
    )

    unexpected = (
        found_ids
        - EXPECTED_TECHNOLOGIES
    )

    print()
    print(
        "Expected :",
        sorted(EXPECTED_TECHNOLOGIES),
    )

    print(
        "Found    :",
        sorted(found_ids),
    )

    print(
        "Missing  :",
        sorted(missing),
    )

    print(
        "Unexpected:",
        sorted(unexpected),
    )

    assert_true(
        not missing,
        f"Missing technology entities: {sorted(missing)}",
    )

    assert_true(
        not unexpected,
        (
            "Unexpected technology entities: "
            f"{sorted(unexpected)}"
        ),
    )

    print()
    print(
        "PASS — Technology ontology returned all "
        "expected technologie entities."
    )

    return results


# ============================================================================
# TEST 4
# EXTRACTION REQUEST
# ============================================================================

def test_extraction_request() -> ExtractionRequest:

    section(
        "TEST 4 — EXTRACTION REQUEST CREATION"
    )

    request = ExtractionRequest(
        sentence=TEST_SENTENCE,
        context={
            "sentence_index": 0,
        },
    )

    assert_true(
        request is not None,
        "ExtractionRequest creation failed.",
    )

    assert_true(
        request.sentence == TEST_SENTENCE,
        "ExtractionRequest sentence mismatch.",
    )

    print(
        "PASS — ExtractionRequest created."
    )

    return request


# ============================================================================
# TEST 5
# TECHNOLOGY KNOWLEDGE EXTRACTION
# ============================================================================

def test_technology_knowledge_extraction(
    extractor: TechnologyExtractor,
    request: ExtractionRequest,
):

    section(
        "TEST 5 — TECHNOLOGY KNOWLEDGE EXTRACTION"
    )

    result = extractor.extract(
        request
    )

    print(
        "Result type :",
        type(result).__name__,
    )

    print(
        "Ontology    :",
        result.ontology,
    )

    print(
        "Found       :",
        result.found,
    )

    print(
        "Count       :",
        result.count,
    )

    assert_true(
        result.found,
        "TechnologyExtractor returned no technology entities.",
    )

    assert_true(
        result.count == len(EXPECTED_TECHNOLOGIES),
        (
            "TechnologyExtractor returned incorrect count. "
            f"Expected {len(EXPECTED_TECHNOLOGIES)}, "
            f"got {result.count}."
        ),
    )

    print()
    print(
        "PASS — TechnologyExtractor returned all "
        "expected technologie knowledge objects."
    )

    return result


# ============================================================================
# TEST 6
# ENTITY IDs
# ============================================================================

def test_entity_ids(
    result,
) -> None:

    section(
        "TEST 6 — TECHNOLOGY ENTITY IDS"
    )

    found_ids = {
        entity.entity_id
        for entity in result.entities
    }

    missing = (
        EXPECTED_TECHNOLOGIES
        - found_ids
    )

    unexpected = (
        found_ids
        - EXPECTED_TECHNOLOGIES
    )

    print(
        "Expected :",
        sorted(EXPECTED_TECHNOLOGIES),
    )

    print(
        "Found    :",
        sorted(found_ids),
    )

    print(
        "Missing  :",
        sorted(missing),
    )

    print(
        "Unexpected:",
        sorted(unexpected),
    )

    assert_true(
        not missing,
        f"Missing technology knowledge entities: {sorted(missing)}",
    )

    assert_true(
        not unexpected,
        (
            "Unexpected technology knowledge entities: "
            f"{sorted(unexpected)}"
        ),
    )

    print()
    print(
        "PASS — All expected technology knowledge entities found."
    )


# ============================================================================
# TEST 7
# OBJECT TYPE
# ============================================================================

def test_object_types(
    result,
) -> None:

    section(
        "TEST 7 — TECHNOLOGY KNOWLEDGE OBJECT TYPES"
    )

    for entity in result.entities:

        print(
            f"{entity.entity_id:<25} "
            f"type={type(entity).__name__:<15} "
            f"canonical='{entity.canonical}'"
        )

        assert_true(
            isinstance(
                entity,
                Technology,
            ),
            (
                f"{entity.entity_id} is not a Technology "
                f"object. Got {type(entity).__name__}."
            ),
        )

    print()
    print(
        "PASS — All technology knowledge objects "
        "have correct Technology type."
    )


# ============================================================================
# TEST 8
# COMMON KNOWLEDGE FIELDS
# ============================================================================

def test_common_fields(
    result,
) -> None:

    section(
        "TEST 8 — COMMON KNOWLEDGE FIELDS"
    )

    for entity in result.entities:

        print(
            f"PASS — {entity.entity_id}: "
            f"original='{entity.original}', "
            f"canonical='{entity.canonical}', "
            f"normalized='{entity.normalized}', "
            f"confidence={entity.confidence:.3f}"
        )

        assert_true(
            entity.found is True,
            f"{entity.entity_id}: found is not True.",
        )

        assert_true(
            entity.confidence >= 0.0,
            f"{entity.entity_id}: invalid confidence.",
        )

        assert_true(
            bool(entity.original),
            f"{entity.entity_id}: original is empty.",
        )

        assert_true(
            bool(entity.canonical),
            f"{entity.entity_id}: canonical is empty.",
        )

        assert_true(
            bool(entity.entity_id),
            f"{entity.entity_id}: entity_id is empty.",
        )

        assert_true(
            entity.ontology_name == "technologies",
            (
                f"{entity.entity_id}: incorrect ontology_name: "
                f"{entity.ontology_name!r}"
            ),
        )

        assert_true(
            entity.entity_type == "technologie",
            (
                f"{entity.entity_id}: incorrect entity_type: "
                f"{entity.entity_type!r}"
            ),
        )

        assert_true(
            entity.matched_phrase == entity.original,
            (
                f"{entity.entity_id}: matched_phrase does not "
                "match original."
            ),
        )

    print()
    print(
        "PASS — Common knowledge fields validated."
    )


# ============================================================================
# TEST 9
# TECHNOLOGY MODEL FIELD EXISTENCE
# ============================================================================

def test_technology_field_existence(
    result,
) -> None:

    section(
        "TEST 9 — TECHNOLOGY MODEL FIELD EXISTENCE"
    )

    expected_fields = {

        # ------------------------------------------------------------
        # Technology definition
        # ------------------------------------------------------------

        "technology_family",
        "technology_group",
        "vendor",
        "version",

        # ------------------------------------------------------------
        # Classification
        # ------------------------------------------------------------

        "programming_language",
        "database",
        "analytics_tool",
        "cloud_platform",
        "operating_system",
        "framework",
        "erp",
        "visualization_tool",

        # ------------------------------------------------------------
        # Enterprise
        # ------------------------------------------------------------

        "commercial",
        "open_source",
        "certification_available",
        "maturity_level",

        # ------------------------------------------------------------
        # Knowledge graph
        # ------------------------------------------------------------

        "graph_node",
        "ats_weight",
    }

    for entity in result.entities:

        missing = [
            field_name
            for field_name in expected_fields
            if not hasattr(
                entity,
                field_name,
            )
        ]

        print(
            f"{entity.entity_id:<25} "
            f"missing_fields={missing}"
        )

        assert_true(
            not missing,
            (
                f"{entity.entity_id} is missing Technology "
                f"fields: {missing}"
            ),
        )

    print()
    print(
        "PASS — All Technology-specific model fields exist."
    )


# ============================================================================
# TEST 10
# TECHNOLOGY FIELD VALUES
# ============================================================================

def test_technology_field_values(
    result,
) -> None:

    section(
        "TEST 10 — TECHNOLOGY-SPECIFIC FIELD VALUES"
    )

    for entity in result.entities:

        print()
        print(
            f"ENTITY: {entity.entity_id}"
        )

        print(
            f"  canonical              : {entity.canonical}"
        )

        print(
            f"  category               : {entity.category}"
        )

        print(
            f"  technology_family      : "
            f"{entity.technology_family}"
        )

        print(
            f"  technology_group       : "
            f"{entity.technology_group}"
        )

        print(
            f"  vendor                 : "
            f"{entity.vendor}"
        )

        print(
            f"  version               : "
            f"{entity.version}"
        )

        print(
            f"  programming_language  : "
            f"{entity.programming_language}"
        )

        print(
            f"  database              : "
            f"{entity.database}"
        )

        print(
            f"  analytics_tool        : "
            f"{entity.analytics_tool}"
        )

        print(
            f"  cloud_platform        : "
            f"{entity.cloud_platform}"
        )

        print(
            f"  operating_system      : "
            f"{entity.operating_system}"
        )

        print(
            f"  framework             : "
            f"{entity.framework}"
        )

        print(
            f"  erp                   : "
            f"{entity.erp}"
        )

        print(
            f"  visualization_tool    : "
            f"{entity.visualization_tool}"
        )

        print(
            f"  commercial            : "
            f"{entity.commercial}"
        )

        print(
            f"  open_source           : "
            f"{entity.open_source}"
        )

        print(
            f"  certification_available: "
            f"{entity.certification_available}"
        )

        print(
            f"  maturity_level        : "
            f"{entity.maturity_level}"
        )

        print(
            f"  graph_node            : "
            f"{entity.graph_node}"
        )

        print(
            f"  ats_weight            : "
            f"{entity.ats_weight}"
        )

        # ------------------------------------------------------------
        # Basic type validation
        # ------------------------------------------------------------

        assert_true(
            isinstance(
                entity.technology_family,
                str,
            ),
            f"{entity.entity_id}: technology_family must be str.",
        )

        assert_true(
            isinstance(
                entity.technology_group,
                str,
            ),
            f"{entity.entity_id}: technology_group must be str.",
        )

        assert_true(
            isinstance(
                entity.vendor,
                str,
            ),
            f"{entity.entity_id}: vendor must be str.",
        )

        assert_true(
            isinstance(
                entity.version,
                str,
            ),
            f"{entity.entity_id}: version must be str.",
        )

        boolean_fields = {

            "programming_language":
                entity.programming_language,

            "database":
                entity.database,

            "analytics_tool":
                entity.analytics_tool,

            "cloud_platform":
                entity.cloud_platform,

            "operating_system":
                entity.operating_system,

            "framework":
                entity.framework,

            "erp":
                entity.erp,

            "visualization_tool":
                entity.visualization_tool,

            "commercial":
                entity.commercial,

            "open_source":
                entity.open_source,

            "certification_available":
                entity.certification_available,

            "graph_node":
                entity.graph_node,
        }

        for field_name, value in boolean_fields.items():

            assert_true(
                isinstance(
                    value,
                    bool,
                ),
                (
                    f"{entity.entity_id}: "
                    f"{field_name} must be bool, "
                    f"got {type(value).__name__}."
                ),
            )

        assert_true(
            isinstance(
                entity.maturity_level,
                int,
            ),
            (
                f"{entity.entity_id}: maturity_level must "
                f"be int."
            ),
        )

        assert_true(
            isinstance(
                entity.ats_weight,
                (int, float),
            ),
            (
                f"{entity.entity_id}: ats_weight must "
                f"be numeric."
            ),
        )

    print()
    print(
        "PASS — Technology-specific field types validated."
    )


# ============================================================================
# TEST 11
# TECHNOLOGY CLASSIFICATION VALIDATION
# ============================================================================

def test_technology_classification(
    result,
) -> None:

    section(
        "TEST 11 — TECHNOLOGY CLASSIFICATION VALIDATION"
    )

    by_id = {
        entity.entity_id: entity
        for entity in result.entities
    }

    # ------------------------------------------------------------
    # Python
    # ------------------------------------------------------------

    python = by_id["TECH_PYTHON"]

    assert_true(
        python.programming_language is True,
        "TECH_PYTHON should be classified as programming_language",
    )

    # ------------------------------------------------------------
    # SQL
    # ------------------------------------------------------------

    sql = by_id["TECH_SQL"]

    assert_true(
        sql.database is True,
        "TECH_SQL should be classified as database.",
    )

    # ------------------------------------------------------------
    # Tableau
    # ------------------------------------------------------------

    tableau = by_id["TECH_TABLEAU"]

    assert_true(
        tableau.analytics_tool is True
        or tableau.visualization_tool is True,
        (
            "TECH_TABLEAU should be classified as "
            "analytics_tool or visualization_tool."
        ),
    )

    # ------------------------------------------------------------
    # Power BI
    # ------------------------------------------------------------

    power_bi = by_id["TECH_POWER_BI"]

    assert_true(
        power_bi.analytics_tool is True
        or power_bi.visualization_tool is True,
        (
            "TECH_POWER_BI should be classified as "
            "analytics_tool or visualization_tool."
        ),
    )

    # ------------------------------------------------------------
    # Pandas
    # ------------------------------------------------------------

    pandas = by_id["TECH_PANDAS"]

    assert_true(
        pandas.framework is True
        or pandas.analytics_tool is True
        or pandas.programming_language is False,
        (
            "TECH_PANDAS classification is inconsistent."
        ),
    )

    # ------------------------------------------------------------
    # Scikit-learn
    # ------------------------------------------------------------

    sklearn = by_id["TECH_SCIKIT_LEARN"]

    assert_true(
        sklearn.framework is True
        or sklearn.analytics_tool is True
        or sklearn.programming_language is False,
        (
            "TECH_SCIKIT_LEARN classification is inconsistent."
        ),
    )

    print(
        "PASS — Technology classification fields "
        "are structurally valid."
    )


# ============================================================================
# TEST 12
# MATCH / KNOWLEDGE ALIGNMENT
# ============================================================================

def test_match_knowledge_alignment(
    result,
) -> None:

    section(
        "TEST 12 — MATCH RESULT / KNOWLEDGE ALIGNMENT"
    )

    assert_true(
        len(result.matches) == len(result.entities),
        (
            "ExtractionResult matches/entities lengths differ."
        ),
    )

    for match, entity in zip(
        result.matches,
        result.entities,
    ):

        print(
            f"{entity.entity_id:<25} "
            f"match='{match.phrase}' "
            f"knowledge_original='{entity.original}' "
            f"confidence={match.confidence:.3f}"
        )

        assert_true(
            match.entity_id == entity.entity_id,
            (
                f"Entity ID mismatch: "
                f"match={match.entity_id}, "
                f"knowledge={entity.entity_id}"
            ),
        )

        assert_true(
            match.phrase == entity.original,
            (
                f"Original phrase mismatch for "
                f"{entity.entity_id}."
            ),
        )

        assert_true(
            match.confidence == entity.confidence,
            (
                f"Confidence mismatch for "
                f"{entity.entity_id}."
            ),
        )

        assert_true(
            match.start_char == entity.start_char,
            (
                f"start_char mismatch for "
                f"{entity.entity_id}."
            ),
        )

        assert_true(
            match.end_char == entity.end_char,
            (
                f"end_char mismatch for "
                f"{entity.entity_id}."
            ),
        )

    print()
    print(
        "PASS — MatchResult and Technology knowledge "
        "objects remain aligned."
    )


# ============================================================================
# TEST 13
# MULTI-MATCH PRESERVATION
# ============================================================================

def test_multi_match_preservation(
    result,
) -> None:

    section(
        "TEST 13 — MULTI-MATCH PRESERVATION"
    )

    assert_true(
        result.count == 6,
        (
            "TechnologyExtractor collapsed multiple "
            f"technology matches. Expected 6, got {result.count}."
        ),
    )

    unique_ids = {
        entity.entity_id
        for entity in result.entities
    }

    assert_true(
        len(unique_ids) == 6,
        (
            "TechnologyExtractor produced duplicate or "
            "collapsed technology entities."
        ),
    )

    print(
        "Technology entities preserved:"
    )

    for entity_id in sorted(unique_ids):
        print(
            f"  PASS — {entity_id}"
        )

    print()
    print(
        "PASS — Multi-match behavior preserved from "
        "pipeline through knowledge extraction."
    )


# ============================================================================
# TEST 14
# ITERATION API
# ============================================================================

def test_extraction_result_iteration(
    result,
) -> None:

    section(
        "TEST 14 — EXTRACTION RESULT ITERATION API"
    )

    entities = list(result)

    assert_true(
        len(entities) == result.count,
        (
            "ExtractionResult iteration count does not "
            "match result.count."
        ),
    )

    assert_true(
        result.first is not None,
        "ExtractionResult.first returned None.",
    )

    assert_true(
        len(result) == result.count,
        (
            "ExtractionResult.__len__ does not match count."
        ),
    )

    print(
        "Iteration count :",
        len(entities),
    )

    print(
        "First entity    :",
        result.first.entity_id,
    )

    print()
    print(
        "PASS — ExtractionResult iteration API works."
    )


# ============================================================================
# TEST 15
# FINAL ARCHITECTURAL TRAVERSAL
# ============================================================================

def test_final_architectural_traversal(
    pipeline: KnowledgeV5Pipeline,
    extractor: TechnologyExtractor,
    request: ExtractionRequest,
    result,
) -> None:

    section(
        "TEST 15 — FINAL ARCHITECTURAL TRAVERSAL"
    )

    print(
        "Resume sentence"
    )

    print(
        f"    {request.sentence}"
    )

    print()
    print(
        "KnowledgeV5Pipeline"
    )

    print(
        "    ↓"
    )

    print(
        "technologies ontology"
    )

    print(
        "    ↓"
    )

    print(
        f"    {len(result.matches)} MatchResult objects"
    )

    print(
        "    ↓"
    )

    print(
        "TechnologyExtractor"
    )

    print(
        "    ↓"
    )

    print(
        f"    {len(result.entities)} Technology objects"
    )

    print()
    print(
        "TECHNOLOGY ENTITIES"
    )

    for entity in result.entities:

        print(
            f"    {entity.entity_id:<25}"
            f" -> {entity.canonical}"
        )

    assert_true(
        result.count == 6,
        "Final traversal did not preserve all 6 technologies.",
    )

    assert_true(
        all(
            isinstance(
                entity,
                Technology,
            )
            for entity in result.entities
        ),
        "Final traversal contains non-Technology objects.",
    )

    print()
    print(
        "PASS — Resume sentence traversed successfully "
        "through Technology Knowledge architecture."
    )


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def test_technology_knowledge_model() -> None:

    print()
    print(
        "=" * 80
    )

    print(
        "ENTERPRISE V5 — TECHNOLOGY KNOWLEDGE "
        "EXTRACTOR COMPLETE TRAVERSAL TEST"
    )

    print(
        "=" * 80
    )

    # ------------------------------------------------------------
    # 1. Pipeline
    # ------------------------------------------------------------

    pipeline = test_pipeline_creation()

    # ------------------------------------------------------------
    # 2. Extractor
    # ------------------------------------------------------------

    extractor = test_technology_extractor_creation(
        pipeline
    )

    # ------------------------------------------------------------
    # 3. Raw multi-match
    # ------------------------------------------------------------

    test_raw_technology_multi_match(
        pipeline
    )

    # ------------------------------------------------------------
    # 4. Extraction request
    # ------------------------------------------------------------

    request = test_extraction_request()

    # ------------------------------------------------------------
    # 5. Knowledge extraction
    # ------------------------------------------------------------

    result = test_technology_knowledge_extraction(
        extractor,
        request,
    )

    # ------------------------------------------------------------
    # 6. Entity IDs
    # ------------------------------------------------------------

    test_entity_ids(
        result
    )

    # ------------------------------------------------------------
    # 7. Object type
    # ------------------------------------------------------------

    test_object_types(
        result
    )

    # ------------------------------------------------------------
    # 8. Common fields
    # ------------------------------------------------------------

    test_common_fields(
        result
    )

    # ------------------------------------------------------------
    # 9. Technology fields
    # ------------------------------------------------------------

    test_technology_field_existence(
        result
    )

    # ------------------------------------------------------------
    # 10. Technology field values
    # ------------------------------------------------------------

    test_technology_field_values(
        result
    )

    # ------------------------------------------------------------
    # 11. Classification
    # ------------------------------------------------------------

    test_technology_classification(
        result
    )

    # ------------------------------------------------------------
    # 12. Match alignment
    # ------------------------------------------------------------

    test_match_knowledge_alignment(
        result
    )

    # ------------------------------------------------------------
    # 13. Multi-match
    # ------------------------------------------------------------

    test_multi_match_preservation(
        result
    )

    # ------------------------------------------------------------
    # 14. Result API
    # ------------------------------------------------------------

    test_extraction_result_iteration(
        result
    )

    # ------------------------------------------------------------
    # 15. Final architecture
    # ------------------------------------------------------------

    test_final_architectural_traversal(
        pipeline,
        extractor,
        request,
        result,
    )

    # ------------------------------------------------------------
    # FINAL
    # ------------------------------------------------------------

    print()
    print(
        "=" * 80
    )

    print(
        "ENTERPRISE V5 — TECHNOLOGY KNOWLEDGE "
        "EXTRACTOR TEST PASSED"
    )

    print(
        "=" * 80
    )

    print(
        "KnowledgeV5Pipeline      : PASS"
    )

    print(
        "Technology ontology      : PASS"
    )

    print(
        "Multi-match extraction   : PASS"
    )

    print(
        "TechnologyExtractor      : PASS"
    )

    print(
        "ExtractionResult         : PASS"
    )

    print(
        "Technology model         : PASS"
    )

    print(
        "Common fields            : PASS"
    )

    print(
        "Technology fields        : PASS"
    )

    print(
        "Classification           : PASS"
    )

    print(
        "Match alignment           : PASS"
    )

    print(
        "Knowledge traversal      : PASS"
    )

    print(
        "=" * 80
    )


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":

    test_technology_knowledge_model()
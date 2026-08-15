"""
Enterprise V5
Full Knowledge Extractor Traversal Test

Purpose
-------
Comprehensively validate:

    KnowledgeV5Pipeline
        ↓
    ontology matcher
        ↓
    multi-match extraction
        ↓
    Knowledge Extractors
        ↓
    Knowledge Models
        ↓
    entity validation

Important repository terminology
--------------------------------
technologies  -> entity_type = "technologie"
methodologies -> entity_type = "methodologie"

The test intentionally does NOT assume that every extractor
uses the same constructor signature.
"""

from __future__ import annotations

import inspect
from typing import Any


# ============================================================================
# PIPELINE
# ============================================================================

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)


# ============================================================================
# EXTRACTION REQUEST
# ============================================================================

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
    ExtractionRequest,
)


# ============================================================================
# EXTRACTORS
# ============================================================================

from app.intelligence.utilities.knowledge.knowledge_extractors.skills_extractor import (
    SkillsExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.technology_extractor import (
    TechnologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.methodology_extractor import (
    MethodologyExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.action_extractor import (
    ActionExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.metric_extractor import (
    MetricExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.domain_extractor import (
    DomainExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.standard_extractor import (
    StandardExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.target_extractor import (
    TargetExtractor,
)


# ============================================================================
# TEST DATA
# ============================================================================

SKILL_SENTENCE = (
    "Experienced in quality assurance, food safety, leadership "
    "and business intelligence."
)

TECHNOLOGY_SENTENCE = (
    "Experienced in Python, SQL, Tableau, Power BI, pandas "
    "and scikit-learn."
)

METHODOLOGY_SENTENCE = (
    "Experienced in HACCP, FSSC 22000, Lean Management, "
    "Six Sigma and Agile Scrum."
)

ACTION_SENTENCE = (
    "Implemented FSSC 22000 requirements and improved "
    "manufacturing yield through data based decision making."
)

METRIC_SENTENCE = (
    "Increased production yield from 70% to 99%."
)

DOMAIN_SENTENCE = (
    "Worked across quality assurance, food safety, manufacturing "
    "and supply chain operations."
)

STANDARD_SENTENCE = (
    "Maintained compliance with FSSC 22000, ISO 9001 and "
    "BRCGS requirements."
)

TARGET_SENTENCE = (
    "Improved production yield from 70% to 99%."
)


# ============================================================================
# EXPECTED PIPELINE ENTITIES
# ============================================================================

EXPECTED_PIPELINE = {

    "skills": {
        "sentence": SKILL_SENTENCE,

        # Adjust these IDs only if your repository uses different
        # skill entity IDs.
        "minimum": 1,
    },

    "technologies": {
        "sentence": TECHNOLOGY_SENTENCE,

        "expected": {
            "TECH_PYTHON",
            "TECH_SQL",
            "TECH_TABLEAU",
            "TECH_POWER_BI",
            "TECH_PANDAS",
            "TECH_SCIKIT_LEARN",
        },

        "expected_count": 6,

        "entity_type": "technologie",
    },

    "methodologies": {
        "sentence": METHODOLOGY_SENTENCE,

        # These should be replaced with the exact repository IDs
        # if they differ.
        "minimum": 1,

        "entity_type": "methodologie",
    },

    "actions": {
        "sentence": ACTION_SENTENCE,
        "minimum": 2,
    },

    "metrics": {
        "sentence": METRIC_SENTENCE,
        "minimum": 1,
    },

    "domains": {
        "sentence": DOMAIN_SENTENCE,
        "minimum": 3,
    },

    "standards": {
        "sentence": STANDARD_SENTENCE,
        "minimum": 2,
    },

    "targets": {
        "sentence": TARGET_SENTENCE,
        "minimum": 1,
    },
}


# ============================================================================
# EXTRACTOR DEFINITIONS
# ============================================================================

EXTRACTORS = {

    "skills": SkillsExtractor,

    "technologies": TechnologyExtractor,

    "methodologies": MethodologyExtractor,

    "actions": ActionExtractor,

    "metrics": MetricExtractor,

    "domains": DomainExtractor,

    "standards": StandardExtractor,

    "targets": TargetExtractor,
}


# ============================================================================
# OUTPUT
# ============================================================================

def banner(title: str) -> None:

    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def section(title: str) -> None:

    print()
    print("-" * 78)
    print(title)
    print("-" * 78)


# ============================================================================
# CONSTRUCTOR HANDLING
# ============================================================================

def create_extractor(
    extractor_class: type,
    pipeline: KnowledgeV5Pipeline,
):
    """
    Instantiate an extractor without assuming that every extractor
    has the same constructor signature.

    Preferred:
        Extractor(pipeline=pipeline)

    If pipeline is not accepted:
        Extractor()

    If the constructor exposes another compatible parameter,
    the test reports it rather than silently inventing arguments.
    """

    signature = inspect.signature(
        extractor_class.__init__
    )

    parameters = signature.parameters

    # --------------------------------------------------------------
    # Preferred architecture
    # --------------------------------------------------------------

    if "pipeline" in parameters:

        parameter = parameters["pipeline"]

        if (
            parameter.kind
            in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
        ):

            return extractor_class(
                pipeline=pipeline
            )

    # --------------------------------------------------------------
    # Alternative name used by some implementations
    # --------------------------------------------------------------

    if "knowledge_pipeline" in parameters:

        parameter = parameters["knowledge_pipeline"]

        if (
            parameter.kind
            in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            )
        ):

            return extractor_class(
                knowledge_pipeline=pipeline
            )

    # --------------------------------------------------------------
    # No pipeline argument
    # --------------------------------------------------------------

    required = []

    for name, parameter in parameters.items():

        if name == "self":
            continue

        if parameter.default is inspect.Parameter.empty:

            required.append(name)

    if not required:

        return extractor_class()

    raise TypeError(
        f"{extractor_class.__name__} has unsupported "
        f"constructor requirements: {required}. "
        f"Signature: {signature}"
    )


# ============================================================================
# REQUEST CREATION
# ============================================================================

def make_request(
    sentence: str,
) -> ExtractionRequest:

    return ExtractionRequest(
        sentence=sentence,
        context={
            "sentence_index": 0,
        },
    )


# ============================================================================
# TEST 1
# ============================================================================

def test_pipeline_creation():

    banner(
        "TEST 1 — KNOWLEDGE V5 PIPELINE CREATION"
    )

    pipeline = KnowledgeV5Pipeline()

    assert pipeline is not None

    print(
        "PASS — KnowledgeV5Pipeline created."
    )

    return pipeline


# ============================================================================
# TEST 2
# ============================================================================

def test_pipeline_api(
    pipeline: KnowledgeV5Pipeline,
):

    banner(
        "TEST 2 — KNOWLEDGE V5 PIPELINE API"
    )

    assert callable(
        getattr(
            pipeline,
            "run",
            None,
        )
    )

    print(
        "PASS — run(...) available."
    )

    assert callable(
        getattr(
            pipeline,
            "best",
            None,
        )
    )

    print(
        "PASS — best(...) available."
    )

    assert callable(
        getattr(
            pipeline,
            "build_parser_context",
            None,
        )
    )

    print(
        "PASS — build_parser_context(...) available."
    )


# ============================================================================
# TEST 3
# ============================================================================

def test_pipeline_multi_ontology(
    pipeline: KnowledgeV5Pipeline,
):

    banner(
        "TEST 3 — PIPELINE MULTI-ONTOLOGY TRAVERSAL"
    )

    pipeline_results = {}

    for ontology, config in EXPECTED_PIPELINE.items():

        section(
            f"ONTOLOGY : {ontology}"
        )

        sentence = config["sentence"]

        print(
            "SENTENCE :",
            sentence,
        )

        results = pipeline.run(
            ontology=ontology,
            sentence=sentence,
        )

        pipeline_results[ontology] = results

        print(
            "RESULT TYPE :",
            type(results).__name__,
        )

        print(
            "MATCH COUNT :",
            len(results),
        )

        for index, match in enumerate(
            results,
            start=1,
        ):

            entity_type = getattr(
                match,
                "entity_type",
                "",
            )

            entity_id = getattr(
                match,
                "entity_id",
                "",
            )

            canonical = getattr(
                match,
                "canonical",
                "",
            )

            phrase = getattr(
                match,
                "phrase",
                "",
            )

            confidence = getattr(
                match,
                "confidence",
                0.0,
            )

            print(
                f"{index}. "
                f"{entity_id=} "
                f"{canonical=} "
                f"{phrase=} "
                f"{confidence=:.3f} "
                f"{entity_type=}"
            )

        assert isinstance(
            results,
            list,
        ), (
            f"{ontology} did not return list."
        )

        minimum = config.get(
            "minimum",
            0,
        )

        assert len(results) >= minimum, (
            f"{ontology} returned "
            f"{len(results)} matches; "
            f"expected at least {minimum}."
        )

        # ----------------------------------------------------------
        # Technology exact validation
        # ----------------------------------------------------------

        if ontology == "technologies":

            expected = config[
                "expected"
            ]

            found = {
                match.entity_id
                for match in results
            }

            missing = (
                expected
                - found
            )

            unexpected = (
                found
                - expected
            )

            print()

            print(
                "EXPECTED TECHNOLOGIES"
            )

            print(
                "Expected count :",
                len(expected),
            )

            print(
                "Found count    :",
                len(found),
            )

            print(
                "Missing        :",
                sorted(missing),
            )

            print(
                "Unexpected     :",
                sorted(unexpected),
            )

            assert not missing, (
                f"Technology ontology missing: "
                f"{sorted(missing)}"
            )

            assert not unexpected, (
                f"Unexpected technology entities: "
                f"{sorted(unexpected)}"
            )

            assert len(found) == config[
                "expected_count"
            ], (
                "Technology multi-match count "
                "is incorrect."
            )

            # ------------------------------------------------------
            # Repository terminology
            # ------------------------------------------------------

            for match in results:

                assert match.entity_type == (
                    config["entity_type"]
                ), (
                    f"Technology entity_type must be "
                    f"'technologie', got "
                    f"{match.entity_type!r}"
                )

            print(
                "PASS — Technology ontology "
                "returned all expected entities."
            )

        # ----------------------------------------------------------
        # Methodology terminology
        # ----------------------------------------------------------

        if ontology == "methodologies":

            expected_type = config[
                "entity_type"
            ]

            for match in results:

                assert match.entity_type == (
                    expected_type
                ), (
                    "Methodology entity_type "
                    f"must be {expected_type!r}, "
                    f"got {match.entity_type!r}"
                )

            print(
                "PASS — Methodology entity_type "
                f"uses repository value "
                f"{expected_type!r}."
            )

    print()

    print(
        "PASS — All ontology pipeline traversals "
        "executed successfully."
    )

    return pipeline_results


# ============================================================================
# TEST 4
# ============================================================================

def test_best_results(
    pipeline: KnowledgeV5Pipeline,
):

    banner(
        "TEST 4 — BEST ENTITY TRAVERSAL"
    )

    for ontology, config in EXPECTED_PIPELINE.items():

        result = pipeline.best(
            ontology=ontology,
            sentence=config["sentence"],
        )

        print()

        print(
            f"Ontology: {ontology}"
        )

        print(
            "Best result:",
            result,
        )

        if config.get(
            "minimum",
            0,
        ) > 0:

            assert result is not None, (
                f"{ontology}.best() returned None."
            )

    print()

    print(
        "PASS — best(...) executed for all "
        "test ontologies."
    )


# ============================================================================
# TEST 5
# ============================================================================

def test_parser_context(
    pipeline: KnowledgeV5Pipeline,
):

    banner(
        "TEST 5 — KNOWLEDGE PARSER CONTEXT"
    )

    context = pipeline.build_parser_context(
        verb=True,
        obj=True,
        metric=True,
        modifier=True,
        numeric=True,
        domain=True,
    )

    print(
        "Context type:",
        type(context).__name__,
    )

    print(
        "Context:",
        context,
    )

    assert isinstance(
        context,
        dict,
    )

    expected_keys = {
        "verb_found",
        "object_found",
        "metric_found",
        "modifier_found",
        "numeric_value",
        "domain_found",
    }

    missing = (
        expected_keys
        - set(context)
    )

    assert not missing, (
        f"Parser context missing keys: "
        f"{sorted(missing)}"
    )

    print(
        "PASS — Parser context created correctly."
    )


# ============================================================================
# TEST 6
# ============================================================================

def test_extractor_creation(
    pipeline: KnowledgeV5Pipeline,
):

    banner(
        "TEST 6 — ALL KNOWLEDGE EXTRACTOR CREATION"
    )

    extractors = {}

    for ontology, extractor_class in (
        EXTRACTORS.items()
    ):

        try:

            extractor = create_extractor(
                extractor_class=extractor_class,
                pipeline=pipeline,
            )

        except Exception as error:

            signature = inspect.signature(
                extractor_class.__init__
            )

            raise AssertionError(
                f"{extractor_class.__name__} "
                f"could not be instantiated.\n"
                f"Ontology: {ontology}\n"
                f"Constructor: {signature}\n"
                f"Error: {error}"
            ) from error

        assert extractor is not None

        extractors[
            ontology
        ] = extractor

        print(
            f"PASS — "
            f"{ontology:<15} "
            f"{extractor_class.__name__} created."
        )

    return extractors


# ============================================================================
# TEST 7
# ============================================================================

def test_extractor_multi_match(
    extractors,
):

    banner(
        "TEST 7 — KNOWLEDGE EXTRACTOR MULTI-MATCH"
    )

    extractor_results = {}

    for ontology, extractor in (
        extractors.items()
    ):

        section(
            f"EXTRACTOR : {ontology}"
        )

        sentence = EXPECTED_PIPELINE[
            ontology
        ]["sentence"]

        request = make_request(
            sentence
        )

        print(
            "REQUEST:",
            sentence,
        )

        result = extractor.extract(
            request
        )

        extractor_results[
            ontology
        ] = result

        print(
            "RESULT TYPE :",
            type(result).__name__,
        )

        print(
            "FOUND       :",
            result.found,
        )

        print(
            "COUNT       :",
            result.count,
        )

        assert result is not None

        assert result.found, (
            f"{ontology} extractor "
            "returned no entities."
        )

        minimum = EXPECTED_PIPELINE[
            ontology
        ].get(
            "minimum",
            0,
        )

        assert result.count >= minimum, (
            f"{ontology} extractor returned "
            f"{result.count} entities; "
            f"expected at least {minimum}."
        )

        for index, entity in enumerate(
            result.entities,
            start=1,
        ):

            print()

            print(
                f"{index}. "
                f"type={type(entity).__name__}"
            )

            print(
                "   entity_id :",
                entity.entity_id,
            )

            print(
                "   canonical :",
                entity.canonical,
            )

            print(
                "   original  :",
                entity.original,
            )

            print(
                "   confidence:",
                entity.confidence,
            )

        # ----------------------------------------------------------
        # Technology validation
        # ----------------------------------------------------------

        if ontology == "technologies":

            expected = EXPECTED_PIPELINE[
                ontology
            ]["expected"]

            found = {
                entity.entity_id
                for entity in result.entities
            }

            missing = (
                expected
                - found
            )

            unexpected = (
                found
                - expected
            )

            print()

            print(
                "TECHNOLOGY ENTITY VALIDATION"
            )

            print(
                "Expected:",
                sorted(expected),
            )

            print(
                "Found:",
                sorted(found),
            )

            print(
                "Missing:",
                sorted(missing),
            )

            print(
                "Unexpected:",
                sorted(unexpected),
            )

            assert not missing

            assert not unexpected

            assert result.count == (
                len(expected)
            )

            # Repository terminology:
            for entity in result.entities:

                assert entity.entity_type == (
                    "technologie"
                ), (
                    f"{entity.entity_id} has "
                    f"entity_type="
                    f"{entity.entity_type!r}; "
                    f"expected 'technologie'."
                )

            print(
                "PASS — Technology extractor "
                "returned all expected entities."
            )

        # ----------------------------------------------------------
        # Methodology validation
        # ----------------------------------------------------------

        if ontology == "methodologies":

            for entity in result.entities:

                assert entity.entity_type == (
                    "methodologie"
                ), (
                    f"{entity.entity_id} has "
                    f"entity_type="
                    f"{entity.entity_type!r}; "
                    f"expected 'methodologie'."
                )

            print(
                "PASS — Methodology extractor "
                "uses entity_type='methodologie'."
            )

    print()

    print(
        "PASS — All knowledge extractors "
        "performed extraction successfully."
    )

    return extractor_results


# ============================================================================
# TEST 8
# ============================================================================

def test_common_knowledge_fields(
    extractor_results,
):

    banner(
        "TEST 8 — COMMON KNOWLEDGE FIELD VALIDATION"
    )

    required_fields = {

        "found",
        "confidence",
        "original",
        "canonical",
        "normalized",
        "entity_id",
        "entity_type",
        "ontology_name",
        "category",
        "description",
        "matched_phrase",
        "matched_alias",
        "start_char",
        "end_char",
        "token_index",
        "token_count",
        "sentence_index",
        "source",
        "metadata",
    }

    for ontology, result in (
        extractor_results.items()
    ):

        print()

        print(
            f"Ontology: {ontology}"
        )

        for entity in result.entities:

            missing = []

            for field_name in required_fields:

                if not hasattr(
                    entity,
                    field_name,
                ):

                    missing.append(
                        field_name
                    )

            assert not missing, (
                f"{ontology} entity "
                f"{entity.entity_id} missing "
                f"fields: {missing}"
            )

            assert entity.found is True

            assert entity.confidence >= 0.0

            assert entity.confidence <= 1.0

            assert entity.entity_id

            assert entity.canonical

            print(
                f"PASS — "
                f"{entity.entity_id}: "
                f"original={entity.original!r}, "
                f"canonical={entity.canonical!r}, "
                f"confidence={entity.confidence:.3f}"
            )

    print()

    print(
        "PASS — Common knowledge fields validated."
    )


# ============================================================================
# TEST 9
# ============================================================================

def test_technology_specific_fields(
    extractor_results,
):

    banner(
        "TEST 9 — TECHNOLOGY KNOWLEDGE MODEL VALIDATION"
    )

    result = extractor_results[
        "technologies"
    ]

    required_fields = {

        "technology_family",
        "technology_group",
        "vendor",
        "version",

        "programming_language",
        "database",
        "analytics_tool",
        "cloud_platform",
        "operating_system",
        "framework",
        "erp",
        "visualization_tool",

        "commercial",
        "open_source",
        "certification_available",
        "maturity_level",

        "graph_node",
        "ats_weight",
    }

    for entity in result.entities:

        print()

        print(
            f"{entity.entity_id:<25}"
            f"type={type(entity).__name__:<20}"
            f"canonical={entity.canonical!r}"
        )

        missing = [
            field
            for field in required_fields
            if not hasattr(
                entity,
                field,
            )
        ]

        assert not missing, (
            f"{entity.entity_id} missing "
            f"technology fields: "
            f"{missing}"
        )

        assert entity.entity_type == (
            "technologie"
        )

        assert entity.ontology_name == (
            "technologies"
        )

        assert isinstance(
            entity.programming_language,
            bool,
        )

        assert isinstance(
            entity.database,
            bool,
        )

        assert isinstance(
            entity.analytics_tool,
            bool,
        )

        assert isinstance(
            entity.visualization_tool,
            bool,
        )

        assert isinstance(
            entity.maturity_level,
            int,
        )

        assert isinstance(
            entity.graph_node,
            bool,
        )

        print(
            "PASS — technology-specific "
            "fields present."
        )

    print()

    print(
        "PASS — Technology model validated."
    )


# ============================================================================
# TEST 10
# ============================================================================

def test_multi_match_integrity(
    pipeline,
    extractor_results,
):

    banner(
        "TEST 10 — PIPELINE → EXTRACTOR MULTI-MATCH INTEGRITY"
    )

    for ontology, result in (
        extractor_results.items()
    ):

        sentence = EXPECTED_PIPELINE[
            ontology
        ]["sentence"]

        pipeline_matches = pipeline.run(
            ontology=ontology,
            sentence=sentence,
        )

        pipeline_ids = [
            match.entity_id
            for match in pipeline_matches
        ]

        extractor_ids = [
            entity.entity_id
            for entity in result.entities
        ]

        print()

        print(
            f"{ontology:<15}"
            f" pipeline={len(pipeline_ids):<3}"
            f" extractor={len(extractor_ids):<3}"
        )

        # Every extractor entity must originate
        # from a pipeline MatchResult.

        pipeline_id_set = set(
            pipeline_ids
        )

        extractor_id_set = set(
            extractor_ids
        )

        unexpected = (
            extractor_id_set
            - pipeline_id_set
        )

        assert not unexpected, (
            f"{ontology} extractor produced "
            f"entities not present in pipeline: "
            f"{sorted(unexpected)}"
        )

        print(
            "PASS — extractor entities correspond "
            "to pipeline matches."
        )

    print()

    print(
        "PASS — Pipeline → Extractor "
        "multi-match integrity validated."
    )


# ============================================================================
# TEST 11
# ============================================================================

def test_no_single_match_regression(
    extractor_results,
):

    banner(
        "TEST 11 — MULTI-MATCH REGRESSION CHECK"
    )

    critical_multi_match = {
        "technologies": 6,
        "domains": 3,
        "actions": 2,
        "standards": 2,
    }

    for ontology, minimum in (
        critical_multi_match.items()
    ):

        result = extractor_results[
            ontology
        ]

        print(
            f"{ontology:<15}"
            f" count={result.count}"
            f" expected>={minimum}"
        )

        assert result.count >= minimum, (
            f"REGRESSION: {ontology} "
            f"returned only {result.count} "
            f"knowledge entities."
        )

    print()

    print(
        "PASS — No single-match regression "
        "detected in critical ontologies."
    )


# ============================================================================
# TEST 12
# ============================================================================

def test_entity_type_terminology(
    extractor_results,
):

    banner(
        "TEST 12 — ENTITY TYPE TERMINOLOGY"
    )

    expected_types = {

        "technologies":
            "technologie",

        "methodologies":
            "methodologie",
    }

    for ontology, expected_type in (
        expected_types.items()
    ):

        result = extractor_results[
            ontology
        ]

        print()

        print(
            f"Ontology : {ontology}"
        )

        print(
            f"Expected : {expected_type}"
        )

        for entity in result.entities:

            print(
                f"  {entity.entity_id:<30}"
                f"{entity.entity_type}"
            )

            assert entity.entity_type == (
                expected_type
            )

        print(
            "PASS — Repository entity terminology "
            "preserved."
        )


# ============================================================================
# MASTER TEST
# ============================================================================

def test_full_enterprise_v5_extractor_traversal():

    banner(
        "ENTERPRISE V5 — FULL KNOWLEDGE EXTRACTOR TRAVERSAL"
    )

    # ================================================================
    # PIPELINE
    # ================================================================

    pipeline = test_pipeline_creation()

    # ================================================================
    # PIPELINE API
    # ================================================================

    test_pipeline_api(
        pipeline
    )

    # ================================================================
    # PIPELINE MULTI-ONTOLOGY
    # ================================================================

    test_pipeline_multi_ontology(
        pipeline
    )

    # ================================================================
    # BEST
    # ================================================================

    test_best_results(
        pipeline
    )

    # ================================================================
    # PARSER CONTEXT
    # ================================================================

    test_parser_context(
        pipeline
    )

    # ================================================================
    # EXTRACTORS
    # ================================================================

    extractors = test_extractor_creation(
        pipeline
    )

    # ================================================================
    # EXTRACTOR MULTI-MATCH
    # ================================================================

    extractor_results = test_extractor_multi_match(
        extractors
    )

    # ================================================================
    # COMMON FIELDS
    # ================================================================

    test_common_knowledge_fields(
        extractor_results
    )

    # ================================================================
    # TECHNOLOGY MODEL
    # ================================================================

    test_technology_specific_fields(
        extractor_results
    )

    # ================================================================
    # PIPELINE / EXTRACTOR INTEGRITY
    # ================================================================

    test_multi_match_integrity(
        pipeline,
        extractor_results,
    )

    # ================================================================
    # REGRESSION
    # ================================================================

    test_no_single_match_regression(
        extractor_results
    )

    # ================================================================
    # TERMINOLOGY
    # ================================================================

    test_entity_type_terminology(
        extractor_results
    )

    # ================================================================
    # FINAL
    # ================================================================

    banner(
        "ENTERPRISE V5 — FULL KNOWLEDGE EXTRACTOR TRAVERSAL PASSED"
    )

    print()
    print(
        "KnowledgeV5Pipeline       : PASS"
    )

    print(
        "Pipeline multi-match      : PASS"
    )

    print(
        "Best entity API           : PASS"
    )

    print(
        "Parser context            : PASS"
    )

    print(
        "All extractors            : PASS"
    )

    print(
        "Technology extraction     : PASS"
    )

    print(
        "Methodology extraction    : PASS"
    )

    print(
        "Common knowledge fields   : PASS"
    )

    print(
        "Technology model          : PASS"
    )

    print(
        "Pipeline/extractor link   : PASS"
    )

    print(
        "Multi-match regression    : PASS"
    )

    print(
        "Entity terminology        : PASS"
    )

    print()
    print(
        "ENTERPRISE V5 KNOWLEDGE "
        "EXTRACTOR TRAVERSAL : PASS"
    )


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":

    test_full_enterprise_v5_extractor_traversal()
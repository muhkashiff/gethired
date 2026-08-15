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


"""
Enterprise V5 — Knowledge Entity / Extractor Traversal Test

Validates the actual KnowledgeV5Pipeline API.

Pipeline API:

    run(ontology, sentence)
    best(ontology, sentence)
    build_parser_context(...)

Architecture:

    sentence
        ↓
    KnowledgeV5Pipeline
        ↓
    Tokenizer
        ↓
    Matcher
        ↓
    Confidence
        ↓
    OverlapResolver
        ↓
    Ranker
        ↓
    Knowledge entities
"""




from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)


# ======================================================================
# TEST DATA
# ======================================================================

TEST_SENTENCES = {

    "skills": (
        "Experienced in Python, SQL, Tableau, Power BI, "
        "pandas and scikit-learn."
    ),

    "actions": (
        "Implemented FSSC 22000 requirements and improved "
        "manufacturing yield through data based decision making."
    ),

    "metrics": (
        "Increased yield from 70% to 99%."
    ),

    "domains": (
        "Worked across quality assurance, food safety, "
        "manufacturing and supply chain operations."
    ),

    "standards": (
        "Maintained compliance with FSSC 22000, ISO 9001 "
        "and BRCGS requirements."
    ),

    "targets": (
        "Improved production yield from 70% to 99%."
    ),
}


# ======================================================================
# DISPLAY HELPERS
# ======================================================================

def print_result(
    ontology: str,
    sentence: str,
    result,
) -> None:

    print()
    print("-" * 70)
    print(f"ONTOLOGY : {ontology}")
    print(f"SENTENCE : {sentence}")
    print(f"RESULT TYPE : {type(result).__name__}")

    print("RESULT:")
    print(result)

    print("-" * 70)


# ======================================================================
# TEST 1
# ======================================================================

def test_pipeline_creation():

    print("=" * 70)
    print("TEST 1 — KNOWLEDGE V5 PIPELINE CREATION")
    print("=" * 70)

    pipeline = KnowledgeV5Pipeline()

    assert pipeline is not None

    print("PASS — KnowledgeV5Pipeline created.")

    return pipeline


# ======================================================================
# TEST 2
# ======================================================================

def test_pipeline_api():

    print()
    print("=" * 70)
    print("TEST 2 — KNOWLEDGE V5 PIPELINE API")
    print("=" * 70)

    pipeline = KnowledgeV5Pipeline()

    assert callable(
        getattr(
            pipeline,
            "run",
            None,
        )
    )

    assert callable(
        getattr(
            pipeline,
            "best",
            None,
        )
    )

    assert callable(
        getattr(
            pipeline,
            "build_parser_context",
            None,
        )
    )

    print("PASS — run(ontology, sentence) available.")
    print("PASS — best(ontology, sentence) available.")
    print(
        "PASS — build_parser_context(...) available."
    )

    return pipeline


# ======================================================================
# TEST 3
# ======================================================================

def test_knowledge_entity_extraction():

    print()
    print("=" * 70)
    print("TEST 3 — KNOWLEDGE ENTITY EXTRACTION")
    print("=" * 70)

    pipeline = KnowledgeV5Pipeline()

    results = {}

    for ontology, sentence in TEST_SENTENCES.items():

        print()
        print(
            f"Running ontology: {ontology}"
        )

        result = pipeline.run(
            ontology,
            sentence,
        )

        results[ontology] = result

        print_result(
            ontology,
            sentence,
            result,
        )

    print()
    print(
        "PASS — KnowledgeV5Pipeline.run() "
        "executed for all test ontologies."
    )

    return results


# ======================================================================
# TEST 4
# ======================================================================

def test_best_entity_selection():

    print()
    print("=" * 70)
    print("TEST 4 — BEST KNOWLEDGE ENTITY")
    print("=" * 70)

    pipeline = KnowledgeV5Pipeline()

    successful = 0

    for ontology, sentence in TEST_SENTENCES.items():

        result = pipeline.best(
            ontology,
            sentence,
        )

        print()
        print(
            f"Ontology: {ontology}"
        )

        print(
            f"Best result: {result}"
        )

        if result is not None:

            successful += 1

    print()

    print(
        f"Best results returned: "
        f"{successful}/{len(TEST_SENTENCES)}"
    )

    print(
        "PASS — KnowledgeV5Pipeline.best() "
        "executed successfully."
    )

    return successful


# ======================================================================
# TEST 5
# ======================================================================

def test_parser_context():

    print()
    print("=" * 70)
    print("TEST 5 — KNOWLEDGE PARSER CONTEXT")
    print("=" * 70)

    pipeline = KnowledgeV5Pipeline()

    context = pipeline.build_parser_context(
        verb=True,
        obj=True,
        metric=True,
        modifier=True,
        numeric=True,
        domain=True,
    )

    assert context is not None

    print(
        "Parser context type:",
        type(context).__name__,
    )

    print(
        "Parser context:"
    )

    print(context)

    print(
        "PASS — Parser context created."
    )

    return context


# ======================================================================
# TEST 6
# ======================================================================

def test_multiple_ontology_traversal():

    print()
    print("=" * 70)
    print("TEST 6 — MULTI-ONTOLOGY TRAVERSAL")
    print("=" * 70)

    pipeline = KnowledgeV5Pipeline()

    total_results = 0

    for ontology, sentence in TEST_SENTENCES.items():

        result = pipeline.run(
            ontology,
            sentence,
        )

        if result is not None:

            total_results += 1

        print(
            f"{ontology:<15} -> "
            f"{type(result).__name__}"
        )

    print()

    assert total_results > 0

    print(
        f"PASS — {total_results} ontology "
        "traversals returned results."
    )

    return total_results


# ======================================================================
# MAIN TEST RUNNER
# ======================================================================

def test_knowledge_pipeline_api():

    print()
    print("=" * 70)
    print(
        "ENTERPRISE V5 — "
        "KNOWLEDGE PIPELINE TRAVERSAL TEST"
    )
    print("=" * 70)

    pipeline = test_pipeline_creation()

    test_pipeline_api()

    results = test_knowledge_entity_extraction()

    test_best_entity_selection()

    test_parser_context()

    test_multiple_ontology_traversal()

    print()
    print("=" * 70)
    print(
        "ENTERPRISE V5 — "
        "KNOWLEDGE PIPELINE TRAVERSAL PASSED"
    )
    print("=" * 70)

    print()
    print(
        "KnowledgeV5Pipeline : PASS"
    )

    print(
        "run() API           : PASS"
    )

    print(
        "best() API          : PASS"
    )

    print(
        "Parser context      : PASS"
    )

    print(
        "Multi-ontology      : PASS"
    )

    print(
        "Knowledge traversal : PASS"
    )

    return results


if __name__ == "__main__":

    test_knowledge_pipeline_api()
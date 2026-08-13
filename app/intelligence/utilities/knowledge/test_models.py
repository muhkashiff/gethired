
"""
Enterprise V5 — Certification Parser Extractor Test

Tests:

    certifications ontology
        ↓
    GenericOntologyParserExtractor
        ↓
    CertificationParserExtractor
        ↓
    CertificationParserModel
        ↓
    ExtractionResult
"""

from __future__ import annotations
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

"""
Enterprise V5 — METRICS Parser Extractor Test
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
    ExtractionRequest,
)

from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline,
)

from app.parser.extractors.metric_parser_extractor import (
    MetricParserExtractor,
)


def main():

    print("=" * 70)
    print("ENTERPRISE V5 — METRICS PARSER EXTRACTOR TEST")
    print("=" * 70)

    sentence = (
        "The facility improved production performance, "
        "increased line efficiency, optimized production yield, "
        "and reduced downtime."
    )

    print("\nSENTENCE")
    print("-" * 70)
    print(sentence)

    print("\nONTOLOGY")
    print("-" * 70)
    print("Metric-KPI")

    # ==============================================================
    # PIPELINE
    # ==============================================================

    pipeline = KnowledgeV5Pipeline()

    # ==============================================================
    # EXTRACTOR
    # ==============================================================

    extractor = MetricParserExtractor(
        pipeline=pipeline
    )

    # ==============================================================
    # REQUEST
    # ==============================================================

    request = ExtractionRequest(
        sentence=sentence
    )

    # ==============================================================
    # EXTRACTION
    # ==============================================================

    result = extractor.extract(
        request
    )

    # ==============================================================
    # RESULT
    # ==============================================================

    print("\nFOUND")
    print("-" * 70)
    print(result.found)

    print("\nCOUNT")
    print("-" * 70)
    print(result.count)

    # ==============================================================
    # ENTITIES
    # ==============================================================

    print("\nEXTRACTED Metrics")
    print("=" * 70)

    for index, entity in enumerate(
        result.entities,
        start=1,
    ):

        print(f"\nMetrics #{index}")
        print("-" * 70)

        print(
            f"found              : "
            f"{entity.found}"
        )

        print(
            f"confidence         : "
            f"{entity.confidence}"
        )

        print(
            f"original           : "
            f"{entity.original}"
        )

        print(
            f"canonical          : "
            f"{entity.canonical}"
        )

        print(
            f"normalized         : "
            f"{entity.normalized}"
        )

        print(
            f"entity_id          : "
            f"{entity.entity_id}"
        )

        print(
            f"entity_type        : "
            f"{entity.entity_type}"
        )

        print(
            f"ontology_name      : "
            f"{entity.ontology_name}"
        )

        print(
            f"category           : "
            f"{entity.category}"
        )

        print(
            f"business_area      : "
            f"{entity.business_area}"
        )

        print(
            f"description        : "
            f"{entity.description}"
        )

        print(
            f"related_metrics    : "
            f"{entity.related_metrics}"
        )

        print(
            f"higher_is_better   : "
            f"{entity.higher_is_better}"
        )

        print(
            f"impact_weight      : "
            f"{entity.impact_weight}"
        )

        print(
            f"matched_phrase     : "
            f"{entity.matched_phrase}"
        )

        print(
            f"matched_alias      : "
            f"{entity.matched_alias}"
        )

        print(
            f"start_char         : "
            f"{entity.start_char}"
        )

        print(
            f"end_char           : "
            f"{entity.end_char}"
        )

        print(
            f"token_index        : "
            f"{entity.token_index}"
        )

        print(
            f"token_count        : "
            f"{entity.token_count}"
        )

        print(
            f"sentence_index     : "
            f"{entity.sentence_index}"
        )

        print(
            f"graph_node         : "
            f"{entity.graph_node}"
        )

        print(
            f"metric_count       : "
            f"{entity.metric_count}"
        )

    # ==============================================================
    # MATCH RESULTS
    # ==============================================================

    print("\nMATCH RESULTS")
    print("=" * 70)

    for index, match in enumerate(
        result.matches,
        start=1,
    ):

        print(f"\nMATCH #{index}")
        print("-" * 70)

        print(
            f"phrase             : "
            f"{match.phrase}"
        )

        print(
            f"confidence         : "
            f"{match.confidence}"
        )

        print(
            f"matched_alias      : "
            f"{match.matched_alias}"
        )

        print(
            f"entity_id          : "
            f"{match.entity_id}"
        )

        print(
            f"entity_type        : "
            f"{match.entity_type}"
        )

    # ==============================================================
    # FIRST ENTITY
    # ==============================================================

    print("\nFIRST ENTITY")
    print("-" * 70)

    first = result.first

    if first is not None:

        print(
            f"Canonical : "
            f"{first.canonical}"
        )

        print(
            f"Type      : "
            f"{first.entity_type}"
        )

        print(
            f"Category  : "
            f"{first.category}"
        )

        print(
            f"Business Area : "
            f"{first.business_area}"
        )

        print(
            f"Entity ID : "
            f"{first.entity_id}"
        )

        print(
            f"Metrics   : "
            f"{first.related_metrics}"
        )

    else:

        print("None")

    print("\n" + "=" * 70)
    print("METRICS PARSER EXTRACTOR TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
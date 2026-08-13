

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
Enterprise V5 — Technology Parser Extractor Test
"""



from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
    ExtractionRequest,
)

from app.parser.extractors.technology_parser_extractor import (
    TechnologyParserExtractor,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (KnowledgeV5Pipeline)

def main():

    print("=" * 70)
    print("ENTERPRISE V5 — TECHNOLOGY PARSER EXTRACTOR TEST")
    print("=" * 70)

    # ==============================================================
    # SENTENCE
    # ==============================================================

    sentence = (
        "The data analytics team used Python and SQL for analytics, "
        "while R was used for statistical analysis."
    )

    print()
    print("SENTENCE")
    print("-" * 70)
    print(sentence)

    # ==============================================================
    # ONTOLOGY
    # ==============================================================

    print()
    print("ONTOLOGY")
    print("-" * 70)
    print("technologies")

    # ==============================================================
    # EXTRACTION REQUEST
    # ==============================================================

    request = ExtractionRequest(
        sentence=sentence,
        context={
            "sentence_index": 0,
        },
    )
    pipeline = KnowledgeV5Pipeline()
    # ==============================================================
    # EXTRACTOR
    # ==============================================================

    extractor = TechnologyParserExtractor(
        pipeline=pipeline,
    )

    # ==============================================================
    # EXTRACT
    # ==============================================================

    result = extractor.extract(
        request
    )

    # ==============================================================
    # RESULT SUMMARY
    # ==============================================================

    print()
    print("FOUND")
    print("-" * 70)
    print(result.found)

    print()
    print("COUNT")
    print("-" * 70)
    print(len(result.entities))

    # ==============================================================
    # EXTRACTED TECHNOLOGIES
    # ==============================================================

    print()
    print("EXTRACTED TECHNOLOGIES")
    print("=" * 70)

    for index, technology in enumerate(
        result.entities,
        start=1,
    ):

        print()
        print(f"TECHNOLOGY #{index}")
        print("-" * 70)

        print(
            f"found              : "
            f"{technology.found}"
        )

        print(
            f"confidence         : "
            f"{technology.confidence:.3f}"
        )

        print(
            f"original           : "
            f"{technology.original}"
        )

        print(
            f"canonical          : "
            f"{technology.canonical}"
        )

        print(
            f"normalized         : "
            f"{technology.normalized}"
        )

        print(
            f"entity_id          : "
            f"{technology.entity_id}"
        )

        print(
            f"entity_type        : "
            f"{technology.entity_type}"
        )

        print(
            f"ontology_name      : "
            f"{technology.ontology_name}"
        )

        print(
            f"category           : "
            f"{technology.category}"
        )

        print(
            f"business_area      : "
            f"{technology.business_area}"
        )

        print(
            f"domain             : "
            f"{technology.domain}"
        )

        print(
            f"description        : "
            f"{technology.description}"
        )

        print(
            f"technology_family  : "
            f"{technology.technology_family}"
        )

        print(
            f"technology_group   : "
            f"{technology.technology_group}"
        )

        print(
            f"vendor             : "
            f"{technology.vendor}"
        )

        print(
            f"version            : "
            f"{technology.version}"
        )

        print(
            f"abbreviation       : "
            f"{technology.abbreviation}"
        )

        print(
            f"programming_language: "
            f"{technology.programming_language}"
        )

        print(
            f"database           : "
            f"{technology.database}"
        )

        print(
            f"analytics_tool     : "
            f"{technology.analytics_tool}"
        )

        print(
            f"cloud_platform     : "
            f"{technology.cloud_platform}"
        )

        print(
            f"operating_system   : "
            f"{technology.operating_system}"
        )

        print(
            f"framework          : "
            f"{technology.framework}"
        )

        print(
            f"erp                : "
            f"{technology.erp}"
        )

        print(
            f"visualization_tool : "
            f"{technology.visualization_tool}"
        )

        print(
            f"commercial         : "
            f"{technology.commercial}"
        )

        print(
            f"open_source        : "
            f"{technology.open_source}"
        )

        print(
            f"certification_available: "
            f"{technology.certification_available}"
        )

        print(
            f"maturity_level     : "
            f"{technology.maturity_level}"
        )

        print(
            f"impact_weight      : "
            f"{technology.impact_weight}"
        )

        print(
            f"ats_weight         : "
            f"{technology.ats_weight}"
        )

        print(
            f"matched_phrase     : "
            f"{technology.matched_phrase}"
        )

        print(
            f"matched_alias      : "
            f"{technology.matched_alias}"
        )

        print(
            f"start_char         : "
            f"{technology.start_char}"
        )

        print(
            f"end_char           : "
            f"{technology.end_char}"
        )

        print(
            f"token_index        : "
            f"{technology.token_index}"
        )

        print(
            f"token_count        : "
            f"{technology.token_count}"
        )

        print(
            f"sentence_index     : "
            f"{technology.sentence_index}"
        )

        print(
            f"graph_node         : "
            f"{technology.graph_node}"
        )

        print(
            f"metadata           : "
            f"{technology.metadata}"
        )

    # ==============================================================
    # MATCH RESULTS
    # ==============================================================

    print()
    print("MATCH RESULTS")
    print("=" * 70)

    for index, technology in enumerate(
        result.entities,
        start=1,
    ):

        print()
        print(f"MATCH #{index}")
        print("-" * 70)

        print(
            f"phrase             : "
            f"{technology.matched_phrase}"
        )

        print(
            f"confidence         : "
            f"{technology.confidence:.3f}"
        )

        print(
            f"matched_alias      : "
            f"{technology.matched_alias}"
        )

        print(
            f"entity_id          : "
            f"{technology.entity_id}"
        )

        print(
            f"entity_type        : "
            f"{technology.entity_type}"
        )

    # ==============================================================
    # FIRST ENTITY
    # ==============================================================

    if result.entities:

        first = result.entities[0]

        print()
        print("FIRST ENTITY")
        print("-" * 70)

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
            f"Domain    : "
            f"{first.domain}"
        )

        print(
            f"Entity ID : "
            f"{first.entity_id}"
        )

    print()
    print("=" * 70)
    print("TECHNOLOGY PARSER EXTRACTOR TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
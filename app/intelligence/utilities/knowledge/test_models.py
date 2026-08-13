

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
Enterprise V5 — Domain Knowledge Extractor Test
"""

from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import (
    DomainKnowledge,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.domain_extractor import (
    DomainExtractor,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
    ExtractionRequest,
)


def test_domain_extractor():

    print("=" * 70)
    print("ENTERPRISE V5 — DOMAIN KNOWLEDGE EXTRACTOR TEST")
    print("=" * 70)

    sentence = (
        "The facility improved operations and quality management "
        "while strengthening food safety and compliance."
    )

    print()
    print("SENTENCE")
    print("-" * 70)
    print(sentence)

    print()
    print("ONTOLOGY")
    print("-" * 70)
    print("domains")

    # ------------------------------------------------------------
    # REQUEST
    # ------------------------------------------------------------

    request = ExtractionRequest(
        sentence=sentence
    )

    # ------------------------------------------------------------
    # EXTRACTOR
    # ------------------------------------------------------------

    extractor = DomainExtractor()

    result = extractor.extract(request)

    # ------------------------------------------------------------
    # RESULT
    # ------------------------------------------------------------

    print()
    print("FOUND")
    print("-" * 70)
    print(result.found)

    print()
    print("COUNT")
    print("-" * 70)
    print(len(result.entities))

    # ------------------------------------------------------------
    # ENTITIES
    # ------------------------------------------------------------

    print()
    print("EXTRACTED DOMAINS")
    print("=" * 70)

    for index, domain in enumerate(
        result.entities,
        start=1,
    ):

        print()
        print(f"DOMAIN #{index}")
        print("-" * 70)

        print(
            f"found              : "
            f"{domain.found}"
        )

        print(
            f"confidence         : "
            f"{domain.confidence:.3f}"
        )

        print(
            f"original           : "
            f"{domain.original}"
        )

        print(
            f"canonical          : "
            f"{domain.canonical}"
        )

        print(
            f"normalized         : "
            f"{domain.normalized}"
        )

        print(
            f"entity_id          : "
            f"{domain.entity_id}"
        )

        print(
            f"entity_type        : "
            f"{domain.entity_type}"
        )

        print(
            f"ontology_name      : "
            f"{domain.ontology_name}"
        )

        print(
            f"category           : "
            f"{domain.category}"
        )

        print(
            f"business_area      : "
            f"{domain.business_area}"
        )

        print(
            f"domain             : "
            f"{getattr(domain, 'domain', '')}"
        )

        print(
            f"impact_weight      : "
            f"{domain.impact_weight}"
        )

        print(
            f"matched_phrase     : "
            f"{domain.matched_phrase}"
        )

        print(
            f"matched_alias      : "
            f"{domain.matched_alias}"
        )

        print(
            f"start_char         : "
            f"{domain.start_char}"
        )

        print(
            f"end_char           : "
            f"{domain.end_char}"
        )

        print(
            f"token_index        : "
            f"{domain.token_index}"
        )

        print(
            f"token_count        : "
            f"{domain.token_count}"
        )

        print(
            f"sentence_index     : "
            f"{domain.sentence_index}"
        )

        print(
            f"graph_node         : "
            f"{domain.graph_node}"
        )

        print(
            f"metadata           : "
            f"{domain.metadata}"
        )

    # ------------------------------------------------------------
    # MATCH RESULTS
    # ------------------------------------------------------------

    print()
    print("MATCH RESULTS")
    print("=" * 70)

    for index, domain in enumerate(
        result.entities,
        start=1,
    ):

        print()
        print(f"MATCH #{index}")
        print("-" * 70)

        print(
            f"phrase             : "
            f"{domain.matched_phrase}"
        )

        print(
            f"confidence         : "
            f"{domain.confidence:.3f}"
        )

        print(
            f"matched_alias      : "
            f"{domain.matched_alias}"
        )

        print(
            f"entity_id          : "
            f"{domain.entity_id}"
        )

        print(
            f"entity_type        : "
            f"{domain.entity_type}"
        )

    # ------------------------------------------------------------
    # FIRST ENTITY
    # ------------------------------------------------------------

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
            f"{getattr(first, 'domain', '')}"
        )

        print(
            f"Entity ID : "
            f"{first.entity_id}"
        )

    print()
    print("=" * 70)
    print("DOMAIN KNOWLEDGE EXTRACTOR TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    test_domain_extractor()
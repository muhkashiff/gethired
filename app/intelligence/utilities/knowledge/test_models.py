from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def main() -> None:

    print("=" * 70)
    print("ENTERPRISE V5 — SKILL PARSER EXTRACTOR TEST")
    print("=" * 70)

    # ---------------------------------------------------------------
    # IMPORTS
    # ---------------------------------------------------------------

    from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_request import (
        ExtractionRequest,
    )

    from app.parser.extractors.skill_parser_extractor import (
        SkillParserExtractor,
    )

    from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
        KnowledgeV5Pipeline,
    )

    # ---------------------------------------------------------------
    # CREATE PIPELINE
    # ---------------------------------------------------------------

    pipeline = KnowledgeV5Pipeline()

    # ---------------------------------------------------------------
    # CREATE SKILL PARSER EXTRACTOR
    # ---------------------------------------------------------------

    extractor = SkillParserExtractor(
        pipeline=pipeline,
    )

    # ---------------------------------------------------------------
    # TEST SENTENCE
    # ---------------------------------------------------------------

    sentence = (
        "Experienced in HACCP, ISO 9001, "
        "food safety management and data analysis."
    )

    request = ExtractionRequest(
        sentence=sentence,
        context={
            "sentence_index": 0,
        },
    )

    # ---------------------------------------------------------------
    # EXTRACT
    # ---------------------------------------------------------------

    result = extractor.extract(
        request
    )

    # ---------------------------------------------------------------
    # BASIC RESULT
    # ---------------------------------------------------------------

    print()
    print("ONTOLOGY")
    print("-" * 70)
    print(result.ontology)

    print()
    print("FOUND")
    print("-" * 70)
    print(result.found)

    print()
    print("COUNT")
    print("-" * 70)
    print(result.count)

    # ---------------------------------------------------------------
    # EXTRACTED ENTITIES
    # ---------------------------------------------------------------

    print()
    print("EXTRACTED SKILLS")
    print("=" * 70)

    for index, knowledge in enumerate(
        result.entities,
        start=1,
    ):

        print()
        print(f"SKILL #{index}")
        print("-" * 70)

        print(
            f"found              : "
            f"{knowledge.found}"
        )

        print(
            f"confidence         : "
            f"{knowledge.confidence}"
        )

        print(
            f"original           : "
            f"{knowledge.original}"
        )

        print(
            f"canonical          : "
            f"{knowledge.canonical}"
        )

        print(
            f"normalized         : "
            f"{knowledge.normalized}"
        )

        print(
            f"entity_id          : "
            f"{knowledge.entity_id}"
        )

        print(
            f"entity_type        : "
            f"{knowledge.entity_type}"
        )

        print(
            f"ontology_name      : "
            f"{knowledge.ontology_name}"
        )

        print(
            f"category           : "
            f"{knowledge.category}"
        )

        print(
            f"business_area      : "
            f"{knowledge.business_area}"
        )

        print(
            f"domain             : "
            f"{knowledge.domain}"
        )

        print(
            f"skill_family       : "
            f"{knowledge.skill_family}"
        )

        print(
            f"skill_group        : "
            f"{knowledge.skill_group}"
        )

        print(
            f"level              : "
            f"{knowledge.level}"
        )

        print(
            f"technical          : "
            f"{knowledge.technical}"
        )

        print(
            f"managerial         : "
            f"{knowledge.managerial}"
        )

        print(
            f"analytical         : "
            f"{knowledge.analytical}"
        )

        print(
            f"operational        : "
            f"{knowledge.operational}"
        )

        print(
            f"compliance         : "
            f"{knowledge.compliance}"
        )

        print(
            f"leadership         : "
            f"{knowledge.leadership}"
        )

        print(
            f"communication      : "
            f"{knowledge.communication}"
        )

        print(
            f"transferable       : "
            f"{knowledge.transferable}"
        )

        print(
            f"certification_req. : "
            f"{knowledge.certification_required}"
        )

        print(
            f"years_required     : "
            f"{knowledge.years_required}"
        )

        print(
            f"ats_weight         : "
            f"{knowledge.ats_weight}"
        )

        print(
            f"graph_node         : "
            f"{knowledge.graph_node}"
        )

        print(
            f"matched_phrase     : "
            f"{knowledge.matched_phrase}"
        )

        print(
            f"matched_alias      : "
            f"{knowledge.matched_alias}"
        )

        print(
            f"start_char         : "
            f"{knowledge.start_char}"
        )

        print(
            f"end_char           : "
            f"{knowledge.end_char}"
        )

        print(
            f"token_index        : "
            f"{knowledge.token_index}"
        )

        print(
            f"token_count        : "
            f"{knowledge.token_count}"
        )

        print(
            f"sentence_index     : "
            f"{knowledge.sentence_index}"
        )

    # ---------------------------------------------------------------
    # MATCHES
    # ---------------------------------------------------------------

    print()
    print("MATCH RESULTS")
    print("=" * 70)

    for index, match in enumerate(
        result.matches,
        start=1,
    ):

        print()
        print(f"MATCH #{index}")
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

    # ---------------------------------------------------------------
    # FIRST ENTITY TEST
    # ---------------------------------------------------------------

    print()
    print("FIRST ENTITY")
    print("=" * 70)

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

    else:

        print(
            "No first entity."
        )

    # ---------------------------------------------------------------
    # FINAL STATUS
    # ---------------------------------------------------------------

    print()
    print("=" * 70)

    if result.found:

        print(
            "TEST PASSED — skills were extracted."
        )

    else:

        print(
            "TEST FAILED — no skills were extracted."
        )

    print("=" * 70)


if __name__ == "__main__":
    main()
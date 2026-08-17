"""
Enterprise Extractor Bridge Test
================================

Purpose:
    Verify that ExtractionCoordinator is actually calling
    KnowledgeV5Pipeline and returning ontology entities.

Run:
    python test_enterprise_extractor_bridge.py
"""

from app.intelligence.utilities.knowledge.knowledge_extractors.extraction_pipeline import (
    ExtractionCoordinator,
)


def test_extractor(sentence: str) -> bool:

    print("\n" + "=" * 80)
    print("ENTERPRISE EXTRACTOR BRIDGE TEST")
    print("=" * 80)

    print("\nInput sentence:")
    print(sentence)

    # ------------------------------------------------------------
    # CREATE COORDINATOR
    # ------------------------------------------------------------

    print("\n" + "-" * 80)
    print("1. CREATE EXTRACTION COORDINATOR")
    print("-" * 80)

    try:

        coordinator = ExtractionCoordinator()

        print("[PASS] ExtractionCoordinator created.")

        print(
            "Coordinator:",
            coordinator.__class__.__name__,
        )

        print(
            "Coordinator module:",
            coordinator.__class__.__module__,
        )

    except Exception as exc:

        print("[FAIL] Could not create coordinator.")
        print("Error:", repr(exc))

        return False

    # ------------------------------------------------------------
    # CHECK PIPELINE
    # ------------------------------------------------------------

    print("\n" + "-" * 80)
    print("2. KNOWLEDGE V5 PIPELINE")
    print("-" * 80)

    try:

        print(
            "Pipeline:",
            coordinator.pipeline.__class__.__name__,
        )

        print(
            "Pipeline module:",
            coordinator.pipeline.__class__.__module__,
        )

    except Exception as exc:

        print(
            "[FAIL] Could not inspect KnowledgeV5Pipeline."
        )

        print(
            "Error:",
            repr(exc),
        )

        return False

    # ------------------------------------------------------------
    # CHECK ONTOLOGIES
    # ------------------------------------------------------------

    print("\n" + "-" * 80)
    print("3. ONTOLOGIES")
    print("-" * 80)

    print(
        "Configured ontologies:"
    )

    for ontology in coordinator.ontologies:

        print(
            f"  - {ontology}"
        )

    # ------------------------------------------------------------
    # RUN EXTRACTION
    # ------------------------------------------------------------

    print("\n" + "-" * 80)
    print("4. CALL ExtractionCoordinator.run()")
    print("-" * 80)

    print(
        "Calling coordinator.run() ..."
    )

    try:

        result = coordinator.run(
            sentence
        )

    except Exception as exc:

        print(
            "[FAIL] ExtractionCoordinator.run() failed."
        )

        print(
            "Exception type:",
            type(exc).__name__,
        )

        print(
            "Exception:",
            repr(exc),
        )

        return False

    print(
        "[PASS] ExtractionCoordinator.run() completed."
    )

    # ------------------------------------------------------------
    # RESULT CONTRACT
    # ------------------------------------------------------------

    print("\n" + "-" * 80)
    print("5. EXTRACTION RESULT")
    print("-" * 80)

    print(
        "Result class:",
        result.__class__.__name__,
    )

    print(
        "Result module:",
        result.__class__.__module__,
    )

    print(
        "Sentence:",
        getattr(
            result,
            "sentence",
            None,
        ),
    )

    # ------------------------------------------------------------
    # COUNTS
    # ------------------------------------------------------------

    print("\n" + "-" * 80)
    print("6. ONTOLOGY COUNTS")
    print("-" * 80)

    try:

        counts = result.counts

        for ontology, count in counts.items():

            print(
                f"{ontology:15} : {count}"
            )

    except Exception as exc:

        print(
            "[WARNING] Could not read counts."
        )

        print(
            "Error:",
            repr(exc),
        )

    # ------------------------------------------------------------
    # ALL ENTITIES
    # ------------------------------------------------------------

    print("\n" + "-" * 80)
    print("7. ALL ENTITIES")
    print("-" * 80)

    entities = getattr(
        result,
        "all_entities",
        [],
    )

    print(
        "Total entities:",
        len(entities),
    )

    if not entities:

        print(
            "\n[FAIL] ZERO ENTITIES RETURNED."
        )

        print(
            "\nThis means the problem is BELOW "
            "ExtractionCoordinator:"
        )

        print(
            "ExtractionCoordinator"
        )

        print(
            "        ↓"
        )

        print(
            "KnowledgeV5Pipeline"
        )

        print(
            "        ↓"
        )

        print(
            "Ontology matching"
        )

        return False

    # ------------------------------------------------------------
    # ENTITY DETAILS
    # ------------------------------------------------------------

    for index, entity in enumerate(
        entities,
        start=1,
    ):

        print(
            f"\nENTITY {index}"
        )

        print(
            "  entity_id       :",
            entity.entity_id,
        )

        print(
            "  canonical       :",
            entity.canonical,
        )

        print(
            "  phrase          :",
            entity.phrase,
        )

        print(
            "  ontology        :",
            entity.ontology,
        )

        print(
            "  confidence      :",
            entity.confidence,
        )

        print(
            "  entity_type     :",
            entity.entity_type,
        )

        print(
            "  category        :",
            entity.category,
        )

        print(
            "  business_area   :",
            entity.business_area,
        )

        print(
            "  domain          :",
            entity.domain,
        )

        print(
            "  impact_weight   :",
            entity.impact_weight,
        )

        print(
            "  matched_alias   :",
            entity.matched_alias,
        )

        print(
            "  is_alias        :",
            entity.is_alias,
        )

        print(
            "  start_char      :",
            entity.start_char,
        )

        print(
            "  end_char        :",
            entity.end_char,
        )

        print(
            "  token_index     :",
            entity.token_index,
        )

        print(
            "  token_count     :",
            entity.token_count,
        )

        print(
            "  metadata        :",
            entity.metadata,
        )

    # ------------------------------------------------------------
    # SUCCESS
    # ------------------------------------------------------------

    print("\n" + "=" * 80)
    print("TEST RESULT")
    print("=" * 80)

    print(
        "[PASS] ExtractionCoordinator produced "
        f"{len(entities)} entities."
    )

    print(
        "\nThe extractor/coordinator layer is functioning."
    )

    return True


def main():

    # ------------------------------------------------------------
    # Diagnostic sentence
    # ------------------------------------------------------------

    sentence = (
        "Spearheaded the site-wide implementation, "
        "execution, and regulatory compliance of the "
        "integrated Quality and Food Safety Management "
        "System (QMS)."
    )

    success = test_extractor(
        sentence
    )

    print("\n")

    if success:

        print(
            "FINAL STATUS: PASS"
        )

    else:

        print(
            "FINAL STATUS: FAIL"
        )


if __name__ == "__main__":

    main()
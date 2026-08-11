from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


"""
Enterprise Knowledge Registry Test
Enterprise V5
"""

from app.intelligence.utilities.knowledge.repository_v5 import repository
from app.intelligence.utilities.knowledge.knowledge_extractors.registry import KnowledgeRegistry


def main():

    print("=" * 70)
    print("KNOWLEDGE REGISTRY TEST")
    print("=" * 70)

    # ------------------------------------------------------------
    # CREATE REGISTRY
    # ------------------------------------------------------------

    registry = KnowledgeRegistry(
        repository=repository
    )

    print(
        f"\nEntity count : {registry.entity_count}"
    )

    print(
        f"Alias count  : {registry.alias_count}"
    )

    # ------------------------------------------------------------
    # ENTITY TEST
    # ------------------------------------------------------------

    entity_id = "SKILL_QUALITY_ASSURANCE"

    print("\nENTITY TEST")
    print("-" * 70)

    print(
        "Exists:",
        registry.exists(
            entity_id
        )
    )

    entity = registry.get(
        entity_id
    )

    print(
        "Entity:",
        entity
    )

    print(
        "Canonical:",
        registry.canonical(
            entity_id
        )
    )

    print(
        "Category:",
        registry.category(
            entity_id
        )
    )

    print(
        "Aliases:",
        registry.aliases(
            entity_id
        )
    )

    print(
        "Impact:",
        registry.impact_weight(
            entity_id
        )
    )

    # ------------------------------------------------------------
    # ALIAS TEST
    # ------------------------------------------------------------

    print("\nALIAS TEST")
    print("-" * 70)

    aliases = [
        "quality assurance",
        "qa",
        "quality management",
    ]

    for text in aliases:

        result = registry.resolve_alias(
            text
        )

        print(
            f"{text!r} -> {result}"
        )

    # ------------------------------------------------------------
    # RELATION TEST
    # ------------------------------------------------------------

    print("\nRELATION TEST")
    print("-" * 70)

    relations = registry.relations_from(
        "SKILL_QUALITY_ASSURANCE"
    )

    print(
        "Outgoing relations:",
        len(relations)
    )

    for relation in relations[:10]:

        print(
            relation
        )

    # ------------------------------------------------------------
    # VALIDATION
    # ------------------------------------------------------------

    print("\nVALIDATION TEST")
    print("-" * 70)

    validation = registry.validate(
        [
            "SKILL_QUALITY_ASSURANCE",
            "SKILL_HACCP",
            "TGT_QMS",
            "DOES_NOT_EXIST",
        ]
    )

    print(
        validation
    )

    # ------------------------------------------------------------
    # STATS
    # ------------------------------------------------------------

    print("\nREGISTRY STATS")
    print("-" * 70)

    print(
        registry.stats()
    )

    print("\n" + "=" * 70)
    print("REGISTRY TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
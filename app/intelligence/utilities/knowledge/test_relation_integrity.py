from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
"""
Relation Missing-ID Diagnostic Test

Reports exactly which entity IDs referenced by relations
are missing from the repository and groups them by prefix.
"""

from collections import defaultdict

from app.intelligence.utilities.knowledge.repository_v5.repository import (
    Repository
)


def main():

    print("=" * 80)
    print("RELATION MISSING-ID DIAGNOSTIC")
    print("=" * 80)

    # ------------------------------------------------------------------
    # 1. LOAD REPOSITORY
    # ------------------------------------------------------------------

    print("\n1. Loading repository...")

    repository = Repository()

    print("   PASS: Repository initialized")

    # ------------------------------------------------------------------
    # 2. BUILD GLOBAL ENTITY INDEX
    # ------------------------------------------------------------------

    print("\n2. Building global entity index...")

    global_entities = {}

    for ontology_name, entities in repository.cache.entity_indexes.items():

        for entity_id, entity in entities.items():

            global_entities[entity_id] = {
                "ontology": ontology_name,
                "entity": entity,
            }

    print(
        f"   PASS: {len(global_entities)} entity IDs loaded"
    )

    # ------------------------------------------------------------------
    # 3. LOAD RELATIONS
    # ------------------------------------------------------------------

    print("\n3. Loading relations...")

    relations = repository.cache.relation_indexes.get(
        "relations",
        {}
    )

    print(
        f"   PASS: {len(relations)} relations loaded"
    )

    # ------------------------------------------------------------------
    # 4. FIND MISSING IDS
    # ------------------------------------------------------------------

    missing_sources = {}
    missing_targets = {}

    for relation_id, relation in relations.items():

        source_id = relation.source
        target_id = relation.target

        if source_id not in global_entities:

            missing_sources[relation_id] = {
                "id": source_id,
                "relation_type": relation.relation_type,
                "target": target_id,
            }

        if target_id not in global_entities:

            missing_targets[relation_id] = {
                "id": target_id,
                "relation_type": relation.relation_type,
                "source": source_id,
            }

    # ------------------------------------------------------------------
    # 5. GROUP BY PREFIX
    # ------------------------------------------------------------------

    source_groups = defaultdict(list)
    target_groups = defaultdict(list)

    for relation_id, data in missing_sources.items():

        entity_id = data["id"]

        prefix = entity_id.split("_")[0]

        source_groups[prefix].append(
            (relation_id, entity_id)
        )

    for relation_id, data in missing_targets.items():

        entity_id = data["id"]

        prefix = entity_id.split("_")[0]

        target_groups[prefix].append(
            (relation_id, entity_id)
        )

    # ------------------------------------------------------------------
    # 6. SOURCE SUMMARY
    # ------------------------------------------------------------------

    print("\n4. MISSING SOURCE SUMMARY")
    print("-" * 80)

    print(
        f"Missing source references: "
        f"{len(missing_sources)}"
    )

    for prefix in sorted(source_groups):

        ids = sorted(
            set(
                entity_id
                for _, entity_id
                in source_groups[prefix]
            )
        )

        print(
            f"\n{prefix}_* : {len(ids)}"
        )

        for entity_id in ids:

            print(
                f"   {entity_id}"
            )

    # ------------------------------------------------------------------
    # 7. TARGET SUMMARY
    # ------------------------------------------------------------------

    print("\n5. MISSING TARGET SUMMARY")
    print("-" * 80)

    print(
        f"Missing target references: "
        f"{len(missing_targets)}"
    )

    for prefix in sorted(target_groups):

        ids = sorted(
            set(
                entity_id
                for _, entity_id
                in target_groups[prefix]
            )
        )

        print(
            f"\n{prefix}_* : {len(ids)}"
        )

        for entity_id in ids:

            print(
                f"   {entity_id}"
            )

    # ------------------------------------------------------------------
    # 8. UNIQUE MISSING IDS
    # ------------------------------------------------------------------

    unique_missing = sorted(
        set(
            data["id"]
            for data in missing_sources.values()
        )
        |
        set(
            data["id"]
            for data in missing_targets.values()
        )
    )

    print("\n6. UNIQUE MISSING ENTITY IDS")
    print("-" * 80)

    print(
        f"Total unique missing IDs: "
        f"{len(unique_missing)}"
    )

    for entity_id in unique_missing:

        print(
            f"   {entity_id}"
        )

    # ------------------------------------------------------------------
    # 9. FINAL
    # ------------------------------------------------------------------

    print("\n" + "=" * 80)

    if not unique_missing:

        print(
            "RESULT: PASS"
        )

        print(
            "All relation references resolve."
        )

    else:

        print(
            "RESULT: DIAGNOSTIC COMPLETE"
        )

        print(
            f"{len(unique_missing)} unique entity IDs "
            f"need investigation."
        )

    print("=" * 80)


if __name__ == "__main__":

    main()
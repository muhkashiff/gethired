from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from app.intelligence.utilities.knowledge.repository_v5.repository import (
    Repository,
)

from app.intelligence.utilities.knowledge.knowledge_extractors.relation_extractor.relation_extractor import (
    RelationExtractor,
)


def main():

    print("=" * 80)
    print("RELATION SYSTEM TEST")
    print("=" * 80)

    ################################################################
    # 1. REPOSITORY
    ################################################################

    print("\n1. Loading repository...")

    repository = Repository()

    print("PASS: Repository initialized")

    ################################################################
    # 2. RELATION INDEXES
    ################################################################

    print("\n2. Checking relation indexes...")

    relation_index = (
        repository.cache.relation_indexes.get(
            "relations"
        )
    )

    relation_type_index = (
        repository.cache.relation_type_indexes.get(
            "relations"
        )
    )

    relation_source_index = (
        repository.cache.relation_source_indexes.get(
            "relations"
        )
    )

    relation_target_index = (
        repository.cache.relation_target_indexes.get(
            "relations"
        )
    )

    assert relation_index is not None
    assert relation_type_index is not None
    assert relation_source_index is not None
    assert relation_target_index is not None

    print("PASS: relation index")
    print("PASS: relation type index")
    print("PASS: relation source index")
    print("PASS: relation target index")

    ################################################################
    # 3. RELATION OBJECT
    ################################################################

    print("\n3. Testing REL_000001...")

    relation = repository.find_relation(
        "REL_000001"
    )

    assert relation is not None

    print(
        "PASS:",
        relation,
    )

    ################################################################
    # 4. CHECK RELATION OBJECT TYPE
    ################################################################

    from app.intelligence.utilities.knowledge.repository_v5.relation_repository_record import (
        RelationRepositoryRecord,
    )

    assert isinstance(
        relation,
        RelationRepositoryRecord,
    )

    print(
        "PASS: Relation is RelationRepositoryRecord"
    )
    
    ################################################################
    # 5. SOURCE ENTITY
    ################################################################

    print("\n5. Resolving source entity...")

    source_entity = (
        repository.find_entity_by_id(
            "actions",
            "ACT_IMPLEMENT",
        )
    )

    assert source_entity is not None

    print(
        "PASS:",
        source_entity.entity_id,
        source_entity.canonical,
    )

    ################################################################
    # 6. TARGET ENTITY
    ################################################################

    print("\n6. Resolving target entity...")

    target_entity = (
        repository.find_entity_by_id(
            "targets",
            "TGT_QMS",
        )
    )

    assert target_entity is not None

    print(
        "PASS:",
        target_entity.entity_id,
        target_entity.canonical,
    )

    ################################################################
    # 7. RELATION EXTRACTOR
    ################################################################

    print("\n7. Creating RelationExtractor...")

    extractor = RelationExtractor(
        repository
    )

    print(
        "PASS: RelationExtractor created"
    )

    ################################################################
    # 8. EXTRACT RELATION
    ################################################################

    print("\n8. Extracting relation...")

    result = extractor.extract(
        source_entity,
        target_entity,
        sentence_index=0,
    )

    assert result is not None

    print("\nResult:")
    print(result)

    ################################################################
    # 9. RESULT TYPE
    ################################################################

    from app.intelligence.utilities.knowledge.knowledge_extractor_models.relation_models import (
        RelationKnowledge,
    )

    assert isinstance(
        result,
        RelationKnowledge,
    )

    print(
        "PASS: Output is RelationKnowledge"
    )

    ################################################################
    # 10. VALIDATE
    ################################################################

    assert result.found is True

    assert result.relation_id == (
        "REL_000001"
    )

    assert result.relation_type == (
        "acts_on"
    )

    assert result.source_entity_id == (
        "ACT_IMPLEMENT"
    )

    assert result.target_entity_id == (
        "TGT_QMS"
    )

    assert result.confidence == 1.0

    print(
        "PASS: Relation extraction"
    )

    ################################################################
    # COMPLETE
    ################################################################

    print("\n" + "=" * 80)
    print("ALL RELATION TESTS PASSED")
    print("=" * 80)


if __name__ == "__main__":
    main()
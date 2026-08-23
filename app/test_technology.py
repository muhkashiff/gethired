from app.intelligence.utilities.knowledge.knowledge_extractor_models.interpretation_models import(
    KnowledgeInterpretation,)
from app.intelligence.utilities.knowledge.knowledge_extractor_models.base_models import (
    KnowledgeEntity,
)


def test_technology_entity_type_is_canonical():
    interpretation = KnowledgeInterpretation()

    entity = KnowledgeEntity(
        entity_type="technologie",
    )

    interpretation.add_entity(entity)

    assert len(interpretation.technologies) == 1
    assert interpretation.technologies[0] is entity
    assert interpretation.entity_count == 1
"""
Enterprise Standard Extractor
Enterprise V5
"""

from __future__ import annotations

from app.intelligence.utilities.knowledge.knowledge_extractor_models.standard_models import (
    StandardKnowledge,
)

from .generic_ontology_extractor import GenericOntologyExtractor


class StandardExtractor(
    GenericOntologyExtractor[StandardKnowledge]
):
    """
    Extracts recognized standards from text.
    """

    ontology_name = "standards"

    knowledge_class = StandardKnowledge

    entity_type = "standard"

    def extra_fields(
        self,
        entity,
        metadata,
    ) -> dict:
        return {
            "graph_node": metadata.get(
                "graph_node",
                True,
            ),
        }
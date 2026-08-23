"""
Enterprise Technology Extractor

Enterprise V5

Extracts technology entities from the technologies ontology.
"""

from __future__ import annotations

from typing import Any, Mapping

from app.intelligence.utilities.knowledge.knowledge_extractor_models.technology_models import (
    Technology,
)

from .generic_ontology_extractor import GenericOntologyExtractor


class TechnologyExtractor(GenericOntologyExtractor[Technology]):
    """
    Extracts technologies and returns Technology knowledge objects.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "technologies"

    knowledge_class = Technology

    entity_type = "technology"

    ####################################################################
    # TECHNOLOGY SPECIFIC FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate technology-specific fields from repository metadata.
        """

        return {
            "technology_family": metadata.get(
                "technology_family",
                entity.technology_family
                if hasattr(entity, "technology_family")
                else "",
            ),

            "technology_group": metadata.get(
                "technology_group",
                entity.technology_group
                if hasattr(entity, "technology_group")
                else "",
            ),

            "vendor": metadata.get(
                "vendor",
                "",
            ),

            "version": metadata.get(
                "version",
                "",
            ),

            "abbreviation": metadata.get(
                "abbreviation",
                "",
            ),

            "programming_language": metadata.get(
                "programming_language",
                True,
            ),

            "database": metadata.get(
                "database",
                True,
            ),

            "analytics_tool": metadata.get(
                "analytics_tool",
                True,
            ),

            "cloud_platform": metadata.get(
                "cloud_platform",
                True,
            ),

            "operating_system": metadata.get(
                "operating_system",
                True,
            ),

            "framework": metadata.get(
                "framework",
                True,
            ),

            "erp": metadata.get(
                "erp",
                True,
            ),

            "visualization_tool": metadata.get(
                "visualization_tool",
                True,
            ),

            "commercial": metadata.get(
                "commercial",
                True,
            ),

            "open_source": metadata.get(
                "open_source",
                True,
            ),

            "certification_available": metadata.get(
                "certification_available",
                True,
            ),

            "maturity_level": metadata.get(
                "maturity_level",
                1,
            ),

            "graph_node": metadata.get(
                "graph_node",
                True,
            ),

            "ats_weight": metadata.get(
                "ats_weight",
                entity.impact_weight,
            ),
        }
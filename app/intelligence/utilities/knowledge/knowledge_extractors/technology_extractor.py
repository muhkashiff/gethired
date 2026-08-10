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

    entity_type = "technologie"

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
                False,
            ),

            "database": metadata.get(
                "database",
                False,
            ),

            "analytics_tool": metadata.get(
                "analytics_tool",
                False,
            ),

            "cloud_platform": metadata.get(
                "cloud_platform",
                False,
            ),

            "operating_system": metadata.get(
                "operating_system",
                False,
            ),

            "framework": metadata.get(
                "framework",
                False,
            ),

            "erp": metadata.get(
                "erp",
                False,
            ),

            "visualization_tool": metadata.get(
                "visualization_tool",
                False,
            ),

            "commercial": metadata.get(
                "commercial",
                False,
            ),

            "open_source": metadata.get(
                "open_source",
                False,
            ),

            "certification_available": metadata.get(
                "certification_available",
                False,
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
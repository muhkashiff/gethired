"""
Enterprise Technology Parser Extractor

Enterprise V5

Parser layer.

Architecture:

BaseParserExtractor
        ↓
GenericOntologyParserExtractor
        ↓
TechnologyParserExtractor
        ↓
TechnologyParserModel
"""

from __future__ import annotations

from typing import Any, Mapping

from app.parser.extractors.generic_ontology_parser_extractor import (
    GenericOntologyParserExtractor,
)

from app.parser.parsed_models.technology import (
    TechnologyParserModel,
)
from app.intelligence.utilities.knowledge.knowledge_pipeline_v5.knowledgev5_pipeline import (
    KnowledgeV5Pipeline
)


class TechnologyParserExtractor(
    GenericOntologyParserExtractor[TechnologyParserModel]
):
    """
    Parser extractor for technologies.
    """

    ####################################################################
    # CONFIGURATION
    ####################################################################

    ontology_name = "technologies"

    knowledge_class = TechnologyParserModel

    # IMPORTANT:
    #
    # Enterprise repository intentionally derives:
    #
    # technologies -> technologie
    #
    entity_type = "technology"

    # ================================================================
    # INITIALIZATION
    # ================================================================
    
    def __init__(
            self,
            pipeline: KnowledgeV5Pipeline | None = None,
        ) -> None:
    
            if pipeline is None:
                pipeline = KnowledgeV5Pipeline()
    
            super().__init__(
                pipeline=pipeline
            )

    ####################################################################
    # EXTRA FIELDS
    ####################################################################

    def extra_fields(
        self,
        entity: Any,
        metadata: Mapping[str, Any],
    ) -> dict[str, Any]:
        """
        Populate technology-specific parser fields.

        Explicit metadata takes priority.

        When classification metadata is absent, category is used
        as the fallback classification source.
        """

        ################################################################
        # CATEGORY
        ################################################################

        category = (
            getattr(
                entity,
                "category",
                "",
            )
            or ""
        ).casefold().strip()

        ################################################################
        # IMPACT WEIGHT
        ################################################################

        impact_weight = getattr(
            entity,
            "impact_weight",
            1.0,
        )

        ################################################################
        # CLASSIFICATION
        #
        # Explicit metadata wins.
        #
        # Otherwise derive the primary classification from category.
        ################################################################

        programming_language = self._bool_value(
            metadata.get(
                "programming_language",
                category == "programming_language",
            )
        )

        database = self._bool_value(
            metadata.get(
                "database",
                category == "database",
            )
        )

        analytics_tool = self._bool_value(
            metadata.get(
                "analytics_tool",
                category == "analytics_tool",
            )
        )

        cloud_platform = self._bool_value(
            metadata.get(
                "cloud_platform",
                category == "cloud_platform",
            )
        )

        operating_system = self._bool_value(
            metadata.get(
                "operating_system",
                category == "operating_system",
            )
        )

        framework = self._bool_value(
            metadata.get(
                "framework",
                category == "framework",
            )
        )

        erp = self._bool_value(
            metadata.get(
                "erp",
                category == "erp",
            )
        )

        visualization_tool = self._bool_value(
            metadata.get(
                "visualization_tool",
                category == "visualization_tool",
            )
        )

        ################################################################
        # RETURN
        ################################################################

        return {

            ################################################################
            # TECHNOLOGY DEFINITION
            ################################################################

            "technology_family": metadata.get(
                "technology_family",
                getattr(
                    entity,
                    "technology_family",
                    "",
                ),
            ),

            "technology_group": metadata.get(
                "technology_group",
                getattr(
                    entity,
                    "technology_group",
                    "",
                ),
            ),

            "vendor": metadata.get(
                "vendor",
                getattr(
                    entity,
                    "vendor",
                    "",
                ),
            ),

            "version": metadata.get(
                "version",
                getattr(
                    entity,
                    "version",
                    "",
                ),
            ),

            "abbreviation": metadata.get(
                "abbreviation",
                getattr(
                    entity,
                    "abbreviation",
                    "",
                ),
            ),

            ################################################################
            # CLASSIFICATION
            ################################################################

            "programming_language": programming_language,

            "database": database,

            "analytics_tool": analytics_tool,

            "cloud_platform": cloud_platform,

            "operating_system": operating_system,

            "framework": framework,

            "erp": erp,

            "visualization_tool": visualization_tool,

            ################################################################
            # ENTERPRISE
            ################################################################

            "commercial": self._bool_value(
                metadata.get(
                    "commercial",
                    False,
                )
            ),

            "open_source": self._bool_value(
                metadata.get(
                    "open_source",
                    False,
                )
            ),

            "certification_available": self._bool_value(
                metadata.get(
                    "certification_available",
                    False,
                )
            ),

            "maturity_level": self._int_value(
                metadata.get(
                    "maturity_level",
                    1,
                )
            ),

            ################################################################
            # IMPACT
            ################################################################

            "impact_weight": impact_weight,

            ################################################################
            # ATS
            ################################################################

            "ats_weight": metadata.get(
                "ats_weight",
                impact_weight,
            ),

            ################################################################
            # GRAPH
            ################################################################

            "graph_node": self._bool_value(
                metadata.get(
                    "graph_node",
                    True,
                )
            ),
        }

    ####################################################################
    # BOOLEAN
    ####################################################################

    @staticmethod
    def _bool_value(
        value: Any,
    ) -> bool:
        """
        Safely convert repository/metadata values to bool.
        """

        if isinstance(
            value,
            bool,
        ):
            return value

        if isinstance(
            value,
            str,
        ):

            normalized = (
                value
                .casefold()
                .strip()
            )

            if normalized in {
                "true",
                "yes",
                "1",
            }:
                return True

            if normalized in {
                "false",
                "no",
                "0",
            }:
                return False

        return bool(value)

    ####################################################################
    # INTEGER
    ####################################################################

    @staticmethod
    def _int_value(
        value: Any,
    ) -> int:

        try:

            return int(value)

        except (
            TypeError,
            ValueError,
        ):

            return 1
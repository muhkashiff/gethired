"""
Enterprise Business KPI Parser Model
Enterprise V5
"""

from dataclasses import dataclass, field

from .base_parser_models import ParserModel


@dataclass
class BusinessKPIParserModel(ParserModel):

    ####################################################################
    # ENTITY
    ####################################################################

    entity_type: str = "business_kpi"

    ontology_name: str = "business_kpi"

    ####################################################################
    # KPI INFORMATION
    ####################################################################

    description: str = ""

    related_metrics: list[str] = field(
        default_factory=list
    )

    higher_is_better: bool = True

    impact_weight: float = 1.0

    ####################################################################
    # KNOWLEDGE GRAPH
    ####################################################################

    graph_node: bool = True

    @property
    def metric_count(self) -> int:
        """
        Number of related business metrics.
        """
        return len(self.related_metrics)
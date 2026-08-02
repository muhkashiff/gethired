"""
Builder Registry

Registers all node builders and edge builders.

Enterprise V6
"""

from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.action_node_builder import (
    ActionNodeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.metric_node_builder import (
    MetricNodeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.measurement_node_builder import (
    MeasurementNodeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.standard_node_builder import (
    StandardNodeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.skill_node_builder import (
    SkillNodeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.node_builders.domain_node_builder import (
    DomainNodeBuilder,
)

from app.intelligence.utilities.knowledge.knowledge_graph.edge_builders.action_metric_edge_builder import (
    ActionMetricEdgeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.edge_builders.action_standard_edge_builder import (
    ActionStandardEdgeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.edge_builders.action_skill_edge_builder import (
    ActionSkillEdgeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.edge_builders.metric_measurement_edge_builder import (
    MetricMeasurementEdgeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.edge_builders.action_object_edge_builder import (
    ActionObjectEdgeBuilder,
)
from app.intelligence.utilities.knowledge.knowledge_graph.edge_builders.domain_entity_edge_builder import (
    DomainEntityEdgeBuilder,
)


class BuilderRegistry:

    def __init__(self):

        self.node_builders = [

            ActionNodeBuilder(),
            MetricNodeBuilder(),
            MeasurementNodeBuilder(),
            StandardNodeBuilder(),
            SkillNodeBuilder(),
            DomainNodeBuilder(),

        ]

        self.edge_builders = [

            ActionMetricEdgeBuilder(),
            ActionStandardEdgeBuilder(),
            ActionSkillEdgeBuilder(),
            MetricMeasurementEdgeBuilder(),
            ActionObjectEdgeBuilder(),
            DomainEntityEdgeBuilder(),

        ]
"""
Enterprise Graph Constants

Centralized constants used across the
Enterprise Knowledge Graph.

Purpose
-------
Avoid hardcoded strings throughout:

- Builders
- Knowledge Graph Builder
- Validators
- Optimizers
- Reasoners

Enterprise V7
"""

from dataclasses import dataclass


# ============================================================
# NODE TYPES
# ============================================================

@dataclass(frozen=True)
class NodeTypes:

    ACTION = "action"

    OBJECT = "object"

    SKILL = "skill"

    METRIC = "metric"

    MEASUREMENT = "measurement"

    STANDARD = "standard"

    DOMAIN = "domain"

    METHODOLOGY = "methodology"

    TOOL = "tool"

    CERTIFICATION = "certification"

    PERSON = "person"

    ORGANIZATION = "organization"


# ============================================================
# EDGE RELATIONS
# ============================================================

@dataclass(frozen=True)
class EdgeRelations:

    # Existing explicit relations

    ACTION_METRIC = "ACTION_METRIC"

    ACTION_STANDARD = "ACTION_STANDARD"

    ACTION_SKILL = "ACTION_SKILL"

    ACTION_OBJECT = "ACTION_OBJECT"

    DOMAIN_ENTITY = "DOMAIN_ENTITY"

    HAS_MEASUREMENT = "HAS_MEASUREMENT"

    # Semantic relations

    BELONGS_TO = "BELONGS_TO"

    SUPPORTS = "SUPPORTS"

    USES = "USES"

    MEASURES = "MEASURES"

    ACHIEVED = "ACHIEVED"

    DEPENDS_ON = "DEPENDS_ON"

    LEADS = "LEADS"

    OWNS = "OWNS"

    COLLABORATES_WITH = "COLLABORATES_WITH"


# ============================================================
# DEFAULT VALUES
# ============================================================

@dataclass(frozen=True)
class GraphDefaults:

    DEFAULT_CONFIDENCE = 1.0

    DEFAULT_IMPACT_WEIGHT = 1.0

    UNKNOWN = "unknown"

    EMPTY = ""


# ============================================================
# GRAPH METADATA KEYS
# ============================================================

@dataclass(frozen=True)
class MetadataKeys:

    VALUE = "value"

    UNIT = "unit"

    BASELINE = "baseline"

    TARGET = "target"

    DIRECTION = "direction"

    QUANTIFIED = "quantified"

    ACHIEVEMENT_TYPE = "achievement_type"

    METRIC_ID = "metric_id"

    STANDARDS = "standards"

    METHODOLOGIES = "methodologies"

    OWNERSHIP = "ownership"

    LEADERSHIP = "leadership"

    SOURCE = "source"


# ============================================================
# GRAPH STATISTICS
# ============================================================

@dataclass(frozen=True)
class StatisticsKeys:

    NODE_COUNT = "node_count"

    EDGE_COUNT = "edge_count"

    ENTITY_COUNTS = "entity_counts"

    CATEGORY_COUNTS = "category_counts"

    DOMAIN_COUNTS = "domain_counts"

    BUSINESS_AREA_COUNTS = "business_area_counts"

    RELATION_COUNTS = "relation_counts"

    CONNECTED_COMPONENTS = "connected_components"

    DENSITY = "density"

    MAX_DEGREE = "max_degree"

    MIN_DEGREE = "min_degree"

    AVERAGE_DEGREE = "average_degree"


# ============================================================
# EXPORT SHORTCUTS
# ============================================================

NODE_TYPES = NodeTypes()

EDGE_RELATIONS = EdgeRelations()

GRAPH_DEFAULTS = GraphDefaults()

METADATA_KEYS = MetadataKeys()

STATISTICS_KEYS = StatisticsKeys()
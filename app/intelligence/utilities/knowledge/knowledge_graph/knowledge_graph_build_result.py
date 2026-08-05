"""
Enterprise Knowledge Graph Build Result

Enterprise V7

Purpose
-------
Represents the complete output of the Knowledge Graph Builder.

Acts as the contract between

    KnowledgeGraphBuilder

and

    ReasoningPipeline

This object intentionally contains ONLY build-related
information.

Reasoning intelligence belongs to ReasoningResult objects.

Enterprise Architecture

Resume
    │
    ▼
Knowledge Parser
    │
    ▼
Knowledge Facts
    │
    ▼
Knowledge Graph Builder
    │
    ▼
KnowledgeGraphBuildResult
    │
    ▼
Reasoning Pipeline
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any

from app.intelligence.utilities.knowledge.knowledge_graph.knowledge_graph import (
    KnowledgeGraph,
)

from app.intelligence.utilities.knowledge.knowledge_graph.graph_models import (
    GraphStatistics,
)


# ==========================================================
# Builder Report
# ==========================================================

@dataclass
class BuilderReport:
    """
    Execution report for a single builder.
    """

    builder_name: str = ""

    success: bool = True

    nodes_created: int = 0

    edges_created: int = 0

    execution_time: float = 0.0

    warnings: List[str] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )


# ==========================================================
# Validation Report
# ==========================================================

@dataclass
class ValidationReport:

    success: bool = True

    errors: List[str] = field(
        default_factory=list
    )

    warnings: List[str] = field(
        default_factory=list
    )

    orphan_nodes: List[str] = field(
        default_factory=list
    )

    duplicate_edges: List[str] = field(
        default_factory=list
    )

    invalid_nodes: List[str] = field(
        default_factory=list
    )

    invalid_edges: List[str] = field(
        default_factory=list
    )

    metadata: Dict = field(
        default_factory=dict
    )


# ==========================================================
# Optimization Report
# ==========================================================

@dataclass
class OptimizationReport:

    optimized: bool = False

    duplicate_edges_removed: int = 0

    metadata_normalized: int = 0

    nodes_sorted: bool = False

    edges_sorted: bool = False

    execution_time: float = 0.0

    metadata: Dict = field(
        default_factory=dict
    )


# ==========================================================
# Knowledge Graph Build Result
# ==========================================================

@dataclass
class KnowledgeGraphBuildResult:

    ##########################################################
    # Core Graph
    ##########################################################

    graph: KnowledgeGraph 

    ##########################################################
    # Statistics
    ##########################################################

    statistics: GraphStatistics = field(
        default_factory=GraphStatistics
    )

    ##########################################################
    # Builder Reports
    ##########################################################

    builder_reports: List[BuilderReport] = field(
        default_factory=list
    )

    ##########################################################
    # Validation
    ##########################################################

    validation_report: ValidationReport = field(
        default_factory=ValidationReport
    )

    ##########################################################
    # Optimization
    ##########################################################

    optimization_report: OptimizationReport = field(
        default_factory=OptimizationReport
    )

    ##########################################################
    # Build Quality
    ##########################################################

    success: bool = True

    confidence: float = 1.0

    execution_time: float = 0.0

    ##########################################################
    # Messages
    ##########################################################

    warnings: List[str] = field(
        default_factory=list
    )

    errors: List[str] = field(
        default_factory=list
    )

    ##########################################################
    # Metadata
    ##########################################################

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
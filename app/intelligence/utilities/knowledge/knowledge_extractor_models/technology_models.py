"""
Enterprise Technology Knowledge Model

Represents Technologies extracted from text.

Examples

Python
SQL
Power BI
Tableau
SAP
Oracle
Docker
PostgreSQL
Azure
Excel
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class Technology(KnowledgeEntity):

    ####################################################################
    # Entity
    ####################################################################

    entity_type: str = "technology"

    ontology_name: str = "technologies"

    ####################################################################
    # Technology Definition
    ####################################################################

    technology_family: str = ""

    technology_group: str = ""

    vendor: str = ""

    version: str = ""

    abbreviation: str = ""

    ####################################################################
    # Classification
    ####################################################################

    programming_language: bool = False

    database: bool = False

    analytics_tool: bool = False

    cloud_platform: bool = False

    operating_system: bool = False

    framework: bool = False

    erp: bool = False

    visualization_tool: bool = False

    ####################################################################
    # Enterprise
    ####################################################################

    commercial: bool = False

    open_source: bool = False

    certification_available: bool = False

    maturity_level: int = 1

    ####################################################################
    # Knowledge Graph
    ####################################################################

    graph_node: bool = True

    ats_weight: float = 1.0
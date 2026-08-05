"""
Enterprise Reasoning Context

Enterprise V7

Purpose
-------
Shared context object passed between all reasoners.

Instead of passing

graph,
dependency_result,
ontology_result,
skill_result,
...

every reasoner receives ONE object.
"""

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ReasoningContext:

    ####################################################################
    # INPUT GRAPH
    ####################################################################

    graph: Any = None

    ####################################################################
    # PARSER OUTPUT
    ####################################################################

    parsed_resume: Any = None

    ####################################################################
    # KNOWLEDGE EXTRACTION
    ####################################################################

    ontology_reasoning: Any = None

    dependency_reasoning: Any = None

    ####################################################################
    # INTELLIGENCE LAYERS
    ####################################################################

    skill_reasoning: Any = None

    achievement_reasoning: Any = None

    leadership_reasoning: Any = None

    executive_reasoning: Any = None

    recommendation_reasoning: Any = None

    ####################################################################
    # GLOBAL CONFIGURATION
    ####################################################################

    configuration: Dict = field(
        default_factory=dict
    )

    ####################################################################
    # SHARED CACHE
    ####################################################################

    cache: Dict = field(
        default_factory=dict
    )

    ####################################################################
    # PIPELINE METADATA
    ####################################################################

    metadata: Dict = field(
        default_factory=dict
    )

    ####################################################################
    # DIAGNOSTICS
    ####################################################################

    diagnostics: Dict = field(
        default_factory=dict
    )
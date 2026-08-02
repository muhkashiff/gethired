"""
Enterprise Knowledge Relation Models

Defines graph relationships between extracted entities.

Used by

• Relation Engine
• Knowledge Graph
• Knowledge Interpreter
• Narrative Builder
• ATS Intelligence

Enterprise V5
"""

from dataclasses import dataclass, field
from typing import Dict


# ==========================================================
# Knowledge Relation
# ==========================================================

@dataclass
class KnowledgeRelation:
    """
    Represents a semantic relationship between two entities.

    Example

        Implement
            ──acts_on──► HACCP

        HACCP
            ──belongs_to──► Food Safety

        Yield
            ──measured_by──► 99%
    """

    # ---------------------------------------------------------
    # Detection
    # ---------------------------------------------------------

    found: bool = False

    confidence: float = 0.0

    # ---------------------------------------------------------
    # Graph
    # ---------------------------------------------------------

    source_id: str = ""

    source_name: str = ""

    source_type: str = ""

    relation: str = ""

    target_id: str = ""

    target_name: str = ""

    target_type: str = ""

    # ---------------------------------------------------------
    # Business
    # ---------------------------------------------------------

    business_area: str = ""

    importance: float = 1.0

    # ---------------------------------------------------------
    # Explainability
    # ---------------------------------------------------------

    reasoning: str = ""

    source: str = "rule"

    metadata: Dict = field(default_factory=dict)
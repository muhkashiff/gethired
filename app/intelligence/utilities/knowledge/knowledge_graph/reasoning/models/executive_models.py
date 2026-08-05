"""
Executive Reasoning Models
"""

from dataclasses import dataclass, field
from typing import Dict, List


# ==========================================================
# Executive Reasoning Result
# ==========================================================

@dataclass
class ExecutiveReasoningResult:

    # -------------------------------------------------
    # Final Executive Score
    # -------------------------------------------------

    executive_score: float = 0.0

    executive_level: str = ""

    confidence: float = 0.0

    # -------------------------------------------------
    # Executive Dimensions
    # -------------------------------------------------

    strategic_thinking: float = 0.0

    organizational_impact: float = 0.0

    business_transformation: float = 0.0

    commercial_leadership: float = 0.0

    financial_leadership: float = 0.0

    operational_excellence: float = 0.0

    people_leadership: float = 0.0

    governance: float = 0.0

    board_readiness: float = 0.0

    innovation: float = 0.0

    # -------------------------------------------------
    # Explainability
    # -------------------------------------------------

    evidence: List[str] = field(default_factory=list)

    executive_actions: Dict[str, int] = field(default_factory=dict)

    dimensions: Dict[str, float] = field(default_factory=dict)

    metadata: Dict = field(default_factory=dict)
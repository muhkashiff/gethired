from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class LeadershipSummary:

    overall_score: float = 0.0

    strongest_dimensions: List[str] = field(default_factory=list)

    weakest_dimensions: List[str] = field(default_factory=list)

    executive_level: str = ""

    readiness: str = ""

    dimension_scores: Dict[str, float] = field(default_factory=dict)

    evidence: Dict[str, List[str]] = field(default_factory=dict)

    summary: str = ""

    confidence: float = 0.0
from dataclasses import dataclass, field
from typing import List


@dataclass
class CareerProgression:

    promotion_count: int = 0

    promotion_velocity: float = 0.0

    career_growth_score: float = 0.0

    stability_score: float = 0.0

    trend: str = ""

    highest_level: str = ""

    executive_potential: float = 0.0

    years_experience: float = 0.0

    title_history: List[str] = field(default_factory=list)

    confidence: float = 0.0
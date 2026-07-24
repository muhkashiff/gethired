from dataclasses import dataclass, field
from typing import List


@dataclass
class MatchResult:

    overall_score: float = 0.0

    skill_score: float = 0.0

    experience_score: float = 0.0

    education_score: float = 0.0

    certification_score: float = 0.0

    technology_score: float = 0.0

    industry_score: float = 0.0

    matched_skills: List[str] = field(default_factory=list)

    missing_skills: List[str] = field(default_factory=list)

    recommendations: List[str] = field(default_factory=list)
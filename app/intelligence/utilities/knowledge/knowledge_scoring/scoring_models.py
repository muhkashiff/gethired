"""
Scoring Models

Universal scoring objects used throughout
the GetHired Intelligence Engine.

Every scoring engine returns one of these.

Leadership
Seniority
Executive
Resume
Skill
Future ML Scores

all become compatible.
"""

from dataclasses import dataclass, field
from typing import Dict


# ---------------------------------------------------------
# Generic Score
# ---------------------------------------------------------

@dataclass
class KnowledgeScore:

    name: str = ""

    score: float = 0.0

    confidence: float = 1.0

    level: str = ""

    reasoning: Dict = field(default_factory=dict)


# ---------------------------------------------------------
# Resume Score
# ---------------------------------------------------------

@dataclass
class ResumeScore:

    overall_score: float = 0.0

    confidence: float = 1.0

    grade: str = ""

    executive_ready: bool = False

    reasoning: Dict = field(default_factory=dict)

    component_scores: Dict[str, KnowledgeScore] = field(default_factory=dict)
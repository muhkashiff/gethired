"""
Enterprise Prediction Models

Enterprise V12
"""

from dataclasses import dataclass, field


@dataclass
class SeniorityPrediction:

    level: str = ""

    score: float = 0.0

    confidence: float = 1.0

    reasoning: list[str] = field(default_factory=list)


@dataclass
class ExecutivePrediction:

    ready: bool = False

    score: float = 0.0

    confidence: float = 1.0

    reasoning: list[str] = field(default_factory=list)


@dataclass
class CareerPrediction:

    career_level: str = ""

    score: float = 0.0

    confidence: float = 1.0

    reasoning: list[str] = field(default_factory=list)
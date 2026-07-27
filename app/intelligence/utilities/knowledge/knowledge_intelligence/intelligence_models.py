"""
Resume Intelligence Models
"""

from dataclasses import dataclass, field


@dataclass
class IntelligenceResult:

    title: str = ""

    score: float = 0.0

    confidence: float = 0.0

    findings: list = field(default_factory=list)

    strengths: list = field(default_factory=list)

    weaknesses: list = field(default_factory=list)

    recommendations: list = field(default_factory=list)


@dataclass
class ResumeIntelligence:

    leadership: IntelligenceResult = field(default_factory=IntelligenceResult)

    quality: IntelligenceResult = field(default_factory=IntelligenceResult)

    food_safety: IntelligenceResult = field(default_factory=IntelligenceResult)

    operations: IntelligenceResult = field(default_factory=IntelligenceResult)

    manufacturing: IntelligenceResult = field(default_factory=IntelligenceResult)

    achievements: IntelligenceResult = field(default_factory=IntelligenceResult)

    overall_score: float = 0.0
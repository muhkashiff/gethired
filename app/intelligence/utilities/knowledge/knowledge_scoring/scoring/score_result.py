from dataclasses import dataclass, field


@dataclass
class ScoreResult:

    category: str = ""

    raw_score: float = 0.0

    normalized_score: float = 0.0

    weight: float = 1.0

    confidence: float = 1.0

    details: dict = field(default_factory=dict)

    metadata: dict = field(default_factory=dict)
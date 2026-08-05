from dataclasses import dataclass, field


@dataclass
class CapabilityEvidence:

    capability: str = ""

    score: float = 0.0

    entities: list[str] = field(default_factory=list)

    relations: list[str] = field(default_factory=list)
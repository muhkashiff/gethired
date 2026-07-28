"""
Domain Knowledge Model

Represents the business domain assigned
to a clause or achievement.

Examples

Food Safety
Quality
Manufacturing
Operations
Supply Chain
Leadership
"""

from dataclasses import dataclass, field


@dataclass
class DomainKnowledge:

    found: bool = False

    confidence: float = 0.0

    entity_id: str = ""

    domain: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    source: str = "ontology"

    metadata: dict = field(default_factory=dict)

    reasoning: str = ""
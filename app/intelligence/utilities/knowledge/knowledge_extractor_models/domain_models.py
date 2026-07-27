"""
Domain Knowledge Model
"""

from dataclasses import dataclass, field


@dataclass
class DomainKnowledge:

    found: bool = False

    # Canonical ontology ID
    entity_id: str = ""

    # Human readable domain
    domain: str = ""

    # Business area
    business_area: str = ""

    # Why the reasoner selected this domain
    reasoning: str = ""

    confidence: float = 0.0

    source: str = "ontology"

    metadata: dict = field(default_factory=dict)
"""
Object Knowledge Model

Represents a business object detected in a sentence.

Examples

FSSC 22000
ISO 9001
Production Yield
Supplier
Customer Complaints
Facility
"""

from dataclasses import dataclass, field


@dataclass
class ObjectKnowledge:

    # ---------------------------------------------------------
    # Detection
    # ---------------------------------------------------------

    found: bool = False

    confidence: float = 0.0

    # ---------------------------------------------------------
    # Linguistic
    # ---------------------------------------------------------

    original: str = ""

    canonical: str = ""

    category: str = ""

    # ---------------------------------------------------------
    # Ontology
    # ---------------------------------------------------------

    entity_id: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    source: str = ""

    metadata: dict = field(default_factory=dict)
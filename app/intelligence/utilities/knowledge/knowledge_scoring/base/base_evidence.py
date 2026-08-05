"""
Evidence Base

Enterprise V12

Every Reasoner produces an Evidence object.

Examples

DomainEvidence
TechnicalEvidence
LeadershipEvidence
AchievementEvidence
ExecutiveEvidence

All inherit from EvidenceBase.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


# ==========================================================
# Evidence Item
# ==========================================================

@dataclass
class EvidenceItem:
    """
    One discovered piece of evidence.
    """

    name: str = ""

    confidence: float = 0.0

    weight: float = 1.0

    frequency: int = 1

    source_entities: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


# ==========================================================
# Evidence Base
# ==========================================================

@dataclass
class EvidenceBase:
    """
    Parent class for every evidence object.
    """

    evidence_type: str = ""

    confidence: float = 0.0

    primary_domain: str = ""

    summary: str = ""

    items: List[EvidenceItem] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------------------------------
    # Utility
    # -----------------------------------------------------

    def add(self, item: EvidenceItem):

        self.items.append(item)

    # -----------------------------------------------------

    def sort(self):

        self.items.sort(

            key=lambda x: (

                x.weight,

                x.confidence,

                x.frequency,

            ),

            reverse=True,

        )

    # -----------------------------------------------------

    def top(self, n=5):

        self.sort()

        return self.items[:n]

    # -----------------------------------------------------

    def count(self):

        return len(self.items)

    # -----------------------------------------------------

    def total_weight(self):

        return round(

            sum(

                item.weight

                for item in self.items

            ),

            2,

        )

    # -----------------------------------------------------

    def average_confidence(self):

        if not self.items:

            return 0.0

        return round(

            sum(

                item.confidence

                for item in self.items

            ) / len(self.items),

            2,

        )
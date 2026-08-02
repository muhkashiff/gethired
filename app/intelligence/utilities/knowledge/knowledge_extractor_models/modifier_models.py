"""
Enterprise Modifier Knowledge Model

Represents semantic modifiers.

Examples

Reduced
Increased
Successfully
Significantly
Approximately
"""

from dataclasses import dataclass

from .base_models import KnowledgeEntity


@dataclass
class ModifierKnowledge(KnowledgeEntity):

    """
    Modifier Entity

    Used for semantic interpretation.
    """

    modifier_type: str = ""

    polarity: str = ""

    intensity: float = 1.0

    direction: str = ""
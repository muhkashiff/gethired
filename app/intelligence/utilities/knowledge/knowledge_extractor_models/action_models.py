"""
Action Knowledge Model

Represents an action (verb) identified in a sentence.

Used by

- Sentence Parser
- Clause Parser
- Knowledge Interpreter
- Narrative Builder
- ATS Intelligence
- Knowledge Graph
"""

from dataclasses import dataclass, field


@dataclass
class ActionKnowledge:
    """
    Represents one detected action.

    Example

        Led cross-functional teams

    original = "led"
    base = "lead"
    gerund = "leading"
    """

    # ---------------------------------------------------------
    # Detection
    # ---------------------------------------------------------

    found: bool = False

    confidence: float = 0.0

    # ---------------------------------------------------------
    # Linguistics
    # ---------------------------------------------------------

    original: str = ""

    base: str = ""

    gerund: str = ""

    category: str = ""

    # ---------------------------------------------------------
    # Ontology
    # ---------------------------------------------------------

    entity_id: str = ""

    business_area: str = ""

    impact_weight: float = 1.0

    source: str = ""

    metadata: dict = field(default_factory=dict)

    # ---------------------------------------------------------
    # Position Information
    # ---------------------------------------------------------

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    sentence_index: int = 0

    # ---------------------------------------------------------
    # Parsing Flags
    # ---------------------------------------------------------

    clause_candidate: bool = True
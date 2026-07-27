"""
Action Knowledge Model

Represents an action (verb) identified in a sentence.

Used by:
- Sentence Parser
- Clause Parser
- Knowledge Interpreter
- Narrative Builder
- ATS Intelligence
"""

from dataclasses import dataclass


@dataclass
class ActionKnowledge:
    """
    Represents one action detected inside a sentence.

    Example:

        "Led cross-functional teams"

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
    # Position Information
    # (Used by Clause Parser)
    # ---------------------------------------------------------

    start_char: int = -1

    end_char: int = -1

    token_index: int = -1

    sentence_index: int = 0

    entity_id: str = ""

    # ---------------------------------------------------------
    # Parsing Flags
    # ---------------------------------------------------------

    clause_candidate: bool = True
"""
Domain Reasoner

Combines Action + Object
to determine business domain.
"""

import json
from pathlib import Path

from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import (
    DomainKnowledge,
)


class DomainReasoner:

    def __init__(self):

        path = (

            Path(__file__).resolve().parent.parent
            / "knowledge_knowledge"
            / "data"
            / "domain_reasoning.json"

        )

        with open(path, encoding="utf8") as f:

            self.rules = json.load(f)

    # ---------------------------------------------------------

    def reason(

        self,

        action,

        obj

    ):

        if not action.found:

            return DomainKnowledge()

        if not obj.found:

            return DomainKnowledge()

        category = action.category

        object_type = obj.category

        if category not in self.rules:

            return DomainKnowledge(

                found=True,

                domain=object_type,

                reasoning="Object only",

                confidence=0.60

            )

        mapping = self.rules[category]

        if object_type not in mapping:

            return DomainKnowledge(

                found=True,

                domain=object_type,

                reasoning="Object only",

                confidence=0.70

            )

        return DomainKnowledge(

            found=True,

            domain=mapping[object_type],

            reasoning=f"{category} + {object_type}",

            confidence=0.95

        )
"""
Enterprise Universal Ontology Entity

Enterprise V5
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RepositoryEntity:

    ####################################################################
    # Core Identity
    ####################################################################

    entity_id: str = ""

    canonical: str = ""

    normalized: str = ""

    aliases: list[str] = field(
        default_factory=list
    )

    ####################################################################
    # Linguistic Forms
    ####################################################################

    base: str = ""

    past: str = ""

    gerund: str = ""

    plural: str = ""

    singular: str = ""

    abbreviation: str = ""

    short_name: str = ""

    ####################################################################
    # Classification
    ####################################################################

    category: str = ""

    entity_type: str = ""

    ontology_name: str = ""

    ####################################################################
    # Business Classification
    ####################################################################

    domain: str = ""

    business_area: str = ""

    description: str = ""

    ####################################################################
    # Business Behaviour
    ####################################################################

    impact_weight: float = 1.0

    business_meaning: str = ""

    preferred_direction: str = ""

    preferred_unit: str = ""

    higher_is_better: bool = True

    ####################################################################
    # Matching
    ####################################################################

    searchable: bool = True

    active: bool = True

    ####################################################################
    # Source
    ####################################################################

    source: str = "ontology"

    metadata: dict = field(
        default_factory=dict
    )

    ####################################################################
    # MATCHING
    ####################################################################

    def matches_text(
        self,
        value: str,
    ) -> bool:
        """
        Determine whether the supplied text represents this entity.

        Matching is performed against every valid linguistic
        representation stored by the ontology.

        This keeps linguistic knowledge inside the repository entity
        rather than inside the Matcher.
        """

        candidate = self._normalize(
            value
        )

        if not candidate:
            return False

        for form in self.text_forms():

            if self._normalize(form) == candidate:
                return True

        return False

    ####################################################################

    def text_forms(self) -> tuple[str, ...]:
        """
        Return all valid textual representations of this entity.
        """

        forms = [
            self.canonical,
            self.normalized,
            self.base,
            self.past,
            self.gerund,
            self.plural,
            self.singular,
            self.abbreviation,
            self.short_name,
        ]

        forms.extend(
            self.aliases
        )

        return tuple(
            form
            for form in forms
            if isinstance(form, str)
            and form.strip()
        )

    ####################################################################

    @staticmethod
    def _normalize(
        value: str,
    ) -> str:
        """
        Normalize text for repository matching.
        """

        return " ".join(
            value.casefold().split()
        )
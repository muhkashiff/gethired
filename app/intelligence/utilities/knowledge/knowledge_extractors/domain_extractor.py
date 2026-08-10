from app.intelligence.utilities.knowledge.repository_v5.repository import (Repository,)

from app.intelligence.utilities.knowledge.knowledge_extractor_models.domain_models import (
    DomainKnowledge,
)


class DomainExtractor:

    ####################################################################
    # INITIALIZATION
    ####################################################################

    def __init__(self, repository=None):

        self.repository = repository or Repository()

    ####################################################################
    # MAIN EXTRACTION
    ####################################################################

    def extract(self, sentence):

        ################################################################
        # Validate input
        ################################################################

        if sentence is None:

            return DomainKnowledge()

        if not isinstance(sentence, str):

            return DomainKnowledge()

        sentence = sentence.strip()

        if not sentence:

            return DomainKnowledge()

        ################################################################
        # Resolve Domain
        ################################################################

        domain = self.repository.find_entity(
            "domains",
            sentence,
        )

        if domain is None:

            return DomainKnowledge()

        ################################################################
        # Resolve Domain Reasoning
        ################################################################

        reasoning = self.repository.find_entity(
            "domain_reasoning",
            domain.canonical,
        )

        ################################################################
        # Default Reasoning Values
        ################################################################

        reasoning_id = ""

        reasoning_confidence = 0.0

        primary_domain = ""

        secondary_domains = []

        trigger_actions = []

        trigger_objects = []

        trigger_skills = []

        trigger_metrics = []

        trigger_certifications = []

        ################################################################
        # Extract Reasoning Metadata
        ################################################################

        if reasoning is not None:

            metadata = getattr(
                reasoning,
                "metadata",
                {},
            )

            if not isinstance(
                metadata,
                dict,
            ):

                metadata = {}

            reasoning_id = metadata.get(
                "reasoning_id",
                "",
            )

            reasoning_confidence = float(
                metadata.get(
                    "confidence",
                    0.0,
                )
                or 0.0
            )

            primary_domain = metadata.get(
                "primary_domain",
                "",
            )

            secondary_domains = list(
                metadata.get(
                    "secondary_domains",
                    [],
                )
                or []
            )

            trigger_actions = list(
                metadata.get(
                    "trigger_actions",
                    [],
                )
                or []
            )

            trigger_objects = list(
                metadata.get(
                    "trigger_objects",
                    [],
                )
                or []
            )

            trigger_skills = list(
                metadata.get(
                    "trigger_skills",
                    [],
                )
                or []
            )

            trigger_metrics = list(
                metadata.get(
                    "trigger_metrics",
                    [],
                )
                or []
            )

            trigger_certifications = list(
                metadata.get(
                    "trigger_certifications",
                    [],
                )
                or []
            )

        ################################################################
        # Domain Classification
        ################################################################

        metadata = getattr(
            domain,
            "metadata",
            {},
        )

        if not isinstance(
            metadata,
            dict,
        ):

            metadata = {}

        ################################################################
        # Return Knowledge Object
        ################################################################

        return DomainKnowledge(

            ################################################################
            # Detection
            ################################################################

            found=True,

            confidence=0.99,

            original=sentence,

            canonical=domain.canonical,

            normalized=domain.normalized,

            ################################################################
            # Repository Entity
            ################################################################

            entity_id=domain.entity_id,

            entity_type="domain",

            ontology_name="domains",

            category=domain.category,

            business_area=domain.business_area,

            domain=domain.domain,

            impact_weight=domain.impact_weight,

            source=domain.source,

            metadata=metadata,

            ################################################################
            # Domain
            ################################################################

            domain_object=domain,

            ################################################################
            # Classification
            ################################################################

            strategic=bool(
                metadata.get(
                    "strategic",
                    False,
                )
            ),

            operational=bool(
                metadata.get(
                    "operational",
                    False,
                )
            ),

            technical=bool(
                metadata.get(
                    "technical",
                    False,
                )
            ),

            compliance=bool(
                metadata.get(
                    "compliance",
                    False,
                )
            ),

            management=bool(
                metadata.get(
                    "management",
                    False,
                )
            ),

            ################################################################
            # Enterprise
            ################################################################

            enterprise_level=int(
                metadata.get(
                    "enterprise_level",
                    1,
                )
                or 1
            ),

            criticality=float(
                metadata.get(
                    "criticality",
                    1.0,
                )
                or 1.0
            ),

            ################################################################
            # Reasoning
            ################################################################

            reasoning_id=reasoning_id,

            reasoning_object=reasoning,

            reasoning_confidence=reasoning_confidence,

            ################################################################
            # Reasoning Relationships
            ################################################################

            primary_domain=primary_domain,

            secondary_domains=secondary_domains,

            trigger_actions=trigger_actions,

            trigger_objects=trigger_objects,

            trigger_skills=trigger_skills,

            trigger_metrics=trigger_metrics,

            trigger_certifications=trigger_certifications,

        )
"""
Object Merger

Creates meaningful business objects by merging related ontology
entities into one semantic business object.

Example

GMP + Food Safety

↓

Food Safety Standards

Example

Water + Treatment + Plant

↓

Water Treatment Plant
"""

from copy import deepcopy


class ObjectMerger:

    """
    Merge related object entities.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def merge(self, resolution):

        entities = resolution.entities

        objects = [

            e

            for e in entities

            if e.entity_type.lower() == "object"

        ]

        domains = [

            e

            for e in entities

            if e.entity_type.lower() == "domain"

        ]

        standards = [

            e

            for e in entities

            if e.entity_type.lower() == "standard"

        ]

        if not objects:
            return resolution

        # ---------------------------------------------
        # Merge object with matching domain
        # ---------------------------------------------

        for obj in objects:

            for domain in domains:

                if (

                    domain.business_area

                    and

                    obj.business_area

                    and

                    domain.business_area == obj.business_area

                ):

                    obj.metadata.setdefault(

                        "related_domains",

                        []

                    ).append(

                        domain.entity_id

                    )

        # ---------------------------------------------
        # Attach standards
        # ---------------------------------------------

        for obj in objects:

            for standard in standards:

                obj.metadata.setdefault(

                    "related_standards",

                    []

                ).append(

                    standard.entity_id

                )

        return resolution
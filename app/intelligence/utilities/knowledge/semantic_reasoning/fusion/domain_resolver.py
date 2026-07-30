"""
Domain Resolver

Resolves the final business domain after extraction.

Example

Action

    Implement

Object

    GMP

↓

Food Safety


Example

Action

    Improve

Metric

    Production Yield

↓

Manufacturing
"""


class DomainResolver:

    """
    Determines the strongest business domain.
    """

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def resolve(self, resolution):

        domains = [

            entity

            for entity in resolution.entities

            if entity.entity_type.lower() == "domain"

        ]

        if not domains:
            return resolution

        # Highest confidence wins

        best = max(

            domains,

            key=lambda d: d.confidence,

        )

        resolution.metadata["primary_domain"] = best.entity_id

        resolution.metadata["primary_business_area"] = (

            best.business_area

        )

        return resolution
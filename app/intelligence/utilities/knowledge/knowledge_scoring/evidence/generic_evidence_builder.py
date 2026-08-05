"""
Enterprise Generic Evidence Builder

Enterprise V12

Capability Evidence
        ↓
Mapping
        ↓
Typed Evidence Model

This builder replaces all individual evidence builders
(Domain, Technical, Leadership, Executive, Business Value, ATS).

Author: Enterprise V12
"""

from dataclasses import fields


class GenericEvidenceBuilder:

    def __init__(self):
        pass

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def build(

        self,

        capability_evidence,

        mapping,

        evidence_cls,

    ):
        """
        Build one typed Evidence object.

        Parameters
        ----------
        capability_evidence

            Dict[str, CapabilityEvidence]

        mapping

            Dict[str, str]

            Capability -> Evidence Bucket

        evidence_cls

            DomainEvidence
            TechnicalEvidence
            LeadershipEvidence
            ExecutiveEvidence
            BusinessValueEvidence
            ATSEvidence

        Returns
        -------
        evidence_cls
        """

        # ------------------------------------------
        # Create typed evidence object
        # ------------------------------------------

        evidence = evidence_cls()

        # ------------------------------------------
        # Populate evidence buckets
        # ------------------------------------------

        for capability_name, capability in capability_evidence.items():

            bucket = mapping.get(capability_name)

            if bucket is None:
                continue

            # Ignore invalid mapping buckets
            if not hasattr(evidence, bucket):
                continue

            current_value = getattr(

                evidence,

                bucket,

            )

            setattr(

                evidence,

                bucket,

                current_value + capability.score,

            )

        # ------------------------------------------
        # Calculate Total Score
        # ------------------------------------------

        evidence.total_score = self._calculate_total(

            evidence,

        )

        return evidence

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _calculate_total(

        self,

        evidence,

    ) -> float:
        """
        Calculates the total evidence score by summing all numeric
        evidence fields except bookkeeping fields.
        """

        total = 0.0

        for field in fields(evidence):

            if field.name in (

                "total_score",

                "metadata",

            ):

                continue

            value = getattr(

                evidence,

                field.name,

            )

            if isinstance(

                value,

                (int, float),

            ):

                total += value

        return round(total, 2)
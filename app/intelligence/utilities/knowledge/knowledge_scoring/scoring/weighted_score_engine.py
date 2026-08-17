from dataclasses import fields, is_dataclass

from .score_result import ScoreResult
from .score_engine_base import ScoreEngineBase


class WeightedScoreEngine(ScoreEngineBase):

    def __init__(
        self,
        category,
        weights=None,
        maximum_score=100,
    ):

        self.category = category

        self.weights = (
            weights
            or {}
        )

        self.maximum_score = (
            maximum_score
        )

    # ============================================================
    # SCORE
    # ============================================================

    def score(
        self,
        evidence,
    ):
        """
        Calculate a weighted score from a typed Evidence object.

        Supported evidence architecture:

            DomainEvidence
            TechnicalEvidence
            LeadershipEvidence
            ExecutiveEvidence
            BusinessValueEvidence
            ATSEvidence

        The GenericEvidenceBuilder stores capability scores directly
        in the typed evidence dataclass fields.

        Therefore this engine does NOT require:

            evidence.scores

        Bookkeeping fields such as total_score and metadata are ignored.
        """

        if evidence is None:

            return ScoreResult(

                category=self.category,

                raw_score=0.0,

                normalized_score=0.0,

                weight=1.0,

                confidence=0.0,

                details={},

            )

        details = {}

        raw_score = 0.0

        # ============================================================
        # EXTRACT NUMERIC EVIDENCE BUCKETS
        # ============================================================

        buckets = self._extract_buckets(
            evidence
        )

        # ============================================================
        # WEIGHTED CONTRIBUTIONS
        # ============================================================

        for bucket, value in buckets.items():

            weight = self.weights.get(
                bucket,
                1.0,
            )

            try:

                value = float(value)

            except (
                TypeError,
                ValueError,
            ):

                continue

            try:

                weight = float(weight)

            except (
                TypeError,
                ValueError,
            ):

                weight = 1.0

            contribution = (
                value * weight
            )

            details[bucket] = round(
                contribution,
                2,
            )

            raw_score += contribution

        # ============================================================
        # NORMALIZE
        # ============================================================

        normalized = min(

            raw_score,

            self.maximum_score,

        )

        # ============================================================
        # CONFIDENCE
        # ============================================================

        confidence = self._calculate_confidence(
            evidence
        )

        # ============================================================
        # RESULT
        # ============================================================

        return ScoreResult(

            category=self.category,

            raw_score=round(
                raw_score,
                2,
            ),

            normalized_score=round(
                normalized,
                2,
            ),

            weight=1.0,

            confidence=confidence,

            details=details,

        )

    # ============================================================
    # EXTRACT TYPED EVIDENCE BUCKETS
    # ============================================================

    def _extract_buckets(
        self,
        evidence,
    ) -> dict:
        """
        Extract numeric scoring fields from a typed Evidence model.

        Preferred architecture:

            dataclass fields
                ↓
            numeric capability buckets

        Excluded:

            total_score
            metadata

        This keeps the scoring engine independent from the exact
        Evidence subclass.
        """

        # --------------------------------------------------------
        # Preferred: dataclass-based evidence models
        # --------------------------------------------------------

        if is_dataclass(
            evidence
        ):

            buckets = {}

            for field in fields(
                evidence
            ):

                field_name = (
                    field.name
                )

                # ----------------------------------------------
                # Bookkeeping fields
                # ----------------------------------------------

                if field_name in {
                    "total_score",
                    "metadata",
                }:

                    continue

                value = getattr(
                    evidence,
                    field_name,
                    None,
                )

                # ----------------------------------------------
                # Only numeric fields participate
                # ----------------------------------------------

                if isinstance(
                    value,
                    (int, float),
                ):

                    buckets[
                        field_name
                    ] = value

            return buckets

        # --------------------------------------------------------
        # Backward compatibility
        # --------------------------------------------------------

        scores = getattr(
            evidence,
            "scores",
            None,
        )

        if isinstance(
            scores,
            dict,
        ):

            return dict(
                scores
            )

        return {}

    # ============================================================
    # CONFIDENCE
    # ============================================================

    def _calculate_confidence(
        self,
        evidence,
    ) -> float:
        """
        Calculate evidence confidence.

        Current Enterprise V12 evidence models do not appear to
        expose a dedicated confidence field, so the engine keeps
        the established behavior of full confidence.

        If a future evidence model exposes confidence, it will
        automatically be respected.
        """

        confidence = getattr(
            evidence,
            "confidence",
            None,
        )

        if confidence is None:

            return 1.0

        try:

            confidence = float(
                confidence
            )

        except (
            TypeError,
            ValueError,
        ):

            return 1.0

        return min(
            max(
                confidence,
                0.0,
            ),
            1.0,
        )
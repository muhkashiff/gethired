"""
Enterprise V5 — Resume Structural Validation
"""

from __future__ import annotations


class ResumeValidationError(
    RuntimeError
):
    pass


class ResumeValidator:

    def validate(
        self,
        resume,
    ):

        errors = []
        warnings = []

        # ============================================================
        # EXPERIENCE
        # ============================================================

        for idx, exp in enumerate(
            getattr(
                resume,
                "experience",
                [],
            )
        ):

            if not exp.title:

                errors.append(
                    f"experience[{idx}] missing title"
                )

            if self._looks_like_location(
                exp.title
            ):

                errors.append(
                    f"experience[{idx}] title "
                    f"contains location-like value: "
                    f"{exp.title!r}"
                )

            if not (
                exp.company
                or exp.location
            ):

                warnings.append(
                    f"experience[{idx}] has no "
                    f"company/location"
                )

            if not exp.start_date:

                warnings.append(
                    f"experience[{idx}] missing start date"
                )

        # ============================================================
        # EDUCATION
        # ============================================================

        for idx, edu in enumerate(
            getattr(
                resume,
                "education",
                [],
            )
        ):

            if not edu.degree:

                errors.append(
                    f"education[{idx}] missing degree"
                )

            if self._looks_like_description(
                edu.degree
            ):

                errors.append(
                    f"education[{idx}] description "
                    f"was incorrectly promoted to degree"
                )

        # ============================================================
        # CONTACT
        # ============================================================

        if not getattr(
            resume,
            "name",
            "",
        ):

            warnings.append(
                "name not detected"
            )

        # ============================================================
        # RESULT
        # ============================================================

        valid = not errors

        return {
            "valid": valid,
            "errors": errors,
            "warnings": warnings,
        }

    def _looks_like_location(
        self,
        value,
    ):

        low = value.lower()

        return any(
            x in low
            for x in (
                "canada",
                "pakistan",
                "ontario",
                "lahore",
                "toronto",
                "brampton",
                "vancouver",
                "punjab",
            )
        )

    def _looks_like_description(
        self,
        value,
    ):

        if len(value) < 80:
            return False

        return any(
            word in value.lower()
            for word in (
                "verified by",
                "completed",
                "gained",
                "focused on",
                "curriculum",
                "experience in",
                "specializing in",
            )
        )
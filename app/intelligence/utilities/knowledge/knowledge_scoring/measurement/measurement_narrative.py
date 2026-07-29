"""
Measurement Narrative

Generates executive-quality narratives from
MeasurementKnowledge objects.

Used by

    Achievement Engine
    Resume Generator
    Cover Letter Generator
    LinkedIn Generator
    Executive Summary
"""

from dataclasses import dataclass


@dataclass
class MeasurementNarrative:

    short: str = ""

    executive: str = ""

    resume: str = ""

    linkedin: str = ""

    cover_letter: str = ""


class MeasurementNarrativeBuilder:

    # ---------------------------------------------------------

    def build(self, measurement):

        narrative = MeasurementNarrative()

        if not measurement.found:
            return narrative

        metric = measurement.metric
        direction = measurement.direction or "changed"

        # -------------------------------------------------
        # Range Measurement
        # -------------------------------------------------

        if measurement.measurement_type == "range":

            start = measurement.from_value
            end = measurement.to_value

            unit = measurement.unit

            short = (

                f"{metric} "

                f"{direction}d "

                f"from "

                f"{start:g}{unit} "

                f"to "

                f"{end:g}{unit}"

            )

            if measurement.percent_change is not None:

                executive = (

                    f"{metric} "

                    f"{direction}d "

                    f"from "

                    f"{start:g}{unit} "

                    f"to "

                    f"{end:g}{unit}, "

                    f"representing "

                    f"{measurement.percent_change:.2f}% "

                    f"relative improvement."

                )

            else:

                executive = short

        # -------------------------------------------------
        # Delta Measurement
        # -------------------------------------------------

        elif measurement.measurement_type == "delta":

            short = (

                f"{metric} "

                f"changed by "

                f"{measurement.change_value:+g}"

                f"{measurement.unit}"

            )

            executive = short + "."

        # -------------------------------------------------
        # Absolute Measurement
        # -------------------------------------------------

        else:

            short = (

                f"{metric} "

                f"reached "

                f"{measurement.numeric_value:g}"

                f"{measurement.unit}"

            )

            executive = short + "."

        # -------------------------------------------------
        # Resume Style
        # -------------------------------------------------

        resume = executive

        # -------------------------------------------------
        # LinkedIn Style
        # -------------------------------------------------

        linkedin = (

            f"Successfully {direction}d "

            f"{metric.lower()} "

            f"through data-driven decision making."

        )

        if measurement.measurement_type == "range":

            linkedin += (

                f" ({measurement.from_value:g}"

                f"{measurement.unit}"

                " → "

                f"{measurement.to_value:g}"

                f"{measurement.unit})"

            )

        # -------------------------------------------------
        # Cover Letter Style
        # -------------------------------------------------

        cover_letter = (

            f"I successfully {direction}d "

            f"{metric.lower()} "

        )

        if measurement.measurement_type == "range":

            cover_letter += (

                f"from "

                f"{measurement.from_value:g}"

                f"{measurement.unit} "

                f"to "

                f"{measurement.to_value:g}"

                f"{measurement.unit}"

            )

            if measurement.percent_change is not None:

                cover_letter += (

                    f", delivering "

                    f"a "

                    f"{measurement.percent_change:.2f}% "

                    f"improvement."

                )

        else:

            cover_letter += (

                f"to "

                f"{measurement.numeric_value:g}"

                f"{measurement.unit}."

            )

        # -------------------------------------------------

        narrative.short = short

        narrative.executive = executive

        narrative.resume = resume

        narrative.linkedin = linkedin

        narrative.cover_letter = cover_letter

        return narrative
"""
Measurement Display

Converts MeasurementKnowledge into a standardized
human-readable representation.

This module is presentation only.

No scoring.
No reasoning.

Used by

    Achievement Engine
    Resume Generator
    Cover Letter Generator
    Executive Summary
    LinkedIn Generator
"""

from dataclasses import dataclass


@dataclass
class MeasurementDisplay:

    headline: str = ""

    display: str = ""

    absolute_change: str = ""

    relative_change: str = ""

    classification: str = ""

    business_signal: str = ""

    executive_summary: str = ""

    confidence: float = 0.0


class MeasurementDisplayBuilder:

    # ---------------------------------------------------------

    def build(self, measurement):

        display = MeasurementDisplay()

        if not measurement.found:

            return display

        # -------------------------------------------------
        # Headline
        # -------------------------------------------------

        display.headline = measurement.metric

        # -------------------------------------------------
        # Display Value
        # -------------------------------------------------

        if measurement.measurement_type == "range":

            display.display = (

                f"{measurement.from_value:g}"
                f"{measurement.unit}"

                " → "

                f"{measurement.to_value:g}"
                f"{measurement.unit}"

            )

        elif measurement.measurement_type == "delta":

            display.display = (

                f"{measurement.change_value:+g}"

                f"{measurement.unit}"

            )

        else:

            display.display = (

                f"{measurement.numeric_value:g}"

                f"{measurement.unit}"

            )

        # -------------------------------------------------
        # Absolute Change
        # -------------------------------------------------

        if measurement.change_value is not None:

            if measurement.unit == "%":

                display.absolute_change = (

                    f"{measurement.change_value:+g}"

                    " percentage points"

                )

            else:

                display.absolute_change = (

                    f"{measurement.change_value:+g}"

                    f" {measurement.unit}"

                )

        # -------------------------------------------------
        # Relative Change
        # -------------------------------------------------

        if measurement.percent_change is not None:

            display.relative_change = (

                f"{measurement.percent_change:+.2f}%"

            )

        # -------------------------------------------------
        # Classification
        # -------------------------------------------------

        if measurement.percent_change is not None:

            pc = abs(measurement.percent_change)

            if pc >= 50:

                display.classification = "Exceptional Improvement"

            elif pc >= 30:

                display.classification = "Major Improvement"

            elif pc >= 15:

                display.classification = "Strong Improvement"

            elif pc >= 5:

                display.classification = "Moderate Improvement"

            else:

                display.classification = "Minor Improvement"

        else:

            display.classification = "Measured Achievement"

        # -------------------------------------------------
        # Business Signal
        # -------------------------------------------------

        weight = measurement.impact_weight

        if weight >= 1.5:

            display.business_signal = "Critical Business Impact"

        elif weight >= 1.2:

            display.business_signal = "High Business Impact"

        elif weight >= 1.0:

            display.business_signal = "Business Impact"

        else:

            display.business_signal = "Supporting KPI"

        # -------------------------------------------------
        # Executive Summary
        # -------------------------------------------------

        if measurement.measurement_type == "range":

            summary = (

                f"{measurement.metric} "

                f"{measurement.direction}d "

                f"from "

                f"{measurement.from_value:g}{measurement.unit} "

                f"to "

                f"{measurement.to_value:g}{measurement.unit}"

            )

            if measurement.percent_change is not None:

                summary += (

                    f", representing "

                    f"{measurement.percent_change:.2f}% "

                    "relative improvement."

                )

        elif measurement.measurement_type == "delta":

            summary = (

                f"{measurement.metric} "

                f"changed by "

                f"{measurement.change_value:+g}"

                f"{measurement.unit}."

            )

        else:

            summary = (

                f"{measurement.metric} "

                f"reached "

                f"{measurement.numeric_value:g}"

                f"{measurement.unit}."

            )

        display.executive_summary = summary

        # -------------------------------------------------

        display.confidence = measurement.confidence

        return display
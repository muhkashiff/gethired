"""
Magnitude Engine

Calculates HOW BIG an achievement is.

This engine only looks at measurements.

It does NOT care about business importance.

Impact Engine
    answers

        "Is Yield important?"

Magnitude Engine
    answers

        "How much was Yield improved?"
"""

from math import fabs


class MagnitudeEngine:

    def __init__(self):

        pass

    # ---------------------------------------------------------

    def score(self, graph):

        results = []

        total = 0

        for measurement in graph.measurements():

            result = self._score_measurement(measurement)

            results.append(result)

            total += result["score"]

        return {

            "score": round(total, 2),

            "count": len(results),

            "measurements": results,

        }

    # ---------------------------------------------------------

    def _score_measurement(self, measurement):

        meta = measurement.metadata

        start = self._number(meta.get("start_value"))

        end = self._number(meta.get("end_value"))

        value = self._number(meta.get("value"))

        direction = meta.get("direction", "neutral")

        # -------------------------------------------------
        # Old parser
        # -------------------------------------------------

        if start is None and end is None:

            return {

                "measurement": measurement.label,

                "score": 1,

                "classification": "Unknown",

                "change": None,

                "percent_change": None,

            }

        # -------------------------------------------------

        if start is None:

            start = value

        if end is None:

            end = value

        if start is None or end is None:

            return {

                "measurement": measurement.label,

                "score": 1,

                "classification": "Unknown",

                "change": None,

                "percent_change": None,

            }

        # -------------------------------------------------

        absolute_change = fabs(end - start)

        if start == 0:

            percent_change = 100

        else:

            percent_change = fabs(

                (end - start) / start

            ) * 100

        # -------------------------------------------------
        # Classification
        # -------------------------------------------------

        if percent_change >= 50:

            classification = "Exceptional"

            score = 10

        elif percent_change >= 30:

            classification = "Major"

            score = 8

        elif percent_change >= 15:

            classification = "Strong"

            score = 6

        elif percent_change >= 5:

            classification = "Moderate"

            score = 4

        else:

            classification = "Minor"

            score = 2

        return {

            "measurement": measurement.label,

            "start": start,

            "end": end,

            "change": round(absolute_change, 2),

            "percent_change": round(percent_change, 2),

            "classification": classification,

            "direction": direction,

            "score": score,

        }

    # ---------------------------------------------------------

    def _number(self, value):

        if value is None:

            return None

        try:

            return float(value)

        except:

            return None
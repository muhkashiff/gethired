"""
Magnitude Engine

Calculates HOW BIG an achievement is.

Uses the Measurement node stored inside the Knowledge Graph.
"""


class MagnitudeEngine:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def score(self, graph):

        results = []
        total = 0

        for measurement in graph.measurements():

            result = self._score_measurement(
                graph,
                measurement,
            )

            results.append(result)

            total += result["score"]

        return {

            "score": round(total, 2),

            "count": len(results),

            "measurements": results,

        }

    # ---------------------------------------------------------

    def _score_measurement(
        self,
        graph,
        measurement,
    ):

        meta = measurement.metadata

        # -------------------------------------------------
        # Resolve Metric from Graph
        # -------------------------------------------------

        metric_name = ""
        metric_entity = ""

        for edge in measurement.incoming_edges:

            if edge.relationship == "measured_by":

                metric_node = graph.get_node_by_entity(
                    edge.source_node
                )

                if metric_node:

                    metric_name = metric_node.canonical
                    metric_entity = metric_node.entity_id

                break

        # -------------------------------------------------
        # Read metadata
        # -------------------------------------------------

        measurement_value = meta.get(
            "value",
            measurement.label,
        )

        measurement_type = meta.get(
            "measurement_type",
            "absolute",
        )

        start = meta.get("start_value")

        end = meta.get("end_value")

        absolute_change = meta.get("change_value")

        percent_change = meta.get("percent_change")

        direction = meta.get("direction", "")

        # -------------------------------------------------
        # Absolute Measurement
        # -------------------------------------------------

        if measurement_type == "absolute":

            return {

                "metric": metric_name,
                "metric_entity": metric_entity,

                "measurement": measurement_value,

                "measurement_type": measurement_type,

                "classification": "Absolute",

                "start": None,

                "end": None,

                "change": None,

                "percent_change": None,

                "direction": direction,

                "score": 1,

            }

        # -------------------------------------------------
        # Calculate percent if missing
        # -------------------------------------------------

        if percent_change is None:

            if start is not None and end is not None:

                try:

                    absolute_change = round(
                        end - start,
                        2,
                    )

                    if start != 0:

                        percent_change = abs(
                            ((end - start) / start) * 100
                        )

                except Exception:

                    percent_change = None

        # -------------------------------------------------
        # Unknown
        # -------------------------------------------------

        if percent_change is None:

            return {

                "metric": metric_name,
                "metric_entity": metric_entity,

                "measurement": measurement_value,

                "measurement_type": measurement_type,

                "classification": "Unknown",

                "start": start,

                "end": end,

                "change": absolute_change,

                "percent_change": None,

                "direction": direction,

                "score": 1,

            }

        # -------------------------------------------------
        # Magnitude Classification
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

        # -------------------------------------------------

        return {

            "metric": metric_name,
            "metric_entity": metric_entity,

            "measurement": measurement_value,

            "measurement_type": measurement_type,

            "start": start,

            "end": end,

            "change": round(
                absolute_change,
                2,
            ) if absolute_change is not None else None,

            "percent_change": round(
                percent_change,
                2,
            ),

            "classification": classification,

            "direction": direction,

            "score": score,

        }
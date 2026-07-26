"""
Career Stability Detector

Extracts tenure information
from Experience objects.
"""


class StabilityDetector:

    def detect(self, experiences):

        durations = []

        evidence = []

        total = 0

        for exp in experiences:

            durations.append(exp.duration)

            total += exp.duration

            evidence.append(

                f"{exp.title} ({exp.duration} yrs)"

            )

        return {

            "durations": durations,

            "companies": len(experiences),

            "total_years": total,

            "evidence": evidence

        }
"""
Career Trajectory Detector
"""


class TrajectoryDetector:

    def detect(self, experiences):

        titles = []

        levels = []

        industries = []

        evidence = []

        for exp in experiences:

            titles.append(exp.title)

            levels.append(exp.seniority_level)

            industries.append(exp.industry)

            evidence.append(

                f"{exp.title} -> {exp.seniority}"

            )

        return {

            "titles": titles,

            "levels": levels,

            "industries": industries,

            "evidence": evidence

        }
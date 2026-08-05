"""
Enterprise Seniority Reasoner

Infers career seniority from graph reasoning.

Inputs
------
- DependencyReasoner
- OntologyReasoner
- LeadershipReasoner
- AchievementReasoner

Output
------
Professional
Senior Professional
Supervisor
Manager
Senior Manager
Director
Executive
"""


class SeniorityReasoner:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def analyze(

        self,

        graph,

        dependency_result,

        ontology_result,

        leadership_result,

        achievement_result,

    ):

        result = {

            "score": 0,

            "level": "",

            "evidence": [],

            "dimensions": {},

        }

        # -------------------------------------------------
        # Leadership
        # -------------------------------------------------

        leadership = leadership_result.get(

            "overall_score",

            0,

        )

        result["dimensions"]["leadership"] = leadership

        result["score"] += leadership * 0.35

        # -------------------------------------------------
        # Achievements
        # -------------------------------------------------

        achievement_score = (

            achievement_result.get(

                "achievement_count",

                0,

            )

            * 8

        )

        result["dimensions"]["achievement"] = achievement_score

        result["score"] += achievement_score * 0.25

        # -------------------------------------------------
        # Standards
        # -------------------------------------------------

        standards = len(

            ontology_result["standards"]

        )

        standard_score = standards * 8

        result["dimensions"]["standards"] = standard_score

        result["score"] += standard_score * 0.15

        # -------------------------------------------------
        # Business Breadth
        # -------------------------------------------------

        breadth = len(

            ontology_result["business_areas"]

        )

        breadth_score = breadth * 6

        result["dimensions"]["breadth"] = breadth_score

        result["score"] += breadth_score * 0.10

        # -------------------------------------------------
        # Domain Breadth
        # -------------------------------------------------

        domains = len(

            ontology_result["domains"]

        )

        domain_score = domains * 5

        result["dimensions"]["domains"] = domain_score

        result["score"] += domain_score * 0.05

        # -------------------------------------------------
        # Technical Depth
        # -------------------------------------------------

        skills = len(

            ontology_result["skills"]

        )

        methods = len(

            ontology_result["methodologies"]

        )

        technical_score = (

            skills * 3

            +

            methods * 4

        )

        result["dimensions"]["technical"] = technical_score

        result["score"] += technical_score * 0.10

        # -------------------------------------------------

        score = round(

            result["score"],

            2,

        )

        result["score"] = score

        # -------------------------------------------------
        # Seniority Classification
        # -------------------------------------------------

        if score >= 85:

            level = "Executive"

        elif score >= 70:

            level = "Director"

        elif score >= 55:

            level = "Senior Manager"

        elif score >= 40:

            level = "Manager"

        elif score >= 28:

            level = "Supervisor"

        elif score >= 15:

            level = "Senior Professional"

        else:

            level = "Professional"

        result["level"] = level

        # -------------------------------------------------
        # Explainability
        # -------------------------------------------------

        if leadership > 50:

            result["evidence"].append(

                "Strong leadership capability"

            )

        if achievement_score > 20:

            result["evidence"].append(

                "Multiple measurable achievements"

            )

        if standards > 0:

            result["evidence"].append(

                "Standards implementation experience"

            )

        if breadth > 1:

            result["evidence"].append(

                "Cross-functional business exposure"

            )

        if technical_score > 20:

            result["evidence"].append(

                "Strong technical expertise"

            )

        return result
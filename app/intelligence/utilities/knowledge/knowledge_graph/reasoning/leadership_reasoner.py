"""
Enterprise Leadership Reasoner

Purpose
-------
Infers leadership capability from:

- Actions
- Domains
- Standards
- Achievements
- Improvements
- Dependencies

Does NOT score.

Returns structured leadership evidence.
"""

from dataclasses import dataclass, field


# =====================================================
# LEADERSHIP EVIDENCE
# =====================================================

@dataclass
class LeadershipEvidence:

    category: str = ""

    source: str = ""

    strength: float = 0.0

    confidence: float = 0.0

    evidence: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)


# =====================================================
# REASONER
# =====================================================

class LeadershipReasoner:

    def __init__(self):

        self.people_actions = {

            "lead",
            "manage",
            "mentor",
            "coach",
            "train",
            "supervise",
            "guide",
            "develop",

        }

        self.change_actions = {

            "implement",
            "improve",
            "optimize",
            "transform",
            "establish",

        }

        self.operational_actions = {

            "coordinate",
            "control",
            "direct",
            "manage",

        }

    # ----------------------------------------------------

    def analyze(

        self,

        graph,

        dependency_result,

        ontology_result,

    ):

        result = {

            "people_leadership": LeadershipEvidence(),

            "change_leadership": LeadershipEvidence(),

            "operational_leadership": LeadershipEvidence(),

            "technical_leadership": LeadershipEvidence(),

            "strategic_leadership": LeadershipEvidence(),

            "overall_confidence": 0.0,

        }

        actions = ontology_result["actions"]

        standards = ontology_result["standards"]

        skills = ontology_result["skills"]

        # =================================================
        # PEOPLE LEADERSHIP
        # =================================================

        people_evidence = []

        for action in actions:

            if action.label.lower() in self.people_actions:

                people_evidence.append(

                    action.label

                )

        result["people_leadership"] = LeadershipEvidence(

            category="people",

            source="actions",

            strength=min(

                len(people_evidence) * 15,

                100,

            ),

            confidence=0.90,

            evidence=people_evidence,

        )

        # =================================================
        # CHANGE LEADERSHIP
        # =================================================

        change_evidence = []

        for action in actions:

            if action.label.lower() in self.change_actions:

                change_evidence.append(

                    action.label

                )

        for standard in standards:

            change_evidence.append(

                standard.label

            )

        result["change_leadership"] = LeadershipEvidence(

            category="change",

            source="actions+standards",

            strength=min(

                len(change_evidence) * 12,

                100,

            ),

            confidence=0.90,

            evidence=change_evidence,

        )

        # =================================================
        # OPERATIONAL LEADERSHIP
        # =================================================

        operational = []

        for action in actions:

            if action.label.lower() in self.operational_actions:

                operational.append(

                    action.label

                )

        result["operational_leadership"] = LeadershipEvidence(

            category="operations",

            source="actions",

            strength=min(

                len(operational) * 10,

                100,

            ),

            confidence=0.85,

            evidence=operational,

        )

        # =================================================
        # TECHNICAL LEADERSHIP
        # =================================================

        technical = []

        for skill in skills:

            technical.append(

                skill.label

            )

        result["technical_leadership"] = LeadershipEvidence(

            category="technical",

            source="skills",

            strength=min(

                len(technical) * 5,

                100,

            ),

            confidence=0.85,

            evidence=technical,

        )

        # =================================================
        # STRATEGIC LEADERSHIP
        # =================================================

        strategic = []

        if standards:

            strategic.extend(

                [s.label for s in standards]

            )

        result["strategic_leadership"] = LeadershipEvidence(

            category="strategy",

            source="standards",

            strength=min(

                len(strategic) * 20,

                100,

            ),

            confidence=0.80,

            evidence=strategic,

        )

        # =================================================
        # OVERALL
        # =================================================

        scores = [

            result["people_leadership"].strength,

            result["change_leadership"].strength,

            result["operational_leadership"].strength,

            result["technical_leadership"].strength,

            result["strategic_leadership"].strength,

        ]

        result["overall_score"] = round(

            sum(scores) / len(scores),

            2,

        )

        result["overall_confidence"] = 0.90

        return result
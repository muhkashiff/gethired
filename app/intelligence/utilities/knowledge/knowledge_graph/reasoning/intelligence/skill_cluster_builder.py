"""
Enterprise Skill Cluster Builder

Groups ontology skills into enterprise capability clusters.

Example

Python
Pandas
NumPy

↓

Machine Learning

-------------------

HACCP
GMP
FSSC22000

↓

Food Safety
"""

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.intelligence.skill_taxonomy import (
    SkillTaxonomy,
)

from app.intelligence.utilities.knowledge.knowledge_graph.reasoning.models.skill_models import (
    SkillCluster,
    SkillEvidence,
)


class SkillClusterBuilder:

    def __init__(self):

        self.taxonomy = SkillTaxonomy()

    # ---------------------------------------------------------

    def build(self, skills):

        """
        Build enterprise capability clusters.
        """

        grouped = self.taxonomy.build_clusters(skills)

        clusters = []

        for cluster_name, cluster_skills in grouped.items():

            cluster = SkillCluster(

                name=cluster_name,

                category=self.taxonomy.get_cluster_category(cluster_name),

                confidence=self._cluster_confidence(cluster_skills),

                score=0.0,  # populated later

            )

            for skill in cluster_skills:

                evidence = SkillEvidence(

                    skill=skill,

                    confidence=getattr(
                        skill,
                        "confidence",
                        1.0,
                    ),

                    business_area=getattr(
                        skill,
                        "business_area",
                        "",
                    ),

                    domain=getattr(
                        skill,
                        "domain",
                        "",
                    ),

                    category=getattr(
                        skill,
                        "category",
                        "",
                    ),

                    impact_weight=getattr(
                        skill,
                        "impact_weight",
                        1.0,
                    ),

                )

                cluster.skills.append(evidence)

            clusters.append(cluster)

        clusters.sort(

            key=lambda c: len(c.skills),

            reverse=True,

        )

        return clusters

    # ---------------------------------------------------------

    def _cluster_confidence(self, skills):

        """
        Average confidence for cluster.
        """

        if not skills:

            return 0.0

        values = [

            getattr(skill, "confidence", 1.0)

            for skill in skills

        ]

        return round(

            sum(values) / len(values),

            2,

        )
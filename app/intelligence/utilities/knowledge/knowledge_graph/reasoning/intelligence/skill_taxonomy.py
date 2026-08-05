"""
Enterprise Skill Taxonomy

Maps ontology skills into enterprise capability clusters.

This is NOT scoring.

It is the enterprise knowledge base that allows reasoning over
skills instead of matching isolated keywords.

Examples

Python
Pandas
NumPy

↓

Machine Learning

-----------------------

FSSC22000
HACCP
GMP

↓

Food Safety Management
"""

from collections import defaultdict


class SkillTaxonomy:

    """
    Enterprise Skill Taxonomy

    Converts ontology skill IDs into higher-level capability clusters.
    """

    def __init__(self):

        # --------------------------------------------------
        # Technical Capability Clusters
        # --------------------------------------------------

        self.capability_map = {

            # ---------------------------
            # Machine Learning
            # ---------------------------

            "SKILL_PYTHON": "Machine Learning",

            "SKILL_PANDAS": "Machine Learning",

            "SKILL_NUMPY": "Machine Learning",

            "SKILL_SCIKIT_LEARN": "Machine Learning",

            "SKILL_TENSORFLOW": "Machine Learning",

            "SKILL_PYTORCH": "Machine Learning",

            "SKILL_XGBOOST": "Machine Learning",

            "SKILL_STATISTICS": "Machine Learning",

            # ---------------------------
            # Data Analytics
            # ---------------------------

            "SKILL_SQL": "Data Analytics",

            "SKILL_POWER_BI": "Data Analytics",

            "SKILL_TABLEAU": "Data Analytics",

            "SKILL_EXCEL": "Data Analytics",

            "SKILL_DATA_ANALYSIS": "Data Analytics",

            # ---------------------------
            # Cloud
            # ---------------------------

            "SKILL_AZURE": "Cloud Engineering",

            "SKILL_AWS": "Cloud Engineering",

            "SKILL_GCP": "Cloud Engineering",

            "SKILL_DOCKER": "Cloud Engineering",

            "SKILL_KUBERNETES": "Cloud Engineering",

            # ---------------------------
            # Backend
            # ---------------------------

            "SKILL_FLASK": "Backend Development",

            "SKILL_FASTAPI": "Backend Development",

            "SKILL_DJANGO": "Backend Development",

            "SKILL_API": "Backend Development",

            # ---------------------------
            # Food Safety
            # ---------------------------

            "SKILL_HACCP": "Food Safety",

            "SKILL_GMP": "Food Safety",

            "SKILL_FSSC22000": "Food Safety",

            "SKILL_BRCGS": "Food Safety",

            "SKILL_PCQI": "Food Safety",

            # ---------------------------
            # Quality
            # ---------------------------

            "SKILL_ROOT_CAUSE_ANALYSIS": "Quality Management",

            "SKILL_CAPA": "Quality Management",

            "SKILL_AUDITING": "Quality Management",

            "SKILL_QMS": "Quality Management",

            "SKILL_ISO9001": "Quality Management",

            # ---------------------------
            # Lean
            # ---------------------------

            "SKILL_LEAN": "Operational Excellence",

            "SKILL_SIX_SIGMA": "Operational Excellence",

            "SKILL_KAIZEN": "Operational Excellence",

            "SKILL_5S": "Operational Excellence",

            # ---------------------------
            # Leadership
            # ---------------------------

            "SKILL_TEAM_MANAGEMENT": "Leadership",

            "SKILL_PEOPLE_MANAGEMENT": "Leadership",

            "SKILL_TRAINING": "Leadership",

            "SKILL_COACHING": "Leadership",

            "SKILL_PROJECT_MANAGEMENT": "Leadership",

        }

    # --------------------------------------------------

    def get_cluster(self, skill_id: str):

        """
        Returns enterprise capability cluster.
        """

        return self.capability_map.get(
            skill_id,
            "General",
        )

    # --------------------------------------------------

    def build_clusters(self, skills):

        """
        Groups ontology skills into enterprise capability clusters.
        """

        clusters = defaultdict(list)

        for skill in skills:

            cluster = self.get_cluster(
                skill.entity_id
            )

            clusters[cluster].append(skill)

        return dict(clusters)

    # --------------------------------------------------

    def get_cluster_counts(self, skills):

        """
        Returns

        {
            Machine Learning : 6,
            Food Safety : 4,
            Leadership : 3
        }
        """

        clusters = self.build_clusters(skills)

        return {

            cluster: len(items)

            for cluster, items in clusters.items()

        }

    # --------------------------------------------------

    def get_primary_cluster(self, skills):

        counts = self.get_cluster_counts(skills)

        if not counts:

            return None

        return max(

            counts,

            key=counts.get,

        )
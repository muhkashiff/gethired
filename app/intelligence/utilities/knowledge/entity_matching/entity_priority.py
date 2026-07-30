"""
Priority rules when multiple entities overlap.
"""


class EntityPriority:

    PRIORITY = {

        "standard": 100,

        "technology": 95,

        "methodology": 90,

        "kpi": 85,

        "metric": 80,

        "object": 70,

        "action": 60,

        "domain": 50,

        "skill": 40,

        "methodology": 85,

    }

    @classmethod
    def get(cls, entity_type):

        return cls.PRIORITY.get(entity_type, 0)
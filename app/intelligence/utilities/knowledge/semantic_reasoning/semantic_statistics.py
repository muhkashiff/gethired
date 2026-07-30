"""
Semantic Statistics

Creates semantic statistics after semantic resolution.
"""


class SemanticStatistics:

    def build(self, resolution):

        stats = {

            "entities": len(resolution.entities),

            "dependencies": len(resolution.dependencies),

            "clusters": len(resolution.clusters),

            "actions": 0,

            "objects": 0,

            "domains": 0,

            "metrics": 0,

            "measurements": 0,

            "methodologies": 0,

            "standards": 0,

        }

        for entity in resolution.entities:

            t = entity.entity_type.lower()

            if t == "action":
                stats["actions"] += 1

            elif t == "object":
                stats["objects"] += 1

            elif t == "domain":
                stats["domains"] += 1

            elif t == "metric":
                stats["metrics"] += 1

            elif t == "measurement":
                stats["measurements"] += 1

            elif t == "methodology":
                stats["methodologies"] += 1

            elif t == "standard":
                stats["standards"] += 1

        return stats